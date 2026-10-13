[A603] Bench lane B16 for #629: the reference peer's loopback; B16b: Direction B's tone through the DUT and B0; B16c: B-CRF and B-AAF; rounds 2 to 10: every figure checked against its receipt, every digit accounted for, an identifier counted only before a closed list of followers, the checked text read through the pinned Markdown parser with a closed allowlist of constructs, each construct judged by the lines its source spans, and where the packet is published

Title, as both reviews ask (for the manager): Record bench lanes B16, B16b and B16c: Direction B's B0 graded, and B-CRF and B-AAF graded at the path's floor (#629)

Refs #629.

Thirteen commits on dev `c20c85bd`, all docs only:

- `694d7da6` adds the dated section "Dev 5603c353, 2026-10-12: lane B16" to `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, with its Contents line and the introduction's pointer.
- `0d4ff919` adds the B16b part to that section (ten `B16b:` subsections, the Contents line and the pointers).
- `e20fd282` adds the B16c part (eleven `B16c:` subsections, the Contents line and the pointers).
- `35e332b6` answers the two reviews: it corrects figures against their receipts and bounds B0's attribution by the taps. It states lane B6's four terms, and adds the subsection "B16, round 2: reduced receipts".
- `0782c55f` answers the next two: it corrects the figures a new figures check found off, and adds the subsection "B16, round 3: figures check".
- `61ae8641` answers the next two: it states where the lane packet is published, narrows the check's exemptions to identifiers, and adds the subsection "B16, round 4: packet and coverage".
- `f60132ca` answers the next two: the check now accounts for every digit, and the commit adds the subsection "B16, round 5: every digit" and states the rounds 3 and 4 checks as they were.
- `36190193` states on the page the check's quoted-mention rule and every separator it reads between a number and its unit.
- `e91a62ee` answers the next two: the check reads the page as rendered and counts an identifier only before a closed list of what may follow it, a figure for several cases is recomputed from each case's receipt, the packet's rounds 4 and 5 are mapped, the covered text is reworded within its lines where the list refused it, and the commit adds the subsection "B16, round 6: the closed list".
- `295ba9d7` answers the next two: the check refuses any line of its text that holds markup, in code too, instead of dropping comments; the section's table markers become blank lines and a code block's placeholders move to braces; round 6's packet is mapped; and the commit adds the subsection "B16, round 7: no markup".
- `b522bb92` answers the next two: the check reads its text through the repository's pinned Markdown parser and judges only the visible text it yields, refusing any construct off a closed allowlist, in the index row too; the section's fenced code block becomes a list of code spans on the same lines; round 7's packet is mapped; and the commit adds the subsection "B16, round 8: the parser".
- `cb5ff79f` answers the next two: the check judges each construct by the lines its source spans rather than the end the parser reports, refuses a paragraph whose lines the parser misplaces, and counts lines as the parser does; the manager's decision on round 8's changed expectations is recorded; round 8's packet is mapped; and the commit adds the subsection "B16, round 9: source extents".

- `f1b2489f` adds round 10: blocks without source starts are refused, rendered digits are conserved, round 9's packet is mapped, and the findings and index state the rule.

Each also updates the lane's row in `docs/findings/README.md`. No repository code, RTL or firmware changes.

## B16 result

On the dev `5603c353` image, after the identity gate passed, the lane tried the assignment's positive reference: the reference peer's own listener bound to its own talker under the binding rule, with lane B15's known tone played into the peer's talker inputs through the same authorised source.

- The loopback did not form, in two runs. The bind answered SUCCESS, but the peer's listener never learned its own talker's stream ID or destination. The talker's connection count stayed 0, the talker sent no PDU on either link, and the peer's digital output read exact zero at the external capture.
- The second run's tap covered the bind. 99.6 ms after the unbind command, the peer sent PROBE_TX (IEEE 1722.1's CONNECT_TX) for its own talker onto the network, and again 200 ms later. Nothing answered in the rest of the capture, 49.6 s, so the stream never started.
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

Open question for the manager (answered; see Round 7, item 3): the assignment asks R624-5's `probe_row3200.py` to turn both line-3200 rows MISMATCH. It turns the LOCKED row MISMATCH. The other row is the window's poll count in "596 of 596", which the probe leaves at 596, so that row is still correct. Making it fail would mean checking the LOCKED count a second time. Line 3174's pair behaves the same, and R624-5's own verification allows "or the check must otherwise fail at line 3200".

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

## Round 7

Documents only, after R624-6 (POSITIVE, two suggestions) and R625-6 (NEGATIVE, one MINOR); neither alleges a DUT defect. Nothing on the bench was touched and no figure on the page changed. Each item of the round's assignment:

1. **No markup in the checked text (R625-6-F1).** The check refuses, line by line, any line of the text it covers that holds `<` directly followed by a letter, `/`, `!` or `?`. That is how every HTML tag, closing tag, comment (the short forms `<!-->` and `<!--->` too), processing instruction, declaration and CDATA section starts, and an autolink. The refusal applies inside code as well, so no difference between the check's reading of code and the renderer's can shelter a tag. Each refused line is named `MARKUP <document>:<line> <markup>` on standard output and in the coverage receipt, the summary counts `markup`, and the check exits 1 whatever else it finds.
   - The only exception is a line equal byte for byte to a marker a repository generator writes. `scripts/check_solution_docs.py` generates its product and interface tables with `<!-- solution-cpu-contract:start -->`, `<!-- solution-cpu-contract:end -->`, `<!-- solution-interface-groups:start -->` and `<!-- solution-interface-groups:end -->`; these four are `GENERATED`. `scripts/gen_toc.py` writes no marker: it finds its list by the `## Contents` heading.
   - The comment-stripping branch of `normalise` is removed, so nothing written on a line is dropped. Backslash escapes and entities still give their characters, code is kept as written, and whitespace still collapses across line breaks within a block. `SEP` and the closed list still look past a tag or a comment, as in round 6, only to decide whether a number is a measurement; they hide nothing, and any line holding markup fails first.
   - On the unchanged page the new check refused 15 places: the section's eleven table markers (`<!-- b16-points -->` and the like) and four placeholders in one code block (`<raw>` twice, `<class map>`, `<list of the twelve reads>`). Each marker's line is now blank, so no line moved: R624-5's and R624-6's probes read lines 3008, 3174, 3200 and 3244 by number. The page renders as before, and the placeholders are now in braces. The spec's table generator now finds the point and grade tables by their header rows; the rebuilt rows are byte-identical to round 6's.
2. **Controls.** `tools/r7_check_controls.py`: 50 of 50 PASS (`controls/r7-controls.json`). Round 6's 39 come first, their code unchanged, then 11 new ones:
   - R625-6's four forms, appended where R625-6 appended them: `CLOCK_DOMAIN 7<!-- -->ppm.`, `CLOCK_DOMAIN 7<!-->ppm<!-- -->.`, `CLOCK_DOMAIN 7<!--->ppm<!-- -->.` and `CLOCK_DOMAIN 7<!-->furlongs<!-- -->.`;
   - R625-5's comment on one line and over a line break, where R625-5 put it;
   - `The residual was 7<span></span>ppm.`, and `` `CLOCK_DOMAIN 7<!-- -->ppm` `` in a code span;
   - `<!-- b16c-grade -->` put back on its blank line;
   - `<!-- solution-cpu-contract:start  -->` (one byte off) appended as the page's last line.

   Each fails with its line named MARKUP, and where it adds a digit, that 7 named UNCOVERED at the line. An 11th control appends the exact marker and must pass: no MARKUP, nothing named that the unchanged page does not name, the unchanged page's exit status (0 at the head), and both appended lines read. It compares with the unchanged page rather than with exit 0, so its verdict does not depend on the page's own figures, which state it; the stated passes of the self-probes are judged the same way.
   - Round 3's to round 6's runners, unchanged, against the new check: 5 of 5, 8 of 8, 22 of 22 and 39 of 39.
   - The new runner against round 6's check (`62bce479...`) and the page at `e91a62ee`, exported with `git archive`: the 39 earlier controls and the exception control PASS, and the 10 new refusal controls FAIL (`controls/r7-controls-on-r6-check.json`). Round 6's check exits 0 on the three short-comment forms, the former marker and the changed marker.
   - The reviews' probes, unchanged (`r7/*-probe-rerun.json`, from `tools/r7_probe_reruns.py`). R625-6's `probe_rendered_comment.py`, run with the repository's hash-locked renderer (cmarkgfm 2025.10.22, html5lib 1.1), gives statuses [0, 1, 1, 1, 1, 1], R625-6's required outcome. Each comment form has `MARKUP` and `UNCOVERED 7` at line 3011. The probe itself exits 1, because its last assertion still states [0, 1, 1, 0, 0, 0], as R625-6 said it would.
   - The six earlier probes give what round 6 recorded: R624-4 8 of 8, R625-4 12 of 12, R625-3 7 of 7, R625-5 [0, 1, 1] (exit 0), R624-5's row probe MISMATCH on the LOCKED row, and R624-5's escape probe 21 of 25.
   - R625-6's `probe_followers.py` and R624-6's `probe_r624_6_escapes.py` and `probe_row3200_polls.py` run too. R625-6's two comment forms that passed (`code_directory_comment`, `malformed_comment`) now fail; every other form keeps its status. R624-6's escape probe gives every form the exit status R624-6 recorded at `e91a62ee`. Its poll-count probe turns line 3200's poll-count row MISMATCH.
3. **Optional.**
   - R624-6-S1 is taken as documentation. "What the rule does not cover" now states the approximate-quantity forms ("or so", "or more", "and a half", "to some" before a unit, and a bare unit after "of" or "and") and a list marker before a unit. It also states that markup outside the covered text is not read. These forms run as stated passes in `r7/self-probes.json`.
   - R624-6-S2: the open question of round 6 is closed as answered. R624-5's `probe_row3200.py` turns line 3200's LOCKED row MISMATCH. The poll-count row there correctly stays OK under that mutation, and R624-6's own poll-count mutation turns it MISMATCH. Both reviews read it the same way.
4. **Texts.** The page's round 7 subsection, its introduction, Contents line and opening paragraph, and the lane's index row state the rule. "Where the packet is" maps round 6 to `author-r6/` (archived at `e91a62ee`, published by `b616e7ea`) and names round 7's `author-r7/`. `tools/r7_evidence_receipt.py` reads it from the object store (`r7/evidence-receipt.json`): `MANIFEST.json` at `b616e7ea` has 3,800 entries. All 84 hash rows of the section at `e91a62ee` equal their files in `author-r6/`, and 646 of its 647 files equal round 6's own MANIFEST.sha256 (the 647th is that manifest).

At `295ba9d7`: 1,834 rows, all equal to their receipts; 14,531 digits, 11,910 in claimed figures, 2,621 in 1,271 identifiers that count, 0 uncovered; 0 lines with markup. `tools/r7_figures_build.py` regenerates the check byte for byte from `tools/r7_figures_spec.py`. The check is 198,839 bytes, under the packet's 200 KB limit. Further forms: 111, each meeting its expectation (`r7/self-probes.json`): 92 detected, 19 passing as stated. The key scan (round 6's `tools/r6_key_scan.py`, unchanged) finds no row key with an unread loop variable among 565 loops. Every round 7 output re-runs byte-equal at the head.

