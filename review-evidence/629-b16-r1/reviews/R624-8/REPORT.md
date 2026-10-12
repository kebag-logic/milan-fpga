[R624] NEGATIVE - exact head b522bb923fa59581478460b61633bce2cb90ac1d

Round R624-8. This is an internal, independent, cleared-context review of issue #629 / PR #725: bench lanes B16, B16b and B16c, findings round 8, documents only.

- Tree: `66bd4852a98ca1065549515aa3c677d2fe482132`.
- Comparison: `c20c85bd..b522bb923fa59581478460b61633bce2cb90ac1d`. That is eleven commits touching two Markdown files, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and `docs/findings/README.md`. No HDL, firmware, script or gitlink changed.
- Evidence: the published packet on `629-b16-review-evidence` at commit `b0134c639a35a731787dd62586fca6c4500842c8`, directory `review-evidence/629-b16-r1/author-r8/`.

All five lenses were applied. Every bench figure in the section still equals its receipt. Both round 7 MINORs are resolved at this head: R624-7-F1 (the image route) and R625-7-F1 (the crash on the index row). Every earlier finding stays resolved.

One new MINOR is open, R624-8-F1. A raw HTML `<pre>` block can open on the uncovered line just above the covered introduction and close on its first covered line. The figures check then neither refuses it nor reads it, while a reader sees the text inside it. With an unreceipted measurement added there, the check exits 0. The cause is the parser's source position for such blocks, which the check trusts.

- RTL is CLEAN.
- Conformance, Robustness, Tests and Docs are UNCLEAN under F1.
- No current figure is wrong and no DUT defect is alleged. The unchanged page contains no raw HTML, and its 1,867 rows all equal their receipts.

## Order of work

I wrote the verdict and the finding after my independent pass over the diff, the check and the probes. Only then did I read the prior public review findings (R624-1 to R624-7, R625-1 to R625-7) and resolve each of them below. The round 8 assignment names R624-7-F1 and R625-7-F1, so I knew their titles from the start.

## Method

**Context.** I read AGENTS.md and CONTRIBUTING.md (by section), docs/README.md and the issue body. I then read the B16 assignment (6117305187), both rulings (6117672835, 6118365090), the round 2 to round 8 assignments (the latest is 6130721355) and the round 8 handoff (6132021882). I also read the live PR body.

**Packet integrity.** `MANIFEST.json` at `b0134c63` has 5,646 entries, 771 of them in `author-r8/`. The checks:

- Every `author-r8/` file equals its `published_sha256`.
- The published and original hashes differ exactly where `path_redacted` is set, which is 57 files.
- All 770 lines of `author-r8/MANIFEST.sha256` equal the `original_sha256`.
- All 35 hash rows of the handoff table and all 98 packet-file hash rows of the section equal their `author-r8/` files.

The receipt is `receipts/packet-and-figures.json`.

**Environment.** A disposable environment was installed from `tools/markdown/requirements.txt` with `--require-hashes`: cmarkgfm 2025.10.22, cffi 2.1.1, html5lib 1.1.

**What I ran, offline, on copies only.** The tools are in `tools/` and the outputs are in `receipts/`.

- The figures check at the head (`receipts/check-at-head.*`):
  - exit 0;
  - 1,867 of 1,867 rows OK;
  - 14,442 digits, of which 12,164 are in claimed figures, 2,278 are in identifiers that count and 0 are uncovered;
  - 0 constructs refused;
  - rows and coverage byte-equal to `author-r8/r8/`.
- The author's round 8 tools, on a copy of `author-r8/` (`receipts/reruns/summary.txt`):
  - the check rebuilds byte for byte from its spec;
  - `controls/r8-controls.json` is byte-equal, 73 of 73 PASS;
  - `r8/self-probes.json` is byte-equal: 138 forms, 108 detected and 30 stated passes;
  - `r8/evidence-receipt.json` is byte-equal;
  - all 13 probe-rerun receipts are byte-equal.
