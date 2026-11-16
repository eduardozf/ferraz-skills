---
name: bar-raiser
description: >-
  Improve a piece of work in rounds until independent reviewer agents each
  score it at or above a target the user sets. Reviewers never see the
  target; between rounds each sees only its own earlier review, and the
  target counts only when a blind round confirms it. Requires T3 Code's
  orchestrator tools. Use when the user says "bar-raiser", /bar-raiser, "run
  the reviewer loop", "review until it scores 9", "loop until both reviewers
  give 9/10", "até os revisores darem nota 9", or otherwise asks to revise
  work until reviewers reach a target score. Not for a single review or
  second opinion, even one that names a score, such as a one-off code review
  of a PR or diff.
---

# Bar raiser

Run rounds of scored reviews and revise the work between rounds until every reviewer reaches the target in the same blind round.

A round is either blind or a follow-up round. In a blind round, every reviewer gets the brief alone. In a follow-up round, each reviewer also gets a note with its own earlier review and what changed since, so it can check whether its points were fixed. The first round is blind. After that, rounds are follow-up rounds until every score reaches the target, and then a blind round confirms it. Reviewers who see their earlier score tend to reward progress, so a follow-up round never claims the target.

## Set up the loop

This workflow needs T3 Code's orchestrator tools: `orchestrator_capabilities`, `delegate_task`, `task_status` and `task_cancel`. If they are unavailable after you load them, tell the user and stop. Do not substitute native subagents: the default reviewers run on other providers with explicit options.

Record these before the first round:

- **Target:** the overall score from 0 to 10 that every reviewer must reach, such as 9. If the user gave none, ask for it once. Never lower it yourself.
- **Reviewers:** if the user names reviewers, use exactly those. Otherwise use the defaults below. If the user names a model without an effort, use xhigh when the model offers it, otherwise its highest level, and say which.
- **Request:** the user's request in their own words, plus any standard they judge by.
- **Evidence:** what the reviewers inspect to judge the result, not only its source. Match it to the claim: screenshots of the running app for a UI, file paths plus the project's own test or command output for code, and before-and-after measurements under the same conditions for performance.
- **Folders:** a private notes folder outside the checkout, such as one in your scratch directory, for the brief, the score table and the follow-up notes. Put the evidence in a new, empty folder made for this loop, such as one from `mktemp -d`.

The default reviewers, as `delegate_task` targets. Set each reviewer's effort, and Claude's `fastMode`, explicitly:

- GPT-6.1 Sol through Codex: `{providerInstanceId: "codex", model: "gpt-6.1-sol", options: [{id: "reasoningEffort", value: "xhigh"}]}`.
- Claude Opus 5.5: `{providerInstanceId: "claudeAgent", model: "claude-opus-5-5", options: [{id: "effort", value: "xhigh"}, {id: "fastMode", value: false}]}`.

Call `orchestrator_capabilities` once before the first round to confirm each target. If a requested or default model is unavailable, tell the user and ask which to use. Do not substitute a model or a lower effort on your own.

## Write the brief once

Read the `context-pollution` skill, in the sibling folder `../context-pollution/SKILL.md`, before writing the brief. Each reviewer starts with only what you send it, so whatever the brief carries shapes the score. Save the brief in the notes folder, in this order:

1. "Review <the work> and score it."
2. The user's request in their words, with the loop instruction and the target cut out, and the standard they judge by.
3. The work and where it lives: identifiers, file paths, and any generator or builder that produces it.
4. The evidence folder.
5. The paths to the source, documentation and reference data the reviewers need.
6. **Verified facts:** platform limits and deliberate decisions, each checked by you, so the reviewers do not re-suggest impossible or excluded changes. End it with an **Out of scope** list: what the user's request or answers leave out or exclude, taken from the user's words, so the reviewers do not score the work down for lacking it.
7. "Review only: read files only under the paths named here, do not change the work or live systems, and do not read other T3 Code threads or tasks, or version-control history, branches or commit messages."
8. "Start your answer with `Score: N/10`, where N is a score from 0 to 10 for how well the work meets the request with the tools and platform as they are today. Then give a prioritized list of concrete improvements, naming the file, line, command or output behind each factual claim. List what you could not check separately."

