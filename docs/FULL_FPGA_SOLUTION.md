# The Full-FPGA Milan Solution — architecture, build, and how to continue

This is the master guide to the **vendor-neutral, fully-FPGA** Milan TSN network
interface: a single **NaxRiscv RV64GC** softcore running Linux, with the entire
Milan/AVB/TSN datapath in fabric, on an **Alinx AX7101 (Xilinx Artix-7 xc7a100t)** —
built with an **open toolchain** (LiteX + Verilator + Yosys; Vivado only for the
final Artix bitstream).

It is written for two audiences:
- **High-level** (§1–§3): what the system is, the protocol stack, the block diagram,
  and current status — enough to reason about the solution and plan work.
- **Medium-level** (§4–§8): module-by-module wiring, the CSR/DMA/IRQ ABI, the exact
  build/run commands, how each boundary is attached, and how to add the next piece.

Companion documents:
- [`PROTOCOL_VALIDATION_MATRIX.md`](PROTOCOL_VALIDATION_MATRIX.md) — **every protocol
  × where it's implemented × the test that validates it** (the validation contract).
- [`FULLY_FPGA_RISCV_MIGRATION.md`](FULLY_FPGA_RISCV_MIGRATION.md) — the deep, step-
  numbered migration plan (§A.x parts are referenced throughout here).
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — the datapath/control-plane internals.
- [`AXIS_CORES_ON_NAXRISCV.md`](AXIS_CORES_ON_NAXRISCV.md) — how AXI-Stream cores
  attach to the CPU (the pattern the Milan NIC follows).
- [`REGISTER_MAP.md`](REGISTER_MAP.md) — the CSR ABI.

---

## 1. What the full-FPGA solution is (high level)

```
        ┌──────────────────────────── FPGA (xc7a100t) ────────────────────────────┐
        │                                                                          │
        │   NaxRiscv RV64GC (Sv39 MMU) ── Linux ── kl-eth driver                   │
        │        │  pbus (AXI-Lite)        │ DMA bus         │ PLIC                 │
        │        ▼                         ▼                 ▲                      │
        │   ┌─────────┐   ┌──────────────────────────┐   ┌──────┐                  │
        │   │milan_csr│◄──┤   milan_datapath  (§A.9)  │──►│ IRQs │                  │
        │   │ 0x000.. │   │  classify→CBS→PTP→ADParb  │   └──────┘                  │
        │   └─────────┘   │  PTP-RX→dest-MAC filter   │                            │
        │      ▲          └────┬────────────────┬─────┘                            │
        │      │  CSR          │ DMA AXIS        │ MAC-facing AXIS                  │
        │      │          ┌────▼─────┐      ┌────▼───────────────┐                 │
        │   CPU bus       │ MilanDMA │      │ MilanMAC           │                 │
        │                 │ tx/rx/ts │      │ LiteEthMACCore     │─► RGMII ─► PHY  │
        │                 │ §A.6     │      │ + s7rgmii PHY §A.7 │                 │
        │                 └────┬─────┘      └────────────────────┘                 │
        │                      ▼ memory (LiteDRAM on board / integrated RAM in sim) │
        └──────────────────────────────────────────────────────────────────────────┘
```

- **One core, MMU, Linux.** NaxRiscv RV64GC + Sv39 (RV32/Sv32 fallback), generated
  by SpinalHDL, integrated by LiteX. Boots the LiteX BIOS → OpenSBI → Linux.
- **The whole TSN datapath is in fabric** — `milan_datapath` (the §A.9 PS-less
  wrapper) owns classification, the credit-based shaper, PTP timestamping, the
  dest-MAC TCAM filter, and the hardware ADP advertiser. It is completely
  vendor-neutral (Verilator- and Yosys-verified; no Xilinx primitives inside).
- **Three clean boundaries** hang off the datapath: the **CSR** control plane
  (to the CPU), the **DMA** boundary (to memory), and the **MAC** boundary (to the
  1G MAC + RGMII PHY). Each is a separate, swappable block.
- **Open toolchain end-to-end** except the final Artix bitstream: LiteX generates
  the SoC, Verilator runs the RTL + boots the softcore, Yosys proves device
  portability. Only `--build` (Vivado place-&-route for xc7a100t) needs the vendor
  tool — and that step is currently blocked by device-support install (see §9).

## 2. The protocol stack (high level)

