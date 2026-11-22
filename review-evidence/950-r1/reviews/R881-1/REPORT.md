[R881] POSITIVE - exact head 287ca1ee96e69f71a5036061d2bf33c564965755

Round R881-1, internal cleared-context review of PR #961 (issues #950 and #954, part of #665). Head
`287ca1ee96e69f71a5036061d2bf33c564965755`, tree `e293283d32580fb8bcfb8fb4dc48d413cda71f68`, 9 commits on the flip
train head `15168e14` (its tree `8f6df0ed` is also dev-soft-core `59b09884`'s tree). I reconstructed the task from
AGENTS.md, the #950 and #954 bodies, the executor's TAKEN and REVIEW READY comments, the PR body, the cited code
authorities (the AECP core, the platform, SRP's registrar, tsn-c-stack's ACMP, the release talker
`KL_acmp_talker.sv`), the diff `15168e14..287ca1ee` and its history, and the public evidence packet at
`e223b05b/review-evidence/950-r1`. I also ran my own tests, plants and probes (listed in MANIFEST.sha256).

Verdict: no BLOCKER, MAJOR or MINOR is open at this head. Two RESIDUE items and two SUGGESTIONs are recorded below.
All five lenses are covered clean at this head.

## What was checked, and the result

**(1) #950: the waiting SET_STREAM_FORMAT's running check is made again.**
- `sw/firmware/ctrl/aecp/aecp.c:961`. When a waiting command is taken, `aecp_again` runs before the swap. If it
  passes, the change is swapped back in (done again), answered and notified (`a->notify = status == AECP_SUCCESS`).
  If it refuses, there is no swap, `aecp_note` gives the face the values in force, nobody is notified, and the held
  command is answered through `refuse(a, status)`. That re-runs the held command with `refusing` set, so the body
  carries the values in force. The not-taken path is unchanged (ENTITY_MISBEHAVING).
- `aecp_commands.c:140`. It returns `running(a, noted_type, noted_index)` only when `noted == AECP_CHANGE_FORMAT`,
  otherwise SUCCESS. `running` (`:127`) is the dispatch's own check from `scalar` (`:342`): brief, a STREAM_INPUT by
  `bound`, a STREAM_OUTPUT by `running`, ENTITY_MISBEHAVING when it can't observe. So the status matches the
  dispatch's: STREAM_IS_RUNNING per IEEE 1722.1-2021 7.4.9, as the dispatch already applies it.
- I checked the claim that nothing can note a change while one waits against every `aecp_note` caller:
  - `aecp_rx` sets `refusing = waiting || ...` (`aecp.c:475`). Under that, SET_CONFIGURATION, SET_NAME, the scalar
    commands, SET_STREAM_INFO, LOCK_ENTITY, SET_CONTROL and the map edits (`aecp_maps.c:437`) each refuse through
    `aecp_foreign_lock` before they note.
  - MVU SET_SYSTEM_ID refuses on `refusing` (`aecp.c:382`).
  - The lock expiry's note is in `asynchronous` (`aecp.c:813`), and `aecp_poll` returns before it while waiting
    (`:952-978`).
  - `aecp_changed` and `aecp_start_done` do not note.
  - So `noted` names the waiting command at the wait's end. The only change noting a format is SET_STREAM_FORMAT's.
- Every stream kind is covered:
  - The core test runs every STREAM_INPUT and STREAM_OUTPUT of the configuration.
  - The platform tests cover input 0 and the CRF input (S13) and every STREAM_OUTPUT (S14), at 8x8/1if and 1x1/1if.
- #947's serialization for inputs 1 to 7 is unchanged. In `ctrl_plat.c`, only comments change in
  `sink_applied`/`sink_changed`. The whole platsinks arm (S1 to S12 beside the new tests) passes at both shapes
  (`sinks-head-*.log`, "whole arm rc=0").
- The other AECP_WAITS commands are unchanged: `aecp_again` returns SUCCESS for them, and the full AECP core arm
  (178 of 178 at one and at two interfaces) and the mailbox/face arm (149 of 149) pass at the head.

**(2) #954: GET_TX_STATE REGISTERING_FAILED.**
- `ctrl_plat.c:104-107` sets `asking_failed = listener_present[n] && !registered[n]` on SRP's registrar of
  `source_interface[n]`.
- `registered` is Ready or Ready Failed (`srp_mbx.c:213`, `:1001`), and `listener_present` is a non-MT registrar
  (`:492`, `:1000`). That is the state `ctrl_app_aecp.c:62-64` reads for GET_STREAM_INFO (#943).
- tsn-c-stack maps the flag to REGISTERING_FAILED (`acmp.c:1064`; Milan v1.2 Table 5.47). The release talker answers
  from the registered Listener state alone (`KL_acmp_talker.sv:1560`, `rf_live_w`), and the new rule matches that.
- `n < CTRL_SRP_SOURCES` holds, because `n_sources = CTRL_SRP_SOURCES` (`ctrl_plat.c:328`).
- No other flag changes: the GET_TX_STATE builder is untouched, and the port only adds this field. T1 runs at every
  output at both shapes: Asking Failed sets the flag, Ready and Ready Failed do not, no other output carries it, and
  it drops once the registration goes.

**(3) Tests first and failing at the base, and every plant killed.** All reproduced here:
- On base code (`15168e14`) with the head's unchanged tests (the tests have not changed since `9ed4fc95`):
  - `Core.AWaitingFormatChangeMakesItsRunningCheckAgainOnceApplied` fails at the 1x1 and 8x8 configurations (two
    interfaces; `core-basehead-*.log`).
  - `Streams.S13`, `S14` and `T1` fail at 8x8/1if and 1x1/1if (`sinks-basehead-*.log`).
- At the head, all of them pass (`core-head-*.log`, `sinks-head-*.log`).
- AECP campaign: 12 of 12 rows caught (`plants-aecp.log`, the campaign's own planting on a copy, drift control
  first). That is the 7 `aecp_again_mutants.py` rows (aecp_again's 4 among them) and the 5 re-anchored
  waiting-command rows. The re-anchored rows still name the same defects on the new `status` lines.
- Control campaign: 6 of 6 caught (`plants-ctrl.log`, the whole table's unnamed-test check empty).

**(4) Budgets.**
- The ledger's facts at the head (`ledger-facts-head.log`):
  - `platform-8x8-one-interface` is at 58.5 (`sw/litex/ctrl_memory.py:330`) and is recorded as ROM debt of 2.5
    RAMB36 owed to the XIP lane (`:349-353`, the design doc's section 5 list `SPLIT_CONTROL_MEMORY.md:307`, the
    platform README `:175`).
  - Its own image plans at 58.5 and is refused at 59.0 (`ctrl_memory_ledger.py:86`, `:173`).
  - Every other REFUSED case is refused by `budget`.
- The full `test_ctrl_memory.py` with the pinned LiteX passes at the head: 0 failures (`tcm-head.log`, run alone).
- Arithmetic checked:
  - 139,304 - 139,264 = 40 B; 58.5 - 56 = 2.5 tiles = 10,240 B; 141,312 - 139,304 = 2,008 B left.
  - The 96 and 104 B deltas match the doc's table (`SPLIT_CONTROL_MEMORY.md:693-702`).
- `load_grade.py`: the 1x1/1if `record.aecp` is 255 in both columns (`:226`, `:279`). `load_grade.py --check` and
  `flip_grade.py --check` at both points PASS at the head (`load-grade-check-head.log`, `flip-grade-*-head.log`).
- The full CPU re-measure is the executor's, at `c7cfba76`. I confirmed that no firmware source changed between
  `c7cfba76` and the head, so those images are the head's. Its receipts agree with the REVIEW READY figures:
  23,858 cycles at 255 us, 0 of 69 statements exceeded, 241 and 240 groups, only the held-egress rows missed.

**(5) Docs.** The `aecp.h:206-215` contract, the AECP README (`:77-90` wait semantics, `:432-435` plants), the
platform README (`:87` source port, `:159` platsinks arm, `:175` the stale "reads false" limitation removed, 35
defects = 29 + 6), the design doc (`:139` ledger row, `:161-163`, `:307`, `:693-702`, section 13 `:3226-3239`), the
split-boot README `:133`, and the `test_ctrl_firmware.py:102-108` docstring. All are consistent with the code, except
the two RESIDUE wordings below.

## Findings

**RES-1 RESIDUE: Docs, `sw/firmware/ctrl/plat/README.md:85`: a stale clause about input 0 and the CRF input.**
- Authority/evidence: the #946 bullet still reads "Input 0 and the CRF input have no context here, and the core
  still does their waiting change again;". Since #950 the core first makes the change's running check again and
  refuses it STREAM_IS_RUNNING onto a stream bound meanwhile (`aecp.c:961`; S13).
- The sentence is not false, since a passed check does it again. But it is the wording that recorded the #950 gap,
  and it is now incomplete. It changes no code, figure, test or clause claim.
- Required outcome: replace it with "Input 0 and the CRF input have no context here: the core makes their waiting
  change's running check again once applied, and does it again only if it passes (#950);".
- Verification: read the line.

**RES-2 RESIDUE: Docs (comment rule of 2026-10-15), `sw/litex/ctrl_memory.py:353`: a lane name in new source text.**
- Authority/evidence: the delta adds "...by the same rule: ROM debt of 2.5 RAMB36 owed to S14" to the ledger
  entry's reason string, a new instance of a lane name in source. The existing instances, e.g. `:287` and `:331`,
  are tracked by #746.
- Wording only: no figure or test reads it.
- Required outcome: drop "owed to S14" from the new clause, or say "owed to the hybrid XIP move (#665 decision D3)".
- Verification: grep the delta's added lines for lane names.

**SUG-1 SUGGESTION: Tests, `sw/firmware/ctrl/test/test_plat_sinks.cpp:1217`/`:1226` (S13) and `:1251`/`:1264`
(S14): "keeps its format" cannot fail.**
- Evidence: S13 and S14 request the format already in force (`was`, `format`), so "S13 input n keeps its format"
  and "S14 output n keeps its format" hold whether or not the refused change is done again.
- Probe P1 swaps on every taken wait, so a refused change is done again while still answered STREAM_IS_RUNNING and
  not notified. Under P1, `Streams.*` pass at both shapes (`probe-p1-streams-*.log`).
- The defect class is caught in the same gate: the core test's `state()` includes the override byte, and plant
  `again-refusal-done-again` is killed. So this is not a coverage hole, only an assertion that cannot fail.
- Optional change: request another supported format where the stream advertises one, or drop or reword the two
  assertions.

**SUG-2 SUGGESTION: Tests, Robustness, `sw/firmware/ctrl/plat/ctrl_plat.c:104`: the source's interface selection is
untested at two interfaces.**
- Evidence: T1 runs only in the one-interface platsinks arm, where `source_interface[n]` is always 0.
- Probe P4 replaces `&p->srp.ifs[interface]` with `&p->srp.ifs[0]`. It is uncaught by platboot1, platboot2,
  platsinks8 and platsinks1 (`probe-p4.log`).
- The code is correct by reading: it uses the same index as the allocation lookup above it. The frozen acceptance
  is every output at 1x1/1if and 8x8/1if, which T1 meets.
- Optional change: a two-interface GET_TX_STATE check, e.g. in platboot2 or a follow-up Issue.

## Prior public review findings

Read after this round's verdict and ledger above were written. PR #961 has no submitted reviews and no review
comments. Its issue comments before this round are the two `INDEPENDENT REVIEW STARTED` notices (R881-1, R882-1),
and #950 and #954 hold only the executor's TAKEN and REVIEW READY. So there is no prior public review finding to
resolve or retain at this head. The parallel external round's report (posted 01:39Z, after this round started) is not
prior to this round and was not read. Its findings belong to that round's own ledger.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `aecp.c:952-978`, `aecp_commands.c:124-143` against `scalar` `:341-344` (IEEE 1722.1-2021 7.4.9); every `aecp_note` caller (`aecp.c:389,813,966`; `aecp_commands.c:228,279,366,439,559,598`; `aecp_maps.c:543`) for the "nothing notes while waiting" claim; `ctrl_plat.c:93-108` against `srp_mbx.c:213,492,1001`, `ctrl_app_aecp.c:62-64`, tsn-c-stack `acmp.c:1064`, `KL_acmp_talker.sv:1560` (Milan v1.2 Table 5.47); #950 and #954 acceptance met (S13/S14/T1, core test pass at head, fail at base) | R881-1 | 287ca1ee96e69f71a5036061d2bf33c564965755 |
| RTL | CLEAN | No HDL in the delta (`git diff --stat 15168e14..287ca1ee`: firmware, Python, docs only). Firmware state machine and widths: `aecp_poll`'s wait-end ordering (check before swap, `waiting` cleared before `aecp_note`, `refuse` with `refusing` set), `aecp_again`'s `uint16_t` arguments, `ctrl_plat.c:102-107` indices bounded by `n_sources = CTRL_SRP_SOURCES` (`:328`) and `MBX_N_IF`; the release talker `KL_acmp_talker.sv:1559-1625` read as the reference behaviour, not changed | R881-1 | 287ca1ee96e69f71a5036061d2bf33c564965755 |
| Robustness | CLEAN | Refused, unobservable, other-flag-only and timeout paths (core test cases, `aecp.c:961-976`); repeated waits after refusal (core test loop, "the refusal ends with the wait"); output stop and rebind after refusal (S13/S14 tails); Listener join/leave across Asking Failed, Ready, Ready Failed and leave (T1, `srp_mbx.c` producers); index bounds at the source port; #947's path unchanged (platsinks S1-S12 whole arm rc 0 at both shapes); SUG-2 recorded (non-blocking) | R881-1 | 287ca1ee96e69f71a5036061d2bf33c564965755 |
| Tests | CLEAN | `test_aecp.cpp:1681-1743`, `test_plat_sinks.cpp:1076-1320`, `aecp_again_mutants.py`, `aecp_mutants.py:726-760,889`, `sink_mutants.py:182-213`; my runs: core test head pass / base fail (1x1, 8x8), Streams head pass / base fail (8x8/1if, 1x1/1if), AECP plants 12/12, control plants 6/6, full AECP app arm 178/178 at if1 and if2, mailbox arm 149/149, ledger facts PASS, `test_ctrl_memory.py` 0 failures, `load_grade`/`flip_grade --check` PASS; probes P1 and P4 (SUG-1, SUG-2, non-blocking) | R881-1 | 287ca1ee96e69f71a5036061d2bf33c564965755 |
| Docs | CLEAN | `aecp.h:206-215`, `sw/firmware/ctrl/aecp/README.md:77-90,432-435`, `sw/firmware/ctrl/plat/README.md:85,87,159,175`, `docs/design/SPLIT_CONTROL_MEMORY.md:139,161-163,307,693-702,3226-3239`, `tb/verilator/ctrl_split_boot/README.md:133`, `test_ctrl_firmware.py:102-108`; figures cross-checked against `ctrl_memory.py:329-353`, `load_grade.py:219-226,276-279` and the executor's receipts; RES-1 and RES-2 are RESIDUE (wording only) | R881-1 | 287ca1ee96e69f71a5036061d2bf33c564965755 |

## Real limits

- I did not run the CPU-budget re-measure, `record_classes.py` over the harness's parts, `fw_coverage.py --check`,
  the twin simulation, the release-image identity check, the boundary gates or the docs workflow steps. For those I
  rely on the executor's published receipts at `c7cfba76`/`f90884e6`/`287ca1ee`. Firmware sources are byte-identical
  from `c7cfba76` to the head.
- I did not run the full firmware gate shards (`--self-test`). Only the named plant rows went through their
  campaigns' own planting.
- No manager source bank, builder bank or merge candidate was run or inferred. No physical calibration and no
  hardware.
- Hosted evidence at this head (`receipts/hosted-checks-287ca1ee.txt`) ran on merge commit `08749c33`, whose tree
  `e293283d` is the head's own tree.
  - `elaborate-gates-4` failed in "Standalone LiteX simulation aggregate, leg 2 of 3" with `FAIL test_ctrl_memory`
    (`receipts/hosted-elaborate-gates-4-excerpt.txt`). The base `15168e14` and other heads' runs the same hour pass
    that leg.
  - The per-test log was not uploaded, so the cause is not visible.
  - Locally, `test_ctrl_memory.py` with the pinned LiteX passes at the head with 0 failures (`tcm-head.log`), and
    the executor's receipt at `a00a3c96` also shows 0 failures. The only later commit changes doc section 13 and
    `load_grade.py`; the test reads the doc's section 3 alone (`test_ctrl_memory.py:893`).
  - One local run that went concurrently with another failed in the SoC-build arm when the CPU generator (`sbt`)
    exited 2 (`tcm-head-concurrent.log`). That is a hint at an environmental cause, not a proof.
  - Many other hosted contexts are cancelled or failed through fail-fast and union aggregation (`verilator-suites`,
    `yosys-portability`, the unions, `docs-check` refusing a cancelled `docs-gates-2`). I did not separate them
    further; acceptance is the manager's.
- Side effect to disclose: the pinned-LiteX interpreter I used read-only (`$VALIDATION_STORAGE/a433/pins-venv`)
  generated CPU Verilog into its own package during my base-tree run. That added
  `pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_191cc593...v`, `VexiiRiscvLitex_c53c0d6a...v` and
  `613077664800086b497e24c8be98f31c.py`, and touched about 177 entries under that package's generator tree.
  - These are generator caches. I left them in place: deleting part of the generator's cache could corrupt it.
  - The reviewed clone is at exact head bytes: HEAD `287ca1ee`, worktree and index clean, the index equal to the
    head tree's blobs and modes, every gitlink at its pin (tsn-c-stack `715589c1`, lwSRP `08ee86e8`, and the
    others as recorded). Nothing untracked or ignored remains; the bytecode caches from an early `--help` run were
    removed.
- Probe-run bookkeeping: `probe-p1` and the concurrent `tcm-head` run finished their output but left no `.rc` file.
  Their per-arm statuses and verdicts are in their logs, and the P1 `Streams.*` verdicts were re-run in the
  foreground (`probe-p1-streams-*.log`, rc 0).

## Pending manager duties

- Hosted acceptance at the exact head, in particular the `elaborate-gates-4` `test_ctrl_memory` failure above:
  re-run it or obtain its log.
- The current-dev merge candidate (builder and native banks) after #960, and the rebase onto it.
- Bench proof after merge.
- Carry RES-1 and RES-2 to the residue checklist.
- The executor reports that SET_CONFIGURATION and SET_STREAM_INFO also wait without repeating their bound and
  running checks. That is outside #950's frozen acceptance and unchanged here; it wants an Issue of its own if one
  is not filed.
- Decide whether the pinned-LiteX venv's regenerated CPU caches (above) need any action by its owner.

R881-1 FINISHED
