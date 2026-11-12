[A776] STOP
Head: `5e6fef3ee74dcf6766ac3923349ae83524bc0e7b` (branch `897-split-as-path`, on #810's round 29 tip `7f50ee6a`)

**The question.** What does a GET_AS_PATH on a valid AVB_INTERFACE answer when the datapath's GSI window does not answer within its bound (a datapath held in reset or wedged)? Acceptance 3 forbids ENTITY_MISBEHAVING "for a read of a valid AVB_INTERFACE". IEEE 1722.1-2021 7.4.41 names no status for this: 7.4.41.2 defines `count` and `path_sequence` only, and 7.4.41.3 names NOT_AUTHENTICATED only. Table 7-141 has one status whose meaning fits, ENTITY_MISBEHAVING (10): "generated an internal error while trying to process the command". So the clause gives no answer, and I have not chosen one.

The same decision covers the core's other ENTITY_MISBEHAVING for a descriptor that exists: an AVB_INTERFACE whose index is past the build's interfaces (`aecp_commands.c:467-468`). No shipped configuration reaches it, because each image holds one AVB_INTERFACE, index 0, and an index past it answers NO_SUCH_DESCRIPTOR.

**Today's answer and what it rests on.** The core answers such a port failure ENTITY_MISBEHAVING (`sw/firmware/ctrl/aecp/aecp_commands.c:476-477`, pinned by `Core.ObservationRefusals`). It answers GET_AVB_INFO's, GET_STREAM_INFO's and GET_COUNTERS' the same way. The all-fabric processor answers the same: its gather watchdog voids a wedged GSI face to ENTITY_MISBEHAVING (protocol-processor `KL_aecp_engine.sv`, `gather_watchdog`). This head changes no status.

**The options I see, for a decision:**
- (a) Keep ENTITY_MISBEHAVING for a datapath that does not answer, by Table 7-141's meaning and the all-fabric image's behaviour, and read acceptance 3 as "with an answering datapath". No code change. **This is my recommendation**: it matches the all-fabric image, which acceptance 1 names as the reference.
- (b) Answer IN_PROGRESS and read the window again inside 9.3.2.6's 120 ms cadence. That still needs a final status for a datapath that never answers, so it ends in (a) or (c). It would also add a retried read to solicited responses, which today never wait on an observation port; only notices retry (`aecp.h`, `AECP_RETRY_MAX_MS`).
- (c) Another status (NO_RESOURCES, or SUCCESS with count 0). No clause supports either. A count of 0 states an empty path the entity has not read (7.4.41.2).

**Done at this head, independent of the answer:**
- The face's `path()` reads GSI kind 2: the count at selector 0, then each ClockIdentity at selector 8 by its ordinal, through the AVB interface's own window, at most `AECP_PATH_ITEMS`. A count past the bound, or a word with no answer, fails that port, as GET_AVB_INFO's does.
- The platform's stub is removed. With an answering datapath, every valid AVB_INTERFACE answers SUCCESS with the datapath's `count` and `path_sequence`, exactly as 7.4.41.2 lays them out (acceptance 1).
- AS_PATH_CHANGED already led to the unsolicited GET_AS_PATH response (Table 5.22). It now carries the datapath's sequence (acceptance 2).
- Five new tests, each with planted defects killed by name: nine AECP plants and one platform plant (acceptance 4). `aecp_face.c` is at 100 % of lines and branches.
- The split datapath serves kind 2 in the split build (`milan_datapath.sv`, `g_sp_ctrl`). No mailbox contract change and no RTL change.
- ROM: each image gains 312 to 328 B of `rom` and takes no extra tile. The fixture's 8x8/2if image stays at 58.0 (cap 58.5) and the platform's at 59.5 (cap 60.5). Every other point is within 56.
- Load: 1x1/1if holds at 0.486 against 0.70.
- Gates: I ran the clean-clone pass once, at this head. It covered every workflow job a pull request to `dev-soft-core` triggers, each on a fresh clean clone, and the lane's gates; the full sweep was left out because no RTL changed.
  - Workflows: 139 steps ran, 226 were not run with a stated reason, and 2 failed (the idiom ratchet in docs-gates-0 and the firmware boundary, below): the same counts and the same two as #810's own pass at `7f50ee6a`.
  - Passing: the firmware self-test in its four shards; the AECP campaign (236 of 236 caught) and the control campaign (697 of 697); `fw_coverage.py --check`; `test_builder.py --require-rv32`; every other docs gate; `behave` (508 scenarios); the split boot simulation at both shapes; the twin.
  - CPU budget harness: fresh builds at both points in arms A, B and the every-port arm. Their sampled groups have 0 refusals and 0 budget misses, and every cost is within its stated table. The images are byte-identical at the final head.
  - Red, as at the base: the C/C++ idiom ratchet (`test_aecp.cpp:1428`), the hooks self-test's ACMP plant anchor, and the firmware boundary's unclassified `flip_grade.py`. #810's round 29 fixes all three after `7f50ee6a`; that fix is not on this branch. The flip check also exits 1, as at the base; it is not a merge gate.

If the ruling is (a), this head needs no code change, and its gate pass stands. If it is another answer, the change is the core's status for the path port's failure, plus `Core.ObservationRefusals` and one plant.
