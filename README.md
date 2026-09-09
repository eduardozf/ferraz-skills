# Ferraz Skills

A collection of portable [Agent Skills](https://agentskills.io/) for coding agents.

## Skills

### `design-consistency-review`

Review an existing interface for contradictions, broken states, polish gaps, and missing capabilities, then render an evidence-backed HTML report. The skill works from source code, screenshots, live applications, design files, and existing feedback.

See [the skill definition](skills/design-consistency-review/SKILL.md).

### `write-as-poteto`

Write, review, or fix a `SKILL.md` using poteto's conventions for intent, triggers, structure, naming, prose, and deliverables.

See [the skill definition](skills/write-as-poteto/SKILL.md).

## Install

From this checkout:

```sh
npx skills add . --skill design-consistency-review
npx skills add . --skill write-as-poteto
```

From the public GitHub repository:

```sh
npx skills add eduardozf/ferraz-skills --skill design-consistency-review
npx skills add eduardozf/ferraz-skills --skill write-as-poteto
```

## Validate

```sh
agentskills validate skills/design-consistency-review
agentskills validate skills/write-as-poteto
npx skills add . --list
```

Install the reference validator with `python -m pip install skills-ref` before running the first command.

## License

No license has been selected yet. Add a root `LICENSE` file before distributing the skill under explicit reuse terms.
