STATUS: REVIEW READY (round 4, executor [A680d]): head `d33a5adc60cd93b34be41dfacf94daaec9d059c2`, every gate rc 0

# #665 lane S1 ([A680d]): round 4, answering R701-3 and R702-3

- Branch `665-s1-faces`, from `dev-soft-core` `e76a755a` (`origin` is `kebag-logic/milan-fpga`).
- Round 3's fifteen commits stand unrewritten; round 4 adds six on `44d95625` (21 one-line commits on `e76a755a`). Nothing pushed.
- Round-4 assignment 6417644908; reviews R701-3 6417591484 and R702-3 6417635453 (PR #795).
- TAKEN: #665 comment 6417906718; REVIEW READY: 6420795336 (text in `REVIEW-READY-COMMENT.md`).
- Round-3 handoff: `../665s1-a680c/HANDOFF.md`.

## Work list

- [x] 1. F1: no SUCCESS and no notification for an unacknowledged face commit; refusal while held; lock expiry; initial publication before AECP opens
- [x] 2. Tests: delayed and missing acknowledgement, partial at two interfaces, second change while held, recovery, initial publication, lock expiry; both probes unmodified; ALateCommit checks ordering
- [x] 3. Docs: MAILBOX_SPLIT.md ordering and verification rows; aecp_face.h; R702-3 F2 through the generator; residues W1 / R1
- [x] Linked images at four points within the ledger (`989c9f53`; firmware unchanged after)
- [x] Gates (table below)
- [x] REVIEW READY (6420795336)

## The defer path, chosen by clause

The defined failure status, within the deadline: ENTITY_MISBEHAVING, inside the same service bound.
IN_PROGRESS is not used. `docs/reference/FR_NFR.md:363` (the AECP response row, IEEE 1722.1-2021
9.3.2.6: respond within 240 ms) keeps "the existing no-IN_PROGRESS policy" (and `MILAN_COMPLIANCE_MATRIX.md:134`
records that GET_DYNAMIC_INFO never answers IN_PROGRESS). ENTITY_MISBEHAVING is the status the core already gives a
datapath that does not answer in its bound (an unanswered window read, `aecp_commands.c`; a START_STREAMING
whose apply expired, `aecp.c` `aecp_start_done`).

Defined outcome of a failed apply:
- the command answers ENTITY_MISBEHAVING and notifies no one;
- its value stays in the held block, which the datapath takes if and when it acknowledges;
- until the acknowledgement returns and the poll republishes the owed interface, every state-changing AEM
  command answers ENTITY_MISBEHAVING before it changes anything (no second value joins the owed state);
- reads, registrations, START/STOP and other notifications are served as before, so service stays bounded;
- a lock expiry meanwhile releases the lock (60 s) and sends no unlock notification;
- AECP does not open until every interface has acknowledged the initial publication.

A read answered while a commit is held reports the value the core holds, which is the value the held block
carries (asserted in `ALateCommitIsOwedAndPublishedAgainWhole`). This is stated in `MAILBOX_SPLIT.md`.

## Changes (file:line, reason)

Commit `8c10b8f2` (the fix and its tests):
- `sw/firmware/ctrl/aecp/aecp.h:109` new port `applied`: whether every change given to `changed` is applied.
  The core cannot see the face; this is its only way to learn that an apply failed. `changed` stays void.
- `sw/firmware/ctrl/aecp/aecp.c:46` `applied()` calls the port inside the reentry guard; `:57` `changes()`
  names the ten state-changing AEM commands (LOCK_ENTITY 1, SET_CONFIGURATION 6, SET_STREAM_FORMAT 8,
  SET_STREAM_INFO 14, SET_NAME 16, SET_SAMPLING_RATE 20, SET_CLOCK_SOURCE 22, SET_CONTROL 24,
  ADD_/REMOVE_AUDIO_MAPPINGS 44/45) as a mask; `:339` before such a command, `applied` false: answer
  ENTITY_MISBEHAVING echoing its data, changing nothing; `:348` after a command that noted a change
  (`a->notify`), `applied` false: ENTITY_MISBEHAVING and `notify` cleared; `:462` a lock expiry notifies only
  when `applied` is true.
- `sw/firmware/ctrl/aecp/aecp_face.c:127` `applied`: no interface owed and none `BUSY`; `:277`
  `aecp_face_open` returns whether every interface's initial publication was acknowledged (it marks each
  interface owed and polls); `:290` the poll no longer tests `BUSY` itself: `publish` already refuses a held
  block and leaves it owed (the separate test was an equivalent mutant the campaign exposed, see below).
