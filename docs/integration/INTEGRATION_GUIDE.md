# Integration guide - wiring `milan_datapath` into your SoC

[`hdl/milan/milan_datapath.sv`](../../hdl/milan/milan_datapath.sv) is the single clean integration boundary of
this project: the whole Milan TSN datapath (classify + 802.1Qav CBS, PTP
clock + timestamping, TCAM RX filter, the AAF/CRF stream engines, MAAP, RMON,
CSR) **plus the entire IEEE 1722.1 / SRP control plane** —
[`hdl/milan/KL_pp_shadow.sv`](../../hdl/milan/KL_pp_shadow.sv), wrapping the
pinned `protocol-processor` submodule — behind flat, host-agnostic ports. It is
`milan_top.sv` **minus the Zynq PS and minus the MAC** - everything inside is
vendor-neutral, Verilator-simulated and Yosys-checked (see
[PORTING_GUIDE.md](PORTING_GUIDE.md)).

Two things an integrator needs to know before wiring anything, because neither
is visible from the port list:

* **`KL_pp_shadow` is instantiated unconditionally** — there is no parameter,
  no fallback and no shadow arm, and it brings the `protocol-processor`
  submodule into your source list (Section 3). It owns ADP, ACMP (talker and listener)
  and SRP; MAAP stays in `hdl/` and is bridged to it by `KL_pp_maap_shim.sv`.
* **On AECP this entity serves the processor's implemented command inventory.**
  The processor's AECP uCPU has landed; this repository's own engine is deleted.
  The inventory includes solicited `GET_COUNTERS` for supported descriptor banks.
  `READ_DESCRIPTOR` returns
  `SUCCESS` with the descriptor, or `NO_SUCH_DESCRIPTOR` / `BAD_ARGUMENTS` with
  the IEEE 1722.1 Section 7.4.5 4-byte stub; an `IDENTIFY_NOTIFICATION` sent as a
  command answers `BAD_ARGUMENTS`; a command aimed at another
  `target_entity_id`, and any AECP response arriving as input, are refused
  silently by design. Unsupported operations receive the conformant fallback,
  which is not command coverage. The Milan Table 5.22 counter-change scheduler,
  remaining mandatory commands, and saved-state persistence across a power cycle
  are genuinely absent. Plan around that boundary if your product needs
  AECP -- and see Section 1.6, because the descriptor half comes with an integration
  obligation you inherit.

