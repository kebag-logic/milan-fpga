[R348] NEGATIVE - exact head 7f997b60d5a74d46beca5c263d27496ccce0ae4f

Round R348-1, internal independent review of PR #588 for issue #397 (service-budget measurement, measurement-only re-scope in issuecomment-5854787465). Exact head `7f997b60d5a74d46beca5c263d27496ccce0ae4f`, tree `e2f28554de998383ec0b6116453120633e322f45`, one commit on source base `ac18b50968b12efe4d15c0a06301264b35656b31`. Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body and the manager's assignment and re-scope comments, SAVED_STATE_FASTCONNECT.md section 9.4, BAREMETAL_FIRMWARE.md, KL_nvm_backend.sv, the product firmware, the diff, and the public evidence tree at `7a649d0c`. No prior public review findings existed on PR #588 or issue #397 when this round started (the PR carried only the review-start comment), so none are carried forward.

Summary: the measurement is sound and reproducible. Both committed scenarios reproduce bit-exact from a clean rebuild at this head: the same raw-log SHA-256, identical rows and the same three 8x8 budget findings. Independent observers inside the fabric and on the UART and SPI boundaries agree with every harness marker I probed. The firmware and the capture harness are untouched. The docs gates pass.

Four findings keep the verdict negative:

- **F1 (MAJOR).** The heartbeat result is misread. The heartbeat gap is never compared with the 2,000 ms liveness expiry. The gap is driven by the zero-idle console schedule, not by device waits, and a three-command probe shows that schedule lapsing `nvm_backed`.
- **F2 (MINOR).** Most grader mutations, including a wrong marker and a wrong clock ratio, pass the self-test.
- **F3 (MINOR).** The AEM copy/CRC "no narrower marker" claim is wrong. SPI flash reads at the AEM offset bracket it about 6-8x tighter.
- **F4 (MINOR).** A device control cannot fail for the defect it names.

## Findings

**F1 - MAJOR - Conformance, Robustness, Docs - `docs/findings/397_SERVICE_BUDGET.md:78`, `:89-91`, `:137-140`, `:148-150`; `tb/verilator/fw_service_budget/README.md:87-93`; `tb/verilator/fw_service_budget/sim_main.cpp:116-122`; `run.py:204-209` - The heartbeat result is compared with the wrong deadline only, and what drives it is not stated.**

Authority and evidence:

- **The deadlines.** SAVED_STATE_FASTCONNECT.md:1247 (section 9.4) sets `T-NVM-WRITER-ALIVE` = 2,000 ms, with a heartbeat period of at most 500 ms. `KL_nvm_backend.sv:141,449,632` re-arms liveness only on a heartbeat write (`wdata[0]`) and drops `nvm_backed` when the 2,000 ms counter expires. Issue acceptance 4 requires `nvm_backed` to stay set across every console command. The manager's focus for this round asks whether the gap exceeds 2,000 ms.
- **What the findings page says.** It compares the gap only with 500 ms. The 2,000 ms expiry and the liveness margin appear nowhere in it.
- **Where the firmware heartbeats.** `milan_baremetal.c` heartbeats only from:
  - the console idle hook (`:1115-1120`, installed at `:1361`);
  - the flash WIP poll loop (`:838-849`);
  - after each page (`:884`);
  - the restore and device-idle waits.

  The pinned BIOS `readline.c:63-66` runs the idle hook only while no UART byte is pending.
- **What the harness does to that.** `sim_main.cpp:116-122` starts sending the next command on the same cycle as the prompt. The idle hook therefore never runs after boot. The 8x8 receipt has four heartbeat writes in 5.03 s:
  - one at restore;
  - one inside each commit's erase wait;
  - one inside the wipe's first erase wait.
