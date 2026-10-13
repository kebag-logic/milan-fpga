[R624] POSITIVE - exact head f1b2489f5b1c929e81eeae79a469b2b27c47e340

Round R624-10. Internal, independent, cleared-context review of issue #629 / PR #725 (bench lanes B16, B16b and B16c, documents only), round 10 of the findings. Head `f1b2489f5b1c929e81eeae79a469b2b27c47e340`, tree `635001816412f045f479ec4776fe641969a48815`, source base `c20c85bd`. Evidence: the published packet at `5775cfa78dc9250ea1b689fc2cfa8e20c41281bb` (`review-evidence/629-b16-r1/`, `author-r10/`).

**Verdict.** All five lenses were applied and all five are CLEAN at this head. No BLOCKER, MAJOR or MINOR is open.

- R624-9-F1 is resolved, and so are R624-9-R1, R625-9-F1 and R625-9-R1. Every earlier public finding stays resolved.
- One new RESIDUE (R624-10-R1) is PR-body wording only.
- There are two SUGGESTIONs. S1 concerns a limit the page already states: an ordered list's number is shown to a reader, and no rule judges it. S2 concerns a refusal that fails closed.
- No finding alleges a DUT defect, and no bench figure, verdict or receipt is wrong. All 1,960 figure rows equal their receipts at this head.

This verdict covers this head only. It does not approve a merge or claim that #629 is complete. Direction B's INTERNAL mismatch control and lane B6's timed ratio stay NOT RUN, as the page states, and #645 stays open.

## How the task was reconstructed

Read in order:

1. `AGENTS.md`, then `CONTRIBUTING.md` (section 6: wording, privacy, the pinned renderer).
2. `docs/README.md`.
3. Issue #629's body and its [A10] comments:
   - the B16 assignment 6117305187, and the rulings 6117672835 and 6118365090;
   - the round assignments, up to round 10's 6134101205;
   - the decision 6132293481, and the PR-body note 6133971231.
