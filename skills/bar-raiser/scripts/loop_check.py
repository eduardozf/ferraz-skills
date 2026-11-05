#!/usr/bin/env python3
"""Mechanical checks for the bar-raiser loop.

leaks:  print each hit in the brief, the task title, and the share folder's
        file names and text contents: the target number, a score out of 10, a
        round number, or a mention of an earlier round, score or review. Exit 0 with no hits, 1 with hits, 2 on bad input or a file error.
scores: read the score log, print the target, the table of rounds, the paused
        reviewers, the reviewers for the next round and the stop decision.
        Exit 0 for any valid log, 2 on bad input or a file error.
"""
import argparse
import math
import re
import sys
from pathlib import Path

MAX_TEXT_BYTES = 1_000_000
PAUSE_AFTER = 2  # equal scores in a row before a reviewer above another is paused
NUMBER = r"\d+(?:\.\d+)?"

# The brief must say "a score from 0 to 10" and "Score: N/10"; those two phrases are not hits.
SCALE = re.compile(r"\b0\s+to\s+10\b|\bN\s*/\s*10\b")
# A numbered brief starts lines with "9. "; the list number is not a hit.
LIST_MARKER = re.compile(r"^\s*(?:\d+|[A-Za-z])[.)]\s+")


class InputError(Exception):
    pass


def format_number(value):
    return str(int(value)) if float(value).is_integer() else str(value)


def target_value(text):
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{text!r} is not a number")
    if not math.isfinite(value) or not 0 <= value <= 10:
        raise argparse.ArgumentTypeError(f"{text} is outside 0 to 10")
    return value


# Leak check ----------------------------------------------------------------

def leak_patterns(target):
    """Return (kind, pattern, sees_scale) for the four high-confidence leak forms.

    sees_scale keeps "/10" in the checked text. Anything else, such as a score in
    words or a reviewer's opinion, is left to the agent's own reading.
    """
    number = re.escape(format_number(target)) + (r"(?:\.0+)?" if float(target).is_integer() else "0*")
    patterns = [
        ("target number", rf"(?<![\w.]){number}(?![\w]|\.\d)", False),
        ("score", rf"\b{NUMBER}\s*(?:/|out\s+of)\s*10\b", True),
        ("round", r"\bround[\s_-]*#?\d+", False),
        ("earlier round or review", r"\b(?:earlier|previous|prior|last)[\s_-]+(?:rounds?|scores?|reviews?|reviewers?)\b", False),
    ]
    return [(kind, re.compile(pattern, re.I), sees_scale) for kind, pattern, sees_scale in patterns]


def find_leaks(source, text, patterns, numbered=False):
    hits = []
    for number, line in enumerate(text.splitlines(), 1):
        body = LIST_MARKER.sub("", line) if numbered else line
        without_scale = SCALE.sub(" ", body)
        kinds = []
        for kind, pattern, sees_scale in patterns:
            if kind not in kinds and pattern.search(body if sees_scale else without_scale):
                kinds.append(kind)
        hits += [f"{source}:{number}: [{kind}] {line.strip()}" for kind in kinds]
    return hits


def read_text_file(path):
    """Return the file's text, or None for a binary or oversized file."""
    if path.stat().st_size > MAX_TEXT_BYTES:
        return None
    data = path.read_bytes()
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def run_leaks(args):
    patterns = leak_patterns(args.target)
    brief = Path(args.brief)
    hits = find_leaks(str(brief), brief.read_text(), patterns, numbered=True)
    hits += find_leaks("title", args.title, patterns)
    skipped = []
    root = Path(args.share)
    if not root.is_dir():
        raise InputError(f"{root}: not a folder")
    paths = sorted(root.rglob("*"))
    names = "\n".join(str(p.relative_to(root)) for p in paths)
    hits += find_leaks(f"{root} (file names)", names, patterns)
    for path in paths:
        if path.is_file():
            text = read_text_file(path)
            if text is None:
                skipped.append(str(path.relative_to(root)))
            else:
                hits += find_leaks(str(path), text, patterns)
    for hit in hits:
        print(hit)
    if skipped:
        print("not scanned (binary or over 1 MB), check by eye:", ", ".join(skipped))
    if not hits:
        print("no hits")
    return 1 if hits else 0