- The probes. All 13 review probes in `author-r8/tools/review-probes/` are byte-identical (by git blob) to the reviewers' originals under `reviews/` (`receipts/review-probes-vs-originals.txt`). I also ran R624-7's and R625-7's probes directly, unchanged (`receipts/reruns/`).
- My own probe, `tools/probe_r624_8_html_block_edge.py` (`receipts/probe-html-block-edge.json`), plus a dump of the parser's node positions (`tools/dump_tree.py`, `receipts/parser-positions.txt`).
- Independent recomputation of key bench figures from the receipts, not through the check (`tools/verify_r8_packet_and_figures.py`, `receipts/packet-and-figures.json`).
- Documentation gates (`receipts/gates/`). Hosted checks, read only (`receipts/hosted-checks.txt`).

## Finding

### R624-8-F1 - MINOR - Conformance, Robustness, Tests, Docs

**A raw HTML block that opens just above the covered text and closes on its first covered line is neither refused nor read.**

**Artifacts:**

- `author-r8/tools/check_b16_figures.py`:
  - `:2759-2760` takes the parser's end position, clamped only when it lies before the start;
  - `:2769` computes the first covered line, `at`, over `range(sl, el + 1)` from that end;
  - `:2770-2772` skips a node with no covered line in that range, and everything under it, without refusing it.
- `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`:
  - `:4152-4159`: "Any other construct is refused at the first line of it that the check covers ... raw HTML inline or as a block";
  - `:4189-4190`: "A construct that starts above the section and runs into it is refused at the first line of it that the check covers."
- `docs/findings/README.md:15`, round 8: "any construct off a closed allowlist, an image or raw HTML among them, is refused at its line and named".
- PR #725 body, Round 8 item 2: "Anything else is refused at its first covered line".

**Authority:** the round 8 assignment, items 1 and 2: judge the visible text the pinned parser yields, and refuse at its line any construct outside the closed allowlist, raw HTML blocks included. Also the round 5 assignment, item 2: a digit run followed by a unit belongs only to a row.

**Evidence:**

`receipts/probe-html-block-edge.json`. Each case replaces whole lines of a copy of the page, so no line moves. In case `intro_pre_from_line_above_with_figure`:

- line 17, the uncovered line above the covered introduction (`:18`), becomes `<pre>`;
- line 18 gets ` THD+N -90 dB</pre>` appended.

The pinned renderer emits `<pre>\nIn lane B16, the operator tried the reference peer's own loopback as the positive reference THD+N -90 dB</pre>`, so a reader sees the measurement. The check exits 0 with 1,867 rows OK, 0 uncovered and 0 markup.

The cause is in `receipts/parser-positions.txt`. For HTML blocks of kinds 1 to 5 (`<pre>`, `<script>`, `<style>`, `<textarea>`, comments, `<?`, `<!X`, CDATA), cmark-gfm reports the end as the line before the closing line:

- `<pre>` on line 2 closed on line 3 is reported as `2:1-2:5`;
- a one-line comment on line 3 is reported as `3:1-2:0`.

So for a block that opens on line 17 and closes on line 18, `range(sl, el + 1)` holds only line 17, which is not covered. The block is skipped silently: neither refused nor read.

Controls in the same receipt behave as stated:

| Case | Result |
|---|---|
| The same `<pre>` closed on the second covered line | `MARKUP ...:18 html_block` |
| A `<div>` block (kind 6) opened on line 17 | `MARKUP ...:18` |
| A `<pre>` block inside the section, on one line or two | MARKUP at its line |
| Heading and Contents variants | Fail only by side effect: a row's figure or an anchor is lost. Not refused |
| An HTML comment over the heading | Hides the text from both the reader and the check |

**Impact:**

- A future edit can place a visible, unreceipted measurement on the first covered line of a covered region whose line above is outside the region, and the check passes it.
- The texts state that such a construct "is refused at the first line of it that the check covers", which is not true for these block kinds.
- This changes executable validation behaviour and an evidence claim, so it is not wording-only RESIDUE.
- No current figure is affected: the covered text holds no raw HTML, and the check reports 0 markup.

