[A680l]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `665-s1-faces` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at head `c3ba2b2647aee7fdfe220cac6634827cf5a47ec1`: a merge of `dev-soft-core` `05439833` and three commits on round 8's `614635b7`. Every gate of the round-8 set is rc 0 at this head, including the four-shard sweep (64 of 64 suites, 2,191,124 checks) and real harness builds at both points with the split CPU's instruction cache. `665-s1-faces` -> `dev-soft-core`.

Merge round 2 follows R701-8 (POSITIVE at `614635b7`) under assignment 6474448163:
- `c6ab3432` merges `dev-soft-core` at `05439833` (PR #796, lane S2c: the split CPU's 4 KiB instruction cache, `milan_soc.ctrl_cpu_args`, and the harness's `--fetch-l1` and `--xip` arms) as a merge commit; nothing is rebased. Both sides are kept: this lane's contract 2.3 face hookup, the bound acknowledgement and the ledgered point, and S2c's fetch-L1 options and arms;
- `c3ba2b26` moves the ledgered plan from a parameter of `split_soc.build` to `build.build`, because the merge gave `split_soc.build` seven parameters and the Python idiom gate allows six;
- R701-8-W1 is applied below and R701-8-W2 in the harness README (`8669b9f4`); `b198a2e1` states what the merge changes in two README claims about the cached core.

The harness's default CPU is now the split's, with the cache. On it, arm A's `aecp` group measures 25 of 25 probes at 1x1 and 39 of 39 at 8x8, with 0 T_svc misses; the worst probe is 3.442 ms at 1x1 and 4.331 ms at 8x8 (6.233 and 8.779 ms on the cacheless core at `0eda061a`). The `as-built` control is caught on both cores with cause 5. Arm B and the other two controls were not run on the cache ([Known limitations](#known-limitations--out-of-scope)).

R701-6 and R702-6 were each POSITIVE at `424b1489`, and R701-8 at `614635b7`. Outside the harness, this lane's own changes are unchanged since `614635b7`; the merge adds S2c's beside them. #665 itself stays open.

## Linked Issue / roles

Relates to #665 (lane S1: assignment 6409739310, rulings 6410169666, 6412739248, 6421238472 and 6425357821, round-4 assignment 6417644908, round-6 assignment 6426858104, merge-round assignment 6447669608, round-8 assignment 6461128613, ruling 6461910715 on its STOP, ruling 6463964028 on the two findings left open, merge-round-2 assignment 6474448163). This PR is one lane of #665 and must not close it.

Executor: `[A680l]` (earlier: `[A680]`, `[A680b]`, `[A680c]`, `[A680d]`, `[A680e]`, `[A680f]`, `[A680g]`, `[A680h]`, `[A680i]`, `[A680j]` and `[A680k]`)
Internal cleared-context reviewer: `[R701]`
External reviewer: `[R702]`

## Description

**The merge (merge round 2, `c6ab3432`).** `c6ab3432` merges `dev-soft-core` at `05439833` (PR #796, lane S2c, and the dev sync PR #798 before it) into `614635b7`, as a merge commit; nothing is rebased. Since this branch's first merge (`6660a1a0`) the two sides changed eleven files in common. Six merged without a conflict: `docs/ARCHITECTURE_HW_SW_SPLIT.md`, `docs/design/SPLIT_CONTROL_MEMORY.md` (this lane's section 3 and 5 rows, S2c's section 7), `docs/reference/FR_NFR.md`, `sw/firmware/ctrl/test/ctrl_configs.py`, `sw/litex/milan_soc.py` (this lane's `CtrlMailbox` face ports, S2c's `CTRL_FETCH_L1` and `ctrl_cpu_args` under `ctrl_mailbox`) and the harness's `run.py`. Five conflicted, all in the CPU budget harness:

| File | Conflict | Resolution |
|---|---|---|
| `build.py` | `build.build`'s call to `split_soc.build`: this lane added the ledgered point's name, S2c the XIP arm's rom image and `Core`'s fetch L1 | both: the rom image, `core.cpu_regions`, `core.fetch_l1` and the ledgered point (`c3ba2b26` then moves the name out of the call, below) |
| `split_soc.py` | `split_soc.build`'s signature and docstring: `ledgered` against `fetch_l1` | both; `ledgered_plan` kept |
| `selftest.py` | this lane's `build_checks` against S2c's `cache_checks` and `cache_build_checks`, and the list in `checks()` | all three, in that order; S2c's stub of `split_soc.build` takes the same parameters as the real one |
| `selftest_mutants.py` | this lane's two `build:` mutants against S2c's eight cache and XIP mutants | all ten |
| `README.md` | Results' opening (this lane: the firmware its figures were measured at; S2c: the cacheless commands); the self-test list and the mutant table | both. The firmware statement now covers [The instruction cache](../tb/verilator/ctrl_service_budget/README.md#the-instruction-cache) too: S2c's figures were also measured on the firmware of `e76a755a`, since neither PR #792 nor PR #796 changes a firmware source |

The merge differs from `614635b7` only in the 21 files `6660a1a0..05439833` changes, and from `05439833` only in the 66 files this lane changes since `6660a1a0`. Every file changed on one side alone equals that side's version.

| After the merge | What changed | Why |
|---|---|---|
| `c3ba2b26` `build.py`, `split_soc.py`, `selftest.py` | `build.build` holds `split_soc.build` under `split_soc.ledgered_plan(ledgered_point(shape, n_if))`; `split_soc.build` keeps S2c's six parameters; the self-test's stub of `split_soc` gains a `ledgered_plan` that patches nothing | The merged `split_soc.build` took seven parameters, and `check_py_idiom.py` failed: "too many parameters 8 > ratchet 7". `ctrl_memory.plan` is called once in `split_soc.build`, by `add_ctrl_memory`, so the patch covers the same call. The real 8x8 build plans 57.5 RAMB36 named `8x8-two-interfaces` before and after, with byte-identical tables |
| `8669b9f4` README | R701-8-W2 as written: the `as-built` control's faulting load is the `lw` at 0x24, and the trap line's last field is the last committed PC, the `bgeu` before it | R701-8 |
| `b198a2e1` README | The acknowledgement's "on this core it measures the same" is the cacheless core's, and has not been run on the cache. S2c's line that the cached CPU's `as-built` control faults with cause 1 at 0x6880 was the firmware of `e76a755a`: at this head the cached CPU is caught with cause 5 at the same load as the cacheless one | Both were true of one side's head only. The second was measured at this head (below) |

**What the cache measures on this branch.** Arm A's `aecp` group at both points, on the split's cache (the default `--fetch-l1 split`, 64 sets of one way; CPU netlist `VexiiRiscvLitex_2c4bb987...`, S2c's):

| Point | Probes | T_svc misses | Worst probe | Against S2c's cached run (`P1-64x1`, `P8-64x1`) | Against this lane's cacheless run (`0eda061a`) |
|---|---:|---:|---:|---|---|
| 1x1, one interface | 25 of 25 | 0 | 3.442 ms, READ_DESCRIPTOR t13 | +0.042 to +0.358 ms a probe; +1 mailbox access on most | -0.751 to -2.791 ms a probe |
| 8x8, two interfaces (planned 57.5, ledgered) | 39 of 39 | 0 | 4.331 ms, SET_NAME if0 | -1.801 to +1.562 ms | -1.203 to -5.424 ms |

Against S2c, the differences are this lane's firmware, as against S2 at round 8: one more access a command (the `applied` check), LOCK_ENTITY and its release +11 to +12 accesses at 1x1 (+0.19 ms) and +17 to +31 at 8x8, the first SET_NAME +21 at 1x1 and +48 on 8x8 interface 0; the rest is phase. At 8x8, about 0.43 ms moves between neighbouring probes either way with the interface whose pass a probe lands in, as in S2's own two-interface runs. The `as-built` control at 1x1 is caught on both cores, with `TRAP 166 0 5 00000020` (cacheless) and `TRAP 195 0 5 00000020` (cache), each a load access fault at the start code's first `.data` copy load.

**The `as-built` control (round 8, `124191ca` and `614635b7`, ruling 6463964028 item 1).** The control builds the CPU with the SoC's rom and sram regions unchanged, so #791's decode defect excludes every rom address with bit 15 set, and it must see the boot refused by that defect. It required an instruction access fault, cause 1, which is what the firmware of `e76a755a` met first. On this branch the 1x1 image's `.data` load image is at 0x197b0, so the start code's first copy load meets the defect first, as a load access fault, cause 5, and the control escaped.

| Piece | What changed |
|---|---|
| The control | `run.py` `AS_BUILT_CAUSES = (1, 5)` and `as_built_faults`: the run is caught by a trap refusal naming an access fault (interrupt bit 0) of cause 1 or 5, matched as a whole field. It prints `CONTROL as-built caught: an instruction or load access fault (cause 1 or 5)`. |
| Self-test | Two checks grade synthetic boot-fault logs through `grade.grade` and `run.verdict`. A cause 1 and a cause 5 fault are caught. A clean boot, an illegal instruction (2), a store access fault (7), cause 15, an interrupt numbered 5, and a bus error each escape. Four mutants, each caught: cause 1 only (the earlier rule), any trap, the cause matched by its leading digit, and caught whatever the boot does. 91 checks passed and 68 mutants were caught at round 8; 97 and 76 since the merge. |
| Real runs, 1x1 | The control at this head is caught: `TRAP 166 0 5 00000020`, rc 0. The planted control is the same run with the CPU generator handed the regions' power-of-two cover, a CPU that decodes correctly, so the image boots clean. It is graded with no trap and prints `CONTROL as-built ESCAPED`, rc 1. Its CPU netlist is the one arm A measures with. |
| README, `scenario.py` | The control's rule and why either cause is the same defect; at this head it is caught with cause 5, and a clean image escapes it. |

**The face commit acknowledgement (round 8, `c2c5abd2` to `bdad673a`, the ruling on the STOP).** With the face block's commit acknowledgement held idle, as `CtrlMailbox` holds it, the size fixture's first commit is never acknowledged, AECP never opens and the hart parks. So the harness measured nothing on this branch, at any head.

| Piece | What changed |
|---|---|
| The acknowledgement | `split_soc.StimulusMailbox.slowest_ack` drives `fw_ack_p_i`. Each interface's commit gets a one-cycle pulse `FACE_ACK_CYCLES` bus cycles after that interface's `fw_send_o` rises. `FACE_ACK_CYCLES` is the generated constant (`mailbox_model.constants`), 64 in contract 2.3, and the bound the firmware's `mbx_face_commit` waits. Every other face input stays idle by name (`FACE_IDLE_INPUTS`), so each window request times out, as the split SoC with no datapath fabric sees it. |
| Its check | Before the SoC is built, `split_soc.ack_deviations` checks two things, and the build refuses if either fails. The bound must be the firmware header's `MBX_FACE_ACK_CYCLES`. And in a migen simulation against `KL_mbx`'s commit rule, every commit must be acknowledged by exactly one pulse at rise + bound, with `fw_send_o` falling the next cycle. The simulation makes three back-to-back commits on one interface and an overlapping one on the other. Two planted mutants are refused by a real build: the pulse one cycle early, and the one-cycle datapath of the STOP's probe. |
| README | It states this one difference from `CtrlMailbox` and why, and what this head boots and measures. It also states which controls are caught here, and that the `as-built` fault is now a load (below). |

**The CPU budget harness on this branch (round 8, `27c54171`).** The merge brought lane S2's harness (`tb/verilator/ctrl_service_budget/`), which was written against the pre-contract-2.3 firmware. R701-7 found that its 8x8 point was refused by this branch's planner (F1), and that its mailbox instance and arm B predated contract 2.3 (F2).

| Piece | What changed |
|---|---|
| The ledgered point (F1) | `build.py` `LEDGERED_POINTS` names `8x8-two-interfaces` for `(endstation_ax7101_8x8, 2)` only. At that point `firmware()` passes `--ledgered-point` to `ctrl_srp_image.py`, and `add_ctrl_memory` plans to that point (`split_soc.ledgered_plan`, a patch on the planner while the harness's SoC is built; since `c3ba2b26` `build.build` applies it around `split_soc.build`). The planner refuses the override on any other image. The product SoC build names none, and `test_ctrl_memory.py` still proves that the default `add_ctrl_memory` refuses the ledgered image. `ctrl_memory.py`'s comment and `SPLIT_CONTROL_MEMORY.md` section 3 now say "the product SoC build names none; the measurement harness names it for that point only". |
| The face block (F2) | `split_soc.StimulusMailbox` connects every contract 2.3 port as `CtrlMailbox` does. The outputs are named Signals of their generated widths, unread, from `milan_soc.ctrl_mailbox_face_ports` at the build's interface count. The 19 inputs are held idle by name (`FACE_IDLE_INPUTS`), and the build refuses them unless they are exactly the inputs `CtrlMailbox` holds idle. `build.verilate` now refuses a mailbox instance (`KL_mbx`, `KL_mbx_wb`) that leaves any port unconnected, which Verilator reports as PINMISSING and `-Wno-fatal` would let pass. At the merge head 77 ports were unconnected; at this head 0 are, at both points. |
| Arm B (F2) | `answering-ports` now replaces the face block's `stream`, `avb` and `counters` ports, in the face's port table before the core takes them, with ones that answer zeroed values, and makes the fixture's `path` port answer an empty sequence. `format` stays the face's GSI read, as it stayed unsupported before. |
| Self-test | Two checks: the ledgered point is named at 8x8 with two interfaces only, by a name the planner ledgers; every labelled arm and control plant applies to the checkout's sources. Each has a mutant: the 1x1 point naming the override, and arm B's old anchors (an earlier rule). 89 checks passed and 64 mutants were caught at round 8, 62 before. |
| README | It names the firmware its figures were measured at: `dev-soft-core` `e76a755a`, before contract 2.3 (PR #792 changes no firmware source). At `27c54171` it stated that AECP never opened and no group measured; since `0eda061a` it states what the bound acknowledgement measures. Its fixture claims are past-tense for that firmware, and present-tense for this head where they differ. Its line citations resolve at the head: `aecp.c:66`, `aecp_commands.c:593`, `aecp.c:535-569`, and `MAILBOX_SPLIT.md:499-506`, `:506`, `:649-661` and `:757-762`, also in `build.py`, `scenario.py` and `grade.py`'s comments, since S1 moved those tables. |

No firmware, RTL, contract or generated file changes. The harness's images at both points are byte-identical to the merge round's linked images: 1x1 one interface `fe939fff...`, 8x8 two interfaces `654921b6...`.

**The merge (round 7).** `0052e62e` merges `dev-soft-core` at `6660a1a0` (PR #792, lane S2: the CPU budget harness `tb/verilator/ctrl_service_budget/`, the CI workflows and scripts it needs, and their docs) into `424b1489`, as a merge commit; nothing is rebased. One file is changed on both sides, `sw/firmware/ctrl/test/ctrl_configs.py`: each side appended to `OUTSIDE` after `sw/mailbox/publication_census.py`. Both are kept verbatim, each with its own reason: this lane's `sw/mailbox/census_ports.py` entry ("classifies every port of the processor wrapper in the census's netlists, naming the firmware that writes each face (#665 S1); it compiles nothing"), then S2's comment and its five harness entries (`build.py`, `runtime_ssp.py`, `scenario.py`, `selftest.py`, `split_soc.py`). S2's `SUITES` entry (`fixture_variant.py`) merged cleanly. The merge differs from `424b1489` only in S2's 36 files and from `6660a1a0` only in this lane's files, and every file but `ctrl_configs.py` equals the version of the side that changed it. The four linked images are byte-identical to round 6's.

The split placement removes the whole processor wrapper (`KL_pp_shadow`, ruling 6088423771, decision 1). This branch decides each of its 217 ports and adds what the mailbox must still carry, as contract 2.3, an additive minor. The all-fabric build is unchanged: its export is digest-identical for every shipped config.

| Piece | What changed |
|---|---|
| Port census | `sw/mailbox/census_ports.py` names each `pp_shadow` port under one class in all six shapes: C 25, F 28, R 34, E 6, M 14, G 110. A G output's cone may end only at the CSR block's processor-status inputs, the twenty memory-master outputs, or `pp_maap_shim` while that shim feeds `pp_shadow` alone. It stops at the map writer's 25 nets, which go with the wrapper; the placement switch must pass the census without that exclusion. There are 12 rules with 18 plants, which ride on existing netlists. |
| Contract 2.3 | `sw/mailbox/mailbox.yaml`, with `mailbox_face.py` the face block's generator and new checks and arms. Each interface's face block holds the settings, published by one commit per interface with a bounded acknowledgement. There are four request windows (CTR, AMAP, EDIT, GSI) with tag and timeout, and four events (COUNTERS_CHANGED per descriptor with a 1,000 ms holdoff, AVB_INFO_CHANGED, AS_PATH_CHANGED, AMAP_LIVE_WRITE). |
| RTL | `KL_mbx` is regenerated with the face ports, and `KL_mbx_evt` gains the face events. `CtrlMailbox` names every face port and leaves it unread, its inputs idle. `milan_datapath.sv` is not touched. Rounds 5 and 6 change no RTL. |
| Firmware | `aecp_face.c` answers the AECP owner's `changed`, `applied`, `format`, `counters`, `stream` and `avb` ports on the face block. A setting is written and committed, and its acknowledgement awaited within a bound. A lock change and a lock expiry are published (`AECP_CHANGE_LOCK`). The store's restore and NVM status are written before AECP opens and on each change. `ctrl_app_open_aecp` opens AECP only once every interface has acknowledged the initial publication. |
| Acknowledged state (round 5) | LOCK_ENTITY, SET_CONFIGURATION, SET_STREAM_FORMAT, SET_STREAM_INFO, SET_CLOCK_SOURCE and SET_CONTROL (`AECP_WAITS`) carry their change in a face commit. Each change records the bytes it overwrites. When `applied` is false after one of them, the core keeps its SUCCESS response, undoes the change, and answers IN_PROGRESS at once with the values in force. Taken by every interface within `AECP_WAIT_MS` (100 ms), the change is done again, and SUCCESS then its notification follow. Otherwise it stays undone and the command answers ENTITY_MISBEHAVING with the values in force, notifying no one. While a change waits, every getter, READ_DESCRIPTOR and notification reports the values in force, the face writes nothing, and the core's own work follows the wait. While a change waits, an expiry's notification waits, or any interface is held or owed, the lock check refuses every other change, with what the command's lock refusal reports. |
| The lock in force (round 6, R702-5 F1) | A lock still expires at 60 s, and its release (LOCK_HELD 0) is still committed then. Until that commit is acknowledged, however late, the lock holds, by its owner, for every response and read. ENTITY_AVAILABLE, LOCK_ENTITY's `locked_id`, the lock the ACMP owner reads (`aecp_locked`) and every refusal report it. So another controller is refused ENTITY_LOCKED, naming the owner, and the owner is refused ENTITY_MISBEHAVING, as under a held lock while the face is held. The expiry's notification leaves once the commit is acknowledged, and from then on the lock is released for every reader. `aecp_other_lock` (`aecp_commands.c`) is the one predicate the lock check, the refusal status and the MVU path use. |
| SET_SYSTEM_UNIQUE_ID (round 6, R701-5 F1, option (a)) | Refused only because a change waits or the face is held, it answers ENTITY_MISBEHAVING with the `system_unique_id` in force, changing nothing, as the AEM refusals do. Under another controller's lock, including the lock in force above, it keeps NOT_IMPLEMENTED. |
| Memory budget | `ctrl_memory.plan` keeps refusing any image past 56 RAMB36. One named override, `8x8-two-interfaces`, lets that point's measurement plan 57.5 (ruling 6425357821), and refuses it past that. The override is refused on every other point. `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 ledgers this head's figures at all four points (below). |
| Tests | The face block's checks run through both adapters, at two interfaces and on the host model, with 24 RTL face arms and 6 model twins. GoogleTest's `Core`, `Face`, `FaceLatency`, `AppFace` and `AppFaceUnacknowledged` hold 101 tests at each interface count. The AECP campaign plants 137 defects, 59 of them the face's. Coverage is 100 % lines and branches with no new exclusion. |
| Docs | `docs/design/MAILBOX_SPLIT.md` "The firmware's writer" (the model, the lock in force, the MVU refusal, its timing and clauses, and "the undone value after a failed change", named and accepted below) and the verification rows; `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3, 5 and 6; `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 1; `docs/reference/FR_NFR.md` (the AECP response row's IN_PROGRESS policy); the aecp and ctrl READMEs; `aecp.h`; `aecp_face.h`. |

**The timing, by clause.** IN_PROGRESS leaves within the service bound of the command. The final response leaves at most `AECP_WAIT_MS` plus the service bound after the command. That is inside the 120 ms IN_PROGRESS cadence of IEEE 1722.1-2021 9.3.2.6, so no second IN_PROGRESS is owed, and inside its 240 ms. `Face.AWaitingChangeIsAnsweredWithinTheInProgressCadence` measures both on the model's millisecond clock, with the 10 ms service bound added, and never reads `AECP_WAIT_MS`. A plant at 130 ms and one at 115 ms (inside 120 ms alone, outside it with the service bound) are each caught. The final response leaves on the interface its command came in on. No getter waits, so GET_DYNAMIC_INFO, which carries only getters, never answers IN_PROGRESS (IEEE 1722.1-2021 7.4.76). `FR_NFR.md`'s no-IN_PROGRESS policy names this one exception.

**Tests for the model.**

- `Core.AChangeThePlatformHasNotAppliedPromisesNothing`: every lock-guarded change refused, its body exactly its lock refusal's; reads answered.
- `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: pending then success, with a getter, READ_DESCRIPTOR and a second command meanwhile; then each of the six commands timing out with the whole core state unchanged and no notification.
- `Core.ALockExpiryIsNotifiedOnceThePlatformAppliedTheRelease`: the expiry's notification held until applied, through a full ring.
- `Core.AnExpiredLockHoldsByItsOwnerUntilThePlatformAppliedItsRelease` (round 6): ENTITY_AVAILABLE from either controller, `aecp_locked`, LOCK_ENTITY's `locked_id`, the refusals' status, and SET_SYSTEM_UNIQUE_ID all report the lock in force until the release is applied. Once it is notified, they report it released.
- `Core.ASystemIdChangeWhileOneWaitsIsRefusedAsEveryChangeIs` (round 6): ENTITY_MISBEHAVING with the identifier in force during a pending wait and after a failed wait; NOT_IMPLEMENTED under another controller's lock.
- `Core.AWaitingChangeIsAnsweredOnTheInterfaceItCameIn` (round 6): asked on interface 1 while interface 0's command is answered meanwhile. IN_PROGRESS, SUCCESS and the failure each leave on interface 1, from its address.
- `Face.AWaitingChangeIsAnsweredWithinTheInProgressCadence` (round 6): above.
- `Face.ALateCommitIsOwedAndPublishedAgainWhole`, `Face.APendingChangeIsAnsweredOnceTheDatapathTakesIt`, `Face.APartialAcknowledgementFailsTheChangeUntilEveryInterfaceTakesIt`, `Face.AMissingAcknowledgementFailsTheChangeAndRefusesEveryOther`, `Face.ALockThatExpiresWhileAChangeWaitsIsNotifiedOnceTaken`.
- Round 6's nine new plants: an expired lock read as released, its owner dropped, unread by the ACMP owner, not held against another controller, or its owner kept once notified; SET_SYSTEM_UNIQUE_ID's refusal at status 1; the waiting response's interface restore removed; `AECP_WAIT_MS` at 130 and at 115. Three round-5 plants were re-pointed to the lines this round changed.

**Every reviewer probe of rounds 3 to 5, unchanged, at round 6's head `424b1489`** (neither merge changes a file they read). Each probe file's sha256 equals its reviewer's published manifest.

| Probe (unchanged) | Result at `424b1489` |
|---|---|
| R702-5 `probe_release_reads.cpp`, core and app arms, one and two interfaces | passes at each: `pending-release ENTITY_AVAILABLE flags=2 lock_owner=1020304050607081`, `pending-release foreign LOCK_ENTITY status=3 locked_id=1020304050607081`, `after-applied ENTITY_AVAILABLE flags=0 lock_owner=0` |
| R702-5 `probe_held_interface.cpp`, two interfaces | passes: `final status=0 egress=1`. At one interface the probe skips itself (`AECP_TEST_INTERFACES < 2`), and the harness's tally counts that skip as a failure, so that run exits 1 by the probe's design; the reviewer ran it at two interfaces only |
| R702-5 `review_mutants.py`: `wait-bound-past-cadence`, `held-interface-not-restored`, `owed-change-not-refused`, `record-not-reset` | each CAUGHT at two interfaces; the first two escaped at round 5 and are caught by `Face.AWaitingChangeIsAnsweredWithinTheInProgressCadence` and `Core.AWaitingChangeIsAnsweredOnTheInterfaceItCameIn` |
| R701-5 `probe_wait_refusals.cpp`, app arm, one and two interfaces | passes at each: SET_NAME 10; SET_SYSTEM_UNIQUE_ID 10 during the wait and 10 after the failed wait |
| R701-5 `count_face_defects.py` | `total 137 face-family 39 core-applied-only 18 sum 57`. The README's 59 is round 5's 50 plus round 6's nine; the script counts by test name (`Applied` or `LockExpiry`), and two new plants' tests (`ASystemIdChange...`, `AWaitingChangeIsAnsweredOnTheInterface...`) name neither |
| R701-3 `response_probe.py`, mailbox arm, one and two interfaces | passes |
| R701-4 `late_ack_notify_probe.py`, R702-4 `delta_probes.py`, R702-3 `probe_ack.py` | each one's own assertion holds; each fails only its first-frame status fixture, by design (next table) |

**The three probe fixtures whose first-frame status check differs.** Item 1 of ruling 6421238472 makes a waiting command's first frame IN_PROGRESS (9), by design. Each fixture below was written before that ruling and checks the first frame's status against the outcome of its own round. The probes are not edited.

| Probe (unchanged) | Fixture's status check | Status at `424b1489`, and why | The probe's own assertion |
|---|---|---|---|
| R701-4 `late_ack_notify_probe.py`, `Face.ReviewerProbeALateAcknowledgedChangeIsAnnounced` | SET_CONTROL (command 24): ENTITY_MISBEHAVING (10), round 4's immediate failure | IN_PROGRESS (9): the change waits for the acknowledgement the probe withholds | holds: `PROBE held: core_identify=0 get_control_identify=0 datapath_identify=255`, then `PROBE after: datapath_identify=255 owed0=0 unsolicited_set_control=1` |
| R702-4 `delta_probes.py`, `Face.ReviewGetterMustNotPromiseUnacknowledgedIdentify` and `Face.ReviewStreamNotificationMustNotPromiseUnacknowledgedOffset` | SET_CONTROL (24) and SET_STREAM_INFO (14): ENTITY_MISBEHAVING (10) | IN_PROGRESS (9), for the same reason | holds: `REVIEW getter: status=0 returned=0 last_acknowledged=0`; no notification with the unacknowledged offset while it is held; `ReviewAutomaticUnlockMustBeNotifiedAfterRecovery` passes (`applied=1 notifications=1 registered=1`); 23 of 25 tests pass at each width |
| R702-3 `probe_ack.py`, `Face.ReviewHeldSettingMustNotPromiseUnwrittenValue` | SET_CONTROL (24): SUCCESS (0), round 3's answer once acknowledged | IN_PROGRESS (9) first, then ENTITY_MISBEHAVING (10): the probe holds the acknowledgement past `AECP_WAIT_MS`, so the change fails and stays undone (ruling item 2) | holds: `response_status=10 core_identify=0 mailbox_identify=255`, so no SUCCESS promises the unwritten value; the script exits 1 because it exits 0 only on the defect |

**The memory figure.** Round 6 added 64 B of `rom` and no `sram` at every point, against round 5's head `6d2b77bb`, and moved no point's RAMB36 count. Neither merge adds anything: the four images linked at `0052e62e` and at this head are byte-identical to `424b1489`'s, and plan the same. Every image is linked against the same runtime (built with `-fno-stack-protector`):

| Point (linked image, planned) | `rom` B, base -> round 5 -> head | `sram` B, base -> head | RAMB36, base -> round 5 -> head | Held to |
|---|---:|---:|---:|---|
| 1x1, one interface | 97,920 -> 104,360 -> 104,424 | 45,920 -> 46,256 | 35.5 -> 37.0 -> 37.0 | 56 |
| 1x1, two interfaces | 99,416 -> 105,944 -> 106,008 | 57,312 -> 57,648 | 38.5 -> 40.5 -> 40.5 | 56 |
| 8x8, one interface | 111,648 -> 118,080 -> 118,144 | 86,496 -> 86,832 | 49.0 -> 50.5 -> 50.5 | 56 |
| 8x8, two interfaces | 113,208 -> 119,736 -> 119,800 | 112,656 -> 112,992 | 56.0 -> 57.5 -> 57.5 | 57.5, by its override (ruling 6425357821) |

The 64 B are `aecp_other_lock` (+64), `aecp_command` (+32), `aecp_locked` (+16), `aecp_rx` (+8), `aecp_poll` (-8) and `aecp_foreign_lock` (-48). The largest point has 1,032 B of `rom` left before 58.0, and 1,016 B would return it to 57.0. The shipping point has 24 B left before 37.5. No compaction was needed, so none is taken. The two measured at round 5 (-64 B each) would leave 119,672 B, still 57.5. Section 5 of `SPLIT_CONTROL_MEMORY.md` records all of this.

## Authoritative references

- #665: ruling 6088423771 (decisions 1 and 2), decisions 6409738976 (D1, D3), assignment 6409739310, rulings 6410169666, 6412739248, 6421238472 and 6425357821, owner clarification 6410301079, round-4 assignment 6417644908, round-6 assignment 6426858104, merge-round assignment 6447669608, round-8 assignment 6461128613, the ruling on its STOP 6461910715 (option (c)), ruling 6463964028 and merge-round-2 assignment 6474448163; PR #795 R701-7 (6461122749) and R701-8 (6466412104); PR #795 reviews R701-5 (6426457867) and R702-5 (6426851137), and R701-6 and R702-6 (POSITIVE at `424b1489`)
- IEEE 1722.1-2021 7.4 (7.4.2 lock, 7.4.3 entity available, 7.4.5.1, 7.4.7 configuration, 7.4.15.1, 7.4.23 clock source, 7.4.42 counters, 7.4.76), 7.5.2 and 9.3.2.6
- Milan v1.2 5.3.7.3, 5.4.2.2, 5.4.2.12, 5.4.4.2, 5.4.5.2 (Table 5.22), 5.6.1; FR-CTRL-03
- Contract 2.3's commit bound: `sw/mailbox/mailbox.yaml` `interface_face_registers.ack_cycles` (64), the generated `MBX_FACE_ACK_CYCLES`, `KL_mbx.sv` `face_commit`
- PR #796 (lane S2c): `docs/design/SPLIT_CONTROL_MEMORY.md` section 7, the split CPU's instruction cache
- `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 1; `docs/reference/FR_NFR.md` (the AECP rows); `docs/design/MAILBOX_SPLIT.md`; `docs/reference/MAILBOX_CONTRACT.md`; `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3, 5 and 6
- `CONTRIBUTING.md` (CDC: every handshake crosses through `cdc_handshake` or toggle-plus-sync)

## How to get into the same state

```sh
git fetch origin
git checkout 665-s1-faces
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

## How to validate

```sh
python3 sw/firmware/ctrl/test/aecp_arms.py --output "$OUT/app1" --app --interfaces 1
python3 sw/firmware/ctrl/test/aecp_arms.py --output "$OUT/app2" --app --interfaces 2
python3 sw/firmware/ctrl/test/aecp_mutants.py --output "$OUT/plants0" --shard 0 4
python3 sw/firmware/ctrl/test/aecp_mutants.py --output "$OUT/plants1" --shard 1 4
python3 sw/firmware/ctrl/test/aecp_mutants.py --output "$OUT/plants2" --shard 2 4
python3 sw/firmware/ctrl/test/aecp_mutants.py --output "$OUT/plants3" --shard 3 4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4
python3 sw/firmware/gtest/fw_coverage.py --check
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/ci_rv32_sdk.py --destination "$SDK"
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
python3 sw/builder/test_builder.py --require-rv32
python3 sw/litex/test_ctrl_memory.py
python3 sw/builder/test_soc_options.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$OUT/budget-1x1" \
  --groups aecp --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir "$OUT/budget-8x8" \
  --groups aecp --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$OUT/budget-1x1-ports" \
  --fetch-l1 none --variant answering-ports --groups aecp-fanout --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir "$OUT/budget-8x8-ports" \
  --fetch-l1 none --variant answering-ports --groups aecp-fanout --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$OUT/budget-slow-adp" \
  --fetch-l1 none --mutation slow-adp-rx
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$OUT/budget-as-built" \
  --fetch-l1 none --cpu-regions as-built
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$OUT/budget-as-built-cache" \
  --cpu-regions as-built
(cd tests && behave --no-capture -f plain)
bash scripts/run_all_suites.sh "$OUT/sweep" --wait
python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml \
  --interfaces 2 --with-aecp --layout split --ledgered-point 8x8-two-interfaces --output "$OUT/image" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
python3 sw/litex/ctrl_memory.py plan "$OUT/image/ctrl_app.elf" --stage-bytes 13264 \
  --ledgered-point 8x8-two-interfaces
```

At this head every command above was run except the following. `aecp_arms.py` and `aecp_mutants.py` (`424b1489`; the firmware self-test's shard 2 runs the same 137 AECP plants, all caught), and `gen_mailbox.py --check --crosscheck` and `--selftest`, `publication_census.py --check --selftest --jobs 4` and `make -C tb/verilator/mbx` (rounds 4 and 5; the sweep runs `mbx` again), read no file either merge or round 8 changes, so their receipts stand. The two arm B commands and `slow-adp-rx` were not run again either: their figures are this lane's cacheless runs at `0eda061a`. The merge does change the harness they run in (S2c's `--fetch-l1` selection, its fetch observers in `build.py` and `sim_main.cpp`), and with `--fetch-l1 none` S2c recorded S2's cacheless figures again; at this head that is shown only by the cacheless `as-built` control, whose trap lines equal round 8's. No firmware source, RTL, contract or generated file changes this round.

**What `run.py --self-test` does not cover.** It regrades a committed trace, `fixture.log`, which was recorded at 1x1 on the firmware of `e76a755a`, against its oracle. It also checks the harness's pure-Python rules. It builds no image, SoC or native model and runs no simulation. So it cannot see a point the planner refuses, a mailbox port left unconnected, a face acknowledgement off the contract's bound, or an image that never reaches its loop on this SoC. Each of those needs the real build (`run.py --point ...`), which needs picolibc's and compiler-rt's packages, the patched LiteX tree and Verilator together; no hosted job runs it. Since round 8 the self-test does check, without building, that the ledgered point is named at its point only, and that every labelled arm and control plant applies to the checkout's sources; since the merge, S2c's checks of the cache's fetch observers, the XIP arm's link script, and the recorded fetch L1 and arm on reuse.

Expected result and pass criteria:

- `$SDK` is a new directory: the installer installs the pinned archive into an absent prefix, or verifies one that carries its receipt, and replaces nothing.
- Every command exits 0. The last two link and plan the 8x8 two-interface image with its override: 57.5 RAMB36, `"ledgered_tiles": 57.5`. Without `--ledgered-point` both refuse it (exit 2), and the other three points plan within 56 and refuse the override.
- The AECP arms pass 101 tests at each interface count.
- The AECP campaign catches 137 of 137 plants (35, 34, 34 and 34 across the four shards). The firmware self-test's shard 2 runs the same 137 again, and shard 1 catches 528 of 528.
- Coverage is 100 % of lines and branches over 31 files, with no new exclusion: `aecp.c` 417/417 and 360/360, `aecp_commands.c` 450/450 and 374/374.
- `ctrl_boundary.py` passes both legs with 0 findings. `test_builder.py` reports one arm not run where no local Arty build report exists.
- `test_ctrl_memory.py` reports 0 failures under LiteX's own interpreter.
- `test_soc_options.py` passes: the 4 KiB direct-mapped instruction cache on the split CPU only, 6 killed controls.
- `check_py_idiom.py` reports `too many parameters: 7 <= 7`.
- `run.py --self-test` (the harness) reports 0 failures: 97 checks pass, and every one of its 76 mutants is caught.
- The two arm A `run.py --point` commands, on the split's cache (`soc.json`: `"fetch_l1": "split"`, geometry `[64, 1]`), each get past `image.log`, the SoC export (after the acknowledgement check), Verilator (no mailbox port unconnected) and `make`. The 8x8 `soc.json` plans 57.5 RAMB36 with `"ledgered": "8x8-two-interfaces"`, and the 1x1 one plans 37.0, naming none. Each then measures every `aecp` probe: 25 of 25 at 1x1 and 39 of 39 at 8x8, 0 refusals, 0 T_svc misses, rc 0; the worst probe is 3.442 ms at 1x1 and 4.331 ms at 8x8.
- The arm B commands (`answering-ports`, `aecp-fanout`, cacheless) measure every probe, rc 0. At 1x1, 4 of 14 instances miss T_svc (S2: 3); at 8x8, 22 of 22 miss (S2: 22), 4 of them over the 24 ms ceiling (S2: 3). The new rows are SET_CONFIGURATION's, whose cause is #801 ([Known limitations](#known-limitations--out-of-scope)).
- `slow-adp-rx` (cacheless) prints `CONTROL slow-adp-rx caught`: `control.discover.if0` 24.614 ms, rc 0. Both `as-built` commands print `CONTROL as-built caught`, rc 0: the boot is refused with `TRAP 166 0 5 00000020` (cacheless) and `TRAP 195 0 5 00000020` (cache), a load access fault.
- `behave` passes 406 scenarios.
- The sweep passes every suite, 64 of 64; `tsn_fuzz` declares its field campaigns skipped without tsn-gen.

## Known limitations / out of scope

- **The harness's face acknowledgement is a model** (the ruling on the STOP, option (c)). There is no datapath behind the face block yet, so the harness's SoC acknowledges each commit at the contract's bound, 64 bus cycles after `fw_send_o` rises. That is its one difference from `CtrlMailbox`, which holds the input idle. A CPU budget needs the slowest acknowledgement the contract allows. On the cacheless core the bound measures cycle for cycle the same as a one-cycle acknowledgement: the firmware's first F_STATUS read after a commit comes later than 64 bus cycles. That comparison has not been run on the split's cache, whose CPU reaches that read sooner; a sooner acknowledgement still makes no commit wait longer than measured. A probe beyond the contract (256 bus cycles) adds one F_STATUS read per commit, +170 CPU cycles, so the measurement does see the acknowledgement. Window answers stay idle, so each window read is measured to its timeout.
- **Against S2's recorded figures**, arm A's differences are the STOP's, unchanged, since its figures are the probe's:
  - each AECP command makes one more mailbox access an interface: the `applied` check reads `F_STATUS.BUSY` (`aecp.c:347`);
  - LOCK_ENTITY and its release add 12 accesses an interface (+0.21 ms at 1x1): the `F_AECP.LOCK_HELD` publication;
  - the first SET_NAME adds 21 at 1x1 and 42 on 8x8 interface 0: its publication on every interface;
  - the rest is phase. That includes S2's one 8x8 miss, `get_configuration.if0`, at 14.822 ms there and 7.675 ms here.

  Arm B's settings commands add 12 to 19 accesses, the settings publication.
- **Arm B, `slow-adp-rx` and `slow-adp-shutdown` were not run on the split's cache at this head**, and no full group set ran on it here: the merge round's measurement is arm A's `aecp` group at both points. Their figures above and in the README are the cacheless core's, and S2c's cached figures are the firmware of `e76a755a`.
- **Arm B's SET_CONFIGURATION misses T_svc at 1x1 and exceeds the 24 ms ceiling at 8x8; the cause is #801, outside this PR** (ruling 6463964028 item 2).
  - At 1x1 the row measures 11.660 ms (S2: 9.233 ms), over T_svc. At 8x8 interface 0 it measures 26.980 ms (S2: 19.788 ms), over the 24 ms ceiling.
  - The cause, #801: on a configuration change, `aecp_face.c`'s `publish(..., every)` writes every stream entry of the configuration on every interface, looking each one up through `aecp_find`, a linear search over the model's descriptors. That adds 131,573 CPU cycles at 1x1 and 439,826 at 8x8 interface 0.
  - Arm A's fan-out does not run SET_CONFIGURATION (its formal rows equal S2's verdicts), so no formal row changes.
- **The `as-built` control does not say which access met #791's defect**, only that an instruction or load access fault refused the boot (ruling 6463964028 item 1). At this head it is the start code's first `.data` copy load (`lw` at 0x24, reading 0x197b0); in S2's firmware it was a call to 0xb1ec (cause 1). The trap line in the driver log names the cause and the last committed PC (0x20 here, the instruction before the faulting load), not the faulting address.
- The 8x8 two-interface image plans 57.5 RAMB36, a tile and a half over the budget, owed to lane S14 (decision D3, hybrid XIP; rulings 6412739248 and 6425357821). The flip (S13) still requires 56 or fewer at every point, with S14 merged. The other three points plan within 56; the shipping point has 24 B of `rom` left before 37.5.
- **The undone value after a failed change** (accepted for this lane by ruling 6425357821 item 2, as R701-4's outcome (a)). A written commit stays in the face block until the datapath takes it, and `cdc_handshake` holds its value. Firmware cannot withdraw it. After a failed command, the datapath takes the undone value with the late acknowledgement, and the poll then publishes the values in force whole. So the datapath ends at the values in force, where the controllers were told, but holds the undone value from that late acknowledgement until it takes the republished block. Closing that window needs the datapath side, so it belongs to the placement switch (#665 F-INT PR 2), which wires that side. `MAILBOX_SPLIT.md` "The firmware's writer" states it by this name.
- A lock that expires while a change waits is released when the wait ends, at most 100 ms late. Until its release is acknowledged it holds, by its owner, for every reader. A datapath that never acknowledges keeps it held, and keeps every change refused.
- SET_SYSTEM_UNIQUE_ID under another controller's lock answers NOT_IMPLEMENTED, as before this lane (R701-5 S4). Whether Milan v1.2 5.4.4.2 requires ENTITY_LOCKED there is outside this lane.
- The image figures are planned by `ctrl_memory.plan`. This branch maps none of them out of context.
- The image measurements use a runtime built with `-fno-stack-protector`. The stack-protected runtime the host SDK builds is lane S3's to resolve.
- The face block's datapath side is unread until the placement switch connects it, with its clock crossing. The acknowledgement path is tested on the host model and, in the CPU budget harness, against a model of the slowest datapath; not on a datapath.
- The audio maps are not applied through the `EDIT` window. `GET_AS_PATH` stays the platform's port.
- `test_builder.py`'s gate 11 needs a local Arty build report and did not run here.
- No changelog entry: the build is default-off, as for the earlier mailbox lanes.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
