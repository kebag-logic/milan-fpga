# Standards and contract receipt

The local standards were extracted directly into temporary storage.
No extracted standards pages are included in this packet.

| Source | SHA-256 |
|---|---|
| Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf | `6bb902be1c1de8c44f4c4c583a645b0b37e0b2dac27870486ce229e68ce3bba8` |
| 1722-2016.pdf | `ba20762d444e6f7795ffc000bcaf6144e9618eff81cadd867863ed58000f8a8c` |
| 1722.1-2021.pdf | `ad7b822008c1b78bce8af1470f1ace177a22344aa48c0da939066d6db9a65b9c` |

Milan v1.2 Annex B.1.1, PDF page 141, states 0.25 seconds.
The project interprets that duration as a minimum.
Annex B.1 discusses a separate five-second media-clock holdover.
IEEE 1722-2016 4.4.4.7 describes uncertainty on clock discontinuities.
It leaves stabilization time implementation-dependent.

The release rule comes from issue #396 decision 5855792297.
The implementation evidence is read-only:
`hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:188` combines PHC
settime/adjtime, fabric discontinuity and GM-identity events.
Line 199 reloads the holdover on every event.
Line 211 combines lack of sync, holdover and the live event.
The rule therefore anchors at the final event before clearing.
Sync requalification receives no additional deadline extension.

The #117 silicon record describes GM adoption followed by a PHC step.
The unchanged public cycle transcription is rerun separately.
Its printed prose describes the reviewed starting head, not the corrected head.
Its numeric sweep remains evidence for the per-event holdover behavior.
No simulation or physical result is claimed from that transcription.

Other scope references read: README release-roadmap and invariant;
REQUIREMENTS section 8; CONTRIBUTING; AGENTS; docs/README;
CODE_QUALITY governing rule and relevant host-code/test contracts;
TESTING sections 6, 6b and 6d; testing methodology;
FR_NFR NFR-REL-01/02; BUILDING cold-soak finding;
MILAN_COMPLIANCE_MATRIX timing holds; tests/README torture tier;
release planner, feature, step definitions and mutation driver;
baremetal_uart_smoke console grading; GM_LOSS_RECOVERY;
and the cited #117 silicon evidence.
The issue body and all eleven comments were read, along with both complete
round-3 public reports and the current PR body.
