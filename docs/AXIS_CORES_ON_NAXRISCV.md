# Attaching AXI-Stream FPGA cores to the NaxRiscv SoC

How to connect an **AXI4-Stream** FPGA core (a MAC, a DSP block, a crypto engine,
the Milan TSN datapath …) to the NaxRiscv/LiteX SoC so that software running on
the core can configure it, move data to/from it, and get interrupts from it.

The concrete, working reference for everything below is
[`sw/litex/milan_soc.py`](../sw/litex/milan_soc.py) (class `MilanNIC`): the Milan
NIC *is* an AXI-Stream core cluster, and it is attached with exactly these three
planes.

---

## 1. The mental model: AXI-Stream is not memory-mapped

A CPU talks to peripherals through **addresses**. AXI-Stream has **no address** —
it is a one-way, back-pressured data-flow bus (`tdata`/`tkeep`/`tvalid`/`tready`/
`tlast`). You therefore never "attach AXIS to the CPU bus" directly. You attach it
on **three separate planes**:

```
                          ┌───────────────────────────────────────────────┐
                          │                 NaxRiscv SoC                   │
   register  ┌────────────┤  pbus (AXI-Lite)  ── CSR / control ───────────►│  ① CONTROL
   reads/    │            │                                                │
   writes    │   AXIS     │  dma_bus (AXI, coherent) ◄─ DMA ─► DRAM/L2 ────│  ② DATA
  ───────────┼──►┌──────┐ │                                                │
   your      │   │ AXIS │─┼──tvalid/tdata──►┌─────┐  AXI  ┌──────────────┐ │
   AXIS  ────┼──►│ CORE │ │◄─tready─────────│ DMA │──────►│ interconnect │ │
   core      │   └──────┘ │                 └─────┘       └──────────────┘ │
             │      │irq  │  irq line ──► EventManager ──► PLIC ───────────│  ③ EVENTS
             └──────┼─────┘                                                │
                    └──────────────────────────────────────────────────────┘
```

- **① Control** — the core's config/status registers, exposed as an **AXI-Lite
  (or CSR) slave** in the CPU's MMIO map. This is how the driver programs it.
- **② Data** — the AXIS `tdata` flow is bridged to/from **memory by a DMA
  engine**. The CPU touches *buffers in DRAM*, never the stream itself.
- **③ Events** — a completion/error line raised into the **PLIC** so the driver
  can use interrupts (NAPI, PTP, …) instead of polling.

The rest of this document is one section per plane, plus clock-domain crossing and
a checklist.

---

## 2. What NaxRiscv exposes in LiteX

`litex/soc/cores/cpu/naxriscv/core.py` gives the SoC these buses:

| Bus | Type | Purpose |
|-----|------|---------|
| `ibus` / `dbus` | AXI-Lite → wishbone/axi | instruction fetch + load/store to memory |
| `pbus` | `AXILiteInterface` | **peripheral bus** — where MMIO slaves (your control plane) land |
| `dma_bus` | `AXIInterface(data_width=64, addr=32, id=4)` | **coherent DMA** into L2/DRAM — only when built with `--with-coherent-dma` |
| `interrupt` | `Signal(32)` | external interrupt lines, driven by the **PLIC** (`0xf0c0_0000`) + CLINT (`0xf001_0000`) |

Two consequences you must respect:

1. **MMIO must be in the IO region.** NaxRiscv marks `0x8000_0000–0xFFFF_FFFF` as
   the uncached IO region. A control-plane slave placed below that (e.g. the Zynq
   address `0x43C0_0000`) fails with *"Region not in IO region, it must be
   cached."* `milan_soc.py` maps the Milan CSR window at `0x9000_0000` for this
   reason (the register **offsets** are unchanged; only the base differs per host).
2. **The DMA data path is 64-bit** on the coherent `dma_bus`. Size your AXIS↔AXI
   bridge and buffers accordingly (`xlen=64` → `data_width=64`).

---

## 3. Plane ① — control (AXI-Lite / CSR slave)

Give the core an AXI-Lite slave and drop it into the peripheral bus. This is a
verbatim reduction of `MilanNIC` in `milan_soc.py`:

