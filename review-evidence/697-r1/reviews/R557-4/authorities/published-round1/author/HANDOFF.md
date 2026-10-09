# Import handoff

Status: REVIEW READY. Local work is complete. Branch `import-cores` is unpushed.

Head: `b9b9c20a9a44650e176db0c72ad7c752bee20dc4`. Import merge: `e529a7b09a783f42290abbb5f5a08724ba5d2e37`.
Base: `b2fb516`. Filtered head: `21d132baa148f4731a1622b425e4327c1ac7a44f`.
Configured author and committer: `hackerman-kl <hackerman-kl@kebag-logic.com>`.
Both new commit messages have one-line subjects, no bodies and no trailers.

Assignment: [issue 697](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074245112).
The issue body and all five decision/assignment comments were read before work.
The [MIT](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074086970),
[separate repository](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074093506),
and [name](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074191062)
decisions govern this import.
[TAKEN](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074254987) was posted at the start.

## Export command and history proof

Workspace: `$LANES/tsn-c-stack-import`.
Scratch: `$VALIDATION_STORAGE/697-a569`.
No submodules were initialized. The pinned source clone is clean and detached at
`6aa25dec977c6ad78bf4ff6275de47fb81d0c246`.
No source repository, hardware, bench, settings or visibility changes were made.

The original export and the repeat both execute this exact filter specification:

```sh
python3 scripts/export_history.py \
  --source $VALIDATION_STORAGE/697-a569/source \
  --destination $VALIDATION_STORAGE/697-a569/reproduce-export \
  --filter-program $WORKSPACE_HOME/.local/bin/git-filter-repo
```

The destination must be new. The script clones without checkout, selects the fixed
source revision, and runs `git-filter-repo --force --refs HEAD` with one `--path`
and `--path-rename old:new` pair for each row below. Its file callback changes SPDX,
splits mixed tests, and removes shared-harness labels. The commit callback replaces
both identities with the configured holder identity and uses a neutral one-line
subject. Dates, graph relationships and retained code changes remain traceable.
Pre-conversion ADP test blobs without separable core cases are omitted.

Import onto the existing branch used:

```sh
git fetch $VALIDATION_STORAGE/697-a569/export HEAD
git merge --allow-unrelated-histories --no-ff FETCH_HEAD \
  -m "Import portable protocol cores and core tests"
```

The export examined 3628 commits and retained 26, each with a unique new commit ID.
The [retained commit map](retained-commit-map.tsv) gives every old-to-new commit pair.
The full map is over 200 KB, so only its size and SHA-256 are recorded in the
[evidence manifest](evidence-manifest.json). The repeat export returned the identical
filtered head. Every author and committer in all 29 reachable commits is the holder
identity. Each reachable commit message has one nonblank line.

The [production byte proof](production-proof.json) verifies all seven production
files against the pinned source after only the SPDX replacement.
The library's protocol behavior is unchanged.

## File map

| Old path | New path |
|---|---|
| `sw/firmware/ctrl/adp/adp.c` | [src/adp.c]($LANES/tsn-c-stack-import/src/adp.c) |
| `sw/firmware/ctrl/adp/adp.h` | [include/adp.h]($LANES/tsn-c-stack-import/include/adp.h) |
| `sw/firmware/ctrl/acmp/acmp.c` | [src/acmp.c]($LANES/tsn-c-stack-import/src/acmp.c) |
| `sw/firmware/ctrl/acmp/acmp.h` | [include/acmp.h]($LANES/tsn-c-stack-import/include/acmp.h) |
| `sw/firmware/ctrl/maap/maap.c` | [src/maap.c]($LANES/tsn-c-stack-import/src/maap.c) |
| `sw/firmware/ctrl/maap/maap.h` | [include/maap.h]($LANES/tsn-c-stack-import/include/maap.h) |
| `sw/firmware/ctrl/wire/wire.h` | [include/wire.h]($LANES/tsn-c-stack-import/include/wire.h) |
| `sw/firmware/ctrl/test/test_adp.cpp` | [tests/test_adp.cpp]($LANES/tsn-c-stack-import/tests/test_adp.cpp) |
| `sw/firmware/ctrl/test/test_adp_reentry.cpp` | [tests/test_adp_reentry.cpp]($LANES/tsn-c-stack-import/tests/test_adp_reentry.cpp) |
| `sw/firmware/ctrl/test/test_acmp.cpp` | [tests/test_acmp.cpp]($LANES/tsn-c-stack-import/tests/test_acmp.cpp) |
| `sw/firmware/ctrl/test/acmp_fake.hpp` | [tests/acmp_fake.hpp]($LANES/tsn-c-stack-import/tests/acmp_fake.hpp) |
| `sw/firmware/ctrl/test/test_maap.cpp` | [tests/test_maap.cpp]($LANES/tsn-c-stack-import/tests/test_maap.cpp) |
| `sw/firmware/ctrl/test/test_maap_debug.cpp` | [tests/test_maap_debug.cpp]($LANES/tsn-c-stack-import/tests/test_maap_debug.cpp) |

