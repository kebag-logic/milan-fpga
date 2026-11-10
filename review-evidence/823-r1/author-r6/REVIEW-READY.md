[A753f] REVIEW READY
Commit: `2905c8749a4573450b9999dd546bb20ae5c7fc38` on the new branch `823-format`, for the new PR to `dev-soft-core`. It is not pushed: this round may not push.
- It is round 4's `30ca4b21` plus seven commits. The merge base is `dev-soft-core` `1d6bf555`, still the remote tip when this was posted.
- Nothing of the save path is on it. Branch `823-nvm-format` (#876, PR #863) is untouched at `7c97e99f`.
- Every item below was written again on this branch. None was cherry-picked.

Changed, by item of the round 6 ruling (PR #863 issuecomment-6767385787):
- **N1** (`249cca50`). SPLIT_CONTROL_MEMORY reports what the `c20ed894` run printed: 3,344 against 13,264 bytes, the KLJ2 stage sizes. It points to section 5 for both formats' sizes.
- **N2** (`249cca50`). QSPI_FLASHBOOT names each reserved range's owner, as FASTCONNECT section 5 does:
  - the split's store writes `journal_klj3`;
  - the all-fabric writer owns `journal`, whose two headers the split store reads and never writes;
  - `user` has no owner.
  The "nothing writes or reads them" and blank-flash text is gone.
- **RS5, RS6** (`249cca50`). FASTCONNECT's contents entry and status row name `journal_klj3`.
- **RS-a** (`64c3565e`, `e0adcc09`). "(#665, the split placement's saved-state store)" is in `nvm_klj2.c`, `nvm_klj2.h` and `nvm_shape.h`.
  - The same wording replaces the lane label in the branch's other comments: `nvm_layout3.h`, `nvm_layout3.py`, `nvm_klj3.py`, `check_nvm_klj3.py`, `endstation_builder.py` and `test_builder.py`.
  - Runtime messages and the page's generated labels are unchanged.
- **RS-b** (`64c3565e`). `nvm_klj3.py` in the six places in `test_nvm_write.cpp`. `nvm_rig.cpp` and `test_nvm_boot.cpp` keep `nvm_klj2.py`, as ruled.
- **RS-d** (`64c3565e`). `scripts/nvm_klj3.py` as the fixture's source in `nvm_rig.hpp` and `nvm_suite.hpp`.
- **R806-5 R2** (`8e29bc74`). The page says "The room, taken from the all-fabric worst case (404.71 ms) and so conservative for the split, is 95.29 ms". The drift gate holds both figures, and the PR body uses the same wording.
- **SG3 = S-a** (`4d0353e3`, `2905c874`). `LINE_CITE_RE` refuses `path:N`, a range, a list, an unquoted path, "`path` line N" and a `#L` link.
  - There are six plants, one per form. Each is caught by a finding that names the whole citation.
- **SG4 = S-b** (`0d9e9b50`). The codec must compile at 255 input entries (`at_width`). The control `mapin_limit_one_early` (`>= 255u`) is caught.
- **S-c** (`0d9e9b50`). `nvm_shape.h` raises `#error` on `NVM_DOCTORED_MAPIN` without `NVM_HOST_TEST`, which only the host suite's own builds define (`nvm_bench.build_suite`).
  - `doctored_outside` requires the refusal in its words, and the control `doctored_error_removed` is caught.
  - Test plan row T17 and the store README say so.
- **Section 4 under #876** (`8e29bc74`). The page's status line, contents, section 4 lead, sections 3 and 9, and the test plan's state cells (through the generator) say the save path is designed here and built under #876. The PR body says the same.
- **#818 waiver** (`8e29bc74`). Section 7 says area under #818's gate is waived for this format, and names the memory plan as the evidence.
- **The boundary fix** (`2905c874`). The first full run on `e0adcc09` found one defect: the firmware boundary refused the drift gate as an unregistered firmware builder. The cause was that S-a's list-form plant cited a path under `sw/firmware/ctrl_nvm`. That plant now cites `scripts/nvm_klj3.py:408,465`.

**#818 waiver evidence**, against `dev-soft-core` `1d6bf555`:
- **HDL.** `git diff --name-only 1d6bf555 2905c874` lists 67 files. None is a `.sv`, `.svh`, `.v`, `.vh` or `.vhd` file, or under `hdl`, `syn` or a submodule.
- **Gitlinks.** None changes: the six submodule pins are equal at both commits.
- **Tracked generated RTL.** Nothing under `configs/generated` changes.
- **Generated SoC RTL.** The shipping AX7101 SoC was elaborated at both commits with its own launch line and no vendor run.
  - The init files, constraints and build script are byte-identical.
  - The Verilog (31,917 lines) and the Tcl are identical, apart from each clone's path, the two date lines and the order of the hierarchy comment's siblings.
- **Area.** The memory table at `30ca4b21` (SPLIT_CONTROL_MEMORY section 5) is the evidence: the ledgered 8x8 two-interface point plans 57.5 RAMB36, its ledger. At this head the store's freestanding RV32 build has the same section sizes as at `30ca4b21`, at all five shapes.

Validation. Every run is on a fresh clean clone of `2905c874` unless stated, and every clone was clean after its job. The receipts are in the round's receipts directory, with SUMMARY.md and an INDEX.md generated from the files present.
- **Workflows.** Every `run:` step of `rtl-fast` (with `cd tests && behave`), `elaborate`, `rtl` (as for a ready PR) and `docs`: 152 ran, all rc 0, and 0 are bad.
  - 145 ran at the head.
  - The 7 steps of `rtl-fast firmware-unit` passed at `e0adcc09`. That head differs from this one only by the plant string in `scripts/check_nvm_format_32x32.py`, which that job neither names nor scans.
  - 198 did not run, each for a stated reason: hosted-only steps, tool installs replaced by the pinned tools, and the Verilator shards the sweep covers.
- **Builder bank.** `test_builder.py --require-rv32`, in the docs legs and in the elaborate legs (`--require-elaboration`): each union is `107 gates exactly once`, rc 0.
- **Store self-test.** `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8`: rc 0, `OK across 5 shape(s), 506 tests, and all 132 planted defects reddened`. That is 127 planted defects and five compile-time controls.
- **Drift gate.** `check_nvm_format_32x32.py` prints `0 finding(s)`. Its `--self-test` prints `self-test: PASS`: all six line-number plants are caught, and `control moved-lines: 0 finding(s)`. The same holds in the docs workflow's NVM record-space step.
- **Other workflow gates.**
  - `behave`: 14 features, 508 scenarios and 2,330 steps passed.
  - The control mutants: `570 of 570 caught`. The AECP and SRP campaigns: `test_ctrl_firmware: PASS`.
  - The firmware boundary: `ctrl_boundary: PASS`.
  - The LiteX simulations: 8 of 8 PASS.
  - The saved-state writer gate: `OK across 5 shape(s), and every planted defect reddened`.
- **Full sweep.** Four shard units at the head; the shard holding `capture_coherence` ran on 4 CPUs.
  - 64 suites passed, 0 failed, 0 in-suite failures.
  - `capture_coherence` hit its 2,400 s wall clock in its shard, which makes the result unknown, not a failure. Run again alone on 4 booked CPUs, with the sweep's own timeout and masked-verdict check, it passed: 2,262 s, 21,721 checks, 0 failures. So 65 of 65 suites pass.
  - Every preflight passed, suite cancellation included. No #833 symptom appeared.
- **Diff check.** `git diff --check 1d6bf555 2905c874`: rc 0.
- **Earlier runs, kept and not counted.**
  - On `e0adcc09`, the boundary refusal above was fixed by `2905c874`.
  - Builder leg 1 timed out twice under host load: once in `test_nvm_firmware.py --self-test` (1,200 s), and after a restart in `test_soc_options.py` (300 s). On a booked CPU range it passed.
  - A host restart near 18:00 cut five runs: the boundary, docs leg 0, yosys shard 3, the sweep and the store self-test. Each ran again from a fresh clone.

Acceptance criteria (round 6 ruling item 1 and this round's assignment):
- Items 2 to 5 of ruling 6754858510, RS-d and R806-5 R2, each written again on this branch: **met**, as listed above.
- Nothing of the save path: **met**. The store keeps the whole-image commit, and no append-path file or text is added.
- The page and the PR body say section 4 is designed here and built under #876: **met**.
- #818 waived while the head changes no HDL, gitlink or generated SoC RTL, shown against `1d6bf555`, with the memory table at `30ca4b21` cited: **met**, as above.
- PR-BODY.md says "Closes #823": **met**.
- The STOP condition does not apply: every accepted item was built without the save path.

Open risks/questions:
- **Partial generated-RTL comparison.** The Arty shipping SoC's launch line fails at both commits in the local LiteX environment (no PLL configuration for its clocks), so only the AX7101 SoC is compared. The split SoC (`--ctrl-mailbox`) needs a firmware image; its memory is the memory table's evidence, as ruled.
- **Local evidence only.** Hosted CI has not run on this head, which is not pushed.
- **Found, not changed:** the `Bench` docstring in `nvm_bench.py` says "how nvm_klj2.py packs them", but `make_bench` frames its records with `nvm_klj3.py`. It is outside the ruled lists.
- **PR body issue keyword.** PR-BODY.md uses "Closes #823", as this round's instruction says, not the template's "Relates to". It also relates #876 and #877.