```python
from litex.soc.interconnect import axi
from litex.soc.integration.soc import SoCRegion

# 1. An AXI-Lite interface the core will terminate.
axil = axi.AXILiteInterface(data_width=32, address_width=32)

# 2. Map it into the CPU IO region (uncached MMIO). MUST be >= 0x8000_0000.
self.bus.add_slave("mycore_csr", axil,
    region=SoCRegion(origin=0x9000_0000, size=0x1_0000, cached=False))

# 3. Wire the AXI-Lite channels to your Verilog core (black box or real RTL).
self.specials += Instance("mycore",
    i_s_axi_awaddr = axil.aw.addr[:16], i_s_axi_awvalid = axil.aw.valid,
    o_s_axi_awready= axil.aw.ready,
    i_s_axi_wdata  = axil.w.data,  i_s_axi_wstrb = axil.w.strb,
    i_s_axi_wvalid = axil.w.valid, o_s_axi_wready = axil.w.ready,
    o_s_axi_bresp  = axil.b.resp,  o_s_axi_bvalid = axil.b.valid,
    i_s_axi_bready = axil.b.ready,
    i_s_axi_araddr = axil.ar.addr[:16], i_s_axi_arvalid = axil.ar.valid,
    o_s_axi_arready= axil.ar.ready,
    o_s_axi_rdata  = axil.r.data,  o_s_axi_rresp = axil.r.resp,
    o_s_axi_rvalid = axil.r.valid, i_s_axi_rready = axil.r.ready,
    # ... AXIS + irq ports below ...
)
```

The driver then `ioremap`s `0x9000_0000` (the DT `reg` base) and reads/writes the
core's registers. If your core has no AXI-Lite port, expose registers with a LiteX
`CSRStorage`/`CSRStatus` bank instead — same idea, LiteX generates the decode.

---

## 4. Plane ② — data (AXI-Stream ↔ memory via DMA)

The CPU cannot read `tdata` directly; a **DMA engine** copies between the stream
and DRAM descriptors. Pick one of these bridges:

### 4a. Coherent DMA (recommended) — no cache flushes in the driver
Build the CPU with coherent DMA and give your AXIS→AXI bridge a master on the
coherent `dma_bus`:

```python
# milan_soc.py: enable it via NaxRiscv args (see §2 table).
_nax_args.with_coherent_dma = True     # -> NaxRiscv.with_dma, exposes self.cpu.dma_bus

# Declare the stream your core drives (RX) / consumes (TX), 64-bit to match dma_bus.
rx_axis = axi.AXIStreamInterface(data_width=64, clock_domain="sys")
tx_axis = axi.AXIStreamInterface(data_width=64, clock_domain="sys")

# A stream<->memory DMA (Forencich axi_dma, or LiteX's own DMA — see 4b).
# Its AXI master goes onto the CPU's coherent DMA bus:
self.dma_bus.add_master("mycore_dma", master=dma.axi_mm)   # coherent -> L2/DRAM
```

Because accesses are coherent, the CPU's caches stay in sync with DMA'd buffers —
the Linux driver uses plain `dma_map_*` without manual invalidation.

### 4b. Non-coherent DMA — simpler fabric, driver must flush
Attach the DMA master to the ordinary system bus instead:

```python
self.bus.add_master("mycore_dma", master=dma.axi_mm)   # into the main interconnect
```

LiteX also ships memory-mover primitives if you don't want an external DMA IP:
`litex.soc.interconnect.wishbone.WishboneDMAReader/Writer` and the LiteDRAM
`LiteDRAMDMAReader/Writer` port DMAs convert a LiteX `stream.Endpoint` to/from
memory; put an adapter between the AXIS core and the LiteX stream endpoint.

### Connecting the AXIS wires to the core
```python
self.specials += Instance("mycore",
    # RX: core -> SoC
    o_m_axis_tdata = rx_axis.data, o_m_axis_tkeep = rx_axis.keep,
    o_m_axis_tvalid= rx_axis.valid, i_m_axis_tready= rx_axis.ready,
    o_m_axis_tlast = rx_axis.last,
    # TX: SoC -> core
    i_s_axis_tdata = tx_axis.data, i_s_axis_tkeep = tx_axis.keep,
    i_s_axis_tvalid= tx_axis.valid, o_s_axis_tready= tx_axis.ready,
    i_s_axis_tlast = tx_axis.last,
)
```

Honour `tready` back-pressure end-to-end and terminate frames with `tlast`; the
DMA uses `tlast` as the packet/descriptor boundary.

