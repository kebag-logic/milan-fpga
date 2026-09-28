[R393] NEGATIVE - exact head 6339479d69830614d4267bd3170113737afbf8f4

# R393-1: external independent review of PR #616 (issue #451)

- Head under review: `6339479d69830614d4267bd3170113737afbf8f4`, tree `bd639facbd225ea39aa77f89149f8e9d94b18b56`.
- Source base: `6d5ebd7357c1e468e446f18a61527c5be6118a04`. The net diff is one added file, `docs/findings/451_TDM8_FIRST_LIGHT.md` (+404). The PR carries four commits: `fba793c0`, `361d1f47`, `4f06bfc7` and `6339479d`. All four have one-line messages with no trailers.
- Round: R393-1, external reviewer, cleared context. I rebuilt the task from AGENTS.md, CONTRIBUTING.md and docs/README.md. I then read the #451 body, the PocketBeagle 2 amendment (#451 comment 5729936674), the A382 assignment (5859278962), the owner restart note (5862732214), the executor TAKEN, STOP and REVIEW READY comments, the PR body and the diff. I also read the cited RTL and generated shape, and the public evidence archive at `851f835c8ba778b82c78ca9cf0ec814613ddfeda:review-evidence/451-r1`.
- Verdict: NEGATIVE. My own round leaves three MINOR findings open, under Docs (all three) and Conformance (one). I also retain R392-F1 (MINOR; Docs, Tests, Robustness), which is still open at this head. I found no error in any measured number on the page. I re-derived every decode table from the hash-verified raw captures, and I confirmed the DIN root cause against the RTL and the regenerated shape.

## Findings

### F1 - MINOR - Docs - `docs/findings/451_TDM8_FIRST_LIGHT.md:265-268`, `:377`: the DIN frame-coherence defect is said to be "recorded ... as a separate issue", but no issue exists

- **Authority and evidence.** AGENTS.md section 4 says: "Newly discovered work becomes another public Issue." `docs/findings/README.md` requires every finding to name its "owning issue". The page says "It is recorded for triage as a separate issue", and the owner-items row reads "NOT MET: a DUT capture-path property, for triage as a separate issue". Neither gives an issue number. The executor's REVIEW READY comment says "(not filed)". I searched the repository's issues for this property (capture crossbar, `KL_chan_map_capture`, latest-sample, torn and coherence), in open and closed state. No issue tracks it.
- **Why it matters.** I re-derived the defect myself (`receipts/din-din3-long.json`, `receipts/din3-state-order.json`): 2,267,868 of 3,360,035 frames are torn between TDM pairs, in four states that cycle once per beat. The page is the only durable record of a real capture-path defect, and it points to a tracking item that does not exist. A cold reader cannot find an owner, and nothing in the project will keep the defect visible.
- **Required outcome.** A public issue records the frame-coherence property, and the page cites it by number, or the page states plainly that it is untracked and who is to file it. Moving the defect to an issue is enough for this PR: the PR is documentation-only and did not introduce the defect.
- **Verification.** The issue exists, and the page's paragraph and owner-items row link it.

### F2 - MINOR - Docs - `docs/findings/README.md:8-17`: the new finding is missing from the findings index

- **Authority and evidence.** `docs/findings/README.md` says the directory "contains current hardware findings" and lists them under "Current entries". The only other issue-numbered findings page in this directory, `117_GPTP_SILICON_EVIDENCE.md`, added its index row in the same commit (`c3eb95fa9`: page +313, `docs/findings/README.md` +1). At this head no file in the repository links `451_TDM8_FIRST_LIGHT.md`: I searched Markdown, Python, JSON and YAML, and only the page itself matches. AGENTS.md section 7 requires "authoritative documentation is current".
- **Why it matters.** Once merged, the directory's own index would not list the page, and nothing in the tree would lead to it. `PP_SHADOW_BASELINE.md` is also missing from the index, but that gap predates this PR and is noted only for context.
- **Required outcome.** Add a "Current entries" row with scope and state, for example: TDM8 first light over the PocketBeagle 2 link, both directions decoded; DIN frame coherence NOT MET; owner items NOT RUN. Alternatively, record why this page is deliberately left out of the index.
- **Verification.** The index row exists, and `scripts/docs_check.py` and `scripts/check_doc_paths.py` still pass.

