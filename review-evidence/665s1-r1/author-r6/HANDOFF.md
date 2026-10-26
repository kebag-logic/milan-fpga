STATUS: REVIEW READY (round 6, executor [A680g]): head `424b1489ccd8062180f90158556d343589b9e1e5`; every gate rc 0

# #665 lane S1 ([A680g]): round 6, answering R701-5 and R702-5

- Branch `665-s1-faces`, from `dev-soft-core` `e76a755a` (`origin` is `kebag-logic/milan-fpga`). Nothing pushed.
- Round-6 assignment 6426858104; reviews R701-5 6426457867 and R702-5 6426851137 (PR #795). Rulings still in
  force: 6421238472 (round-5 design) and 6425357821 (memory).
- Four commits on round 5's `6d2b77bb`; nothing below it is rewritten: `e493dccd` (firmware, tests, plants),
  `168ae33d` (docs), `c66927c0` (one name per declaration, the C++ idiom ratchet), `424b1489` (two test comments'
  clauses).
- TAKEN: #665 comment 6426971677 (text in `TAKEN-COMMENT.md`); REVIEW READY: 6429960542 (text in
  `REVIEW-READY-COMMENT.md`).

## Work list (assignment 6426858104)

- [x] 1. R702-5 F1, first option: an expired lock holds, by its owner, for every reader until its release is
  applied. Named test; `probe_release_reads.cpp` unchanged at one and two interfaces (core and app arms): passes.
- [x] 2. R701-5 F1, option (a): MVU SET_SYSTEM_UNIQUE_ID refused only because a change waits or the face is held
  answers ENTITY_MISBEHAVING with the `system_unique_id` in force; another controller's lock keeps
  NOT_IMPLEMENTED. Named test (pending wait, failed wait); plant restoring status 1.
- [x] 3. R702-5 F2: named test and plant, a change asked on interface 1 that waits while interface 0's command is
  answered; the final response's egress interface asserted (SUCCESS and failure).
- [x] 4. R702-5 F3: named test in absolute milliseconds (IEEE 1722.1-2021 9.3.2.6), the service bound included;
  plants at `AECP_WAIT_MS` 130 and 115 are caught.
- [x] 5. Residue: R701-5 W1-W3 and R702-5 RES1-RES3 (W2 and RES2 reconciled, below); the stray blank line.
- [x] 6. Memory: +64 B `rom`, +0 `sram` at every point; 37.0, 40.5, 50.5 and the ledgered 57.5 unchanged. No
  compaction needed; no STOP.
- [x] Gates (table below)
- [x] PR-BODY.md, REVIEW READY

## Design

**The lock in force (item 1).** The lock that controllers see is `locked || unlocked`, owned by `lock_owner`.
At expiry the core still clears `locked` and hands the release to `changed`, so the face publishes LOCK_HELD 0
(`aecp_face.c:41` reads `locked`, unchanged). It no longer clears `lock_owner` then. `unlocked` already meant
"released, not yet notified"; it now also means "still held, by `lock_owner`, for every reader". When `applied`
turns true, the notification is built and `lock_owner` is cleared, so every reader sees the release from then
on. The readers:

- ENTITY_AVAILABLE (`aecp_commands.c:606-609`): `locked || unlocked`, `lock_owner`.
- `aecp_locked` (`aecp.c:203`), which the ACMP owner reads through `ctrl_app_aecp.c:13`.
- LOCK_ENTITY's `locked_id` (`aecp_commands.c` `lock()`, `lock_owner`, unchanged code).
- The lock check's "another controller holds it" half, now `aecp_other_lock` (`aecp_commands.c:16-21`), used by
  `aecp_foreign_lock` (`:25-28`), by the ENTITY_LOCKED-to-ENTITY_MISBEHAVING mapping (`aecp.c:372`) and by the
  MVU path (`aecp.c:273`). So during a pending release another controller is refused ENTITY_LOCKED, naming the
  owner, and the owner ENTITY_MISBEHAVING, naming itself, exactly as under a held lock while the face is held.