| Plane | Protocols | Where |
|-------|-----------|-------|
| **Media transport** | AVTP (IEEE 1722) AAF / CRF, 48/96/192 kHz | SW talker/listener (optional D5) + entity model |
| **Control / AVDECC** | ADP, AECP/AEM, ACMP, MVU (Milan) — IEEE 1722.1-2021 + Milan v1.2 | HW ADP advertiser + SW entity (AECP/ACMP/MAAP) |
| **Reservation** | SRP / MSRP / MVRP (802.1Q) | SW (future) + HW TCAM filter |
| **Timing** | gPTP / 802.1AS, PTP hardware clock | HW PHC + timestamping, SW `ptp4l` |
| **Shaping / QoS** | 802.1Qav CBS, 802.1Q PCP classification | HW (per-queue, only shaped queues) |
| **L2 / L1** | 802.3 1G MAC, RGMII PHY, dest-MAC filtering, RMON | HW MAC + fabric datapath |

The per-protocol **status and the test that validates each** is the subject of
[`PROTOCOL_VALIDATION_MATRIX.md`](PROTOCOL_VALIDATION_MATRIX.md). Scope decisions
(redundancy out; only 48/96/192 kHz; stereo talker + format-adaptive listener) are
recorded in [`MILAN_V12_DEPENDENCY_MATRIX.md`](MILAN_V12_DEPENDENCY_MATRIX.md) and
the entity model under `avdecc/`.

## 3. Status at a glance

| Layer | State | Evidence |
|-------|-------|----------|
| TSN datapath RTL (classify/CBS/PTP/filter/ADP) | ✅ complete + verified | 15 Verilator harnesses green; 18 Yosys tops |
| `milan_datapath` §A.9 PS-less wrapper | ✅ complete + verified | `tb/verilator/milan_dp` (11 checks); Yosys |
| NaxRiscv SoC (CPU + CSR + IRQ) | ✅ boots in sim | `sw/litex/evidence/naxriscv_sim_boot.log` |
| **CPU reads NIC ID="MILN" (M-A2)** | ✅ proven on softcore | `sw/litex/evidence/naxriscv_reads_MILN.log` |
| §A.6 DMA (AXIS↔memory, simple-mode CSRs) | ✅ assembled + elaborates | `milan_soc.py --with-dma` gateware export |
| §A.7 MAC + RGMII PHY (LiteEth s7rgmii) | ✅ assembled + elaborates | `milan_soc.py --with-mac` gateware export |
| **Full SoC (`--full`: NIC+DMA+MAC)** | ✅ elaborates + exports gateware | `milan_soc.py --full` |
| HW ADP advertiser | ✅ complete + verified | `tb/verilator/adp` (121 checks) |
| AVDECC SW (AECP/ACMP/MAAP/MVU) | 🟡 entity model + prior work | `avdecc/`, `docs/aem-and-aecp.md` |
| Linux driver (kl-eth) | 🟡 ABI defined | `sw/driver/README.md`, DT binding |
| Artix-7 bitstream + board bring-up | ⛔ blocked (Vivado device install) | see §9 |
| SRP/MSRP/MVRP, AVTP media datapath | ⏳ future | matrix rows |

---

## 4. Repository map (medium level)

```
hdl/                         vendor-neutral RTL (Verilator + Yosys verified)
  common/
    milan_datapath.sv        §A.9 PS-less wrapper — the fabric NIC (CSR+DMA+MAC-AXIS boundary)
    milan_top.sv             Zynq variant (PS + MAC in-line) — kept for the Zynq build
    milan_csr.sv (../csr/)   AXI4-Lite control plane (register map)
    tcam.sv, rx_mac_filter.sv  dest-MAC TCAM database + RX filter
    cdc_pulse/handshake.sv   open CDC primitives (replaced xpm_cdc_*)
  802_1q_traffic_shaper/     classify + 802.1Qav CBS (traffic_controller_802_1q)
  ptp_timestamp/             PHC + TX/RX timestamping (ptp_ts_top)
  adp/                       HW ADP advertiser (adp_advertiser) + TX arbiter
  eth_event_counter/         RMON counters (ethernet_events)
third_party/verilog-axis/    Forencich AXIS cores (vendored)
sw/
  litex/
    milan_soc.py             THE board SoC target (NaxRiscv + NIC + DMA + MAC)
    milan_sim.py             Verilator sim SoC (proves M-A2 on the softcore)
    platforms/alinx_ax7101.py  the AX7101 (xc7a100t) LiteX platform
    evidence/                captured sim boot + MILN-read logs
  dts/                       device tree (kl,dma-ether) + binding
  driver/                    kl-eth driver ABI contract
tb/verilator/                15 self-checking RTL harnesses (see its README)
syn/yosys/                   sv2v + Yosys device-portability check (18 tops, incl. ECP5)
docs/                        this file + the companions listed at the top
```

## 5. The three datapath boundaries (medium level)

