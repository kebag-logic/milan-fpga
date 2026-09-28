[R392] NEGATIVE - exact head 6339479d69830614d4267bd3170113737afbf8f4

Round R392-1, internal independent review of PR #616 (Relates to #451), tree
`bd639facbd225ea39aa77f89149f8e9d94b18b56`, source base
`6d5ebd7357c1e468e446f18a61527c5be6118a04`. The net change is one added
documentation page, `docs/findings/451_TDM8_FIRST_LIGHT.md`, over four commits
(`fba793c0`, `361d1f47`, `4f06bfc7`, `6339479d`).

All five lenses were applied. The first-light result reproduces from the
hash-verified raw captures: slot and tag tables, valid-word counts, torn-frame
counts, the pair-offset histogram, beat clusters and AVTP sequence gaps. The
DIN root cause (a dynamic STREAM_PORT_OUTPUT 0 map left empty) is correct
against the RTL, the generated shape, the shape YAML and the archived
GET_AUDIO_MAP replies. The page does not claim #386 acceptance 4, the #117
listener-audio sequence or a USB-audio-device capture. Every documentation gate
passes.

The verdict is NEGATIVE because of two MINOR findings:

- **F1.** The page states twice that the routed DIN line reads idle-high
  whenever the SoC is not playing, and concludes that a zero word could not
  have come from the pin. The page's own routed capture contradicts this: 777
  frames at the playback stop carry zero words.
- **F2.** A newly found DUT capture-path defect is described as "recorded for
  triage as a separate issue", but no such issue exists.

## Method

- **Reading order.** The contract (AGENTS.md, CONTRIBUTING.md) and the
  documentation index came first. Then the #451 body and all ten issue comments:
  the recipe, the 2026-09-18 amendment, the 2026-09-27 assignment, the STOP,
  both owner notes, TAKEN, the second STOP and REVIEW READY. Then the PR body,
  the diff and history, and the public evidence tree
  `review-evidence/451-r1` at `851f835c`.
- **Raw captures.** The captures are indexed in the author packet's
  `RAW-ARTIFACTS.json`. They were read from the run's raw root on the bench host
  only after each SHA-256 matched both the index and the page's artifact table
  (`raw-hashes.txt`). Seven files match in both bytes and hash, including the
  three DIN recordings, both DOUT captures and the DIN pattern.
- **Independent decoder.** `r392_decode.py` was written from the page's stated
  pattern rule alone, not from the author's tools, and decodes S32_LE captures
  and AAF pcaps. Planted controls (`r392_decoder_controls.py`) show it detects
  a slot rotation, one torn frame, a low-byte violation and a single dropped
  frame (`receipts/decoder-controls.json`, all fired).
- **Edge and beat probes.** `r392_din_edges.py` locates non-idle words outside
  the DIN playback region. `r392_dout_beat.py` classifies the DOUT clusters by
  93,990-frame chaining.
- **Gates.** Seventeen documentation and scope gates ran at the exact head with
  the pinned Markdown lock environment (`receipts/gates/`, all rc 0).
- **Exact head restored.** The only bytes the runs left in the clone were an
  ignored bytecode cache, which was removed. The worktree and index equal
  HEAD, and the gitlinks are the pins (`receipts/head-verification.txt`).
- **No prior findings.** No public review finding existed on PR #616 before
  this round; only the two review-start notices. None is carried forward.

## Re-derived evidence (independent decode against the page)

