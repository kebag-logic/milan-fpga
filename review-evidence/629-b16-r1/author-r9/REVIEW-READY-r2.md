[A603] REVIEW READY (B16, findings round 2)

Commit: `35e332b6be3de2b36c4aec0f1d0bc9f390447b74` on `629-b16-tone`, one new commit on `e20fd282` (no rebase, no amend). Not pushed. Refs #629.

This round is documents only, under the [round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119316763). There was no bench action: no lock, controller, board or instrument was touched. It answers [R624-1](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119236428) and [R625-1](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119311570).

Changed:
- `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`: corrections in the B16, B16b and B16c subsections, and a new subsection, "B16, round 2: reduced receipts". The new subsection holds the corrections table, the receipts, the extraction commands, the twelve tone-source read hashes and the round's file hashes.
- `docs/findings/README.md`: the lane's row.
- No other file changed, and there is no DUT change.

The packet gains:
- `r2/`: two poll receipts and two poll traces, the source receipt and B0's receipt;
- three extraction tools under `tools/`;
- `controls/r2-controls.json`: 6 of 6 PASS on altered copies;
- `RAW-ARTIFACTS.json` now also lists the twelve retained tone-source reads, with their sizes withheld.

Validation: all 14 gates rc 0 at the head, each to its own log, unpiped, on the physical /data path, with the Markdown gates in the pinned environment:
- `docs_check.py`, `check_doc_style.py`;
- `gen_toc.py --check` and `--verify-anchors`;
- `check_em_dash.py --base e8454e27`: 0 findings over 3,179 added lines;
- `check_doc_paths.py`, `ci_scope.py --selftest`;
- `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`;
- `git diff --check`, and `git diff --check c20c85bd HEAD`.

The same set was rc 0 on the working tree before the commit.

| Item | Finding | Now |
|---|---|---|
| 1 | R624-1 F1 = R625-1 F3: figures | B0's floor medians are -123.98 dB (997 Hz) and -123.95 dB (9,973 Hz); `pts3` is -123.98 dB on both. The degraded runs are 0 to 18, 28 to 31, 43 to 44, 46 to 54 and eleven later runs. The B0 recording starts at about 06:38:05.2: the capture command at 06:38:03.2 plus the 2 s playback lead, 26 s after the 06:37:39.2 binds. The same lead was also found in `pts2`, whose McASP0 10 s start at about 06:28:31.5; corrected too |
| 2 | R624-1 F2 = R625-1 F4: lane B6's four terms | Stated for both B-CRF and B-AAF. LOCKED: met. Counted ratio within 0.5 ppm: met. 0 listener discontinuities: met. Timed ratio's interval holds zero: NOT RUN. The counted ratio stands in as evidence only, and no recorded decision replaces the term. Applied in the B16c table, the following record, the acceptance row, the limits and the index |
| 3 | R625-1 F1: attribution | 131 stays the count at (c). 23 of the 131 lie inside the taps' 34.1 s (whole blocks 0 to 33) and are shown in (a) sample for sample. The other 108 lie beyond the taps, including the worst block of each tone, and are labelled inference. The same applies in the B16b table, the attribution table, the limits, B16c's "Against B0", the index and PR-BODY.md |
| 4 | R625-1 F2 (and R624-1 S2): reduced receipts | Published; see below. Every figure they carry reproduces, and two statements were narrowed: B16b's state comparison, and B16's other source outputs |
| 5 | R624-1 R2 = R625-1 R2 | The first counter mark is now 20 s after the DUT's set, about 6 s before the window. The table header is "before the window and near its end"; the MEDIA_RESET and CLOCK_DOMAIN paragraphs name the marks |
| - | R1 (title) | For the manager: the reviewers' title is in PR-BODY.md |
| - | S1 (census "44 of 45 reads") | Not taken: it is optional, and the existing count is true under the tool's definition |

**The reduced receipts.** Each receipt is bound to the raw SHA-256 it reads.