### F3 - MINOR - Docs, Conformance - `docs/findings/451_TDM8_FIRST_LIGHT.md:107-109`, `:370`: the claim that the owner checked "all five connections" has no public source and conflicts with the seven-conductor wiring spec

- **Authority and evidence.** The authoritative PocketBeagle 2 amendment (#451 comment 5729936674) specifies "Seven conductors: four signals, three grounds". The page says "The owner reported checking all five connections". No owner report of a wiring check appears on #451 or PR #616, and the public packet's HANDOFF.md and README.md mention the check without a count or a source.
- **Why it matters.** Five cannot be squared with the recipe without explanation. Either the page misstates the check, or the bench link has fewer ground returns than the amendment requires. The second case would be an undisclosed deviation of the as-built bench from its spec, and the page is the first-light record of that bench. The claim is also unverifiable from public state, which AGENTS.md section 2 forbids a future cold reviewer to depend on.
- **Required outcome.** Either cite a public record of the owner's check and reconcile its count with the amendment, or record the as-built conductor set if it differs from the amendment, or drop the count. The electrical continuity check stays NOT RUN either way; the page already says so.
- **Verification.** The page text matches a public source, and the count matches the amendment or is recorded as a deviation.

### Suggestions (optional; they do not affect lens coverage)

- **S1 (Docs, `:229-230`; superseded, see the retained R392-F1 below).** "Outside the region ... the slot words read `0xffffff00`" is not exact. Immediately after the playback region, recording frames 3,510,525 to 3,511,301 (777 frames, about 16 ms) carry 6,213 zero words, and frame 150,489 is a partial transition frame (`receipts/din3-outside-census.json`). This is the SoC's transmit start and stop transient. In my independent pass I rated this a suggestion, because the inference on lines 124-125 still holds on a narrower argument: the unrouted recordings are all zero, including about 25 s in which the SoC was not playing. I now retain it at MINOR as R392-F1, for the reason given there.
- **S2 (Docs, `:3`).** "[A403] REVIEW READY. Refs #451." is a transient lane status. It becomes false at merge, and no other findings page carries one.
- **S3 (Docs, Conformance, `:365-381`).** The recipe checklist item "Capture identifiable samples in both directions through the USB Audio device" is not delivered by this run: both legs bypass the USB function (`:127-130`, `:164`, `:170`). The page never claims otherwise, and "does not close #451" covers it. An explicit NOT RUN row would still make the remaining #451 scope readable at a glance.
- **S4 (Docs, PR body).** The PR body says "Three commits", but the PR carries four. `fba793c0` adds the attempt page that `361d1f47` removes.
- **S5 (Docs, `:281-285`, `:260`).** Two of the 36 beat crossings in the DOUT capture fall inside underrun clusters: the clusters starting at frames 129,825 (483 repeats, 484 drops) and about 411,320. The "34" row is therefore the 34 clean crossings, not every crossing (`receipts/dout-long-beat-chain.json`). Also, the TDM hold read is at `KL_chan_map_capture.sv:959-960`; line 958 is the I2S arm.
- **S6 (Docs, `:385-387`).** The packet `451-a403` is named but not linked. A link to the public archive would let a cold reader reach the validation record.

## Independent reconstruction (what each claim was checked against)

Raw captures come from the author's raw root. Every file was matched to the page's artifact table and `RAW-ARTIFACTS.json` by SHA-256 before use (`raw-sha256.txt`: 8 of 8 equal). The remaining three rows are the assigned bitstream, the AEM image and the SoC-built period. The period's hash is re-derived below, and the image CRCs match the UART identity transcript. I did not re-hash the bitstream or AEM image binaries. All decoders are my own (`scripts/`); I used none of the author's tools.

| Page claim | Independent result | Receipt |
|---|---|---|
| DOUT 70 s: 8 channels × 3,357,952 valid words; tag t on channel t-1; 0 torn, 0 invalid; only zero words are the first 2,048-frame period | Equal on every point | `receipts/dout-dout-long.json` |
| DOUT: 2,173 repeated, 2,191 dropped, net 18; 51 clusters at 50 ms grouping | Equal | same |
| DOUT beat class: 34 clusters, 657 / 691, spacing 93,989 to 93,992 | Equal for the 34 clean crossings; the other 17 clusters total 1,516 / 1,500, which equals 975 + 541 and 963 + 537 (see S5) | `receipts/dout-long-beat-chain.json` |
| DOUT 3 s second session: 144,000 frames, no torn, invalid or zero word; 40 / 42 in two clusters, net one drop each | Equal; spacing 93,989 | `receipts/dout-dout2-sanity.json` |
| DIN routed: playback region 3,360,035 frames (70.001 s), 8 × 3,360,035 valid own-tag words, identity order | Equal (region frames 150,490 to 3,510,524) | `receipts/din-din3-long.json` |
| DIN: 758,870 PDUs, 0 AVTP sequence gaps; AAF format 0x02 (INT32), nsr 5 (48 kHz), 8 channels, 32-bit depth, 192-byte payload, PCP 3, VID 2 | Equal | same |
| DIN torn 2,267,868 (67.5%); pair-internal disagreement never; shape table 1,092,167 / 761,510 / 761,459 / 744,899; longest runs 30,477 and 21,096 | Equal | same |
| State cycle order and "back and forth a few times at each change" | 0,0,0 → 0,0,-1 → 0,-1,-1 → -1,-1,-1 → 0,0,0 (36/36/36/35 transitions); dither runs at most 2 frames | `receipts/din3-state-order.json` |
| DIN per-pair clusters 35/36/36/36; repeats and skips 711/676, 736/700, 734/698, 734/698; spacing 93,990 to 93,993; each nets one repeat | Equal. First-cluster frames are 1 lower in my convention (step index versus following frame) | `receipts/din-din3-long.json` |
| Unrouted DIN: 4,550,280 and 4,554,432 frames, all zero, 0 sequence gaps | Equal (only value `00000000`) | `receipts/din-din-long.json`, `receipts/din-din2-long.json` |
| Pattern `(t<<16 \| n&0xffff)<<8`; SoC period of 65,536 frames with SHA-256 `b6a92e97...`; played bytes equal the first-session source | The source equals the formula at every word, is periodic in 65,536 frames, and its first period hashes to `b6a92e97...` | `receipts/din-pattern-check.json` |
| SoC TX DMA 1,648 periods in each DIN run; RX DMA 249.7 and 249.8 periods/s | 2280-632, 3936-2288 and 5584-3936 = 1,648; 4,997 / 20.01 s = 249.7; 1,254 / 5.02 s = 249.8 | packet `soc-play.log`, `soc-h08-clock.log`, `s2-h02-clock.log` |
| SLIP_TDM 10,682 → 14,893 over 8,244.7 s = 0.5108/s = 10.64 ppm | `0x8D8` low half 0x29BA → 0x3A2D; 12:04:22.537Z to 14:21:47.209Z = 8,244.67 s; 4,211 / 8,244.67 = 0.5108; ÷48,000 = 10.64 ppm; divider plan in CLOCK_DOMAINS.md:119 is about -10.64 ppm | packet `identity-uart.txt`, `s2/dut/s2-dut-final.txt` |
| Identity: VERSION 00020060; ROM 52,216 B CRC 9b6576a9; QSPI 3,825,788 B CRC 3c18c276; AEM 7,352 B CRC 93742dd2; ENTITY and CONFIGURATION equal to verified payloads | Equal in the UART transcript and `identity-aecp.json` | packet |
| Image source `9e9954e9` after `9c423e2c` (and the recipe floor `0a3a78a9`); pins PP `870ff88a`, gPTP `5dce647a`, AXIS `48ff7a7e`, external `efeb541a` | Ancestry holds; the gitlinks at `9e9954e9` are exactly these four; `9e9954e9` is an ancestor of the head | local git |
| Reservation admitted: Ready listener, idleSlope 16,576,000 bit/s | `LWSRP_STATUS` 0x35E (bits 1:0 = 2 ready, bit 2 registered); `LWSRP_SLOPE` 0x00FCEE00 = 16,576,000 | packet `s2/din3-long/dut-streaming.txt`, REGISTER_MAP.md:1178-1179 |
| DOUT listener: 0 seq mismatch, unsupported or uncertain; 0 depacketizer drops; locked, no unlock or interrupt; ts_delta 1.98 ms; rails 3 → 142 | `AVTPRX_STAT` 0x101, `AVTPRX_ERR` 0, `PCMRX_CNT[31:16]` 0, `AVTPRX_TSD` 1,980,008 ns, `RENDER_STAT[31:16]` 3 (active-1/2) → 142 | packet `dout-long/dut-*.txt` |
| Map edits: GET_AUDIO_MAP on 0x000F/0 answers number_of_maps 1, 0 mappings; 8 identity adds; removed; reads back empty | Payloads decode to exactly that | packet `s2/din3-long/ctl-map-*.jsonl` |
| Census matched except propagation delay (and, in session 1, the MAAP destination) | S2: 1 of 32 differs (GET_AVB_INFO delay). S1: 4 differ, namely the delay, the DMAC `91e0f0003f0a`, and the two baseline map entries that the disclosed `0x002A` (REBOOT) mistake answered NOT_IMPLEMENTED. `maps-before.jsonl`, the corrected baseline, equals the after state | `receipts/census-s1.json`, `receipts/census-s2.json` |
| McASP0 `dsp_a`, codec side bit-clock and frame master, 8 × 32-bit slots, serializer 0 TX / 1 RX | Device-tree dump agrees | packet `soc-h04-tree.log` |
| Controller gPTP daemon is slave-only | Started with `-s`; no transition to MASTER, PRE_MASTER or GRAND_MASTER in any of the 14 daemon logs | packet `tools/with_gptp.py`, `ctl-*`, `s2/ctl/staging/*-gptp.log` |

### DIN root cause (focus item 2)

- **The generated shape makes the output map dynamic.** `configs/endstation_ax7101_1x1_tdm8.yaml:233` declares the talker `map_mode: dynamic`. The generated `adp_shape_defaults.svh:59` sets `ADP_DMAP_OUT_MASK_C = 64'h1` (bit 0 = STREAM_PORT_OUTPUT 0).
- **The generated file is current.** I regenerated the shape with `sw/builder/endstation_builder.py` at the head, and the output is byte-identical to the tracked file. The builder also rewrote the tracked `adp_shape_defaults.svh` and `sweep_opts_ax7101.sh` in place, but with identical blobs `e7c35196...` and `0105deeb...`, so the index and worktree were unchanged. The clone-integrity receipt confirms this.
- **Dynamic ownership forces the capture crossbar into the talker path.** `milan_datapath.sv:3302` has `assign aecp_odmap_dyn_w = |ADP_DMAP_OUT_MASK_C;`. At `:1344-1348`, `cap_xbar_live_w = aecp_odmap_dyn_w | cfg_chmap_enable` selects the `KL_chan_map_capture` outputs over the zero-fill front end.
- **Only the protocol processor writes the map.** The map RAM is written only by the ADD/REMOVE transaction block (`:1225-1239`, `:3299-3301`) or the CSR override. No boot seeder exists in the RTL. The builder's `AEM_ODMAP_INIT_C` image has no RTL consumer in `hdl/`.
- **Unmapped channels are silent.** `KL_chan_map_capture.sv:957` gates the source on the entry's EN bit, so an unmapped channel resolves to silence (CHANNEL_MAP_64.md section 4). On the wire, the empty map observed at baseline and in the session-2 pre-edit read therefore yields all-zero talker words, which is exactly what both unrouted recordings show.
- **The observed GET_AUDIO_MAP reply is the expected dynamic-port behaviour.** A dynamic port answers from the RTL mapping store, with one page because the output partition is at most 8 channels (generated AEM comment, IEEE 1722.1-2021 7.4.44, Milan v1.2 5.4.2.26 to 5.4.2.28), so `number_of_maps` 1 with 0 mappings is expected.
- **The cited files are the ones the image was built from.** `milan_datapath.sv`, `KL_chan_map_capture.sv`, the shape YAML, the generated `.svh`, `CHANNEL_MAP_64.md` and the platform file are identical between the image source `9e9954e9` and the head.
- **The mechanism was exercised in simulation.** The focused `tb/verilator/chmap_capture` RTL harness passes at the head with 204 checks and 0 failures, including "unmapped pair is silence". Removing the EN gate (`unique case (src_f)`) makes 6 silence checks fail, so those checks can detect the claimed behaviour (`receipts/chmap-capture-*.log`).

### Frame-coherence mechanism

`KL_chan_map_capture.sv:486-487` writes each `tdm_hold_r[pair]` on that pair's own `tdm_pair_valid_i`. The emit walk (`:986-1060`) resolves each slot live through `resolve_ch` (`:976-977`, `:959-960`) with no frame snapshot. This is consistent with the measured four-state cycle: coherent, then pair 3 old, then pairs 2 and 3 old, then pairs 1 to 3 old, once per 10.64 ppm beat. The page correctly limits this to a DUT capture-path property and records it as NOT MET (see F1).

### Overclaim check (focus item 3)

- The page says it does not close #451, #448, #386 or #117.
- The #386 acceptance 4 row and the calibrated #117 listener-audio row are NOT RUN owner items.
- Both legs are stated to bypass the SoC's USB function. The page never claims a USB-audio-device capture (see S3).
- The gPTP-slope figure is labelled uncalibrated.
- The identity gate is described as CRC consistency and descriptor identity, not a SHA-256 readback.

No overclaim was found.

### Public-record check (focus item 4)

I scanned the page for home, tmp and data paths, IP and MAC addresses, host names, peer, switch, instrument and suite product names, and private identifiers. Nothing was found: the page uses neutral role labels throughout ("controller host", "bench host", "reference peer", "SoC board"). The public packet uses redaction placeholders.

### Markdown gates (focus item 5)

All eight gate commands pass (rc 0) at the head. Gates 3 and 4 ran under a private venv holding the hash-pinned renderer. I also rendered the page with cmark-gfm: all 11 tables have a constant cell count per row and no empty cell. Receipts: `receipts/gates/`, `receipts/table-cells.json`.

## Reviewer-owned completion ledger (R393-1)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F3 open) | #451 body, amendment 5729936674, assignment 5859278962 (scope items 1 to 4, NOT RUN list, rules, gates), page `:1-381` against every packet artifact and all 8 hash-verified raw captures (table above), IEEE 1722.1 and Milan dynamic-map semantics against the GET/ADD/REMOVE payloads | R393-1 | `6339479d69830614d4267bd3170113737afbf8f4` |
| RTL | CLEAN | `hdl/milan/milan_datapath.sv:1225-1239,1333-1348,3294-3302`; `hdl/ieee1722/aaf/KL_chan_map_capture.sv:470-489,941-977,979-1060`; `configs/generated/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh:55-82` (regenerated byte-identical); shape YAML `:206-233`; equality of the cited RTL between image source `9e9954e9` and head; focused harness 204/0 plus mutant kill | R393-1 | `6339479d69830614d4267bd3170113737afbf8f4` |
| Robustness | UNCLEAN (retained R392-F1 open) | Boundary and failure behaviour in the evidence: DIN region edges and idle or transient words (`receipts/din3-outside-census.json`), the all-zero unrouted runs, 0 AVTP sequence gaps in 3 recordings, DOUT first-period exclusion and cluster classes, the refused REBOOT (`0x002A`) with slip-counter continuity, and restoration census diffs for both sessions (`receipts/census-s*.json`). My own application found nothing further; the lens stays unclean only because of the stop-boundary claim | R393-1 | `6339479d69830614d4267bd3170113737afbf8f4` |
| Tests | UNCLEAN (retained R392-F1 open) | `git diff --stat 6d5ebd73..6339479d` changes no test and no RTL (one Markdown file), so no new test is owed. The page's executable evidence was re-derived by independent decoders (`scripts/decode_dout.py`, `decode_din.py`, `din_state_order.py`, `dout_beat_chain.py`, `check_pattern.py`, `census_diff.py`). The existing `tb/verilator/chmap_capture` harness passes at the head, and its silence checks fail under an EN-gate mutant. My own application found nothing further; the lens is unclean only through R392-F1's lens assignment | R393-1 | `6339479d69830614d4267bd3170113737afbf8f4` |
| Docs | UNCLEAN (F1, F2, F3 and retained R392-F1 open) | `docs/findings/451_TDM8_FIRST_LIGHT.md` (all 404 lines), `docs/findings/README.md:1-21`, `docs/CHANNEL_MAP_64.md:222-240,312-345`, `docs/design/TIME_SYNC.md:322-345`, `docs/litex/CLOCK_DOMAINS.md:119`, `docs/reference/REGISTER_MAP.md` (0x694, 0x698, 0x6B8 to 0x6EC, 0x8D4, 0x8D8, 0x8DC), PR body, 8 gates, 11-table render check, public-record scan | R393-1 | `6339479d69830614d4267bd3170113737afbf8f4` |

## Prior public review findings on this PR

I read the prior public findings only after the verdict and ledger above were written. One round had posted findings: R392-1 (PR #616 comment 5872415917, NEGATIVE, same exact head). Nothing has changed since it posted (the head is still `6339479d`), so every finding is disposed of at this head as follows.

| R392 finding | Severity and lenses (as R392 assigned) | Disposition at `6339479d` | Basis |
|---|---|---|---|
| F1: "reads all ones whenever the SoC is not playing, so a zero word could not have come from the pin" (`:124-125`) and "Outside the region ... `0xffffff00`" (`:229-230`) are contradicted by the routed capture | MINOR; Docs, Tests, Robustness | **RETAINED, open.** I agree with the fact and the severity. | My own receipt shows the same 777-frame zero tail (frames 3,510,525 to 3,511,301; 6,213 words) and the transition frame 150,489. The first tail frame is torn like the pattern frames: pair 0 is `00000000` while pairs 1 to 3 still read ordinal `0x44ff` (`receipts/din3-outside-census.json`). So the zeros passed through the per-pair TDM holds, which means they came from the pin. The page's literal premise is therefore false. The root-cause conclusion survives only on the narrower argument (the unrouted runs are zero also over idle intervals where the routed run reads `0xffffff00`). My independent S1 recorded the fact as a suggestion; after this reasoning I retain it at MINOR. |
| F2: coherence defect "recorded ... as a separate issue", but no issue exists | MINOR; Docs | **RETAINED, open.** It duplicates my F1. | Same evidence as my F1. |
| F3: transient "[A403] REVIEW READY" status at `:3` | SUGGESTION; Docs | Retained (optional). It duplicates my S2. | — |
| F4: owner items omit the USB Audio device capture item | SUGGESTION; Docs | Retained (optional). It duplicates my S3. | — |
| F5: findings index lacks the page | SUGGESTION; Docs | Retained. **I rate the same defect MINOR** (my F2). | On live dev `7a7582f0`, 3 of 4 issue-numbered findings pages (#75, #397, #117) have index rows, and only the #394 page lacks one. The index still promises "Current entries". The two reviewers disagree on severity; I keep MINOR. |
| F6: PR body says "Three commits" | SUGGESTION; Docs | Retained (optional). It duplicates my S4. | — |
| F7: the underrun 9 / 8 split rests on a fitted alignment multiple | SUGGESTION; Docs, Tests | Retained (optional). | I list the same dependence under Limits. The totals and beat class are unaffected. |

With R392-F1 retained, Robustness and Tests are not covered clean at this head, even though my own application of both found nothing further (AGENTS.md section 8: "a lens is not covered clean while a finding under it is open"). The ledger above reflects this. R392's clean results (Conformance, RTL) and mine (RTL) are independent. My Conformance lens is unclean through my F3, which R392 did not raise.

## Limits (real)

- **Physical measurements.** Physical calibration was NOT RUN, and no hardware was touched. Every bench fact is taken from the archived evidence: the SoC-side kernel fix, the no-flash, power, wiring and gadget statements, and the lock discipline. Field skips are not hardware proof.
- **Raw captures.** The raw captures were read from the author's raw root (not public). I verified each by SHA-256 before use. The page's claims are reproducible only while that root is retained.
- **DOUT underrun attribution.** The 9 / 8 split between "after logged talker lateness" and "no host-visible lateness" depends on the author's wall-clock alignment multiple (8). I verified the combined totals and the beat-chain split, not that alignment.
- **Uncalibrated slope figure.** The -5 ppm gPTP-slope figure (page `:319-322`, labelled uncalibrated) was not re-derived.
- **Verilator build.** The Verilator path named in the review brief did not exist. The focused harness used another Verilator 5.050 build on the review host ("Verilator 5.050 2026-07-01 rev v5.050", `verilator_bin` SHA-256 `51910d8d47cfa29ee548a42eca10147e94b2f5b6014d68c110de1740274cc26a`), with at most 8 build jobs.
- **Netlist leg.** The harness's netlist leg (`make netcheck`, which needs sv2v and yosys) was not run.
- **Protocol-processor seeding.** Whether the protocol processor seeds an output map at power-on was not established from its sources. The RTL has no seeder, and the page makes no power-on claim; the observed baseline map was empty.

## Pending manager duties

- Hosted evidence at the exact head: `rtl-fast`, `bdd-conformance`, `changes`, `elaborate`, `full-ci-gate`, `wire-accountability` and `docs-check-no-git` show pass; `docs-check` was still pending when read. `verilator-suites`, `yosys-portability`, `verilator-lint` and `yosys-elaboration` are skipped contexts (documentation-only scope), not executed evidence.
- The act replica and hosted acceptance.
- The final current-dev candidate build against live `dev` `7a7582f03ce5ba7863a90ac342c21be18d90db0b` at the merge turn.
- Filing or recording the tracking issue for F1 (the same item as R392-F2).
- Getting the executor's answers to F1 to F3 and to the retained R392-F1 at a new head, then re-review at that head. Any edit to the page re-opens Docs, and re-opens Conformance if it touches the scope, wiring or root-cause text.
- Merge authorization. Two independent POSITIVE reviews are still required, and R392-1 is also NEGATIVE at this head.

## Clone state after probes

- **Worktree.** The review clone is at the exact head, with no untracked or ignored files: `git status --porcelain --ignored` is empty.
- **Tracked files and index.** All 931 regular tracked files rehash to their index blobs, with 0 file-mode mismatches. The index equals the HEAD tree in mode, blob and path.
- **Gitlinks.** `external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `870ff88a` and `third_party/verilog-axis` `48ff7a7e` all equal HEAD.
- **Stray files removed.** A failed probe invocation left two stray logs in the clone root, and `__pycache__` directories came from running the builder and gates. All were removed and verified absent (`receipts/clone-integrity.txt`). All probes and builds ran on copies under the packet's scratch directory.

R393-1 FINISHED
