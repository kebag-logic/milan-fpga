[R249] NEGATIVE - exact head 09419d88053bd7777de966ce825e4ad7fe71c713

# R249-4: composition review of issue #400 / PR #566 (issues #400 and #403) on the merge-train candidate

- Candidate `09419d88053bd7777de966ce825e4ad7fe71c713`, tree `d1c94326094b9c9c2ef2f6ecce0f065f003fd7bb`.
  - First parent: train candidate C_545 `551e4b5dfa8ac7ec68a3161c95d4000eb6337396` (#545 on #551 on #559 on #443, over the live-dev lineage).
  - Second parent: PR #566 source head `c6c65e803f9eb270a11dfd65fda5814fb0b0ea55`.
- Scope is composition acceptance only: defects that the composed tree has and the reviewed sources do not.
- All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs.
- The verdict is NEGATIVE on one BLOCKER, F1. It is a real composition defect. The PR edits the product firmware, and #559, already in the train and in live dev, pins that firmware's digest in a required gate.

## Reconstruction

Read in order:

1. AGENTS.md and CONTRIBUTING.md sections 2.1 and 3.
2. docs/README.
3. Issue #400: its body and every maintainer/manager comment. These include the decision 5770922734, the assignment 5781042070, the 2026-09-23 owner decision moving restored PTOF to #70, and the round 1-4 assignments.
4. The candidate diff and history.
5. Hosted evidence for PR #566.

Prior public review findings were read only after my own pass over the diff and after F1 had been found and receipted.

**Merge integrity** (`receipts/00_merge_tree.log`): `git merge-tree --write-tree 551e4b5d c6c65e80` independently produces `d1c94326...`, so the candidate tree is exactly the clean three-way merge. The merge base is `864b36f5`.

**Overlap census** (`receipts/01_overlap.log`):

- Eight files are changed by both sides:
  - `docs/reference/REGISTER_MAP.md` and `docs/reference/SUBMODULES.md`
  - `hdl/common/csr/milan_csr.sv`, `hdl/milan/KL_pp_shadow.sv` and `hdl/milan/milan_datapath.sv`
  - `tb/verilator/csr/sim_main.cpp` and `tb/verilator/csr/sim_win.cpp`
  - `tb/verilator/milan_dp/README.md`
- The PR's other 32 files have byte-identical blobs at the PR head and in the candidate.

**Semantic interactions examined** beyond the textual overlap:

- #559's capture receipt pins the product firmware, which the PR edits. This is F1.
- #559's `nvm_capture_cpu/soc.py` consumes `fabric_constants()`, which the PR extends.
- #551's crf_licence, #545's gmstep and #443's render legs program CSRs whose resets the PR neutralises.
- The docs-check step inventory pinned by `ci_events.py`.
- The TOC/anchor, test-evidence and module-matrix inventories.
- The gptp-processor gitlink: the train has `5dce647a` and the PR has `e5dcea6e`. The candidate carries the train's, and the PR does not touch it.

## Findings

### F1 - BLOCKER - Tests, Conformance, Docs - `sw/firmware/milan_baremetal/milan_baremetal.c:41,1375-1383` against `tb/verilator/nvm_capture_cpu/measurements.json:17` and `scripts/check_nvm_capture.py:62`: the composed tree fails the required capture-measurement gate

**Authority and evidence.**

- #559 (in the train at `b02af048` and in live dev `1299b461`) records its product-CPU capture timing in `measurements.json`. It binds that receipt to the exact product firmware through `product_firmware_sha256 = 7cdc5e68...`.
- `check_nvm_capture.py:62` fails whenever the firmware differs.
  - The suite README says so directly: "The product firmware hash also prevents carrying timing across edits" (`tb/verilator/nvm_capture_cpu/README.md:150-151`).
  - The step "Capture measurement census and clock gate" runs in the required `docs-check` context (`.github/workflows/docs.yml:222-224`; `docs/testing/CI_WORKFLOWS.md:614`, `:1200-1210`).
- PR #566 changes `configure_fabric()` in `milan_baremetal.c`: the TCAM_CTRL define, the MAC_CTRL/TCAM boot writes, and the generated `MILAN_AAF_CTRL_BOOT` and `MILAN_MAAP_CTRL_BOOT`. That is within its accepted scope.
- The firmware blob digest is `7cdc5e68...` at 864b36f5, 551e4b5d and live dev 1299b461. It is `0bf43cd4...` at c6c65e80 and at the candidate (`receipts/60_nvm_capture_hashes.log`).

**Measured.**

- On the candidate, `python3 scripts/check_nvm_capture.py` exits 1 with `FAIL: product firmware changed; remeasure the copy` (`receipts/43_nvm_capture.log`). The census inputs (bytes, records, clocks) agree; only the firmware pin fails.
- Causality probe: I swapped only `milan_baremetal.c` for the train parent's bytes, and the same gate passed. The candidate bytes were then restored and the blob id re-verified (`receipts/61_probe_nvm_capture_train_firmware.log`, `scripts/probe_nvm_capture_firmware.sh`).
- Independent hosted confirmation comes from the PR's own `pull_request` run 36171850304 on the merge ref, which is the PR plus live dev. `docs-check` failed at exactly this step, and the 22 later steps (30-51) were skipped (`receipts/62_hosted_docs_check_failure.log`, `receipts/64_hosted_docs_check_steps.tsv`).

**Why this is a composition defect.**

- The PR's own base `864b36f5` has no capture gate. Its source reviews, R250-4 and R249-3, therefore could not see this failure at the source head.
- It arises only when the PR meets #559, which is already in live dev. So it will reproduce on the manager's final current-dev candidate too.

**Lens attribution.**

- **Tests:** a required gate is red on the merge tree, and the #559 timing evidence no longer describes the firmware that ships.
- **Conformance:** section 7 requires the required gates to pass. The #559 capture contract (8x8 at or below 24.5 ms) is also left unmeasured for the composed product firmware, and its recorded margin is only 0.19546 ms.
- **Docs:** `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1572-1576` publishes the measured maxima and states "Product firmware, RTL and builder census lists remain unchanged". On the composed tree the product firmware has changed.

**Impact.**

- Merging as composed turns the required `docs-check` context red on `dev`.
- It also hides the 22 downstream docs-check steps behind the failure: the saved-state writer gate, the source-list, idiom, CI-event, TOC and shape gates. I ran those gates locally; see below.
- Published capture timing would describe a firmware that no longer ships.

**Required outcome.**

- The candidate that merges must carry a capture re-measurement for the composed product firmware. It follows the `tb/verilator/nvm_capture_cpu/README.md` procedure: both traffic arms, both contract shapes, and the 100 MHz comparison.
- It must refresh `measurements.json`: the firmware digest, the rows and the maxima.
- It must update any changed figures in `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18.
- A public decision must name the lane that owns it.
- The gate, its firmware pin and its ratchets must not be weakened, and the firmware change must not be reverted to obtain a pass. It is accepted #400 scope.
- **Feasibility probe:** the harness's instrumentation anchors still apply uniquely to the candidate firmware in all three modes (`receipts/63_probe_capture_anchors.log`). The harness also drops the `milan_init` registration, so the edited `configure_fabric()` is outside the timed interval. That is an expectation only: the contract requires measurement, not inference.

**Verification.**

- `python3 scripts/check_nvm_capture.py` exits 0 on the new candidate.
- Hosted `docs-check` is green on the exact candidate, with steps 30-51 executed.
- A reviewer re-reviews the new receipt: rows graded, maxima recomputed, margin against 24.5 ms stated.

No other composition finding.

## Composition evidence per acceptance focus (all on the candidate; receipts under `receipts/`)

Tool: Verilator 5.050 (`receipts/02_tool_identity.log`). The job cap is 8, using a wrapper that rewrites `--build -j 0` to `-j 8` (`scripts/verilator-wrapper.sh`).

**(1) `milan_csr.sv`.** #443's RENDER_STAT (0x8DC) arm and this PR's neutral AAF/MAAP resets and lwSRP VID coexist.

- `make -C tb/verilator/csr` exits 0 (`70_csr_default.log`).
  - The default build runs 400 checks and the other legs run 400/400/121/44/400. The reset-bits leg, built with `-DCSR_SRP_RESET_BITS=3u`, also passes.
  - The RENDER_STAT and "AAF/MAAP neutral reset" checks execute in the same runs.
- Composed-file mutants, each detected and restored byte-exact:
  - AAF reset back to `0x0002_0000`: csr fails with `AAF neutral reset VID got=0x2` (`92_mut_csr_aaf_reset_vid2.log`).
  - RENDER_STAT read tied to zero: csr fails with four RENDER_STAT checks (`93_mut_csr_render_stat_zero.log`).

**(2) `KL_pp_shadow.sv` / `milan_datapath.sv`.** #551's real-grant licence, #545's slew wiring and this PR's VID binding coexist.

- Static gates exit 0: `xvlog_gate --check` (it ran, 4 findings equal to the ratchet), `lint_rtl --check`, `check_port_contracts`, `check_sv_idiom` and `check_rtl_source_lists` (receipts 30-37).
- `make -C tb/verilator/pp_shadow` exits 0 with three legs of 402 checks each. VID73 reaches the parent/wrapper/top/child path (`0x00030049`) (`71_pp_shadow_default.log`).
- milan_dp legs, all exit 0:

  | Leg | Result | Receipt |
  |---|---|---|
  | crflic | 415 checks, including the #551 G/H refused/admitted arms and the I/J unwarmed arms for both sources and both phases | `72` |
  | gmstep | 58 checks, plus its 3 default controls caught | `73`, `74` |
  | gptp (fabric plane on, the #545 slew context) | 181 checks | `95` |
  | aclk render law | 190 checks | `75` |
  | render_mutants | 2 clean controls and 4 mutants caught | `76` |
  | render-csr-controls | 4/4 | `77` |
  | PR-edited harnesses on the composed datapath: `sim_main` 1x1 | 234 checks | `78` |
  | PR-edited harnesses on the composed datapath: `sim_nxn` 4x4 | 1844 checks | `79` |
  | `milan_dp_render` suite | 65 checks, plus defect controls | `80` |

- Composed-file mutants, each detected and restored byte-exact:
  - Drop `.SRP_DOM_DEF_VID_P (ADP_SRP_DOM_DEF_VID_C)`: VID73 fails, reading 2 instead of 73 (`90`).
  - Revert the #551 licence to ACTIVE-only: crflic fails on the refused-re-declaration checks (`91`).
  - Drop the `KL_pp_shadow` pass-through: VID73 fails three VID checks (`94`).
- The train's CSR programming is absolute, not read-modify-write, so the neutral resets cannot leak into it: `sim_crf_licence.cpp:828-830` writes AAF `0x00020001` and MAAP `0x201`; `sim_gmstep.cpp:807` writes AAF `0x00020003`.

**(3) Builder and firmware artifacts for all five configs.**

- `test_builder.py --require-rv32` exits 0 with ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 calibration). It used a digest-verified SDK extraction and 855 mapped compiler invocations (`86_*`, `84`, `85`).
- The compiler-absent `test_builder.py --require-elaboration` exits 0 with EXCEPT 2 NOT RUN: gate 1b is absent by design and gate 11 is calibration (`87_*`).
- Gates 18a-18d, 20a, 23a-23l, 35 and 40 ran.
- `test_declarations.py` exits 0: five configs, 26 refusals and 9 binding/reset mutants (`81`).
- `test_nvm_firmware.py --self-test` exits 0 on 5 shapes, with every planted defect reddened (`82`). Hosted skipped this step on the merge ref because of F1.
- `make -C tb/verilator/nvm_cosim` exits 0: 465 checks and 39/39 mutants (`83`).
- `check_nvm_record_space` exits 0 (`44`). The capture gate's census half agrees; its firmware half is F1.

**(4) REGISTER_MAP / SUBMODULES / milan_dp README.**

- Rows edited by both sides are consistent. The composed REGISTER_MAP carries #551's `CRFT_CTRL[6]`, `LWSRP_STATUS[8]` and `0x698` licence text alongside the PR's `0x654`, `0x680`, `0x684`, `0x6CC`, `0x75C` and `0x788` rows, with no contradiction. The "While enabled the plane declares" paragraph is unchanged from both parents.
- SUBMODULES keeps both sides.
- The README's `ADP_STROUT_PRES_NS_C` line and #551/#545 sections coexist.
- A scan of every train-added line found no claim that the PR's reset, offset or boot changes falsify, other than F1's section 18 sentence.
- Gates, all exit 0:
  - `docs_check` in git mode (`10`) and no-git mode (`97`, a `git archive` export).
  - `gen_toc --check` and `--verify-anchors`.
  - `check_em_dash` against both parents.
  - `check_doc_style` and `check_doc_paths`.
  - `measure_test_evidence --check` and `ci_events --check` / `--selftest`.
  - The module matrix, submodule docs and diagram, diagram PNGs, DOC_MAP, solution and gPTP docs, and feature status.
  - `git diff --check` against both parents.
  - BDD: 344/344 scenarios (`96`).

## Per-lens results (same three fields as a finding)

- [R249] UNCLEAN Conformance - F1 (`check_nvm_capture.py:62`, `measurements.json:17`); otherwise examined: the composed VID binding and reset/boot posture against decision 5770922734 (receipts 70, 71, 90, 94), and the coexistence of the #551 licence and #443 RENDER_STAT (72, 91, 93).
- [R249] PASS RTL - `milan_csr.sv:1211-1213,1547-1557,1980-1991,2392-2396`, `KL_pp_shadow.sv:189,1060`, `milan_datapath.sv:1424-1428,2039,2764-2775,6646-6647,7397` - composed merge tree plus xvlog, lint, port-contract, idiom and source-list gates; csr, pp_shadow and milan_dp legs; five overlap mutants detected.
- [R249] PASS Robustness - `sim_crf_licence.cpp:828-830`, `sim_gmstep.cpp:807`, `tb/verilator/csr/Makefile:128-132` - the neutral resets meet only absolute CSR writes in the train legs; crflic refused/unwarmed arms and the reset-bits leg pass; no read-modify-write dependence on the old `0x0002_0000` / `0x0800` resets in train-added code.
- [R249] UNCLEAN Tests - F1 (required `docs-check` step red; receipts 43, 61, 62, 64). All other composed legs and gates exit 0.
- [R249] UNCLEAN Docs - F1 (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1572-1576`, `nvm_capture_cpu/README.md:150-151`); REGISTER_MAP, SUBMODULES and the milan_dp README are otherwise consistent, and all doc gates exit 0.

