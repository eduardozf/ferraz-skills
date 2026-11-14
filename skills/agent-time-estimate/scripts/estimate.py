#!/usr/bin/env python3
"""Convert estimated tool calls into wall-clock time for a coding agent, using measured calibration.

Calibration lookup order: $AGENT_TIME_CALIBRATION, ~/.config/agent-time-bench/calibration.json,
then calibration.default.json next to this script.

Example:
  estimate.py --tool-calls 8,20,45 --model claude-opus-5-5 --checkpoints 2
"""
import argparse
import json
import math
import os
import random
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLES = 20000
Z90 = st.NormalDist().inv_cdf(0.9)


def load_calibration():
    paths = [os.environ.get('AGENT_TIME_CALIBRATION'),
             os.path.expanduser('~/.config/agent-time-bench/calibration.json'),
             os.path.join(HERE, 'calibration.default.json')]
    for p in paths:
        if p and os.path.exists(p):
            with open(p) as f:
                cal = json.load(f)
            if cal.get('schema') != 1:
                sys.exit(f'{p}: unsupported calibration schema {cal.get("schema")}')
            return p, cal
    sys.exit('no calibration file found')


def parse_tool_calls(s):
    try:
        v = [float(x) for x in s.split(',')]
    except ValueError:
        sys.exit('--tool-calls takes one number or P10,P50,P90, such as 8,20,45')
    if len(v) == 1:
        v = [v[0] / 2.5, v[0], v[0] * 2.5]
    if len(v) != 3 or not (0 <= v[0] <= v[1] <= v[2]):
        sys.exit('--tool-calls needs P10 <= P50 <= P90, all >= 0')
    return v


def from_quantiles(q, rng):
    """Sample from a distribution given as 21 evenly spaced quantiles."""
    u = rng.random() * (len(q) - 1)
    i = int(u)
    j = min(i + 1, len(q) - 1)
    return q[i] + (q[j] - q[i]) * (u - i)


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--tool-calls', required=True, help='P10,P50,P90 tool calls for the first run, or one P50 value')
    ap.add_argument('--model', help='model that will do the work, such as claude-opus-5-5')
    ap.add_argument('--estimator', help='model and effort making this estimate, such as gpt-6-luna:low')
    ap.add_argument('--checkpoints', type=float, help='times the user reviews or answers before the work is done '
                                                      '(default: the measured median follow-ups)')
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()

    path, cal = load_calibration()
    p10, p50, p90 = parse_tool_calls(a.tool_calls)
    curve = cal.get('models', {}).get(a.model) or cal['pooled']
    curve_name = a.model if a.model in cal.get('models', {}) else 'pooled'
    est = cal.get('estimators', {}).get(a.estimator) or cal.get('default_estimator') or {}
    bias = est.get('tool_call_bias', 1.0)
    widen = est.get('interval_widen', 1.0)
    checkpoints = a.checkpoints if a.checkpoints is not None else (cal.get('followups_p50') or 0)

    # Estimators undercount tool calls and give ranges that are too narrow; both corrections come from evals.
    mu = math.log((p50 + 1) / bias)
    sigma = max((math.log(p90 + 1) - math.log(p10 + 1)) / (2 * Z90), 0.05) * widen
    rng = random.Random(1)
    first, review, followup = [], [], []
    whole = int(checkpoints)
    frac = checkpoints - whole
    for _ in range(SAMPLES):
        n1 = math.exp(rng.gauss(mu, sigma))   # tool calls + 1
        first.append(10 ** (curve['a'] + curve['b'] * math.log10(n1) + from_quantiles(curve['resid_q'], rng)))
        k = whole + (1 if rng.random() < frac else 0)
        review.append(sum(from_quantiles(cal['review_gap_s_q'], rng) for _ in range(k)))
        followup.append(sum(from_quantiles(cal['followup_run_s_q'], rng) for _ in range(k)))
    total = [f + r + u for f, r, u in zip(first, review, followup)]

    def summary(xs):
        return {p: round(pct(xs, q) / 60, 1) for p, q in (('p10', .1), ('p50', .5), ('p80', .8), ('p90', .9))}

    out = dict(first_run_agent_min=summary(first), followup_agent_min=summary(followup),
               user_review_min=summary(review), total_min=summary(total),
               inputs=dict(tool_calls=[p10, p50, p90], checkpoints=checkpoints, curve=curve_name,
                           tool_call_bias=bias, interval_widen=widen),
               calibration=dict(path=path, generated_at=cal.get('generated_at')))
    if a.json:
        print(json.dumps(out, indent=1))
        return
    print(f'calibration: {path} ({cal.get("generated_at")}), curve: {curve_name}, checkpoints: {checkpoints:g}')
    print(f'{"":24s}{"P10":>7s}{"P50":>7s}{"P80":>7s}{"P90":>7s}  (minutes)')
    for label, key in (('agent, first run', 'first_run_agent_min'), ('agent, follow-ups', 'followup_agent_min'),
                       ('user review', 'user_review_min'), ('total', 'total_min')):
        s = out[key]
        print(f'{label:24s}{s["p10"]:7.1f}{s["p50"]:7.1f}{s["p80"]:7.1f}{s["p90"]:7.1f}')


if __name__ == '__main__':
    main()
