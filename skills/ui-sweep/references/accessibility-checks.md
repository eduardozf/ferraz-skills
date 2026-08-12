# Measurable accessibility checks

Use these checks when the project does not define a stricter accessibility standard. They support the UI sweep's signal check; they do not establish WCAG conformance. Test with assistive technology or route to a dedicated accessibility audit when conformance is the goal.

## Perceivable

- Require a contrast ratio of at least 4.5:1 for normal text and 3:1 for large text.
- Require a contrast ratio of at least 3:1 for essential graphical objects, component boundaries, and interaction states.
- Verify that color is not the only way to communicate meaning, status, selection, or errors.
- Verify that content reflows without loss of information or functionality at the project's required zoom and narrow-width conditions.

## Operable

- Reach and operate every interactive element with a keyboard.
- Verify that focus is visible, follows a logical order, and is not entirely obscured.
- Verify that keyboard focus is never trapped unless an obvious keyboard action releases it.
- Require pointer targets to be at least 24 by 24 CSS pixels or satisfy a WCAG 2.2 target-size exception.
- Provide a way to pause, stop, or hide non-essential moving or auto-updating content when required.

## Understandable

- Give controls names that describe their outcome and keep the same control labeled consistently.
- Associate instructions and errors with the relevant field; do not rely on placeholder text as the label.
- Make error messages identify the problem and, when possible, explain how to correct it.
- Keep repeated navigation and help mechanisms in a consistent relative order.

## Robust

- Give interactive elements an accessible name, role, value, and state.
- Announce important asynchronous status changes without unexpectedly moving focus.
- Prefer native semantic elements; verify custom controls with the accessibility tree and actual keyboard behavior.

## Evidence

Record the tested route or component, viewport, theme, input method, observed result, and relevant source location. Mark checks as unverified when the available evidence cannot establish the behavior.

Sources: [WCAG 2.2](https://www.w3.org/TR/WCAG22/) and [How to Meet WCAG 2.2](https://www.w3.org/WAI/WCAG22/quickref/).
