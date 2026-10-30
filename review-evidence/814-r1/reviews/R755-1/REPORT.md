[R755] NEGATIVE - exact head 8b28ebaf035e786ccf5b8e50098dbc111f51831f

# R755-1 internal cleared-context review: kebag-logic/milan-fpga PR #826 (issue #814)

- Head under review: `8b28ebaf035e786ccf5b8e50098dbc111f51831f`, tree `1a9c6972e1e2c19edd9138e1d481a1bbcbe4fd4a`.
- Base: dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
- Delta: five commits `cd83cd16..8b28ebaf` touching:
  - `sw/litex/milan_soc.py`
  - `sw/litex/test_soc_timing_cuts.py`
  - `scripts/run_litex_sims.sh`
  - `ci/image/exec-audit.json`
  - `docs/testing/TESTING.md`
  - `docs/litex/CLOCK_DOMAINS.md`
- Every reviewer run used the pinned LiteX set from `sw/litex/litex_pins.txt`, checked out at exactly those revisions, on Python 3.14.8:
  - migen `4c2ae8df`
  - litex `a1e1c365`
  - litedram `f9b75e03`
  - litespi `02d5a209`

## Verdict

**NEGATIVE.** The three stages are functionally sound, and so are their timing cuts. Reviewer probes show:

- no drop, duplicate or reorder;
- the AXI handshake rules hold;
- SPI chip-select alignment holds;
- refresh spacing is preserved.

Two MINOR findings make the verdict NEGATIVE:

- **F-1.** The gate's behaviour arms never put a beat into either stage's skid register. A stage that keeps the timing cut but loses a held beat passes every arm.
- **F-2.** The registered refresher changes when LiteDRAM issues a ZQCS. On an idle controller at the board clock, the shipped image stops issuing ZQCS altogether. The source, the test and the PR body all say ZQCS is only one cycle later, or unchanged, and the gate does not grade ZQCS.

Neither finding is wording only. Together they leave four lenses unclean: Conformance, RTL, Tests and Docs.

## Reconstruction (public state only)

- AGENTS.md, CONTRIBUTING.md (by reference) and docs/README.md, for the lens and severity rules.
- Issue #814: body, Scope and Acceptance.
  - The #708 rule: a logic cut in `sw/litex/milan_soc.py`, recipe unchanged, no pblocks, no floor exception.
  - Each cut keeps its bus contract.
  - Flash boot, `check_nvm_capture.py`, the SoC and DDR-backed suites, the full sweep, rtl-fast and the docs gates must pass.
- Rulings, read by ID rather than by listing comments:
  - issuecomment-6514717735: the assignment and its gates. It includes the STOP "a cut changes bus behaviour that a suite sees, beyond latency".
  - issuecomment-6527475726: #814 is back in the release. The round-2 route set is judged with the #818 gate, and the record is not re-recorded.
- PR #826, read through `gh pr view --json` only: title, body, head and base, files, commits.
- Published evidence `review-evidence/814-r1` at `28195920`:
  - `author/REVIEW-READY.md`
  - `author/receipts/gate818/check-set.log` and `.rc`
  - `author/receipts/builder-8b28ebaf/builder_bank.rc`
  - the receipt tree listing: sweep shards 0 to 3, rtl-fast logs, docs receipts.

## What was checked, and how

### F1 `SPIPHYStage`

Code: `sw/litex/milan_soc.py:2465-2507`, installed by `MilanSoC.add_spi_flash` at `:3670-3690`.

