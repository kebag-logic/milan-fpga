STATUS: STOP (round 5, executor [A680e]): head `4e3aab32`; the 8x8 two-interface image plans 57.5 RAMB36, over the ledgered 57; every other gate rc 0

# #665 lane S1 ([A680e]): round 5, answering R701-4 and R702-4

- Branch `665-s1-faces`, from `dev-soft-core` `e76a755a` (`origin` is `kebag-logic/milan-fpga`).
- Round 4's 21 commits stand unrewritten; round 5 adds commits on `d33a5adc`. Nothing pushed.
- Round-5 ruling 6421238472; reviews R701-4 6421229873 and R702-4 6421210118 (PR #795).
- TAKEN: #665 comment 6421674945 (text in `TAKEN-COMMENT.md`); STOP: 6425326942 (text in `STOP-COMMENT.md`).
- Round-4 handoff: `../665s1-a680d/HANDOFF.md`.

## Work list

- [x] 1. Pending commit: IN_PROGRESS at once, then one final response, inside 120 ms / 240 ms
- [x] 2. Timed-out commit: undone in the core, ENTITY_MISBEHAVING, nothing notified, the face given the values in force
- [x] 3. Reads and notifications show only acknowledged state while a change waits
- [x] 4. Automatic unlock notified once LOCK_HELD is acknowledged, however late (R702-4 F2)
- [x] R701-4 F2: refusals carry what the command's lock refusal reports
- [x] 5. Tests and plants; the four reviewer probes of rounds 3 and 4 rerun unmodified at the final head
- [x] 6. Docs: MAILBOX_SPLIT.md, aecp_face.h, ARCHITECTURE_HW_SW_SPLIT.md:55, aecp README, FR_NFR.md:363
- [x] Linked images at the four points: 37.0 / 40.5 / 50.5 within 56; 8x8 two interfaces 57.5, over the ledgered 57: STOP
- [x] Gates (table below)
- [x] PR-BODY.md, STOP comment (`STOP-COMMENT.md`)

## Design (ruling 6421238472)

Acknowledged state is the only truth a controller sees.

- Commands whose change a face commit carries (`AECP_WAITS`, `aecp.h:116`): LOCK_ENTITY, SET_CONFIGURATION,
  SET_STREAM_FORMAT, SET_STREAM_INFO, SET_CLOCK_SOURCE, SET_CONTROL. SET_NAME, SET_SAMPLING_RATE and the map
  commands change no face value (only DYN_DIRTY, which no response or read reports), so they do not wait.
- Each change records the bytes it overwrites (`aecp_keep`, at most `AECP_KEPT` 4). When `applied` is false after
  a command of `AECP_WAITS`, the core keeps its SUCCESS response (`held`, 122 B), swaps the recorded bytes back
  (the change undone), and answers IN_PROGRESS at once, its body the values in force as the command's lock refusal
  reports them (the command re-run under `refusing`).
- While it waits: every getter, READ_DESCRIPTOR and notification reports the values in force; the face writes
  nothing (each publication is owed); every other lock-guarded change is refused; the core's own work (Table 5.22,
  probes, lock expiry) follows the wait.
- Taken by every interface within `AECP_WAIT_MS` (100 ms) of the command: swapped again (done), the held SUCCESS
  sent, then its notification; the change is handed to `changed` again (the store re-marks it; the face's owed
  interfaces are republished whole, already holding it).
- Not taken: stays undone; the change is handed to `changed` again (the face gets the values in force where its
  block is free, owes them where held; the store re-latches); ENTITY_MISBEHAVING with the values in force; no
  notification.
- Timing: IN_PROGRESS within the service bound; the final response at most 100 ms + T_svc after the command, so
  within 120 ms of the IN_PROGRESS (no second one owed) and 240 ms of the command (IEEE 1722.1-2021 9.3.2.6).
