# [A818] round 2 handoff: #584 / PR #975, correction round

Status: REVIEW READY at `64d539f12532b2591f734b8e756f8a9358bb742c` (resumed 2026-11-22 19:47 CET after the host
restart: nothing of this lane was running, and the round-1 head `2b295a44` was intact and clean; updated 21:40). Five
local commits on `2b295a44`, not pushed. Every R894-1 and R893-1 finding is answered. REVIEW READY posted once on #584, issuecomment-7085448602 (`receipts/public/review-ready-r2.md`); no other comment was posted, edited or deleted. F1 is stated as pending the
owner's disposition, which is not yet posted on #584; if it requires loopback-backed input clusters, that is round 3.

Answering R894-1 (F1 MAJOR, F2 MAJOR, F3-F5 MINOR) and R893-1 (F1-F3 MINOR, R1-R4 residue).

| Finding | Plan | State |
|---|---|---|
| R894-F1 / R893-F1 backing deviation | stated as pending owner disposition: PR body, D8, D10, the ownership page's #584 section, the changelog | done `25ad9c9a` |
| R894-F2 / R893-F2 no shipping mapping-to-wire proof | new `milan_dp_render` case `ship8` (124 checks) and `ship8-mutants` (4 plants caught, 1 refusal), a fourth CI piece | done `e2a0858c`, `3a94bc3d`, `3c33027a` |
| R894-F3 / R893-F3 uniform growth claim | per-image deltas; the breakdown that did not add up dropped | done `25ad9c9a` |
| R894-F4 stale waiver text | L1, row 45, the 32x32 census prose (a checked figure) | done `25ad9c9a` |
| R894-F5 receipt index | the three normalized receipts hold the published bytes; index regenerated, 80/80 rows match `4ee921e6` | done (output directory) |
| R893 R1-R3 | wording; R4 left (it would change every config's `build_plan.md`) | done `25ad9c9a` |

## Commits (on `2b295a44`)

| Commit | What |
|---|---|
| `e2a0858c` | `sim_ship8_render.cpp`, `ship8_params.py`, `ship8_mutants.py`, the `ship8` case and `ship8-mutants` target, the evidence-reader disposition, the fourth CI piece, TESTING.md rows |
| `3a94bc3d` | the piece figure from the cold four-CPU CI-driver run |
| `25ad9c9a` | F1 (D8, D10, ownership page, changelog), F3, F4, R1-R3 |
| `3c33027a` | `suite_shards.py` back to its 1000-line ratchet (the provenance moved to TESTING.md), a changelog sentence, the regenerated documentation audit |
| `64d539f1` | the leg names every passing check |

## Gate table

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| 8x8 render leg | `make -C tb/verilator/milan_dp_render ship8` | `64d539f1` | 124 checks, 0 failures, every check named | `rtl/ship8-64d539f1.log` |
| Its planted faults | `make ... ship8-mutants` | `64d539f1` | 6 checks: 6 PASS (clean leg; projection x2, adapter, bus binding caught; the BUS_SLOTS_P mis-tie refused at elaboration) | `rtl/ship8-mutants-64d539f1.txt` |
| CI case driver, cold | `ci_make_cases.py --suite milan_dp_render --shard 3/4`, 4 CPUs | `e2a0858c` | PASS, 147.9 s (the piece figure's basis) | `rtl/ship8-ci-driver-e2a0858c.txt` |
| Render suite | `make -C tb/verilator/milan_dp_render` | `25ad9c9a` | PASS: ship 263, multi 79, ship8 124 checks; 5 of 5 leg-side defect arms; then the plants 6/6 | `rtl/milan_dp_render-suite-25ad9c9a.txt`, `rtl/ship8-25ad9c9a.log`, `rtl/ship8-mutants-25ad9c9a.txt` |
| Builder suite, two CI legs and union | `ci_builder_legs.py run 0`, `run 1`, `union --workflow elaborate` | `25ad9c9a` | ALL GATES PASS EXCEPT 1 NOT RUN each (gate 1b's make arm; gate 11's bench-local report); 113 gates exactly once, rc 0 | `gates/builder-leg*-25ad9c9a.*`, `gates/builder-legs-union-25ad9c9a.txt` |
| Builder outputs, five configs | the builder at `2b295a44` and at the working tree | `25ad9c9a` | byte-identical (`diff -r`) | - |
| Twin | `make -C tb/verilator/milan_dp twin` | `25ad9c9a` | 0 findings; the four documented observed differences | `gates/twin-ledger-25ad9c9a.txt` |
| Ledger | `test_ctrl_memory.py`, `plat_ledger.py` | `25ad9c9a` | PASS, PASS | `gates/twin-ledger-25ad9c9a.txt` |
| Docs workflow, 103 commands | `quick.sh docswf.tsv` | `64d539f1` | 99 pass; the 4 hosted-environment rows as at the base; tree clean | `docs/docswf-64d539f1.txt` |
| Scheduler and CI self-tests | `suite_shards.py --selftest`, `ci_suite_pieces_selftest`, `ci_suite_collect_selftest`, `ci_make_cases_selftest`, `ci_case_receipts_selftest` | `3c33027a` | PASS | (docs workflow rows 83-97 at `64d539f1`) |
| F5 index | the round-1 index against the blobs at `4ee921e6` | - | 80 of 80 rows match | `f5/index-check.md`, `f5/round1-INDEX-corrected.md` |

`25ad9c9a`..`64d539f1` changes the changelog, the documentation audit, TESTING.md, one comment line in
`suite_shards.py` and the leg's pass echo, which none of the runs at `25ad9c9a` read. Round 2 changes no RTL,
firmware or entity model, so round 1's route, firmware bank, saved-state and budget evidence carry, and no re-route ran.

## Open questions

1. F1: the owner's disposition of the 8x8's backing (no loopback-backed input cluster, the lane off, TDM32 slot 0 for
   the first TDM8 channel). Not posted on #584 at 21:40.
2. The `ship8` CI piece's 240 s is a scaled local run; its hosted window is owed.
3. R893 R4 (the generated build plan's name list) is left: it would change every configuration's `build_plan.md`.

REVIEW READY 64d539f12532b2591f734b8e756f8a9358bb742c