| Page claim | Page value | Reviewer decode | Receipt |
|---|---|---|---|
| DOUT 70 s: valid words per channel, tag = channel + 1, identity slot order | 3,357,952 each | 3,357,952 each; tag histogram single-valued per channel | `receipts/dout-long.json` |
| DOUT 70 s: torn, invalid, zero outside first DMA period | 0 / 0 / only the first 2,048 frames | 0 / 0 / 2,048 all-zero leading frames (16,384 words) | same |
| DOUT 70 s: repeated / dropped / clusters | 2,173 / 2,191 / 34 + 9 + 8 = 51 | 2,173 / 2,191 / 51 clusters (50 ms grouping) | same |
| DOUT beat class | 34 clusters, 657 / 691, spacing 93,989 to 93,992, net one drop each | 35 chained clusters, all net -1; the extra one is the 483 / 484 cluster at frame 129,825, which the page files under underrun. 657 + 483 = 1,140 and 691 + 484 = 1,175 reproduce the page's split exactly | `receipts/dout-long-beat.json` |
| DOUT 3 s second session | 144,000 frames, own tag everywhere, 0 torn / invalid / zero, 40 repeated / 42 dropped, two clusters net one drop | identical; cluster spacing 93,989 | `receipts/dout2-sanity.json` |
| DIN routed: PDUs, AVTP sequence gaps | 758,870, 0 | 758,870 AAF PDUs of stream `0200000000010000`, 0 gaps; AAF PCM32, 8 ch, 6 frames per PDU | `receipts/din3-long.json` |
| DIN routed: playback region and valid words | 3,360,035 frames (70.001 s), every word valid with own tag | region frames 150,490 to 3,510,524 = 3,360,035; 0 invalid words; each channel 3,360,035 own-tag words | same |
| DIN torn frames and pair offsets | 2,267,868 (67.5%); 0,0,0 1,092,167; 0,0,-1 761,510; 0,-1,-1 761,459; -1,-1,-1 744,899 | identical counts; within-pair disagreement 0 on all four pairs | same |
| Longest runs | coherent 30,477; each other state 21,096 | 30,477; 21,096 / 21,096 / 21,096 | same |
| Per-pair beat clusters | pairs 0 to 3: 35 / 36 / 36 / 36 clusters; 711/676, 736/700, 734/698, 734/698; first at 237,364 / 216,211 / 195,061 / 173,908; spacing 93,990 to 93,993 | identical, every cluster net +1 repeat, 0 backward steps | same |
| Unrouted DIN recordings | 4,550,280 and 4,554,432 frames, all zero, 0 gaps | 4,550,280 (758,380 PDUs) and 4,554,432 (759,072 PDUs), every word zero, 0 gaps | `receipts/din-long.json`, `receipts/din2-long.json` |
| Pattern source and SoC-built period | 138,240,000 bytes; period SHA-256 `b6a92e97...` | 4,320,000 frames, 0 mismatches against `((t<<16)|(n&0xffff))<<8`; first 65,536-frame period hashes `b6a92e97...` | `receipts/din-pattern.json`, `receipts/din-pattern-first-period.sha256` |
| SoC transmit DMA consumed 1,648 periods in each DIN run | 1,648 | transmit DMA interrupt deltas 1,648 / 1,648 / 1,648 in the three `soc-play.log` files | evidence packet |
| SoC receive DMA rate | 249.7 / 249.8 periods per second | 1,254 over 5.02 s = 249.8 (second session); 20.01 s window = 249.7 (first) | evidence packet |
| Identity gate | VERSION `00020060`; ROM `9b6576a9` / 52,216; QSPI `3c18c276` / 3,825,788; AEM `93742dd2` / 7,352; ENTITY and CONFIGURATION identical | identical in `identity-uart.txt` and `identity-aecp.json`; the same ROM, QSPI and AEM values appear on the merged #394 page for the same image; bitstream and AEM hashes equal the #394 image assignment | evidence packet |
| SLIP_TDM | 10,682 to 14,893 over 8,244.7 s = 0.5108/s, 10.64 ppm | `0x8D8` dup half `0x29BA` at 12:04:22.537Z and `0x3A2D` at 14:21:47.209Z: 4,211 over 8,244.67 s = 0.51076/s = 10.641 ppm; the register is one event per frame (`milan_csr.sv:925`, REGISTER_MAP) | evidence packet |
| Real reservation | Ready listener, gate open, idleSlope 16,576,000 | `LWSRP_STATUS` `0x35E` (bits 1:0 = 2), `ACMP_TALKER` `0x0A`, `LWSRP_SLOPE` `0x00FCEE00` = 16,576,000 | `s2/din3-long/dut-streaming.txt` |
| Dynamic map edits | eight identity mappings added, removed, empty after | GET_AUDIO_MAP `000f 0000 0000 0001 0000 0000` before and after (map_index 0, number_of_maps 1, 0 mappings); ADD of 8 pairs stream channel c to cluster offset c; 8 mappings read back; REMOVE; empty | `s2/din3-long/ctl-map-*.jsonl` |

**DIN root cause, checked against the implementation and the clauses:**

- **Generated shape.** `configs/generated/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh:59`
  sets `ADP_DMAP_OUT_MASK_C = 64'h1`. The source YAML declares `Stream Out 0`
  with `map_mode: dynamic` (`configs/endstation_ax7101_1x1_tdm8.yaml:233`).
