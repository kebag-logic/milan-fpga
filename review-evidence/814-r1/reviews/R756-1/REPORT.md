[R756] NEGATIVE - exact head 8b28ebaf035e786ccf5b8e50098dbc111f51831f

# R756-1: external independent review of PR #826 (#814)

- PR: kebag-logic/milan-fpga #826, `814-soc-timing-cut` -> `dev`.
- Exact head: `8b28ebaf035e786ccf5b8e50098dbc111f51831f`, tree `1a9c6972e1e2c19edd9138e1d481a1bbcbe4fd4a`.
- Base: `1e80128f0a467b58bf884b7d9bf62e013a2fb141` (live dev at review time). The base is an ancestor of the head, and the head is five one-line commits with no trailers.
- Delta reviewed: `git diff 1e80128f..8b28ebaf`, six files. `sw/litex/milan_soc.py` gains `AXIReadyStage`, `RegisteredRefresher`, `add_staged_sdram`, `SPIPHYStage`, `stage_spi_phy` and `MilanSoC.add_spi_flash`. Also new: `sw/litex/test_soc_timing_cuts.py`, its `scripts/run_litex_sims.sh` inventory entry and `ci/image/exec-audit.json` stand-in, and edits to `docs/testing/TESTING.md` and `docs/litex/CLOCK_DOMAINS.md`.
- Authorities read: AGENTS.md, CONTRIBUTING.md (by reference), the #814 issue body, and the rulings issuecomment-6514717735 (assignment, gates and STOP list), issuecomment-6527475726 (back in the release) and issuecomment-6525285974 (record rule). Also read: the pinned LiteX, LiteSPI and LiteDRAM sources the stages build on, and the executor's evidence packet at `28195920:review-evidence/814-r1/author`.
- Stack used: `sw/litex/litex_pins.txt` revisions, migen `4c2ae8df`, litex `a1e1c365`, litedram `f9b75e03` and litespi `02d5a209` (`receipts/litex_stack_identity.txt`). LiteX carries the project patch series, as `sw/litex/patches/apply.sh` applies it.

## Verdict

NEGATIVE. Two MINOR findings are open. All three cuts are functionally transparent for every flash command, AXI beat and refresh. Under random backpressure, both stream stages keep every beat in order and the AXI handshake rules hold. I found no protocol breach. Two problems remain:

1. **F-1.** The registered refresher changes whether LiteDRAM's ZQCS is issued at all, not only when. Its docstring, the test's reason for not grading ZQCS, and the PR text all say otherwise. No check covers it.
2. **F-2.** The behaviour arms never stall either stage's output, so the registered-ready hold path is never exercised. Planted lossy stages on AXI aw/ar, SPI tx and SPI rx each pass every arm of their path. The real SPI PHY stalls on every new burst.

## Findings

### F-1 MINOR - Conformance, RTL, Tests, Docs - `sw/litex/milan_soc.py:2430-2450`, `sw/litex/milan_soc.py:2440`, `sw/litex/test_soc_timing_cuts.py:583-597` - the registered refresher changes whether LiteDRAM issues ZQCS

**Authority and evidence.**

- The contract:
  - #814 is a logic cut with no behaviour change beyond latency. The STOP list in issuecomment-6514717735 includes "a cut changes bus behaviour that a suite sees, beyond latency".
  - The `RegisteredRefresher` docstring (`milan_soc.py:2439-2440`) says "each refresh and ZQCS starts and ends one cycle later, with its own tRP, tRFC and tZQCS spacing".
  - The PR body says the ZQCS coincidence "is upstream behaviour, unchanged here".
- How LiteDRAM decides a ZQCS (pinned `litedram/core/refresher.py`, `Refresher`):
  - `DO-REFRESH` starts a ZQCS only if `zqcs_timer.done` is high in the same cycle as `sequencer.done`.
  - `zqcs_timer` is a free-running `RefreshTimer`. Its `done` is a one-cycle pulse every `clk_freq/zqcs_freq` cycles. It re-phases only when a ZQCS completes.
