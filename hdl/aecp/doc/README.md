# AECP / AEM Listener — Developer Reference

**Spec:** IEEE 1722.1-2021 §9 · Milan v1.2 §5.4  
**Target:** Artix-7 XC7A100T (`xc7a100tcsg324-1`) · 125 MHz  
**Package:** `hdl/aecp/aecp_pkg.sv`

---

## Pipeline overview

```
Ethernet RX (64-bit AXI-Stream, big-endian)
        │
        ▼
KL_aecp_packet_validator   — drop on bad message_type / CDL < 20
        │ valid frames only
        ▼
KL_aecp_common_parser      — extract aecp_hdr_t, check entity_id
        │ hdr_o.hdr_valid pulse + AXI passthrough
        ├──────────────────────────────────────────┐
        ▼                                          ▼
KL_aecp_cmd_specific_extract              KL_aecp_l0_state
  (acquire/lock/read-desc fields)   ◄──── (lock/acquire SM, config index)
        │                                          │ status_o / reject_o
        ▼                                          │
KL_aecp_accessor ──► KL_aecp_aem_store             │
        │ (BRAM descriptor lookup)                 │
        ▼                                          │
KL_aecp_aem_dyn_mux  (live field overlay)          │
        │                                          │
        └────────────► KL_aecp_response_builder ◄──┘
                              │
                    KL_aecp_egress_mux
                    KL_aecp_unsolicited_table ──► unsolicited TX
                    KL_aecp_vu_milan          ──► vendor-unique TX
```

`KL_aecp_timers` feeds `tick_1khz_o` to `KL_aecp_l0_state` and `KL_aecp_unsolicited_table`.  
`KL_aecp_nv_overlay` sits between `KL_aecp_aem_store` and the external NV device.

---

## AXI-Stream beat layout (64-bit, big-endian)

All modules expect `TDATA_WIDTH_P = 64`. The `axi_stream_if` defaults to 32;
instantiate with `#(.TDATA_WIDTH_P(64))`. In-module `tdata` accesses above
bit 31 are guarded with `/* verilator lint_off SELRANGE */`.

| Beat | Bytes | Fields |
|------|-------|--------|
| 0 | 0–7 | `[63:48]` EtherType 0x22F0 · `[47:40]` subtype 0xFB · `[39:36]` h/ver · `[35:32]` message_type · `[31:27]` status · `[26:16]` CDL · `[15:0]` target_eid[63:48] |
| 1 | 8–15 | `[63:16]` target_eid[47:0] · `[15:0]` ctlr_eid[63:48] |
| 2 | 16–23 | `[63:16]` ctlr_eid[47:0] · `[15:0]` sequence_id |
| 3 | 24–31 | `[63]` u_flag · `[62:48]` command_type · `[47:0]` cmd-specific start |
| 4+ | 32+ | Command payload (ACQUIRE/LOCK flags, descriptor fields…) |

---

## Key package constants

| Constant | Value | Meaning |
|----------|-------|---------|
| `AVTP_ETYPE_C` | `0x22F0` | AVTP EtherType |
| `AECP_SUBTYPE_C` | `0xFB` | AECP subtype |
| `MILAN_PROTOCOL_ID_C` | `48'h001BC50AC100` | Milan VU OUI |
| `LOCK_TIMER_TICKS_C` | `17'd60_000` | Lock auto-expiry (60 s @ 1 kHz) |
| `STALE_TIMER_TICKS_C` | `16'd30_000` | Stale controller threshold |
| `COUNTER_THROTTLE_TICKS_C` | `10'd1_000` | GET_COUNTERS gate (1 s) |
| `MAX_UNSOLICITED_CTLR_C` | `16` | Unsolicited registry depth |
| `NUM_CONFIGURATIONS_C` | `3` | Milan configs (48/96/192 kHz) |

---

## Message types

| Mnemonic | Value |
|----------|-------|
| `MSG_AEM_COMMAND` | 0 |
| `MSG_AEM_RESPONSE` | 1 |
| `MSG_VENDOR_UNIQUE_COMMAND` | 6 |
| `MSG_VENDOR_UNIQUE_RESPONSE` | 7 |

## Status codes

| Mnemonic | Value |
|----------|-------|
| `STATUS_SUCCESS` | 0 |
| `STATUS_NOT_IMPLEMENTED` | 1 |
| `STATUS_NO_SUCH_DESCRIPTOR` | 2 |
| `STATUS_ENTITY_LOCKED` | 3 |
| `STATUS_ENTITY_ACQUIRED` | 4 |
| `STATUS_BAD_ARGUMENTS` | 7 |
| `STATUS_NO_RESOURCES` | 8 |
| `STATUS_IN_PROGRESS` | 9 |
| `STATUS_INVALID_COMMAND` | 10 |
| `STATUS_PROTOCOL_ERROR` | 11 |

## Command types (subset)

| Mnemonic | Value |
|----------|-------|
| `CMD_ACQUIRE_ENTITY` | 0 |
| `CMD_LOCK_ENTITY` | 1 |
| `CMD_READ_DESCRIPTOR` | 4 |
| `CMD_SET_CONFIGURATION` | 6 |
| `CMD_GET_CONFIGURATION` | 7 |
| `CMD_SET_NAME` | 16 |
| `CMD_REGISTER_UNSOLICITED_NOTIFICATION` | 36 |
| `CMD_DEREGISTER_UNSOLICITED_NOTIFICATION` | 37 |

---

## Implementation status

| Module | Status | Notes |
|--------|--------|-------|
| `KL_aecp_packet_validator` | ✅ complete | |
| `KL_aecp_l0_state` | ✅ complete | |
| `KL_aecp_timers` | ✅ complete | |
| `KL_aecp_common_parser` | 🔧 stub | Beats 4+ extracted as TODO |
| `KL_aecp_cmd_specific_extract` | 🔧 stub | |
| `KL_aecp_accessor` | 🔧 stub | |
| `KL_aecp_aem_store` | 🔧 stub | BRAM inference pending |
| `KL_aecp_nv_overlay` | 🔧 stub | |
| `KL_aecp_aem_dyn_mux` | 🔧 stub | |
| `KL_aecp_unsolicited_table` | 🔧 stub | |
| `KL_aecp_vu_milan` | 🔧 stub | |
| `KL_aecp_response_builder` | 🔧 stub | |
| `KL_aecp_egress_mux` | 🔧 stub | |

---

## Lint

```bash
./scripts/run-verilator-lint.sh           # all 13 modules
./scripts/run-verilator-lint.sh --strict  # + -Wall
```

All modules pass Verilator 5.048 `--lint-only --sv`.

---

## Testbench quick-start

**T0 — Vivado XSIM** (run from repo root):
```bash
cd tb/utests/aecp/kl-aecp-packet-validator
vivado -mode tcl -source tb_top.tcl
```

**T1 — behave offline** (no DUT binary needed):
```bash
pip install behave
behave tests/features --tags ~@T2
```

**T1 — with Verilator DUT** (once C++ harness is implemented):
```bash
./scripts/run-dut-sim.sh KL_aecp_packet_validator &
behave tests/features --tags ~@T2
```

See `tests/README.md` for the full three-tier strategy.