- **Crossbar select.** `hdl/milan/milan_datapath.sv:3302` derives
  `aecp_odmap_dyn_w = |ADP_DMAP_OUT_MASK_C`. `:1344` makes the capture
  crossbar the packetizer source whenever that is set.
- **Empty entries.** An empty entry resolves to digital silence:
  `KL_chan_map_capture.sv:409` (SRC_ZERO = 0), `:957` (`en_f ? src_f : 0`)
  and `:972-977`. This matches `docs/CHANNEL_MAP_64.md` section 4.
- **Cluster table.** The CSRC table (`:82`) puts output clusters 0 to 7 on TDM
  pairs 0 to 3, left then right, so cluster c is TDM slot c.
- **Tested image.** There is no change in `hdl`, `configs`, `sw` or any
  gitlink between the image source `9e9954e9` and the base. `9c423e2c` and
  `0a3a78a9` are ancestors of the image source.
- **Clause semantics.** Under IEEE 1722.1-2021 (STREAM_PORT number_of_maps = 0
  means dynamic mapping; GET_AUDIO_MAP pages a dynamic map) and Milan v1.2
  (5.3.3.9 dynamic mapping; 5.3.9.1 lets a channel be not mapped while the
  stream still owes its packets), an empty dynamic output map sends silent PDUs
  until a controller adds mappings. The unrouted and routed runs differ only in
  the map edit, and the result flips from all-zero to fully decoded. The root
  cause is stated correctly. It is a controller-configuration fact, not a DUT
  defect, and the page does not call it one.

**Frame-coherence mechanism, checked against the RTL:**

- **Hold writes.** Each TDM pair's hold is written by its own pair-valid pulse
  (`KL_chan_map_capture.sv:486-487`).
- **Walk reads.** The media-tick walk reads the latest hold of each pair
  (`:959-960`).
- **Observed shape matches.** Pairs never disagree internally, pair 0 is
  always the newest, and the state cycles once per 93,990-frame beat. That is
  what per-pair holds without a frame-wide buffer produce under a 10.64 ppm
  grid offset. The attribution to the DUT capture path is supported.

## Findings

**F1 - MINOR - lenses: Docs, Tests, Robustness**

- **Where:** `docs/findings/451_TDM8_FIRST_LIGHT.md:124-125` and `:229-230`.
- **Evidence:** The page says "With the map routed, the DIN line reads all ones
  whenever the SoC is not playing, so a zero word could not have come from the
  pin". It also says "Outside the region the SoC was not playing, and the slot
  words read `0xffffff00`: the line idles high". The routed recording
  (`2ab93c0b...`) contradicts both statements:
  - frames 3,510,525 to 3,511,301 follow the playback region and carry zero
    words: 777 frames, about 16.2 ms, 6,213 words;
  - the first of them is torn exactly like the pattern frames (pair 0 zero,
    pairs 1 to 3 still carrying the last pattern ordinal). So the zeros
    arrived through the per-pair TDM holds, that is, from the pin;
  - frame 150,489 is a mixed transition word set
    (`ffffff00 fff80000 00000000 x6`).

  The author's own `s2/din3-long/decode.json` records 775 silent frames and 776
  to 777 zero words per channel (`receipts/din3-edges.json`).
- **Impact:** The root-cause paragraph rests its exclusion of the pin on a
  premise the page's own evidence refutes, and a cold reader cannot reconcile
  the text with the archive. The conclusion itself survives only through the
  narrower argument: the unrouted runs are zero also across the idle intervals
  where the routed run reads `0xffffff00`, and the only difference between the
  two second-session runs is the map edit.
- **Required outcome:** Both statements describe what the routed capture shows:
  - idle-high before playback and after the stop tail;
  - a zero tail of about 777 frames when playback stops;
  - the transition frames.

  The root-cause argument is stated in its supportable form.
- **Verification:** Re-decode the routed pcap outside the region
  (`r392_din_edges.py`) and compare it with the revised text.

**F2 - MINOR - lens: Docs**

- **Where:** `docs/findings/451_TDM8_FIRST_LIGHT.md:265-268` and owner-items
  row `:377`.
