[A472] Record #117 audio continuity end to end against the reference peer on dev ec0cc0c1

Refs #117 (acceptance box 4, the audio continuity row), under the bench lane B5 assignment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5925737609

Head `cf38633ad9a5bdb05517bedba73ce50965af967b` on dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. Three commits: the round 1 record `bf9e5d82`, the round 2 restatement `e29d12b1` and the round 3 restatement `cf38633a`.

## Change

- `docs/findings/117_AUDIO_CONTINUITY.md` (new): the bench record of the audio continuity row.
- `docs/findings/README.md`: its index row.

No other documentation, code or configuration changes.

## Result (operator measurements, not review verdicts)

The first-light pattern enters the DUT's TDM input from the SoC board's McASP0. The DUT's AAF talker carries it to the reference peer's listener, and an external, hardware-clocked audio capture records the peer's digital output. Image: dev `ec0cc0c1`, as installed; identity gate PASS.

| Item | Verdict |
|---|---|
| Integrity: stream channels 0 and 1 bit-exact at 24 bits, in order, over 660 s | PASS: 31,569,594 of 31,569,600 frames; 0 torn, 0 invalid; 6 single zero frames |
| Continuity over 660 s | FAIL: 334 repeats at the DUT's documented INTERNAL beat; 520 one-frame drops, one every 1.266 s, attributed by inference to the peer's output rate; 117,104 more frames in skips of two frames or more: 236 of the 239 of 60 or more stall-aligned capture-path loss, the other three, of 72, 78 and 108 frames, not stall-aligned; those of 2 to 59 not separated from a packet-sized drop downstream of the peer's receive counters |
| Restarts: 30 unbind and rebind cycles, rebind response to first valid sample | PASS, 30 of 30 under 1 s: median 0.0279 s, maximum 0.1358 s, no growth |
| Direction B, the peer's talker to the DUT's listener | NOT RUN: it was not established whether a known signal can reach the peer's talker channels without a wiring change; the descriptors naming each cluster's signal source were not read, because the survey walk is defective |
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
- **Direction B (R425-1 F3).** The reason now states only what was observed. The peer's STREAM_PORT_OUTPUT 0 owns four clusters and its dynamic map draws only from them. Its AUDIO_UNIT declares no external or internal port and no routing element, so the clusters' source is not visible over AEM (round 3 replaces this reason). The survey walk is marked defective for reuse: four descriptor type codes are wrong against IEEE 1722.1 Table 7.1 as `avdecc/aem_descriptors.py` encodes it, so no AUDIO_CLUSTER descriptor was read.
- **Controller tool revision (R424-1 F2).** The revision that ran the binds and format sets cannot be established from the packet's records. The start snapshot hashed `24208ef2` (8,642 bytes). The descriptor survey 70 s later shows that the controller copy had changed, with no hash recorded. The listed `47b7387a` is the end snapshot's re-staged copy.
- **Tables.** 14 of the page's 15 tables are byte-identical. The summary verdict table changes only the Evidence cells of the continuity row and the row verdict. Their Item and Verdict cells and every figure are unchanged.

## Round 3

Under the round 3 assignment (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5927406852), answering R424-2 and R425-2. Docs only, with no bench access. One commit, `cf38633a`, on `docs/findings/117_AUDIO_CONTINUITY.md` and its index row.

- **F1 (R424-2 F1, R425-2 F1), the published read record.** The manager republished it as `a-long-reads.u16.gz`. The page now gives the reproduction steps: `gunzip -kf a-long-reads.u16.gz`, check the SHA-256, then run `b5_attrib.py figures`.
  - The `-f` is needed. The copy with three bytes masked still sits beside the `.gz`, and `gunzip -k` alone refuses to overwrite it (rc 2).
  - From the public archive alone, `gunzip -kf` restores SHA-256 `2183d57f…`, and the published `b5_attrib.py` reproduces the published `attribution.txt` byte for byte.
- **Direction B reason (R425-2 F2, item 1).** The page no longer says the clusters' source is not visible over AEM. It says what was observed: four clusters on STREAM_PORT_OUTPUT 0, a dynamic map that draws only from them, and no external port, internal port or routing element.
  - Each AUDIO_CLUSTER descriptor names its cluster's signal source (`signal_type`, `signal_index`, `signal_output`, IEEE 1722.1 7.2.16). Those descriptors were not read, because the survey walk is defective.
  - So whether a known signal can reach the peer's talker channels without a wiring change is open. NOT RUN stays. The summary row's Evidence cell says the same.