- `sw/firmware/ctrl/aecp/aecp_face.h` describes `applied`, the open's result and the poll.
- `sw/firmware/ctrl/aecp/aecp_mbx.c:100`, `sw/firmware/ctrl/app/ctrl_app_aecp.c:111` forward `applied`
  through the two adapters.
- `sw/firmware/ctrl/app/ctrl_app_aecp.c:243` `ctrl_app_open_aecp` opens nothing (no IRQ, filter or AECP)
  and returns false until the initial publication is acknowledged; `ctrl_app_aecp.h` says so.
- Tests (`sw/firmware/ctrl/test/test_aecp.cpp`): the mock port `Applied` (`:76`, default true);
  `Far.deaf` (`:1778`) withholds one interface's acknowledgement; `AppFace.acknowledged` (`:2254`).
  New and changed tests, listed under "New checks".
- `sw/firmware/ctrl/test/aecp_wire_model.hpp` gives the wire model's ports `applied` (always true).
- `sw/firmware/ctrl/test/aecp_mutants.py`: the `face-store-status-after-open` site follows the open's new
  line; twelve new defects (below).

Commit `ecfb432e` (residues and R702-3 F2):
- Both reviewers' wording residues, as listed (issue-comment IDs out of new comments, the F-number heading
  prefixes, "T0 has failed"; R701-3 offered "the request-open assertion has failed", R702-3 "the timing check
  has failed", the latter taken); comment-only in `KL_mbx_evt.sv`, `mbx.h`, `ctrl_memory.py`,
  `milan_soc.py` (a docstring), `census_plants.py`, `census_ports.py`, `census_selftest.py`,
  `mailbox_face.py`, `publication_census.py`, `tb/verilator/mbx/{mutants.py,suite.hpp,suite_face.hpp}`;
  the firmware's own were in the first commit (`aecp.h`, `aecp_face.h`, `ctrl_app_aecp.h`,
  `aecp_mutants.py`, `test_aecp.cpp`).
- `sw/mailbox/mailbox.yaml:505` F_RESTORE's doc: "the firmware's saved-state store" (R702-3 F2), regenerated
  by `gen_mailbox.py --write` into `KL_mbx_pkg.sv`, `mbx_contract.h`, `MAILBOX_CONTRACT.md` (that phrase
  only; `KL_mbx.sv` unchanged). `mailbox.yaml:443` (a comment, generating nothing) no longer promises the
  value unconditionally: one not acknowledged in the bound is promised by no response.

Commit `989c9f53`: the missing-acknowledgement test also holds the command whose own commit times out on
every interface to the AECP service bound.

## New checks, planted mutants, failing words

Tests (`sw/firmware/ctrl/test/test_aecp.cpp`, run at one and two interfaces in the app arm):
- `Core.AChangeThePlatformHasNotAppliedPromisesNothing` (`:717`): on the mock `Applied` port, false: each of the
  ten state-changing commands answers ENTITY_MISBEHAVING echoing its body, calls `Changed` never, sends the refusal
  alone (a second controller registered); GET_CONFIGURATION, GET_CONTROL, GET_AUDIO_MAP answered; SET_VIDEO_FORMAT
  still NOT_IMPLEMENTED, ACQUIRE still NOT_SUPPORTED. True then false: SET_CONTROL makes its change, answers
  ENTITY_MISBEHAVING, no notification. A lock expiry with `Applied` false: unlocked at 60 s, no 0x8001 frame.
