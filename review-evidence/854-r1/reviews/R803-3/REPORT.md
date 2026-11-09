[R803] POSITIVE - exact head a853461dd57f8e493ca079e0faa1f07229c3cb16

Review R803-3 (internal, cleared context) of issue #854 / PR #862, round 3 delta.

- **Head:** `a853461dd57f8e493ca079e0faa1f07229c3cb16`, tree `d1801ae25340d9c083458e1799c4f4db986111aa`. The live PR head equals it (`gh pr view 862`, not draft).
- **Base:** `dev` `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36`, the live `dev` tip.
- **Delta reviewed:** `de71984e..a853461d`, two commits (`8d6b623b`, `a853461d`), under the round 3 ruling (#854 issuecomment-6743871886).

**Verdict: POSITIVE.** I found no BLOCKER, MAJOR, MINOR or RESIDUE in the delta. Both round 2 MINORs (R803-2-F1 = R804-2-F1) are resolved. Ruling items 1 to 3 are met. Every FF and LUT figure the new text cites matches the author's published hierarchy reports and the two baseline records; I re-derived each one with a script (29 of 29 match). Two optional wording SUGGESTIONs follow; they do not affect the verdict.

## Reconstruction (public state only)

- **Authorities read:** AGENTS.md sections 3 and 5 to 8, and CONTRIBUTING.md through AGENTS.md. Then the round 3 ruling, the round 3 TAKEN and REVIEW READY comments on #854, and the review-start comment (PR #862 issuecomment-6746818948).
- **Evidence:** the published packet `review-evidence/854-r1` at `edebc85d`. I downloaded the ten files I relied on and checked each against the packet's `MANIFEST.json` `published_sha256`: 10 of 10 match, none path-redacted (`receipts/evidence-hash-check.txt`). These are:
  - `author-r2/receipts/area/runs/{eppo,aslh,eto,ooc-1x1,ooc-8x8}/baseline_hierarchy.rpt`;
  - `author/receipts/route/baseline_hierarchy.rpt`;
  - `author-r2/receipts/area/route-figures.md`;
  - `author-r2/receipts/area/record/baseline-{dev-ac0a01e3,final}.json`, byte-identical to `syn/ooc/pp_resource_baseline.json` at `ac0a01e3` and at the head;
  - `author-r2/PR-BODY.md`.
- **Prior findings:** I read the round 2 reports (PR #862 issuecomment-6743685710 and issuecomment-6743864788) only after my own pass over the delta.

## Delta scope (no route, record, JSON or RTL change)

`git diff --name-status de71984e..a853461d` (`receipts/delta-name-status.txt`) lists:

- `M docs/design/AREA_BUDGET.md`;
- `M docs/findings/234_PP_SHADOW_AREA_BASELINE.md`;
- `M tb/verilator/pp_shadow/drops_mutant.py`, docstrings only: `:25-26` and `:111`.

Nothing else changed:

- no `hdl/`, `syn/`, record JSON or Makefile change;
- no gitlink change against `ac0a01e3` (`receipts/clone-integrity.txt`);
- no route was re-run.

The second block of `delta-name-status.txt` lists the lane's `hdl/` and `syn/` changes against `ac0a01e3`. They are from rounds 1 and 2, unchanged since `de71984e`, which the ruling accepted as built.

## Ruling items, judged at the head

### Item 1: the +13 FF attribution (R803-2-F1 = R804-2-F1)

The text now says the change carries +10 FF and the other +3 is SoC placement replication. It says so at every place that attributes the figure:

- **`234_PP_SHADOW_AREA_BASELINE.md:110-113`.** Every figure is correct (`receipts/derive-figures.txt`, `receipts/ff-directive-diff.txt`):
  - the wrapper holds 20,038 FF at all three directives;
  - `milan_datapath` holds 43,435 FF at all three;
  - the write bridge's `aligner` holds 146 FF at ExtraPostPlacementOpt and 143 at both other directives.
  - The 3 FF that differ between directives are all in `VexiiRiscvLitex/dma_bridge_write_bridge/aligner`. The FF column of the three routed hierarchy reports differs in no other row: the parent rows move by the same 3, and AltSpreadLogic_high equals ExtraTimingOpt row for row.
  - Record 15 has 54,837 FF at both AltSpreadLogic_high and ExtraPostPlacementOpt (`234_...:208-209`, unchanged from `ac0a01e3:...:81-82`). So AltSpreadLogic_high moves +10 (54,837 to 54,847) and ExtraPostPlacementOpt moves +13: the +3 is ExtraPostPlacementOpt's alone.
  - The +10 matches the RTL: the 8-bit `rx_drops_o` (`KL_pp_shadow.sv:1636-1640`), `last_kept_r` (`:868-873`) and `axis_fifo.v:213` `overflow_reg`, which is now read through `status_overflow` (`KL_pp_shadow.sv:917`).
  - It also matches the gate: the route wrapper FF goes from 20,028 to 20,038, and both standalone wrappers move by +10.
- **`AREA_BUDGET.md:256-257`.** "The route moved by" replaces "the change moved by". The +10/+3 split is given, with the AltSpreadLogic_high +10 as evidence. Correct.
- **`AREA_BUDGET.md:697-698`, the sixteenth ledger entry.** Same correction. Correct. "Of those FFs" is unambiguous, because both preceding figures are +13.
- **The PR body (live, `receipts/pr-body-live.md`), "Of the +13 FF the change carries +10".** Correct, and it adds the one-checkpoint and aligner evidence.
- **Places left at +13 on purpose.** All are route or image figures, not attributions to the change. I accept each one:
  - **`CHANGELOG.md:78`:** "Against #851's route it grows 106 LUTs and 13 FFs." Its subject is the image, and the comparison crosses directives.
  - **`syn/ooc/pp_resource_baseline.json` route `measured` note.** It gives the cross-directive +13 FF as "this change's and the selected directive's", which is true: +10 is the change and +3 is ExtraPostPlacementOpt placement. Its same-directive "+13 FF" is the route's, not the change's. The ruling forbids a JSON change.
  - **`AREA_BUDGET.md:246` and `234_...:92,105`:** the gate's and the table's route figures.

### Item 2: the LUT share is the change in the remainder

- **`234_...:116`, `:124`, `:126-128` and `AREA_BUDGET.md:259-261`.** The text calls the tap's share the change in the wrapper's remainder, not a cell count. It says the FF share is exact and the LUT share is not, and why.
- **Checked against the hierarchy reports** (`receipts/derive-figures.txt`):
  - **Own-cell row:** 18 LUT and 332 FF on all three routes; 18 LUT and 340 FF at `ooc-1x1`; 17 LUT and 341 FF at `ooc-8x8`.
  - **Remainder (total less `ctl_fifo`, `u_nvm` and `u_pp`):** +1, 0 and 0 LUT on the three routes, and -5 and -6 LUT standalone. The FF remainder equals the own-cell row in all five reports.
  - **Change in the remainder from record 15 to record 16, computed from the two records' `scopes`:** +8/+9 on the route, +7/+9 at `ooc-1x1` and +6/+9 at `ooc-8x8`.
- The text matches every figure above.

### Item 3: the `drops_mutant.py` docstrings

`:25-26` and `:111` are R804-2-R1's exact text. They match the driver: `main()` at `:130-135` returns 1 unless both controls (RXFILT=1 and RXFILT=0) pass, and `:162` prints "both clean controls pass". No lane label, review round, reviewer ID or comment ID was added (comment rule).

### Item 4: the hosted `RXFILT=0 --drops-only` run

It goes to #495 by ruling. The PR body names it at its limitations, lines 242-243. This is not a lens defect.

## Prior findings at this head

| Finding | Severity | State at `a853461d` | Evidence |
|---|---|---|---|
| R803-2-F1 (the +13 FF called "the change's") | MINOR | **Resolved** | ruling item 1 above; `234_...:110-113`; `AREA_BUDGET.md:256-257,697-698`; PR body |
| R803-2-S1 (hosted `RXFILT=0` `[DR]`) | SUGGESTION | **Carried** to #495 by ruling item 4, and named in the PR body | PR body lines 242-243 |
| R804-2-F1 (same as R803-2-F1) | MINOR | **Resolved** | as R803-2-F1 |
| R804-2-R1 (docstring wording) | RESIDUE | **Resolved** with the exact text | `drops_mutant.py:25-26,111` |
| R804-2-S1 (LUT share is a remainder change) | SUGGESTION | **Taken** | ruling item 2 above |
| R804-2-S2 (same as R803-2-S1) | SUGGESTION | **Carried** to #495 | as R803-2-S1 |
| Round 1 findings (R803-1-F1 to F4, R804-1-F1, S1, R1, R2) | | Resolved or carried at round 2. The delta does not touch their artifacts. | R803-2 prior-findings table |

## Findings

**No BLOCKER, MAJOR, MINOR or RESIDUE in the delta.**

**R803-3-S1: SUGGESTION, lens `Docs`.** At `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:126`: "332 FFs on every route, 340 at 1x1 and 341 at 8x8".
- **Evidence:** the route is also a 1x1 shape. The two standalone figures are the `ooc-1x1` and `ooc-8x8` endpoints, as the table's column heads at `:118` name them.
- **Impact:** a reader could take "at 1x1" to mean the route. The figures are correct.
- **Optional outcome:** "332 FFs on every route, 340 at `ooc-1x1` and 341 at `ooc-8x8`". The same applies to `:127`'s "-5 and -6 standalone", which is already clear.
- **Verification:** re-read `:126` against `area/runs/ooc-{1x1,8x8}/baseline_hierarchy.rpt` row `(KL_pp_shadow)`.

**R803-3-S2: SUGGESTION, lens `Docs`.** In the PR #862 body, "The tap's own share (...)" paragraph: "The tap's own share is +9 FF, ... and about +8 LUT (+6 to +8 across the three endpoints)."
- **Evidence:** the round 2 bar accepted "about +8 LUT", and the next sentences give the remainder framing. The repository pages now say "a change of +6 or +7 LUTs in the tap's remainder" (`234_...:128`).
- **Impact:** none on a figure or claim. It is a small framing mismatch with ruling item 2 inside one paragraph.
- **Optional outcome:** "The tap's share is +9 FF, the 8-bit count and `last_kept_r`, and a change of +6 to +8 LUT in the wrapper's remainder across the three endpoints."
- **Verification:** re-read the PR body paragraph.

## Executed at the exact head

All of these ran in this clone at `a853461d`. Receipts are under `receipts/`.

- **`make -C tb/verilator/pp_shadow drops-mutant`: rc 0.** Verilator 5.050 rev v5.050 came from the scoped pinned wrapper (`receipts/drops-mutant.verilator-version.txt`), with `VERILATOR_JOBS=16`.
  - Both clean controls passed: `clean control (RXFILT=1)` and `clean control (RXFILT=0)`.
  - All 8 arms were KILLED by their named checks. The failing-check counts were 7, 7, 3, 3, 2, 7, 1 and 2.
  - The final line was `PASS: [DR] catches every arm (8 of 8); both clean controls pass`.
  - The log is `receipts/drops-mutant.log`, with the clone path redacted to `<clone>`.
- **docs.yml gates whose inputs the delta touches:** 22 gates, all rc 0 (`scripts/run_gates.sh`, `receipts/gates/*.log|.rc`). The pinned Markdown renderer came from `tools/markdown/requirements.txt` with `--require-hashes`, installed into a private scratch venv. The gates:
  - `docs_check.py` (0 findings over 214 md files);
  - `check_feature_status.py`;
  - `check_em_dash.py --base ac0a01e3` (0 findings over 264 added lines);
  - `check_doc_style.py` and its `--selftest`;
  - `check_gptp_docs.py`;
  - `check_doc_paths.py`;
  - `check_archive.py`;
  - `gen_toc.py --verify-anchors` (603 links) and `gen_toc.py --check`;
  - **`docs_inventory.py --check`** (`documentation inventory: OK`) and its `--selftest`;
  - `DOC_MAP.gen.py --check`;
  - `gen_module_matrix.py --check`;
  - `check_hygiene.py --check`;
  - `check_py_idiom.py`;
  - `measure_fail_fast.py --check`;
  - `measure_test_evidence.py --check`;
  - `measure_naming.py --check`;
  - `check_todo_ownership.py`;
  - `check_solution_docs.py`;
  - `git diff --check ac0a01e3 HEAD`.
- **docs.yml `docs-check-no-git` equivalent:** `docs_check.py` and `check_feature_status.py` on a `git archive` copy with no `.git`, rc 0 (`receipts/gates/nogit_docs_check.*`).
- **Figure re-derivation:** `scripts/derive_figures.py`, rc 0, 29 of 29 OK (`receipts/derive-figures.txt`).
- **Directive FF diff:** `scripts/ff_directive_diff.sh`; the output is `receipts/ff-directive-diff.txt`.

**Not run:**
- the builder legs, RV32 SDK, sv2v, HDL reference build and `act_ci` selftest steps of docs.yml (shared installs or banks, which this review is not allowed to run);
- the `pp_shadow` suite;
- the resource gate's `check`, `check-baseline`, selftest and mutants.

The delta changes none of their inputs: its `AREA_BUDGET.md` hunks, at `@@ -253` and `@@ -692`, are prose under the sixteenth record and leave the policy and record tables alone. I relied on the author's published round 3 receipts for those, and did not re-execute them.

**Hosted checks at the exact head**, inspected and not accepted (`receipts/hosted-checks-snapshot.txt`):
- 50 completed/success, including `rtl-fast`, `docs-gates-0/1/2`, `docs-check` and `docs-check-no-git`;
- 10 in progress (nine Verilator shards and fail-fast);
- 1 skipped context: `Physical gPTP (nightly and manual)`, which is not hardware proof.

**Clone integrity** (`receipts/clone-integrity.txt`), checked after the runs:
- Generated build products (two hex files and one cache directory) were removed. No untracked or ignored entries remain.
- The worktree and index are clean.
- The index modes, blobs and paths equal the HEAD tree (1,480 entries).
- The six gitlinks are at their recorded commits, unchanged against `ac0a01e3`.

## Reviewer-owned completion ledger (R803-3)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling items 1 to 4 judged above. The delta's area claims checked against the published record 15 and 16 JSON (`scopes`, `figures`) and the five hierarchy reports (`receipts/derive-figures.txt`). #854's Required items are unchanged since `de71984e` (no `hdl/`, `syn/` or test-logic change). | R803-3 | a853461dd57f8e493ca079e0faa1f07229c3cb16 |
| RTL | CLEAN | The delta has no `hdl/`, `syn/` or gitlink change (`receipts/delta-name-status.txt`, `receipts/clone-integrity.txt`). The text's FF attribution checked against `KL_pp_shadow.sv:868-876,917,1636-1640` and `axis_fifo.v:213,256`. The SoC placement attribution checked against the routed hierarchy, where the FF column differs only in `dma_bridge_write_bridge/aligner` (`receipts/ff-directive-diff.txt`). | R803-3 | a853461dd57f8e493ca079e0faa1f07229c3cb16 |
| Robustness | CLEAN | `drops_mutant.py:130-135`: either failing control returns 1, so the docstring claim is enforced. Executed `drops-mutant` controls at RXFILT=1 and RXFILT=0, including the runt and oversize arms (`counts-runts`, `misses-oversize`) (`receipts/drops-mutant.log`). The RTL behaviour is unchanged since R803-2. Reset during a burst is carried to #495 by ruling. | R803-3 | a853461dd57f8e493ca079e0faa1f07229c3cb16 |
| Tests | CLEAN | `drops_mutant.py:4-27,110-163` (the docstrings against the code). `make drops-mutant` rc 0: 8 of 8 KILLED and both controls pass. `check_py_idiom.py`, `measure_test_evidence.py --check` and `measure_fail_fast.py --check` rc 0. | R803-3 | a853461dd57f8e493ca079e0faa1f07229c3cb16 |
| Docs | CLEAN (S1 and S2 are SUGGESTIONs) | `234_PP_SHADOW_AREA_BASELINE.md:80-132`, `AREA_BUDGET.md:246-262,692-701`, `CHANGELOG.md:70-84`, the record JSON `measured` notes, the live PR #862 body (`receipts/pr-body-live.md`), the comment-rule scan of the `drops_mutant.py` delta, the 22 docs.yml gates and the no-git docs gate (`receipts/gates/`). | R803-3 | a853461dd57f8e493ca079e0faa1f07229c3cb16 |

All five lenses were applied at this head. Each covering head is the merge candidate source head.

## Real limits

- I ran no Vivado, Yosys or out-of-context build. The area judgement rests on the author's published round 2 hierarchy reports, which I hash-verified against the packet manifest, and on the repository's records.
- I ran no full parent, PP, gPTP, builder or complete docs.yml bank, and not the `pp_shadow` suite or the resource gate. Their inputs are unchanged in this delta.
- Record 15's own ExtraPostPlacementOpt hierarchy report is not published. The +3 attribution therefore rests on two facts. First, record 15's two directives have equal FF totals (54,837). Second, this record's three directives differ only in the write aligner. That is sufficient for the claim as worded.
- **Not simulated:** reset during an overflow burst (#495), and hardware. Physical calibration NOT RUN. Field skips are not hardware proof.
- No manager source bank runs at this head, and I infer none.

## Pending manager duties

- **Optional wording:** carry S1 and S2 if wanted. Neither is RESIDUE or a lens defect.
- **#495:** keep the hosted `RXFILT=0 --drops-only` run and reset during an overflow burst on #495.
- **Hosted acceptance at the exact head:** the Verilator shards and fail-fast were still in progress at my snapshot.
- **Merge-candidate validation at the merge turn:** validate the current-dev candidate (builder and native banks) against the live `dev` of that time, and run the act replica.
- **External review:** the external review at this head.
- **Merge:** maintainer authorization for the merge.

R803-3 FINISHED
