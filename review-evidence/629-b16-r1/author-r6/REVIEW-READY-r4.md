[A603] REVIEW READY (B16, findings round 4)

Commit: `61ae86419c50f2707d6ee1dc5433bc6dee66ce84` on `629-b16-tone`, one new commit on `0782c55f` (no rebase, no amend). Not pushed. Refs #629.

This round is documents only, under the [round 4 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6121193402). There was no bench action: no lock, controller, board or instrument was touched. It answers [R624-3](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6121093801) and [R625-3](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6121186527).

Changed:
- `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`:
  - a "Where the packet is" paragraph in "B16: artifact hashes", and the section's opening pointer to it;
  - round 3's coverage paragraph, now true of round 3's check;
  - a new subsection, "B16, round 4: packet and coverage";
  - the census stated as reads in lane B16's five census statements;
  - seventeen rewordings;
  - the introduction and Contents pointers.
- `docs/findings/README.md`: the lane's row.
- No other file changed, and there is no DUT change.

| Item | Finding | Now |
|---|---|---|
| 1 | R624-3-F1: where the packet is | Branch `629-b16-review-evidence`, pinned at `b84584e4ccb069248909f0fdeb7f8b72a1c41ae4`. The packet label `629-b16-a603` maps to `review-evidence/629-b16-r1/author-r1/` (lanes B16, B16b and B16c, page at `e20fd282`), `author-r2/` (`35e332b6`) and `author-r3/` (`0782c55f`); round 4 follows as `author-r4/`. `MANIFEST.json` there (SHA-256 `8d417d54b13a264484bfcb0b69f8a643e5cd3bf2819294cea201242a2f67f034`, 1,680 entries) binds each file's original and published hash with a `path_redacted` flag. 27 author files are path-redacted (1, 9 and 17 by round). All 66 packet-file rows on the page at `0782c55f` equal both hashes and the published file in `author-r3/`, and none is redacted. Every new figure, hash and commit has a row reading `r4/evidence-receipt.json`, written by `tools/r4_evidence_receipt.py` from the repository's object store |
| 2 | R625-3-F1: figures inside quoted phrases and link labels | No whole-link or whole-quote exemption. Identifier categories only, each bound to its keyword: commits (listed), clause numbers, descriptor, channel, step, round and list-item indices, the packet's label and branch name, and a link's target. Every other category is gone: its tokens have rows or were reworded. A measurement guard: a token followed by a unit can only be claimed by a row. Tokens now include 40-character commits and the tens |
| 2 | Controls | `controls/r4-controls.json`, 8 of 8 PASS: round 3's five, code unchanged; R625-3's quoted and linked forms, each with a unitless number in the same form; and a category planted to match every token, with the figure in plain text. Each fails the check and names the figure UNCOVERED; the planted case names it a measurement. Round 3's runner, unchanged, against the new check: 5 of 5 (`controls/r4-rerun-r3-controls.json`) |
| 3 | R625-3-S1 (optional) | Taken: "44 of 45 reads equal, the census's start record aside", each count recomputed from both census files by `census_cmp.py`'s rule and checked against the comparison file's counts less the start record |

Note: the round-1 directory on the evidence branch is `author-r1/`, not `author/` as the assignment and R624-3 wrote. The page states the real name.

**The check at `61ae8641`** exits 0: 1,727 rows, all equal to their receipts; 1,874 tokens, 147 in identifier categories, 0 uncovered.
- Its outputs re-run byte-equal, and `tools/r4_figures_build.py` regenerates the check byte for byte from `tools/r4_figures_spec.py`.
- The same controls run against round 3's check (`13d7a0de...`) and page give 5 PASS and the three new FAIL (`controls/r4-controls-on-r3-check.json`). So each new control fails for the defect it targets.
- R625-3's own probe, run unchanged against the new check: 7 of 7 detected, its quoted and linked forms included (`r4/r625-3-probe-rerun.json`).

| Packet file | Bytes | SHA-256 |
|---|---|---|
| `tools/check_b16_figures.py` | 192,835 | `d2b51f85b10f33427396044703f20820df64b7b57601fe25f498a44e28f17edd` |
| `r4/figures-rows.tsv` (its output, one line per row) | 113,578 | `fd7eef805484d5827f899e1a35b913f84f7d113879eda1e314fd0ba478c96927` |
| `r4/figures-coverage.tsv` (every token a category covers) | 8,647 | `a184d9ab7f31102695a67b1846d2928dca6de9441f3254ba6411e0c86844c1c1` |
| `tools/r4_figures_build.py` | 4,673 | `ba3085a75a99d17009fda6580adf90887db21c8c64f50144ce8d6fd173688de0` |
| `tools/r4_figures_spec.py` | 152,849 | `ee2fef18f24849f255f90743bfa8375dda42855a8ca00297a5f3f45a6729c18d` |
| `tools/r4_check_controls.py` | 10,379 | `54d2e1df507cb1b8c8b77214942f49cfcbe3a524f4e52b882ae124384e6d4e0f` |
| `controls/r4-controls.json` (8 of 8 PASS) | 3,116 | `d01b56caf89cf99604dc32ce2d69118618fae457074c7c723eb792ef890b68e5` |
| `controls/r4-rerun-r3-controls.json` (5 of 5 PASS) | 1,579 | `a0c9a8ed6f768b70208c1c28e6d37c402444a57b2877b882f175c5db4586ce87` |
| `controls/r4-controls-on-r3-check.json` | 3,576 | `90cba016cf3d19974fc88efb86f98226ef2c4d712cf7ebf2b361c9cc96b545f0` |
| `tools/r4_evidence_receipt.py` | 5,191 | `7dca8a53f24c1e7330ed2e154e41f4e30a47012171d68c2a80c138c2834c6164` |
| `r4/evidence-receipt.json` | 38,177 | `1a433cd27edb2632a92e7abbc1f4eebca9ad4d15fae55f23d98a48647ee9805a` |
| `r4/r625-3-probe-rerun.json` | 4,201 | `0dcf575d7ddb381d3353ac4b959992dacee8b5fd923baa5c0a0a1b8bf67ac8db` |

The page hashes the evidence receipt and its tool, the controls runner and its two controls files, but not the check, its outputs or the authoring aids, for round 3's reason.

Validation: all 14 gates rc 0 at the head, each to its own log, unpiped, on the physical /data path, with the Markdown gates in the pinned environment:
- `docs_check.py`, `check_doc_style.py`;
- `gen_toc.py --check` and `--verify-anchors`;
- `check_em_dash.py --base e8454e27`: 0 findings over 3,427 added lines;
- `check_doc_paths.py`, `ci_scope.py --selftest`;
- `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`;
- `git diff --check`, and `git diff --check c20c85bd HEAD`.

The same set ran rc 0 on the working tree first.

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

The packet (`629-b16-a603`, publication the manager's) holds HANDOFF.md and PR-BODY.md, each with a Round 4 section, and MANIFEST.sha256.