- `Face.ALateCommitIsOwedAndPublishedAgainWhole` (`:2026`), changed to check ordering: the late command answers
  ENTITY_MISBEHAVING with no notification; a second change while held is refused, writes nothing, leaves the core at
  the held value; a read answers with the held value; per-interface acknowledgement and republish; after recovery the
  next change (R701-3's anchor line, kept verbatim) is committed and taken before its response, and its
  notification follows.
- `Face.APartialAcknowledgementFailsTheChangeUntilEveryInterfaceTakesIt` (`:2080`): the last interface withholds its
  acknowledgement (`Far.deaf`); ENTITY_MISBEHAVING; the acknowledging interface holds the value, the other holds it
  busy and owed; a stream's change on its own interface refused; acknowledged but not yet republished is still not
  applied; the poll republishes whole; the next change succeeds everywhere.
- `Face.AMissingAcknowledgementRefusesEveryChangeAndNotifiesNothing` (`:2110`): the timed-out command and each of the
  ten refusals within `aecp_service_limit_ns`; reads answered; no write meets a held block; the lock expires with no
  0x8001 notification; once acknowledged, LOCK_HELD 0 reaches every interface, still unnotified.
- `AppFaceUnacknowledged.AecpOpensOnlyOnceTheInitialPublicationIsAcknowledged` (`:2411`): `ctrl_app_open_aecp`
  false and AECP closed, nothing sent, while held; a second open refused; after the acknowledgements it opens,
  `READY` published on every interface, and AECP answers.
- `Face.BeforeOpenTheSettingsCarryNoReadyAndAHeldBlockIsOwed` gains: a commit someone else left waiting is not applied.

Planted (`aecp_mutants.py`, each graded on its test's own words; final campaign 108 of 108 at `a6519873`,
`receipts/aecp-mutants/`; in the firmware self-test's shard 2 also 108 of 108):

| Defect | Edit | Test | Failing words |
|---|---|---|---|
| `unapplied-earlier-change-admits-the-next` | `aecp.c` before-check disabled | `Core.AChangeThePlatformHasNotAppliedPromisesNothing` | "command 1 refused before it changes anything" |
| `unapplied-change-claims-success` | `aecp.c` after-check disabled | same | "a change the platform did not apply promises nothing: no notification" |
| `unapplied-lock-release-notified` | `aecp.c` expiry notifies unconditionally | `Face.AMissingAcknowledgement...` | "no unlock notification while LOCK_HELD is held" |
| `held-face-admits-lock-entity` | mask bit 1 cleared | `Core...` | "command 1 refused before it changes anything" |
| `held-face-admits-add-audio-mappings` | `(cmd \| 1u) == 45u` to `cmd == 45u` | `Core...` | "command 44 refused before it changes anything" |
| `held-face-refuses-get-control` | mask bit 25 set | `Core...` | "a read is still answered: 25" |
| `face-never-unapplied` | `applied` always true | `Face.ALateCommitIsOwedAndPublishedAgainWhole` | "the refusal alone: no notification promises the held value" |
| `face-owed-interface-counted-applied` | `applied` ignores `owed` | `Face.APartialAcknowledgement...` | "an owed interface is not applied while its block is free" |
| `face-held-commit-counted-applied` | `applied` ignores `BUSY` | `Face.BeforeOpen...` | "a commit someone else left waiting is not applied" |
| `face-publish-writes-a-held-block` | `publish` ignores `BUSY` | `Face.AMissingAcknowledgement...` | "no write meets a held value" |
| `face-open-claims-its-acknowledgement` | `aecp_face_open` returns true | `AppFaceUnacknowledged...` | "AECP opens only once the initial publication is acknowledged" |
| `aecp-opens-before-its-publication-is-acknowledged` | `ctrl_app_open_aecp` ignores the open's result | same | same |

`face-store-status-after-open` was re-pointed to the open's new line (still caught). The first campaign (before
`989c9f53`, `receipts/aecp-mutants/first-run-*`) caught 107 of 108: `face-poll-writes-a-held-block` (the poll's own
`BUSY` test removed) escaped because `publish` already refuses a held block, an equivalent mutant. The poll's test was
removed as redundant (`aecp_face.c:290`), and the defect re-planted on `publish`'s guard (above), which is caught.

## Probes (unmodified; byte-identical to the reviewers' manifests, `receipts/probes/probe-hashes.txt`)

- R701-3 `scripts/response_probe.py` (sha256 `9d018fe7...`), applied by `probes/run_response_probe.py` to a copy of
  the test directory (the only file it edits), then `Face.ALateCommitIsOwedAndPublishedAgainWhole` built from the
  checkout at one and two interfaces. Final head `a6519873`: PASS at both (`receipts/probes/r701-response-probe-final.log`).
  Control at the reviewed head `44d95625` (a detached worktree with its submodules at the pins): FAIL at both,
  "a successful second response must not precede its F value", 255 against 0, as R701-3 recorded.
- R702-3 `probe_ack.py` (sha256 `bfaee807...`), run as published from its own scratch directory against the checkout
  (two interfaces). Final head: its assertion "successful response must not promise an unwritten F value" holds:
  `response_status=10 core_identify=255 mailbox_identify=255 busy=1 owed=1`. Its test still fails, only on the
  fixture's default status check inside its two `receive(24, ...)` calls ("status for command 24", expected 0,
  actual 10): the probe expects SUCCESS from both commands it sends while the acknowledgement is withheld, which
  item 1 of the assignment forbids for the first as for the second. The script exits 1 because it exits 0 only when
  it observes the defect. Control at `44d95625`: the assertion fails (`response_status=0 ... mailbox_identify=255`),
  the script exits 0. R702-3's own stated criterion, "the corrected firmware must make that assertion pass", is met.

