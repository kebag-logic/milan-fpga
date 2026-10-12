[A603] REVIEW READY (B16, findings round 6)

Head: `e91a62ee266e182a804ca1f45a0f18f715096563` on `629-b16-tone`, one new commit on `36190193`, with no rebase and no amend. Not pushed. Refs #629.

This round is documents only, under the [round 6 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6126774639). There was no bench action: no lock, controller, board or instrument was touched. It answers [R624-5](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6126709633) and [R625-5](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6126763696). No figure on the page changed.

Changed:
- `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`:
  - a new subsection, "B16, round 6: the closed list";
  - the covered text reworded within its lines wherever the closed list refused an identifier's follower (127 edits). No line before the new subsection moved, so R624-5's probe still reads lines 3008, 3174 and 3200. The three acceptance headings now read "acceptance of #629", and nothing linked to their old anchors;
  - "Where the packet is", now mapping rounds 4 and 5 (R624-5-F3);
  - R624-5-R1's exact wording in round 5's list of identifiers;
  - the introduction, Contents and opening pointers.
- `docs/findings/README.md`: the lane's row.
- No other file changed, and there is no DUT change.

| Item | Assignment | Now |
|---|---|---|
| 1 | R624-5-F1: the line-3200 LOCKED row | The row reads each case's count from that case's own receipt. If the counts differ it is a MISMATCH that names each, and its receipt column names both files. R624-5's `probe_row3200.py`, unchanged, reports `row3200_insensitive` false: the LOCKED row is MISMATCH, recomputed `bcrf 595, baaf 596`. A key scan finds no other key with an unread loop variable; on round 5's check it finds exactly this row |
| 2 | Normalise before matching | Every HTML comment is dropped before any token or category is matched, including one over several lines. Escapes and entities are decoded, and code is kept as written. Blocks are split at blank lines and every whitespace run collapses to one space. Every line number in the output is the source line |
| 3 | Identifiers by a closed follower list | An identifier counts only before: the end of the text; a mark that ends a phrase (. , ; : ! ? a table's bar, a spaced dash); a possessive; or "and", "or", "to", "of", unless a measurement follows that word. The check looks past spaces, dashes, slashes, emphasis and code marks, brackets, quotes and a link's target. Anything else makes the digits a measurement for a row. A code literal ends with its code word. `MEASURE` also reads the units' names. Controls, each failing and naming the figure as a measurement: per cent, decibels, hertz, kilohertz, parts per million and per billion, milli-, micro- and nanoseconds, msec, usec and nsec after `CLOCK_DOMAIN 7`; `B16 milliseconds`; `IEEE 1722.1 milliseconds`; `CLOCK_DOMAIN 7 furlongs`; and R625-5's comment over a line break, where R625-5 put it |
| 3 | Earlier controls, probes, page | `controls/r6-controls.json`: 39 of 39 PASS, round 5's 22 first with their code unchanged. Round 3's, 4's and 5's runners, unchanged: 5 of 5, 8 of 8, 22 of 22. On round 5's check (`2641412c...`) and page, all 17 new controls FAIL and the 22 earlier ones PASS. The probes, unchanged and checked against their published SHA-256: R624-4 8 of 8, R625-4 12 of 12, R625-3 7 of 7; R625-5's comment probe [0, 1, 1], exit 0; R624-5's escape probe 18 of its 19 `id+` forms, every ruling unit in words among them. 78 further forms each meet their expectation. The unchanged page passes |
| 4 | R624-5-F3 | `author-r4/` is archived at `61ae8641` and published by `b83e5d76`; `author-r5/` is archived at `36190193` and published by `a73ce5c4`; round 6 follows as `author-r6/`. `r6/evidence-receipt.json`: all 76 section hash rows at `36190193` equal their files in `author-r5/`, and 592 of its 593 files equal round 5's own manifest (the 593rd is that manifest) |
| 5 | R624-5-R1 | Applied verbatim on the page and in PR-BODY.md, Round 5 item 1 |

Choices, stated on the page:
- "Channels 2 and 3 carry" stays verbatim because R625-5's probe asserts it, and the list refuses "carry". Rows claim the two indices from every run's point summaries, each bound to the text around it, so R625-4's unbound continuation still fails.
- A digit is a measurement only when every identifier holding it is refused; this keeps round 5's planted control green.
- The colon stays a phrase end: adding it to the unit separator would read "round 4: packet" as a measurement. So `CLOCK_DOMAIN 7: ppm` passes, as does a full stop, a comma or a spaced dash before a unit. These are stated limits, and they run as self-probes recorded passing.

Open question: the assignment asks the unchanged `probe_row3200.py` to turn both line-3200 rows MISMATCH. It turns the LOCKED row MISMATCH. The second row is the window's poll count in "596 of 596"; the probe leaves it at 596, so it stays OK and correct. Making it fail would mean checking the LOCKED count twice. Line 3174's pair behaves the same, and R624-5's verification allows "or the check must otherwise fail at line 3200". A decision is needed if both rows must fail.

**The check at `e91a62ee`** exits 0:
- 1,790 rows, all equal to their receipts;
- 13,849 digits: 11,445 in claimed figures, 2,404 in 1,186 identifiers that count, 0 uncovered.

Its outputs re-run byte-equal, and `tools/r6_figures_build.py` regenerates the check byte for byte from `tools/r6_figures_spec.py`.

| Packet file | Bytes | SHA-256 |
|---|---|---|
| `tools/check_b16_figures.py` | 194,617 | `62bce479615dc54b107261b3f987434271bbab25e8acedd8bb39579b9be19274` |
| `r6/figures-rows.tsv` | 119,688 | `1e1d70550f1f36c75932c7868d87e9ff9f091bda08391c3e552a826adbda273b` |
| `r6/figures-coverage.tsv` | 77,339 | `e7649dcc4166596a2e83b1bdc2da045fb8d4d256174cc1059de538bc9808ab70` |
| `tools/r6_figures_build.py` | 5,229 | `cb8aab2fe2530178bfe5e004dbd396e59006d6fcf3d824b2eb19318c9473433f` |
| `tools/r6_figures_spec.py` | 158,415 | `64c5314e274cbbcc454f76f56f22d1238ba4459c54372b8aeabb05c55bbca7e4` |
| `tools/r6_check_controls.py` | 21,545 | `789a4f7ca25b8ef0d5b38bae9432d9f6be23434fe69ad20f0db9d7a80eb875de` |
| `controls/r6-controls.json` (39 of 39 PASS) | 14,414 | `a9709363266aaa05cc1a04b2d90cbbb095a426650a9f802325cbf3fe0335f043` |
| `controls/r6-rerun-r3-controls.json` (5 of 5 PASS) | 1,579 | `4871ef3e84d940d91cc7938ca2ebaf3f904e39b74e21678aa03c602dae7e3560` |
| `controls/r6-rerun-r4-controls.json` (8 of 8 PASS) | 3,115 | `cde959a0d411c360f6a2159196d22bc0311006bea9025a863e192b75b3d0d02b` |
| `controls/r6-rerun-r5-controls.json` (22 of 22 PASS) | 8,153 | `d3e0663e86195cf88e45353661cdd9464eb26d1f8622c378fc0abffaf667613f` |
| `controls/r6-controls-on-r5-check.json` | 14,432 | `8f03249c0ec24a6b018122b5be2d45780ab97d145d692d067abd43c2bb141943` |
| `tools/r6_evidence_receipt.py` | 6,586 | `71d32ba09f2ec1f4ab02bc9adf8085b66e96e5ca35c7243026b25ba10fe1f0bb` |
| `r6/evidence-receipt.json` | 46,562 | `bc3c0e91362f28ebcdc21d13c2e9d2ae875803da60e216b29e9227f79d35a58d` |
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

The page hashes the controls runner, its five controls files, the evidence tool and its receipt. It does not hash the check, its outputs, the authoring aids or the probe receipts, for round 3's reason.

Validation: all 14 gates rc 0 at the head, each to its own log, unpiped, on the physical /data path, with the Markdown gates in the pinned environment:
- `docs_check.py`, `check_doc_style.py`;
- `gen_toc.py --check` and `--verify-anchors`;
- `check_em_dash.py --base e8454e27`: 0 findings over 3,722 added lines;
- `check_doc_paths.py`, `ci_scope.py --selftest`;
- `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`;
- `git diff --check`, and `git diff --check c20c85bd HEAD`.

The same set ran rc 0 on the working tree before the commit.

**Per-run tables, as now stated (unchanged in this round).** THD+N is the median, with the worst block in brackets. Each pair of values is 997 Hz / 9,973 Hz.

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

The packet (`629-b16-a603`, publication the manager's) holds HANDOFF.md and PR-BODY.md, each with a Round 6 section, and MANIFEST.sha256.

