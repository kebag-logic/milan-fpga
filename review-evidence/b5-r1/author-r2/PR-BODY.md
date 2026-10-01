[A472] Record #117 audio continuity end to end against the reference peer on dev ec0cc0c1

Refs #117 (acceptance box 4, the audio continuity row), under the bench lane B5 assignment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5925737609

Head `e29d12b1d5ee858eaf4684aaa8dc6647f6309857` on dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. Two commits: the round 1 record `bf9e5d82` and the round 2 restatement `e29d12b1`.

## Change

- `docs/findings/117_AUDIO_CONTINUITY.md` (new): the bench record of the audio continuity row.
- `docs/findings/README.md`: its index row.

No other documentation, code or configuration changes.

## Result (operator measurements, not review verdicts)

The first-light pattern enters the DUT's TDM input from the SoC board's McASP0. The DUT's AAF talker carries it to the reference peer's listener, and an external, hardware-clocked audio capture records the peer's digital output. Image: dev `ec0cc0c1`, as installed; identity gate PASS.

| Item | Verdict |
|---|---|
| Integrity: stream channels 0 and 1 bit-exact at 24 bits, in order, over 660 s | PASS: 31,569,594 of 31,569,600 frames; 0 torn, 0 invalid; 6 single zero frames |
| Continuity over 660 s | FAIL: 334 repeats at the DUT's documented INTERNAL beat; 520 one-frame drops, one every 1.266 s, attributed by inference to the peer's output rate; 117,104 more frames in skips of two frames or more, those of 60 or more stall-aligned capture-path loss, those of 2 to 59 not separated from a packet-sized drop downstream of the peer's receive counters |
| Restarts: 30 unbind and rebind cycles, rebind response to first valid sample | PASS, 30 of 30 under 1 s: median 0.0279 s, maximum 0.1358 s, no growth |
| Direction B, the peer's talker to the DUT's listener | NOT RUN: no known signal reaches the peer's talker channels without an instrument or wiring change |
| #117 audio continuity row | FAIL as measured |

Binding rule: the listener's stream format was set to the talker's before each run's first bind, and set back after each run; the talker's format was never set. The bench was restored and the restore proven; the one residual is the SoC board bridge legs' new process IDs.

## Round 2

Under the round 2 assignment (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5926598386), answering R424-1 and R425-1. Docs and evidence only, with no bench access.

- **Attributions (R424-1 F1, R425-1 F1).** The page, its summary rows and the index row now state each cause only as strongly as the evidence carries it. Skips of 60 frames or more are stall-aligned capture-path loss. Skips of 2 to 59 frames are not separated from a packet-sized drop downstream of the peer's receive counters. The one-frame drops are attributed to the peer's output rate by inference, with a drop at the capture's input named as the alternative.
- **Reproducible figures (R425-1 F2).** A new tool derives the window's read record (131,540 bytes) from the local read-time file and computes every attribution figure from published inputs.
  - 236 of 239 reproduces with the stall defined as a read interval over 15 ms, one or two reads before the skip.
  - The stall excess, 109,069 frames, reproduces. The recurrence is corrected to 3.00 s (2.99 to 3.02 s).
  - The count drift 115,614 does not reproduce. It is corrected to 117,653 frames from `summary.json`'s `window_time`.
  - The slip rate is stated as 16.46 ppm, one frame in 60,768.
  - The absolute host-clock rates (0.8 and 17.3 ppm) are dropped: they held only if every skip of two frames or more was a capture loss.
  - The whole-run integrity counts are now derived from the raw pair; the six window zero frames are named.
  - The Limits share is split: skips of two frames or more removed 0.37% of the frames, 0.35% in the stall-aligned skips.
- **What the read record adds.** A frame lost inside the capture path after sampling delays every later read, so the capture's delivery deficit steps by the frames lost.
  - The 284 smaller skips inside stall clusters are consistent with that, in aggregate.
  - The 237 smaller skips away from any stall, in 121 clusters, never come with a deficit step of their size: 95 clusters stay within 3 frames, 22 step by 1 ms, and 4 match neither.
  - Controls: beat repeats, one-frame skips and planted losses behave as expected, and the result holds across a parameter sweep.
  - So those skips are not attributed, and whether a lossless capture path would remove them is open.
- **Direction B (R425-1 F3).** The reason now states only what was observed. The peer's STREAM_PORT_OUTPUT 0 owns four clusters and its dynamic map draws only from them. Its AUDIO_UNIT declares no external or internal port and no routing element, so the clusters' source is not visible over AEM. The survey walk is marked defective for reuse: four descriptor type codes are wrong against IEEE 1722.1 Table 7.1 as `avdecc/aem_descriptors.py` encodes it, so no AUDIO_CLUSTER descriptor was read.
- **Controller tool revision (R424-1 F2).** The revision that ran the binds and format sets cannot be established from the packet's records. The start snapshot hashed `24208ef2` (8,642 bytes). The descriptor survey 70 s later shows that the controller copy had changed, with no hash recorded. The listed `47b7387a` is the end snapshot's re-staged copy.
- **Tables.** 14 of the page's 15 tables are byte-identical. The summary verdict table changes only the Evidence cells of the continuity row and the row verdict. Their Item and Verdict cells and every figure are unchanged.

## Open items

- The stall-aligned skips of 60 frames or more remove 0.35% of the frames, so a clean continuity window was not recorded. A capture path that loses no frames is an owner item.
- The 237 skips of 2 to 59 frames away from capture stalls are not attributed. Placing them, between the peer's receive counters and the capture's input, needs a decision.
- The one-frame drops are attributed by inference to the peer's INTERNAL media clock, running 16.46 ppm slower than the stream. Testing that needs the peer's media clock to follow the stream, a clock-source change on the peer outside this lane. It needs a decision.

## Validation

All rc 0 at the head, from the physical lane path: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9`, `check_doc_paths.py` in the pinned Markdown environment; `scripts/ci_scope.py --selftest`; `scripts/check_baremetal_only.py --check`; `scripts/check_feature_status.py --self-test`; `git diff --check` and `git diff --check e4b771f9 HEAD`; `gen_toc.py --verify-anchors`.

Evidence: lane packet `b5-a472` (tools, per-action evidence, summaries, raw-artifact index by size and SHA-256, redaction record, manifest) and round 2 packet `b5-a473`: the analysis tools, the derived read record, the attribution, records and table-identity receipts, the gate outputs and a manifest. Raw captures stay outside the packets and the repository.