Commits `4903da07`, `a6519873`, `d33a5adc` (docs): `MAILBOX_SPLIT.md` "The firmware's writer" (the ordering, the
failure path and its clause, what a read reports, a datapath that never acknowledges), the verification rows (census
138 arms and 43 rules with its 217 ports; the bench's common checks 523 / 530 and the AXI4-Lite build's own 45; the
face block's bench row; the model's 488 of 530 in `run-if2`; the AECP face's host-test row; seven quick plants; the
AECP campaign); `SPLIT_CONTROL_MEMORY.md` section 5 (the ledger at `989c9f53`); `aecp/README.md` (the `applied`
contract, the face paragraph, the 30 face defects); `ctrl/README.md` (30); `ARCHITECTURE_HW_SW_SPLIT.md:106` (a
response promises a setting only once acknowledged). `docs_check.py` found one bare reference at `4903da07`, linked in
`a6519873`; `d33a5adc` rewords the writer's opening sentence.

## Gate table

Final head `d33a5adc`. A gate run at an earlier head counts for it only where no later commit touched anything the
gate reads: `a6519873` differs from `d33a5adc` in `docs/design/MAILBOX_SPLIT.md` alone; `989c9f53` differs from
`a6519873` in docs alone; `8c10b8f2`..`989c9f53` firmware commits are all in every firmware gate below.

