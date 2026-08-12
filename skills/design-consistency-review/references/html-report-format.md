# HTML Report Format

## Contents

1. [Scaffold](#scaffold)
2. [Theme toggle](#theme-toggle)
3. [Header](#header)
4. [Fix first](#fix-first)
5. [Finding card](#finding-card)
6. [Evidence patterns](#evidence-patterns)
7. [Style guidance](#style-guidance)
8. [Gaps and Preferences sections](#gaps-and-preferences-sections)
9. [Tone](#tone)

Render the review as a single self-contained HTML file in the OS temp directory. Load Tailwind from the CDN; hand-build everything else: annotated screenshots, swatch grids, side-by-side variant strips, and state matrices. Do not use a diagramming library. Design findings are *evidence*, not graphs: the reader needs to see the two things that disagree, next to each other, at real size.

Self-contained means self-contained. Inline every screenshot as a base64 data URI so the file survives being moved, zipped, or emailed. If that pushes the file past about 10 MB, downscale the images instead of linking to paths that will break.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Design review — {{target}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = { darkMode: "class" };
      // Set before first paint to avoid a flash of the wrong theme.
      if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
        document.documentElement.classList.add("dark");
      }
    </script>
    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         annotation pins, hairline rules over screenshots, swatch checkerboards */
      .pin { font-variant-numeric: tabular-nums; }
      .checker { background-image: conic-gradient(#e7e5e4 25%, transparent 0 50%, #e7e5e4 0 75%, transparent 0); background-size: 12px 12px; }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="fix-first">...</section>
      <section id="findings" class="space-y-10">...</section>
      <section id="gaps">...</section>
    </main>
  </body>
</html>
```

## Theme toggle

The report must ship a working light/dark toggle. This is not decoration: half the findings in a design review concern colour, contrast, and state, and the reader will flip their own product between themes while reading. A report that renders only in light mode cannot be checked against a dark-mode finding.

Rules:

- **Put the toggle in the header**, at the top-right, as an icon button with an accessible label. Use one control with two states; do not add a three-way system dropdown.
- **Default from `prefers-color-scheme`**, set before first paint as shown in the scaffold so there is no flash.
- **Do not use `localStorage`.** The toggle only needs to hold for the session; persistence breaks in sandboxed viewers and adds little value to a document read once.
- **Give every surface a `dark:` pair.** Cover backgrounds, borders, and text. A card with `bg-white` but no `dark:bg-slate-900` becomes a glowing rectangle.
- **Give severity colours separate dark values.** `red-600` on white is right; on slate-950 use `red-400`. Do the same for emerald and amber. Check that all five severity badges remain distinguishable in both themes.
- **Do not theme screenshots.** A light-mode screenshot directly on a dark page reads as a report defect. Put every image in a neutral fixed container (`bg-stone-100` with a border in both themes) so it reads as a specimen rather than part of the page. If both light and dark captures exist for the same surface, show them side by side and label them; do not switch them with the toggle.
- **Never rely on the theme to carry meaning.** Mark leakage, drift, and severity with a label or icon as well as colour.

```html
<button id="theme" aria-label="Toggle dark mode"
  class="rounded-md border border-slate-300 dark:border-slate-700 px-3 py-1.5 text-sm">
  <span class="dark:hidden">Dark</span><span class="hidden dark:inline">Light</span>
</button>
<script>
  theme.onclick = () => document.documentElement.classList.toggle("dark");
</script>
```

## Header

Show the target name, date, and scope line: what was reviewed and how. Then show a compact legend for the severity badges and a one-line statement of the canon, whether documented or derived from the dominant pattern. Do not write an introduction paragraph. Go straight into Fix first.

## Fix first

Place one card at the top. List three to five findings with the best impact-to-effort ratio, one line each, as anchor links to their full cards. Do not add a summary of the summary.

## Finding card

Let the evidence carry the weight. Keep prose sparse and plain.

Use one `<article>` for each finding:

- **ID** — `DR-01`, monospaced and small, before the title. People paste these into trackers.
- **Title** — short and naming the contradiction, such as "Two tab styles for the same navigation."
- **Badge row** — severity (`broken` = red, `inconsistent` = amber, `polish` = slate, `gap` = indigo, `preference` = stone), effort (`S` / `M` / `L`), and the category tag.
- **Where** — monospaced list of surfaces, files, or routes using `font-mono text-sm`.
- **Evidence** — the centrepiece. Use the patterns below.
- **What** — one sentence naming the two instances that disagree.
- **Fix** — one sentence naming which side wins.
- **Notes** (when applicable) — one line in an amber-tinted box for intentional divergence, a blocked decision, or an already merged change.

Do not write paragraphs of explanation. **If a finding needs a paragraph to be understood, the evidence is wrong; rebuild the evidence.**

## Evidence patterns

Choose the pattern that fits the finding. Mix them; readers stop seeing a report where every card uses the same pattern around the fourth card.

### Annotated screenshot (the workhorse)

Put the image in a `relative` container with absolutely positioned numbered pins over it: small circles, `text-xs`, with high contrast against whatever is beneath them. Place a short numbered key below the image. Use this whenever the finding is "look at this specific spot."

Do not annotate more than four points on one image. Five pins means five findings were merged into one card.

### Side-by-side instances (for any "same meaning, different form")

Put two or more tightly cropped screenshots in a grid, each labelled with its origin. This pattern *proves* an inconsistency, so prefer it when the finding is a divergence. Show only the element in question. Mark the winning instance with a small emerald label so the fix is visible without reading.

### Variant strip (for "N implementations of one thing")

Show a horizontal row of every variant found, with its file path or location underneath in `font-mono text-xs`. Eleven button instances in a row make an argument no prose can. Grey out the variants that should be deleted.

### Swatch / token grid

Render colour chips as small squares with the hex value beneath. Group near-duplicates so the drift is obvious; `#3B82F6` and `#3C82F5` next to each other need no commentary. Use the checkerboard class behind anything transparent. Apply the same pattern to radii, shadows, and border widths.

### Scale ruler (for spacing and type)

Render horizontal bars at their actual pixel widths and label them. Use the accent colour for values on the scale and red for off-scale values. One glance should show how many arbitrary numbers are in play.

### State matrix

Build a table with components down the side and states across the top: default, hover, focus, disabled, loading, empty, and error. Use a checkmark for present, an em dash for missing, or a small red marker for wrong. This is the fastest way to show a hole in state coverage and usually produces the most `broken` findings in the report.

### Order mismatch

Place two narrow columns side by side: interaction order on the left, numbered as the user performs it, and visual order on the right, matching top-to-bottom placement. Draw connecting lines with inline SVG where they disagree. Use this only for hierarchy findings. It is the one abstract diagram in the report and should remain rare.

## Style guidance

- Aim for lean editorial, not a corporate dashboard. Use generous whitespace. `font-serif` headings work well against stone and slate.
- Use one accent, indigo or emerald, plus the severity palette. Add no other colours.
- Keep evidence blocks around 320–400px tall so a card fits on screen without scrolling.
- Use `text-xs uppercase tracking-wider` for labels inside evidence blocks so they read as annotation, not UI.
- Hold the report's spacing scale, type scale, and dark mode to the same standard as the findings. A review that flags inconsistent padding while using inconsistent padding undermines itself.
- Allow only the Tailwind CDN and theme-toggle scripts. Do not add app code, filtering UI, or any interaction beyond the toggle.

## Gaps and Preferences sections

Put separate Gaps and Preferences sections after the findings. Use the same card format but make them visually quieter: no badges beyond the category and lighter borders. Do not let them compete with defects for attention.

## Tone

Use plain, concise English. Keep the vocabulary aligned with the skill.

**Use exactly:** canon, drift, instance, variant, token, surface, affordance, state, severity, finding.

**Never substitute:** "issue," "bug," or "nit" for finding; "problem" for drift; "style" for token; "screen" for surface when referring to a surface that appears across screens.

Phrasings that fit:

- "Tabs drift: underline in Settings, pill in Projects. Pill is canon — four other views."
- "Control has no disabled state; it stays live with nothing selected."
- "Eleven button instances; three cover 90% of usage."
- "Off-scale: 13px, 18px, 22px against a 4pt scale."

Never write "clean," "modern," "intuitive," "user-friendly," "polished," or "improves UX." They assert a judgement without evidence, which is exactly what this report exists to prevent. If a sentence could be a bullet, make it a bullet. If a bullet could be cut, cut it.
