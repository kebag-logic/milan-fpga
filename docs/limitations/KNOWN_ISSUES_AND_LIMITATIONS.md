# Known issues & limitations

The single page that makes every error, limitation and hazard apparent.
Three kinds of entries, kept separate: **open limitations** (things that do
not work or do not exist yet), **operational hazards** (things that work but
bite you if mispaired), and **refuted approaches** (things measured and
proven not to help - do not re-try without new evidence). Fixed bugs are not
listed here; their post-mortems live in the [findings log](../findings/README.md)
(§5) and field-level symptom→fix recipes in [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

_Last reconciled against the tree: 2026-07-23 (note: this page does not yet fully
reflect the −83.9 dB media-clock servo, the AX42 e2 MAC-TX logic fix, the on-chip
BRAM PCM-ring option, or ALSA record)._

---

## 1. Scope limitations (by design, current state)

| Limitation | Detail |
|---|---|
| **Single endpoint port** | One MAC/PHY today; the 4-port AVB switch is direction, not implementation ([../overview/AVB_SWITCH_DIRECTION.md](../overview/AVB_SWITCH_DIRECTION.md)) |
| **MTU fixed at 1500** | A deliberate decision of the switch direction doc; no jumbo support |
| **802.1 standards gaps** | The normative gap analysis (~60 items: SRP/MSRP, full gPTP stack, MVRP, …) is [`REQUIREMENTS.md`](../../REQUIREMENTS.md) §3 - read it before claiming Milan conformance. [../reference/MILAN_V12_DEPENDENCY_MATRIX.md](../reference/MILAN_V12_DEPENDENCY_MATRIX.md) traces what is covered |
| **MDIO not yet fabric-driven** | `MAC_STATUS` fields are partly hardcoded until the MDIO master lands (see `sw/litex/evidence/hw_ma3_dma_datapath_100mhz.md`); `i_mac_speed` etc. tied to constants on the LiteX build |
| **Open CBS requirements** | REQ-CBS-05/06/07 (credit-skew/pacing refinements) are open in [`REQUIREMENTS.md`](../../REQUIREMENTS.md) |
| **Latent CBS slope truncation** | The CBS slope divide truncates: zero error only while configured slopes divide evenly (today's do). Documented in the CBS math section of [`REQUIREMENTS.md`](../../REQUIREMENTS.md) - re-check before exotic `tc cbs` configs |

## 2. Build & reproducibility gaps

| Gap | Impact | Workaround |
|---|---|---|
| **No CI** | Nothing runs the (CI-ready) suites automatically; regressions are caught by discipline | run the [TESTING.md](../testing/TESTING.md) layers 1/2/4 before pushing |
| **No version pins** | No requirements.txt / lockfile; `sw/litex/patches` are diffed against LiteX `master` and can stop applying | known-good LiteX: `a1e1c36` (recorded in `sw/litex/evidence/hw_naxriscv_reads_MILN.log`); re-diff per `patches/README.md` |
| **CPU default ≠ published config** | `milan_soc.py --cpu` defaults to `naxriscv` and `deploy.sh` does not override it, while the **shipped config is 1-hart VexiiRiscv** (`--cpu vexiiriscv` + `--l2-bytes 32768`). (The dual-hart `--cpu-count 2` scoreboard was a superseded perf-lineage variant.) | see [../litex/LITEX_SOC.md](../litex/LITEX_SOC.md) §2.5 |
| **`--coherent-dma` not implied by `--all-blocks`** | Omitting it builds a NIC that silently drops all RX and TXes garbage (DMA bypasses the snooping bus) | always pass it (deploy.sh does); hardware-confirmed 2026-07-04 |
| **`external` submodule is SSH-only** | anonymous `git clone --recurse-submodules` fails on it | it is **not needed** - init only `third_party/verilog-axis` |
| **Driver out of tree** | the `kl-eth` Linux driver lives in the sibling repo `kl-linux-drivers`; no kernel-version pin is documented | contract in [`sw/driver/README.md`](../../sw/driver/README.md) |
| **DT `phy-mode` says `rgmii-id`, board is GMII-wired** | `sw/dts/boards/ax7101.json` + the generated `milan-nic.litex.dtsi` carry `rgmii-id`; the AX7101 e1 port is GMII ([BOARD_PORTING_AX7101 §3](../integration/BOARD_PORTING_AX7101.md)) | code fix pending; harmless only as long as the driver ignores phy-mode for this PHY setup |
| **`avtp_stream_parser` portability unchecked** | has a Verilator suite but no `syn/yosys` top | add it to `run.sh` `tops=()` |

## 3. Timing & clocking constraints

* **The CBS slope divide is the 100 MHz critical path.** The build only
  closes with the multicycle constraint that `add_milan_datapath()` emits
  (or with the datapath in its own slower domain, `--milan-clk-freq 50e6`,
  which is what `deploy.sh` ships). Porting to another toolchain? Re-express
  it: [../integration/PORTING_GUIDE.md](../integration/PORTING_GUIDE.md) §4.5.
* **112.5 MHz sys was built, measured, and reverted** - reset-fanout timing
  (`sys_rst` replication proved impossible - DONT_TOUCH); see
  [../findings/LATENCY_INVESTIGATION.md](../findings/LATENCY_INVESTIGATION.md).
  DDR3 pins sys at 100 MHz.
* **`--gtx-tx-invert` is required on the AX7101** - edge-aligned GMII TX
  launch is hold-marginal at the RTL8211E (25-40 % corrupt frames without
  it). Other boards must re-evaluate TX clock phase.

## 4. Operational hazards - lethal pairings (gateware ⇄ driver)

The header-split / BD-format features couple gateware and driver builds.
These pairings are **known-fatal**:

| Pairing | Consequence | Guard |
|---|---|---|
| driver `--hs-page-bytes` ≠ gateware `hs_page_bytes` | **kernel panic** (Bad page map class) | `milan_dma_hs_pgsz_cap` reads back the elaborated size (`0xf000311c` in the reference build — LiteX assigns CSR offsets at build time, so confirm against your build's `csr.csv`); the hsplit16 driver **refuses to load** on mismatch. Reads 0 on older gateware = warn-and-trust |
| hsplit10+ driver on ≤hsq5 gateware | **silent ring lap** (by construction, no error) | never load it there - see [../findings/RX_PERF_TUNING_MAP.md](../findings/RX_PERF_TUNING_MAP.md) |
| BD-256 ring depth without the hsq6 drain gate | RX wedge under overload | use hsq6+ gateware ([../findings/RX_OVERLOAD_WEDGE.md](../findings/RX_OVERLOAD_WEDGE.md) history) |

STRICT-pairing rules and the current compatibility ledger:
[../findings/RX_PERF_TUNING_MAP.md](../findings/RX_PERF_TUNING_MAP.md) and
[../findings/SESSION_HANDOFF.md](../findings/SESSION_HANDOFF.md).

## 5. Refuted performance levers (measured; do not rebuild without new evidence)

Each was implemented or modeled, **measured on silicon**, and rejected -
the write-ups explain why, so the next person doesn't re-spend the effort:

| Lever | Verdict | Where |
|---|---|---|
| TX reader prefetch | "MEASURED VERDICT: do not build it" | [../findings/TX_READER_PREFETCH_PLAN.md](../findings/TX_READER_PREFETCH_PLAN.md) |
| Second core for single-flow throughput | single flow is latency-bound, not CPU-bound; SMP helps multi-flow TX instead | [../findings/SINGLE_PORT_PERF.md](../findings/SINGLE_PORT_PERF.md), [../findings/LATENCY_INVESTIGATION.md](../findings/LATENCY_INVESTIGATION.md) |
| Interrupt-coalescing sweeps for single-flow RX | `rx-usecs` 5 µs→1 ms flat | [../findings/SINGLE_PORT_PERF.md](../findings/SINGLE_PORT_PERF.md) |
| 112.5 MHz sys clock | built + measured, reverted (reset fanout) | [../findings/LATENCY_INVESTIGATION.md](../findings/LATENCY_INVESTIGATION.md) |
| L2 > 64 KB, BRAM scratchpad, software prefetch (blocking D$) | no measured gain on this core | campaign ledger: [`CHANGELOG.md`](../../CHANGELOG.md), [../findings/PERFORMANCE_GOAL.md](../findings/PERFORMANCE_GOAL.md) |
| Socket zero-copy RX (TCP_ZEROCOPY_RECEIVE) on this core+kernel | 110-113 Mbit at 87 % zero-copied - equilibrium economics refute the lane; AF_XDP ZC remains the open >500 lane | [../findings/SESSION_HANDOFF.md](../findings/SESSION_HANDOFF.md), [../findings/RX_PERF_TUNING_MAP.md](../findings/RX_PERF_TUNING_MAP.md) |

## 6. Performance: where the numbers actually live

Historical docs quote different RX/TX figures because each is a **dated
measurement** of a moving system (and several older docs carry superseded
banners). The rules:

* The per-lever measured ledger is [`CHANGELOG.md`](../../CHANGELOG.md).
* The narrative current-state is [../findings/RX_TX_PERFORMANCE.md](../findings/RX_TX_PERFORMANCE.md),
  with the newest working state in [../findings/SESSION_HANDOFF.md](../findings/SESSION_HANDOFF.md)
  (which re-baselined the no-copy RX ceiling measurement).
* Any number embedded elsewhere (including the root README) is a snapshot
  with a date - trust the ledger over prose.

## 7. Legacy collateral that can mislead

* `tb/utests/`, `tb/itests/` - Vivado-xsim era, partly stale interfaces
  ([../testing/TESTING.md](../testing/TESTING.md) §5).
* `sw/litex/milan_rgmii.py` - unused legacy RGMII PHY experiment; the board
  is GMII.
* `milan_top.sv` + `bd/` + `constraints/*.xdc` - the Zynq-7020 variant,
  maintained but not the primary target; `REQUIREMENTS.md`/`TODO.md` still
  describe some Zynq-era mechanics (`0x43C0_0000`, IRQ_F2P) that only apply
  there.
* `aem-and-aecp.md` (root) - design notes for AEM/AECP prior work, not
  implemented RTL.
