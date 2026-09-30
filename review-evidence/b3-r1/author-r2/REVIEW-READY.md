[A456] REVIEW READY
Commit: `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb` on `b3-bench-0930`, one commit on `6dfa64a7` (local; not pushed). One-line subject, no body, no trailers.
Changed: documentation only, +51 -14 in three files, under the round-2 assignment https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5904487454.
1. Index (ruling on R414-1 F1 and R415-1 F1): `docs/findings/README.md:12-13` add one row per new page, directly after the first-light row, in file-name order. `:11`: the first-light row's State now points at the `ec0cc0c1` DIN re-run (0 torn) and the USB Audio capture FAIL.
2. R414-1 F2: `docs/findings/451_USB_AUDIO_CAPTURE.md:126-127` McASP0 receive 250.0 periods/s (was 250.7). `:129-133` state the consistent bracket: 18,942 and 18,957 periods in 75.78 s and 75.83 s, between the same uptime read of the before and after status logs; 47,992 and 47,999 frames/s. The packet `HANDOFF.md` step 5 is corrected too.
3. R414-1 F3: `docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md:275-278` and `docs/findings/451_USB_AUDIO_CAPTURE.md:216-219` name `review-evidence/b3-r1/author/` on branch `b3-review-evidence`. The five grading-tool hashes on the pages match the files there.
4. R415-1 S1: `617_DIN_FRAME_COHERENCE_BENCH.md:107-112`: the whole-recording count covers the frames with pattern words, which are the region's. `:158-161`: frame 45,587 and the 777 transition frames are graded by inspection.
5. R415-1 S2: `617_DIN_FRAME_COHERENCE_BENCH.md:54-58`: VERSION, AEM CRC32, entity ID and ROM CRC32 are unchanged from `13eda870`; only the QSPI payload CRC32 differs. `:61-63`: the packet does not hold the `ec0cc0c1` build's own payload CRC32, so `d178f19a` stays recorded as read.
6. R415-1 S3: `617_DIN_FRAME_COHERENCE_BENCH.md:239-252`: `pend=1` and `PP_STAT` bit 11 are one wire (`PP_NVM_STAT[22]`, `PP_STAT[11]`). A channel-map write holds it until reset, so a next lane that needs the durable reading must reset the DUT first.
7. R415-1 S4 (packet only): `summary/summary.json` and `summary/usb-long-frame-1632.json` carry frame 1,632's eight words, read from the raw `usb-long` capture after its SHA-256 check (`7995b44a…d7ca`): `016ec820 026ec838 036ec850 046ec868 056ec878 066ec890 076ec8a8 086ec8c0`. The packet's updated `MANIFEST.sha256` has 169 entries.
Validation: at `a66996aa`, all rc 0, unpiped, from the physical `/data` lane path.
- Pinned Markdown environment: `docs_check.py` (0 findings), `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base ec0cc0c1` (0 findings over 512 added lines), `check_doc_paths.py` (860 paths).
- Also `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test` (46/46), and `git diff --check` (plain, against `ec0cc0c1` and against `6dfa64a7`).
- Table cell counts are constant in all three pages, rendered and in the source.
- The 9 relative links added in round 2 reach their targets, anchors included.
- The reviewer's `mcasp_rx_rate.py` reproduces 249.96 and 249.99 periods/s from the published status logs.
Measurement tables: in `617_DIN_FRAME_COHERENCE_BENCH.md`, 12 of 12 tables are byte-identical to `6dfa64a7`. In `451_USB_AUDIO_CAPTURE.md`, 7 of 8 are byte-identical. The eighth, the bridge-side table, differs only in item 2's two rate cells: 2 bytes, `7` to `0`, by `cmp -l`. The check is `diff <(git show 6dfa64a7:<page> | grep '^|') <(git show a66996aa:<page> | grep '^|')`: empty for the #617 page, and the two rate lines for the #451 page.
Acceptance criteria: assignment items 1 to 7 are met as above. Every measured figure and verdict is unchanged, except the corrected McASP0 rate.
Open risks/questions:
- The McASP0 rate sits in a table, so correcting it is the one table change. Item 2 requires it.
- The corrected packet files (handoff, summary, frame-1,632 words, rate receipt, extraction tool, manifest) are in the round-2 packet, for publication beside `review-evidence/b3-r1/author/`.
- The private-name scan of the round-2 packet, the commit diff and the commit subject found 0 hits.
- No push, PR edit, bench, NAS or hardware action.
