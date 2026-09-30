[R415] NEGATIVE - exact head 6dfa64a7506a8660a70d77eaa7c96c5de2886f5d

# R415-1: external review of PR #624 (#617 acceptance 4, #451 USB Audio capture)

- Head `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d`, tree `1538061a99a88ef7e870dbcc079cc9dbdf0ca16f`. It is one commit on dev `ec0cc0c1df7d7ab3e25d973958f53f0074393d2c`, with a one-line subject, no body and no trailers.
- The diff is documentation only: `docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md` (+258) and `docs/findings/451_USB_AUDIO_CAPTURE.md` (+216). No gitlink, RTL, test or tooling change.
- The review ran in a cleared context. I rebuilt the task from these public sources:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the #617 body and the B3 assignment (#617 comment 5903384996);
  - the #451 recipe and the PocketBeagle 2 amendment (5729936674);
  - the first-light page and REGISTER_MAP `SLIP_TDM`;
  - TIME_SYNC "Talker capture handoff" and SAVED_STATE_SNAPSHOT_OWNERSHIP;
  - the diff and history `ec0cc0c1..6dfa64a7`;
  - the public evidence packet at `68e0f45b6313bee8d74f2a92d990ba200b78d518:review-evidence/b3-r1`.
- I read no private author material and no other reviewer's report.
- **Verdict: NEGATIVE, on one MINOR (Docs).** Every measurement claim in both pages re-derives from the public packet. #617 acceptance 4 is met by the evidence. The only open item is the findings-index gap, which needs a manager scope decision.

## Answers to the assigned focus

1. **Identity gate: PASS, as the assignment defined it.**
   - Re-derived from the packet (`receipts/identity-recheck.txt`): VERSION `00020060`, AEM CRC32 `93742dd2` over 7,352 B, entity `020000fffe000001`.
   - The AECP ENTITY (312 B) and CONFIGURATION (106 B) payloads are byte-equal to the console's QSPI dumps at `0x01400110` and `0x01400248`.
   - VERSION, AEM CRC, entity and ROM CRC `acad92b9` are the same on `13eda870`. VERSION and AEM CRC are also the same on first light's `9e9954e9`. Only the QSPI payload CRC (`d178f19a`, against `d84bce7b` on `13eda870`) shows that a different bitstream was installed. The `ec0cc0c1` build's own payload CRC is not in the public record, and the page says it is "recorded as read" (S2).
   - The image's RTL delta is exactly PR #618's four `.sv` files; PR #619 changes an import only (`git diff` at each first-parent merge). The page states this correctly.
2. **#617 acceptance 4: met.**
   - **Definition.** Inside the playback region every word is a valid pattern word (0 invalid frames). There the page's rule ("valid words carry more than one ordinal") is exactly #617's definition: a frame carrying samples of two TDM frames.
   - **Counts.** Every figure re-derives from `runs/din-long/grade.json` (`receipts/numbers-recheck.txt`):
     - region 45,588 to 3,405,623 = 3,360,036 frames; 758,604 PDUs x 6 = 4,551,624 frames; 0 sequence gaps;
     - torn 0 in the region and 0 in the whole recording;
     - pair state `[0,0,0]` in all 3,360,036 frames; left/right mismatch 0 in every pair;
     - outside words 9,526,486 `ffffff00` + 1 `fffff000` + 6,217 zero = 1,191,588 x 8;
     - zero words 6 + 776 x 8 + 3.
   - **Grader.** Synthetic probes (`receipts/grader-probes.txt`) show `grade_617.py` counts 101 injected first-light-shape tears, 3 left/right tears and whole-frame repeats exactly, so the 0 can fail. The whole-recording figure uses a narrower rule than #617 outside the region (S1). The acceptance rests on the region count, which is exact.
   - **DIN continuity.**
     - 36 non-unit steps, all repeats, at identical frames in all 8 channels, spaced 93,990 to 93,993.
     - `SLIP_TDM` (`0x8D8` low half) reads 383, 391, 427, 440, skips 0. The streaming to after-play interval is 70.47 s, with +36 against 35.99 expected at 10.64 ppm (`receipts/slip-rate.txt`).
     - This is the design law of TIME_SYNC "Talker capture handoff" (one whole-frame slip per 1.958 s beat, counted once) and of the REGISTER_MAP `SLIP_TDM` reading table. The INTERNAL tick drifts through the whole TDM frame once per beat, so 36 beats sample every relative phase at which the old design tore 67.5%.
   - **DOUT, unchanged in kind.** Re-derived from `decode.json` and `attribution.json`:
     - 3,360,000 frames, each channel only its own tag, 0 torn, 0 zero;
     - 59 clusters: 36 beat clusters (696 repeats, 732 skips, net one drop each, 93,989 to 93,992 apart) and 23 underrun clusters;
     - alignment multiple 7 is the only one of 0 to 12 that matches more than 2 underruns: it matches 12 (`receipts/dout-alignment-recheck.txt`).
   - **Channel order.** Identity in both directions.
   - The first-light tool copies are byte-identical to the public #451 archive (`receipts/first-light-tools-unchanged.txt`).
   - **#617 can close.** Acceptance 1 to 3 landed with PR #618 (merged `9e3ccbfb`), and acceptance 4 is shown here. The PR says Refs only, so closure is by hand once this record lands.