- How the stage changes it:
  - Registering `cmd.valid` delays the controller's grant by one cycle, so every `sequencer.done` moves one cycle later. The ZQCS pulse does not move.
  - At 100 MHz on MT41J256M16 1:4 (the AX7101 shipping clock and part), tREFI = 782 and the ZQCS period = 100,000,000 cycles. gcd(782, 10^8) = 2, so an idle controller can only coincide on one cycle parity.
  - Measured with the test's own `DramSoC` (`scripts/probe_zqcs_phase.py`, `receipts/probe_zqcs_phase.log`):
    - LiteDRAM's refresher: sequencer done at 841 + 782k. The first idle ZQCS comes at sys cycle 7,599,999,999 (76.0 s after reset).
    - Staged: sequencer done at 842 + 782k. That parity never matches, so idle ZQCS never happens.
  - Direct confirmation on the DFI (`scripts/probe_zqcs_dfi.py`, `receipts/probe_zqcs_dfi.log`). The ZQCS period is shortened to 842 cycles, which keeps the same gcd of 2 with tREFI. Over 6,000 idle cycles:
    - LiteDRAM's refresher: 7 REFRESH and 1 ZQCS (cycle 846).
    - Staged: 7 REFRESH and 0 ZQCS.
- Why the test misses it:
  - Z3 grades only PRECHARGE and REFRESH.
  - Its docstring (`test_soc_timing_cuts.py:586-589`) excuses ZQCS because "the ZQCS executer's commands leave the same registered fields, behind the same two registers". That reason is true of the command fields. It does not cover the issue decision, which is what the stage changes.

**Impact.**

- On the shipping image, the DRAM command stream changes beyond a one-cycle delay. Whether a ZQCS fires shifts by one cycle parity against a timer the stage does not delay.
- With an idle DRAM, the change goes from a first ZQCS at 76 s to none ever. Under traffic, both designs fire ZQCS only by chance.
- I show no JEDEC breach. DDR3 sets no maximum ZQCS interval, tREFI spacing is unchanged at 782 cycles, and the tZQCS spacing inside a ZQCS is LiteDRAM's own.
- Still, the stated "one cycle later" contract is false for ZQCS. The change is unchecked, and the reason given for not checking it is incorrect.

**Required outcome.** One of these:

- (a) Keep LiteDRAM's ZQCS decision cycle-identical to the unstaged refresher, apart from the one-cycle shift. For example, the ZQCS timer's phase moves with the request.
- (b) A recorded maintainer decision accepts the changed ZQCS behaviour. The docstring at `milan_soc.py:2439-2440`, the test docstring at `:586-589` and the PR text then say what actually changes.

Either way, a check grades ZQCS behaviour, so the chosen contract can fail.

**Verification.** A test arm with a shortened ZQCS period of the shipping parity class, as in `scripts/probe_zqcs_dfi.py`:

- Under (a), it requires the staged ZQCS commands to equal the unstaged ones shifted by one cycle.
- Under (b), it requires the documented behaviour.
- A planted variant must fail it.

### F-2 MINOR - Tests, Robustness - `sw/litex/test_soc_timing_cuts.py:288-357` (flash behaviour), `:437-518` (DRAM behaviour) - the stall path of both registered-ready stages is never exercised

**Authority and evidence.**

- The rules: AGENTS.md section 6, Tests ("each new test can fail for the defect it claims to detect") and Robustness ("backpressure and timeout paths").
- What the test claims:
  - D4: "the stage changes nothing the native port sees, cycle for cycle".
  - F3 to F5: the flash image and its command order are preserved through the stage.
- What the stages do: their only non-trivial behaviour is the registered READY, the LiteX `PipeReady` skid that holds a beat while the downstream stalls.
- What the arms actually exercise:
  - The DRAM traffic is one outstanding single-beat burst at a time, which LiteDRAM never stalls.
  - The flash arms use `LiteSPIPHYModel`, which never stalls.
  - The real `LiteSPISDRPHYCore` holds `sink.ready` low until `cs_control.enable`, which is `cs_delay` = 10 cycles after chip select. So the shipping PHY stalls the stage on the first command of every new burst.
