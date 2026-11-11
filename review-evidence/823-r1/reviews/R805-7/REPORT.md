[R805] POSITIVE - exact head 2905c8749a4573450b9999dd546bb20ae5c7fc38

# R805-7: composition review of the #823 merge-train candidate (PR #880)

- **Role:** internal independent reviewer, cleared context.
- **Head under review:** PR #880 head `2905c8749a4573450b9999dd546bb20ae5c7fc38`, tree `c28f687748dec7d97d4346844d5bfce183aa010d`. This is the same head R805-6 and R806-6 reviewed, both POSITIVE.
- **Composition under review:** candidate `e282ecd2691bdf2018d31376d3930c984a2c0499`, tree `466d464aee94d3086419197f23e0fa862e65db16`. Its parents are `663555fd` (tree `9b067a62`, which is `dev-soft-core` `764482b4`'s tree, S7 / PR #874 merged) and `2905c874`. The merge base is `1d6bf555`.
- **Scope, as assigned:** the composition delta only. Code that the composition does not change keeps its R805-6 / R806-6 lens verdicts.

## Verdict

POSITIVE. The composition keeps both sides' intent. Every reader of the one overlapping file passes at the candidate. So do the two S7 gates that compile #823's changed store, and no bank had run either of them.

- No BLOCKER, MAJOR or MINOR is open.
- One new RESIDUE (C-RS1) and two SUGGESTIONs are recorded.
- The two RESIDUE items of the prior rounds (RS1, RS2) are still present and carried.
- All five lenses are covered clean for the composition delta.

## What I checked, and how

### 1. The candidate is the merge it claims to be

Receipt: `receipts/composition.txt`.

- I recomputed `git merge-tree --write-tree 764482b4 2905c874` independently. It gives `466d464a`, which equals the candidate's tree. The merge is clean.
- `origin/dev-soft-core` is still `764482b4`, and PR #880's base is `dev-soft-core`.
- The six gitlinks are identical on `2905c874`, `764482b4` and `e282ecd2`: `external` efeb541a, `gptp-processor` 135afd04, `protocol-processor` a9e84b66, `third_party/lwSRP` 08ee86e8, `third_party/tsn-c-stack` 70936b77, `third_party/verilog-axis` 48ff7a7e.
- Since `1d6bf555`, the only file both sides changed is `sw/firmware/ctrl/test/ctrl_configs.py`. S7 changed 16 files and PR #880 changed 67.

### 2. Composed `ctrl_configs.py`: nothing lost, duplicated or contradictory

Receipts: `receipts/ctrl_configs.{s7-side,pr880-side,composed}.diff`, `composition.txt`, `dupkeys-e282ecd2.txt`, `probe_registry-e282ecd2.txt`.

- **Union.** S7 adds 8 lines and #823 adds 7. The composed diff from the merge base adds 15, the exact multiset union of the two, and no side removes a line.
  - #823's four `OUTSIDE` entries are at `:179-185`: `nvm_layout3.py`, `nvm_klj3.py`, `check_nvm_klj3.py` and `nvm_format_32x32_tables.py`.
  - S7's `OUTSIDE` grader `srptx_grade.py` is at `:242-244`, and its `SUITES` entry `srptx_mutants.py` is at `:272-276`.
  - Each side's entries sit in their own hunk, with no interleaving.
- **No duplicates.** `dupkeys.py` checks every dict display in the file by AST. It finds 49 constant keys and 0 duplicates. Python would silently keep the last of a duplicate key, so a textual check is not enough here.
- **All six keys exist** as files at `e282ecd2`.
- **Each entry carries weight.** `probe_registry.py` imports the candidate's own `ctrl_configs` and runs its text finder, `builder_texts`.
  - It finds 64 builders by text. Each of the six composed keys is among them, and none is covered by `BUILDERS` or `PART_OF`.
  - Four are programs and two are not. `held()` at `ctrl_configs.py:373` would refuse each of the six by name if its entry were missing.
  - So the boundary gate's PASS below is direct evidence that both sides' entries are present and in effect.
- **The values are prose.** The reason strings are only membership-read (`:373`).

### 3. The readers of `ctrl_configs.py` at the candidate

Environment for all runs:
- RV32 compiler: the pinned Bootlin SDK, `riscv32-ilp32d--glibc--stable-2025.08-1`, gcc 14.3.0. `scripts/ci_rv32_sdk.py --verify-only` returned rc 0 (`receipts/sdk-verify.txt`).
- Submodules: real clones at their gitlinks.

The assignment names `test_ctrl_firmware.py` and `test_ctrl_nvm.py`. Neither imports `ctrl_configs.py`: `test_ctrl_firmware.py:137-147` has no such import, and `test_ctrl_nvm.py` only names it in its docstring. Its reader is the TSN stack boundary gate `ctrl_boundary.py:132`, which runs both scripts as builders. I ran all three.

| Gate at `e282ecd2` | Result | Receipt |
|---|---|---|
| `test_ctrl_firmware.py --require-rv32 --jobs 6` | rc 0, `test_ctrl_firmware: PASS`, 72 `RESULT: PASS`. The RV32I freestanding build ran (1 check, 0 failures). No arm was SKIPPED or REFUSED. | `receipts/ctrl_firmware.{log,rc}` |
| `test_ctrl_nvm.py --require-rv32 --self-test --jobs 6` | rc 0, "OK across 5 shape(s), 506 tests, and all 132 planted defects reddened". The rv32 sizes are printed for every shape. | `receipts/ctrl_nvm.{log,rc}` |
| `ctrl_boundary.py --require-rv32 --without verilator` | rc 0, `ctrl_boundary: PASS`. It judged 3,284 compiled sources out of 3,534 recorded invocations, from 26 builder runs. "Every known builder held" was printed, and the builders-found-by-text check ran (no `--only`). | `receipts/ctrl_boundary.{log,rc}` |

Notes on these runs:
- **Image builders.** Their "exit 2, stopped at its link" is the gate's accepted capture mode (`ctrl_runs.py:117-123`, `stopped_at_link`). It is not a failure.
- **LiteX.** The builder `sw/litex/test_ctrl_memory.py` needs LiteX. I extracted clean `git archive` copies of the seven packages at exactly the revisions in `sw/litex/litex_pins.txt` (`receipts/litex-pins.txt`) and put them on `PYTHONPATH`.
- **Earlier attempts.** Two first attempts refused for environment reasons only and are kept unpublished: archive-filled submodules that were not checkouts, and no LiteX on the path. Both were fixed before the runs above.

### 4. Other contradictions in the composed tree

- **S7's split firmware compiles #823's store.** `tb/verilator/milan_dp/twin_fw.py:58` compiles `nvm_klj2.c`, `nvm_store.c` and `host/nvm_fmodel.c`, and #823 changed all three, plus the shape header contract. `twin_split.cpp:340-348` calls `nvm_fmodel_window(NVM_SLOT_A, NVM_SLOT_B + NVM_SLOT_BYTES)`, and both names still exist at the candidate (`nvm_shape.h:142-144`, `nvm_fmodel.h:85`). twin_fw gets its headers through `plat_arms`, which #823 moved to the new `shape_header(inputs)` signature. No caller of the old three-argument form remains anywhere in the candidate.
- **No bank or CI job runs these gates.** `make twin` and `make srptx` appear in no workflow, `ci_events.py`, `suite_shards.py` or `run_suites.sh`. The candidate's native-bank `milan_dp.log` has no twin run. So I ran both at the candidate with Verilator 5.050 (`receipts/verilator-version.txt`, the pinned wrapper). This is S7's documented behaviour (#867, `docs/design/MAILBOX_SPLIT.md:1845-1858`, `sw/firmware/ctrl/srp/README.md:381`) with #823's store compiled in:

  | Gate at `e282ecd2` | Result | Receipt |
  |---|---|---|
  | `make -j8 twin` (both halves built, split firmware via `twin_fw.py`, `twin_compare.py`) | rc 0, `twin: 0 finding(s)` | `receipts/make_twin.redacted.log`, `make_twin.rc` |
  | `make -j8 srptx` (scenarios wire, hold, licence; off-grid 16280 and 16240) | rc 0. All five report `0 finding(s)`. wire: 1,449 MRPDUs over 600,000 ms. hold: 169 MRPDUs. Each licence run: 69 MRPDUs. | `receipts/make_srptx.redacted.log`, `make_srptx.rc` |

  The redacted logs replace the home-directory prefix of tool paths with `$HOME` and change nothing else.
- **The control count S7 changed.** S7 changed `sw/firmware/ctrl/README.md:255` from "181 pin controls" to "183 pin controls", and `ctrl_boundary.py:164` checks that figure under `--selftest`. `ctrl_pin.py:881-893` derives the count partly from the Makefile targets that reach the stack. PR #880 changes no Makefile and none of `ctrl_boundary.py`, `ctrl_pin.py` or `ctrl_capture.py`, so the composition cannot move the figure.
- **Docs.** Neither side's added text mentions the other's subject. #823 adds nothing on twin or srptx, and S7 adds nothing on KLJ3 or layout 3.
- **Manager candidate banks at `e282ecd2`**, from `$VALIDATION_STORAGE/823-candidate-0923`:
  - The integrity receipt is PASS: tree `466d464a`, 1,551 files, and the gitlinks above.
  - `manager-builder/results.json` has 48 entries, all exit 0. They include `ci_events.py --check/--selftest`, `measure_test_evidence.py --check/--selftest` (which reads S7's `measure_test_evidence_readers.py`), `docs_check.py`, `gen_toc.py --verify-anchors`, `check_doc_paths.py`, `test_nvm_firmware.py --self-test`, and the builder suite on the pinned SDK.
  - `full-native/results.json` has 5 entries, all exit 0: parallel suites (5 shards, each rc 0), Yosys, protocol-processor, gptp-processor and behave.
  - I checked these receipts. I did not re-run them.

### 5. Prior findings at this head

I read these after my own pass. The head is unchanged from the one R805-6 and R806-6 reviewed.

| Prior finding | Status at `2905c874` and in the composition |
|---|---|
| RS1 (R805-6) = RS-1 (R806-6), RESIDUE, `scripts/nvm_format_32x32_tables.py:427` | **Retained** (carried, residue). The composition does not touch it. |
| RS2 (R805-6) = RS-2 (R806-6), RESIDUE, `sw/firmware/ctrl_nvm/test/nvm_bench.py:114` | **Retained** (carried, residue). The composition does not touch it. |
| SG1-SG3 (R805-6), S-1 and S-2 (R806-6), SUGGESTIONs | Optional. They are unchanged and do not affect coverage. |
| R805-5 / R806-5 append-path MAJORs and F4 MINOR | Outside this branch by the round 6 split ruling. They stay open under #876. This composition has no append-path code. |

## Findings

### C-RS1 - RESIDUE - Docs - `sw/firmware/ctrl/test/ctrl_configs.py:179,181,185` - lane label in the registry reasons this PR added

- **Evidence.** The three `OUTSIDE` reason strings #823 added say "the F1 store's nvm_layout3.h", "the F1 store's host suite" and "in the F1 store".
  - "F1" is #665's lane label. The PR's own commit `e0adcc09` names this rule ("Name the split placement's saved-state store, not its lane label"). The round 5 ruling item 4, as R805-6 and R806-6 quote it, asked for every comment instance.
  - These lines are identical at `2905c874` and `e282ecd2`. Neither prior round flagged them.
  - The strings are only membership-read (`ctrl_configs.py:373`), so this is pure wording: no test, gate, figure or generated artifact reads them.
  - The base already has 40 instances of "F1 store" or "lane F1" under `sw/` and `scripts/`, which #746 tracks. These three are new in this PR.
- **Impact.** Wording only: a workflow label in source text that the comment rule says should state behaviour.
- **Exact fix.**
  - `:179`: "from the F1 store's nvm_layout3.h" -> "from the split placement's saved-state store's nvm_layout3.h".
  - `:181`: "the F1 store's host suite" -> "the split placement's saved-state store's host suite".
  - `:185`: "in the F1 store (#823)" -> "in the split placement's saved-state store (#823)".
- **Verification.** `git grep -n "F1 store" -- sw/firmware/ctrl/test/ctrl_configs.py` is empty, and `ctrl_boundary.py` still passes. The values are not read, so this edit needs no other gate.

### C-SG1 - SUGGESTION - Tests (process) - `tb/verilator/milan_dp/twin_fw.py:58` - the twin and srptx gates are in no bank

- `make twin` and `make srptx` compile the saved-state store (`nvm_klj2.c`, `nvm_store.c`, `host/nvm_fmodel.c`) together with the split firmware. No CI workflow, `ci_events.py` entry, suite shard or manager bank runs them.
- A change to `sw/firmware/ctrl_nvm` or to the shape header contract therefore reaches them without any gate. That happened here; both pass, so it is not a defect.
- **Optional outcome:** register them, or add them to the merge-lane composition checklist for PRs that touch `sw/firmware/ctrl_nvm` or `tb/verilator/milan_dp/twin_*`.

### C-SG2 - SUGGESTION - Tests (process) - composition acceptance names the wrong reader

- Composition checks of `ctrl_configs.py` should name `ctrl_boundary.py --require-rv32` (with `--without verilator` or `--only verilator`, as `ci_events.py:2589,2621` does) as the reader.
- `test_ctrl_firmware.py` and `test_ctrl_nvm.py` do not import `ctrl_configs.py`.
- The boundary gate needs the pinned LiteX on the import path for its `sw/litex/test_ctrl_memory.py` builder.

## Reviewer-owned completion ledger (composition delta)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composed `ctrl_configs.py:176-185,239-244,269-276` against both sides' diffs (union, 0 removed). #823's format gate `test_ctrl_nvm.py --self-test` (506 tests, 132 plants). S7's #867 `make srptx` (5 runs, 0 findings) and #665 `make twin` (0 findings), against `MAILBOX_SPLIT.md:1845-1858`. | R805-7 | `e282ecd2` (candidate of `2905c874`) |
| RTL | CLEAN | The composition changes no RTL: the only overlap is a Python registry, and the gitlinks are identical. Verilator 5.050 builds of `milan_datapath.sv` plus `tb_split_top.sv` in `obj_twin_af` and `obj_twin_sp`. Manager native bank at `e282ecd2`: Yosys, suites and both processors, all exit 0. | R805-7 | `e282ecd2` |
| Robustness | CLEAN | Registry probe: every composed entry is load-bearing in `held()` (`ctrl_configs.py:373`). The NVM self-test's 132 planted defects are caught at the composition. srptx off-grid controls 16280 and 16240 give 0 findings. Duplicate-key AST check finds 0. | R805-7 | `e282ecd2` |
| Tests | CLEAN | `test_ctrl_firmware.py --require-rv32` PASS. `test_ctrl_nvm.py --require-rv32 --self-test` OK. `ctrl_boundary.py --require-rv32 --without verilator` PASS. `make twin` and `make srptx` rc 0. Manager builder bank: 48/48 entries exit 0. C-SG1 and C-SG2 are optional. | R805-7 | `e282ecd2` |
| Docs | CLEAN (C-RS1 residue, carried RS1/RS2) | `sw/firmware/ctrl/README.md:255` figure (Makefile-derived, unchanged by #880). `MAILBOX_SPLIT.md` and `srp/README.md` (S7) against #823's `SAVED_STATE_FORMAT_32X32.md` and `SPLIT_CONTROL_MEMORY.md`: no cross-reference. Manager `docs_check`, `gen_toc --verify-anchors` and `check_doc_paths` exit 0 at `e282ecd2`. | R805-7 | `e282ecd2` |

The PR's own content keeps its lens verdicts from R805-6 and R806-6, both POSITIVE at `2905c874`, because the head has not changed.

## Real limits

- **Boundary gate.** It ran `--without verilator`, so three builders are LEFT OUT by design: `tb/verilator/mbx/Makefile`, `maap_differential.py` and `aecp_wire.py`. It ran without `--selftest`, so its controls and README figures were not re-planted. I argue above that the composition cannot change them, since neither side touched the gate's own files and only S7 changed Makefiles. That is reasoning from the diff, not a run.
- **Firmware gate.** `test_ctrl_firmware.py` ran without `--self-test`, so its mutants were not planted at the candidate. I did not run `srptx-plants`, `srptx-mutants` or `twin-plants`.
- **LiteX.** The packages came from a local bench's git objects at the pinned revisions, as clean archives. Two of that bench's checkouts have local edits, which were not used.
- **Not checked.** I did not inspect hosted or act evidence, ran nothing at the PR's source head, and did not infer any manager source bank. Physical calibration NOT RUN, and field skips are not hardware proof.
- **Base.** The candidate I validated is against `dev-soft-core` `764482b4`, the PR's base. Live `dev` (`fa6c094b8e196666a8a8865788d5e83b5bbaea09`) is a separate merge-turn candidate.

## Pending manager duties

- Publish this report and the receipts listed in `MANIFEST.sha256`.
- Carry C-RS1, RS1 and RS2 to the residue checklist.
- Decide C-SG1 and C-SG2.
- Own the hosted and act acceptance of the candidate, and any further merge-turn candidate.

## Integrity after probes

Receipt: `receipts/integrity-after.txt`.

- **Review clone:** HEAD `2905c874`, tree `c28f6877`. Status is empty, the index equals HEAD and the worktree equals the index. The required submodules are at their gitlinks; `external` is uninitialised, as it was at the start. Only objects and remote-tracking refs were fetched into the clone. No tracked byte was touched.
- **Candidate scratch tree:** HEAD `e282ecd2`, tree `466d464a`. After every gate there were 0 tracked modifications, and every submodule is at its gitlink with 0 modifications.

R805-7 FINISHED
