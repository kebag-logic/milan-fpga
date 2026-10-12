[A603] Bench lane B16 for #629: the reference peer's loopback; B16b: Direction B's tone through the DUT and B0; B16c: B-CRF and B-AAF; rounds 2 to 6: every figure checked against its receipt, every digit accounted for, an identifier counted only before a closed list of followers, and where the packet is published

Title, as both reviews ask (for the manager): Record bench lanes B16, B16b and B16c: Direction B's B0 graded, and B-CRF and B-AAF graded at the path's floor (#629)

Refs #629.

Nine commits on dev `c20c85bd`, all docs only:

- `694d7da6` adds the dated section "Dev 5603c353, 2026-10-12: lane B16" to `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, with its Contents line and the introduction's pointer.
- `0d4ff919` adds the B16b part to that section (ten `B16b:` subsections, the Contents line and the pointers).
- `e20fd282` adds the B16c part (eleven `B16c:` subsections, the Contents line and the pointers).
- `35e332b6` answers the two reviews: it corrects figures against their receipts and bounds B0's attribution by the taps. It states lane B6's four terms, and adds the subsection "B16, round 2: reduced receipts".
- `0782c55f` answers the next two: it corrects the figures a new figures check found off, and adds the subsection "B16, round 3: figures check".
- `61ae8641` answers the next two: it states where the lane packet is published, narrows the check's exemptions to identifiers, and adds the subsection "B16, round 4: packet and coverage".
- `f60132ca` answers the next two: the check now accounts for every digit, and the commit adds the subsection "B16, round 5: every digit" and states the rounds 3 and 4 checks as they were.
- `36190193` states on the page the check's quoted-mention rule and every separator it reads between a number and its unit.
- `e91a62ee` answers the next two: the check reads the page as rendered and counts an identifier only before a closed list of what may follow it, a figure for several cases is recomputed from each case's receipt, the packet's rounds 4 and 5 are mapped, the covered text is reworded within its lines where the list refused it, and the commit adds the subsection "B16, round 6: the closed list".

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

The bench was restored and read back at each lane's end: census 44 of 45 reads equal, the census's start record aside, the other read the DUT's live propagation delay, and counters moved only as the method implies. Every tool control passed before any grade.

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
   - It also read the numbers, times, hashes and number words its token pattern finds in that text, and failed on any that neither a row nor a named identifier category covered. A number written in a form the pattern does not read escaped it; round 5 closes that.
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

## Round 4

Documents only, after the reviews R624-3 and R625-3; nothing on the bench was touched. Each item of the round's assignment:

1. **Where the packet is (R624-3-F1).** Lane B16's section now says, in "B16: artifact hashes", as lane B15's does:
   - the evidence branch `629-b16-review-evidence`, pinned at `b84584e4ccb069248909f0fdeb7f8b72a1c41ae4`;
   - the packet label `629-b16-a603` mapped to `review-evidence/629-b16-r1/author-r1/` (lanes B16, B16b and B16c, page at `e20fd282`), `author-r2/` (round 2, `35e332b6`) and `author-r3/` (round 3, `0782c55f`). The round-1 directory is `author-r1/`, not `author/`. Round 4's packet follows as `author-r4/`;
   - `MANIFEST.json` there, SHA-256 `8d417d54b13a264484bfcb0b69f8a643e5cd3bf2819294cea201242a2f67f034`, 1,680 entries. Each entry gives a file's original hash (the lane packet's) beside its published hash, with a `path_redacted` flag, and the hashes differ exactly where the flag is set. 27 author files are path-redacted (1, 9 and 17 by round): gate logs, gate results and `tools/gates_r2.py`;
   - no hash row on the page names a redacted file. All 66 packet-file rows at `0782c55f` equal the original hash, the published hash and the published file in `author-r3/`, by size and SHA-256.

   `tools/r4_evidence_receipt.py` reads all of it from the repository's object store into `r4/evidence-receipt.json`, and each of the paragraph's figures, hashes and commits has a row reading that receipt.
2. **Coverage (R625-3-F1).** The check no longer exempts a link or a quoted phrase as a whole. Its categories are now identifiers only, each bound to its keyword: commit names (listed), clause numbers, descriptor, channel, step, round and list-item indices, the packet's label and branch name, and a link's target (URL or anchor, not its label).
   - Every other category is gone. Its tokens now have rows (the tone frequencies, the block length, the comparison's bit width, the decode's frame step, the one-LSB floor, the lane's limit on a locked action, the four capture points, dates in link labels, each quoted reworded phrase) or were reworded (seventeen phrases that state no figure).
   - A guard under the categories: a token followed by a unit (dB, dBFS, ppm, %, s, Hz, frames, blocks, polls, bits, LSB and the like) was a measurement, and only a row could claim it, whatever category matched. It read only tokens, with at most a single space, non-breaking space or hyphen before the unit; round 5 closes the forms it missed.
   - Its tokens now include 40-character commit names and the number words for tens.
   - At `61ae8641`: 1,727 rows, all equal to their receipts; 1,874 tokens, 147 in identifier categories, 0 uncovered. `r4/figures-rows.tsv` and `r4/figures-coverage.tsv` reproduce byte-equal, and `tools/r4_figures_build.py` regenerates the check byte for byte from `tools/r4_figures_spec.py`.
   - Its controls, `controls/r4-controls.json`, pass 8 of 8. Round 3's five are there with their code unchanged, and round 3's own runner passes 5 of 5 against the new check. The three new ones are R625-3's two forms, quoted and as a link label, each with a unitless number in the same form, and a category planted to match every token with the figure in plain text. Each fails the check and names the figure UNCOVERED; the planted case names it a measurement.
   - The same runner against round 3's check (`13d7a0de...`) and page: round 3's five pass and the three new fail (`controls/r4-controls-on-r3-check.json`). So each new control can fail for the defect it targets.
   - R625-3's own probe, run unchanged against the new check, detects 7 of 7, its quoted and linked forms included (`r4/r625-3-probe-rerun.json`).
3. **R625-3-S1, taken.** The five census statements in lane B16's section read "44 of 45 reads equal, the census's start record aside". Each row recomputes both counts from the two census files with `census_cmp.py`'s rule, and checks them against the comparison file's counts less the start record.

The check's files are pinned here and in the packet's `MANIFEST.sha256`, not on the page:

| Packet file | Bytes | SHA-256 |
|---|---|---|
| `tools/check_b16_figures.py` | 192,835 | `d2b51f85b10f33427396044703f20820df64b7b57601fe25f498a44e28f17edd` |
| `r4/figures-rows.tsv` | 113,578 | `fd7eef805484d5827f899e1a35b913f84f7d113879eda1e314fd0ba478c96927` |
| `r4/figures-coverage.tsv` | 8,647 | `a184d9ab7f31102695a67b1846d2928dca6de9441f3254ba6411e0c86844c1c1` |
| `tools/r4_figures_build.py` (authoring aid) | 4,673 | `ba3085a75a99d17009fda6580adf90887db21c8c64f50144ce8d6fd173688de0` |
| `tools/r4_figures_spec.py` (authoring aid) | 152,849 | `ee2fef18f24849f255f90743bfa8375dda42855a8ca00297a5f3f45a6729c18d` |
| `r4/r625-3-probe-rerun.json` | 4,201 | `0dcf575d7ddb381d3353ac4b959992dacee8b5fd923baa5c0a0a1b8bf67ac8db` |
| `controls/r4-controls-on-r3-check.json` | 3,576 | `90cba016cf3d19974fc88efb86f98226ef2c4d712cf7ebf2b361c9cc96b545f0` |

The other round 4 files, `tools/r4_evidence_receipt.py`, `r4/evidence-receipt.json`, `tools/r4_check_controls.py`, `controls/r4-controls.json` and `controls/r4-rerun-r3-controls.json`, are hashed on the page.

At `61ae8641` all 14 gates are rc 0, as listed under Validation (`check_em_dash.py`: 0 findings over 3,427 added lines).

## Round 5

Documents only, after the reviews R624-4 and R625-4, each NEGATIVE on one MINOR about the check's coverage. Nothing on the bench was touched and no figure on the page changed. Each item of the round's assignment:

1. **Every digit (R624-4-F1, R625-4-F1).** The check no longer decides coverage from tokens. Every digit of its text, any Unicode digit or numeral, must lie in one of two places:
   - a figure that a row claims and recomputes from its receipt;
   - an identifier that a category binds to its keyword in the same sentence. The text is read in blocks of consecutive non-blank lines, so a keyword binds across a line break, and a match that crosses a table cell or a sentence's end counts for nothing.

   Any other digit is UNCOVERED, named with its line, its spelling (sign, leading point and exponent kept) and the text around it. The token pattern is unchanged and now only finds row candidates. A spelling it does not read, such as `26s`, `.5 ppm` or `7e2 ppm`, can never be claimed, so it always fails. A row's figure must also be the whole number written there, so a figure after a minus sign the pattern does not read now fails its row.
   - The categories, each with its keyword or test:
     - commit names, listed, in code or after "Dev";
     - IEEE 1722.1 and Milan v1.2 Table 5.4;
     - descriptor, channel, step and round indices after their keyword, and a second channel index after "and" or "to", or a second step or round index after "and"; across a line break. R625-4's continuation is now bound to "Channels", and the line-start exemption is gone;
     - list-item indices only in a real ordered list, at their place in it;
     - closed lists of names: lanes and cases, reviews and findings, the operator, the issue numbers it cites, McASP0, SHA-256, CRC32, the entity name and serial number, the Python command, two manifest field names, the packet's label, branch and published directories, and the page's markers;
     - a path in code that names a packet file or directory, or a raw file the packet lists;
     - a link target that resolves: an anchor of a heading on the page, or an issue, pull request or comment of the repository.
   - At `36190193`: 1,749 rows, all equal to their receipts; 13,209 digits, 11,037 in claimed figures, 2,172 in 1,098 bound identifiers, 0 uncovered.
2. **A measurement is never an identifier.** A number followed by a unit is a measurement, and only a row covers its digits, whatever stands between number and unit. That can be nothing, or any run of spaces or line breaks (non-breaking, thin and zero-width ones too). It can be a soft, non-breaking or plain hyphen, emphasis or code marks, a backslash, a double quote, an opening bracket, or an HTML entity, tag or comment. Units are read in either case; the list is `MEASURE` in the check, and "zero" before a unit counts as a number. This held only for the units that list spells: R624-5 and R625-5 found a unit written as a word, or set beyond a comment over a line break, passing after an identifier; Round 6 closes both. Two rules are stated on the page:
   - A link target that resolves is an address, not text: an anchor's hyphens stand for its heading's spaces and punctuation, and the heading is read where it stands.
   - A number quoted on its own (`"37"`) is a mention: its closing quote does not join it to a unit. No category takes a quoted number, so it needs a row either way. This keeps round 4's quoted control green with its code unchanged.
3. **Controls.** `tools/r5_check_controls.py` passes 22 of 22 (`controls/r5-controls.json`). The 8 controls of rounds 3 and 4 run first with their code unchanged. Each control below fails the check and names its figure in its spelling.
   - The required forms, each on the attribution row R625-3 used: `26s`, `10dB`, `300ms`, `.5 ppm`, `-.25 ppm`, `7e2 ppm` and `CLOCK_DOMAIN 7  ppm` (double space).
   - R625-4's unbound continuation, applied where the continuation is, because a table row cannot hold a line break.
   - A non-breaking space and a hyphen before the unit.
   - A Unicode minus before a figure that a row claims.
   - A cited path that names no packet file, and an anchor that names no heading.
   - A category planted to match every number, with a figure and its unit added. The figure is the only thing UNCOVERED, named a measurement.
   - Round 3's runner and round 4's, unchanged, pass 5 of 5 and 8 of 8 against the new check (`controls/r5-rerun-r3-controls.json`, `controls/r5-rerun-r4-controls.json`).
   - The new runner against round 4's published check (`d2b51f85...`) and the page at `61ae8641` (`controls/r5-controls-on-r4-check.json`): the 8 earlier controls pass, and 11 of the 14 new ones fail. The 3 that pass, a non-breaking space, a hyphen and the planted category, are forms round 4's guard already read. Round 4's check passes its own page in that tree. So each other new control can fail for the defect it targets.
   - The reviews' probes, unchanged, copied into `tools/review-probes/` with their published SHA-256, detect every form they insert: R624-4's `probe_escape_forms.py` 8 of 8, R625-4's `probe_coverage.py` 12 of 12 (exit 0), and R625-3's `probe_figure_coverage.py` 7 of 7 (`r5/r624-4-probe-rerun.json`, `r5/r625-4-probe-rerun.json`, `r5/r625-3-probe-rerun.json`, from `tools/r5_probe_reruns.py`).
   - 36 further escape forms, each detected (`r5/self-probes.json`, from `tools/r5_self_probes.py`): a descriptor index set off from its unit by a line break, bold, code, brackets, an HTML entity or comment, a thin, zero-width or escaped space, or with the unit in capitals; identifiers glued to or set before a unit; a fullwidth digit, a vulgar fraction, a superscript, a Unicode minus, a quoted mention, number words, a hex word, a slash fraction and a range; a path, an anchor, a link off the repository and a page marker that name nothing real; and a line inside a paragraph that starts with a number.
4. **Texts.** The page states the rule as it now is in "B16, round 5: every digit". Round 3's and round 4's paragraphs now describe their checks as they were: what the token pattern found, and the guard's single separator. The introduction, the Contents entry, the index row and this body point to round 5. R624-4-S1 is taken: the section's opening paragraph points to rounds 2 to 5.

The check now writes a receipt equal to the row above's as `^`, and `parse_rows` restores it. This keeps the check under the packet's 200 KB file limit; the rows output is unchanged in form. `tools/r5_figures_build.py` regenerates the check byte for byte from `tools/r5_figures_spec.py`.

The check's files are pinned here and in the packet's `MANIFEST.sha256`, not on the page:

| Packet file | Bytes | SHA-256 |
|---|---|---|
| `tools/check_b16_figures.py` | 180,489 | `2641412c62d2c55c800b96dde53eecbd3983ec7d251dbab58eeda90312d73814` |
| `r5/figures-rows.tsv` | 115,411 | `77ac9643dd311bf001d58f1e8cb2e4f4b70355bdb58017f81533e2b1a8013b11` |
| `r5/figures-coverage.tsv` | 71,176 | `613dea0c155e54b4abdf0b757dbc3986d51bbadcc6f9faf324cc83a682fe2ed9` |
| `tools/r5_figures_build.py` (authoring aid) | 4,767 | `b7d95befe349e1f15ea4cc3ef027afd3e78ece53a80a347d7a86e4d0509af0e6` |
| `tools/r5_figures_spec.py` (authoring aid) | 155,187 | `725dbe2c0d40bce8de478b3a64300d7387bb643dad78d77b1ec09d7883dd8565` |
| `tools/r5_probe_reruns.py` | 3,526 | `893b97d6a71c6a78df33af38ecbad2c7ce3d1f21400b9a930869cd8aeb3a84c2` |
| `r5/r624-4-probe-rerun.json` | 4,754 | `45e4e2043b8629755d257b2a3024270470638a43a98660da625203d2801f0034` |
| `r5/r625-4-probe-rerun.json` | 12,204 | `cf07527318d74e6cf844154d2da5878c8e0fa98983b896729a93598ec2680bda` |
| `r5/r625-3-probe-rerun.json` | 4,978 | `5c756dd1006338951709df7bffac24cf4aa6a6e169892105e7261382f464afb7` |
| `tools/r5_self_probes.py` | 6,083 | `c936663d25276c463a946d50b5dbeb59dd80cce27c83e22bf53b38d61c9d981b` |
| `r5/self-probes.json` | 11,617 | `f8d34c0d5a6c17a29e73525ef096d0ffadb32f1f6e53c574123fb1ff9cc77e1c` |

The other round 5 files, `tools/r5_check_controls.py`, `controls/r5-controls.json`, `controls/r5-rerun-r3-controls.json`, `controls/r5-rerun-r4-controls.json` and `controls/r5-controls-on-r4-check.json`, are hashed on the page.

At `36190193` all 14 gates are rc 0, as listed under Validation (`check_em_dash.py`: 0 findings over 3,565 added lines).

## Round 6

Documents only, after the reviews R624-5 (three MINOR, one residue) and R625-5 (one MINOR), both NEGATIVE; neither alleges a DUT defect. Nothing on the bench was touched and no figure on the page changed. Each item of the round's assignment:

1. **R624-5-F1, the line-3200 LOCKED row.** It now reads each case's count from that case's own receipt through `each()`: the shared value, or a MISMATCH that names every case's value. Its receipt column names both files, `r2/bcrf-poll-receipt.json; r2/baaf-poll-receipt.json`. The poll-count row beside it reads the same way. R624-5's `probe_row3200.py`, unchanged, now reports `row3200_insensitive` false: at line 3200 the LOCKED row is MISMATCH, recomputed `bcrf 595, baaf 596`. The poll-count row stays OK, because the probe changes only the LOCKED count and the window still holds 596 polls; see the open question below. A new key scan finds no other row key whose loop variable goes unread. On round 5's check it finds exactly this row (`r6/key-scan.json`, `r6/key-scan-r5-check.json`).
2. **Normalise before matching (R625-5-F1).** Before any token or category is matched, every HTML comment is dropped, including one over several lines. A backslash escape gives its character and an HTML entity its character. Code (a fenced block, an indented line, a code span) is kept as written. The text is split into blocks at blank lines, and every whitespace run, line breaks included, collapses to one space. Every line number in the output is still the source line. A comment that holds a blank line is dropped only where it starts a line, as an HTML block; elsewhere CommonMark shows it as text and the check reads it.
3. **Identifiers by a closed follower list (R624-5-F2).** An identifier counts only when what follows it, after the check looks past spaces, dashes, a slash or backslash, emphasis and code marks, brackets, quotes and a link's target, is one of these:
   - the end of the text;
   - a mark that ends a phrase (. , ; : ! ? a table's bar, a dash set off by spaces; a point or comma before a digit is a decimal);
   - a possessive 's;
   - one of the words "and", "or", "to" and "of", unless a measurement follows the word, as in a range.

   Any other word, a number or a symbol makes its digits a measurement that only a row can claim. A code literal (a packet path, a listed commit, the label, the branch, a field name, a packet directory or the command) ends with its code word. A link's target stays an address. `MEASURE` also reads the units' names (per cent, decibels, hertz and its multiples, parts per million, billion or trillion, milli- to picoseconds, msec, usec, nsec), every dash, and a comment over a line break.
   - The page was reworded within its lines where the list refused its own text, an identifier before a verb or noun (127 edits, no line moved, no figure changed). The three acceptance headings now read "acceptance of #629"; nothing linked to the old anchors.
   - "Channels 2 and 3 carry" stays verbatim, because R625-5's probe asserts it. Rows claim those indices from every run's point summaries, each bound to the text around it ("Channels «2» and", "and «3» carry"), so R625-4's unbound continuation still fails.
   - Controls, each failing the check and naming the figure as a measurement: a descriptor index before per cent, decibels, hertz, kilohertz, parts per million, parts per billion, milliseconds, microseconds, nanoseconds, msec, usec and nsec; R624-5's `B16 milliseconds` and `IEEE 1722.1 milliseconds`; `CLOCK_DOMAIN 7 furlongs`; R625-5's comment over a line break, where R625-5 put it. A further control changes only B-CRF's LOCKED count and sees the row's MISMATCH.
   - `tools/r6_check_controls.py`: 39 of 39 PASS (`controls/r6-controls.json`), round 5's 22 first, their code unchanged. Round 3's, round 4's and round 5's runners, unchanged, pass 5 of 5, 8 of 8 and 22 of 22 against the new check. The new runner against round 5's published check (`2641412c...`) and the page at `36190193` fails all 17 new controls and passes the 22 earlier ones (`controls/r6-controls-on-r5-check.json`).
   - The reviews' probes, unchanged, copied into `tools/review-probes/` with their published SHA-256 (`r6/*-probe-rerun.json`, from `tools/r6_probe_reruns.py`): R624-4's 8 of 8, R625-4's 12 of 12 and R625-3's 7 of 7 detected. R625-5's `probe_comment_separator.py` gives [0, 1, 1] and exits 0. R624-5's `probe_r624_5_escapes.py` detects 18 of its 19 `id+` forms, every ruling unit written as a word among them. The one it does not is `CLOCK_DOMAIN 7: ppm`, because a colon ends the identifier's phrase. Its three `word:` forms carry no digit to detect.
   - 78 further forms, each meeting its expectation (`r6/self-probes.json`, from `tools/r6_self_probes.py`). Round 5's forms run first: all still fail but its page marker, which now sits inside a comment the check drops. Of the forms that passed in R625-5's own campaign, the small and fullwidth hyphen-minus, the em dash, the closing bracket and the apostrophe now fail; a full stop between an identifier and its unit still passes. A word after each kind of identifier fails, and so do an entity, an escape, a comment in code, a range into a claimed figure and a code literal before a unit. Eight forms pass as the page states.
4. **R624-5-F3.** "Where the packet is" now maps round 4 to `author-r4/` (archived at `61ae8641`, published by `b83e5d76`) and round 5 to `author-r5/` (archived at `36190193`, published by `a73ce5c4`), and names round 6's `author-r6/`. `tools/r6_evidence_receipt.py` reads it from the object store (`r6/evidence-receipt.json`): `MANIFEST.json` at `a73ce5c4` has 3,044 entries. All 76 hash rows of the section at `36190193` equal their files in `author-r5/`, and 592 of its 593 files equal round 5's own MANIFEST.sha256 (the 593rd is that manifest). Rows recompute the paragraph's commits from the receipt.
5. **R624-5-R1.** Applied verbatim on the page, in round 5's list, and in this body, Round 5 item 1. R624-5-S1 is taken: "What the rule does not cover" states the limits, which run as self-probes.

Open question for the manager: the assignment asks R624-5's `probe_row3200.py` to turn both line-3200 rows MISMATCH. It turns the LOCKED row MISMATCH. The other row is the window's poll count in "596 of 596", which the probe leaves at 596, so that row is still correct. Making it fail would mean checking the LOCKED count a second time. Line 3174's pair behaves the same, and R624-5's own verification allows "or the check must otherwise fail at line 3200".

At `e91a62ee`: 1,790 rows, all equal to their receipts; 13,849 digits, 11,445 in claimed figures, 2,404 in 1,186 identifiers that count, 0 uncovered. `tools/r6_figures_build.py` regenerates the check byte for byte from `tools/r6_figures_spec.py`. The check is 194,617 bytes, under the packet's 200 KB limit.

The check's files are pinned here and in the packet's `MANIFEST.sha256`, not on the page:

| Packet file | Bytes | SHA-256 |
|---|---|---|
| `tools/check_b16_figures.py` | 194,617 | `62bce479615dc54b107261b3f987434271bbab25e8acedd8bb39579b9be19274` |
| `r6/figures-rows.tsv` | 119,688 | `1e1d70550f1f36c75932c7868d87e9ff9f091bda08391c3e552a826adbda273b` |
| `r6/figures-coverage.tsv` | 77,339 | `e7649dcc4166596a2e83b1bdc2da045fb8d4d256174cc1059de538bc9808ab70` |
| `tools/r6_figures_build.py` (authoring aid) | 5,229 | `cb8aab2fe2530178bfe5e004dbd396e59006d6fcf3d824b2eb19318c9473433f` |
| `tools/r6_figures_spec.py` (authoring aid) | 158,415 | `64c5314e274cbbcc454f76f56f22d1238ba4459c54372b8aeabb05c55bbca7e4` |
| `tools/r6_probe_reruns.py` | 5,847 | `a08f1f4d718acd15c62203a3fd9ea932a0d74e19e39a4954d8d82d5f06ad7cae` |
| `r6/r624-5-row3200-probe-rerun.json` | 2,234 | `c42e748d8852ce4ccdac3676403ba1da3c5c32e9dfb3bd91d7ad110c70f33e64` |
| `r6/r624-5-escapes-probe-rerun.json` | 19,465 | `ef94d1c3fc05ddc6be60d8d6c9e5e0ec280f9a71a71dda0776baff78e31a3fa8` |
| `r6/r625-5-comment-probe-rerun.json` | 4,527 | `02a525a067fae1d909bfc7c720b2f98a6842f8a5c1bfbb9da3fc9c2e6391225b` |
| `r6/r624-4-probe-rerun.json` | 5,006 | `8946b02514a2e93541f3e1328737da8d0f61e4b19cf86f4df31d179b6b8aa75e` |
| `r6/r625-4-probe-rerun.json` | 13,600 | `2b1613462dc7061975d430794a0187b7fc60423be665e07a0d51de958edecc68` |
| `r6/r625-3-probe-rerun.json` | 5,206 | `c9374869ace93c2a52a1f09158d95c0e105ebb1b2bf45925697b1890e7582041` |
| `tools/r6_self_probes.py` | 9,132 | `f614715a9b4e4ffe504e9e2dafb043bdea7bf1656592a790e4016628d8da4bb5` |
| `r6/self-probes.json` | 34,340 | `6b46980ca65079088767f8308c4525f34306f4de395afc567efa4a3cbd612602` |
| `tools/r6_key_scan.py` | 1,767 | `084a9d17ff7e74f070f32a18c9b05495e7c51f1d9e9fd6e6c027d563c68f14ed` |
| `r6/key-scan.json` | 147 | `c4a3f14f7693ee79d2ac9b88d1debb94681928f55f3272f0061d8c807cd0aa9d` |
| `r6/key-scan-r5-check.json` | 295 | `b8800a9446cb27853926624a858710f912aca7caad8884408455c6305704575b` |

The other round 6 files, `tools/r6_check_controls.py`, the five `controls/r6-*.json`, `tools/r6_evidence_receipt.py` and `r6/evidence-receipt.json`, are hashed on the page.

At `e91a62ee` all 14 gates are rc 0, as listed under Validation (`check_em_dash.py`: 0 findings over 3,722 added lines).