4. The author's public STOP and REVIEW READY comments, including round 10's 6135221777.
5. `git diff c20c85bd..f1b2489f`: two files, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` with 2,340 added lines and `docs/findings/README.md` row 15, over 13 commits. Then `git diff cb5ff79f..f1b2489f`, round 10, which touches lines 39, 84, 2312, 2616, 4150 and 4309, adds 4425 to 4602, and touches README row 15.
6. Authorities:
   - `docs/reference/REGISTER_MAP.md`: `0x8F8` `MCSRV_STAT`, `0x8E0` `AAFM_STAT`, `0x8E4`, `0x748` `CRF_RATE`;
   - `docs/design/MEDIA_CLOCK_FOLLOWING.md`, its Bench rows B AAF, B CRF and Switch;
   - `tools/markdown/requirements.txt` and `scripts/gen_toc_renderer.py`.
7. The published packet at `5775cfa7`.

The independent pass, its verdict and its ledger draft were written before any prior review finding was read. The R624-9 and R625-9 comments were read afterwards, to resolve them. No private material and no other report was used to form the verdict.

## Round 10 assignment, item by item

| Item (6134101205) | Result at `f1b2489f` | Evidence |
|---|---|---|
| 1. A node with no valid source start, other than a soft or hard break, refuses its whole block at the first covered line | Met. `blocks()`: `bad_start = sl < 1 and kind not in ("", "softbreak", "linebreak")` sets NOPOS on the open leaf, and on a block or enclosing node itself. The 12 missing-start mutations and 3 digit mutations meet, 15 of 15 | `tools/check_b16_figures.py` (`a9f36f9d...`, 199,268 bytes), lines 2911-2938; `receipts/runs-summary.json` `round10_tools`, `reader-controls.json` byte-equal |
| 2. Digit conservation: each covered block rendered with the pinned renderer, its visible digit multiset equal to the digits judged, else the block refused | Met. `shown()` renders the block's own source with uncovered digits written as `x`, with gen_toc_renderer's options and extensions, through html5lib. `sorted(filter(str.isnumeric, ...))` must be equal, else SUM | lines 2760-2777, 2920-2925, 2949-2960; layers: conservation alone catches the entity and escape forms (`layers.json` byte-equal) |
| 3. R624-9's `probe_r624_9_autolink.py`, unchanged; the later-line control; the extents audit; every earlier runner and probe | Met (details below) | `receipts/probe-outcomes-vs-author.json`, `receipts/runs-summary.json` |
| 4. Texts: page, index row, PR body state the rule; R624-9-R1 applied; location paragraph gains round 9 at `author-r9/` (`4ab00ba5`) | Met. The page states the rules at `:4451-4481` and the limits at `:4569-4576`. Pointers are at `:39`, `:84`, `:2312`, `:4150` and `:4309`. README:15 carries "Round 10: ...". The PR body states the rules at lines 494-497 and has the R624-9-R1 text at line 424. `:2616` maps round 9 to `author-r9/`, `cb5ff79f`, `4ab00ba5`, and names `author-r10/` "in a later commit". `5775cfa7` holds it and descends from `4ab00ba5`, with `author-r1/` to `author-r9/` unchanged between them | `git diff 4ab00ba5 5775cfa7 -- author-r1..r9` is empty; `evidence-receipt.json` reproduced byte-equal |

### Executable evidence, run by this review

These ran in a fresh environment installed from `tools/markdown/requirements.txt` with `--require-hashes`: cmarkgfm 2025.10.22, html5lib 1.1, cffi 2.1.1 and pycparser 3.0.

- **The check on the unchanged page.** It exits 0 with 1,960 of 1,960 rows OK. Its 15,597 digits are 12,988 in rows, 2,609 in identifiers and 0 uncovered, with markup 0. Its stdout, rows and coverage are byte-equal to the published `r10/figures-check.stdout`, `r10/figures-rows.tsv` (`ccaae4a0...`) and `r10/figures-coverage.tsv` (`f8cc3827...`).
- **R624-9's probe, unchanged.** `probe_r624_9_autolink.py` (`a77ad603...`) is byte-equal to `reviews/R624-9/tools/`. The unchanged page passes, and all 14 detect cases exit 1:
  - The `www.`, `https://` and plain cases each name `UNCOVERED ...:19 7` or `README.md:15 7`, at the true line.
  - The e-mail and `mailto:` cases are refused as MARKUP at their block's first covered line. That is `:18` for the introduction, with the edit at 19; `:2301` for the section paragraph, edited at 2301 or 2302; `:2324` for the table cell; and `README.md:15` for the index row. I confirmed the index refusal on the probe's own altered tree.
  - No case escapes. This is the outcome item 1 prescribes.
- **All 15 published review probes, unchanged.** Each is byte-equal to its `reviews/R62x-n/` original. All 15 reproduce the author's `r10/*-probe-rerun.json` case by case on exit status, verdict and every named line: 202 cases, 202 equal. R625-6's `probe_rendered_comment.py` exits 1 on its own frozen round-6 assertion, as the author records. That probe's comment cases are superseded by round 7's refusal of markup.
- **Control runners against the new check.** The rounds 3 to 9 runners pass 5/5, 7/8, 21/22, 38/39, 48/50, 73/73 and 97/97. Every FAIL is one of the two expectations superseded by decision 6132293481: "a figure with its unit added as a link label" in r4 to r7, and "a comment inside a code span" in r7.
- **Round 10's runner.** It passes 117/117. Against round 9's check and page at `cb5ff79f`, it passes 103 of 117: the 97 earlier and 6 new controls pass, and the 14 new controls fail. Every verdict equals the published `controls/r10-*.json`.
  - The later-line control works as asked. A `www.` or `https://` address before a figure on line 2302 is named `UNCOVERED :2302 7` with nothing at 2301. The e-mail form on 2302 is refused at `:2301` as a whole block, per item 1.
