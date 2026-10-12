[A603] Bench lane B16 for #629: the reference peer's loopback; B16b: Direction B's tone through the DUT and B0; B16c: B-CRF and B-AAF; rounds 2 and 3: every figure checked against its receipt

Title, as both reviews ask (for the manager): Record bench lanes B16, B16b and B16c: Direction B's B0 graded, and B-CRF and B-AAF graded at the path's floor (#629)

Refs #629.

Five commits on dev `c20c85bd`, all docs only:

- `694d7da6` adds the dated section "Dev 5603c353, 2026-10-12: lane B16" to `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, with its Contents line and the introduction's pointer.
- `0d4ff919` adds the B16b part to that section (ten `B16b:` subsections, the Contents line and the pointers).
- `e20fd282` adds the B16c part (eleven `B16c:` subsections, the Contents line and the pointers).
- `35e332b6` answers the two reviews: it corrects figures against their receipts and bounds B0's attribution by the taps. It states lane B6's four terms, and adds the subsection "B16, round 2: reduced receipts".
- `0782c55f` answers the next two: it corrects the figures a new figures check found off, and adds the subsection "B16, round 3: figures check".

Each also updates the lane's row in `docs/findings/README.md`. No code, RTL or firmware changes.

## B16 result

On the dev `5603c353` image, after the identity gate passed, the lane tried the assignment's positive reference: the reference peer's own listener bound to its own talker under the binding rule, with lane B15's known tone played into the peer's talker inputs through the same authorised source.

- The loopback did not form, in two runs. The bind answered SUCCESS, but the peer's listener never learned its own talker's stream ID or destination. The talker's connection count stayed 0, the talker sent no PDU on either link, and the peer's digital output read exact zero at the external capture.
- The second run's tap covered the bind. 99.6 ms after the bind command, the peer sent PROBE_TX (IEEE 1722.1's CONNECT_TX) for its own talker onto the network, and again 200 ms later. Nothing answered in the rest of the capture, 49.6 s, so the stream never started.
- The tone source, read only: its playback reaches the outputs the documented wiring uses at 0 dB, as lane B15 read, and also a second pair of outputs that lane B15 read silent.

Under the assignment's step 2 that was a STOP.

## B16b result

After the manager's ruling, the lane ran lane B15's four-point capture with the DUT's listener bound to the peer's talker, then step 4.

- The tone is present in the peer's own talker stream, (a): 997 Hz on channel 0 and 9,973 Hz on channel 1. It is equal on the DUT's link, (b). At the DUT's TDM output, (c), it equals both sample for sample in all three 10 s runs (480,000 of 480,000 frames) and over the 34.1 s the taps cover in B0. The positive control at the external capture, (d), lane B6's loop through the DUT's talker and the peer's listener, is present.
- B0, the DUT on INTERNAL with both of the peer's talkers bound, 300 s at McASP0: THD+N -123.95 dB at 997 Hz and -122.80 dB at 9,973 Hz (median), SNR the same, 0 discontinuities, 0.0000 ppm. The floor blocks' medians are -123.98 dB and -123.95 dB. 131 of the 300 blocks at the TDM output sit off the floor, with no discontinuity.
- Inside the 34.1 s the taps cover, every impairment is already in the peer's talker stream, sample for sample: the path's floor, 23 of the 131 degraded blocks, and in the earlier runs an offset of +6.94 to +6.96 ppm. The network and the DUT add none there. The other 108 degraded blocks lie beyond the taps and are assigned upstream by inference only. No DUT change was needed.
- The tone source's clock setting changed during the lane, outside it (read only). With it the tone at (a) stepped from +6.94 to +6.96 ppm and -14.1353 dBFS to 0.000 ppm and -14.1035 dBFS.
- B-CRF and B-AAF did not run, and the lane stopped for a decision. As found, the peer's clock follows the DUT's CRF talker, so following the peer would have the DUT follow its own clock through the peer. The clock-source rule forbids setting the peer, the talker in both cases.

## B16c result

After the manager's second ruling, which allows setting the reference peer's clock source to INTERNAL for these two cases only, each read back and restored:

- Each case set the peer's CLOCK_DOMAIN to INTERNAL and read it back. It bound the peer's CRF and AAF talkers to the DUT under the binding rule, then set the DUT's CLOCK_DOMAIN to its CRF source (B-CRF) or its AAF source (B-AAF) and read it back. It recorded 300 s at the DUT's TDM output on McASP0 with the four-point capture. It then put the DUT back on INTERNAL, undid the binds and returned the peer to its CRF input, as found, each read back.
- B-CRF: servo LOCKED 2.585 to 3.161 s after the set and at all 596 polls of the window. THD+N -123.98 dB at 997 Hz and -123.97 dB at 9,973 Hz (median), with all 300 one-second blocks at the path's floor, 0 discontinuities and 0.0000 ppm.
- B-AAF: servo LOCKED 6.602 to 7.180 s after the set and at all 596 polls. The AAF meter held 0 history restarts, with a largest deviation of 30 ns. THD+N -123.98 dB and -123.97 dB, all 300 blocks at the floor, 0 discontinuities.
- Against lane B6's four pass terms, both cases meet three: LOCKED, the counted ratio within 0.5 ppm (0 net steps, below 0.07 ppm), and 0 listener discontinuities. The fourth, the timed ratio, was NOT RUN: this mode ran no timing sampler. No recorded decision replaces it.
- In both cases the TDM output equals the received stream sample for sample over the taps' 34 s. The positive control shows 0 discontinuities and 0 net steps between the DUT's TDM clock and the peer's output in 14.58 million frames, and `SLIP_TDM` stays 0. `SLIP_LB` stepped only before LOCKED; #645's slip after LOCKED did not repeat.
- No stage loses the tone, so no DUT change was needed.
- The new run mode was dry-run offline against stand-ins first: 8 of 8 scenarios, including a deadline mid-window and a controller agent ending mid-case.

The bench was restored and read back at each lane's end: census 45 of 46 equal, the other entry the DUT's live propagation delay, and counters moved only as the method implies. Every tool control passed before any grade.

## Validation

At each head every gate was rc 0, unpiped, from the physical worktree path:

- in the pinned Markdown environment: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27` (0 findings) and `check_doc_paths.py`;
- `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, and `check_feature_status.py --self-test`;
- `git diff --check` and `git diff --check c20c85bd HEAD`.

## #629

Direction B's bench quality metric is now graded for both followed sources, B-CRF and B-AAF, and with the DUT on INTERNAL. Lane B6's timed ratio for B-CRF and B-AAF was not run. Direction B's INTERNAL mismatch control did not run: B0 had the peer following the DUT, and the exception covers B-CRF and B-AAF only. #645 stays open, so #629 stays open.

## Round 2

Documents only, after the two reviews; nothing on the bench was touched. Each item of the round's assignment:

1. **Figures.** B0's floor medians are -123.98 dB (997 Hz) and -123.95 dB (9,973 Hz). The degraded runs are 0 to 18, 28 to 31, 43 to 44, 46 to 54 and eleven later runs. The B0 recording starts at about 06:38:05.2: the capture command at 06:38:03.2 plus the board's 2 s of playback, about 26 s after the binds. The same 2 s lead, in the earlier `pts2` run, is corrected too.
2. **Lane B6's four terms** are stated for B-CRF and B-AAF: three met, the timed ratio NOT RUN. The counted ratio stands in as evidence only, and no recorded decision replaces the term.
3. **Attribution.** 131 stays the count of degraded blocks at the TDM output. 23 of them lie inside the taps' overlap and are shown in the peer's talker stream directly; the other 108 are labelled inference. This applies in the findings, the index and this body.
4. **Reduced receipts**, neutral and bound to the retained raw hashes, with the extraction commands and 6 of 6 tool controls:
   - each B16c case's console poll: extrema per span, and every `SLIP_LB` step with its two polls and servo states;
   - the tone source's meters and state comparisons;
   - B0's overlap.

   Every figure they carry reproduces. Two statements were narrowed: two of B16b's four differing source entries differ only in which messages were caught, and the source's other outputs read no higher than -135.2 dBFS.
5. **The first counter mark** in B16c is now stated as 20 s after the DUT's set, about 6 s before the window.

At `35e332b6` all 14 gates are rc 0, as listed under Validation (`check_em_dash.py`: 0 findings over 3,179 added lines).

## Round 3

Documents only, after the reviews R624-2 and R625-2; nothing on the bench was touched. Each item of the round's assignment:

1. **A figures check**, `tools/check_b16_figures.py` in the lane packet, not the tree. It holds one row per quoted figure in lane B16's section, in the page's introduction and Contents entry on lane B16, and in lane B16's part of the findings index row: the document line, the figure as shown, the receipt, the key and the displayed precision.
   - It recomputes each figure from its receipt and fails on any mismatch after rounding. Receipts are read as exact decimals and rounded half up; clock times are cut to the last digit shown.
   - It also reads every number, time, hash and number word in that text, and fails on any that neither a row nor a named identifier category covers.
   - At `0782c55f`: 1,610 rows, all equal to their receipts; 1,815 tokens, 205 in identifier categories, none uncovered.
   - Its output, `r3/figures-rows.tsv` and `r3/figures-coverage.tsv`, is published as its receipt and reproduces byte-equal.
   - Its controls, `controls/r3-controls.json`, pass 5 of 5 on altered copies: a figure changed on the page, a receipt value changed, a figure added without a row, a row at the wrong line, and a clock time rounded instead of cut.
2. **R625-2-F1**: the exact replacement, "At (a), medians are -123.98/-123.97 dB for B-CRF and -123.98/-123.98 dB for B-AAF (997/9,973 Hz); every worst block is -123.93 dB."
3. **R624-2-F1**: the positive control's floor counts cover only blocks wholly inside the playback: all 303 in `b0-2`, `bcrf` and `baaf`, and 11 of 13 in `pts2` (blocks 6 and 12 hold its repeats). Blocks 0 and 1 precede the playback and block 2 holds its start. The same applies to the taps in `pts2`: all 15 blocks wholly inside the playback.
4. **R624-2-F2**: each LOCKED bracket runs from the start of the last poll that read ACQUIRE, the poll its state read falls in, to the end of the first that read LOCKED: 2.585 to 3.161 s and 6.602 to 7.180 s.
5. **R624-2-R1 and R2**: both source-state statements are narrowed to the entries the reads both hold (1,255; 618 and 668), and the five steps before the set are attributed only as far as the receipts show, with the reviewers' wording. R3's wording is in the "#629" section above.

The check found more figures off its receipts, each corrected on the page and listed in its round 3 table:

- clock times under one rule, cut to the last digit shown, in lanes B16, B16b and B16c, and lane B16's tone start, now the first status read less the frames played;
- `loop2`'s "remaining 49 s", now 49.6 s;
- the drift and offset before the tone source's change, now +3.00 and +3.01 frames, and +6.94 to +6.96 ppm;
- B16c's decoded span at (d), now 303.8 s and 303.9 s, and the peer's rate, now +10.59 to +10.65 ppm.

Statements with no retained receipt were narrowed or cited:

- the resume times, now the first bench action;
- lane B15's `pts1` flags, now only what lane B15's section records;
- lane B16b's underruns, cited to the operator's record because that log was overwritten;
- six number words.

A neutral receipt of the two retained playback logs, `r3/playback-logs.json`, backs "no underrun" in lanes B16 and B16c. The optional servo-status limit (R624-2-S1) is added. The census wording suggestion (R624-2-S2, R625-2-S1) is not taken.

The check's files are pinned here and in the packet's `MANIFEST.sha256`. The page cannot hold the check's own hash, because the check holds the page's figures:

| Packet file | Bytes | SHA-256 |
|---|---|---|
| `tools/check_b16_figures.py` | 179,675 | `13d7a0deb20ca5b16c478491c1499de37864693545a70d0c876ef7e9288d1ea3` |
| `r3/figures-rows.tsv` | 104,749 | `459a55780b5df8817bddfc4f46c3a986c8ff0101464e5c9768a35527a3a1ce7b` |
| `r3/figures-coverage.tsv` | 11,186 | `1eb17bab1279870b3b672fe7115b46ff8d3aa62e3001477e85c586579a75a94e` |
| `tools/r3_figures_build.py` (authoring aid) | 3,736 | `ec0e1ce6baa09891204687d097f7bca54f9a58f7d781a12a4cc488023b1e5519` |
| `tools/r3_figures_spec.py` (authoring aid) | 141,228 | `6338e6fd1a63ccd0d9022942863e491c942dc66d08a6194d9539a9ced54b57fa` |

The other round 3 files, `tools/r3_check_controls.py`, `controls/r3-controls.json`, `tools/r3_playback_logs.py` and `r3/playback-logs.json`, are hashed on the page.

At `0782c55f` all 14 gates are rc 0, as listed under Validation (`check_em_dash.py`: 0 findings over 3,306 added lines).