---

## 5. Plane ③ — events (IRQ → PLIC)

Surface each interrupt line through a LiteX `EventManager`; `self.irq.add` routes
it to the PLIC that NaxRiscv already instantiates. Straight from `MilanNIC`:

```python
from litex.soc.interconnect.csr_eventmanager import EventManager, EventSourceLevel

self.submodules.ev = ev = EventManager()
ev.rx  = EventSourceLevel()      # one source per line
ev.tx  = EventSourceLevel()
ev.finalize()

self.specials += Instance("mycore",
    o_irq_rx = ev.rx.trigger,
    o_irq_tx = ev.tx.trigger,
    # ...
)

# In the SoC, after adding the module:
self.irq.add("mycore", use_loc_if_exists=True)   # -> allocates a PLIC source
```

The allocated PLIC source numbers are what the driver's device-tree `interrupts`
property references (`interrupt-parent = <&plic>`), exactly as in
[`sw/dts/milan.dtsi`](../sw/dts/milan.dtsi).

---

## 6. Clock-domain crossing

AXIS cores frequently run in a **different clock domain** than the SoC — e.g. the
Milan datapath's RGMII side is 125 MHz while `sys` is 100 MHz. Cross the stream
*before* it reaches the DMA/bus:

- Use an async stream FIFO in the fabric — `third_party/verilog-axis`'s
  `axis_async_fifo` (already vendored) is the drop-in for this, or LiteX's
  `stream.ClockDomainCrossing`.
- Declare the interface's domain with `AXIStreamInterface(..., clock_domain="eth_rx")`
  and rename core submodules with `ClockDomainsRenamer("eth_rx")`.
- Add the extra clock to the platform and constrain it:
  `platform.add_period_constraint(cd.clk, 1e9/125e6)` and
  `platform.add_false_path_constraints(sys_clk, eth_clk)` for the CDC.

Never let a raw AXIS bus cross clock domains without a CDC FIFO — `tvalid`/`tready`
handshakes will corrupt.

---

## 7. Adding the RTL and constraints

```python
platform.add_source_dir("../../hdl")                       # your core + wrappers
platform.add_source_dir("../../third_party/verilog-axis/rtl")
platform.add_source("mycore.v")
```

`milan_soc.py` keeps `milan_datapath` a **black box** until the PS-less wrapper
lands; LiteX still exports a synthesizable top with the instance in place (you can
see `[BB:milan_datapath]` in the generated gateware tree). Provide the real RTL
before place-&-route.

---

## 8. Checklist / gotchas

- [ ] Control-plane MMIO base **≥ `0x8000_0000`** (IO region), `cached=False`.
- [ ] DMA data width matches the CPU (**64-bit** for RV64 `dma_bus`).
- [ ] Prefer `--with-coherent-dma` so the driver skips manual cache maintenance.
- [ ] Every AXIS hop honours `tready`; frames end on `tlast`.
- [ ] CDC FIFO on any AXIS bus that changes clock domain; constrain the crossing.
- [ ] One `EventSourceLevel` per IRQ line; `self.irq.add(...)` → PLIC → DT `interrupts`.
- [ ] Byte order: LiteX/AXIS is little-endian lane 0 first; match your core (the
      Milan RTL documents its big-endian-on-the-wire convention in the harnesses).

---

## 9. Worked example — the Milan NIC

The Milan NIC exercises all three planes at once, and `MilanNIC` in
`sw/litex/milan_soc.py` is the literal implementation:

| Plane | Milan realisation |
|-------|-------------------|
| ① control | `milan_csr` AXI-Lite slave @ `0x9000_0000` (register map: `docs/REGISTER_MAP.md`) |
| ② data | `milan_datapath` AXIS TX/RX ↔ `axi_dma` ↔ `dma_bus` (TX/RX/timestamp rings) |
| ③ events | `o_irq_tx/rx/ts/csr` → `EventManager` → `self.irq.add("milan")` → PLIC → DT `interrupts = <1..4>` |

The internal AXIS pipeline (classifier → per-queue FIFOs → CBS shaper → MAC, plus
the RX MAC filter) is all AXI-Stream and is verified stand-alone in
`tb/verilator/` — attaching it to NaxRiscv is purely the three-plane wiring above.