- **Round 10's tools, all byte-equal to their published outputs.**
  - `r10_parser_extents.py`: 37 + 22 cases met (12 no-line forms, 3 no-column forms, 7 placed).
  - `r10_layers.py`.
  - `r10_reader_controls.py`: 15/15.
  - `r10_self_probes.py`: 172 met.
  - `r10_reader_on_r9.py`: rows, coverage and stdout equal.
  - `r10_evidence_receipt.py` at (`4ab00ba5`, `cb5ff79f`).
  - `r10_figures_build.py` regenerates the check byte for byte.
- **Documentation gates at the head, pinned environment.** All are rc 0:
  - `docs_check.py`: 0 findings, scrub self-test 23/23;
  - `check_doc_style.py` and `check_doc_paths.py`;
  - `gen_toc.py --check` and `--verify-anchors`;
  - `check_em_dash.py --base c20c85bd`: 0 over 2,341 added lines;
  - `git diff --check c20c85bd HEAD`.
- **Published packet binding.**
  - `MANIFEST.json` at `5775cfa7` holds 7,731 entries. Every published file hashes to its `published_sha256`, and the hashes differ exactly where `path_redacted` is set: 75 files in `author-r10/`. No unlisted file exists.
  - `author-r10/MANIFEST.sha256` (936 lines) equals each entry's `original_sha256`.
  - The stated hashes of the check, the spec, the build tool, `controls/r10-controls.json`, the rows, the coverage and `probe-comparison.json` equal the published files.
- **Every hash row of the section** (`receipts/hash-rows-vs-published-r10.json`). There are 156 rows:
  - 114 packet rows equal `author-r10/`'s original SHA-256, and size and hash where the file is not redacted;
  - 42 raw rows are listed in `RAW-ARTIFACTS.json`.

  My parser misread the two playback-log rows at `:3603-3604`, whose penultimate cell is an underrun count. Their SHA-256 is listed under `playback/` with the size withheld.
- **Own escape forms** (`receipts/probe_r624_10_own_forms.json`, `receipts/probe_r624_10_list_markers.json`).
  - These are detected: decimal and hexadecimal entities before a unit; `&half;`; struck text; a figure as a resolving link's text; `7. ppm` in a table cell; an entity in a cell and in the index row's covered part; a `:seven:` shortcode, by its number word.
  - Ordered-list numbers pass, which is a stated limit: see S1.
  - `&half;` before the index row's covered part is refused, which fails closed: see S2.

## Bench content checked independently (Conformance, RTL)

`spot_check_r624_10.py` reads only per-block grades, raw poll words and run events from `author-r10/` (`receipts/spot-check.json`).

- **B0, `b0-2`.**
  - THD+N over all blocks: -123.95 (-100.47) and -122.80 (-80.48) dB.
  - The floor holds 169 blocks, at -123.98 (-123.91) and -123.95 (-120.18) dB.
  - 131 blocks are degraded, in 15 runs: 0-18, 28-31, 43-44, 46-54 and eleven later runs. 23 lie in blocks 0-33 and 108 beyond them, in 13 runs.
  - The worst block of each tone is 224, and block 7 reads -100.61 and -80.63 dB.
  - Phase moved 0.0005 frames, and the largest block offset is 0.030 ppm.

  These equal `:2822-2834` and `:2842`.
