[A603] REVIEW READY (B16, findings round 7)

Head: `295ba9d7f7dfed65e95002478ed6d55ccc14e580` on `629-b16-tone`, one new commit on `e91a62ee`, with no rebase and no amend. Not pushed. Refs #629.

This round is documents only, under the [round 7 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6128175910). There was no bench action: no lock, controller, board or instrument was touched. It answers [R625-6](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6128099316) and takes the suggestions of [R624-6](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6128169977). No figure on the page changed.

Changed:
- `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`:
  - a new subsection, "B16, round 7: no markup";
  - the section's eleven HTML-comment table markers replaced by blank lines, and one code block's four angle-bracket placeholders put in braces. No line before the new subsection moved, so R624-5's probe still reads lines 3008, 3174 and 3200, and R624-6's line 3244. The page renders as before;
  - "Where the packet is", now mapping round 6 to `author-r6/` (`e91a62ee`, published by `b616e7ea`) and naming round 7's `author-r7/`;
  - the introduction, Contents and opening pointers.
- `docs/findings/README.md`: the lane's row.
- No other file changed, and there is no DUT change.

| Item | Assignment | Now |
|---|---|---|
| 1 | No markup in the checked text | The check refuses, by line, any covered line holding `<` directly followed by a letter, `/`, `!` or `?`: every HTML tag, closing tag, comment (`<!-->` and `<!--->` included), processing instruction, declaration and CDATA section, and an autolink. It refuses inside code too, so its code reading cannot shelter a tag. Each refused line is named `MARKUP <document>:<line> <markup>`, and the check exits 1. The comment-stripping branch of `normalise` is removed; whitespace still collapses across line breaks. The only exception is a line equal byte for byte to a generator's marker: the four that `scripts/check_solution_docs.py` writes around its generated tables (`gen_toc.py` writes none; it finds its list by its heading). The section's own markup was replaced with plain Markdown, as above |
| 2 | Controls | `controls/r7-controls.json`: 50 of 50 PASS, round 6's 39 first with their code unchanged. The 11 new ones: R625-6's four forms where R625-6 put them (`<!-- -->`, `<!-->`, `<!--->`, and `<!-->` before furlongs); R625-5's two, where R625-5 put them; `7<span></span>ppm`; a comment in a code span; a former table marker put back; a generator's marker one byte off. Each fails with its line named MARKUP, and the added 7 UNCOVERED there. The last control, the exact marker, passes. Round 3's to 6's runners, unchanged: 5 of 5, 8 of 8, 22 of 22, 39 of 39. On round 6's check (`62bce479...`) and page, the 10 refusal controls FAIL (round 6's check exits 0 on the three short forms and both markers), and the 39 earlier and the exception PASS |
| 2 | Probes and page | R625-6's `probe_rendered_comment.py`, unchanged, under the repository's hash-locked renderer (cmarkgfm 2025.10.22, html5lib 1.1): statuses [0, 1, 1, 1, 1, 1], R625-6's required outcome; every comment form names MARKUP and `UNCOVERED 7` at line 3011. The probe itself exits 1, from its last assertion, which still states [0, 1, 1, 0, 0, 0], as R625-6 wrote. Round 6's six probes give what round 6 recorded: R624-4 8 of 8, R625-4 12 of 12, R625-3 7 of 7, R625-5 [0, 1, 1] (exit 0), R624-5's row probe LOCKED row MISMATCH, R624-5's escape probe 21 of 25. Also run: R625-6's `probe_followers.py` (its `code_directory_comment` and `malformed_comment` now fail, the other 20 unchanged); R624-6's `probe_r624_6_escapes.py` (every status as R624-6 recorded at `e91a62ee`); and R624-6's `probe_row3200_polls.py` (poll-count row MISMATCH). The unchanged page passes |
| 3 | Optional | R624-6-S1 taken as documentation: the approximate-quantity forms ("or so", "or more", "and a half", "to some", a bare unit after "of" or "and") and a list marker before a unit are stated limits, run as stated passes. R624-6-S2: the round 6 open question on R624-5's row probe is closed as answered (PR-BODY.md, Round 7 item 3); please record it |
| 4 | Texts | The page's round 7 subsection and the PR body state the rule. `r7/evidence-receipt.json`: `MANIFEST.json` at `b616e7ea` has 3,800 entries; all 84 section hash rows at `e91a62ee` equal their files in `author-r6/`; 646 of its 647 files equal round 6's own manifest (the 647th is that manifest) |