**Required outcome:**

- Any construct off the allowlist whose actual source extent reaches a covered line is refused at that line, whatever end position the parser reports. For example, an `html_block`'s last line can be taken from its literal (start line + literal lines - 1) or from the source, not from the node's end.
- A standing control: case `intro_pre_from_line_above_with_figure` must fail with MARKUP at the introduction's first covered line.
- The page, the index row and the PR body state the rule as it then holds.

**Verification:** run `tools/probe_r624_8_html_block_edge.py` unchanged under the pinned environment. `intro_pre_from_line_above_with_figure` must be DETECTED with `MARKUP 629_MEDIA_CLOCK_FOLLOWING_BENCH.md:18 html_block`, and every other case keeps its outcome. Then re-run the controls runners, the 13 review probes and the unchanged page.

### R624-8-S1 - SUGGESTION - Docs, Tests

The check's reader is cmark-gfm. GitHub renders two things it does not model:

- Emoji shortcodes. `CLOCK_DOMAIN 7:smile:ppm.` passes, because the shortcode's colon counts as a phrase-ending mark, while GitHub shows a glyph between the 7 and the unit (case `emoji_shortcode_between_identifier_and_unit`).
- Link titles, which GitHub shows as hover tooltips. A figure in a link title passes (case `link_title_with_figure`). The page states titles are not read, but calls them text "the reader" does not see.

Both are consistent with the assignment's model, which judges what the pinned parser yields. Optionally, either:

- state both in "What the rule does not cover" (`:4179-4190`); or
- refuse `:word:` shortcodes and link titles in the covered text.

## Round 8 assignment, item by item

| Item | Result | Evidence |
|---|---|---|
| 1. Read through the pinned parser; judge only visible inline text; source maps for lines | Met, except F1 | `bind()` `:2637-2661` verifies the versions with `scripts/gen_toc_renderer.py`'s `verify` and the renderer's extensions and options. `blocks()` `:2737-2797` reads only text, code (with code marks) and link text. Line numbers are the parser's positions. Without the parser the check exits 1 naming it (control 73). F1 is a case where the parser's position is wrong for a refused block |
| 2. Closed allowlist; images, raw HTML and anything else refused at its line; only exact generator markers excepted; hand-written comment and markup regexes gone | Met, except F1 | `ALLOWED` `:2618-2619`; `GENERATED` `:2621-2622`, matched as a whole line byte for byte. Controls cover image, html_inline, html_block, fenced and indented code, thematic break, strikethrough, footnote reference and definition, and task list item, each named. No `MARKUP` regex and no comment, tag or entity alternatives remain in `SEP` (`:2460`) or `PAST` (`:2477-2478`) |
| 3. R625-7: the index row through the same path; named `README.md:15` refusal; both receipts; no traceback | Met | `probe_markup.py`, unchanged: the four index markup cases each print `MARKUP README.md:15 html_inline ...`, with `rows_written` and `coverage_written` true and `exception` false; the ordinary-digit case is UNCOVERED at `README.md:15` (`receipts/reruns/r625-7-markup.json`, `pm.stdout`) |
| 4. Controls: R624-7's image forms, R625-7's four index cases, one per refused construct; earlier controls and probes keep their outcomes; unchanged page passes | Met. Two expectations changed, for the manager's ruling | `probe_r624_7_markdown_escapes.py`, unchanged: `escapes` false for every form, all 8 image forms exit 1, and exit 0 only for the unchanged page and the stated full-stop form. `probe_r624_7_invisible.py`: all 10 exit 1. Controls are 73 of 73 PASS. The two changed expectations (round 4's link-label control, round 7's comment inside a code span) still have the check exit 1 and name the added number; both follow from item 1, and I see no reason to keep the old expectations. Likewise R624-6's "any" form `link-ref-title` renders nothing, and its pass is correct |
| 5. Texts state the rule; the location paragraph maps round 7 to `author-r7/` (`fa974c3f`) | Met for the mapping; the texts overclaim under F1 | `:2616` maps `author-r7/` (archived at `295ba9d7`, published by `fa974c3f`) and names `author-r8/`, which `b0134c63` publishes. `r8_evidence_receipt.py` re-run is byte-equal: 4,711 entries, 93 of 93 rows, 706 of 707 files |