The check's files are pinned here and in the packet's `MANIFEST.sha256`, not on the page:

| Packet file | Bytes | SHA-256 |
|---|---|---|
| `tools/check_b16_figures.py` | 198,839 | `6b2570b8361356f71f36dc8ec72197c5a8882fa3507f7a01a533f23e575897a0` |
| `r7/figures-rows.tsv` | 123,223 | `6585aa3ec0e68a098270834557902233a04ba05e8e5d4f9f7497368671706ae7` |
| `r7/figures-coverage.tsv` | 83,205 | `15807ad6921efcd83302c18678b1c07b1fd7583bdcbecadfd9d13ca6c5105923` |
| `tools/r7_figures_build.py` | 5,318 | `2be351307059e55b1e5065111f5f238867258f8b858ce6f6f093856fbd6ed52d` |
| `tools/r7_figures_spec.py` | 161,071 | `635427db447ec4dd575af3d55da60836ec4e17a6471bc20e23cbffa0709f211b` |
| `tools/r7_probe_reruns.py` | 9,983 | `66a23643d0b01973b8f7f32ae08ac235a9b3ffff048392125bded8bab630a379` |
| `r7/r625-6-rendered-probe-rerun.json` | 10,522 | `261646308805968b28c61346788af7d008b196a12d87e9f7bee84339803b2aba` |
| `r7/r625-6-followers-probe-rerun.json` | 21,504 | `7bbcbc0bb824f418824945fd0a3c6316d3febd1c6f9527885ad2e0e1d9551afc` |
| `r7/r624-6-escapes-probe-rerun.json` | 28,204 | `1968e5ce0209f1df5984ad7db7790c4ae114cd2150e00c9861acff650eb895ea` |
| `r7/r624-6-row3200-polls-probe-rerun.json` | 1,823 | `1e315b5408d1250c30d61e8794c16a48454cd444fcd2a2724d57d8b0980cd63b` |
| `r7/r624-5-row3200-probe-rerun.json` | 2,250 | `51125c1f0b4322d6019c8856475ac3cc1048ca2a34121e82c56095d038ab7f54` |
| `r7/r624-5-escapes-probe-rerun.json` | 19,915 | `f4e064144211d532a4aa62ba055a13dc577574fbcb1d49484d1cc33ea419ce52` |
| `r7/r625-5-comment-probe-rerun.json` | 6,676 | `93a86e311605a8652b3bbaf6e439e5f0936196cf56e96099cfa0a17018f99e1e` |
| `r7/r624-4-probe-rerun.json` | 5,142 | `33f3aa330647d1d731c8bbba689533b297c6b22ae54414abdbfd53b658a7f22c` |
| `r7/r625-4-probe-rerun.json` | 13,984 | `bd6849268e7a619159364abe413d75961c8543be70fcc266ec58509270bac949` |
| `r7/r625-3-probe-rerun.json` | 5,325 | `8226cb50e1143c6b6b3b7f0ce0d19f29227014371e7224d0ff616f79648a11d7` |
| `tools/r7_self_probes.py` | 9,571 | `28e553c86740d55fae92fcc661c051a771af692f82bd03afcdc26db8477ae843` |
| `r7/self-probes.json` | 44,095 | `fd04e1a94063615eed8996490436f12129cc8ec47912dad8625bb88d1c11b325` |
| `r7/key-scan.json` | 147 | `728516963fafd03ebb6c580d722a6670da678d1092f1b7365c95d192992d120a` |
| `tools/review-probes/probe_rendered_comment.py` | 3,299 | `22c38feb3cd3cac780bf5a2f299716b125047c9703df0b60dbe54beccc3aed57` |
| `tools/review-probes/probe_followers.py` | 2,817 | `6703a34616f606f2be81d943646a1022fd6e8070d273f4aaaa459cf29a0e451b` |
| `tools/review-probes/probe_r624_6_escapes.py` | 5,181 | `f4c9d523e6ea15f87e160768c61dc5229f51306dd1f4429984e7e380a27facc2` |
| `tools/review-probes/probe_row3200_polls.py` | 1,674 | `13a323fd7a4609309fb900b2c654d8bcbacaf21e8646a4b703e709990bb5c3e5` |

