# Entity: KL_aecp_timers
- **File:** `hdl/aecp/KL_aecp_timers.sv`
- **Spec:** IEEE 1722.1-2021 §9; Milan v1.2 §5.4

Centralised timer source for the AECP pipeline. All periodic strobes originate here; other modules are purely combinational or edge-triggered on these pulses.

---

## Ports

| Port | Dir | Type | Description |
|------|-----|------|-------------|
| `clk_i` | in | `wire` | 125 MHz clock |
| `rst_n` | in | `wire` | Active-low reset |
| `ptp_ts_i` | in | `wire [63:0]` | gPTP timestamp — reserved, unused |
| `tick_1khz_o` | out | `logic` | 1-cycle pulse every 1 ms (125 000 cycles) |
| `lock_start_i` | in | `wire` | Reload lock downcounter to `LOCK_TIMER_TICKS_C` |
| `lock_clear_i` | in | `wire` | Stop and clear lock downcounter |
| `lock_expired_o` | out | `logic` | 1-cycle pulse when lock timer reaches zero |
| `counter_gate_o` | out | `logic` | 1-cycle pulse every 1 000 `tick_1khz_o` pulses (1 s) |
| `stale_tick_o` | out | `logic` | Controller staleness tick (= `tick_1khz_o`, simplified) |

---

## Sub-modules / counters

### 1 kHz generator
- 17-bit counter `ms_ctr_r`, reloads at `TICK_DIV_C - 1` = 124 999
- `tick_1khz_o` asserts for one cycle on reload → exact 1 ms period at 125 MHz

### Lock downcounter
- 17-bit `lock_ctr_r`, `lock_running_r` flag
- `lock_start_i` → reload to `LOCK_TIMER_TICKS_C` (17'd60 000) and start
- `lock_clear_i` → zero counter and stop (higher priority than start)
- Decrements once per `tick_1khz_o`; `lock_expired_o` pulses when `lock_ctr_r == 0`

### Counter gate
- 10-bit `gate_ctr_r`, reloads to `COUNTER_THROTTLE_TICKS_C` (10'd1 000) on each `tick_1khz_o`
- `counter_gate_o` pulses once per second — throttles `GET_COUNTERS` responses

### Staleness tick
- `stale_tick_o = tick_1khz_o` (simplified)
- TODO: gate per-controller against `STALE_TIMER_TICKS_C` when `KL_aecp_unsolicited_table` is implemented

---

## Constants (from `aecp_pkg.sv`)

| Constant | Value | Used by |
|----------|-------|---------|
| `LOCK_TIMER_TICKS_C` | `17'd60_000` | Lock downcounter reload |
| `COUNTER_THROTTLE_TICKS_C` | `10'd1_000` | Gate counter reload |
| `STALE_TIMER_TICKS_C` | `16'd30_000` | Future staleness tracking |
