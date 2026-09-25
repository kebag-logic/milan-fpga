# CSR verification harness (`milan_csr` AXI4-Lite control plane)

Self-checking [Verilator](https://verilator.org) harness for
[`hdl/common/csr/milan_csr.sv`](../../../hdl/common/csr/milan_csr.sv), the memory-mapped
control/status-register block that gives firmware a way to configure the
TSN datapath (the "memory-mapped configuration" called out in
[`REQUIREMENTS.md`](../../../REQUIREMENTS.md), `REQ-CSR-*`).

## Contents

- **[Run it](#run-it)** -- Default builds, generated fixtures, and exit-code validation.
- **[What it checks](#what-it-checks)** -- Register behavior and modeled handshake coverage.
- **[Extending](#extending)** -- Keep the register map and executable checks aligned.

## Run it

```
cd tb/verilator/csr
make            # build and run every default leg
make reset-bits # run only the generated SRP reset fixture
make clean      # remove every build directory
```

`make` runs these builds against the same register block:

| Source and executable | Shape under test |
|---|---|
| `sim_main.cpp`: `obj_dir/Vcsr_sim` | `arty_current` headers; flat map, `N=1` aliases, out-of-range rules |
| `sim_main.cpp`: `obj_100m/Vcsr_sim100` | Same headers; frequency-derived resets at 100 MHz |
| `sim_win.cpp`: `obj_win/Vcsr_win` | `arty_4x4` headers; 4x4 indexed window against modeled engines |
| `sim_gptp.cpp`: `obj_gptp/Vcsr_gptp` | `ax7101_8x8` headers; fabric gPTP publication enabled |
| `sim_main.cpp`: `obj_pps/Vcsr_pps` | `arty_current` headers; PPS enabled with `PPS_WIDTH_CYC` |
| `sim_main.cpp`: `obj_reset/Vcsr_reset` | Generated `arty_current` fixture; both SRP admission reset bits set |

`fixtures/reset_bits.yaml` declares the reset overrides.
`tb/common/gen_declaration_fixture.py` validates them through the real builder.
Its headers live under `obj_reset/fixture/gen`.
The harness independently expects `CSR_SRP_RESET_BITS=3u`.

Each executable reports its current results.
The command's exit code is the gate: zero means success.
No vendor tools are required for this standalone AXI4-Lite slave.

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
* **ACMP bind-restore (0x7A0, E1)**: `sim_main.cpp` stages records.
  It checks held requests, acknowledgements, and busy/done/status readback.
  The harness supplies acknowledgements directly; no live engine runs here.

The AXI slave uses the combinational-ready, single-outstanding pattern, so a
compliant master that drops `*VALID` on handshake still commits every transfer.

## Extending

When new register groups are added (classifier PCP table, more PTP fields),
extend the offsets in both `hdl/common/csr/milan_csr.sv` and [`docs/reference/REGISTER_MAP.md`](../../../docs/reference/REGISTER_MAP.md), then
add the corresponding `ck(...)` assertions here. This harness is the executable
contract for the CSR ABI (`REQ-VER-04`).