The alternative (keep `locked` true and have the face publish `locked && !unlocked`) was not taken: it would
change what `a.locked` means to two existing tests ("the lock still expires at sixty seconds") and to the
face, the timer and the expiry check, against four readers here. Not changed: `arm()` and the expiry check read
`locked`, the published value, so no timer is armed on the past deadline.

**The MVU refusal (item 2).** `aecp.c:271-291`: a well-formed SET_SYSTEM_UNIQUE_ID (`set`) not under another
controller's lock answers ENTITY_MISBEHAVING with the identifier in force while `refusing`, else is taken as
before. Under another controller's lock (including the lock in force of item 1) the path is unchanged:
NOT_IMPLEMENTED, echoing the request (R701-5 S4 is outside this lane).

## Changes (file:line, reason)

Commit `e493dccd` (firmware, tests, plants):
- `sw/firmware/ctrl/aecp/aecp_commands.c:16-21` `aecp_other_lock`: another controller holds the lock in force
  (R702-5 F1); `:25-28` the lock check uses it; `:606-609` ENTITY_AVAILABLE reports the lock in force; the second
  blank line after `aecp_note` removed (R701-5 S3, R702-5 S2; [A680e]'s nit).
- `sw/firmware/ctrl/aecp/aecp.c:203` `aecp_locked` reports the lock in force (the ACMP owner's reader);
  `:271-291` the MVU refusal (R701-5 F1 (a)); `:372` the refusal-status mapping uses `aecp_other_lock`; `:489-496`
  the expiry no longer clears `lock_owner`; `:497-501` the notification clears it.
- `sw/firmware/ctrl/aecp/aecp_internal.h:13` declares `aecp_other_lock`.
- `sw/firmware/ctrl/aecp/aecp.h:102-112` the `applied` port's contract: ENTITY_LOCKED under another controller's
  lock in force, and the expired lock held for every response and read until applied; `:201` `unlocked`'s comment.
- `sw/firmware/ctrl/aecp/aecp_face.h:16-20` R701-5 W2 / R702-5 RES2 (below), and the expired lock.
- `sw/firmware/ctrl/test/test_aecp.cpp:165-171` Core helper `set_system_id`; `:720-721` RES1/W1, "(#665; IEEE
  1722.1-2021 7.4.15.1)"; four tests (below).
- `sw/firmware/ctrl/test/aecp_mutants.py`: three plants re-pointed to the changed lines (same defects):
  `foreign-lock-ignored`, `unapplied-change-not-refused`, `refusal-claims-a-lock`; nine new plants (below). 137 in
  all (128 at round 5).

Commit `168ae33d` (docs):
- `docs/design/MAILBOX_SPLIT.md` "The firmware's writer": the refusal bullet (another controller's lock in force,
  the MVU refusal), the expiry bullet (the lock holds, by its owner, for every response and read until LOCK_HELD's
  commit is acknowledged), the timing paragraph (the service bound, measured in milliseconds; the egress
  interface); the AECP face's verification row names the four new tests.
- `docs/ARCHITECTURE_HW_SW_SPLIT.md:57` the expired lock; `:110-111` W2/RES2 (below).
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 5: this head's figures at all four points (firmware `e493dccd`);
  W3/RES3 (below); the 64 B this round adds; 24 B left at the shipping point before 37.5 (R702-5 S4); 1,032 B left
  at the ledgered point before 58.0; 1,016 B to return to 57.0; the compactions marked as measured at `4e3aab32`.
- `sw/firmware/ctrl/aecp/README.md`: the `applied` paragraph (the MVU refusal, the expired lock, the service bound
  and egress interface); the face's defects 50 -> 59 and their list. `sw/firmware/ctrl/README.md:602` 50 -> 59.

Commit `c66927c0`: `test_aecp.cpp:919-920`, `:923-924`, `:952-953`, `:2479-2480` one name per declaration. The docs
gates at `168ae33d` failed `check_cpp_idiom.py` alone: "multi-declarator declaration 4 > ratchet 0"
(`receipts/superseded/docs-gates-168ae33d.txt`).

Commit `424b1489`: two comments in `test_aecp.cpp`. `:870-871` cited ENTITY_AVAILABLE as IEEE 1722.1-2021 7.4.1
(ACQUIRE_ENTITY); it is 7.4.3 (`docs/history/v1/traceability/ieee1722_1-2021.md` CMD-2). `:2471-2475` states 9.3.2.6's
two bounds as `FR_NFR.md` reads them (a response within 240 ms of its command; 120 ms after an IN_PROGRESS).

### Residue as applied

- W1 = RES1: `test_aecp.cpp:720-721` exactly as written.
- W2 and RES2 give different exact text for the same two lines. `aecp_face.h`: W2's text, which contains RES2's
  ("else it fails and the core keeps the values in force (the datapath ends there once it takes the republished
  block)"). `ARCHITECTURE_HW_SW_SPLIT.md:110-111`: both sentences carried, RES2's link pointed at the in-tree
  document rather than a review-evidence copy: "otherwise the command fails and the core keeps the values in
  force. The datapath ends at them too, holding the undone value until it takes the republished block (see [the
  undone value after a failed change](design/MAILBOX_SPLIT.md#the-firmwares-writer))."
- W3 and RES3 differ in order and in "its flags" against "three flags": "All 224 B of `sram` are the core's new
  state: the held response (`AECP_HELD_BYTES`, 122 B) with its interface, length and requester, the four recorded
  values, the noted change, the wait's deadline and its three flags." The flags are `waiting`, `refusing` and
  `unlocked` (`aecp.h:197-199`); `kept` is the record's count.

### Suggestions not taken

- R701-5 S1 / R702-5 S1 (`aecp_keep` bound refusal in `aecp_init`): optional, and costs `rom` at every point.
- R701-5 S2 (state the `refuse()` invariant beside `AECP_WAITS`): optional; not asked by the assignment.
- R701-5 S5 (cite ruling 6425357821 alone in `MAILBOX_SPLIT.md`): optional; not asked.
- R702-5 S3 (`ctrl_memory.py` reason string): optional; would re-open `test_ctrl_memory.py` plants for wording.
- R702-5 S4 is taken as one sentence of section 5 (24 B left at the shipping point).

## New checks, planted mutants, failing words

Tests (`sw/firmware/ctrl/test/test_aecp.cpp`; all run in the app arm at one and two interfaces):
- `Core.AnExpiredLockHoldsByItsOwnerUntilThePlatformAppliedItsRelease` (`:872`): the release handed to the
  platform at 60 s and not notified; ENTITY_AVAILABLE from either controller reports locked by the owner;
  `aecp_locked` the same; another controller's LOCK_ENTITY ENTITY_LOCKED naming the owner, the owner's
  ENTITY_MISBEHAVING naming it; SET_CONTROL likewise; another controller's SET_SYSTEM_UNIQUE_ID NOT_IMPLEMENTED,
  the owner's ENTITY_MISBEHAVING with the identifier in force; nothing changed; once applied, one notification,
  then ENTITY_AVAILABLE and `aecp_locked` report unlocked with no owner, and another controller takes the lock.
- `Core.ASystemIdChangeWhileOneWaitsIsRefusedAsEveryChangeIs` (`:917`): ENTITY_MISBEHAVING, 54 B, the identifier
  in force, during a pending wait and after a failed wait while the platform still holds it; nothing changed;
  NOT_IMPLEMENTED under another controller's lock, applied or not; taken once unlocked and applied.
- `Core.AWaitingChangeIsAnsweredOnTheInterfaceItCameIn` (`:950`): asked on interface `AECP_TEST_INTERFACES-1`
  (1 at two interfaces), a read answered on interface 0 meanwhile; IN_PROGRESS, then SUCCESS (taken) and
  ENTITY_MISBEHAVING (failed) each leave on the asking interface, from its address, to the controller.
- `Face.AWaitingChangeIsAnsweredWithinTheInProgressCadence` (`:2476`): on the model, a change the datapath never
  takes; the model's clock advanced 1 ms at a time; the final response's frame time minus IN_PROGRESS's, in ns,
  plus `aecp_service_limit_ns` (10 ms) <= 120 ms; minus the command's, plus the service bound, <= 240 ms. Nothing
  refers to `AECP_WAIT_MS`.

Plants (`aecp_mutants.py`, each graded on its test's own words at two interfaces):

| Defect | File | Test: failing words |
|---|---|---|
| `expired-lock-read-released` | `aecp_commands.c` | `Core.AnExpiredLock...`: "ENTITY_AVAILABLE reports the lock in force: locked" |
| `expired-lock-owner-dropped` | `aecp.c` | `Core.AnExpiredLock...`: "by its owner" |
| `expired-lock-not-read-by-acmp` | `aecp.c` | `Core.AnExpiredLock...`: "the lock the ACMP owner reads is the lock in force" |
| `expired-lock-not-held-against-others` | `aecp_commands.c` | `Core.AnExpiredLock...`: "another controller's LOCK_ENTITY is refused by the lock in force, naming its owner"; "another controller's SET_SYSTEM_UNIQUE_ID keeps its status under the lock in force" |
| `expired-lock-owner-kept-once-notified` | `aecp.c` | `Core.AnExpiredLock...`: "read unlocked once notified, with no owner" |
| `system-id-refusal-not-implemented` (status restored to 1) | `aecp.c` | `Core.ASystemIdChange...`: "refused while a change waits, as every change is"; "and after the wait failed, while the platform has not applied it" |
| `waiting-response-leaves-on-the-last-interface` (the restore removed) | `aecp.c` | `Core.AWaitingChangeIsAnsweredOnTheInterfaceItCameIn`: "leaves on the interface the command came in on" |
| `wait-bound-past-the-cadence` (`AECP_WAIT_MS` 130) | `aecp.h` | `Face.AWaitingChange...Cadence`: "the final response within 120 ms of its IN_PROGRESS, the service bound included" |
| `wait-bound-past-the-cadence-with-its-service` (`AECP_WAIT_MS` 115: 115 ms alone is inside 120 ms, so only the service bound catches it) | `aecp.h` | the same words |

Re-pointed, not new (the lines changed): `foreign-lock-ignored` (`aecp_other_lock`'s comparison),
`unapplied-change-not-refused` (`return a->refusing || aecp_other_lock(a);` -> `return aecp_other_lock(a);`),
`refusal-claims-a-lock` (the mapping's new condition).

One escape found and closed before commit: `expired-lock-not-held-against-others` first failed the test only on
`ask()`'s generic "status for command 1"; the test now checks that status with its own words.

The face's defects, 59 = round 5's 50 + these 9. R701-5's `count_face_defects.py` (unchanged) prints `total 137
face-family 39 core-applied-only 18 sum 57`: it counts by test-name pattern (`Applied|LockExpiry`), and
`system-id-refusal-not-implemented` and `waiting-response-leaves-on-the-last-interface` name tests without either.

## Probes (rounds 3 to 5, unchanged, at `424b1489`)

`probes/run_all_probes.sh` runs them all; hashes in `receipts/probes/probe-hashes.txt`, each equal to its reviewer's
manifest (R702-5 `MANIFEST.sha256`, R701-5 `MANIFEST.sha256`, and round 5's `probe-hashes.txt` for rounds 3 and 4).
The C++ probes are appended to a disposable copy of `test_aecp.cpp` (`probes/run_cpp_probe.sh`) and built with
R702-5's own `run_arm.py`, reading the checkout's firmware.

| Probe | Result |
|---|---|
| R702-5 `probe_release_reads.cpp`, core and app arms, 1 and 2 interfaces | rc 0 at each: `pending-release ENTITY_AVAILABLE status=0 flags=2 lock_owner=1020304050607081`; `pending-release foreign LOCK_ENTITY status=3 locked_id=1020304050607081`; `after-applied ... flags=0 lock_owner=0` |
| R702-5 `probe_held_interface.cpp`, core arm | 2 interfaces rc 0 (`final status=0 egress=1`); 1 interface rc 1: the probe's own `GTEST_SKIP` below two interfaces, which the tally counts as a failure (fixture differs by design; the reviewer ran it at two only) |
| R702-5 `review_mutants.py` (4 mutants, 2 interfaces) | all CAUGHT; `wait-bound-past-cadence` by `Face.AWaitingChange...Cadence`, `held-interface-not-restored` by `Core.AWaitingChange...ItCameIn` (both ESCAPED at round 5) |
| R701-5 `probe_wait_refusals.cpp`, app arm, 1 and 2 interfaces | rc 0 at each: SET_NAME 10, SET_SYSTEM_UNIQUE_ID 10 during the wait and 10 after it failed |
| R701-5 `count_face_defects.py` | `total 137 face-family 39 core-applied-only 18 sum 57` (59 in the README; above) |
| R701-3 `response_probe.py` (round 5's `run_probe.py`, mailbox arm) | rc 0 at both widths |
| R701-4 `late_ack_notify_probe.py` (app arm) | its own assertions hold (`held: core_identify=0 get_control_identify=0 datapath_identify=255`; `after: datapath_identify=255 owed0=0 unsolicited_set_control=1`); fails only "status for command 24" (9, not 10), as at round 5 |
| R702-3 `probe_ack.py` (as published) | holds (`response_status=10 core_identify=0 mailbox_identify=255`); fails only its two "status for command 24" checks (9 and 10, not 0), as at round 5 |
| R702-4 `delta_probes.py` (as published) | 23 of 25 at each width (the new Face test is in its filter); getter `returned=0 last_acknowledged=0`; no notification with the unacknowledged offset; unlock `applied=1 notifications=1 registered=1`; fails only the two first-frame status fixtures, as at round 5 |

## Gate table

Final head `424b1489ccd8062180f90158556d343589b9e1e5`. `git diff --stat 6d2b77bb..HEAD`: `sw/firmware/ctrl/aecp/`
(`aecp.c`, `aecp.h`, `aecp_commands.c`, `aecp_face.h`, `aecp_internal.h`, `README.md`), `sw/firmware/ctrl/README.md`,
`sw/firmware/ctrl/test/` (`test_aecp.cpp`, `aecp_mutants.py`), `docs/` (three files); nothing under `hdl/`, `tb/`,
`syn/`, `sw/mailbox/`, `sw/litex/`, `tests/` or `configs/`, and no generated file.

| Gate | Head | Result | Receipt (`receipts/`) |
|---|---|---|---|
| `test_ctrl_firmware.py --require-rv32 --self-test`, four shards | `424b1489` | rc 0 each (438, 1,196, 591, 869 s); shard 1: 528 of 528; shard 2: AECP 137 of 137 | `fw/shard-*.txt` |
| `aecp_mutants.py --output --shard k 4`, four shards | `424b1489` | rc 0, 137 of 137 (35, 34, 34, 34), 0 escaped | `aecp-mutants/` |
| `aecp_arms.py --app --interfaces 1` and `2` | `424b1489` | rc 0, 101 of 101 each | `gates/aecp-arms-app-if*.txt` |
| the same with `--asan` | `424b1489` | rc 0, 101 of 101 each, no sanitizer report | `gates/aecp-arms-app-if*-asan.txt` |
| `fw_coverage.py --check` | `424b1489` | rc 0, 31 files at 100 %: `aecp.c` 417/417, 360/360; `aecp_commands.c` 450/450, 374/374; `aecp_face.c` 172/172, 152/152; `ctrl_app_aecp.c` 164/164, 124/124; no new exclusion | `gates/fw-coverage-check.txt` |
| linked images, four points (`probes/image_points.sh ... ledgered`, the shared `-fno-stack-protector` runtime) | `424b1489` | link and plan rc 0 at each: 37.0, 40.5, 50.5 within 56; 8x8 two interfaces 57.5 with `--ledgered-point`; refused without it (rc 2); the override refused on the other three (rc 2); ELFs identical to `e493dccd`'s link | `images/` |
| image receipt, base `e76a755a`, round 5 `6d2b77bb`, head (`probes/image_receipt.py`) | `424b1489` | +64 B `rom`, +0 `sram` at every point; 24, 488, 640 and 1,032 B of `rom` before each next granule | `images/linked-images.txt` |
| `sw/litex/test_ctrl_memory.py` (LiteX's interpreter, LiteX and migen on `PYTHONPATH`) | `424b1489` | rc 0, 0 failures | `gates/test-ctrl-memory.txt` |
| docs gates (`probes/docs_gates.sh`: the docs workflow's 69 commands, including `check_baremetal_only.py --check` and `--selftest`, `check_cpp_idiom.py`, `check_py_idiom.py`) | `424b1489` | 69 of 69 rc 0 | `gates/docs-gates.txt` |
| `cd tests && behave --no-capture -f plain` | `424b1489` | rc 0: 14 features, 406 scenarios, 1,977 steps | `gates/behave.txt` |
| every reviewer probe of rounds 3 to 5 | `424b1489` | above | `probes/` |
| `ctrl_boundary.py --require-rv32 --selftest --without verilator` | `424b1489` | rc 0, PASS, 918 s: 2,864 compiled sources of 3,094 invocations, 0 findings | `gates/ctrl-boundary-without.txt` |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` | `424b1489` | rc 0, PASS, 564 s (pinned Verilator 5.050 first on `PATH`): 790 compiled sources of 887 invocations, 0 findings; round 5 had 840 of 953, the mailbox bench's `make` finding part of its build up to date (35 s against 89 s); the twelve `ctrl_srp_image.py` builds stop at their link, as at round 5 (the stack-protected runtime, lane S3) | `gates/ctrl-boundary-only.txt` |
| `test_builder.py --require-rv32` | `424b1489` | rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN": gate 11 needs a local Arty build report this host lacks; 1,430 s | `gates/test-builder.txt` |
| four-shard Verilator sweep (`native-shards.py`, pinned Verilator 5.050 and sv2v 0.0.12, CPUs 0-3, 4-7, 8-11, 12-15) | `424b1489` | rc 0 each: shards 0 to 3 pass 15, 17, 16 and 16 suites (64), 250,913 + 1,536,446 + 380,086 + 23,679 = 2,191,124 checks, 0 in-suite failures, 0 timed out (4,538, 3,860, 5,187, 3,659 s, on 4 CPUs each); declared skips only `tsn_fuzz`'s two field campaigns (tsn-gen not installed) | `sweep/sweep-424b1489/` |
| `gen_mailbox.py --check --crosscheck`, census, `make -C tb/verilator/mbx`, `lint_rtl.py`, `KL_mbx` OOC | not rerun | rounds 5 and 6 change no file under `hdl/`, `sw/mailbox/`, `tb/` or `syn/` and no generated file; round 5's receipts (`4e3aab32`) and round 4's stand | earlier rounds |

## Process notes

- The C++ idiom ratchet (0 multi-declarators) failed at `168ae33d` on four new test declarations; fixed in
  `c66927c0`. Every gate already run at `168ae33d` and then at `c66927c0` was run again at `424b1489` after the
  clause correction; the sweep was stopped at `168ae33d` and at `c66927c0` and runs once, at `424b1489`. The
  superseded runs stay in the work directory and are not cited, except the docs gates' failure at `168ae33d`.
- A plant (`expired-lock-not-held-against-others`) was first caught only on `ask()`'s generic words; the test now
  names that status. Scratch plant runs: `receipts/plants-before-commit/`.
- No free CPU range for the sweep for about 15 minutes (another lane's candidate sweep held 112-127); `0-15` freed
  and was split four ways, as in round 5.
- `ctrl_boundary.py` and `test_builder.py` are not in the round's gate list; they were run because the firmware
  changed and the CPUs were otherwise idle while the sweep waited, without `MILAN_RV32_CC`.

## Receipts

`receipts/INDEX.md` is generated from the files present by `probes/collect_receipts.sh` (host paths replaced by
placeholders; files over 200 KB listed in `receipts/large-files.txt`, never copied). Scripts under `probes/`:
`run_gate.sh` (a command's log and its rc), `run_cpp_probe.sh` and `run_all_probes.sh` (the probes), `run_probe.py`
and `subset_mutants.py` (round 5's, unchanged), `image_points.sh` and `docs_gates.sh` (round 5's, unchanged),
`image_receipt.py` (round 5's, relabelled base / round 5 / head), `collect_receipts.sh`.