- **What the published gap is.** The 1,449.77764 ms maximum is the sum of consecutive heartbeat-free spans: the end of commit 4's read-back, the whole of status command 5 (788.877 ms) and the start of the wipe. It is not a single duty's latency.
- **Independent probes, graded by reviewer scripts:**
  - **PD** (8x8; three back-to-back `milan_nvm` status commands; no flash WIP). The fabric's `backed_r` falls at 2,893.00 ms, 1,999.04 ms after the only heartbeat kick. The firmware's own third status print reads `backed=0 dirty=0 stale=1`. So ordinary console commands, streamed without idle time, lapse liveness and latch `stale`. No device wait is involved.
  - **PC** (8x8; one commit; 3 s erase and 5 ms page WIP, the section 9.4 device maxima). Heartbeats continue every 250.0007 ms inside the erase (12 of them). Device-maximum WIP therefore does not push the gap toward 2,000 ms. The largest gaps are 588.61 ms and 532.52 ms. The first comes from the pre-START capture, prefill and seal phase, 449.56 ms after the command starts. The second comes from the heartbeat-free read-back after the last page, 475.24 ms from the last page to ACK. Both exceed the 500 ms period even for a single commit.
  - **PB** (the committed 8x8 plan, observed inside the fabric). The liveness counter had 550 ms left at the kick that ended the 1,449.78 ms gap, so no lapse occurred in the published scenario.
- **What the page says instead.** It gives none of this, only "The heartbeat observations end at the final command" and "A short run with no reported lapse cannot prove the issue's release-gates torture."

Impact: this table is the manager's input to the one-hart, two-hart or offload decision. As published it presents a -949.78 ms margin as a service-latency overrun and says nothing about liveness. A reader cannot tell three things:

- The gap is unbounded under back-to-back console input, and three 8x8 status commands already lapse `nvm_backed`.
- With a paced console, the bound is roughly the 250 ms tick period plus the longest heartbeat-free span. At 8x8 that span is the status command, 788.9 ms, so the bound is about 1,039 ms: over 500 ms, under 2,000 ms.
- Device waits are not the cause. The heartbeat-free CPU spans (slot validation by byte-wise memory-mapped flash reads, capture and seal, read-back) and the idle-hook-only heartbeat are.

Those three facts point to different remedies: a firmware heartbeat inside long loops, offload, or a second hart.

Required outcome:
- For each duty, the findings record its longest heartbeat-free span, from the harness's own markers.
- They say that the published maximum gap depends on the schedule: under zero-idle input the idle hook never runs, and the gap is a sum across commands.
- They compare the heartbeat against both the 500 ms period and the 2,000 ms `T-NVM-WRITER-ALIVE` expiry, with margins.
- They state what happens at device-maximum WIP: heartbeats continue inside the WIP loops, and the heartbeat-free read-back remains.
- They record the demonstrated lapse under back-to-back commands, or an equivalent harness run, as a measured finding for the manager's decision.

Verification: re-read the updated findings against receipts `receipts/probe-PD-8x8-status3.txt`, `receipts/probe-PC-8x8-devicemax.txt` and `receipts/probe-PB-8x8.txt`. Any new run must reproduce the lapse, or give a reason it does not.

**F2 - MINOR - Tests - `tb/verilator/fw_service_budget/run.py:216-262` (`trace_controls`, `self_test`) - The self-test does not pin marker selection or unit conversion.**

Authority and evidence: the AGENTS.md Tests lens requires that "each new test can fail for the defect it claims to detect". The manager's focus item 4 asks for mutations such as a wrong marker or a wrong clock ratio. `scripts/mutate_grader.py` applied 15 single-line grader mutations to a disposable export of this head (`receipts/mutation-grader.txt`).

The self-test caught 4: both budget-scale mutations, the status-budget mutation and a restore-walk marker mutation. It passed 11. Among the 11:

- heartbeat marker = the commit START strobe;
- entity-enable marker on bit 1;
- boot start at cycle 0;
- CPU cycles at 1:1;
- milliseconds at 50 MHz;
- command-end index shifted by one;
- commit budget 500 ms;
- WIP not subtracted;
- erase envelope ending at ACK;
- final heartbeat tail dropped.

Each of those 11 would change published rows. Re-deriving the committed receipts' raw logs with the mutated grader and comparing rows exposes every row-changing mutation. The self-test already loads the 1x1 receipt, but checks only that its budget findings are empty and that the delayed-status refusal fires.

Impact: the measurement is not part of the continuous-integration sweep. A future edit that swaps a marker or a conversion would leave the self-test green and republish wrong figures.

