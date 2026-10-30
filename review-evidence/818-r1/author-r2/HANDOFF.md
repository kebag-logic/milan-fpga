# [A710b] #818 round 2 handoff

Lane `818-wns-gate`, base head `32f0d9b5` (PR #820), round-2 head `50e5d08dda6e89cf010a740cea5cf4539807db01` (two commits on top; nothing pushed). Origin `https://github.com/kebag-logic/milan-fpga.git`; dev `1e80128f` is still the remote tip.
Scope: the [A10] round-2 comment on #818; R748-1 F1, F2, F3, R1, S1. TAKEN: issuecomment-6530808744.

## Status

REVIEW READY at `50e5d08dda6e89cf010a740cea5cf4539807db01` (posted: issuecomment-6531847255); every gate below rc 0. Nothing pushed; remote `818-wns-gate` is still `32f0d9b5`, remote dev `1e80128f`.

## Commits

- `fda977a374` Print the fall WARNING beside a floor failure, and arm the corner-agreement guard against a timing summary below every signoff corner and the BRAM tile ceiling against a route not selected, each with killed mutants (#818)
- `50e5d08dda` Mark the Mark II mapping record as the shipping selection and state the fall WARNING beside a floor failure in the area budget and the recipe (#818)

## Changes (file:line, reason)

- `syn/ooc/pp_resource_gate.py:572-578` (`verdict_for`): F2. The floor REGRESSION and the fall WARNING are collected as notes and joined with `; `; the figure fails only on a floor miss (`not missed`). Before, the floor branch returned first and the fall was never published beside a failure.
- `syn/ooc/pp_resource_gate.py:537` (`judge`): F2. A figure is counted for the WARNING summary line when its verdict holds `WARNING: fell`, not only when it starts with WARNING.
- `syn/ooc/pp_resource_gate_set_selftest.py:73-79, 95-99`: F2 arms (below).
- `syn/ooc/pp_resource_gate_set_selftest.py:106-109`: F3 arms (below). The guard `if worst != figures[figure]` (`pp_resource_gate.py:401`) was already two-way; no gate change.
- `syn/ooc/pp_resource_gate_set_selftest.py:156-160`: S1 ceiling arms.
- `syn/ooc/pp_resource_gate_mutants.py:31, 306-311, 318-321, 370-375`: rewritten `timing floor`, `floor names its corners`, `a fall never fails` to the new spans; six new mutants.
- `docs/design/MARK_II_AREA_PLAN.md:1340-1347`: F1. The record line takes `--shipping-selection`, with the reason: the map reads one routed checkpoint, so the record is of that one route.
- `docs/design/AREA_BUDGET.md:442`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:588`: F2. The WARNING prints also beside a floor failure (the recipe's "still passes" was wrong beside a floor miss). `docs/integration/BUILDING.md:578` already states it without condition and is unchanged.
- R1: `PR-BODY.md` Status bullet 2 is exact (receipts `mutant-words-pr.tsv`, `mutant-delta-dev.json`).

## New checks, planted mutant, failing words

From `receipts/mutant-words.tsv` (round-2 run of each mutant alone):

| Arm | Mutant killed | Failing words |
|---|---|---|
| `WNS below the floor and fell more than the timing fall: both reported` (exit 1, holds `REGRESSION: below the floor 0.03 at Slow_0C, Slow_85C; WARNING: fell by more than 0.25 from the record`, the summary WARNING and MATERIAL REGRESSION) | `fall warned beside a floor miss` (`and not missed`), `fall warning summarized beside a floor miss` (`verdict.startswith("WARNING")`), also `timing fall`, `fall warning summarized` | `route arm 'WNS below the floor and fell more than the timing fall: both reported': exit 1, wanted 1 naming (...)` |
| `WNS below the floor within the timing fall: no warning` (floor 0.3, WNS 0.290: exit 1, lacks WARNING) | guards a warning on any floor miss | - |
| `WHS below the floor and fell more than the timing fall: both reported` / `... within the timing fall: no warning` | the same, for WHS | - |
| `the summary's WNS below every corner's, under the floor` (summary 0.010, corners 0.5: exit 2) | `corners agree in both directions` (`worst < figures[figure]`, R748-1 X5) | `route arm "the summary's WNS below every corner's, under the floor": exit 0, wanted 2 naming "the signoff corners' worst WNS_ns is 0.5 and the timing summary's 0.01: the reports are not of one run"` |
| `the summary's WHS below every corner's, under the floor` (summary -0.050: exit 2) | as above for WHS | - |
| existing `a corner's WNS below the summary's` | `corners agree in the other direction` (`worst > figures[figure]`) | `route arm "a corner's WNS below the summary's": exit 0, wanted 2 ...` |
| `a selected comparison is judged on the BRAM tile ceiling` (exit 1, `REGRESSION: 5.5 exceeds the ceiling 5.0`) | `ceiling judged on the selected route` (R748-1 X17) | `route-set arm 'a selected comparison is judged on the BRAM tile ceiling': exit 0, wanted 1 ...` |
| `a route not selected is not judged on the BRAM tile ceiling` (exit 0, lacks `ceiling`) | `ceiling not judged on a route not selected` (max over every route) | `route-set arm 'a route not selected is not judged on the BRAM tile ceiling': exit 1, wanted 0 ...` |

Rewritten: `timing floor` (`not missed` -> `True`) killed by `WNS below the floor`; `floor names its corners` killed by `WNS below the floor`; `a fall never fails` (`not missed` -> `not notes`) killed by `WNS fell more than the timing fall: a warning, never a failure`.

PR-wide against dev (`receipts/mutant-delta-dev.json`, `receipts/mutant-words-pr.tsv`): 44 added, 9 edits changed, 0 removed; 192 -> 236. All 55 (44 + 9 + `timing fall`, `timing fall boundary`) killed; 54 by a named arm or check, `every corner model read` by the fixture record's Refusal before the arms run.

Not done from S1: X1-X4 (sub-conditions of `bound()`'s shipping-script precondition) stay unarmed; each is redundant with a later check (R748-1's own inspection), so no single removal changes a verdict. Stated in PR-BODY Known limitations.

## Resource and route timing

No RTL change, no Vivado run. Resources and route timing are the recorded #814 routes, unchanged from round 1 (93 report files verified by size and sha256, `receipts/routes-verify.txt`). Head gate on the three recorded sets (`receipts/after/`, path-scrubbed): every log byte-identical to round 1's at `32f0d9b5`:

| Set | Exit | Selected |
|---|---|---|
| dev `1e80128f` | 0 | ExtraPostPlacementOpt, +0.303 ns (AltSpreadLogic_high +0.230, ExtraTimingOpt +0.106) |
| #814 head `8b28ebaf` | 0 | ExtraPostPlacementOpt, +0.128, WARNING for the 0.312 fall |
| #814 control | 0 | AltSpreadLogic_high, +0.342 |

So no recorded verdict changes in round 2. Real-route probes (R748-1's `route_probes.py` at this head, `receipts/route-probes/`): 28 PASS; `best-wns-one-corner.log` now prints `REGRESSION: below the floor 0.03 at Slow_85C; WARNING: fell by more than 0.25 from the record`, the summary WARNING and exit 1. F3 on real routes (`receipts/f3/`): summaries at 0.010 beside the recorded corners exit 2 at head; the one-way mutant passes them (now killed by the campaign).

F1 (`receipts/f1/`): the documented `cp` and `record` lines, extracted from the doc, run with `WORK` holding dev's recorded `ax7101` tree: rc 0, the record names ExtraPostPlacementOpt at 0.303; a check against the scratch record passes; the tracked baseline unchanged. The map step (Vivado) NOT RUN.

## Gates

| Gate | Result | Receipt |
|---|---|---|
| `python3 syn/ooc/pp_resource_gate.py --selftest` | rc 0, 312 arms and 500 generated cases PASS, placement controls PASS | `receipts/gates/selftest.log` |
| `python3 syn/ooc/pp_resource_gate_mutants.py` | rc 0, all 236 mutants fail | `receipts/gates/mutants.log` |
| `python3 syn/ooc/pp_resource_gate.py check-baseline` | rc 0, baseline PASS: 3 endpoints | `receipts/gates/check-baseline.log` |
| `python3 scripts/check_py_idiom.py` | rc 0 | `receipts/gates/py_idiom.log` |
| rtl-fast replica (`changes`, `bdd-conformance`, `yosys-elaboration`) at the head, clean clone whose dev is the remote tip | rc 0, 824 s, every job success; behave 14 features, 495 scenarios, 2,288 steps; its gate step: 312 arms, 236 mutants, baseline PASS | `receipts/rtlfast-50e5d08d/` |
| docs workflow replica at the head, clean clone (GNU Make 4.3, CPython 3.12.3) | rc 0: 44 steps, 0 failed, 2 skipped by rule; builder leg 1 with the LiteX interpreter rc 0; the five markdown gates rc 0 (em-dash, links, contents, cited paths); the no-git `docs_check` and `check_feature_status` rc 0 | `receipts/docs-50e5d08d/` |
| Recorded route sets, head gate | 15 runs, outputs byte-identical to round 1 | `receipts/after/`, `receipts/routes-verify.txt` |
| R748-1 real-route probes at the head | 28 PASS, 0 FAIL | `receipts/route-probes/summary.txt` |
| F1 documented record command | rc 0; re-check rc 0 | `receipts/f1/rc.txt` |
| F3 real-route probe | head rc 2; one-way mutant rc 0 | `receipts/f3/F3.txt` |

## Scripts

`scripts/` holds the runners used: `mutant_words.py` (round-2 mutants with their failing words), `mutant_delta.py`, `verify_routes.py`, `run_routes.sh`, `make_clone.sh`, `rtlfast_run.sh`, `docs_run.sh` and their step drivers (round 1's, scratch paths changed), `gen_index.py`. `receipts/mutant-words-pr.tsv` is round 1's `mutant_words.py` run at this head (all 55 PR mutants). R748-1's `route_probes.py` and `x5_probe.py` were run from the review packet, scratch outside the tree.

## Not run

Vivado (none needed; the map step of the Mark II procedure), hardware, the full sweep (no RTL), act/hosted CI.
