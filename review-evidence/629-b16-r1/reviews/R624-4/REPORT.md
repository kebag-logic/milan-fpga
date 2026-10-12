[R624] NEGATIVE - exact head 61ae86419c50f2707d6ee1dc5433bc6dee66ce84

Round R624-4, internal independent review of issue #629 / PR #725, documents only.
Head `61ae86419c50f2707d6ee1dc5433bc6dee66ce84`, tree `ed284e802555e2e1cb92f15d95dafa2702d3fc1d`.
Comparison `c20c85bd..61ae8641`: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (+1,433 lines, lane B16's section, intro and Contents) and `docs/findings/README.md` (the lane's row). No code, RTL, firmware or generated tree artifact changed.

**Verdict.** One MINOR finding is open, under Conformance, Robustness, Tests and Docs, so the verdict is NEGATIVE. RTL is CLEAN. The finding alleges no DUT defect. It changes no figure on the page and reverses no bench verdict. Every figure I recomputed independently from the receipts equals the page. The finding is that the figures check that round 4 hardened still lets a number written against its unit, such as `26s`, `10dB`, `300ms` or `.5 ppm`, enter the covered text without a receipt row while the check passes. That is the same defect class as R625-3-F1, in a form the round-4 changes did not reach.

Order of reconstruction: AGENTS.md and CONTRIBUTING.md (sections 2, 6 and 6.1); docs/README.md; the #629 issue body; the B16 assignment, the two rulings and the round 2, 3 and 4 assignments; the executor's TAKEN, STOP, STOP (B16b) and four REVIEW READY comments; lane B6's pass rule (findings page lines 333-335), the design's bench rows (`docs/design/MEDIA_CLOCK_FOLLOWING.md:1670-1671`) and `docs/reference/REGISTER_MAP.md` (`MCSRV_STAT`, `AAFM_STAT`, `CRF_RATE`, `SLIP_LB`); then the full diff and the six-commit history; then the published evidence branch `629-b16-review-evidence` at `b83e5d76` (author-r1 to author-r4 and `MANIFEST.json`), and at the pinned `b84584e4`. I wrote my independent pass over the diff before I opened any earlier review report. I then read the six earlier reports (R624-1 to R624-3, R625-1 to R625-3) on the same branch, to settle their findings and re-run R625-3's probe. I used no private author material.

## What was executed

Every command ran in the foreground. Receipts are listed in `MANIFEST.sha256`.

