---
name: ui-sweep
description: Use this when the user asks for a UI sweep, design QA, visual-consistency review, interface-polish audit, or pre-release frontend review of an existing application. Also trigger when the goal is to find design-system drift, missing interaction states, responsive UI problems, or basic accessibility issues.
---

# UI sweep

Run an evidence-led review of an existing interface. Default to an audit: do not modify the application unless the user explicitly asks for fixes. Treat checklist heuristics as prompts for investigation, not automatic defects. Separate product-capability gaps from defects, and never present this sweep as a complete accessibility-conformance audit.

## Process

### 1. Establish scope

Enumerate the screens, routes, components, states, themes, and viewport sizes in scope. Record which evidence is available: a live application, source code, design files, or screenshots. Infer a reasonable scope from the provided artifacts when possible and state any material assumptions.

*Complete when:* the review inventory names every in-scope surface and available evidence source.

### 2. Gather evidence

Use every evidence mode available:

- **Live application:** exercise user flows, keyboard navigation, interaction states, themes, loading, error handling, and responsive behavior.
- **Source code:** inspect components, tokens, styles, variants, and state logic; cite exact files and lines.
- **Design files:** compare hierarchy, tokens, component variants, content, and responsive intent.
- **Screenshots only:** assess visible properties and label dynamic behavior as unverified.

Capture concrete evidence as screenshots, routes, component names, measurements, source locations, or reproducible interaction steps. Do not turn an unsupported hunch into a finding.

*Complete when:* every in-scope surface has been inspected through all evidence modes available for it, and unavailable behavior is marked unverified.

### 3. Run the checklist

Work through every checklist section in order. Mark each section as checked, not applicable, or unverified so an early cluster of findings does not end the sweep. When accessibility checks apply, read [the measurable accessibility checks](references/accessibility-checks.md) and use the project's standard if it is stricter.

*Complete when:* every applicable checklist section has a recorded disposition and every finding has evidence.

### 4. Consolidate and prioritize

Merge symptoms that share a root cause. Keep defects separate from missing capabilities. Use the project's severity scale when one exists; otherwise use:

- **Critical:** blocks task completion or creates a serious accessibility or safety risk.
- **Major:** repeatedly harms comprehension, navigation, or interaction.
- **Moderate:** creates a meaningful inconsistency or resilience problem.
- **Minor:** causes localized polish or consistency debt with limited user impact.

*Complete when:* findings are deduplicated, assigned a severity, and separated into defects and capability gaps.

### 5. Report

Lead with the highest-impact patterns rather than checklist order. Include:

1. Executive summary
2. Scope, evidence, and limitations
3. Findings ordered by severity
4. Systemic patterns and root causes
5. Product-capability gaps
6. Recommended remediation order

Write each finding with this contract:

```markdown
## [Severity] Finding title

- Category:
- Affected surfaces:
- User impact:
- Evidence:
- Recommendation:
- Confidence:
```

If the user also requests fixes, preserve the findings report, connect every change to a finding, and recheck the affected surfaces after implementation.

*Complete when:* every finding follows the contract, limitations are explicit, and the remediation order reflects user impact and root-cause leverage.

## Checklist

Work through the full pass in order. Skip sections that do not apply deliberately. Each item is something to check, not a rule to recite; the “prove it” notes turn a hunch into a defensible finding.

