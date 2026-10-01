# B6 round 2 ([A480]) handoff

Refs #629, PR #630 (bench lane B6, the dev `ec0cc0c1` image). Round 2: docs only, no bench access.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5932539168
- Round-1 reviews answered: PR #630 comments 5932376922 (R426-1, three MINOR) and 5932505979 (R427-1, three MINOR).
- Manager's PR #630 comment read: 5932531424 (self-test evidence, archive tip `ff542b62`, A2 tracked on #74, PR body in the template). #74 comments read: 5932380322 (A2 root cause) and 5932538721 (the DRP config-mismatch observation).
- Read-only inputs: the round-1 packet (`b6-a477`), the round-1 raw captures (local, never copied), the review packets of R426-1 and R427-1, and the evidence archive at `ff542b62ae79f283b80b7945dd76110f986b0737` (read with `git show` only).

## State

**DONE, REVIEW READY.**

- Commit `e3f28f2f69343b54844ddfea368ef4cdd03facb6` on `b6-bench-1001`, parent `b5e9242e2e1911bb2bac11221527f8965a4ccaef`. One-line subject, no body, no trailers. It changes one file: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, +143 / -17 lines. The worktree is clean.
- **Not pushed.** No PR edit, no merge. The live PR #630 head is still `b5e9242e`; the manager pushes `e3f28f2f` and applies `PR-BODY.md`.
- Every measurement table is byte-identical to `b5e9242e` (15 of 15). No rule, verdict or measured figure changed.
- Gates at `e3f28f2f`: every invocation rc 0 (`gates/gates.txt`).
- Token scan of the diff, the page at the head, the commit message and this packet: no private name. The only two pattern hits are four-part clause numbers that the IPv4 pattern matches in the PR body's references, carried unchanged from the live body.
- Posted on #629: `[A480] TAKEN` (https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5932556696) and `[A480] REVIEW READY` (https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5932914235). Each readback equals the posted text but for one trailing newline. No existing comment was edited or deleted; nothing else was posted.

## The change, by assignment item (page lines at `e3f28f2f`)