These integration-boundary claims are checked against the
[Milan feature status ledger](../reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `aem.served-command-set` | `implemented` | - |
| `aem.mandatory-missing-set` | `implemented` | - |
| `state.nonvolatile-persistence` | `missing` | - |
| `notifications.change-events` | `implemented` | - |
<!-- milan-feature-status:end -->

This guide is the contract you integrate against. The two in-repo reference
integrations of exactly this boundary:

* **LiteX RISC-V SoC** - `MilanNIC`/`add_milan_datapath()` in
  [`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py) (and the same function reused by the Verilator SoC
  sim [`sw/litex/milan_sim.py`](../../sw/litex/milan_sim.py)). Documented in [../litex/LITEX_SOC.md](../litex/LITEX_SOC.md).
* **Zynq-7000 PS** - `milan_top.sv` + `milan_dma_wrapper.v` + `bd/*.tcl`
  (the pre-migration variant, MAC and PS in place).

```
CPU  ── AXI4-Lite slave (s_axi_*, 16-bit offset) ─────► control plane
DMA  ── s_axis_tx_* (DRAM→) / m_axis_rx_* (→DRAM) / m_axis_ts_* (→DRAM)
MAC  ── m_axis_mac_tx_* (→MAC) / s_axis_mac_rx_* (MAC→) + o_mac_* cfg / i_mac_* status
MEM  ── o_desc_mem_* / i_desc_mem_* (read-only master → your main memory:
        the AECP descriptor image lives there, Section 1.6)
IRQ  ── o_irq_csr (milan_csr aggregate; DMA-done IRQs come from your DMA engine)
```

Internal TX order: DMA → classifier/queues/CBS → PTP-TX timestamp → a
four-mux arbiter cascade → MAC. LSB-first in `A_TXARB_DIAG` (`0x784`) the muxes
are 0 `ctl_tx` (the protocol processor's packed TX + MAAP → the control lane),
1 `aaf_final`, 2 `crf_dp`, 3 `adp_tx` (the MAC boundary); bits 7:4 read a
structural zero. Internal RX order: MAC → PTP-RX timestamp → TCAM dest-MAC
filter → DMA, with the control plane and the AVTP media path as pure monitor
taps that never drive the stream back.

---

## Contents

- **[1. Ports, group by group](#1-ports-group-by-group)** -- The whole boundary, one table per group: clocks, the AXI4-Lite window, DMA streams, MAC sideband, and the descriptor-image read master. Section 1.6 records the compile-time base, mandatory error arm, and the tracked builder plus loader flow.
- **[2. Minimum viable integration (the M-A2 pattern)](#2-minimum-viable-integration-the-m-a2-pattern)** -- The stub-everything first step: clocks, reset, CSR port, every AXIS input tied off, then read `"MILN"` at offset `0x0`. This is how both the SoC sim and first silicon were validated, and it names the separately testable attach order: MAC, DMA, then the descriptor-image master.
- **[3. Source files and includes](#3-source-files-and-includes)** -- Where the canonical file list lives (`_MILAN_DATAPATH_SOURCES`), and the reason it cannot silently drift: the Verilator harness and the Yosys flow consume the same list. Also the six `svh` include dirs, both submodule prerequisites, the two generated control-plane ROM images, and the two files a non-Zynq build must exclude.
- **[4. Running the datapath on its own clock](#4-running-the-datapath-on-its-own-clock)** -- The escape hatch when 100 MHz timing is tight: the three crossing mechanisms `--milan-clk-freq` uses, and why a 64-bit datapath at 50 MHz still exceeds 1 GbE line rate.
- **[5. Software contract](#5-software-contract)** -- The register ABI, the `kl,dma-ether-0.9` DT compatible string, and the generated device tree. Add an IR JSON for a new host rather than hand-writing a dtsi.
- **[6. Verifying your integration](#6-verifying-your-integration)** -- A four-rung ladder from RTL boundary to first silicon and on to controller enumeration, each rung naming its harness and the doc that walks it.

## 1. Ports, group by group

Parameters: `TDATA_WIDTH = 64` (all AXIS ports; `tkeep` is
`TDATA_WIDTH/8 = 8` bits), `NUM_QUEUES = 5` (from
`ethernet_packet_pkg::NUMBER_OF_QUEUES`; **higher index = higher priority**,
see [../reference/EGRESS_QUEUE_MAP.md](../reference/EGRESS_QUEUE_MAP.md)).
Byte order on AXIS is big-endian (wire order = memory order; see
[`hdl/common/parameters.svh`](../../hdl/common/parameters.svh)).

### 1.1 Clocks / reset

| Port | Dir | Description |
|---|---|---|
| `axis_clk` | in | system clock (~100 MHz proven; see [Section 3 of PORTING_GUIDE.md](PORTING_GUIDE.md#3-clocking-and-reset-requirements-vendor-independent-contract)) - runs the entire datapath and the CSR bus |
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
* The map is decoded in [`hdl/common/csr/milan_csr.sv`](../../hdl/common/csr/milan_csr.sv) in 0x100-sized groups
  (0x000 ID/IRQ, 0x100 MAC, 0x200 RMON stats, 0x300 classifier,
  0x400 CBS per-queue (`0x400`-`0x49F`, stride `0x20` × 5 queues), 0x500 PTP,
  0x600 entity identity, 0x700 RX filter/TCAM, and up through the
  `0x920`-`0x930` protocol-processor window).
* **The entity enable is ORed from two bits**: `PP_CTRL[0]` (`0x920`) and the
  historic `ADP_CTRL.en` (`0x600` bit 0). Either one enables the entity, so a
  bring-up script written against the old bit still works. `milan_csr` has no
  `PP_PLANE_P` parameter any more — the `0x920` window is always decoded, and
  `PP_STAT` always carries its `0x5B` tag, which makes it a usable
  second smoke test after `"MILN"`.
* **No register was removed** when the legacy control plane was deleted; the map
  is an ABI. Words whose source went away read documented **structural zeros**,
  a few provisioning words are **write-only scratch** (they read back what you
  wrote and reach nothing on the wire), and `A_TXARB_DIAG` **renumbered**. Do
  not infer liveness from a plausible value — check
  [../reference/REGISTER_MAP.md](../reference/REGISTER_MAP.md).

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
[`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py) - `RingDMAReader`/`RingDMAWriter` - implement; their
design history is in [../findings/RX_RING_DMA.md (archived)](../../historical_now_obsolete/findings/RX_RING_DMA.md)).

### 1.4 MAC-facing streams + sideband (to/from your MAC)

| Port(s) | Dir | Semantics |
|---|---|---|
| `m_axis_mac_tx_*` | out | TX frames to the MAC: shaped CPU traffic, the AAF/CRF streams and the control lane, merged by the four-mux cascade above |
| `s_axis_mac_rx_*` | in | RX frames from the MAC (CRC-stripped, good frames). The protocol processor and the AVTP media path tap this stream internally; you drive it exactly as before |
| `o_mac_tx_en, o_mac_rx_en, o_mac_promisc, o_mac_allmulti, o_mac_is_1g` | out | MAC enables/config, driven from CSR group 0x100 |
| `o_mac_ifg[7:0]` | out | inter-frame gap config |
| `o_mac_addr[47:0]`, `o_mc_hash[63:0]` | out | station address + multicast hash for MAC-level filtering |
| `o_phy_reset_n` | out | PHY reset, CSR-controlled |
| `i_mac_speed[1:0]` | in | 00=10M, 01=100M, 10=1G convention; synchronized internally, feeds CSR readback + link-change IRQ |
| `i_link_up`, `i_full_duplex` | in | PHY/MAC status readback |
| `i_mac_events[N-1:0]` | in | one-cycle RMON event pulses; lane index = `ethernet_events_t` enum ([`hdl/common/eth_event_counter/ethernet_events.svh`](../../hdl/common/eth_event_counter/ethernet_events.svh)), counted by the 9 RMON counters in CSR group 0x200 |
| `o_irq_csr` | out | level interrupt: `tx_ts_ready \| link_change \| rmon_rollover` (see 1.5) |

Any MAC works if you can adapt it to 64-bit AXIS with `tkeep`/`tlast` and
supply the sideband (unused status inputs can be tied to sane constants -
the LiteX build tied `i_mac_speed=2'b10, i_link_up=1` until the MAC landed).

### 1.5 Interrupts

`o_irq_csr` is the datapath's only IRQ: a level line aggregating the CSR
events (TX timestamp ready, link change, RMON rollover). DMA-completion
interrupts are **your DMA engine's** to generate. The Linux driver expects
four lines named `tx-dma`, `rx-dma`, `ts-dma`, `csr`
([`sw/driver/README.md`](../../sw/driver/README.md)); on the LiteX host they are EventManager sources
folded into one PLIC line, on Zynq four separate GIC lines - the device
tree, not the RTL, encodes that difference ([`sw/dts/`](../../sw/dts)).

### 1.6 Descriptor-image read master (the entity model lives in YOUR memory)

The AECP descriptor store does not hold the entity model in fabric — it
**fetches it from your main memory** over this read-only master. This is the one
port group that gives the integrator a job beyond wiring.

| Port(s) | Dir | Semantics |
|---|---|---|
| `o_desc_mem_req_valid`, `i_desc_mem_req_ready` | out/in | request handshake; **one outstanding request**, held until ready |
| `o_desc_mem_req_addr[31:0]`, `o_desc_mem_req_beats[8:0]` | out | byte address and burst length in **64-bit beats** (at least 1, at most 128) |
| `i_desc_mem_rsp_valid`, `o_desc_mem_rsp_ready` | in/out | response handshake; `rsp_ready` is tied 1 by the processor — it always sinks |
| `i_desc_mem_rsp_data[63:0]`, `i_desc_mem_rsp_last` | in | responses **in order**; a beat carries its **lowest byte address in bits [63:56]** (1722.1 wire order, big-endian — a byte-reverse of what a little-endian bus hands you), and `rsp_last` marks the final beat |
| `i_desc_mem_rsp_err` | in | read error. **Propagate it, never mask it** |

Four things to get right:

* **The base is compile-time.** `PP_DESC_BASE_P` (8-byte aligned) is an
  elaboration parameter and the processor holds **no base register**, so nothing
  can be pointed anywhere at runtime. **Derive it from your own memory map** —
  the LiteX build takes the top 1 MiB of `main_ram`, which the device tree
  reserves, rather than mirroring a literal.
* **The error arm is not optional.** LiteX's `wishbone2axi` asserts `err`
  *together with* `ack`, so an `If(ack, …)` alone accepts a failed read and
  latches whatever the data bus held. Wire `rsp_err`: the store aborts the burst
  and degrades that locate to `NO_SUCH_DESCRIPTOR`, so a corrupt descriptor is
  never served as though it were good.
* **Tying `i_desc_mem_req_ready` to 0 is legal, and it must be deliberate.** The
  store's watchdog (4096 cycles, about 41 µs at 100 MHz, covering the request
  handshake as well) abandons the burst, so the image never validates and every
  `READ_DESCRIPTOR` answers `BAD_ARGUMENTS` instead of hanging — but the entity then serves no
  descriptors at all, and that has to be a stated choice, not an oversight.
* **Load the builder-generated image before entity enable.** The end-station
  builder produces `aem_desc.bin`, `aem_desc.json`, and `aem_desc.map` for the
  selected configuration. The tracked board flow uses `aemi-load` to verify the
  paired metadata and place the image at `PP_DESC_BASE_P` before enabling the
  entity. A custom integration must provide the equivalent step. The image
  header's magic (`"AEMI"`, `0x41454D49`),
  layout version and checksum make an unloaded region read as **"image not
  loaded"** rather than as a valid empty model, and a **late load heals without
  a reset** — each locate against an invalid image re-arms the header probe.

---

## 2. Minimum viable integration (the M-A2 pattern)

Wire only clocks + reset + the AXI4-Lite CSR port; tie every AXIS input to
zero and every `*_tready` input to 0, tie `i_mac_speed=2'b10`,
`i_link_up=1`, `i_full_duplex=1`, `i_mac_events=0`, and tie
`i_desc_mem_req_ready=0` / `i_desc_mem_rsp_*=0` (the descriptor store's watchdog
handles that cleanly -- Section 1.6).

This elaborates, meets timing, and gives you a live CPU⇄CSR path: read
offset `0x0`, expect `"MILN"`. This exact stub-everything pattern is what
`add_milan_datapath()` does before the DMA/MAC are attached, and it is how
both the SoC sim and first silicon were validated.

Then attach the MAC (Section 1.4), then the DMA (Section 1.3) - in that order, each step
separately testable. The descriptor-image master (Section 1.6) is a fourth step, and
the only one with a software half: bridging it makes `READ_DESCRIPTOR` capable
of succeeding, and **loading an image at the base** is what makes it actually
succeed.

## 3. Source files and includes

The canonical file list is `_MILAN_DATAPATH_SOURCES` in
[`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py) - packages first, then the verilog-axis cores
(`axis_fifo`, `axis_demux`, `axis_arb_mux`, `arbiter`, `priority_encoder`),
then the datapath RTL **including the `protocol-processor` submodule's sources
and [`hdl/milan/KL_pp_shadow.sv`](../../hdl/milan/KL_pp_shadow.sv)**, ending in
[`hdl/milan/milan_datapath.sv`](../../hdl/milan/milan_datapath.sv). Read that
list rather than reconstructing it: the control plane is no longer a directory
you can glob out of `hdl/`.

The same set is used by the [`tb/verilator/milan_dp`](../../tb/verilator/milan_dp) harness and the
[`syn/yosys`](../../syn/yosys) flow, so it cannot silently drift.

Add these include directories for the `` `include `` files (`*.svh`):
[`hdl/common`](../../hdl/common), [`hdl/ieee8021q/ts`](../../hdl/ieee8021q/ts), [`hdl/ieee8021as/ptp_timestamp`](../../hdl/ieee8021as/ptp_timestamp),
[`hdl/ieee17221/adp`](../../hdl/ieee17221/adp), [`hdl/common/csr`](../../hdl/common/csr), [`hdl/common/eth_event_counter`](../../hdl/common/eth_event_counter).

Prerequisites: `git submodule update --init third_party/verilog-axis` **and
`git submodule update --init protocol-processor`** — the datapath does not
elaborate without the latter, since `KL_pp_shadow` is instantiated
unconditionally. `KL_pp_shadow` also takes **two `$readmemh` images** that must
be readable from the simulator's or synthesiser's working directory — pass them
as absolute paths, because a relative one resolves against wherever the tool was
launched: `TROM_HEX_P` (the ACMP listener transition ROM,
`protocol-processor/hdl/acmp/rom/gen_ltn_rom.py`) and `UCODE_HEX_P` (the **AECP uCPU microcode**,
`protocol-processor/hdl/aecp/ucode/gen_ucode.py`). Both are generated at build
time by `add_milan_datapath()`. An all-zero microcode store is an AECP engine
that answers nothing, which looks exactly like a build from before the uCPU
landed — so a missing `UCODE_HEX_P` fails as silence, not as an error.
`PP_DESC_BASE_P` has no default worth inheriting either: the LiteX helper
**raises** rather than falling back, because the submodule's placeholder base is
not guaranteed to be memory on your SoC (Section 1.6).

Do **not** add [`hdl/milan/milan_top.sv`](../../hdl/milan/milan_top.sv) or [`hdl/milan/milan_dma_wrapper.v`](../../hdl/milan/milan_dma_wrapper.v)
to a non-Zynq build - they are the Zynq variant and drag in the
verilog-ethernet MAC and PS7.

## 4. Running the datapath on its own clock

If 100 MHz timing is tight in your system (the CBS slope divide is the known
critical path), you can run the whole datapath in a slower clock domain and
cross at the boundary - the LiteX build implements this as `--milan-clk-freq`:

- AXI-Lite crosses through an async-FIFO CDC (`AXILiteClockDomainCrossing`);
- each AXIS lane through a `stream.ClockDomainCrossing`;
- the IRQ through a 2-FF synchronizer.

A 64-bit datapath at ≥50 MHz still exceeds 1 GbE line rate, so this costs
no throughput.

See `add_milan_datapath()` and `_axis_dp_cdc()` in [`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py)
for the working pattern, plus the CBS multicycle constraint described in
[Section 4.5 of PORTING_GUIDE.md](PORTING_GUIDE.md#45-timing-constraints-translate-dont-skip).

## 5. Software contract

* **Register ABI:** [../reference/REGISTER_MAP.md](../reference/REGISTER_MAP.md)
  (offsets defined once in `milan_csr.sv`; the [`tb/verilator/csr`](../../tb/verilator/csr) harness
  asserts RTL and doc agree).
* **Linux driver:** `kl-eth` (sibling repo `kl-linux-drivers`), DT binding
  `compatible = "kl,dma-ether-0.9"` - resource layout and caveats in
  [`sw/driver/README.md`](../../sw/driver/README.md).
* **Device tree:** generated, per-host, by [`sw/dts/milan_dt.py`](../../sw/dts/milan_dt.py) from the
  build's `csr.json` - see [`sw/dts/README.md`](../../sw/dts/README.md). If
  you integrate on a new host, add an IR JSON there rather than hand-writing
  a dtsi.

## 6. Verifying your integration

| Step | Check | Where |
|---|---|---|
| RTL boundary sanity | [`tb/verilator/milan_dp`](../../tb/verilator/milan_dp) drives this exact module: CSR ID read, classifier program, TX/RX byte-exact | [../testing/TESTING.md](../testing/TESTING.md) |
| Your SoC in sim | LiteX users: `milan_sim.py` boots the BIOS and reads `"MILN"` over the real CPU bus | [../testing/SIMULATION.md](../testing/SIMULATION.md) |
| First silicon | CSR ID read at your base address (M-A2), then MAC loopback, then DMA rings | [BOARD_PORTING_AX7101.md](BOARD_PORTING_AX7101.md) shows the worked sequence |
| Enumeration | write a descriptor image at your derived base, then `READ_DESCRIPTOR` the ENTITY descriptor from a controller. `BAD_ARGUMENTS` everywhere means the image is missing or corrupt (or the master is not bridged), not that AECP is broken; `NO_SUCH_DESCRIPTOR` means the opposite -- the image loaded and that descriptor is genuinely absent from the model | Section 1.6; [Section 26 of ../limitations/TROUBLESHOOTING.md](../limitations/TROUBLESHOOTING.md#section-26-the-controller-finds-the-entity-and-enumerates-nothing---the-descriptor-image-was-never-loaded-into-dram) |

---

*Related: [PORTING_GUIDE.md](PORTING_GUIDE.md) (toolchain/board level) ·
[../fpga/FPGA_DESIGN.md](../fpga/FPGA_DESIGN.md) (what is inside the boundary) ·
[../reference/REGISTER_MAP.md](../reference/REGISTER_MAP.md) (the CSR ABI) ·
[../litex/LITEX_SOC.md](../litex/LITEX_SOC.md) (reference host).*
