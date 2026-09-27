[R348] POSITIVE - exact head 3ef7ed1b2508988f7bd9b67efef7bb6c9249dae9

# R348-3: composition review of #397 / PR #588 on the merge-train candidate

- Candidate: `3ef7ed1b2508988f7bd9b67efef7bb6c9249dae9`, tree `e6a2ed3b09ed3f1442a49227b3529da9459f4017`.
- The candidate's parents are `10a5bf59a6a73e9b6487d9ea6f42669ce142ae25` (C_396) and PR head `ff75a70807c151517860c73a06d7ea36e2a46008`.
- Source base of the PR: `ac18b50968b12efe4d15c0a06301264b35656b31`.
- Role: independent composition reviewer. Scope: composition acceptance only.
- The PR source was reviewed POSITIVE by R348-2 and R349-2 at `ff75a708`.

Verdict: the composed tree adds no defect beyond the reviewed sources. The review has one SUGGESTION and no open BLOCKER, MAJOR or MINOR.

## 1. Reconstruction

I read these in order:

1. AGENTS.md and CONTRIBUTING.md (verification, em-dash and merge rules).
2. docs/README.md.
3. The #397 body.
4. The manager's public comments on #397:
   - readiness correction;
   - owner decision of 2026-09-23;
   - lane assignment;
   - re-scope to the product-CPU simulation, with `nvm_capture_cpu` read-only and firmware unchanged;
   - the round-2 assignment;
   - the decision for option (a).
5. The manager's comments on PR #588: builder-bank FAIL 45/48 at `7f997b60` (receipts moved off-tree), and the R348-3 start.
6. The diff `10a5bf59..3ef7ed1b`, and the predecessor diff `ac18b509..10a5bf59`.
7. The protocol-processor pin change `0922e434..870ff88a`.
8. Public executable evidence:
   - the `397-review-evidence` author receipts `round2-{1x1,8x8}-all.json`;
   - their sha256 values match the table in `docs/findings/397_SERVICE_BUDGET.md`.

I read no reviewer report, private author material or management directory before writing the verdict and ledger. The author handoff files in the evidence tree were not opened. Only the receipt JSONs and the evidence MANIFEST were read.

## 2. Composition facts (receipts/composition.txt)

