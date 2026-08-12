---
name: design-consistency-review
description: Use when the user asks to review an existing UI, run a UI/UX audit, perform visual QA or a polish pass, find design inconsistencies, explain what looks off, or turn scattered interface feedback into actionable findings. Trigger for reviews based on screenshots, source code, a live app or URL, design files, or existing user feedback.
---

# Design Consistency Review

Find the places where a UI contradicts itself, then hand back a triage list someone can work through on a Tuesday afternoon.

The failure mode this skill exists to prevent is **the vibes review**: an agent looks at one screen, says the spacing feels a bit tight and the palette is nice, and produces nothing anyone can act on. A real design review is not an aesthetic opinion. It is a *comparison*. You cannot find an inconsistency by looking at one thing — you find it by looking at the same thing in two places and noticing they disagree.

So the core move is always: **inventory first, compare second, judge last.**

## What counts as a finding

Two shapes, and it's worth knowing which one you're holding:

- **Same meaning, different form.** One action, status, or concept is rendered two ways. Two tab styles for the same kind of navigation. A refresh control that sits top-right on one panel and inline on another. An icon that means "settings" drawn at 16px here and 20px there.
- **Different meaning, same form.** Two things that behave differently look identical. A button that's live and a button that does nothing until you select a row. A normal item and a special item with no visual distinction between them.

Both are objective — you can point at two places and show the contradiction. Keep them separate from a third, weaker category:

- **Preference.** "I'd give this more breathing room." Legitimate, often right, but it's taste. Label it as such so the team can weigh it differently. Never dress up a preference as an inconsistency; it burns the credibility of the whole list.

## Process

### 1. Establish scope and evidence

Inventory the screens, routes, components, states, themes, and viewport sizes in scope. Record which evidence is available: source code, screenshots, a live app or URL, design files, or existing feedback. Infer a reasonable scope from the artifacts instead of blocking on questions, but state material assumptions.

When only one screenshot is available, assess visible properties, identify what additional evidence would unlock, and mark dynamic behavior unverified. Never pad the list with guesses.

**Complete when:** every in-scope surface and available evidence source is named.

### 2. Establish the canon

An inconsistency only exists relative to a rule. Before flagging anything, spend a few minutes finding out what the rules are:

- Look for a design system, token file, theme config, Tailwind config, component library, or Storybook. If tokens exist, drift *from the tokens* is the strongest possible finding — it's objectively checkable.
- If there's no written system, derive the de-facto one: whatever treatment appears most often is the canon, and the outliers are the findings. Say explicitly that you're doing this, since the majority isn't always right.
- Note the platform conventions in play (iOS, Material, macOS, web). A violation of an explicit house rule outranks a violation of a general convention.

If you flag a divergence, **say which side should win.** "These two disagree" is half a finding. "These two disagree, and B is the canon because it's used in six other places" is the whole thing.

**Complete when:** the report can name the documented or derived rule used to judge every inconsistency.

### 3. Inspect and compare

Adapt to whatever access you have. In rough order of usefulness:

1. **Source code.** The highest-signal input, and the most under-used. Search the component tree for repeated patterns: how many button implementations exist, how many distinct spacing values, how many hardcoded hex colors that should be tokens, how many one-off `<div>`s doing a component's job. Counting is a superpower here — `N` variants of one thing is a finding you can prove.
2. **Screenshots.** Compare *across* images, not within one. Line up the same element in different contexts. If you're given several screenshots, the whole point is the diff between them.
3. **A live URL or running app.** Walk the real flows. Interaction states are invisible in a static image — this is where you find the button that's always enabled.
4. **Existing feedback** (a thread, issue tracker, support notes, a chat dump). Extract and normalize; see below.
5. **Design files or specs.** Compare intent against what shipped.

Work the dimensions in the [sweep checklist](references/sweep-checklist.md) — it's the full sweep, organized so you can run it against any UI. Read it before you start listing findings; it exists so the review doesn't stop at whatever caught your eye first.

Mark every checklist section `checked`, `not applicable`, or `unverified`. Capture evidence as routes, component names, screenshots, measurements, source locations, or reproducible interaction steps. Do not file unsupported hunches.

**Complete when:** every in-scope surface has been inspected through every available evidence mode, every checklist section has a disposition, and every proposed finding has concrete evidence.

#### Review dimensions

The checklist has the detail. These are the buckets, and every finding lands in exactly one:

1. **Hierarchy and layout.** Does visual order match interaction order? If a flow reads *search → new → pick a project*, but the project selector sits below the button that demands it, the layout is lying about the sequence. Also: surfaces that accumulate items without grouping (sidebars, toolbars, menus are the usual suspects) — clutter is rarely a decision anyone made, it's what happens when nobody owns the container.
2. **Component consistency.** Same job, same component. Count the divergent implementations.
3. **Iconography.** One style set, consistent sizing, optical (not mathematical) alignment, and one icon per meaning across the whole app.
4. **Spacing, alignment, density.** Values off the scale, optical misalignment, inconsistent padding between sibling surfaces.
5. **Typography and color.** Ad-hoc sizes and weights, one-off shades that almost match a token, semantic colors used decoratively.
6. **Interaction states and affordances.** The richest vein, and the one static reviews miss entirely. Every interactive element owes you: default, hover, focus, active, disabled, loading, error. A control that stays visually live while doing nothing is a broken affordance, not a nitpick — it teaches users the UI is unreliable.
7. **Status, feedback, and progress.** Spinners, toasts, banners, empty states, and status labels drifting in placement, tone, and prominence.
8. **Copy and labeling.** Terminology drift for one concept, casing inconsistency, button labels that don't say what happens.
9. **Scaling and resilience.** What this looks like at 0, 1, 20, and 500 items; with a 60-character name; in a narrow window; translated. "This is already growing out of control" is a scaling finding, and it's usually the earliest signal that a container needs grouping or virtualization.
10. **Gaps.** Missing affordances users clearly need — grouping, reordering, linking, bulk actions, undo. These aren't inconsistencies, but they surface in the same pass and belong in the same document, clearly marked so they don't get triaged as bugs.

