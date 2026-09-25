[R325] NEGATIVE - exact head 32076148acb0b9122e8c92a44f8e2ebbc8169280

# R325-1: external review of PR #564 (issue #559), round 1

- Head: `32076148acb0b9122e8c92a44f8e2ebbc8169280`, tree `1d25c86b6a9c2577103d27ecbfb6e1e686772518`, source base and live dev `a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4`.
- Diff: 8 files. `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` changes section 18 and UNRESOLVED 6. `tb/verilator/nvm_capture_cpu/` is new: `README.md`, `firmware.py`, `probe.py`, `run.py`, `sim_main.cpp`, `soc.py` and `measurements.json`. No product RTL, firmware, builder, config or workflow file changes.
- Reconstructed from:
  - AGENTS.md and CONTRIBUTING.md (section 3);
  - the issue #559 body;
  - the assignment and decisions in issuecomment-5828771434;
  - the executor's TAKEN and REVIEW READY comments;
  - the PR body;
  - the public evidence tree `c16e4aed:review-evidence/559-r1`;
  - the authorities cited below.
- Prior public review findings on this PR: none. The PR has no reviews and no review comments. Its only comments are the two review-start notices, which I read after my own pass. Nothing needs to be carried forward.

## Verdict summary

The harness is real. It uses the board's CPU netlist, bus, crossings and memory controller, with a faithful DDR latency model. I rebuilt it in the documented environment and it reproduces the published 8x8 figure: 18.9963 ms, against the published range of 18.99012 to 19.00433 ms.

Two problems remain with what the figure is taken to show:

- **Wrong CPU clock (F1).** The 8x8 figure is for a 100 MHz CPU clock. No cacheless 8x8 build has closed timing at that clock. The product build contract states 50 MHz. At 50 MHz, the same harness measures **24.152 ms**. That is 2.07x against the hold and about 3.4% under the 25 ms bar, not 2.63x.
- **Not the true maximum (F2).** At the published 100 MHz point, the harness's own no-traffic condition gives a longer copy: **19.790 ms**. So the published 19.00433 ms is not the maximum even on the author's premise.

Also, the new directory breaks the TESTING.md rule that every `tb/verilator/` directory needs a Makefile. No test document records that it sits outside the sweep (F3).

At both clocks, the measured worst case still meets the assigned 25 ms bar. The remedy ("50 ms is enough") may therefore survive. But the published figure, the margin and the retired clock factor must be corrected, and the thin margin at the build-contract clock must be put to the decision owner.

## Answers to the six assigned questions

1. **CPU, variant, bus, L2 and memory path; substitutions.**
   - **What is the board's own.** The top module is the product `MilanSoC` (`tb/verilator/nvm_capture_cpu/soc.py:62`), built with the shape's own `xlen`, `cpu_count`, `cpu`, `l2_bytes=0` and `scala_args` (`soc.py:131-152`).
     - The CPU is VexiiRiscv, not NaxRiscv. My builds and the author's log record the variant `baremetal`, `with_cpu_clk=True`, `with_dma=True` and `l2_bytes=0`.
     - Its netlist is `VexiiRiscvLitex_f5f08b17…`, sha256 `c208df0b…`. That is byte-identical to the author's 8x8 receipt and the same in all four of my builds (`receipts/probe-environment.txt`).
     - The #359 `memory_port_cdc0` (AXI clock-domain crossing), the PP `descmem`/`respmem`/`nvmmem` crossings and bridges, the LiteDRAM controller and crossbar, and the SPI controller all stay in place.
     - The PP memory masters enter through the CPU DMA slave, so controller traffic contends inside the real CPU memory path.
     - The LiteX components are pinned at the author's recorded revisions.
   - **What is substituted, all named in the README except the UART:**
     - The clock generator (`SimClocks`, ideal in-phase edges).
     - The DDR3 PHY and device (`SDRAMPHYModel` MT41J256M16 1:4). It keeps the board A7DDRPHY's `read_latency`/`write_latency` and phases (`soc.py:48-59`). LiteDRAM's model delays reads by `settings.read_latency`, so controller-facing latency is the board's. Leveling is off; that only affects boot.
     - The SPI flash device (`LiteSPIPHYModel`). It only matters before ARM.
     - The Ethernet MAC and PHY are removed (`with_mac=False`, `soc.py:134`). Traffic is injected at the datapath MAC AXIS face; `MilanMAC` has no bus master, so no memory contention is lost.
     - The UART PHY is a simulated console (`uart_name='sim'`, `soc.py:151`). The README does not name it (S1).
     - BIOS delays, CRC and the DDR test are disabled, all outside the timed interval.
   - **Can a substitution make the copy faster than silicon?** For the memory path, I found no mechanism. The CPU clock is the exception (F1). Deterministic clock phase and the traffic condition are a sensitivity: at 100/100 MHz the result moves by 4.2% between the two traffic conditions (F2).