The ADP test keeps A0 through A24 core scenarios and the re-entry suite.
The MAAP test keeps core cases and Table B.7 cases before the CSR fixture.
The ACMP test and its fake ports are core-only and retained in full.
`acmp_nvm` is excluded: its header requires `nvm_state.h` and its role is the saved-state adapter.
The core still supplies binding restore, rollback and latch APIs.
The source integration walks, generated processor expectations, mailbox tests,
platform mutation plants and all SRP material remain outside this repository.

## Coverage and mutation

There are 365 executed test instances across seven binaries and 107 test declarations.
The generated traceability matrix covers 17 requirement IDs.
Every test declaration has at least one named mutation control.
All 311 exported core plants are caught; all 325 required assertion kills hold.
Header plants rebuild their test translation unit. A compile failure, crash,
timeout, absent report or unrelated failure is an escape, never a kill.
Adapter-based killers were replaced by core frame, state or callback-budget assertions.
The original test names remain recorded in the mutation table for provenance.

| File | Raw lines | Raw branches | Adjusted lines | Adjusted branches |
|---|---|---|---|---|
| `src/adp.c` | 203/205 | 93/100 | 203/203 | 93/93 |
| `src/acmp.c` | 742/742 | 348/348 | 742/742 | 348/348 |
| `src/maap.c` | 209/209 | 140/140 | 209/209 | 140/140 |
| `include/wire.h` | 10/10 | 2/2 | 10/10 | 2/2 |

Adjusted totals: 1164/1164 lines and 583/583 branches, both 100%.
Five inherited ADP exclusion rows name seven unreachable arcs and two statements.
The reader verifies exact uncovered arc positions, not merely percentages.
The release coverage denominator excludes test code, example glue and debug assertion
instructions. Separate debug binaries exercise assertions. The prior mixed harness
combined additional debug instrumentation; this denominator is explicit in the new docs.

## Sanitizers and static analysis

Clang builds and all seven binaries pass address, leak and undefined-behavior checks.
GCC and Clang also pass standalone library-only release builds with tests disabled.
Cppcheck and clang-tidy report no project diagnostics after listed suppressions.
Cppcheck exceptions cover the unchanged MAAP decoder's const advice and three example
callback contexts whose types must match the public API. Clang-tidy exceptions cover
signed integer promotion in bit operations, adjacent scalar parameters, and optional
Annex K replacement advice. System headers use the analyzer's default exclusion.
All exceptions are listed in the repository suppression register.

## Gates

The full run used this foreground workload under a detached launcher, with its own
log, PID and return-code file. No command output was piped to another command.

```sh
python3 scripts/validate.py \
  --work $VALIDATION_STORAGE/697-a569/validation-final --jobs 16 --graphs
```

The orchestration return code is 0. Independent builds and campaigns ran concurrently.
Builds use `-j16`; campaigns use `--jobs 16`. Peak service memory was 7,259,619,328 bytes
(about 7.26 GB), below the requested 9 GB ceiling.

| Gate | Result |
|---|---|
| `boundary` | rc 0 |
| `license` | rc 0 |
| `traceability` | rc 0 |
| `test-inventory` | rc 0 |
| `coverage-controls` | rc 0 |
| `privacy` | rc 0 |
| `gcc-configure` | rc 0 |
| `gcc-build` | rc 0 |
| `gcc-test` | rc 0 |
| `coverage` | rc 0 |
| `clang-sanitizers-configure` | rc 0 |
| `clang-sanitizers-build` | rc 0 |
| `clang-sanitizers-test` | rc 0 |
| `mutation` | rc 0 |
| `static-analysis` | rc 0 |
| `graphs` | rc 0 |
| Library-only GCC | rc 0 |
| Library-only Clang | rc 0 |
| Repeat export | rc 0, identical head |
| Final committed-history privacy scan | rc 0 |
| Local document links and whitespace | pass |

