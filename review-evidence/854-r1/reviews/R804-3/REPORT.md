[R804] POSITIVE - exact head a853461dd57f8e493ca079e0faa1f07229c3cb16

# External independent review R804-3: issue #854 / PR #862 (round 3 delta)

- **Head:** `a853461dd57f8e493ca079e0faa1f07229c3cb16`, tree `d1801ae25340d9c083458e1799c4f4db986111aa`. The remote branch tip equals it at review time (`receipts/hosted_checks.txt`, last line).
- **Source base:** `dev` `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36`, the live `dev` tip.
- **Delta judged:** `de71984e..a853461d`, two commits (`8d6b623b`, `a853461d`). It is judged against the round 3 ruling (issuecomment-6743871886) and the author's REVIEW READY (round 3, issuecomment-6745967653).
- **Already accepted:** the ruling accepted round 2 as built. That covers record 16, the same-directive comparison, the runt and oversize legs with their mutants, and the comment-only RTL.

## Verdict basis

**POSITIVE.** This round has no BLOCKER, MAJOR, MINOR or RESIDUE finding, and no new SUGGESTION.

- **Prior findings.** My three open round 2 items (R804-2-F1, R804-2-S1, R804-2-R1) are resolved at this head. The internal reviewer's R803-2-F1 is resolved. Its R803-2-S1 (= R804-2-S2) was carried by the ruling to the residue checklist #495, and the PR body names it there.
- **Scope.** The delta is text only: two documentation pages and two docstrings in a test driver. It contains no route, record, JSON, RTL, submodule or gitlink change (`receipts/delta_scope.txt`).
- **Gates.** Every gate the ruling's "done means" names passes when I run it at the head. That includes the em-dash gate, which round 2 could not run.

## Ruling items, judged at the head

### Item 1: the FF attribution (R803-2-F1 = R804-2-F1)

**Met at every place that attributes the figure.**

Each new figure was checked against the published route and standalone hierarchy reports. Their hashes match the evidence packet's manifest (`receipts/evidence_fetch_verify.txt`). The parsed figures are in `receipts/hier_attribution.txt` and `receipts/datapath_ff.txt`.

**`docs/findings/234_PP_SHADOW_AREA_BASELINE.md:110-113`.** The old sentence ("the flip-flop figure, +13 at both, is the change's") is gone. The page now says:

- Both figures move with placement.
- The change carries +10 FF. That is 8 for the count, 1 for `last_kept_r` and 1 for the FIFO's overflow register.
- The wrapper is 20,038 FF at all three directives. Checked: eppo, aslh and eto are each (…, 20038).
- The other +3 is in `dma_bridge_write_bridge/aligner`, at 146 FF against 143. Checked: eppo (143 LUT, 146 FF), aslh (145, 143).
- `milan_datapath` is 43,435 FF at all three directives. Checked: eppo, aslh and eto are each 43,435.
- AltSpreadLogic_high moved from 54,837 to 54,847, which is +10. Checked:
  - record 15's AltSpreadLogic_high row is 54,837 at `ac0a01e3:docs/findings/234_PP_SHADOW_AREA_BASELINE.md:81`;
  - the head's route is 54,847 in `author-r2/receipts/area/route-figures.md`.
- The routes came "from the same synthesis checkpoint". This is supported by:
  - `author-r2/receipts/area/runs/runs.md`, where only the ExtraPostPlacementOpt run is "with synthesis";
  - `syn/ooc/pp_resource_gate.py:25-27,139`, where a route set places each directive from `alinx_ax7101_synth.dcp`.

**`docs/design/AREA_BUDGET.md:256-257`.**
- "The change moved by" now reads "the route moved by".
- A new sentence gives +10 to the change and +3 to replication in the SoC's DMA write bridge, citing the AltSpreadLogic_high +10.

**The sixteenth ledger entry, `AREA_BUDGET.md:697-698`.** Corrected in the same way ("the route moved by"), with the +10 / +3 sentence.

**The PR body, "The change at one directive".** It carries the same correction with the same figures. Its commit table lists `8d6b623b` and `a853461d`.