- **B-CRF and B-AAF.** All 300 blocks are at the floor, at -123.98 (-123.93) / -123.97 (-123.90) and -123.98 (-123.92) / -123.97 (-123.91) dB, with 0 events.
- **Polls, decoded by REGISTER_MAP.**
  - `0x8F8` `[2:0]` 4 is LOCKED. The word reads `0x34` (bit 4 DRP mismatch, bit 5 MMCM locked) or `0x74` (bit 6 fine-PS busy), and IDLE reads `0x20`.
  - `AAFM_STAT` `0x001e0007` decodes as locked, rate valid, enabled, listener 0, 0 restarts and 30 ns.
  - LOCKED brackets: 2.585 to 3.161 s (polls 44 and 45) and 6.602 to 7.180 s (polls 52 and 53).
  - The window holds 596 polls, all LOCKED, at 580/16 and 584/12. A poll straddling the window's end is excluded, as the receipt's rule says.
  - Trim runs -6.000 to -6.125 ppm. CRF runs +10.60 to +10.65 and +10.59 to +10.65 ppm, and the AAF meter +10.60 to +10.63 ppm. `SLIP_TDM` is 0 throughout.

  These equal `:3172-3185` and `:3200`.
- **Clock sources** (`runs/bcrf|baaf/events.jsonl`). In each case:
  1. the peer is set to 0, SUCCESS, read back 0;
  2. the DUT is set to 1 or 2 and read back;
  3. the DUT is set back to 0 and read back;
  4. the unbinds follow;
  5. the peer is set back to 1, read back 1.

  The final record reads `equal_to_found: true`, `differ: []`. The census of B16c holds 45 of 46 equal, the start record included; the other entry is the DUT's propagation delay. These match `:3084-3098`, `:3290-3296` and the ruling 6118365090.
- **Design and attribution claims.**
  - The design's bench row B AAF (`MEDIA_CLOCK_FOLLOWING.md:1670`) equals the six terms at `:3188-3193`. B CRF is "As B6" (`:1671`), and one MEDIA_RESET per switch is declared under Milan v1.2 Table 5.4 (`:1677`).
  - The INTERNAL mismatch control is stated NOT RUN at `:3321`, `:3326` and `:3344`, and lane B6's timed ratio at `:3202-3207` and `:3336-3338`.
  - The tone source's route and clock changes are attributed outside the lane, at `:2488-2492` and `:2769-2799`.
  - B0's 23 blocks shown directly are separated from the 108 assigned by inference, at `:2836-2845`, `:2931-2934` and `:3255-3265`.
- **Privacy.** The repository's identity scrub (`docs_check.scrub_text`) and a host-path and IPv4 sweep find nothing in the PR body or in the diff's added lines (`receipts/public-text-scrub.json`). The reference peer and the external capture are named only by role.

## Findings

### R624-10-R1 - RESIDUE - Docs

**Where:** the PR #725 body, "Round 10", line 500 of the body as fetched at head `f1b2489f`: "Local commit: `f1b2489f5b1c929e81eeae79a469b2b27c47e340`, not pushed."

**Why:** the commit is now the PR's published head. The sentence was true when written, but it now misstates the branch's state. It is wording only: it changes no measurement, figure, verdict, test, code, generated artifact or clause claim, and it touches no privacy rule.

**Exact fix:** replace "Local commit: `f1b2489f5b1c929e81eeae79a469b2b27c47e340`, not pushed." with "Commit: `f1b2489f5b1c929e81eeae79a469b2b27c47e340`, the PR head."

### R624-10-S1 - SUGGESTION - Tests, Docs

**Where:** `tools/check_b16_figures.py` `blocks()`. Only paragraphs, headings and table cells are leaves, so an ordered list's number, which the parser holds on the `list` node, is never read. The page states this at `:4041-4042` (round 7) and `:4181-4182` (round 8): "A list's numbers are not text, so a numbered item that is only a unit passes". `:4569` keeps it.

**Evidence** (`receipts/probe_r624_10_list_markers.json`):

- Each of these, appended after the page's last line, renders `<ol start="17">` (or `131`), and the check exits 0 with nothing named:
  - `17. ppm: the peer's offset in B-AAF, against the DUT's TDM clock.`
  - the same written with `17)`;
  - `131. blocks sat off the floor in B-CRF, not none.`
- So does `> 17. ppm, ...` (`probe_r624_10_own_forms.json`).
- Renumbering the page's own lists also passes. Line 2879's list made to start at 7, or line 3025's at 300, gives exit 0.