- `refusing` (`aecp.c:341`) = a change waits, or an expiry's notification waits, or `applied` false. Every lock
  check (`aecp_foreign_lock`, `aecp_commands.c:20`) refuses then, so the refusal carries what that command's lock
  refusal carries (R701-4 F2: current fields, LOCK_ENTITY's current `locked_id`); `aecp.c:366` turns its
  ENTITY_LOCKED into ENTITY_MISBEHAVING unless a foreign lock really holds.
- Lock expiry (`aecp.c:484`): released at 60 s (after a waiting change, at most 100 ms late); `unlocked` keeps its
  notification until `applied`, then sends it once (R702-4 F2); no change is taken before it leaves.
- The face (`aecp_face.c:79`, `:132`): while a change waits, `publish` writes nothing (owed instead), and `applied`
  means "no commit held" (the waiting change's commits taken), owed being what waits for it.

The reviewers' suggestions: R701-4 S2's census-row precision is applied (`MAILBOX_SPLIT.md`, the census row: "the 39
reads of 21 of the 25 class-D nets (4 are unread)"); its `census_ports.py:50` wording and the ragged reflows are not
touched (optional, and the census file would cost a census run for a comment). R701-4 S1 (the measurement image's
`main` should retry `ctrl_app_open_aecp` from the loop rather than exit) is not taken: `ctrl_aecp_image.c` is a
measurement build and the boot path is the placement switch's.

A nit to fold into the next round's first commit: `aecp_commands.c:56` is a second blank line left where
`aecp_mirror` was removed (round 5 kept it rather than move the gated head for whitespace).

Not updated at this head, pending the STOP's decision: `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 still ledgers
round 4's figures (57.0 at the ledgered point); `sw/litex/ctrl_memory.py`'s ledgered figure stays 57.

Residual (published in TAKEN, risk 1): a written commit stays in the block until the datapath takes it
(`cdc_handshake`), so after a failure the datapath takes the undone value with the late acknowledgement and holds
it until the republished block is taken; it ends at the values in force (R701-4 outcome (a), "what the datapath
finally takes"). Withdrawing a held commit needs the datapath side (the placement switch).

## Changes (file:line, reason)

Commit `bd0b7ff1` (the model, its tests and plants):
- `sw/firmware/ctrl/aecp/aecp.h:102` the `applied` port's contract restated for the new model; `:116` `AECP_WAITS`
  (bits 1, 6, 8, 14, 22, 24: the six commands a face commit carries); `:120` `AECP_WAIT_MS` 100, chosen so the final
  response follows IN_PROGRESS within the 120 ms cadence and the command within 240 ms (IEEE 1722.1-2021 9.3.2.6);
  `:123` `AECP_HELD_BYTES` 122 (SET_STREAM_INFO's response, the longest of `AECP_WAITS`); `:128` `AECP_KEPT` 4 and
  `struct aecp_kept` (address, length, 8 bytes); `:197` the core's new state (`waiting`, `refusing`, `unlocked`, the
  record, the noted change, the deadline, the held response and its requester and interface).
- `sw/firmware/ctrl/aecp/aecp_commands.c:20` the lock check also refuses while `refusing`, so a refused change
  carries what its lock refusal carries (R701-4 F2); `:28` `aecp_keep` records the bytes a change overwrites; `:41`
  `aecp_override` records the override byte; `:47` `aecp_note` records the change's kind, type and index for the
  redo; record calls at `:146`/`:154` (configuration, ENTITY copies), `:294` (scalar value), `:364` (latency),
  `:479-481` (lock state, owner, deadline), `:522-523` (identify, its descriptor byte).
- `sw/firmware/ctrl/aecp/aecp.c:91` `swap` exchanges the recorded bytes (undo, then redo); `:105` `refuse` answers the
  held command again under `refusing`, so IN_PROGRESS and the failure carry the values in force as a refusal reports
  them; `:341` `refusing` per command (a change waits, an expiry's notification waits, or `applied` false), the
  record reset only for an admitted command (a reset on every read lost the redo, found by the first Core test);
  `:366` ENTITY_LOCKED from a refusal turned ENTITY_MISBEHAVING unless a foreign lock holds; `:370` the hold: SUCCESS
  response kept, change undone, IN_PROGRESS; `:483-500` the expiry releases at 60 s and keeps its notification in
  `unlocked` until `applied` (R702-4 F2); `:582` the wait resolved: taken (done again, SUCCESS, notified) or at the
  deadline (left undone, ENTITY_MISBEHAVING, not notified), the change handed to `changed` again either way; the
  round-4 `changes()` mask, before-check and after-check are removed.
- `sw/firmware/ctrl/aecp/aecp_face.c:79` `publish` writes nothing while a change waits (the core holds it undone),
  owing the interface instead; `:132` `applied` while a change waits counts held commits only.
- `sw/firmware/ctrl/aecp/aecp_internal.h:20` declares `aecp_keep`.
- `sw/firmware/ctrl/test/test_aecp.cpp`: the round-4 Core test and three Face tests rewritten, four tests added
  (below).
- `sw/firmware/ctrl/test/aecp_mutants.py`: the round-4 plants for the removed code dropped, the face's `applied` and
  `publish` plants re-pointed, `foreign-lock-ignored` re-pointed to the new lock check; 24 new plants (below). 128 in
  all (108 at round 4).

Commit `0cce1525` (docs): `docs/design/MAILBOX_SPLIT.md` "The firmware's writer" (the model, the timing and its
clauses, GET_DYNAMIC_INFO, the residual after a failure) and the AECP face's verification row, and R701-4 S2's precision
on the census row; `docs/ARCHITECTURE_HW_SW_SPLIT.md:55-57` and `:109-112`; `docs/reference/FR_NFR.md:363` and `:374`
(the no-IN_PROGRESS policy now has its one exception); `sw/firmware/ctrl/aecp/README.md` (the `applied` paragraph,
the face's 50 defects); `sw/firmware/ctrl/README.md:602` (50); `sw/firmware/ctrl/aecp/aecp_face.h:9` (the `applied`
port); `sw/mailbox/mailbox.yaml:446` (a comment; `gen_mailbox.py --check --crosscheck` reports 0 findings, so no
generated file moves).

Commit `4e3aab32`: `aecp_commands.c:147` SET_CONFIGURATION records its override before the ENTITY copies, so a model
with more copies than `AECP_KEPT` loses an unread copy, never the override (`aecp.h:124` states the capacity);
`test_aecp.cpp:2003` (EachSetting...) requires one response per setting, and `:2635` (AHeldCommitKeepsTheLoopBusy)
checks the loop after the change has failed: two pre-existing plants, `face-write-after-response` and
`face-owed-commit-lets-the-loop-sleep`, escaped the first self-test shard 2 at `0cce1525` because a waiting change
now answers IN_PROGRESS and keeps the loop busy by itself; both are caught at `4e3aab32`.

## New checks, planted mutants, failing words

Tests (`sw/firmware/ctrl/test/test_aecp.cpp`; the Face and AppFace ones run in the app arm at one and two interfaces):
- `Core.AChangeThePlatformHasNotAppliedPromisesNothing` (`:715`), rewritten: with `applied` false, each of the twelve
  lock-guarded changes (the ten of round 4 plus START/STOP_STREAMING) answers ENTITY_MISBEHAVING, changing nothing,
  alone, with exactly the body its lock refusal carries under another controller's lock (captured first);
  LOCK_ENTITY's `locked_id` is the lock in force (none, then its owner's); a foreign lock still answers
  ENTITY_LOCKED; reads, SET_VIDEO_FORMAT, ACQUIRE and a registration answered as before (R701-4 F2).
- `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce` (`:764`), new: SET_CONTROL whose apply is late:
  IN_PROGRESS with 0, the change undone (core and descriptor), GET_CONTROL and READ_DESCRIPTOR 0, a second change and
  a LOCK_ENTITY refused with the values in force; applied: SUCCESS with 255 and the command's own sequence, then the
  notification to the other controller, handed to `changed` again. Then each command of `AECP_WAITS` (LOCK_ENTITY
  take and release, SET_CONFIGURATION, SET_STREAM_FORMAT, SET_STREAM_INFO, SET_CLOCK_SOURCE, SET_CONTROL) not applied:
  the whole core state (descriptor bytes, overrides, latencies, identify, lock, owner, deadline, configuration)
  unchanged while waiting, nothing at `AECP_WAIT_MS - 1`, one ENTITY_MISBEHAVING at `AECP_WAIT_MS` with the body
  IN_PROGRESS carried, no notification, state unchanged, the values handed to the platform again; then the same
  command applied succeeds at once. SET_NAME does not wait. A final response that cannot leave is kept.
- `Core.ALockExpiryIsNotifiedOnceThePlatformAppliedTheRelease` (`:835`), new: released at 60 s with `applied` false,
  no notification; a change refused before and after `applied` turns true until the notification leaves; exactly
  one notification, to the registered controller, `locked_id` 0; through a full ring it waits for room (R702-4 F2's
  backpressure).
- `Face.ALateCommitIsOwedAndPublishedAgainWhole` (`:2128`), rewritten (name kept: two probes anchor on it): timeout
  and rollback on the model. IN_PROGRESS with 0; the held block carries 255; core 0; GET_CONTROL and READ_DESCRIPTOR
  0; a second change refused with 0, writing nothing; nothing at 99 ms; one ENTITY_MISBEHAVING with 0 at 100 ms, no
  notification; core 0; the late acknowledgement republishes 0 whole on each interface; then 255 and R701-3's anchor
  line (0) each committed and taken before their response.
- `Face.APendingChangeIsAnsweredOnceTheDatapathTakesIt` (`:2204`), new: SET_STREAM_INFO whose own interface acknowledges
  late: IN_PROGRESS with the latency in force; GET_STREAM_INFO the latency in force; a stream-info event meanwhile waits;
  a second change refused, writing nothing; the store's status meanwhile written nowhere; then SUCCESS (4321), its
  notification, and the stream-info notification that waited, with 4321; the status reaches every interface.
- `Face.APartialAcknowledgementFailsTheChangeUntilEveryInterfaceTakesIt` (`:2251`), rewritten: one interface deaf; the
  failure gives the interface that took 255 the value 0 at once, the deaf one when its late acknowledgement frees it;
  a change refused until then.
- `Face.AMissingAcknowledgementFailsTheChangeAndRefusesEveryOther` (`:2287`), renamed and rewritten: IN_PROGRESS and
  the failure each within the service bound; the ten changes refused within it, writing nothing; reads answered; the
  lock expires at 60 s with no notification; once taken, LOCK_HELD 0 and IDENTIFY 0 on every interface and one
  unlock notification to each registered controller (R702-4 F2).
- `Face.ALockThatExpiresWhileAChangeWaitsIsNotifiedOnceTaken` (`:2336`), new: the expiry follows the wait; frames in
  order SET_CONTROL response, its notification, the unlock notification; LOCK_HELD falls before it.
- `Face.EachSettingIsCommittedBeforeTheResponseThatPromisesIt` (`:2003`) also requires one response per setting;
  `AppFace.AHeldCommitKeepsTheLoopBusy` (`:2635`) checks the loop after the change failed.

Planted (`aecp_mutants.py`, each graded on its test's own words; the self-test's shard 2 at `4e3aab32` caught 128 of
128; the 24 new ones and the six re-pointed are these 30):

| Defect | File | Test: failing words |
|---|---|---|
| `unapplied-change-not-refused` | `aecp_commands.c` | `Core.AChangeThePlatformHasNotAppliedPromisesNothing`: "refused before it changes anything" |
| `refusal-reports-the-request` | `aecp.c` | `Core.AChangeThePlatformHasNotAppliedPromisesNothing`: "the refusal reports what its lock refusal reports" |
| `refusal-claims-a-lock` | `aecp.c` | `Core.AChangeThePlatformHasNotAppliedPromisesNothing`: "status for command 6" |
| `change-before-the-expiry-is-notified` | `aecp.c` | `Core.ALockExpiryIsNotifiedOnceThePlatformAppliedTheRelease`: "nor once applied, before its notification" |
| `waiting-change-not-undone` | `aecp.c` | `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: "the change waits undone"; `Face.ALateCommitIsOwedAndPublishedAgainWhole`: "GET_CONTROL reports the value in force" |
| `unapplied-change-claims-success` | `aecp.c` | `Face.APendingChangeIsAnsweredOnceTheDatapathTakesIt`: "IN_PROGRESS alone" |
| `stream-info-does-not-wait` | `aecp.h` | `Face.APendingChangeIsAnsweredOnceTheDatapathTakesIt`: "IN_PROGRESS reports the latency in force" |
| `lock-entity-does-not-wait` | `aecp.h` | `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: "command 1 waits undone" |
| `in-progress-reports-the-request` | `aecp.c` | `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: "IN_PROGRESS reports the IDENTIFY in force" |
| `waiting-change-not-redone` | `aecp.c` | `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: "done again once applied" |
| `waiting-success-not-notified` | `aecp.c` | `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: "the final response, then its notification"; `Face.APendingChangeIsAnsweredOnceTheDatapathTakesIt`: "the response, its notification and the notification that waited" |
| `waiting-failure-notified` | `aecp.c` | `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: "one final response, no notification"; `Face.ALateCommitIsOwedAndPublishedAgainWhole`: "one final response, no notification" |
| `waiting-never-times-out` | `aecp.c` | `Face.ALateCommitIsOwedAndPublishedAgainWhole`: "one final response, no notification" |
| `waiting-times-out-early` | `aecp.c` | `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: "waits its whole bound" |
| `waiting-failure-not-republished` | `aecp.c` | `Face.APartialAcknowledgementFailsTheChangeUntilEveryInterfaceTakesIt`: "the interface that took it is given the value in force again" |
| `waiting-failure-reports-the-request` | `aecp.c` | `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: "the values in force, as IN_PROGRESS reported them"; `Face.ALateCommitIsOwedAndPublishedAgainWhole`: "with the value in force" |
| `waiting-response-forgets-its-requester` | `aecp.c` | `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: "notified to the other controller, not the one that asked" |
| `waiting-change-not-kept` | `aecp_commands.c` | `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: "the change waits undone" |
| `waiting-lock-deadline-not-kept` | `aecp.h` | `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: "command 1 waits undone" |
| `waiting-override-not-kept` | `aecp_commands.c` | `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: "command 6 waits undone" |
| `waiting-undo-misses-a-byte` | `aecp.c` | `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: "the change waits undone" |
| `waiting-expiry-not-deferred` | `aecp.c` | `Face.ALockThatExpiresWhileAChangeWaitsIsNotifiedOnceTaken`: "the expiry follows the wait" |
| `unapplied-lock-release-notified` | `aecp.c` | `Core.ALockExpiryIsNotifiedOnceThePlatformAppliedTheRelease`: "no unlock notification while the platform has not applied the release"; `Face.AMissingAcknowledgementFailsTheChangeAndRefusesEveryOther`: "no unlock notification while LOCK_HELD is held" |
| `late-lock-release-never-notified` | `aecp.c` | `Face.AMissingAcknowledgementFailsTheChangeAndRefusesEveryOther`: "the expiry, notified to each registered controller once LOCK_HELD is taken" |
| `face-never-unapplied` | `aecp_face.c` | `Face.ALateCommitIsOwedAndPublishedAgainWhole`: "IN_PROGRESS alone: no notification promises the held value" |
| `face-owed-interface-counted-applied` | `aecp_face.c` | `Face.APartialAcknowledgementFailsTheChangeUntilEveryInterfaceTakesIt`: "an owed interface is not applied while its block is free" |
| `face-held-commit-counted-applied` | `aecp_face.c` | `Face.BeforeOpenTheSettingsCarryNoReadyAndAHeldBlockIsOwed`: "a commit someone else left waiting is not applied" |
| `face-owed-counted-while-a-change-waits` | `aecp_face.c` | `Face.APendingChangeIsAnsweredOnceTheDatapathTakesIt`: "the response, its notification and the notification that waited" |
| `face-publishes-while-a-change-waits` | `aecp_face.c` | `Face.APendingChangeIsAnsweredOnceTheDatapathTakesIt`: "nothing is written while a change waits" |
| `face-publish-writes-a-held-block` | `aecp_face.c` | `Face.AMissingAcknowledgementFailsTheChangeAndRefusesEveryOther`: "no write meets a held value" |

Re-pointed, not new: `foreign-lock-ignored` (the lock check's new line), `face-never-unapplied`,
`face-owed-interface-counted-applied`, `face-held-commit-counted-applied`, `face-publish-writes-a-held-block`,
`unapplied-change-claims-success`, `unapplied-lock-release-notified` (new sites, same defects). Dropped with the
code they planted into: `unapplied-earlier-change-admits-the-next`, `held-face-admits-lock-entity`,
`held-face-admits-add-audio-mappings`, `held-face-refuses-get-control`. Re-graded: `face-write-after-response`
("one response, its commit taken inside the port").

Escapes found and closed in this round (scratch runs, `receipts/aecp-mutants/`): `waiting-undo-misses-a-byte` (graded
first on words a fatal assertion never reached), `face-publishes-while-a-change-waits` (no interface was free while
the change waited: the test now delays only the stream's own interface); and at `0cce1525`'s self-test shard 2
`face-write-after-response` and `face-owed-commit-lets-the-loop-sleep` (fixed in `4e3aab32`, above).

## Probes (unmodified; byte-identical to the reviewers' manifests)

Hashes (`receipts/probes/probe-hashes.txt`): R701-4 `late_ack_notify_probe.py` a8d51f4b...fad and R701-3
`response_probe.py` 9d018fe7...e54 (R701-4's packet manifest; R701-3's too); R702-4 `delta_probes.py` 01d60e9f...d4
and R702-3 `probe_ack.py` bfaee807...aab (R702-4's packet manifest; R702-3's too). All run at `4e3aab32`, at one
and two interfaces. `probes/run_probe.py` (round 4's `run_response_probe.py` with the arm and filter as arguments)
applies a test-editing probe to a disposable copy of the test directory and builds the checkout's firmware with it;
`probe_ack.py` and `delta_probes.py` run as published, from their own scratch directories.

The ruling's item 1 makes a waiting command's first frame IN_PROGRESS. Three probes' fixtures expect another status
there (ENTITY_MISBEHAVING in R701-4's and R702-4's, SUCCESS in R702-3's), so those three report that status check
failing; every probe's own assertion holds:

| Probe | Its own assertion | Result at `4e3aab32` |
|---|---|---|
| R701-3 `response_probe.py` (arm `mailbox`) | "a successful second response must not precede its F value" | PASS at both widths, rc 0 |
| R701-4 `late_ack_notify_probe.py` (arm `app`) | the change took effect (datapath 255) and is announced (FR-CTRL-03) | both hold: `PROBE held: core_identify=0 get_control_identify=0 datapath_identify=255`, `PROBE after: datapath_identify=255 owed0=0 unsolicited_set_control=1`; the test fails only "status for command 24" (9, not 10), rc 1 |
| R702-3 `probe_ack.py` (arm `mailbox`, two interfaces) | "successful response must not promise an unwritten F value" | holds: `response_status=10 core_identify=0 mailbox_identify=255 ... busy=1 owed=1`; the test fails only its two "status for command 24" checks (9 and 10, not 0); the script exits 1 because it exits 0 only on the defect |
| R702-4 `delta_probes.py` (arm `app`, 24 tests) | getter: no SUCCESS with the unacknowledged value; notification: none with offset 4321 while held; unlock: notified once after recovery | getter holds (`status=0 returned=0 last_acknowledged=0`), its test fails only "status for command 24"; notification holds (no 0x800f frame while held: no `REVIEW notification` line), its test fails only "status for command 14"; `ReviewAutomaticUnlockMustBeNotifiedAfterRecovery` passes (`applied=1 notifications=1 registered=1`); 22 of 24 pass at each width |

Controls: the reviewers' own runs at `d33a5adc` (their published receipts) fail each assertion above; the R701-4
probe's run there printed `unsolicited_set_control=0`, R702-4's `returned=255`, `offset=4321` and `notifications=0`.

## Gate table

Final head `4e3aab32`. Every gate below ran there unless its row says otherwise; nothing under `hdl/`, `sw/litex/`,
`syn/`, `tb/`, `tests/` or `configs/` changed since round 4's head (`git diff --stat d33a5adc..HEAD` over those paths is
empty), and `gen_mailbox.py --check --crosscheck` finds no generated file moved by the one `mailbox.yaml` comment.

| Gate | Head | Result | Receipt (`receipts/`) |
|---|---|---|---|
| `make -C tb/verilator/mbx` (Wishbone, AXI4-Lite, cosim, `run-if2`, quick plants; pinned Verilator 5.050) | `4e3aab32` | rc 0: 523, 568, 32; at two interfaces 530, 575, model 488; 7 of 7 | `gates/mbx-make.txt` |
| `gen_mailbox.py --check --crosscheck`; `--selftest` | `4e3aab32` | rc 0, 0 findings; rc 0, 0 arms failed | `gates/gen-check.txt`, `gates/gen-selftest.txt` |
| `publication_census.py --check --selftest --jobs 4` (pinned sv2v 0.0.12) | `4e3aab32` | rc 0, 934 s: 217 ports per shape, 138 arms, 43 rules removed in turn | `gates/census.txt` |
| `test_ctrl_firmware.py --require-rv32 --self-test`, four shards | `4e3aab32` | rc 0 each (332, 1,119, 405, 740 s); shard 1: 528 of 528; shard 2: AECP 128 of 128 | `fw/shard-*.txt` |
| the same, first run | `0cce1525` | shards 0, 1, 3 rc 0; shard 2 rc 1: `face-write-after-response` and `face-owed-commit-lets-the-loop-sleep` escaped (closed in `4e3aab32`) | `fw/first-run-0cce1525/` |
| `aecp_mutants.py --output`, four shards | `4e3aab32` | rc 0, 128 of 128 (32 each) | `aecp-mutants/` |
| `aecp_arms.py --app --interfaces 1` and `2` | `4e3aab32` | rc 0, 97 of 97 each | `gates/aecp-arms-app-if*.txt` |
| `fw_coverage.py --check` | `4e3aab32` | rc 0, 31 files at 100 %: `aecp.c` 414/414, 350/350; `aecp_commands.c` 448/448, 368/368; `aecp_face.c` 172/172, 152/152; `ctrl_app_aecp.c` 164/164, 124/124; no new exclusion | `gates/fw-coverage-check.txt` |
| `ctrl_boundary.py --require-rv32 --selftest --without verilator` (LiteX on `PYTHONPATH`) | `4e3aab32` | rc 0, PASS, 1,120 s | `gates/ctrl-boundary-without.txt` |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` (pinned Verilator 5.050) | `4e3aab32` | rc 0, PASS, 758 s: 840 compiled sources of 953 invocations, 0 findings | `gates/ctrl-boundary-only.txt` |
| `test_builder.py --require-rv32` | `4e3aab32` | rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN": gate 11 needs a local Arty build report this host lacks; 1,625 s | `gates/test-builder.txt` |
| `cd tests && behave --no-capture -f plain` | `4e3aab32` | rc 0: 14 features, 406 scenarios, 1,977 steps | `gates/behave.txt` |
| `test_ctrl_memory.py` (LiteX's interpreter) | `4e3aab32` | rc 0, 0 failures | `gates/test-ctrl-memory.txt` (and the system interpreter's refusal, `gates/test-ctrl-memory-system-python-refused.txt`) |
| `lint_rtl.py --check` (pinned Verilator) | `4e3aab32` | rc 0 (89 <= 89) | `gates/lint-rtl.txt` |
| docs gates (`probes/docs_gates.sh`: the docs workflow's 69 commands) | `4e3aab32` | 69 of 69 rc 0 | `gates/docs-gates.txt` (and `docs-gates-0cce1525.txt`, also 69 of 69) |
| the four reviewer probes, unmodified | `4e3aab32` | each probe's own assertion holds; three fail only their fixture's first-frame status check (above) | `probes/` |
| linked images, four points, base `e76a755a` (round 4's base images, same runtime) | `4e3aab32` | 37.0, 40.5, 50.5 within 56; 8x8 two interfaces 57.5, refused with its override (exit 2) and without it (exit 2): **the STOP**; the override still refused on the other three (exit 2) | `images/` |
| compaction measured (throwaway edits, restored) | `4e3aab32` plus edits | constant port tables in `aecp_face.c`, `aecp_mbx.c`, `ctrl_app_aecp.c`: -64 B; IN_PROGRESS carrying the held SUCCESS body: -64 B more; 119,608 B, still 57.5 | `images/compaction-*.log` |
| four-shard Verilator sweep (`native-shards.py`, pinned Verilator 5.050 and sv2v 0.0.12) | `4e3aab32` | rc 0 each: shards 0 to 3 pass 15, 17, 16 and 16 suites (64), 250,913 + 1,536,446 + 380,086 + 23,679 = 2,191,124 checks, 0 in-suite failures, 0 timed out (4,697, 4,022, 5,186, 3,704 s, on 4 CPUs each); declared skips only `tsn_fuzz`'s two field campaigns (tsn-gen not installed) | `sweep/sweep-4e3aab32/` |
| `KL_mbx` OOC, `xvlog_gate.py`, Yosys on the mailbox tops, `make -C tb/verilator/mbx mutants`, the all-fabric export | not rerun | round 5 changes no file under `hdl/`, `sw/litex/`, `syn/` or `tb/` and no generated file; round 4's receipts (989c9f53, inputs unchanged since) stand | round 4 |

## Process notes

- The first Core test run found the record reset on every command, reads included, so a redo after a read swapped
  nothing and SUCCESS went out over the undone value; the reset now happens only for a command the lock check admits.
- Two plants escaped their first grading in scratch runs and two pre-existing plants escaped the first self-test
  shard 2 (above); each was closed by a stronger test, never by a weaker plant.
- Firmware shards build from the live tree: the reorder of `4e3aab32` was queued (`pending_edits.py`, scratch) until
  the first four shards had ended, then all four were run again.
- `test_ctrl_memory.py` was first run under the system interpreter and refused 11 arms (no
  pythondata-cpu-vexiiriscv); rerun under LiteX's own, as round 4: 0 failures.
- One launch line backgrounded its whole list, so the AECP campaign's work-directory variable was empty and its
  shards never started (their redirects failed; nothing was written); relaunched alone.
- No CPU range was free for the sweep for over an hour; when `0-15` freed, it was split `0-3 4-7 8-11 12-15`, one
  per shard unit, checked against each unit's affinity at launch.
- The probes' controls are the reviewers' own runs at `d33a5adc` (their published receipts); no `d33a5adc` tree was
  rebuilt here.

## Receipts

See `receipts/INDEX.md` (generated from the files present by `probes/collect_receipts.sh`; host paths replaced by
placeholders; files over 200 KB listed with size and sha256 in `receipts/large-files.txt`). Scripts, under `probes/`:
`run_probe.py` (the probe driver), `subset_mutants.py` (scratch plant subsets), `image_points.sh` and
`image_receipt.py` (round 4's; the receipt's refusal pattern now reads a fractional figure), `docs_gates.sh`,
`collect_receipts.sh`.