The [gate table](gates.json), [versions](versions.txt), [privacy log](privacy.log) and
[evidence manifest](evidence-manifest.json) are retained here. Raw logs, mutation
binaries, rendered graphs and source clones stay in scratch. Each large artifact is
represented by a SHA-256 and byte size. No tree export, package, environment, toolchain
or file over 200 KB is placed in this output directory.

Development runs found missing core coverage paths, adapter-only mutation killers,
a strict callback-order test setup error and const-context analysis advice. These
were resolved through tests, campaign routing and listed suppressions. The final
complete run has no failure or escape. Production source code was not altered.
The hosted workflow has not run: publication is reserved for the manager.

## Privacy scan

The final scan covers 29 reachable commits, 87 historical blobs and 51 current files.
It verifies one-line commit messages and holder identities. It checks source and
history for host locations, assistant product identifiers, credential patterns and
private-key markers. No matches were found. Exported fixtures use synthetic
identities; no private device or instrument names were found in manual inspection.
The seven production files preserve their original copyright notices where present.
All current source, build and workflow files carry MIT SPDX identifiers.
The PR body contains no host paths, home paths, individual accounts or attribution footer.

## Each test and its defect

The table below mirrors the generated repository test inventory. Parameterized
entries stand for every generated instance. The exact old/new substitutions and
required assertion text live in the repository mutation table.

