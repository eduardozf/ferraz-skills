---
name: agent-time-estimate
description: >-
  Estimate how long a coding agent will take on a task, in wall-clock minutes
  measured from the user's real agent runs, plus the time the user spends
  reviewing. Converts estimated tool calls into time with a bundled script
  instead of guessing in human time. Use when the user asks "how long will this
  take", "quanto tempo vai levar", "estima o tempo", "time estimate", "ETA", or
  /agent-time-estimate, or when a plan or reply would state a duration for agent
  work. Not for estimating work a human team will do by hand, or for measuring
  how long a past run took, which the run's timestamps answer.
---

# Agent time estimate

Estimate agent work by counting tool calls and converting them with `scripts/estimate.py`. Do not state a duration from intuition: raw estimates in human time or in "agent minutes" ran 8 to 12 times too long against the user's measured runs, while tool-call counts converted through the calibration landed within about 2 times.

## Estimate

1. Define the unit. Estimate the run the user will wait on, from sending the message until the agent hands back. If the work needs several runs, such as plan then implement, estimate each run and add them.
2. List the steps the agent will take: reading and searching, edits, commands, checks and web lookups. Count one tool call per command, search, file edit or fetch. Add a fix loop for each check that may fail. Give a P10, P50 and P90 total.
3. Compare your P50 with these medians from real first runs before you settle it. Estimators undercount by about 20%, mostly by skipping exploration and verification.

   | Task kind | Tool calls, P25 / P50 / P75 | Real minutes, P50 |
   |---|---|---|
   | Question answered from context | 3 / 5 / 9 | 0.6 |
   | Ops or machine setup | 8 / 12 / 36 | 2 |
   | Research or reading code | 8 / 15 / 42 | 3 |
   | Small change | 9 / 21 / 53 | 2 |
   | Debugging | 12 / 28 / 48 | 4 |
   | UI design work | 36 / 56 / 73 | 10 |
   | Feature | 45 / 85 / 124 | 20 |

4. Count checkpoints: each time the user must answer, approve, test or review before the work is done. Plan mode adds one. If the user asks when they will get a first answer or result, pass `--checkpoints 0`. If you cannot tell, omit `--checkpoints` and the script uses the measured median.
5. Run the script:

   ```sh
   python3 scripts/estimate.py --tool-calls P10,P50,P90 --model <model that will do the work> --estimator <your model:effort> [--checkpoints N]
   ```

   The script applies the estimator's measured bias, widens your range to the measured coverage, and simulates agent time, follow-up runs and user review. Pass `--json` when another tool consumes the output. It exits with code 1 and a message when the tool-call range is invalid.

## Report

Lead with the P50 and P80 total, then split it into agent time and the user's review time. State the tool-call range it rests on. Use P80 when the user is planning around the result.

If the output names `calibration.default.json`, say the estimate uses generic calibration. The user's own calibration comes from `atb.py calibrate` in their `agent-time-bench` checkout, which installs `~/.config/agent-time-bench/calibration.json`.

Return the estimate table, the tool-call range and checkpoint count you used, and the calibration path the script printed.
