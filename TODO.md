# TODO — TSN on FPGA

Work items to satisfy [`REQUIREMENTS.md`](REQUIREMENTS.md). Ordered by dependency:
the **memory-mapped CSR plane (Phase 1)** is the critical path — it unblocks PTP,
CBS, classifier, MAC config, the Linux driver, and the device tree.

Legend: `[ ]` todo · `[~]` in progress · `[x]` done · `(REQ-xxx)` requirement ·
**B**=blocker **H**=high **M**=medium **L**=low.

---

## Progress — 2026-07-01 (Verilator-verified, no Xilinx tools required)

Implemented and unit-tested this session (all harnesses green in
[`tb/verilator/`](tb/verilator)):

* **CSR plane** (`hdl/csr/milan_csr.sv`) — AXI4-Lite control plane, 44 checks.
* **CBS runtime config** (`credit_based_shaper` + `traffic_shaping_core`) —
  per-queue idleSlope/hi/lo/enable from CSR, strict-priority bypass, back-pressure
  accrual, hiCredit down-clamp on reconfig. CBS math (87 k) + arbiter (61 k).
* **802.1Q classification** (`traffic_class_map` + `traffic_classifier`) —
  PCP→regen→TC→queue tables, untagged default priority, legacy fallback (200 k).
* **PTP hardware clock** (`timestamp_counter` + `ptp_csr_sync`) — adjfine/adjtime/
  settime/gettime phase accumulator + CSR↔PHC CDC (201 k).
* **Integration** — `milan_top` wires `milan_csr` to MAC cfg, classifier, CBS,
  PTP, RMON stats + IRQ; `ethernet_events` packed readback + rollover; `bd/
  milan-dma.tcl` + `milan_dma_wrapper.v` expose the CSR master + IRQ (needs a
  Vivado BD regen to finalise — unavailable this session).

Remaining (need a kernel tree / Vivado / hardware): Linux driver (Phase 7),
device tree (Phase 8), multi-channel DMA (Phase 6), block-design regeneration,
and end-to-end bring-up (Phase 9).

## Progress — 2026-07-02 (fully-FPGA softcore solution — open toolchain)

The design was ported off the Zynq PS to a **NaxRiscv RV64GC + LiteX** SoC and the
full-FPGA solution is **assembled and elaborating** end-to-end. See
[`docs/FULL_FPGA_SOLUTION.md`](docs/overview/FULL_FPGA_SOLUTION.md) (master guide) and
[`docs/PROTOCOL_VALIDATION_MATRIX.md`](docs/testing/PROTOCOL_VALIDATION_MATRIX.md) (protocol×test).

* **De-Xilinx complete** — all XPM/vendor IP replaced by Forencich `verilog-axis`
  + open CDC/TCAM; 15 Verilator harnesses + 18 Yosys tops (incl. Lattice ECP5).
* **`milan_datapath.sv`** — PS-less §A.9 wrapper; verified `tb/verilator/milan_dp`.
* **Softcore** — NaxRiscv boots the LiteX BIOS in sim; the CPU reads the NIC
  `ID="MILN"` over the bus (**M-A2**) — `sw/litex/milan_sim.py`, evidence saved.
* **`milan_soc.py --full`** — the whole FPGA SoC (NIC + §A.6 DMA + §A.7 MAC/RGMII
  PHY) elaborates and exports gateware; only the Artix-7 Vivado bitstream is blocked
  (device-support install).
* Device tree (`sw/dts/`), driver ABI (`sw/driver/`), and the DMA CSR ABI documented.

Remaining for on-hardware bring-up (roadmap in FULL_FPGA_SOLUTION.md §9): Artix-7
Vivado device install → LiteDRAM → board M-A2/M-A3 → Linux (M-A4) → driver (M-A5) →
AVDECC SW protocols (AECP/ACMP/MAAP/MVU, then SRP/MSRP/MVRP, then AVTP media).

---

## Phase 0 — Verification & docs (start here; partly done)

