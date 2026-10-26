[A680e] STOP
Head: `4e3aab32ba4da009c21af2494b29c7a9af85e13f`, three commits on round 4's `d33a5adc` (nothing pushed).

**Why I stopped.** The condition is the one stated in TAKEN (6421674945), taken from the ruling of 6412739248 item 1. The 8x8 two-interface image now plans **57.5 RAMB36**, where that ruling allows it 57. `ctrl_memory.plan` refuses it even with the `8x8-two-interfaces` override (exit 2).
- `rom` is 119,736 B in 120,832, and `sram` is 112,992 B in 114,688.
- The other three points stay within 56: 1x1 one interface 37.0, two interfaces 40.5, 8x8 one interface 50.5.
- Round 4 left 104 B of `rom` before that point's next bank. The round-5 model adds 1,056 B of `rom` and 224 B of `sram` at every point:
  - the change record and its ten call sites;
  - the undo and redo swap;
  - the held SUCCESS response and its re-answer as a refusal;
  - the wait's resolution;
  - the expiry's kept notification;
  - the lock-check refusal.
- RV32I has no compressed instructions. I measured two compactions on throwaway edits:
  - constant port tables in three files: -64 B;
  - IN_PROGRESS carrying the held SUCCESS body instead of a re-answer: -64 B.

  That gives 119,608 B, still 57.5. Nothing I have found approaches the 952 B the point needs.

**Decision needed.** One of:
- **(a)** Let that point plan 57.5, owed to S14 with the first tile. That means the override's figure in `sw/litex/ctrl_memory.py`, its test, and `docs/design/SPLIT_CONTROL_MEMORY.md` section 5. Section 5 is unchanged at this head and still states round 4's figures.
- **(b)** Recover at least 952 B of `rom` at that point elsewhere first. Name where, because no candidate I measured comes close.
- **(c)** Narrow the model the ruling asked for. Name what to drop.

I recommend (a). Decision D3's hybrid XIP (S14) exists to take exactly this pressure off `rom`. The flip (S13) already waits for S14 at every point. (b) and (c) would trade code that the ruling's model needs for half a tile that S14 removes anyway.

Also for decision: TAKEN's risk 1. A written commit stays in the face block until the datapath takes it, and `cdc_handshake` holds its value. After a command that failed, the datapath therefore holds the undone value from its late acknowledgement until the republished block is taken. It then ends at the values in force: R701-4's outcome (a), "what the datapath finally takes". Closing that window needs the datapath side, which the placement switch wires.

