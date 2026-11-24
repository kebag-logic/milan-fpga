Status: STOP: F2 disabled 8x8 grows by 1041 LUTs; exact equality is not met.
ETA: validation and packet complete; no active jobs. No remaining-work ETA is claimed for the unmet F2 resource requirements.

[A826] round 3, issue #979 / PR #987.
Local head `855529fe21fea685725a9edc4fe0a798154c6469`, branch `pf-loopbram-1`, target `dev-soft-core`.
Delta from `2e278379c1ae9ea09063b3e3cb183d0e8a3f0929`; base `3cda030c174b325e36c26af6420487ff91346d15`.

Three local commits:

- `c9c6e5ff225d266e05313885ceebefa60a4ae9b5` Fix optional loopback isolation and parent integration
- `a0f33d9026e96870192575bc138a684350f598bb` Preserve disabled scheduling and correct loopback page metadata
- `855529fe21fea685725a9edc4fe0a798154c6469` Keep the drain mutation anchored to copy scheduling

The mutation campaigns, enabled parent integration, retention defect, timestamp bound,
lead refusal, banners and wording findings have concrete fixes and exact-head receipts.
All executed regression gates pass. The 114-entry union includes one unchanged NOT RUN
calibration-report row. Selected enabled routes clear every required floor. Disabled
artifact and firmware-load byte identity pass. Enabled 8x8 allocation remains refused at
70.5 tiles; S14 remains open.

The disabled capture structure is repaired, but F2 remains OPEN: disabled 8x8 grows by 1041 LUTs, violating the owner no-growth rule. Exact equality is also unmet. Capture: 3961 FF and 4339 LUT at both commits. Queue: 406 FF at both commits, 1017 -> 1015 LUT (-2). The full-image results below are measured independently and do not waive the equality criterion.

| Shape | LUT base / head (delta) | FF base / head (delta) | BRAM tiles base / head (delta) | F7 / F8 mux delta |
|---|---:|---:|---:|---:|
| endstation_ax7101_1x1_tdm8 | 33792 / 33692 (-100) | 42649 / 42642 (-7) | 80 / 80 (+0) | +62 / +3 |
| endstation_ax7101_8x8 | 45199 / 46240 (+1041) | 53086 / 53051 (-35) | 99 / 99 (+0) | -14 / +3 |

The permitted F4 documentation outcome was used: five guards remain explicitly untested
in isolation. The new parent harness uses the production command core and real parent
transactions, without processor/mailbox execution. No hardware claim is made.

- [Finding dispositions and validation](REVIEW-READY.md)
- [Full updated PR body](PR-BODY.md)
- [Exact-head receipts and source hashes](receipts/INDEX.md)

No push, public comment, merge, board, bench or test-machine access occurred.
Remaining work is to remove the disabled 8x8 LUT growth and meet the exact leaf/image
equality criterion, followed by validation at the corrected head.
The manager owns publication. No reviewer approval or clean-lens ledger is claimed.
The clean checkout and all source hashes were rechecked after validation.

STOP: F2 disabled 8x8 grows by 1041 LUTs and exact disabled utilisation equality is not met.
