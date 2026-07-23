# Minimal Milan v1.2 talker — ACMP state machine + AECP streaming (design)

Reference truth (measure-don't-assume): every behavior below was extracted
from the pipewire module-avb Milan v1.2 implementation (the project's
normative reference) — `acmp-cmds-resps/acmp-milan-v12.c`,
`aecp-aem-cmds-resps/cmd-get-set-stream-info.c`, `cmd-start-stop-streaming.c`,
`cmd-register-unsolicited-notifications.c`, `reply-unsol-helpers.c`,
`stream.c` — plus docs/LWSRP_FPGA_ARCHITECTURE.md for the gating contract.
Wire message types are IEEE 1722.1-2021; semantics are Milan v1.2.

## The Milan v1.2 talker connection model (what surprised us)

Milan v1.2 does NOT use CONNECT_TX as talker-side connection bookkeeping.
The talker is **near-stateless in ACMP**:

- `CONNECT_TX_COMMAND` **is** Milan's `PROBE_TX_COMMAND` (§4.3.3.1, §5.5.4.1):
  the listener probes the talker for stream parameters. The talker ACTIVATES
  its stream source on the first probe and re-arms a **15 s freshness
  window** on every probe.
- The talker DEACTIVATES only when BOTH conditions lapse: no probe in 15 s
  AND no SRP Listener attribute registered for the stream (periodic sweep).
- `connection_count` in every talker response is **always 0** (the reference
  hard-codes it; listeners/controllers derive connection state elsewhere).
- `DISCONNECT_TX_COMMAND` (§5.5.4.2): always SUCCESS, zeroed stream fields,
  NO state change (not even deactivation).
- `GET_TX_CONNECTION_COMMAND` (§5.5.4.4): NOT_SUPPORTED for talkers — the
  existing KL_acmp_responder already does this correctly.

## Command/response matrix (talker-relevant)

### ACMP (multicast 91:E0:F0:01:00:00, subtype 0xFC, 70 B frames)

| Wire message (in) | Milan meaning | Guard | Response |
|---|---|---|---|
| CONNECT_TX_COMMAND (0) | PROBE_TX | talker_guid==EID else IGNORE; unique_id!=0 -> TALKER_UNKNOWN_ID | CONNECT_TX_RESPONSE (1), SUCCESS: live stream_id/dmac/vlan, count=0, clear FAST_CONNECT+STREAMING_WAIT flags; side effect: `probe_armed`, 15 s timer re-arm |
| DISCONNECT_TX_COMMAND (2) | unbind notification | same guards | DISCONNECT_TX_RESPONSE (3), SUCCESS, stream fields ZERO, count=0; NO state change |
| GET_TX_STATE_COMMAND (4) | state query | same guards | GET_TX_STATE_RESPONSE (5), SUCCESS: live stream_id/dmac/vlan, count=0, clear FAST_CONNECT+STREAMING_WAIT+SRP_REG_FAILED |
| GET_TX_CONNECTION_COMMAND (6) | n/a for talkers | — | NOT_SUPPORTED echo (already shipped, keep) |

Live stream parameters (single source of truth — MUST byte-match the AVTP
frames the AAF talker emits):
- `stream_id = {station_mac[47:0], talker_unique_id[15:0]}` — the reference
  formula (stream.c: mac<<16|index) and exactly what aaf_talker_i2s already
  puts on the wire (`{station_mac_i, 16'd0}`).
  **BUG FIXED BY THIS WORK: the current GET_STREAM_INFO reports
  stream_id = entity_id (02:00:00:FF:FE:...), which can NEVER match the
  AVTP stream — a listener binding on it would fail.**
- `stream_dest_mac / stream_vlan_id` = the CSR AAF group (`A_AAF_DMLO/DMHI`
  reset = MAAP-range 91:E0:F0:00:FE:01, `A_AAF_CTRL[27:16]` VID=2) — the
  same registers the framer reads; no second copy.

### AECP additions/corrections (Milan §5.4.2)

| Command | Milan rule | Fabric behavior |
|---|---|---|
| GET_STREAM_INFO (STREAM_OUTPUT) | §5.4.2.10.2, Tables 5.11/5.12: fixed 56 B payload; flags STREAM_FORMAT_VALID\|CONNECTED\|MSRP_ACC_LAT_VALID\|STREAM_ID_VALID\|STREAM_DEST_MAC_VALID\|STREAM_VLAN_ID_VALID always 1 (0xF6000000); pbsta=acmpsta=0; flags_ex.REGISTERING = declaring && listener_observed | Payload layout already shipped; fill LIVE values: stream_id (formula above), dest_mac, msrp_accumulated_latency (presentation offset, default 2 000 000 ns = the talker's TRANSIT), vlan_id, flags_ex |
| SET_STREAM_INFO (STREAM_OUTPUT) | §5.4.2.9: ONLY the MSRP_ACC_LAT_VALID sub-command is supported; any other requested sub-command -> NOT_SUPPORTED; while listener_observed -> STREAM_IS_RUNNING; range 0..0x7FFFFFFF else BAD_ARGUMENTS; response echoes flags | NEW dispatch: parse flags+msrp_lat from the command, update the presentation-offset register (feeds the AAF talker's timestamp TRANSIT), gate on listener_observed |
| SET_STREAM_INFO (STREAM_INPUT) | not implemented for inputs | NOT_SUPPORTED (no STREAM_INPUT descriptor anyway -> NO_SUCH_DESCRIPTOR path already covers) |
| START_STREAMING / STOP_STREAMING | §5.4.2.19/20: Stream-INPUT-only commands; **NOT_SUPPORTED on Stream Outputs** | NEW dispatch: NOT_SUPPORTED (status 11) echo. (Currently falls to default NOT_IMPLEMENTED — wrong status.) |
| REGISTER_UNSOLICITED_NOTIFICATION | §5.4.2.21: dedup by controller_id -> SUCCESS; store {controller_id, src MAC, next_seq=0}; table full -> NO_RESOURCES | Real 4-deep table (reference uses 16; 4 is plenty for the bench and bounded in fabric) replacing the accept-stub |
| DEREGISTER_UNSOLICITED_NOTIFICATION | clear the slot -> SUCCESS | ditto |
| Unsolicited pushes | on stream-output state change, send a full GET_STREAM_INFO response, u=1, UNICAST per registered controller with THAT controller's entity_id and its own per-controller unsolicited sequence_id++ (skip the controller that caused the change via a solicited command) | Minimal trigger set: probe_armed edge (activation/deactivation), presentation-offset change, listener_observed edge |

## Activation state machine (fabric, KL_acmp_responder evolves)

```
                 probe (valid PROBE_TX for uid 0)
   IDLE ────────────────────────────────────────► ARMED
    ▲     probe_timer := 15 s                       │ probe -> re-arm timer
    │                                               │
    └── timer expired && !listener_observed ────────┘
```

- `talker_active = ARMED || listener_observed` — exported to the datapath.
- Tick source: the existing 1 s `adp_tick_1s` (shared; already clock-true).
- `listener_observed` is an INPUT — the lwSRP hook per
  LWSRP_FPGA_ARCHITECTURE.md ("gate = talker declared && listener READY &&
  domain ok"; "PROBE_TX arms talker0"). Until lwSRP lands it is driven by a
  CSR override bit so the bench can pin the gate open.

## AAF gate (milan_datapath)

```
aaf_gate = cfg_aaf_enable && (cfg_aaf_bypass ? 1'b1 : talker_active)
```
- `cfg_aaf_bypass` (NEW, A_AAF_CTRL bit 1) **resets to 1** = today's
  behavior (enable -> stream always): flash-boot benches keep working and
  the Milan probe-gated mode is opt-in until the flow is silicon-proven,
  then the default flips.
- The talker's `TRANSIT_NS` localparam becomes an input driven by the
  presentation-offset register (SET_STREAM_INFO target, reset 2 000 000).

## CSR additions

- `A_AAF_CTRL[1]` = bypass (reset 1). `[0]` enable unchanged.
- `A_ACMP_TALKER = 0x66C` (RO): {probe_armed, talker_active,
  listener_observed(csr-or-lwsrp), probe_timer[7:0], unsol_registered[3:0],
  presentation_offset[…]} — exact packing in the RTL header.
- `A_ACMP_LOBS = 0x670` (RW): [0] listener_observed override (pre-lwSRP).
- NOTE: LWSRP_FPGA_ARCHITECTURE.md's CSR sketch (0x660-0x674) is STALE —
  0x660/0x664/0x668 are now AAF_FRAMES/AAF_PAIRS/ADP_DIAG. lwSRP's block has
  LANDED at `0x680`–`0x6A0` (in fabric).

## Explicitly out of scope (this increment)

> **UPDATE:** this "out of scope" list is from the original talker-SM
> increment. Since then **lwSRP**, **fabric MAAP**, and the **ACMP listener**
> have all LANDED in fabric (silicon-validated, per
> `docs/ARCHITECTURE_HW_SW_SPLIT.md` rev 2) — they are no longer out of scope.

- lwSRP itself (MSRP TA declare / Listener Ready registrar) — the
  `listener_observed` input is its socket. **(LANDED — see update above.)**
- STREAM_INPUT / listener side, BIND_RX/UNBIND_RX/GET_RX_STATE. **(ACMP
  listener has LANDED — see update above.)**
- MAAP dynamic allocation (static MAAP-range dmac from CSR). **(LANDED — fabric
  MAAP, see update above.)**
- GET_DYNAMIC_INFO (Milan §5.4.2.24) — la_avdecc enum passes without it;
  revisit if Hive complains.
- Talker counters STREAM_START/STREAM_STOP wiring into GET_COUNTERS
  (masks already advertised; values stay 0 this increment).

## Gates

Unit TB (acmp): probe->armed + response fields byte-exact vs a C++ model,
15 s expiry (tick-driven), listener_observed hold, disconnect no-op,
GET_TX_STATE live fields, unknown-uid/foreign-guid ignores. AECP TB:
SET_STREAM_INFO accept/reject matrix, STREAM_IS_RUNNING gate,
START/STOP -> NOT_SUPPORTED, unsolicited register/dedup/full/dereg +
push sequencing. milan_dp e2e: PROBE_TX through the real datapath ->
AAF frames on the MAC carry the probed stream_id/dmac/vlan; gate opens
only in probe mode (bypass=0) and closes on expiry; GET_STREAM_INFO
matches the AVTP header bytes. Then the standard yosys + full-regression
+ 3-seed sweeps + silicon drill (controller PROBE_TX from pw0, ADP census,
la_avdecc Milan=1 CLEAN re-cert).
