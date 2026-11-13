[A683zo] STOP

Head: `187eeed89235d5ab7ce68bcd4953c7ef118e9245` on `665-s2b-cycles`.
- Nine ordinary commits on round 29's `b2d39235`: the ruling's items 1 to 3 (issuecomment-6828629878).
- Then one merge commit (parents `70e30d7b` and `8bc1dfc0`) of PR #892's round 4 head `8bc1dfc0`, which carries `dev-soft-core` `0fb66211`.
- No rebase, force or amend; nothing pushed. tsn-c-stack stays at `715589c`. This lane makes no RTL or mailbox-contract change; the merge brings `dev-soft-core`'s own.

**Why STOP: at the merge, the size fixture's 8x8/2if image plans 58.5 RAMB36.** The ruling holds it at 58.0, and the owner's decision of 2026-11-12 (issuecomment-6824896581) caps it at 58.5, which the ledger refuses.
- The link reads: `REFUSED: allocation over budget: 58.5 RAMB36 (rom 123808 bytes in 124928, sram 113168 bytes in 114688) exceeds the 58-RAMB36 budget ledgered for 8x8, two interfaces`. It fails the same way on a clean clone of the head, and so does the CPU budget harness's own 8x8 build.
- **Neither side is over alone.**
  - This lane's `rom` already took 61 granules at round 29 (123,112 B), with `sram` 64 B under 55 granules (112,576 of 112,640 B).
  - `0fb66211`'s KLJ3 stage and open bits add about 590 B of `sram` (#823's own table: +576 B at that point), so `sram` takes a 56th granule.
  - The pin move's own composed fixture stays at 58.0 because its `rom` (121,064 B) is a granule smaller.
- **Ways back to 58.0:** cut 928 B of `rom` (to 122,880 B) or 528 B of `sram` (to 112,640 B). Either is a firmware change outside this round, as is a ledger decision past the cap.
- **What this blocks.** The merge moves measured costs: the mailbox answers a register read a cycle later (`3ba76ae7`), and KLJ3 changes the store. So the legs need a re-grade at both points. With the 8x8/2if image refused, that re-grade cannot run, and neither can the four cost controls at the merge or the full gate pass.
- The tree states the overrun in `SPLIT_CONTROL_MEMORY.md` section 5, the entry stays 58.0, and the image is refused by name.

**Done.**
1. **F1 (`cd87c3b2`).**
   - The platform entry is 60.0, refused at 60.5, stated as ROM debt of 4.0 RAMB36 owed to S14.
   - Section 5 states the decision with its link, in place of the superseded criterion and the "waits for a ruling" text.
   - The new gate `tb/verilator/ctrl_split_boot/plat_ledger.py` links the platform image at all four points against each shape's own split export, with the override its point takes. It grades `LINK`, `KEY` (`ctrl_plat` against `ctrl_memory_ledger.py` and the override's key), `TILES` and `LEDGER`, each apart, so a stale key cannot hide an overrun.
   - At the head: 4 of 4 points PASS (platform 39.5 / 43.0 / 53.0 / 59.5) and 7 of 7 planted ledgers graded as required.
   - End to end, the gate fails (rc 1) with the entry at round 29's 59.0 and with a stale `ctrl_plat` key.
2. **F2 (`ef913ca4`), option (c).**
   - One run measures `notice-every-2` on the planted build and on this tree's unplanted image (`run.reference_run`). The control is caught only past a 5 % margin: the 5 % a stated cost carries over its measurement.
   - `CONTROL srp-compared-by-memcmp caught`: 35,908 against 32,866 cycles (+9.3 %), rc 0, on round 29's image.
   - The table rule is unchanged and no stated cost is lowered.
   - The README and section 13 state it. The harness self-test (0 failures, 213 mutants caught, at the merge head too) holds the verdict with four checks and six mutants.
3. **The suggestions.**
   - **S1:** rule windows at each solved row's W and a microsecond either side of 20 ms plus R4's record. "W less two records" is refused (41 SRP records ahead at 20.206 ms, against 42). No solved W alone sees it at this head.
   - **R712-8 S2:** driver test T7, with its plant caught.
   - **S5:** `load_grade.py --check` refuses swapped columns (rc 1 end to end).
   - **S7:** `also` names #892's kill test at the words it fails on in the composed tree. That is its C9 line; its C5 line passes under the plant, at 35 accesses against a bound of 35.
4. **The merge (`187eeed8`).**
   - Eleven conflicts, each resolved from the composed tree.
   - The store marks a record by id with no walk, on KLJ3's counted open set. `nvm_any` leaves both hot lists: KLJ3's is inlined, and the link refused the name.
   - Both entries are keyed on `nvm_stage` 13,594 B. `ctrl_plat` is unchanged at 17,472 / 19,008 / 18,112 / 20,288 B. The ratchet goes through `fw_coverage.py --write`.
   - At the merge: the firmware gate PASS, the store gate (526 tests), the memory test, the hooks self-test (28 of 28, 96 of 96) and the round's three plants.

**Not run at this head, owing to the STOP:** the workflow jobs, the full mutant campaigns, the legs, the four cost controls, `test_builder.py`, `behave`, the split boot runs and the sweep.

Handoff, PR body and receipts are in the lane's output directory (`HANDOFF.md`, `PR-BODY.md`, `receipts/INDEX.md`). That directory is the session's own, not the one the brief named: that one holds round 29's receipts, which the reviews cite.

Asked: a decision on the size fixture's 8x8/2if point at the merge (a cut of 928 B of `rom` or 528 B of `sram`, or the ledger). Then round 30's re-grade and full pass can run.
