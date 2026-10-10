---
name: session-closeout
description: >-
  Close out completed project work by documenting current behavior and deleting
  obsolete documentation and related project leftovers. Use for "close out this
  session", "document what we did and clean up", "update the docs after this
  feature", or requests to leave the project current after implementation.
  Exclude historical retrospectives, release-note-only requests, and unfinished
  feature implementation.
---

# Session closeout

Leave the project describing and supporting what exists now. Prefer removing
material over accumulating explanations of how the project used to work.

## Establish the current state

1. Read repository instructions, the session context, and the relevant diff or
   commits. Identify completed behavior, changed interfaces, and replaced
   workflows. Treat the implementation and verified behavior as evidence;
   distinguish them from proposals and unfinished work.
2. If the session context is missing, use the supplied change range or available
   diff. If you cannot identify the completed work, ask for its scope before
   deleting material based on an assumed session.
3. Find the documentation that readers use for the affected behavior. Search
   throughout the project for old names, paths, commands, configuration keys,
   and claims displaced by the change. Follow references beyond the changed
   files wherever they could still mislead a reader.

## Document and subtract

Update the existing canonical documentation with the minimum information needed
to use, operate, or maintain the current implementation. Include changed setup,
contracts, constraints, and non-obvious decisions when readers need them. Create
a new document only when no existing location serves that audience.

For each affected passage or artifact, choose its treatment:

- If it is false, superseded, duplicated, or no longer useful, delete it. Rewrite
  only the part that still has a current purpose. Delete an entire file when
  nothing useful remains, then remove or repair its incoming references.
- If several locations explain the same thing, keep one authoritative
  explanation and link to it only where the link helps readers.
- If a note records completed tasks, abandoned approaches, temporary debugging,
  or session chronology, remove it after incorporating any lasting decision
  into the appropriate documentation. Do not create a session report in the
  repository by default.
- If material supports a currently supported version, required migration,
  audit obligation, or maintained release history, retain only what that purpose
  requires. Age alone does not make it obsolete.

Do not archive obsolete material, append a correction beneath a false claim,
comment out dead content, or add "previously" sections to preserve it. Use version
control for recoverable history unless the project has a continuing need for a
historical record.

Inspect related leftovers beyond prose: unused examples, scratch files,
superseded configuration, dead references, and code or tests left behind by the
completed change. Before deleting them, check callers, scripts, packaging, and
supported workflows. Remove them when their lack of a current purpose is
established. Keep uncertain items and report the missing evidence. Keep cleanup
tied to the completed work and contradictions it exposes; do not expand it into
an unrelated refactor or discard another contributor's unfinished work.

## Verify the remaining project

Search again for displaced claims and references to removed material. Check
paths, links, examples, and commands against the current implementation. Run the
repository's relevant documentation checks; if executable artifacts changed,
run the focused checks for the affected behavior.

Review the final diff for unnecessary additions and accidental loss of still
needed information. Finish when affected documentation agrees with the verified
implementation, obsolete material is removed, and remaining references resolve.
If evidence or checks are unavailable, state the specific unresolved limit.

## Deliver

Apply the documentation and cleanup changes unless the user requested a draft.
Return links to the updated documentation, a brief account of what you removed
and why, the checks actually completed, and any unresolved items. Keep the
closeout summary in the reply rather than adding another project artifact.