**Places left at +13 on purpose: judged correct, no finding.** Each states the route's or the image's movement and attributes nothing to the change:
- **`CHANGELOG.md:78`:** "Against #851's route it grows 106 LUTs and 13 FFs". This is the image's growth against the record, and it is true.
- **`syn/ooc/pp_resource_baseline.json`, the route-1x1 `measured` note (line 451):**
  - "the route moved by … +13 FF (+600)" is the gate's own figure against record 15;
  - "this route at ExtraPostPlacementOpt moved by … +13 FF" is a route figure.
  - The ruling forbids a record change in this round.
- **`AREA_BUDGET.md` gate-pass line and the PR tables:** these give "54,850 FFs (+13, tolerance +600)" and the "FF 54,837 / 54,850 / +13" rows. They are measurements, and the attribution follows them.

My `git diff ac0a01e3..HEAD` scan of added lines finds no other "+13" or "13 FF" attribution.

### Item 2: the LUT share (R804-2-S1)

**Met, and it agrees with the hierarchy reports.**

**`234_…:116,124`.** The share is "the change in the wrapper's remainder". The table row is "the wrapper's remainder, the tap's share".

**`234_…:126-128` and `AREA_BUDGET.md:259-261`.** They say:
- The FF share is an exact count, because the remainder equals the own-cell row.
- The LUT share is not a cell count, because LUT totals are not additive at this boundary.

The quoted figures match `receipts/hier_attribution.txt` exactly:

| Figure | eppo | aslh | eto | ooc-1x1 | ooc-8x8 |
|---|---:|---:|---:|---:|---:|
| Own-cell FF row | 332 | 332 | 332 | 340 | 341 |
| Own-cell LUT row | 18 | 18 | 18 | 18 | 17 |
| Total less children, LUT | +1 | 0 | 0 | -5 | -6 |

**PR body.** The same text, with "about +8 LUT (+6 to +8 across the three endpoints)" kept beside the caveat.

### Item 3: the docstrings (R804-2-R1)

**Met with the exact fix.**
- **`tb/verilator/pp_shadow/drops_mutant.py:25-26`:** "Exit 0 = both clean controls passed and every arm was caught by its named check; 1 = otherwise."
- **`:111`:** "The two clean controls, then every arm; 0 when each arm was caught." This is `main()`'s docstring (`:110`), as the PR body says.
- **Rest of the file:** the only changed lines are these two (`receipts/delta_scope.txt`).
- **Comment rule:** the new lines carry no lane label, bench label, round, reviewer ID or comment ID (scan in the same receipt).

### Item 4: hosted `RXFILT=0 --drops-only`

Carried to #495 by the ruling. The PR body's "Known limitations" names it (R803-2-S1, R804-2-S2). Recording it on #495 is the manager's duty (below).

### "No route, record or RTL change"

**Confirmed.** `git diff --stat de71984e..a853461d` lists:
- `docs/design/AREA_BUDGET.md` (+7 -4);
- `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` (+9 -4);
- `tb/verilator/pp_shadow/drops_mutant.py` (+2 -2).

Nothing under `hdl/`, `syn/` or `third_party/` changes, and no gitlink changes. The `AREA_BUDGET.md` policy table that `pp_resource_gate.py` reads is untouched: the hunks are prose at `:256-261` and `:697-698`. `check-baseline` passes.

## Prior public findings at this head

| Finding | Severity then | Status at `a853461d` | Evidence |
|---|---|---|---|
| R804-2-F1, +13 FF credited to the change | MINOR | **RESOLVED** | Item 1 above; `234_…:110-113`, `AREA_BUDGET.md:256-257,697-698`, PR body |
| R803-2-F1, the same sentence | MINOR | **RESOLVED** | As R804-2-F1 |
| R804-2-S1, LUT share is a remainder change | SUGGESTION | **TAKEN** | Item 2 above |
| R804-2-R1, docstrings name one control | RESIDUE | **RESOLVED** (exact fix) | Item 3 above |
| R804-2-S2 = R803-2-S1, hosted `RXFILT=0` grade | SUGGESTION | **CARRIED** to #495 by ruling item 4 | PR body "Known limitations" |