**What is done at this head** (ruling 6421238472, items 1 to 6):
1. LOCK_ENTITY, SET_CONFIGURATION, SET_STREAM_FORMAT, SET_STREAM_INFO, SET_CLOCK_SOURCE and SET_CONTROL (`AECP_WAITS`) answer IN_PROGRESS at once when their face commit is not acknowledged, then exactly one final response. That response follows the IN_PROGRESS within IEEE 1722.1-2021 9.3.2.6's 120 ms cadence, so no second IN_PROGRESS is owed, and follows the command within its 240 ms. `FR_NFR.md:363` now names this one exception to the no-IN_PROGRESS policy. No getter waits, so GET_DYNAMIC_INFO never answers IN_PROGRESS (IEEE 1722.1-2021 7.4.76).
2. Not acknowledged within `AECP_WAIT_MS` (100 ms): the change stays undone in the core, from the bytes it recorded. The face is given the values in force, and the command answers ENTITY_MISBEHAVING with those values, notifying no one.
3. While a change waits, it is undone: every getter, READ_DESCRIPTOR and notification reports the values in force, and the face writes nothing. A notification that falls due meanwhile is sent after the wait, with the value then in force. A change's own notification follows its SUCCESS.
4. The automatic unlock still releases at 60 s (Milan v1.2 5.4.2.2). If a change is waiting then, it releases when that wait ends, at most 100 ms late. Its LOCK_ENTITY notification is kept until LOCK_HELD's publication is acknowledged, however late, and is sent once (R702-4 F2). No change is taken before it leaves.
5. Tests:
   - `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: pending then success, with a getter, READ_DESCRIPTOR and a second command; each of the six commands timing out with the whole core state unchanged.
   - `Core.ALockExpiryIsNotifiedOnceThePlatformAppliedTheRelease`: through a full ring.
   - `Face.ALateCommitIsOwedAndPublishedAgainWhole`: timeout with rollback on the model; the datapath ends at the value in force.
   - `Face.APendingChangeIsAnsweredOnceTheDatapathTakesIt`: a notification held until acknowledged.
   - `Face.APartialAcknowledgement...`, `Face.AMissingAcknowledgementFailsTheChangeAndRefusesEveryOther` (the automatic unlock), `Face.ALockThatExpiresWhileAChangeWaitsIsNotifiedOnceTaken`.
   - 24 new plants; the campaign catches 128 of 128.
   - R701-4 F2: every refusal now goes through the lock check, so it carries exactly what that command's lock refusal reports, including LOCK_ENTITY's current `locked_id`. `Core.AChangeThePlatformHasNotAppliedPromisesNothing` compares the two byte for byte.
6. Docs: `MAILBOX_SPLIT.md` "The firmware's writer", `aecp_face.h`, `ARCHITECTURE_HW_SW_SPLIT.md:55`, `FR_NFR.md:363`, and the aecp and ctrl READMEs.

**The reviewers' probes, rerun unmodified** (hashes match the manifests). Each probe's own assertion holds. Item 1 makes a waiting command's first frame IN_PROGRESS, so three probe fixtures fail only their first-frame status check: R701-4's and R702-4's expect ENTITY_MISBEHAVING, R702-3's SUCCESS.
- R701-3 `response_probe.py`: PASS at one and two interfaces.
- R701-4 `late_ack_notify_probe.py`: `PROBE held: core_identify=0 get_control_identify=0 datapath_identify=255`, then `PROBE after: datapath_identify=255 owed0=0 unsolicited_set_control=1`.
- R702-3 `probe_ack.py`: `response_status=10 core_identify=0 mailbox_identify=255`.
- R702-4 `delta_probes.py`:
  - getter: `status=0 returned=0 last_acknowledged=0`;
  - no stream notification while held;
  - `ReviewAutomaticUnlockMustBeNotifiedAfterRecovery` passes (`applied=1 notifications=1 registered=1`);
  - 22 of 24 tests pass at each width.

**Gates at `4e3aab32`**, all rc 0:
- the firmware self-test, four shards: 528 of 528, and AECP 128 of 128;
- `aecp_mutants.py`: 128 of 128;
- `aecp_arms.py --app`: 97 of 97 at one and at two interfaces;
- `fw_coverage.py --check`: 31 files at 100 % with no new exclusion (`aecp.c` 414/414 lines, 350/350 branches);
- `ctrl_boundary.py`, both legs;
- `test_builder.py`: one gate NOT RUN, needing a local Arty build report;
- `behave`: 406 scenarios;
- `test_ctrl_memory.py`;
- `make -C tb/verilator/mbx`: 523, 568, 32 and 530, 575, 488, with 7 of 7 plants;
- `gen_mailbox.py --check --crosscheck --selftest`;
- the census: 217 ports, 138 arms, 43 rules, 934 s;
- `lint_rtl.py`;
- the docs gates, 69 of 69;
- the four-shard Verilator sweep: 64 of 64 suites, 2,191,124 checks, 0 failures (`tsn_fuzz` declares its field campaigns skipped).

Round 5 changes nothing under `hdl/`, `sw/litex/`, `syn/` or `tb/`, and no generated file, so round 4's out-of-context, `xvlog`, Yosys, `make mutants` and all-fabric export evidence stands. Receipts and the handoff are with the manager.
