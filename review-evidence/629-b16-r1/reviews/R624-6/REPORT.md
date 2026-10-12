[R624] POSITIVE - exact head e91a62ee266e182a804ca1f45a0f18f715096563

Round R624-6. Internal independent review, cleared context, of issue #629 / PR #725 (bench lanes B16, B16b and B16c; documents and findings only). Head `e91a62ee266e182a804ca1f45a0f18f715096563`, tree `f35f3e423e4b6a744b44f124a9281fb0f413d0e7`, source base `c20c85bd`. Round 6 assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6126774639.

**Verdict.** No BLOCKER, MAJOR, MINOR or RESIDUE is open at this head. All five lenses were applied and each is CLEAN, with the evidence named below. Every prior public finding on this PR is resolved at this head, including all of round 5's (R624-5-F1, F2, F3, R1 and R625-5-F1). Two optional SUGGESTIONs are recorded; they affect no figure, verdict or lens.

- The figures check passes at the head. I re-ran it and its outputs are byte-equal to the published ones: 1,790 rows, all OK; 13,849 digits, 0 uncovered.
- Separately, I recomputed the section's headline figures myself, straight from the published receipts and without the check. All of them equal the page.
- I re-ran every earlier control suite, and the six published review probes unchanged. Each gives the result the page and the author's receipts state.
- My own 37 escape probes found no measurement in natural spelling that passes. The forms that do pass all lie inside the ruling's closed list (S1).

I made no source change, commit, push or GitHub write. I ran nothing on the bench and used no sub-agent, Docker or act. Every probe ran on copies inside this packet's scratch directory. The clone is byte-exact at the head (see the end of this report).

## Context reconstructed

I read, in this order:

1. AGENTS.md (sections 3 to 8), CONTRIBUTING.md section 6 (documentation wording and privacy), and docs/README.md.
2. The #629 issue body: the proof and acceptance items, including the bench quality metric with its two controls.
3. The lane B16 assignment (6117305187) and the two rulings:
   - 6117672835: B16b, the four-point capture;
   - 6118365090: B16c. The maintainer's exception lets the peer be set to INTERNAL for B-CRF and B-AAF only, read back, and restored to its CRF input with a read-back.
