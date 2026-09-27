[R348] POSITIVE - exact head ff75a70807c151517860c73a06d7ea36e2a46008

Round R348-2, internal independent review of PR #588 for issue #397 (service-budget measurement, measurement-only). Exact head `ff75a70807c151517860c73a06d7ea36e2a46008`, tree `aa2fd7c8fe3499303efa316650e73b45b341dcf5`. The head is one commit (`ff75a708`) on round-1 head `7f997b60`, over source base `ac18b50968b12efe4d15c0a06301264b35656b31`. This is a delta review of `7f997b60..ff75a708` against the round-2 assignment (issuecomment-5855879265).

Reconstruction order:
1. AGENTS.md and CONTRIBUTING.md; docs/README.md.
2. The #397 body; re-scope issuecomment-5854787465; round-2 assignment issuecomment-5855879265; the builder-bank comment on PR #588 (issuecomment-5855512699); #590.
3. SAVED_STATE_FASTCONNECT.md section 9.4; BAREMETAL_FIRMWARE.md; `KL_nvm_backend` liveness semantics; the product firmware.
4. The diff and history.
5. The public evidence branch `397-review-evidence` (the requested snapshot `7a649d0c`, plus the author's round-2 packet `review-evidence/397-r1/author-r2/`, now at `bcc86c8d`).

I read the round-1 external review's public findings only after my own pass over the diff. I read no current-round review by anyone else.

Summary: every round-1 finding from both reviews is closed at this head, with executed evidence.

- **Reproducibility.** I rebuilt both shapes from the exact head and ran all eight named plans (`all`, `uart-paced`, `queued-input`, `device-wait` at 1x1 and 8x8). Every run reproduces its published receipt bit-exact: the same raw-log SHA-256, rows, budget findings, heartbeat record, liveness samples and input hashes. All 42 numeric rows of the findings page recompute from the published receipts, and again from my own runs, with no mismatch.
- **Round-1 probes, rerun unchanged.**
  - The three-command probe PD lapses liveness exactly as the page states.
  - PA, PB, PC and PD reproduce their round-1 stdout logs and probe side files byte for byte.
  - My 15 round-1 grader mutants now all fail the self-test (round 1: 4 of 15).
  - Deleting the flash busy predicate now fails its named control.
- **Gates.** The three builder-bank gates that failed at `7f997b60` pass, as do the docs, harness, host-model and capture gates.
- **Protected paths.** Firmware, capture harness, RTL, LiteX and submodule pins are unchanged.

No BLOCKER, MAJOR or MINOR finding is open. Three SUGGESTIONs follow; they do not affect coverage.

## Round-1 findings: disposition at this head

| Finding | Status | Evidence at `ff75a708` |
|---|---|---|
| R348-1 F1 = R349-1 F1 (MAJOR, heartbeat/liveness) | **Closed** | See "F1" below |
| R348-1 F2 = R349-1 F2 (MINOR, self-test does not pin markers/conversion/deadlines) | **Closed** | `run.py:342-410`, `oracle.json`: complete rows, findings, heartbeat and liveness of three fixed traces are pinned. `receipts/mutation-grader-r1suite.txt`: 15/15 of my unchanged round-1 mutants fail `--self-test` (hb marker = START, bitmask, final tail dropped, enable bit 1, boot start 0, walk end, CPU 1:1, ms at 50 MHz, budget scale x2 both ways, command-end shift, status budget 8000, commit budget 500, WIP not subtracted, erase envelope to ACK); unmutated control passes. The control count is computed (`run.py:409`), not a literal. Receipts are emitted whole by `run.py:473-480`; no manual assembly step. |
| R348-1 F3 = R349-1 F3 (MINOR, AEM bounded by the whole boot) | **Closed** | `sim_main.cpp:72-76` + `flash.hpp:101-104` mark the first read whose address `0x400000` (= generated `MILAN_AEM_FLASH_OFFSET`) is accepted; `run.py:289-291`. `all`-plan rows: 1x1 255.20053 -> 310.97023 ms = 55.77034 ms; 8x8 896.67231 -> 1031.43961 ms = 134.76794 ms. My unchanged probe PA (fabric/SPI observer) gives first AEM read 255.21 ms and read-completion-to-enable 55.76 ms (`receipts/probe-PA-1x1.txt`); PD gives 896.67788 ms and 134.76237 ms at 8x8. The page states the marker and why the observer figure is slightly shorter (`397_SERVICE_BUDGET.md:44-48`); "no narrower marker" is gone from every changed file. |
| R348-1 F4 (MINOR, busy control cannot fail) | **Closed** | `flash_test.cpp:67-75`. Deleting `cycle < busy_until_` from `flash.hpp:72` now fails "program while busy refused" (13/14 pass); unmutated 14/14 (`receipts/mutation-flash-busy.txt`). The control's non-monotonic test times are stated as such (`README.md:167-169`, page `:322-325`). |
| R348-1 S1 / R349-1 F4 (ADP valid time) | **Closed** | Boot-to-enable is compared with 20,000 ms (valid_time 10 in 2 s units, Milan v1.2 5.6.2/5.6.3), per the manager's decision in item 5; BIOS CRC, delays and memory test are named as excluded and physical boot acceptance is disclaimed (`397_SERVICE_BUDGET.md:102-106`; `run.py:290`). |
| R348-1 S2 (build writes ignored files in the checkout) | **Closed** | `README.md:31-32` now says so. |
| R349-1 F5 (`--device-wait-us` range) | **Closed** | Separate `--device-wait-us`/`--program-wait-us` (`run.py:426-427`), bounded 0..3,000,000 and 0..5,000 us (`run.py:51-56`), which include the section 9.4 corner. `receipts/cli-wait-refusals.txt`: 3,000,001, -1, 4,294,967,296 (erase) and 5,001, -1 (program) exit 1 with the named error and create no build directory; the corner itself is accepted and was executed (`device-wait` runs, both shapes, reproduced bit-exact). Largest supported WIP 4 x 3 s + 100 x 5 ms = 12.5 s; the longest executed no-WIP plan (8x8 `uart-paced`, final prompt 5,191.30 ms) leaves the 30 s guard satisfied. |
| R349-1 S1 (SPI bias direction) | **Closed** | `397_SERVICE_BUDGET.md:279-285`, `README.md:148-151`: optimistic, 65 vs 67, 257 vs 259, +11 at CS reassertion. |
| Builder bank (manager, issuecomment-5855512699) | **Closed** | `docs/findings/397_SERVICE_BUDGET_{1X1,8X8}.json` are deleted. `pp_srcs.py --check`, `check_baremetal_only.py --check` (0 findings, 907 files) and `check_entity_shape.py --self-test` (136 checks, 0 failures) return 0 at this head (`receipts/gates-builder-three.txt`). The ten receipt SHA-256 values at `397_SERVICE_BUDGET.md:362-373` equal the files at `review-evidence/397-r1/author-r2/receipts/` on `397-review-evidence` (`bcc86c8d`). |

### F1 (heartbeat and liveness), point by point

The assignment's item 1 has five parts. Each is met, and each checks out against executed evidence.

1. **Which intervals a gap spans; that queued input suppresses the idle hook.** `397_SERVICE_BUDGET.md:174-177, 201-217` and `README.md:127-132`. The endpoints in the schedule table are exact. They recompute from every receipt's heartbeat record, and so do "Final tail?" and the backing samples (`receipts/table-recompute-r2.txt`).
2. **For each duty, the longest stretch with no tick opportunity, and the period bound (250 ms phase + stretch + TX), against 500 ms.** `397_SERVICE_BUDGET.md:122-172`; `run.py:75-133`.
   - **Observer (static check).** The opportunity observer samples the CPU's committed PC at the linked `nvm_heartbeat_tick` entry (`build.py:104-126`, `sim_main.cpp:34`, `observe.vlt`). I checked it statically (`receipts/heartbeat-entry-static.txt`):
     - the ELF has exactly one out-of-line `nvm_heartbeat_tick` (8x8 `0x66ec`, 1x1 `0x6658`);
     - there are 5 `jal` call sites, equal to the 5 source call sites, with no tail call and no inlined strobe store;
     - the pinned netlist (`c208df0b...`) has a single commit port (`ports_0` only).
   - **Observer (dynamic check).** In all eight receipts, every `PP_NVM_STAT <- 1` strobe follows an observed entry by 495-575 system cycles. No closed strobe gap exceeds 250 ms plus the longest no-entry span inside it (`receipts/liveness-observer-check.txt`, and the same result on my own runs). So the bound model is consistent with what the product does.
   - **Observation does not perturb.** Stripping the new `ticks`/`aem_read` lines from the head's `all` logs gives the round-1 raw logs byte for byte at both shapes (`receipts/strip-compare-*.txt`).
3. **2,000 ms T-NVM-WRITER-ALIVE, with the printed backing evidence, and whether queued input lapses each shape.**
   - `397_SERVICE_BUDGET.md:190-245`. Both `queued-input` runs reproduce bit-exact (`receipts/rerun-*-queued-input.txt`).
     - **1x1.** The only strobe is at 252.58315 ms. Samples by command index are 1 through index 8 (2,188.86040 ms) and 0 from index 9 (2,397.34614 ms).
     - **8x8.** The only strobe is at 893.96257 ms. The samples are 1, 1, 0, 0.
   - My unchanged probe PD shows the same directly in the fabric (`receipts/probe-PD-8x8-status3.txt`). `backed_r` falls at 2,893.00065 ms, 1,999.0381 ms after the only kick, with `alive=0`, `stale=1`, and the third status prints `backed=0 dirty=0 stale=1`. That matches the page's `:221-222` exactly.
   - The page states the lapse in both shapes (`:7`, `:242`) and routes the repair to #590, per the manager's decision.
4. **WIP polling at device-length waits, executed.** I reran the `device-wait` plans (3 s erase, 5 ms page) at both shapes and they reproduce bit-exact. Each erase envelope contains 12 strobes at a maximum spacing of 250.00068 ms. The heartbeat-free read-back remains: 8x8 START-to-ACK has a 470.23145 ms no-tick tail, 4,869.01 to 5,339.25 ms (`receipts/device-wait-heartbeats.txt`). The page says exactly this (`:256-277`).
5. **Heartbeat row removed or qualified; named plans.** The "Maximum heartbeat gap" row is gone from both duty tables. It survives only in the plan-qualified schedule table, and in receipts as `maximum_heartbeat_gap`, which carries `plan`. `uart-paced` and `queued-input` are named `--plan` modes (`run.py:20, 41-48, 425`; `sim_main.cpp:45-52, 105, 112`), documented at `README.md:45-59`.

## Findings

None at BLOCKER, MAJOR or MINOR.

**S1 - SUGGESTION - Tests - `tb/verilator/fw_service_budget/run.py:41-48`, `:342-410` - The named plan definitions are not pinned by the portable self-test.**
- Evidence: in `receipts/mutation-grader-r2.txt`, 16 of 17 new mutants aimed at the round-2 code fail `--self-test`. Those 16 cover the 250 ms phase, the 2,000 ms margin, the TX baud and owner, each tick-span term, the `PP_STAT[6]` bit, right-censoring, the AEM start, the boot and restore budgets, both wait limits, and the per-command WIP sum. The one that passes changes the 8x8 `queued-input` length from 3 to 12 commands.
- Why this is only a suggestion: a regrade of the published 8x8 receipt would still refuse on the command census, so no published number can drift silently. A future edit could still redefine a documented named mode without any gate noticing.
- Optional change: assert each plan's command tuple in the self-test.

**S2 - SUGGESTION - Docs - `docs/findings/397_SERVICE_BUDGET.md:356-360` - Name where the hashed receipts live.**
- The ten SHA-256 values are correct, and the evidence branch is linked at `:226`.
- The page still says the packet "is prepared for the manager to publish" and gives no path. A cold reader has to search the branch for `review-evidence/397-r1/author-r2/receipts/`.
- Optional change: add that path (and the branch) next to the hash table.

**S3 - SUGGESTION - Docs - `docs/findings/397_SERVICE_BUDGET.md:218-219` - Say that "command 8" and "command 9" are zero-based.**
- They are the receipts' `command_index` values: the 9th and 10th of the thirteen commands.
- #590 and the original P3 text describe the same events by elapsed time, so a reader cross-checking can be off by one.

## Verification detail

- **Builds.** I built both shapes from the exact head: pinned LiteX revisions with the product patches, the cached CPU netlist `c208df0b...`, the RV32 SDK and Verilator 5.052 (`scripts/build_shape.sh`).
  - Against the published receipts' `build_hashes`, 143 of 150 entries are equal at each shape, including `bios.bin`, `retirement.hpp`, `aem_desc.bin` and all harness and product sources.
  - The 7 that differ are generated headers, `sim.v`, `bios.elf` and the native binary, which embed build paths and times (`receipts/build-compare.txt`).
  - Every raw log is nonetheless bit-identical to the published one.
- **Runs.** All eight plans ran with the published arguments (`scripts/run_plan.sh`), and every one reproduces its receipt exactly (`receipts/rerun-*.txt`).
  - Wall times were 578 s to 3,186 s on a shared host.
  - Six published receipts lack the `media.shape` key, because they were regraded from preserved native runs, as the page says at `:346`. That does not affect any row: fresh head runs add the key, and everything else is equal.
- **Regrade integrity** (`receipts/regrade-refusals.txt`):
  - `--regrade` of the 1x1 `all` log passes;
  - one appended byte fails with "recorded log changed";
  - the default mode refuses the queued-input budget finding (rc 1), and `--record-budget-findings` retains it (rc 0).
- **Tables.** `scripts/check_tables_r2.py` parses every table of the findings page and recomputes all of them. That is 28 duty and opportunity rows, including the plan-at-maximum, TX-allowance and bound arithmetic, 8 schedule rows and 6 device-max rows. It uses both the published receipts and my own runs: 42 rows each, 0 mismatches.
- **Gates at this head** (`receipts/gates-docs-harness.txt`, `receipts/gates-builder-three.txt`). All of the following return 0:
  - `run.py --self-test`; `make -C tb/verilator/fw_service_budget`;
  - `test_nvm_firmware.py --self-test`; `check_nvm_capture.py`; `check_feature_status.py --self-test`;
  - `docs_check`, `check_doc_paths`, `check_doc_style`, `check_archive`, `gen_toc --check`, `check_em_dash --base ac18b509`;
  - `git diff --check ac18b509 ff75a708`; `check_py_idiom`, `check_cpp_idiom`, `check_hygiene --check`, `measure_test_evidence --check`;
  - `pp_srcs --check`, `check_baremetal_only --check`, `check_entity_shape --self-test`.
- **Protected paths** (`receipts/protected-paths.txt`).
  - `git diff ac18b509..ff75a708` touches only the 13 listed files.
  - The `7f997b60..ff75a708` delta touches 12 of them, including the deletion of the two raw receipts.
  - `milan_baremetal.c` (blob `a4e560fb`, SHA-256 `0bf43cd4...47a6`), `tb/verilator/nvm_capture_cpu`, `hdl`, `sw/litex`, `configs` and all four gitlinks are identical at base and head.
- **Round-1 probes at this head** (`receipts/probe-raw-sha256.txt`, `receipts/probe-P*.txt`). I recompiled my unchanged round-1 probe driver against the head builds and reran PA (1x1 `all`), PB (8x8 `all`), PC (8x8 one commit at 3 s / 5 ms WIP) and PD (8x8 three queued statuses). All eight output files (four stdout logs, four side files) have the same SHA-256 as in round 1. PC: commit START-to-ACK 3,856.7271 ms, largest fabric-kick gap 588.61054 ms, no backing lapse. These equal the page's PC row and its `device-wait` 8x8 figures.
- **Public probe provenance** (`receipts/public-probe-log-identity.txt`). The author's reruns of P1, P2, P3, PC and PD are byte-identical to the logs the round-1 reviews published.
- **PR state.** PR #588's head is `ff75a708` and it says "Refs #397" with no closing keyword, correct while the decision and board proof remain open.
- **Hosted evidence.** A snapshot at this head is in `receipts/hosted-checks-at-head.txt`. `rtl-fast` succeeded; Verilator shards 1/5 and 4/5 were still in progress; physical gPTP was skipped. This is recorded for the manager, not accepted by this round.

## Lens ledger (reviewer-owned)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #397 acceptance 1 and 3; re-scope 5854787465; assignment 5855879265 items 1-8; SAVED_STATE_FASTCONNECT.md 9.4 (500 ms, 2,000 ms, 3 s / 5 ms); `397_SERVICE_BUDGET.md:19-290`; `run.py:41-56,259-339`; generated `MILAN_AEM_FLASH_OFFSET`; 42 recomputed rows; queued-input lapse in both shapes (receipts + probe PD fabric lapse at 1,999.04 ms) | R348-2 | ff75a70807c151517860c73a06d7ea36e2a46008 |
| RTL | CLEAN | `observe.vlt`; `build.py:89-126` (retirement header from the linked ELF, one symbol, one CPU wrapper); `sim_main.cpp:32-43,58-82,97-163` (commit-PC sampling on the aligned CPU edge, boundary flushes, AEM marker, UART pacing at 8,681 cycles, wait widths); `flash.hpp:67-104`; ELF call-site census (5/5, no inlining) and single commit port in netlist `c208df0b`; strobe-after-entry 495-575 cycles in all receipts; non-perturbation (stripped logs == round-1 logs; PA/PD side files identical to round 1) | R348-2 | ff75a70807c151517860c73a06d7ea36e2a46008 |
| Robustness | CLEAN | queued-input (both shapes, lapse reproduced), uart-paced, device-max corner executed; CLI wait refusals before any build dir; tampered-log and default-mode budget refusals; `tick_span` loud refusals (`run.py:83-93`, `tick_controls`); 30 s guard arithmetic against the longest executed plan; zero-based sample indexing checked against times | R348-2 | ff75a70807c151517860c73a06d7ea36e2a46008 |
| Tests | CLEAN (S1 optional) | `run.py:342-410`, `oracle.json` (three traces = published receipts, no local paths); `flash_test.cpp:35-81`; 15/15 round-1 mutants and 16/17 round-2 mutants caught, unmutated control passes; busy-predicate mutant caught; `make` default target; bit-exact rerun of all eight plans | R348-2 | ff75a70807c151517860c73a06d7ea36e2a46008 |
| Docs | CLEAN (S2, S3 optional) | `docs/findings/397_SERVICE_BUDGET.md` (all tables recomputed; receipt hashes verified on `397-review-evidence`); `tb/verilator/fw_service_budget/README.md`; `BAREMETAL_FIRMWARE.md:1879-1885`; `docs/findings/README.md:11`; `docs/testing/TESTING.md:403-406`; no stale round-1 claims; no references to the deleted receipts; all docs gates | R348-2 | ff75a70807c151517860c73a06d7ea36e2a46008 |

Every lens was applied at the exact merge-candidate source head. No later commit exists.

## Limits

- **Simulator.** The scoped Verilator path given for this round (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. As in round 1, I used the system Verilator 5.052. The bit-identical raw logs show the published receipts were produced by an equivalent build.
- **Background execution.** Each native run takes 10 to 55 minutes, longer than one foreground tool call allows. The eight plan runs and four probes therefore ran as detached processes, polled by foreground checks. Never more than 8 of my jobs ran at once, and none is left running.
- **Probe build.** `scripts/round1/compile_probe_j1.py` is my round-1 `compile_probe.py` with only `-j 8` changed to `-j 1`, to respect the job limit. The probe sources are unchanged.
- **Not established.**
  - One deterministic clock phase; the flash device modeled at its stream boundary (optimistic, as stated); no packet traffic; BIOS CRC, delays and memory test excluded.
  - No physical calibration, hardware or bench liveness proof. Field skips are not hardware proof.
  - The conditional period bounds are analysis for isolated duties, not a schedule guarantee, as the page says.
- **Not run.** The full parent, protocol-processor, gPTP, Yosys and builder banks; hosted or local CI replicas; the other reviewer's probes (P1-P3, `make_probe.py`), whose published logs I only compared byte-wise.
- **Clone restore.** The product build wrote two ignored ROM files into this clone, and one import wrote a bytecode cache. I removed them. The clone is at exact head bytes: no untracked or ignored files, and the index equals the tree (937 entries, modes and blobs). The four gitlinks and the initialized submodules' HEADs are unchanged and clean (`receipts/clone-integrity.txt`).
- **Shared trees.** I edited no other checkout and installed nothing. My read-only `git status` checks on the product LiteX tree refreshed its `.git` index stat caches; no tracked content changed.
- **Other reviews.** I read the round-1 external review's public findings only after my own diff pass. I read no current-round review by anyone else.

## Pending manager duties

- Publish this report.
- Own hosted and local-replica acceptance at the exact head. Two Verilator shards were still in progress at my snapshot, and physical gPTP was skipped.
- Obtain the external round-2 verdict.
- Build and validate the final candidate on the live `dev` tip (`682ecf0c`; source base `ac18b509`) at the merge turn.
- Merge authorization. Keep #397 open for the hart decision, the future-duty inventory and the AX7101 liveness torture. #590 owns the queued-input firmware repair.

R348-2 FINISHED