3. **#451 capture through the USB Audio device: FAIL, measured correctly, not overstated.**
   - **Runs.** Both are 3,600,000 frames with rc 0 (75.116 s and 75.108 s), and `strict.valid_frames` is 0 in each. The class sums close exactly to 3,600,000, and every other figure in both tables re-derives (`receipts/numbers-recheck.txt`).
   - **Grader.** The probes show that an exact pattern passes the strict rule 5,000 of 5,000. A 3-word rotation is classified `rot3`, and a low-byte offset fails strict but stays `aligned`. So 0 of 3,600,000 is not a grader artifact.
   - **Reference.** The McASP0-direct recording of the DUT output (`dout-long`) is exact.
   - **Attribution.** The page places the loss in "the bridge leg, the USB Audio function or the bench host's USB path". It says the lane cannot separate them. It uses the rate-converting copy only as a comparison ("as a sample-rate converter's output does"). The DUT is excluded on three grounds:
     - the direct recording under the same method;
     - clean DUT listener counters during both USB runs;
     - McASP0 receiving at full rate (DMA edge count +18,942 in about 75.6 s).
   - That exclusion is an inference across runs, since McASP0 cannot be recorded directly while the bridge owns it. It is sound, because DUT-side render events only produce whole-frame repeats and jumps, never rotation, interpolation or silence.
4. **Continuity check: NOT RUN, correctly recorded.** It needs a meter on the unpowered boards, and the assignment forbids power, wiring and instrument actions. The page limits the signal-data substitute to the four signal pins, not grounds or resistances.
5. **Restore: proven.**
   - Census 33 of 33 equal, ignoring exchange fields (`receipts/census-recheck.txt`). All 18 stream states have `conn_count` 0, and both audio maps read `number_of_mappings` 0.
   - The controller clock frequency reads `28062.332153` ppb at start and end, with a 4,352 ns trajectory residual. Timestamping is tx 1 rx 1 and no daemon remains.
   - The SoC board is on the same boot, with both legs on the recorded command lines, PCM states as at the start and the fault scan at 0.
   - NVM: commits 0 to 6, slots 229/230 to 235/236, `PP_NVM_STAT` `c30000e4` to `c34000e4`, `PP_STAT` `5b000444` to `5b000c44`. `dirty=0` at the end, so the slots hold the as-left, unbound state.
   - Per SAVED_STATE_SNAPSHOT_OWNERSHIP (records `0x60` to `0x7F`), a channel-map write keeps `nvm_pend` at 1 until the next reset. This matters only to a next lane that needs `nvm_pend` 0 or an unchanged slot sequence, which must reset first. The page states the residual but not that consequence (S3).
6. **Docs gates.**
   - All rc 0 at the head in the pinned Markdown environment (`receipts/gates/`): docs_check, check_doc_style, gen_toc `--check`, check_em_dash `--base ec0cc0c1`, check_doc_paths, check_baremetal_only, check_feature_status `--self-test` and `git diff --check`.
   - All 20 tables render with a constant cell count (`receipts/table-cells.txt`).
   - No private host, peer, switch or instrument name appears in the added lines. The PocketBeagle 2 name is public in the owner's amendment.
   - **The findings index needs rows (F1).**

## Findings

**F1 MINOR (Docs):** `docs/findings/README.md:9-22` (the "Current entries" table), and the two new pages.
- **Evidence.** The index lists "current hardware findings", and neither new page appears in it. `451_USB_AUDIO_CAPTURE.md` is linked from no tracked file. `617_DIN_FRAME_COHERENCE_BENCH.md` is linked only from that page, so both are unreachable from any documentation entry point (`receipts/findings-index-links.txt`). The index's first-light row still reads "DIN frame coherence NOT MET, tracked by #617" with no pointer to the bench result. The same gap was raised as a MINOR on PR #616 (the round-2 assignment on #451, 5872564881, item 3) and fixed with a row. The author disclosed the gap; the assignment forbade other doc edits.
- **Impact.** A reader who starts from the documentation cannot find either result: the #617 bench closure evidence, or the #451 USB-path FAIL that matters to any #448 or #117 planning.
- **Required outcome.** One index row per new page, in the index's own ordering. The alternative is a public manager decision that waives the rows, because the assignment's scope decides this edit.
- **Verification.** Every new page is named in `docs/findings/README.md`, and the Markdown gates pass. Four pages already on dev are also unindexed: 387, 394_387, 599_394 and PP_SHADOW_BASELINE. That is pre-existing, out of this PR's scope, and a candidate follow-up Issue.

