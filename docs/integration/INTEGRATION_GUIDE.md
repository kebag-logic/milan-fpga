# Integration guide - wiring `milan_datapath` into your SoC

`hdl/common/milan_datapath.sv` is the single clean integration boundary of
this project: the whole Milan TSN datapath (classify + 802.1Qav CBS, PTP
clock + timestamping, TCAM RX filter, ADP advertiser, RMON, CSR) behind flat,
host-agnostic ports. It is `milan_top.sv` **minus the Zynq PS and minus the
MAC** - everything inside is vendor-neutral, Verilator-simulated and
Yosys-checked (see [PORTING_GUIDE.md](PORTING_GUIDE.md)).

This guide is the contract you integrate against. The two in-repo reference
integrations of exactly this boundary:

* **LiteX RISC-V SoC** - `MilanNIC`/`add_milan_datapath()` in
  `sw/litex/milan_soc.py` (and the same function reused by the Verilator SoC
  sim `sw/litex/milan_sim.py`). Documented in [../litex/LITEX_SOC.md](../litex/LITEX_SOC.md).
* **Zynq-7000 PS** - `milan_top.sv` + `milan_dma_wrapper.v` + `bd/*.tcl`
  (the pre-migration variant, MAC and PS in place).

```
CPU  ── AXI4-Lite slave (s_axi_*, 16-bit offset) ─────► control plane
DMA  ── s_axis_tx_* (DRAM→) / m_axis_rx_* (→DRAM) / m_axis_ts_* (→DRAM)
MAC  ── m_axis_mac_tx_* (→MAC) / s_axis_mac_rx_* (MAC→) + o_mac_* cfg / i_mac_* status
IRQ  ── o_irq_csr (milan_csr aggregate; DMA-done IRQs come from your DMA engine)
```

Internal TX order: DMA → classifier/queues/CBS → PTP-TX timestamp → ADP
arbiter → MAC. Internal RX order: MAC → PTP-RX timestamp → TCAM dest-MAC
filter → DMA.

---

## 1. Ports, group by group

Parameters: `TDATA_WIDTH = 64` (all AXIS ports; `tkeep` is
`TDATA_WIDTH/8 = 8` bits), `NUM_QUEUES = 4` (from `ethernet_packet_pkg`).
Byte order on AXIS is big-endian (wire order = memory order; see
`hdl/common/parameters.svh`).

### 1.1 Clocks / reset

| Port | Dir | Description |
|---|---|---|
| `axis_clk` | in | system clock (~100 MHz proven; see [PORTING_GUIDE.md](PORTING_GUIDE.md) §3) - runs the entire datapath and the CSR bus |
| `axis_resetn` | in | synchronous, active-low, `axis_clk` domain |
| `gtx_clk` | in | 125 MHz PTP/MAC-RX timestamp domain |
| `gtx_resetn` | in | synchronous, active-low, `gtx_clk` domain |

Tying `gtx_clk = axis_clk` is legal and is what the LiteX build does (the
internal CDC still functions; it just becomes same-clock). If the two really
are asynchronous, declare them as async clock groups in your constraints -
all crossings are handled inside (`ptp_csr_sync`, `cdc_pulse`,
`cdc_handshake`, 2-FF speed sync).

### 1.2 AXI4-Lite CSR slave (control plane)