Never let a reviewer read the target. Keep earlier scores, round numbers and what other reviewers said out of the brief, the task title, the evidence folder, and the branch names and commit messages of the work's checkout. Leave out your own assessment. Between rounds, change only the verified facts, the out-of-scope list, and the description of the work when a fix changes it.

## Write the follow-up notes

In a follow-up round, write a note for each reviewer that has an earlier review. A reviewer without one, such as a replacement, gets the brief alone. Put only this in the note:

1. "This is round <round> of the review. Your earlier review follows, then what changed since."
2. That reviewer's own latest review, verbatim, with its score.
3. The changes made since that review, each with the file or evidence that shows it.
4. That reviewer's suggestions you declined, each with its one-line reason.
5. "Judge the work as it is now against the request, not against your earlier review, and check each of your earlier points again."

Never put the target, another reviewer's score or review, or the number of reviewers in a note.

## Run a round

1. From the second round on, apply the fixes first. In every round, run the project's own tests, lint and build where they cover the work, and note any check you could not run.
2. Replace the evidence folder's contents with fresh evidence of the current state, so no reviewer judges work that no longer exists.
3. Read the brief, the title, the notes and the evidence folder once for anything that reveals the target or another reviewer's view.
4. Start every reviewer in the same turn, each as a new task with `role: "review"`, `mode: "async"`, `isolation: "shared"`, the same neutral `title`, such as "Review the work", and as `task` the brief followed by that reviewer's note in a follow-up round. Never send a message to an earlier reviewer's task. Then end your turn; the completion notices wake you.
5. When a result arrives, add its score to the table in `<notes>/scores.md`, with one row per round, one column per reviewer, and blind rounds marked. If other reviewers are still running, check this result's factual claims now and plan its fixes in the notes, but change nothing a reviewer reads until the last one finishes.
6. If a reviewer fails or returns no score, start it again once. If it fails again, ask the user whether to continue without it or replace it. Never count a missing score as a pass.
7. When the work is in a git checkout, compare `git status` before and after the round. If a reviewer changed the work, tell the user and undo the change only after the user agrees.

If the user stops the loop or changes the request, the reviewers or the work while reviewers run, cancel their tasks with `task_cancel`.

## Act on the feedback

- Merge the reviews. Do first what more than one reviewer raises and what blocks the request. When a score drops, find what that reviewer says got worse. A drop in a blind round after follow-up rounds often means the follow-up scores ran high, so look for what the reviewer says is missing.
- Before acting on a factual claim about the work, the platform or the data, check it against the source or the live state. Reviewers state false limits and bugs with confidence.
- Keep the scope to the user's request. Decline a suggestion that goes beyond it, even when it would raise a score. When the request does not settle whether a suggestion is in scope, leave it out and report it. Add an area to the out-of-scope list when reviewers keep raising it, and move it into the work only when the user asks.
- When a reviewer suggests something impossible or deliberately excluded, add the checked fact to the verified facts, not their opinion.
- When reviewers conflict, check the source and keep the version that better serves the user's request.
- Make the fixes yourself. When a fix needs the user's approval, such as changing live data, deleting something, or touching an outside system, gather those into one question for the round with your recommendation for each.

## Decide what comes next

- **Every reviewer at or above the target in a blind round:** stop. If this was the first round, first confirm the evidence let the reviewers observe the behavior, and if it did not, strengthen it and run another blind round. Fixes made after this round are unreviewed; list them and offer one more round.
- **Every reviewer at or above the target in a follow-up round:** apply the fixes, then run a blind round with every reviewer.
- **Otherwise:** run a follow-up round. After two rounds in a row where neither the lowest nor the average score beats every earlier round, change the approach, such as adding the evidence reviewers said was missing or restructuring the work instead of patching it. After three, ask the user whether to run one more round with a named change or accept the current state.

## Deliver

Report the target, the reviewers with each model and effort, the score table, whether the target was reached and why the loop stopped, the main changes per round, reviewer claims you found false, suggestions you declined and why, checks you could not run, changes no reviewer saw, and changes that need the user's approval. If the work ends in a pull request, offer to add the score table to its description.
