# R509-2 primary-clause audit

Head: `8fb296e3e02985aee27ef04cb08278836b734a14`.
The four source document identities are in `standards-identities.json`.
Licensed documents and extracted text remain in unpublished scratch storage.
This audit paraphrases the examined clauses; it does not reproduce them.

| Candidate artifact | Primary authority examined | Result |
|---|---|---|
| FR_NFR.md:367, MAAP PROBE/conflict row | IEEE 1722-2016 B.3.2/Table B.7, B.3.3/Table B.8, B.3.4.2, B.3.5.5, B.3.6.6 | State-dependent conflict processing and restart are assigned to the state machine; constants remain assigned to the constants table. The received conflicting-PROBE event and DEFEND transmission action retain their separate references. Probe spacing remains strictly between 500 and 600 ms, with three retransmissions. |
| FR_NFR.md:368, MAAP announcement/reallocation row | IEEE 1722-2016 B.3.2/Table B.7, B.3.3/Table B.8 and B.3.4.1 | Loss/retry now cites the transition authority. Announcement spacing remains strictly between 30 and 32 seconds. No numeric DEFEND-response maximum is invented. |
| FR_NFR.md:360, listener timing row | IEEE 1722.1-2021 6.2.2.5; Milan v1.2 5.6.2, 5.6.4.1, Table 5.54, 5.6.4.5.1-.4 | Received AVAILABLE validity is 1..31 in two-second units. Milan's transmitted value 10 does not replace the received field. The 2-second minimum supplies a 200 ms project-budget ceiling; connection actions relate to Milan's 200 ms ACMP timeout, yielding 20 ms. Both exceed the proposed 10 ms service allowance. |
| FR_NFR.md:403,411; MAILBOX_SPLIT.md:345 | Milan v1.2 5.6.4.1 and Table 5.54 | Each matching bound sink must be processed. One receipt/original-expiry start covers discovery, resulting connection state, and the last resulting TX commit. State handoff and delayed event publication cannot restart the allowance. Normative waits remain separately measured. |
| FR_NFR.md:422 | Milan v1.2 5.6.4.5.1 | Undiscovered AVAILABLE first checks GM/domain; matching input saves interface/index, arms received validity, commits discovered state and triggers connection discovery. |
| FR_NFR.md:423 | Milan v1.2 5.6.4.5.2 | Discovered AVAILABLE rejects interface mismatch. Rising index refreshes validity; non-rising index first triggers departure, then checks GM/domain before rediscovery or loss. The candidate does not incorrectly apply the restart-only GM check to every fresh advertisement. |
| FR_NFR.md:424 | Milan v1.2 5.6.4.5.3 | Matching-interface DEPARTING stops aging and triggers the connection departure; another interface is ignored. |
| FR_NFR.md:425,426 | Milan v1.2 5.6.4.5.4 and Table 5.54 | Original aging expiry commits loss and connection departure. Undiscovered DEPARTING is ignored. A stray expiry is a robustness injection into a normative impossible cell and must not invent a departure. |
| FR_NFR.md:361-363 | Milan v1.2 5.5.2.3/Table 5.26, 5.4.3.4; IEEE 1722.1-2021 9.3.2.6 | Rechecked the unchanged 200 ms ACMP and 240/250 ms AECP/MVU distinctions. The 120 ms IN_PROGRESS cadence remains hypothetical, not newly enabled. |
| FR_NFR.md:369; ieee8021q.md:138 | Milan v1.2 4.2.7.1.1/Table 4.3 | Rechecked join 180..240 ms, leave 4500..7500 ms, periodic 900..1500 ms and LeaveAll 9.5..15.5 s. The unchanged conservative mandatory ceiling is 18 ms. |

The new H-DISC checks include received validity 1, 10 and 31, unchanged-state input completion, all matching sinks, restart ordering, interface and GM/domain mismatch, departure, expiry and stale expiry. Global requirements also retain reset, wrap, CPU stalls, full rings, NVM work, both adapters and every supported placement/shape. Delaying listener processing can fail H-DISC while advertiser checks remain green. These are future integration-test obligations, not implemented timing instrumentation.

No normative clause or numeric timing change outside the round-2 correction was inferred. Earlier unaffected conclusions remain intact.