- **The candidate patch equals the source patch.** `git diff 10a5bf59 HEAD` and `git diff ac18b509 ff75a708` have identical bodies once index and hunk headers are dropped. 11 of the 13 PR files are byte-identical blobs to the source head.
- **Textual overlaps with predecessors:** exactly `docs/integration/BAREMETAL_FIRMWARE.md` (#565) and `docs/testing/TESTING.md` (#502, #396). Both merge textually clean.
- **Semantic interactions found and examined:**
  1. The harness reuses `tb/verilator/nvm_capture_cpu`, which #565 changed.
     - `soc.py` and `recipe.py` changed by one comment or docstring line each.
     - `measurements.json` was re-measured.
     - `firmware.py`, `probe.py` and `run.py` are unchanged.
     - The monkeypatched names `build.py` depends on are unchanged: `ProductSimulation.add_spi_flash`, `_firmware_constants`, `firmware.prepare`, `soc.milan.nvmmem_{req,rsp}_sys` and `soc.bus.slaves['milan_csr']`.
     - `sw/firmware` and `sw/litex` are unchanged since the source base.
  2. Parent RTL on the measured path changed.
     - `milan_csr.sv` and `KL_nvm_backend.sv` changed in comments only. `VERSION` stays `0x0002_0060`.
     - #502 made functional changes to `KL_pp_shadow.sv` and `milan_datapath.sv`. The processor pin moved `0922e434` to `870ff88a`, adding `aecp_name_wr_o`.
     - These changes raise `nvm_pend` only on accepted AECP live name writes (`KL_aecp_desc_store` `name_wr_o = take_wr_w && st_name_i`) or on map-edit phase-5 writes (`amap_edit_live_wr_p` requires `pp_amap_edit_req_w`).
     - Both require AECP packet traffic. The harness forces `args.traffic = 'off'` (`tb/verilator/fw_service_budget/run.py:442`) and builds with `with_mac=False` (`tb/verilator/nvm_capture_cpu/soc.py:137`).
     - The pending source feeding the firmware's `nvm_dirty` commit trigger is therefore unreachable in every harness plan.
  3. `configs/endstation_ax7101_8x8.yaml` now declares 50 MHz (#565).
     - I derived both shapes' artifacts with the repository's builder and descriptor generators, at the source base and at the candidate (`aem_probe.py`; receipts `aem-*.json`, `generated-artifact-diff.txt`, `generated-8x8-diff-detail.txt`).
     - The AEM images are byte-identical: 1x1 is 7,352 B `9b077636...` and 8x8 is 18,288 B `193bf187...`. The shape headers are also identical.
     - The 8x8 AEM sha equals the receipt's `build/aem_desc.bin`.
     - The 1x1 generated set is identical.
     - For 8x8, only the clock-derived outputs differ: `gptp_ucode.hex` (7 words), `lwsrp_table.svh` `LWSRP_CLK_FREQ_C` (100 MHz to 50 MHz), `soc_params.json`, `lwsrp_table.json` and `build_plan.md`.
  4. Receipt input drift (`receipt_drift.py`, receipt `receipt-input-drift.txt`).
     - Against the source base, every recorded tracked input matches, apart from files absent from that base, so the published receipts describe `ac18b509` exactly.
     - Against the candidate, 14 recorded inputs differ for the 8x8 receipt and 13 for the 1x1 receipt: the items above plus the 8x8 generated `lwsrp_table.svh`.
     - The harness binds reuse and regrade to these hashes (`run.py:171-172`, `run.py:453`, `run.py:461`). A stale build directory is therefore refused with "stale or unbound build; rebuild" rather than silently regraded.

## 3. Gates run on the candidate (receipts/gates/, script gates.sh)

- Tools:
  - Python 3.14.7 through the repository docs venv.
  - Verilator 5.050, rev v5.050, `verilator_bin` sha256 `44898b22...`.
- About the Verilator path:
  - The directed path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host.
  - I wrapped the same pinned 5.050 install that the #397 candidate tool directory references and checked its identity with `--version`.
  - None of the gates below compiles with Verilator.
- All 38 commands returned 0:
  - `make -C tb/verilator/fw_service_budget` and `run.py --self-test`: 30 oracle checks and 14 flash checks, 0 failures.
  - `test_nvm_firmware.py --self-test`.
  - `check_nvm_capture.py`: "capture census, clocks, both timing arms and receipt agree".
  - `check_feature_status.py` and its `--self-test`.
  - `pp_srcs.py --check --selftest`.
  - `check_baremetal_only.py` with `--check` and `--selftest`.
  - `check_entity_shape.py --self-test`.
  - `docs_check.py`: 0 findings over 171 md files.
  - `check_doc_paths.py`, `check_doc_style.py`, `check_archive.py`.
  - `gen_toc.py --check` and `--verify-anchors` (188 fragments).
  - `check_em_dash.py --base 10a5bf59` (0 findings over 575 added lines), `--base ac18b509`, and `--selftest`.
  - `check_solution_docs.py`, `check_submodule_docs.py`, `check_todo_ownership.py`.
  - py, cpp and sh idiom ratchets.
  - `check_hygiene.py --check`, `measure_naming.py --check`, `measure_fail_fast.py --check`.
  - `measure_test_evidence.py --check`: 76 <= 77.
  - `suite_shards.py --selftest`.
  - `ci_events.py` with `--check` and `--selftest`.
  - `ci_scope.py --selftest`.
  - `git diff --check` from both bases.
  - Working tree clean afterwards.
- Suite inventory (`suite_shards.py --suite-root tb/verilator`): 56 suites. `fw_service_budget` is present and `nvm_capture_cpu` stays excluded (receipt `suite-inventory.txt`).
- Disposable probes on an archive copy of the candidate (`probe_selftest.sh`, receipt `selftest-probes.txt`):

  | Probe | Result |
  | --- | --- |
  | Control | rc 0 |
  | Added firmware `define_command` | rc 1, "product dispatch census changed" |
  | Period budget 500 changed to 900 | rc 1, "control trace changed" |
  | Restored control | rc 0 |

## 4. Decisive questions

1. **Composed `BAREMETAL_FIRMWARE.md`: consistent.**
   - #565's build contract is intact at lines 34-64: the enforced checks, "The 50 MHz target is not checked by either tool", and the 8x8 50 MHz declaration.
   - #397's four lines sit in the Runtime paragraph at lines 1893-1896.
   - They add queued-input idle-hook suppression and the #590 owner. They say nothing about clocks, so they cannot contradict the 50 MHz contract.
2. **Composed `TESTING.md`: each entry appears exactly once.**
   - #502 `pending-mutant` row: line 268.
   - #396 "Standing release campaigns": line 846 under `## 6d`.
   - #397 `fw_service_budget` paragraph: lines 404-407 in section 1.1.
   - Inbound anchors `#6d-unattended-campaign-vehicle` and `#6b-bench-evidence-retention` resolve, and `gen_toc.py --verify-anchors` passes.
3. **Harness on the candidate: builds, and its `--self-test` passes.**
   - The portable build (`make`, which compiles `flash_test.cpp`) and the self-test pass. `check_nvm_capture.py` passes.
   - The full product-CPU build and simulation were **not** run: no LiteX/migen environment is provisioned for this review.
   - The composition evidence in section 2 stands in its place:
     - the capture reuse contract is unchanged;
     - the RTL deltas are unreachable without traffic;
     - the only 8x8 generated-input change is clock-derived fabric constants.
   - This is analysis, not a measurement.
4. **Docs gates on the candidate:** all pass (section 3).

## 5. Findings

### R348-3-S1 - SUGGESTION - Docs, Conformance - `docs/findings/397_SERVICE_BUDGET.md:5-6,25-27,352`: the page's 8x8 provenance reads stale once #565 lands

- **Authority/evidence:**
  - Candidate `configs/endstation_ax7101_8x8.yaml:56` declares `milan_clk_hz: 50000000`. `tb/verilator/nvm_capture_cpu/README.md:45` says both shapes declare the contract clock after #565.
  - The page says the 8x8 Milan-clock declaration "is overridden by the existing capture recipe to satisfy this assignment's explicit 50 MHz contract". It also says firmware, RTL, submodule pins and capture hashes "remain unchanged".
  - The published 8x8 receipts were built from the 100 MHz declaration. Their generated `lwsrp_table.svh` sha is `59bfe055...` at `LWSRP_CLK_FREQ_C = 100000000`, and the gPTP ROM matches, while the CPU and Milan clocks ran at 50 MHz.
  - A merged-tree 8x8 build generates 50 MHz constants, and the #502/processor RTL and the capture harness hashes differ from the recorded inputs.
  - The page pins its product base explicitly (line 5), so no sentence is false. It is merely no longer the current tree's state, and the 100 MHz-derived fabric constants in the measured 8x8 build are not stated.
- **Impact:**
  - A reader of merged `dev` may take the 8x8 figures for a measurement of the tree they are reading.
  - The expected effect on firmware service figures is nil: no traffic, and the PHC and backend liveness intervals in the receipts already run at the 50 MHz rate (250.00068 ms erase heartbeats, 1,999.04 ms backing lapse). This is an argument, not a re-measurement.
- **Required outcome (optional):** when the page is next touched, for example by the #590 re-measure, state these three things:
  - the figures are for `ac18b509`;
  - that measurement's 8x8 generated gPTP and lwSRP constants followed the then-100 MHz declaration;
  - #565 and #502 changed the declaration and packet-side RTL afterwards.
- **Verification:** the next measurement receipt's recorded `configs/endstation_ax7101_8x8.yaml` and `lwsrp_table.svh` hashes match the tree it is published in, and the page text agrees.

No BLOCKER, MAJOR or MINOR finding.

## 6. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN (S1 is a SUGGESTION) | #397 body and the manager's scope and decision comments; `BAREMETAL_FIRMWARE.md:34-64,1889-1896` (50 MHz contract vs the #397 note); the 1x1 and 8x8 derivations and generated-artifact diff (AEM bytes identical, 8x8 clock constants changed); receipt input drift; `check_nvm_capture.py`, `check_baremetal_only.py`, `check_feature_status.py` | R348-3 (this round, composition). Source content covered by R348-2 and R349-2. | `3ef7ed1b2508988f7bd9b67efef7bb6c9249dae9` |
| RTL | CLEAN | The PR changes no RTL. The composition touches the measured path through predecessor RTL: `KL_pp_shadow.sv` (`latch_live_pending`, `nvm_pend_w`), `milan_datapath.sv` (`amap_edit_live_wr_p`), processor `KL_aecp_desc_store.sv` (`name_wr_o`), `KL_aecp_engine.sv`, `protocol_processor_top.sv` (`0922e434..870ff88a`), and the comment-only `milan_csr.sv` / `KL_nvm_backend.sv`; checked against harness `run.py:442` (`traffic='off'`), capture `soc.py:137` (`with_mac=False`), `build.py` observation taps and `observe.vlt` (CPU netlist unchanged) | R348-3 (composition). Source RTL scope covered by R348-2 and R349-2. | `3ef7ed1b2508988f7bd9b67efef7bb6c9249dae9` |
| Robustness | CLEAN | Reuse and regrade binding to input hashes (`run.py:153-183,451-461`), shown by `receipt-input-drift.txt` to refuse a source-base build on the candidate; unsupported wait inputs refused (wait controls inside `--self-test`); census failure on an added firmware command (probe) | R348-3 (composition). Source covered by R348-2 and R349-2. | `3ef7ed1b2508988f7bd9b67efef7bb6c9249dae9` |
| Tests | CLEAN | `make -C tb/verilator/fw_service_budget`, `run.py --self-test` (30+14), `test_nvm_firmware.py --self-test`, `check_nvm_capture.py`; four disposable probes (2 planted faults caught, 2 controls pass); suite inventory (56, harness included); test-evidence, naming, idiom, fail-fast and hygiene ratchets on the composed tree | R348-3 (composition). Source covered by R348-2 and R349-2. | `3ef7ed1b2508988f7bd9b67efef7bb6c9249dae9` |
| Docs | CLEAN (S1 is a SUGGESTION) | Composed `BAREMETAL_FIRMWARE.md`, `TESTING.md` (lines 268, 404-407, 846) and `docs/findings/README.md:11`; `397_SERVICE_BUDGET.md`; harness `README.md`; `docs_check`, `check_doc_paths`, `check_doc_style`, `check_archive`, `gen_toc --check/--verify-anchors`, and `check_em_dash` from `10a5bf59` and `ac18b509` plus its selftest | R348-3 (composition). Source covered by R348-2 and R349-2. | `3ef7ed1b2508988f7bd9b67efef7bb6c9249dae9` |

Every lens is touched by the composition, through shared docs, the reused capture harness, or predecessor RTL on the measured path. Each was applied in this round rather than inherited.

## 7. Prior public review findings on this PR

I read these after sections 1-6 were written: R349-1 and R348-1 (NEGATIVE, `7f997b60`), and R349-2 and R348-2 (POSITIVE, `ff75a708`).

Every file that carries a closure below is byte-identical between `ff75a708` and the candidate (receipt `composition.txt`): `run.py`, `oracle.json`, `flash.hpp`, `flash_test.cpp`, `sim_main.cpp`, harness `README.md` and `397_SERVICE_BUDGET.md`. The candidate's portable gate reruns the pinned traces (30+14 pass).

| Prior finding | Severity | Status at `3ef7ed1b` | Basis |
| --- | --- | --- | --- |
| R348-1 F1 = R349-1 F1 (heartbeat/liveness) | MAJOR | Resolved, not reopened | Closure text and receipts-derived tables are unchanged. The composed `BAREMETAL_FIRMWARE.md:1893-1896` keeps the queued-input lapse note and the #590 owner. The composition adds no traffic path that alters liveness (section 2, item 2). |
| R348-1 F2 = R349-1 F2 (self-test pins) | MINOR | Resolved | `oracle.json` trace controls pass on the candidate. The period-budget probe is caught ("control trace changed"). |
| R348-1 F3 = R349-1 F3 (AEM envelope) | MINOR | Resolved | Same code. The AEM image bytes are identical at the candidate (`aem-*.json`), so the marked envelope input is unchanged. |
| R348-1 F4 (busy control) | MINOR | Resolved | `flash_test.cpp` and `flash.hpp` unchanged; 14/14 flash checks pass. |
| R349-1 F4 / R348-1 S1 (ADP valid time) | MINOR / SUGGESTION | Resolved | Unchanged page and code; the manager's decision is recorded on #397. |
| R349-1 F5 (wait range) | MINOR | Resolved | `validate_waits` unchanged; wait controls pass inside `--self-test`. |
| R349-1 S1 (SPI bias direction) | SUGGESTION | Resolved | Page text unchanged. |
| R348-1 S2 (ignored build outputs) | SUGGESTION | Resolved | README text unchanged. |
| R349-2 S2, S3, S4; R348-2 S1, S2, S3 | SUGGESTION | Retained, unchanged | These are not composition matters and do not affect coverage. R348-3-S1 above is a separate composition-only suggestion. |

No prior BLOCKER, MAJOR or MINOR finding is open at this head.

## 8. Real limits

- **Product-CPU build and measurement not run on the candidate.**
  - The harness's product-CPU build and the eight plans were not run: this review has no LiteX/migen environment or RV32 SDK provisioned, and installing one is outside what this review may do.
  - The source rounds rebuilt at `ff75a708` and reproduced the receipts bit-exact. The candidate's recorded inputs differ (section 2, item 4), so those reproductions do not transfer byte-for-byte.
  - My argument that the firmware service figures are unaffected is static:
    - the RTL deltas are unreachable without AECP traffic;
    - `milan_csr` and `KL_nvm_backend` changed in comments only;
    - AEM bytes are identical;
    - the 8x8 changes are clock-derived fabric constants only.
  - This is not a re-measurement.
- **Directed Verilator path missing.** The directed Verilator 5.050 path does not exist. I used the same pinned 5.050 install through my own wrapper, checked with `--version`. No gate in this round compiled with Verilator.
- **Scratch trees lack `third_party/verilog-axis`.** The archived scratch trees omit it, so four receipt entries report ABSENT against the source base. The gitlink `48ff7a7e` is unchanged.
- **No hosted or act evidence.** I did not inspect or run any: the candidate is not a PR head, and the manager owns that acceptance.
- **Physical proof not run.** Physical calibration, the AX7101 torture (acceptance 4) and field behaviour were not run. Nothing here is hardware proof.
- **Clone restored.** The clone is at exact head bytes (receipt `clone-integrity.txt`):
  - HEAD `3ef7ed1b`, tree `e6a2ed3b`, and `write-tree` equals the tree;
  - `diff-index` is clean, with 0 untracked or ignored changes;
  - the gitlinks `external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `870ff88a` and `third_party/verilog-axis` `48ff7a7e` are unchanged;
  - the three initialized submodules are clean at their pins, with ignored files included;
  - `external` is uninitialized, as it was at the start.
  - The gate run left ignored Python bytecode caches in the clone: `avdecc/`, `scripts/`, `sw/litex/platforms/` and `protocol-processor/hdl/aecp/desc/`. Every file in them was newer than the session start. I removed them.
  - All probes ran on scratch copies.

## 9. Pending manager duties

- Candidate banks at `3ef7ed1b`: static, builder, native, and the product-CPU `fw_service_budget` build with at least one plan per shape. If the manager wants the figures confirmed on the composed product, this also confirms the static argument in section 8.
- Hosted and act acceptance.
- Final current-`dev` candidate validation at the merge turn (live `dev` `9e9954e9`), then post-merge containment.
- Merge authorization.
- Keep #397 open ("Refs #397") for acceptance 2-4 after #590.
- Optionally carry R348-3-S1 into the #590 re-measure.

## 10. Packet

- Scripts:
  - `gates.sh`
  - `composition.sh`
  - `aem_probe.py`
  - `receipt_drift.py`
  - `probe_selftest.sh`
- Receipts are under `receipts/`, and every published file is listed in `MANIFEST.sha256`.
- `scratch/` (extracted trees, generated artifacts, downloaded receipts) is not published.

R348-3 FINISHED
