[A603] REVIEW READY (B16, findings round 3)

Commit: `0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5` on `629-b16-tone`, one new commit on `35e332b6` (no rebase, no amend). Not pushed. Refs #629.

This round is documents only, under the [round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119906508). There was no bench action: no lock, controller, board or instrument was touched. It answers [R624-2](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119878041) and [R625-2](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119899949).

Changed:
- `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`: corrections in the B16, B16b, B16c and round 2 subsections, and a new subsection, "B16, round 3: figures check". The new subsection describes the check and lists every corrected figure, Was and Now, with its receipt.
- `docs/findings/README.md`: the lane's row.
- No other file changed, and there is no DUT change.

**The figures check** is `tools/check_b16_figures.py`, in the packet, not the tree.
- It holds one row per quoted figure: the document line, the figure as shown, the receipt, the key and the displayed precision. The text it covers is lane B16's section, the page's introduction and Contents entry on lane B16, and lane B16's part of the index row.
- It recomputes each figure from its receipt and fails on any mismatch after rounding. Receipts are read as exact decimals and rounded half up. Clock times are cut to the last digit shown.
- It also reads every number, time, hash and number word in that text, and fails on any token that neither a row nor a named identifier category covers.
- At `0782c55f` it exits 0: 1,610 rows, all equal to their receipts; 1,815 tokens, 205 in identifier categories, none uncovered. A re-run is byte-equal.
- Its controls on altered copies, `controls/r3-controls.json`, pass 5 of 5: a figure changed on the page, a receipt value changed, a figure added without a row, a row at the wrong line, and a clock time rounded instead of cut.
- The authoring aids `tools/r3_figures_build.py` and `tools/r3_figures_spec.py` regenerate its rows byte-equal from the committed page.

| Packet file | Bytes | SHA-256 |
|---|---|---|
| `tools/check_b16_figures.py` | 179,675 | `13d7a0deb20ca5b16c478491c1499de37864693545a70d0c876ef7e9288d1ea3` |
| `r3/figures-rows.tsv` (its output, one line per row) | 104,749 | `459a55780b5df8817bddfc4f46c3a986c8ff0101464e5c9768a35527a3a1ce7b` |
| `r3/figures-coverage.tsv` (every token a category covers) | 11,186 | `1eb17bab1279870b3b672fe7115b46ff8d3aa62e3001477e85c586579a75a94e` |
| `tools/r3_check_controls.py` | 6,541 | `85fc57876334b823cd349a9752bf12581bbb22f9f5c5b2a4d6f68ab948a54157` |
| `controls/r3-controls.json` (5 of 5 PASS) | 1,579 | `6b6f8bc7b99e5ec6843a7c385e681b4bcf4b89b1b56d84dcc10a88889ce6cc05` |
| `tools/r3_playback_logs.py` | 1,990 | `27334c6d3106f9305187deef6196a7dcb7e14b10d6fbea08f721029766dcf595` |
| `r3/playback-logs.json` | 795 | `68e905288cf0c01c385a995bf66edc78e6323e041de99c1e0f1f3e4b360f64fe` |
| `tools/r3_figures_build.py` | 3,736 | `ec0e1ce6baa09891204687d097f7bca54f9a58f7d781a12a4cc488023b1e5519` |
| `tools/r3_figures_spec.py` | 141,228 | `6338e6fd1a63ccd0d9022942863e491c942dc66d08a6194d9539a9ced54b57fa` |

The page hashes the controls and the playback-log files, rows 4 to 7, but not the check, its two outputs or the authoring aids. The check holds the page's figures, so the page cannot hold the check's hash.

Validation: all 14 gates rc 0 at the head, each to its own log, unpiped, on the physical /data path, with the Markdown gates in the pinned environment:
- `docs_check.py`, `check_doc_style.py`;
- `gen_toc.py --check` and `--verify-anchors`;
- `check_em_dash.py --base e8454e27`: 0 findings over 3,306 added lines;
- `check_doc_paths.py`, `ci_scope.py --selftest`;
- `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`;
- `git diff --check`, and `git diff --check c20c85bd HEAD`.

On the working tree first, `docs_check.py` flagged one bare reference to the findings index. It became a link, and the full set then ran rc 0 on the working tree and again at the head.

