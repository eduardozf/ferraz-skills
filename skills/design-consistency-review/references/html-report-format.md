# HTML report format

## Start from the template

When rendering a report, copy [report-template.html](../assets/report-template.html) into the OS temp directory. Replace every `{{PLACEHOLDER}}` with escaped report text, set the document language, and insert finding sections as described below. The input is the review evidence and classified findings; the output is one standalone HTML file. Remove unused sections and authoring comments.

Keep CSS and scripts inline. Embed every screenshot as a base64 data URI. Do not load external fonts, styles, scripts, or images, or reference local asset paths. If images push the file past about 10 MB, downscale them while preserving legible evidence. If the template cannot be read, report the missing resource rather than substituting a CDN scaffold.

Use the template's CSS classes for cards, badges, grids, and evidence. Add inline CSS only where an evidence pattern requires it. Do not add app code, filtering, diagramming libraries, or interactions beyond the theme toggle and anchor links.

## Header and coverage

Show the target, date, scope, available evidence, and documented or derived canon. Add a compact legend for the classes used in the report. If no canon can be established, state that limitation.

Record checklist coverage as `checked`, `not applicable`, or `unverified`. State material assumptions, evidence limitations, and unavailable artifact checks under Coverage and limitations. Put unresolved intent or unlocalized feedback under Open questions. Omit empty optional sections.

## Fix first and empty reviews

After the header, list up to five supported defect findings with the best impact-to-effort ratio as anchor links to their cards. Use only actual findings; one finding warrants one link. Omit Fix first when there are no defects.

When there are no findings of any class, keep the template's empty-review statement and coverage section. When defects exist, replace that statement with their cards. When only gaps or preferences exist, omit Findings or state that no defects were established, then place those cards in their separate sections. Do not invent findings to fill the layout.

## Finding card

Use one `<article class="card" id="DR-01">` per finding. Give each card:

- ID: a stable identifier such as `DR-01`, displayed in monospace.
- Title: the contradiction, broken behavior, visible defect, missing capability, or proposed choice.
- Metadata: class, effort (`S`, `M`, `L`), and checklist category. Use `.badge` with `.broken`, `.inconsistent`, `.polish`, `.gap`, or `.preference` for the class.
- Where: named surfaces, routes, or files in monospace.
- Evidence: captured instances, measurements, source evidence, or reproducible steps. Label reconstructions as illustrations; do not present them as captures of the application.
- What and Fix: use the class-specific requirements below.
- Notes, when needed: intentional exceptions, unresolved decisions, verification limits, or resolved status.

| Class | What | Fix |
| --- | --- | --- |
| `inconsistent` | Comparable instances and the rule they contradict. | Winning treatment and the basis for choosing it. |
| `broken` | Expected versus observed behavior and its trigger. | Action restoring the expected behavior. |
| `polish` | Visible cosmetic defect and supporting evidence. | Specific correction. |
| `gap` | User task or reported need and the capability missing from the inspected flow. | Proposed capability and any decision it requires. |
| `preference` | Proposed aesthetic choice, explicitly labeled as taste. | Suggested treatment and tradeoff. |

Keep explanations concise. Do not invent a second instance for a finding that does not require one.

Put defects under Findings. Put Gaps and Preferences in separate sections afterward. Use `.card.quiet` for those cards, retaining class, effort, category, and evidence without competing visually with defects.

## Evidence patterns

Choose the pattern that establishes the claim:

- Annotated screenshot: put the image in `.evidence`, with a `.screenshot` wrapper and absolutely positioned `.pin` markers. Add a numbered key; split unrelated observations into separate findings.
- Side-by-side instances: use `.grid` with tightly cropped captures and labeled origins. For an inconsistency, state why contexts are equivalent and mark the recommended treatment.
- Variant strip: show relevant variants with their source locations. Explain which differences are accidental rather than treating the count as proof.
- Swatch or token grid: show values beside `.swatch` chips; use `.checker` for transparency. Identify the violated token or rule.
- Scale ruler: use `.ruler` bars at measured pixel widths and name the documented scale. Label off-scale values in text as well as color.
- State matrix: use a table with applicable states as columns. Distinguish `present`, `missing`, `wrong`, `not applicable`, and `unverified`. A state unavailable in a screenshot is unverified, not missing.
- Order mismatch: place observed interaction order beside visual order. Use inline SVG connectors only if needed to explain the mismatch.
- Reproduction or source evidence: include steps, expected and observed results, or quoted source locations when screenshots cannot establish the finding.

Use readable evidence sizes. Do not shrink captures to meet an arbitrary card height. Keep screenshots in a fixed neutral container and never recolor them with the report theme. When both themes were captured, show and label both; the report toggle must not switch the evidence.

## Theme and style

Keep the template's light/dark toggle in the header. Default from `prefers-color-scheme` before first paint, maintain its accessible label and pressed state, and avoid storage. The toggle must work without an external global.

Use the template's theme variables for backgrounds, borders, text, and badges. Keep class labels visible independently of color. Use one accent and the class palette; distinguish all classes in both themes.

Use sentence case headings, short paragraphs, and concrete actions. Preserve terms such as finding, token, instance, state, and canon where they describe the evidence. Avoid unsupported claims such as “modern”, “intuitive”, or “improves UX”.

## Check before delivery

Open the completed report and inspect both themes, visible content, evidence, and narrow layouts. Follow each Fix first link to its card. Check runtime errors and that embedded images load. With external requests blocked, confirm that styling and the theme toggle still work; if that check is unavailable, inspect asset references and state the execution limit.

Remove unresolved placeholders and unused sections. Return the HTML file link with any checks that could not be completed.
