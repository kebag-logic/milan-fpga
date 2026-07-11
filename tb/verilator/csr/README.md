# CSR verification harness (`milan_csr` AXI4-Lite control plane)

Self-checking [Verilator](https://verilator.org) harness for
[`hdl/csr/milan_csr.sv`](../../../hdl/csr/milan_csr.sv), the memory-mapped
control/status-register block that gives the Linux driver a way to configure the
TSN datapath (the "memory-mapped configuration" called out in
[`REQUIREMENTS.md`](../../../REQUIREMENTS.md), `REQ-CSR-*`).

## Run it

```
cd tb/verilator/csr
make            # verilate + build + run (44 checks)
```

No Xilinx tools required — `milan_csr.sv` is a standalone AXI4-Lite slave.

## What it checks

An AXI4-Lite master BFM (`sim_main.cpp`) exercises the register map
([`docs/REGISTER_MAP.md`](../../../docs/reference/REGISTER_MAP.md)):

* **Identification / capabilities** — `ID = "MILN"`, `VERSION`, and `CAP`
  (num_queues, CBS/PTP/STATS feature bits, timestamp width) so the driver can
  self-describe.
* **Reset values** — MAC_CTRL, IFG, PHY reset, classifier map/queue map, PTP
  nominal increment, per-queue CBS idleSlope/enable defaults.
* **RO enforcement** — writes to `ID`/`MAC_STATUS` are ignored.
* **RW + output wiring** — SCRATCH, MAC control bits drive `o_mac_*`, station MAC
  reconstructs on `o_mac_addr`, per-queue CBS idleSlope drives
  `o_cbs_idle_slope[q]`, CBS enable drives `o_cbs_enable`.
* **IRQ** — hardware event latch → `IRQ_STATUS`, masking → `o_irq`, and
  write-1-to-clear.
* **PTP command strobes** — `PTP_CMD` snapshot latches the live TOD into
  `PTP_TOD_RD`, load/adjust emit single-cycle apply pulses, and the command
  register reads back 0.
* **Statistics** — snapshot latches `i_stats[9]` into the read window; reset
  emits a pulse.

The AXI slave uses the combinational-ready, single-outstanding pattern, so a
compliant master that drops `*VALID` on handshake still commits every transfer.

## Extending

When new register groups are added (classifier PCP table, more PTP fields),
extend the offsets in both `hdl/csr/milan_csr.sv` and `docs/REGISTER_MAP.md`, then
add the corresponding `ck(...)` assertions here. This harness is the executable
contract for the CSR ABI (`REQ-VER-04`).
