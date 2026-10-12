[A603] REVIEW READY (B16, findings round 5)

Head: `3619019350936d5af851933df0b5444ef8387e69` on `629-b16-tone`. There are two new commits on `61ae8641`, with no rebase and no amend:
- `f60132ca` changes the check and the page;
- `36190193` completes the page's list of separators and states the quoted-mention rule.

Not pushed. Refs #629.

This round is documents only, under the [round 5 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6125608002). There was no bench action: no lock, controller, board or instrument was touched. It answers [R624-4](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6125594896) and [R625-4](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6125596576). No figure on the page changed.

Changed:
- `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`:
  - a new subsection, "B16, round 5: every digit";
  - round 3's and round 4's paragraphs, which now describe those checks as they were;
  - the section's opening paragraph, which now points to rounds 2 to 5 (R624-4-S1, taken);
  - the introduction and Contents pointers.
- `docs/findings/README.md`: the lane's row.
- No other file changed, and there is no DUT change.

| Item | Assignment | Now |
|---|---|---|
| 1 | Account for every digit | Coverage is decided per digit. Every digit of the covered text, any Unicode digit or numeral, must lie in a figure a row claims, or in an identifier that a category binds to its keyword in the same sentence. The text is read in blocks, so the keyword binds across a line break; a match that crosses a table cell or a sentence's end counts for nothing. Any other digit is UNCOVERED, named with its line, its spelling (sign, leading point and exponent kept) and the text around it. TOKEN is unchanged and only finds row candidates, so a spelling it does not read can never be claimed. A row's figure must be the whole number written there. Open categories are tested: a path in code must name a packet file or a listed raw file, a link target must resolve to a heading of the page or to the repository's issues and PRs, and a list-item index must sit in a real ordered list |
| 2 | A measurement is never an identifier | A number followed by a unit is a measurement, and only a row covers its digits. Between number and unit there may be nothing, any whitespace run or line break (non-breaking, thin, zero-width), any hyphen, emphasis or code marks, a backslash, a double quote, an opening bracket, or an HTML entity, tag or comment. Units are read in either case, and "zero" counts. Stated exceptions: a resolving link target is an address, read at its heading. A number quoted on its own is a mention, which its closing quote does not join to a unit; no category takes it, so it needs a row either way |
| 3 | Controls | `controls/r5-controls.json`, 22 of 22 PASS. Rounds 3 and 4's eight run with their code unchanged. The new ones are on the attribution row: `26s`, `10dB`, `300ms`, `.5 ppm`, `-.25 ppm`, `7e2 ppm`, and `CLOCK_DOMAIN 7  ppm` with a double space, a non-breaking space or a hyphen. R625-4's continuation is applied where it stands. Also: a Unicode minus before a claimed figure, a path naming no file, an anchor naming no heading, and a category planted to match every number. Each fails and names its figure. Round 3's and round 4's runners, unchanged: 5 of 5 and 8 of 8. On round 4's check (`d2b51f85...`) and page, 11 new controls FAIL; the 3 that PASS (non-breaking space, hyphen, planted category) are forms round 4's guard already read (`controls/r5-controls-on-r4-check.json`) |
| 3 | The reviews' probes, unchanged | R624-4's `probe_escape_forms.py` 8 of 8, R625-4's `probe_coverage.py` 12 of 12 (exit 0) and R625-3's `probe_figure_coverage.py` 7 of 7 detected. Each is checked against its published SHA-256 (`r5/r624-4-probe-rerun.json`, `r5/r625-4-probe-rerun.json`, `r5/r625-3-probe-rerun.json`). 36 further forms are detected too (`r5/self-probes.json`) |
| 4 | Texts | The page and PR-BODY.md state the rule as it now is, and round 3's and round 4's claims about the check are narrowed to what those checks did |

Two notes:
- The quoted-mention rule keeps round 4's quoted control (`in "37" blocks`, expected not a measurement) green with its code unchanged.
- The rows table writes a receipt equal to the row above's as `^`. This keeps the check under the packet's 200 KB limit, and the rows output is unchanged in form.