- **What LiteSPI reads from the PHY.** Only `phy.sink`, `phy.source`, `phy.cs` and `phy.flash` (`litespi/__init__.py:77-119`). `stage_spi_phy` swaps exactly those three before `LiteSPI(...)` is built, so both the core and the crossbar bind to the stage.
- **No command is in flight when cs drops.** The PHY returns one status or data word per command (`litespi/phy/generic_sdr.py`, SEND-STATUS-DATA). Every mmap state that issues a command waits for that return before cs changes (`litespi/core/mmap.py`: CMD-RET, ADDR-RET, DUMMY-RET, BURST-DAT).
- **Command and cs stay aligned.** The registered cs and the `stream.Buffer(pipe_valid=True)` command reach the PHY together, one cycle later. The one-cycle cs gap on a new burst (`mmap.py` IDLE, `cs.eq(0)`) is kept, shifted by one cycle.
- **The PHY is built the way pinned LiteX builds it** (`litex/soc/integration/soc.py`, `add_spi_flash`):
  - the same divisor, rounded to even at 1:1;
  - the same pads request, including `number`;
  - the same `LiteSPIPHY(...)` arguments. The one exception is `master_with_irq`, which the PHY ignores (`LiteSPICSControl(**kwargs)`).
- **CSR names and constants are unchanged.** The PHY is still added as the core's `phy` submodule, so names and constants such as `SPIFLASH_PHY_FREQUENCY` stay the same. `LiteSPIPHY.get_csrs` returns only the inner core's CSRs, so the stage adds none.
- **No moved cell is named anywhere.** No constraint or `syn/` script names one; `syn/resmap/resmap_map.py:111` matches by prefix.
- **Stall probe** (`scripts/probe_spi_stage.py standalone`, random PHY READY and core READY):
  - 300 commands and 300 responses, none dropped, duplicated or reordered;
  - PHY cs equals core cs one cycle earlier, on every cycle;
  - the tx skid was full for 424 cycles and the rx skid for 499.
  - Receipt: `receipts/probe_spi_standalone.log`, PASS.
- **The firmware's LiteSPI master path also runs through the stage.** `tb/verilator/nvm_capture_cpu/soc.py:63-70` builds through `MilanSoC.add_spi_flash`, so the capture recipe covers erase, program and read-back. The published capture is 13.85922 ms against 24.5 ms; that is author evidence.
- **The planted-wire arm F2 names the bridge.** In the planted-wire build, the AXI-Lite bridge's own FSM reaches `litespiclkgen_cnt` and the SDR shift counters. With the shipping stage, nothing from the bridge or the core reaches them (`receipts/probe_f2_bridge.log`).

### F2 `AXIReadyStage`

Code: `:2397-2427`, used in `cross_cpu_memory_ports` at `:2382-2392`.

- **Clock domain.** `cd_to` is `"sys"` at every call site (`:3139`, and the test), so the stage's `sync` block is correct.
- **LiteX `PipeReady`** (`litex/soc/interconnect/stream.py`):
  - `sink.ready = ~valid` is a register, so READY has no combinational path and there is no loop;
  - a held beat is presented next, with VALID and payload stable until READY;
  - with no stall, no cycle is added.
- **Other channels.** `w`, `b` and `r` pass straight through. AXI4 lets `w` lead `aw`, and the stage reorders nothing within a channel, so the aw/w relation is unchanged.
- **Stall probe** (`scripts/probe_axi_stage.py shipping`): random back-to-back and stalled AXI-legal traffic on aw, w and ar, against a random slave READY:
  - 400 beats per channel, identical and in order;
  - 0 slave-face VALID or payload stability violations;
  - hold engaged on 455 cycles (aw) and 547 (ar);
  - r passes through.
- **Controls.** The `lossy` mutant fails, accepting 238 and 232 of 400. The `dup` mutant deadlocks the probe. Receipts: `receipts/probe_axi_stage_*.log` and `.rc`.

### F3 `RegisteredRefresher`

Code: `:2430-2462`.

- **How the controller uses it.** It is built as `refresh_cls(settings, clk_freq=, zqcs_freq=, postponing=)` (`litedram/core/controller.py:89`). The controller uses only `.cmd` (`multiplexer.py:258,320,393-394`).
- **What is registered.** `valid` and `last`. The payload passes from the executers' flip-flops, and `ready` passes back.
- **Refresh is correct.** The inner FSM waits on the outer READY, and the multiplexer's REFRESH state exits on the registered `last`. So the sequence keeps its order and shifts by one cycle. The tREFI timer runs free, so the average refresh rate is unchanged, and so are tRP and tRFC inside a sequence. The gate's Z3 arm confirms this for PRECHARGE and REFRESH.
- **ZQCS is not just shifted.** See F-2.