The other round 7 files, `tools/r7_check_controls.py`, the six `controls/r7-*.json`, `tools/r7_evidence_receipt.py` and `r7/evidence-receipt.json`, are hashed on the page.

At `295ba9d7` all 14 gates are rc 0, as listed under Validation (`check_em_dash.py`: 0 findings over 3,847 added lines).

## Round 8

Documents only, after R624-7 and R625-7 (both NEGATIVE, one MINOR each); neither alleges a DUT defect. Nothing on the bench was touched and no figure on the page changed. Each item of the round's assignment:

1. **Read through the pinned parser.** The check parses both documents whole with the repository's pinned Markdown parser, cmark-gfm through the cmarkgfm binding at the releases `tools/markdown/requirements.txt` pins. It verifies them with `scripts/gen_toc_renderer.py`'s `verify` (the documentation gates' check) and uses that renderer's extensions and options. It judges only the visible inline text the parser yields: text, code spans and link text. A code span is read with a code mark at each end that every rule looks past; a code category must lie inside one parser code span. Every line it names is the parser's source position.
   - Removed: round 7's markup pattern (`MARKUP`, `markup()`), round 6's code, escape and entity reading (`normalise`'s fence, indent and span logic, `ESCAPABLE`, `ENTITY`, `BLANK`), the entity, comment, tag and link-target alternatives of `SEP` and `PAST`, and the list-item and link-target categories, which read source syntax the parser does not yield as text. `normalise` keeps its name and signature (R625-6's probe extracts it) and now only collapses whitespace and drops invisible characters.
   - A link's target and title are not read. A target must still resolve (round 5's rule); one that does not is read as text of its own at its line, so round 5's anchor control keeps its outcome.
   - Without the pinned parser the check names what is missing and exits 1. The gates' Markdown environment and a fresh environment installed from the lock with `--require-hashes` give byte-equal outputs.