`milan_datapath` (see the file header for the full port list) exposes exactly three
external boundaries; each is attached by a small LiteX submodule in `milan_soc.py`
via the shared `add_milan_datapath()` helper (`extra_ports`). This is the same
control/data/event pattern documented generically in
[`AXIS_CORES_ON_NAXRISCV.md`](AXIS_CORES_ON_NAXRISCV.md).

### 5.1 Control — `milan_csr` (AXI4-Lite)
- A 64 KB AXI4-Lite slave mapped in the CPU IO region at **`0x9000_0000`** (the
  register *offsets* `0x000..0x700` are unchanged from the Zynq build at
  `0x43C0_0000`; only the base is host-specific — see [`REGISTER_MAP.md`](REGISTER_MAP.md)).
- LiteX bridges the CPU Wishbone bus → AXI-Lite automatically (`Bus adapted`).
- **Proven on the softcore:** the BIOS `mem_read 0x90000000` returns `4d 49 4c 4e`
  ("MILN") + `0x00010003` (VERSION) — migration milestone **M-A2**.

### 5.2 Data — `MilanDMA` (§A.6, `--with-dma`)
- Three LiteX simple-mode DMA engines, each its own Wishbone master:
  - **TX** `WishboneDMAReader`: memory → `s_axis_tx` (frames to send)
  - **RX** `WishboneDMAWriter`: `m_axis_rx` → memory (received frames)
  - **TS** `WishboneDMAWriter`: `m_axis_ts` → memory (PTP timestamp metadata)
- Each has `with_csr=True` → a **simple-mode register block** (`base`, `length`,
  `enable`, `done`, `loop`, `offset`) auto-mapped in the LiteX CSR space. This is the
  ABI the Linux driver programs; it mirrors the Zynq `axi_dma` simple mode so the
  driver's DMA model is unchanged. (Scatter-gather / multi-queue = Option 6b, later.)
- On the board these target LiteDRAM; in sim/elaboration they target integrated RAM.

### 5.3 MAC — `MilanMAC` (§A.7, `--with-mac`)
- **LiteEthPHYRGMII** (Artix-7 `s7rgmii`, needs the 200 MHz IDELAYCTRL the CRG adds)
  + **LiteEthMACCore** (preamble/CRC/padding, PHY-width conversion) at 64-bit.
- A thin stream↔AXIS adapter connects the MAC core's `sink`/`source` to the
  datapath's `m_axis_mac_tx_*` / `s_axis_mac_rx_*`. The Milan datapath does *all*
  packet processing; the MAC core only does L1/framing.
- Board-gated details (exact `last_be`↔`tkeep`, MDIO link/speed status, RMON event
  pulses) are wired to sensible values for elaboration and validated on hardware.

### 5.4 Events — IRQ → PLIC
- `o_irq_csr` (link-change / PTP-TX-ready / RMON-rollover aggregate) plus the three
  DMA-done sources are collected by a LiteX `EventManager` into **one** NaxRiscv
  **PLIC** line (`milan_interrupt`); the driver demuxes via `milan_csr` `IRQ_STATUS` +
  the EventManager `pending` register. The device tree therefore lists a single
  interrupt on the LiteX build (four discrete GIC lines on Zynq) — generated per
  platform, see [`../sw/dts/README.md`](../sw/dts/README.md).

## 6. Build & run (medium level)

All commands assume the LiteX venv + toolchain from [`../sw/README.md`](../sw/README.md)
(`~/litex-milan/venv`, `JAVA_HOME=/usr/lib/jvm/java-17-openjdk`), run from a work dir
that is **not** the litex-repos parent.

```sh
# --- RTL verification (no Vivado, no LiteX) ---
cd tb/verilator && for d in cbs shaper_core cls ptp ptp_sync csr adp adp_tx \
  classifier queues tcam rx_filter cdc datapath milan_dp; do (cd $d && make) || break; done
cd syn/yosys && ./run.sh                       # 18 device-portability tops

# --- softcore in simulation (Verilator; proves the CPU + NIC CSR path) ---
./sw/litex/milan_sim.py --xlen 32              # build + boot; mem_read 0x90000000 => MILN

# --- the full FPGA SoC (elaborate + export gateware; no vendor tools) ---
./sw/litex/milan_soc.py --full                 # NIC + DMA + MAC + PHY, RV64
./sw/litex/milan_soc.py --full --xlen 32       # RV32 fallback (tighter fabric/timing)

# --- the Artix-7 bitstream (needs Vivado with Artix-7 device support — see §9) ---
./sw/litex/milan_soc.py --full --build         # place & route -> .bit
./sw/litex/milan_soc.py --full --build --load  # + program the board

# --- Linux (needs the board / a bitstream) ---
litex_json2dts_linux build/csr.json > milan.dts
sw/dts/milan_dt.py extract --platform litex build/csr.json --board sw/dts/boards/ax7101.json \
  > sw/dts/ir/milan-dt.litex.json
sw/dts/milan_dt.py gen sw/dts/ir/milan-dt.litex.json >> milan.dts   # kl,dma-ether (generated, real addrs)
# build Image + OpenSBI + Buildroot; boot; then bring the NIC up (ethtool/ptp4l/tc cbs)
```

