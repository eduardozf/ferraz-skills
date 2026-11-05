---
name: bar-raiser
description: >-
  Improve a piece of work in rounds until independent reviewer agents each
  score it at or above a target the user sets, keeping the target, earlier
  scores and round count hidden from the reviewers. Use when the user says
  "bar-raiser", /bar-raiser, "run the reviewer loop", "review until it scores
  9", "loop until both reviewers give 9/10", "até os revisores darem nota 9",
  or otherwise gives a target score for subagent reviews. Not for a single
  review or second opinion with no target score, or a code review of a PR or
  diff.
---

# Bar raiser

Run rounds of blind, scored reviews and revise the work between rounds. Stop when every reviewer reaches the target in the same round, or when the scores plateau and the user decides.

## Set up the loop

Record these before the first round:

- **Target:** the overall score from 0 to 10 that every reviewer must reach, such as 9. If the user gave none, ask for it once.
- **Reviewers:** the models and effort the user named. Otherwise use two reviewers at xhigh reasoning effort: GPT-6.1 Sol (`gpt-6.1-sol`) and Claude Opus 5.5 (`claude-opus-5-5`). Different model families have different blind spots.
- **Request:** the user's request in their own words, plus any standard they judge by.
- **Evidence:** what the reviewers inspect to judge the result, not only its source. For a UI, give screenshots of the running app. For code, give the files plus a command or test output that shows the behavior.
- **Score log:** where you record each round's scores. Use the project's status or history log if it keeps one. Otherwise use a file in your scratch directory.

Start the reviewers through the T3 Code orchestrator. Call `orchestrator_capabilities` once, then call `delegate_task` for each reviewer with `role: "review"` and `mode: "async"`. Set the effort explicitly, because both models default lower:

- GPT-6.1 Sol: `target: {providerInstanceId: "codex", model: "gpt-6.1-sol", options: [{id: "reasoningEffort", value: "xhigh"}]}`.
- Opus 5.5: `target: {providerInstanceId: "claudeAgent", model: "claude-opus-5-5", options: [{id: "effort", value: "xhigh"}]}`.

For another model, take its provider and option names from `orchestrator_capabilities`.

If a requested or default model is unavailable, tell the user and ask which to use. Do not substitute another model or a lower effort on your own.

## Keep the context clean

Load the `context-pollution` skill before writing the brief, and follow it for the whole loop. Each reviewer starts with only the brief, so whatever the brief carries shapes the score. Your own context fills with long reviews, so keep the conclusions and the checked facts, and leave the review text in the task results.

## Write the brief once

Save the brief to a file and reuse it every round. Write it in this order:

1. One line: "Review <the work> and score it."
2. The user's request in their words, and the standard they judge by.
3. What was built and where: identifiers, file paths, and any generator or builder that produces it.
4. The evidence folder.
5. The source and documentation of any app or platform involved.
6. Reference data the reviewers need, such as schemas or inventories.
7. **Verified facts:** platform limits and deliberate decisions, each checked by you, so the reviewers do not re-suggest impossible or excluded changes.
8. "Review only: do not edit files, change live systems, or submit forms."
9. "Score the work from 0 to 10 for how well it meets the request with the tools and platform as they are today. Then give a prioritized list of concrete improvements. List changes that need the platform, outside systems or the user's decision separately."

Keep the brief free of anything that steers the result:

- Never state the target, an earlier score, the round number, or what an earlier reviewer said. This includes task titles, folder names and file names the reviewer can see.
- Leave out your hypotheses and your own assessment.
- Between rounds, change only the verified facts you add. Point the brief at one evidence folder with a neutral name, such as `review-evidence/`, and refill it each round.
- Do not point the reviewers at the score log or at files that contain earlier reviews.

## Run a round

1. Apply the round's fixes and confirm they are live or built.
2. Delete everything in the evidence folder. Then capture fresh evidence of the current state, with file names that say what each one shows. An image of an older state makes the reviewer judge work that no longer exists.
3. Start every reviewer in the same turn, each as a new task. Never send a follow-up message to an earlier reviewer, because it would carry its earlier round.
4. Wait for every reviewer to finish before revising. Rely on the completion notice; do not poll.
5. Record each reviewer's score in the score log, with the date and the main changes behind it.

## Act on the feedback

- Merge the reviews. Do first what both reviewers raise and what blocks the request.
- Before acting on a factual claim about the app, platform or data, check it against the source or the live state. Reviewers state false limits and bugs with confidence.
- When a reviewer suggests something impossible or deliberately excluded, add the checked fact to the verified facts. Do not add their opinion.
- Make the fixes within the work yourself. When a fix needs the user's approval, such as changing live data, deleting something, or touching an outside system, gather those fixes into one question for the round. Give the reviewer's reason and your recommendation for each. Continue with the other fixes meanwhile.
- When a later round reverses advice you already applied, keep the version that better serves the user's request. Note the reversal for the plateau check.

## Stop

- **Target reached:** every reviewer scores at or above the target in the same round. Stop and report.
- **Plateau:** stop and ask the user how to proceed when all three conditions hold:
  - the scores have stalled for about three rounds;
  - the advice contradicts earlier rounds;
  - the remaining points need changes outside the work.
  Give the scores, the remaining gaps and the options: one more round, accept the current state, or approve the outside changes.
- **After stopping:** if the last round found real defects, fix them without another round and say they were not reviewed again.

## Deliver

Report:

- a table of every round's score per reviewer, and why the loop stopped;
- the main changes per round;
- reviewer claims you checked and found false;
- suggestions you did not apply, and why;
- changes that need the user's approval or a platform change;
- where the score log, the brief and the final evidence are.