2. **The timed interval and the timer conversion.**
   - Where the interval runs, in `firmware.py:73-85` against `sw/firmware/milan_baremetal/milan_baremetal.c:937-1028`:
     - It starts after prefill and poisoning, immediately before the ARM write.
     - It ends after the ATTEST read-back succeeds, at `cap.ok = 1`.
     - It includes all eight ownership reads, every `nvm_rec_after()` call, the guarded byte copy and the fence.
   - This over-covers the backend hold. The hold starts at `arm_ok_w` and ends at `attest_w` (`hdl/milan/KL_nvm_backend.sv:721-778`), both inside the interval.
   - The timer is LiteX `timer0`, a 32-bit down-counter on `sys`. `CONFIG_CLOCK_FREQUENCY` is `sys_clk_hz` (100 MHz). `run.py:48` converts with `sys_cycles / sys_hz * 1000` ms, and the unsigned subtraction handles wrap. This is correct.
   - The hold's ms tick uses `MILAN_CLK_FREQ_HZ`, the Milan/CPU clock (`milan_datapath.sv:7396`, `KL_nvm_backend.sv:603-615`). It is correct at either clock.
   - Note: the hold is loaded at ARM and counted on a free-running ms tick. The effective hold is therefore 49 to 50 ms, so half the minimum hold is about 24.5 ms. This does not change any verdict below.