**Contents**
1. [Hierarchy and layout](#1-hierarchy-and-layout)
2. [Component consistency](#2-component-consistency)
3. [Iconography](#3-iconography)
4. [Spacing, alignment, density](#4-spacing-alignment-density)
5. [Typography and color](#5-typography-and-color)
6. [Interaction states and affordances](#6-interaction-states-and-affordances)
7. [Status, feedback, progress](#7-status-feedback-progress)
8. [Copy and labeling](#8-copy-and-labeling)
9. [Scaling and resilience](#9-scaling-and-resilience)
10. [Accessibility basics](#10-accessibility-basics)
11. [Gaps](#11-gaps)
12. [Code-level sweeps](#12-code-level-sweeps)

---

## 1. Hierarchy and layout

- Does reading order match interaction order? Walk the flow and write down the sequence of decisions the user makes, then compare it to the top-to-bottom order on screen. A control that demands a prerequisite sitting *above* that prerequisite is the classic version.
- Does the visually dominant element match the most important action? Check whether the primary action is actually the most prominent thing, and that there's exactly one primary per view.
- Are containers grouped, or just accumulating? Sidebars, toolbars, kebab menus, and settings pages all drift toward flat lists of unrelated entries as features land. Treat roughly seven ungrouped items as a prompt to test scanability, not an automatic defect.
- Do items in a shared container have a discernible ordering logic (frequency, alphabetical, workflow order)? Arbitrary order is a real cost at scale.
- Is anything in the wrong container — a global setting in a per-item menu, a one-off action in a persistent nav?
- Does the same information appear in two places, and can they disagree?
- Is alignment consistent across sibling panels — do their content edges line up, or does each panel have its own margin?

*Prove it:* screenshot the flow in order and annotate the mismatch between step order and visual order.

## 2. Component consistency

- One job, one component. Count the implementations of each recurring element: buttons, tabs, cards, modals, dropdowns, empty states, list rows, badges, toolbars.
- Are variants principled (primary/secondary/danger) or accidental (three near-identical buttons that differ by 2px)?
- Do similar contexts use the same navigation pattern? Tabs in one section and segmented controls in another, for the same kind of switching, is a finding.
- Is the same control placed consistently — is "refresh" always top-right of its panel, or wherever it landed?
- Do dialogs share a shape: title placement, button order, dismissal behavior, escape handling?
- Are there `<div>`s doing a component's job — hand-rolled dropdowns, ad-hoc tooltips — next to the real component that already exists?
- Does a shared component have per-caller overrides that quietly fork it?

*Prove it:* count. "Four tab implementations across six views" is unarguable.

## 3. Iconography

- One icon set, or several mixed? Mixed sets read as sloppy even when nobody can name why — check stroke weight, corner radius, and fill style.
- Consistent sizing within a context. Status indicators especially: a row of indicators at 14px, 16px, and 18px looks broken.
- Optical alignment, not mathematical. Icons with heavy visual mass on one side need nudging; centered-by-math often reads as off-center.
- One meaning per icon, one icon per meaning. The same glyph meaning two different things is worse than two glyphs meaning one thing.
- Do icons carry consistent semantic color, or is color decorative in some places and meaningful in others?
- Icon-only controls: do they all have tooltips and accessible labels, or only some?
- Consistent icon-plus-label spacing and ordering across the app.

*Prove it:* crop the same icon from each context and put the sizes side by side.

## 4. Spacing, alignment, density

- Does spacing come off a scale (4/8pt or whatever the system uses), or are there arbitrary values?
- Consistent padding inside like surfaces — do all cards have the same internal padding?
- Consistent gaps between sibling elements in a list or grid.
- Section rhythm: is the space above a heading consistently larger than the space below it?
- Optical alignment of mixed-content rows (icon + text + badge) — do baselines line up?
- Is density consistent for equivalent content? One list at 32px rows and another at 44px, for the same kind of item, is a finding.
- Do panel edges and content columns align across adjacent regions?

*Prove it:* pull the actual values from source or a screenshot measurement and list the distinct ones.

## 5. Typography and color

- How many distinct font sizes and weights are in use, and does the type scale account for them?
- Is the same semantic level (page title, section header, body, caption) rendered identically everywhere?
- Line height and max line length consistent for body text.
- Truncation handled consistently — ellipsis, wrap, or tooltip, but the same choice for the same kind of content.
- Hardcoded colors instead of tokens; near-duplicate shades that almost match a token.
- Semantic colors (success, warning, danger) used for their meaning and nothing else.
- Contrast holds in both themes, if there are two. Dark mode regressions cluster in borders, disabled states, and hover fills.
- Border radius, border width, shadow, and elevation drawn from a fixed set.

*Prove it:* grep the codebase for hex values and font-size declarations; the count usually speaks for itself.

## 6. Interaction states and affordances

The section that static reviews miss. For every interactive element, check all of these exist and are distinguishable:

- **Default / hover / focus / active / disabled.** Focus especially — keyboard focus rings get dropped in custom components constantly.
- **Disabled is real.** A control that stays visually live but does nothing until a precondition is met is a broken affordance. It should look disabled *and* be non-interactive, with the precondition explained (tooltip or helper text) rather than left for the user to discover by clicking.
- **Loading.** Does the control show progress, and is it non-double-submittable while in flight?
- **Selected / current.** Selection distinguishable from hover, and current-page distinguishable from both.
- **Error / invalid.** Consistent placement and tone of validation messages.
- **Read-only vs disabled** distinguished, since they mean different things.
- Clickable things look clickable; non-clickable things don't. Check hover affordances on cards and rows.
- Destructive actions treated differently from safe ones, consistently, and confirmed the same way everywhere.
- Special variants of a thing are visually distinguishable from the normal case — a stacked item vs a plain one, a draft vs a published one. If the only difference is a low-contrast text label, that's usually not enough weight.
- Transitions and animation durations consistent; nothing animating for no reason.

*Prove it:* interact with the flow and tab through every control with the keyboard.

## 7. Status, feedback, progress

- Does every async action produce feedback, and the same *kind* of feedback for the same kind of action?
- Toast vs inline vs banner vs modal — is the choice principled, or per-implementation?
- Consistent placement for the same class of message.
- Status vocabulary is closed and consistent: don't mix "completed", "done", and "finished" for one state.
- Status is rendered consistently — pick badge or plain text for a given context and hold it.
- Do status displays and their actions belong together? A polished banner sitting next to a bare label-and-link often means two features grew separately.
- Empty states: does every list, table, and panel have one, and do they share a shape (illustration or not, explanation, primary action)?
- Error states: recoverable, specific, and consistently styled — no raw error strings next to friendly copy elsewhere.

## 8. Copy and labeling

- One term per concept, app-wide. Thread/conversation/chat drift is the canonical example.
- Casing consistency in buttons, headers, menu items, and tabs (sentence vs title case).
- Button labels name the outcome ("Create project") rather than a generic verb.
- Consistent tone — don't mix playful microcopy with terse system language in one surface.
- Punctuation consistency in labels, tooltips, and helper text.
- Truncated or ambiguous labels that only make sense to someone who built the feature.
- Dates, times, numbers, and currency formatted the same way everywhere; relative vs absolute time used consistently.

## 9. Scaling and resilience

- Zero, one, few, many. What does each container look like with no items, one item, and several hundred?
- Which containers have no ceiling? An unbounded list in a fixed-height sidebar is a problem the moment a real user arrives. Flag it before it's visible.
- Long content: a 60-character name, a paragraph in a one-line field, a very wide table.
- Narrow and wide viewports; does anything overflow, overlap, or reflow badly?
- Localization pressure — do labels have room to grow ~30%?
- Slow network: does the layout shift when data lands, and is there a skeleton or spinner that matches the final shape?

## 10. Accessibility basics

This is a signal check, not a conformance audit. Use the project standard when one exists; otherwise use [the measurable accessibility checks](references/accessibility-checks.md):

- Text and non-text contrast, including disabled text, placeholder text, focus indicators, and component boundaries.
- Visible keyboard focus on every interactive element.
- Touch and click targets meet the applicable minimum size or a documented exception.
- Meaning never conveyed by color alone.
- Icon-only buttons have accessible names.
- Heading levels form a sensible outline.

## 11. Gaps

Missing capabilities that surface during a review. File separately from defects:

- Organization: grouping, folders, tags, pinning, favorites.
- Ordering: manual reorder, sort options, drag-and-drop.
- Relationships: linking items, dependencies, blocking, parent/child.
- Bulk operations: multi-select and act on many.
- Search and filter where the list has outgrown scanning.
- Undo, or confirmation for anything destructive without it.
- Keyboard shortcuts for high-frequency actions.
- Persistence of view state (sort, filter, collapsed sections) across sessions.

## 12. Code-level sweeps

When you have the source, these turn subjective findings into counts. Adapt the patterns to the stack.

- **Component inventory.** List files under the component directory; look for near-duplicate names (`Button`, `ButtonNew`, `PrimaryBtn`).
- **Hardcoded colors.** Search for hex codes and `rgb(` outside the token/theme file.
- **Raw spacing values.** Search for `padding:`/`margin:`/`gap:` with pixel literals, or arbitrary-value utilities like `p-[13px]`.
- **Font sizes.** Search for `font-size:` or text-size utilities; count the distinct set against the type scale.
- **Ad-hoc z-index.** Values not drawn from a defined layer scale predict stacking bugs.
- **Inline styles** on components that have a variant API.
- **Duplicate icon imports** from two different icon packages.
- **Disabled logic.** Search for `disabled=` and check it against the conditions that should gate each action — this is where you find the always-enabled button.
- **`!important`** and specificity hacks, which usually mark a place where the system fought the author and lost.

Report these as counts with a few named examples, not as an exhaustive dump.
