[R249] POSITIVE - exact head 6b3936b3b47c0c7d1a6423e9f69ff28b4e7deada

# R249-7: composition review of issue #400 / PR #566 (issues #400 and #403) on the merge-train candidate

- Candidate `6b3936b3b47c0c7d1a6423e9f69ff28b4e7deada`, tree `2ceadf884745dcae5ef5bf1b26efcca872cf666f`.
  - First parent: live `dev` `1658ded24f77177cd1640a7e78ed346826791d27` (PR #563 for #545, merged 2026-09-25T21:38:34Z). Live `dev` still read `1658ded2` during this review.
  - Second parent: PR #566 source head `a07a75de78b19369e228d4ab8403a52f7435fd64`. Two independent POSITIVE source reviews exist at that head: R250-6 (PR comment 5843508715) and R249-6 (PR comment 5843735790).
- Scope: composition acceptance only. The question is whether the composed tree has a defect that neither reviewed source has.
- All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs.
- **Verdict: POSITIVE.** There is no composition finding at any severity. The R249-4 F1 BLOCKER is CLOSED at this head.

## 1. Reconstruction

Read in this order:

1. AGENTS.md, then CONTRIBUTING.md sections 2.1-2.2 and 3.
2. docs/README.md.
3. Issue #400: its body and the manager comments (decision 5770922734, prerequisite disposition 5781750191, round assignments).
4. The PR #566 body, rounds 1-5.
5. The linked authorities: `docs/reference/SUBMODULES.md`, `docs/reference/REGISTER_MAP.md`, the `docs/testing/TESTING.md` explicit-campaign table, the `docs/testing/CI_WORKFLOWS.md` budgets and `.github/workflows/docs.yml`.
6. `git diff 1658ded2..6b3936b3` and the history.
7. Hosted evidence.

I read prior public review findings only after my own pass over the diff and after the gates and legs below had run.

**Merge integrity** (`receipts/merge_integrity.txt`):

- `git merge-tree --write-tree 1658ded2 a07a75de` independently produces `2ceadf88`, and the remerge-diff of the candidate is empty (0 bytes). So the candidate is exactly the clean three-way merge.
- The merge base is `220cb5a3`. #545's delta `220cb5a3..1658ded2` is 38 paths (`receipts/pred_files.txt`). The PR's delta `220cb5a3..a07a75de` is 42 paths (`receipts/pr_files.txt`).
- The 34 predecessor-only paths equal `dev`, and the 38 PR-only paths equal the source head, blob for blob (72 `EQ` lines).

**Overlap census** (`receipts/overlap_files.txt`). Four paths are changed by both sides:

- `docs/reference/REGISTER_MAP.md`
- `docs/reference/SUBMODULES.md`
- `hdl/milan/milan_datapath.sv`
- `tb/verilator/milan_dp/README.md`

For each of the four, the candidate carries both sides' changed lines unchanged: the digest of the `dev`-side delta replayed over the PR equals the original, and the same holds the other way.

**Semantic interactions examined** beyond the textual overlap:

- #545's gitlink bump (`gptp-processor` `e5dcea6e` to `5dce647a`) against the ROM digest ledger `syn/yosys/rom_digests.tsv` and the pin table and guide links in SUBMODULES.md.
- #545's `scripts/measure_test_evidence.py` dispositions and `docs/testing/TESTING.md` inventory against this PR's new tb files.
- #545's `gmstep_mutants.py` option-off controls, which grade this PR's changed `tb/verilator/milan_dp/sim_main.cpp`.
- #545's slew wiring and #551's real-grant licence gate against this PR's generated VID binding, per-output presentation defaults and neutral AAF/MAAP resets.
- #559's capture receipt (`tb/verilator/nvm_capture_cpu/measurements.json`) against the composed product firmware.
- The docs-job step inventory, TOC/anchors, the CHANGELOG contents and the diagram generators.

## 2. Findings

**None.** No BLOCKER, MAJOR, MINOR or SUGGESTION arises from the composition.

## 3. Evidence per acceptance focus (all on the candidate)

Tool identities are in `receipts/tool_identity.txt`:

- Verilator 5.050: `verilator_bin` sha256 `44898b22...`. The assigned wrapper path was absent. I used an identical wrapper to the same 5.050 installation that the manager's round-5 pinned wrapper targets.
- sv2v v0.0.12, Vivado 2026.1 `xvlog` and Python 3.14.7.
- The pinned RV32 SDK archive `d42680e9...`, installed and verified by `scripts/ci_rv32_sdk.py` into a disposable prefix.

At most 8 parallel jobs were used.

### (1) Capture gate and the full docs step set

`scripts/run_docs_steps.sh` runs 77 gate commands (`receipts/docs_steps/`, see `NOTES.txt`). They are the docs job of `.github/workflows/docs.yml` plus the wire-accountability job, excluding tool installation and the act runner self-test.

- **Step 38, `python3 scripts/check_nvm_capture.py`: exit 0.** It prints `PASS: capture census, clocks, both timing arms and receipt agree`, and all seven controls are detected.
  - The firmware is the same on both sides. The sha256 of `sw/firmware/milan_baremetal/milan_baremetal.c` at the candidate is `0bf43cd4...`, which equals `measurements.json` `product_firmware_sha256`.
  - `sw/` and `tb/verilator/nvm_capture_cpu/` are byte-identical between the source head and the candidate, because #545 changed no firmware, harness or config.
- **Every step after the capture gate, 39-77, exits 0.** These include:
  - `test_nvm_firmware.py --self-test`
  - the source-list, port-contract, idiom and test-evidence gates
  - `ci_events.py --check` and `--selftest`
  - `check_doc_paths`, the archive gate, `gen_toc.py --selftest`, `--verify-anchors` and `--check`
  - the AEM, sweep, deploy, entity and wire-accountability gates
- Steps 1-31 and 33-34 exit 0. They include:
  - `docs_check.py`
  - `check_em_dash.py --base 1658ded2`
  - doc-style, diagram and submodule-docs gates
  - `check_gptp_docs.py --with-submodule` and `make -C gptp-processor docs`
  - the compiler-absent firmware controls (381 s)
- Step 32: the first run failed because the host's default SDK prefix is a local build with no provenance receipt. After the pinned SDK was installed, the re-run exited 0.
- Step 35 (`test_builder.py --require-rv32`, the full builder bank) was stopped by my own 595 s foreground timeout. No verdict is drawn from it. The full builder bank is outside my allowed scope, and the manager's bank is its evidence.
  - Its composition-relevant input is the composed datapath elaboration. That is covered separately: `scripts/elab_all_shapes.sh` lint-elaborates the composed `milan_datapath` under all five shipped generated shapes with the gPTP plane off and on. All 10 combinations exit 0 (`receipts/elab/summary.tsv`).
- `docs_check.py` and `check_feature_status.py` in an extracted tree with no `.git` both exit 0 (`receipts/docs_check_nogit.log`, `receipts/feature_status_nogit.log`).

### (2) `milan_datapath.sv`: slew wiring, licence gate and generated VID/reset posture coexist

**Composed text.**

- #545: `gptp_slew_active_w` (`hdl/milan/milan_datapath.sv:1469`), the `slew_rate_alignment` tail (`:2771-2775`), the servo port (`:5573`), the engine port (`:6916`) and the plane-absent tie-off (`:7008`).
- #551: the licence gate `lwsrp_stream_gate` (`:2036`).
- This PR:
  - the passive RX taps (`:1425`) and `ptp_now_w` public read (`:2039`)
  - the per-output `ADP_STROUT_PRES_NS_C` fold (`:3282-3284`)
  - `.SRP_DOM_DEF_VID_P (ADP_SRP_DOM_DEF_VID_C)` (`:7397`)
- The hunks are disjoint and no identifier collides.

**Static gates** (`receipts/rtl/`):

- `xvlog_gate.py --check` ran with Vivado: 0 `hdl/` findings and 4 pinned-processor findings, equal to the ratchet, PASS.
- `lint_rtl.py --check`: 90 violations, at or below the ratchet of 90, PASS.
- `lint_rtl.py --pragmas`, `pp_srcs.py --check` and `--selftest`, and `xvlog_gate.py --selftest` all exit 0.
- `check_port_contracts.py` and `--selftest` pass as docs steps 47-48.

**milan_dp legs** (`receipts/sim/`):

- `make gmstep`: 58 checks, 0 failures. This includes #545's nine `slew path:` checks, which run on the composed tree.
- #545's three `--slew` connection controls are each caught (tied-low level, missing tail, extra addend stage), and the positive control passes.
- The whole 14-control `gmstep-mutants` inventory is caught:
  - the three sweep controls (`gmstep_mutants_sweep.log`)
  - the three slew controls
  - the two option-off controls, which grade this PR's changed `sim_main.cpp` (`gmstep_optoff_controls.log`, via `scripts/gmstep_optoff_controls.py`)
  - the remaining six (`gmstep_remaining_controls.log`)
  - The two driver scripts reuse the suite's own `CONTROLS` and verdict code unchanged.
- `make crflic`: 415 checks, 0 failures.
- `crflic_mutants.py`: 7/7. The positive control passes and all six licence mutants are caught.
- `make option-off` (this PR's `sim_main.cpp`): 234 checks, 0 failures.
- `make gptp`: 181 checks, 0 failures.
- The `run` recipe's `obj_nxn` leg, at 4x4 (1844 checks, 0 failures), and `obj_nxn8` leg, at 8x8 with loopback (3524 checks, 0 failures). Both use `scripts/nxn_legs.mk`, which runs those recipes verbatim.

**csr and pp_shadow default targets:**

- `make -C tb/verilator/pp_shadow`: base, vid73 and crf fixture legs, 402 checks each, 0 failures. The `#400 generated parent/wrapper/top/child startup VID` check passes.
- `make -C tb/verilator/csr`: legs of 400, 400, 121, 44 and 400 checks with 0 failures, plus the `reset_bits.yaml` fixture leg (400 checks, 0 failures).

**Composed-file probe** (`scripts/probe_vid_binding.sh`, `receipts/sim/probe_vid_binding.log`):

- Deleting the composed `.SRP_DOM_DEF_VID_P` binding makes `run-vid73` fail three `#400` checks, for example `got=0x00030002 exp=0x00030049`.
- The file was then restored, and its blob `8db60887...` is identical to HEAD.

### (3) SUBMODULES.md, gitlinks and the ROM digest record (`receipts/pins_and_roms.txt`)

- The pin table equals the gitlinks for all four submodules: `gptp-processor` `5dce647a...` (from #545) and `protocol-processor` `990f9652...`. The four gPTP guide links use `5dce647a`, and no tracked file outside the digest ledger still names `e5dcea6e`.
- This PR's disclosure lines (`docs/reference/SUBMODULES.md:138-142`) sit after #545's slew sentences (`:113-117`) without contradiction.
- `submodule_boundaries.gen.py --check` and `check_submodule_docs.py` pass.
- The ROM images, generated by the `ooc.sh` recipe at the candidate gitlinks, match `syn/yosys/rom_digests.tsv`:

  | Image | Pin | Digest |
  |---|---|---|
  | `ltn_rom.hex` | `990f9652` | `23cc67ee...` |
  | `ucode.hex` | `990f9652` | `23605682...` |
  | `gptp_ucode.hex` | `5dce647a` | `c496ed8a...` |

  The milan_dp `gptp_ucode.hex` differs by design: it is the 2 MHz simulation image built with `--clk-hz 2000000 --cease-ms 3000`.

### (4) REGISTER_MAP, anchors and inventories

- The REGISTER_MAP hunks are disjoint: this PR's are at `:777-1242` and #545's `MCSRV_STAT` row is at `:2027`.
- `gen_toc.py --verify-anchors` and `--check`, `docs_check.py` in both modes, and `measure_test_evidence.py --check` and `--selftest` all exit 0.
- The composed milan_dp README states "fourteen controls" (`tb/verilator/milan_dp/README.md:657`), which equals the measured inventory of 14. The README also keeps this PR's `ADP_STROUT_PRES_NS_C` sentence (`:754`).

## 4. Prior public findings, resolved or retained at this head

| Finding | Status at 6b3936b3 | Evidence |
|---|---|---|
| R249-4 F1 BLOCKER (Tests, Conformance, Docs): composed tree failed `check_nvm_capture.py` on the firmware pin | **CLOSED** | Step 38 exits 0, and the receipt firmware digest `0bf43cd4...` equals the candidate. Steps 39-77 exit 0. Section 18 / UNRESOLVED 6 of `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` state the refreshed measurement, and the file is byte-identical to the reviewed source head. |
| R249-2/R250-2/R250-3 findings (closed before R249-4) | Remain CLOSED | Every PR-only path is byte-identical to `a07a75de`. The four overlap files carry the PR's delta unchanged. |
| R250-6 S1, R249-6 S1 and S2 (SUGGESTION) | Retained as SUGGESTION, unchanged | `scripts/check_nvm_capture.py`, `measurements.json` and `boot_policy.py` are byte-identical to the source head. No coverage effect. |
| R250-3/R250-4 S1 and R249-2/R249-3 S1 (SUGGESTION, routed to #495) | Retained as SUGGESTION | The files are unchanged by the composition. No coverage effect. |

## 5. Reviewer-owned completion ledger (composition)

Every lens's scope is touched by the composition, so every lens is covered by this round at the candidate. Content the composition does not alter (the 38 PR-only paths, byte-identical) stays covered by the source reviews R250-6 and R249-6 at `a07a75de78b19369e228d4ab8403a52f7435fd64`.

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Capture-gate contract (`check_nvm_capture.py:61-63`, `measurements.json`), generated-VID binding `milan_datapath.sv:7397` with vid73 probe, #545 slew path `:2771-2775,5573` against the gmstep slew checks, #551 licence gate `:2036` with crflic and its mutants, SUBMODULES pins | R249-7 | `6b3936b3b47c0c7d1a6423e9f69ff28b4e7deada` |
| RTL | CLEAN | `hdl/milan/milan_datapath.sv` overlap hunks, `xvlog_gate --check` (Vivado), `lint_rtl --check`, `check_port_contracts`, `check_sv_idiom`, `check_rtl_source_lists`, 10 shape/gPTP elaborations, ROM digest ledger | R249-7 | `6b3936b3b47c0c7d1a6423e9f69ff28b4e7deada` |
| Robustness | CLEAN | Plane-absent tie-off `:7008` (gPTP-off elaborations, option-off leg), all five shapes, neutral resets under the gmstep, crflic and gptp legs, link-cycle VID restore in pp_shadow, refused-grant crflic arms | R249-7 | `6b3936b3b47c0c7d1a6423e9f69ff28b4e7deada` |
| Tests | CLEAN | Full 14-control gmstep inventory including option-off controls on this PR's `sim_main.cpp`, crflic 7/7, gmstep/crflic/option-off/gptp/nxn/nxn8 legs, csr and pp_shadow defaults with fixture legs, `measure_test_evidence --check`, 76 docs-job commands | R249-7 | `6b3936b3b47c0c7d1a6423e9f69ff28b4e7deada` |
| Docs | CLEAN | `REGISTER_MAP.md` (`:777-1242`, `:2027`), `SUBMODULES.md` (`:20-27`, `:110-142`), `tb/verilator/milan_dp/README.md` (`:651-664`, `:754`, `:1083-1090`), section 18 / UNRESOLVED 6; docs_check in both modes, em-dash vs `1658ded2`, `gen_toc --verify-anchors/--check`, diagram and submodule-doc gates | R249-7 | `6b3936b3b47c0c7d1a6423e9f69ff28b4e7deada` |

## 6. Limits

- **Hosted evidence:** none exists for this candidate. The commit is not published: the hosted API reports "No commit found". PR #566's hosted runs at `a07a75de` started at about 21:00Z on 2026-09-25, before #563 landed at 21:38:34Z; `docs-check` completed at 21:17:24Z. They therefore ran on the pre-#545 merge ref and do not cover this composition (`receipts/hosted_checks_a07a75de.tsv`).
- **Builder bank:** `test_builder.py --require-rv32` was not run to completion (see 3.1). Compiler-present firmware coverage here comes from `test_nvm_firmware.py --self-test` and the compiler-absent audit.
- **Capture receipt:** `measurements.json` was measured at `6d181922`, a SoC that predates #545's datapath, servo and gPTP-pin change.
  - The gate's binding contract (firmware, harness, census and clocks) holds.
  - #545's delta is outside the CPU/CSR/NVM-port copy path.
  - I did not re-run the capture harness. This is already covered by the retained R249-6 S2 SUGGESTION: the pin covers only the firmware source bytes.
- **Suites not re-run:** the default `milan_dp` sweep as a whole was not run, and neither were `mmcm_servo`, `crf_rx`, `gptp_shadow`, the Yosys gates, and the PP/gPTP banks. #545's own suites use no file that this PR changes.
- **Hardware:** physical calibration was NOT RUN, and no hardware or field result is claimed.

## 7. Pending manager duties

- Build and validate the final current-dev candidate at the merge turn, and re-confirm that live `dev` is still `1658ded2`. Any later `dev` movement needs a new composition check.
- Hosted exact-head evidence for the merge candidate: `docs-check` including steps 30-51 (`check_nvm_capture.py` onward), `rtl-fast`, `verilator-suites` and `yosys-portability`. Within the `milan_dp` 3600 s budget, the composed `milan_dp` shard's wall clock includes both #545's slew phase and this PR's added harness checks.
- The full builder bank, the native banks and act acceptance.
- Merge only with explicit maintainer authorization, then post-merge containment.

## 8. Receipt integrity

- After every probe, the clone is at `6b3936b3` / `2ceadf88` (`receipts/final_tree_verification.txt`):
  - The worktree and the index are clean.
  - The index records equal `ls-tree HEAD`, and no assume-unchanged or skip-worktree flag is set.
  - All 908 tracked non-gitlink files match their blobs and modes.
  - The gitlinks are `external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `990f9652` and `third_party/verilog-axis` `48ff7a7e`, and the submodule checkouts are clean.
  - All build outputs were removed.
- Host home paths in receipts are redacted to `<host-home>`.

R249-7 FINISHED
