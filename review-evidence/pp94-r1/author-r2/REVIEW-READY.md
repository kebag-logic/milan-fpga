[A252] REVIEW READY

Local head: `2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f` (branch `94-desc-mem-guard`).

Round 2 addresses R290-2 F1 = R291-2 F1 and R291-2 S1-S4. Both PNGs are
regenerated at the required widths and visually checked. The new priority
test passes at 78/78; the inverted-priority mutant fails only its new
completed assertion (77 PASS / 1 FAIL, make rc 2).

Every repository CI gate and all five requested parent consumer gates
returned 0. Full source bank: 32 suites / 15,895 checks. NVM figures:
46 builds. Parent simulation: 371 checks. The parent index was restored
byte for byte, and its submodule checkout remains at this source head.

`HANDOFF.md`, the full replacement `PR-BODY.md`, and receipts are ready in
the round-2 packet `2026-09-23/pp94-a252` for manager archival. No push, PR
edit, merge, parent commit, or hardware operation was performed. Independent
re-review and the manager's publication and remaining gates are pending.