Standard AXI4-Lite, `s_axi_*`: 16-bit address (a 64 KB window), 32-bit data,
`wstrb`, single outstanding transaction semantics. Only the low 16 bits are
decoded - put the window at **any** base address your interconnect likes and
present the offset. Bases used so far: `0x9000_0000` (LiteX - must be in the
CPU's uncached MMIO region) and `0x43C0_0000` (Zynq GP0).

Register offsets are the ABI shared with the Linux driver and device tree:
[../reference/REGISTER_MAP.md](../reference/REGISTER_MAP.md). Two facts worth
hard-coding into your bring-up:

* Offset `0x0` reads the ID `"MILN"` (`0x4d494c4e`) - the canonical
  first-silicon smoke test (milestone M-A2).
* The map is decoded in `hdl/csr/milan_csr.sv` in 0x100-sized groups
  (0x000 ID/ctrl, 0x100 MAC, 0x200 classifier, 0x300 CBS, 0x400 PTP,
  0x500 RMON, 0x600 ADP, 0x700 RX filter/TCAM).

### 1.3 DMA streams (to/from your memory engine)

| Stream | Dir | Semantics |
|---|---|---|
| `s_axis_tx_*` | in | frames from DRAM into the shaper (your TX DMA reader drives this; `tdata/tkeep/tvalid/tlast/tready`) |
| `m_axis_rx_*` | out | received frames (post TCAM filter) toward DRAM (your RX DMA writer) |
| `m_axis_ts_*` | out | PTP timestamp metadata records (timestamp + seq id + direction) toward DRAM |

Full Ethernet frames, one frame per `tlast` packet, no `tuser` sideband. The
datapath asserts backpressure-correct AXIS handshakes on all three; your
engine must too (the RX path ultimately needs an always-ready sink at line
rate or frames drop at the MAC FIFO, which is what the ring-DMA engines in
`sw/litex/milan_soc.py` - `RingDMAReader`/`RingDMAWriter` - implement; their
design history is in [../findings/RX_RING_DMA.md](../findings/RX_RING_DMA.md)).

### 1.4 MAC-facing streams + sideband (to/from your MAC)

| Port(s) | Dir | Semantics |
|---|---|---|
| `m_axis_mac_tx_*` | out | shaped/timestamped/ADP-merged TX frames to the MAC |
| `s_axis_mac_rx_*` | in | RX frames from the MAC (CRC-stripped, good frames) |
| `o_mac_tx_en, o_mac_rx_en, o_mac_promisc, o_mac_allmulti, o_mac_is_1g` | out | MAC enables/config, driven from CSR group 0x100 |
| `o_mac_ifg[7:0]` | out | inter-frame gap config |
| `o_mac_addr[47:0]`, `o_mc_hash[63:0]` | out | station address + multicast hash for MAC-level filtering |
| `o_phy_reset_n` | out | PHY reset, CSR-controlled |
| `i_mac_speed[1:0]` | in | 00=10M, 01=100M, 10=1G convention; synchronized internally, feeds CSR readback + link-change IRQ |
| `i_link_up`, `i_full_duplex` | in | PHY/MAC status readback |
| `i_mac_events[N-1:0]` | in | one-cycle RMON event pulses; lane index = `ethernet_events_t` enum (`hdl/eth_event_counter/ethernet_events.svh`), counted by the 9 RMON counters in CSR group 0x500 |
| `o_irq_csr` | out | level interrupt: `tx_ts_ready \| link_change \| rmon_rollover` (see 1.5) |

Any MAC works if you can adapt it to 64-bit AXIS with `tkeep`/`tlast` and
supply the sideband (unused status inputs can be tied to sane constants -
the LiteX build tied `i_mac_speed=2'b10, i_link_up=1` until the MAC landed).

### 1.5 Interrupts

`o_irq_csr` is the datapath's only IRQ: a level line aggregating the CSR
events (TX timestamp ready, link change, RMON rollover). DMA-completion
interrupts are **your DMA engine's** to generate. The Linux driver expects
four lines named `tx-dma`, `rx-dma`, `ts-dma`, `csr`
(`sw/driver/README.md`); on the LiteX host they are EventManager sources
folded into one PLIC line, on Zynq four separate GIC lines - the device
tree, not the RTL, encodes that difference (`sw/dts/`).

---

## 2. Minimum viable integration (the M-A2 pattern)

Wire only clocks + reset + the AXI4-Lite CSR port; tie every AXIS input to
zero and every `*_tready` input to 0, tie `i_mac_speed=2'b10`,
`i_link_up=1`, `i_full_duplex=1`, `i_mac_events=0`. This elaborates, meets
timing, and gives you a live CPU⇄CSR path: read offset `0x0`, expect
`"MILN"`. This exact stub-everything pattern is what
`add_milan_datapath()` does before the DMA/MAC are attached, and it is how
both the SoC sim and first silicon were validated. Then attach the MAC
(§1.4), then the DMA (§1.3) - in that order, each step separately testable.

## 3. Source files and includes

The canonical file list is `_MILAN_DATAPATH_SOURCES` in
`sw/litex/milan_soc.py` - packages first, then the verilog-axis cores
(`axis_fifo`, `axis_demux`, `axis_arb_mux`, `arbiter`, `priority_encoder`),
then the datapath RTL, ending in `hdl/common/milan_datapath.sv`. The same
set is used by the `tb/verilator/milan_dp` harness and the `syn/yosys` flow,
so it cannot silently drift. Add these include directories for the
`` `include `` files (`*.svh`): `hdl/common`, `hdl/802_1q_traffic_shaper`,
`hdl/ptp_timestamp`, `hdl/adp`, `hdl/csr`, `hdl/eth_event_counter`.

Prerequisite: `git submodule update --init third_party/verilog-axis`.

Do **not** add `hdl/common/milan_top.sv` or `hdl/common/milan_dma_wrapper.v`
to a non-Zynq build - they are the Zynq variant and drag in the
verilog-ethernet MAC and PS7.

## 4. Running the datapath on its own clock

If 100 MHz timing is tight in your system (the CBS slope divide is the known
critical path), you can run the whole datapath in a slower clock domain and
cross at the boundary - the LiteX build implements this as `--milan-clk-freq`:
AXI-Lite crosses through an async-FIFO CDC (`AXILiteClockDomainCrossing`),
each AXIS lane through a `stream.ClockDomainCrossing`, and the IRQ through a
2-FF synchronizer. A 64-bit datapath at ≥50 MHz still exceeds 1 GbE line
rate, so this costs no throughput. See `add_milan_datapath()` and
`_axis_dp_cdc()` in `sw/litex/milan_soc.py` for the working pattern, plus
the CBS multicycle constraint described in
[PORTING_GUIDE.md](PORTING_GUIDE.md) §4.5.

## 5. Software contract

* **Register ABI:** [../reference/REGISTER_MAP.md](../reference/REGISTER_MAP.md)
  (offsets defined once in `milan_csr.sv`; the `tb/verilator/csr` harness
  asserts RTL and doc agree).
* **Linux driver:** `kl-eth` (sibling repo `kl-linux-drivers`), DT binding
  `compatible = "kl,dma-ether-0.9"` - resource layout and caveats in
  [`sw/driver/README.md`](../../sw/driver/README.md).
* **Device tree:** generated, per-host, by `sw/dts/milan_dt.py` from the
  build's `csr.json` - see [`sw/dts/README.md`](../../sw/dts/README.md). If
  you integrate on a new host, add an IR JSON there rather than hand-writing
  a dtsi.

## 6. Verifying your integration

| Step | Check | Where |
|---|---|---|
| RTL boundary sanity | `tb/verilator/milan_dp` drives this exact module: CSR ID read, classifier program, TX/RX byte-exact | [../testing/TESTING.md](../testing/TESTING.md) |
| Your SoC in sim | LiteX users: `milan_sim.py` boots the BIOS and reads `"MILN"` over the real CPU bus | [../testing/SIMULATION.md](../testing/SIMULATION.md) |
| First silicon | CSR ID read at your base address (M-A2), then MAC loopback, then DMA rings | [BOARD_PORTING_AX7101.md](BOARD_PORTING_AX7101.md) shows the worked sequence |

---

*Related: [PORTING_GUIDE.md](PORTING_GUIDE.md) (toolchain/board level) ·
[../fpga/FPGA_DESIGN.md](../fpga/FPGA_DESIGN.md) (what is inside the boundary) ·
[../reference/REGISTER_MAP.md](../reference/REGISTER_MAP.md) (the CSR ABI) ·
[../litex/LITEX_SOC.md](../litex/LITEX_SOC.md) (reference host).*
