# Ferraz Skills

A collection of portable [Agent Skills](https://agentskills.io/) for coding agents.

## Skills

### `design-consistency-review`

Review an existing interface for contradictions, broken states, polish gaps, and missing capabilities, then render an evidence-backed HTML report. The skill works from source code, screenshots, live applications, design files, and existing feedback.

See [the skill definition](skills/design-consistency-review/SKILL.md).

## Install

From this checkout:

```sh
npx skills add . --skill design-consistency-review
```

After publishing the repository to GitHub:

```sh
npx skills add eduardozf/ferraz-skills --skill design-consistency-review
```

## Validate

```sh
agentskills validate skills/design-consistency-review
npx skills add . --list
```

Install the reference validator with `python -m pip install skills-ref` before running the first command.

## License

No license has been selected yet. Add a root `LICENSE` file before publishing or distributing the skill.
