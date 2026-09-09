---
name: theo-agent-guidance
description: 'Shape repository instructions in "Theo style" or "T3 Code style" when writing or updating AGENTS.md or equivalent files. Excludes SKILL.md authoring and implementation work.'
---

# Theo agent guidance

## Guidance from Theo

Use these short excerpts from Theo:

> I like ambitious ideas, simple systems, and software that feels obvious.

Describe the maintainer's priorities. Favor instructions that reduce implementation complexity.

> Inferred types over annotations.

Make engineering preferences concrete. Treat them as defaults the developer can override, distinct from language requirements and project invariants.

## Ground the document

Read the existing instructions and the sources named in the task. Inspect relevant code and configuration. Use the target repository's conventions.

Distinguish implemented behavior, agreed direction, and unresolved proposals. Keep temporary task lists out of the document.

## Put the project first

Open with what the product does and who uses it.

- "What matters": constraints that affect product decisions, including performance, supported environments, and user needs.
- "A small glossary": ambiguous terms and roles. Clarify "you," "we," "user," and overloaded words such as "client." Define roles by the work people perform.
- "Where code lives": main packages, their responsibilities, and how they interact. Verify paths; skip component and function catalogs.
- "Taste": engineering choices about types, boundaries, abstractions, comments, and performance.

Use only sections the material needs. Put essential domain context directly in the document so an agent can understand the project without opening the original sources.

## Cover recurring failures

Turn documented failures into specific safeguards. Identify affected clients, entry points, integrations, and shared contracts. Include reverse operations where needed, such as reopening a closed item.

Specify focused verification using the repository's scripts and CI responsibilities.

Keep development procedures in contributor guidance and user workflows in end-user documentation.

## Keep it concise

Replace generic rules with concrete constraints. Keep each instruction in one place.

Link specialized guidance only when needed. Put the reading condition before the link and verify the target exists.

Use short paragraphs and parallel bullets.

## Deliverable

Edit the requested instruction file, or show a draft if requested. Reply with its link, the main changes, and unresolved points that affect the wording.