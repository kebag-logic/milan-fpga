[R624] NEGATIVE - exact head 295ba9d7f7dfed65e95002478ed6d55ccc14e580

Round R624-7, internal independent review of issue #629 / PR #725 (bench lanes B16, B16b and B16c, docs and
findings only), findings round 7 (documents only). Tree `160ba4535ed6caf63d23994b364b1f054bd95589`; comparison
`c20c85bd..295ba9d7f7dfed65e95002478ed6d55ccc14e580` (ten commits, two Markdown files:
`docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and `docs/findings/README.md`). Evidence: the published
packet at `629-b16-review-evidence` commit `fa974c3f1f9a1ef3a461ebb3b090b1915faaf251`, directories
`author-r1/` to `author-r7/`.

All five lenses were applied. Every round 7 item of the assignment is met, and every earlier finding on this PR
is resolved at this head. One new MINOR remains: R624-7-F1. Markdown image syntax placed between an identifier's
digit and a unit passes the figures check while a reader sees the measurement. This is a new route in the class
that R625-6-F1 belonged to. RTL is CLEAN; Conformance, Robustness, Tests and Docs are UNCLEAN under F1.
No current bench figure is wrong and no DUT defect is alleged: the unchanged page has no image syntax, and its
1,834 rows all equal their receipts.

## Order of work

The verdict and a draft ledger were written after the independent pass and before any prior review finding was
read. The draft listed F1 under Tests, Robustness and Docs. Conformance was added when the final report was
written, on the round 5 assignment's item 2 ("A measurement is never an identifier ... whatever the spacing"):
the rendered text `7ppm` is a digit run directly followed by a unit. The verdict did not change. The prior
findings were then read, and each is resolved or retained below.

## Method

- Context: AGENTS.md, CONTRIBUTING.md sections 4-6, docs/README.md, the issue body, the B16 assignment,
  both rulings, and the round 2 to round 7 assignments; the round 7 handoff (issue comment 6129482994) and the
  live PR body.
- Diff and history: `git diff c20c85bd..295ba9d7` and `git diff e91a62ee..295ba9d7`. Every commit changes only
  the two Markdown files. No HDL, firmware, script, build file or gitlink changed.
- Packet integrity: `MANIFEST.json` at `fa974c3f` lists 4,711 entries. Every `author-r1/` to `author-r7/` file
  equals its `published_sha256`, and the two hashes differ exactly where `path_redacted` is set. In
  `author-r7/`, the 49 files that do not match `MANIFEST.sha256` are exactly the 49 path-redacted entries.
- Executed against the head, offline, on copies only. Commands are in `scripts/` and outputs in `receipts/`:
  - the figures check;
  - the five controls runners;
  - the round 7 runner against round 6's check and page;
  - the ten published review probes, unchanged;
  - the author's self-probes, key scan, evidence receipt and check rebuild;
  - two probes of my own;
  - a rendered comparison of `e91a62ee` against the head;
  - a hash-row verification;
  - nine documentation gates.

  Renderer probes ran under the repository's hash-locked renderer (cmarkgfm 2025.10.22, html5lib 1.1),
  installed from `tools/markdown/requirements.txt` into a disposable environment.

## Finding

### R624-7-F1 - MINOR - Conformance, Robustness, Tests, Docs

**Image syntax hides a phrase mark from the reader, but not from the figures check.**

- **Artifact:**
  - `author-r7/tools/check_b16_figures.py:2475`: `ENDS = ".,;:!?|"`, the closed list's phrase marks;
  - `:2759`: `MARKUP = re.compile(r"<[A-Za-z/!?]")`, which reads only HTML;
  - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3876-3878`: the closed list as stated, with "question or
    exclamation mark" among the marks;
  - `:4012`: round 7's "No markup";
  - `:4036`: "What the rule does not cover";
  - `docs/findings/README.md:15`: round 6 says a unit directly after an identifier makes its digits a
    measurement, and round 7 says "no markup can hide a unit from it";
  - the PR #725 body, Round 6 item 3 and Round 7 item 1.
- **Authority:**
  - the round 5 assignment, item 2: "A measurement is never an identifier. A digit run followed by a unit
    belongs only to a row, whatever the spacing";
  - the round 6 assignment, item 3: "Units are then caught whether or not they are listed";
  - the round 7 assignment: "the class is closed by refusing markup rather than imitating the renderer".
- **Evidence:** `receipts/own-markdown-escapes.json`, from `scripts/probe_r624_7_markdown_escapes.py`. Each
  form is appended to the B16c attribution row at line 3011, where R625-6 placed its forms, and the reader's
  text comes from the pinned renderer:

  | Inserted | Reader sees | Check exit |
  |---|---|---|
  | `CLOCK_DOMAIN 7 ppm.` (control) | `CLOCK_DOMAIN 7 ppm.` | 1 |
  | `CLOCK_DOMAIN 7![](x.png)ppm.` | `CLOCK_DOMAIN 7ppm.` | 0 |
  | `CLOCK_DOMAIN 7![](x.png) ppm.` | `CLOCK_DOMAIN 7 ppm.` | 0 |
  | `Channel 2![](x.png) dB.` | `Channel 2 dB.` | 0 |
  | `Round 7![](x.png) ms.` | `Round 7 ms.` | 0 |
  | `CLOCK_DOMAIN 7![](x.png) furlongs.` | `CLOCK_DOMAIN 7 furlongs.` | 0 |
  | `CLOCK_DOMAIN 7![.](x.png) ppm.`, `CLOCK_DOMAIN 7 ![and](x.png) ppm.`, `CLOCK_DOMAIN 7![](x.png "and") ppm.` | `CLOCK_DOMAIN 7 ppm.` | 0 |

  - Each false pass keeps all 1,834 rows OK and reports the added digit in an identifier, with 0 uncovered and
    0 markup.
  - The renderer emits `<p>CLOCK_DOMAIN 7<img src="x.png" alt="" />ppm.</p>`: the `!` is never shown, yet the
    check reads it as a phrase-ending exclamation mark on the closed list.
  - Neighbouring forms are detected: an empty link with a title, a link label with a title, empty reference
    links, a pointy-bracket destination, a footnote reference and ten invisible format characters
    (`receipts/own-invisible.json`).
  - No earlier probe or control tries this route. R624-6's `image-alt` form puts the digits inside the alt
    text, and it is detected.
  - Round 6's stated limit ("an identifier followed by a full stop, a comma, a colon or a dash ... and then a
    unit, passes") assumes a mark the reader sees. Here the reader sees none.
- **Impact:**
  - A future edit can state an unreceipted measurement after an identifier in visible text, and the check
    passes it.
  - This is the guarantee rounds 5 to 7 were assigned to close by construction. The cause is the same one
    behind R625-6-F1: the check reads a character the reader never sees as a closed-list follower. Here the
    character comes from Markdown inline syntax instead of an HTML comment.
  - It changes executable validation behaviour and an evidence claim, so it is not wording-only RESIDUE.
  - No current figure is affected: the section holds no `![`.
- **Required outcome:**
  - The check refuses Markdown image syntax (`![`) in the text it covers, as it refuses markup, and names the
    line. Alternatively, a closed-list mark must count only where it is visible text, not where it opens an
    image.
  - Add a standing control: `CLOCK_DOMAIN 7![](x.png)ppm.` on the attribution row must fail and name the 7.
    Add it as a control or as a fix to the stated rule; stating the image route as a limit does not meet the
    round 5 and 6 assignments.
  - All earlier controls, the ten review probes and the unchanged page must stay as they are now.
  - The page, the index row and the PR body must state the rule as it then is.
- **Verification:** run `scripts/probe_r624_7_markdown_escapes.py`, unchanged, under the pinned renderer
  interpreter. It must report `escapes: false` for every form. At this head it reports true for the eight
  image forms. Then re-run the controls runners and the review probes.

## Round 7 assignment, item by item

| Item | Result | Evidence |
|---|---|---|
| 1. Refuse, by line, any HTML comment or raw HTML tag, except exact generator markers byte for byte; comment normaliser removed; whitespace still collapses | Met for HTML | `:2759-2769` refuses `<` followed by a letter, `/`, `!` or `?` on any covered line, code included. The only exception is the four `GENERATED` markers of `scripts/check_solution_docs.py`, compared as whole lines. `normalise` (`:2638-2692`) has no comment branch. The unchanged page reports `"markup": 0`. Markdown image syntax is not HTML, so the ruling's letter is met: see F1 |
| 1. Replace the section's markup with plain Markdown | Met | The 11 marker lines are now blank and the code-block placeholders are in braces. The render comparison over every block before the round 7 subsection shows 8,853 blocks on each side; the only differences are the 7 intended text edits (`receipts/render-compare-e91a-vs-head.json`) |
| 2. R625-6's six probes end refused at their line | Met | `probe_rendered_comment.py`, unchanged, gives statuses `[0, 1, 1, 1, 1, 1]`. Each comment form names `MARKUP` and `UNCOVERED 7` at line 3011. The probe exits 1 only from its own final assertion, which records round 6's statuses, as R625-6 stated |
| 2. A raw tag splitting a number from its unit is refused | Met | The control "a raw tag between a number and its unit" (`7<span></span>ppm`) passes, and against round 6's check it fails (`receipts/controls/r7-controls-at-head.json`, `r7-controls-on-r6-check.json`) |
| 2. Earlier probes, controls and the unchanged page stay green | Met | Runners for rounds 3 to 7: 5/5, 8/8, 22/22, 39/39 and 50/50 PASS. Round 7's runner on round 6's check and page: 40 PASS, and the 10 refusal controls FAIL. All ten probes reproduce the author's published results (identical result files). Each copied probe is byte-equal to its original under `reviews/` (`receipts/review-probes-vs-published.txt`). The check exits 0 on the page: 1,834/1,834 rows, 14,531 digits, 0 uncovered, 0 markup. Rows and coverage are byte-equal to `author-r7/r7/`, and the check rebuilds byte for byte from its spec |
| 3. Optional R624-6-S1 and S2 | Taken | `:4036` onward states the approximate-quantity and list-marker limits. The self-probes run 111 forms: 92 detected and 19 stated passes, reproduced. PR body Round 7 item 3 closes the open question. My rerun of R624-6's escape probe gives every exit status recorded at `e91a62ee` |
| 4. Texts; "Where the packet is" maps round 6 | Met | `:2608-2616` maps `author-r6/` to `e91a62ee`, published by `b616e7ea`, and names `author-r7/`. `fa974c3f` is the round 7 publication. `r7_evidence_receipt.py`, re-run, is byte-equal to the published receipt: 3,800 entries; 84 of 84 rows equal; 646 of 647 files. All 93 hash rows of the section at the head equal their `author-r7/` files (`receipts/hash-rows-vs-author-r7.json`) |

## Independent results by lens

[R624] PASS RTL - `git diff --stat c20c85bd..295ba9d7` (two Markdown files; gitlinks unchanged, `receipts/clone-integrity.txt`), `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:402-410`, `docs/reference/REGISTER_MAP.md:2139` (0x8F8) and `:1870-1871` (0x8D4/0x8D8), `author-r7/tools/r2_poll_b16c.py:48-60`, `author-r7/r2/{bcrf,baaf}-poll-trace.tsv` - no RTL, firmware or interface change. The poll decode matches the RTL encoding: state `[2:0]` with 3 ACQUIRE and 4 LOCKED, bit 4 DRP config mismatch, trim `[31:16]`/16, and the SLIP dups `[15:0]`. Recomputed from the raw words: 596 of 596 window polls LOCKED in each case (words `0x..34`/`0x..74`), and the brackets 2.585-3.161 s and 6.602-7.180 s, from polls 44/45 and 52/53.

Conformance (examined; unclean only under F1):

- B16: `summary/loop2/acmp-peer-tap.json` holds CONNECT_TX_COMMAND (Milan's PROBE_TX) at +99.6 ms and +299.6 ms,
  with no response. The page's 49.6 s is the tap's end less the second probe.
- B16b: `summary/b0-2/c-b9-grade.json` recomputes, block by block, 169 floor blocks with medians -123.98/-123.95
  dB, all-block medians -123.95/-122.80 dB and 131 degraded. `r2/b0-2-receipt.json` gives 23 degraded inside
  the 34.1136 s overlap and 108 beyond, stated as inference.
- B16c: `summary/{bcrf,baaf}/c-b9-grade.json` have 300 of 300 blocks at the floor, medians -123.98/-123.97 dB
  and 0 events.
- Clock sources: `runs/{bcrf,baaf}/events.jsonl` show every SET_CLOCK_SOURCE read back: peer 0, DUT 1 or 2, DUT
  restored to 0, then the peer restored to 1 after the DUT's unbinds.
- Bindings: `restore/census-startc.jsonl` and `census-endc.jsonl` show the peer's STREAM_INPUT 0 and 8 bound to
  the DUT's talkers 0 and 1, the DUT's inputs unbound, the DUT's clock source 0 and the peer's 1. Each census
  comparison is 45 of 46 equal; the one difference is the DUT's propagation delay.
- Attribution: the tone source's route and clock changes are attributed outside the lane. The INTERNAL mismatch
  control is stated NOT RUN at `:3321`, in the paragraph after that table, at `:3344-3345`, in the index row and
  in the PR body.
- Privacy: no host path, address or equipment name appears in the added lines or the PR body.

Robustness (examined; unclean only under F1):

- Failure and reset paths of the record: the B16 and B16b STOPs, the restore residuals, the dry-run controls
  `controls/b16c-dryrun-*.json`, and the playback underrun record.
- The check under adversarial input: the ten review probes, 111 self-probes, 50 controls, my 17 Markdown forms
  and 10 invisible format characters. All behave as stated except F1's eight image forms.

Tests (examined; unclean only under F1):

- Each round 7 control can fail for its defect: 10 of the 11 fail on round 6's check, and the exact-marker
  control passes on both, as designed.
- The key scan finds 0 unread loop variables over 565 loops, byte-equal.
- The check reproduces its outputs byte-equal.
- F1 is a false pass of the check itself.

Docs (examined; unclean only under F1):

- The round 7 subsection, introduction, Contents line, `:2312` pointer, `:2608-2616` location paragraph, index
  row and PR body describe the round accurately. The PR body equals `author-r7/PR-BODY.md` but for one
  trailing blank line.
- The documentation gates pass: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and
  `--verify-anchors`, and `check_em_dash.py` from both `c20c85bd` and the merge base, which is also
  `c20c85bd`. So do `check_doc_paths.py` and `git diff --check` over the worktree and the range; all rc 0 in
  `receipts/gates/`.
- The stated rule overclaims for F1's route.

## Prior public findings at this head

| Finding | Lenses | Status at 295ba9d7 | Evidence |
|---|---|---|---|
| R624-1-F1 = R625-1-F3 (B0 figures) | Conformance, Tests, Docs | RESOLVED | Floor medians -123.98/-123.95 dB over 169 blocks; runs 43-44 and 46-54; recording at 06:38:05.2, 26.0 s after the binds (`r2/b0-2-receipt.json`); check rows OK |
| R624-1-F2 = R625-1-F4 (lane B6's four terms) | Conformance, Tests, Docs | RESOLVED | The terms table states three met and the timed ratio NOT RUN, with no decision replacing it; the same in the acceptance, limits, index and body |
| R625-1-F1 (attribution, shown against inference) | Conformance, Tests, Docs | RESOLVED | 131 at (c), 23 shown inside the overlap, 108 by inference, in the page, index and body |
| R625-1-F2 = R624-1-S2 (reduced receipts) | Tests, Docs | RESOLVED | `r2/` receipts are bound to raw hashes, with the extraction commands; traces re-decoded above |
| R624-1-R1, R624-1-R2 / R625-1-R1, R2 (title, counter mark) | Docs | RESOLVED | The live title is as requested; the first mark is 20 s after the set, about 6 s before the window |
| R624-1-S1, R625-1-S1, R624-2-S2, R625-2-S1, R625-3-S1 (census wording) | Docs | TAKEN | "44 of 45 reads equal, the census's start record aside"; census files 45/46 |
| R624-2-F1 (positive-control floor counts) | Robustness, Tests, Docs | RESOLVED | 303 of 303 and 11 of 13, with blocks 0-2 stated; check rows OK |
| R624-2-F2 (LOCKED bracket) | Tests, Docs | RESOLVED | Recomputed from the traces above |
| R624-2-R1, R2, R3 | Docs | RESOLVED | Narrowed source statements (1,255; 618 and 668); qualified pre-set slips; the body names the INTERNAL mismatch control |
| R624-2-S1 (servo bit 4) | Docs | TAKEN | `:3341-3342`; bit 4 set in every ACQUIRE/LOCKED word |
| R625-2-F1 (exact replacement at (a)) | Conformance, Tests, Docs | RESOLVED | Verbatim at `:3244`; check rows OK |
| R624-3-F1 (where the packet is) | Docs | RESOLVED | `:2608-2616` through `author-r7/`; evidence receipt byte-equal |
| R625-3-F1 (quoted and linked figures) | Conformance, Robustness, Tests, Docs | RESOLVED | The probe detects 7 of 7 at the head |
| R624-4-F1, R625-4-F1 (glued units, spellings, spacing, continuation) | Conformance, Robustness, Tests, Docs | RESOLVED | Probes detect 8 of 8 and 12 of 12 at the head |
| R624-4-S1 | Docs | TAKEN | `:2289-2312` points to every round |
| R624-5-F1 (line-3200 row per case) | Tests, Conformance | RESOLVED | `probe_row3200.py`: LOCKED row MISMATCH (`bcrf 595, baaf 596`); R624-6's poll probe turns the poll-count row MISMATCH |
| R624-5-F2 (spelled-out units) | Conformance, Robustness, Tests, Docs | RESOLVED | `probe_r624_5_escapes.py`: 21 of 25 detected, the four undetected being the stated `id+ colon` limit and three digitless `word:` forms; r6 controls PASS |
| R624-5-F3 (round 5 packet location) | Docs | RESOLVED | `:2616` |
| R624-5-R1 (identifier categories as stated) | Docs | RESOLVED | The exact fix is at `:3765` and `:3770`, and in the PR body Round 5 item 1 |
| R624-5-S1 | Tests | TAKEN | Limits stated at `:3915-3926` and `:4036` onward |
| R625-5-F1 (comment over a line break) | Conformance, Robustness, Tests, Docs | RESOLVED | `probe_comment_separator.py`: `[0, 1, 1]`; now refused as MARKUP |
| R625-6-F1 (short comment forms) | Conformance, Robustness, Tests, Docs | RESOLVED | `[0, 1, 1, 1, 1, 1]`; MARKUP and UNCOVERED 7 at line 3011; standing controls in r7 |
| R624-6-S1, S2 | Tests, Robustness; Docs | TAKEN | See item 3 above |

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R624-7-F1) | Findings `:2287-4115`, index `:15`, PR body; `author-r7` runs, summaries, `r2/`, `restore/`; round 5-7 assignments | R624-7 | 295ba9d7f7dfed65e95002478ed6d55ccc14e580 |
| RTL | CLEAN | The full diff; `KL_mmcm_drp_servo.sv:402-410`; `REGISTER_MAP.md:1870-1871`, `:2139`; poll traces and decoder | R624-7 | 295ba9d7f7dfed65e95002478ed6d55ccc14e580 |
| Robustness | UNCLEAN (R624-7-F1) | Restore and STOP records; dry-run controls; the check under 10 review probes, 111 self-probes, 50 controls, 27 own forms | R624-7 | 295ba9d7f7dfed65e95002478ed6d55ccc14e580 |
| Tests | UNCLEAN (R624-7-F1) | `check_b16_figures.py` (`6b2570b8...`), controls r3-r7, r7-on-r6, key scan, rebuild, probe reruns | R624-7 | 295ba9d7f7dfed65e95002478ed6d55ccc14e580 |
| Docs | UNCLEAN (R624-7-F1) | Round 7 subsection, location paragraph, intro, Contents, index row, PR body; 9 gates rc 0; 93 hash rows | R624-7 | 295ba9d7f7dfed65e95002478ed6d55ccc14e580 |

## Real limits

- Documents only. No bench, hardware, board, controller or instrument was touched. Physical calibration was NOT
  RUN, and printed precision is not calibrated accuracy.
- No manager source bank ran at this head, and none is claimed or inferred. The bench figures rest on the
  author's published receipts, and I recomputed key figures from them, not from hardware.
- The pinned renderer reproduces GitHub's `gfm` rendering. A broken image on GitHub may show a broken-image
  glyph between the digit and the unit. The digit and the unit remain visible text either way.
- Hosted checks at this head, read only: docs-check, docs-check-no-git, full-ci-gate, bdd-conformance,
  publication-census, wire-accountability and Yosys shards 1-3 succeeded. The Verilator shards, Yosys shard 0,
  yosys-elaboration, elaborate, verilator-lint and the firmware jobs were queued or in progress. The physical
  gPTP job was skipped (`receipts/hosted-checks.txt`). This is not hosted acceptance.
- One receipt (`receipts/probes/r625-6-rendered.stdout`) had local absolute paths replaced by `<packet>`,
  `<repo>` and `<author-r7 copy>`. Probe result JSON files were scanned the same way; none held a path.

## Pending manager duties

- Route R624-7-F1 to the executor. Re-review the corrected check and texts at the new head.
- Validate the current-dev merge candidate (source base `c20c85bd`, live dev `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`)
  with the builder and native banks, and link the receipts on the PR.
- Own hosted and act acceptance of the exact head; the long hosted gates are still running.
- Keep issue #629 open: Direction B's INTERNAL mismatch control, lane B6's timed ratio for B-CRF and B-AAF, and
  #645 remain open.
- Publish this report and the files listed in `MANIFEST.sha256`.

R624-7 FINISHED