### Gate kill power

Reviewer mutants, run through the gate's own arms with `scripts/probe_gate_mutants.py`:

| Mutant | Gate arms run | Result |
|---|---|---|
| `axi-aronly` (aw left unpiped) | D0..D2 | KILLED (D0, D1) |
| `axi-lossy` (READY tied high) | D0..D4 | KILLED (D0) |
| `ref-lastcomb` (`last` combinational) | Z0..Z2 | KILLED (Z0, Z1) |
| `ref-2cycle` (two registers) | Z3 | KILLED |
| `axi-dropheld` (registered READY kept, held beat lost) | D0..D4 | **SURVIVED** |
| `spi-dropheld` (registered READY kept, held beat lost) | F0..F5 | **SURVIVED** |
| `spi-lossy` (READY tied high in the skid) | F3..F5 | **SURVIVED** |

With the shipping stages in place, the gate's own behaviour traffic never fills a skid register. The SPI tx and rx skids and the AXI aw and ar skids stay empty on every cycle (`receipts/mutant_hold_flash.log`, `receipts/mutant_hold-dram.log`).

## Findings

### F-1 MINOR — lens: Tests — the behaviour arms never exercise a stage's stall path

**Where**
- `sw/litex/test_soc_timing_cuts.py:288-357`: `flash_reads` and `flash_behaviour` run on `LiteSPIPHYModel`, whose `sink.ready` is `cs` (`litespi/phy/model.py:67`).
- `sw/litex/test_soc_timing_cuts.py:437-518`: `dram_traffic` and `dram_behaviour` send one single-beat burst at a time; each write waits for B and each read for R.
- The same claims appear in `docs/testing/TESTING.md:735-741`.

**Authority**
- AGENTS.md section 6, Tests: each new test can fail for the defect it claims to detect.
- AGENTS.md section 5: test the ordering and failure paths.
- The assignment's STOP (issuecomment-6514717735): "a cut changes bus behaviour that a suite sees, beyond latency".

**Evidence**
- A READY register adds exactly one new piece of state: the beat it holds while the far side stalls. The gate's traffic leaves that register empty on every cycle:
  - `receipts/mutant_hold_flash.log`: `{'spi.tx.pipe_ready': 0, 'spi.rx.pipe_ready': 0}`
  - `receipts/mutant_hold-dram.log`: `{'axi.aw_pipe': 0, 'axi.ar_pipe': 0}`
- A stage that keeps the registered READY, and so keeps the cut, but loses the held beat passes all six flash arms and all five DRAM arms (`receipts/mutant_spi-dropheld.log`, `receipts/mutant_axi-dropheld.log`: `MUTANT SURVIVED`).
- The real product reaches this path:
  - **SPI.** On the real PHY, a new burst inside the burst window drops cs for one cycle (`mmap.py` IDLE). `LiteSPICSControl` then holds `enable` low for `cs_delay + 1` = 11 cycles (`litespi/cscontrol.py`). `WAIT-CMD-DATA` takes a command only on `cs_control.enable & sink.valid` (`generic_sdr.py`), so the stage's tx skid holds that command.
  - The real PHY cannot be elaborated in migen simulation because it contains Xilinx primitives (`receipts/probe_spi_realphy.log`). This case is argued from source.
  - **DRAM.** LiteDRAM's AXI-to-native arbitration stalls aw and ar whenever it serves the other direction or the native port is not ready.

**Impact.** The shipping stages are correct today, as the F1 and F2 probes above show. But the repository's evidence for "no behaviour change" covers only the pass-through branch. A regression in, or a substitute for, the skid logic would merge green.

