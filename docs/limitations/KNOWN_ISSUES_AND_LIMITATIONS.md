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
BRAM PCM-ring option, or ALSA record). §1.1 and the 2026-07-26 rows in §4 are
newer than that reconciliation._

---

## 1. Scope limitations (by design, current state)

| Limitation | Detail |
|---|---|
| **Single endpoint port** | One MAC/PHY today; the 4-port AVB switch is direction, not implementation ([../overview/AVB_SWITCH_DIRECTION.md](../overview/AVB_SWITCH_DIRECTION.md)) |
| **MTU fixed at 1500** | A deliberate decision of the switch direction doc; no jumbo support |
| **802.1 standards gaps** | The normative gap analysis (~60 items: SRP/MSRP, full gPTP stack, MVRP, …) is [`REQUIREMENTS.md`](../../REQUIREMENTS.md) §3 - read it before claiming Milan conformance. [../reference/MILAN_V12_DEPENDENCY_MATRIX.md](../reference/MILAN_V12_DEPENDENCY_MATRIX.md) traces what is covered |
| **MDIO not fabric-driven — `MAC_STATUS` is SOFTWARE-published** | There is no hardware MDIO master anywhere in the design. LiteEth's `LiteEthPHYGMII`/`LiteEthPHYMII` expose **no** link, speed or duplex output — only `LiteEthPHYMDIO`, a software bit-bang register pair at the DT `phy` window (`0xf000_3800`, 0xc bytes). Since 2026-07-26 `milan_soc.py` no longer hardwires `i_link_up`/`i_full_duplex`/`i_mac_speed`: they come from the `milan_mac_link_status` CSR (`0xf000_381c`, fields `link_up[0] speed[2:1] full_duplex[3]`, reset = the old per-board constants), so software that reads the PHY over MDIO can publish the truth into `MAC_STATUS` 0x110 and into `o_mac_is_1g` (REQ-MAC-03). **Until the driver writes it, the register still reports its reset default** — that half needs `kl-eth` phylib work, and a fabric MDIO poller (new SystemVerilog) would be needed to make it hardware-driven | 
| **Open CBS requirements** | REQ-CBS-05/06/07 (credit-skew/pacing refinements) are open in [`REQUIREMENTS.md`](../../REQUIREMENTS.md) |
| **Latent CBS slope truncation** | The CBS slope divide truncates: zero error only while configured slopes divide evenly (today's do). Documented in the CBS math section of [`REQUIREMENTS.md`](../../REQUIREMENTS.md) - re-check before exotic `tc cbs` configs |

### 1.1 Silicon blockers

| Blocker | State | Evidence / next step |
|---|---|---|
| **Fabric listener never accepts on the 8×8 AX gateware** | **CLOSED 2026-07-26** — root-caused, fixed in RTL (`VERSION 0x0001_000F`, and in every build since), mechanism confirmed on silicon | The cause was **entry-0 provisioning, not the parser and not a placement artifact**: `win_commit_glue` staged the `0x800` window's `SID_LO`/`SID_HI` in one global register pair shared by every index, so a route-flags-only `CTRL` write at index 0 armed entry 0 with another index's sid; `KL_stream_table` then set `ovr_armed_r[idx]` on any write and cleared it only on reset, so entry 0 never returned to the ACMP alias. The fix tags staging with the index it was staged for and makes `{en=0, sid=0}` a **release-to-alias**. Confirmed on silicon by **causation** — the trap was triggered on purpose and the listener went deaf, then recovered by re-staging ([findings/STRESS_0726.md](../findings/STRESS_0726.md) §D, tests D0/D1/D2). Regression guards: `tb/verilator/milan_dp` `sim_nxn.cpp` TRAP-1 (N=4 and N=8) and `tb/verilator/avtp_parser` `sim_tbl.cpp` T6, both with negative legs. Full walk: [TROUBLESHOOTING §21](TROUBLESHOOTING.md) |

> The silicon confirmation was obtained on a board still carrying the **pre-fix**
> `VERSION 0x0001_000B` — it proves the *mechanism*, and the *fix* is proven in
> simulation by the two regression guards above. A board that has not been
> reflashed past `0x000F` still needs the workaround (stage the sid at index 0
> before committing `CTRL`).

## 2. Build & reproducibility gaps

| Gap | Impact | Workaround |
|---|---|---|
| **CI runs everything except hardware** (2026-07-26) | GitHub Actions runs the paper gates in [`docs.yml`](../../.github/workflows/docs.yml) (docs gate — links, wording, dead references, local info — twice, the second time with `.git` deleted; the traceability no-drift gate; the end-station builder gates) **and the RTL gates** in [`rtl.yml`](../../.github/workflows/rtl.yml): the full Verilator sweep via `scripts/run_all_suites.sh`, the Yosys portability sweep, and the BDD conformance suite. **Nothing on hardware runs automatically** — silicon regressions are still caught by discipline | run the [TESTING.md](../testing/TESTING.md) layers before pushing; [`../../QUICKSTART.md`](../../QUICKSTART.md) §2 has the exact local commands |
| **No version pins** | No requirements.txt / lockfile; `sw/litex/patches` are diffed against LiteX `master` and can stop applying | known-good LiteX: `a1e1c36` (recorded in `sw/litex/evidence/hw_naxriscv_reads_MILN.log`); re-diff per `patches/README.md` |
| **CPU default ≠ published config** | `milan_soc.py --cpu` defaults to `naxriscv` and `deploy.sh` does not override it, while the **shipped config is 1-hart VexiiRiscv** (`--cpu vexiiriscv` + `--l2-bytes 32768`). (The dual-hart `--cpu-count 2` scoreboard was a superseded perf-lineage variant.) | see [../litex/LITEX_SOC.md](../litex/LITEX_SOC.md) §2.5 |
| **`--coherent-dma` not implied by `--all-blocks`** | Omitting it builds a NIC that silently drops all RX and TXes garbage (DMA bypasses the snooping bus) | always pass it (deploy.sh does); hardware-confirmed 2026-07-04 |
| **`external` submodule is SSH-only** | anonymous `git clone --recurse-submodules` fails on it | it is **not needed** - init only `third_party/verilog-axis` |
| **Driver out of tree** | the `kl-eth` Linux driver lives in the sibling repo `kl-linux-drivers`; no kernel-version pin is documented | contract in [`sw/driver/README.md`](../../sw/driver/README.md) |
| **DT `phy-mode` `rgmii-id` in `sw/dts` — RESOLVED by retirement (2026-07-26)** | `sw/dts/boards/ax7101.json` + `milan-nic.litex.dtsi` carry `rgmii-id` on a GMII-wired board ([BOARD_PORTING_AX7101 §3](../integration/BOARD_PORTING_AX7101.md)). Those files are now **historical artifacts**: the shipping node comes from `sw/builder/endstation_builder.py`, which emits `phy-mode = "gmii"` / `"mii"` from the config and byte-matches both deployed `.dts` files | nothing to do; do not deploy `sw/dts/milan-nic.*.dtsi` |
| **`build.sh cfg_ax8x8` L2 ≠ the 8x8 config's L2** | the FLASHED ax8x8 gateware was built with `--l2-bytes 16384` (`build_ax8x8_rxq1fix_eppo.log` line 1: `l2_bytes=16384`) because the 8-stream shape did not close at 32K, but `configs/endstation_ax7101_8x8.yaml` still declares `l2_bytes: 32768` — and `test_builder.py` gate 9 pins `sweep.sh`'s L2 to that config, so `sweep.sh ax7101` now builds an 8x8 at 32K, a combination **never placed and routed** | the divergence is PINNED and re-verified by `scripts/check_sweep_shape.py` (it fails if either side moves). Real fix: change `l2_bytes` in the config to 16384 (configs/ is the declarative source), then regenerate the sweep fragment |
| ~~**`avtp_stream_parser` portability unchecked**~~ | **CLOSED** — it is a top in `syn/yosys/run.sh` `tops=()` and is swept on every portability run | nothing to do |

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
| BD-256 ring depth without the hsq6 drain gate | RX wedge under overload | use hsq6+ gateware ([../findings/RX_OVERLOAD_WEDGE.md](../../historical_now_obsolete/findings/RX_OVERLOAD_WEDGE.md) history) |
| **RX-queue count differs PER BOARD** (2026-07-26) | the queue count sets the DMA window map: the shipping ax7101 gateware is **1 queue** (no `rx1_*`/steer registers in its `csr.csv`), the deployed arty is **2**. Building either with the other's count shifts every DMA window under an unchanged DTB — the CSR-rot failure of [TROUBLESHOOTING §20](TROUBLESHOOTING.md), silent until the host plane is dead | `rx_queues` lives in each board's `configs/endstation_*.yaml` and flows into `sweep.sh` as `RXQ`; builder gate 9 asserts config ⇄ sweep agreement per board. Change it only together with a full boot-chain rebuild for that board |
| **Extra talker (`t > 0`) armed while the lwSRP engine is OFF** (2026-07-26) | the admitted stream transmits **unpaced** — the reservation bandwidth gate *is* the pacer. Measured ~56 k frames/s from one context; the peer board's 50 MHz core drowns in the interrupt storm and stops answering the network until the talker is disarmed | never leave `LWSRP_CTRL[0] = 0` with an armed `t > 0` context; arm extras only with the engine running ([TROUBLESHOOTING §22](TROUBLESHOOTING.md)) |
| **`t > 0` context (`TCTX`) window writes while the engine is OFF** (2026-07-26) | writes are **silently dropped** (provisioning-commit coupling holds `wr_rdy` low) — the arm looks done and is not | arm/disarm `t > 0` with the engine ON, and take the arm truth from a snapped `A_STRMW_STATE 0x82C[3]` (composed admission), never from the write itself |

STRICT-pairing rules and the current compatibility ledger:
[../findings/RX_PERF_TUNING_MAP.md](../findings/RX_PERF_TUNING_MAP.md) and
[../findings/BENCH_TOPOLOGY.md](../findings/BENCH_TOPOLOGY.md) (which gateware/rootfs
pair is on which board).

## 5. Refuted performance levers (measured; do not rebuild without new evidence)

Each was implemented or modeled, **measured on silicon**, and rejected -
the write-ups explain why, so the next person doesn't re-spend the effort:

| Lever | Verdict | Where |
|---|---|---|
| TX reader prefetch | "MEASURED VERDICT: do not build it" | [../findings/TX_READER_PREFETCH_PLAN.md](../../historical_now_obsolete/findings/TX_READER_PREFETCH_PLAN.md) |
| Second core for single-flow throughput | single flow is latency-bound, not CPU-bound; SMP helps multi-flow TX instead | [../findings/LATENCY_INVESTIGATION.md](../findings/LATENCY_INVESTIGATION.md) §2.1 |
| Interrupt-coalescing sweeps for single-flow RX | `rx-usecs` 5 µs→1 ms flat | [../findings/LATENCY_INVESTIGATION.md](../findings/LATENCY_INVESTIGATION.md) §2/§2.1 |
| 112.5 MHz sys clock | built + measured, reverted (reset fanout) | [../findings/LATENCY_INVESTIGATION.md](../findings/LATENCY_INVESTIGATION.md) |
| L2 > 64 KB, BRAM scratchpad, software prefetch (blocking D$) | no measured gain on this core | campaign ledger: [`CHANGELOG.md`](../../CHANGELOG.md), [../findings/PERFORMANCE_GOAL.md](../findings/PERFORMANCE_GOAL.md) |
| Socket zero-copy RX (TCP_ZEROCOPY_RECEIVE) on this core+kernel | 110-113 Mbit at 87 % zero-copied - equilibrium economics refute the lane; AF_XDP ZC remains the open >500 lane | [../findings/PERFORMANCE_GOAL.md](../findings/PERFORMANCE_GOAL.md), [../findings/RX_PERF_TUNING_MAP.md](../findings/RX_PERF_TUNING_MAP.md) |

## 6. Performance: where the numbers actually live

Historical docs quote different RX/TX figures because each is a **dated
measurement** of a moving system (and several older docs carry superseded
banners). The rules:

* The per-lever measured ledger is [`CHANGELOG.md`](../../CHANGELOG.md).
* The consolidated campaign record is [../findings/PERFORMANCE_GOAL.md](../findings/PERFORMANCE_GOAL.md)
  (it carries the no-copy RX ceiling re-baseline); the newest *board* state — which
  gateware and rootfs each board is actually running — is
  [../findings/BENCH_TOPOLOGY.md](../findings/BENCH_TOPOLOGY.md).
* Any number embedded elsewhere (including the root README) is a snapshot
  with a date - trust the ledger over prose.

## 7. Legacy collateral that can mislead

* `tb/utests/`, `tb/itests/` - Vivado-xsim era, partly stale interfaces
  ([../testing/TESTING.md](../testing/TESTING.md) §5).
* `sw/litex/milan_rgmii.py` - unused legacy RGMII PHY experiment; the board
  is GMII.
* `milan_top.sv` + `bd/` + `constraints/*.xdc` - the Zynq-7020 variant,
  maintained but not the primary target; [`REQUIREMENTS.md`](../../REQUIREMENTS.md)/[`TODO.md`](../../TODO.md) still
  describe some Zynq-era mechanics (`0x43C0_0000`, IRQ_F2P) that only apply
  there.
* [`docs/design/AEM_AND_AECP.md`](../design/AEM_AND_AECP.md) - the AEM/AECP design record, reconciled to
  the as-built fabric subsystem (2026-07-25).