4. The executor's TAKEN, STOP and REVIEW READY comments.
5. The round 2 to 6 assignments (6119316763, 6119906508, 6121193402, 6125608002, 6126774639).
6. The linked authorities:
   - `docs/reference/REGISTER_MAP.md`, at 0x738 `CRF_RATE`, 0x8D4 `SLIP_LB`/`SLIP_TDM`, 0x8E0 `AAFM_STAT`/`AAFM_RATE` and 0x8F8 `MCSRV_STAT`;
   - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1670-1678`, the B AAF, B CRF, Switch and Lock loss bench rows.
7. The diff `c20c85bd..e91a62ee` (two Markdown files, 1,729 insertions, 1 deletion) and the nine one-line commits.
8. The published evidence:
   - branch `629-b16-review-evidence` at `b616e7ea`, the directories `author-r1/` to `author-r6/` and `MANIFEST.json`;
   - the live PR body.

Only after my independent result was recorded (`receipts/independent-pass-note.txt`) did I read the prior review findings, R624-1 to R624-5 and R625-1 to R625-5, and their published probes.

## What I ran (receipts in this packet)

| Check | Result | Receipt |
|---|---|---|
| Packet integrity: every file of `author-r1/` to `author-r6/` against `MANIFEST.json` at `b616e7ea` | All published hashes equal. In `author-r6/`, 647 files: 41 are path-redacted (gate logs, gate results and `tools/gates_r2.py`). Its `MANIFEST.sha256` equals the manifest's `original_sha256` for all 646 other files | Done by command; summary here |
| Evidence commits named on the page | `b84584e4`: `MANIFEST.json` SHA-256 `8d417d54...`, 1,680 entries, 27 author files path-redacted (1, 9 and 17). `b83e5d76` holds `author-r4/`, and `a73ce5c4` holds `author-r5/` (3,044 entries). `b616e7ea` holds `author-r6/` | `receipts/independent-pass-note.txt` |
| `check_b16_figures.py` at the head, unchanged (`62bce479...`) | rc 0. 1,790 rows OK. 13,849 digits: 11,445 claimed by rows, 2,404 in 1,186 identifiers, 0 uncovered. Rows and coverage output are byte-equal to `r6/figures-rows.tsv` and `r6/figures-coverage.tsv` | `receipts/check/` |
| Row keys, parsed without running the check | 0 keys are literals, and 0 use only builtins on constants: every row reads a receipt. The 34 rows whose receipt is the findings page read text outside lane B16's section (another lane's section), or the page at an earlier commit. None reads its own figure | `audit_row_keys.py`, `audit_self_receipts.py`, `receipts/check/row-keys.json`, `receipts/self-receipt-rows.json` |
| My own recomputation of the headline figures, straight from the receipts | 0 mismatches. Checked: the B16c lock brackets (polls 44/45 and 52/53); 596 of 596 window polls LOCKED; 580/16 and 584/12 busy polls; trim -6.000 to -6.125 ppm; the CRF and AAF rates; `AAFM_STAT` `0x001e0007`; `SLIP_LB` 162 to 188 with every step bracketed. Also every B0, B-CRF and B-AAF grade cell; B0's 131/23/108 split, thirteen runs beyond, and worst blocks 7 and 224; every alignment and its total (3,077,452/3,077,980 and 3,289,015/3,290,863); the (d) decodes; all eight clock-source sets with their read-backs and the final state equal to as found | `indep_figures.py`, `receipts/indep-figures.json` |
| The loopback's ACMP record (`summary/loop2/acmp-peer-tap.json`) | CONNECT_RX response SUCCESS with connection count 1 at 99.6 ms. CONNECT_TX (PROBE_TX) commands at 99.6 ms and 299.6 ms, with 0 responses. Only the DUT's AAF and CRF streams are on the peer's link | `acmp_loop2_check.py`, `receipts/acmp-loop2.json` |
| Every hash row on the page from line 2287 on, and in the live PR body | Page: 84 packet rows equal size, SHA-256 and `original_sha256`; 40 raw rows are listed in `RAW-ARTIFACTS.json`. PR body: 37 rows equal. Its other 3 are rounds 3, 4 and 5's checks, and each equals its file in `author-r3/`, `author-r4/` and `author-r5/` | `check_hash_rows.py`, `receipts/hash-rows-*.txt` |
| Round 6's rewording, line by line against `36190193` | 126 lines changed before the new subsection, and no line moved. 0 verdict words changed. The digit and link changes are only the new round 6 pointers, the round 5 note, the round 4/5 packet mapping, reordered phrases (`#629`, `#645`, CRC32), and "Lane B15" becoming "That lane" | `audit_r6_rewording.py`, `receipts/r6-rewording-audit.json` |
| Identifiers that cover digits | Each of the 1,186, listed with the text that follows it. None stands for a measurement | `audit_identifiers.py`, `receipts/identifier-followers.tsv` |
| Control runners at the head, each unchanged | Round 6's: 39 of 39. Round 5's: 22 of 22. Round 4's: 8 of 8. Round 3's: 5 of 5. Each output is byte-equal to its published `controls/r6-*.json` | `receipts/controls/` |
| Round 6's runner against round 5's check (`2641412c...`) and the page at `36190193`, in an exported tree | Round 5's check passes its own page (rc 0). The 22 earlier controls PASS, and the 17 new ones FAIL. Output is byte-equal to `controls/r6-controls-on-r5-check.json` | `receipts/controls/r6-runner-on-r5-check.json` |
| The six published review probes, unchanged. Each script's SHA-256 equals the author's copy in `tools/review-probes/` | R624-5 `probe_row3200.py`: `row3200_insensitive` false, and the LOCKED row is MISMATCH `bcrf 595, baaf 596`. R624-5 `probe_r624_5_escapes.py`: 18 of 19 `id+` forms detected, the colon form excepted, and every ruling unit in words detected. R625-5 `probe_comment_separator.py`: [0, 1, 1]. R624-4: 8 of 8. R625-4: 12 of 12. R625-3: 7 of 7 | `receipts/review-probes/` |
| My mutation of line 3200's second row: B-CRF's window poll count set to 595 in a copy of its receipt | Line 3174's poll-count row and line 3200's second row turn MISMATCH (`bcrf 595, baaf 596`). Each line-3200 row reads each case's own receipt | `probe_row3200_polls.py`, `receipts/row3200-polls-probe.json` |
| My own escape probes, 37 forms, on page copies | Detected, as required: a `<br>` or `<sup>` tag; a decimal or hex entity digit; a word joiner, BOM, narrow or ideographic space; fullwidth units; Arabic-Indic and mathematical digits; a range into a unit word; a glued lane name; an issue number or uncited issue; a step index before ms; a `McASP7`; fenced code; an HTML block; image alt text; a heading; a blockquote; a title attribute; a link-reference title; "a hundred ppm". Passing, all inside the ruling's closed list (S1): an identifier before "of"/"and" plus a bare unit, a possessive, "or so"/"or more"/"and a half"/"to some" plus a unit, a colon or a full stop, and a two-cell table. A single-item list `7. ppm`, which renders as list marker 7, also passes | `probe_r624_6_escapes.py`, `receipts/own-escape-probes.json` |
| Documentation gates at the head | All rc 0 in the pinned Markdown environment (cmarkgfm 2025.10.22, html5lib 1.1): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors` (479 cross-page fragments), and `check_doc_paths.py`. `check_em_dash.py --base c20c85bd` gives 0 findings over 1,729 added lines; `--base e8454e27` gives 0 findings over 3,722. Also rc 0: `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test`, and `git diff --check c20c85bd HEAD` | `receipts/gates/` |
| Privacy scan of the added lines and the live PR body | No host path, IP, MAC or host name. No vendor or product name for the reference peer, the external capture or the tone source. The only serial is the DUT's own | Done by command; no hits |
| Hosted contexts at the exact head | Executed and successful: `rtl-fast`, `changes`, `elaborate`, `full-ci-gate`, `wire-accountability`, `bdd-conformance` and `docs-check-no-git`. `docs-check` was still in progress when read. Skipped by docs-only scheduling: the Verilator and Yosys contexts and shards, `firmware-unit`, `publication-census` and physical gPTP. Skips are not executions | `receipts/hosted-check-runs.tsv` |

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

### R624-6-S1 SUGGESTION (Tests, Robustness): the closed list's word followers still let an identifier carry an approximate quantity

- **Where:**
  - the follower rule in `author-r6/tools/check_b16_figures.py`;
  - the page's statement of it, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3880-3881`, and its limits, `:3915-3926`.
