[A603] REVIEW READY (B16, findings round 9)

Head: `cb5ff79f1f69117efba353484851eceb620e5c92` on `629-b16-tone`, one new commit on `b522bb92`, with no rebase and no amend. Not pushed. Refs #629.

This round is documents only, under the [round 9 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132350672). There was no bench action: no lock, controller, board or instrument was touched. It answers [R624-8](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6132342798) and records the [decision](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132293481) that settles [R625-8](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6132288182). No figure on the page changed.

Changed:
- `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`:
  - a new subsection, "B16, round 9: source extents";
  - round 8's "Earlier expectations" paragraph and its runner list now record the decision; round 8's rule paragraph points to round 9;
  - "Where the packet is" maps round 8 to `author-r8/` (archived at `b522bb92`, published by `b0134c63`) and names round 9's `author-r9/`;
  - the introduction, Contents and opening pointers. Every edit before the new subsection keeps its line.
- `docs/findings/README.md`: the lane's row (round 9's rule).
- No other file changed, and there is no DUT change.

| Item | Assignment | Now |
|---|---|---|
| 1 | Real extent | `extents()` judges each node by the lines its source spans. An `html_block` ends on its literal's last line, never on the reported end; cmark-gfm reports blocks ending at a closing marker as ending a line early. A node spans its descendants; the parser ends struck text where it starts. A link or image starts a line higher per break in its text; the parser starts it on its last line. A construct off the allowlist is refused at the first covered line its source reaches. The same audit (`r9/parser-extents.json`, 37 of 37 cases) found two more ways positions fall short, both fixed. (a) A backslash line break, a link's or image's target, title or reference label over a line break, or a reference definition opening a paragraph makes the parser place everything after it on an earlier line, so a figure on the introduction's first covered line went unread. Such a block is now refused whole (`MARKUP ... paragraph`, with its own reason). (b) `scope()` split lines with `splitlines`, which also splits at U+000B, U+000C, U+001C to U+001E, U+0085, U+2028 and U+2029; lines are now counted as the parser counts them. Round 9's reader with round 8's rows on the page at `b522bb92` is byte-equal to round 8's outputs (`r9/reader-on-r8.json`) |
| 2 | Control | R624-8's `probe_r624_8_html_block_edge.py`, unchanged: `intro_pre_from_line_above_with_figure` DETECTED, `MARKUP 629_MEDIA_CLOCK_FOLLOWING_BENCH.md:18 html_block <pre>`. No case escapes, and every other case keeps its exit status and verdict; the heading and Contents cases now also name their block MARKUP. `controls/r9-controls.json`: 97 of 97 PASS, round 8's 73 unchanged and 24 new. The new controls are R624-8's case; the seven other raw HTML block kinds; struck text and an image across a covered boundary; the six misplacing breaks; and the eight separators. On round 8's check and page the 73 PASS and the 24 FAIL. The 13 earlier probes give round 8's readings, but for the line of a footnote that R624-7's `footnote_ref_and` appends after the page's end (4424, was 4274), which moves with the page. 156 further forms meet their expectations (122 detected, 34 stated passes). The unchanged page passes |
| 3 | Texts | The round 9 subsection, the index row and the PR body state the rule as it now holds. The decision is recorded where the earlier runners' outcomes are listed. Against the new check: 5 of 5, 7 of 8, 21 of 22, 38 of 39, 48 of 50 and 73 of 73. Each FAIL is a superseded expectation, and the runners are not reported as wholly green. R624-8-S1 is taken as text: the emoji shortcode and the link title are stated limits. Refusing them would flip two of R624-8's own cases, which item 2 keeps. `r9/evidence-receipt.json`: `MANIFEST.json` at `b0134c63` has 5,646 entries; all 98 section hash rows at `b522bb92` equal their files in `author-r8/`; 770 of its 771 files equal round 8's own manifest (the 771st is that manifest) |

Choices, stated on the page or in the packet:
- A block whose lines the parser misplaces is refused, not repaired: correcting the positions would mean imitating the parser.
- The check would have exceeded the packet's 200 KB limit. Row keys now name the two most-looped case pairs once (`BC`, `PT`) and a grade's tone pair (`tones(d)`), and round 8's control sums use `passed(d)`. These were replaced in string literals only, and no row's line, figure, receipt or value changed. The check's own documentation was condensed (199,529 bytes).
- `tools/r9_parser_extents.py` imports the check and is run with `-B`, so no bytecode lands in the packet.

**The check at `cb5ff79f`** exits 0:
- 1,909 rows, all equal to their receipts;
- 14,956 digits: 12,531 in claimed figures, 2,425 in identifiers that count, 0 uncovered;
- 0 constructs refused.

The key scan finds no unread loop variable (541 loops). The outputs, made in a scratch copy, were installed and regenerated byte-equal in the packet at the head (54 files); the probe records ran twice, byte-equal. `tools/r9_figures_build.py` regenerates the check byte for byte from `tools/r9_figures_spec.py`. All 14 gates are rc 0 at the head (`check_em_dash.py`: 0 findings over 4,156 added lines).

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
| `tools/r9_check_controls.py` | 43,115 | `11fc340920756e9e86dbe415f132b1eac204c8c5bcca4ce70114e5be09072c1e` |
| `controls/r9-controls.json` | 34,200 | `8b5ec97c1b2da15a1cdc9f0c14f3828c59dc47f2fa234999cf8f05118496a92a` |
| `controls/r9-controls-on-r8-check.json` | 34,224 | `9678b0a74ccaaed2b7b0e4a9ae4e6e2a6541619f4469931fb3dd964dbc06b930` |
| `tools/r9_parser_extents.py` | 6,592 | `d26cdd914e6da3916adcc64782e357bed4e22a18192adc5fffa5b2593a078885` |
| `r9/parser-extents.json` | 13,280 | `e165a7f72e18d38a0397f2736d8f99441f55bc6a8e56aaf6e9c1d226b4097a44` |
| `tools/r9_evidence_receipt.py` | 7,868 | `681dc44a5272671ccbce6d1f87cecbf2d812f4c3f47b3175d674f602881487fb` |
| `r9/evidence-receipt.json` | 65,166 | `98dbaee7054883eed16431ae4f2b7e3fd4aacbc6f1392655196c976683a517ec` |

Open: Direction B's INTERNAL mismatch control, lane B6's timed ratio for B-CRF and B-AAF, and #645, so #629 stays open.