| Test | Defect caught | Requirements |
|---|---|---|
| [AcmpCore.A0EverySinkStartsUnboundAndNothingIsCalled]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L229) | acmp-init-reads-the-seed | ACMP-01 |
| [AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L189) | acmp-init-no-interface; acmp-init-too-many-sinks; acmp-init-too-many-sources; acmp-init-sink-interface; acmp-init-source-interface | ACMP-01 |
| [AcmpCore.A10NoResponseSendsTheDuplicateThenGivesUp]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L637) | acmp-duplicate-takes-a-new-sequence-id; acmp-second-timeout-keeps-status-0; acmp-no-duplicate | ACMP-04 |
| [AcmpCore.A11RetryWaitsForTheTalkerOrDelays]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L658) | acmp-retry-ignores-discovery; acmp-retry-zeroes-the-status | ACMP-04 |
| [AcmpCore.A12DelaySendsANewProbe]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L678) | acmp-sequence-id-never-advances; acmp-delay-resends-the-old-probe | ACMP-04 |
| [AcmpCore.A13NoTalkerAttributeReprobes]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L693) | acmp-no-tk-keeps-srp; acmp-reprobe-ignores-discovery | ACMP-04 |
| [AcmpCore.A14RegisteredSettlesTheReservation]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L717) | acmp-registered-anywhere; acmp-registered-keeps-no-tk | ACMP-04 |
| [AcmpCore.A15UnregisteredReprobes]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L742) | acmp-reprobe-ignores-discovery; acmp-unregistered-anywhere; acmp-unregistered-keeps-srp | ACMP-04 |
| [AcmpCore.A16OneCounterForEveryNewProbe]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L806) | acmp-sequence-id-never-advances; acmp-sequence-id-per-sink | ACMP-04 |
| [AcmpCore.A17EachInterfaceTimerHoldsItsEarliestDeadline]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L822) | acmp-timer-at-the-latest-deadline; acmp-timer-port-called-every-time; acmp-timer-never-stopped; acmp-expiry-takes-every-interface; acmp-expiry-not-consumed | ACMP-05 |
| [AcmpCore.A18AZeroDelayProbesInTheSameExpiry]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L850) | acmp-zero-delay-waits; acmp-delay-up-to-4s | ACMP-05 |
| [AcmpCore.A18TheSeedIsTakenAtTheFirstDraw]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L874) | acmp-seed-at-every-draw; acmp-rng-left-at-0 | ACMP-05 |
| [AcmpCore.A19AFullQueueDropsTheCommandBeforeItActs]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1093) | acmp-full-queue-acts | ACMP-09 |
| [AcmpCore.A19AProbeWithoutRoomIsLostAndRecovered]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1110) | acmp-lost-probe-uncounted; acmp-lost-probe-held | ACMP-09 |
| [AcmpCore.A19AResponseWithoutRoomIsOwedAndItsChangeWaits]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1055) | acmp-poll-drains-everything; acmp-change-not-held-for-its-response | ACMP-09 |
| [AcmpCore.A19NothingPassesAnOwedFrame]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1079) | acmp-response-passes-an-owed-frame; acmp-poll-newest-first | ACMP-09 |
| [AcmpCore.A19TwoOwedResponsesForOneSinkReleaseTogether]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1130) | acmp-first-owed-releases-every-change | ACMP-09 |
| [AcmpCore.A1BindFromUnboundRespondsThenProbes]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L246) | acmp-header-no-resp-2s; acmp-header-cdl-84; acmp-bind-count-0; acmp-probe-without-fast-connect; acmp-probe-before-response; acmp-no-resp-2s; acmp-bind-starts-no-discovery; acmp-bind-change-before-response; acmp-nothing-persisted; acmp-streaming-wait-ignored; acmp-frames-to-the-own-mac; acmp-header-version-1 | ACMP-03, ACMP-02 |
| [AcmpCore.A1BindWithoutStreamingWaitBindsStarted]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L296) | acmp-new-bind-never-started; acmp-bind-response-always-streaming-wait | ACMP-03, ACMP-02 |
| [AcmpCore.A20DisconnectGetTxStateAndGetTxConnection]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L945) | acmp-disconnect-always-succeeds; acmp-get-tx-state-echoes-the-listener; acmp-get-tx-state-registering-failed-0; acmp-get-tx-state-unheld-mac; acmp-get-tx-connection-supported | ACMP-08 |
| [AcmpCore.A20ProbeTxIsAnsweredFromTheSource]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L892) | acmp-probe-tx-reports-asking-failed; acmp-probe-tx-echoes-every-flag; acmp-probe-tx-any-interface; acmp-probe-tx-no-destination-mac-check; acmp-unknown-source-answered | ACMP-08 |
| [AcmpCore.A21MalformedFramesAreCounted]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1032) | acmp-short-pdu-read; acmp-longer-pdu-refused | ACMP-02 |
| [AcmpCore.A21MessagesNotForThisEntityAreIgnored]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1011) | acmp-every-listener-is-this-one; acmp-every-talker-is-this-one | ACMP-02 |
| [AcmpCore.A22AvailableDiscoversWhenTheGrandmasterMatches]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1148) | acmp-header-valid-time-in-seconds; acmp-discovery-reads-no-grandmaster; acmp-discovery-reads-no-domain; acmp-valid-time-in-seconds | ACMP-06 |
| [AcmpCore.A22DepartingAndAging]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1252) | acmp-departing-taken-undiscovered; acmp-departing-interface-unchecked; acmp-departing-keeps-aging; acmp-no-aging | ACMP-06 |
| [AcmpCore.A22DiscoveredStartsTheProbeFromPrbWAvail]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1179) | acmp-discovered-probing-stays-passive; acmp-grandmaster-read-twice | ACMP-06 |
| [AcmpCore.A22DiscoveredStateCells]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1194) | acmp-discovered-interface-unchecked; acmp-restart-on-a-smaller-index-only; acmp-restart-raises-no-discovered; acmp-restart-mismatch-keeps-aging; acmp-refresh-notes-no-index; acmp-grandmaster-sampled-for-the-refresh | ACMP-06 |
| [AcmpCore.A22OnlyBoundSinksOfThatTalkerOnThatInterface]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1279) | acmp-discovery-on-every-interface; acmp-discovery-on-unbound-sinks; acmp-grandmaster-sampled-per-sink; acmp-discovery-takes-the-first-sink | ACMP-06 |
| [AcmpCore.A22OtherAdpFramesAreIgnored]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1302) | acmp-adp-short-frame-taken; acmp-adp-ethertype-unchecked; acmp-adp-subtype-unchecked; acmp-adp-discover-taken | ACMP-06 |
| [AcmpCore.A23EveryEntryRefusesACallFromInsideAPort]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1324) | acmp-reentry-unguarded; acmp-reentry-untrapped; acmp-send-port-unflagged; acmp-owed-probe-timer-runs; acmp-open-unguarded | PORT-01 |
| [AcmpCore.A23EveryPortIsGuarded]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1360) | acmp-reentry-unguarded; acmp-timer-port-unflagged; acmp-gptp-port-unflagged; acmp-clock-port-unflagged; acmp-seed-port-unflagged; acmp-lock-port-unflagged; acmp-source-port-unflagged; acmp-srp-port-unflagged; acmp-persist-port-unflagged; acmp-changed-port-unflagged; acmp-bind-reads-the-clock-twice; acmp-admit-port-unflagged | PORT-01 |
| [AcmpCore.A24ARestoredBindingFastConnects]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1387) | acmp-restore-lands-in-prb-w-resp; acmp-restore-starts-no-discovery; acmp-record-unique-id-little-endian; acmp-restore-unique-id-little-endian | ACMP-07 |
| [AcmpCore.A24StartedIsSavedAndReported]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1436) | acmp-started-not-saved | ACMP-07 |
| [AcmpCore.A24TheRecordIsTheProcessorsPayloadOneFlagAtATime]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1471) | acmp-record-flags-swapped; acmp-record-flag-defines-swapped; acmp-record-valid-bit-moved | ACMP-07 |
| [AcmpCore.A24UnboundRecordsRefusalsAndRollback]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1407) | acmp-roll-back-keeps-the-bindings; acmp-unbound-record-not-zero; acmp-longer-record-applied | ACMP-07 |
| [AcmpCore.A25OnlyTable522ItemsAreReported]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1505) | acmp-second-timeout-keeps-status-0; acmp-discovery-notifies; acmp-status-not-notified | ACMP-02 |
| [AcmpCore.A26AnotherAvtpVersionIsDiscardedBeforeItIsRead]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1533) | acmp-version-unchecked; acmp-adp-version-unchecked; acmp-version-bits-misread | ACMP-02 |
| [AcmpCore.A27AProbeOwedPastAnUnbindARebindOrASuccessStartsNothing]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1665) | acmp-owed-probe-sequence-unchecked; acmp-stop-keeps-the-hold | ACMP-05 |
| [AcmpCore.A27AStalledDuplicateGetsItsWholeInterval]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1621) | acmp-owed-probe-timer-runs; acmp-owed-probe-never-starts | ACMP-05 |
| [AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1584) | acmp-owed-probe-timer-runs; acmp-owed-probe-never-starts; acmp-owed-probe-no-resp-2s; acmp-owed-probe-unnamed; acmp-owed-probe-names-the-next-sink; acmp-held-timer-expires; acmp-held-timer-armed | ACMP-05 |
| [AcmpCore.A28EveryTimerExpiresAtItsDeadlineAcrossTheWrap]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1722) | acmp-due-unsigned; acmp-no-adp-due-unsigned; acmp-no-resp-deadline-saturates; acmp-retry-deadline-saturates; acmp-no-tk-deadline-saturates; acmp-delay-deadline-saturates; acmp-no-adp-deadline-saturates | ACMP-05 |
| [AcmpCore.A28TheEarliestDeadlineIsChosenAcrossTheWrap]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1787) | acmp-due-unsigned; acmp-earliest-unsigned | ACMP-05 |
| [AcmpCore.A29RestoredBindingsAreAdmittedWhenTheTransportOpens]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1849) | acmp-restore-announced; acmp-reset-forgets-the-admitted; acmp-open-does-nothing | ACMP-07 |
| [AcmpCore.A29TheAdmitPortFollowsEachSinksBoundTalker]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1815) | acmp-admit-never-called; acmp-admit-on-every-entry; acmp-admit-ignores-another-talker; acmp-admit-on-interface-0 | ACMP-06 |
| [AcmpCore.A2GetRxStateInEveryState]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L305) | acmp-getrx-count-unbound; acmp-getrx-no-fast-connect | ACMP-03, ACMP-02 |
| [AcmpCore.A2GetRxStateReportsStreamingWaitAndRegisteringFailed]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L338) | acmp-header-registering-failed-bit; acmp-sw-read-from-fast-connect; acmp-getrx-no-registering-failed; acmp-registered-kind-dropped; acmp-view-without-registering-failed | ACMP-03, ACMP-02 |
| [AcmpCore.A2UnknownSinkIsAnsweredListenerUnknownId]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L350) | acmp-header-listener-unknown-is-2; acmp-unknown-sink-silent | ACMP-03, ACMP-02 |
| [AcmpCore.A30ADuplicateTakenAtOnceRunsFromTheClockAfterItsSend]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1919) | acmp-probe-timer-before-its-send; acmp-taken-probe-timer-from-the-entry-clock | ACMP-05 |
| [AcmpCore.A30AProbeTakenAtOnceRunsFromTheClockAfterItsSend]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1883) | acmp-probe-timer-before-its-send | ACMP-05 |
| [AcmpCore.A30ATimerDueAfterAnEarlierSinksSendIsTakenInTheSameExpiry]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1952) | acmp-expiry-due-at-its-first-read | ACMP-05 |
| [AcmpCore.A3UnbindInEveryState]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L373) | acmp-unbind-not-persisted; acmp-unbind-echoes-the-talker; acmp-unbind-keeps-srp; acmp-unbind-srp-after-response; acmp-unbind-keeps-discovery; acmp-unbind-change-before-response | ACMP-03, ACMP-02 |
| [AcmpCore.A4LockedByAnotherControllerRefusesBindAndUnbind]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L409) | acmp-not-authorized-is-13; acmp-lock-ignored | ACMP-03, ACMP-02 |
| [AcmpCore.A4TheLockingControllerPassesAndGetRxStateIsNotLocked]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L441) | acmp-lock-refuses-the-holder; acmp-get-rx-state-locked | ACMP-03, ACMP-02 |
| [AcmpCore.A5RebindTheSameSourceUpdatesAndExits]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L456) | acmp-rebind-same-reprobes; acmp-rebind-same-keeps-the-controller | ACMP-03, ACMP-02 |
| [AcmpCore.A6BindAnotherSourceRestartsTheSink]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L485) | acmp-rebind-not-persisted; acmp-bind-new-keeps-srp | ACMP-03, ACMP-02 |
| [AcmpCore.A6TheSameTalkerAnotherSourceIsANewBinding]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L515) | acmp-bind-same-talker-is-the-same-source | ACMP-03, ACMP-02 |
| [AcmpCore.A7EachGuardTermIsChecked]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L539) | acmp-guard-controller-dropped; acmp-guard-talker-dropped; acmp-guard-unique-id-dropped; acmp-guard-sequence-id-dropped | ACMP-04 |
| [AcmpCore.A7ResponsesKeyOnTheListenerUniqueId]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L527) | acmp-response-keyed-on-the-source | ACMP-04 |
| [AcmpCore.A7ResponsesOutsideProbingAreIgnored]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L572) | acmp-responses-taken-outside-probing | ACMP-04 |
| [AcmpCore.A7TheGuardReadsTheSentProbeNotTheBinding]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L561) | acmp-guard-reads-the-binding | ACMP-04 |
| [AcmpCore.A8SuccessSettles]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L597) | acmp-header-no-tk-5s; acmp-vlan-masked; acmp-no-tk-1s; acmp-settle-starts-no-srp; acmp-settle-swaps-stream-fields | ACMP-04 |
| [AcmpCore.A9FailureWaitsForTheRetry]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L620) | acmp-header-retry-2s; acmp-failure-status-dropped; acmp-failure-retries-at-200ms | ACMP-04 |
| [AcmpCore.CommandPortBudgets]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1993) | acmp-get-rx-state-reads-the-clock; acmp-probe-response-reads-the-clock-twice; acmp-unbind-reads-the-clock; acmp-talker-reads-the-clock | PORT-01 |
| [AcmpCore.DepartingStopsEveryProbingTimer]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L1975) | acmp-probing-status-not-notified | ACMP-06 |
| [AcmpCore.DiscoveryPortBudgets]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L2027) | acmp-available-reads-the-clock-twice; acmp-departing-samples-the-grandmaster; acmp-aging-samples-the-grandmaster | PORT-01 |
| [AcmpCore.KindChangesOnlyTheSettledView]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L775) | acmp-kind-lost; acmp-kind-any-state | ACMP-04 |
| [AcmpCore.TimerPortBudgets]($LANES/tsn-c-stack-import/tests/test_acmp.cpp#L2012) | acmp-expiry-reads-the-clock-twice; acmp-second-no-resp-samples-the-grandmaster; acmp-retry-samples-the-grandmaster; acmp-delay-reads-the-clock-again; acmp-no-tk-samples-the-grandmaster | PORT-01 |
| [AdpCore.A0toA2Schedule]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L555) | gm-change-ignored; advertise-expiry-skips-delay; advertise-period-wrong; link-up-draws-startup-kind; frame-misses-config-index | ADP-02, PORT-01 |
| [AdpCore.A10toA14DepartingIndex]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L571) | departing-sends-zero | ADP-03, ADP-02 |
| [AdpCore.A15OwedDepartingAcrossARestart]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L575) | available-replaces-owed-departing | ADP-03, ADP-02 |
| [AdpCore.A16SecondShutdownQueuesItsOwn]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L579) | second-departing-dropped; second-shutdown-overwrites-index | ADP-03, ADP-02 |
| [AdpCore.A17RoomBackBeforeAPoll]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L583) | available-passes-owed-departing | ADP-03, ADP-02 |
| [AdpCore.A18LinkLossKeepsTheOwedDeparting]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L587) | link-loss-drops-owed-departing | ADP-03, ADP-02 |
| [AdpCore.A19IgnoredInputsKeepTheOwedAvailable]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L591) | gm-change-drops-owed-available; discover-drops-owed-available; stray-expiry-drops-owed-available | ADP-03, ADP-02 |
| [AdpCore.A20LinkLossDropsTheOwedAvailable]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L595) | link-loss-keeps-owed-available | ADP-03, ADP-02 |
| [AdpCore.A21DepartingCapacity]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L599) | departing-queue-unbounded; coalesced-departing-uncounted; coalesce-drops-queued-departing; coalesce-overwrites-oldest-index | ADP-03, ADP-02 |
| [AdpCore.A22GeneratorNeverStuckAtZero]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L603) | seed-left-at-zero | ADP-02, PORT-01 |
| [AdpCore.A23RepeatedEnableOrDisableChangesNothing]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L605) | enable-not-idempotent | ADP-02, PORT-01 |
| [AdpCore.A24OtherEtherTypeOrSubtypeDiscarded]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L607) | other-subtype-accepted | ADP-01, ADP-02 |
| [AdpCore.A3toA5DiscoverAndDiscard]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L559) | own-discover-discarded; down-answers-discover; foreign-discover-answered | ADP-01, ADP-02 |
| [AdpCore.A6toA8DeferredSends]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L563) | departing-keeps-index; delay-ignores-link-down; shutdown-in-down-departs | ADP-03, ADP-02 |
| [AdpCore.A9DrawKinds]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L567) | draw-kinds-merged | ADP-02, PORT-01 |
| [AdpCore.EntityFieldsUseIndependentCounts]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L633) | frame-sources-from-sinks | ADP-01, ADP-02 |
| [AdpCore.LinkLevelsAndDisabledInputs]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L611) | link-down-departs | ADP-02, PORT-01 |
| [AdpCore.MockedPortOrder]($LANES/tsn-c-stack-import/tests/test_adp.cpp#L659) | advertise-period-wrong | ADP-02, PORT-01 |
| [AdpPortEntry.RefusesBeforeTouchingState]($LANES/tsn-c-stack-import/tests/test_adp_reentry.cpp#L195) | reentry-not-ignored | PORT-01 |
| [AdpReentry.AdvertiseInlineExpiry]($LANES/tsn-c-stack-import/tests/test_adp_reentry.cpp#L139) | reentry-guard-removed; reentry-uncounted | PORT-01 |
| [AdpReentry.DelayInlineExpiryOnGmChange]($LANES/tsn-c-stack-import/tests/test_adp_reentry.cpp#L167) | reentry-guard-removed | PORT-01 |
| [ExamplePort.DefersExpiryAndRetainsBlockedOutput]($LANES/tsn-c-stack-import/tests/test_port.cpp#L8) | departing-keeps-index | PORT-01 |
| [MaapCell.TableB7]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L140) | maap-table-b7-0; maap-table-b7-1; maap-table-b7-2; maap-table-b7-3; maap-table-b7-4; maap-table-b7-5; maap-table-b7-6; maap-table-b7-7; maap-table-b7-8; maap-table-b7-9; maap-table-b7-10; maap-table-b7-11; maap-table-b7-12; maap-table-b7-13; maap-table-b7-14; maap-table-b7-15; maap-table-b7-16; maap-table-b7-17; maap-generic-initial-handles-conflict; maap-generic-probe-state-defends; maap-generic-probe-defend-uses-priority | MAAP-03 |
| [MaapCore.BeginBeforePortOperationalRetainsRange]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L321) | maap-begin-down-forgets-range | MAAP-02 |
| [MaapCore.ConstantsStrictTimersAndSeed]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L118) | maap-constant-probe_base; maap-constant-probe_variation; maap-constant-announce_base; maap-constant-announce_variation; maap-seed-clock-ignored; maap-zero-seed-sticks | MAAP-02 |
| [MaapCore.DefendEchoAndIntersection]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L222) | maap-defend-multicast; maap-defend-echo-own-range; maap-intersection-too-long | MAAP-03 |
| [MaapCore.DisjointAdjacentZeroAndDefendRange]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L235) | maap-adjacent-overlaps; maap-zero-count-conflicts; maap-defend-checks-request | MAAP-03 |
| [MaapCore.InitAndPreferredRangeBounds]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L274) | maap-range-end-off-by-one | MAAP-02 |
| [MaapCore.InitialAndThreeRetransmissions]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L95) | maap-initial-send-absent; maap-retransmit-count; maap-probe-count-not-decremented; maap-wire-version; maap-wire-length; maap-wire-source; maap-wire-padding; maap-allocation-seam-disconnected | MAAP-02 |
| [MaapCore.LinkBounceDrawsAfterSuppliedRange]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L342) | r2-saved-range-never-consumed | MAAP-02 |
| [MaapCore.MalformedAndVersionCompatibility]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L247) | maap-malformed-ethertype; maap-malformed-subtype; maap-malformed-version; maap-malformed-reserved-zero; maap-malformed-reserved-high; maap-malformed-cdl-short; maap-malformed-cdl-truncated; maap-malformed-cdl-current; maap-malformed-source-zero; maap-malformed-source-group; maap-malformed-destination; maap-malformed-own-probe; maap-valid-minimum-refused; maap-future-version-refused | MAAP-01 |
| [MaapCore.PriorityAfterTiedOctets]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L181) | maap-reverse-five-octets; maap-compare-mac-lsb-only | MAAP-03 |
| [MaapCore.QueueBoundAndWithdrawal]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L384) | maap-overflow-uncounted; maap-poll-unbounded; maap-release-leaves-output | MAAP-04 |
| [MaapCore.ReentrantPortsAreCountedAndIgnored]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L398) | maap-reentry-not-counted | PORT-01 |
| [MaapCore.ReleaseLossAndRetry]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L297) | maap-down-start-keeps-owner; maap-port-up-keeps-claim; maap-release-keeps-enable | MAAP-04 |
| [MaapCore.RestartDrawsNewRange]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L198) | maap-restart-reuses-range | MAAP-02 |
| [MaapCore.ReverseOctetPriority]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L171) | maap-numeric-mac-priority; maap-generic-equal-mac-wins | MAAP-03 |
| [MaapCore.StalledOutputRetainsOrderAndOriginalExpiry]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L365) | maap-expiry-forgotten-on-stall; maap-allocation-before-commit; maap-probe-announce-reordered; maap-stall-unqueued | MAAP-04 |
| [MaapCore.UniformDrawRejectsIncompleteBucket]($LANES/tsn-c-stack-import/tests/test_maap.cpp#L211) | maap-biased-random-bucket | MAAP-02 |
| [MaapDebug.SynchronousExpiryAsserts]($LANES/tsn-c-stack-import/tests/test_maap_debug.cpp#L10) | maap-debug-no-assert | PORT-01 |

## Delivery

Suggested PR title: Import the ADP, ACMP and MAAP cores with the validation kit (relates kebag-logic/milan-fpga#697).
Use [PR-BODY.md](PR-BODY.md). The manager pushes `import-cores` and opens the PR
against `main`. Two independent reviews remain required. The repository stays private.
No push or PR creation was performed. The consumer pin, image identity and hardware
validation belong to the later consumer lane.

[REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074485343) was posted with the full branch head. No push or PR creation was performed.