- **What the walk sent (R424-2 S2, item 2).** It sent 20 reads of type 0x0010 at indices 0 to 19, each answered NO_SUCH_DESCRIPTOR. It sent no map read, because both stream ports declare no static map, and no external port read. The dynamic maps came from GET_AUDIO_MAP.
- **Which skips "stall-aligned" covers (R424-2 S3, R425-2 S2, item 3).** 236 of the 239 skips of 60 frames or more are stall-aligned, 109,670 frames. The stall excess, 109,069 frames, is now compared with those 109,670.
  - The other three are named: 72 frames at 34.0 s into the window, and 78 and 108 frames on consecutive reads at 634.0 s. They are not stall-aligned, and the stall attribution does not cover them.
  - The summary row, the index row and the Limits share say "236 of the 239".
- **Where the 1 ms steps fall (R424-2 S1, R425-2 S1, item 4).** Stated as an observation, without attribution: 22 of the 121 off-stall clusters step by 1 ms, against about 0.26 by chance. The chance figure is 7 one-millisecond steps over 51,828 clear read positions, about 3,240 windows of the floor test's 16 reads.
- **Suggestions (item 5).**
  - R425-2 S3, taken: the page now says the planted-loss control is linear by construction, so it checks where the floor windows sit, not the test's power. The round 3 receipt shows a plant reads back as the floor's own step plus the plant, with a largest difference of 0.
  - R424-2 S4, the suggestions retained from round 1:
    - R424-1 S2, the free-run acceptance rule, taken. The page cites the register map's slip counters, which record the 1.958 s beat as "the standing free-run rule, slips accepted".
    - R424-1 S3, the order criterion, taken. "In order" means 0 backward steps, as the grader defines them, and the window has 0.
    - R424-1 S3, the ordinals around the six skip, zero, skip events, taken. They are read from the local graded pair and published as a derived receipt. Each zero frame sits between consecutive ordinals and replaces no pattern frame. So each event drops two frames and inserts one: one frame fewer, like a single skip.
    - R424-1 S1, the forward pointers from the #117 ledger and the #75 index row, retained. Those rows are on other pages. The B5 assignment fixed the output as this page and its index row, and round 3 did not extend it, so adding them stays the manager's call.
- **Tables.** 14 of the page's 15 tables are byte-identical to round 2, and every table after the summary verdict table is byte-identical to round 1. The summary verdict table changes only two Evidence cells: the continuity row (item 3) and the Direction B row (item 1). Their Item and Verdict cells are unchanged, and so is every figure of the old cells.

## Open items

- The 236 stall-aligned skips of 60 frames or more remove 0.35% of the frames, so a clean continuity window was not recorded. A capture path that loses no frames is an owner item.
- Direction B: whether a known signal can reach the peer's talker channels without a wiring change is open. A read-only read of the peer's AUDIO_CLUSTER descriptors, type 0x0014, would show the source each cluster names. It needs a decision.
- The 237 skips of 2 to 59 frames away from capture stalls are not attributed. Placing them, between the peer's receive counters and the capture's input, needs a decision. The 1 ms steps that concentrate there are not explained.
- The one-frame drops are attributed by inference to the peer's INTERNAL media clock, running 16.46 ppm slower than the stream. Testing that needs the peer's media clock to follow the stream, a clock-source change on the peer outside this lane. It needs a decision.

## Validation

All rc 0 at the head `cf38633a`, from the physical lane path: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9` (0 findings over 505 added lines), `check_doc_paths.py` in the pinned Markdown environment; `scripts/ci_scope.py --selftest`; `scripts/check_baremetal_only.py --check`; `scripts/check_feature_status.py --self-test`; `git diff --check`, `git diff --check e4b771f9 HEAD` and `git diff --check e29d12b1 HEAD`; `gen_toc.py --verify-anchors`.

Evidence: lane packet `b5-a472` (tools, per-action evidence, summaries, raw-artifact index by size and SHA-256, redaction record, manifest) and round 2 packet `b5-a473`: the analysis tools, the derived read record, the attribution, records and table-identity receipts, the gate outputs and a manifest. Round 3 packet `b5-a474`: `b5_round3.py`; its figures, zero-frame ordinals and F1 reproduction receipts; the table-identity and private-name scan receipts; the gate outputs and a manifest. Raw captures stay outside the packets and the repository.
