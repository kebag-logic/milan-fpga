[A656] REVIEW READY (round 3, PR #768)
Commit: `1e914414557874648ac5041aff88b96908e0e053` (branch `637-map-records`, local, not pushed; three commits on `8000520c`, no rebase or amend; processor pin `2cbed0a9` unchanged; no file under `hdl`, `syn` or `constraints` changed). Answers R669-2 and R670-2 under the round-3 assignment (PR #768 comment 6295599722).

Changed:
- R669-2-F1 (`dc7dd727`..`600565b4`): `tb/verilator/milan_dp/sim_nxn.cpp` `maprec_lone_record_section` adds four windows. Each holds one framed map record failing one term of the validated-record test: its crc16 (a payload byte changed under it), or its layout, id or magic (each re-sealed). Each case grades every port on its reset set and PP_STAT done 1, busy 0, fail 0, blank 1 (D3 3 rule 7, 8.7). `dynmap_mutants.py` rows 61 to 63 each remove one term of `amr_rs_valid_r`'s condition: crc16, layout and id, magic and length. Each is caught by its named blank check (1, 2 and 1 failures of 649).
- R669-2-F2 (`dc7dd727`): REGISTER_MAP's PP_STAT paragraph and `[3]` row, and D3 8.7, now say the map restore adds no cause of its own. `[20:18]` reads 0 because it runs only after a D3 walk that ended with none. `[22:21]` keeps the binding walk's.
- R670-2-F1: the validation account below, the PR body and the handoff now separate the round-2 campaign runs.
- `1e914414`: the milan_dp README campaign table (re-measured) and the Makefile count; TESTING.md's count is in `600565b4`.

Validation (round 3; clean clones, unpiped, one log and rc each):
- `make -C tb/verilator/milan_dp dynmap`, `maprec8`, `maprec4` at `1e914414`: rc 0 each; 649/0, 219/0, 137/0.
- `make -C tb/verilator/milan_dp_render tdm8render-build` (rc 0), then `make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=4` as one full command at `600565b4` (differs from the head only in the milan_dp README and a Makefile comment): **rc 0**, 68 checks, 68 PASS. Five clean legs pass and 63 of 63 controls are caught.
- docs.yml, the same 95 commands as round 2, at `1e914414`: all rc 0.
- Builder legs 0 and 1 at `1e914414`: rc 0, rc 0. Builder gate 11 is declared NOT RUN by the builder, as in round 2.
- Not rerun, because no file they read changed: route-1x1, ooc-1x1, ooc-8x8, xvlog and the full Yosys run. Round 2's rc 0 records at `887b6bf2` and `af5eefc6` stand.
- Superseded, not cited: a first builder launch refused within a second in both legs, because the scratch clone's `tsn-c-stack` origin was not the `.gitmodules` URL. After `git submodule sync` it reran from the start.

Round-2 account, corrected (R670-2-F1). This corrects the round-2 REVIEW READY (comment 6294768287), which listed this campaign under "all rc 0":
- The full `dynmap-mutants` campaign at `af5eefc6`, from a fresh clone: **rc 2**, 65 checks, 63 PASS, 2 FAIL. The two FAILs are the listener leg's clean run and its row-36 mutant: the clone held no `milan_dp_render` build ([receipt](https://github.com/kebag-logic/milan-fpga/blob/180fc3a8e01eb0022b77b504b4709c3e8a3194a4/review-evidence/637-r1/author-r2/receipts/round2/campaign/campaign-af5eefc6.log.excerpt)).
- The listener rerun at `af5eefc6`, after `make -C tb/verilator/milan_dp_render tdm8render-build` (`python3 dynmap_mutants.py --jobs 2 36`): rc 0, 2 checks, 2 PASS ([receipt](https://github.com/kebag-logic/milan-fpga/blob/180fc3a8e01eb0022b77b504b4709c3e8a3194a4/review-evidence/637-r1/author-r2/receipts/round2/campaign/campaign-row36-af5eefc6.log)).
- Aggregate across those two executions: 60 of 60 caught and five clean legs passed. The full campaign command itself did not exit 0.
- Synthesis is separate: the full Yosys run at `af5eefc6`, rc 0; route-1x1, ooc-1x1 and ooc-8x8 at `887b6bf2`, rc 0.

Acceptance criteria: unchanged from round 2. Items 1 to 4 and the #763 desk items are met. The on-board cold cycle is NOT done (no bench access), so the PR stays "Relates to #637".

Open risks/questions: the residue (R670-2-R1 to R3, R669-2 RES-1 to RES-5) is left for the merge checklist, per assignment item 4. Only R670-2-R3, the PR body's role lines, is applied, because this round rewrites those lines anyway. R669-2's suggestions S1 to S3 were not assigned and are not taken. The PR body and receipts for this round are in the lane's output; nothing is pushed.
