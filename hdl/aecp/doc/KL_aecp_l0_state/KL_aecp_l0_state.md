# Entity: KL_aecp_l0_state
- **File:** `hdl/aecp/KL_aecp_l0_state.sv`
- **Spec:** IEEE 1722.1-2021 §7.5.1, §7.5.2, §9.2.7, §9.2.8

Entity-level ACQUIRE / LOCK state machine. Produces `status_o` combinationally so the response builder can latch the result on the same cycle as `hdr_i.hdr_valid`. No AXI-Stream interface — drives/reads `aecp_hdr_t` and `aecp_l0_state_t` directly.

---

## Ports

| Port | Dir | Type | Description |
|------|-----|------|-------------|
| `clk_i` | in | `wire` | 125 MHz clock |
| `rst_n` | in | `wire` | Active-low reset |
| `entity_id_i` | in | `wire [63:0]` | EUI-64, driven from top-level MAC |
| `hdr_i` | in | `aecp_hdr_t` | Parsed header from `KL_aecp_common_parser` |
| `tick_1khz_i` | in | `wire` | 1 kHz strobe from `KL_aecp_timers` |
| `cmd_done_i` | in | `wire` | Response TX done (from `KL_aecp_response_builder`) |
| `l0_state_o` | out | `aecp_l0_state_t` | Full L0 state struct (entity_id, locks, config) |
| `status_o` | out | `logic [4:0]` | Status for current command (combinational) |
| `reject_o` | out | `logic` | Command rejected — lock/acquire/bad-args (combinational) |

---

## Registers

| Name | Width | Description |
|------|-------|-------------|
| `acquired_r` | 1 | Entity is acquired |
| `acquiring_controller_id_r` | 64 | Controller holding the acquire |
| `locked_r` | 1 | Entity is locked |
| `locking_controller_id_r` | 64 | Controller holding the lock |
| `lock_timer_r` | 17 | Tick downcounter; reloaded to `LOCK_TIMER_TICKS_C` (60 000) on LOCK |
| `current_config_r` | 16 | Active configuration index |

---

## Combinational decision logic

Evaluated every cycle when `hdr_i.hdr_valid = 1`:

```
priority:
  1. w_block_acquired  → STATUS_ENTITY_ACQUIRED  (acquired by other ctlr, mutating cmd)
  2. w_block_locked    → STATUS_ENTITY_LOCKED    (locked by other ctlr)
  3. w_bad_config      → STATUS_BAD_ARGUMENTS    (SET_CONFIGURATION out of range)
  4. default           → STATUS_SUCCESS
```

**Exempt commands** (always allowed regardless of lock/acquire state):  
`ACQUIRE_ENTITY`, `LOCK_ENTITY`, `ENTITY_AVAILABLE`, `CONTROLLER_AVAILABLE`,  
`READ_DESCRIPTOR`, `GET_CONFIGURATION`, `GET_NAME`, `GET_SAMPLING_RATE`,  
`GET_CLOCK_SOURCE`, `GET_CONTROL`, `GET_AVB_INFO`, `GET_COUNTERS`,  
`GET_AUDIO_MAP`, `REGISTER_UNSOLICITED_NOTIFICATION`, `DEREGISTER_UNSOLICITED_NOTIFICATION`

---

## Sequential command handling

| Command | Action |
|---------|--------|
| `CMD_ACQUIRE_ENTITY` (u_flag=0) | Set `acquired_r`; latch `acquiring_controller_id_r` |
| `CMD_ACQUIRE_ENTITY` (u_flag=1, RELEASE) | Clear `acquired_r` if called by acquiring controller |
| `CMD_LOCK_ENTITY` (u_flag=0) | Set `locked_r`; latch `locking_controller_id_r`; reload `lock_timer_r` |
| `CMD_LOCK_ENTITY` (u_flag=1, UNLOCK) | Clear `locked_r` **only if** `controller_entity_id == locking_controller_id_r` |
| `CMD_SET_CONFIGURATION` | Update `current_config_r` if index < `NUM_CONFIGURATIONS_C`; else rejected by `w_bad_config` |

**Lock auto-expiry:** `lock_timer_r` decrements on every `tick_1khz_i` pulse while `locked_r = 1`. When it reaches zero, `locked_r` is cleared automatically (60 s timeout).

> **Stub:** `u_flag` is used as RELEASE/UNLOCK indicator pending full payload flag extraction from `KL_aecp_cmd_specific_extract`.
