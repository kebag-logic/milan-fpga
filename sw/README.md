# `sw/` — boot one RISC-V core with the Milan NIC + driver

A **configurable, single-core** software/SoC bring-up: one NaxRiscv core running
Linux, with the Milan TSN NIC memory-mapped and its `kl-eth` driver bound via the
device tree. This is the smallest bootable slice of
[`docs/FULLY_FPGA_RISCV_MIGRATION.md`](../docs/FULLY_FPGA_RISCV_MIGRATION.md).

```
   milan_soc.py  ──build──▶  bitstream + LiteX BIOS      (1 core + DDR + UART + Milan NIC)
        │                          │
        │ --csr-json               ▼
        ▼                    OpenSBI ─▶ Linux (RV64GC) ─▶ Buildroot rootfs
   milan.dtsi  ────overlay────────────────┘  │
   (kl,dma-ether)                            ▼
                                     kl-eth driver binds ─▶ eth0 up (NAPI/XDP/PTP/ethtool)
```

| File | What |
|------|------|
| [`litex/milan_soc.py`](litex/milan_soc.py) | Configurable LiteX target: **1× NaxRiscv** (RV64GC, `--xlen 32` fallback) + DDR + UART + the Milan datapath as a peripheral (CSR @ `0x43C0_0000`, DMA, 4 IRQs → PLIC). |
| [`dts/milan.dtsi`](dts/milan.dtsi) | The `kl,dma-ether` device-tree node the driver binds to. |
| [`dts/bindings/kl,dma-ether.yaml`](dts/bindings/kl,dma-ether.yaml) | Normative DT binding (the DT requirements, `FR-DT-*`). |
| [`driver/README.md`](driver/README.md) | The `kl-eth` platform driver (NAPI/XDP/PTP/ethtool, `FR-DRV-*`) and its DT match. |

## Build & boot (needs LiteX + the AX7101 board)

```sh
# 0. prereqs: LiteX (enjoy-digital/litex + pythondata-cpu-naxriscv), a RISC-V linux
#    toolchain, Buildroot; the Milan RTL (../hdl) + vendored cores (../third_party)
#    + the verilog-ethernet MAC. See migration plan §A.1.

# 1. build the SoC (single core) + bitstream
cd litex
./milan_soc.py --build            # RV64GC, 1 core; add --load to program the board
./milan_soc.py --xlen 32 --build  # RV32 fallback if fabric/timing is tight
./milan_soc.py --no-milan --build # bare SoC smoke test (BIOS + DRAM memtest, no NIC)

# 2. Linux + rootfs (linux-on-litex-vexriscv drives NaxRiscv via --cpu-type naxriscv):
#    build Image + OpenSBI + Buildroot; generate the base DT from the SoC:
#      litex_json2dts_linux build/csr.json > milan.dts
#    then overlay the NIC node:
#      cat ../dts/milan.dtsi >> milan.dts   (or /include/ it)  # kl,dma-ether

# 3. boot over serial, then bring the NIC up:
#      ip link set eth0 up && udhcpc -i eth0
#      ethtool -T eth0        # PHC + HW timestamping advertised   (FR-DRV-P/E)
#      ethtool -S eth0        # RMON counters from the CSR stats
#      ptp4l -i eth0 -m       # gPTP lock
#      tc qdisc add dev eth0 ... cbs offload 1   # shape q0/q1  (kl,shaped-queues)
```

## Configurability
- **Cores:** `--cpu-count 1` here (single core). The same target scales to SMP by
  raising it (see `NFR-SCOUT-*`); the driver's per-queue NAPI already spreads work.
- **ISA width:** `--xlen 64` (default, standard Linux userspace) or `--xlen 32`.
- **NIC present:** `--no-milan` builds a bare SoC for board/DRAM bring-up first.
- **MAC target:** the RTL `MAC_TARGET` param (T2.1) — `XILINX` on the Artix build,
  `GENERIC` for open flows / sim.

## Status
`milan_soc.py` is the *configuration* (syntax-checked); the actual build/boot needs
the LiteX toolchain + the AX7101 board (not present in this repo's CI). The Milan
RTL it instantiates is all Verilator-verified (`tb/verilator/`, 14 harnesses) and
Yosys device-portable (`syn/yosys/`). The `milan_datapath` wrapper (milan_top minus
the Zynq PS) is the one remaining RTL glue to add (migration §A.9).