Required outcome: the portable self-test fails when a marker is selected wrongly or a cycle or ms conversion is wrong. One way is to regrade both committed receipts' raw logs and require row equality; named controls would also do.

Verification: rerun `scripts/mutate_grader.py <export> <out.json>`. Every row-changing mutation must make `--self-test` return nonzero.

**F3 - MINOR - Conformance, Docs - `docs/findings/397_SERVICE_BUDGET.md:35-37`, `:54`, `:74`; `tb/verilator/fw_service_budget/README.md:70-71`; `run.py:170-171` - AEM copy/CRC is bounded by the whole boot although a narrower external marker exists.**

Authority and evidence: the re-scope says to time duties from externally visible markers, including SPI flash command sequences, and to use an enclosing interval only "where a duty has no external marker". `milan_baremetal.c:1404-1422` copies the AEM image byte by byte from the memory-mapped flash at `MILAN_AEM_FLASH_OFFSET`, then computes its CRC and enables the entity. Those flash reads cross the harness's own device boundary (`sim_main.cpp:53-71`).

Reviewer probes logged every flash command with its address:
- **1x1.** 5,519 AEM-offset reads start at 255.21 ms. First AEM read to the enable write is 55.76 ms, against the published 310.97 ms.
- **8x8.** 13,721 reads start at 896.68 ms. First read to enable is 134.76 ms, against 1,031.44 ms.

The pages say AEM copy/CRC "has no separate marker" and has "no narrower marker". That is not correct.

Impact: the AEM duty is overstated about 5.6x at 1x1 and 7.7x at 8x8, and the text misstates what the harness can observe. The impact on the hart decision is small, because boot has no liveness armed and no numeric deadline.

Required outcome: bracket AEM copy/CRC with the first AEM-offset flash read and the enable write, and correct the claim. If that marker is judged unsuitable, state why.

Verification: `receipts/probe-PA-1x1.txt` and `receipts/probe-PB-8x8.txt` (`aem_copy_crc`) against the updated table.

**F4 - MINOR - Tests - `tb/verilator/fw_service_budget/flash_test.cpp:67-73`; `flash.hpp:72-73` - The "program while busy refused" control cannot fail for the busy check.**

Evidence: the control issues WREN while the device is busy. At `flash.hpp:70`, WREN sets WEL only when not busy, so the following program is refused for missing WEL. Deleting `cycle < busy_until_` from `flash.hpp:72` leaves all 14 device checks passing (`receipts/mutation-flash-busy.txt`).

Impact: the model's refusal to program or erase during WIP, which is part of the device-boundary contract, has no control.

Required outcome: a control that fails when the busy refusal is removed, for example with WEL set before the busy window.

Verification: repeat the mutation in `receipts/mutation-flash-busy.txt`; the control must fail.

**S1 - SUGGESTION - Conformance, Docs - `docs/findings/397_SERVICE_BUDGET.md:103-105`.** The issue body names Milan 5.6.3 as "the ADP valid time the boot must beat", and the first assignment listed it. The PR reasons publicly that 5.6.3 fixes no power-on-to-enable deadline, and reports N/A. Record this as an explicit open decision for the manager on #397, or give a conditional margin that names the excluded BIOS terms, so the deviation from the issue's wording is not left implicit.

**S2 - SUGGESTION - Docs - `tb/verilator/fw_service_budget/README.md:17-18`.** "Keep builds outside the checkout" is not sufficient. The product build run by `build.py` wrote ignored artifacts into the checkout: `configs/generated/ltn_rom.hex`, `configs/generated/ucode.hex` and bytecode caches in `avdecc/`, `sw/litex/platforms/` and the protocol-processor submodule. This is inherited from the product builder, not introduced by this PR; a one-line note would help the next reproducer.

## Verification of the manager's focus items

**1. Protected paths unchanged; capture gate** (`receipts/protected-paths.txt`, `receipts/gates-selftest-capture.txt`):
- `git diff ac18b509..7f997b60` touches only the 12 listed files.
- The blob ids of `milan_baremetal.c` and of every `tb/verilator/nvm_capture_cpu` file are identical at base and head. The firmware SHA-256 is `0bf43cd4...47a6`.
- All four gitlinks are unchanged.
- `scripts/check_nvm_capture.py` passes, and all four of its `--mutation` controls exit 1.

