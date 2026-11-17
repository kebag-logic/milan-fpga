# Saved individual mutant runs

These are expected failing mutant executions from the earlier session, not a completed final-head campaign.

| Configuration folder | Plant | Observed failing words |
|---|---|---|
| plants-srp1 | `talker-notice-declaration-missed` | [FAIL] Talker.DeclarationAndWithdrawalAreNoticed: a declaration is noticed |
| plants-srp1 | `talker-notice-every-declared-source` | [FAIL] Talker.TypeSwapIsNoticed: a Talker Failed withdrawn is noticed; [FAIL] Talker.TypeSwapIsNoticed: a swap lwSRP refuses is not noticed until it is made |
| plants-srp1 | `talker-notice-not-taken` | [FAIL] SrpGate.F936AProbeAndItsExpiryEachNoticeTheSource: a probe's declaration notices its source; [FAIL] SrpGate.F936AProbeAndItsExpiryEachNoticeTheSource: the SRP delivery takes SRP's record; [FAIL] SrpGate.F936AProbeAndItsExpiryEachNoticeTheSource: the probe's expiry notices its source |
| plants-srp1 | `talker-notice-record-dropped` | [FAIL] Talker.DeclarationAndWithdrawalAreNoticed: a declaration is noticed; [FAIL] Talker.DeclarationAndWithdrawalAreNoticed: a withdrawal is noticed |
| plants-srp1 | `talker-notice-record-kept` | [FAIL] SrpGate.F936AProbeAndItsExpiryEachNoticeTheSource: the SRP delivery takes SRP's record; [FAIL] SrpGate.F936AProbeAndItsExpiryEachNoticeTheSource: the probe window's periodic declarations notice nothing |
| plants-srp1 | `talker-notice-refused-swap-noticed` | [FAIL] Talker.TypeSwapIsNoticed: a swap lwSRP refuses is not noticed until it is made; [FAIL] Talker.TypeSwapIsNoticed: a type swapped in place is noticed |
| plants-srp1 | `talker-notice-reset-forgets-what-was-shown` | [FAIL] Talker.ResetNoticesNothingUnchanged: a source a reset declares again unchanged is not noticed |
| plants-srp1 | `talker-notice-swap-missed` | [FAIL] Talker.TypeSwapIsNoticed: a type swapped in place is noticed |
| plants-srp1 | `talker-notice-vid-missed` | [FAIL] Talker.AdoptedDomainVidIsNoticed: a declared Talker carrying another VID is noticed |
| plants-srp1 | `talker-notice-vid-on-every-domain` | [FAIL] Talker.AdoptedDomainVidIsNoticed: a Domain that keeps the VID notices nothing |
| plants-srp1 | `talker-notice-withdrawal-missed` | [FAIL] Talker.DeclarationAndWithdrawalAreNoticed: a withdrawal is noticed |
| plants-srp2 | `talker-notice-declaration-missed` | [FAIL] Talker.DeclarationAndWithdrawalAreNoticed: a declaration is noticed |
| plants-srp2 | `talker-notice-every-declared-source` | [FAIL] Talker.TypeSwapIsNoticed: a Talker Failed withdrawn is noticed; [FAIL] Talker.TypeSwapIsNoticed: a swap lwSRP refuses is not noticed until it is made |
| plants-srp2 | `talker-notice-not-taken` | [FAIL] SrpGate.F936AProbeAndItsExpiryEachNoticeTheSource: a probe's declaration notices its source; [FAIL] SrpGate.F936AProbeAndItsExpiryEachNoticeTheSource: the SRP delivery takes SRP's record; [FAIL] SrpGate.F936AProbeAndItsExpiryEachNoticeTheSource: the probe's expiry notices its source |
| plants-srp2 | `talker-notice-record-dropped` | [FAIL] Talker.DeclarationAndWithdrawalAreNoticed: a declaration is noticed; [FAIL] Talker.DeclarationAndWithdrawalAreNoticed: a withdrawal is noticed |
| plants-srp2 | `talker-notice-record-kept` | [FAIL] SrpGate.F936AProbeAndItsExpiryEachNoticeTheSource: the SRP delivery takes SRP's record; [FAIL] SrpGate.F936AProbeAndItsExpiryEachNoticeTheSource: the probe window's periodic declarations notice nothing |
| plants-srp2 | `talker-notice-refused-swap-noticed` | [FAIL] Talker.TypeSwapIsNoticed: a swap lwSRP refuses is not noticed until it is made; [FAIL] Talker.TypeSwapIsNoticed: a type swapped in place is noticed |
| plants-srp2 | `talker-notice-reset-forgets-what-was-shown` | [FAIL] Talker.ResetNoticesNothingUnchanged: a source a reset declares again unchanged is not noticed |
| plants-srp2 | `talker-notice-swap-missed` | [FAIL] Talker.TypeSwapIsNoticed: a type swapped in place is noticed |
| plants-srp2 | `talker-notice-vid-missed` | [FAIL] Talker.AdoptedDomainVidIsNoticed: a declared Talker carrying another VID is noticed |
| plants-srp2 | `talker-notice-vid-on-every-domain` | [FAIL] Talker.AdoptedDomainVidIsNoticed: a Domain that keeps the VID notices nothing |
| plants-srp2 | `talker-notice-withdrawal-missed` | [FAIL] Talker.DeclarationAndWithdrawalAreNoticed: a withdrawal is noticed |
| plants-aecp | `app-output-notice-as-an-input` | [FAIL] App.SrpDeclarationChangeIsItsStreamOutputsNotice: a declaration changed notifies its STREAM_OUTPUT's GET_STREAM_INFO to every registered controller |
| plants-aecp | `app-output-notice-dropped` | [FAIL] App.SrpDeclarationChangeIsItsStreamOutputsNotice: a declaration changed notifies its STREAM_OUTPUT's GET_STREAM_INFO to every registered controller |
| plants-aecp | `app-output-notice-kept` | [FAIL] App.SrpDeclarationChangeIsItsStreamOutputsNotice: the bridge raises every STREAM_OUTPUT the delivery took; [FAIL] App.SrpDeclarationChangeIsItsStreamOutputsNotice: a declaration changed notifies its STREAM_OUTPUT's GET_STREAM_INFO to every registered controller; [FAIL] App.SrpDeclarationChangeIsItsStreamOutputsNotice: a pass with no record notifies nothing; [FAIL] App.SrpDeclarationChangeIsItsStreamOutputsNotice: a source the record does not name is notified nothing |
| plants-aecp | `app-output-notice-next-source` | [FAIL] App.SrpDeclarationChangeIsItsStreamOutputsNotice: a declaration changed notifies its STREAM_OUTPUT's GET_STREAM_INFO to every registered controller; [FAIL] App.SrpDeclarationChangeIsItsStreamOutputsNotice: a source the record does not name is notified nothing |