**Earlier rounds' items, rechecked at this head.**

- Round 3: the check covers every summary and attribution figure (1,867 rows OK).
- Rounds 4 and 5: per-digit coverage and spellings. R624-4's probe detects 8 of 8, R625-4's 12 of 12 and R625-3's 7 of 7.
- Round 6: the closed follower list and per-case LOCKED. Both line-3200 probes MISMATCH as before.
- Round 7: comments and tags are refused. R625-6's statuses are `[0, 1, 1, 1, 1, 1]`.

All 13 rerun receipts are byte-equal to the author's.

## Independent results by lens

`[R624] PASS RTL` - `git diff --raw c20c85bd..b522bb92` (two `100644` Markdown files only; gitlinks unchanged, `receipts/clone-integrity.txt`) and `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:403-409` (status `[2:0]`: ACQUIRE 3, LOCKED 4). No RTL, firmware or interface change. The poll decode matches the RTL encoding:

- polls 44/45 (B-CRF) and 52/53 (B-AAF) read state 3 and then 4;
- the brackets are 2.585-3.161 s and 6.602-7.180 s;
- the window holds 596 of 596 LOCKED polls in each case, with 580/16 and 584/12 at `0x..34`/`0x..74`.

**Conformance** (examined; unclean only under F1):

- **B16.** `summary/loop2/acmp-peer-tap.json` shows CONNECT_TX_COMMAND (Milan's PROBE_TX) at +99.6 and +299.6 ms from the UNBIND, with no response. The loopback did not form.
- **B16b, B0.** `summary/b0-2/c-b9-grade.json`:
  - 169 blocks at the floor, medians -123.98 and -123.95 dB;
  - all-block medians -123.95 and -122.80 dB, worst -100.47 and -80.48 dB;
  - 0 events.

  `r2/b0-2-receipt.json` gives 131 degraded blocks: 23 inside the 34.1136 s overlap and 108 beyond it, stated as inference. The recording starts 26.0 s after the binds. (c) equals (a) in 3,077,452 frames and (b) in 3,077,980 over the four runs. THD+N is about -124 dB, as assigned.
- **B16c.** `summary/{bcrf,baaf}/c-b9-grade.json`:
  - 300 of 300 blocks at the floor, medians -123.98 and -123.97 dB, 0 events;
  - (d): 0 net steps over 14,583,391 and 14,585,924 frames;
  - (c) equals (a) and (b) in 3,289,015 and 3,290,863 frames.
- **Clock sources and restore.** `runs/{bcrf,baaf}/events.jsonl` record each `set-clock` with its readback: peer 0, DUT 1 or 2, DUT restored to 0, then peer restored to 1. `restore/census-compare-b16c.txt` matches 45 of 46 entries; the one difference is the DUT's propagation delay. Lane B6's four terms are stated, with the timed ratio NOT RUN. The INTERNAL mismatch control is stated as not run (`:3321`, `:3326-3329`, `:3344-3345`, the index and the PR body). The tone source's route and clock changes are attributed as outside the lane.
- **Privacy.** No host path, address, e-mail or equipment name appears in the added lines or the PR body. The reference peer and the external capture are not named.

**Robustness** (examined; unclean only under F1). The check under adversarial input:

- 13 review probes;
- 138 self-probes;
- 73 controls;
- my 13 cases: HTML blocks at a region's edge and inside it, a comment, a link title and an emoji shortcode.

Everything except F1 behaves as stated.

**Tests** (examined; unclean only under F1):

- Each new round 8 control fails on round 7's check: 25 fail and 48 pass (`controls/r8-controls-on-r7-check.json`, hash on the page).
- The check reproduces its outputs byte for byte.
- F1 is a false pass of the check itself, and no control covers a block whose parser end falls short.

**Docs** (examined; unclean only under F1):

- The round 8 subsection, introduction, Contents line, `:2312` pointer, `:4026` pointer, location paragraph, index row and PR body describe the round. The rendered extraction commands are unchanged in content.
- Documentation gates, all rc 0:
  - `docs_check.py`, `check_doc_style.py`;
  - `gen_toc.py --check` and `--verify-anchors`;
  - `check_em_dash.py --base e8454e27`: 0 findings over 4,004 lines;
  - `check_doc_paths.py`, `ci_scope.py --selftest`;
  - `check_baremetal_only.py --check` and `--selftest`, under the system interpreter, which has the YAML module the parser environment lacks;
  - `check_feature_status.py --self-test`;
  - `git diff --check`, and `git diff --check c20c85bd HEAD`.
- The texts overclaim the refusal rule under F1.

## Prior public findings at this head

| Finding | Lenses | Status at b522bb92 | Evidence |
|---|---|---|---|
| R624-7-F1 (image syntax hid a phrase mark) | Conformance, Robustness, Tests, Docs | RESOLVED | R624-7's probe, unchanged: no form escapes; the 8 image forms exit 1 with `MARKUP ... image` and the digit UNCOVERED at 3011; 8 standing controls |
| R625-7-F1 (index-row markup crashed the check) | Conformance, Robustness, Tests, Docs | RESOLVED | R625-7's probe, unchanged: the 4 index cases are named `MARKUP README.md:15 html_inline`, receipts written, no exception; 4 standing controls |
| R625-6-F1 (short comments) | Conformance, Robustness, Tests, Docs | RESOLVED | Statuses `[0, 1, 1, 1, 1, 1]`, byte-equal rerun; the comments are refused as `html_inline` |
| R624-1-F1 = R625-1-F3 (B0 figures) | Conformance, Tests, Docs | RESOLVED | Floor medians -123.98/-123.95 dB over 169 blocks; recording at 26.0 s after the binds; rows OK |
| R624-1-F2 = R625-1-F4 (lane B6's four terms) | Conformance, Tests, Docs | RESOLVED | `:3198-3207`: three met, the timed ratio NOT RUN |
| R625-1-F1 (shown against inferred attribution) | Conformance, Tests, Docs | RESOLVED | 23 inside, 108 by inference (`:2829-2845`, index, body) |
| R625-1-F2 = R624-1-S2 (reduced receipts) | Tests, Docs | RESOLVED | `r2/` receipts bound to raw hashes; the extraction commands now a code-span list, content unchanged |
| R624-1-R1/R2, R625-1-R1/R2 | Docs | RESOLVED | Title as requested; the counter-mark timing is exact |
| R624-1-S1, R625-1-S1, R624-2-S2, R625-2-S1, R625-3-S1 | Docs | TAKEN | "44 of 45 reads equal, the census's start record aside" |
| R624-2-F1 (positive-control floor counts) | Robustness, Tests, Docs | RESOLVED | 303 of 303 and 11 of 13; rows OK |
| R624-2-F2 (LOCKED bracket) | Tests, Docs | RESOLVED | Recomputed above from the traces |
| R624-2-R1/R2/R3, R624-2-S1 | Docs | RESOLVED / TAKEN | Text unchanged since R624-7 confirmed them |
| R625-2-F1 (exact replacement at (a)) | Conformance, Tests, Docs | RESOLVED | `:3244`; rows OK |
| R624-3-F1, R624-5-F3 (where the packet is) | Docs | RESOLVED | `:2608-2616` through `author-r7/`, naming `author-r8/` |
| R625-3-F1; R624-4-F1, R625-4-F1 | Conformance, Robustness, Tests, Docs | RESOLVED | Detected 7 of 7, 8 of 8 and 12 of 12, unchanged probes |
| R624-5-F1 (line-3200 row per case) | Tests, Conformance | RESOLVED | Both line-3200 probes give MISMATCH, byte-equal |
| R624-5-F2 (spelled-out units) | Conformance, Robustness, Tests, Docs | RESOLVED | 21 of 25; the four undetected forms are stated limits, unchanged |
| R625-5-F1 (comment over a line break) | Conformance, Robustness, Tests, Docs | RESOLVED | `[0, 1, 1]` |
| R624-5-R1, R624-4-S1, R624-5-S1, R624-6-S1, R624-6-S2 | Docs, Tests | RESOLVED / TAKEN | Text unchanged since confirmed |

No earlier BLOCKER, MAJOR or MINOR is retained.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R624-8-F1) | Findings `:2287-4272`, `README.md:15`, PR body; `author-r8` summaries, `r2/`, `runs/*/events.jsonl`, `restore/`; round 8 assignment items 1-5 | R624-8 | b522bb923fa59581478460b61633bce2cb90ac1d |
| RTL | CLEAN | `git diff --raw c20c85bd..HEAD`; gitlinks; `KL_mmcm_drp_servo.sv:403-409`; poll traces | R624-8 | b522bb923fa59581478460b61633bce2cb90ac1d |
| Robustness | UNCLEAN (R624-8-F1) | `check_b16_figures.py` `blocks()`/`tree()` under 13 review probes, 138 self-probes, 73 controls and 13 own cases; restore records | R624-8 | b522bb923fa59581478460b61633bce2cb90ac1d |
| Tests | UNCLEAN (R624-8-F1) | Check (`2eb5a24e...`), rebuild, controls r8 and r8-on-r7, probe reruns, own probe | R624-8 | b522bb923fa59581478460b61633bce2cb90ac1d |
| Docs | UNCLEAN (R624-8-F1) | Round 8 subsection, intro, Contents, location paragraph, index row, PR body; gates rc 0; 98 hash rows | R624-8 | b522bb923fa59581478460b61633bce2cb90ac1d |

## Real limits

- Documents only. No bench, hardware, board, controller or instrument was touched.
- Physical calibration was NOT RUN, and printed precision is not calibrated accuracy.
- No manager source bank ran at this head, and none is claimed or inferred. The bench figures rest on the author's published receipts, which I recomputed. They were not re-measured.
- The pinned parser models GitHub's cmark-gfm stage only. GitHub's post-processing, such as emoji, is not modelled (S1).
- The hosted checks at this head were read only at 2026-10-12T20:43:31Z and are not hosted acceptance (`receipts/hosted-checks.txt`):
  - 13 completed successfully, including all four Yosys shards, verilator-lint, docs-check-no-git and full-ci-gate;
  - 10 were in progress: docs-check, publication-census, elaborate, yosys-elaboration, firmware-control-mutants and the five Verilator shards;
  - the physical gPTP job was skipped.
- Receipts were scanned for local absolute paths, which were replaced by `<scratch>` and `<repo>`. None remain.
- The clone was not modified. HEAD, the tree, the index, the modes and the gitlinks are verified in `receipts/clone-integrity.txt`.

## Pending manager duties

- Route R624-8-F1 to the executor and re-review the corrected check and texts at the new head. S1 is optional.
- Rule on the two changed earlier expectations (round 4's link-label control, round 7's comment-in-code control). This review finds them consistent with item 1.
- Validate the current-dev merge candidate (source base `c20c85bd`, live dev `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`) with the builder and native banks, and link the receipts on the PR.
- Own hosted and act acceptance of the exact head; the long hosted gates were still running.
- Keep issue #629 open: Direction B's INTERNAL mismatch control, lane B6's timed ratio for B-CRF and B-AAF, and #645 remain open.
- Publish this report and the files listed in `MANIFEST.sha256`.

R624-8 FINISHED
