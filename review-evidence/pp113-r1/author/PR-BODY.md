[A280]

Closes #113

A latency-only Talker refresh now sends an unsolicited GET_STREAM_INFO response to registered controllers when it changes the addressed Stream Input's accumulated-latency latch. An unchanged refresh sends none; unrelated sinks remain quiet.

Milan v1.2, Section 5.4.5.2 requires the Table 5.22 notifications asynchronously when entity state changes. Directly checked in the consolidated final specification dated 2023-11-30, printed pages 62–63. Relevant excerpt from the GET_STREAM_INFO row:

> Sent when one of these pieces of information changes:
> • MSRP accumulated latency (Stream Input only)

The registrar compares each matching sink's previous latch on the actual attribute write and registers a notification-only strobe. It travels through the existing per-descriptor pending path. Registration, failure and latency changes on that same write coalesce into one event. The strobe does not drive the applicant or ACMP event router. No new rate limit or processor top-level port is added.

Response tests send real Talker JoinIn refreshes to two settled streams, one Advertise and one Failed. The harness gathers the real published latency with zero ingress delay. It checks the complete response, exact notification count, unchanged refresh silence and other-sink isolation. Distinct values, bit 31, zero and all ones exercise the full 32-bit latch. Removing the latency trigger must fail the named exact-count check, with golden and restored controls passing.

F06.13, the Section 06 live-event list, the SRP latch contract, the interface event catalog and REQ-NOT-003 now name the implemented trigger. Its original-document coverage marker is historical and remains unchanged.

Default-shape OOC area, using `syn/ooc/protocol_processor_ooc.tcl` on the complete 8-input / 8-output processor, reference part `xc7a100tfgg484-2` and 10 ns clock:

| Resource | Base `a8f8ce81` | Change | Delta |
|---|---:|---:|---:|
| Slice LUTs | 28,649 | 28,643 | -6 |
| Registers | 31,095 | 31,123 | +28 |
| RAMB36 / RAMB18 / DSP | 23 / 2 / 4 | 23 / 2 / 4 | 0 |

The changed SRP listener instance adds 73 LUTs and 8 registers. Whole-processor remapping accounts for the difference from the total; the small total LUT decrease is not a saving attributed to the trigger. Both builds have negative post-synthesis OOC slack at 10 ns (-10.089 ns base, -8.192 ns change). No routed timing or hardware claim.

Processor head: `29840136bb2d21bc0fbe92c7c533368f40837ff6`.

| Validation | Result |
|---|---|
| Every processor workflow gate, run locally | rc 0 |
| Full bank | 33 suites, 1,009,045 checks, zero failures |
| Processor-top responses | 2,074 checks; focused GI 614 checks |
| Retained mutations | 14/14 detected by named checks; golden/restored 614 checks each |
| Lint and portability, including response-memory mapping | rc 0 |
| Documentation, traceability and NVM figure gates | rc 0 |
| Default-shape baseline/candidate OOC recipe | both rc 0 |

The latency-trigger mutant builds successfully and then fails all four changed-latency exact-count checks, reporting zero notifications. The unchanged-refresh and unrelated-sink cases pass on the unmodified implementation.

Parent consumer checks used dev `573f0052a0e4412e81f0845438fcec2086ce5d55` with locally committed gitlinks: control `9947af735f2228c7780c44ba98eadb368f5efd04` at processor `a8f8ce81`, candidate `dd8b228b1c1949b10af3b98aab398265477c0775` at this head. All seven commands return rc 0 at both pins, and both consumer runs pass 371 checks with zero failures. The same four front-end ratchet findings are retained. There is no failing command attributable to either the old pin gap or this change. Both builder runs explicitly leave one historical resource-calibration arm unrun because its reference placement report is absent; this shared limitation is recorded, not counted as hardware evidence. The parent remains clean at the local candidate commit; nothing was pushed.
