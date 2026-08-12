# Ferraz Skills

A collection of portable [Agent Skills](https://agentskills.io/) for coding agents.

## Skills

### `ui-sweep`

Run an evidence-led quality sweep of an existing application interface. The skill covers hierarchy, component consistency, interaction states, responsive resilience, accessibility signals, and code-level design-system drift.

See [the skill definition](skills/ui-sweep/SKILL.md).

## Install

From this checkout:

```sh
npx skills add . --skill ui-sweep
```

After publishing the repository to GitHub:

```sh
npx skills add <owner>/ferraz-skills --skill ui-sweep
```

## Validate

```sh
agentskills validate skills/ui-sweep
npx skills add . --list
```

Install the reference validator with `python -m pip install skills-ref` before running the first command.

## License

No license has been selected yet. Add a root `LICENSE` file before publishing or distributing the skill.