**2. Markers bracket their duties** (`receipts/probe-PA-1x1.txt`, `receipts/probe-PB-8x8.txt`). I recompiled the same gateware with a probe driver (`scripts/probe_sim_main.cpp`) and read-only public access to three `KL_nvm_backend` registers. The driver records UART bytes, every flash command with its address, unmasked CSR write addresses and the fabric's liveness state in a side file. Its stdout is bit-identical to the committed logs at both shapes, so the probe does not perturb the design.

- **Boot to entity-enabled.** The enable write (1x1: 310.97087 ms; 8x8: 1,031.44025 ms) lies between the end of the "AEM ... CRC" UART line and the first byte of "fabric entity enabled". The CSR address is `0x90000920`. The boot start at cycle 64 matches reset release: `sim_main.cpp:190` deasserts reset after 128 half-periods, which is 64 rising edges.
- **NVM status.** At 8x8 each status command makes 52,264 journal flash reads spanning 781.77 of its 788.86 ms (1x1: 13,570 reads over 201.51 of 208.49 ms). The interval is the firmware's slot validation (`milan_baremetal.c:1516-1522`), not a harness artifact.
- **Heartbeat gap.** Fabric liveness kicks equal the CSR heartbeat writes (1x1: 3/3; 8x8: 4/4). The fabric-side maximum gap is 1,449.77764 ms and the counter's remaining value at that kick is 550 ms.

Clocks: 50 MHz CPU and 100 MHz system clock with aligned rising edges (`sim_main.cpp:166-173`). The build spec records `cpu_hz` 50,000,000 and, for 8x8, `configured_cpu_hz` 100,000,000. CPU cycles are ceil(sys/2) and ms are sys/100,000. `receipts/table-recompute.txt` recomputes all 38 published table cells from the receipts' integer cycles with no mismatch. The PHC runs at real time in this simulation: `milan_status` prints a TAI of 319.10 ms at a measured 312.49-320.20 ms.

**3. Deadlines and the service/WIP split.**
- The compared limits are correct: 3,000 ms restore, 3,500 ms erase, 8,000 ms commit and the 500 ms heartbeat period.
- The 2,000 ms liveness expiry is missing (F1).
- The service/WIP split for commits is honest. At device-maximum WIP (probe PC), the measured START-to-ACK of 3,856.73 ms and the whole-commit time of 4,307.68 ms lie within 0.5 ms of the published conditional projections (3,857.20 and 4,308.16 ms).
- For the heartbeat: device WIP does not drive the gap toward 2,000 ms, because heartbeats run inside the WIP loops. Back-to-back console input does drive it there: probe PD lapsed `nvm_backed` with three 8x8 status commands.
- What the harness cannot show: a paced console (it always streams input); physical flash timing; bus contention from packet traffic.

**4. Self-test.** It plants an over-budget duty and catches it. The exact-budget interval passes, one extra system cycle is refused, and the delayed-status trace is refused by name. Mutation resistance is weak (F2, F4).

**5. Reproducibility.** I rebuilt both shapes at this head. Toolchain: the pinned LiteX revisions, the cached CPU netlist `c208df0b...` and the RV32 SDK. The 1x1 and 8x8 populated runs reproduce the committed raw logs bit-exact:
- 1x1 log SHA-256 `e1a48895...2e61`, zero findings.
- 8x8 log SHA-256 `c38caa7b...6115`, with findings NVM status 788.87705 ms ×2 and heartbeat gap 1,449.77764 ms.

Rows are identical, and the bound-log `--regrade` passes. The default mode refuses the 8x8 findings (rc 1), and a tampered log is refused with "recorded log changed" (`receipts/reproduce-*.txt`, `receipts/regrade.txt`). The generated BIOS image hash is identical to the receipt's. Six build hashes differ only in generated headers, `sim.v` and the native binary.

**6. Docs gates and receipt size.** All of these pass: `docs_check`, `check_doc_paths`, `check_doc_style`, `check_archive`, `gen_toc --check`, `check_em_dash --base ac18b509`, `git diff --check`, `check_feature_status --self-test` (46/46), `check_py_idiom`, `check_cpp_idiom`, `check_hygiene --check` and `measure_test_evidence --check` (`receipts/gates-docs.txt`).

