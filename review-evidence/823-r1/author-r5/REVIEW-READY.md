[A753e] REVIEW READY
Commit: `7c97e99f53ab0efc3e05e4617ee652dbab6e1b14` on `823-nvm-format`, for PR #863 to `dev-soft-core`. It is not pushed: this round may not push.
It is four commits on round 4's `30ca4b21`. The remote `dev-soft-core` was still at `1d6bf555` when this was posted, so nothing was merged.
This is posted on #823, not on PR #863 as the ruling says, because this round may post only on #823.

Changed, by item of the round 5 ruling (issuecomment-6754858510):
1. **The split store's append-only save path** (`sw/firmware/ctrl_nvm`), decisions 3, 4, 5 and 7:
   - A slot is a base and a log of deltas behind it, from the page after the base.
   - A save appends the records whose staged bytes changed, as one delta of at most 28 pages with a sequence above the last. It never erases.
   - The boot walks each slot's log. A walk counts only when two reads agree, as a refusal does. It then replays the chosen slot's deltas into the stage, up to the end the walk found.
   - A torn delta, or a delta that fails, makes the next write a compaction.
   - A compaction writes the stage as a base into the other slot, at the authoritative slot's sequence, one page at a time. It yields to a save between pages. A record cut by a page boundary is carried whole to the next page.
   - Once the base verifies, the deltas the old slot took during the compaction are copied behind it. Then the authority moves, and the next delta's higher sequence ends the tie.
   - The other slot is prepared in the background. Every page is read blank. A written block is erased once and read again. After three failed preparations it stops until reset.
   - A save during that erase suspends it (PES), times the suspend, programs, verifies and resumes it (PER). The port gains `suspend` and `resume`.
   - The firmware first-dirty window is 150 ms (`NVM_WINDOW_MS`). `T-NVM-COMMIT-TIMEOUT` is 500 ms per append (`NVM_APPEND_TIMEOUT_MS`).
   - The page's drift gate holds those two, the segment cap and the suspend room to the page's figures.
   - The save path reaches the flash only through the store's own LiteSPI port. The processor, `KL_nvm_backend` and `milan_baremetal.c` are unchanged, so the STOP condition does not apply.
   - Tests:
     - `test_nvm_journal.cpp`: 23 tests;
     - `test_nvm_bound.cpp`;
     - the write tests, rewritten on the append path;
     - a power-cut sweep of a compaction.
   - The reference gains its journal (`klj3_delta`, `klj3_slot`, `klj3_slot_decode`), and its gate has 3 more plants.
   - The store's self-test has 183 planted defects, up from 127, and 8 controls, up from 3.
   - Two guards of a delta's walk have no planted defect: a record header past the segment's end, and a payload past it. The record rules and the pad rule refuse every delta either guard would, so no verdict can tell a store without them (store README).
   - **The 32x32 worst case.** The store runs at 32x32/2if TDM8, with the flash model at tSE 3 s and tPP 5 ms and the suspend at its typical 15 us.
     - `save_bound` measures the change to read back: 321,274 us during the erase and 325,187 us during a compaction, against 500 ms.
     - The page's arithmetic gives 304.71 ms plus the suspend. That leaves 95.29 ms for the suspend, 6,352 times its typical 15 us.
     - `commit_deadline`: twice the worst append is 350,374 us (the worst append is 175,187 us), within the 500 ms deadline.
     - The writer times every suspend. `suspend_us_max` is the longest, and `suspend_slow` counts each one longer than the 95.29 ms room.
2. **N1.** SPLIT_CONTROL_MEMORY reports what the `c20ed894` run printed: 3,344 against 13,264 bytes. It points at section 5 for the KLJ3 sizes.
3. **N2.** QSPI_FLASHBOOT now says who reads and writes each reserved range, as FASTCONNECT section 5's table does. The "nothing writes or reads them" and "blank-flash responder" sentences are gone.
4. **Residue.**
   - RS5 and RS6 are fixed in FASTCONNECT.
   - RS-a: "(#665, the split placement's saved-state store)" in `nvm_klj2.c`, `nvm_klj2.h` and `nvm_shape.h`, and in this change's other comments.
   - RS-b: the rewritten write tests name `nvm_klj3.py`. `nvm_rig.cpp` and `test_nvm_boot.cpp` keep theirs, as ruled.
5. **Suggestions.**
   - S-a: `LINE_CITE_RE` also refuses a range, a list, an unquoted path, "`path` line N" and a `#L` link, each with a plant.
   - S-b: the codec compiles at 255 input entries, and a control moves the limit one entry early.
   - S-c: `nvm_shape.h` has an `#error` for `NVM_DOCTORED_MAPIN` outside the host test's build, with a control.
6. **Area.** #818's gate is a routed Vivado gate, and this round runs no Vivado, so it was **not run**. The split memory plan was linked instead, on clean clones of `30ca4b21` and this head, with the pinned SDK:
   - The append path adds 5,280 B of `rom` at every point (5,288 at 8x8 with one interface), and 800 to 1,248 B of `sram`.
   - 1x1 goes from 37.5 to 39.0 RAMB36, 1x1 with two interfaces from 41.0 to 42.0, and 8x8 from 51.0 to 52.5.
   - **8x8 with two interfaces plans 59.5 RAMB36 against its ledgered 57.5, and `ctrl_srp_image.py --ledgered-point` refuses it.** `30ca4b21` reproduces the ledger's 57.5 exactly.
   - SPLIT_CONTROL_MEMORY records this table. The ledger is not moved.