Choices, stated on the page or in the packet:
- Markup is refused inside code too. The check's code reading imitates the renderer, and a difference there could shelter a tag. The cost was the code block's placeholders, now in braces.
- The markers became blank lines rather than being deleted, because the reviews' probes read lines by number. Two blank lines render as one, and the gates pass.
- `SEP` and the closed list still look past a tag or a comment, only to decide whether a number is a measurement; they hide nothing, and any line with markup fails first.
- The exception control, and the self-probes' stated passes, compare with the unchanged page (same exit status, nothing new named) instead of requiring exit 0, because the page states their counts. Requiring exit 0 made a cycle that never settles.
- A file name the page cannot write: `probe_row3200_polls.py` reads as 3200 before the unit "polls", so the page names it R624-6's poll-count probe.

**The check at `295ba9d7`** exits 0:
- 1,834 rows, all equal to their receipts;
- 14,531 digits: 11,910 in claimed figures, 2,621 in 1,271 identifiers that count, 0 uncovered;
- 0 lines with markup.

111 further forms each meet their expectation (92 detected, 19 passing as stated). The key scan finds no unread loop variable. All 33 round 7 outputs re-run byte-equal at the head, and `tools/r7_figures_build.py` regenerates the check byte for byte from `tools/r7_figures_spec.py`.

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
| `tools/r7_check_controls.py` | 28,060 | `6a53a284ef5e70910282c3551285d82161d77412804c27830b7c684adc80c8fb` |
| `controls/r7-controls.json` | 18,201 | `5b782cd6734c2a637df54b968693dfd230e9210677778f5039d08eb37f39e576` |
| `controls/r7-rerun-r3-controls.json` | 1,579 | `4871ef3e84d940d91cc7938ca2ebaf3f904e39b74e21678aa03c602dae7e3560` |
| `controls/r7-rerun-r4-controls.json` | 3,115 | `f635748893ab28b258768f74aeede60a58b2ffa3a41abecac5af8b11ce3d1b60` |
| `controls/r7-rerun-r5-controls.json` | 8,153 | `cfba195f4842f725385f6a7c7de1449c780050d94b05495bdff0289de32a00e7` |
| `controls/r7-rerun-r6-controls.json` | 14,414 | `79e4edf8360106c43474d4bc77807c8beb1296f62fb27d211217c0e89b648946` |
| `controls/r7-controls-on-r6-check.json` | 18,212 | `f288208a13bff378280fd5f9e4cbb1e4e17a137790730bc1d007319d398fa6e3` |
| `tools/r7_evidence_receipt.py` | 6,919 | `a46c4ad554c6a1448319f7d1e26fdf6e01407aedb0d4868d1fb96bf66d8b099e` |
| `r7/evidence-receipt.json` | 52,808 | `23322f43d94c68a2dcc6da0412007596828c33bcb60fdb522f1a0f4fbf4a128f` |
| `tools/review-probes/probe_rendered_comment.py` | 3,299 | `22c38feb3cd3cac780bf5a2f299716b125047c9703df0b60dbe54beccc3aed57` |
| `tools/review-probes/probe_followers.py` | 2,817 | `6703a34616f606f2be81d943646a1022fd6e8070d273f4aaaa459cf29a0e451b` |
| `tools/review-probes/probe_r624_6_escapes.py` | 5,181 | `f4c9d523e6ea15f87e160768c61dc5229f51306dd1f4429984e7e380a27facc2` |
| `tools/review-probes/probe_row3200_polls.py` | 1,674 | `13a323fd7a4609309fb900b2c654d8bcbacaf21e8646a4b703e709990bb5c3e5` |

The page hashes the controls runner, its six controls files, the evidence tool and its receipt. It does not hash the check, its outputs, the authoring aids or the probe receipts, for round 3's reason.

Validation: all 14 gates rc 0 at the head, each to its own log, unpiped, on the physical /data path, with the Markdown gates in the pinned environment:
- `docs_check.py`, `check_doc_style.py`;
- `gen_toc.py --check` and `--verify-anchors`;
- `check_em_dash.py --base e8454e27`: 0 findings over 3,847 added lines;
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

The packet (`629-b16-a603`, publication the manager's) holds HANDOFF.md and PR-BODY.md, each with a Round 7 section, and MANIFEST.sha256.