- Mutation result (`scripts/mutate_timing_cuts.py`, `receipts/mut_*.log`): a planted stage registers READY from the previous stall and passes the payload combinationally. It drops the beat offered into a fresh stall. It **survives** every arm of its path:
  - `axi_lossy_ready`: D0 to D4 all ok.
  - `spi_tx_lossy_ready`: F0 to F5 all ok.
  - `spi_rx_lossy_ready`: F0 to F5 all ok.
- Mutants the test does kill:
  - `axi_ar_unstaged` (D0, D1).
  - `axi_pipevalid` (D0, D4).
  - `spi_cs_comb` (F0, F1).
  - `spi_tx_no_pipe_ready` (F0, F1).
  - `ref_last_comb` (Z0, Z1).
  - `ref_ready_registered` (Z3).
  - `ref_no_last` (Z3).
- The shipping stages themselves are correct under stall. `scripts/probe_stage_transparency.py` (`receipts/probe_stage_transparency.log`) checks 3 seeds × 300 beats per channel under random VALID and READY:
  - every beat out equals every beat in, in order;
  - output VALID and payload are held until the handshake;
  - the PHY-side chip select is the core's exactly one cycle later;
  - the same probe goes red on the planted lossy stage, losing 53 and 49 beats.

**Impact.** This is not a product defect at this head. It is a gate that cannot detect loss or duplication in the very path the stage adds. A later change to these stages that loses a beat under backpressure passes `test_soc_timing_cuts.py`. On hardware, that path runs on every new flash burst and under LiteDRAM contention.

**Required outcome.** The behaviour arms drive backpressure at each stage's output (the LiteDRAM-side `aw`/`ar` READY and the PHY-side `sink` READY / core-side `source` READY), and a planted lossy registered-ready stage fails them.

**Verification.** Re-run `scripts/mutate_timing_cuts.py <repo>/sw/litex {axi_lossy_ready,spi_tx_lossy_ready,spi_rx_lossy_ready}` against the revised test. Each must report `KILLED`, while the shipping stages still pass.

No RESIDUE. The delta's source comments, docs and commit subjects carry no lane labels, lane names, review rounds, reviewer IDs or issue-comment IDs.

## Per-lens results