## Earlier public findings at this head

| Finding | Status at `09419d88` | Evidence |
|---|---|---|
| R249-2 F1 / R250-2 F1 (BLOCKER): `nvm_cosim` stale caller | CLOSED | `run_cases.py` is byte-identical to c6c65e80; `make -C tb/verilator/nvm_cosim` shows 465 checks and 39/39 (`83`) |
| R249-2 F2 / R250-2 F2 (MINOR): uncommitted discriminating legs | CLOSED | Default csr reset-bits and pp_shadow vid73/crf legs run and discriminate (`70`, `71`, `90`, `94`) |
| R249-2 F3 (MINOR): RTL contract comments | CLOSED | The PR text at `milan_csr.sv:1547-1557` and `milan_datapath.sv:274-275,299-301` survives the merge unchanged |
| R249-2 F4 / R250-2 F3 (MINOR): as-built docs | CLOSED | MAAP_FABRIC, AREA_BUDGET and `milan_soc.py` are byte-identical to c6c65e80; the composed milan_dp README keeps the `ADP_STROUT_PRES_NS_C` line |
| R250-3 N1 (MINOR): builder comments | CLOSED | `endstation_builder.py` is byte-identical to c6c65e80 (R250-4 evidence) |
| R250-3 S2, S3 and R249-3 S2 (SUGGESTION) | CLOSED | These files are byte-identical to c6c65e80 |
| R250-2/3 S1 and R249-2/3 S1 (SUGGESTION): timer instance, `boot_policy` literals | Retained as SUGGESTION, routed to #495 | No coverage effect |
| R250-4 pending duty 1 (capture gate on the current-dev candidate) | Confirmed as F1 on this candidate | receipts 43, 61, 62 |