- [x] **B — Runnable CBS verification harness** `(REQ-VER-01)`
  `tb/verilator/cbs/` — three-way check (RTL DUT vs cycle-accurate fixed-point
  replica vs ideal 802.1Qav model), directed scenarios + 50 k randomized cycles,
  `make` → PASS with CI exit code. Supersedes the stale
  `tb/utests/802_1q_traffic_shaper/tb_credit_based_shaper.sv`.
- [x] **B — Requirements & gap analysis** `(REQUIREMENTS.md §3–§4)` — done.
- [x] **B — This task list** — done.
- [x] **B — Register-map ABI doc** `docs/REGISTER_MAP.md` `(REQ-CSR-05)` — the
  contract shared by HDL + driver + DT. Done.
- [x] **B — Developer documentation** — `docs/ARCHITECTURE.md` (system map +
  maintainability guide), `docs/README.md` (doc index), `hdl/csr/doc/milan_csr.md`
  (TerosHDL module page), `tb/verilator/README.md`; all RTL annotated in TerosHDL
  `//!` syntax with named processes.
- [x] **H — Delete/replace stale CBS TB** — remove or `git mv` the old
  `tb_credit_based_shaper.sv` once the Verilator harness is the reference.

## Phase 1 — Memory-mapped CSR plane (critical path) `(REQ-CSR-*)`

- [x] **B — AXI4-Lite CSR RTL** `hdl/csr/milan_csr.sv` `(REQ-CSR-01)` — 32-bit,
  64 KB window, combinational-ready single-outstanding AXI4-Lite slave; register
  groups for PTP / CBS / classifier / MAC / stats / IRQ per the ABI; lint-clean.
- [x] **B — ID / VERSION / CAPABILITIES regs** `(REQ-CSR-02)` — CAPABILITIES
  encodes `NUMBER_OF_QUEUES` + feature bits (done, verified).
- [x] **H — IRQ_STATUS (W1C) / IRQ_MASK + PS IRQ line** `(REQ-CSR-04)` — aggregate
  TX-ts-ready, link-change, RMON-rollover; command strobes + stats/TOD snapshot.
- [x] **H — CSR/register-map TB** `(REQ-VER-04)` — `tb/verilator/csr` (44 checks
  PASS): reset values, RO/RW/W1C, output wiring, strobes, snapshot.
- [x] **B — CDC for gtx_clk/axis_clk fields** `(REQ-CSR-03)` — the CSR emits
  value + apply-strobe already; add the 2-FF/handshake synchronizers at the
  `gtx_clk` consumers (PTP counter, TX side) when wiring Phase 2.
- [~] **B — Block-design integration** `bd/milan-dma.tcl` — add a 3rd `axi_smc`
  master, connect `milan_csr` S_AXI_LITE, `assign_bd_address 0x43C0_0000/64K`,
  widen `IRQ_F2P`/`ilconcat`; wire `milan_csr` into `hdl/common/milan_top.sv`
  (needs Vivado; RTL + ABI are ready).

## Phase 2 — PTP hardware clock (PHC) `(REQ-PTP-*)`

- [x] **B — Register-controlled accumulator** `hdl/ptp_timestamp/timestamp_counter.sv`
  `(REQ-PTP-01)` — replace fixed `+STEP_SIZE` with `+ (nominal_incr + adj)` using a
  fractional-ns phase accumulator; SW-writable addend (adjfine).
- [x] **B — adjtime / settime** `(REQ-PTP-02)` — `load_value`+`load_valid` and
  signed `step_delta`+`step_valid`, applied atomically in the counter clock domain.
- [x] **B — gettime snapshot** `(REQ-PTP-03)` — read-strobe latches 64-bit TOD
  (pair with ARM global timer for `gettimex64`).
- [~] **B — TX-timestamp IRQ + unambiguous key** `(REQ-PTP-04)` — add
  messageType (+ HW cookie) to `ts_metadata` (`hdl/common/ethernet_packet_pkg.sv`);
  raise IRQ on TX ts available.
- [ ] **M — Event-only timestamping** `(REQ-PTP-05)` — parse `messageType[3:0]`
  (+domain) in `ptp_ts_core.sv`; only assert `ptp_pending` for event messages.