| Lens | Result | Artifact | What was checked |
|---|---|---|---|
| Conformance | UNCLEAN (F-1) | `sw/litex/milan_soc.py:2430-2462`, pinned `litedram/core/refresher.py`, `receipts/probe_zqcs_phase.log`, `receipts/probe_zqcs_dfi.log` | ZQCS issue decision changed beyond latency. Checked clean: tREFI spacing 782 cycles in both (free-running timer, so no drift); each refresh +1 cycle; tRP/tRFC/tZQCS spacing from LiteDRAM's executers; the acceptance items against the rulings (paths >1 ns from the worst at all three directives per the executor's route table; capture 13.85922 ms against 24.5 ms; record not re-recorded under issuecomment-6525285974, which is not a finding) |
| RTL | UNCLEAN (F-1) | `sw/litex/milan_soc.py:2391,2397-2427,2465-2507,3670-3690`; pinned LiteX `stream.PipeReady` / `stream.Buffer`, LiteSPI `LiteSPI.__init__`, `phy/generic.py`, `generic_sdr.py`, `cscontrol.py`; `receipts/probe_stage_transparency.log` | F-1 as above. Checked clean: `AXIReadyStage` is a skid on aw/ar only, w/b/r pass through, and source VALID is `sink.valid \| held` with no READY dependence and no combinational loop; it adds no cycle (D4 and probe); w may lead aw as AXI4 allows, and LiteDRAM's converter takes them independently. `SPIPHYStage`: tx and rx `Buffer(pipe_valid, pipe_ready)`, cs one flip-flop, so command and chip select reach the PHY together. LiteSPI reads only `sink`/`source`/`cs`/`flash`/`dummy_bits`, so the restaging is complete. The real PHY's cs_delay acts on the delayed cs uniformly. `MilanSoC.add_spi_flash` rebuilds the PHY with LiteX's own divisor, pads and kwargs; the only ordering difference is `master_with_irq`, which `LiteSPICSControl(**kwargs)` swallows, so it is inert. The stage is installed whenever the CPU has `cpu_clk`, as the shipping AX7101 build does (`milan_soc.py:3132-3139`) |
| Robustness | UNCLEAN (F-2) | `receipts/mut_axi_lossy_ready.log`, `receipts/mut_spi_tx_lossy_ready.log`, `receipts/mut_spi_rx_lossy_ready.log`, `receipts/probe_stage_transparency.log` | Stall path unexercised by the gate. Checked clean on the shipping stages: random backpressure on all five channels and three seeds; back-to-back transfers at full rate; flash reads across the 256-cycle burst timeout (F3); chip-select edges identical with and without the stage (F5) |
| Tests | UNCLEAN (F-1, F-2) | `sw/litex/test_soc_timing_cuts.py` at head: `receipts/head_test_soc_timing_cuts.log` (15/15 ok, `RESULT: PASS`, rc 0, 6 m 42 s), `receipts/mut_*.log`, `receipts/run_litex_sims_selftest.log` (10/10), `receipts/test_cpu_memory_port_cdc.log` (PASS) | F-1 and F-2. Checked clean: structural arms read the elaborated migen netlist; the planted-wire controls go red, naming the bridge state into `litespiclkgen_cnt`, `axiburst2beat_beat_count` into the FIFO `memory_adr`, and `refreshtimer_count` into `syncfifo_level`; 7 of 10 independent mutants killed; inventory entry and stand-in present, and the aggregate self-test is green |
| Docs | UNCLEAN (F-1) | `sw/litex/milan_soc.py:2439-2440`, `sw/litex/test_soc_timing_cuts.py:586-589`, PR body "unchanged here"; `docs/testing/TESTING.md:722-741`, `docs/litex/CLOCK_DOMAINS.md:276-281` | The ZQCS claims are incorrect (F-1). Not RESIDUE, because they are the stated reason a behaviour check is absent. Checked clean: TESTING.md's arm description matches the code; CLOCK_DOMAINS.md matches `AXIReadyStage`; comment rule clean in the delta |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F-1 open) | `milan_soc.py:2430-2462`; refresher/multiplexer/steerer sources; ZQCS phase and DFI probes; issue body and three rulings; executor's #818 gate receipts (`gate818/check-set.log`: ExtraPostPlacementOpt selected +0.128 ns, Slow corners WNS +0.128 / WHS +0.059, Fast WNS +1.311 / WHS +0.030, fall printed `WARNING`, `RESULT: PASS`) | R756-1 | 8b28ebaf035e786ccf5b8e50098dbc111f51831f |
| RTL | UNCLEAN (F-1 open) | `milan_soc.py:2391-2507,3670-3690`; LiteX stream, LiteSPI core/PHY/CS control sources; stage transparency probe | R756-1 | 8b28ebaf035e786ccf5b8e50098dbc111f51831f |
| Robustness | UNCLEAN (F-2 open) | random-backpressure probe; lossy-stage mutants; F3/F5 burst-timeout and cs-edge arms | R756-1 | 8b28ebaf035e786ccf5b8e50098dbc111f51831f |
| Tests | UNCLEAN (F-1, F-2 open) | `test_soc_timing_cuts.py` run at head; 10 mutants; aggregate self-test; `test_cpu_memory_port_cdc.py`; executor receipts (sweep shards 14/17/17/16 = 64/64 rc 0 at head; rtl-fast replay `success; failed jobs: none`; builder bank `ALL GATES PASS EXCEPT 2 NOT RUN`) | R756-1 | 8b28ebaf035e786ccf5b8e50098dbc111f51831f |
| Docs | UNCLEAN (F-1 open) | `milan_soc.py` docstrings in the delta; `test_soc_timing_cuts.py` docstrings; TESTING.md; CLOCK_DOMAINS.md; PR body; commit subjects | R756-1 | 8b28ebaf035e786ccf5b8e50098dbc111f51831f |

