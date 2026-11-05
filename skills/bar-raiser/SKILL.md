---
name: bar-raiser
description: >-
  Improve a piece of work in rounds until independent reviewer agents each
  score it at or above a target the user sets, keeping the target, earlier
  scores and round count hidden from the reviewers. Requires T3 Code's
  orchestrator tools. Use when the user says "bar-raiser", /bar-raiser, "run
  the reviewer loop", "review until it scores 9", "loop until both reviewers
  give 9/10", "até os revisores darem nota 9", or otherwise asks to revise
  work until reviewers reach a target score. Not for a single review or
  second opinion, even one that names a score, such as a one-off code review
  of a PR or diff.
---

# Bar raiser

Run rounds of blind, scored reviews and revise the work between rounds until every reviewer reaches the target in the same round.

## Set up the loop

This workflow needs T3 Code's orchestrator tools: `orchestrator_capabilities`, `delegate_task`, `task_status` and `task_cancel`. If they are unavailable after you load them, tell the user and stop. Do not substitute native subagents: the default reviewers run on other providers with explicit options, and the loop relies on async starts and completion notices.

Record these before the first round:

- **Target:** the overall score from 0 to 10 that every reviewer must reach, such as 9. If the user gave none, ask for it once. Never lower it yourself.
- **Reviewers:** if the user names reviewers, use exactly those. If they give only a number, take that many from the defaults below, in order, and ask which models to add beyond two. Otherwise use both defaults. If the user names a model without an effort, use xhigh when the model offers it, otherwise its highest level, and say which.
- **Request:** the user's request in their own words, plus any standard they judge by.
- **Evidence:** what the reviewers inspect to judge the result, not only its source. Match it to the claim: screenshots of the running app for a UI, file paths plus the project's own test or command output for code, and before-and-after measurements under the same conditions for performance.
- **Folders:** a private notes folder outside the checkout, such as one in your scratch directory, for the brief, the score log and each round's records. Keep everything the reviewers read in a new share folder whose parent holds nothing else, such as one made with `mktemp -d`, with the evidence in `review-evidence/` and, for self-contained work, a copy in `work/`. Never use a folder the user supplied, because each round replaces what the share folder holds.


The default reviewers, as `delegate_task` targets. Set each reviewer's effort, and Claude's `fastMode`, explicitly instead of relying on inherited or default values:

- GPT-6.1 Sol through Codex: `{providerInstanceId: "codex", model: "gpt-6.1-sol", options: [{id: "reasoningEffort", value: "xhigh"}]}`.
- Claude Opus 5.5: `{providerInstanceId: "claudeAgent", model: "claude-opus-5-5", options: [{id: "effort", value: "xhigh"}, {id: "fastMode", value: false}]}`.

Call `orchestrator_capabilities` once before the first round to confirm each target. Call it again with `search` for a model its short list omits, or after an error. Use only an instance with `canRunChildTask: true`. If a requested or default model is unavailable, tell the user and ask which to use, recommending one from a model family the other reviewers do not cover. Do not substitute a model or a lower effort on your own.

## Keep the context clean

Read the `context-pollution` skill, in the sibling folder `../context-pollution/SKILL.md`, before writing the brief, and apply it to the brief and to your notes for the whole loop. Each reviewer starts with only the brief, so whatever the brief carries shapes the score. Keep the scores, checked facts and decisions in the notes folder, and leave the review text in the task results.

## Write the brief once

Save the brief in the notes folder. Write it in this order:

1. One line: "Review <the work> and score it."
2. The user's request in their words, with the loop instruction and the target cut out, and the standard they judge by.
3. The work and where it lives: identifiers, file paths, and any generator or builder that produces it.
4. The evidence folder.
5. The paths to the source and documentation of any app or platform involved.
6. The paths to reference data the reviewers need, such as schemas or inventories, or the smallest excerpt when no file holds it.
7. **Verified facts:** platform limits and deliberate decisions, each checked by you, so the reviewers do not re-suggest impossible or excluded changes.
8. "Review only: read files only under the paths named here, write files only in your own temporary folder, do not list, read or search other T3 Code threads or tasks, do not read version-control history, branches or commit messages, and do not change live systems, send messages, open issues or pull requests, or submit forms."
9. "Start your answer with `Score: N/10`, where N is a score from 0 to 10 for how well the work meets the request with the tools and platform as they are today. Then give a prioritized list of concrete improvements, naming the file, line, command or output behind each factual claim. List what you could not check, and list changes that need the platform, outside systems or the user's decision, separately."