2. **A closed allowlist.** Paragraph, heading, list, item, block quote and table structure; text; soft and hard breaks; emphasis; strong; links, read on their text; code spans. Anything else is refused at its first covered line and named `MARKUP <document>:<line> <parser's name> <source>`: an image, raw HTML inline or as a block, a fenced or indented code block, a thematic break, struck text, a footnote reference or definition (which the parser types `<unknown>`; named by type number), a task list item, and anything else. What a refused construct holds is not read; the check fails whatever else it finds. The only exception is raw HTML that is one whole line equal byte for byte to one of `scripts/check_solution_docs.py`'s four markers.
   - On the unchanged page the reader refused one construct: the section's fenced code block of round 2's four extraction commands. It is now a list of code spans on the same lines, its fence lines blank, so no line moved and the page passes.
3. **R625-7.** The index row is parsed with its document and read from the lane B16 part's first byte, by the parser's source columns. R625-7's `probe_markup.py`, unchanged: every case but the unchanged page fails; the four index markup cases are each named `MARKUP README.md:15 html_inline ...`, write both receipts and raise nothing, and the index digit case names its number UNCOVERED at `README.md:15`.
4. **Controls.** `tools/r8_check_controls.py`: 73 of 73 PASS (`controls/r8-controls.json`). Round 7's 50 come first, then 23 new:
   - R624-7's eight image forms on the attribution row (`CLOCK_DOMAIN 7![](x.png)ppm.` and the others in R624-7's table): each named `MARKUP ... image` and its 7 (or 2) UNCOVERED at line 3011;
   - R625-7's four index cases: each named MARKUP at `README.md:15`, its 7 UNCOVERED where it adds one, both receipts written, no exception;
   - one per construct off the allowlist, written with no digit: image, raw HTML inline, raw HTML block, fenced code block, indented code block, thematic break, strikethrough, footnote reference, footnote definition, task list item; each named MARKUP by its parser name at its first line;
   - the check run by an interpreter without the parser: exit 1, the parser named, no receipt.

   R624-7's `probe_r624_7_markdown_escapes.py`, unchanged: no form escapes (exit 0 only for the unchanged page and the stated full-stop form); its `probe_r624_7_invisible.py`: every form fails. The new runner against round 7's check and page (`git archive` of `295ba9d7`): the 48 unchanged controls PASS and the 2 changed and 23 new FAIL (`controls/r8-controls-on-r7-check.json`).

   **For the manager's decision: two earlier expectations change.** The ten earlier review probes keep their readings. One exception is a form R624-6 marked "any", a reference definition with a title, which renders nothing and now passes. Round 3's to round 7's runners, unchanged, against the new check: 5 of 5, 7 of 8, 21 of 22, 38 of 39 and 48 of 50. Each FAIL is one of two expectations that reading only what the parser yields changes; in both the check still exits 1 and names the added number at the line:
   - round 4's link-label control expects the `37` of `in [37](#b16c-attribution) blocks` not to be named a measurement, because the link's target stood between the number and "blocks" in the raw text; a reader sees "37 blocks", so the check now names it a measurement (this control is in the r4 to r7 runners);
   - round 7's control for `` `CLOCK_DOMAIN 7<!-- -->ppm` `` in a code span expects MARKUP; a reader sees the comment written out in the code, so the check reads it as text, names 7 UNCOVERED and refuses nothing.

   Keeping either expectation would need a character the reader does not see, or a markup pattern inside code, the two things items 1 and 2 remove. `tools/r8_check_controls.py` carries both forms with the round 8 expectation (`"expectation": "round 8"`). Five of round 7's own self-probe forms are ruled to pass for the same reason (an autolink, a tag in a code span, a comment after a backslash, an unclosed tag, angle brackets around a target that resolves).
5. **Texts.** The page's round 8 subsection, its introduction, Contents line and opening paragraph, round 7's rule paragraph (a pointer to round 8) and the lane's index row state the rule; the index row's round 7 sentence no longer claims that no markup can hide a unit. "Where the packet is" maps round 7 to `author-r7/` (archived at `295ba9d7`, published by `fa974c3f`) and names round 8's `author-r8/`. `tools/r8_evidence_receipt.py` reads it from the object store (`r8/evidence-receipt.json`): `MANIFEST.json` at `fa974c3f` has 4,711 entries. All 93 hash rows of the section at `295ba9d7` equal their files in `author-r7/`, and 706 of its 707 files equal round 7's own MANIFEST.sha256 (the 707th is that manifest).

At `b522bb92`: 1,867 rows, all equal to their receipts; 14,442 digits, 12,164 in claimed figures, 2,278 in 1,243 identifiers that count, 0 uncovered; 0 constructs refused. `tools/r8_figures_build.py` regenerates the check byte for byte from `tools/r8_figures_spec.py`. The check is 199,434 bytes, under the packet's 200 KB limit (its own documentation was condensed; the page states every rule). Further forms: 138, each meeting its expectation (`r8/self-probes.json`): 108 detected, 30 passing as stated. The key scan (round 6's `tools/r6_key_scan.py`, unchanged) finds no row key with an unread loop variable among 569 loops. Every round 8 output re-runs byte-equal at the head.

