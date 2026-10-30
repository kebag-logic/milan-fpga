# [A707d] FPGA-gPTP #96 documentation sweep, round 4: handoff

Status: REVIEW READY. Nothing pushed; PR #97 not edited (not allowed in this lane).

- Repository: Mister-M-alt/FPGA-gPTP, branch `96-docs-sweep`.
- Source base: main `135afd043309369a87ddbc8d6550aff8ec52a157`.
- Round 4 base (round 3 head, PR #97 remote head): `411b35fcc56d11c2361d861e7205307587a04a1d`.
- **Round 4 head: `db9ab2215ba18aec4c1828090b3611b001dbf2b8`**. Local only: 2 commits on top of `411b35fc`, with no rebase and no force.
- TAKEN on #96: issuecomment-6522001129.
- REVIEW READY on #96: issuecomment-6522201186.
- Brief: the [A10] round 4 ruling on #96 (2026-10-30T11:48:47Z), with reports R739-3 and R740-3. Round 3 handoff: `gptp96-a707c/HANDOFF.md`.

## The ruling, and how it was applied

The ruling, verbatim in substance:
1. Remove every prose statement of the gate's matching rules, accepted forms and rejected forms (gate page, constants-table preamble, PR body).
2. In their place, one sentence: the rules are `scripts/check_docs.py`, and its self-test cases are the specification, with a link to the self-test.
3. A named case that is a gate defect becomes a self-test case. Either fix the checker or record an expected failure. Never describe it in prose.
4. Make no other change.

Applied:
1. Every gate-rule sentence on a current page is removed. The audit is below.
2. The sentence reads: "`make docs` rules are `scripts/check_docs.py`; its [`selftest()`](../scripts/check_docs.py) cases are the specification." It stands once beside each checked table:
   - `docs/README.md:48` (status table);
   - `docs/INTEGRATION.md:856` (constants preamble);
   - `docs/MANAGER.md:59` (ROM budget).

   The page's 10-word limit rules out "The" at the start; with it the sentence counts 11. The link targets the file, because a `#L` line anchor would drift silently and no gate checks it. The link text names the function.
3. Every case the reviews named was a checker defect. The checker is fixed for each one, and each has a self-test arm. No case is left as an expected failure.
4. No other change. The PR body keeps its structure; only the freshness section, intro and gate section changed.

## Commits (one-line subjects, no body, no trailers)

| Commit | Subject | Ruling item |
|---|---|---|
| `c6bca77` | Pass decimal minutes, larger number words and tilde fences, and catch unspaced minutes and comma-less unit cells, each with a self-test arm (#96) | 3 |
| `db9ab22` | Replace the prose statements of the docs gate rules with one pointer to the checker and its self-test (#96) | 1, 2 |

Delta `411b35f..db9ab22`: 4 files, +46/-33.
- `docs/INTEGRATION.md`, `docs/MANAGER.md`, `docs/README.md`.
- `scripts/check_docs.py`, a docs-gate script.

No RTL, generator, generated file, test or build input changed. Whole PR `135afd04..db9ab22`: 14 files, +865/-125.

## Changes, with file:line and reason

### Docs (`db9ab22`)

| Location (head) | Change | Reason |
|---|---|---|
| `docs/INTEGRATION.md:852-856` | Removed 13 prose units at old `:854-872`: drift, missing, duplicate and formatted rows; unit source; the rejected forms; exemptions; unitless rows; passes; "Review keeps those forms out." Added the pointer sentence at `:856`. | Ruling 1, 2. R739-3 F1, F2; R740-3 F1, F2. |
| `docs/INTEGRATION.md:884` | Removed "`make docs` does not check them." after the cadence sentence. | Ruling 1: a statement of what the gate accepts. The doc fact stays: "These cadences are literals inside generator legs." |
| `docs/MANAGER.md:55-59` | Removed "`make docs` fails when this table drifts from it." and "The seeded row is checked with `--seq-seed 0x200000`." Added "The seeded row counts the `--seq-seed 0x200000` image." (`:57`) and the pointer (`:59`). | Ruling 1, 2. The kept sentence says which image the row counts, not what the gate does. Verified: that seed builds 1,023 real words of 1,024 and shipping builds 1,022 (`receipts/rom_counts.txt`). It matches the engine suite's seeded run (`tb/verilator/engine/Makefile:36`). |
| `docs/README.md:46-48` | Removed "`make docs` fails when a page lacks its row." Added the pointer at `:48`. | Ruling 1, 2. |

Unchanged on purpose:
- `docs/TEST_DEVELOPER.md:11` and `:52`. They list the gate areas `make docs` covers (style, links, status, constants, diagrams), but no matching rule.
- `docs/INTEGRATION.md:854`: "Other pages name the constant and link its row." This is the authoring convention, not a gate statement.

An extra sentence ("`make docs` checks this table and those links") was drafted and removed before commit. It went beyond the one sentence, and "those links" was false: the gate rejects restated values but does not require the link.

### Checker (`c6bca77`), `scripts/check_docs.py`

| Line (head) | Change | Named case (report) |
|---|---|---|
| `:121-123` `UNIT_CELL_RE` | A Meaning cell ending in a comma, a space or an opening parenthesis before ms, ns or ppm gives the unit. Before, only a comma did. | "syncReceiptTimeout ms" (R740-3 F2); "syncReceiptTimeout in ms" (R739-3 F1 `u_meaning_ends_in_ms`); "(ms)" (R739-3 `u_meaning_paren`). Before the fix, each passed a real copy. |
| `:124`, `:477-482` | Fences open on a backtick or tilde marker and close only on the same marker. | `~~~` fence false finding (R739-3 F2 `x_fenced_tilde`). |
| `:456` minute digits | Number lookbehind `(?<![\d.,])`, optional separator, `min`/`mins`/`minute(s)` ending on a word boundary. | "2.5 min", "7.5 minutes" (R739-3 F2); "0.5 minutes", "1.5 min" (R740-3 F1): false findings before. "5min" (R739-3 F1): an escaped copy before. "5 minimum" (R739-3 S-1): a false finding before. |
| `:457` minute words | Lookbehind `(?<![\w-])`; accepts `min` as well as `minute(s)`. | "five min" (R739-3 F1): an escaped copy before. "twenty-five minutes" (R739-3 S-1): a false finding before. |
| `:759-787` | 11 new self-test arms: 5 pass, 3 copy and 3 unit-cell. Each copy and unit-cell arm needs its named "restates" finding. | One per case above. One extra arm checks that a `~~~` fence is not closed by a backtick line. |

Self-test: 42 arms become 53. Production check at head: 14 current pages and 18 historical pages, rc 0, so no current page changes verdict.

## Evidence for each checker change

| Check | Result | Receipt |
|---|---|---|
| Revert each of the 9 checker changes alone in a scratch copy, then run `--selftest` | All 9 rc 1, each at its own arm; the unmutated control rc 0 with 53 arms | `receipts/checker_mutants.py`, `checker_mutants.log` |
| Plant 25 probes in archive copies of the real tree and run the docs check: every named case plus the controls the reviews kept | At `411b35f`, 13 probes differ from expectation, reproducing every named defect. At `db9ab22`, 0 differ. | `receipts/tree_probes.py`, `tree_probes_411b35f.log`, `tree_probes_db9ab22.log` |
| Silence each finding site, then run `--selftest` (round 3 harness, full file range) | 18 killed, the same 18 as round 3. Rule-site survivors are the same five the PR body names (`:375`, `:377`, `:421`, `:431`, `:533`) plus the archive-banner rule and `required_current` (both before this PR). The rest are production aggregators (`:558-582`) that the self-test does not call. | `receipts/site_mutants.py`, `site_mutants_head.log` |

Probe outcomes at head, with "reject" meaning a named "restates" finding:
- Pass: the 4 decimal minutes, the tilde fence, "twenty-five minutes", "5 minimum", "0.375 s", "375 milliseconds", a backtick fence, and the control.
- Reject: "5min", "five min", all 3 comma-less unit cells, the comma-cell control, a copy after a tilde fence, "5 min", "five minutes", "five-minute", "5 mins", "300 s", "20 us" and "300,000 ms".

## Gate-claim audit at head (every sentence about the docs gate)

| Location | Sentence | Kind |
|---|---|---|
| `docs/README.md:48`, `docs/INTEGRATION.md:856`, `docs/MANAGER.md:59` | The pointer sentence | The ruling's sentence |
| `docs/TEST_DEVELOPER.md:11` | "Documentation gates check style, links, status and generated values." | Area list, no rule |
| `docs/TEST_DEVELOPER.md:24`, `:52` | Layer and entry-point tables | Area list, no rule |
| `README.md:36` | "`scripts/` / Documentation and diagram gates" | Layout |
| PR body, "Freshness checks" | The pointer sentence; arm counts; the mutant and probe results; the five findings without an arm | Test facts, no rule |

`grep -rnE "fails|rejects|exempt|not checked|does not check|pass" README.md docs/*.md docs/diagrams tb` turns up no other docs-gate rule sentence. The remaining hits are about RTL, other gates or release criteria.

## Inventory (round 4 head)

Status legend:
- **Current**: checked against the source and against IEEE 802.1AS-2011 with Cor1/Cor2 and Milan v1.2 chapter 4.
- **Historical**: archived and bannered.

Per-page evidence is in the round 1 handoff, updated in rounds 2 and 3. Round 4 edits only the rows marked "edited".

| Page | Lines | Purpose / audience | Describes | Status | Round 4 evidence |
|---|---:|---|---|---|---|
| `README.md` | 98 | Start here; every reader | Scope, layout, reading order | Current (unchanged) | Status gate rc 0. |
| `docs/README.md` | 88 | Map and status table; every reader | All pages | Current (edited) | `:48` is the pointer; status table unchanged. |
| `docs/GLOSSARY.md` | 52 | Defined terms; every reader | 802.1AS-2011, Milan 4.2.6, engine terms | Current (unchanged) | Round 2 clause check stands. |
| `docs/MANAGER.md` | 129 | Readiness, ROM budget; manager | Delivery status | Current (edited) | `:57` checked against generator output; `:59` is the pointer. |
| `docs/INTEGRATION.md` | 910 | External contract; integrator | Ports, policy, publication, constants | Current (edited) | `:856` is the pointer; constants and cadence tables unchanged. |
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

| Gate | Base `411b35fc` | Head `db9ab22` |
|---|---|---|
| `make docs` | rc 0: 14 current, 18 historical; docs self-test 42; source evidence 20 exact, self-test 7 | rc 0: 14 current, 18 historical; docs self-test 53; source evidence 20 exact, self-test 7 |
| `make diagrams-check` | rc 0 | rc 0 |
| `make contract` | rc 0 | rc 0 |
| `make lint` | rc 0 | rc 0 |
| `git diff --check 135afd04 HEAD` | rc 0 | rc 0 |
| `git diff --check 411b35fc HEAD` | rc 0 (empty) | rc 0 |
| `git status --porcelain --ignored` after gates | ignored build dirs only | ignored build dirs only |

- The suites (`make tb`) were not rerun. The delta touches no `hdl/`, `tb/`, `bench/`, `syn/` or Makefile path, and the round 2 runs stand.
- Not run: the engine mutation arm and `make ooc`, as in rounds 1 to 3.

### Parent consumer gates (required, because `scripts/check_docs.py` changed)

Setup:
- A fresh scratch clone of kebag-logic/milan-fpga at PR #805 head `e06ade312a80eb578579365134ab797cda90622b`, with submodules.
- The lane branch was fetched into its gptp-processor checkout, after a `--show-toplevel` check. The gitlink was then set with `update-index` to each SHA (`receipts/parent_gates.sh`, unchanged from round 3).
- Afterwards the pin was restored to `f97c1803`, and parent `git status` is clean. Nothing was committed or pushed.

| Gate | `f97c1803` (PR #805 pin) | `411b35fc` | `db9ab22` |
|---|---|---|---|
| `check_gptp_docs.py` | 0 | 1 | 1 |
| `check_gptp_docs.py --with-submodule` | 0 | 1 | 1 |
| `check_gptp_docs.py --selftest` | 0 | 1 | 1 |
| `make -C gptp-processor docs` | 0 | 0 | 0 (53 arms) |
| `check_submodule_docs.py` | 0 | 1 | 1 |
| `check_submodule_docs.py --selftest` | 0 | 0 | 0 |
| `measure_naming.py --check` | 0 | 0 | 0 |
| `measure_fail_fast.py --check` | 0 | 0 | 0 |
| `measure_test_evidence.py --check` | 0 | 0 | 0 |
| `check_hygiene.py --check` | 0 | 0 | 0 |
| `check_gptp_docs.py --with-submodule`, parent docs re-pinned to the gitlink (13 files, scratch only, restored) | n/a | 0 | 0 |

- The rc 1 rows are pin-driven, as in rounds 1 to 3: "donor reference must use gitlink ..., found f97c1803...".
- Once the SHA is normalised, the findings at `411b35fc` and `db9ab22` are byte-identical (`receipts/parent_diff.txt`).
- Logs: `receipts/parent/`, `receipts/parent_gates.txt`.

## Not done / follow-ups

- R739-3 S-2 (a coincident unrelated figure is reported as a copy): not taken. It is not one of the named defects, and it errs on the safe side.
- R739-3 S-3 (`VERILATOR ?=` in the Makefile): a build change, outside this docs lane.
- R739-3 S-4: `docs/history/v1/RESOURCE_DELTAS_2026_10.md:30` does not say where WNS moves to. Not taken under "make no other change". The page is historical and links the candidate timing report.
- The base `without_fences` (`scripts/check_docs.py:163-174`, used by the style rule) still treats only backtick fences as code. That case was not named, and the function predates this PR.
- The parent bump must re-pin the parent gPTP docs and the submodule-docs page and diagram.
- The engine mutation arm and `make ooc` were not run.

## Postings on #96

- TAKEN: issuecomment-6522001129
- REVIEW READY with head `db9ab2215ba18aec4c1828090b3611b001dbf2b8`: issuecomment-6522201186