**S1 SUGGESTION (Conformance, Tests, Docs):** `617_DIN_FRAME_COHERENCE_BENCH.md:16,98-100` and `grade_617.py` `torn()`.
- **Evidence.** The rule reads only valid pattern words, so a frame that mixes one pattern ordinal with zero or idle words is never torn. First light's own torn stop-tail frame (pair 0 zero, pairs 1 to 3 at the last ordinal) scores 0 under it (probe `limit-first-light-stop-tail`).
- **Impact.** "0 in the whole 4,551,624-frame recording" and "the count covers every frame" read wider than the rule. The conclusion stands: the stop-tail frame is graded directly (all zero), and the 778 transition frames carry no pattern word.
- **Suggested change.** Qualify the whole-recording figure as covering "frames with pattern words". Name the edge frames as graded by inspection.

**S2 SUGGESTION (Conformance, Docs):** `617_DIN_FRAME_COHERENCE_BENCH.md:43-56`.
- **Suggested change.** State that VERSION, AEM CRC, entity and ROM CRC are unchanged from `13eda870`. The image-specific identity is then the changed payload CRC plus the manager's install record. Record the `ec0cc0c1` build's payload CRC when it is available.

**S3 SUGGESTION (Robustness, Docs):** `617_DIN_FRAME_COHERENCE_BENCH.md:222-228`.
- **Evidence.** `pend=1` and `PP_STAT` bit 11 are one wire (`PP_NVM_STAT[22]`), not two facts.
- **Suggested change.** State the consequence for the next lane from answer 5: map writes keep `nvm_pend` at 1 until a reset, and `dirty=0` means the slots hold the as-left, unbound state.

**S4 SUGGESTION (Docs):** `451_USB_AUDIO_CAPTURE.md:134-143`.
- **Evidence.** The frame-1,632 low-byte progression (`0x20` to `0xc0`) and the gain reading cannot be re-derived from the public packet, because the raw captures are hashes only.
- **Suggested change.** Publish that frame's eight words in the packet summary.

**Prior public findings on PR #624:** none existed at review start. The thread held only the two review-start notices, so nothing is carried or retained.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (S1 and S2 are suggestions) | #617 acceptance 4 against `grade.json` and the region rule. #451 checklist and amendment against both USB grades. Assignment items 1 to 5 and STOP rules against HANDOFF, events and SoC logs. Identity re-derivation. PR body: no closing keyword, `closingIssuesReferences` empty | R415-1 | `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d` |
| RTL | CLEAN | No RTL in the diff. Checked the pages' RTL claims against the image source: `KL_chan_map_capture.sv:341,569,586` (frame publish), `milan_datapath.sv:1217-1223`, the `13eda870..ec0cc0c1` hdl delta, REGISTER_MAP `0x8D8` law, TIME_SYNC beat row, and `adp_shape_defaults.svh` CSRC table (clusters 0 to 7 on TDM slots 0 to 7) | R415-1 | `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d` |
| Robustness | CLEAN (S3 is a suggestion) | Region edges and transition frames, ordinal wrap, sequence gaps, whole-frame repeat vs tear, beat-phase coverage over 36 beats. Restore: census, maps, controller clock, SoC PCM states. NVM residual against SAVED_STATE_SNAPSHOT_OWNERSHIP records `0x60` to `0x7F` | R415-1 | `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d` |
| Tests | CLEAN (S1 is a suggestion) | The graders as executable evidence. `grade_617.py`, `grade_usb.py` and `decode_capture.py` driven with injected tears, rotations and low-byte offsets (all detected). Alignment sweep 0 to 12. First-light tool blobs byte-identical to the public archive. Hosted contexts at head: executed ones succeeded; `verilator-suites` and `yosys-portability` skipped by the docs-only selector | R415-1 | `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d` |
| Docs | UNCLEAN (F1 MINOR open) | Both pages line by line against the packet. Findings index and inbound links. Eight docs gates in the pinned environment. Rendered table cells. Privacy scan of added lines. Stale-statement search for #617, torn and USB Audio claims in the tree (none falsified) | R415-1 | `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d` |

## Limits

- The raw captures (DIN pcap, DOUT and USB raws) are not public. Every count was re-derived from the published graded outputs and tools, with synthetic probes of those tools; the raw bytes were not re-read. The frame-1,632 words (S4) could not be checked.
- No bench access. Physical calibration, the continuity check and scope measurements are NOT RUN. A field skip is not hardware proof.
- PR #618's own review record was not re-audited. It is cited as merged.
- The full source, Yosys, builder and Verilator banks were not run: the diff is documentation, and the manager runs them.
- The clone was verified clean afterwards (`receipts/clone-integrity.txt`): tree `1538061a`, index equal to HEAD, gitlinks equal to the HEAD tree, no untracked file.

## Pending manager duties

- Decide F1: amend the scope for two index rows, or waive publicly. Then a re-review of the resulting head.
- Build and gate the candidate against live dev, own hosted and local-replica acceptance, and merge only with authorization.
- Close #617 by hand after landing, since the PR says Refs only. Keep #451 open for the USB-path loss, the playback direction, continuity, scope and the calibrated items.
- Optionally, file the pre-existing index gap: four unindexed pages on dev.

R415-1 FINISHED