**Required outcome.** The behaviour arms must:
- hold a beat in each stage's skid register, using a PHY or native side that withholds READY, plus back-to-back AXI traffic;
- require the same transfers, in the same order, as the wired build;
- fail when a stage loses or repeats a held beat.

**Verification.** At the fixed head, the hold counts are non-zero, and these mutants (or the gate's own planted equivalents) are killed:
- `scripts/probe_gate_mutants.py <repo> spi-dropheld`
- `scripts/probe_gate_mutants.py <repo> axi-dropheld`

### F-2 MINOR — lenses: Conformance, RTL, Tests, Docs — the registered refresher stops idle ZQCS, but the change says ZQCS is only one cycle later

**Where**
- `sw/litex/milan_soc.py:2439-2440`: "So each refresh and ZQCS starts and ends one cycle later, with its own tRP, tRFC and tZQCS spacing".
- `sw/litex/test_soc_timing_cuts.py:586-589`: Z3 leaves ZQCS out because its commands are "behind the same two registers".
- PR body, Known limitations: "That is upstream behaviour, unchanged here."

**Authority**
- Issue #814 and its assignment: a logic cut, with no bus-behaviour change beyond latency.
- Check (1) of this round's brief: the refresh and ZQCS intervals that LiteDRAM's settings declare are kept.
- AGENTS.md section 8: never hide a material behaviour change in code.

**How LiteDRAM issues a ZQCS**
- The ZQCS timer emits a one-cycle pulse every Z = int(clk/zqcs_freq) cycles, counted from reset (`litedram/core/refresher.py`, `RefreshTimer` with `wait = ~zqcs_executer.done`).
- The FSM starts a ZQCS only when that pulse lands on the cycle `sequencer.done` is high (DO-REFRESH).
- On an idle controller, `sequencer.done` falls k cycles after each free-running tREFI pulse.

**Measured** on the gate's own DramSoC (MT41J256M16, 100 MHz; `receipts/probe_zqcs_phase.log`):
- tREFI = 782 and Z = 100,000,000, so gcd(Z, tREFI) = 2.
- k = 60 for LiteDRAM's refresher. k = 61 for the shipping one, because the registered request delays the bank-machine grant by one cycle.
- That log's per-line "first ZQCS pulse at 0 / coincides" fields are wrong. They read a reset-less mirror of the ZQCS counter. The actual first pulse is at Z - 1 = 99,999,999, from the counter's reset value. Use that log for tREFI, Z, the first tREFI pulse (781) and k only.
- A coincidence needs Z - 1 - 781 - k to be even (`receipts/zqcs_real_period.txt`):
  - LiteDRAM's own refresher issues its first idle ZQCS 76 s after reset, then one every 391 s.
  - The shipping refresher never issues one while idle.

**Simulated directly**, in the same parity class with the ZQCS period shortened to 10 cycles (`receipts/probe_zqcs_direct.log`):
- LiteDRAM's refresher puts a ZQCS on the DFI at cycle 3974.
- The shipping refresher puts none in 5,092 cycles. Its PRECHARGE and REFRESH commands are otherwise as expected.

**Impact**
- On an idle DDR3 at the board clock, the shipped image no longer issues ZQCS, the ZQ short calibration for driver and ODT drift.
- Under traffic, both versions issue ZQCS only by coincidence, and neither comes near the declared 1 Hz.
- DDR3 does not mandate a ZQCS interval, so this is not a protocol breach. It is an undeclared behaviour change, hidden behind a "one cycle later" claim that the gate cannot see.

**Required outcome.** One of these, and in both cases a ZQCS arm in the gate:
- The shipping refresher preserves LiteDRAM's ZQCS issuance.
- Or the change is published with its measured effect and a recorded maintainer decision, and the three statements above are corrected.

The gate must grade ZQCS with a shortened ZQCS period (for example, by passing `zqcs_freq` through `refresh_cls`), so that a change in ZQCS issuance is graded, not argued.

**Verification**
- `scripts/probe_zqcs_direct.py <repo>` shows the outcome the decision chose.
- The gate's ZQCS arm passes on it and fails on the other refresher.

### S-1 SUGGESTION — lens: Tests — `sw/litex/test_soc_timing_cuts.py:282`: F2's filter does not tell the bridge from the core

- F2 checks `path.startswith("fsm_state")`. That also matches LiteSPI's mmap FSM, so the arm would still pass if only the core reached the counter.
- The bridge path does exist today (`receipts/probe_f2_bridge.log`), so this is optional.
- A sharper filter would intersect the starts with `registers(bridge)`, as the probe does.

## Clean results

- [R755] PASS Robustness — `sw/litex/milan_soc.py:2418-2427,2443-2451,2483-2493`, with `receipts/probe_axi_stage_shipping.log` and `receipts/probe_spi_standalone.log`.
  - Checked: the stages under random stalls, back-to-back beats, idle gaps and both READY directions.
  - Result: no loss, duplicate or reorder, and VALID and payload stay stable under backpressure.
  - Every stage register resets to 0 with sys.
  - Lossy and duplicating skids are caught (`probe_axi_stage_lossy.rc`, `probe_axi_stage_dup.rc`).

These partial results bank no lens:

- `sw/litex/milan_soc.py:3670-3690`, compared against pinned LiteX `add_spi_flash`: the PHY, divisor, pads, CSR names and constants are equivalent.
- The `ci/image/exec-audit.json` entry `57b84e8b…` was recomputed. It equals the sha256 of the stand-in that `run_litex_sims.sh --selftest` writes.
- Comment rule: `git diff 1e80128f..8b28ebaf` was scanned. The delta has no lane, round, reviewer or issue-comment label.

## Executed at this head (reviewer)

- `cd sw/litex && python3 test_soc_timing_cuts.py`: rc 0, 15 arms `[ok]`, `RESULT: PASS`, 6 m 45 s (`receipts/head_test_soc_timing_cuts.log` and `.rc`).
- `scripts/run_litex_sims.sh --selftest`: rc 0, 10 of 10 (`receipts/litex_sims_selftest.log` and `.rc`).
- `scripts/run_litex_sims.sh <dir>`: rc 0, `simulations: 8 passed: 8 failed: 0 skipped: 0 timed out: 0`, 17 m 01 s (`receipts/litex_sims_aggregate.log` and `.rc`).
- The probes and mutants listed above. Each script is in `scripts/` and takes the repository root as its first argument.
- Host paths in the receipts are replaced by placeholders: `<clone>`, `<packet>`, `<litex-env>`, `<home>`, `<tools>` and `<tmp>`.
- About `receipts/mutant_hold_flash.log`:
  - It is the first `hold` run. Its flash half printed the flash hold counts, which this report uses.
  - Its DRAM half then stopped on a probe bug, an `AttributeError` on the planted `WirePassThrough`. So it has no `.rc`.
  - The DRAM counts come from the corrected `hold-dram` run.
- No probe edited the clone. Mutants were installed in-process with Python monkeypatching only.
- After the runs, the generated and ignored files the runs created were removed (`__pycache__`, `sw/builder/out`, `configs/generated/*.hex`, `tb/verilator/gptp_txts/obj_pad`). Then the clone was checked against the head (`receipts/clone_restore_check.txt`):
  - HEAD `8b28ebaf…`;
  - tree and index tree `1a9c6972…`;
  - `git status --ignored` empty;
  - all six gitlinks as at the head.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F-2) | issue #814 acceptance and rulings; `milan_soc.py:2397-2507,3670-3690`; LiteSPI mmap, PHY and cscontrol, and LiteDRAM refresher, multiplexer and controller at the pins; `probe_zqcs_*` | R755-1 | 8b28ebaf035e786ccf5b8e50098dbc111f51831f |