### 4. Classify and triage

Tag every finding with both:

**Class**
- `broken` — misleads the user or blocks them. Enabled controls that do nothing, states with no visual distinction, unreachable actions.
- `inconsistent` — provably contradicts a rule or the dominant pattern.
- `polish` — real but cosmetic; the UI works.
- `gap` — a missing capability, not a defect.
- `preference` — your taste, honestly labeled.

**Effort** — `S` (one component, contained), `M` (touches several places or needs a token added), `L` (needs a design decision or a real refactor first).

The `broken` + `S` findings are the ones that make a review worth reading. Sort so they're impossible to miss.

Merge symptoms with one root cause and preserve meaningful exceptions. Keep gaps and preferences separate from defects. Use stable IDs so findings can move into an issue tracker without losing identity.

**Complete when:** every finding has one class, one effort estimate, one root-cause home, and a clear recommended action.

### 5. Report

Use this structure. Stable IDs matter — people paste them into issue trackers.

```markdown
# Design review — <target> — <date>

**Scope:** what you looked at, and how (screenshots / source / live app).
**Canon:** the rules you reviewed against, and whether they're documented or derived.
**Findings:** N total — X broken, Y inconsistent, Z polish, W gaps.

## Fix first
The three-to-five findings with the best impact-to-effort ratio, by ID and one line each.

## 1. Hierarchy and layout

### DR-01 — Sidebar accumulates ungrouped items `inconsistent` `M`
**Where:** left sidebar, all screens.
**What:** Six unrelated entries share one flat list with no separators or ordering logic.
**Evidence:** Six entries observed on `/projects`; other primary navigation groups use labeled sections.
**Why it matters:** Nothing has priority, so scanning cost grows with every feature added.
**Fix:** Group into <named sections>; move <item> under <section>.

### DR-02 — ...

## 2. Component consistency
...

## Gaps
Missing capabilities, same format, clearly separated from defects.

## Preferences
Taste calls, honestly labeled, so they can be dismissed cheaply.

## Not filed
Things you considered and deliberately didn't flag, with the reason. Prevents the same debate next review.

## Open questions
Anything you couldn't resolve without the team — intentional divergences, states you couldn't reach.
```

Every finding needs **Where**, **What**, **Evidence**, and **Fix**. A finding without a location is unactionable; one without evidence is a hunch; one without a proposed fix pushes your work onto the reader. **Why it matters** can be dropped when it's self-evident.

Prefer twenty solid findings over sixty padded ones. If two findings share one root cause — six components drifting because there's no spacing token — file the root cause once and list the symptoms under it. That's one fix, not six.

**Complete when:** the report states scope, evidence, canon, and limitations; every finding satisfies the contract; and the fix-first list reflects impact-to-effort rather than checklist order.

## When the input is existing feedback

Sometimes the job isn't inspecting a UI, it's turning a messy thread of complaints into something triageable. Same output format, plus:

- **One finding per issue.** Split compound complaints; merge duplicates reported by different people.
- **Translate vague to concrete.** "This feels cluttered" becomes a named surface and the specific thing accumulating in it. If you genuinely can't localize it, keep it under Open questions rather than inventing a location.
- **Preserve status.** If something is already fixed, merged, or explicitly rejected, mark it and don't re-litigate it.
- **Keep provenance when it changes the weight.** Whether a report came from a daily power user or a first-run visitor changes how you triage it, so note it. Summarize the tone of the feedback separately at the end — it's context for whoever reads this, not a finding.
- **Don't add findings that nobody reported** without marking them as yours. Mixing your observations into someone else's report silently is how a compilation loses trust.

## Phrasing

- Name the two instances: `tabs in Settings use an underline; tabs in Projects use a pill — pill wins, it's used in 4 other views.`
- Quantify when you can: `11 distinct button implementations; 3 cover 90% of usage.`
- Say what to do: `disable when no PR is selected` beats `should reflect state`.
- Don't hedge into uselessness. If you're unsure whether something is intentional, ask it in Open questions instead of filing a mushy finding.
- Skip the compliments section unless the user asked for one. It pads the document and delays the list.

## Stay in scope

This is triage, not a redesign or a full accessibility-conformance audit. Default to review-only: do not modify the application unless the user explicitly asks for fixes. Don't propose a new information architecture, a new palette, or a rebuild unless the user asked — and if the findings genuinely point at a structural problem, say so in one paragraph under Open questions and let them decide. A review that turns into a redesign pitch gets read once and actioned never.

When fixes are requested, preserve the findings report, map every change to a finding ID, and recheck the affected surfaces after implementation.
