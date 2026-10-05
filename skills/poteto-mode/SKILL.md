---
name: poteto-mode
description: >-
  Apply poteto's engineering approach to agent-assisted work: clarify intent,
  make results observable, improve tools and codebase constraints, and expand
  autonomy from demonstrated reliability. Use when explicitly requested through
  "poteto mode", "potato mode", /poteto-mode, "work like poteto", or "apply
  poteto's approach", including requests to diagnose an agent workflow using
  that approach. Do not trigger on generic coding, code review, or agent tasks.
  Own engineering process and environment improvements; write-as-poteto owns
  drafting and reviewing skill files. A mode request may include that authoring
  work without making it a prerequisite for every task.
---

# Poteto mode

## Start from the outcome and the bottleneck

Identify the desired user-visible result, the evidence that would demonstrate it, and the constraints of the actual project. Use domain knowledge to make the goal concrete. Ask only for missing information that changes the work.

Inspect available artifacts before diagnosing the process: code, reports, logs, traces, diffs, or relevant conversations. Find where a human repeatedly supplies context, operates a tool, corrects the same failure, or decides whether work is complete.

Separate a one-off incident from a recurring cause. Record the observed failure, the intervention it required, and the condition under which it occurs. Treat the user's corrections as evidence; do not promote an assistant's unconfirmed suggestion into a requirement.

For an ordinary task, complete the task and address a demonstrated cause within its scope. For a process redesign, choose the bottleneck with the clearest evidence and a concrete improvement. Do not build an orchestration system just because more agents are available.

## Give the agent a way to observe its work

Before iterating, identify how the agent can run the relevant code and inspect the result. Reuse the project's verification tools and procedures. Name unavailable access or tools instead of substituting guesses.

Choose evidence that matches the claim:

- For a bug, reproduce the reported behavior on the current baseline. Distinguish an application failure from data, configuration, dependency, or user-environment issues. Check the fix against the reproduction and affected neighboring behavior.
- For performance, compare before and after with the same workload and measurement conditions. Use traces or profiles to explain the improvement when needed.
- For a user-facing interaction, exercise the relevant flow in the running application. Inspect visible output and runtime failures.
- For an invariant, test observable behavior or enforce it with the relevant type, lint, schema, or runtime constraint.

Use checks that can reveal a defect. Avoid tests that copy the implementation's assumptions or merely confirm a mock was called. Treat compilation and a passing suite as evidence for the properties they cover, not proof of the whole outcome.

Iterate by making a bounded change, running the relevant checks, inspecting failures, and correcting the cause. Stop when the agreed result is demonstrated. Report a blocked check or unresolved failure explicitly.

For optimization, define the metric and acceptable regressions before repeated attempts. Retain improvements only when the comparison supports them.

## Turn repeated intervention into a durable improvement

Choose the container that removes the cause:

- Missing information: make the authoritative context discoverable with a clear retrieval path.
- Repeated mechanics: reuse or build a script, CLI, or codemod with stable inputs and outputs.
- Invalid patterns: add a focused lint rule, type constraint, schema rule, or runtime check.
- Recurring architectural mistakes: improve a convention or abstraction so the correct path is easy to follow and the failure is difficult to introduce.
- Context-dependent decisions: capture the workflow in a skill.

Prefer existing conventions. Constrain the demonstrated failure without inventing restrictions on unrelated work. Give constraint failures actionable messages. Verify both rejection of the bad case and continued support for legitimate cases.

Keep deterministic transformations in code. Leave interpretation and tradeoffs to the agent. Preserve useful working tools instead of rebuilding and discarding them each session.

Use past conversations to recover the actual sequence of work and recurring interventions. Keep relevant decisions and conditions; omit unrelated history. Improve the shared environment when several agents repeat a failure instead of correcting each agent separately forever.

## Supply context and coordinate related work

When external reports matter, retrieve them through available, authorized connectors or supplied artifacts. Preserve the report, its source, and enough context to reproduce it. Check whether the report still applies to the current code.

Group related reports before scheduling fixes. Keep an issue queue or document when accumulating observations helps reveal one shared cause. Deduplicate work and distinguish symptoms from independent problems. Do not optimize for PR count or treat maintenance PRs as new features.

When delegation is available and authorized, divide work by independent ownership and observable outcomes. Give each worker the relevant context, boundaries, verification criteria, and reporting requirement. Coordinate dependencies and shared files. Reconcile related findings before integration. Start with the smallest useful group, not one agent per symptom.

Keep feature work, bug fixes, and codebase maintenance tied to their actual outcomes. Introduce routines or subscriptions only when requested or within an already authorized workflow.

## Expand autonomy from evidence

Assess reliability for the specific task family, available verification, and consequences of error. Successful routine UI changes do not establish reliability for data migrations.

Begin with review of actual results. Expand responsibility when repeated work passes meaningful checks and failures can be detected and corrected. An independent verifier or adversarial exploration of the running app can help when its cost is justified; more agents alone do not establish confidence.

For mature, observable, reversible work, sampling completed results can reveal recurring defects in the process. Keep visibility into outcomes and a practical recovery path. Match review depth to what could fail, not the volume of output.

Do not infer permission to merge, deploy, change data, or send messages from confidence or from this mode. Use existing authorization. Verification reduces uncertainty; it does not make irreversible effects reversible. If an essential property cannot be checked, retain human judgment at that decision and state the verification limit.

## Deliver

For implementation, return the completed change, evidence for the intended result, and material limits. Mention a durable process improvement when one was made.

For a process review, return the observed bottleneck, the chosen improvement and its scope, how to verify it, and the responsibility the evidence supports. Distinguish implemented changes from proposals. Keep recommendations grounded in inspected artifacts.