## Completion ledger (reviewer-owned)

Every lens's scope is touched by the composition, through the overlap files or the #559 firmware pin. No lens is banked on the source reviews alone. The source reviews covering the PR-only content are R250-4 POSITIVE at `c6c65e803f9eb270a11dfd65fda5814fb0b0ea55` and R249-3 POSITIVE at its ancestor `e122f3302cf8a8e89de960233a8638b9dd1387dc`.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Capture pin, VID binding and reset posture against 5770922734, #551/#443 coexistence | R249-4 | 09419d88053bd7777de966ce825e4ad7fe71c713 |
| RTL | CLEAN | milan_csr, KL_pp_shadow and milan_datapath overlap; xvlog, lint and port gates; csr, pp_shadow and milan_dp legs; 5 mutants | R249-4 | 09419d88053bd7777de966ce825e4ad7fe71c713 |
| Robustness | CLEAN | Neutral resets against the train legs' CSR programming; refused/unwarmed arms; reset-bits leg | R249-4 | 09419d88053bd7777de966ce825e4ad7fe71c713 |
| Tests | UNCLEAN (F1) | 70+ receipts; the red `check_nvm_capture` | R249-4 | 09419d88053bd7777de966ce825e4ad7fe71c713 |
| Docs | UNCLEAN (F1) | REGISTER_MAP, SUBMODULES, milan_dp README, snapshot section 18, doc gates in both modes | R249-4 | 09419d88053bd7777de966ce825e4ad7fe71c713 |

