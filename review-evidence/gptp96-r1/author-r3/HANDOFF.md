# [A707c] FPGA-gPTP #96 documentation sweep, round 3: handoff

Status: REVIEW READY. Nothing pushed; PR #97 not edited (not allowed in this lane).

- Repository: Mister-M-alt/FPGA-gPTP, branch `96-docs-sweep`.
- Source base: main `135afd043309369a87ddbc8d6550aff8ec52a157`.
- Round 3 base (round 2 head, PR #97 remote head): `806957b35c3c23a36505744d205f9692720d19e2`.
- **Round 3 head: `411b35fcc56d11c2361d861e7205307587a04a1d`**. Local only: 4 commits on top of `806957b3`, no rebase, no force.
- TAKEN on #96: issuecomment-6521397706.
- REVIEW READY on #96: issuecomment-6521611261.
- Brief: the [A10] round 3 comment on #96 (issuecomment after 6520923345, 2026-10-30T11:18:41Z). It names R739-2 F1 and F2 and R740-2 F1, and gives this ruling: each sentence about the gate states what it checks, and only that. Narrow the claim or extend the checker with a planted failure, whichever is smaller. No new gate features.
- Round 2 handoff: `gptp96-a707b/HANDOFF.md`. Round 1 handoff: `gptp96-a707/HANDOFF.md`.

## Commits in this round (one-line subjects, no body, no trailers)

| Commit | Subject | Resolves |
|---|---|---|
| `5c78cc9` | Link the four PR #76 engine utilization and timing reports themselves at parent 4999d8d6 (#96) | R740-2 F1 |
| `a43fa21` | Add a self-test arm that plants a duplicate constants row and expects its named finding (#96) | R739-2 F1; also carries R739-2 RES-3 (see note) |
| `c55a631` | State exactly which restated forms the copy rule rejects and which seeded image the ROM row is checked against (#96) | R739-2 F2 (option b, narrow); R739-2 S-4 / R740-2 S1 claim scope |
| `411b35f` | Say the commit cycle always presents a complete tuple, and that staging writes change outputs first (#96) | R739-2 RES-1, RES-2 |

Note on `a43fa21`: the same commit also appends "(#96)" to the three new source comments (R739-2 RES-3). The subject names only the arm. Both changes are comment or test edits in `scripts/check_docs.py`.

Delta `806957b..411b35f`: 5 files, +35/-8.
- Four Markdown files: `docs/INTEGRATION.md`, `docs/MANAGER.md`, `docs/HDL_DEVELOPER.md`, `docs/history/v1/RESOURCE_DELTAS_2026_10.md`.
- One docs-gate script, `scripts/check_docs.py`: one self-test arm (6 lines) and three comment tags. No production rule changed.
- `git diff --name-only 806957b HEAD -- hdl tb bench syn Makefile` is empty. No RTL, generator, generated file, test or build input changed.

Whole PR `135afd04..411b35f`: 14 files. 12 are Markdown; the other two are `scripts/check_docs.py` and `scripts/check_source_evidence.py`.

## Findings: resolution at head

### R740-2 F1: history page must link the `.rpt` files

- `docs/history/v1/RESOURCE_DELTAS_2026_10.md:32-37` now reads "The measurement reports are at parent commit `4999d8d6`:", then four label-free links:
  - baseline utilization: `.../blob/4999d8d6344e373e0204995cb36c93cf616e8f9e/review-evidence/gptp75-r1/author/baseline-engine_util.rpt`;
  - candidate utilization: `.../candidate-engine_util.rpt`;
  - baseline timing: `.../baseline-engine_timing.rpt`;
  - candidate timing: `.../candidate-engine_timing.rpt`.
- Each link returns HTTP 200 (`receipts/history_links.txt`).
- I fetched the four blobs through the contents API at that commit. Their figures match the page:
  - LUTs 4,773 → 4,853 (+80);
  - registers 3,646 → 3,652 (+6);
  - memory LUTs 466 / 466;
  - WNS +2.249 → +1.773 ns.
- The historical values and the commit pin are unchanged. The ucpu and `util_hier` reports are not linked, because the page states no figure from them.

### R739-2 F1: no self-test arm for a duplicate constants row

- New arm at `scripts/check_docs.py:713-718`. It appends a second copy of the true `SYNC_RTO_MS_C` row to the true table. It then requires a finding containing "duplicate constant row: SYNC_RTO_MS_C". Self-test: 41 → 42 arms.
- Planted mutant: the reviewer's `checker_mutants.sh`, run unchanged against the lane. `no_const_duplicate` now gives selftest rc 1, "duplicate constant row escaped". The other seven weakenings still give rc 1, and the unmutated control gives rc 0 (`receipts/reviewer_checker_mutants.log`). The real-tree duplicate fails the gate (`dup_const_row_real_tree`, rc 1).
- The PR body's coverage claim ("Every rule has a true control ...") was also too broad. It is narrowed; see "Gate-claim audit".

### R739-2 F2: copy rule misses decimal and spelled-unit forms

- Option (b), narrowing the claim, is smaller than extending `value_spellings`, so it was taken.
- `docs/INTEGRATION.md:852-874` now states the rule as `value_spellings` and `copy_findings` implement it:
  - "Units come from Meaning cells ending ms, ns or ppm." (`UNIT_CELL_RE`, `:123`; R739-2 S-2)
  - "Elsewhere on current pages, `make docs` rejects that row value as:"
    - "the integer and its unit symbol, as in `7 ms`" (plain or comma-grouped; `:446-450`);
    - "ms in whole seconds, ns in whole microseconds, by symbol" (`:442-445`);
    - "ms as one to ten whole minutes: `2 min`, `two minutes`" (`:451-454`).
  - "Fenced code and this section are exempt." (`:474-480`)
  - "Rows without such a unit are not checked for copies." (R739-2 S-2, S-3)
  - "Decimals and other unit words, such as milliseconds, pass."
  - "Review keeps those forms out."
- The drift sentence was narrowed too. It was "fails when any value drifts from the generator", but the cadence table in the same section is unchecked. It now reads "fails when a row drifts from its constant".
- Every stated form and every stated pass was probed in a real-tree copy (`receipts/copy_probes.py`, log `receipts/copy_probes.log`, 0 probe failures). Results:
  - rejected with the named diagnostic: `375 ms`, `375ms`, `375-ms`, `300,000 ms`, `200 ppm`, `800 ns`, `300 s`, `20 us`, `20 µs`, `20 μs`, `5 min`, `five minutes`, `five-minute`, and `375 ms` in a later section of `INTEGRATION.md`;
  - passing, as stated: `0.375 s`, `0.1 ms`, `375 milliseconds`, `20 microseconds`, a fenced `375 ms`, `375 ms` inside the Protocol constants section, "fifth", and `375 ms` on a historical page.
- The reviewer's `plant_probes_r2.sh` at head: all 24 expect-fail probes fail and the control passes. The five `limit_*` probes still pass, and each is now a stated limit (`receipts/reviewer_plant_probes.log`).

### R739-2 RES-1, RES-2, RES-3 (wording; applied)

- RES-1, `docs/INTEGRATION.md:567`: "The commit cycle always presents a complete tuple." The suggested wording ran to 12 words, over the page's 10-word limit. This keeps its meaning and drops "only".
- RES-2, `docs/HDL_DEVELOPER.md:12`: "- Sample on `pub_commit_o`; staging writes change outputs first." This is the suggested wording, shortened to fit 10 words.
- RES-3: `scripts/check_docs.py:112`, `:122` and `:394` end with "(#96)".

### R739-2 S-4 = R740-2 S1 (seeded ROM row), claim side only

- `docs/MANAGER.md:59`: "The seeded row is checked with `--seq-seed 0x200000`." The gate binds only that image (`SEEDED_SEQ_SEED`, `scripts/check_docs.py:129`, used at `:556`). "`make docs` fails when this table drifts from it" no longer implies more.
- The `--sync-seq-seed 0x10000` image is not added to the checker: that would be a new gate feature. Both images build 1,023 words today (R740-2 `spot-*.log`).

## Gate-claim audit (every sentence about the gate, at head)

| Location | Sentence | Backed by | Isolating evidence |
|---|---|---|---|
| `docs/README.md:48` | `make docs` fails when a page lacks its row. | `status_findings` "no status row for" | site mutant `:380` killed |
| `docs/MANAGER.md:57` | `make docs` fails when this table drifts from it. | `rom_findings` | site mutants `:521`, `:532`, `:536` killed |
| `docs/MANAGER.md:59` | The seeded row is checked with `--seq-seed 0x200000`. | `freshness_findings` `:556` | code read |
| `docs/INTEGRATION.md:854` | `make docs` fails when a row drifts from its constant. | `constant_findings` `:425-428` | site mutant `:426` killed |
| `docs/INTEGRATION.md:856` | It also fails on a missing, duplicate or formatted row. | `:431`, `:415`, `:422` | all three killed; `:415` by the new arm |
| `docs/INTEGRATION.md:860-874` | Copy rule, its forms and its limits | `value_spellings`, `copy_findings` | 23 copy probes; reviewer limit probes |
| `docs/INTEGRATION.md:904` | `make docs` does not check them. (cadences) | no rule reads the cadence table | code read |
| `docs/TEST_DEVELOPER.md:24`, `:52` | Lists what `make docs` covers | the Makefile `docs` target | no coverage claim beyond the list |
| PR body, "Freshness checks" | rewritten to match the above | as above | as above |

Site mutants (`receipts/site_mutants.py`) silence one finding site of `check_docs.py` at a time, then run `--selftest` (`receipts/site_mutants_head.log`). At head 18 of 32 sites are killed. 14 survive:
- Archive banner rule, `:296-315` (8 sites): predates this PR. No arm at base either.
- `required_current_findings` extend, `:330`: predates this PR.
- Status, `:374` "no document status rows" and `:376` "no status row for docs/history/v1/".
- Constants, `:420` "is not a generator constant" and `:430` "no protocol constant rows". Their arms (unknown name, empty table) also produce a "no protocol constant row for" finding, so a second finding masks them.
- ROM, `:528` "counts are not plain decimals".

No Current page or PR-body sentence claims self-test coverage for these 14 sites. The PR body names them as a limit and does not claim that every rule has an arm. Adding arms for them would go beyond the findings, so none were added. At base the same harness shows 15 survivors; `:415` is the one this round kills.

## Inventory (round 3 head)

Status legend:
- **Current**: checked at head against the source and against IEEE 802.1AS-2011 with Cor1/Cor2 and Milan v1.2 chapter 4.
- **Historical**: archived and bannered.

The round 1 handoff has the full per-page evidence. Round 2 updated it, and round 3 changes only the rows marked "edited".

| Page | Lines | Purpose / audience | Describes | Status | Round 3 evidence |
|---|---:|---|---|---|---|
| `README.md` | 98 | Start here; every reader | Scope, layout, reading order | Current (unchanged) | Status gate rc 0. |
| `docs/README.md` | 88 | Map and status table; every reader | All pages | Current (unchanged) | `:48` claim backed (site `:380` killed). |
| `docs/GLOSSARY.md` | 52 | Defined terms; every reader | 802.1AS-2011, Milan 4.2.6, engine terms | Current (unchanged) | Round 2 clause check stands. |
| `docs/MANAGER.md` | 129 | Readiness, ROM budget; manager | Delivery status | Current (edited) | `:59` names the checked seeded image (`check_docs.py:129`, `:556`). |
| `docs/INTEGRATION.md` | 930 | External contract; integrator | Ports, policy, publication, constants | Current (edited) | `:852-874` match `value_spellings` (23 probes). `:567` matches `KL_gptp_engine.sv:1134-1146`. |
| `docs/HDL_DEVELOPER.md` | 418 | Structure, invariants; HDL contributor | `hdl/` | Current (edited) | `:12` matches the output assigns. |
| `docs/TEST_DEVELOPER.md` | 217 | Verification layers; test developer | `tb/`, `bench/`, `scripts/` | Current (unchanged) | `:52` lists gates, claims no coverage. |
| `docs/SOURCE_EVIDENCE.md` | 59 | Claim-to-source ledger; reviewer | RTL and generator anchors | Current (unchanged) | 20 exact, 0 findings; selftest 7. |
| `docs/diagrams/README.md` | 81 | Diagram sources; maintainer | `docs/diagrams/` | Current (unchanged) | Diagram check and selftest rc 0. |
| `tb/verilator/engine/README.md` | 20 | Suite entry; test developer | Engine suite | Current (unchanged) | Inputs unchanged since round 2. |
| `tb/verilator/parser/README.md` | 24 | Suite entry | Parser suite | Current (unchanged) | Inputs unchanged. |
| `tb/verilator/ucpu/README.md` | 18 | Suite entry | MicroCPU suite | Current (unchanged) | Inputs unchanged. |
| `tb/verilator/gaskets/README.md` | 20 | Suite entry | Gasket loopback | Current (unchanged) | Inputs unchanged. |
| `tb/tsngen/README.md` | 20 | Suite entry | Independent decode | Current (unchanged) | Inputs unchanged. |
| `docs/history/v1/README.md` + 18 pages | - | Archive; maintainer | Superseded records | Historical | Archive check rc 0. `RESOURCE_DELTAS_2026_10.md:32-37` links the four `.rpt` blobs (62 lines). |

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
- Verilator 5.050, the pinned build, first on `PATH`; identity is in `receipts/gates-*/identity.txt`.
- `TMPDIR` set to scratch.
- Every command ran in the foreground, unpiped, output to a log, rc from the command (`receipts/gates.sh`).

### Repository gates (docs and CI hygiene; the repository has no hosted workflow files)

| Gate | Base `806957b3` | Head `411b35fc` |
|---|---|---|
| `make docs` | rc 0 (14 current, 18 historical; selftest 41; source evidence 20 exact, selftest 7) | rc 0 (14 current, 18 historical; selftest 42; source evidence 20 exact, selftest 7) |
| `make diagrams-check` | rc 0 | rc 0 |
| `make contract` | rc 0 | rc 0 |
| `make lint` | rc 0 | rc 0 |
| `git diff --check 135afd04 HEAD` | rc 0 | rc 0 |
| `git diff --check 806957b3 HEAD` | rc 0 | rc 0 |
| `git status --porcelain` after gates | clean (ignored build dirs only) | clean (ignored build dirs only) |

- Suites (`make tb`) were not rerun this round. No input to them changed since `806957b3`: the delta touches no `hdl/`, `tb/`, `bench/`, `syn/` or Makefile path. The round 2 base and head runs stand.
- Not run: the engine mutation arm and `make ooc`, as in rounds 1 and 2.

### Planted defects and mutants (every new or changed claim)

| Check | Result | Receipt |
|---|---|---|
| New duplicate-row arm vs. `no_const_duplicate` mutant | selftest rc 1 "duplicate constant row escaped" | `reviewer_checker_mutants.log` |
| Reviewer's other 7 checker weakenings | rc 1 each; control rc 0 | same |
| Real-tree duplicate constants row | gate rc 1, named finding | same |
| Copy-rule claims: 14 rejected forms, 8 stated passes, control | all as stated, 0 probe failures | `copy_probes.log` |
| Reviewer plant probes (24 fail, 5 limits, control) | all as expected; limits now stated | `reviewer_plant_probes.log` |
| Site mutants of every finding site | base 15 survivors, head 14; survivors listed above | `site_mutants_base.log`, `site_mutants_head.log` |
| History links | 4 × HTTP 200; figures match the blobs | `history_links.txt` |

### Parent consumer gates (required: `scripts/check_docs.py` changed)

Setup:
- A fresh scratch clone of kebag-logic/milan-fpga at PR #805 head `e06ade312a80eb578579365134ab797cda90622b`, with submodules initialised.
- The lane head was fetched into the gptp-processor checkout. The gitlink was set with `update-index` to each SHA in turn, with `--show-toplevel` verified first (`receipts/parent_gates.sh`, unchanged from round 2).
- The pin was restored to `f97c1803` afterwards; parent `git status` is clean. Nothing was committed or pushed.

| Gate | Gitlink `f97c1803` (PR #805 pin) | Gitlink `806957b3` | Gitlink `411b35fc` |
|---|---|---|---|
| `check_gptp_docs.py` | 0 | 1 | 1, identical to `806957b3` |
| `check_gptp_docs.py --with-submodule` | 0 | 1 | 1, identical |
| `check_gptp_docs.py --selftest` | 0 | 1 | 1, identical |
| `make -C gptp-processor docs` | 0 | 0 | 0 (42 arms) |
| `check_submodule_docs.py` | 0 | 1 | 1, identical |
| `check_submodule_docs.py --selftest` | 0 | 0 | 0 |
| `measure_naming.py --check` | 0 | 0 | 0 |
| `measure_fail_fast.py --check` | 0 | 0 | 0 |
| `measure_test_evidence.py --check` | 0 | 0 | 0 |
| `check_hygiene.py --check` | 0 | 0 | 0 |
| `check_gptp_docs.py --with-submodule`, parent docs re-pinned to the gitlink (13 files, scratch only, restored) | n/a | 0 | 0 |

- The rc 1 rows are pin-driven, as in rounds 1 and 2. The parent pages deep-link to `f97c1803`, so the gate reports "donor reference must use gitlink ...".
- The findings at `806957b3` and `411b35fc` are byte-identical once the SHA is normalised.
- With the pins rewritten, as an adopting PR would do, the gate passes at both.

## Not done / follow-ups

- The 14 surviving finding sites listed above have no isolating arm. Five belong to rules this PR added: `:374`, `:376`, `:420`, `:430` and `:528`. No claim depends on them. Arms would be a test extension beyond this round's findings.
- R739-2 S-1 (coincident figures are reported as copies): not taken. It errs on the safe side.
- R739-2 S-2: claim side done (the page says the unit comes from the Meaning cell). Deriving the unit from the name suffix would be a gate feature.
- R739-2 S-3, unitless constants: stated as a limit, enforced by review.
- R739-2 S-4 = R740-2 S1: claim side done. Checking the Sync-seeded image would be a gate feature.
- R739-2 S-5 (`VERILATOR ?=` in the Makefile): a build change, outside this docs lane.
- Engine mutation arm and `make ooc`: not run.
- The parent bump must re-pin the parent gPTP docs and the submodule-docs page and diagram.

## Postings on #96

- TAKEN: issuecomment-6521397706
- REVIEW READY with head `411b35fcc56d11c2361d861e7205307587a04a1d`: issuecomment-6521611261
