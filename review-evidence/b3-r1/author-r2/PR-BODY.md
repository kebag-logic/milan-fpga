[A453] Bench lane B3 on the dev `ec0cc0c1` image: the #617 DIN torn-frame re-run and the #451 capture through the USB Audio device.

Refs #617 (acceptance 4). Refs #451 (capture through the USB Audio device; continuity check). This PR records measurements only; both issues keep their other items.

Head `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb` on `b3-bench-0930`, two commits on dev `ec0cc0c1`, documentation only:

- `docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md` (new): #617 acceptance 4.
- `docs/findings/451_USB_AUDIO_CAPTURE.md` (new): #451 capture through the USB Audio device, and the continuity check.
- `docs/findings/README.md`: one index row per new page, and the first-light row's State points at both (round 2).

No other file changes. Commit `6dfa64a7` records the measurements; commit `a66996aa` answers the round-1 reviews (see [Round 2](#round-2)).

## Verdicts (operator measurements, not review verdicts)

| Item | Verdict | Evidence |
|---|---|---|
| Identity gate | PASS | VERSION `00020060`, AEM CRC `93742dd2`, entity `020000fffe000001`; ENTITY and CONFIGURATION byte-equal to the QSPI AEM bytes; grader 10/10 |
| #617 acceptance 4: 0 torn AAF frames in the #451 DIN capture | PASS | 0 of 3,360,036 playback frames, 0 of 4,551,624 recorded frames (first light: 67.5%) |
| DIN and DOUT slot and channel order | PASS, identity | Every frame, both directions |
| Render path unchanged (DOUT) | PASS | 0 torn, 0 invalid in 3,360,000 frames; first-light discontinuity classes |
| #451 capture through the USB Audio device, order and continuity | FAIL | 0 of 3,600,000 frames pass the pattern rule in each of two 75 s runs; rotating channel order; silent stretches |
| #451 continuity check | NOT RUN | Needs a meter on the unpowered boards |

The whole-recording torn count covers the frames that carry pattern words, which are the playback region's; the edge frames were graded by inspection (round 2, item 4).

## Per-run results

| Run | Direction and capture point | Frames | Torn | Invalid words | Order | Discontinuities | Result |
|---|---|---|---|---|---|---|---|
| `din-long` | DIN, DUT talker stream, 70 s playback | 3,360,036 in the region, 4,551,624 recorded | 0 | 0 | Identity | 36 whole-frame repeats, the same frames in all 8 channels, 93,990-93,993 apart; `SLIP_TDM` +36, skips 0 | PASS |
| `dout-long` | DOUT, McASP0 direct, 70 s | 3,360,000 | 0 | 0 | Identity | 36 beat clusters (net one drop each); 23 underrun clusters, 12 after logged talker lateness | PASS |
| `usb-long` | DOUT, USB Audio card through the bridge, 75 s | 3,600,000 | not gradable | 97.4% of words have a non-zero low byte | In order in 9.6% of frames; 2,833 rotation changes | 327,339 silent frames in 2,420 stretches | FAIL |
| `usb-long2` | Same, repeated | 3,600,000 | not gradable | 97.7% | In order in 11.9%; 238 rotation changes | 3,244 silent frames in 4 stretches | FAIL |

The direct McASP0 path is bit-exact on the same image. So the USB-path loss arises between McASP0 receive and the bench host's capture buffer: in the bridge leg, the USB Audio function or the bench host's USB path. The bridge was not changed, and none of the assignment's STOP conditions occurred.

## Restore

Bridge legs running with the recorded command lines (new process IDs). All 18 stream states unbound and both DUT maps empty; the census equals the start in 33 of 33 entries; DUT control words equal. The controller clock frequency reads back as found and is back on its recorded trajectory. The bench lock is free.

Residual: the method's map and bind edits made the DUT persist its saved state. NVM commits went from 0 to 6 (slots 229/230 to 235/236); at the end the last commit is `VD_OK` and `dirty=0`, so the slots hold the state as left. `nvm_pend` is left at 1: the console's `pend=1` and `PP_STAT` bit 11 are that one wire (`PP_NVM_STAT[22]`, `PP_STAT[11]`). A channel-map write holds it at 1 until the next reset, so the next lane cannot read the durable state until the DUT is reset. First light recorded the same bit.

## Round 2

Executor [A456], documentation only, no bench access, under the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5904487454). It answers [R414-1](https://github.com/kebag-logic/milan-fpga/pull/624#issuecomment-5904469593) and [R415-1](https://github.com/kebag-logic/milan-fpga/pull/624#issuecomment-5904480629). Commit `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb`, one-line subject, no body, no trailers; +51 -14 in three files.

| Item | Source | Change at `a66996aa` |
|---|---|---|
| 1. Findings index | Ruling on R414-1 F1 and R415-1 F1 | `docs/findings/README.md:12-13`: one row per new page, directly after the first-light row they follow up, in file-name order (the placement PR #622 used for its 606 and 608 rows). `:11`: the first-light row's State now points at the `ec0cc0c1` DIN re-run (0 torn) and the USB Audio capture FAIL, keeping its first-light text, as PR #622 did for its row |
| 2. McASP0 receive rate | R414-1 F2 | `451_USB_AUDIO_CAPTURE.md:126-127`: 250.7 becomes 250.0 periods/s. `:129-133`: the bracket, 18,942 and 18,957 periods in 75.78 s and 75.83 s, between the same uptime read of the before and after status logs; 47,992 and 47,999 frames/s. The packet `HANDOFF.md` step 5 is corrected too |
| 3. Packet locator | R414-1 F3 | `617_DIN_FRAME_COHERENCE_BENCH.md:275-278` and `451_USB_AUDIO_CAPTURE.md:216-219` name `review-evidence/b3-r1/author/` on branch `b3-review-evidence`. The five grading-tool hashes on the pages match the files there |
| 4. Whole-recording torn count | R415-1 S1 | `617_DIN_FRAME_COHERENCE_BENCH.md:107-112`: the rule reads only pattern words, so the count covers the frames that carry them, which are the region's. `:158-161`: frame 45,587 and the 777 transition frames after the region were graded by inspection |
| 5. Identity chain | R415-1 S2 | `617_DIN_FRAME_COHERENCE_BENCH.md:54-58`: VERSION, AEM CRC32, entity ID and ROM CRC32 are unchanged from `13eda870`; only the QSPI payload CRC32 differs. `:61-63`: the lane packet does not hold the `ec0cc0c1` build's own payload CRC32, so `d178f19a` stays recorded as read |
| 6. `nvm_pend` | R415-1 S3 | `617_DIN_FRAME_COHERENCE_BENCH.md:239-252`: `pend=1` and `PP_STAT` bit 11 are one wire; a channel-map write holds it until reset, so a next lane that needs the durable reading must reset the DUT first |
| 7. Frame 1,632 | R415-1 S4 | Packet only: `summary/summary.json` and `summary/usb-long-frame-1632.json` publish the eight words, read from the raw `usb-long` capture after its SHA-256 check: `016ec820 026ec838 036ec850 046ec868 056ec878 066ec890 076ec8a8 086ec8c0`. One ordinal, `0x6ec8`, in slot order, low bytes `0x20` to `0xc0`, as the page states |

**Measurement tables.** Every table in `617_DIN_FRAME_COHERENCE_BENCH.md`, 12 of 12, is byte-identical to `6dfa64a7`. In `451_USB_AUDIO_CAPTURE.md` 7 of 8 are byte-identical, including the generated `usb-runs` and `usb-detail` tables. The eighth, the bridge-side table, differs only in item 2's two rate cells: 2 bytes, `7` to `0`, by `cmp -l`. The index table changes by item 1.

**Corrected packet files**, for publication beside the round-1 packet: `HANDOFF.md` with the rate correction, `summary/summary.json` with each USB run's McASP0 bracket and the frame-1,632 words, `summary/usb-long-frame-1632.json`, `tools/usb_frame_words.py`, `receipts/mcasp-rx-rate.txt`, and `MANIFEST.sha256` (169 entries: the round-1 manifest with two files re-hashed and three added).

## Validation at `a66996aa`

All rc 0, unpiped, from the physical `/data` lane path; the Markdown gates with the pinned Markdown environment:

- `scripts/docs_check.py`: 0 findings.
- `scripts/check_doc_style.py`.
- `scripts/gen_toc.py --check`.
- `scripts/check_em_dash.py --base ec0cc0c1`: 0 findings over 512 added lines in 3 pages.
- `scripts/check_doc_paths.py`: 860 paths.
- `scripts/ci_scope.py --selftest`.
- `scripts/check_baremetal_only.py --check`.
- `scripts/check_feature_status.py --self-test`: 46/46.
- `git diff --check`, `git diff --check ec0cc0c1 HEAD` and `git diff --check 6dfa64a7 HEAD`.

Every table in the three pages has a constant cell count, rendered and in the source. The 9 relative links added in round 2 reach their targets, anchors included. The McASP0 rate re-derives from the published status logs with the reviewer's `mcasp_rx_rate.py`.

## Open questions

1. The assignment keeps the measurement tables byte-identical and corrects the McASP0 rate, which sits in the bridge-side table. Only that table's two rate cells changed. Every other table is byte-identical.
2. #451's capture through the USB Audio device fails. Locating the loss needs a change on the SoC board or the bench host, for example a capture with the bridge's rate conversion off. That is outside this lane.
3. #451's playback direction through the USB Audio device was not assigned, and remains NOT RUN.

The lane packet holds the tools, the redacted per-action evidence, the gate outputs and the raw-artifact index. Its redacted copy is `review-evidence/b3-r1/author/` on branch `b3-review-evidence`; the round-2 corrections above are for publication beside it.
