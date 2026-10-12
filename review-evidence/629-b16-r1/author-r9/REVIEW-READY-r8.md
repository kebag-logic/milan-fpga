[A603] REVIEW READY (B16, findings round 8)

Head: `b522bb923fa59581478460b61633bce2cb90ac1d` on `629-b16-tone`, one new commit on `295ba9d7`, with no rebase and no amend. Not pushed. Refs #629.

This round is documents only, under the [round 8 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6130721355). There was no bench action: no lock, controller, board or instrument was touched. It answers [R624-7](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6130711392) and [R625-7](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6130634625). No figure on the page changed.

Changed:
- `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`:
  - a new subsection, "B16, round 8: the parser";
  - the section's fenced code block (round 2's four extraction commands) rewritten as a list of code spans on the same lines, its fence lines blank. No line before the new subsection moved: the reviews' probes still read lines 3008, 3011, 3108, 3174, 3200 and 3244;
  - "Where the packet is", now mapping round 7 to `author-r7/` (`295ba9d7`, published by `fa974c3f`) and naming round 8's `author-r8/`;
  - a pointer from round 7's rule to round 8's, and the introduction, Contents and opening pointers.
- `docs/findings/README.md`: the lane's row (round 8's rule; round 7's sentence no longer claims that no markup can hide a unit).
- No other file changed, and there is no DUT change.