The receipts are 49.6 KB and 63.3 KB. Each embeds its raw log (10-15 KB) bound by SHA-256, contains no local paths, and its `input_hashes` all match this head.

## Lens ledger (reviewer-owned)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F3) | #397 body and comments 5854692469, 5854787465; SAVED_STATE_FASTCONNECT.md:1247 (section 9.4); `docs/findings/397_SERVICE_BUDGET.md`; `run.py:145-213`; `milan_baremetal.c:757-1180,1395-1456,1516-1522`; probes PA/PB/PC/PD | R348-1 | 7f997b60d5a74d46beca5c263d27496ccce0ae4f |
| RTL | CLEAN | `sim_main.cpp:144-193` (clock ratio, aligned edges, reset release at 64 rising edges); `build.py:29-71` (device boundary keeps the LiteSPI controller; observation on the system-side `milan_csr` bus after CDC; backend handshake pads); `flash.hpp` SPI timing (8 cycles/bit + 1); `KL_nvm_backend.sv:141,449,603-660` heartbeat and liveness semantics against the harness's `value == 1` marker; build spec clocks; fabric-side cross-check (PA/PB) | R348-1 | 7f997b60d5a74d46beca5c263d27496ccce0ae4f |
| Robustness | UNCLEAN (F1) | back-to-back console input and the idle-hook starvation path (probe PD); device-maximum WIP (probe PC); refused-argument and numeric-limit commands in the committed plan; tampered-log and stale-build refusal (`receipts/regrade.txt`); default-mode refusal of budget findings | R348-1 | 7f997b60d5a74d46beca5c263d27496ccce0ae4f |
| Tests | UNCLEAN (F2, F4) | `run.py:216-262`; `flash_test.cpp`; 15 grader mutations plus 1 device mutation; `make -C tb/verilator/fw_service_budget`; bit-exact rebuild and rerun of both shapes; `check_nvm_capture.py` and its mutations | R348-1 | 7f997b60d5a74d46beca5c263d27496ccce0ae4f |
| Docs | UNCLEAN (F1, F3) | `docs/findings/397_SERVICE_BUDGET.md`; `tb/verilator/fw_service_budget/README.md`; `docs/findings/README.md:11`; `docs/testing/TESTING.md:403-406`; all docs and style gates; 38-cell table recompute; receipt contents and size | R348-1 | 7f997b60d5a74d46beca5c263d27496ccce0ae4f |

## Limits

- **Simulator.** The Verilator path given for this round (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. I used the system Verilator 5.052 instead, which is the simulator both committed receipts record.
- **Probe coverage.** The probe runs PC and PD use command plans the harness grader does not accept. The reviewer scripts `scripts/analyze_probe.py` and inline analysis grade them.
- **Paced-console bound.** The bound of about 1,039 ms at 8x8 is reviewer analysis from the firmware's tick structure. It is not a simulated paced run, because the harness cannot pace input.
- **Not established.** One deterministic clock phase; the device modelled at its stream boundary; no packet traffic; BIOS CRC, delay and memory-test excluded. No hardware, physical calibration or bench liveness proof. Field skips are not hardware proof.
- **Not run.** Full parent, protocol-processor, gPTP, Yosys and builder banks; hosted or local CI replicas.
- **Clone restore.** The product build wrote ignored artifacts into this clone. I removed them. The clone is now at exact head bytes: the index equals the tree (937 entries), there are no untracked or ignored files, and the gitlinks are unchanged (`receipts/clone-integrity.txt`). No other checkout or shared install was modified; the CPU-netlist cache listing is unchanged.
- **Other reviews.** I read no other reviewer's report.

## Pending manager duties

- Publish this report.
- Own hosted and local-replica acceptance at the exact head, distinguishing executed jobs from skipped contexts.
- Run the separate source bank.
- Obtain the external review.
- Build and validate the final candidate on the live `dev` tip (`63fe4fb0`; source base `ac18b509`) at the merge turn.
- After the lane addresses F1-F4, re-review the corrected head.
- Make the hart decision and schedule the AX7101 liveness torture. Both remain open.

R348-1 FINISHED
