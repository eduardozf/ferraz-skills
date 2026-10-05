---
name: design-consistency-review
description: >-
  Review an existing UI for contradictions and render evidence-backed findings
  as a self-contained HTML report. Use for a UI/UX audit, visual QA, a review
  of polish gaps, "find design inconsistencies", "explain what looks off", or
  organizing interface feedback. Accept screenshots, source code, a live app
  or URL, design files, and existing feedback. Default to review-only; do not
  select this skill for a request solely to build or redesign an interface.
---

# Design consistency review

Inventory the interface, compare equivalent contexts, and report supported findings with concrete actions. Distinguish contradictions from broken behavior, missing capabilities, and personal preference.

## 1. Establish scope and evidence

Name the screens, routes, components, states, themes, and viewport sizes in scope. Record the available source code, screenshots, live application, design files, and feedback. Infer a reasonable scope from the artifacts and state material assumptions.

When only one screenshot is available, assess visible properties and mark dynamic behavior unverified. State which additional evidence would establish it. Do not pad the review with guesses.

Complete when every in-scope surface and available evidence source is named.

## 2. Establish the canon

Look for a design system, tokens, theme configuration, component library, or documented platform convention. Use explicit project rules before general conventions.

If no documented rule exists, compare equivalent contexts and propose the dominant treatment as the canon. Label it as derived and check for intentional exceptions; frequency alone does not establish correctness.

For an inconsistency, name the violated rule and recommend which treatment should win. If intent is unresolved, place the decision under Open questions rather than asserting a defect.

Complete when each inconsistency has a documented or explicitly derived rule.

## 3. Inspect and compare

Read the [sweep checklist](references/sweep-checklist.md) before listing findings. Use the evidence appropriate to each claim:

- Source code: inventory repeated components, tokens, values, and overrides. Counts identify candidates; prove a mismatch in equivalent contexts before reporting drift.
- Screenshots: compare the same element across contexts or against a documented rule. Do not infer runtime behavior from a static capture.
- Live application: exercise relevant flows, applicable interaction states, keyboard behavior, and scaling cases.
- Design files: compare specified behavior and appearance with the implementation.
- Existing feedback: normalize reports using the rules below and distinguish reported behavior from observations you reproduced.

For every checklist section, record `checked`, `not applicable`, or `unverified`, including material coverage limits. Capture routes, component names, screenshots, measurements, source locations, or reproducible steps. Missing evidence is not evidence of a missing state.

Complete when in-scope surfaces have been inspected using the relevant available evidence, checklist coverage is recorded, and each finding has concrete support.

## 4. Classify and triage

Give every finding one class, an effort estimate, and a category from the checklist:

- `broken`: misleads or blocks the user. Record expected versus observed behavior.
- `inconsistent`: contradicts a documented rule or a justified dominant pattern. Name the comparable instances and the winning treatment.
- `polish`: an evidenced cosmetic defect. Name the visible defect and the correction.
- `gap`: a missing capability supported by a user task or reported need. Name the task and proposed capability.
- `preference`: a proposed aesthetic choice. Label it as taste and state the tradeoff.

Estimate effort as `S` for a contained component change, `M` for several locations or a new token, and `L` for a design decision or substantial refactor.

Merge symptoms sharing one root cause and preserve intentional exceptions. Use stable finding IDs. Keep gaps and preferences separate from defects. Prioritize by impact and effort, placing small fixes for blocking behavior prominently.

Complete when each finding has evidence, class, effort, category, and a concrete action.

## 5. Render and check the report

Before generating HTML, read the [report format](references/html-report-format.md) and start from its bundled template. Write one HTML file in the OS temp directory with inline CSS, scripts, and screenshot data. Include scope, evidence, canon, checklist coverage, and limitations.

List up to five supported defect findings under Fix first, ordered by impact and effort. When there are no defects, omit that list. When there are no findings at all, state that none were established within the inspected scope; retain unverified areas without implying they passed.

Open the generated file in the available browser. Check light and dark themes, finding anchors, embedded evidence, layout, and runtime errors. Block external requests when the browser supports it and confirm the report still works. Otherwise, inspect its asset references and state that offline execution remains unchecked. Correct defects before delivery. If browser access is unavailable, explicitly report that rendering remains unchecked.

Complete when the report meets the format contract and the artifact checks pass, or unavailable checks are named.

## When the input is existing feedback

- Split compound complaints and merge duplicate reports.
- Localize vague feedback to a named surface and observable behavior. Keep unresolved reports under Open questions.
- Preserve fixed, merged, and rejected status. Do not present resolved reports as active defects.
- Preserve source and user context when they affect interpretation or priority. Summarize feedback tone separately if useful.
- Label your own observations separately from supplied reports. State which reports remain unverified.

## Stay in scope

Default to review-only. Modify the application only when the user requests fixes. Keep structural redesign proposals under Open questions unless redesign is requested. Accessibility checks are signals, not a full conformance audit.

When fixes are requested, map each change to a finding ID and recheck affected surfaces. Preserve the report unless the user requests its removal.

## Deliver

Return a link to the HTML report, the highest-priority findings, and material evidence or verification limits. Use concrete locations and actions; omit a compliments section unless requested.