| Item | Assignment | Now |
|---|---|---|
| 1 | Read through the pinned parser | Both documents are parsed whole by cmark-gfm through the cmarkgfm binding, at the releases `tools/markdown/requirements.txt` pins, verified with `scripts/gen_toc_renderer.py`'s `verify` and parsed with that renderer's extensions and options. Only the visible inline text it yields is judged: text, code spans (with a code mark at each end that every rule looks past) and link text. Line numbers are the parser's source positions. A link's target and title are not read; a target that does not resolve is read as text (round 5's rule). Without the parser the check exits 1 naming it |
| 2 | Closed allowlist | Paragraph, heading, list, item, block quote and table structure; text; soft and hard breaks; emphasis; strong; links; code spans. Anything else is refused at its first covered line as `MARKUP <document>:<line> <parser's name> <source>`, and not read: image, raw HTML inline or block, fenced or indented code block, thematic break, strikethrough, footnote reference or definition, task list item, anything else. The only exception: raw HTML that is one whole line equal byte for byte to one of `scripts/check_solution_docs.py`'s four markers. Removed: round 7's markup pattern, round 6's code, escape and entity reading, the entity, comment, tag and target alternatives of `SEP` and `PAST`, and the list-item and link-target categories. `normalise` keeps its name and signature for R625-6's probe |
| 3 | R625-7 | The index row is parsed with its document and read from the lane B16 part's first byte by the parser's columns. `probe_markup.py`, unchanged: all four index markup cases are named `MARKUP README.md:15 html_inline ...`, both receipts written, no traceback; every case but the unchanged page fails |
| 4 | Controls | `controls/r8-controls.json`: 73 of 73 PASS. Round 7's 50 first, then 23 new: R624-7's eight image forms (each `MARKUP ... image` and its digit UNCOVERED at line 3011); R625-7's four index cases (MARKUP at `README.md:15`, receipts, no exception); one per refused construct with no digit (image, raw HTML inline and block, fenced and indented code block, thematic break, strikethrough, footnote reference and definition, task list item), each named by its parser name; and the check without the parser. `probe_r624_7_markdown_escapes.py`, unchanged: no form escapes (exit 0 only for the unchanged page and the stated full stop). `probe_r624_7_invisible.py`: all 10 fail. On round 7's check (`6b2570b8...`) and page, the 2 changed and 23 new controls FAIL and the 48 unchanged PASS. The ten earlier probes keep their readings, but for each MARKUP's construct name and R624-6's "any" form `link-ref-title` (a reference definition, which renders nothing), now exit 0. 138 further forms each meet their expectation (108 detected, 30 stated passes). The unchanged page passes |
| 5 | Texts | The page's round 8 subsection, the index row and the PR body state the rule. `r8/evidence-receipt.json`: `MANIFEST.json` at `fa974c3f` has 4,711 entries; all 93 section hash rows at `295ba9d7` equal their files in `author-r7/`; 706 of its 707 files equal round 7's own manifest (the 707th is that manifest) |

**For the manager's decision: two earlier expectations change.** Item 4 asks that earlier controls keep their outcomes. Round 3's to round 7's runners, unchanged, give 5 of 5, 7 of 8, 21 of 22, 38 of 39 and 48 of 50. Every FAIL is one of two expectations that reading only what the parser yields changes; in both, the check still exits 1 and names the added number at the line:
- round 4's link-label control (in the r4 to r7 runners) expects the `37` of `in [37](#b16c-attribution) blocks` not to be a measurement, because the link's target stood between the number and "blocks" in the raw text. A reader sees "37 blocks", and the check now names it a measurement;
- round 7's code-span control expects `` `CLOCK_DOMAIN 7<!-- -->ppm` `` named MARKUP. A reader sees the comment written out in the code, so the check reads it as text, names 7 UNCOVERED and refuses nothing.

Keeping either would need a character the reader does not see, or a markup pattern inside code, which items 1 and 2 remove. `tools/r8_check_controls.py` carries both forms with the round 8 expectation, and five of round 7's own self-probe forms are ruled to pass for the same reason: an autolink, a tag in a code span, a comment after a backslash, an unclosed tag, and angle brackets around a target that resolves. Please rule whether these expectations stand as changed.

Choices, stated on the page or in the packet:
- Code spans are read with a code mark at each end, which no rule treats as a phrase mark, so the code categories keep their patterns; they must also match inside one parser code span.
- The parser types footnotes `<unknown>`, reports a raw HTML block's end on the line before its start, and gives an autolink's text no start column. The check names footnotes by type number, ends the block on its own line, and places autolinked text at its end column.
- The check's own documentation was condensed to stay under the packet's 200 KB limit (199,434 bytes); the page states every rule.
- A disposable environment installed from `tools/markdown/requirements.txt` with `--require-hashes` ran everything. The gates' Markdown environment gives byte-equal check outputs.

**The check at `b522bb92`** exits 0:
- 1,867 rows, all equal to their receipts;
- 14,442 digits: 12,164 in claimed figures, 2,278 in 1,243 identifiers that count, 0 uncovered;
- 0 constructs refused.

The key scan finds no unread loop variable (569 loops). The round's outputs were made in a scratch copy, installed and regenerated byte-equal in the packet at the head. The probe records ran twice there, byte-equal. `tools/r8_figures_build.py` regenerates the check byte for byte from `tools/r8_figures_spec.py`.

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
| `tools/r8_check_controls.py` | 36,524 | `68f85edf41723ad7e87aa7dd4353182666022bb7286cdfa81cccbbe86fb864d6` |
| `controls/r8-controls.json` | 26,053 | `83f791b3819086772ce214262e148c0b8e5e6241f1895cb31acc09cecb7ed64b` |
| `controls/r8-controls-on-r7-check.json` | 26,077 | `ddea3af5efc65645fcadde07c5e38f7d7d70149956d7437ae4d6fcc3949a4b40` |
| `tools/r8_evidence_receipt.py` | 7,353 | `95c3ca5ea4f5ebda66ea3d5bbeb2584cb7dda9773182ac40b3b9aea4c6a1ebee` |
| `r8/evidence-receipt.json` | 59,920 | `1377b5d575bd0adb974a5cfc5f002a8e3d12d222e8b89ff22cd7f6f14709b502` |

The page hashes the controls runner, `controls/r8-controls.json`, `controls/r8-controls-on-r7-check.json`, the evidence tool and its receipt. It does not hash the check, its outputs, the authoring aids or the probe receipts, for round 3's reason.

Validation: all 14 gates rc 0 at the head, each to its own log, unpiped, on the physical /data path, with the Markdown gates in the pinned environment:
- `docs_check.py`, `check_doc_style.py`;
- `gen_toc.py --check` and `--verify-anchors`;
- `check_em_dash.py --base e8454e27`: 0 findings over 4,004 added lines;
- `check_doc_paths.py`, `ci_scope.py --selftest`;
- `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`;
- `git diff --check`, and `git diff --check c20c85bd HEAD`.

The same set ran rc 0 on the working tree before the commit.

**Per-run tables, as now stated (unchanged).** THD+N is the median, with the worst block in brackets. Each pair of values is 997 Hz / 9,973 Hz.

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

The packet (`629-b16-a603`, publication the manager's) holds HANDOFF.md and PR-BODY.md, each with a Round 8 section, and MANIFEST.sha256.