| RTL | UNCLEAN (F-2) | `milan_soc.py:2382-2507`; LiteX `PipeReady`, `PipeValid` and `Buffer`; clock-domain call site `:3139`; name references in constraints and `syn/` | R755-1 | 8b28ebaf035e786ccf5b8e50098dbc111f51831f |
| Robustness | CLEAN | `probe_axi_stage.py`, `probe_spi_stage.py standalone`; stage reset values | R755-1 | 8b28ebaf035e786ccf5b8e50098dbc111f51831f |
| Tests | UNCLEAN (F-1, F-2) | `sw/litex/test_soc_timing_cuts.py:1-618`; `scripts/run_litex_sims.sh` inventory and self-test; `ci/image/exec-audit.json`; `probe_gate_mutants.py` (9 arms) | R755-1 | 8b28ebaf035e786ccf5b8e50098dbc111f51831f |
| Docs | UNCLEAN (F-2) | `docs/testing/TESTING.md:719-741`; `docs/litex/CLOCK_DOMAINS.md:273-281`; `milan_soc.py` docstrings; PR body | R755-1 | 8b28ebaf035e786ccf5b8e50098dbc111f51831f |

## Prior public findings on this PR

This section was written after the verdict and the ledger above were on disk.

**What PR #826 carried when read:**
- Two manager review-start notices: 6530896916 and 6530905878.
- One review round: `[R756] NEGATIVE - exact head 8b28ebaf…` (6532064254), posted at this same head while this round ran.
- No review bodies and no inline review comments.

