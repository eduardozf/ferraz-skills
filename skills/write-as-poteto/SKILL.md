---
name: write-as-poteto
description: "Write, review, or fix a SKILL.md using poteto's conventions from the pstack corpus (cursor/plugins). Use for \"write as poteto\", /write-as-poteto, \"write a skill\", \"create a skill for this\", \"turn this into a skill\", \"review this SKILL.md\", \"why isn't my skill triggering\", \"cria uma skill pra isso\", \"transforma isso numa skill\", or any edit to a skill's frontmatter, description, or body."
---

# Write as poteto

Conventions distilled from poteto's skills in `cursor/plugins` (pstack). Everything needed is in this file. Don't send the reader to another skill mid-task.

## Start with intent

Before any writing, answer these. If you can't, there is no skill here yet.

1. **What behavior changes?** Name the thing the agent does differently with this skill loaded versus without it. "Writes better docs" is not an answer. "Puts the condition before the instruction" is.
2. **What made you want it?** A correction you've repeated, a workflow you keep re-explaining, a mistake that keeps landing. One instance is an anecdote. Twice is a skill.
3. **What does the user type when it should fire?** Their exact words, not a topic label. A trigger you can't write in the user's own phrasing means the skill has no job.
4. **Is a skill the right container?** A fact belongs in a doc. A rule a machine can check belongs in a lint rule or a test. A skill is for judgment the agent has to exercise in the moment.

Write the answers down before drafting. They become the description, and they are what you check the draft against at the end. Intent drift is the common failure: a skill that starts as "stop over-abstracting" and ends as a general essay on architecture.

If the intent is broad enough to need sections on unrelated things, it's two skills.

## The description

This is the whole triggering mechanism. Two parts: what the skill does, then when to use it.

Pick the opener by type:

- Workflow skill: lead with the verb. `Spawn N reviewers, collect verdicts, reconcile them.` Then `Use for /x, "x this", or <situation>.`
- Principle skill: `Apply when <specific situation>.` Then the imperative in one line.
- Personal style skill: trigger on the handle and `/handle-mode`, never on generic keywords like "write code".

Rules:

- Quote the phrases the user actually types. Three or four beat a category label. "For code review tasks" loses to "review this", "tear this apart", "find blind spots".
- Name the skill you collide with and hand off to it. If two skills answer nearby questions, say which owns what.
- Every "when to use" fact lives here. None in the body.
- One YAML scalar. Quote it, or use `>-` with indented continuation. Escape inner quotes.
- The description decides whether the rest of the file ever runs. Change it last, and if the skill fires on the wrong prompts, fix this before touching anything else.

## The body

- Second person imperative. Tell it to do the thing.
- Skip the reason. Explain only when the rule is confusing or dangerous without one. One clause, not a paragraph.
- Keep it self-contained. Copy in the few rules the skill actually needs. A reader who has to open a second file to follow the first will skip it.
- Point at the real thing: the type, the config key, the command, the file path. Write the actual symbol name, not a description of it.
- Number rules only if something else cites them. Numbered ids are permanent. Removing one leaves a gap; never renumber.
- End with the deliverable contract: what the reply contains, in what shape. Without it the same skill returns a different shape each run.
- Add `## When not to use` whenever a neighboring skill is the better answer.
- Add a section only for a rule that is specific and non-default. "Communicate clearly" is not a section. "Bullets only when the items are genuinely parallel" is.
- Don't force symmetry. Missing sections are correct when there's nothing to say.

Length follows scope. Principles land short, workflows longer, and a router that indexes other skills is allowed to be long. Treat that as a smell test, not a limit: cut sentences that don't change a decision, and stop when everything left does.

## Prose

An agent reads this file every time it fires, so ornament costs on every run.

- No em dashes. Use a period or a comma.
- Sentence case headings. No emoji.
- No bold label plus colon that restates the line. A bold lead-in ending in a period, followed by new detail, is fine.
- Active voice, actor named. "The loader parses the file", not "the file is parsed".
- Plain words. Use, not utilize. Help, not facilitate. Many, not numerous.
- No invented jargon and no abstract metaphor nouns: substrate, wedge, vector, surface, scaffolding, north star. Say the concrete thing.
- No aphorisms, no rhetorical fragments, no personified code. Say what you mean.
- Cut filler. "In order to" is "to". "It is important to note that" is nothing.
- One thought per sentence, but vary the length so it doesn't read machine-written.
- A sentence that could appear unchanged in a different skill says nothing about this one. Cut it.

## Naming

- Workflow: a verb or a short noun the user would type.
- Principle: `principle-<imperative>`, e.g. `principle-fix-root-causes`.
- Personal style: `<handle>-mode`.
- The name in frontmatter matches the directory name.

## Checking the draft

Read it back against the four intent answers. Every section should trace to one of them; anything that doesn't is the essay creeping in.

Then check by type. A skill with a checkable output gets 3 to 5 real prompts, run and read yourself. A skill about voice or style gets shown to the user instead, and expect several rounds. When comparing two versions, keep the test blind: no words like eval, test, or judge where the model can see them, and grade from what it did rather than what it says it did.

## When not to use

- Building an eval harness or a scored comparison across versions. That's measurement work, a different job from authoring.
- Editing prose that isn't a skill file.
- Capturing someone's whole working style rather than one workflow. That's a mode skill, a different shape and a longer interview.

## Guardrails

- **Don't be clever.** Metaphors, aphorisms, and rhythm cost tokens and do nothing for an agent reader.
- **Don't overfit to one conversation.** A preference stated once and contradicted later is noise.
- **Don't write a manual.** A skill is the shortest set of instructions that changes behavior, not documentation of a topic.
- **Don't bury the trigger.** If the skill isn't firing, the description is wrong.
- **Fix a broken skill in its own change.** Don't block on it and don't work around it silently.

**Reply:** the skill's purpose in one line, the intent answers, the description with its trigger phrases, and what you cut and why.