Keep the brief free of anything that steers the result:

- Never state the target, an earlier score, the round number, or what an earlier reviewer said anywhere a reviewer can read it, because reviewers can read any local path and other T3 Code threads. Outside the notes folder and the task results, this covers the brief, the task title, the share folder, agent memory, project files, and the branch names, tags and commit messages of the work's checkout. The leak check reads only the brief, the title and the share folder, so check branch names and recent commit messages yourself.
- Leave out your hypotheses and your own assessment.
- Between rounds, change only neutral content: the verified facts, the description of the work when a fix changes it, and missing context that names no score or round.

## Run a round

1. From the second round on, apply the fixes first. In every round, run the project's own tests, lint and build where they cover the work, and add a check only where none does. Inspect the output, and note any check you could not run.
2. Capture fresh evidence of the current state into `<share>/review-evidence/`, with file names that say what each one shows. From the second round on, first move the previous evidence into `<notes>/round-<previous round>/evidence/`. An image of an older state makes the reviewer judge work that no longer exists.
3. Keep reviewer writes away from the work, and detect any that happen. When the work is self-contained files, such as a document or a skill, replace `<share>/work/` with a fresh copy and point the brief at the copy. Otherwise reviewers review in place, because they need the project's environment, such as a running app. In both cases, save into `<notes>/round-<round>/` the `sha256sum` of the original work's files and of every file in the share folder, and, when the work is in a git checkout, its `git status --porcelain --untracked-files=all`.
4. Run the leak check, remove each leak, and rerun it until every hit is justified. A hit is justified only when the work itself needs it, such as a version number that equals the target. Then read the brief, the title and the share folder yourself for what the check does not look for, such as a score written in words, a reviewer's opinion, or a binary file it lists.
5. Start the reviewers in the same turn: all of them in the first round, and afterwards those the score check lists under "Next round". Start each as a new task with `role: "review"`, `mode: "async"`, `isolation: "shared"`, because a worktree would leave out uncommitted fixes, the brief's full text as `task`, and the same neutral `title`, such as "Review the work". Never send a follow-up message to an earlier reviewer, because it would carry its earlier round. Then end your turn. The completion notices wake you; do not poll.
6. When a notice arrives, read its result once, or read it with `task_status` if the notice lacks it. Add the score to the score log. If another reviewer of this round is still running, end your turn again, and continue only after the last notice.
7. If a reviewer fails or returns no score, start it again as a new task with the same brief. If it fails a second time, ask the user whether to continue without it or replace it. Then add a void line for the round and a new roster line, and run a fresh round, with the next number, for the reviewers the score check lists. Never count a missing score as a pass.
8. After every reviewer finishes, compare the hashes and `git status` with the saved ones. If a reviewer changed the work or the share folder, add a void line for the round, tell the user, and undo the change only after the user agrees.
9. Run the score check and follow its decision under "Stop".

If the user stops the loop, or changes the request, the standard, the reviewers or the work while reviewers run, cancel their tasks with `task_cancel`.

## Run the loop checks

`scripts/loop_check.py` in this skill's folder, written `<skill folder>` below, runs the leak check and the score check with Python 3. Before the first round, and after changing the script or the brief template, run `python3 <skill folder>/scripts/test_loop_check.py` and `python3 <skill folder>/scripts/mutation_check.py`. Every test must pass, and every deliberate bug the mutation check plants must make a test fail. The mutation check first confirms that the unchanged tests pass. If it reports a stale mutant, update `MUTANTS` in `scripts/mutation_check.py` to match the changed code.

