# CSR verification harness (`milan_csr` AXI4-Lite control plane)

Self-checking [Verilator](https://verilator.org) harness for
[`hdl/common/csr/milan_csr.sv`](../../../hdl/common/csr/milan_csr.sv), the memory-mapped
control/status-register block that gives firmware a way to configure the
TSN datapath (the "memory-mapped configuration" called out in
[`REQUIREMENTS.md`](../../../REQUIREMENTS.md), `REQ-CSR-*`).

## Contents

- **[Run it](#run-it)** — One `make`, three self-checking harnesses over the same register block (legacy N=1 map, the `0x800` window against modelled engines, the same window against live ones). No vendor tools — the register block is a standalone AXI4-Lite slave. Says where the check count is printed rather than quoting a number that rots.
- **[What it checks](#what-it-checks)** — Eight families of assertion, from `ID`/`CAP` self-description through reset values, read-only enforcement, output wiring, IRQ write-1-to-clear and the PTP command strobes, ending with the ACMP bind-restore window driven against the live listener context. Also states the AXI pattern in use — combinational-ready and single-outstanding — so a master that drops `*VALID` on handshake still commits.
- **[Extending](#extending)** — The rule that keeps the ABI honest: a new register group is three edits (RTL, [`REGISTER_MAP.md`](../../../docs/reference/REGISTER_MAP.md), and a `ck(...)` here), because this harness *is* the executable contract for the CSR ABI.

## Run it

```
cd tb/verilator/csr
make            # verilate + build + run all three harnesses; each prints its
                # own live "checks: N   failures: N" tally and RESULT: PASS/FAIL
```

`make` builds and runs **three** self-checking harnesses against the same
register block:

| Harness | Shape under test |
|---|---|
| `sim_main.cpp` → `Vcsr_sim` | the legacy flat map at the `N=1` silicon shape, plus the `0x800` index-0 hard aliases and the out-of-range rule |
| `sim_win.cpp` → `obj_win/Vcsr_win` | the `0x800` indexed window at `N_LISTENERS_P=4`/`N_TALKERS_P=4` against **modelled** lane-K engines |
| `sim_live.cpp` → `obj_live/Vcsr_win_live` | the same window against **live** `KL_lwsrp_top` + `KL_acmp_lstn_ctx` (wrapper `csr_win_live.sv`) |

Each prints its own `checks: <n>   failures: 0` / `RESULT: PASS` line — that
printout is where the current count lives. No total is quoted here on purpose:
a hand-maintained count rots on the next register group, and the exit code is
the gate anyway.

No Xilinx tools required — `milan_csr.sv` is a standalone AXI4-Lite slave.

## What it checks

An AXI4-Lite master BFM (`sim_main.cpp`) exercises the register map
([`docs/reference/REGISTER_MAP.md`](../../../docs/reference/REGISTER_MAP.md)):

* **Identification / capabilities** — `ID = "MILN"`, `VERSION`, and `CAP`
  (num_queues, CBS/PTP/STATS feature bits, timestamp width) so the driver can
  self-describe.
* **Reset values** — MAC_CTRL, IFG, PHY reset, classifier map/queue map, PTP
  nominal increment, per-queue CBS idleSlope/enable defaults.
* **RO enforcement** — writes to `ID`/`MAC_STATUS` are ignored.
* **RW + output wiring** — SCRATCH, MAC control bits drive `o_mac_*`, station MAC
  reconstructs on `o_mac_addr`, per-queue CBS idleSlope drives
  `o_cbs_idle_slope_bps[q]`, CBS enable drives `o_cbs_enable`.
* **IRQ** — hardware event latch → `IRQ_STATUS`, masking → `o_irq`, and
  write-1-to-clear.
* **PTP command strobes** — `PTP_CMD` snapshot latches the live TOD into
  `PTP_TOD_RD`, load/adjust emit single-cycle apply pulses, and the command
  register reads back 0.
* **Statistics** — snapshot latches `i_stats[9]` into the read window; reset
  emits a pulse.
* **Channel-map RAM readback (`0x910` `CHMAP_SNAP` / `0x914` `CHMAP_LOOP`)** —
  split deliberately across two executables, because the property is a
  *capability*, not a value. `sim_win.cpp` elaborates `-GCHMAP_RDBK_P=3` and
  drives a modelled map RAM on the readback port: a written entry reads back
  through the *fabric* (not `0x908`'s shadow), and the three states that matter
  on a board with no audio pins — `mapped=1 fed=1`, `mapped=1 fed=0`
  (`LOOP_SUSPECT`, the mis-wired loopback), and unmapped — are distinguishable,
  as is a *measured* zero from the poison `0xDEADDEAD` that means "no
  measurement". Its negative control makes the modelled RAM go silent: the
  watchdog must report `timeout` and re-poison the data word rather than latch
  the bus. `sim_main.cpp` leaves `CHMAP_RDBK_P` at its default 0 — "no read
  port in this build", the state `milan_datapath` actually shipped in — and
  asserts that an arm is *refused* (`unsupported`), that no request reaches the
  fabric, and that the data word never becomes 0.
* **ACMP bind-restore (0x7A0, E1)** — staging-register RW (incl. the
  `0xA5C35A3C` feature-probe pattern at `0x7A0`), commit → held
  `o_acmp_rest_*` request with the staged record, busy/done/status readback
  through the engine ack. `sim_live.cpp` drives the LIVE
  `KL_acmp_lstn_ctx` end-to-end (inject → PRB_W_AVAIL, occupied/record-only
  refusals) and reads the E2 window words `0x860-0x868`
  (controller_entity_id + {flags, tuid}) back through the tbl port.

The AXI slave uses the combinational-ready, single-outstanding pattern, so a
compliant master that drops `*VALID` on handshake still commits every transfer.

## Extending

When new register groups are added (classifier PCP table, more PTP fields),
extend the offsets in both `hdl/common/csr/milan_csr.sv` and [`docs/reference/REGISTER_MAP.md`](../../../docs/reference/REGISTER_MAP.md), then
add the corresponding `ck(...)` assertions here. This harness is the executable
contract for the CSR ABI (`REQ-VER-04`).