| Receipt | Bound to | What it carries |
|---|---|---|
| `r2/bcrf-poll-receipt.json`, `r2/baaf-poll-receipt.json`, with traces | The raw polls `9cfc79bb...` and `476a0077...`. The tool refuses a raw poll whose size or hash differs from the run's own record, and recomputes the published poll summary equal | Per span: servo states, trim, rates, `AAFM_STAT`, `SLIP_LB` and `SLIP_TDM` minimum and maximum; every `SLIP_LB` step with its two polls and servo states |
| `r2/source-receipt.json` | The twelve tone-source reads (hashes in the new subsection) and the private class map's hash | Meter levels per role, output settings, and the four state comparisons with neutral classes. No control, address, channel or clock value is named |
| `r2/b0-2-receipt.json` | Packet files only | Floor medians, degraded runs, overlap boundary, inside and beyond counts and worst blocks, and the recording start |

**Per-run tables, as now stated.** THD+N is the median, with the worst block in brackets. Each pair of values is 997 Hz / 9,973 Hz.

| Run | (c) at the floor | (c), all blocks | Degraded at (c) | Inside the taps' 34.1 s, shown | Beyond, inference |
|---|---|---|---|---|---|
| `b0-2`, B0 | 169 blocks; -123.98 (-123.91) / -123.95 (-120.18) dB | -123.95 (-100.47) / -122.80 (-80.48) dB | 131 of 300, no discontinuity | 23: blocks 0 to 18 and 28 to 31, worst -100.61 / -80.63 dB | 108: blocks 43 to 251 in thirteen runs, worst -100.47 / -80.48 dB |

| Lane B6's term | B-CRF | B-AAF |
|---|---|---|
| Servo LOCKED | Met: 596 of 596 window polls; 2.66 to 3.16 s after the set | Met: 596 of 596; 6.68 to 7.18 s |
| Counted ratio within 0.5 ppm | Met: 0 net steps in 14,583,391 frames, below 0.07 ppm | Met: 0 net steps in 14,585,924 frames |
| Timed ratio's interval holds zero | NOT RUN | NOT RUN |
| 0 listener discontinuities | Met: 0 at (c) and (d) | Met: 0 at (c) and (d) |

| Case, window polls | Trim | Followed rate | Servo word | `SLIP_LB` steps, against the DUT's set |
|---|---|---|---|---|
| B-CRF | -6.125 to -6.000 ppm | CRF sink +10.600 to +10.652 ppm | `0x...0034` 580, `0x...0074` 16 | Five between the binds and the set, servo IDLE; one at 2.08 to 2.66 s in ACQUIRE; none after LOCKED; 162 to 174 dups |
| B-AAF | -6.125 to -6.000 ppm | AAF meter +10.600 to +10.631 ppm; `AAFM_STAT` `0x001e0007` at all 596 | `0x...0034` 584, `0x...0074` 12 | Five between the binds and the set, servo IDLE; two at 2.08 to 2.65 s and 5.10 to 5.68 s in ACQUIRE; none after LOCKED; 174 to 188 dups |

| State comparison | Entries | Both hold | Differ |
|---|---|---|---|
| B16, 05:48 against 06:01 | 2,262 / 2,262 | 2,262 | 0 |
| B16b, 06:23 against 06:50 | 2,262 / 1,255 | 1,255 | 4. Two are settings: the clock setting and an unused output's level. Two are monitoring-mix inputs that differ only in which messages each read caught, all at minus infinity |
| B16b 06:50 against B16c 07:48 | 1,255 / 1,351 | 618 | 0 |
| B16c, 07:48 against 08:03 | 1,351 / 1,248 | 668 | 2: monitoring-mix inputs, which messages caught, all at minus infinity |

In every meter read during the tone, the playback reads -20.0 dBFS. The documented pair of outputs reads -38.5 dBFS leaving and -20.0 before its -18.5 dB setting. The second pair reads -14.0 leaving, -20.0 before, at a +6.0 dB setting. No other output reads above -135.2 dBFS.

Acceptance criteria (round 2): items 1 to 5 met, with the evidence above and in the new subsection. On #629: Direction B is graded for B-CRF and B-AAF, with three of lane B6's four terms met and the timed ratio NOT RUN. The INTERNAL mismatch control is NOT RUN. #645 is open. Refs #629.

Open risks/questions:
- Lane B6's timed ratio for B-CRF and B-AAF needs a mode with McASP0's timing sampler, or a recorded decision.
- Direction B's INTERNAL control needs the peer-on-INTERNAL exception for B0.
- The raw files and the class map remain private. Their hashes are in the packet.