Round 1 findings were resolved or carried at `de71984e` (R804-2's table), and the delta touches none of them.

## Findings

None at BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION.

Wording residue scan:
- I re-read every changed sentence in the two pages and the PR body against the reports.
- The REVIEW READY's cited line ranges (`234_…:110-113,116,124,126-128`; `AREA_BUDGET.md:256-257,259-261,697-698`) point at the changed text.
- No defect found.

## Reviewer-run gates at the exact head

All ran on this clone at `a853461d`, run by `scripts/run_gates.sh`.

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| `make -C tb/verilator/pp_shadow drops-mutant` (as `python3 drops_mutant.py`) | 0 | Both clean controls pass (RXFILT=1, RXFILT=0); 8 of 8 arms KILLED by their named checks; the failing-check counts per arm are 7, 7, 3, 3, 2, 7, 1, 2. Run with the pinned Verilator 5.050 (`VERILATOR` resolves to it; the 5.054 on `PATH` was not used) | `receipts/drops_mutant.log`, `.rc`, `receipts/environment.txt` |
| docs.yml steps reading the changed files: `docs_check.py`, `check_em_dash.py --base ac0a01e3`, `check_doc_style.py` (+`--selftest`), `check_gptp_docs.py`, `DOC_MAP.gen.py --check`, `check_solution_docs.py`, `check_feature_status.py` (+`--self-test`), `gen_module_matrix.py --check`, `measure_test_evidence.py --check`, `check_hygiene.py --check`, `check_py_idiom.py`, `check_doc_paths.py`, `check_archive.py`, `gen_toc.py --verify-anchors` and `--check` | 0 each | `docs_check: 0 finding(s)`; `check_em_dash: 0 finding(s) over 264 added line(s) in 8 changed Markdown page(s)`, run with the pinned renderer from `tools/markdown/requirements.txt` (`--require-hashes`) in a private environment | `receipts/docs_gates.log`, `.rc` |
| `docs_inventory.py --check` | 0 | `documentation inventory: OK (547 lines, docs/DOCUMENTATION_AUDIT.md is fresh)` | `receipts/docs_gates.log` |
| `git diff --check ac0a01e3 HEAD`; `git diff --check de71984e HEAD` | 0; 0 | no output | `receipts/docs_gates.log` |
| `pp_resource_gate.py check-baseline` | 0 | `baseline PASS: 3 endpoints` | `receipts/docs_gates.log` |
| published evidence, fetched files against `MANIFEST.json` at `edebc85d` | 0 | 8 files MATCH, 0 problems | `receipts/evidence_fetch_verify.txt`, `scripts/verify_fetched.py` |
| hierarchy re-derivation | 0 | the figures in items 1 and 2 | `receipts/hier_attribution.txt`, `receipts/datapath_ff.txt`, `scripts/hier_attribution.py`, `scripts/datapath_ff.py`, `scripts/hier_rows.py` |
| restore check | - | `HEAD` and `write-tree` both give `d1801ae2…`; `diff-index`, porcelain status and worktree diff are empty; the five initialised gitlinks are at their recorded commits and clean (`external` is not initialised); only ignored outputs remain (`__pycache__`, `*.hex`) | `receipts/restore_verify.txt` |

## Lens coverage and ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| `Conformance` | CLEAN | Ruling items 1 to 4 against the head: `234_PP_SHADOW_AREA_BASELINE.md:100-133`, `AREA_BUDGET.md:253-262,692-701`, `CHANGELOG.md:78`, the `measured` note at `syn/ooc/pp_resource_baseline.json:451`, the PR #862 body. Figures checked against the published `runs/{eppo,aslh,eto,ooc-1x1,ooc-8x8}/baseline_hierarchy.rpt`, `route-figures.md`, `runs.md` (`receipts/evidence_fetch_verify.txt`, `hier_attribution.txt`, `datapath_ff.txt`) and `ac0a01e3`'s record 15 rows. `check-baseline` at the head. #854 Required items unchanged since R804-2 | R804-3 | `a853461dd57f8e493ca079e0faa1f07229c3cb16` |
| `RTL` | CLEAN | The delta touches no `hdl/`, `syn/`, `third_party/` or gitlink path (`receipts/delta_scope.txt`), so R804-2's coverage stands. That covered `hdl/milan/KL_pp_shadow.sv:70-73,752,857-896` and `hdl/common/csr/milan_csr.sv:699`, comment-only against `e87f2179`, with comments checked against `axis_fifo.v:204,217,275-283` | R804-2 (carried; nothing in scope touched since) | `de71984e4fc1b568065dffec483ea3ff51518604`, an ancestor of the head |
| `Robustness` | CLEAN | The delta touches no `sim_main.cpp`, `Makefile`, `drops_probes.vlt` or RTL (`receipts/delta_scope.txt`). R804-2's coverage of the `[DR]` runt, oversize and saturation grades and its `RXFILT=0` probe stands. The hosted `RXFILT=0` run and reset during a burst are carried to #495 by rulings (SUGGESTIONs, not open findings) | R804-2 (carried; nothing in scope touched since) | `de71984e4fc1b568065dffec483ea3ff51518604`, an ancestor of the head |
| `Tests` | CLEAN | `tb/verilator/pp_shadow/drops_mutant.py` at the head: the docstring delta (`:25-26,111`) checked against `main()`'s two controls. `drops-mutant` re-run at the head: both controls pass, 8 of 8 KILLED (`receipts/drops_mutant.log`). `check_py_idiom.py`, `measure_test_evidence.py --check` and `check_hygiene.py --check` rc 0 | R804-3 | `a853461dd57f8e493ca079e0faa1f07229c3cb16` |
| `Docs` | CLEAN | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:100-133`, `docs/design/AREA_BUDGET.md:253-262,692-701`, `CHANGELOG.md:70-84`, `drops_mutant.py` docstrings, the PR #862 body (status, commit table, area section, limitations), the REVIEW READY line references. The docs.yml subset, `docs_inventory --check`, `git diff --check` and the em-dash gate, all rc 0 (`receipts/docs_gates.log`) | R804-3 | `a853461dd57f8e493ca079e0faa1f07229c3cb16` |

## Real limits

- **Area.** I did not run Vivado. The figures are the author's published runs, checked through the manifest hashes. The evidence commit `edebc85d` is not cryptographically signed, so its integrity rests on matching hashes.
- **The +3 against record 15's own ExtraPostPlacementOpt route.** Record 15's hierarchy report is not published. So the attribution of that +3 is inferred, not read from record 15 directly. It rests on two facts:
  - the head's same-checkpoint ExtraPostPlacementOpt and AltSpreadLogic_high routes differ by exactly 3 FF in the aligner, with `milan_datapath` constant;
  - record 15's ExtraPostPlacementOpt and AltSpreadLogic_high totals are equal (54,837).

  The ruling accepted this framing, and the text states its basis.
- **docs.yml.** I ran the steps that read the changed files, not all 65. The author reports all 65 run, 0 bad, in the round 3 REVIEW READY.
- **Not re-run, per the ruling:** the `pp_shadow` suite, since no input of it moved. I also did not re-run the resource gate's self-test and mutants.
- **Hosted runs.** At `a853461d`: 70 check runs completed successfully and 1 was skipped ("Physical gPTP (nightly and manual)") (`receipts/hosted_checks.txt`). I make no claim about hosted acceptance or act acceptance; both belong to the manager.
- **Hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Manager bank.** No manager source bank ran at this head, and none is claimed.

## Pending manager duties

- Record the hosted `RXFILT=0 --drops-only` run (ruling item 4) and reset during an overflow burst on the residue checklist #495.
- Own hosted and act acceptance at the exact head.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts.
- Obtain explicit maintainer authorization before any merge.

R804-3 FINISHED
