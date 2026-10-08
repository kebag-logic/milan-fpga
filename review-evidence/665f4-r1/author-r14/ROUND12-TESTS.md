[A560]

# Round 12 named feedback plants

Each plant compiles and fails the named observable at IF=1 and IF=2.
These 25 plants extend the standing campaign; the full campaign receipt is separate.

| Plant | Standing test | Required failure | IF=1/2 |
| --- | --- | --- | --- |
| `feedback-advertise-missing` | `SrpBinding.AdvertiseFeedbackIsDeferredAndSurvivesNoTalkerDeadline` | Advertise reaches ACMP | caught / caught |
| `feedback-failed-as-advertise` | `SrpBinding.FailedRegistrationReachesAcmpAndWithdrawalReprobes` | Failed flag reaches ACMP | caught / caught |
| `feedback-withdrawal-missing` | `SrpBinding.FailedRegistrationReachesAcmpAndWithdrawalReprobes` | withdrawal reaches ACMP | caught / caught |
| `feedback-sink-crossed` | `SrpBinding.RegistrationKeepsSinkAndInterfaceIdentity` | feedback keeps sink identity | caught / caught |
| `feedback-interface-suppressed` | `SrpBinding.RegistrationKeepsSinkAndInterfaceIdentity` | feedback uses configured interface | caught / caught |
| `feedback-repeated` | `SrpBinding.AdvertiseFeedbackIsDeferredAndSurvivesNoTalkerDeadline` | unchanged registration is delivered once | caught / caught |
| `feedback-kind-failed-lost` | `SrpFeedback.AdvertiseToFailedUpdatesTheSettledWireView` | current kind reaches ACMP | caught / caught |
| `feedback-kind-advertise-lost` | `SrpFeedback.FailedToAdvertiseUpdatesTheSettledWireView` | current kind reaches ACMP | caught / caught |
| `feedback-withdrawal-overwritten` | `SrpFeedback.WithdrawalThenRegistrationRetainsTheFirstEvent` | retained withdrawal reprobes | caught / caught |
| `feedback-intrapdu-lost` | `SrpFeedback.SinglePduWithdrawalThenRegistrationRetainsTheFirstEvent` | retained withdrawal reprobes | caught / caught |
| `feedback-expiry-lost` | `SrpFeedback.ExpiryThenRegistrationRetainsTheFirstEvent` | expiry retained before receive | caught / caught |
| `feedback-first-registration-lost` | `SrpFeedback.FirstRegistrationThenWithdrawalIsDeliveredInOrder` | retained withdrawal reprobes | caught / caught |
| `feedback-kind-order-lost` | `SrpFeedback.KindThenWithdrawalIsDeliveredInOrder` | kind precedes withdrawal | caught / caught |
| `feedback-supersession-lost` | `SrpFeedback.WithdrawalIsIsolatedAndSupersededEvenForAnIdenticalStream` | kind preserves settled state | caught / caught |
| `feedback-withdrawal-sink-crossed` | `SrpFeedback.WithdrawalIsIsolatedAndSupersededEvenForAnIdenticalStream` | retained withdrawal reprobes | caught / caught |
| `feedback-advertise-copy-lost` | `SrpFeedback.SinglePduKindReplacementsRemainContinuous` | kind preserves settled state | caught / caught |
| `feedback-failed-copy-lost` | `SrpFeedback.SinglePduKindReplacementsRemainContinuous` | kind preserves settled state | caught / caught |
| `feedback-identity-copy-stale` | `SrpFeedback.SinglePduIdentityMismatchThenRecoveryStillWithdraws` | retained withdrawal reprobes | caught / caught |
| `p11-supersession-kind-stale` | `SrpFeedback.IdenticalRebindAfterUndeliveredWithdrawalSettlesNoRsv` | retired kind cannot settle the new epoch | caught / caught |
| `p11-reset-withdrawal-lost` | `SrpFeedback.LinkResetWithdrawsTheSettledRegistration` | link reset withdraws registration | caught / caught |
| `p11-postwithdrawal-kind-overwrite` | `SrpFeedback.LaterKindAfterWithdrawalIsNotReported` | retained pre-withdrawal kind | caught / caught |
| `r10-feedback-ignores-pending` | `SrpFeedback.ReplacementAwaitingDeliveryGetsNoOldRegistration` | old registration cannot settle replacement | caught / caught |
| `r10-transient-refusal-forgotten` | `SrpFeedback.EarlierSinkTransientRefusalKeepsDeliveryAwake` | earlier refusal keeps delivery awake | caught / caught |
| `r10-feedback-allowance-quarter` | `SrpFeedback.DiscoveredWithdrawalMeasuresTheFundedPath` | measured feedback per sink allowance | caught / caught |
| `r10-feedback-allowance-eight` | `SrpFeedback.DiscoveredWithdrawalMeasuresTheFundedPath` | measured feedback per sink allowance | caught / caught |

The three `p11-*` source edits exactly match the review packet.
The prior intra-PDU plant now removes copied-state capture rather than a registrar visit.
Build failures do not satisfy the mutation oracle.