**The check at `36190193`** exits 0:
- 1,749 rows, all equal to their receipts;
- 13,209 digits: 11,037 in claimed figures, 2,172 in 1,098 bound identifiers, 0 uncovered.

Its outputs re-run byte-equal, and `tools/r5_figures_build.py` regenerates the check byte for byte from `tools/r5_figures_spec.py`.

| Packet file | Bytes | SHA-256 |
|---|---|---|
| `tools/check_b16_figures.py` | 180,489 | `2641412c62d2c55c800b96dde53eecbd3983ec7d251dbab58eeda90312d73814` |
| `r5/figures-rows.tsv` (one line per row) | 115,411 | `77ac9643dd311bf001d58f1e8cb2e4f4b70355bdb58017f81533e2b1a8013b11` |
| `r5/figures-coverage.tsv` (each identifier and its category) | 71,176 | `613dea0c155e54b4abdf0b757dbc3986d51bbadcc6f9faf324cc83a682fe2ed9` |
| `tools/r5_figures_build.py` | 4,767 | `b7d95befe349e1f15ea4cc3ef027afd3e78ece53a80a347d7a86e4d0509af0e6` |
| `tools/r5_figures_spec.py` | 155,187 | `725dbe2c0d40bce8de478b3a64300d7387bb643dad78d77b1ec09d7883dd8565` |
| `tools/r5_check_controls.py` | 16,186 | `bf84a387ebdaae6fee5dc93f9da5b9b06bcb827281ff1c51eac3b7da17a8aa2e` |
| `controls/r5-controls.json` (22 of 22 PASS) | 8,154 | `c22a199aa34ed8fb4d01fe238bf601d45f519cec484fe3035aee833b179a0188` |
| `controls/r5-rerun-r3-controls.json` (5 of 5 PASS) | 1,579 | `4871ef3e84d940d91cc7938ca2ebaf3f904e39b74e21678aa03c602dae7e3560` |
| `controls/r5-rerun-r4-controls.json` (8 of 8 PASS) | 3,116 | `a79d24b9c9e272960eb1ffe528c5ada294571f5a5a63fbe217e8d2c344e4964d` |
| `controls/r5-controls-on-r4-check.json` | 8,165 | `2569e99d4283036b2bc38868812721621330b86b8dbfa735e5ad08fad544391b` |
| `tools/r5_probe_reruns.py` | 3,526 | `893b97d6a71c6a78df33af38ecbad2c7ce3d1f21400b9a930869cd8aeb3a84c2` |
| `r5/r624-4-probe-rerun.json` | 4,754 | `45e4e2043b8629755d257b2a3024270470638a43a98660da625203d2801f0034` |
| `r5/r625-4-probe-rerun.json` | 12,204 | `cf07527318d74e6cf844154d2da5878c8e0fa98983b896729a93598ec2680bda` |
| `r5/r625-3-probe-rerun.json` | 4,978 | `5c756dd1006338951709df7bffac24cf4aa6a6e169892105e7261382f464afb7` |
| `tools/r5_self_probes.py` | 6,083 | `c936663d25276c463a946d50b5dbeb59dd80cce27c83e22bf53b38d61c9d981b` |
| `r5/self-probes.json` | 11,617 | `f8d34c0d5a6c17a29e73525ef096d0ffadb32f1f6e53c574123fb1ff9cc77e1c` |

The page hashes the controls runner and its four controls files, but not the check, its outputs, the authoring aids or the probe receipts, for round 3's reason.

Validation: all 14 gates rc 0 at the head, each to its own log, unpiped, on the physical /data path, with the Markdown gates in the pinned environment:
- `docs_check.py`, `check_doc_style.py`;
- `gen_toc.py --check` and `--verify-anchors`;
- `check_em_dash.py --base e8454e27`: 0 findings over 3,565 added lines;
- `check_doc_paths.py`, `ci_scope.py --selftest`;
- `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`;
- `git diff --check`, and `git diff --check c20c85bd HEAD`.

The same set ran rc 0 on the working tree before each commit, and at `f60132ca`.

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

The packet (`629-b16-a603`, publication the manager's) holds HANDOFF.md and PR-BODY.md, each with a Round 5 section, and MANIFEST.sha256.
