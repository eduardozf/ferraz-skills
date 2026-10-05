---
name: investigate
description: Investigate bugs, issues, unexpected behavior, or implementation details in a codebase. Use when the goal is research and diagnosis only, producing a technical draft for someone else to review or implement.
---

# Investigate

Investigate the requested problem without modifying anything.

## Rules

- Work read-only.
- Do not edit code.
- Do not create commits, branches, PRs, issues, or comments.
- Do not publish findings anywhere.
- Do not implement the fix unless explicitly requested.
- Separate confirmed findings from hypotheses.

## Research

Inspect the relevant code paths and, when useful:

- Git history
- Existing issues and PRs
- Dependencies
- Upstream projects
- Related implementations in other repositories

Trace the behavior far enough to identify where it originates and what likely causes it.

## Output

Produce a concise draft containing:

- Summary
- Findings
- Relevant code paths
- Evidence
- Likely root cause or hypotheses
- Useful references
- Remaining unknowns
- Suggested direction for whoever implements the fix

The result is for manual review only.