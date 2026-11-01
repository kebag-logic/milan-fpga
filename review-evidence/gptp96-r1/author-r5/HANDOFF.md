# [A707e] FPGA-gPTP #96 documentation sweep, round 5: handoff

Status: REVIEW READY. Nothing pushed; PR #97 not edited (not allowed in this lane).

- Repository: Mister-M-alt/FPGA-gPTP, branch `96-docs-sweep`.
- Source base: main `135afd043309369a87ddbc8d6550aff8ec52a157`.
- Round 5 base (round 4 head, PR #97 remote head): `db9ab2215ba18aec4c1828090b3611b001dbf2b8`.
- **Round 5 head: `9bd82bfb8739de2312da54a9a7b16fa596ec3a91`**. Local only: 4 commits on top of `db9ab221`, no rebase, no force.
- TAKEN on #96: issuecomment-6562872732.
- Brief: the [A10] round 5 ruling on #96 (issuecomment-6525270244), with reports R739-4 and R740-4. Round 4 handoff: `gptp96-a707d/HANDOFF.md`.

## Decisions for the manager to check

1. **Ten real-copy forms still pass the gate, as expected-failure self-test arms.** See "Expected failures". They lie outside the ruling's lists, so I did not widen the matcher. No current page uses any of them (`receipts/xfail_real_tree.log`). They are recorded under the round 4 rule (a named gate defect becomes a self-test case), not fixed. If you want any of them caught, each is a small change; its arm then moves to the must-fail list.
2. **The ruling's text conflicts with its own test on one point.** Item 2 says replace every `_`; item 3 says `snake_5_min` must pass, and replacing every `_` would make it read `snake 5 min` and fail. I took "delimiter" in the CommonMark sense: an underscore between two word characters delimits nothing, so it stays (`scripts/check_docs.py:129`). All six non-copies pass.
3. **Closing fences accept trailing tabs as well as spaces.** The ruling says "nothing but trailing spaces"; CommonMark 0.31.2 §4.5 says "spaces or tabs". I followed the spec the ruling names, because refusing a tab would leave the fence open and hide what follows.
4. **More than the ruling's three behaviours went into the scanner.** All of it is in `scripts/check_docs.py`, and each piece closes a real-copy escape measured at the round 4 head: §4.5's opening rules, list-item containers, and fence markers inside HTML comments. "Why the scanner goes past the ruling's sentences" gives the detail.
5. **The page pointer sentence is unchanged (R739-4 RES-1, R740-4 R2).** The ruling says no prose changes. The wording those reports propose also fails the page gate at 14 words against a limit of 10 (run through `style_findings`), so it cannot land as written. The PR body does take the wording.

## The ruling, and how it was applied

| Ruling item | Applied | Location (head) |
|---|---|---|
| 1. Fences follow CommonMark 0.31.2 §4.5: track character and run length; close only on the same character, at least as long, nothing else after; a shorter or different line inside is content | One scanner, `unfenced_lines` | `scripts/check_docs.py:169-210`, `:31-33` |
| 2. Replace every emphasis, strong and code-span delimiter outside code blocks with a space before the value rules; the boundary rules need no underscore case | `INLINE_MARKUP_RE` and `without_markup`; the value patterns in `value_spellings` are untouched | `:129`, `:502-507`, `:510-` |
| 3a. Each reviewer's plant becomes a self-test arm that must fail | 39 new must-fail arms, including all plants from both reports | `:838-887` |
| 3b. The six non-copies in R739-4's `underscore_boundary.txt` must pass | Pass arms (three already existed with the same text; three added) | `:812-814` and the existing arms above them |
| 3c. A planted mutant per rule: fence length ignored, fence char ignored, markup not stripped, each killed | The first three of 46 mutants, all killed | `receipts/checker_mutants.py`, `checker_mutants.log` |
| Scope: `scripts/check_docs.py` and its self-test only; no prose changes | One file changed; no Markdown changed | `git diff --raw db9ab221 HEAD` |

## Commits (one-line subjects, no body, no trailers)

| Commit | Subject |
|---|---|
| `6f80d59` | Follow CommonMark 4.5 for fences in one scanner and neutralise inline markup before the copy rule, each reviewed plant a self-test arm (#96) |
| `e85ef8d` | Record the real copies the rule still misses as expected-failure self-test arms (#96) |
| `46de6dd` | Record the fence after a lazy list line as an expected-failure self-test arm (#96) |
| `9bd82bf` | Use the two remaining reviewed fence plants verbatim as self-test arms (#96) |

Delta `db9ab221..9bd82bf`: 1 file (`scripts/check_docs.py`), mode unchanged. No RTL, generator, generated file, test bench, build input or Markdown changed.

## Changes, with file:line and reason

| Location (head) | Change | Reason |
|---|---|---|
| `scripts/check_docs.py:31-33` | `LIST_ITEM_RE`, `FENCE_OPEN_RE`, `FENCE_CLOSE_RE` | Ruling 1. |
| `:129` | `INLINE_MARKUP_RE`; replaces `FENCE_MARKERS` | Ruling 2. R739-4 F2, R740-4 F2. |
| `:169-210` `unfenced_lines` | One line scanner per §4.5 | Ruling 1. R739-4 F1, R740-4 F1. |
| `:213-215` `without_fences` | Now calls the scanner | R739-4 S-3, R740-4 S7: the style rule had the same toggle defect. |
| `:502-507` `without_markup` | Returns the line with delimiters spaced out and closed up, whitespace collapsed | Ruling 2. See below. |
| `:510-` `copy_findings` | Iterates the scanner's lines and searches both markup views | Ruling 1, 2. A heading inside a fence can no longer move the home section. |
| `:812-832` | 21 pass arms | Ruling 3b, and the "shorter or different line is content" cases. |
| `:838-887` | 39 must-fail arms; fixture gains `FU_RTO_MS_C` so R740-4's 125 ms plants stay verbatim | Ruling 3a. |
| `:900-916` | 4 arms: a fenced heading must not close or open the home section; the style rule's two fence cases | Scanner callers. |
| `:918-935` | 10 expected-failure arms | See below. |
| `:936` | `usage ={` restored to `usage = {` | R739-4 S-2, R740-4 S6. |

Self-test: 53 arms become 127. Production check at head: 14 current and 18 historical pages, rc 0, so no current page changes verdict.

### Why the scanner goes past the ruling's sentences

Each of these was a real-copy pass at `db9ab221`, measured in `receipts/tree_probes_db9ab22.log`, and §4.5 decides the first two:
- A fence on a list marker (`list_marker_fence`): the old check saw only the closing line, which then opened a fence hiding the rest of the page.
- A list item ending an unclosed fence (`list_end_closes_fence`): §4.5 ends the block with its container.
- A fence marker inside an HTML comment (`comment_fence_marker`): this falls under §4.6, not §4.5, but it is the same failure. Commenting out a code block is ordinary practice, and it hid the rest of the page.

### Why two markup views

The ruling's space replacement alone leaves `**5**-minute` reading `5 -minute`, which the separator rule does not match, and it splits `37*5* ms`. The closed-up view catches those. The spaced view catches a code span against a value, as in `` `hold`five minutes ``. Each view has a mutant killed at its own arm. The ruling says the fix holds "whatever markup surrounds a value", and whitespace collapse follows from it: `**375** ms` becomes `375  ms` after replacement.

## Expected failures (real copies that still pass)

`scripts/check_docs.py:918-935`. Each arm asserts no finding today. A change that catches the form fails the arm by name, and the case then moves to the must-fail arms.

| Form | Example | Why not fixed here |
|---|---|---|
| Decimal seconds | `0.375 s` | R739-4 S-1, R740-4 S2; accepted as a pass in round 3 |
| Spelled unit | `375 milliseconds` | Same |
| Wrapped line | `375` at a line end, `ms` on the next | The rule matches line by line; not markup |
| Link on the value | `[375](x.md) ms` | Not in the ruling's delimiter list |
| HTML tag on the value | `<b>375</b> ms` | Same |
| HTML entity as the space | `375&nbsp;ms` | Same |
| Strikethrough on the value | `~~375~~ ms` | Same; GFM, not CommonMark |
| Fence marker in an HTML block | `<pre>`, a fence line, `</pre>` | §4.6 block types beyond comments |
| Indented heading after the home section | `  ## Aside` on the constants page | Heading detection, outside the ruling |
| Fence after a lazy list line | `- Item.`, `lazy`, `  ` + fence | Needs paragraph tracking; the one scanner divergence the fuzz found |

Evidence:
- Each form gives rc 0 at head on a real page (`receipts/tree_probes_head.log`, kind `open`).
- Each has a mutant that closes it and trips its arm (`xfail_*` in `checker_mutants.log`).
- With each mutant applied to the production check, the real tree still passes (`receipts/xfail_real_tree.log`, all rc 0), so no current page holds such a copy.

## Evidence

| Check | Result | Receipt |
|---|---|---|
| 46 planted mutants, each run against `--selftest` in a scratch copy | All 46 rc 1, each at its expected arm; control rc 0 with 127 arms | `receipts/checker_mutants.py`, `checker_mutants.log` |
| 46 tree probes (real tree, one plant each): both reports' plants, the six non-copies, earlier controls, the 10 expected failures | `db9ab221`: 18 differ from expectation. Head: 0 differ | `receipts/tree_probes.py`, `tree_probes_db9ab22.log`, `tree_probes_head.log` |
| R739-4's own `fence_cases.py` | 0 disagreements (5 at `db9ab221`) | `receipts/r739_fence_cases.log` |
| R739-4's own `copy_probes_r4.sh`, 55 probes | Only `c_decimal_s` and `c_word_ms` still pass, both expected-failure arms; no false failure | `receipts/r739_copy_probes_head.txt` |
| Fuzz against a CommonMark parser (markdown-it-py 3.0.0, scratch venv), 300,000 documents | 160 escapes and 100 wrong-fence loud cases in about 405,000 sentinels | `receipts/commonmark_diff.py`, `commonmark_diff_full.log`, `parser_identity.txt` |
| The same fuzz with lazy continuation made impossible, 300,000 documents | **0 escapes, 0 wrong-fence cases**, so lazy continuation accounts for every divergence in this grammar | `receipts/commonmark_diff_nolazy.log` |
| Finding-site silencing (round 3 harness, full file) | 18 killed, 23 survive: the same sets as round 4, with lines moved | `receipts/site_mutants.py`, `site_mutants_head.log` |

Limits of this evidence:
- The fuzz grammar is a fixed list of fence, list and comment shapes. It exercises the scanner only, not the markup views, and contains no blockquote shapes.
- `LOUD-INDENT` (about 37,000 sentinels) is indented code, which the copy rule has always scanned. A copy there is reported, not hidden; I left that unchanged.
- A blockquoted fence is not recognised, so a copy inside one is reported (checked by a direct call at head). That is the safe direction, and it is unchanged from `db9ab221`.

## Prior findings at this head

| Finding | Resolution |
|---|---|
| R739-4 F1, R740-4 F1 (fence run length and trailing text) | Fixed in the scanner; plants are must-fail arms. |
| R739-4 F2, R740-4 F2 (underscore emphasis) | Fixed by the neutraliser, with no boundary-rule change; plants are must-fail arms. |
| R739-4 RES-1, R740-4 R2 (pointer scope wording) | Pages unchanged, per "no prose changes"; see decision 5. PR body updated. |
| R740-4 R1 (PR body's five-item enumeration) | Removed from `PR-BODY.md`. |
| R739-4 S-1, R740-4 S2 (decimal and unit-word limits) | Now expected-failure arms. Unitless rows have no arm: the rule only reads rows with a unit. |
| R739-4 S-2, R740-4 S6 (`usage ={`) | Fixed. |
| R739-4 S-3, R740-4 S7 (shared fence parser) | Done. |
| R739-4 S-4, R740-4 S1 (coincident figures) | Not taken; errs on the safe side. |
| R739-4 S-5, R740-4 S4 (`VERILATOR ?=`) | Not taken; a Makefile change, outside this scope. |
| R739-4 S-6, R740-4 S5 (WNS end value in the archive page) | Not taken; a prose change. |
| R740-4 S3 (second seeded image) | Not taken; outside this ruling. |

## Inventory (round 5 head)

Status legend:
- **Current**: checked against the source and against IEEE 802.1AS-2011 with Cor1/Cor2 and Milan v1.2 chapter 4.
- **Historical**: archived and bannered.

Per-page evidence is in the round 1 handoff, updated in rounds 2 to 4. Round 5 edits no Markdown.

| Page | Lines | Purpose / audience | Describes | Status | Round 5 evidence |
|---|---:|---|---|---|---|
| `README.md` | 98 | Start here; every reader | Scope, layout, reading order | Current (unchanged) | Status gate rc 0. |
| `docs/README.md` | 88 | Map and status table; every reader | All pages | Current (unchanged) | Status gate rc 0. |
| `docs/GLOSSARY.md` | 52 | Defined terms; every reader | 802.1AS-2011, Milan 4.2.6, engine terms | Current (unchanged) | Round 2 clause check stands. |
| `docs/MANAGER.md` | 129 | Readiness, ROM budget; manager | Delivery status | Current (unchanged) | ROM gate rc 0. |
| `docs/INTEGRATION.md` | 910 | External contract; integrator | Ports, policy, publication, constants | Current (unchanged) | Constants gate rc 0. |
| `docs/HDL_DEVELOPER.md` | 418 | Structure, invariants; HDL contributor | `hdl/` | Current (unchanged) | Round 3 evidence stands. |
| `docs/TEST_DEVELOPER.md` | 217 | Verification layers; test developer | `tb/`, `bench/`, `scripts/` | Current (unchanged) | States areas only. |
| `docs/SOURCE_EVIDENCE.md` | 59 | Claim-to-source ledger; reviewer | RTL and generator anchors | Current (unchanged) | 20 exact, 0 findings; self-test 7. |
| `docs/diagrams/README.md` | 81 | Diagram sources; maintainer | `docs/diagrams/` | Current (unchanged) | Diagram check and self-test rc 0. |
| `tb/verilator/engine/README.md` | 20 | Suite entry; test developer | Engine suite | Current (unchanged) | Inputs unchanged. |
| `tb/verilator/parser/README.md` | 24 | Suite entry | Parser suite | Current (unchanged) | Inputs unchanged. |
| `tb/verilator/ucpu/README.md` | 18 | Suite entry | MicroCPU suite | Current (unchanged) | Inputs unchanged. |
| `tb/verilator/gaskets/README.md` | 20 | Suite entry | Gasket loopback | Current (unchanged) | Inputs unchanged. |
| `tb/tsngen/README.md` | 20 | Suite entry | Independent decode | Current (unchanged) | Inputs unchanged. |
| `docs/history/v1/README.md` + 18 pages | - | Archive; maintainer | Superseded records | Historical (unchanged) | Archive check rc 0. |

Archive pages (18): `BENCH_FIRSTLIGHT`, `BENCH_GRANDMASTER`, `PROJECT_STATUS`, `RESOURCE_DELTAS_2026_10`, `RESOURCE_VALIDATION`; under `prototype/`: `ARCHITECTURE`, `BENCH_ASCAPABLE`, `BENCH_OPERATIONS`, `BENCH_TAP_WIRETRUTH`, `FSM_CONFORMANCE`, `INTEGRATION_GUIDE`, `IP_BLOCKS`, `MGMT_INTERFACE`, `RESOURCE_VALIDATION`, `VERIFICATION`; under `testing/`: `ENGINE_TEST_RECORD`, `PARSER_TEST_RECORD`, `UCPU_TEST_RECORD`.

## Findings the docs cannot fix (carried; for a code lane)

None is new this round.

| # | Location | Observation | Clause / source | Which side is wrong |
|---|---|---|---|---|
| G1 | `hdl/top/KL_gptp_engine.sv:43-45` | The header says the publish bank is "latched by OP_COMMIT". No latch exists: `:1134-1146` assign the staging registers to `pub_*_o`. | RTL `:994-997`, `:1037-1053`, `:1134-1146` | The source comment |
| G2 | `hdl/ucode/gen_gptp_ucode.py:2499` | The `--p1` default is the literal `248`, beside `P1_C = 248` at `:513`. | Milan v1.2 4.2.6.2.1 | The generator (`default=P1_C`) |
| F1 | `gen_gptp_ucode.py:284` | The history note says asCapable falls "at the fourth" lost response. The code clears it at `LOST_CLEARS_AT_C`. | 802.1AS-2011 Figure 11-8 (Cor1) | The source comment |
| F2 | `gen_gptp_ucode.py:292-296` | The history note says syncReceiptTimeout "clears the sync-ok verdict". Since #89 it ages the grandmaster when gmPresent. | 10.3.11, Figure 10-13 (Cor1) | The source comment |
| F3 | `gen_gptp_ucode.py:315-317` | The history note says the 4.2.6.2.5 cease is "still deliberately out". It is implemented. | Milan v1.2 4.2.6.2.5 | The source comment |
| F4 | `KL_gptp_engine.sv:43-45` | Repeated phrase "becomes ... becomes wires". | n/a | Source comment wording |
| F5 | `docs/HDL_DEVELOPER.md` OOC table | The figures are dated (main `5dce647a`, 2026-10-11). | n/a | Neither; needs `make ooc` |

## Gate table

Environment:
- The pinned Verilator 5.050, first on `PATH` (identity in `receipts/gates-*/identity.txt`).
- `TMPDIR` set to scratch.
- Every command ran in the foreground and unpiped, with its output to a log and its own rc recorded (`receipts/gates.sh`).

### Repository gates (docs and CI hygiene; the repository has no hosted workflow files)

| Gate | Base `db9ab221` | Head `9bd82bf` |
|---|---|---|
| `make docs` | rc 0: 14 current, 18 historical; docs self-test 53; diagram self-test 10; source evidence 20 exact, self-test 7 | rc 0: 14 current, 18 historical; docs self-test 127; diagram self-test 10; source evidence 20 exact, self-test 7 |
| `make diagrams-check` | rc 0 | rc 0 |
| `make contract` | rc 0 | rc 0 |
| `make lint` | rc 0 | rc 0 |
| `git diff --check 135afd04 HEAD` | rc 0 | rc 0 |
| `git diff --check db9ab221 HEAD` | rc 0 (empty) | rc 0 |
| `git status --porcelain` after gates | clean | clean |

- The suites (`make tb`) were not rerun. The delta touches no `hdl/`, `tb/`, `bench/`, `syn/` or Makefile path, and the round 2 runs stand.
- Not run: the engine mutation arm and `make ooc`, as in rounds 1 to 4.

### Parent consumer gates (required, because `scripts/check_docs.py` changed)

Setup:
- A fresh scratch clone of kebag-logic/milan-fpga at PR #805 head `e06ade312a80eb578579365134ab797cda90622b`, with submodules.
- The lane branch was fetched into its gptp-processor checkout, after a `--show-toplevel` check. The gitlink was then set with `update-index` to each SHA (`receipts/parent_gates.sh`, unchanged from round 4).
- Afterwards the pin was restored to `f97c1803`, and parent `git status` is clean. Nothing was committed or pushed.

| Gate | `f97c1803` (PR #805 pin) | `db9ab221` | `9bd82bf` |
|---|---|---|---|
| `check_gptp_docs.py` | 0 | 1 | 1 |
| `check_gptp_docs.py --with-submodule` | 0 | 1 | 1 |
| `check_gptp_docs.py --selftest` | 0 | 1 | 1 |
| `make -C gptp-processor docs` | 0 | 0 | 0 (127 arms) |
| `check_submodule_docs.py` | 0 | 1 | 1 |
| `check_submodule_docs.py --selftest` | 0 | 0 | 0 |
| `measure_naming.py --check` | 0 | 0 | 0 |
| `measure_fail_fast.py --check` | 0 | 0 | 0 |
| `measure_test_evidence.py --check` | 0 | 0 | 0 |
| `check_hygiene.py --check` | 0 | 0 | 0 |
| `check_gptp_docs.py --with-submodule`, parent docs re-pinned to the gitlink (13 files, scratch only, restored) | n/a | 0 | 0 |

- The rc 1 rows fail on the pin, as in rounds 1 to 4: "donor reference must use gitlink ..., found f97c1803...". They will fail on any gitlink move until the parent pins are rewritten.
- Once the SHA is normalised, the logs at `db9ab221` and `9bd82bf` are byte-identical (`receipts/parent_diff.txt`).
- Logs: `receipts/parent/`, `receipts/parent_gates.txt`.

## Not done / follow-ups

- The parent bump must re-pin the parent gPTP docs and the submodule-docs page and diagram.
- The engine mutation arm and `make ooc` were not run.
- The S-items listed as "not taken" above.

## Postings on #96

- TAKEN: issuecomment-6562872732
- REVIEW READY with head `9bd82bfb8739de2312da54a9a7b16fa596ec3a91`: posted on the issue thread after this file was finalised.
