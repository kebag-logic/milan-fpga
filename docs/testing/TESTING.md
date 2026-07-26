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
| Verilator harnesses | `verilator >= 5.050` (the CI pin — see §7: 5.020 **cannot build** four suites and 5.032 mis-reads six `aecp` checks), a C++17 compiler, **and** `git submodule update --init third_party/verilog-axis` (five suites elaborate Forencich cores) - no vendor tools |
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

### 1.1 Suite index — the full sweep, run 2026-07-26

`scripts/run_all_suites.sh` over every dir under `tb/verilator/` that has a
`Makefile`:

```
suites: 55   passed: 55   failed: 0
checks: 2064050   in-suite failures: 0
```

Verilator v5.050. The check total aggregates the suites that print a `checks:`
line; the rest are exit-code gated only, which is why the third column is a note
rather than a number for those.

**This table is not the authority — `ls tb/verilator/` is.** Rerun the sweep
rather than trusting the row count here.

| suite | 2026-07-26 sweep | note |
|---|---|---|
| `tb/verilator/aaf` | PASS | — |
| `tb/verilator/aaf_audio_loop` | PASS | — |
| `tb/verilator/aaf_latency_taps` | PASS | 73 checks — the per-stage TX/RX taps |
| `tb/verilator/acmp` | PASS | — |
| `tb/verilator/acmp_lstn` | PASS | — |
| `tb/verilator/adp` | PASS | — |
| `tb/verilator/adp_tx` | PASS | — |
| `tb/verilator/aecp` | PASS | — |
| `tb/verilator/aes3` | PASS | 50 checks — the AES3/S-PDIF ser/des family |
| `tb/verilator/avtp_parser` | PASS | 10 665 checks — the listener ACCEPT VERDICT at every shipping shape; carries the entry-0 blocker guard (T6) |
| `tb/verilator/avtp_rxmon` | PASS | — |
| `tb/verilator/avtp_stream` | PASS | — |
| `tb/verilator/cbs` | PASS | 129 407 checks — CBS arithmetic vs a fixed-point replica and an ideal 802.1Qav model |
| `tb/verilator/cdc` | PASS | — |
| `tb/verilator/chmap_capture` | PASS | — |
| `tb/verilator/chmap_render` | PASS | — |
| `tb/verilator/classifier` | PASS | — |
| `tb/verilator/cls` | PASS | 200 073 checks — classification incl. the reserved-DMAC control table and the tagged-0x22F0 negative |
| `tb/verilator/controller_rate` | PASS | the gating regression born from the CBS datapath bug |
| `tb/verilator/crf_rx` | PASS | — |
| `tb/verilator/crf_tx` | PASS | — |
| `tb/verilator/csr` | PASS | 337 checks — the executable form of [REGISTER_MAP.md](../reference/REGISTER_MAP.md) |
| `tb/verilator/datapath` | PASS | — |
| `tb/verilator/eth_tx_reset` | PASS | — |
| `tb/verilator/hostplane` | PASS | 77 checks — the silicon-shape host lanes (RX delivery, ts records, filter-no-leak) |
| `tb/verilator/i2spb` | PASS | — |
| `tb/verilator/ifg` | PASS | — |
| `tb/verilator/lat_history_ring` | PASS | — |
| `tb/verilator/link_guard` | PASS | — |
| `tb/verilator/lwsrp` | PASS | — |
| `tb/verilator/lwsrp_ctx` | PASS | — |
| `tb/verilator/lwsrp_rx` | PASS | — |
| `tb/verilator/lwsrp_switchpdu` | PASS | — |
| `tb/verilator/lwsrp_tx` | PASS | — |
| `tb/verilator/maap` | PASS | — |
| `tb/verilator/mac_rmon` | PASS | the revived RMON event derivation + STATS_CAP |
| `tb/verilator/milan_dp` | PASS | 282 checks — the whole milan_datapath wrapper at legacy, N=4 and N=8; carries the entry-0 blocker guard (TRAP-1) |
| `tb/verilator/mmcm_servo` | PASS | — |
| `tb/verilator/mmcm_servo_autorepair` | PASS | — |
| `tb/verilator/pcm_playback` | PASS | 40 checks — host ring → KL_pcm_tx → render crossbar → feed mux → DAC pin, bit-exact plus the negatives |
| `tb/verilator/pcm_ring_bram` | PASS | — |
| `tb/verilator/pcm_tx` | PASS | — |
| `tb/verilator/pcmlpf` | PASS | — |
| `tb/verilator/persist` | PASS | the KLJ1 saved-state journal decode + replay |
| `tb/verilator/ptp` | PASS | 201 250 checks — PHC arithmetic vs an independent reference model |
| `tb/verilator/ptp_sync` | PASS | — |
| `tb/verilator/ptp_ts` | PASS | — |
| `tb/verilator/queues` | PASS | — |
| `tb/verilator/rx_filter` | PASS | — |
| `tb/verilator/shaper_core` | PASS | 1 520 848 checks — FQTSS/arbitration, incl. the gPTP-not-starved measurement |
| `tb/verilator/tcam` | PASS | — |
| `tb/verilator/tcam_csr` | PASS | — |
| `tb/verilator/tdm` | PASS | — |
| `tb/verilator/tdm_render` | PASS | — |
| `tb/verilator/tsn_fuzz` | PASS | the IEEE 1722.1 field-validation campaign (skips cleanly without tsn-gen) |

