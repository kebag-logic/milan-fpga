[A329] REVIEW READY

Head: `691f1d2b3a73705a50a8f827e2bb16837dc0dcdc` on `120-name-wr-export` (local; not pushed).

The donor exports `aecp_name_wr_o` from the descriptor store’s actual live name-write acceptance, with no new state or changed NVM mark timing. Contracts and tests are included. All donor gates pass: 1,014,722 suite checks; 85 focused acceptance checks; the decode-driven mutant builds and fails the required multi-lane, lock-refusal and abort checks, then the restored run passes. Whole-top area is 66,461 → 66,439 mapped LUTs; registers, RAM and DSP are unchanged, with one added output buffer.

**Full acceptance remains blocked at the parent boundary.** Against parent `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`, both integration tops elaborate and the 231-check datapath leg passes with the output omitted. The strict `pp_shadow` suite (rc 2) and parent lint (rc 1) reject the omitted port as `PINMISSING`. An explicit `.aecp_name_wr_o()` open connection is needed. Parent edits were prohibited, so no parent source or warning policy was changed and these failures are retained.

`HANDOFF.md`, `PR-BODY.md`, gate logs, mutant results and area receipts are in the assigned `pp120-a329` output directory. No push, PR operation, merge or hardware operation was performed.
