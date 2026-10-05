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

For a behavioral bug, record expected and observed behavior, inputs, environment, and a safe reproduction or existing trace before diagnosing the cause. If reproduction is unavailable, say what remains unverified. Distinguish code defects from data, configuration, dependency, and environment differences.

If running the original system would change state, use existing artifacts or an isolated reproduction. Keep the source project read-only. For a request to explain code, trace the implementation without requiring a runtime reproduction.

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
- Reproduction result or verification limits, when investigating a behavioral bug
- Likely root cause or hypotheses
- Useful references
- Remaining unknowns
- Suggested direction for whoever implements the fix

The result is for manual review only.
