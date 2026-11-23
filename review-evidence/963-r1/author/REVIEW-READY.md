[A819] REVIEW READY
Commit: 4cca956932073b3f704f12f81c53f2934cfa215c (branch `pf-963-1`, on PR #960's reviewed flip head `dd163e41`; PR base `dev-soft-core`; the firmware is final at `25d3dd7a`, `50d3f10e` re-anchors one plant, `4cca9569` is the design doc)

Changed:
- **Cause, which notice.** The over-share passes take `aecp-largest-notice`'s REMOVE and ADD_AUDIO_MAPPINGS of 63 at 8x8/1if. Their notice is the 550 B unsolicited response (`0x802d`, `0x802c`) for STREAM_PORT_OUTPUT 0, sent to 15 controllers. 8x8's input maps have capacity 0, so the edit is the output map's.
- **Cause, which map walk.** The edit's check loop walks the command's 63 mappings (`aecp_maps.c`, `aecp_map_command`). At each it ran the output port's running check (`idle`, #943), a brief observation of the one stream: 63 `aecp_stream_read` calls a pass, 55,052 cycles inclusive in answering-ports and 56,005 in declaring-outputs (a committed-PC trace of the base's four passes), each after zeroing the observation a second time.
- **The cut** (`sw/firmware/ctrl/aecp/aecp_maps.c`).
  - The check observes each stream an edit maps once, at the first of its mappings to reach it, and holds it in a table local to the edit. The observation is zeroed once.
  - A stream found running or unanswered refuses the edit at that mapping, as before (Milan v1.2 5.4.2.27, 5.4.2.28: the condition is the Stream Output's).
  - `aecp_map_command` is the base's size and every loaded byte outside it is the base's in all 16 harness arm images.
  - THE SHARE, the stated costs, the rows' limits, the mailbox contract and the RTL are unchanged.
- **Tests** (`test_aecp.cpp`). `Core.MapEditsAreTheirDefinitionRowForRow`'s definition reads the port once a stream, with its legal mappings over two streams. New `Core.MapEditWorkObservesEachOutputStreamOnce`. Both fail on their own words on the base's firmware.
- **Plants.** Four new in `aecp_map_mutants.py`, each caught on its words. Two rows are now caught by the edit's map, and two re-anchored where this fix rewrote their text.
- **Docs:** `docs/design/SPLIT_CONTROL_MEMORY.md`, "The running check, once a stream".

Validation:
- **`aecp-largest-notice` at 8x8/1if, graded strictly** (a pass over THE SHARE fails the run). Head: rc 0 in answering-ports (0 of 106 over, the longest 149,307 CPU cycles) and rc 0 in declaring-outputs (0 of 106, 153,071). Base: rc 1 and rc 1, 2 of 108 over each.
- **The CPU service-budget harness, every group of every arm at 1x1/1if and 8x8/1if, base and head.** 481 groups a tree, every save window included; every run rc 0 under the formal options. The process checkpoint driver was calibrated in all 16 arms: an ordinary complete log byte-identical each time.
- **Strict differential, nothing masked.** 481 of 481 groups are the base's: every wire frame in order, every publication write, the TXC counts, the refusals, every probe's status and verdicts. The target is exact in all five point-arm combinations that run it.
- **Record classes, complete:** RESULT: PASS.
  - 1x1/1if: long 82,546 (base 91,641), paced 29,822 (29,993), other 23,726 (23,726).
  - 8x8/1if: long 90,258 (163,316), paced 56,327 (56,492), other 20,202 (20,202).
- **Measured load** (#872's model on this lane's complete measurements): 0.48911 at 1x1/1if and 0.60082 at 8x8/1if, the base's exactly (owner bounds 0.70, 0.75). The load gate, the flip check at both points and the shape table are byte-identical to the base's.
- **The firmware gate's four shards** (`test_ctrl_firmware.py --require-rv32 --self-test --shard k/4`): PASS. Plants caught 88 (shard 0, at `25d3dd7a`), 826, 389 (AECP's campaign) and 543; none escaped.
- **The firmware-unit steps:** rc 0 each, `firmware coverage: PASS (40 files)`.
- **The twin:** `twin: 0 finding(s)`, every plant refused. **The harness self-test:** 0 failures (no file under `tb/` changes).
- **Portable gates:** rc 0 each (idiom, hygiene, test evidence, naming, docs, hot list, memory planner, split boot at both points with its plants). **The docs workflow's gate steps:** 45 of 46 gate steps rc 0 in the workflow pass; the em-dash step, which reads the hosted event, rc 0 against the PR's merge base `59b09884` (0 findings over 181 added lines in 33 pages); the no-git docs gate also on a fresh checkout, rc 0.

Acceptance criteria:
- Every work pass of `aecp-largest-notice` at 8x8/1if within THE SHARE, at both arms: **met** (0 of 106 over in each).
- The graded rows unchanged: **met**. Every probe's verdict is the base's in all 481 groups; no stated cost or limit moved.
- The cause named: **met** (which notice and which map walk, above).
- A cut, not a restatement of THE SHARE: **met**. 62 of 63 observations an edit are removed, and the second zeroing of each.
- The 1x1/1if and 8x8/1if images within their ledgers: **met**, and the same size as the base's.
  - Every harness arm image has the base's ROM and SRAM bytes.
  - The target platform's 8x8/1if image is 139,208 B of ROM, the base's, at its 58.0-RAMB36 ledger.
  - Its 1x1/1if image is 45.0 tiles.

Open risks/questions:
- **The port's reads change:** once a stream an edit maps, not once a mapping. Only a window that answers a stream's first read in a record and not a later one could tell the two apart: the base then refused at the later mapping, while the head keeps the first answer.
- **The host crash of 2026-11-23 00:39.** It cut the head's campaign, three firmware shards and the docs gates. Each was re-run from clean state, and no partial result is counted.
- **Not run:** the full native Verilator sweep. Four CPU ranges were never free.
