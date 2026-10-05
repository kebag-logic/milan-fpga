[R497] NEGATIVE - exact head a3ea8ffe16585270911705ffabd68ca5e17fc9e0

Independent first pass, recorded before reading prior public review findings.
All five lenses applied. Prior finding reconciliation and final packet remain pending.

R497-2-F1, MAJOR, Conformance / RTL / Robustness / Tests.
Artifact: sw/firmware/ctrl/adp/adp.c:110,148,165,216,248; scripts/restart_probe.c.
A deferred DEPARTING is overwritten by a new startup's TMR_DELAY expiry. With the send port full, advertise -> shutdown -> re-enable -> expiry -> recover sends AVAILABLE index 0 without the owed DEPARTING index 1. The public API has no restart serialization restriction. The positive deferred-send cases in test_adp.c finish the departure before restarting.
Required outcome: retain/serialize the owed departure and its index through restart; cover this ordering with backpressure and expiry.
Verification: receipts/restart-probe.log has two failed assertions; a broader model probe is being recorded next. This is the architecture part of the RTL lens, not a claim of a defect in the bus RTL.

R497-2-F2, MINOR, Docs.
Artifact: docs/design/MAILBOX_SPLIT.md:365.
The authoritative verification table reports 30 RTL / 28 firmware mutation arms, whereas the tables and locally completed campaigns report 44 / 37. Required outcome: update those figures to 44 and 37, or refer to the executable inventory without duplicating counts. This changes numerical evidence claims, so is not RESIDUE under the assignment.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #665 scope/rulings; REQUIREMENTS.md; mailbox.yaml; adp.c; adp_walk.cpp | R497-2 | a3ea8ffe16585270911705ffabd68ca5e17fc9e0 |
| RTL | UNCLEAN | KL_mbx*.sv; milan_soc.py; adp.c output-state architecture | R497-2 | a3ea8ffe16585270911705ffabd68ca5e17fc9e0 |
| Robustness | UNCLEAN | axil_checks.hpp; suite.hpp H0-H2/X2; test_adp.c; restart probe | R497-2 | a3ea8ffe16585270911705ffabd68ca5e17fc9e0 |
| Tests | UNCLEAN | generator/scope selftests; 44 RTL and 37 firmware mutants; co-simulation; restart probe | R497-2 | a3ea8ffe16585270911705ffabd68ca5e17fc9e0 |
| Docs | UNCLEAN | MAILBOX_SPLIT.md; MAILBOX_CONTRACT.md; ctrl and mbx READMEs; public evidence | R497-2 | a3ea8ffe16585270911705ffabd68ca5e17fc9e0 |

The registered AXI interface, sequence merge, owed-output poll, events-first access bounds and guards passed the repository's focused tests. Default-off source gating was examined relative to the merged dev parent. Final source identity and exact default-off structural comparison remain to be recorded. No full banks, hardware, hosted/act acceptance or candidate merge validation performed here.
