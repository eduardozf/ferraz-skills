# Ferraz Skills

A collection of portable [Agent Skills](https://agentskills.io/) for coding agents.

## Skills

### `agent-time-estimate`

Estimate how long a coding agent will take by counting tool calls and converting them to wall-clock time with a bundled script. The script corrects for estimators that undercount tool calls, simulates follow-up runs and the user's review time, and reports P10 to P90 minutes. It uses `~/.config/agent-time-bench/calibration.json` when present and a generic calibration otherwise.

See [the skill definition](skills/agent-time-estimate/SKILL.md).

### `bar-raiser`

Improve a piece of work in rounds until independent reviewer agents each score it at or above a target you set. Reviewers never see the target. Between rounds each reviewer sees only its own earlier review and what changed, and the target counts only when a final blind round, with the brief alone, confirms it. Out-of-scope suggestions are declined, and the loop changes approach or asks you when scores stop improving.

See [the skill definition](skills/bar-raiser/SKILL.md).

### `context-pollution`

Keep task context focused by avoiding unnecessary content, tracking verified facts, removing outdated instructions, and recovering cleanly when context becomes polluted.

See [the skill definition](skills/context-pollution/SKILL.md).

### `design-consistency-review`

Review an existing interface for contradictions, broken states, polish gaps, and missing capabilities, then render an evidence-backed HTML report. The skill works from source code, screenshots, live applications, design files, and existing feedback.

See [the skill definition](skills/design-consistency-review/SKILL.md).

### `investigate`

Investigate bugs or explain code behavior without changing the project. Return a technical draft separating evidence, hypotheses, and remaining unknowns.

See [the skill definition](skills/investigate/SKILL.md).

### `poteto-mode`

Apply poteto's engineering approach to agent-assisted work: clarify intent, make results observable, shape the code, verify against the real artifact, improve the environment, and expand autonomy from evidence.

See [the skill definition](skills/poteto-mode/SKILL.md).

### `session-closeout`

Close out completed work by updating documentation to match the current implementation and deleting obsolete instructions, duplicate explanations, and related project leftovers. Prefer removal over preserving superseded material.

See [the skill definition](skills/session-closeout/SKILL.md).

### `write-as-poteto`

Write, review, or fix a `SKILL.md` using poteto's conventions for intent, triggers, structure, naming, prose, and deliverables.

See [the skill definition](skills/write-as-poteto/SKILL.md).

### `theo-agent-guidance`

Shape repository instructions in "Theo style" or "T3 Code style" when writing or updating `AGENTS.md`.

See [the skill definition](skills/theo-agent-guidance/SKILL.md).

## Install

```sh
npx skills add eduardozf/ferraz-skills
```

## License

No license has been selected yet. Add a root `LICENSE` file before distributing the skill under explicit reuse terms.
