---
name: write-as-poteto
description: >-
  Write, review, or improve skills using poteto's conventions: explicit intent,
  compact workflows, precise language, and reusable tools for deterministic work.
  Use for "write as poteto", /write-as-poteto, "write a skill", "turn this into a
  skill", "review this SKILL.md", "why isn't my skill triggering", "cria uma
  skill pra isso", or edits to a skill's instructions or triggering description.
  Own skill authoring; poteto-mode owns the broader engineering approach. Exclude
  ordinary prose editing, standalone evaluation systems, and engineering work
  that does not involve authoring a skill.
---

# Write as poteto

## Establish the intent

Before drafting, record four answers from the request and available examples:

- What observable behavior should change with this skill loaded? Name a decision or action, such as putting the condition before the instruction.
- What correction, repeated explanation, or explicitly requested workflow motivates it?
- What would the user actually type to invoke it? Record their wording and a nearby request that should not invoke it.
- Which parts require judgment, and which belong in documentation, a script, a lint rule, a test, or a codebase constraint?

Use supplied conversations as process evidence. Identify the intervention, what the agent was doing, and the corrected behavior. Group repeated interventions by cause. Preserve the condition that made the correction appropriate; do not turn one local preference into a universal rule. Separate the user's decisions from the assistant's unconfirmed suggestions.

For a new workflow without conversation history, use the user's intended steps and a concrete example. Do not invent repeated failures. Ask only for missing information that changes the workflow or its boundaries.

Keep one coherent purpose. Split unrelated workflows. For an existing skill, preserve its purpose and working rules unless the request or evidence supports changing them.

## Encode the process

Write the sequence of decisions, actions, and checks that produces the intended result. State inputs, branch conditions, and completion criteria where they change execution. Replace "be rigorous" with the action that demonstrates rigor.

Keep expertise that changes a decision. Omit explanations a capable model already knows. Use a compact term such as "tautological test" only when it conveys the intended behavior reliably; define unfamiliar terms through a concrete action.

Separate judgment from mechanics:

- Keep interpretation, tradeoffs, and context-dependent choices in the instructions.
- Reuse an existing script or CLI for stable mechanical work. Bundle a tool when agents would otherwise rebuild the same working code each run.
- Put mechanically enforceable prohibitions in lint rules, types, tests, or constraints. Keep instructions for interpreting failures or choosing a remedy.

For a bundled tool, state its path, inputs, output, invocation condition, and failure handling. Run it before relying on it. Do not imply a tool exists when it is only proposed.

Remove command recipes the model can safely infer. Preserve exact commands, symbols, paths, and ordering when they are required for correctness or prevent an observed failure. Keep the intended outcome and verification condition even when implementation details disappear.

Keep the core workflow self-contained. Put lengthy optional schemas or domain references in bundled files, with an explicit reading condition. Do not send the reader to another skill for essential instructions or require reading every resource on every invocation.

## Write the triggering description

Finalize the description after the workflow is stable. Put what the skill does and all selection conditions here, including exclusions needed to distinguish neighboring skills.

- For a workflow, lead with the action, then concrete invocation phrases or situations.
- For a principle, name the specific situation and the decision it changes.
- For a personal mode, trigger on the handle or explicit mode invocation, not generic phrases such as "write code".

Use phrases users actually type. Include nearby boundaries when collisions are plausible. Name another skill only when that distinction or a real handoff is necessary.

Use one YAML scalar, quoted or folded with `>-`. Keep frontmatter to `name` and `description`. Use a short lowercase, hyphenated name. Match the initial folder name to it; preserve managed folder names assigned after installation.

If the skill selects the wrong requests, fix the description before rewriting the body.

## Edit the language

- Use second-person imperatives, active voice, and sentence case headings.
- State the condition before the action when it controls whether the action applies.
- Point to the actual type, config key, command, or file. Avoid vague substitutes.
- Explain a rule only when its application would otherwise be confusing. Keep the reason short.
- Use plain words. Remove filler, invented jargon, metaphors, aphorisms, emoji, and em or en dashes.
- Keep each rule once. Cut repeated warnings, research history, unnecessary dates, and claims that the content is already distilled.
- Add a section only for a distinct decision. Do not force matching sections across skills.
- Number sequential steps when order matters. Preserve stable rule identifiers when other instructions cite them.
- End the authored skill with its deliverable contract: what the agent returns and what evidence belongs with it.

Keep attribution brief if needed. Put the learned instruction directly in the skill; a source link does not replace necessary knowledge. Add links only when consultation is part of execution, with a reading condition.

Length follows the workflow. Cut a sentence if removing it changes no decision, action, or required output.

## Check the behavior

Trace every section to the intent answers. Remove unrelated additions, even when they are good engineering advice.

Validate frontmatter, resource paths, tool invocations, and consistency between the description and body. Structural validity alone does not show that the skill works.

For a checkable workflow, run three to five realistic requests: a normal case, a meaningful variation, and a boundary or failure case. Inspect the actual artifacts or actions against the user's goal. Do not grade a model's claim that it followed instructions or use checks that merely restate the implementation. If execution is unavailable, identify what remains untested.

For voice or style, show representative output to the user and iterate. For comparisons, use fresh context without version labels, intended answers, or words such as "eval", "test", or "judge" in the task prompt. Keep observations separate from the candidate instructions.

## Deliver

Create or update the complete skill and any necessary resources through the available skill-management workflow. Briefly report its purpose, the material changes and cuts, and the checks actually completed. Make the skill available for review. Include the intent answers only when they resolve ambiguity or the user requests them.