# Score check ---------------------------------------------------------------

def parse_score(text, where):
    text = text.strip()
    if text.endswith("/10"):
        text = text[:-3].strip()
    try:
        score = float(text)
    except ValueError:
        raise InputError(f"{where}: the score must be a number such as 9 or 9.5")
    if not math.isfinite(score) or not 0 <= score <= 10:
        raise InputError(f"{where}: the score must be from 0 to 10")
    return score


def read_scores(path):
    """Return (rounds, rosters, void, final roster). Names are compared in lower case."""
    rounds, rosters, void = {}, {}, set()
    roster = None
    for number, raw in enumerate(Path(path).read_text().splitlines(), 1):
        where = f"{path}:{number}"
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [part.strip() for part in line.split("\t")]
        kind = parts[0].lower()
        if kind == "roster" and len(parts) == 2:
            roster = {name.strip().lower() for name in parts[1].split(",") if name.strip()}
            if not roster:
                raise InputError(f"{where}: the roster names no reviewer")
            continue
        if kind == "void" and len(parts) == 2 and parts[1].isdigit():
            void.add(int(parts[1]))
            continue
        if len(parts) != 3 or not parts[0].isdigit():
            raise InputError(f"{where}: expected 'roster<TAB>a,b,c', 'void<TAB>N' "
                             f"or 'N<TAB>reviewer<TAB>score', got {line!r}")
        if roster is None:
            raise InputError(f"{where}: add a roster line before the first score")
        round_number, reviewer = int(parts[0]), parts[1].lower()
        if round_number in void:
            raise InputError(f"{where}: round {round_number} is void; give a fresh round the next number")
        rosters.setdefault(round_number, roster)
        if reviewer not in rosters[round_number]:
            raise InputError(f"{where}: {parts[1]} is not in the roster for round {round_number}; "
                             "void the round and start a fresh one after the new roster line")
        scores = rounds.setdefault(round_number, {})
        if reviewer in scores:
            raise InputError(f"{where}: a second score for {parts[1]} in round {round_number}")
        scores[reviewer] = parse_score(parts[2], where)
    if not rounds:
        raise InputError(f"{path}: no scores")
    return rounds, rosters, void, roster


def mean(scores):
    return round(sum(scores.values()) / len(scores), 6)


class Result:
    def __init__(self):
        self.decision = None
        self.notes = []
        self.held = {}          # paused reviewer -> carried score, going into the next round
        self.effective = {}     # counted round -> scores, carried ones included
        self.carried = {}       # counted round -> reviewers whose score was carried
        self.next_round = []


