[R624] NEGATIVE - exact head 3619019350936d5af851933df0b5444ef8387e69

Round R624-5. Internal independent review, cleared context, of issue #629 / PR #725 (bench lanes B16, B16b and B16c; documents and findings only). Head `3619019350936d5af851933df0b5444ef8387e69`, tree `11777358b03b38ceda5ade1e1ed59e31b08473e5`, source base `c20c85bd`. Round 5 assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6125608002.

**Verdict.** Three MINOR findings are open, so the verdict is NEGATIVE. None alleges a DUT defect. None changes a figure on the page or reverses a bench verdict: every focus figure I recomputed independently equals the page. RTL is CLEAN. Conformance, Robustness, Tests and Docs are UNCLEAN at this head.

- **F1** (Tests, Conformance): one row of the figures check names B-CRF's receipt, but it recomputes only B-AAF's value.
- **F2** (Conformance, Robustness, Tests, Docs): "A measurement is never an identifier" fails when the unit is spelled out. Examples: `CLOCK_DOMAIN 7 milliseconds`, `per cent`, `decibels`, `hertz`, `parts per million`. The check passes all of these.
- **F3** (Docs): the page never says where round 5's packet is published.

One RESIDUE (wording only) is recorded with its exact fix.

All five lenses were applied, each against the artifacts named below. I made no source change, commit, push or GitHub write, ran nothing on the bench, and used no sub-agent, Docker or act. All probes ran on copies under the packet's scratch directory. The clone is byte-exact at the head (see the end of this report).

## Context reconstructed

I read, in this order:

1. AGENTS.md, CONTRIBUTING.md sections 4 and 6, and docs/README.md.
2. The #629 issue body.
3. The lane assignment (6117305187) and the rulings 6117672835 (B16b) and 6118365090 (B16c, the maintainer's exception: the peer may be set to INTERNAL for B-CRF/B-AAF and must be restored).
4. The round assignments for rounds 2 (6119316763), 3 (6119906508), 4 (6121193402) and 5 (6125608002).
5. The executor's REVIEW READY for round 5 (6126360842).
6. `git diff c20c85bd..3619019350936d5af851933df0b5444ef8387e69`: two files, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` with +1,571 lines and `docs/findings/README.md` with one row. I read all eight commits.
7. The published evidence at `629-b16-review-evidence` @ `a73ce5c42ee97fb53b272a51b5f41a55afba5fa5`: `MANIFEST.json`, `author-r4/` and `author-r5/`. I did not open the `reviews/` tree before writing this verdict. From it I extracted only the three probe scripts this round requires me to re-run, by path, and checked each against its published SHA-256.

## Executable evidence (this round, offline, documents only)

| What | Result | Receipt |
|---|---|---|
| Publication binding: every file in `author-r5/` (592) and `author-r4/` (555) against `MANIFEST.json` (3,044 entries, sha256 `c2407465...`) and the round's own `MANIFEST.sha256` | 0 problems. `original_sha256` equals the packet's own manifest. `published_sha256` equals the file. Hashes differ exactly on the `path_redacted` files (33 in r5, 25 in r4). No file is listed without being present, or present without being listed | `receipts/publication-author-r5.json`, `receipts/publication-author-r4.json` |
| `check_b16_figures.py` (sha256 `2641412c...`, equal to the REVIEW READY's) on the head page | rc 0. 1,749 rows, 1,749 OK. 13,209 digits: 11,037 by row, 2,172 by category, 0 uncovered. Both outputs byte-equal to the published `r5/figures-rows.tsv` and `r5/figures-coverage.tsv` | `receipts/check/` |
| `r5_figures_build.py` regenerating the check from `r5_figures_spec.py` | Byte-equal to the published check | `receipts/controls/build.stdout` |
| `r5_check_controls.py` | 22 of 22 PASS. Output byte-equal to the published `controls/r5-controls.json` | `receipts/controls/r5-controls.json`, `r5.stdout` |
| Round 3's and round 4's runners, unchanged, against the new check | 5 of 5 and 8 of 8 PASS. Byte-equal to the published reruns | `receipts/controls/r5-rerun-r3.json`, `r5-rerun-r4.json` |
| Published `controls/r5-controls-on-r4-check.json` | 11 round-5 controls FAIL on round 4's check. The 3 that PASS are the forms round 4's guard already read: non-breaking space, hyphen and the planted category. This equals the page's claim | the published file |
| `r5_self_probes.py` | 36 of 36 detected. Byte-equal to the published `r5/self-probes.json` | `receipts/controls/self-probes.json` |
| R624-4's `probe_escape_forms.py`, unchanged (sha256 `5c2dbc69...` equals the published one) | rc 0. 8 of 8 forms rc 1, each naming the inserted number: `7.25`, `26`, `10`, `300`, `7.25`, `.5`, `2.585`/`-9.99`, `−130.00` | `receipts/probes/r624-4-escape-forms.json`, `r624-4.stdout` |
| R625-4's `probe_coverage.py`, unchanged (`e8749cbe...`) | Exit 0. 12 of 12 rc 1, each naming its number at the inserted line. The continuation case names `3` at line 3109 | `receipts/probes/r625-4-coverage-probes.json`, `r625-4.stdout` |
| R625-3's `probe_figure_coverage.py`, unchanged (`f4c4d91b...`). It expects its output `receipts/` directory to exist, so I created it | Exit 0. 7 of 7 expected rc observed | `receipts/probes/r625-3.stdout` |
| My own escape probes, `scripts/probe_r624_5_escapes.py` | Every free digit is caught. Identifier-bound digits followed by a unit spelling outside `MEASURE` pass (F2) | `receipts/probes/r624-5-escapes.json` |
| Mutation probe of the line-3200 row, `scripts/probe_row3200.py` | With only B-CRF's window LOCKED count changed to 595, the line-3008 and line-3174 rows turn MISMATCH, but both line-3200 rows stay OK (F1) | `receipts/probes/row3200-probe.json` |
| Independent recompute of B16c's poll, `scripts/recompute_b16c_poll.py`. It decodes `MCSRV_STAT[2:0]`/`[4]`/`[6]`/`[31:16]` per `docs/reference/REGISTER_MAP.md` 0x8F8 from the published per-poll traces and the runs' own marks | Both windows LOCKED 596 of 596. Brackets 2.585 to 3.161 s and 6.602 to 7.180 s, at polls 44/45 and 52/53. Busy 16 and 12, word `0x34` 580 and 584. Trim -6.125 to -6.000 ppm. Bit 4 at every ACQUIRE/LOCKED poll. `SLIP_LB` steps: five IDLE before each set, then 1 (B-CRF) and 2 (B-AAF) in ACQUIRE at 2.08 to 2.66 s, 2.08 to 2.65 s and 5.10 to 5.68 s, and none after LOCKED. `SLIP_LB` 162 to 174 to 188 | `receipts/recompute-b16c-poll.json` |
| Independent recompute of B0, B-CRF and B-AAF, `scripts/recompute_b0.py`, from the per-block grades and the alignments | B0: all-block medians -123.95/-122.80 dB, worst -100.47/-80.48 dB at block 224. Floor medians -123.98/-123.95 dB, worst -123.91/-120.18 dB. 169 at the floor and 131 degraded, in runs 0-18, 28-31, 43-44, 46-54 and eleven later runs. Overlap 1,637,452 frames = 34.1 s, whole blocks 0-33. 23 inside (worst -100.61/-80.63 dB, block 7). 108 beyond, in thirteen runs. B-CRF and B-AAF: 300 of 300 at the floor, medians -123.98/-123.97 dB, worst as tabled. Alignments SAMPLE-EXACT over 34.2 to 34.3 s. Totals 3,077,452/3,077,980 (B16b) and 3,289,015/3,290,863 (B16c) | `receipts/recompute-b0-b16c.json` |
| Every hash-table row in lane B16's section and in the live PR body, against `author-r5/` and its `RAW-ARTIFACTS.json` (`scripts/verify_hash_tables.py`) | 76 packet rows and 54 raw rows on the page, and 23 rows in the body, all equal. The body's two other `check_b16_figures.py` rows are rounds 3 and 4: they equal the published `author-r3/` (`13d7a0de...`) and `author-r4/` (`d2b51f85...`) checks | `receipts/hash-tables.json`, `receipts/body-earlier-check-hashes.txt` |
| Documentation gates at the head, in the pinned Markdown environment (cmarkgfm 2025.10.22, html5lib 1.1) | All rc 0: `docs_check.py` (0 findings, scrub self-test 23/23), `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base c20c85bd` (0 findings over 1,572 added lines) and `--selftest`, `check_doc_paths.py`, `check_feature_status.py --self-test`, and `git diff --check c20c85bd HEAD` | `receipts/gates/` |
| Privacy scan of the 1,572 added lines | No host path, IP, MAC, interface or host name, and no vendor or product name for the reference peer, the external capture or the tone source | Done by command; no hits to record |
| Hosted contexts at the exact head | Executed and successful: `rtl-fast`, `changes`, `elaborate`, `full-ci-gate`, `wire-accountability`, `bdd-conformance`, `docs-check-no-git`. `docs-check` was still in progress when read. Skipped, as docs-only scheduling: the Verilator suites, lint and shards, the Yosys contexts, `firmware-unit`, `publication-census` and physical gPTP. Skips are not executions | `receipts/hosted-check-runs.tsv` |

## Findings

### R624-5-F1 MINOR (Tests, Conformance): the line-3200 row names B-CRF's receipt but reads only B-AAF's

- **Where:**
  - `author-r5/tools/check_b16_figures.py:1193`, the ROWS_TSV row `3200	596	r2/bcrf-poll-receipt.json	d#0	same(win('baaf')['servo']['LOCKED'] for r in ('bcrf', 'baaf'))`;
  - its source, `author-r5/tools/r5_figures_spec.py:1059`;
  - the page line it guards, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3200`.
- **Evidence:**
  - At spec line 1059 the key is an f-string, `f"same({WIN(r)}['servo']['LOCKED'] for r in ...)"`. It is evaluated when the spec is built, so `{WIN(r)}` takes the spec's leftover `r`, which is `'baaf'`. The following `.replace("{WIN(r)}", ...)` therefore never matches.
  - The emitted key ignores its own loop variable. `same()` over two identical values returns B-AAF's count, and the row's receipt column, published in `r5/figures-rows.tsv` row 667, names `r2/bcrf-poll-receipt.json`.
  - The mutation probe changes only B-CRF's window LOCKED count to 595. Rows on lines 3008 and 3174 turn MISMATCH, and both line-3200 rows stay OK (`receipts/probes/row3200-probe.json`).
  - It is the only row whose key ignores its loop variable.
  - The value itself is correct: B-CRF's window is LOCKED 596 of 596 by my independent decode.
- **Authority:** the round 3 assignment requires that the check "recomputes each value from the receipts and fails on any mismatch". The page states the same at `:3529-3530`. Line 3200's 596 is the evidence for lane B6's LOCKED term in both columns, B-CRF and B-AAF, and its B-CRF half is not recomputed.
- **Impact:**
  - A future page could state 595 for B-CRF at lines 3008/3174 and leave "596 of 596" for both cases at line 3200, and still pass.
  - The published rows receipt misstates which receipt was read for that row.
  - This is a defect in an executable check and its generated output, not wording.
- **Required outcome:** the line-3200 LOCKED row recomputes the count of each case from that case's own receipt, and the rows output names what it read.
- **Verification:** re-run `probe_row3200.py` unchanged. Both line-3200 rows must turn MISMATCH, or the check must otherwise fail at line 3200. The unchanged page still passes.

### R624-5-F2 MINOR (Conformance, Robustness, Tests, Docs): a spelled-out unit lets an identifier stand for a measurement

- **Where:**
  - `author-r5/tools/check_b16_figures.py:2333-2338` (`SEP`, `MEASURE`);
  - the page's rule, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3741-3752`, with its heading "A measurement is never an identifier";
  - the index row, `docs/findings/README.md:15` ("no identifier can stand for a measurement");
  - the commit subject of `f60132ca`.
- **Authority:** the round 5 assignment, item 2: "A digit run followed by a unit belongs only to a row, whatever the spacing ... and whatever the spelling ... This includes a percentage, dB, ppm, s, ms, ns, Hz or a frame or sample count."
- **Evidence:** `scripts/probe_r624_5_escapes.py`, on the attribution row the earlier probes used:
  - The check exits 0, reporting full coverage, for each of these:
    - `CLOCK_DOMAIN 7 milliseconds`, `microseconds`, `nanoseconds` and `msec`;
    - `CLOCK_DOMAIN 7 per cent`;
    - `CLOCK_DOMAIN 7 decibels`;
    - `CLOCK_DOMAIN 7 hertz` and `kilohertz`;
    - `CLOCK_DOMAIN 7 parts per million`;
    - `B16 milliseconds`;
    - `IEEE 1722.1 milliseconds`.
  - Each is a percentage, dB, ppm, s fraction or Hz from the ruling's own list, written in words.
  - Controls in the same run, with the same harness, are detected: `CLOCK_DOMAIN 7 ms`, a free `7 milliseconds`, and `seven milliseconds`.
  - `MEASURE` already reads `percent`, `seconds` and `minutes` as words. The words for the units in the ruling's own list are the gap, not wordiness as such.
  - The page says units are read for "seconds and their fractions", and the index row says no identifier can stand for a measurement. Neither holds for these spellings.
- **Impact:** this is the class that rounds 3 to 5 set out to close by construction. A measurement written beside a keyword-bound identifier still enters the covered text with no receipt, and the check reports 0 uncovered. The current page holds no such sentence, and every figure on it is unaffected.
- **Required outcome:**
  - A number followed by the spelled-out forms of the units the ruling names is a measurement that only a row can claim: at least per cent, decibel(s), hertz and its multiples, parts per million/billion, and milli-, micro- and nanosecond(s) with their `msec`/`usec`/`nsec` forms.
  - Each added spelling has a standing control that fails and names the figure.
  - The page's and the index row's statement of the rule is true of the list as shipped.
- **Verification:** re-run `probe_r624_5_escapes.py` unchanged. Every `id+` form whose unit is one of the ruling's units, written in words, must be detected. The 22 controls, the earlier runners and the unchanged page stay green.

### R624-5-F3 MINOR (Docs): the page does not say where round 5's packet is published

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2608-2616`, "Where the packet is", and the round 5 evidence table at `:3826-3833`.
- **Evidence:**
  - The paragraph maps rounds 1 to 3 to `author-r1/` to `author-r3/` and says round 4's packet goes to `author-r4/`. It says nothing about round 5.
  - The round 5 table hashes `tools/r5_check_controls.py` and the four `controls/r5-*.json` files. These exist only in `author-r5/` at `a73ce5c4`: I bound them byte for byte there, and they are absent from `author-r3/` and `author-r4/`.
  - A cold reader following the page's own mapping looks in the wrong directories.
- **Authority:**
  - R624-3-F1 (MINOR) and the round 4 assignment item 1 require the mapping of each round's directory.
  - AGENTS.md section 6, Docs lens: "The PR and Issue contain enough evidence for another cold reviewer."
- **Impact:** the round's hashed evidence cannot be located from the page. The fix adds identifier tokens (`author-r5/`), so the check's coverage output regenerates. By R624-3-F1's precedent this is MINOR, not RESIDUE.
- **Required outcome:** the paragraph maps round 5 to `author-r5/`, as it does round 4. With a published commit available, it pins one.
- **Verification:** the paragraph names `author-r5/`. Every round 5 hash row equals its file there. The check still passes.

### R624-5-R1 RESIDUE (Docs): the stated identifier categories differ slightly from the check's

- **Where:**
  - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3764-3765`;
  - the PR #725 body, round 5 item 1, the third sub-bullet of "The categories".
- **Evidence:**
  - The check binds a second index after "and" or "to" only for channels. For steps and rounds it binds one after "and" only, and for descriptors it binds none (`check_b16_figures.py`, EXCLUDE).
  - The check also exempts issue numbers `#629` and `#645` as a closed list, which neither text names.
  - The check is stricter than described. No figure, verdict, test or generated artifact changes.
- **Exact fix (page line 3764-3765, and the same words in the body):** "descriptor, channel, step and round indices after their keyword, and a second channel index after "and" or "to", or a second step or round index after "and";". Add "the issue numbers it cites," to the closed-list bullet after "the operator,".

### Suggestions (optional, do not affect coverage)

- **R624-5-S1 (Tests):** `MEASURE` is a closed list, so other identifier-bound counts and separators also pass. These lie outside the ruling's named units and spacings, so they are not findings:
  - counts: `channel 3 underruns`, `STREAM_INPUT 2 events`, `channels 0 and 4 drops`, `CLOCK_DOMAIN 7 dBm`;
  - separators: `(CLOCK_DOMAIN 7) ppm`, `7 'ppm'`, `7: ppm`, `7/ppm`;
  - number words outside the token list: "a million frames", "thousands of frames", "a dozen slips".
  
  A short statement of these limits beside the rule would make the guarantee exact.

## Prior public findings at this head (read after my own pass)

| Finding | Disposition at `36190193` |
|---|---|
| R624-1 F1 = R625-1-F3, B0's figures | Resolved. The floor medians are -123.98/-123.95 dB, the runs are 43 to 44 and 46 to 54, and the start is 06:38:05.2, 26 s after the binds (`:2700-2702`, `:2822-2828`). I recomputed them independently |
| R624-1 F2 = R625-1-F4, lane B6's four terms | Resolved: `:3195-3207` and `:3008-3009`. Three are met and the timed ratio is NOT RUN, with no decision replacing it |
| R624-1 R1 = R625-1-R1, PR title | Resolved: the title now reads "Direction B's B0 graded, and B-CRF and B-AAF graded at the path's floor" |
| R624-1 R2 = R625-1-R2, the counter mark | Resolved: "20 s after the DUT's set, about 6 s before the window" (`:3040-3042`, `:3095-3097`) |
| R624-1 S1 = R625-1-S1 = R625-2-S1 = R625-3-S1, the census header | Taken: "44 of 45 reads equal, the census's start record aside" |
| R624-1 S2 = R625-1-F2, reduced receipts | Resolved: the `r2/` receipts are bound to raw hashes, with the extraction at `:3426-3494`. My own trace decode agrees |
| R625-1-F1, attribution inside and beyond the overlap | Resolved in the findings (`:2829-2845`), the index row and the PR body. Inside, 23 blocks are shown directly. Beyond, 108 are by inference |
| R624-2-F1, the positive control's floor counts | Resolved: `:2743-2744`, `:3157-3158` (303 of 303, `pts2` 11 of 13, the pre-playback blocks stated) |
| R624-2-F2, the LOCKED bracket | Resolved: 2.585 to 3.161 s and 6.602 to 7.180 s, as I recomputed from the poll trace |
| R624-2-R1 and R2 | Resolved: `:2784-2786`, `:3260-3264`, `:3214-3216` |
| R624-2-R3, the body's antecedent | Resolved: the body says "Direction B's INTERNAL mismatch control did not run" |
| R624-2-S1, servo bit 4 | Taken: `:3341-3343`. I confirmed it at every ACQUIRE/LOCKED poll |
| R625-2-F1, the exact replacement | Resolved: `:3244` is the given sentence verbatim, and its rows are mutation-sensitive (R625-3's probe) |
| R624-3-F1, where the packet is | Resolved for rounds 1 to 4 (`:2608-2633`; `MANIFEST.json` binding verified). Round 5's directory is now missing: F3 |
| R625-3-F1, quoted and link-label figures | Resolved: R625-3's probe and R625-4's `quoted`/`linked`/`code` cases are detected |
| R624-4-F1, glued units and a leading point | Resolved for the forms named: probe 8 of 8 |
| R625-4-F1, sign plus point, exponent, double space, continuation | Resolved for the forms named: probe 12 of 12. The class remains open for spelled-out units: F2 |
| R624-4-S1, the opening paragraph | Taken: `:2305-2312` |

## Lens results

- [R624] MINOR Tests, Conformance - `author-r5/tools/check_b16_figures.py:1193` (`r5_figures_spec.py:1059`) - the line-3200 row reads only B-AAF's count (R624-5-F1).
- [R624] MINOR Conformance, Robustness, Tests, Docs - `author-r5/tools/check_b16_figures.py:2333-2338`; `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3741-3752`; `docs/findings/README.md:15` - spelled-out units are not measurements (R624-5-F2).
- [R624] MINOR Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2608-2616` - round 5's packet directory is not stated (R624-5-F3).
- [R624] PASS RTL - `git diff --stat c20c85bd..3619019350936d5af851933df0b5444ef8387e69` (two Markdown files, no HDL, firmware, script or build file), the 0x8F8 `MCSRV_STAT` decode in `docs/reference/REGISTER_MAP.md` against the page's servo claims (`:3172-3193`, `:3339-3343`), and `docs/design/MEDIA_CLOCK_FOLLOWING.md:1670-1677` (B AAF, B CRF and Switch rows) against `:3186-3207` and `:3228-3238`. The register decode, the six B-AAF terms, the MEDIA_RESET count per Milan v1.2 Table 5.4 and the CLOCK_DOMAIN counter movement agree with `runs/bcrf|baaf/events.jsonl` marks and my poll decode. No interface or module contract changes.

What each unclean lens did check clean, apart from its findings:

- **Conformance:**
  - Every clock-source set was read back and restored. The peer was set to 0 before each case, read back 0, and returned to 1 after the DUT's unbinds, read back 1. The DUT was set to 1 or 2, read back, and restored to 0. `final.equal_to_found` is true in both runs.
  - The binding rule held: no listener format needed setting.
  - The census differs only in the DUT's propagation delay, 0x183 to 0x179, so 387 to 377 ns.
  - The loopback record shows CONNECT_TX (Milan PROBE_TX) at +99.6 and +299.6 ms with no response, and only the DUT's CRF and AAF streams on the peer's link.
  - The source route and clock changes are attributed outside the lane, not to the DUT (`:2488-2492`, `:2769-2799`).
  - The INTERNAL mismatch control is stated as NOT RUN (`:3326-3329`, `:3344-3345`, index row).
- **Robustness:** the incident run (`b0`, McASP busy) is excluded from grading and its restore is verified. The dry-run scenarios and the wrapper's deadline path are published (`controls/b16c-dryrun-summary.json`, `b16c-wrapper-deadline.txt`).
- **Tests:**
  - The 22 controls fail for their defects: 11 of the 14 new ones fail on round 4's check, and the other 3 are forms round 4 already read.
  - The probes are unchanged and re-run, and the build regenerates byte for byte.
  - The check's other rows I sampled read the right receipt fields (B0, B16c, attribution and positive-control rows).
- **Docs:**
  - The hash tables equal their files.
  - The gates pass.
  - No product name and no host path appear.
  - The reference peer and the external capture are referred to by role only.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Issue #629 acceptance and the rulings. `629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2287-3833`, `README.md:15`. `runs/bcrf|baaf/events.jsonl`, `restore/census-compare*.txt`, `summary/loop2/acmp-peer-tap.json` and the r5 check | R624-5 | `3619019350936d5af851933df0b5444ef8387e69` |
| RTL | CLEAN | Diff stat (docs only). `REGISTER_MAP.md` 0x8F8. `MEDIA_CLOCK_FOLLOWING.md:1670-1677`. Poll traces `r2/*-poll-trace.tsv` | R624-5 | `3619019350936d5af851933df0b5444ef8387e69` |
| Robustness | UNCLEAN (F2) | The escape probes, the incident handling and the dry-run controls | R624-5 | `3619019350936d5af851933df0b5444ef8387e69` |
| Tests | UNCLEAN (F1, F2) | `check_b16_figures.py`, `r5_figures_spec.py`, `r5_check_controls.py`, the three reviewer probes, `r5_self_probes.py` and the controls on round 4's check | R624-5 | `3619019350936d5af851933df0b5444ef8387e69` |
| Docs | UNCLEAN (F2, F3) | The page section, the introduction and Contents entry, the index row, the PR #725 title and body, the hash tables, and the gates | R624-5 | `3619019350936d5af851933df0b5444ef8387e69` |

## Real limits

- Documents only. I re-ran no bench measurement. The raw captures, polls and source reads stay off the published packet, so my recomputes start from the published per-block grades, alignments, poll traces and run events. I bound these to the raw hashes through the packet's own records, not by reading the raw files.
- I sampled the check's 1,749 rows for semantic fidelity: the B0, B16c, attribution, positive-control and lane B6 term rows, and every row whose key ignores a loop variable. I did not read every row's key.
- The escape space is open-ended. F2 and S1 list what I tried, not everything that exists.
- The hosted `docs-check` context had not finished when I read it. The other skipped contexts are skips, not executions.
- I ran no Verilator or Yosys build: the diff contains no RTL.
- Physical calibration was NOT RUN. Printed precision is not calibrated accuracy.

## Pending manager duties

- Publish this report and its receipts. Carry R624-5-R1 to the residue checklist.
- Own hosted and act acceptance at the exact head, including the in-progress `docs-check`.
- At the merge turn, build and validate the current-dev merge candidate (source base `c20c85bd`, live dev `c6bd08c6`) with the builder and native banks. No manager source bank ran at this head, and none is claimed or inferred here.
- Post-merge containment, and merge authorization by a maintainer.

## Clone integrity after the probes

The clone was never written; every probe ran on copies.

- HEAD is `3619019350936d5af851933df0b5444ef8387e69`, and `git write-tree` returns `11777358b03b38ceda5ade1e1ed59e31b08473e5`.
- The worktree and index are clean, and the index equals HEAD.
- The gitlinks equal HEAD's: `external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `2ad2f845`, `third_party/lwSRP` `08ee86e8`, `third_party/verilog-axis` `48ff7a7e` (`receipts/clone-integrity.txt`).

R624-5 FINISHED