- **Evidence:** The page says the torn DIN frames are "recorded for triage as a
  separate issue". No such issue exists: a search of all repository issues at
  review time found none. The executor's REVIEW READY comment on #451 says
  "(not filed)".
  - AGENTS.md section 4 requires that "Newly discovered work becomes another
    public Issue".
  - `docs/findings/README.md` requires each finding to name its owning issue.
- **Impact:** The defect is real and re-derived here. 67.5% of the talker's AAF
  frames carry samples from two TDM frames, a one-sample inter-pair skew on the
  shipping capture path. It has no public tracking. The page reads as if
  tracking exists, and nothing links a future fix to this evidence.
- **Required outcome:** A public issue for the DIN frame-coherence defect
  exists, and the page links it where it names the separate issue.
- **Verification:** The link resolves to an open issue that cites this page's
  evidence.

**F3 - SUGGESTION - lens: Docs**

- **Where:** `docs/findings/451_TDM8_FIRST_LIGHT.md:3`.
- **Issue:** The line `[A403] REVIEW READY. Refs #451.` is lane workflow state
  inside a durable page, and will read stale once merged.
- **Suggestion:** Keep the issue reference and the operator attribution, and
  drop the status token.

**F4 - SUGGESTION - lens: Docs**

- **Where:** `docs/findings/451_TDM8_FIRST_LIGHT.md:365-378`.
- **Issue:** The owner-items table omits the #451 checklist item "Capture
  identifiable samples in both directions through the USB Audio device ...
  record the result under #448". The page is explicit elsewhere that both legs
  used McASP0 directly (`:127-129`, `:163-164`, `:170`), so it does not
  overclaim.
- **Suggestion:** Add an explicit NOT RUN row, so the "Sixty seconds of
  identifiable audio" row cannot be read as that checklist item.

**F5 - SUGGESTION - lens: Docs**

- **Where:** `docs/findings/README.md:8-17`.
- **Issue:** The "Current entries" index does not list the new page. The
  precedent is mixed: later dev rows exist for #75 and #397, but none for the
  #394 page.
- **Suggestion:** Consider adding a row.

**F6 - SUGGESTION - lens: Docs**

- **Where:** PR #616 body.
- **Issue:** The body says "Three commits" and says it removes
  `451_TDM8_FIRST_LIGHT_ATTEMPT.md`. The range has four commits (`fba793c0`
  added that page), and against dev the net change is one added file.
- **Suggestion:** Correct the body for a cold reader.

**F7 - SUGGESTION - lenses: Docs, Tests**

- **Where:** `docs/findings/451_TDM8_FIRST_LIGHT.md:281-285`.
- **Issue:** The split between "after logged talker lateness" (9) and "no
  host-visible lateness" (8) depends on a wall-clock alignment multiple. The
  packet README says that multiple was chosen partly because it is the only
  neighbour under which underruns line up with late PDUs. The page presents
  the split as an observed cause.
- **Suggestion:** State that the attribution uses a fitted alignment. The
  totals (2,173 / 2,191) and the beat class are unaffected.

## Clean-lens results

```text
[R392] PASS Conformance - docs/findings/451_TDM8_FIRST_LIGHT.md:5-24,39-81,111-119,365-381 against #451 assignment 5859278962, amendment 5729936674, owner note 5862732214; adp_shape_defaults.svh:59,82; milan_datapath.sv:1344,3302; endstation_ax7101_1x1_tdm8.yaml:233; s2/din3-long/ctl-map-*.jsonl - assignment items 1-4 recorded (sample format, slot order, -10.64 ppm offset, drops over >= 60 s per direction); NOT RUN owner items retained; not #386 acceptance 4, not #117, not a USB-audio-device capture, does not close #451/#448/#386/#117; dynamic-map root cause matches IEEE 1722.1-2021 dynamic mapping and GET_AUDIO_MAP paging and Milan v1.2 5.3.3.9 / 5.3.9.1
[R392] PASS RTL - hdl/milan/milan_datapath.sv:1335-1348,3290-3302; hdl/ieee1722/aaf/KL_chan_map_capture.sv:409-411,479-489,946-977; hdl/common/csr/milan_csr.sv:924-925; configs/generated/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh:58-82 - every RTL statement on the page (crossbar select, silence on empty entries, cluster-to-slot table, per-pair holds read at the media tick, SLIP_TDM one event per frame) matches the source at the image's RTL (0 paths differ from 9e9954e9 in hdl/configs/sw/gitlinks); no RTL in the diff
```