- [ ] **M — Ingress/egress latency correction regs + SFD capture** `(REQ-PTP-06)`.
- [ ] **M — PHC clock source** `(REQ-PTP-07)` — clock counter from fixed 125 MHz
  (not speed-switched `gtx_clk`) or tie increment to link-speed/adjfine.
- [ ] **M — VLAN-tagged gPTP offsets** `(REQ-PTP-09)` — shift PTP field offsets by
  the C-TAG width when 0x8100 present.
- [ ] **L — 1PPS / extts / perout** `(REQ-PTP-08)`.

## Phase 3 — 802.1Qav CBS fixes + runtime config `(REQ-CBS-*)`

- [x] **B — Runtime idleSlope/hiCredit/loCredit + per-queue enable** `(REQ-CBS-01)`
  — convert `credit_based_shaper.sv` params to CSR-driven input ports; recompute
  slope-per-cycle/per-byte in HW (or accept precomputed Q-format from driver).
- [x] **H — Exclude non-SR classes from CBS** `(REQ-CBS-02)` — per-queue "shaped"
  bit; force `allow_transmit=1` for strict-priority classes in
  `traffic_shaping_core.sv`.
- [x] **H — deltaBandwidth ≤ 75 % default** `(REQ-CBS-03)` — fix
  `ethernet_packet_pkg.sv` idleSlope defaults; driver rejects over-subscription.
- [x] **M — Accrue credit during grant-with-backpressure** `(REQ-CBS-04)` — replace
  the "hold" branch (`credit_based_shaper.sv:133-135`) with idle accrual.
- [ ] **M — Remove credit/transmit pipeline skew** `(REQ-CBS-05)` — collapse double
  registration; non-stale `allow_transmit` to arbitration.
- [ ] **M — Round slope fixed-point / widen fraction** `(REQ-CBS-06)` — matters once
  idleSlope is runtime; harness measures the residual error.
- [ ] **M — Pace egress to line rate** `(REQ-CBS-07)` — ensure `bytes_sent`/
  `is_transmitting` reflect real occupancy; assert/doc upstream pacing.
- [x] **H — Multi-queue arbitration harness** `(REQ-VER-02)` — approach already
  proven (flat wrapper + XMR into `gen_cbs[*].u_cbs.credit` lints clean).

## Phase 4 — 802.1Q classification `(REQ-CLS-*)`

- [x] **B — PCP-driven classification** `(REQ-CLS-01)` — slice `PCP=vlan_tci[15:13]`,
  `DEI=vlan_tci[12]`; index a programmable priority-regeneration + PCP→TC table
  instead of the EtherType `case` in `traffic_classifier.sv:124-141`.
- [x] **B — Programmable PCP→TC / TC→queue tables via CSR** `(REQ-CLS-02, CLS-04)`.
- [x] **H — Configurable default port priority for untagged** `(REQ-CLS-03)`.
- [ ] **M — DEI sideband** `(REQ-CLS-05)`.
- [ ] **M — Back-to-back line-rate parsing** `(REQ-CLS-06)` — re-arm header FSM on
  `tlast` same-cycle.
- [ ] **M — Reserved DMAC validation** `(REQ-CLS-07)`.
- [ ] **L — S-TAG / 802.1ad** `(REQ-CLS-08)` · **L — 802.1Qci PSFP** `(REQ-CLS-09)`.
- [x] **H — Classifier harness** `(REQ-VER-03)`.

## Phase 5 — 802.3 MAC configuration & management `(REQ-MAC-*)`

- [x] **B — Drive MAC cfg from CSR** `(REQ-MAC-01)` — `cfg_ifg/tx_en/rx_en/is_1g/
  stats_reset` from registers (default to current constants at reset);
  `hdl/common/milan_top.sv:151,206,256-258`.
- [ ] **H — RX address filter** `(REQ-MAC-02)` — exact-match unicast + multicast
  hash/CAM + promisc/allmulti on the RX AXIS path.
