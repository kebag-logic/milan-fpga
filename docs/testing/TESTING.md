# Testing & verification - the complete map

Every layer of verification in this repo, what it proves, and the exact
command to run it. This page is the map; the per-layer detail stays next to
the tests ([`tb/verilator/README.md`](../../tb/verilator/README.md),
[SIMULATION.md](SIMULATION.md), [RUNNING_TESTS.md](RUNNING_TESTS.md)) and the
protocol-level coverage contract is
[PROTOCOL_VALIDATION_MATRIX.md](PROTOCOL_VALIDATION_MATRIX.md).

> **Suite counts in prose go stale.** Never trust a number in a doc: the
> authoritative harness count is the directory listing (`ls tb/verilator/`,
> one dir per suite) and the authoritative synthesis-top count is the `tops`
> array in `syn/yosys/run.sh`. If a doc and the tree disagree, the tree wins.

## 0. Prerequisites

| Layer | Needs |
|---|---|
| Verilator harnesses | `verilator >= 5.0`, a C++17 compiler, **and** `git submodule update --init third_party/verilog-axis` (five suites elaborate Forencich cores) - no vendor tools |
| Yosys portability | `yosys` + [`sv2v`](https://github.com/zachjs/sv2v) on `PATH` + the same submodule |
| Migen DMA sims / SoC sim | a LiteX Python environment ([../litex/LITEX_SOC.md](../litex/LITEX_SOC.md) §7) |
| Legacy utests/itests | Vivado (xsim); `tb/avtp_packet_gen_sv` needs Modelsim/Questa |

## 1. Verilator RTL harnesses - `tb/verilator/` (the live regression)

Self-checking, exit `0` = PASS:

```sh
cd tb/verilator
for d in */ ; do ( cd "$d" && make clean >/dev/null && make ) || exit 1; done
```

Per-suite DUT/what-it-proves table: [`tb/verilator/README.md`](../../tb/verilator/README.md).
`ls tb/verilator/` is authoritative (one dir per suite).
Highlights: `milan_dp` drives the **whole `milan_datapath` wrapper** (the
LiteX integration boundary - CSR ID read, classifier programming, byte-exact
TX/RX); `controller_rate` is the gating regression born from the
[CBS datapath bug](../findings/CBS_DATAPATH_BUG.md); `cbs`/`ptp` check
arithmetic against independent reference models (10⁴-10⁵ checks each).


### 0.1 Coverage map — the module ↔ spec ↔ test matrix

[`docs/traceability/MODULE_MATRIX.md`](../traceability/MODULE_MATRIX.md) maps
**every** `hdl/` module to its spec family, the clause(s) it appears against,
and the testbench(es) that compile it — with a top **⚪ untested** list that
makes coverage gaps visible (roadmap item-3 per-module traceability). It is
**generated** from the RTL tree + the TB Makefiles + the tsn_fuzz campaign, so
it never drifts: `make matrix` regenerates it and `make matrix-check` (run by
`make` in `tb/verilator/tsn_fuzz/`) fails if the committed copy is stale. Each
spec-family leaf dir carries the same table as `README-tests.md`.

### 1.0 `tb/verilator/tsn_fuzz/` — IEEE 1722.1 field-validation campaign (2026-07-25)

Four co-simulation campaigns that drive the **real RTL** with spec-modelled
1722.1 traffic and grade every field of every message. tsn-gen supplies the
field/constraint model; the campaign builds real wire frames, reads DUT state
in-band, and gates on state stability. **3049 checks, 0 failures, 4 tracked
gaps.**

| campaign | DUT | checks | covers |
|---|---|---:|---|
| `make aecp` | `KL_aecp_top` | 2602 | getters × 19 descriptor types, setters (legal/illegal/SET→GET), header fuzz, addressing, length, **Milan v1.2 mandatory census 10/10** |
| `make adp` | `adp_advertiser` | 222 | all 20 advertised fields at their wire offsets, events, `available_index` |
| `make acmp` | `KL_acmp_listener` | 123 | 15 ACMP fields, all 16 message types, BIND→state→UNBIND, 70-byte rule |
| `make aaf` | parser→rxmon→depacketizer | 102 | per-field accept/reject verdicts, wire-truth channels, **lock survival** |
| `make legacy` | `KL_aecp_top` | 42 | the original 14-command cosim smoke driver |

Run `make` in that directory (~3 min). It **skips cleanly** when tsn-gen is
absent, so the suite stays runnable without the generator. Each campaign
writes its `TEST_RESULTS.md` **into the folder of the RTL it validates**
(`hdl/ieee17221/{aecp,acmp,adp}/doc/`, `hdl/ieee1722/avtp/doc/`), so a block's
verification status is visible from the block itself. Full rationale,
the tsn-gen wire-layout caveat and the tracked gaps: [`tb/verilator/tsn_fuzz/README.md`](../../tb/verilator/tsn_fuzz/README.md).

### 1.1 Suite index (47 harnesses, auto-listed 2026-07-25)

| suite | last verified |
|---|---|
| `tb/verilator/aaf` | run `make` in the dir |
| `tb/verilator/aaf_audio_loop` | run `make` in the dir |
| `tb/verilator/aaf_latency_taps` | 58/58 (07-25) |
| `tb/verilator/acmp` | run `make` in the dir |
| `tb/verilator/acmp_lstn` | run `make` in the dir |
| `tb/verilator/adp` | run `make` in the dir |
| `tb/verilator/adp_tx` | run `make` in the dir |
| `tb/verilator/aecp` | run `make` in the dir |
| `tb/verilator/avtp_rxmon` | run `make` in the dir |
| `tb/verilator/avtp_stream` | run `make` in the dir |
| `tb/verilator/cbs` | run `make` in the dir |
| `tb/verilator/cdc` | run `make` in the dir |
| `tb/verilator/chmap_capture` | PASS (07-25) |
| `tb/verilator/chmap_render` | 58/0 (07-25) |
| `tb/verilator/classifier` | run `make` in the dir |
| `tb/verilator/cls` | run `make` in the dir |
| `tb/verilator/controller_rate` | run `make` in the dir |
| `tb/verilator/crf_tx` | run `make` in the dir |
| `tb/verilator/csr` | 206+58+28 PASS (07-25 merge tip) |
| `tb/verilator/datapath` | run `make` in the dir |
| `tb/verilator/eth_tx_reset` | run `make` in the dir |
| `tb/verilator/hostplane` | KNOWN-FAIL on main until rtl-hostplane-fix merges (07-25) — see the suite README (host-plane lanes in the silicon shape) |
| `tb/verilator/i2spb` | run `make` in the dir |
| `tb/verilator/ifg` | run `make` in the dir |
| `tb/verilator/lat_history_ring` | run `make` in the dir |
| `tb/verilator/link_guard` | 104/104 (07-24 merge gate) |
| `tb/verilator/lwsrp` | run `make` in the dir |
| `tb/verilator/lwsrp_ctx` | run `make` in the dir |
| `tb/verilator/lwsrp_rx` | run `make` in the dir |
| `tb/verilator/lwsrp_switchpdu` | run `make` in the dir |
| `tb/verilator/lwsrp_tx` | run `make` in the dir |
| `tb/verilator/maap` | run `make` in the dir |
| `tb/verilator/milan_dp` | 70/0 + 82/0 (07-25 merge tip) |
| `tb/verilator/mmcm_servo` | run `make` in the dir |
| `tb/verilator/mmcm_servo_autorepair` | run `make` in the dir |
| `tb/verilator/pcm_ring_bram` | run `make` in the dir |
| `tb/verilator/pcm_tx` | run `make` in the dir |
| `tb/verilator/pcmlpf` | run `make` in the dir |
| `tb/verilator/ptp` | run `make` in the dir |
| `tb/verilator/ptp_sync` | run `make` in the dir |
| `tb/verilator/ptp_ts` | run `make` in the dir |
| `tb/verilator/queues` | run `make` in the dir |
| `tb/verilator/rx_filter` | run `make` in the dir |
| `tb/verilator/shaper_core` | run `make` in the dir |
| `tb/verilator/tcam` | run `make` in the dir |
| `tb/verilator/tcam_csr` | run `make` in the dir |
| `tb/verilator/tdm` | run `make` in the dir |
| `tb/verilator/tdm_render` | run `make` in the dir |

The six counts above were re-run at the 2026-07-25 11-PR merge tip; every
other suite is one `make` away (self-checking, exit-code gated). The standing
rule: every round grows this table, never shrinks it.

## 2. Migen DMA-engine sims - `sw/litex/test_*.py`

Behavioral sims of the ring-DMA/BD engines that live in `milan_soc.py`
(the layer the RTL harnesses cannot see, and the SoC sim is too slow to
sweep). Self-checking (`ALL PASS`):

```sh
cd sw/litex
for t in test_ring_dma test_ring_bd test_ring_tx test_ring_writeback \
         test_rx_steer test_tx_bd; do python3 $t.py || exit 1; done
```

## 3. SoC-level simulation - `sw/litex/milan_sim.py`

Boots the real LiteX BIOS on the softcore with the real `milan_datapath`
mapped at `0x9000_0000`, over Verilator - proves the CPU⇄CSR path end to end
(milestone M-A2: BIOS reads ID `"MILN"`).

```sh
cd sw/litex && ./milan_sim.py --non-interactive
```

Detail (incl. what each of the three sim layers can and cannot catch):
[SIMULATION.md](SIMULATION.md).

## 4. Device-portability check - `syn/yosys/`

sv2v + Yosys `synth` + `hierarchy -check` over every top in the
`syn/yosys/run.sh` `tops` array (the authoritative list; fails on any
leftover vendor primitive), plus a concrete non-Xilinx mapping:

```sh
cd syn/yosys
make          # generic, device-independent
make ecp5     # Lattice ECP5 mapping
```

Proves synthesizability off-Xilinx, not behaviour (layer 1 does that) and
not timing. See [../integration/PORTING_GUIDE.md](../integration/PORTING_GUIDE.md) §5.
`run.sh` also prints two trailing structural reports: the tied-off-input
inventory (`scripts/check_tied_inputs.sh`, the RMON class) and the
observer-purity check (`syn/yosys/check_tap_purity.sh` — taps/telemetry must
never drive the observed streams' nets; standalone it is exit-coded and
self-tests against a deliberately-broken fixture).

## 5. Legacy / auxiliary testbenches

| Where | What | Status |
|---|---|---|
| `tb/utests/` | Hand-written SystemVerilog TBs run under Vivado **xsim** (`vivado -mode tcl -source <tb>.tcl` where a `.tcl` exists) | **Superseded** for regression by the Verilator suites ([`tb/utests/802_1q_traffic_shaper/README.md`](../../tb/utests/802_1q_traffic_shaper/README.md) maps old→new); waveform-inspection style, not exit-code gating |
| `tb/itests/` | xsim integration TBs: `ptp_timestamp/` (has `.tcl`, Vivado 2023.1) and `802_1q_traffic_shaper/` (**`.sv` only - no `.tcl` runner**) | Legacy; the Verilator `milan_dp`/`datapath` suites cover the integration seams without vendor tools |
| `tb/avtp_packet_gen_sv/` | Randomized AVTP packet-generator class library for the xsim TBs (Modelsim/Questa: `cd tb/avtp_packet_gen_sv/examples && do run.do`) | Development aid, in-progress |
| `tb/common/` | `axi_stream_driver.svh` - shared AXIS BFM class for the xsim TBs (the Verilator suites have their own C++ BFMs) | - |

## 6. On-silicon validation

**Mandatory first step after EVERY flash: `scripts/hostplane_smoke.sh` on
the board shell (~60 s).** It verifies the host plane specifically —
`rx_packets` increments, the dma-ts ring offset advances, ID=`MILN` +
VERSION readable, the `AAF_CTRL` VID field intact (`0x0002xxxx`), the ALSA
card module loaded — one PASS/FAIL line per check, nonzero exit on any FAIL.
Rationale: a build whose fabric paths (AAF/CRF/SRP/ADP) run perfectly can
still ship with a dead host plane (2026-07-25 regression class), and every
audio-first drill stays green while the kernel sees nothing. Do not start
any other board procedure until this passes.

Bring-up order and board procedures:
[../integration/BOARD_PORTING_AX7101.md](../integration/BOARD_PORTING_AX7101.md)
(CSR ID read → MAC → DMA), [../integration/QSPI_FLASHBOOT.md](../integration/QSPI_FLASHBOOT.md)
(boot), [RUNNING_TESTS.md](RUNNING_TESTS.md) (all-layers walkthrough incl.
board), and the in-fabric telemetry that instruments silicon runs:
[../fpga/pipeline-telemetry.md](../fpga/pipeline-telemetry.md). Protocol-by-
protocol validation status: [PROTOCOL_VALIDATION_MATRIX.md](PROTOCOL_VALIDATION_MATRIX.md).
Performance measurements on silicon are logged in the
[findings log](../findings/README.md) with their methodology.

## 7. Known gaps (kept honest)

* **CI runs the paper gates only.** [`.github/workflows/docs.yml`](../../.github/workflows/docs.yml)
  runs the docs gate (twice — the second time with `.git` deleted, so the
  tarball/zip path stays honest), the traceability no-drift gate and the
  end-station builder gates. The Verilator harnesses are CI-ready (exit codes)
  but **nothing runs them automatically**; adding layers 1, 2 and 4 to that
  workflow is the obvious next step. Local commands:
  [`../../QUICKSTART.md`](../../QUICKSTART.md) §2.
* **`avtp_stream_parser` has a Verilator suite but is not in the Yosys tops
  list** - its device portability is unchecked.
* `milan_top` (Zynq variant) is not coverable by the open flows (PS7 + the
  external verilog-ethernet MAC); its TSN content is covered via
  `milan_dp`.
* The legacy xsim TBs test pre-rework interfaces in places; trust the
  Verilator suites where they disagree.
* Check-counts quoted in READMEs are informational; the harnesses print
  their own counts at run time.

## Policy

Every DUT change ships with its harness update **in the same commit** - the
CSR harness is the executable form of
[../reference/REGISTER_MAP.md](../reference/REGISTER_MAP.md), and a new RTL
module is not "done" until it appears in layer 1 (and layer 4 unless it is
vendor-gated).