The check's files are pinned here and in the packet's `MANIFEST.sha256`, not on the page:

| Packet file | Bytes | SHA-256 |
|---|---|---|
| `tools/check_b16_figures.py` | 199,434 | `2eb5a24e427015d39154d28f778693f1170cf513e3e3d34f2cac308f2adc0284` |
| `r8/figures-rows.tsv` | 125,589 | `0e79bee9d9efe80be192daa6c65d8450fdbbbe4af855dbf394a8e9f809c0c714` |
| `r8/figures-coverage.tsv` | 79,399 | `515d0163ebac75849f0783d5607c2b7c45de6d4e6a0476c89d5ff3c664d5d43e` |
| `tools/r8_figures_build.py` | 5,383 | `95b1abb5aef4063253f236649a982aaa464cee5b4092e807b017e75633325ee7` |
| `tools/r8_figures_spec.py` | 163,934 | `d7873c54bc42e64410dd9bc6ecb4f21d020037007672c293adf4d57039056d80` |
| `tools/r8_probe_reruns.py` | 13,525 | `1213ddb41e1c3d4653a50173e43ae8f0b9f2667dc72fd6fcce5a017b2f6b49da` |
| `r8/r624-7-escapes-probe-rerun.json` | 20,529 | `a42da87febfccf574d36a42d9cdcd31bb6ea940f3210eb66b5224b1770d8fe8f` |
| `r8/r624-7-invisible-probe-rerun.json` | 3,416 | `bbbbb38526f4cbe79fe87a231aa394fbe2acb0a3f3e32db9c4feb03dad23ad0c` |
| `r8/r625-7-markup-probe-rerun.json` | 157,850 | `368002b33f2b008d8ceceb231d5065c65562bb14c37403a872f5907b28a333e7` |
| `r8/r625-6-rendered-probe-rerun.json` | 9,942 | `09c9b71392e62ab149bb7bec9837d3ce3b8843941f1e15cd18bbf3b8f07cc6ad` |
| `r8/r625-6-followers-probe-rerun.json` | 19,376 | `1878dd24e689f449ffe55061e41ae4449c60791c3da6bec4296d3e727da7e179` |
| `r8/r624-6-escapes-probe-rerun.json` | 26,141 | `3c1f2823107da9c0f42fb5546209628cb9e5446c79329fa6fd8bac6b1c62b7d3` |
| `r8/r624-6-row3200-polls-probe-rerun.json` | 1,823 | `314727163755f54e7929bd58d21d13f3052fefe5af574323af3f5678314eafad` |
| `r8/r624-5-row3200-probe-rerun.json` | 2,250 | `97b32e135dc72eedfad68ad4e478b6aa04ec35eec2429cf1869b01d07f4fbd9d` |
| `r8/r624-5-escapes-probe-rerun.json` | 19,273 | `b98e1fc9e5a6e701b047414a425d23d2315437326bb564e91b5755aedd9d2b09` |
| `r8/r625-5-comment-probe-rerun.json` | 8,585 | `98284d2994798c7ec366465e254222bc667dc36b60c7e8c8fa51a06e1c529746` |
| `r8/r624-4-probe-rerun.json` | 5,142 | `5bdee0d1502109fbb9ac2bbc5ec9420d80964f35061a3628f189fdc90afef483` |
| `r8/r625-4-probe-rerun.json` | 13,649 | `5bc44df6cd2746a018b7a3e58b3d4d09ade6ea7ec428807aad37a76c7d8caab3` |
| `r8/r625-3-probe-rerun.json` | 5,325 | `4d21af4cbc5812358a6c6643fe85047e1a6d1b0b261bd695545f523ec1a5018d` |
| `tools/r8_self_probes.py` | 9,116 | `ae8637b6dea365f9870867e1d0f0245e496c84b6eb143ffa467c817af7d41f39` |
| `r8/self-probes.json` | 57,605 | `ce098ada3a73611c1f74ae10bfa51dcca36fe0cc03ec0cd1c6cf479920fa7bff` |
| `r8/key-scan.json` | 147 | `6b2db4cfb84433394c3587f86ae229edb8fb5b00ba86daedd9fd3b4acb43ed70` |
| `tools/review-probes/probe_r624_7_markdown_escapes.py` | 4,503 | `4366f8caa9b6d320a515fa73a49d3e0fda80f77f35dbae5b781a7d529e627d29` |
| `tools/review-probes/probe_r624_7_invisible.py` | 1,462 | `ef5ebaae7fc5cda62c98993c7bb1f4bdeb1ea98617950b0eba8cfb830d439e9f` |
| `tools/review-probes/probe_markup.py` | 3,426 | `d23a4cb52d0f4616efcad37a3f10620190bdf61e97a7eba3779cccf8769e691d` |
| `controls/r8-rerun-r3-controls.json` | 1,579 | `4871ef3e84d940d91cc7938ca2ebaf3f904e39b74e21678aa03c602dae7e3560` |
| `controls/r8-rerun-r4-controls.json` | 3,117 | `d8e72afe1deed6b9d5518373c63e2257faf2ad359bbf0c58d2cdc874435c61af` |
| `controls/r8-rerun-r5-controls.json` | 8,155 | `cc852cf8cb2ed98a823e97f37ee7bb05c3c63dc7eb5c13b96c64deec7f7da1d9` |
| `controls/r8-rerun-r6-controls.json` | 14,416 | `a23c47a74a0655444282bec887dcdf8e1d5935f82ee99ddf91d0c36962d59968` |
| `controls/r8-rerun-r7-controls.json` | 18,204 | `e57886abf0967012cb24dacdfbe6e336e15e1200d2d03af1126e44a8d90faae8` |