| Check | Result | Receipt |
|---|---|---|
| The packet's `tools/check_b16_figures.py` (`d2b51f85...`), run by me against the head page | rc 0: 1,433 lines, 1,874 tokens, 1,727 rows all OK, 147 by category, 0 uncovered; both outputs byte-equal to the published `r4/figures-rows.tsv` and `r4/figures-coverage.tsv` | `receipts/figures-check.*`, `receipts/figures-rows.tsv`, `receipts/figures-coverage.tsv` |
| `tools/r4_figures_build.py` from `tools/r4_figures_spec.py` | Regenerates the check byte for byte (1,727 rows) | `receipts/figures-build.stdout` |
| Round 4's controls (`r4_check_controls.py`) against the round-4 check | 8 of 8 PASS, each rc 1 and naming its figure; the planted catch-all category covers 147 tokens and the guard still names the figure as a measurement | `receipts/r4-controls-rerun.json` |
| The same 8 controls against round 3's check (`13d7a0de...`) and the page at `0782c55f`, exported to a plain tree | Round 3's five PASS; the three new controls FAIL (not named). So each new control fails for the defect it targets | `receipts/r4-controls-on-r3-check-rerun.json` |
| Round 3's own runner against the round-4 check | 5 of 5 PASS | `receipts/r3-controls-on-r4-check-rerun.json` |
| R625-3's probe (`probe_figure_coverage.py`, `f4c4d91b...`, unchanged) against the round-4 check | 7 of 7 detected, including the quoted and linked `7.25 ppm` | `receipts/r625-3-probe-rerun.*`, `tools/r625-3-probe_figure_coverage.py` |
| My escape-form probe (`tools/probe_escape_forms.py`), one sentence inserted on R625-3's attribution row | Detected: plain `7.25 ppm`, `7.25ppm`, `2.585-9.99 s`, a U+2212 minus. **Not detected (rc 0, 0 uncovered):** `26s`, `10dB`, `300ms`, `.5 ppm` | `receipts/escape-probes.json` |
| Every digit run in the check's scope that its TOKEN regex never reads (`tools/untokenized_digits.py`) | 1,051 runs, all identifiers: lane, review and run names (B16, R624-3, `pts2`), McASP0, SHA-256, issue numbers, packet paths in backticks, `v1.2`, `1x1`, `AX7101-0001`, CRC32, HTML markers. **No measured figure on the page escapes at this head** | `receipts/untokenized-digits.*` |
| The 147 category tokens, read in context | Each is an identifier bound to its keyword: commits (7), clauses (4), descriptor (39), channel (24), step or round (57), list item (11), packet label (3), branch (1), link target (1). No whole-quote or whole-link exemption remains (`EXCLUDE`, check lines 2315-2328) | `receipts/figures-coverage.tsv` |
| Rows whose receipt is a page | The `git:` rows (88) claim only the "Was" columns and quoted reworded phrases of the round tables, lines 3404-3681. The `repo:` rows read other sections (lane B6's rule at :333, B7's window at :188/:839, B8's slip at :1325, B15 at :2108) or the design doc; none reads lane B16's own text | `receipts/figures-rows.tsv` |
| "Where the packet is" (`tools/audit_packet.py`) | The pinned `b84584e4` `MANIFEST.json` has SHA-256 `8d417d54...`, 1,680 entries, and 27 author files path-redacted (1/9/17); the flag is set exactly where the two hashes differ; every entry equals its published file; author-r1 to author-r3 exist at the pin and author-r4 only at the tip `b83e5d76`. All 71 packet-file rows at the head equal the author-r4 file by size and SHA-256. All 54 raw-file and source-read hashes are in `RAW-ARTIFACTS.json`. 133 of 133 checks pass | `receipts/audit-packet.json` |
| The page's "66 packet-file rows at `0782c55f`" (`tools/audit_r3_rows.py`) | 66 of 66 equal `original_sha256`, `published_sha256` and the published author-r3 file, none redacted | `receipts/audit-r3-rows.json` |
| Tip manifest, author-r4 | 25 path-redacted (gate logs and results, `tools/gates_r2.py`); none is a hash row on the page. `gates_r2.py` appears only in the redaction sentence at :2619 | `receipts/tip-manifest-r4.txt` |
| Independent recompute from primary summaries (`tools/recompute_b16.py`), not through the author's check | See the table below; every value equals the page | `receipts/recompute-b16.json` |
| Census recount, the start record excluded | 44 of 45 reads equal in B16, B16b and B16c; the one difference is GET_AVB_INFO's propagation delay (`0x183` to `0x179`, 387 to 377 ns in B16) | read from `restore/census-*.jsonl` (results in this report) |
| Doc gates at the head, in the locked Markdown environment | `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base c20c85bd` and `--base e8454e27`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check` and `git diff --check c20c85bd HEAD`: all rc 0 | `receipts/gates/` |
| Privacy | No host path, address, interface name, serial path, vendor or product name in the added lines. The reference peer, the tone source and the external capture are named by role only. The published packet's host and identity fields are placeholders (`<host-if>`, `<peer-eid>`, `<external-capture-device>`) | (scan in this report) |
| Clone integrity after all probes | HEAD and tree as published; 0 status lines; index equals HEAD; the five gitlinks (`external`, `gptp-processor`, `protocol-processor`, `third_party/lwSRP`, `third_party/verilog-axis`) equal HEAD's | `receipts/integrity-final.txt` |

Independent recompute, from `summary/*/c-b9-grade.json`, the alignments, `summary/*/d-extcap-pair.json`, `summary/*/d-loop-decode.json` and `r2/*-poll-trace.tsv`, decoded by REGISTER_MAP:

| Figure | Recomputed | Page |
|---|---|---|
| B0 floor blocks, degraded, medians | 169; 131; floor -123.98/-123.95 dB, all -123.95/-122.80, worst -100.47/-80.48 (block 224) | :2817-2828, :3133-3134 |
| B0 runs and overlap | 0-18, 28-31, 43-44, 46-54 and 11 more; 1,637,452/1,637,980 frames (34.1136 s), whole blocks 0-33; 23 inside, 108 beyond in 13 runs; worst inside -100.61/-80.63 (block 7) | :2822-2829, :2837 |
| B0 recording start | capture command 06:38:03.2, 2 s playback lead, 06:38:05.2; 24.0 s / 26.0 s after the binds (`r2/b0-2-receipt.json` timing; `run_b16.py` lead) | :2668, :2694-2697 |
| B-CRF / B-AAF at (c) | 300/300 at floor, 0 events; -123.98 (-123.93)/-123.97 (-123.90) and -123.98 (-123.92)/-123.97 (-123.91) | :3129-3132 |
| (c) against (a)/(b) | 1,647,859/1,646,473 and 1,641,156/1,644,390 frames, 0 differing | :3144-3145 |
| (d) floor | 303 of 303 whole blocks (blocks 0-1 silent, 2 the start) in `b0-2`, `bcrf` and `baaf`; `pts2` 11 of 13, blocks 6 and 12 off; spans 303.82/303.87 s; 0 net steps | :2738-2739, :3152-3155 |
| LOCKED brackets | polls 44/45 and 52/53: 2.585-3.161 s and 6.602-7.180 s | :3169-3175 |
| Window polls | 596 LOCKED in each; actuator busy 16 and 12 (`0x74`); every ACQUIRE/LOCKED word carries bit 4; `SLIP_TDM` 0 | :3178-3180, :3336 |
| Rates | CRF +10.60 to +10.65 (B-CRF), +10.59 to +10.65 (B-AAF); AAF meter +10.60 to +10.63; `AAFM_STAT` `0x001e0007` (locked, valid, enabled, 0 restarts, 30 ns) | :3169-3170 |
| `SLIP_LB` | 162 to 174 to 188 in steps of two; five steps per case between the binds and the set, from 0.149/0.138 s after the binds to 1.380/1.388 s before the set, all IDLE; ACQUIRE steps 2.08-2.66, 2.08-2.65 and 5.10-5.68 s; none after the first LOCKED poll | :3204-3221 |
| Clock-source record | `runs/bcrf/events.jsonl` and `runs/baaf/events.jsonl`: peer set 0, read back 0; DUT set 1 or 2, read back the same; DUT restore 0, read 0; peer restore 1, read 1; `final equal_to_found: true` | :3079-3093 |
| B16 loopback | `summary/loop2/acmp-peer-tap.json`: UNBIND 0.0 ms, BIND command 0.1 ms, response and PROBE_TX (CONNECT_TX) 99.6 ms, second PROBE_TX 299.6 ms, no CONNECT_TX response among 38 ACMP messages | :2420-2430 |

## Findings

### R624-4-F1 MINOR (Conformance, Robustness, Tests, Docs): the figures check does not read a number written against its unit, so such a figure needs no receipt row

- **Where:**
  - Packet `author-r4/tools/check_b16_figures.py:2287-2297`, the `TOKEN` regex. Its lookbehind `(?<![\w/#.+\-])` and lookahead `(?![\w])` drop any digit run joined to a letter, and any decimal with a leading point.
  - `:2299-2303`, the `MEASURE` guard. It is applied only to tokens, so it never sees these forms.
  - Page claims about the check: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3531` ("The check also reads every number, time, date, hash and number word in that text"), `:3642` and `:3649-3652`. The PR body says the same under Round 3, item 1 ("It also reads every number...").
- **Authority and evidence:**
  - The round 4 assignment, item 2: "A measurement-bearing token (a number with a unit, a percentage, a dB, ppm, s or frame count) needs a receipt row wherever it appears".
  - The manager's round-4 review brief asks to confirm that "a number followed by a unit is always claimed by a row".
  - R625-3-F1, accepted as MINOR, set the standard: the protection against unreceipted figures must hold for the forms text can take.
  - My probe inserts one sentence on the B16c attribution row (R625-3's row, line 3006), leaves the check and the receipts unchanged, and runs the published check (`receipts/escape-probes.json`):

    | Inserted | Check exit | Uncovered |
    |---|---|---|
    | `The measured residual was 7.25 ppm.` (control) | 1 | `7.25` |
    | `The residual settled in 26s.` | **0** | none |
    | `The residual sat 10dB above the floor.` | **0** | none |
    | `The probe answered after 300ms.` | **0** | none |
    | `The measured residual was .5 ppm.` | **0** | none |
    | `The measured residual was 7.25ppm.` | 1 | `7` (by backtracking, not by design) |

- **Impact:**
  - No figure on the page escapes today. `receipts/untokenized-digits.tsv` shows that every digit run the tokenizer skips at this head is an identifier.
  - The defect is in the protection that rounds 3 and 4 were assigned to provide, which the page and the PR body describe as complete. A measurement written in a common engineering form can be added to lane B16's section, the introduction, the Contents entry or the index row with no receipt, and the check still reports 0 uncovered.
  - Its own planted-category control cannot catch this, because it plants figures with a space before the unit.
  - This changes test behaviour and a claim about a test, so it is not wording-only RESIDUE.
- **Required outcome:**
  - The check reads a number joined to its unit (`26s`, `10dB`, `300ms`) and a decimal written with a leading point (`.5 ppm`) as tokens.
  - Followed by a unit, each is a measurement that only a row can claim.
  - Digit-bearing identifiers stay covered only by categories bound to their shape or keyword, as the existing ones are.
  - Standing controls are added for at least `26s`, `10dB` and `.5 ppm` on the attribution row. Each must fail and name the figure.
  - The unchanged page still passes, and the eight existing controls stay green.
  - Merely narrowing the page's "reads every number" would not meet the assignment's "wherever it appears".
- **Verification:**
  - Re-run `tools/probe_escape_forms.py` from this packet against the corrected check. Every form must give exit 1.
  - Re-run `tools/untokenized_digits.py`, adapted to the corrected TOKEN. It must show no digit run outside a token or a bound identifier category.
  - Re-run the check, its controls and R625-3's probe at the new head.

### R624-4-S1 SUGGESTION (Docs): lane B16's opening paragraph points to rounds 2 and 3 but not to round 4

- `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2304-2307` lists the second and third findings rounds. The page introduction (:34-36) and the Contents entry (:81) both point to [B16, round 4: packet and coverage]. Line 2321-2323 also points to the packet paragraph.
- Optional: add ", and the fourth in [B16, round 4: packet and coverage](#b16-round-4-packet-and-coverage)" to the end of the sentence at :2307. Keep it on the same source line, so that no check row moves. It does not affect lens coverage.

## Earlier findings at this head

| Earlier item, lenses | At `61ae8641` | Evidence |
|---|---|---|
| R624-1-F1 = R625-1-F3 (B0's figures), Conformance, Tests, Docs | RESOLVED | Floor medians -123.98/-123.95 dB; runs split at 45; recording start 06:38:05.2, 26 s; recomputed above |
| R624-1-F2 = R625-1-F4 (lane B6's four terms), Conformance, Tests, Docs | RESOLVED | :3190-3202 state all four terms for both cases: three met, timed ratio NOT RUN, no decision replaces it. The same at :3316, :3331-3333, the index row and the PR body |
| R625-1-F1 (attribution, shown against inference), Conformance, Tests, Docs | RESOLVED | :2826-2840, :3250-3255, :2926-2929, the index row and the PR body all separate 23 shown inside the taps' 34.1 s from 108 assigned by inference |
| R625-1-F2 = R624-1-S2 (reduced receipts), Tests, Docs | RESOLVED | `r2/*-poll-receipt.json`, `r2/*-poll-trace.tsv`, `r2/source-receipt.json` and `r2/b0-2-receipt.json` are bound to the raw SHA-256s, with the extraction at :3459-3467; the source receipt names roles only, with sizes withheld; 6 of 6 tool controls |
| R624-1-R1 = R625-1-R1 (PR title), Docs | RESOLVED | Live title equals the requested text |
| R624-1-R2 = R625-1-R2 (counter mark), Docs | RESOLVED | :3035-3037, :3167, :3416 |
| R624-1-S1, R625-1-S1, R624-2-S2, R625-2-S1, R625-3-S1 (census), Docs | Taken | "44 of 45 reads equal, the census's start record aside" in all five places; my recount agrees |
| R625-2-F1 (attribution at (a)), Conformance, Tests, Docs | RESOLVED | :3239 is the exact requested text; it equals the `a-peer-tap` summaries |
| R624-2-F1 (positive-control floor counts), Robustness, Tests, Docs | RESOLVED | 303 of 303 and 11 of 13, with the silent and start blocks stated; recomputed |
| R624-2-F2 (LOCKED bracket from the poll's state read), Tests, Docs | RESOLVED | 2.585-3.161 and 6.602-7.180 s, from the start of the last ACQUIRE poll; recomputed from the traces |
| R624-2-R1, R2 and R3, Docs | RESOLVED | :2779-2781, :3256-3260 (1,255; 618 and 668); :3209-3211; the PR body's "#629" section |
| R624-2-S1 (servo bit 4), Docs | Taken | :3336-3338; bit 4 confirmed in every ACQUIRE and LOCKED word |
| R624-3-F1 (where the packet is), Docs | RESOLVED | :2603-2628 name the branch, pinned `b84584e4`, `author-r1/` (the real name), `author-r2/`, `author-r3/`, `author-r4/` at a later commit, and `MANIFEST.json`; its hash, count, flags and the 66 rows all verified |
| R625-3-F1 (quoted and linked figures), Conformance, Robustness, Tests, Docs | RESOLVED for the two forms it names | No whole-quote or whole-link category; R625-3's probe 7 of 7; the new controls discriminate against round 3's check. The class is not closed: see R624-4-F1 |

## Lens results at this head

| Lens | Result | Artifacts examined |
|---|---|---|
| Conformance | UNCLEAN (R624-4-F1) | All of lane B16's #629 judgements, :2542-2553, :2906-2915 and :3312-3324. The INTERNAL mismatch control is stated as not run (:3316, :3339-3340, the index row, the PR body). Format adaptation is on the listener only (the format-check events show `set: null`). The peer-clock exception applies to B-CRF and B-AAF only, with each set read back and restored. Lane B6's four terms are against its rule at :333-335. The design's B AAF row is at `MEDIA_CLOCK_FOLLOWING.md:1670`, and MEDIA_RESET per switch is cited as the design cites it. The round-4 acceptance item 2 is not fully met (F1) |
| RTL | CLEAN | `git diff --stat c20c85bd..61ae8641`: no `hdl/`, `sw/`, `syn/`, `tb/` or config change. The RTL statements on the page agree with `REGISTER_MAP.md`: `MCSRV_STAT` `[2:0]` state, `[4]` DRP mismatch and `[6]` actuator busy (`0x33`/`0x34`/`0x74`); `AAFM_STAT` fields (`0x001e0007`); `CRF_RATE`/`AAFM_RATE` at 512 units per ppm; `SLIP_LB` `[15:0]` dups. Lane B16 claims no DUT fix and no RTL behaviour beyond these reads |
| Robustness | UNCLEAN (R624-4-F1) | Malformed and unusual input to the figures check: probes on quoted, linked, glued, leading-point, hyphen-range and U+2212 forms. Identifier categories read in context. Ordering of the round tables, which use `git:` receipts only for superseded values |
| Tests | UNCLEAN (R624-4-F1) | The check run and regenerated byte-equal; 8 of 8 controls, which discriminate against round 3's check; R625-3's probe 7 of 7; my probe, where 4 forms pass undetected; an independent recompute of the B0, B16c, (d), poll and `SLIP_LB` figures; census recount; packet hash audit |
| Docs | UNCLEAN (R624-4-F1) | The section, the introduction, the Contents entry, the index row and the PR body. "Where the packet is" verified against the pinned and tip commits. Privacy scan of the added lines and of the published packet. All 14 doc and tree gates rc 0 at the head. S1 is optional |

## Completion ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R624-4-F1 open) | Findings :2284-3695, the index row, the PR body, the issue and rulings, design :1670-1671, findings :333-335 | R624-4 | `61ae86419c50f2707d6ee1dc5433bc6dee66ce84` |
| RTL | CLEAN | Diff stat (docs only), REGISTER_MAP `0x8F8`/`0x8E0`/`0x748`/`0x8D4` against the page's decoded words | R624-4 | `61ae86419c50f2707d6ee1dc5433bc6dee66ce84` |
| Robustness | UNCLEAN (R624-4-F1 open) | `check_b16_figures.py` TOKEN/MEASURE/EXCLUDE; `receipts/escape-probes.json`; `receipts/untokenized-digits.tsv` | R624-4 | `61ae86419c50f2707d6ee1dc5433bc6dee66ce84` |
| Tests | UNCLEAN (R624-4-F1 open) | The check and its outputs, the build, the controls (three runs), R625-3's probe, `receipts/recompute-b16.json`, `receipts/audit-packet.json`, `receipts/audit-r3-rows.json` | R624-4 | `61ae86419c50f2707d6ee1dc5433bc6dee66ce84` |
| Docs | UNCLEAN (R624-4-F1 open) | Findings page and index at the head, PR #725 body and title, `receipts/gates/*`, the packet's published files at `b84584e4` and `b83e5d76` | R624-4 | `61ae86419c50f2707d6ee1dc5433bc6dee66ce84` |

## Limits and manager duties

- No manager source bank ran at this head, and none is claimed. The manager validates the current-dev merge candidate (source base `c20c85bd`, live dev `c6bd08c6`) at the merge turn. The author's published gate receipts are the source-head execution evidence. My own gate runs are listed above.
- Hosted contexts at `61ae8641`, inspected read-only, show:
  - executed and successful: `rtl-fast`, `elaborate`, `docs-check-no-git`, `wire-accountability`, `bdd-conformance`, `changes` and `full-ci-gate`;
  - in progress when read: `docs-check`;
  - skipped through the no-op path: `verilator-suites` and `yosys-portability`;
  - skipped: the other conditional jobs.

  Hosted and act acceptance is the manager's (`receipts/hosted-check-runs.tsv`).
- The raw captures, polls and source reads stay off the packet. My recompute starts from the packet's published summaries and traces, which bind those raws by SHA-256. It does not re-derive THD+N from audio.
- Bench facts (identity, timings, wiring, the tone source's routes) rest on the published run records. No hardware was touched, and the physical calibration was NOT RUN. Printed precision is not calibrated accuracy.
- The first `check_em_dash.py` attempt outside the locked Markdown environment refused to judge (renderer missing). Its rc 0 result is from the locked environment, whose packages equal `tools/markdown/requirements.txt`.
- `tools/r625-3-probe_figure_coverage.py` is an unchanged copy of R625-3's published script (`f4c4d91b...`), kept so the re-run can be reproduced.

R624-4 FINISHED