Validation: every run is on a fresh clean clone of `7c97e99f`, except the sweep (below). Receipts are in the round's receipts directory, with SUMMARY.md and an INDEX.md generated from the files present.
- **Workflows.** Every `run:` step of the four workflows a pull_request to `dev-soft-core` triggers: `rtl-fast` (with `cd tests && behave`), `elaborate`, `rtl` as for a ready PR, and `docs`.
  - 30 jobs. 152 steps ran, all rc 0, and every clone was clean after its job.
  - 198 steps did not run, each with its reason in the receipts' not-run table. Most need the hosted context or a sudo install, or are the hosted shard and union jobs that the sweep replaces.
- **The builder bank**, `test_builder.py --require-rv32`, ran in its two legs in `docs`, and in `elaborate` with `--require-elaboration`. Each union is `107 gates exactly once`, rc 0.
- **The LiteX simulations**: 8 of 8 PASS.
- **The saved-state writer gate**: `OK across 5 shape(s), and every planted defect reddened`.
- **The store's suites** (`firmware-unit`): `OK across 5 shape(s), 728 tests`, with the bound figures above. The coverage ratchet passes.
- **The control mutants**: `570 of 570 caught`. The AECP and SRP campaigns are rc 0. `behave`: 508 scenarios passed, 0 failed.
- `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8`: rc 0, `OK across 5 shape(s), 728 tests, and all 191 planted defects reddened` (183 planted defects and 8 controls).
- **The drift gate**: `check_nvm_format_32x32.py` prints `0 finding(s)`, and its `--self-test` prints `self-test: PASS`.
- `make twin` and `make twin-plants`: rc 0. `twin: 0 finding(s)`, and each of the 20 plants is refused twice.
- `git diff --check 1d6bf555 HEAD`: rc 0.
- **The full sweep**, four shard units on 4 CPUs each, ran at `b6a60fbd`. The shard holding `capture_coherence` had 4 CPUs.
  - 65 of 65 suites PASS, 0 timed out, 2,192,899 checks, 0 in-suite failures.
  - Every preflight passed, suite cancellation included. No #833 symptom appeared, so nothing was re-run.
  - It stands for this head: `b6a60fbd..7c97e99f` changes 8 files under `sw/firmware/ctrl/test` and `sw/firmware/ctrl_nvm`, and no sweep suite reads any of them (SUMMARY.md).
- **Earlier runs.** Each found a defect, fixed by a later commit. The gates above then ran at the fixed head, the sweep excepted as stated:
  - `b6a60fbd`: `firmware-boundary` refused the page gate as an unregistered builder. Fixed by `d01c66ad`.
  - `d01c66ad`: the control mutants caught 569 of 570, and the store's self-test missed 12 planted defects. Fixed by `a9c6391f` and `7c97e99f`.
- **A planned host power-off** cut four runs at this head. Each ran again from a fresh clone. Their partial logs are kept and not counted.

Acceptance criteria (the ruling's "done means"), on a clean clone of the head:
- Items 1 to 5 committed and gated: **met**, in `b6a60fbd`, `d01c66ad`, `a9c6391f` and `7c97e99f`, with the evidence above.
- Item 6 committed and gated: **not met as ruled**. #818's routed gate needs Vivado, which this round may not run. The split memory plan was measured instead, and it refuses the 8x8 two-interface ledger (open risks).
- Every `run:` step of the `dev-soft-core` workflows passes on a clean clone of the head: **met**. 152 ran, all rc 0. The 198 that cannot run here each have a reason.
- The twin and `twin-plants` re-run: **met**, rc 0.
- The full sweep, the builder bank, the store's self-test and the drift gate: **met**, all rc 0. The sweep ran at `b6a60fbd`, for the reason above.
- The shipped 1x1 and 8x8 images keep their behaviour apart from the format: **met**. The processor, `KL_nvm_backend`, `milan_baremetal.c` and every HDL file are unchanged. The builder's diff is two comments, and no tracked generated output changed.
- `dev-soft-core` did not move, so no merge was needed.

Open risks/questions:
- **Decision needed: the 8x8 two-interface ledger.** The append path does not fit the owner's 57.5 RAMB36 (rulings 6412739248 and 6425357821): it plans 59.5. No CI gate plans the linked image, so no gate fails today. The options are to raise the ledger, or to shrink the store or another tenant.
- **#818's route was not run** (no Vivado this round). It needs a ruling, or a round that may run Vivado.
- The target platform's image was not linked again: `ctrl_plat_image.py` takes the store from its own tree. SPLIT_CONTROL_MEMORY records that at `b8628704` its ledgered point had 1,928 B of `rom` left before its next bank. That is less than the 5,280 B the fixture gained.
- The TAKEN comment said authority moves when the new base verifies with a higher sequence. As built, the base takes the authoritative slot's sequence, and the old slot's newer deltas are copied behind it. Both slots hold every value a save reported when the authority moves, and the next delta's higher sequence ends the tie (format page section 4, rule 4).
- The stage stays the whole container, and the page and the carried record sit beside it. A stage of only those bytes would need compaction to stream from the owners. That is not built (format page section 3).
- The suspend latency is graded at the datasheet's typical 15 us, which has no maximum. The real part's latency, timing and power cuts are unproven without the board.
- Hosted CI has not run on this head, which is not pushed. The evidence above is local.
- Found, not changed: the header comments of `nvm_rig.hpp` and `nvm_suite.hpp` still name `scripts/nvm_klj2.py` as the fixture's source. It is `nvm_klj3.py`. They are not in the ruling's residue list.