**Why only a suggestion:** the limit is disclosed in the page's own limits paragraphs, and no figure on the page today is written as a list number. One sentence reads as wider than the rule, though. Round 10's closing line, `:4578-4579`, says "every digit lies in a claimed figure or in an identifier", and the section's existing list numbers (`:2879-2883`, `:3025-3044`) are digits a reader sees that lie in neither.

**Suggested outcome:** have the check judge an ordered list's displayed numbers as covered digits. For example, refuse an ordered list in the covered text that does not start at 1, or bind the numbers 1 to n of such a list as a list-ordinal identifier. Alternatively, make `:4578-4579` read "every digit of the text it reads".

### R624-10-S2 - SUGGESTION - Tests, Docs

**Where:** `blocks()`, the conservation source at lines 2951-2957. Only characters that are `isnumeric()` outside the covered text are written as `x`. A named entity outside it that renders a numeral, `&half;` for example, stays live.

**Evidence:** `&half; ` written just before the index row's `Lane B16, `5603c353`:` is refused, exit 1, as `MARKUP README.md:15 table_cell ... (refused: the digits a reader sees differ from those the check read)`. No covered digit changed (`probe_r624_10_own_forms.json`, `index_half_entity_before_covered_part`).

**Why only a suggestion:** the refusal fails closed and loses nothing. The page's limit at `:4573-4576` names a different cause of a refusal that loses nothing, a block rendered outside its context.

**Suggested outcome:** optionally, count only the covered text's rendered digits, or add this cause to the stated limit.

## Earlier public findings at this head