**Each R756-1 finding, retained at this head:**
- **R756 F-1 MINOR** (ZQCS issuance changed, with incorrect ZQCS claims). RETAINED. It is the same defect as this round's F-2, found independently, under the same four lenses: Conformance, RTL, Tests and Docs.
  - R756 used its own probe at a different shortened period. It also got upstream 1 ZQCS against shipping 0, and the upstream first idle ZQCS at 76.0 s. Both figures agree with `receipts/probe_zqcs_phase.log`, `receipts/probe_zqcs_direct.log` and `receipts/zqcs_real_period.txt`.
- **R756 F-2 MINOR** (the stall path of both registered-READY stages is never exercised). RETAINED. It is the same defect as this round's F-1.
  - The lens attribution differs. R756 files it under Tests and Robustness. This round files it under Tests only, because the shipping stages' backpressure behaviour was applied and found clean here (`receipts/probe_axi_stage_shipping.log`, `receipts/probe_spi_standalone.log`).
  - The gap is the repository's gate, not the design.
  - Under AGENTS.md section 3, a disputed label is recorded under both lenses. The manager should treat Robustness as unclean until the fix lands. Doing so changes no verdict, and the re-review at the fixing head re-covers Robustness either way.

No prior finding is resolved at this head. Both stay open until a new commit fixes them.

## Real limits

- **No hardware.**
  - The real LiteSPI PHY could not be simulated, so its stall is argued from source.
  - The bench report of an integration image that carries this change is the manager's; this review did not observe it.
- **Not re-run by the reviewer.** These are author receipts (`review-evidence/814-r1/author/receipts`): the full suite sweep, rtl-fast, the docs gates, the builder bank, `check_nvm_capture.py`, the Vivado routes and the #818 gate.
  - The #818 `check-set.log` was read: rc 0, ExtraPostPlacementOpt at +0.128 ns, every corner at or above +0.030 / 0, the fall a WARNING.
  - The builder bank result was read: rc 0.
- **No manager source bank** exists at this head, and none is claimed.
- **No physical calibration.** It was not run, and field skips are not hardware proof.
- **The ZQCS figures (76 s, 391 s) assume** an idle controller at exactly 100 MHz from reset. Under CPU or DMA traffic, k varies and both refreshers issue ZQCS only by coincidence.
- **The record** still carries dev's route. Under the manager's record rule, that is not a finding.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and link the receipts.
- Hosted and act acceptance for the exact head.
- Carry F-1 and F-2 to the executor. Both need a new commit, so coverage of every lens they touch must be banked again at that head.

R755-1 FINISHED