The other round 8 files, `tools/r8_check_controls.py`, `controls/r8-controls.json`, `controls/r8-controls-on-r7-check.json`, `tools/r8_evidence_receipt.py` and `r8/evidence-receipt.json`, are hashed on the page.

At `b522bb92` all 14 gates are rc 0, as listed under Validation (`check_em_dash.py`: 0 findings over 4,004 added lines).

## Round 9

Documents only, after R624-8 (NEGATIVE, one MINOR) and R625-8 (NEGATIVE, one MINOR, settled by the manager's decision [6132293481](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132293481)); neither alleges a DUT defect. Nothing on the bench was touched and no figure on the page changed. Each item of the round's assignment:

1. **Real extent.** A construct off the allowlist is refused at the first covered line its actual source extent reaches, whatever end the parser reports. `extents()` computes each node's extent from its source:
   - an `html_block` ends on its literal's last line (start line + literal lines - 1), never on the reported end. cmark-gfm reports blocks that end at a closing marker (`</pre>`, `</script>`, `</style>`, `</textarea>`, `-->`, `?>`, `>`, `]]>`) as ending on the line before their last, and such a block on one line as ending above it;
   - every node spans all its descendants. The parser reports struck text as ending where it starts;
   - a link or image starts as many lines above its reported line as its text holds line breaks. The parser starts such a node on its last line;
   - a node whose extent reaches no covered line is passed over with all it holds; otherwise it is refused (off the allowlist) or read.

   The same audit found two more ways the parser's positions fall short, both fixed in the same way, by the source:
   - **Misplaced text.** In a paragraph the parser counts a line break only where it yields a soft break or a trailing-space hard break, or inside a code span or inline HTML. A backslash line break, a link's target, title or reference label over a line break, an image's title over a line break, and a reference definition opening the paragraph each hold a break it does not count, and every later node is placed on an earlier line. The introduction's covered part starts partway through its paragraph (line 18 of a paragraph from line 6), so such a break above it moved line 18's text to line 17 (not covered), unread. The check now compares the parser's last line in each paragraph, heading or table cell with the source's, and where they differ refuses the block at its first covered line (`MARKUP <document>:<line> paragraph ...`, with its own reason).
   - **Line numbering.** `scope()` used `str.splitlines()`, which also splits at U+000B, U+000C, U+001C to U+001E, U+0085, U+2028 and U+2029, characters the parser reads as text; such a character above a covered region shifted the covered lines from the parser's. Both documents are now split as the parser counts lines (`lines_of`).

   `tools/r9_parser_extents.py` runs the check's own `tree()` and `extents()` on 37 small documents, each with its true lines (`r9/parser-extents.json`, 37 of 37 met). The kinds whose reported lines fall short of their source are `html_block`, `image`, `link` and `strikethrough`, and six paragraph forms are misplaced. Inline HTML, code spans, emphasis, footnotes and references, fenced and indented code, thematic breaks, task list items, setext headings, table cells and lazy continuation are reported where they stand.

   Round 9's reader with round 8's rows and categories, on the page at `b522bb92`, gives rows, coverage and output byte-equal to round 8's (`tools/r9_reader_on_r8.py`, `r9/reader-on-r8.json`), so the change in reading moves nothing on the unchanged page.
2. **Control.** R624-8's `probe_r624_8_html_block_edge.py`, unchanged (SHA-256 `106710c3...`, from `629-b16-review-evidence` at `f4936667`): `intro_pre_from_line_above_with_figure` is DETECTED with `MARKUP 629_MEDIA_CLOCK_FOLLOWING_BENCH.md:18 html_block <pre>`. No case escapes, and every other case keeps its exit status and verdict. The heading and Contents cases (`heading_pre_*`, `heading_comment_*`, `contents_pre_*`) now also name the block MARKUP at the covered line, where round 8's check failed them only by a lost row. The round 8 runner (73 of 73), the 13 earlier review probes and the unchanged page were re-run:
   - the earlier probes give round 8's exit statuses, verdicts and named lines (their summary counts and the check's hash follow the new page and check), but for R624-7's `footnote_ref_and` form: its footnote definition, appended after the page's last line, is named at line 4426 instead of 4274, because the page grew;
   - `tools/r9_check_controls.py`: 97 of 97 PASS (`controls/r9-controls.json`). Round 8's 73 come first, unchanged, then 24 new ones, each replacing whole lines so no line moves:
     - R624-8's case;
     - the other seven raw HTML block kinds that end at a closing marker (`<script>`, `<style>`, `<textarea>`, a comment, `<?`, `<!A`, CDATA), with no digit;
     - struck text from the line above the introduction onto its first covered line;
     - an image whose description runs from the Contents entry onto the line below;
     - the six misplacing breaks;
     - the eight separators `splitlines` splits at and the parser does not, each with a figure that must be named UNCOVERED at line 18 with no row failing.

     Against round 8's check (`2eb5a24e...`) and the page at `b522bb92`, the new runner passes the 73 earlier controls and fails all 24 new ones (`controls/r9-controls-on-r8-check.json`), so each new control can catch the defect.
   - Further forms, `tools/r9_self_probes.py`: 156, each meeting its expectation (`r9/self-probes.json`), with 122 detected and 34 passing as stated. Round 9's 18 cover:
     - constructs that open above a covered part and close inside it, at the introduction, the heading and the Contents entry;
     - each misplacing break, with a figure;
     - forms the parser places correctly, which pass: a trailing-space hard break, emphasis and link text over a line break, and R624-8-S1's emoji shortcode.

     No earlier form changed its outcome.