## Real limits

- **Tool path.** The briefed `372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host.
  - I used a copy of the lane's manager wrapper, which points at the same container-layer binary. It reports `Verilator 5.050 2026-07-01 rev v5.050`; the binary's sha256 is in `receipts/02_tool_identity.log`.
  - The wrapper only rewrites `-j 0` to `-j 8`. Parallelism inside test_builder elaborations was not separately bounded or logged.
- **Not run:**
  - The full milan_dp `run`: gptp-lat, nxndv, nxn8, nxn4c, nolpf, prune, ax1x1 and notify were not run here.
  - `run_all_suites.sh`, and the PP, gPTP and Yosys banks.
  - `crflic-mutants` and `gmstep-mutants --all`.
  - The nvm_capture_cpu re-measurement itself, which needs the product LiteX tree and CPU netlist.
  - act and host act_ci.
  - OOC area.
  - Physical calibration was NOT RUN, and field skips are not hardware proof.
- **SDK mode** mapped `subprocess.run` calls on the fixed selector to a scratch SDK extraction verified by digest. Any compiler call made outside `subprocess.run` would reach the pre-existing home SDK, which was used, not modified.
- **Builder gate 11** (mf48 calibration report absent) did not run in either mode. Gate 1b is absent by design in compiler-absent mode.
- **Hosted evidence** is PR #566's `pull_request` merge ref (the PR plus live dev), not this candidate. It is read-only and cited for F1 confirmation only. Hosted acceptance is the manager's.
- **Disclosed mistakes.**
  - One stray test_builder invocation was stopped early and left no receipt; the tree was verified clean afterwards.
  - The first `clone_integrity.sh` run misparsed `ls-tree` fields. It was fixed and rerun, and the receipt is the corrected run.
- **Clone integrity** after all probes (`receipts/98_clone_integrity.log`):
  - HEAD and tree are exact, the index equals HEAD, and status is clean.
  - 908 tracked entries match in bytes and mode, and no index flags are set.
  - Gitlinks `gptp-processor 5dce647a`, `protocol-processor 990f9652` and `verilog-axis 48ff7a7e` are at their recorded commits and clean. `external` is not checked out.
  - Ignored build outputs remain in suite `obj_*` directories.

## Pending manager duties

1. Resolve F1 before merge: publicly assign the capture re-measurement for the composed firmware, then re-run `check_nvm_capture.py` and the hosted `docs-check` (steps 30-51 executed) on the exact candidate. Re-review the refreshed receipt.
2. The final current-dev candidate (source base 551e4b5d, live dev 1299b461) will show F1 as well, because live dev already carries #559.
3. Exact-candidate hosted `rtl-fast`, `verilator-suites` and `yosys-portability`; trusted act; maintainer merge authorization; post-merge containment.
4. #495 keeps the two carried suggestions.

R249-4 FINISHED