- **Leak check:** `python3 <skill folder>/scripts/loop_check.py leaks --target <target> --title "<title>" <brief> <share folder>` prints each hit in the brief, the title, and the share folder's file names and text files. It flags four forms only: the target number, a score out of 10 such as `8/10`, a round number such as `round 2`, and a mention of an earlier round, score or review. It ignores the scale wording `0 to 10` and `N/10` and the brief's list numbers, and lists the binary or large files it did not read. It exits 1 when it finds a hit.
- **Score check:** `python3 <skill folder>/scripts/loop_check.py scores --target <target> <score log>` prints the target, the score table, any reviewer whose score dropped, the paused reviewers, the reviewers for the next round, and one decision: `continue`, `target reached`, `incomplete`, `change the approach` or `ask the user`. It exits 0 for any valid log.

Both exit 2 on bad input, such as a target outside 0 to 10, or on a file error.

The score log is a tab-separated file in the notes folder. Its first non-comment line is `roster<TAB><reviewer>,<reviewer>,...`. Each score is a line `<round><TAB><reviewer><TAB><score>`, such as `2<TAB>opus<TAB>8.5`. A line `void<TAB><round>` removes a round from the count, and a new roster line applies to the rounds after it. The target needs a round scored under the latest roster. Give a fresh round the next number, and use one fixed name per reviewer. The score check skips an earlier round that lacks a score from an active reviewer, and says so.

The score check applies these rules to the rounds that are complete and not void:

- **Pause:** a reviewer that gives the same score twice in a row, while another reviewer is below that score, is paused. Its last score carries forward, and it skips the next rounds until every other reviewer reaches that score or every score reaches the target. Once every score, carried or new, is at or above the target, every reviewer reviews the next round, because the target needs all of them in the same round.
- **Progress:** a round is progress when its lowest or mean score, counting carried scores, beats that of every earlier counted round since the roster last changed, so each roster change starts a fresh count. The check answers `change the approach` after two counted rounds in a row without progress, and `ask the user` after three.

## Act on the feedback

- Merge the reviews. Do first what more than one reviewer raises and what blocks the request. When the score check reports a drop, find what that reviewer says got worse before you plan the fixes.
- Before acting on a factual claim about the work, the platform or the data, check it against the source or the live state. Reviewers state false limits and bugs with confidence. Log each claim you checked and what you found.
- When a reviewer suggests something impossible or deliberately excluded, add the checked fact to the verified facts. Do not add their opinion. When a later check contradicts a verified fact, replace it.
- When reviewers conflict, in the same round or across rounds, check the source, keep the version that better serves the user's request, and log the choice.
- Make the fixes within the work yourself, and log each suggestion you decline with a one-line reason. When a fix needs the user's approval, such as changing live data, deleting something, or touching an outside system, gather those fixes into one question for the round, with the reviewer's reason and your recommendation for each. Make the other fixes meanwhile, and start the next round after the user answers.

## Stop

- **Continue:** run the next round with the reviewers the score check lists.
- **Target reached:** if this happened in the first round, confirm that the evidence let the reviewers observe the behavior. If it did not, strengthen the evidence and run another round. In every other case, stop. If the round found verified defects, fix them, run their checks, and capture final evidence. Claim the target only for the scored version, list the later changes as unreviewed, and offer the user one more round to score them.
- **Change the approach:** confirm the evidence shows the current state. Then pick a different strategy for the next round, such as adding the evidence the reviewers said was missing, fixing the lowest scorer's first item first, or restructuring the work instead of patching it. Log what changed.
- **Ask the user:** give the score table, the remaining gaps, whether the advice contradicts earlier rounds or needs outside changes, and the options: one more round with a named change, accepting the current state, or approving the outside changes.
- **Incomplete:** follow step 7 of "Run a round".

## Deliver

Report:

- the target, the reviewers with each model and effort, and the score table from the score check;
- whether the target was reached, and why the loop stopped;
- the main changes per round;
- reviewer claims you checked and found false;
- suggestions you did not apply, and why;
- checks you could not run or that were inconclusive;
- changes made after the last scored round, which no reviewer saw;
- changes that need the user's approval or a platform change;
- where the score log, the brief, each round's records and the final evidence are;
- if the project keeps a status or history log, an offer to copy the score table into it.
