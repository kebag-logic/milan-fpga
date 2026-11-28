Status: REVIEW READY for round 6 only. ETA: complete.

Candidate: `b4a1df4a0913d7a9b03c8ed0678a035ba2eda5d6`. Scope: the supplied Contents and octet-unit repair, adapted to the existing implementations. The new diff contains eight Contents descriptions and one corrected normative-document fragment. No firmware or gateware bytes change.

- Both complete CI gate blocks pass: boundary-unit naming (66 self-checks) and Contents (1501 self-checks, 764 reproduced cross-page anchors, final freshness check).
- USB-network tests pass 92,755 checks and four clock-source command cases. All 72 named planted defects are caught.
- Six fresh builds confirm Arty and both ALINX ELF/map-header identities against the same-pin #1004 comparison.
- Regenerated Arty logic, constraints and initialization match the retained route inputs. No reroute is required.
- [Source identity](receipts/source/source-identity.json) and [evidence carry](receipts/final-head-evidence.json) connect the measured inputs to this final head.

The [100 Mb/s egress ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7216971645) remains a dependency: #1004 supplies the grader first, then #1020 adds injection. It was not implemented or discharged in this round. Physical acceptance, attachment integration, broader required gates and independent re-review remain open. This file is executor readiness evidence, not approval or merge authorization. Nothing pushed or posted.

See [HANDOFF-r6.md](HANDOFF-r6.md) for preserved limitations and [receipts/INDEX.md](receipts/INDEX.md) for exact commands and hashes.