def analyze(rounds, rosters, void, target, final_roster):
    """Apply the pause, progress and stop rules to the counted rounds."""
    result = Result()
    live = [r for r in sorted(rounds) if r not in void]
    held, history, counted, skipped = {}, {}, [], []
    for r in live:
        roster = rosters[r]
        actual = rounds[r]
        held = {n: s for n, s in held.items() if n in roster and n not in actual}
        missing = sorted(roster - set(actual) - set(held))
        if missing:
            if r == live[-1]:
                result.decision = f"incomplete: round {r} has no score from {', '.join(missing)}"
                return result
            skipped.append(r)
            continue
        eff = {**held, **actual}
        result.effective[r], result.carried[r] = eff, set(held)
        counted.append(r)
        for name, score in actual.items():
            history.setdefault(name, []).append(score)
        if all(score >= target for score in eff.values()):
            held = {}
            continue
        held = {n: s for n, s in held.items() if not all(eff[o] >= s for o in eff if o != n)}
        for name, score in actual.items():
            recent = history[name][-PAUSE_AFTER:]
            if len(recent) == PAUSE_AFTER and len(set(recent)) == 1 and any(eff[o] < score for o in eff if o != name):
                held[name] = score
    if skipped:
        result.notes.append("Not counted, incomplete: round " + ", ".join(map(str, skipped)))
    if void:
        result.notes.append("Not counted, void: round " + ", ".join(map(str, sorted(void))))
    if not counted:
        result.decision = "continue: every logged round is void"
        result.next_round = sorted(final_roster)
        return result
    latest = counted[-1]
    if len(counted) > 1:
        before, now = result.effective[counted[-2]], rounds[latest]
        drops = [f"{name} {format_number(before[name])} -> {format_number(now[name])}"
                 for name in sorted(now) if name in before and now[name] < before[name]]
        if drops:
            result.notes.append("Dropped since the previous counted round: " + ", ".join(drops))
    result.held = {n: s for n, s in held.items() if n in final_roster}
    result.next_round = sorted(final_roster - set(result.held))
    if rosters[latest] != final_roster:
        result.decision = f"continue: the roster changed after round {latest}; run a round with the new roster"
        return result
    eff = result.effective[latest]
    if all(score >= target for score in eff.values()):
        if result.carried[latest]:
            result.decision = "continue: every reviewer reviews the next round to confirm the target"
        else:
            result.decision = "target reached"
            result.next_round = []
        return result
    segment, segments = 0, []
    for index, r in enumerate(counted):
        if index and rosters[r] != rosters[counted[index - 1]]:
            segment += 1
        segments.append(segment)
    stalled = 0
    for index in range(1, len(counted)):
        same_roster = [r for r, seg in zip(counted[:index], segments) if seg == segments[index]]
        if not same_roster:
            stalled = 0
            continue
        earlier = [result.effective[r] for r in same_roster]
        current = result.effective[counted[index]]
        progress = (min(current.values()) > max(min(s.values()) for s in earlier)
                    or mean(current) > max(mean(s) for s in earlier))
        stalled = 0 if progress else stalled + 1
    if stalled >= 3:
        result.decision = f"ask the user: no progress for {stalled} rounds"
    elif stalled == 2:
        result.decision = "change the approach: no progress for 2 rounds"
    else:
        result.decision = "continue"
    return result


def table(rounds, rosters, void, result):
    reviewers = []
    for r in sorted(rounds):
        reviewers += [name for name in sorted(rosters[r]) if name in rounds[r] and name not in reviewers]
    lines = ["| Round | " + " | ".join(reviewers) + " | Lowest | Mean |",
             "|---" * (len(reviewers) + 3) + "|"]
    for r in sorted(rounds):
        scores = result.effective.get(r, rounds[r])
        carried = result.carried.get(r, set())
        cells = [(f"({format_number(scores[n])})" if n in carried else format_number(scores[n]))
                 if n in scores else "-" for n in reviewers]
        label = str(r)
        if r in void:
            label += " (void)"
        elif r not in result.effective:
            label += " (incomplete)"
        lines.append(f"| {label} | " + " | ".join(cells) +
                     f" | {format_number(min(scores.values()))} | {format_number(round(mean(scores), 2))} |")
    if any(result.carried.values()):
        lines += ["", "A score in parentheses was carried from a paused reviewer's last round."]
    return "\n".join(lines)


def run_scores(args):
    rounds, rosters, void, final_roster = read_scores(args.log)
    result = analyze(rounds, rosters, void, args.target, final_roster)
    print(f"Target: {format_number(args.target)}")
    print(table(rounds, rosters, void, result))
    print()
    for note in result.notes:
        print(note)
    for name, score in sorted(result.held.items()):
        print(f"Paused: {name} at {format_number(score)}, until every other reviewer reaches "
              f"{format_number(score)} or every score reaches the target")
    if result.next_round:
        print("Next round: " + ", ".join(result.next_round))
    print("Decision:", result.decision)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)

    leaks = commands.add_parser("leaks", help="print each hit that can reveal the target, a score or the round")
    leaks.add_argument("--target", type=target_value, required=True)
    leaks.add_argument("--title", required=True, help="the delegate_task title")
    leaks.add_argument("brief")
    leaks.add_argument("share", help="the share folder: the evidence and any work copy")
    leaks.set_defaults(run=run_leaks)

    scores = commands.add_parser("scores", help="print the score table and the stop decision")
    scores.add_argument("--target", type=target_value, required=True)
    scores.add_argument("log", help="tab-separated: roster, void and score lines")
    scores.set_defaults(run=run_scores)

    args = parser.parse_args()
    try:
        return args.run(args)
    except (InputError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