3. **The clock premise.** The 8x8 CPU clock of 100 MHz comes from `configs/endstation_ax7101_8x8.yaml:56`. It is emitted as `--milan-clk-freq 100e6` in the board argv (`receipts/clock-premise-evidence.txt`). The 1x1 value of 50 MHz comes from `configs/endstation_ax7101_1x1_tdm8.yaml:44`. The harness reproduces the configured recipe faithfully, but that recipe has no evidence that it can be built. See F1. The doc does state the clock each figure holds for (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1568`, `:1707`). It does not state the 8x8 figure at the build-contract clock. I measured it: 24.152 ms. The earlier assignment estimate of about 38 ms overstates the effect, because the DDR and sys-domain share of each access does not scale with the CPU clock.
4. **Does the traffic arm contend, and is the no-traffic run a real control?**
   - Requests, responses and shared-memory read ACKs are counted per capture, between the walk start and ATTEST. The response check verifies EtherType, subtype, AEM_RESPONSE, SUCCESS and command_type (`sim_main.cpp:89-93`). The read ACKs come from the real descriptor Wishbone bus (`probe.py:22`).
   - The no-traffic mutation is a real control of counter integrity. My runs caught it at both clocks.
   - It is not a control of contention. The traffic has no measurable effect at 1x1/50 MHz (the author's public no-traffic log: 655,072 to 655,196 cycles, against 654,490 to 655,479) or at 8x8/50 MHz. At 8x8/100 MHz the no-traffic copy is 4.2% *longer*. See F2.
5. **Docs replace the model and name the retired factors.** Section 18 and UNRESOLVED 6 replace the model with measured figures. They name the retired factors (`:1604-1607`): 6 instructions per byte, 50 per record, 10 cycles per instruction, 30 per access, 2 accesses per byte and the twofold penalty. They also retire "the blanket 50 MHz CPU assumption" (`:1607`). That last retirement is wrong for the product build contract (F1).
6. **Runnability and hosted scope.**
   - The harness ran as documented, with the documented environment variables, an offline network namespace and the pinned SDK. Four builds and simulations completed. The unmodified 100 MHz control reproduced the published figure.
   - It is outside the hosted sweep: `scripts/run_all_suites.sh --list` lists 55 suites and not this one, because it has no Makefile.
   - The workflows are unchanged, and nothing in hosted CI imports or runs it. Hosted runners therefore gain no RV32-compiler or new LiteX dependency. (The existing `elaborate` job already installs pinned LiteX; it does not touch this harness.)
   - TESTING.md does not state that the harness is out of the sweep, and it contradicts itself on this directory (F3).

## Findings

### F1 - MAJOR - Conformance, RTL, Docs - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1561-1562,1568,1607,1705,1707`; `tb/verilator/nvm_capture_cpu/README.md:66`; `tb/verilator/nvm_capture_cpu/measurements.json` (8x8 row) - the 8x8 figure and margin hold only at a 100 MHz CPU clock that no cacheless 8x8 build has closed; at the build-contract 50 MHz the measured worst copy is 24.152 ms

**Authority and evidence**

- The assignment asks for the product SoC "as the board build configures them". Acceptance 2 asks for a stated margin. AGENTS.md section 2: a conflict between the configuration and the documentation is published for a decision, not resolved privately.
- `docs/integration/BAREMETAL_FIRMWARE.md:43` is the product build contract. It says: "The cacheless CPU side and the 64-bit Milan plane run at 50 MHz."
- `BAREMETAL_FIRMWARE.md:1991-2002`: the first option-on build kept both planes at 100 MHz and failed setup timing at WNS -3.762 to -3.933 ns. "That result is why the cacheless CPU and 64-bit Milan plane run at 50 MHz." That was the smaller 1x1 shape. At 50 MHz it already fills 15,849 of 15,850 slices (`:1981,1987`).
- Commit `1e80a106` moved the shipping core to 50 MHz because its "direct fetch/data TileLink paths are intentionally longer". It changed only the 1x1 config.
- The 8x8 line `milan_clk_hz: 100000000  # single fast domain (AX timing CLOSED)` has not changed since `a94296d4` (2026-07-22). Its "CLOSED" refers to the Linux-era L2 16 KiB close of 07-24 (WNS +0.080), which the config history records. That note was deleted when the 8x8 went cacheless in `dc9ed422`/`dfcf83ce` (2026-08-25/26), but the clock was never revisited.
- No 8x8 bare-metal placement record exists in `BAREMETAL_FIRMWARE.md`, `AREA_BUDGET.md` or `CLOCK_DOMAINS.md`. All of this is in `receipts/clock-premise-evidence.txt`.

**My measurements.** Same head, the harness unchanged, only the 8x8 `milan_clk_hz` set to 50 MHz (`receipts/probe-cpu50-config.diff`), same CPU netlist and instrumented firmware (`receipts/probe-environment.txt`):

- With traffic: 2,414,638 to 2,415,248 sys cycles over 4 captures. That is **24.15248 ms maximum, 2.0702x**. All captures attested, census 12,634 bytes / 156 records, zero mismatches, and positive requests, responses and reads. The harness's own grader passes it (`receipts/b8x8_50.measurement.json`).
- With no traffic: 2,414,830 to 2,415,108 cycles, 24.15108 ms.
- The unmodified 100 MHz control gives 18.99632 ms, reproducing the receipt. So the difference is the clock alone (`receipts/timing-summary.txt`).
- Section 18 instead writes "Configured clocks replace the blanket 50 MHz CPU assumption". It deletes the previous "Hold sizing must use the writer's actual clock". It publishes 2.6310x as the 8x8 margin, without saying that the 100 MHz 8x8 clock contradicts the build contract.

**Impact**

- The published 8x8 margin (2.63x, 6 ms under the bar) is for a clock no 8x8 bitstream has met.
- At the only clock the cacheless core is documented to close, the copy is 24.15 ms. That leaves 0.85 ms (3.4%) under the 25 ms bar, and about 1.4% under half the effective 49 ms minimum hold.
- That headroom is also less than the 4.2% condition sensitivity measured in F2.
- A reader of section 18 would plan 8x8 growth or copy additions against headroom that does not exist at the product clock.

**Required outcome**

- Section 18, UNRESOLVED 6 and the receipt must state the 8x8 figure at the CPU clock an 8x8 cacheless build actually runs at. Either measure it at 50 MHz, or give placed-and-routed evidence that the 8x8 cacheless build closes at 100 MHz.
- The configuration versus build-contract clock conflict must be published for a decision.
- The retirement of "the 50 MHz CPU assumption" must be corrected.
- Whether 24.15 ms counts as "enough" against the thin margin is the decision owner's call under the assigned remedy order. It must be made on that figure, not on 19.00 ms.

**Verification**

- Re-review the doc and receipt text.
- Re-run `scripts/r325_clock_probe.sh <clone> <scratch> 50 none 16`. The maximum must match the published 50 MHz figure, and the doc's clock statement must match the configuration (or the build contract) at the merge head.

### F2 - MINOR - Conformance, Robustness, Tests, Docs - `tb/verilator/nvm_capture_cpu/run.py:31-56`; `tb/verilator/nvm_capture_cpu/measurements.json`; `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1561-1562,1705` - the published "maximum" is not the maximum over the harness's own operating conditions, and the traffic arm's contention effect is not characterized

**Authority and evidence**

- The assignment asks for "the worst case over repeated captures". A capture with an idle or absent controller is a real operating condition the hold must also cover.
- At the published 8x8/100 MHz point, the harness's own `--mutation no-traffic` build gives **1,979,024 and 1,978,694 cycles (19.79024 ms, 2.5265x)**. The published maximum with traffic is 1,900,433 cycles (19.00433 ms), so the no-traffic copy is 4.1% longer. The firmware symbol layout is identical in both builds (`receipts/probe-environment.txt`); only the traffic condition differs.
- At 8x8/50 MHz and at 1x1/50 MHz (the author's public `final-mut-no-traffic-uart.log`) the two conditions agree within 0.1%.
- The grader measures and gates only the traffic arm. The no-traffic run is graded only for counter integrity, and its time is never compared with the traffic arm.
- The docs present the traffic arm as the worst case. They do not state that traffic made no difference at 50 MHz and a negative one at 100 MHz.

**Impact**

- The published figure is 4% optimistic even on the author's own clock premise.
- The phrase "under controller traffic" suggests stress margin that the evidence does not show.
- The copy time is sensitive to the operating condition by about 4% at 100/100 MHz. That is larger than the 3.4% headroom F1 leaves at 50 MHz.

**Required outcome**

- The published maximum must be the maximum over at least the conditions the harness already provides: traffic and no traffic.
- The docs must state what the traffic arm does and does not change.

**Verification**

- The receipt contains both arms at the stated clock or clocks. Section 18 quotes their maximum.
- Re-running both arms (`scripts/r325_clock_probe.sh … none|no-traffic …`) reproduces it.

### F3 - MINOR - Docs, Tests - `docs/testing/TESTING.md:164,373`; `tb/verilator/README.md`; `tb/verilator/nvm_capture_cpu/` - a Makefile-less directory under the suite root, with its out-of-sweep status recorded nowhere in the test documentation

**Authority and evidence**

- TESTING.md:164 says "`ls tb/verilator/` is authoritative (one dir per suite)". TESTING.md:373 says "Every directory needs a `Makefile`; only `milan_dp_gptp` runs separately."
- CONTRIBUTING.md section 3 points to TESTING.md for the suite index.
- `tb/verilator/nvm_capture_cpu/` is now the only directory under `tb/verilator/` without a Makefile. `scripts/run_all_suites.sh --list` silently omits it.
- TESTING.md and the `tb/verilator/README.md` suite table do not mention it. They also do not mention its LiteX, CPU-generator and RV32 SDK prerequisites, or that neither the hosted nor the local sweep runs it (`receipts/harness-sweep-and-docs-census.txt`).

**Impact**

- The suite-index authority is false at this head.
- A future reader, or a tool built on the "one directory per suite" rule, either treats the harness as a suite, or cannot find it or learn that it is manual and environment-dependent.

**Required outcome.** Either reconcile TESTING.md with the harness, or move the harness out of the suite root. For example, TESTING.md and `tb/verilator/README.md` could name it as an out-of-sweep, environment-dependent measurement harness with its prerequisites.

**Verification.** Every directory under the suite root satisfies the documented rule, or the rule names its exception. The suite table, or the SoC-level simulation section of TESTING.md, records the harness.

### S1 - SUGGESTION - Docs - `tb/verilator/nvm_capture_cpu/README.md:98-102` - name every substituted model

The README names the clock, DDR, flash and MAC substitutions. It omits the simulated UART console (`uart_name='sim'`, with no baud-rate back-pressure) and the simulator version the figures used. The receipt records the version; the README does not. Naming both would complete the substitution list the assignment asks for. This is optional.

## Per-lens results

Each entry names what was checked and found correct within the lens, and the open findings that keep the lens UNCLEAN.

- **Conformance.**
  - Checked and correct: the bracket covers ARM through ATTEST, including the walk (`firmware.py:73-85`, `milan_baremetal.c:937-1028`).
  - Checked and correct: the census of 12,634/156 and 3,218/53 (`run.py:42`, the receipt, my runs).
  - Checked and correct: the 25 ms gate (`run.py:55`), the hold clock (`milan_datapath.sv:7396`, `KL_nvm_backend.sv:603-615,721-778`), and "no firmware/RTL change" (diff stat).
  - UNCLEAN: F1, F2.
- **RTL.**
  - No product RTL changes.
  - Checked: the probe CSR and packet ports are observation and injection only (`probe.py:10-48`). The CPU netlist matches the board recipe and the author's receipt (`receipts/probe-environment.txt`). The #359 memory crossing is present (`milan_soc.py:2694-2701`, and the build hierarchy). The backend hold derives its tick from the Milan clock.
  - UNCLEAN: F1, an invalid clock assumption for the 8x8 figure.
- **Robustness.**
  - Checked and correct: the anchors must be unique and drift is refused (`firmware.py:88-96`). A failed attestation yields `sys_cycles=0` and fails the grade.
  - Checked and correct: the 30 s simulated bound and the nonmonotonic-clock refusal (`sim_main.cpp:131-138`). The rational edge schedule has no overflow within the bound, including the tdm32 clock of 98.304 MHz.
  - Checked and correct: the external build directory is enforced (`run.py:87-88`) and the 32-bit timer wrap is handled.
  - UNCLEAN: F2, where the idle-controller condition is the worse case.
- **Tests.**
  - Checked: the skip-copy oracle (the author's public log shows 3,218 of 3,218 mismatches, rc 1, caught). The no-traffic oracle was caught in my runs at both clocks. The grader checks every row, the index sequence, ok, open, census and traffic (`run.py:43-47`).
  - The input hashes in `measurements.json` match the head files (verified for all five harness files and the product firmware).
  - UNCLEAN: F2, where the worst case is not taken over the harness's own conditions, and F3.
- **Docs.**
  - Checked and correct: section 18 and UNRESOLVED 6 carry the measured figures, which match the receipt (recomputed). The retired model factors are named. The commands in section 18 and the README reproduce.
  - UNCLEAN: F1 (the clock retirement and the missing build-contract figure), F2 (the "maximum" claim) and F3 (TESTING.md).

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR, F2 MINOR) | issue #559 body and assignment 5828771434; `firmware.py`, `run.py`, `soc.py`; `milan_baremetal.c:508-530,937-1028`; `KL_nvm_backend.sv:603-615,721-778`; `measurements.json`; four probe runs | R325-1 | 32076148acb0b9122e8c92a44f8e2ebbc8169280 |
| RTL | UNCLEAN (F1 MAJOR) | `soc.py`, `probe.py`; `milan_soc.py` clock and #359 crossing path (`:2691-2701`, `:2762-2770`); 8x8 and 1x1 shape clocks; `BAREMETAL_FIRMWARE.md:43,1981-2002`; CPU netlist identity | R325-1 | 32076148acb0b9122e8c92a44f8e2ebbc8169280 |
| Robustness | UNCLEAN (F2 MINOR) | `sim_main.cpp`, `run.py`, `firmware.py` failure paths; the no-traffic condition at two clocks | R325-1 | 32076148acb0b9122e8c92a44f8e2ebbc8169280 |
| Tests | UNCLEAN (F2 MINOR, F3 MINOR) | grader and both mutation oracles; the author's public mutation logs; my no-traffic runs; suite-root census | R325-1 | 32076148acb0b9122e8c92a44f8e2ebbc8169280 |
| Docs | UNCLEAN (F1 MAJOR, F2 MINOR, F3 MINOR) | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 (`:1505-1622`) and UNRESOLVED 6 (`:1702-1717`); harness README; `docs/testing/TESTING.md`; `tb/verilator/README.md`; `BAREMETAL_FIRMWARE.md`; `CLOCK_DOMAINS.md` | R325-1 | 32076148acb0b9122e8c92a44f8e2ebbc8169280 |

## Receipts (listed in MANIFEST.sha256)

- `receipts/timing-summary.txt`: all four probe runs, with cycles, ms and margins, plus the author comparison points.
- `receipts/b8x8_{50,50_nt,100,100_nt}.capture.log`, `.spec.json` and `.vsim.rc`: raw simulator UART output, the build's clocks and mode, and the simulator exit status.
- `receipts/b8x8_{50,100}.measurement.json`: the harness grader's own output for the traffic arms.
- `receipts/probe-cpu50-config.diff`: the only change in the 50 MHz probe copy.
- `receipts/probe-environment.txt`: component revisions, simulator, compiler, CPU-netlist and firmware hashes, and firmware symbol layout.
- `receipts/clock-premise-evidence.txt`: the configuration clock lines and their history, the 50 MHz commit, the build-contract and closure-record lines, and the derived board argv for both shapes.
- `receipts/harness-sweep-and-docs-census.txt`: the Makefile census, the sweep list, the TESTING.md rule lines, and the missing documentation references.
- `scripts/r325_clock_probe.sh`: portable reproduction of the four probe runs.

## Real limits

- These are simulation results. Physical calibration was NOT RUN, and nothing here is silicon timing or memory-ordering proof.
- My probe runs used 4 captures at 50 MHz with traffic, and 2 captures for the other three arms, to fit bounded foreground steps. The per-capture spread is at most 0.03% in every arm.
- The 100 MHz traffic control reproduces the published 16-capture range.
- I did not diagnose why the 8x8/100 MHz traffic arm is faster than its no-traffic arm. F2 rests on the observed values alone.
- I did not build or place an 8x8 bitstream. F1 rests on the absence of any closure record, on the documented 1x1 failure at 100 MHz, and on the build contract.
- I did not run the skip-copy mutation myself; I relied on the author's public log for it.
- I did not run any full parent, PP, gPTP, Yosys or builder bank. The manager's source validation covers these.
- Probe trees and builds were disposable copies under the packet's `scratch/`, which is not published. The review clone was verified afterwards:
  - HEAD and tree are as above;
  - all 896 tracked non-gitlink blobs and modes are byte-equal to the index;
  - the index equals the HEAD tree;
  - the four gitlinks are unchanged, and the three initialized submodules are clean at their gitlinks;
  - no untracked or ignored files are left. I removed the bytecode caches my own read-only imports created.

## Pending manager duties

- Hosted exact-head acceptance. The check runs listed at this head show success for rtl-fast, verilator-suites (5 shards), yosys-portability (4 shards), elaborate, docs-check (both modes) and wire-accountability. Physical gPTP was skipped as nightly/manual; that is not an executed pass.
- Candidate-merge build on current dev.
- The decision F1 requires: the 8x8 CPU clock and whether 24.15 ms is "enough".
- Re-review of the corrected head.
- A merge needs two independent positive reviews and the full completion bar.

R325-1 FINISHED