3. **Texts.** The page's round 9 subsection, its introduction, Contents line and opening paragraph, round 8's rule paragraph (a pointer: the rule now holds whatever end the parser reports) and the lane's index row state the rule as it now holds.
   - The decision 6132293481 is recorded where the earlier runners' outcomes are listed: in round 8's "Earlier expectations" paragraph and its runner list, and in round 9's "The decision". Against the new check the historical runners give 5 of 5, 7 of 8, 21 of 22, 38 of 39 and 48 of 50, and the round 8 runner 73 of 73. Each FAIL is one of the two superseded expectations, so the runners are not reported as wholly green.
   - R624-8-S1 is taken as text: the emoji shortcode and the link title are stated in "What the rule does not cover". Refusing them would have changed two of R624-8's own cases, which item 2 keeps.
   - "Where the packet is" maps round 8 to `author-r8/`, archived at `b522bb92` and published by `b0134c63`, and names round 9's `author-r9/`. `tools/r9_evidence_receipt.py` reads it from the object store (`r9/evidence-receipt.json`): `MANIFEST.json` at `b0134c63` has 5,646 entries; all 98 hash rows of the section at `b522bb92` equal their files in `author-r8/`; and 770 of its 771 files equal round 8's own MANIFEST.sha256 (the 771st is that manifest).

At `cb5ff79f`: 1,909 rows, all equal to their receipts; 14,956 digits, 12,531 in claimed figures, 2,425 in identifiers that count, 0 uncovered; 0 constructs refused. `tools/r9_figures_build.py` regenerates the check byte for byte from `tools/r9_figures_spec.py`.

The check is 199,529 bytes, under the packet's 200 KB limit. Round 9's rows name the two cases most rows loop over once (`BC`, `PT`) and read a grade's two tone rows through `tones(d)`, and round 8's control rows use `passed(d)`, the same sums written shorter. No figure, line or receipt of any row changed. The key scan finds no row key with an unread loop variable among 541 loops. The outputs, generated in a scratch copy and regenerated in the packet at the head, are byte-equal (54 files), and the 14 probe records are byte-equal on a second run.

The check's files are pinned here and in the packet's `MANIFEST.sha256`, not on the page:

| Packet file | Bytes | SHA-256 |
|---|---|---|
| `tools/check_b16_figures.py` | 199,529 | `bafea39b3af1d6ba654cfbfc8c2feaf30e147a0abb5e8226650108d1e3238f11` |
| `r9/figures-rows.tsv` | 128,679 | `b571fa5c07a76ed4659788e4c0db40b2ef5fe73c839a67b3a7106f1da01a2226` |
| `r9/figures-coverage.tsv` | 84,627 | `b97648436d53cbbbcc23d75009ca9191302a12e7dee3b86eeec418af0f39032e` |
| `tools/r9_figures_build.py` | 5,464 | `6a96840c61ebdf57acb1b7b131a508ef89e246c14fb3be620d8c000bd2b14d62` |
| `tools/r9_figures_spec.py` | 164,406 | `857a99905d04e00dfdababd641cd94f8c96aefb2ad152d15b401439f517cd45a` |
| `tools/r9_probe_reruns.py` | 15,043 | `05deed808a213deb448a8d08ab0891f539a6283147f551aef39462ef7367cb8a` |
| `tools/r9_self_probes.py` | 12,100 | `5a42d8018b72e4c0d2d6ee6aeef398ea7245e0c76f56e01812406971c89097fe` |
| `tools/r9_reader_on_r8.py` | 3,002 | `5641dd595603005e472e94f7ddb290bacbdfcb0b376ed44c9058e161bb34e6e0` |
| `r9/reader-on-r8.json` | 915 | `665c3d544f76dda18351d8ae42dfc5bd2683b2dd56f9ab8947e297e756d6a22b` |
| `r9/self-probes.json` | 67,766 | `5b49ddbc117ce566d675429d171564d0321e4eebbc28cbd64dd66e4c73fe7587` |
| `r9/key-scan.json` | 147 | `02b0065dd736eab01a102458b596cede8aa39b32e0f05ed47d119fdf4fd76136` |
| `tools/review-probes/probe_r624_8_html_block_edge.py` | 5,117 | `106710c3213e985d6a59eb212444b7ac8056664c59b9e3ae24c610c48c03424f` |
| `r9/r624-8-html-block-edge-probe-rerun.json` | 19,246 | `1e4778353214717efece4c3d242692e52cd3dcaa6fc1ded4e3859a1bd6541783` |
| `r9/r624-4-probe-rerun.json` | 5,142 | `47e820db63dc7d66f6a2c5f9cb44280bdbdf747f70721be25ba8381c12abfff3` |
| `r9/r624-5-escapes-probe-rerun.json` | 19,273 | `d5b782cb752303ea8fa411ac57de0243eae4079ada1bc0c9d28e56bb9edcbc7e` |
| `r9/r624-5-row3200-probe-rerun.json` | 2,250 | `95fc18411e3c4d3f96af389fa948bc62bc966b484702d1e503be804c14b516ab` |
| `r9/r624-6-escapes-probe-rerun.json` | 26,141 | `ced977cd899b896876134f89695f01ed7d12af6e87ebb8cecc82d569751bbfc7` |
| `r9/r624-6-row3200-polls-probe-rerun.json` | 1,823 | `117a1ab4e6eb9ad983c7deeaddbafed860d531b3729e331549ab14598543e8ba` |
| `r9/r624-7-escapes-probe-rerun.json` | 20,529 | `8a6948def79afe7dbf0c6e0f02c1c20fb1ed2fff28107dee4d2137a8a1645186` |
| `r9/r624-7-invisible-probe-rerun.json` | 3,416 | `6c77fee4b655f24bee4112c029b9f99b692b87479718a49996bcf8e2a5b5a82a` |
| `r9/r625-3-probe-rerun.json` | 5,325 | `774473d2a752c770ea46d10c3a1738d2e8d87eb9a4ed3ba0d6d201d9a80e9c16` |
| `r9/r625-4-probe-rerun.json` | 13,649 | `db52c8c13f13522e625cbc6037d3f6890c16920d630b53586372dad45379ec01` |
| `r9/r625-5-comment-probe-rerun.json` | 9,224 | `474293ae87cb7b73278fd9a3cf053fada1e871f715ebd66ce9d8e7b556ee8c24` |
| `r9/r625-6-followers-probe-rerun.json` | 19,376 | `0d59699cd16b52f859281897fe19d3cc459a21edc846091ae9a3409060fb08d0` |
| `r9/r625-6-rendered-probe-rerun.json` | 9,942 | `1ac4efd58006e806abd3199353dd432b54e6e30eef9e6aa12102185955c1ca02` |
| `r9/r625-7-markup-probe-rerun.json` | 157,850 | `74f416a4f124ace82e23749791b751863ba07e991cd6a56ac5666f6c5cd88ea4` |
| `controls/r9-rerun-r3-controls.json` | 1,579 | `4871ef3e84d940d91cc7938ca2ebaf3f904e39b74e21678aa03c602dae7e3560` |
| `controls/r9-rerun-r4-controls.json` | 3,117 | `829f85ed77e85f71479262092c3fb9038312a079367a26b91b8b7ff6eccd1dee` |
| `controls/r9-rerun-r5-controls.json` | 8,155 | `c4fa91a58be8036dc8a81ffdfbe52a5dbf5886f84c48cca27781ae8bd28f5b75` |
| `controls/r9-rerun-r6-controls.json` | 14,416 | `278f4966b6dfb384c4b06fae829ac860e33bb628b83929d3e1b10b198db5d308` |
| `controls/r9-rerun-r7-controls.json` | 18,204 | `ab8fa1db8771f0ac7188b629a6b82fe4b56a7a53da7b40320dcf18627e6c0e62` |
| `controls/r9-rerun-r8-controls.json` | 26,053 | `0ad5e5a5298f3266d56fe648f3bedf4b3cca3f38442c47044ed19d8f5a9e7d20` |

