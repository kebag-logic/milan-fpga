[A560]

# Round 10 tests and discriminating plants

The complete campaign runs these composition/bound plants at IF=1 and IF=2. Each planted variant must compile and fail its named runtime observable. A compiler refusal is not a kill. Earlier binding tests remain in the campaign; the obsolete invalid-VID busy-loop expectation is replaced by parking and sleep.

| Plant | Test artifact / case | Named failure |
| --- | --- | --- |
| `binding-delivery-missing` | `sw/firmware/ctrl/test/srp_binding.hpp:85` / `SrpBinding.BindIsDeferredAndKeepsEverySinkAndInterface` | binding delivered |
| `binding-synchronous` | `sw/firmware/ctrl/test/srp_binding.hpp:85` / `SrpBinding.BindIsDeferredAndKeepsEverySinkAndInterface` | callback only queues the binding |
| `binding-poll-adds-access` | `sw/firmware/ctrl/test/srp_binding.hpp:85` / `SrpBinding.BindIsDeferredAndKeepsEverySinkAndInterface` | binding poll makes no mailbox access |
| `binding-interface-lost` | `sw/firmware/ctrl/test/srp_binding.hpp:85` / `SrpBinding.BindIsDeferredAndKeepsEverySinkAndInterface` | binding delivered |
| `binding-sink-lost` | `sw/firmware/ctrl/test/srp_binding.hpp:85` / `SrpBinding.BindIsDeferredAndKeepsEverySinkAndInterface` | binding delivered |
| `binding-refusal-dropped` | `sw/firmware/ctrl/test/srp_binding.hpp:118` / `SrpBinding.RefusedReceiveRetriesAfterRecoveryOrExpiry` | binding delivered |
| `binding-owed-retry-dropped` | `sw/firmware/ctrl/test/srp_binding.hpp:143` / `SrpBinding.OwedTransmissionRetriesAfterCommit` | binding delivered |
| `binding-unbind-lost` | `sw/firmware/ctrl/test/srp_binding.hpp:160` / `SrpBinding.UnbindCancelsPendingAndWithdrawsAcceptedBinding` | unbind supersedes pending bind |
| `binding-replacement-lost` | `sw/firmware/ctrl/test/srp_binding.hpp:180` / `SrpBinding.ReplacementSupersedesPendingIdentity` | stream identity delivered |
| `binding-pending-sleeps` | `sw/firmware/ctrl/test/srp_binding.hpp:118` / `SrpBinding.RefusedReceiveRetriesAfterRecoveryOrExpiry` | pending binding keeps service awake |
| `binding-count-overflow` | `sw/firmware/ctrl/test/srp_binding.hpp:311` / `SrpBinding.AttachmentRefusesMissingRoomAndShapeWithoutPartialBinding` | ctrl_app_attach_srp |
| `binding-poll-overflow` | `sw/firmware/ctrl/test/srp_binding.hpp:311` / `SrpBinding.AttachmentRefusesMissingRoomAndShapeWithoutPartialBinding` | ctrl_app_attach_srp |
| `binding-reattach-recurses` | `sw/firmware/ctrl/test/srp_binding.hpp:311` / `SrpBinding.AttachmentRefusesMissingRoomAndShapeWithoutPartialBinding` | recompose before replacing the attached adapter |
| `srp-bound-event` | `sw/firmware/ctrl/test/srp_app.cpp:94` / `EventReceiveAndTransmitPollFitTheirMeasuredBounds` | SRP event bound |
| `srp-bound-receive` | `sw/firmware/ctrl/test/srp_app.cpp:94` / `EventReceiveAndTransmitPollFitTheirMeasuredBounds` | SRP refused receive bound |
| `srp-bound-poll-transmit` | `sw/firmware/ctrl/test/srp_app.cpp:94` / `EventReceiveAndTransmitPollFitTheirMeasuredBounds` | SRP transmitting poll bound |
| `srp-bound-poll` | `sw/firmware/ctrl/test/srp_app.cpp:94` / `EventReceiveAndTransmitPollFitTheirMeasuredBounds` | SRP retained receive poll bound |
| `srp-bound-tx-record` | `sw/firmware/ctrl/test/srp_app.cpp:94` / `EventReceiveAndTransmitPollFitTheirMeasuredBounds` | SRP maximum TX record bound |
| `srp-bound-rx-record` | `sw/firmware/ctrl/test/srp_app.cpp:94` / `EventReceiveAndTransmitPollFitTheirMeasuredBounds` | SRP maximum RX record bound |
| `srp-bound-pass` | `sw/firmware/ctrl/test/srp_app.cpp:94` / `EventReceiveAndTransmitPollFitTheirMeasuredBounds` | SRP complete pass bound |
| `feedback-advertise-missing` | `sw/firmware/ctrl/test/srp_binding.hpp:245` / `SrpBinding.AdvertiseFeedbackIsDeferredAndSurvivesNoTalkerDeadline` | Advertise reaches ACMP |
| `feedback-failed-as-advertise` | `sw/firmware/ctrl/test/srp_binding.hpp:272` / `SrpBinding.FailedRegistrationReachesAcmpAndWithdrawalReprobes` | Failed flag reaches ACMP |
| `feedback-withdrawal-missing` | `sw/firmware/ctrl/test/srp_binding.hpp:272` / `SrpBinding.FailedRegistrationReachesAcmpAndWithdrawalReprobes` | withdrawal reaches ACMP |
| `feedback-sink-crossed` | `sw/firmware/ctrl/test/srp_binding.hpp:291` / `SrpBinding.RegistrationKeepsSinkAndInterfaceIdentity` | feedback keeps sink identity |
| `feedback-interface-suppressed` | `sw/firmware/ctrl/test/srp_binding.hpp:291` / `SrpBinding.RegistrationKeepsSinkAndInterfaceIdentity` | feedback uses configured interface |
| `feedback-repeated` | `sw/firmware/ctrl/test/srp_binding.hpp:245` / `SrpBinding.AdvertiseFeedbackIsDeferredAndSurvivesNoTalkerDeadline` | unchanged registration is delivered once |
| `binding-park-keeps-old` | `sw/firmware/ctrl/test/srp_binding.hpp:219` / `SrpBinding.ParkedReplacementRetiresThePreviouslyAcceptedBinding` | parking retires the old accepted binding |
| `binding-invalid-retries` | `sw/firmware/ctrl/test/srp_binding.hpp:193` / `SrpBinding.PermanentRefusalParksAndDoesNotBlockAnotherSink` | permanent refusal allows sleep |
| `binding-invalid-upper-bound` | `sw/firmware/ctrl/test/srp_binding.hpp:193` / `SrpBinding.PermanentRefusalParksAndDoesNotBlockAnotherSink` | permanent refusal is visible |
| `binding-park-never-clears` | `sw/firmware/ctrl/test/srp_binding.hpp:193` / `SrpBinding.PermanentRefusalParksAndDoesNotBlockAnotherSink` | replacement clears parking |
| `srp-term-fixed` | `sw/firmware/ctrl/test/srp_app.cpp:149` / `Srp.PollTermsAreMeasuredSeparatelyThroughRealCallbacks` | poll fixed term is funded independently |
| `srp-term-transmit-count` | `sw/firmware/ctrl/test/srp_app.cpp:149` / `Srp.PollTermsAreMeasuredSeparatelyThroughRealCallbacks` | poll transmit count is funded independently |
| `srp-term-interface-count` | `sw/firmware/ctrl/test/srp_app.cpp:149` / `Srp.PollTermsAreMeasuredSeparatelyThroughRealCallbacks` | poll fixed term is funded independently |
| `srp-term-send-cost` | `sw/firmware/ctrl/test/srp_app.cpp:149` / `Srp.PollTermsAreMeasuredSeparatelyThroughRealCallbacks` | real send callback maximum |
| `srp-term-event-record` | `sw/firmware/ctrl/test/srp_app.cpp:195` / `Srp.PassFundsEveryEventRecordAndBothMaximumReceives` | pass event records are funded independently |
| `srp-term-rx-count` | `sw/firmware/ctrl/test/srp_app.cpp:195` / `Srp.PassFundsEveryEventRecordAndBothMaximumReceives` | pass receive count is funded independently |
| `srp-term-pass-poll` | `sw/firmware/ctrl/test/srp_app.cpp:195` / `Srp.PassFundsEveryEventRecordAndBothMaximumReceives` | pass funds the independently measured poll envelope |
| `srp-poll-extra-read` | `sw/firmware/ctrl/test/srp_app.cpp:149` / `Srp.PollTermsAreMeasuredSeparatelyThroughRealCallbacks` | one link read per interface |
| `srp-send-extra-read` | `sw/firmware/ctrl/test/srp_app.cpp:149` / `Srp.PollTermsAreMeasuredSeparatelyThroughRealCallbacks` | real send callback has only the TX record accesses |

The seven changed/new cases cover: permanent VID 0, 4095 and 65535; clearing on replacement/unbind; retiring an accepted binding despite transient refusal; Advertise registration surviving more than 10 seconds with peer refresh; Failed registration and withdrawal/reprobe; sink/interface isolation; separately funded poll and pass terms. The two-sink retirement variation covers a second refused sink after pending work is already present. The loop-poll helper removes duplicate fixture plumbing.

`srp_cost_probe.hpp:16` wraps lwSRP transmit only in the test arm and passes a maximum-length padded PDU to the real firmware send callback. It measures every callback access, requires both participants on every interface, and separately exercises reset and retained-receive branches. No firmware send callback or mailbox driver is replaced.

## Independent review packet

The exact `probe_tk_registered.hpp` and `probe_invalid_vid.hpp` are appended only in a disposable test copy. Both pass at IF=1/2. The six TSV plants and eight Python plants are tested at both counts; 27 non-equivalent cases are caught. Replacing MBX_N_IF with 1 is identical at IF=1 and is recorded as equivalent, not detected. The standing `srp-term-interface-count` plant subtracts one interface and is detectable at both counts. `ROUND10-REVIEW-PROBES.json` lists every outcome.

## Sanitizer controls

The inherited A0 source-count control passes unplanted under GCC and Clang, each plain and with AddressSanitizer. Its `acmp-init-too-many-sources` plant fails the source-count assertion without an overflow. SRP access and composition suites pass with AddressSanitizer at IF=1/2 under both compilers; the final two-sink parking fixture is rerun in all four combinations. The SRP build now forwards the sanitizer setting, and executable symbols confirm instrumentation.

## Measured bound terms

| Term | IF=1 | IF=2 | Method |
| --- | ---: | ---: | --- |
| Fixed poll branch envelope | 4 | 8 | Common link reads plus separately measured reset and retained-RX increments |
| Actual participant calls / sends | 2 / 2 | 4 / 4 | Real callbacks, each padded to the channel maximum |
| Accesses per maximum real send | 383 | 383 | Every actual callback access counted |
| Poll envelope | 770 | 1540 | Independent fixed and send contributions |
| Full event-record allowance | 56 | 56 | Eight actual LINK records |
| Two maximum receive allowance | 770 | 770 | Two actual records, readiness reads, and separately measured refusal-clock alternative |
| SRP pass envelope | 1596 | 2366 | Event + receive + independently measured poll |
| Application feedback allowance | 64 | 64 | At most 16 sinks, clock + seed + timer rearm on withdrawal |
| Four-module application pass | 3192 | 4041 | Shared event record reads counted once |

Reset and retained reception are alternative paths. These conservative sums do not claim simultaneous realization in one pass. CPU work and external callbacks remain outside the mailbox count.