- **Evidence:** on the attribution row, the check exits 0 for each of these (`receipts/own-escape-probes.json`):
  - `CLOCK_DOMAIN 7 or so ppm`, `CLOCK_DOMAIN 7 or more ppm`, `CLOCK_DOMAIN 7 and a half ppm`, `CLOCK_DOMAIN 7 to some ppm`, `channel 1 or so dB`;
  - `CLOCK_DOMAIN 7 of ppm`, `CLOCK_DOMAIN 7 and ppm`, `CLOCK_DOMAIN 7's ppm`.

  The word after the identifier is "and", "or", "to" or "of", or a possessive. Each is on the round 6 ruling's closed list, and what follows that word holds no number, so the check does not treat it as a measurement.
- **Why not a finding:**
  - The ruling names "and", "to", "of" and "or" as permitted followers, and the check implements the list as ruled.
  - The page holds no such text, and every figure on it is verified above.
  - The forms need an identifier keyword directly before the quantity.
  - R624-5 classified forms outside the ruling's terms the same way (R624-5-S1).
- **Optional improvement:** refuse a follower word when a unit word appears before the next phrase end. Or add "an approximate quantity after and, or, to or of" to "What the rule does not cover".

### R624-6-S2 SUGGESTION (Docs): the "both rows MISMATCH" open question can be closed as answered