| Gate | Head | Result | Receipt (`receipts/`) |
|---|---|---|---|
| `make -C tb/verilator/mbx` (Wishbone, AXI4-Lite, cosim, `run-if2`, quick plants; pinned Verilator 5.050) | `989c9f53` (docs after) | rc 0: 523, 568, 32; at two interfaces 530, 575, model 488; 7 of 7 | `gates/mbx-make.txt` |
| `make -C tb/verilator/mbx mutants` | `989c9f53` | rc 0: four positive controls, 199 of 199, 574 s | `gates/mbx-mutants.txt` |
| `gen_mailbox.py --check --crosscheck`; `--selftest` | `989c9f53` | rc 0, 0 findings; rc 0, 0 arms failed | `gates/gen-mailbox-*.txt` |
| `publication_census.py --check --selftest --jobs 4` (pinned sv2v 0.0.12) | `ecfb432e`; nothing it reads changed after | rc 0, 949 s locally: 217 ports per shape, 138 arms, 43 rules removed in turn | `gates/census.txt` |
| `test_ctrl_firmware.py --require-rv32 --self-test`, four shards | `989c9f53` | rc 0 each (416, 1,483, 411, 894 s); shard 1: 528 of 528; shard 2: AECP 108 of 108 | `fw/shard-*.txt` |
| `aecp_mutants.py --output`, four shards | `a6519873` | rc 0, 108 of 108 | `aecp-mutants/` |
| `aecp_arms.py --app --interfaces 1` and `2` | `a6519873` | rc 0, 93 of 93 each | `gates/aecp-arms-app-if*.txt` |
| `fw_coverage.py --check` | `a6519873` | rc 0, 31 files at 100 %: `aecp.c` 372/372, 318/318; `aecp_face.c` 172/172, 148/148; `aecp_mbx.c` 104/104, 40/40; `ctrl_app_aecp.c` 164/164, 124/124 | `gates/fw-coverage-check.txt` |
| `ctrl_boundary.py --require-rv32 --selftest --without verilator` (LiteX on `PYTHONPATH`) | `d33a5adc` | rc 0, PASS, 1,082 s | `gates/ctrl-boundary-without.txt` |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` (pinned Verilator 5.050) | `d33a5adc` | rc 0, PASS, 648 s: 775 compiled sources of 885 invocations, 0 findings | `gates/ctrl-boundary-only.txt` |
| `test_builder.py --require-rv32` | `a6519873` | rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN": gate 11 needs a local Arty build report this host lacks | `gates/test-builder.txt` |
| `cd tests && behave --no-capture -f plain` | `989c9f53` | rc 0: 14 features, 406 scenarios, 1,977 steps | `gates/behave.txt` |
| `test_ctrl_memory.py` (LiteX interpreter) | `989c9f53` | rc 0, 0 failures | `gates/test-ctrl-memory.txt` |
| `lint_rtl.py --check` (pinned Verilator); `xvlog_gate.py --check` (host lock); Yosys on `KL_mbx`, `KL_mbx_wb`, `KL_mbx_axil` | `989c9f53` | rc 0 (89 <= 89); rc 0 (0 findings); rc 0, cells 420,989 / 5 / 136, as at round 3's measured head | `gates/lint-rtl.txt`, `gates/xvlog-gate.txt`, `gates/yosys-mailbox-tops.txt` |
| docs gates (`probes/docs_gates.sh`: the docs workflow's 69 commands) | `d33a5adc` | 69 of 69 rc 0 | `gates/docs-gates.txt` (and `docs-gates-a6519873.txt`, `docs-gates-4903da07-one-finding.txt`) |
| both review probes, unmodified | `a6519873` (firmware) | R701-3: PASS at one and two interfaces (control at `44d95625` fails); R702-3: assertion holds, test fails only at its two default SUCCESS checks (control fails the assertion) | `probes/` |
| linked images, four points, base `e76a755a` (round 3's) against `989c9f53` | `989c9f53` (firmware unchanged after) | 37.0, 40.5, 50.5 within 56; 8x8 two interfaces 57.0 by its override, refused without it (exit 2); the override refused on the other three (exit 2) | `images/` |
| `KL_mbx` OOC | not rerun | round 4 changes only comments in the mailbox RTL (Yosys cells identical), so round 3's 5,515 LUT, 7,632 FF, 1/10, WNS +0.123 ns stand | round 3 `ooc/` |
| all-fabric export, five shipped configs (Arty at 100 MHz), base `e76a755a` against `989c9f53`, one scratch worktree and paths | `989c9f53`; `milan_soc.py` and `hdl/` unchanged after | normalised digest identical per config; `compare_same.py` clean (rc 0) | `export/` |
| four-shard Verilator sweep (`native-shards.py`, pinned Verilator 5.050 and sv2v 0.0.12) | `a6519873` (docs only after) | rc 0 each: shards 0 to 3 pass 15, 17, 16 and 16 suites (64), 250,913 + 1,536,446 + 380,086 + 23,679 = 2,191,124 checks, 0 in-suite failures, 0 timed out (4,200, 2,727, 3,931, 2,803 s); declared skips only `tsn_fuzz`'s two field campaigns (tsn-gen not installed) | `sweep/sweep-a6519873/` |

## Process notes

- Firmware shards 0 and 2 were first started at `ecfb432e` and stopped after about a minute to add the timed-out
  command's service-bound check (`989c9f53`); all four were then run at `989c9f53`.
- The first `ctrl_boundary.py --without verilator` run was refused at once: `MILAN_RV32_CC` pointed at the
  `-fno-stack-protector` wrapper used to link the image runtime, and `fw_rv32_selftest.py` checks the SDK's own
  stack-protector behaviour. The wrapper was dropped for the builder and boundary gates (`test_builder.py`, started
  with it, was stopped and restarted without). The firmware shards ran with it: their compiles already carry
  `-fno-stack-protector` (`ctrl_build.RV32_FLAGS`), so the wrapper's flag changes no command they run.
- The second boundary run was refused after 731 s: `test_ctrl_memory.py --build-only` needs migen; rerun with the
  LiteX checkout on `PYTHONPATH`, as round 3.
- The `--only verilator` boundary leg was restarted after two minutes to use the pinned Verilator 5.050 instead of
  the 5.052 on `PATH`.
- The docs gates found one bare file reference at `4903da07` (`docs_check.py`), fixed in `a6519873`.
- The sweep ran on CPUs 16-23, 24-31, 80-87 and 88-95 (the two free 16-CPU ranges, split), checked against every
  unit's affinity at launch.
- A detached worktree of `44d95625` with its submodules at the pins (scratch) served the probe controls and the
  export's base/head checkouts.

## Receipts

See `receipts/INDEX.md` (generated from the files present by `probes/collect_receipts.sh`; host paths replaced by
placeholders; files over 200 KB listed with size and sha256 in `receipts/large-files.txt`). Scripts used, under
`probes/`: `run_response_probe.py` (R701-3's probe driver), `image_points.sh`, `image_receipt.py`, `export_compare.sh`,
`export_digest.py`, `compare_same.py`, `docs_gates.sh` (the last six from round 3). Scratch, outside the tree: the work
directory and a detached worktree of the lane with its submodules (both left in place).