| Item | Finding | Now |
|---|---|---|
| 1 | A figures check | As above |
| 2 | R625-2-F1: B16c's attribution at (a) | The exact replacement: "At (a), medians are -123.98/-123.97 dB for B-CRF and -123.98/-123.98 dB for B-AAF (997/9,973 Hz); every worst block is -123.93 dB." |
| 3 | R624-2-F1: the positive control's floor counts | Counted over the blocks wholly inside the playback: all 303 in `b0-2`, `bcrf` and `baaf`, and 11 of 13 in `pts2`, where blocks 6 and 12 hold its repeats. Blocks 0 and 1 precede the playback and block 2 holds its start. The `pts2` taps likewise: all 15 blocks wholly inside the playback. Applied at every location R624-2 lists |
| 4 | R624-2-F2: B16c's LOCKED brackets | From the start of the last poll that read ACQUIRE, the poll its state read falls in, to the end of the first that read LOCKED: 2.585 to 3.161 s and 6.602 to 7.180 s, at the trace's ms precision. Applied in the summary rows, the following record, lane B6's term table, the round 2 paragraph, the index row and PR-BODY.md |
| 5 | R624-2-R1 and R2 | The reviewers' exact texts: the state comparisons narrowed to the entries both reads hold (1,255; 618 and 668), and the five steps before the set attributed only as far as the receipts show |
| - | R624-2-R3 (PR body) | The exact text, in PR-BODY.md's "#629" section |
| - | R624-2-S1 | Taken: the servo status bit 4, set at every ACQUIRE and LOCKED poll of both traces, is in B16c's limits |
| - | R624-2-S2 = R625-2-S1 | Not taken: it is optional, and "45 of 46 entries" is true under the census tool's definition |

**The check's own findings**, each corrected on the page and listed in its round 3 table:
- Clock times now follow one rule, cut to the last digit shown, across lanes B16, B16b and B16c.
- Lane B16's tone start is now 05:55:37: the first status read less the frames played.
- `loop2`'s "remaining 49 s" is now 49.6 s after the second probe.
- Before the tone source's change, the drift is now +3.00 and +3.01 frames, and the offset +6.94 to +6.96 ppm.
- In B16c, the decoded span at (d) is now 303.8 s and 303.9 s, and the peer's rate +10.59 to +10.65 ppm.

Statements with no retained receipt were narrowed or cited:
- The resume times are now each round's first bench action, 06:22:23 and 07:48:07.
- Lane B15's `pts1` flags now give only what lane B15's section records.
- Lane B16b's five underruns now cite the operator's record at the tone's stop. That log was overwritten when lane B16c started the playback, so "0.43 to 1.63 s each" is removed.
- Six number words were reworded.
- `r3/playback-logs.json`, bound to the two retained logs, now backs "no underrun" in lanes B16 and B16c.

**Per-run tables, as now stated.** THD+N is the median, with the worst block in brackets. Each pair of values is 997 Hz / 9,973 Hz.

| Run | (c) at the floor | (c), all blocks | Degraded at (c) | (d), lane B6's loop |
|---|---|---|---|---|
| `b0-2`, B0 | 169 blocks; -123.98 (-123.91) / -123.95 (-120.18) dB | -123.95 (-100.47) / -122.80 (-80.48) dB | 131 of 300, no discontinuity; 23 inside the taps' 34.1 s, 108 beyond | 0 discontinuities in 14,583,286 frames; all 303 blocks wholly inside the playback at the floor |
| `bcrf`, B-CRF | 300 blocks; -123.98 (-123.93) / -123.97 (-123.90) dB | the same | None | 0 net steps in 14,583,391 frames; all 303 at the floor |
| `baaf`, B-AAF | 300 blocks; -123.98 (-123.92) / -123.97 (-123.91) dB | the same | None | 0 net steps in 14,585,924 frames; all 303 at the floor |

| Lane B6's term | B-CRF | B-AAF |
|---|---|---|
| Servo LOCKED | Met: 596 of 596 window polls; 2.585 to 3.161 s after the set | Met: 596 of 596; 6.602 to 7.180 s |
| Counted ratio within 0.5 ppm | Met: 0 net steps, below 0.07 ppm | Met: 0 net steps |
| Timed ratio's interval holds zero | NOT RUN | NOT RUN |
| 0 listener discontinuities | Met: 0 at (c) and (d) | Met: 0 at (c) and (d) |

Open, as before: Direction B's INTERNAL mismatch control, lane B6's timed ratio for B-CRF and B-AAF, and #645. #629 stays open.

The packet (`629-b16-a603`, publication the manager's) holds HANDOFF.md with a Round 3 section, PR-BODY.md with a Round 3 section, and MANIFEST.sha256.
