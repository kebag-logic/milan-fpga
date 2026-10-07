# HANDOFF: [A559] lane F3 for #665 (ACMP on the bare-metal core)

Status: REVIEW READY at `351ae81f` (every gate below rc 0), with the open decision on the
adp filter term ("Open questions and risks" 1).

- Branch `665-f3-acmp`, head `351ae81f33efc1ca818c1fea21d360260ecc2587`, not pushed.
- Base: the FC head `021b9c1fb966e9a1a4acef6b5233edd3518f32a0` (PR #685). FC is not in
  `dev` yet (checked 2026-10-07: `git merge-base --is-ancestor 021b9c1f origin/dev` exits 1,
  `origin/dev` at `79b086d44`), so `dev` is not merged here; the `--no-ff` merge of `dev`
  is owed once FC lands.
- Assignment: issue #665 comment 6026721148. TAKEN: comment 6026823815.
  REVIEW READY: comment 6029338230 (head `351ae81f`).
- Scope held: no file under `hdl/`, `sw/litex/`, `configs/` or `sw/mailbox/` changes
  (`git diff --stat 021b9c1f HEAD -- hdl sw/litex configs sw/mailbox` is empty), so the
  default all-fabric build, the shipping image and the register map are unchanged.

## Summary

| Item of the assignment | Where | State |
|---|---|---|
| 1. Talker and listener, Milan v1.2 5.5 bind model, 200 ms TMR_NO_RESP, retry, sequence IDs, responses keyed on the consumer's unique ID | `sw/firmware/ctrl/acmp/acmp.c` | done; every Table 5.30 transition, talker 5.5.4.1 to .4 |
| 2. Listener discovery (5.6.4, Table 5.54) through F0's ADP public API | `acmp.c:547-600`, `acmp_mbx.c:109` (the tap) | done in firmware; the tree's adp filter passes no ENTITY_AVAILABLE/DEPARTING (decision open, see "Open questions") |
| 3. Fast connect from the F1 store; no persistence on a read fault | `sw/firmware/ctrl/acmp/acmp_nvm.c`, `acmp.c:1096` | done; N1 to N6 on the real store |
| 4. Response before notification (#653) | `acmp.c:240` (owed FIFO, release mask), `acmp.c:415` (`finish`) | done; A19, E1 |
| 5. Differential against the processor's ACMP suites | `sw/firmware/ctrl/test/acmp_walk.cpp`, `ctrl_reuse.py` | done; 88 + 33 cells, talker F05.11; 4 differences asserted |
| 6. H-ACMP and H-DISC (#664 3.4.2) on the host model | `test_acmp_mbx.cpp` C0 to C12, E1, E2, F0 to F5 | done in mailbox accesses; time not measured (A4) |
| GoogleTest at the ratchet, 100 % branches, no unjustified exclusion | `sw/firmware/gtest/coverage.ratchet`, `README.md:319` | done; one new exclusion row, same form as F0's |
| A planted defect per check | `sw/firmware/ctrl/test/acmp_mutants.py` | 195 defects; every test of the three arms named, proven by `unnamed_tests` |
| Co-simulate with the host mailbox model | `test_acmp_mbx.cpp` (model), `tb/verilator/mbx/cosim_main.cpp` (RTL vs model) | done; 12 frames identical |
| No RTL change; default build unchanged | see above | held |

## Progress log

- Confirmed origin and base head.
- Posted TAKEN: issue #665 comment 6026823815. Blocker published there: the
  tree's `adp` channel filter passes only ENTITY_DISCOVER and both of its
  accept terms are used, so a bound talker's ENTITY_AVAILABLE/DEPARTING
  cannot reach the core without an RTL change (forbidden here). Decision
  requested; the rest of the lane proceeds.
- Differential finding (processor, not fixed here): `pp_acmp_pkg.sv:123`
  answers CONTROLLER_NOT_AUTHORIZED with 13; IEEE 1722.1-2021 Table 8-3 says
  16 (13 is TALKER_MISBEHAVING).
- Core `sw/firmware/ctrl/acmp/acmp.[ch]`, adapter `acmp_mbx.[ch]`, store
  glue `acmp_nvm.[ch]`, app compose/open split written; the existing arms all
  pass with them compiled in (rv32 text 11,756 -> 24,800 bytes).
- Commits 574911a2 (firmware) and 4a9fa9db (tests): arms acmp (66 tests),
  acmpwalk (127), acmpnvm (6) green; coverage ratchet written, every ctrl
  file 100 % lines and branches after exclusions; one new exclusion row
  (ctrl_app.c ACMP attach refusal, unreachable in the app, same form as F0's
  ADP row, whose function name moved to ctrl_app_compose).
- Commit 331455c9: 175 ACMP planted defects (ctrl_mutants.py, after F0/FC's
  93; table now 268), each caught by the check it names in a scratch run with
  4 workers; tests now spell the standards' numbers in `spec` (acmp_fake.hpp)
  so a wrong constant in acmp.h fails them; `--slice K/N` added to the gate.
- Added the H-DISC bound behind a full adp ring in the ADP+ACMP composition
  (`ACMP_MBX_ADP_RX_ACCESSES`, test F5; measured 333 accesses in pass 13
  against 21,670) with three planted defects.
- Added ACMP to the RTL co-simulation (`tb/verilator/mbx/cosim_main.cpp`):
  twelve frames identical on the RTL and the model. The first run exposed a
  harness limit (a second frame committed in the same pass was collected one
  millisecond late); the collector now waits while frames finish
  (`bench.hpp` `tx_open()`). A planted firmware defect (ACMP never composed)
  fails the new check; recorded below.
- Audit of the planted defects against the tests: five tests of the ACMP
  arms and several labelled checks (C6 to C9, F0 to F2, A2's view, B2) had
  no defect naming them, contrary to the earlier progress entry. Added 17
  defects and extra kills on six existing ones; every test of the ACMP
  arms is now named, and `unnamed_tests` proves it in the campaign before
  planting. B2's "to the multicast address" check now reads the address.
- Docs: ctrl README, gtest README, ctrl_nvm README, mbx README,
  MAILBOX_SPLIT.md (the ACMP module section, latency tables, differences,
  open items).
- Commits 048cd2b3 (H-DISC full-ring bound, co-simulation, defect audit), 6afca717 (docs),
  351ae81f (lane F3's defects in `acmp_mutants.py`, lines within 120 columns, the discovery
  walk's rig out of its test body, for the Python and C++ idiom gates).
- Gates run at 351ae81f (table below). The first builder run used the host's Verilator by
  mistake and was stopped; it was rerun with the pinned 5.050.
- Posted REVIEW READY on #665 (comment 6029338230). FC still open (#685) at posting; `dev` unmerged.

## Changes (file:line)

Firmware (all new unless noted):

- `sw/firmware/ctrl/acmp/acmp.h:1-108`: the module's contract and every clause it implements;
  `acmp.h:120-136` static sizes and wire constants; `acmp.h:286-301` `struct acmp_env`;
  `acmp.h:378-406` the entries.
- `sw/firmware/ctrl/acmp/acmp.c`:
  - `:83` `enter()`, the #678 guard; `:94-165` every port wrapped with the in-port flag.
  - `:174-220` decode, build (to the ACMP multicast address, `:197`), echo.
  - `:240-279` `transmit`/`respond`/`room`: owed FIFO of 8, release mask per frame (#653), busy drops.
  - `:286-353` the sink timers, the lazy seed and draw (`:299`), one timer per interface at its earliest deadline (`:330`).
  - `:355-435` the Table 5.22 view, the 20-byte saved record, `finish()` (persist on a record change, notify after the response).
  - `:456-600` discovery (5.6.4): start/stop, EVT_TK_DISCOVERED (`:501`), EVT_TK_DEPARTED (`:515`), TMR_NO_ADP from valid_time (`:525`), the one gPTP sample per frame (`:547`), AVAILABLE (`:557`), DEPARTING (`:589`).
  - `:602-672` SRP stop, probe with a fresh sequence_id (`:612`, `:635`), every timer expiry (`:648`).
  - `:676-833` the listener: lock (`:676`), BIND_RX (`:695`), UNBIND_RX (`:730`), GET_RX_STATE (`:751`), dispatch (`:772`), PROBE_TX_RESPONSE keyed on listener_unique_id and the sent probe (`:798`).
  - `:834-884` the talker: PROBE_TX, GET_TX_STATE, DISCONNECT_TX, GET_TX_CONNECTION.
  - `:886-1155` the public entries.
- `sw/firmware/ctrl/acmp/acmp_mbx.h:1-90` the adapter's contract, the tap and the latency
  derivation; `:110-143` the per-path and backlog bounds, incl. `ACMP_MBX_ADP_RX_ACCESSES` (`:142`).
- `sw/firmware/ctrl/acmp/acmp_mbx.c:10-48` ports on the mailbox; `:50` init; `:69-107` frame, event (tag rule), poll; `:109` the ADP tap; `:119` attach.
- `sw/firmware/ctrl/acmp/acmp_nvm.h:43-50`, `acmp_nvm.c:9-68`: the binding owner on F1's `nvm_state` port.
- `sw/firmware/ctrl/app/ctrl_app.h:18-23, 44, 50, 65-79` (changed): compose/open split, `CTRL_APP_ACMP_FIRST_SLOT`, the ACMP config; `ctrl_app.c:10, 29, 44` (changed).

Tests and harness:

- `sw/firmware/ctrl/test/acmp_fake.hpp`: the standards' numbers (`spec`), fakes, frame builders.
- `test_acmp.cpp` (A0 to A25, core), `test_acmp_mbx.cpp` (B1 to B7, C0 to C12, E1, E2, F0 to F5, U5, model), `acmp_walk.cpp` (Table 5.30, Table 5.54, LD3, LW2, TW1 to TW4), `test_acmp_nvm.cpp` (N1 to N6).
- `ctrl_arms.py:43, 51, 69` the arms `acmp`, `acmpwalk`, `acmpnvm`; `ctrl_build.py:36-41` sources and includes; `ctrl_reuse.py:37-43` the three processor slices; `test_ctrl_firmware.py:131` `--slice K/N`.
- `acmp_mutants.py` (lane F3's 195 defects), `ctrl_mutant.py` (the `Mutant` type), `ctrl_mutants.py:419-430` `NAMED_SOURCES` and `unnamed_tests`, `:491` `sliced`.
- `tb/verilator/mbx/cosim_main.cpp:88-95` the frame collector waits while frames finish; `:197-245` the ACMP stimulus and config; `tb/verilator/mbx/bench.hpp:149` `tx_open()`; `Makefile:39-47` firmware sources.
- Existing tests given the two new config fields: `adp_walk.cpp`, `test_adp.cpp`, `test_unit_seams.cpp`.

Docs: `docs/design/MAILBOX_SPLIT.md:484-620` (The ACMP module, discovery and the adp filter,
ACMP service latency, differences from the processor), open items and verification rows;
`sw/firmware/ctrl/README.md:44` (The ACMP module), arms, reuse, planted defects;
`sw/firmware/gtest/README.md` (F3 arms, exclusion row `:319`); `sw/firmware/ctrl_nvm/README.md`
(the binding owner); `tb/verilator/mbx/README.md` (the co-simulation).

## Tests and the planted defect each catches

Arms: `acmp` 67 tests, `acmpwalk` 127 (88 Table 5.30 cells, 33 Table 5.54 cells, 6
scenarios), `acmpnvm` 6. The campaign plants each defect in a copy and requires the named
test to print `[FAIL]` with the named words; `unnamed_tests` fails the campaign when any
test of the three sources is named by no defect. Full campaign at the head: 288 of 288
caught (12 slices of 24), 0 escapes, 0 unnamed tests. Generated from the table:

| Test | Arm | Planted defects that must fail it |
|---|---|---|
| `AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold` (test_acmp.cpp) | `acmp` | 5: `acmp-init-no-interface`, `acmp-init-sink-interface`, `acmp-init-source-interface`, `acmp-init-too-many-sinks`, `acmp-init-too-many-sources` |
| `AcmpCore.A0EverySinkStartsUnboundAndNothingIsCalled` (test_acmp.cpp) | `acmp` | 1: `acmp-init-reads-the-seed` |
| `AcmpCore.A1BindFromUnboundRespondsThenProbes` (test_acmp.cpp) | `acmp` | 10: `acmp-bind-change-before-response`, `acmp-bind-count-0`, `acmp-bind-starts-no-discovery`, `acmp-header-cdl-84`, `acmp-header-no-resp-2s`, `acmp-no-resp-2s`, `acmp-nothing-persisted`, `acmp-probe-before-response`, `acmp-probe-without-fast-connect`, `acmp-streaming-wait-ignored` |
| `AcmpCore.A1BindWithoutStreamingWaitBindsStarted` (test_acmp.cpp) | `acmp` | 2: `acmp-bind-response-always-streaming-wait`, `acmp-new-bind-never-started` |
| `AcmpCore.A2GetRxStateInEveryState` (test_acmp.cpp) | `acmp` | 2: `acmp-getrx-count-unbound`, `acmp-getrx-no-fast-connect` |
| `AcmpCore.A2GetRxStateReportsStreamingWaitAndRegisteringFailed` (test_acmp.cpp) | `acmp` | 5: `acmp-getrx-no-registering-failed`, `acmp-header-registering-failed-bit`, `acmp-registered-kind-dropped`, `acmp-sw-read-from-fast-connect`, `acmp-view-without-registering-failed` |
| `AcmpCore.A2UnknownSinkIsAnsweredListenerUnknownId` (test_acmp.cpp) | `acmp` | 2: `acmp-header-listener-unknown-is-2`, `acmp-unknown-sink-silent` |
| `AcmpCore.A3UnbindInEveryState` (test_acmp.cpp) | `acmp` | 5: `acmp-unbind-change-before-response`, `acmp-unbind-echoes-the-talker`, `acmp-unbind-keeps-discovery`, `acmp-unbind-keeps-srp`, `acmp-unbind-srp-after-response` |
| `AcmpCore.A4LockedByAnotherControllerRefusesBindAndUnbind` (test_acmp.cpp) | `acmp` | 2: `acmp-lock-ignored`, `acmp-not-authorized-is-13` |
| `AcmpCore.A4TheLockingControllerPassesAndGetRxStateIsNotLocked` (test_acmp.cpp) | `acmp` | 2: `acmp-get-rx-state-locked`, `acmp-lock-refuses-the-holder` |
| `AcmpCore.A5RebindTheSameSourceUpdatesAndExits` (test_acmp.cpp) | `acmp` | 2: `acmp-rebind-same-keeps-the-controller`, `acmp-rebind-same-reprobes` |
| `AcmpCore.A6BindAnotherSourceRestartsTheSink` (test_acmp.cpp) | `acmp` | 2: `acmp-bind-new-keeps-srp`, `acmp-rebind-not-persisted` |
| `AcmpCore.A6TheSameTalkerAnotherSourceIsANewBinding` (test_acmp.cpp) | `acmp` | 1: `acmp-bind-same-talker-is-the-same-source` |
| `AcmpCore.A7ResponsesKeyOnTheListenerUniqueId` (test_acmp.cpp) | `acmp` | 1: `acmp-response-keyed-on-the-source` |
| `AcmpCore.A7EachGuardTermIsChecked` (test_acmp.cpp) | `acmp` | 4: `acmp-guard-controller-dropped`, `acmp-guard-sequence-id-dropped`, `acmp-guard-talker-dropped`, `acmp-guard-unique-id-dropped` |
| `AcmpCore.A7TheGuardReadsTheSentProbeNotTheBinding` (test_acmp.cpp) | `acmp` | 1: `acmp-guard-reads-the-binding` |
| `AcmpCore.A7ResponsesOutsideProbingAreIgnored` (test_acmp.cpp) | `acmp` | 1: `acmp-responses-taken-outside-probing` |
| `AcmpCore.A8SuccessSettles` (test_acmp.cpp) | `acmp` | 5: `acmp-header-no-tk-5s`, `acmp-no-tk-1s`, `acmp-settle-starts-no-srp`, `acmp-settle-swaps-stream-fields`, `acmp-vlan-masked` |
| `AcmpCore.A9FailureWaitsForTheRetry` (test_acmp.cpp) | `acmp` | 3: `acmp-failure-retries-at-200ms`, `acmp-failure-status-dropped`, `acmp-header-retry-2s` |
| `AcmpCore.A10NoResponseSendsTheDuplicateThenGivesUp` (test_acmp.cpp) | `acmp` | 3: `acmp-duplicate-takes-a-new-sequence-id`, `acmp-no-duplicate`, `acmp-second-timeout-keeps-status-0` |
| `AcmpCore.A11RetryWaitsForTheTalkerOrDelays` (test_acmp.cpp) | `acmp` | 2: `acmp-retry-ignores-discovery`, `acmp-retry-zeroes-the-status` |
| `AcmpCore.A12DelaySendsANewProbe` (test_acmp.cpp) | `acmp` | 2: `acmp-delay-resends-the-old-probe`, `acmp-sequence-id-never-advances` |
| `AcmpCore.A13NoTalkerAttributeReprobes` (test_acmp.cpp) | `acmp` | 2: `acmp-no-tk-keeps-srp`, `acmp-reprobe-ignores-discovery` |
| `AcmpCore.A14RegisteredSettlesTheReservation` (test_acmp.cpp) | `acmp` | 2: `acmp-registered-anywhere`, `acmp-registered-keeps-no-tk` |
| `AcmpCore.A15UnregisteredReprobes` (test_acmp.cpp) | `acmp` | 3: `acmp-reprobe-ignores-discovery`, `acmp-unregistered-anywhere`, `acmp-unregistered-keeps-srp` |
| `AcmpCore.A16OneCounterForEveryNewProbe` (test_acmp.cpp) | `acmp` | 2: `acmp-sequence-id-never-advances`, `acmp-sequence-id-per-sink` |
| `AcmpCore.A17EachInterfaceTimerHoldsItsEarliestDeadline` (test_acmp.cpp) | `acmp` | 5: `acmp-expiry-not-consumed`, `acmp-expiry-takes-every-interface`, `acmp-timer-at-the-latest-deadline`, `acmp-timer-never-stopped`, `acmp-timer-port-called-every-time` |
| `AcmpCore.A18AZeroDelayProbesInTheSameExpiry` (test_acmp.cpp) | `acmp` | 2: `acmp-delay-up-to-4s`, `acmp-zero-delay-waits` |
| `AcmpCore.A18TheSeedIsTakenAtTheFirstDraw` (test_acmp.cpp) | `acmp` | 2: `acmp-rng-left-at-0`, `acmp-seed-at-every-draw` |
| `AcmpCore.A20ProbeTxIsAnsweredFromTheSource` (test_acmp.cpp) | `acmp` | 4: `acmp-probe-tx-any-interface`, `acmp-probe-tx-no-destination-mac-check`, `acmp-probe-tx-reports-asking-failed`, `acmp-unknown-source-answered` |
| `AcmpCore.A20DisconnectGetTxStateAndGetTxConnection` (test_acmp.cpp) | `acmp` | 5: `acmp-disconnect-always-succeeds`, `acmp-get-tx-connection-supported`, `acmp-get-tx-state-echoes-the-listener`, `acmp-get-tx-state-registering-failed-0`, `acmp-get-tx-state-unheld-mac` |
| `AcmpCore.A21MessagesNotForThisEntityAreIgnored` (test_acmp.cpp) | `acmp` | 2: `acmp-every-listener-is-this-one`, `acmp-every-talker-is-this-one` |
| `AcmpCore.A21MalformedFramesAreCounted` (test_acmp.cpp) | `acmp` | 2: `acmp-longer-pdu-refused`, `acmp-short-pdu-read` |
| `AcmpCore.A19AResponseWithoutRoomIsOwedAndItsChangeWaits` (test_acmp.cpp) | `acmp` | 2: `acmp-change-not-held-for-its-response`, `acmp-poll-drains-everything` |
| `AcmpCore.A19NothingPassesAnOwedFrame` (test_acmp.cpp) | `acmp` | 2: `acmp-poll-newest-first`, `acmp-response-passes-an-owed-frame` |
| `AcmpCore.A19AFullQueueDropsTheCommandBeforeItActs` (test_acmp.cpp) | `acmp` | 1: `acmp-full-queue-acts` |
| `AcmpCore.A19AProbeWithoutRoomIsLostAndRecovered` (test_acmp.cpp) | `acmp` | 1: `acmp-lost-probe-uncounted` |
| `AcmpCore.A19TwoOwedResponsesForOneSinkReleaseTogether` (test_acmp.cpp) | `acmp` | 1: `acmp-first-owed-releases-every-change` |
| `AcmpCore.A22AvailableDiscoversWhenTheGrandmasterMatches` (test_acmp.cpp) | `acmp` | 4: `acmp-discovery-reads-no-domain`, `acmp-discovery-reads-no-grandmaster`, `acmp-header-valid-time-in-seconds`, `acmp-valid-time-in-seconds` |
| `AcmpCore.A22DiscoveredStartsTheProbeFromPrbWAvail` (test_acmp.cpp) | `acmp` | 2: `acmp-discovered-probing-stays-passive`, `acmp-grandmaster-read-twice` |
| `AcmpCore.A22DiscoveredStateCells` (test_acmp.cpp) | `acmp` | 6: `acmp-discovered-interface-unchecked`, `acmp-grandmaster-sampled-for-the-refresh`, `acmp-refresh-notes-no-index`, `acmp-restart-mismatch-keeps-aging`, `acmp-restart-on-a-smaller-index-only`, `acmp-restart-raises-no-discovered` |
| `AcmpCore.A22DepartingAndAging` (test_acmp.cpp) | `acmp` | 4: `acmp-departing-interface-unchecked`, `acmp-departing-keeps-aging`, `acmp-departing-taken-undiscovered`, `acmp-no-aging` |
| `AcmpCore.A22OnlyBoundSinksOfThatTalkerOnThatInterface` (test_acmp.cpp) | `acmp` | 3: `acmp-discovery-on-every-interface`, `acmp-discovery-on-unbound-sinks`, `acmp-grandmaster-sampled-per-sink` |
| `AcmpCore.A22OtherAdpFramesAreIgnored` (test_acmp.cpp) | `acmp` | 4: `acmp-adp-discover-taken`, `acmp-adp-ethertype-unchecked`, `acmp-adp-short-frame-taken`, `acmp-adp-subtype-unchecked` |
| `AcmpCore.A23EveryEntryRefusesACallFromInsideAPort` (test_acmp.cpp) | `acmp` | 3: `acmp-reentry-unguarded`, `acmp-reentry-untrapped`, `acmp-send-port-unflagged` |
| `AcmpCore.A23EveryPortIsGuarded` (test_acmp.cpp) | `acmp` | 10: `acmp-changed-port-unflagged`, `acmp-clock-port-unflagged`, `acmp-gptp-port-unflagged`, `acmp-lock-port-unflagged`, `acmp-persist-port-unflagged`, `acmp-reentry-unguarded`, `acmp-seed-port-unflagged`, `acmp-source-port-unflagged`, `acmp-srp-port-unflagged`, `acmp-timer-port-unflagged` |
| `AcmpCore.A24ARestoredBindingFastConnects` (test_acmp.cpp) | `acmp` | 4: `acmp-record-unique-id-little-endian`, `acmp-restore-lands-in-prb-w-resp`, `acmp-restore-starts-no-discovery`, `acmp-restore-unique-id-little-endian` |
| `AcmpCore.A24UnboundRecordsRefusalsAndRollback` (test_acmp.cpp) | `acmp` | 2: `acmp-roll-back-keeps-the-bindings`, `acmp-unbound-record-not-zero` |
| `AcmpCore.A24StartedIsSavedAndReported` (test_acmp.cpp) | `acmp` | 1: `acmp-started-not-saved` |
| `AcmpCore.A25OnlyTable522ItemsAreReported` (test_acmp.cpp) | `acmp` | 3: `acmp-discovery-notifies`, `acmp-second-timeout-keeps-status-0`, `acmp-status-not-notified` |
| `AcmpMailbox.B1TheChannelCarriesCommandsAndResponsesInOrder` (test_acmp_mbx.cpp) | `acmp` | 2: `acmp-frames-on-the-adp-channel`, `acmp-frames-to-the-own-mac` |
| `AcmpMailbox.B2OwnUnicastIsAToleranceAndForeignUnicastIsRefused` (test_acmp_mbx.cpp) | `acmp` | 4: `acmp-frames-to-the-own-mac`, `app-own-mac-not-the-entity-mac`, `model-mismatch-never-counted`, `model-own-any-unicast` |
| `AcmpMailbox.B3TheTimersRunOnTheInterfaceSlot` (test_acmp_mbx.cpp) | `acmp` | 3: `acmp-no-resp-2s`, `acmp-timer-deadline-taken-as-a-delay`, `acmp-timer-on-the-next-slot` |
| `AcmpMailbox.B4AnExpiryThatRacedAStopOrAReArmIsDiscarded` (test_acmp_mbx.cpp) | `acmp` | 3: `acmp-stale-tag-taken`, `acmp-stop-keeps-the-arm`, `acmp-tag-reused` |
| `AcmpMailbox.B5TheTapHandsAvailableToDiscoveryAndTheRestToAdp` (test_acmp_mbx.cpp) | `acmp` | 3: `acmp-no-tap`, `acmp-tap-drops-the-rest`, `acmp-tap-takes-discover` |
| `AcmpMailbox.B6TheGrandmasterIsTheInterfaces` (test_acmp_mbx.cpp) | `acmp` | 1: `acmp-domain-not-sampled` |
| `AcmpAdapterUnit.B7RefusalsOfTheAdapter` (test_acmp_mbx.cpp) | `acmp` | 5: `acmp-attach-before-adp`, `acmp-attach-ignores-poll-room`, `acmp-attach-ignores-sink-room`, `acmp-interfaces-past-the-mailbox`, `acmp-slots-past-the-bank` |
| `AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem` (test_acmp_mbx.cpp) | `acmp` | 5: `acmp-bind-reads-the-clock-twice`, `acmp-get-rx-state-reads-the-clock`, `acmp-probe-response-reads-the-clock-twice`, `acmp-talker-reads-the-clock`, `acmp-unbind-reads-the-clock` |
| `AcmpMailbox.C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry` (test_acmp_mbx.cpp) | `acmp` | 5: `acmp-delay-reads-the-clock-again`, `acmp-expiry-reads-the-clock-twice`, `acmp-no-tk-samples-the-grandmaster`, `acmp-retry-samples-the-grandmaster`, `acmp-second-no-resp-samples-the-grandmaster` |
| `AcmpMailbox.C10C11DiscoveryPathsAreServedInThePassThatTakesTheRecord` (test_acmp_mbx.cpp) | `acmp` | 4: `acmp-available-reads-the-clock-twice`, `acmp-departing-samples-the-grandmaster`, `acmp-grandmaster-read-twice`, `acmp-timer-never-stopped` |
| `AcmpMailbox.C12AgingIsServedInThePassThatTakesTheExpiry` (test_acmp_mbx.cpp) | `acmp` | 1: `acmp-aging-samples-the-grandmaster` |
| `AcmpMailbox.E1AnOwedResponseLeavesFirstAndItsChangeAfterIt` (test_acmp_mbx.cpp) | `acmp` | 2: `acmp-change-not-held-for-its-response`, `acmp-poll-owes-nothing` |
| `AcmpMailbox.E2AnOwedResponseIsCommittedInPassKPlus1` (test_acmp_mbx.cpp) | `acmp` | 2: `acmp-poll-drains-everything`, `acmp-poll-newest-first` |
| `AcmpMailbox.F0ToF3FullRingsAreTakenWithinTheBound` (test_acmp_mbx.cpp) | `acmp` | 5: `acmp-backlog-understated`, `acmp-pass-bound-understated`, `events-halved`, `model-event-ring-a-record-short`, `rx-one-record-per-pass` |
| `AcmpMailbox.F4TheSmallestRecordsTheFilterPassesFillTheRing` (test_acmp_mbx.cpp) | `acmp` | 2: `acmp-backlog-understated`, `acmp-smallest-record-overstated` |
| `AcmpMailbox.F5AnAvailableBehindAFullAdpRingIsServedWithinTheBound` (test_acmp_mbx.cpp) | `acmp` | 3: `acmp-adp-ring-bound-understated`, `acmp-discovery-takes-the-first-sink`, `rx-one-record-per-pass` |
| `AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract` (test_acmp_mbx.cpp) | `acmp` | 4: `acmp-init-reads-the-seed`, `acmp-no-tap`, `app-acmp-before-adp`, `app-acmp-never-composed` |
| `ListenerWalk.Graded` (acmp_walk.cpp) | `acmpwalk` | 35: `acmp-bind-count-0`, `acmp-bind-new-keeps-srp`, `acmp-bind-starts-no-discovery`, `acmp-delay-resends-the-old-probe`, `acmp-discovery-notifies`, `acmp-duplicate-takes-a-new-sequence-id`, `acmp-failure-retries-at-200ms`, `acmp-failure-status-dropped`, `acmp-getrx-count-unbound`, `acmp-getrx-no-fast-connect`, `acmp-header-no-resp-2s`, `acmp-header-retry-2s`, `acmp-no-duplicate`, `acmp-no-tk-1s`, `acmp-no-tk-keeps-srp`, `acmp-probe-without-fast-connect`, `acmp-probing-status-not-notified`, `acmp-rebind-same-reprobes`, `acmp-registered-anywhere`, `acmp-registered-keeps-no-tk`, `acmp-registered-kind-dropped`, `acmp-reprobe-ignores-discovery`, `acmp-responses-taken-outside-probing`, `acmp-retry-ignores-discovery`, `acmp-retry-zeroes-the-status`, `acmp-second-timeout-keeps-status-0`, `acmp-sequence-id-per-sink`, `acmp-settle-starts-no-srp`, `acmp-settle-swaps-stream-fields`, `acmp-unbind-echoes-the-talker`, `acmp-unbind-keeps-discovery`, `acmp-unbind-keeps-srp`, `acmp-unbind-not-persisted`, `acmp-unregistered-anywhere`, `acmp-unregistered-keeps-srp` |
| `ListenerScenario.LD3TheLockRefusalStatus` (acmp_walk.cpp) | `acmpwalk` | 1: `acmp-not-authorized-is-13` |
| `ListenerScenario.LW2GuardsUnknownSinksAndForeignMessages` (acmp_walk.cpp) | `acmpwalk` | 4: `acmp-guard-controller-dropped`, `acmp-guard-sequence-id-dropped`, `acmp-guard-talker-dropped`, `acmp-guard-unique-id-dropped` |
| `DiscoveryWalk.Graded` (acmp_walk.cpp) | `acmpwalk` | 10: `acmp-departing-interface-unchecked`, `acmp-departing-keeps-aging`, `acmp-discovered-interface-unchecked`, `acmp-discovery-reads-no-domain`, `acmp-discovery-reads-no-grandmaster`, `acmp-no-aging`, `acmp-refresh-notes-no-index`, `acmp-restart-mismatch-keeps-aging`, `acmp-restart-raises-no-discovered`, `acmp-valid-time-in-seconds` |
| `TalkerWalk.TW1ProbeTheFlagLawAndTheSource` (acmp_walk.cpp) | `acmpwalk` | 2: `acmp-probe-tx-echoes-every-flag`, `acmp-probe-tx-no-destination-mac-check` |
| `TalkerWalk.TW2GetTxStateReadsRegisteringFailedLive` (acmp_walk.cpp) | `acmpwalk` | 3: `acmp-get-tx-state-echoes-the-listener`, `acmp-get-tx-state-registering-failed-0`, `acmp-unknown-source-answered` |
| `TalkerWalk.TW3DisconnectAndGetTxConnection` (acmp_walk.cpp) | `acmpwalk` | 2: `acmp-disconnect-always-succeeds`, `acmp-get-tx-connection-supported` |
| `TalkerWalk.TW4TheInterfaceAndTheStatelessProperty` (acmp_walk.cpp) | `acmpwalk` | 1: `acmp-probe-tx-any-interface` |
| `AcmpStore.N1ABindSurvivesAPowerCycleAndFastConnects` (test_acmp_nvm.cpp) | `acmpnvm` | 6: `acmp-nothing-persisted`, `acmp-nvm-bindings-latched-by-the-others`, `acmp-nvm-bindings-to-the-others`, `acmp-restore-announced`, `acmp-restore-lands-in-prb-w-resp`, `acmp-restore-starts-no-discovery` |
| `AcmpStore.N2AnUnbindIsSavedAsAnUnboundRecord` (test_acmp_nvm.cpp) | `acmpnvm` | 1: `acmp-unbind-not-persisted` |
| `AcmpStore.N3EachSinksStartedStateIsSaved` (test_acmp_nvm.cpp) | `acmpnvm` | 2: `acmp-record-flags-swapped`, `acmp-started-not-saved` |
| `AcmpStore.N4AnUnreadSlotRefusesPersistence` (test_acmp_nvm.cpp) | `acmpnvm` | 1: `acmp-rebind-not-persisted` |
| `AcmpStore.N5ARecordTheCoreRefusesKeepsItsDefault` (test_acmp_nvm.cpp) | `acmpnvm` | 1: `acmp-nvm-refusal-applied` |
| `AcmpStore.N6TheRollBackAndEveryOtherGroup` (test_acmp_nvm.cpp) | `acmpnvm` | 7: `acmp-nvm-d3-roll-back-kept`, `acmp-nvm-latch-length-unchecked`, `acmp-nvm-model-always-ready`, `acmp-nvm-refusal-applied`, `acmp-nvm-release-dropped`, `acmp-nvm-settle-dropped`, `acmp-roll-back-keeps-the-bindings` |

Labelled assertions inside a test are not each proven. Of the 323 labelled `EXPECT`/`ASSERT`
statements in the four sources, 152 are named by no defect's words at the head (168 before
this round). The rule enforced mechanically is F1's (every test is named), plus the checks
the test names themselves carry (C6 to C9, F0 to F2), which now have defects of their own.
Some of the 152 are preconditions (for example "B1 the filter passes a BIND_RX"); the rest
are a gap a reviewer may weigh under `Tests`.

Co-simulation (`make run-cosim`): the planted firmware defect "ACMP never composed"
(`ctrl_app.c`, `return true ||`) fails `the firmware answered ACMP on the model, each frame
of the scenario in order` (run by hand, tree restored; the RTL campaign `mutants.py` builds
only the suite).

## Coverage table

`python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4`, rc 0, at the head:

| File | Lines | Branches | After exclusions |
|---|---:|---:|---|
| sw/firmware/ctrl/acmp/acmp.c | 690/690 | 316/316 | 100 % / 100 % |
| sw/firmware/ctrl/acmp/acmp_mbx.c | 66/66 | 26/26 | 100 % / 100 % |
| sw/firmware/ctrl/acmp/acmp_nvm.c | 38/38 | 10/10 | 100 % / 100 % |
| sw/firmware/ctrl/adp/adp.c | 168/170 | 73/80 | 100 % / 100 % |
| sw/firmware/ctrl/adp/adp_mbx.c | 83/83 | 38/40 | 100 % / 100 % |
| sw/firmware/ctrl/app/ctrl_app.c | 20/21 | 17/20 | 100 % / 100 % |
| sw/firmware/ctrl/loop/ctrl_loop.c | 95/95 | 56/56 | 100 % / 100 % |
| sw/firmware/ctrl/mbx/mbx.c | 173/173 | 62/62 | 100 % / 100 % |
| sw/firmware/ctrl/mbx/mbx_wire.h | 15/15 | 12/12 | 100 % / 100 % |
| sw/firmware/ctrl/plat/mbx_plat_mmio.c | 10/10 | 0/0 | 100 % / 100 % |
| sw/firmware/ctrl/port/ctrl_debug.c | 19/19 | 6/6 | 100 % / 100 % |
| sw/firmware/ctrl/port/ctrl_pool.c | 99/99 | 60/60 | 100 % / 100 % |
| sw/firmware/ctrl/port/shlan_port.c | 22/22 | 6/6 | 100 % / 100 % |
| sw/firmware/ctrl/wire/wire.h | 10/10 | 2/2 | 100 % / 100 % |
| sw/firmware/ctrl_nvm/nvm_klj2.c | 195/196 | 104/108 | 100 % / 100 % |
| sw/firmware/ctrl_nvm/nvm_store.c | 434/434 | 259/266 | 100 % / 100 % |
| sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c | 100/100 | 63/64 | 100 % / 100 % |

The ACMP files are 100 % raw. The one new exclusion (`ctrl_app.c`, the ACMP attach refusal,
unreachable in the composition) is `sw/firmware/gtest/README.md:319`, with its reason; F0's
row moved with the function to `ctrl_app_compose`.

## Measured figures

- Per path, in mailbox accesses on the host model (bound / measured): BIND_RX 72/72, UNBIND_RX
  48/48, GET_RX_STATE 47/47, PROBE_TX_RESPONSE 28/28, talker commands 47/47, TMR_DELAY or the
  first TMR_NO_RESP 34/34, the second TMR_NO_RESP, TMR_RETRY, TMR_NO_TK 13/12 to 13,
  ENTITY_AVAILABLE 35/35, ENTITY_DEPARTING 30/29, TMR_NO_ADP 12/12.
- Backlogs: pass bound 985 (worst measured 185); an event by pass 2 (2,955); an ACMP command
  behind a full acmp ring by pass 10 (10,835; measured 19 smallest records cleared in pass 10);
  an ENTITY_AVAILABLE behind a full adp ring by pass 21 (21,670; measured pass 13 of 26
  records, 333 accesses); an owed response in pass k + 1 (8,865; measured 25, 100, 200 for
  k = 0, 3, 7).
- RV32I freestanding (`riscv32-linux-gcc -march=rv32i -mabi=ilp32`): text 11,756 bytes at the
  base, 24,848 at the head; data 0; bss 170 (unchanged); externals `__lshrdi3, __mulsi3,
  __udivsi3, __umodsi3, memcpy, memset, vsnprintf` (no heap). Static state on RV32:
  `struct acmp` 4,416 bytes (a sink 224), `struct acmp_mbx` 4,464, `struct ctrl_app` 6,544.
- Co-simulation: 12 frames (5 ADP, 7 ACMP), identical bytes and NOW_MS on the RTL and the
  model; 28 checks, 0 failures.

## Gate table

Each command run on its own, at head `351ae81f`, rc recorded, output never piped.

| Gate | Command | rc | Result |
|---|---|---:|---|
| firmware-unit: tally | `python3 sw/firmware/gtest/tally_selftest.py` | 0 | the tally reads a failing and a crashing test as failures |
| firmware-unit: ctrl suites | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32` | 0 | every arm PASS: `acmp` 67, `acmpwalk` 127, `acmpnvm` 6 tests; rv32 text 24,848 bytes, no heap symbol |
| ctrl campaign | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --slice K/12`, K = 1 to 12, each its own process | 0 (x12) | `mutants: 24 of 24 caught` in every slice: 288 of 288, 0 escapes, 0 unnamed tests |
| firmware-unit: coverage | `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | |
| firmware-unit: coverage | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4` | 0 | 17 files at the ratchet, 100 % lines and branches after exclusions (146 s) |
| firmware-unit: store | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 5 shapes, 434 tests (98 s) |
| mbx suite | `make -C tb/verilator/mbx clean`, then `make -C tb/verilator/mbx -j2 run-wb run-axil` | 0 | 285 checks (Wishbone), 330 (AXI4-Lite) |
| mbx suite | `make -C tb/verilator/mbx` | 0 | both adapters; co-simulation 28 checks, 12 identical frames; two interfaces 285/330/285; `mutants.py --quick` 5 of 5 |
| mbx suite | `make -C tb/verilator/mbx mutants` | 0 | `mbx mutants: 67 of 67 caught` (107 s) |
| contract | `python3 sw/mailbox/gen_mailbox.py --check --crosscheck` | 0 | 0 findings |
| contract | `python3 sw/mailbox/gen_mailbox.py --selftest` | 0 | 0 arms failed |
| builder bank | `python3 sw/builder/test_builder.py --require-rv32` | 0 | "ALL GATES PASS EXCEPT 1 NOT RUN": gate 11 needs a placed utilization report from a Vivado build tree, which this host does not hold (1,255 s, RTL mutation variants linted) |
| saved-state writer | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 5 shapes, every planted defect reddened |
| scope | `git diff --stat 021b9c1f HEAD -- hdl sw/litex configs sw/mailbox` | | empty |
| docs workflow | `python3 scripts/docs_check.py` | 0 | |
| docs workflow | `python3 scripts/check_em_dash.py --base 6714181d0c8a16e2983f85b724f4d688f5111835` | 0 | |
| docs workflow | `python3 scripts/check_em_dash.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_doc_style.py` | 0 | |
| docs workflow | `python3 scripts/check_doc_style.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_gptp_docs.py` | 0 | |
| docs workflow | `python3 scripts/check_gptp_docs.py --selftest` | 0 | |
| docs workflow | `python3 docs/DOC_MAP.gen.py --check` | 0 | |
| docs workflow | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | |
| docs workflow | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | |
| docs workflow | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_solution_docs.py` | 0 | |
| docs workflow | `python3 scripts/check_solution_docs.py --selftest` | 0 | |
| docs workflow | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | |
| docs workflow | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_submodule_docs.py` | 0 | |
| docs workflow | `python3 scripts/check_submodule_docs.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_diagram_pngs.py` | 0 | |
| docs workflow | `python3 scripts/check_diagram_pngs.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_feature_status.py --self-test` | 0 | |
| docs workflow | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | |
| docs workflow | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | |
| docs workflow | `python3 scripts/measure_control_flow.py --selftest` | 0 | |
| docs workflow | `python3 scripts/measure_cohesion.py --selftest` | 0 | |
| docs workflow | `python3 scripts/measure_naming.py --check` | 0 | |
| docs workflow | `python3 scripts/measure_naming.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_port_contracts.py` | 0 | |
| docs workflow | `python3 scripts/check_port_contracts.py --selftest` | 0 | |
| docs workflow | `python3 scripts/measure_fail_fast.py --check` | 0 | |
| docs workflow | `python3 scripts/measure_fail_fast.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_todo_ownership.py` | 0 | |
| docs workflow | `python3 scripts/check_todo_ownership.py --selftest` | 0 | |
| docs workflow | `python3 scripts/measure_test_evidence.py --check` | 0 | |
| docs workflow | `python3 scripts/measure_test_evidence.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_hygiene.py --check` | 0 | |
| docs workflow | `python3 scripts/check_hygiene.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_sv_idiom.py` | 0 | |
| docs workflow | `python3 scripts/check_sv_idiom.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_cpp_idiom.py` | 0 | |
| docs workflow | `python3 scripts/check_cpp_idiom.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_py_idiom.py` | 0 | |
| docs workflow | `python3 scripts/check_py_idiom.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_sh_idiom.py` | 0 | |
| docs workflow | `python3 scripts/check_sh_idiom.py --selftest` | 0 | |
| docs workflow | `python3 scripts/ci_events.py --check` | 0 | |
| docs workflow | `python3 scripts/ci_events.py --selftest` | 0 | |
| docs workflow | `python3 scripts/act_ci.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_doc_paths.py` | 0 | |
| docs workflow | `python3 scripts/check_archive.py` | 0 | |
| docs workflow | `python3 scripts/check_archive.py --selftest` | 0 | |
| docs workflow | `python3 scripts/gen_toc.py --selftest` | 0 | |
| docs workflow | `python3 scripts/gen_toc.py --verify-anchors` | 0 | |
| docs workflow | `python3 scripts/gen_toc.py --check` | 0 | |
| docs workflow | `python3 avdecc/gen_aem_store.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_deploy_shape.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_baremetal_only.py --check` | 0 | |
| docs workflow | `python3 scripts/check_baremetal_only.py --selftest` | 0 | |
| docs workflow | `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_nvm_record_space.py` | 0 | |
| docs workflow | `python3 scripts/check_nvm_record_space.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_nvm_capture.py` | 0 | |
| docs workflow | `python3 scripts/check_soc_sources.py` | 0 | |
| docs workflow | `python3 scripts/check_soc_sources.py --selftest` | 0 | |
| docs workflow | `python3 sw/litex/iob_pack_selftest.py` | 0 | |
| docs workflow | `python3 scripts/check_rtl_source_lists.py` | 0 | |
| docs workflow | `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_sweep_shape.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_entity_shape.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_wire_accountability.py --self-test` | 0 | |

Verilator for every build and lint above: the pinned 5.050 (`verilator --version` printed
in each log). Temporary trees on the scratch disk, except the ctrl suite run and campaign
slice 1, which used the default temporary directory before that was set. The docs-workflow commands
are the `docs.yml` steps that need no hosted install; not run here: the HDL reference build
(its pinned pip set), the wavedrom no-drift checks (`wavedrom` not installed) and the
`--absent` compiler audit, none of which reads a file this lane changed. The em-dash base is
`git merge-base origin/dev HEAD` (`6714181d`), which includes F0's and FC's lines.
Peak memory of the service unit during the campaign: 4.4 GiB.

## Open questions and risks

1. **The adp channel's AVAILABLE/DEPARTING term (decision open, TAKEN comment 6026823815).**
   The contract passes only ENTITY_DISCOVER into the adp channel and both terms are used; any
   added term changes the elaborated filter (RTL), which this lane may not touch. Until it
   lands, discovery receives nothing from the fabric: a restored binding waits in
   PRB_W_AVAIL, and a bound sink whose probe fails or times out reaches PRB_W_AVAIL after
   TMR_RETRY (5.5.3.5.30 step 1) and stays there. H-DISC is shown on the host model with
   records written into the adp ring in the contract's layout, and the co-simulation shows
   the RTL's filter refusing the AVAILABLE as the model does.
2. **T_svc at full backlog.** The full-ring bounds fit T_svc = 10 ms only at 0.92 us per
   access or less (acmp ring) and 0.46 us or less (H-DISC behind a full adp ring; 0.92 us for
   the 20 ms ceiling). The access time is unmeasured (A4). The bounds charge every term at
   its maximum at once; the measured backlogs are far below them.
3. **Processor differences (submodule, not changed here; for the maintainers to file):**
   lock refusal status 13 instead of 16 (`pp_acmp_pkg.sv:123`); UNBIND_RX_RESPONSE echoes the
   talker fields (Table 5.36: 0); TMR_RETRY with the talker discovered zeroes the ACMP status
   (5.5.3.5.30 step 2 sets none); DISCONNECT_TX of an unknown source answers SUCCESS (5.5.4.2
   step 1: TALKER_UNKNOWN_ID). Not exercised by the reused stimulus: the processor masks
   stream_vlan_id to 12 bits (5.3.8.9 keeps the value); its probe guard reads the current
   binding's controller rather than the sent probe's.
4. **Harness finding (F0's, not changed here):** `tb/verilator/mbx/Makefile`'s `run-cosim`
   relinks `Vmbx_cosim` only when Verilator rebuilds, so a firmware-only change runs a stale
   binary in a dirty tree; CI builds from clean. All evidence here is from `make clean`.
5. The `--no-ff` merge of `dev` is owed once FC is in `dev`; the gates must then run again.
