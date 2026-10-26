[A680g] REVIEW READY
Commit: `424b1489ccd8062180f90158556d343589b9e1e5` (four commits on round 5's `6d2b77bb`, nothing pushed)

Changed (assignment 6426858104, answering R701-5 and R702-5):
1. **R702-5 F1, the first option.** An expired lock still releases at 60 s, and LOCK_HELD 0 is still committed then. Until that commit is acknowledged, the lock holds, by its owner, for every response and read. That covers ENTITY_AVAILABLE, LOCK_ENTITY's `locked_id`, `aecp_locked` (the ACMP owner's reader) and every refusal. Another controller is refused ENTITY_LOCKED, naming the owner; the owner is refused ENTITY_MISBEHAVING. The owner is dropped when the notification leaves. `aecp_other_lock` (`aecp_commands.c:16-21`) is the one predicate the lock check, the refusal status (`aecp.c:372`) and the MVU path use. Test: `Core.AnExpiredLockHoldsByItsOwnerUntilThePlatformAppliedItsRelease`, with five plants.
2. **R701-5 F1, option (a).** SET_SYSTEM_UNIQUE_ID refused only because a change waits or the face is held answers ENTITY_MISBEHAVING with the `system_unique_id` in force (`aecp.c:271-291`). Another controller's lock keeps NOT_IMPLEMENTED. Test: `Core.ASystemIdChangeWhileOneWaitsIsRefusedAsEveryChangeIs` (pending wait and failed wait); plant `system-id-refusal-not-implemented` restores status 1.
3. **R702-5 F2.** `Core.AWaitingChangeIsAnsweredOnTheInterfaceItCameIn`: asked on interface 1 while interface 0's command is answered. IN_PROGRESS, SUCCESS and the failure each leave on interface 1. Plant: the restore removed.
4. **R702-5 F3.** `Face.AWaitingChangeIsAnsweredWithinTheInProgressCadence` measures on the model's millisecond clock, never reading `AECP_WAIT_MS`. The final response must be within 120 ms of its IN_PROGRESS and 240 ms of its command, with the 10 ms service bound added. The plants at 130 ms and at 115 ms are both caught; 115 is inside 120 alone and caught only with the service bound.
5. **Residue.** W1 = RES1 as written. W2 and RES2 give different exact text for the same two lines. `aecp_face.h` takes W2's, which contains RES2's. `ARCHITECTURE_HW_SW_SPLIT.md:110-111` carries both sentences, with RES2's link pointed at the in-tree `MAILBOX_SPLIT.md` rather than a review-evidence copy. W3/RES3 are merged as "... with its interface, length and requester, the four recorded values, the noted change, the wait's deadline and its three flags". The stray blank line is removed. No reviewer ID remains in a source comment.
6. **Memory.** +64 B `rom`, +0 `sram` at every point. 1x1 one interface 37.0, two interfaces 40.5, 8x8 one interface 50.5, 8x8 two interfaces 57.5 (ledgered), each unchanged. 1,032 B are left before 58.0 at the ledgered point. No compaction was needed. `SPLIT_CONTROL_MEMORY.md` section 5 is at these figures.

Also: 137 plants (128 + 9; three re-pointed to changed lines), and the docs (`MAILBOX_SPLIT.md` "The firmware's writer" and verification row, `ARCHITECTURE_HW_SW_SPLIT.md` section 1, the aecp and ctrl READMEs, `aecp.h`). Two later commits answer my own gates. `c66927c0` puts one name per declaration in the new tests, because the C++ idiom ratchet refused four at `168ae33d`. `424b1489` fixes a new comment that cited ENTITY_AVAILABLE as 7.4.1; it is 7.4.3.

Validation at `424b1489`, all rc 0 unless stated:
- Firmware self-test, four shards: rc 0 each. Shard 1 catches 528 of 528, and shard 2 runs the AECP campaign at 137 of 137.
- `aecp_mutants.py`, four shards: 137 of 137.
- `aecp_arms.py --app`: 101 of 101 at one and at two interfaces, and again with AddressSanitizer.
- `fw_coverage.py --check`: 100 % over 31 files, with `aecp.c` at 417/417 and 360/360.
- Linked images at four points: as above, with the override refused elsewhere and without it.
- `test_ctrl_memory.py`: 0 failures.
- Docs gates: 69 of 69, including `check_baremetal_only.py` and `check_cpp_idiom.py`.
- `cd tests && behave`: 406 scenarios.
- `ctrl_boundary.py --require-rv32 --selftest`: PASS on both legs (`--without verilator` and `--only verilator`), 0 findings.
- `test_builder.py --require-rv32`: all gates pass except gate 11, not run, which needs a local Arty build report.
- Verilator sweep, four shards: 64 of 64 suites, 2,191,124 checks, 0 failures. The only declared skips are `tsn_fuzz`'s field campaigns, because tsn-gen is not installed.

Probes, every reviewer probe of rounds 3 to 5, unchanged, each sha256 equal to its manifest:
- R702-5 `probe_release_reads.cpp` passes at one and two interfaces, in the core and app arms.
- R702-5 `probe_held_interface.cpp` passes at two interfaces. At one it skips itself by design, and the tally counts the skip as a failure.
- R702-5's four mutants are all caught.
- R701-5 `probe_wait_refusals.cpp` passes at both widths, with 10, 10 and 10.
- R701-3 `response_probe.py` passes.
- R701-4, R702-3 and R702-4 fail only their first-frame status fixtures (IN_PROGRESS by ruling 6421238472), as in round 5. Each one's own assertion holds.
- R701-5 `count_face_defects.py` prints 57 where the README says 59. It counts by test name, and two of the nine new plants name tests it does not match.

Acceptance criteria: as in round 5. The ledgered point is within its ruled 57.5, and every other point is within 56. This PR relates to #665 and does not close it.

Open risks/questions:
- The undone value after a failed change stays as accepted by ruling 6425357821, owed to the placement switch.
- SET_SYSTEM_UNIQUE_ID under another controller's lock keeps NOT_IMPLEMENTED (R701-5 S4, outside this lane).
- The shipping point has 24 B of `rom` left before 37.5.
