# CBS verification harness (IEEE 802.1Qav credit-based shaper)

A self-checking [Verilator](https://verilator.org) harness for
`hdl/ieee8021q/ts/credit_based_shaper.sv`. It answers the
REQUIREMENTS.md concern that *"the math behind the CBS logic is a little too
complicated, propose something to verify and run it."*

## Run it

```
cd tb/verilator/cbs
make          # verilate + build + run
```

No Xilinx tools are needed - `credit_based_shaper.sv` is pure RTL (no XPM/DSP
primitives are actually instantiated; the `(* use_dsp *)` attribute is a hint).
Requires `verilator >= 5.0` and a C++17 compiler. Exit code is `0` on pass,
non-zero on any mismatch, so it drops into CI directly.

## What it checks

The harness drives the **unmodified** DUT and compares it, every cycle, against
two independent reference models in `cbs_ref_model.h`:

| Model | Purpose |
|-------|---------|
| `FixedPointRef` | Bit-exact replica of the RTL's own Q16 integer arithmetic, its pipeline stages, AND the sequential slope engine (via `SlopeEngineRef`). `DUT.credit == FixedPointRef.credit` proves the RTL implements the arithmetic it was written to implement. |
| `IdealRef` | The same 802.1Qav credit FSM in floating point with the *exact* idle/send rates (cadence-aligned with the engine). `\|DUT - IdealRef\|` is the quantization error of the fixed-point representation (asserted <= 1 byte). |

### The slope engine mirror (STRICT pairing)

Since 2026-07-11 the DUT derives `idle_slope_per_cycle_r` /
`send_slope_per_byte_r` with a **sequential slope engine**: one serial
restoring divider on a fixed 100-cycle cadence (sample config at cnt 0, 48
iterations per divide, commit both results atomically at cnt 99). The old
per-cycle combinational divides cost ~2.3K LUTs per queue and are gone.
`SlopeEngineRef` in `cbs_ref_model.h` mirrors that engine **state-for-state**,
and the harness compares the DUT slope registers against it **every cycle**,
including reset warm-up (slopes read 0 until the first commit, 99 cycles after
reset release) and mid-run reconfiguration transitions. Convergence asserts
additionally pin the committed values to the exact SystemVerilog `/` results
after every long stable-config run. If you change the engine's state timing in
the RTL you MUST update `SlopeEngineRef` in the same commit, and vice versa.

`cbs_ver_wrap.sv` exposes the DUT's internal `credit` and the engine-committed
slope registers via cross-module references so the arithmetic is checked
directly, not just through the 1-bit `allow_transmit_o` output.

### Scenarios

1. **Idle accumulation** - credit climbs at idleSlope and saturates at `HI_CREDIT`; engine convergence asserted.
2. **Transmit drain** - credit falls at sendSlope, saturates at `LO_CREDIT`, `allow_transmit` deasserts.
3. **Empty-queue reset** - positive credit with no frames snaps to 0.
4. **Negative-credit recovery** - negative credit with no frames climbs back to 0 (not snapped).
5. **Randomized stress** - 50 000 cycles of random `queue_has_data/is_transmitting/is_granted/bytes_sent`; the DUT must track `FixedPointRef` exactly.
6. **100 Mbit/s config** - re-checks the slope terms with `is_1g = 0`; engine convergence asserted.
7. **Strict-priority bypass** (`shaped = 0`, REQ-CBS-02) - always eligible, credit parked at 0.
8. **Back-pressure accrual** (REQ-CBS-04) - granted but not transmitting keeps accruing to `HI_CREDIT`.
9. **Live reconfiguration** (REQ-CBS-01) - idleSlope/hi/lo reprogrammed mid-run; DUT tracks the reference across the change (the new slope commits within two engine passes, at most 200 cycles) and saturates at the new `HI_CREDIT`; engine convergence asserted.

## Configuration

The queue-under-test config lives in `cbs_ver_wrap.sv` parameter defaults and is
mirrored in `sim_main.cpp:mk()` defaults (queue-0 / Class-A @1G: `idleSlope =
500 Mbit/s`, `HI = +761`, `LO = -761`, `clk = 100 MHz` - i.e. the values
`ethernet_packet_pkg.sv` computes for queue 0). Change both to sweep another
queue/link config.

## Notes surfaced by this harness

* The DUT is **bit-exact** to its intended arithmetic and, for the queue-0
  config, has **zero** quantization error vs the ideal (the rates divide evenly).
  Precision is only at risk for idleSlope values that don't divide
  `clk*8` / `link_rate` evenly - sweep the config to quantify those.
* The pre-existing `tb/utests/802_1q_traffic_shaper/tb_credit_based_shaper.sv`
  no longer matches the DUT (it omits the `is_granted_i` port added later) and is
  not self-checking; this harness supersedes it for regression.
* The harness verifies a **single** CBS instance. Multi-queue arbitration
  (`traffic_shaping_core.sv`) has its own harness in `tb/verilator/shaper_core`.
