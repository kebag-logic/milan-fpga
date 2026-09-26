[A327] TAKEN

Branch: `509-pp-descriptor-ownership`
Base: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`
Processor pin: `990f96526bb89356c963a260ebbdcf2a77e6623a`

Authoritative references: #509 and assignment comment 5844867005;
REQUIREMENTS.md REQ-VER-03/04; processor memory-map section 3.1;
processor issues 38, 39, 60, 82 and 89.

Interpreted scope: publish the L1-L10 and ADP ownership matrix,
decode all five tracked configurations, and distinguish construction
from discriminating refusals. Reconcile identity bytes and update the
parent contract. Record exact processor wording for its separate change.
Keep #478, #464 and #495 repairs with their existing owners.
New product findings will be listed for maintainer filing.

Validation plan: full builder test with the pinned SDK and without
a compiler; generator self-test with its #464 state recorded;
NVM, bare-metal, documentation, CI, style, source-list, lint,
traceability and behavior gates specified in the assignment.

Roles: author [A327]; independent reviewers [R330] and [R331].
The public readiness decision is recorded; board moved to In progress.
Blockers: none. Publication and merge remain with the maintainer.