| Finding | Lenses | Status at `f1b2489f` | Evidence |
|---|---|---|---|
| R624-9-F1 (text after a bare e-mail or `mailto:` autolink unread) | Conformance, Robustness, Tests, Docs | RESOLVED | Its unchanged probe has no escape, and each case is refused at its block's first covered line or named at its own line. 14 standing controls fail on round 9's check and pass here. The extents audit gains 22 zero-position cases. The rule is stated on the page (`:4451-4466`), in README:15 and in the PR body (494) |
| R624-9-R1 (PR body, probe readings "byte for byte") | Docs | RESOLVED | PR body line 424 carries the exact replacement text |
| R625-9-F1 (PR body, the probe delay's origin) | Docs | RESOLVED | PR body line 31: "99.6 ms after the unbind command". It equals the page's origin, `:2423`, and `summary/loop2/acmp-peer-tap.json`: DISCONNECT_RX_COMMAND at 2.6006 s, the first CONNECT_TX_COMMAND at 2.700216 s and the second at 2.900231 s, with no CONNECT_TX_RESPONSE |
| R625-9-R1 (PR body, footnote locator) | Docs | RESOLVED | PR body line 424: "line 4426 instead of 4274". Line 504 records the move to 4604, which my rerun of R624-7's probe reproduces |
| R624-8-F1, R625-8-F1 (decision 6132293481), R624-7-F1, R625-7-F1, R625-6-F1, R625-5-F1, R624-5-F1/F2/F3, R624-4-F1, R625-4-F1, R625-3-F1, R624-3-F1, R624-1-F1/F2, R625-1-F1 to F4, R624-2-F1/F2, R625-2-F1 | Conformance, Robustness, Tests, Docs | RESOLVED, held | All 15 probes and 9 runner sets reproduce the recorded outcomes. Every row is OK. Outside round 10's own section, round 10 changed only pointer sentences. The decision is recorded at `:4343-4355` and `:4537-4541` |
| Earlier RESIDUE and SUGGESTION items, including R624-8-S1 (emoji, link title) | Docs, Tests | TAKEN or RESOLVED, held | Text unchanged; the stated limits are at `:4401-4405` and `:4569-4576` |

## Reviewer ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round 10 assignment items 1-4 against `check_b16_figures.py:2760-2977` and its controls. The B16, B16b and B16c scope rulings against `:2287-3399`. `receipts/spot-check.json` (B0, B-CRF, B-AAF, brackets, clock sources, final state). PR body lines 31, 424 and 494-504 | R624-10 | `f1b2489f5b1c929e81eeae79a469b2b27c47e340` |
| RTL | CLEAN | The diff holds no RTL, firmware or tooling, only two Markdown files (`git diff --stat c20c85bd..f1b2489f`). The DUT behaviour claims were decoded against `REGISTER_MAP.md` `0x8F8`, `0x8E0`, `0x8E4` and `0x748`, and against `MEDIA_CLOCK_FOLLOWING.md:1661-1678`: `0x34`/`0x74`/`0x20`, `0x001e0007`, trim and rate units, one MEDIA_RESET per switch | R624-10 | `f1b2489f5b1c929e81eeae79a469b2b27c47e340` |
| Robustness | CLEAN | `blocks()` NOPOS and SUM paths. 15 reader mutations. 12 own escape forms, and 8 list cases (5 list-number forms, 3 controls): every undisclosed form is detected, and the list numbers are a stated limit (S1). Fail-closed refusal (S2). Clone integrity after the probes | R624-10 | `f1b2489f5b1c929e81eeae79a469b2b27c47e340` |
| Tests | CLEAN | Check on the unchanged page (byte-equal outputs). 15 review probes (202 cases equal). Runners r3-r10 and r10 on round 9 (all verdicts equal). 7 round-10 tools byte-equal. The rebuild is byte-equal. `receipts/runs-summary.json`, `probe-outcomes-vs-author.json` | R624-10 | `f1b2489f5b1c929e81eeae79a469b2b27c47e340` |
| Docs | CLEAN (one RESIDUE carried) | Page `:39`, `:84`, `:2312`, `:2616`, `:4150`, `:4309` and `:4425-4602`. README:15. PR body. 156 hash rows against `author-r10/`. Manifest binding at `5775cfa7`. 7 documentation gates rc 0. Privacy scrub of the PR body and the added lines | R624-10 | `f1b2489f5b1c929e81eeae79a469b2b27c47e340` |

## Real limits of this review

- **No bench.** This review did not touch the bench. Its bench evidence is the published packet's reduced and per-block receipts. The raw captures (pcap, McASP and external-capture files) stay with the operator and were not re-decoded here. Physical calibration was NOT RUN, and printed precision is not calibrated accuracy.
- **Rendering.** The check, and my probes, read the pinned cmark-gfm, not GitHub's live renderer. GitHub's differences are disclosed (CONTRIBUTING section 6 and the page's limits).
- **Hosted CI.** The exact head's hosted contexts were only inspected:
  - Completed with success: `rtl-fast`, `changes`, `full-ci-gate`, `verilator-lint`, `yosys-elaboration`, the four Yosys shards and `docs-check-no-git`.
  - Still in progress at inspection: `docs-check`, `elaborate` and the five Verilator shards.
  - Skipped, not executed: `Physical gPTP`.

  No manager source bank was run or inferred at this head.
- **The checker's coverage.** The figures check covers lane B16's section, the introduction's lane B16 part, its Contents entry and README:15. The rest of the page is outside it, and was judged here by reading.

## Pending manager duties

- Publish this report and the listed receipts.
- Carry R624-10-R1 to the residue checklist.
- Hosted and local-replica acceptance at the exact head: `docs-check`, `elaborate` and the Verilator shards were still running when inspected.
- At the merge turn, the current-dev merge candidate: source base `c20c85bd`, live dev `d5858bbee328cf8d2c39a99ec14203f5d0ddd123`, with the builder and native banks.
- The external review, and the two-positive bar.
- Issue #629 stays open for Direction B's INTERNAL mismatch control, lane B6's timed ratio for B-CRF and B-AAF, and #645.

R624-10 FINISHED
