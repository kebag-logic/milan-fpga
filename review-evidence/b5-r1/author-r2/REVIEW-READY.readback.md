[A473] REVIEW READY

Round 2 for PR #628 (bench lane B5, #117 acceptance box 4, the audio continuity row), under the [A10] round 2 assignment (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5926598386). It answers R424-1 F1 and F2 and R425-1 F1 to F3. Docs and evidence only, with no bench access. Refs #117.

Commit: `e29d12b1d5ee858eaf4684aaa8dc6647f6309857`
Branch: `b5-bench-1001`, parent `bf9e5d82a401d167a8ffc786677a19dc7aac0cf2`, base dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. One new commit, local only: not pushed, PR not edited.
Changed: `docs/findings/117_AUDIO_CONTINUITY.md` (Continuity, Direction B, Limits, Artifact hashes, and the two cause cells of the summary verdict table) and its row in `docs/findings/README.md`. No other file.

**1. Attributions.** Each cause is now stated only as strongly as the evidence carries it, in the page body, the summary rows and the index row.
- Skips of 60 frames or more: stall-aligned capture-path loss.
- Skips of 2 to 59 frames: not separated from a packet-sized drop downstream of the peer's receive counters.
- The 1.266 s one-frame drops: attributed to the peer's output rate by inference, from the period and its INTERNAL clock source. A drop at the capture's input is named as the alternative.

**2. Reproducible figures.** A new tool (`b5_attrib.py`, in round 2 packet `b5-a473`) derives the window's read record from the local read-time file: 131,540 bytes, SHA-256 `2183d57f0646cf94405b95aea5547b83f5ff0b9190ac0bd1bdcc87760c919961`. From that record and round 1's published summary and event list, it computes every attribution figure.
- **Stall:** a read interval over 15 ms, the grader's definition. 220 stalls, one every 3.00 s (2.99 to 3.02 s); the page's "2.99 s" is corrected.
- **Alignment:** 236 of the 239 skips of 60 frames or more fall one or two reads after a stall. Each stall is followed by exactly one skip of 240 frames or more. The stall excess is 109,069 frames against 109,928.
- **Count drift:** 115,614 does not reproduce. It is corrected to 117,653 frames from `summary.json`'s `window_time`; the boundary reads give 117,652.1.
- **Rates:** the slip rate is 16.46 ppm, one frame in 60,768. The absolute host-clock rates (0.8 and 17.3 ppm) are dropped, because they held only if every multi-frame skip was a capture loss.
- **Whole run:** the integrity counts now derive from the raw pair. The zero frames are before the first valid frame, in the cycle holds, after the last, and the window's six.

**Beyond the wording.** A frame lost inside the capture path after sampling delays every later read, so the capture's delivery deficit steps by the frames lost.
- In the 222 stall clusters, the deficit steps by 116,138 frames against 115,314 skipped, including 284 of the smaller skips. That is consistent with capture-path loss in aggregate.
- The other 237 smaller skips, 1,790 frames in 121 clusters away from any stall, never come with a step of their size. 95 of those clusters stay within 3 frames, 22 step by 1 ms, and 4 match neither.
- Controls hold. Beat repeats and one-frame skips stay within 3.2 frames, and planted 6, 12 and 24-frame losses are recovered within 5. Over 51,828 clear positions there are 7 steps of 1 ms with no frame missing.
- The result holds over 7 parameter sets. These skips are not attributed.

**3. Direction B.** The reason states only what was observed.
- The peer's STREAM_PORT_OUTPUT 0 owns four clusters, and its dynamic map draws only from them.
- Its AUDIO_UNIT declares no external or internal port and no routing element, so the clusters' source is not visible over AEM.
- A known signal would therefore need an instrument or wiring change.
- The survey walk is marked defective for reuse. Its cluster, map and external-port type codes are wrong against IEEE 1722.1 Table 7.1 as `avdecc/aem_descriptors.py` encodes it, so no AUDIO_CLUSTER descriptor was read.

**4. Controller tool revision.** It cannot be established from the packet's records, and the page says so.
- The start snapshot hashed `24208ef2…` (8,642 bytes), and its descriptor survey had no audio-unit walk.
- The survey 70 s later carries that walk, so the controller copy changed with no hash recorded.
- The run tool records no hash, and the listed `47b7387a…` is the end snapshot's re-staged copy.
- The binding rule record rests on the logged exchanges.

**Tables.** 14 of the page's 15 tables are byte-identical: SHA-256 per table, plus a literal `diff` of all 119 table lines, `bf9e5d82` against `e29d12b1`. The summary verdict table changes only the Evidence cells of the continuity row and the row verdict, as item 1 and R425-1 F1 require. Their Item and Verdict cells and every figure are unchanged.

**Public text.** A label-only scan covered the packet, the added diff lines and the commit message. It used the private redaction map, MAC and home-directory patterns, and a private list of channel numbers, clock-topology words and tool names. It found 0 hits.

Validation, all rc 0 at `e29d12b1` from the physical lane path, none piped:
- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9` and `check_doc_paths.py` (pinned Markdown environment);
- `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check` and `scripts/check_feature_status.py --self-test`;
- `git diff --check` and `git diff --check e4b771f9 HEAD`;
- `gen_toc.py --verify-anchors`.

Acceptance criteria (the assignment's four items): met, with the evidence above. Packet `b5-a473` holds the tools, the derived read record, the receipts, the gate outputs, `HANDOFF.md`, `PR-BODY.md` and `MANIFEST.sha256`; the raw files stay local.

Open risks/questions:
- The 237 skips of 2 to 59 frames away from stalls are not attributed. Placing them, between the peer's receive counters and the capture's input, needs a decision. Whether a capture path that loses no frames removes them is open.
- The one-frame drops' attribution needs the peer's media clock to follow the stream to test it. That is a decision item, as before.
- The floor test resolves about 4 frames, and the 1 ms delivery steps it finds are not explained.