- **Where:** the open question at the end of the round 6 REVIEW READY and the PR body.
- **Evidence:**
  - `probe_row3200.py` changes only B-CRF's LOCKED count. It turns line 3200's LOCKED row MISMATCH.
  - The second row there is the window's poll count. It is right to stay OK under that mutation.
  - My mutation of the poll count alone turns that second row MISMATCH, naming each case (`receipts/row3200-polls-probe.json`).
  - R624-5-F1's own verification reads "Both line-3200 rows must turn MISMATCH, or the check must otherwise fail at line 3200". It is met.
- **Optional improvement:** the manager records the question as answered.

## Lens results

[R624] PASS Conformance - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2287-3990`, `docs/findings/README.md:15`, `runs/bcrf|baaf/events.jsonl`, `summary/loop2/acmp-peer-tap.json`, `restore/census-compare*.txt`, `summary/*/c-b9-grade.json`, `summary/*/align-*.json` - checked against #629's acceptance, the B16 assignment and both rulings, and the round 2 to 6 assignments:
- **B16:** the loopback did not form. The two PROBE_TX commands are unanswered, the talker sent 0 PDUs, and the output read exact zero. The lane stopped at step 2.
- **B16b:**
  - The four points are present and (c) is sample-exact to (a) and (b).
  - B0 is -123.95/-122.80 dB, with floor medians -123.98/-123.95 dB.
  - The runs are 0-18, 28-31, 43-44 and 46-54. The recording starts at 06:38:05.2, 26 s after the binds.
  - 23 degraded blocks are shown inside the taps' overlap, and the other 108 are labelled inference.
- **B16c:** B-CRF and B-AAF are LOCKED at 596/596, with brackets 2.585-3.161 s and 6.602-7.180 s. THD+N is -123.98/-123.97 dB. Attribution at every stage.
- **Clock sources:** the peer was set to 0 and read back 0, then restored to 1 and read back 1 after the DUT's unbinds. The DUT was set to 1 or 2 and back to 0, each read back. The DUT's clock source is set only as the listener.
- **Restore:** census 45 of 46 entries equal at every lane boundary (44 of 45 reads, the start record aside); only the DUT's propagation delay differs. The census covers both entities' clock, bindings, formats and maps.
- **Lane B6's four terms:** stated, with the timed ratio NOT RUN.
- **Outside the lane:** the source's route and clock changes are attributed outside it, not to the DUT.
- **INTERNAL mismatch control:** stated as NOT RUN (`:3321`, `:3344-3345`, the index row and the PR body).
- **Round 6 items 1 to 5:** met. Item 1's "both rows" is addressed under S2.

[R624] PASS RTL - `git diff --stat c20c85bd..e91a62ee` (two Markdown files; no HDL, firmware, script, build file or gitlink change), `docs/reference/REGISTER_MAP.md` 0x8F8, 0x8E0, 0x8D4 and 0x738, `docs/design/MEDIA_CLOCK_FOLLOWING.md:1670-1678`, `r2/bcrf-poll-trace.tsv`, `r2/baaf-poll-trace.tsv` - checked the page's register and interface claims against the authorities:
- `MCSRV_STAT[2:0]`: 3 is ACQUIRE and 4 is LOCKED. Bit 4 is the DRP mismatch and bit 6 the fine-PS busy flag (`0x...0034`/`0x...0074`). The trim is signed, in 1/16 ppm.
- `CRF_RATE` is 512 units per ppm, and `AAFM_RATE` uses the same units.
- `AAFM_STAT` `0x001e0007` decodes as locked, rate valid, enabled, listener 0, 0 restarts and 30 ns.
- The six B AAF bench-row terms, and one MEDIA_RESET per switch per Milan v1.2 Table 5.4, agree with the run marks.
- No module or interface contract changes.

[R624] PASS Robustness - `author-r6/tools/check_b16_figures.py` (normalisation, closed list, `MEASURE`), `controls/r6-controls.json`, `receipts/own-escape-probes.json`, `runs/b0/events.jsonl`, `controls/b16c-dryrun-summary.json`, `controls/b16c-wrapper-deadline.txt` - checked:
- **Malformed and adversarial page input**, 37 escape forms of my own plus the six review probes. Every natural measurement spelling fails the check, named at its source line. The comment, entity, tag, invisible-character, Unicode-digit and code forms are caught. Multi-line forms keep their source line numbers (3993/3994 for appended blocks).
- **The incident run** (`b0`, McASP busy) is excluded from grading, and its restore was read back.
- **The dry-run and deadline paths** are published.

S1 records the residual approximate-quantity forms that the ruling admits.

[R624] PASS Tests - `author-r6/tools/check_b16_figures.py` (`62bce479...`), `tools/r3_check_controls.py` to `tools/r6_check_controls.py`, `controls/r6-controls-on-r5-check.json`, `tools/review-probes/*.py`, `r6/*-probe-rerun.json` - checked:
- **Output:** the check's output reproduces byte for byte.
- **Row keys:** every key reads a receipt. No key ignores its loop variable, and no page-receipt row reads its own figure.
- **The line-3200 rows:** each reads each case's own receipt, and each fails under a mutation of its own figure (R624-5's probe and mine).
- **Controls:** 39/22/8/5 PASS at the head. On round 5's check the 17 new controls FAIL, so each can fail for its defect.
- **Review probes:** all six run unchanged with the stated results.
- **Independent recomputation:** my figures from the receipts agree with every checked row.

[R624] PASS Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:18-39`, `:84`, `:2287-3990`, `docs/findings/README.md:15`, the live PR #725 title and body, `review-evidence/629-b16-r1/MANIFEST.json` at `b84584e4`, `b83e5d76`, `a73ce5c4` and `b616e7ea`, `receipts/gates/` - checked:
- **"Where the packet is"** (`:2608-2633`) names the branch and pinned commit, and the directories `author-r1/` to `author-r5/` with their commits. It names `author-r6/`, now published at `b616e7ea`, and the manifest's binding and redaction counts.
- **Hash rows:** 84 packet rows and 40 raw rows on the page equal their files, and the PR body's rows equal theirs.
- **R624-5-R1** is applied verbatim at `:3764-3765` and `:3770`, and in the PR body's round 5 item 1.
- **Round 6's rule and its limits** are stated on the page, and the follower words are named in the check and on the page.
- **Gates:** all pass.
- **Privacy:** no host path, and the peer, the capture and the tone source are named by role only.
- **Commits:** one line each, with no trailers.

## Prior public findings at this head (read after my own pass)

| Finding | Disposition at `e91a62ee` |
|---|---|
| R624-5-F1, the line-3200 row reads only B-AAF's count | Resolved. `each()` reads each case's own receipt, and the receipt column names both files. `probe_row3200.py`, unchanged, turns the LOCKED row MISMATCH (`bcrf 595, baaf 596`). My poll-count mutation turns the second row MISMATCH. The verification's "or the check must otherwise fail at line 3200" is met (S2) |
| R624-5-F2, spelled-out units after an identifier | Resolved. The closed follower list refuses any word after an identifier, and `MEASURE` reads the ruling's unit names. `probe_r624_5_escapes.py`, unchanged, detects every ruling unit in words, `B16 milliseconds` and `IEEE 1722.1 milliseconds`. Controls stand for each, and for `furlongs`. The colon form remains a stated limit (`:3918-3920`); it was R624-5-S1, not part of F2 |
| R624-5-F3, round 5's packet location | Resolved. `:2614-2616` maps round 4 to `author-r4/` (`61ae8641`, `b83e5d76`) and round 5 to `author-r5/` (`36190193`, `a73ce5c4`), and names round 6's `author-r6/`. I verified each commit's tree and manifest |
| R624-5-R1, the identifier categories | Applied verbatim on the page and in the PR body |
| R624-5-S1, the limits | Taken: "What the rule does not cover", `:3915-3926` |
| R625-5-F1, a multi-line HTML comment | Resolved. Comments are dropped before matching. `probe_comment_separator.py`, unchanged, gives [0, 1, 1] with exit 0. The standing control is in `controls/r6-controls.json` |
| R624-4-F1, R625-4-F1, R625-3-F1 (the coverage class) | Still resolved. Unchanged probes detect 8 of 8, 12 of 12 and 7 of 7 |
| R624-3-F1, where the packet is | Still resolved, and extended to rounds 4 to 6 |
| R624-2-F1, F2, R1, R2, R3, S1, and R625-2-F1 | Still resolved. The positive control's 303/303 and 11/13; the LOCKED brackets from the poll's start; the source-state claims narrowed to the common entries; the `SLIP_LB` attribution bounded; the body's antecedent named; bit 4 in the limits; the exact replacement verbatim at `:3244` |
| R624-1-F1 = R625-1-F3, R624-1-F2 = R625-1-F4, R625-1-F1, R625-1-F2 (R624-1-S2), R1 and R2, and the census suggestions | Still resolved: the B0 figures, lane B6's four terms, inside-against-beyond attribution, the reduced receipts, the PR title, the counter mark, and "44 of 45 reads" |

No prior finding is retained. No RESIDUE is open.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #629 acceptance; the B16 assignment, both rulings and the round 2 to 6 assignments; `629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2287-3990`; `README.md:15`; `runs/bcrf|baaf/events.jsonl`; `summary/loop2/acmp-peer-tap.json`; `restore/census-*`; grades and alignments | R624-6 | `e91a62ee266e182a804ca1f45a0f18f715096563` |
| RTL | CLEAN | Diff stat (docs only, gitlinks unchanged); `REGISTER_MAP.md` 0x738, 0x8D4, 0x8E0 and 0x8F8; `MEDIA_CLOCK_FOLLOWING.md:1670-1678`; both poll traces | R624-6 | `e91a62ee266e182a804ca1f45a0f18f715096563` |
| Robustness | CLEAN | The check's normalisation, closed list and `MEASURE`; 37 escape forms of my own; six review probes; the incident and dry-run receipts | R624-6 | `e91a62ee266e182a804ca1f45a0f18f715096563` |
| Tests | CLEAN | `check_b16_figures.py` and its 1,790 row keys; four control runners at the head and on round 5's check; six unchanged review probes; two mutation probes; independent recomputation | R624-6 | `e91a62ee266e182a804ca1f45a0f18f715096563` |
| Docs | CLEAN | The page's introduction, Contents, lane B16 section and round subsections; the index row; the PR title and body; the hash rows; the evidence-branch manifests; gates; privacy | R624-6 | `e91a62ee266e182a804ca1f45a0f18f715096563` |

## Real limits

- Documents only. I re-ran no bench measurement.
  - The raw captures, polls and tone-source reads are private. My recomputation starts from the published reductions: per-block grades, alignments, poll traces, run events and census files.
  - These are bound to the raw hashes through the packet's own records. I did not read the raw files.
- I sampled row semantics by recomputing the headline figures independently. Every row key was audited statically for a receipt read. I did not read all 1,790 keys by hand.
- The escape space is open-ended. My 37 forms, and the six review probes, are what was tried.
- The hosted `docs-check` context had not finished when I read it. The skipped hosted contexts are skips, not executions.
- I ran no Verilator, Yosys or builder bank: the diff holds no RTL. No manager source bank ran at this head, and none is claimed or inferred.
- Physical calibration was NOT RUN. Printed precision is not calibrated accuracy. Field skips are not hardware proof.

## Pending manager duties

- Publish this report and the files listed in `MANIFEST.sha256`.
- Record the S2 open question as answered, if the manager agrees.
- Own hosted and act acceptance at the exact head, including the in-progress `docs-check`.
- At the merge turn, build and validate the current-dev merge candidate (source base `c20c85bd`, live dev `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`) with the builder and native banks, and link those receipts.
- Obtain the second independent positive review and the external review.
- Obtain maintainer merge authorization, then post-merge containment.
- #629 stays open after this PR. Still open: Direction B's INTERNAL mismatch control, lane B6's timed ratio for B-CRF and B-AAF, and #645.

## Clone integrity after the probes

The clone was never written; every probe ran on copies.

- HEAD is `e91a62ee266e182a804ca1f45a0f18f715096563`, and `git write-tree` returns `f35f3e423e4b6a744b44f124a9281fb0f413d0e7`.
- The worktree and index are clean, and the index equals HEAD.
- The gitlinks equal HEAD's and `c20c85bd`'s: `external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `2ad2f845`, `third_party/lwSRP` `08ee86e8`, `third_party/verilog-axis` `48ff7a7e` (`receipts/clone-integrity.txt`).

R624-6 FINISHED