The standing rule: every round grows this table, never shrinks it.

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

* **The BDD conformance suite runs on every verification round** (USER standing
  order, 2026-07-26). `cd tests && behave` — 21 features / 113 scenarios /
  1169 steps, offline by default (the Python models in `tests/steps` mirror the
  RTL, so it needs no DUT binary and no simulator, and finishes in ~3 s). It is
  the spec-facing counterpart to the Verilator suites: those prove the RTL does
  what it does, this proves it does what the standard says. Wired in as the
  `bdd-conformance` job so it is a gate, not something to remember.
* **CI now runs the RTL gates too** (2026-07-26).
  [`.github/workflows/docs.yml`](../../.github/workflows/docs.yml) runs the docs
  gate (twice — the second time with `.git` deleted, so the tarball/zip path
  stays honest), the traceability no-drift gate and the end-station builder
  gates; [`.github/workflows/rtl.yml`](../../.github/workflows/rtl.yml) runs the
  whole Verilator sweep via `scripts/run_all_suites.sh` and the Yosys
  portability sweep. Both RTL jobs need the `verilog-axis` submodule, which is
  why they are a separate workflow from the submodule-free docs gates. Local
  commands: [`../../QUICKSTART.md`](../../QUICKSTART.md) §2.
* **The Verilator version matters, and distro packages are not enough.**
  Measured 2026-07-26 by running the suites under each version in a container:

  | Verilator | ships with | result |
  |---|---|---|
  | 5.020 | Ubuntu 24.04 | **cannot build** `aecp`/`hostplane`/`milan_dp`/`tsn_fuzz` — `BLKLOOPINIT: Delayed assignment to array inside for loops`, on legal SystemVerilog that Yosys synthesises fine |
  | 5.032 | Debian trixie, Ubuntu 25.04 | builds, but **6 of 490 `aecp` checks** read back `0` (AS_PATH / AVB_INFO CDL, `UNSUPPORTED_FORMAT`, `FRAMES_RX`) — a testbench/C++ ABI sensitivity, not a known RTL fault. **Open.** |
  | 5.050 | Arch, and the CI pin | reference: **55/55 suites green, 2 064 050 checks, 0 failures** (full sweep 2026-07-26) |

  CI therefore **builds Verilator from source at a pinned tag** (`VERILATOR_VERSION`
  in the workflow) and caches it, rather than trusting `apt`. The RTL was
  deliberately NOT contorted to satisfy 5.020: the construct it rejects is legal
  and synthesises, so the cost belongs on the toolchain pin, not the design.
  If you are on a distro Verilator and a datapath harness will not build, this
  is why.
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