The other round 9 files, `tools/r9_check_controls.py`, `controls/r9-controls.json`, `controls/r9-controls-on-r8-check.json`, `tools/r9_parser_extents.py`, `r9/parser-extents.json`, `tools/r9_evidence_receipt.py` and `r9/evidence-receipt.json`, are hashed on the page.

At `cb5ff79f` all 14 gates are rc 0, as listed under Validation (`check_em_dash.py`: 0 findings over 4,156 added lines).

## Round 10

Documents only under the [round 10 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6134101205). Answers [R624-9](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6134093761). No bench action; bench figures, verdicts and remaining acceptance items stand.

- A node without a valid source start, except a soft or hard break, refuses its entire block at the first covered line. This includes bare e-mail, `mailto:` and `xmpp:` autolinks, their text and trailing text. Missing positions on the block itself or its enclosing structure also refuse it.
- Each covered block is rendered with the pinned Markdown renderer and its HTML parser. The multiset of its visible digits must equal the multiset the checker read. A difference refuses the block at its first covered line. This also detects an entity or escape just before the index suffix that previously hid the suffix's first digits. The page states the partial-block masking and rendering limits.
- R624-9's probe is retained unchanged. The standing controls include each autolink form and a later-line figure. The parser-extents audit includes the zero-position nodes; parser-output mutations also check missing starts on other node kinds, and lost, duplicated or substituted digits. Final results and hashes are recorded below.
- The findings and index state both rules. The packet map adds `author-r9/`, source `cb5ff79f`, evidence `4ab00ba5`, and names the new `author-r10/` packet for publication by the manager.
- R624-9-R1 is applied above: earlier probes retained exit statuses, verdicts and named lines, with the stated footnote movement; their full output bytes also contain updated counts and the check's hash. R625-9's manager-applied corrections remain: “99.6 ms after the unbind command” and “line 4426”.

Local commit: `f1b2489f5b1c929e81eeae79a469b2b27c47e340`, not pushed. All 14 gate entries are rc 0 at this head; the final 117-control repeat is byte-equal to its published receipt. Refs #629.

Round 10 results: 1,960 of 1,960 rows equal their receipts; 15,597 digits (12,988 in claimed figures, 2,609 in identifiers), zero uncovered and zero blocks refused. Standing controls pass 117 of 117 at the local head. Earlier runners retain 5/5, 7/8, 21/22, 38/39, 48/50, 73/73 and 97/97; only the previously superseded expectations fail. All 172 further forms meet their expectations. The parser audit passes 37 earlier plus 22 position cases, and all 15 parser-output mutation controls pass.

R624-9's unchanged probe passes the original and rejects all 14 altered cases by naming the figure or refusing its block. All 14 older probes retain their exit statuses and outcomes (`r10/probe-comparison.json`); only the appended footnote locator moves from 4426 to 4604. The reader compatibility output and regenerated checker are byte-equal. The final checker is 199,268 bytes. File hashes are in MANIFEST.sha256; the per-run tables and selected hashes are in REVIEW-READY-r10.md. Required gate commands and results are in gates/r10/results.json.
