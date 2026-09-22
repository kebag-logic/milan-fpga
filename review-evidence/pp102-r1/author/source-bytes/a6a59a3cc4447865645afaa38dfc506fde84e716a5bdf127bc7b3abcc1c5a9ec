<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# srp_decoder — KL_srp_decoder MRPDU vector-decode suite

Proves the SRP MRPDU vector decoder (`hdl/srp/KL_srp_decoder.sv`) against
[10 §3](../../docs/architecture/10_srp_engine.md) (F10.6/F10.7/F10.8, the
vector-value-k paragraph, the dual-EndMark framing rule and the Milan
§4.2.7.1.2 tolerance rules, tested per F09.4): `make` = build + run,
exit 0 = PASS, 113 checks.

Every MRPDU is hand-built **byte-exact** in the harness and every expected
event is an explicit hand-computed constant — the C++ never re-implements
the decoder. The stream is driven through the validator's rule-V9
pass-through face (`mrp_valid/data/last` + MSRP/MVRP select), honoring
`mrp_ready_o` (the decoder paces packed-byte drains at one event per cycle).

Covered:

- **THE +k regression pin**: the certified-bench Domain shape — 802.1Q
  §35.2.2.9's own worked example, `NumberOfValues = 2` from FirstValue
  `{SRclassID 5, prio 2, VID}` — class A surfaced as value 1 with priority
  3 and `evt_class_a_o` set, VID unchanged.
- Multi-value Talker Advertise range reconstruction: {unique_id, DA}
  increment together per value, TSpec/PCP/rank/accumulated_latency ride
  every value; Talker Failed FailureInformation (system id + code 1).
- Listener pairing through the sync-read three-packed RAM: all four
  four-packed declaration codes paired with their three-packed events,
  stream_id +k, no DA.
- MVRP VID decode (no AttributeListLength field), VID +k per value.
- **Dual-EndMark framing truth**: a PDU ending after the AttributeList
  EndMark alone is malformed — the already-emitted prefix stands.
- **AttributeListLength is counted, never trusted**: a lying declared
  length is flagged (`listlen_bad_o`, counted value 9 exposed) while
  EndMark framing carries the walk into the next message; PDU still ok.
- Tolerance per F09.4: truncation mid-FirstValue (no events, malformed),
  truncation mid-vector (3-value prefix emitted, malformed), bad
  AttributeLength (nothing emitted, next PDU decodes cleanly), a bad
  attribute mid-PDU (good first message emitted, fully-valid third message
  proven discarded), out-of-alphabet three-packed digit (> 215).
- **Per-application LeaveAll** (corrected §6.5 rule): an MSRP LeaveAll
  never strobes `la_mvrp_o` and vice versa; LeaveAll with
  `NumberOfValues = 0` consumes its FirstValue and emits no events.
- Explicit-EndMark-then-padding (min-frame pad bytes inert, one done).

Mutation-proven 2026-08-11 (backup/sed/run/restore):

| Mutation | Result |
|---|---|
| Domain `SRclassPriority` +k increment removed | 2 of 113 FAIL (A "+k prio 3", F prefix) |
| FourPacked extraction order flipped (MS-first → LS-first) | 5 of 113 FAIL (D/G/J/O declaration codes) |
| Talker/Listener DA +k increment removed | 4 of 113 FAIL (B DA range checks) |

All three restored; suite back to 113/113 PASS.