- [ ] **H — Speed/duplex from PHY + link status** `(REQ-MAC-03)` — use MAC `speed[]`;
  drive `is_1g`; expose link-status bit + IRQ.
- [x] **H — Stats readback + snapshot + reset** `(REQ-MAC-04)` — map
  `ethernet_events` counters into CSR; replace `// TODO Add VIO`.
- [ ] **M — MAC/link/error IRQ** `(REQ-MAC-05)` · **M — PHY reset GPIO**
  `(REQ-MAC-06)` · **M — MDIO reachable by driver** `(REQ-MAC-08)`.
- [ ] **L — PAUSE / MTU** `(REQ-MAC-07)`.

## Phase 6 — Multi-channel DMA (enables N queues)

- [ ] **B — Replace single `axi_dma` with `axi_mcdma`** `bd/milan-dma.tcl` — real
  per-queue TX/RX channels for CBS/mqprio; enable Scatter-Gather (`c_include_sg=1`)
  for descriptor rings/coalescing. (Or document a single-queue reduction.)

## Phase 7 — Linux driver `(REQ-DRV-*)` (`../kl-linux-drivers`)

- [ ] **B — Rewrite `kl-eth.c` into a compiling platform driver** `(REQ-DRV-01)` +
  fix `Makefile` `obj-m`.
- [ ] **B — Datapath: open/stop/xmit, DMA ring, NAPI, IRQ** `(REQ-DRV-02)`.
- [ ] **B — Multi-queue netdev mapped to HW queues** `(REQ-DRV-03)`.
- [ ] **B — PHC (`ptp_clock_info`)** against CSR PTP regs `(REQ-DRV-04)`.
- [ ] **B — HW timestamping (`SIOCSHWTSTAMP`, ts-metadata consumer, skb_*)**
  `(REQ-DRV-05)`.
- [ ] **B — CBS offload (`ndo_setup_tc` CBS/mqprio, opt taprio)** `(REQ-DRV-06)`.
- [ ] **H — MDIO bus + phylib + `adjust_link`** `(REQ-DRV-07)`.
- [ ] **H — ethtool_ops (`get_ts_info`, `-S`, coalesce)** `(REQ-DRV-08)`.

## Phase 8 — Device tree & generator `(REQ-DT-*)` (`../fpga-ps-tools`)

- [ ] **B — DT binding yaml + board `.dtsi` node** `(REQ-DT-01)` — compatible, reg
  (CSR+DMA), interrupts, `kl,txq/rxq-cnt`, `phy-handle`+mdio subnode,
  `local-mac-address`, clocks.
- [ ] **B — Wire Xilinx `device-tree-xlnx` (dtg) into `fpga-ps-tools`** `(REQ-DT-02)`
  — submodule init; `xsct`/`hsi` from `.xsa`/`.hwh` → `pl.dtsi`; overlay the
  `kl,dma-ether` node.
- [ ] **S — Emit CBS/PHC props consistent with the CSR ABI** `(REQ-DT-03)`.

## Phase 9 — End-to-end bring-up `(REQ-VER-05)`

- [ ] `ethtool -T` advertises PHC · `ptp4l`/`phc2sys` lock · `tc qdisc … cbs
  offload 1` shapes SR while BE uses the remainder · `ethtool -S` counters · CBS +
  CSR harnesses green in CI.

---

### Dependency summary

```
Phase 0 (docs+CBS harness ✓, REGISTER_MAP ABI)
        │
        ▼
Phase 1  CSR plane ──────────────┬─────────────┬──────────────┬────────────┐
        │                        │             │              │            │
        ▼                        ▼             ▼              ▼            │
Phase 2 PTP/PHC   Phase 3 CBS cfg  Phase 4 CLS   Phase 5 MAC   Phase 6 mcDMA
        └────────────┬───────────┴──────┬───────┴──────┬───────┘            │
                     ▼                  ▼              ▼                     │
                  Phase 7 Linux driver (PHC, hwtstamp, tc-CBS, mqprio) ◄─────┘
                     │
                     ▼
                  Phase 8 Device tree + dtg ──► Phase 9 end-to-end bring-up
```