Robustness, Tests and Docs are not clean: F1 is open under all three and F2
under Docs. Robustness was otherwise applied as follows:

- stream start and stop transitions;
- unrouted versus routed configuration;
- AVTP sequence gaps;
- AAF header stability across all PDUs;
- the xz-to-gzip transfer fallback;
- the REBOOT operator error, checked against continuous slip counters;
- restoration: DUT control words and PP_STAT equal across the second session.

Its only defect is the F1 stop-boundary claim. Tests was otherwise applied as
the independent re-derivation above, and the author's decode agrees with the
reviewer's decode on every count.

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | page `:5-24,39-81,111-119,365-381`; #451 body, assignment, amendment, owner notes; `adp_shape_defaults.svh:59,82`; `endstation_ax7101_1x1_tdm8.yaml:233`; `milan_datapath.sv:1344,3302`; GET_AUDIO_MAP / ADD / REMOVE replies; identity evidence against the #394 assignment and page | R392-1 | `6339479d69830614d4267bd3170113737afbf8f4` |
| RTL | CLEAN | `milan_datapath.sv:1335-1348,3290-3302`; `KL_chan_map_capture.sv:409-411,479-489,946-977`; `milan_csr.sv:924-925`; generated shape `:58-82`; image-source-to-base diff (0 paths) | R392-1 | `6339479d69830614d4267bd3170113737afbf8f4` |
| Robustness | UNCLEAN (F1) | routed and unrouted pcaps at the start and stop boundaries (`receipts/din3-edges.json`); AAF header stability; sequence gaps; restoration words (`s2-dut-before/final.txt`); operator-error disclosure | R392-1 | `6339479d69830614d4267bd3170113737afbf8f4` |
| Tests | UNCLEAN (F1) | seven hash-verified raw captures decoded independently (`receipts/*.json`); decoder planted controls (all fired); author `decode.json` / `pairs.json` / `attribution.json` cross-checked | R392-1 | `6339479d69830614d4267bd3170113737afbf8f4` |
| Docs | UNCLEAN (F1, F2) | the full page; `docs/findings/README.md`; linked anchors (`CHANNEL_MAP_64.md` section 4, `TIME_SYNC.md` listener render latency, `CLOCK_DOMAINS.md:119`); the public-record scan of the page (no private host, peer, switch, instrument or suite name, no absolute home path); 17 gates rc 0 (`receipts/gates/`); PR body | R392-1 | `6339479d69830614d4267bd3170113737afbf8f4` |

## Limits

- **Not re-derived.** The following were taken from the author's logs and
  census files, and were not re-derived from raw data:
  - the DOUT listener counters, presentation offset and rail counts
    (`:294-298`);
  - the gPTP-slope FSYNC estimate (`:319-322`);
  - the software talker's pacing (`:156-161`);
  - the peer-side restoration states (`:328-330`).
- **Evidence-side only.** The raw captures were read from the run's raw root
  on the bench host after hash matching. They are not published, because the
  originals can carry bench identifiers. The re-derivation is reproducible by
  anyone holding bytes with the listed hashes.
- **Scope of the probes.** No simulation or builder probe was run, and none was
  needed for a documentation-only diff: the RTL claims were checked by
  reading the source. There was no physical measurement. Calibration,
  continuity and scope items stay NOT RUN, and field skips are not hardware
  proof.
- **Hosted checks at the exact head, as observed:**
  - completed successfully: `rtl-fast`, `docs-check-no-git`, `elaborate`,
    `wire-accountability`, `full-ci-gate`, `changes`, `bdd-conformance`;
  - skipped contexts, not executed evidence: `verilator-suites` and
    `yosys-portability`;
  - still in progress when observed: `docs-check`.

## Pending manager duties

- **F1 and F2.** Both must be answered at a new head and re-reviewed. This
  round's CLEAN results for Conformance and RTL cover only
  `6339479d69830614d4267bd3170113737afbf8f4`. A later edit to the page
  re-opens Docs, and re-opens Conformance if it touches the scope or root-cause
  text.
- **Hosted and local acceptance.** The manager owns hosted and act acceptance,
  including the `docs-check` conclusion at the final head.
- **Candidate merge.** The manager owns validation of the current-dev candidate
  (base `6d5ebd73`, live dev `7a7582f0`) at the merge turn.
- **Second review.** The second independent review is still required.

R392-1 FINISHED