## Executed here (all at the exact head, pinned stack)

| What | Result | Receipt |
|---|---|---|
| `cd sw/litex && python3 test_soc_timing_cuts.py` | 15/15 ok, `RESULT: PASS`, rc 0 | `receipts/head_test_soc_timing_cuts.log`, `.rc` |
| `scripts/run_litex_sims.sh --selftest` | 10/10 PASS, rc 0 | `receipts/run_litex_sims_selftest.log`, `.rc` |
| `cd sw/litex && python3 test_cpu_memory_port_cdc.py` | `RESULT: PASS`, rc 0 | `receipts/test_cpu_memory_port_cdc.log`, `.rc` |
| `scripts/probe_stage_transparency.py` | shipping stages PASS (3 seeds); planted lossy stage FAILs as required | `receipts/probe_stage_transparency.log`, `.rc` |
| `scripts/probe_zqcs_phase.py` | staged: idle ZQCS impossible; unstaged: first at 76.0 s | `receipts/probe_zqcs_phase.log`, `.rc` |
| `scripts/probe_zqcs_dfi.py <sw/litex> 842 6000` | staged 0 ZQCS; unstaged 1 ZQCS (cycle 846); 7 REFRESH each | `receipts/probe_zqcs_dfi.log`, `.rc` |
| `scripts/mutate_timing_cuts.py <sw/litex> <mutant>` × 10 | 7 KILLED, 3 SURVIVED (the lossy registered-ready stages) | `receipts/mut_*.log`, `.rc` |
| Clone restore check | HEAD, tree and index tree equal the head; status empty including ignored; six gitlinks as at head | `receipts/clone_restore_check.txt` |

Hosted, read only (`receipts/hosted_check_runs_8b28ebaf.tsv`, sampled during this round): 57 check runs at the head. 46 completed success, 1 skipped, 10 still queued or in progress, none failed. The manager owns hosted and act acceptance. I neither claim nor infer a hosted verdict.

## Real limits

- No hardware. The flash stage has not run against a real pad-level flash. Bench evidence was a different integration image (an identity gate plus a REBOOT, cold-cut and gPTP re-check), and it is not hardware proof of this head. Physical calibration was NOT RUN.
- I ran no Vivado route, no full sweep, no rtl-fast, no builder bank and no manager source bank. The sweep (64/64), rtl-fast, docs gates, builder bank, #818 verdict, ooc and capture figures are the executor's published receipts, which I read; I did not reproduce them.
- F-1's idle analysis assumes both LiteDRAM timers leave reset together, as one sys reset releases them. Under DRAM traffic the bank-machine wait varies, so both designs issue ZQCS only by chance. I did not measure that rate.
- The LiteX checkout carries the project's patch series (VexiiRiscv variant and BIOS hook). No stage under review touches those files.
- The full LiteX aggregate (`run_litex_sims.sh <outdir>`) was not run here. Only its self-test and the two affected members were.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn and link the receipts.
- Accept hosted and act exact-head evidence, including the 10 runs still in flight when sampled.
- Route F-1 for either a fix or a recorded maintainer decision on the ZQCS contract.
- Route F-2 for a stalling behaviour arm.
- Re-record the area record on dev after the last release merge (record rule). This is not a finding here.

## Prior public findings on this PR

This section was read and written after the verdict and ledger above were on disk. At the time of reading, PR #826 has two issue comments, both the manager's review-start notices (6530896916, 6530905878). It has no review bodies and no inline review comments. There are no prior published review findings to resolve or retain at this head. F-1 and F-2 are new in this round.

R756-1 FINISHED
