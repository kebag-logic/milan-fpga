[A560]

# Round 9 tests and planted defects

Each mutation must fail its named behavioral observable; compilation failures do not count.
Both interface counts execute the new binding and bound controls. Existing SRP plants remain in the full campaign.

| Plant | Test | Failed observable |
| --- | --- | --- |
| `binding-debug-guard` | `srp_mbx.cpp` / `SynchronousBindingFromOutputAsserts` | `failed to die` |
| `binding-delivery-missing` | `srp_binding.hpp:59` / `SrpBinding.BindIsDeferredAndKeepsEverySinkAndInterface` | `binding delivered` |
| `binding-synchronous` | `srp_binding.hpp:59` / `SrpBinding.BindIsDeferredAndKeepsEverySinkAndInterface` | `callback only queues the binding` |
| `binding-poll-adds-access` | `srp_binding.hpp:59` / `SrpBinding.BindIsDeferredAndKeepsEverySinkAndInterface` | `binding poll makes no mailbox access` |
| `binding-interface-lost` | `srp_binding.hpp:59` / `SrpBinding.BindIsDeferredAndKeepsEverySinkAndInterface` | `binding delivered` |
| `binding-sink-lost` | `srp_binding.hpp:59` / `SrpBinding.BindIsDeferredAndKeepsEverySinkAndInterface` | `binding delivered` |
| `binding-refusal-dropped` | `srp_binding.hpp:94` / `SrpBinding.RefusedReceiveRetriesAfterRecoveryOrExpiry` | `binding delivered` |
| `binding-owed-retry-dropped` | `srp_binding.hpp:119` / `SrpBinding.OwedTransmissionRetriesAfterCommit` | `binding delivered` |
| `binding-unbind-lost` | `srp_binding.hpp:136` / `SrpBinding.UnbindCancelsPendingAndWithdrawsAcceptedBinding` | `unbind supersedes pending bind` |
| `binding-replacement-lost` | `srp_binding.hpp:156` / `SrpBinding.ReplacementSupersedesPendingIdentity` | `stream identity delivered` |
| `binding-pending-sleeps` | `srp_binding.hpp:94` / `SrpBinding.RefusedReceiveRetriesAfterRecoveryOrExpiry` | `pending binding keeps service awake` |
| `binding-first-refusal-forgotten` | `srp_binding.hpp:169` / `SrpBinding.OneRefusedSinkDoesNotBlockAnotherOrLetTheLoopSleep` | `earlier refusal keeps service awake` |
| `binding-count-overflow` | `srp_binding.hpp:183` / `SrpBinding.AttachmentRefusesMissingRoomAndShapeWithoutPartialBinding` | `ctrl_app_attach_srp` |
| `binding-poll-overflow` | `srp_binding.hpp:183` / `SrpBinding.AttachmentRefusesMissingRoomAndShapeWithoutPartialBinding` | `ctrl_app_attach_srp` |
| `binding-reattach-recurses` | `srp_binding.hpp:183` / `SrpBinding.AttachmentRefusesMissingRoomAndShapeWithoutPartialBinding` | `recompose before replacing the attached adapter` |
| `srp-bound-event` | `srp_app.cpp` / `EventReceiveAndTransmitPollFitTheirMeasuredBounds` | `SRP event bound` |
| `srp-bound-receive` | `srp_app.cpp` / `EventReceiveAndTransmitPollFitTheirMeasuredBounds` | `SRP refused receive bound` |
| `srp-bound-poll-transmit` | `srp_app.cpp` / `EventReceiveAndTransmitPollFitTheirMeasuredBounds` | `SRP transmitting poll bound` |
| `srp-bound-poll` | `srp_app.cpp` / `EventReceiveAndTransmitPollFitTheirMeasuredBounds` | `SRP retained receive poll bound` |
| `srp-bound-tx-record` | `srp_app.cpp` / `EventReceiveAndTransmitPollFitTheirMeasuredBounds` | `SRP maximum TX record bound` |
| `srp-bound-rx-record` | `srp_app.cpp` / `EventReceiveAndTransmitPollFitTheirMeasuredBounds` | `SRP maximum RX record bound` |
| `srp-bound-pass` | `srp_app.cpp` / `EventReceiveAndTransmitPollFitTheirMeasuredBounds` | `SRP complete pass bound` |

A0: `acmp-init-too-many-sources` fails `AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold` at “A0 more sources than ACMP_MAX_SOURCES are refused”. The control passes under GCC, AddressSanitizer and Clang; each planted run has exactly the named failure, with no AddressSanitizer diagnostic.

External reviewer probes:

| Probe | Required result |
| --- | --- |
| `binding_probe.py`, direct-delivery control removed and expected verdict inverted | Composed adapter is bound at IF=1 and both interfaces at IF=2 |
| `srp-poll-drops-tx` | SRP transmitting poll bound fails at IF=1/2 |
| `srp-pass-drops-rx-and-poll` | SRP complete pass bound fails at IF=1/2 |
| `srp-rx-max-zero` | SRP refused receive bound fails at IF=1/2 |
| `srp-event-max-zero` | SRP event bound fails at IF=1/2 |
| `control-none` | Both SRP composition suites pass at IF=1/2 |