## 7. How to extend (medium level, cookbook)

| To add… | Do this |
|---------|---------|
| a new CSR register | add it in `hdl/csr/milan_csr.sv` (write-case + read-mux + reset), extend `tb/verilator/csr`, document in `REGISTER_MAP.md` (the harness asserts they agree) |
| a new datapath stage | insert into `milan_datapath.sv` between the existing AXIS hops; add a `tb/verilator/*` harness; add it to `syn/yosys/run.sh` |
| a new AXIS core on the CPU | follow the 3-plane pattern in [`AXIS_CORES_ON_NAXRISCV.md`](AXIS_CORES_ON_NAXRISCV.md) |
| the LiteDRAM controller | add a `ddram` pad group to `platforms/alinx_ax7101.py` (needs the AX7101 DDR3 pinout) + `A7DDRPHY`/`MT41J256M16` in `_CRG`/`MilanSoC` (migration §A.3) |
| link/speed status (MDIO) | drive `i_i_mac_speed`/`i_i_link_up` from the LiteEth PHY status / a fabric MDIO master (§A.7 refine) |
| scatter-gather DMA | replace `MilanDMA`'s simple-mode engines with a descriptor-ring DMA (Option 6b) + rework the driver rings |
| an AVDECC protocol (AECP/ACMP/MAAP) | implement in the driver/daemon per the entity model (`avdecc/milan-v12-entity.json`); the HW path is the CSR + control-frame filter |

## 8. The CSR / DMA / IRQ ABI (medium level)

- **milan_csr** window `0x9000_0000` + offsets `0x000..0x700` — full table in
  [`REGISTER_MAP.md`](REGISTER_MAP.md). Groups: `0x000` ID/VERSION/CAP, `0x100` MAC,
  `0x200` RMON stats, `0x300` classifier, `0x400` CBS (per-queue), `0x500` PTP,
  `0x600` ADP, `0x700` TCAM.
- **DMA** simple-mode CSRs (LiteX CSR space, auto-mapped; names in `build/csr.csv`):
  `milan_dma_tx_{base,length,enable,done}`, `milan_dma_rx_{…}`, `milan_dma_ts_{…}`.
- **IRQ** → PLIC sources `tx-dma, rx-dma, ts-dma, csr` (DT `interrupts = <1..4>`).

---

## 9. What remains, and how to finish it (the roadmap)

Ordered; each item names the file(s) to touch and the test that closes it.

1. **Artix-7 Vivado device support** *(blocked, user action)* — install the AMD
   Artix-7 device data so `--full --build` can place & route. Recipe + status in the
   `vivado-zynq7000-not-installed` memory note; the AUR config is pre-staged with
   `Artix-7 FPGAs:1`. Closes: a real `.bit` + a resource report (§A.9 deliverable).
2. **LiteDRAM** *(needs AX7101 DDR3 pinout)* — add the `ddram` pads + `A7DDRPHY` +
   `MT41J256M16` (migration §A.3). Closes: BIOS DRAM memtest on the board (**M-A1**).
3. **Board bring-up of the CSR path** — program the bitstream, repeat the M-A2
   `mem_read` on hardware. Closes M-A2 on-board.
4. **DMA loopback + IRQs** — driver programs `milan_dma_*` base/length/enable; frame
   goes memory→MAC→(external loopback)→MAC→memory; DMA-done IRQs fire. Closes **M-A3**.
5. **Linux boot** — OpenSBI + kernel + Buildroot + the `kl,dma-ether` DT overlay.
   Closes **M-A4**.
6. **Driver bring-up** — `kl-eth` up: `ping` over RGMII, `ethtool -T` (PHC),
   `ptp4l` locks, `tc … cbs offload` shapes q0/q1. Closes **M-A5** = "Milan on FPGA".
7. **AVDECC protocols** — AECP/AEM enumeration, ACMP connect, MAAP, MVU, then
   SRP/MSRP/MVRP, then (optional) the AVTP media datapath. Each row in the
   [`PROTOCOL_VALIDATION_MATRIX.md`](PROTOCOL_VALIDATION_MATRIX.md) names its test.

Everything up to and including the **gateware export of the full `--full` SoC is
done and reproducible today** with the open toolchain; step 1 is the gate to the
first real bitstream, and steps 2–7 are the on-board bring-up sequence.