| Item | Finding | Page lines | What changed |
|---|---|---|---|
| 1 | R426-1 F1, R427-1 F2 | `629_MEDIA_CLOCK_FOLLOWING_BENCH.md:220-264` (Method, "What the attribution can absorb") | The five absorption paths, each with its A1 and B CRF check (below) |
| 1 | R426-1 F1 | `:492-499` (The capture path) | The two 48 n + 13 skips named: A0's 1,165-frame skip and a 109-frame skip in an A2 stale-replay cluster; A0's 519 and A2's 494 listener drops may each be one low, each counted ratio about 0.03 ppm low |
| 1 | R426-1 F1, R427-1 F2 | `:555-559` (Limits) | The five paths, the one residual (a drop at the very edge of A1's 12.4 s loss), and the A0 and A2 qualification |
| 2 | R426-1 F2, R427-1 F1(a) | `:155-159` (Method, "Cases") | Windows open 20 s after the last bind or set and its read-back, in 0.5 s steps (20.0 to 20.5 s); B CRF 20.5 s after the set, 14.0 s after the servo first read LOCKED |
| 3 | R426-1 F3, R427-1 F1(b) | `:507-516` (The capture path) | Listener events: 497 of 520 (A0), 135 of 674 (A2), 485 of 507 (B INTERNAL) have a measurable rise, at most 1.0 ms with no exception; A1 and B CRF have none. The 2.7 ms and 177 ms exceptions are A2 DUT beat repeats within 0.4 s of its 13.3 s stall |
| 4 | archive pointer | `:603-624` (Artifact hashes, "Where the packet is") | Branch `b6-review-evidence` at `ff542b62...`; `b6-a477` maps to `review-evidence/b6-r1/author/`; the twelve label-masked files' hashes are `original_sha256`; the two reproduction commands from the PR body, with their expected results |
| 5 | R426-1 S4, R427-1 S3 | `:421-423` (A2), `:562-568` (Limits) | A2's root cause tracked on #74 (comment 5932380322); the DRP config-mismatch bit observed and not analysed, recorded on #74 (comment 5932538721) |
| 6 | R426-1 S2; R427-1 S2 | `:93-109` (Method, "Shakedown runs") | The three shakedown runs (`smoke-a0-clkparse`, `smoke-a0`, `smoke2-a0`) and the bridge legs stopped by process ID and restarted |
| 6 | R427-1 S1 | `:316-322` (Tool controls) | The floor checked without the tool: DFT within 0.0001 dB, analytic -146.05 dB; a 3 dB band error would show |
| 6 | R426-1 S1 | `:384-390` (A0) | 17.2 ppm for the 519 drops, 17.1 ppm net of the insert (the verdict table's figure); lane B5's 16.46 ppm with a link to PR #628 |
| 6 | R427-1 S2 | `:379`, `:409-410` | Comb residual "within 1.82 frames"; `hdl/ieee1722/crf/KL_crf_tx.sv` beside the datapath port comment |
| 6 | R426-1 S3, R427-1 S2 | `:460-462` (B CRF) | LOCKED at the three in-window reads, 5 s, 315 s and 615 s in, `SLIP_TDM` static |

Contents descriptions for Method and Artifact hashes (`:40`, `:48`) name the new passages. No heading was added.

### Item 1, the five paths and their checks (receipts/attribution-checks.txt)

| Path | A1 | B CRF | Elsewhere |
|---|---|---|---|
| 1. One-frame drop merged with a capture loss (48 n + 13; a repeat 48 n + 11) | 48 of 50 capture-path skips 48 n + 12; the 23,880 replay edge cancels exactly; the 12.4 s loss (12 loops + 18,626) has no size pattern: a drop at its very edge cannot be excluded and is indistinguishable from lost audio | 38 of 38 skips 48 n + 12; both replay steps exactly -24,000 | A0 cluster 0's 1,165 and A2 cluster 15's 109 are 48 n + 13; no 48 n + 11 anywhere |
| 2. Repeat within 50 frames of a beat tooth | 315 members, one per tooth, spacing >= 93,989; every member >= 75 capture frames from a capture-path event; 7 missing teeth all inside cluster 13 (the 12.4 s loss) | no one-frame event of any kind | A0, B INTERNAL: one member per tooth, none missing; A2: 6 missing teeth all inside cluster 55 |
| 3. Spoiled rise accepted on gap + size | 0 clusters | 0 clusters | A2: clusters 17 and 56 |
| 4. 2-to-48-frame skip, no stall (band to about 98 frames with the 1.0 ms floor step) | smallest loss 60; 4 clusters under 98 frames, each one 60-frame skip, gaps 14.9 to 59.8 ms | smallest loss 60; 3 clusters under 98 frames, each one 60-frame skip, gaps 16.2 to 18.7 ms | no capture-path cluster under 60 frames in any case |
| 5. Gap-only branch (no size check) | 2 clusters, every skip 48 n + 12 | none | read positions meeting the 11 ms gap test: A0 16.3 %, A1 23.0 %, A2 27.5 %, B INTERNAL 24.5 %, B CRF 16.0 % |

Notes for review:

- **Path 4 is wider than the assignment's wording.** A zero rise matches any skip up to 48 frames. With the read-time floor's measured 1.0 ms step on no-loss events, a no-loss skip up to about 98 frames can match. The page says so. The 60-frame clusters' rises, 0.99 to 1.00 ms, sit at that step, so for those seven clusters in A1 and B CRF the read gap and the 48 n + 12 size carry the attribution.
- **Path 5's figure is measured, not estimated.** R427-1 estimated 9 to 28 % from stall counts. Re-derived from the raw read times with the grader's own window (60 reads before through 2 after, gap >= 11 ms), the share is 16.0 to 27.5 %. The page states "16 to 28 %".
- **Path 1 leaves one residual in A1.** Nothing in the record can tell a one-frame drop at the very edge of the 12.4 s loss from one more lost frame. The page states this as the one exception, and notes that lost audio and any event inside it are already left out of every figure.
- **Path 2 placement.** A listener repeat could stand in for a beat only at a tooth whose beat was hidden in lost audio, which puts it within about 52 frames of a capture-path event. A1's nearest member is 75 capture frames away.
- The round-1 `HANDOFF.md:92` in the archive repeats the misstated B CRF window rule. It is archived evidence and stays unchanged.

### Item 2, the B CRF window (receipts/window-check.txt)

From `runs/<case>/events.jsonl`: every window opened 20.008 to 20.497 s after the last bind or set (the tool polls in 0.5 s steps after taking `t_set` behind the set's read-back, `run_b6.py` around lines 513-530). B CRF: the servo-lock read came 6.493 s after the set, and window-start came 14.004 s after it. In-window reads at 5.2, 315.4 and 615.2 s all read state 4, LOCKED, with `SLIP_TDM` 0xc066 throughout.

### Item 4, the archive (receipts/archive-check.txt, receipts/repro.txt)

- `ff542b62` is the remote tip of `b6-review-evidence`.
- 291 of 291 manifest files re-hash to `published_sha256`; 29 are label-masked.
- Page hashes at `e3f28f2f`: 54 of 54 resolve, 33 to `original_sha256` (12 of them label-masked), 21 to `RAW-ARTIFACTS.json`.
- From files taken out of the archive with `git show`, `b6_tone.py` regenerates the loop at `566d3dfa...5588`, and `b6_thdn.py controls` rc 0 with `ALL_PASS True` and `cmp` silent against the archived `controls.json`.

### Item 6, R427-1 S1 (receipts/floor-check.txt)

A 48,000-point DFT of the loop, the band summed with the fundamental (and, for SNR, the harmonics) masked out, gives 997 Hz THD+N -146.065 dB and SNR 146.067 dB, and 9,973 Hz -145.993 and 145.993 dB. That equals the published floor within 0.0001 dB. The analytic floor is 146.051 dB. A first version summed the band and subtracted the fundamental, which lost the residual to float64 cancellation (a 0.07 dB error at 9,973 Hz). It was corrected before any figure was used. No control was added to `b6_thdn.py`: the tool and `controls.json` are hashed evidence of the graded runs, so the suggestion is answered on the page and retained as a tool control.

## Byte-identical table proof

- `receipts/table-identity.txt`: `tools/table_identity.py` splits both commits' page into tables (maximal runs of lines starting with `|`). All 15 tables at `b5e9242e` equal the 15 at `e3f28f2f` byte for byte, in order, with none added or removed. RESULT PASS.
- `receipts/table-diff.txt`: every table line of both commits (161 lines, 16,010 bytes each, the same sha256 `540ab528...d847`); `diff` rc 0 with empty output.
- The PR body's How to validate step 2 repeats the check with `git show`, `grep` and `cmp`; it was run as written, `cmp` rc 0.

## Token scan

- `tools/token_scan.py` loads the round-1 private redaction map (27 literal and 5 regex entries) and two token lists. The lists cover tool and model names, account names, home paths, capture-layout tokens (channel counts, indices and the byte sizes that divide to them), interface names, serial devices, MAC and IPv4 patterns, USB bus, ID and product strings, and instrument and switch brands. All three stay outside this packet and are never printed.
- Scanned: the round-2 diff `b5e9242e..e3f28f2f`, the page at `e3f28f2f`, the commit message, and every file in this packet, including `PR-BODY.md`, this file and the REVIEW READY text. Result (`receipts/token-scan.txt`): two hits, both the IPv4-shaped pattern on four-part Milan and IEEE 1722.1 clause numbers in the PR body's Authoritative references, carried unchanged from the live body. They are not addresses; no real hit. A planted-token self-test hits as expected.
- A read of the diff by hand finds no host, peer, switch or instrument name. It also finds no wiring, channel map, stream count, capture layout or clock topology. The new text names roles only ("the reference peer", "the capture read times").

## Gates (gates/)

Run at `e3f28f2f` from the physical lane worktree path, each output to its own file, never piped. Markdown gates used the pinned environment (md-venv `40cdefe08ebd`).

| Gate | rc |
|---|---|
| `docs_check.py` | 0 |
| `check_doc_style.py` | 0 |
| `gen_toc.py --check` | 0 |
| `check_em_dash.py --base ea3fb388` | 0 |
| `check_doc_paths.py` | 0 |
| `ci_scope.py --selftest` | 0 |
| `check_baremetal_only.py --check`, `--selftest` | 0, 0 |
| `check_feature_status.py --self-test` | 0 |
| `git diff --check`; `ea3fb388 HEAD`; `b5e9242e HEAD` | 0, 0, 0 |
| `gen_toc.py --verify-anchors` | 0 |

## Reproduce (placeholders, not host paths)

```sh
python3 tools/attribution_checks.py <round-1 packet> <round-1 raw dir>
python3 tools/window_check.py <round-1 packet>
python3 tools/floor_check.py <dir with the archived b6_tone.py> <archived controls/controls.json>
python3 tools/archive_check.py <evidence clone> ff542b62ae79f283b80b7945dd76110f986b0737 <page at e3f28f2f>
python3 tools/table_identity.py <lane clone> b5e9242e2e1911bb2bac11221527f8965a4ccaef e3f28f2f69343b54844ddfea368ef4cdd03facb6 docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md
python3 tools/token_scan.py <private map> <regex tokens> <name tokens> <files...>
```

`attribution_checks.py` needs the raw `grade-full.json` and `cap-ts.bin` of each case, which stay local. Their SHA-256 values are on the page and in the receipt's header.

## Open for the manager

- Push `e3f28f2f` to `b6-bench-1001` and apply `PR-BODY.md` to PR #630. The PR body keeps the `[A477]` first line, the template sections and "Relates to #629", and adds the Round 2 section.
- Self-test evidence at `e3f28f2f` (the DoD item stays unchecked until then), hosted and act acceptance at the new head, and re-review of R426-1 F1 to F3 and R427-1 F1 to F2.
- Archive this packet if reviewers are to re-run the round-2 receipts.

## Packet layout

| Path | What |
|---|---|
| HANDOFF.md | This file |
| PR-BODY.md | The PR #630 body for the manager to apply |
| TAKEN.md, REVIEW-READY.md, their `.readback.md` copies, `taken-url.txt`, `review-ready-url.txt` | The two #629 posts, read back from GitHub, and their URLs |
| tools/ | `attribution_checks.py`, `window_check.py`, `floor_check.py`, `archive_check.py`, `table_identity.py`, `token_scan.py` |
| receipts/ | Each tool's output: `attribution-checks.txt`, `window-check.txt`, `floor-check.txt`, `archive-check.txt`, `repro.txt`, `table-identity.txt`, `table-diff.txt`, `token-scan.txt` |
| gates/ | `gates.txt` and each gate's output at `e3f28f2f` |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |
