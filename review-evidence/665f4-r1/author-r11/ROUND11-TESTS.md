[A560]

# Round 11 standing checks

| Artifact | Change |
|---|---|
| `sw/firmware/ctrl/srp/srp_mbx.h:34` | Per-interface, per-sink continuous kind and first-withdrawal latch. |
| `sw/firmware/ctrl/srp/srp_mbx.c:515` | Capture complete wire events, expiry and reset; retain the event prefix until binding retirement. |
| `sw/firmware/ctrl/app/ctrl_app_srp.c:61` | Retire old feedback on accepted intent, preserve pending guards, deliver kind before withdrawal. |
| `sw/firmware/ctrl/acmp/acmp.h:420` | Public, authorized settled-kind view entry and Table 5.23/5.30 interpretation. |
| `sw/firmware/ctrl/acmp/acmp.c:1132` | Guard the new entry; update failure view without changing the state machine. |
| `sw/firmware/ctrl/app/ctrl_app.h:72` | Six accesses per sink cover initial registration followed by withdrawal; wrap the attach comment. |
| `sw/firmware/ctrl/test/srp_feedback.hpp:4` | Eleven temporal integration cases, wire flags, sink/interface isolation and funded-path measurements. |
| `sw/firmware/ctrl/test/srp_binding.hpp:272` | Check Failed at the first delivery, before later polling could repair a wrong initial kind. |
| `sw/firmware/ctrl/test/test_acmp.cpp:751` | Unit checks for kind notification, idempotence and invalid states; add the entry to reentry checks. |
| `sw/firmware/ctrl/test/test_acmp_mbx.cpp:1231` | Include the temporal cases in every SRP composition run. |
| `sw/firmware/ctrl/test/acmp_mutants.py:356` | Two new ACMP plants; keep the pre-existing withdrawal plant specific to its own entry. |
| `sw/firmware/ctrl/test/srp_mutants.py:786` | Thirteen new feedback plants; adapt earlier plants to the event fields without weakening their oracles. |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:202` | Include all four named review plants in the IF=1 repeat bank. |
| `sw/firmware/gtest/coverage.ratchet:5` | Generator-only ratchet growth; all 22 files remain 100% after unchanged exclusions. |
| `sw/firmware/ctrl/README.md:134` | Composition event model, authorized ACMP view contract and revised aggregate bounds. |
| `sw/firmware/ctrl/srp/README.md:53` | Observation boundaries, atomic replacement, withdrawal retention, retirement and standing evidence. |
| `docs/design/MAILBOX_SPLIT.md:715` | Recalculate the six-access feedback allowance and every four-module timing row. |

The tests use actual mailbox ingress and the composition poll. The two kind
cases observe GET_RX_STATE_RESPONSE flags. Eleven new integration tests and one
new core test have 15 new named plants. Existing reentry plants also exercise
the newly listed ACMP entry. The earlier Failed-registration plant now fails
at first delivery. All new SRP plants run at both interface counts.

| Standing test / artifact | Planted defect | Required failing observable |
|---|---|---|
| `SrpFeedback.AdvertiseToFailedUpdatesTheSettledWireView` (`sw/firmware/ctrl/test/srp_feedback.hpp:36`) | `feedback-kind-failed-lost` | current kind reaches ACMP |
| `SrpFeedback.FailedToAdvertiseUpdatesTheSettledWireView` (`sw/firmware/ctrl/test/srp_feedback.hpp:52`) | `feedback-kind-advertise-lost` | current kind reaches ACMP |
| `SrpFeedback.WithdrawalThenRegistrationRetainsTheFirstEvent` (`sw/firmware/ctrl/test/srp_feedback.hpp:63`) | `feedback-withdrawal-overwritten` | retained withdrawal reprobes |
| `SrpFeedback.SinglePduWithdrawalThenRegistrationRetainsTheFirstEvent` (`sw/firmware/ctrl/test/srp_feedback.hpp:74`) | `feedback-intrapdu-lost` | retained withdrawal reprobes |
| `SrpFeedback.ExpiryThenRegistrationRetainsTheFirstEvent` (`sw/firmware/ctrl/test/srp_feedback.hpp:85`) | `feedback-expiry-lost` | expiry retained before receive |
| `SrpFeedback.FirstRegistrationThenWithdrawalIsDeliveredInOrder` (`sw/firmware/ctrl/test/srp_feedback.hpp:104`) | `feedback-first-registration-lost` | retained withdrawal reprobes |
| `SrpFeedback.KindThenWithdrawalIsDeliveredInOrder` (`sw/firmware/ctrl/test/srp_feedback.hpp:112`) | `feedback-kind-order-lost` | kind precedes withdrawal |
| `SrpFeedback.WithdrawalIsIsolatedAndSupersededEvenForAnIdenticalStream` (`sw/firmware/ctrl/test/srp_feedback.hpp:125`) | `feedback-supersession-lost` | kind preserves settled state |
| `SrpFeedback.WithdrawalIsIsolatedAndSupersededEvenForAnIdenticalStream` (`sw/firmware/ctrl/test/srp_feedback.hpp:125`) | `feedback-withdrawal-sink-crossed` | retained withdrawal reprobes |
| `SrpFeedback.ReplacementAwaitingDeliveryGetsNoOldRegistration` (`sw/firmware/ctrl/test/srp_feedback.hpp:147`) | `r10-feedback-ignores-pending` | old registration cannot settle replacement |
| `SrpFeedback.EarlierSinkTransientRefusalKeepsDeliveryAwake` (`sw/firmware/ctrl/test/srp_feedback.hpp:159`) | `r10-transient-refusal-forgotten` | earlier refusal keeps delivery awake |
| `SrpFeedback.DiscoveredWithdrawalMeasuresTheFundedPath` (`sw/firmware/ctrl/test/srp_feedback.hpp:167`) | `r10-feedback-allowance-quarter` | measured feedback per sink allowance |
| `SrpFeedback.DiscoveredWithdrawalMeasuresTheFundedPath` (`sw/firmware/ctrl/test/srp_feedback.hpp:167`) | `r10-feedback-allowance-eight` | measured feedback per sink allowance |
| `AcmpCore.KindChangesOnlyTheSettledView` (`sw/firmware/ctrl/test/test_acmp.cpp:751`) | `acmp-kind-lost` | kind updates the reported view |
| `AcmpCore.KindChangesOnlyTheSettledView` (`sw/firmware/ctrl/test/test_acmp.cpp:751`) | `acmp-kind-any-state` | kind refuses non-settled state |

The retained reviewer source is hash-bound in ROUND11-REVIEW-INPUTS.json.
Nine applicable probes pass at each interface count, including both R533 kind
replacements, coalesced and separate-pass withdrawal, both R532 kind directions,
the two pending/refusal guards and discovered-talker withdrawal. The diagnostic
`R10WithdrawalFeedbackCostFitsAllowance` asserts nonzero cost on the known
zero-access undiscovered path; it is not an acceptance case and is not claimed
as passing. The funded discovered path is run verbatim.

The historical `r10-feedback-allowance-quarter` plant name is preserved.
At the revised formula it replaces six with one access per sink; the fixed-eight
plant still replaces the entire formula with eight. Both must fail the measured
per-sink assertion, not compilation or a restated macro identity.

The inherited `acmp-open-unguarded` oracle now names entry 10 in
`sw/firmware/ctrl/test/acmp_review_mutants.py:256`, matching the expanded
`AcmpCore.A23EveryEntryRefusesACallFromInsideAPort` list. It still requires
the same reentry assertion; the original entry-9 oracle is recorded as a
development failure and is not counted as a final catch.
