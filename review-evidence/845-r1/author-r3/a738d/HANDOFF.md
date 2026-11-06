# HANDOFF: milan-fpga issue #845, round 3, [A738d]

Status: **REVIEW READY posted.** All four items of the [A10] round 3 ruling are done. Nothing pushed by this session; the manager pushes.

- Repository: milan-fpga, origin https://github.com/kebag-logic/milan-fpga.git, branch `845-adopt-pp-92100657`.
- Base of the round: `bf6c5a67778a5e5d479ae51b3b4377ad4f763801`. No rebase, no force.
- Head: `853ca25ae00fe26b09e019fbfe70893666617fc1`, three commits on top, one-line subjects, no body, no trailers.
- dev: `87e9d03aa2a4797957ac0124d0c7851a2eec234c`, also the merge base. It had not moved at the last fetch.
- Assignment: the [A10] round 3 ruling on #845; the maintainer decision issuecomment-6689114981.

## The result the manager needs

| Endpoint | Measured at | Exit, twelfth record | Figures, delta | Exit, new record |
|---|---|---:|---|---:|
| `route-1x1`, ExtraTimingOpt selected | `b16f0175` | 1 | 52,529 LUT (+517 of +500), 54,582 FF (+875 of +600), 15,835 slices (+55 of +80), WNS +0.373, WHS +0.012 | 0 |
| `ooc-1x1` | `b16f0175` | 1 | 24,996 LUT (+650 of +250), 20,934 FF (+530 of +250) | 0 |
| `ooc-8x8`, not routed | `bf6c5a67` | 1 | 36,864 LUT (+2,708 of +316), 32,036 FF (+2,254 of +339) | 0 |

`check-baseline` exits 0. No tolerance, floor or ceiling moved: a script compared the two JSON files, and only `record` and `measured` differ. The record's only identity change is `place_design -directive ExtraTimingOpt`.

## Three things to read before merging

1. **The `ooc-8x8` growth is much the largest, and the decision's words name the shipping image.** It is nearly all the SRP listener, +2,279 LUT and +2,239 FF. 8x8 is not the shipping image. The ruling's item 3 orders all three endpoints re-baselined, so I recorded it; the wording gap is yours to judge.
2. **A re-export does not reproduce the record's `inputs_sha256`.** See "New finding" below. It changes no result here, but I had expected the digests to match and they did not.
3. **Route and `ooc-1x1` reuse round 2's measurement directories** at `b16f0175`; they were not re-measured. `git diff b16f0175 bf6c5a67` over `hdl syn sw configs protocol-processor gptp-processor third_party` is empty, and the inputs equal the head's export with comments removed.

## New finding, not fixed: for a new Issue

`pp_resource_gate.py inputs()` strips `//` comments from the generated top but not its `/* */` module-tree block, and LiteX writes that tree in a different order between exports. Two exports of `853ca25a`, both with `PYTHONHASHSEED=0`, differ in 18 lines, and equal each other with comments removed. So at the head all three gate digests differ from the record, and with block comments removed all three are equal to the measured exports (`receipts/gate/digest-at-head.txt`).

Impact: the "identical inputs with different figures" refusal can miss a real case, because equal designs can digest differently. `check` is unaffected here: it reads each measurement's own export. The earlier claim that a digest "reproduces" may have been luck. I filed nothing, because this session may post only on #845; the PR body lists it as a limitation.

## Changes

| Item | File:line | Change | Basis |
|---|---|---|---|
| 3 | `syn/ooc/pp_resource_baseline.json` | three records through `record --write`; `measured` notes at :451, :919, :1377 by `scripts/set_measured.py`, since the gate leaves them | ruling item 3; `PP_SHADOW_BASELINE_RECIPE.md` Resource gate |
| 1 | `docs/design/AREA_BUDGET.md:163-169` | the decision replaces "pending"; figures, three directives and 15 slices kept; `ooc-8x8` added at :182 | ruling item 1 |
| 3 | `docs/design/AREA_BUDGET.md:13`, `:123-127`, `:142-152`, `:187-192`, `:204-216`, `:467`, `:602-607` | the record's table and figures, critical path, record history, the thirteenth entry | follows the re-baseline |
| 1 | `docs/reference/SUBMODULES.md:587-615` | the decision, the `ooc-8x8` row, `check` exits 0; 15 slices kept at :629 | ruling item 1 |
| 1 | `CHANGELOG.md:92-96` | the decision, re-recorded | ruling item 1 |
| 3 | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:46-152`, `:13-17`, `:24` | the thirteenth record's section, intro and contents | precedent `ca39dc1b` |
| 3 | `docs/design/MARK_II_AREA_PLAN.md:59`, `:937-938`; `docs/findings/README.md:25` | the current record's anchor | precedent `ca39dc1b` |
| - | `docs/DOCUMENTATION_AUDIT.md` | `python3 scripts/docs_inventory.py --write` | generator |
| 4 | `PR-BODY.md` | Status, Round 3, Definition of Done, each result's measured head; `Closes #845` stays | ruling item 4 |

The ruling names three pages for item 1. The four other pages changed because each states "the current record", which the re-baseline makes false.

No clause text changed this round and no new check was added, so there is no planted mutant to report: the change is a budget record and its documentation.

## Gates, at `853ca25ae00fe26b09e019fbfe70893666617fc1` on clean clones

| Gate | Result | Receipt |
|---|---|---|
| `pp_resource_gate.py check` route-1x1, route set | rc 0, RESULT: PASS | `receipts/gate/after-route-1x1.log`, `.rc` |
| `pp_resource_gate.py check` ooc-1x1 | rc 0, RESULT: PASS | `receipts/gate/after-ooc-1x1.log`, `.rc` |
| `pp_resource_gate.py check` ooc-8x8 | rc 0, RESULT: PASS | `receipts/gate/after-ooc-8x8.log`, `.rc` |
| `pp_resource_gate.py check-baseline` | rc 0, 3 endpoints | `receipts/gates/check-baseline.log` |
| `pp_resource_gate.py --selftest`, not required | rc 0 | `receipts/gates/gate-selftest.log` |
| every `run:` step of `.github/workflows/docs.yml` | verifier rc 0: 72 ran rc 0, 24 not run with a reason, 0 bad; 8 job trees clean | `receipts/docsyml/docs-yml-table.md` |
| `docs_inventory.py --check` | rc 0 | `receipts/gates/docs-inventory-check.log` |
| `git diff --check 87e9d03a HEAD` | rc 0 | `receipts/gates/git-diff-check.log` |
| privacy check | rc 0, 0 private lines | `receipts/gates/privacy-check.log` |
| `check_submodule_docs.py`, not required | rc 0 | `receipts/gates/check-submodule-docs.log` |

Before the re-baseline, against the twelfth record: `receipts/gate/before-*.log`, each rc 1. `check` on the 1x1 endpoints reads round 2's measurement directories, and on `ooc-8x8` this round's.

Vivado, through `vivado-slot.sh`, one run at a time, each scope capped at 14 GB: RTL elaboration rc 0, 74 s; `ooc-8x8` rc 0, 1,969 s, peak 6,433 MB. 8x8 was not routed. All 18 memory-image entries rehashed and match; no `[Synth 8-4445]` diagnostic in any log.

## Not taken, for the manager

- R786-R1 ("Recipe" wording) and the processor `integrator.md` sentence: left alone; the ruling sends both to #495.
- The new finding above needs an Issue.
- Merge order is the ruling's: this PR first, then #846 syncs, routes and re-baselines on it.

## Judgement calls to check

- I ticked "Required local verification bar passes", as the ruling's item 4 asks for that box. The box says the sweep, firmware self-test, builder and behave are at `519d9c2b`, not the head.
- Status reads GREEN for re-review. It describes this lane's evidence only; hosted checks and both reviews are not mine to claim, and those boxes stay unticked.
- "Mark II recovers the area" stays beside the decision. That is the budget's existing plan, not something the decision says, so I kept it in its own clause.

## Limits

- No sweep, firmware self-test, builder or behave ran after `519d9c2b`, as assigned.
- `ooc-8x8` is measured at `bf6c5a67`, not at the final head. The later commits touch only the baseline JSON and documentation.
- The deltas run from the `f65c8ff7` records, so they include dev's movement and, on the route, a change of directive. No standalone figure exists at dev's pin `a9e84b66`, so this adoption's share of the standalone growth is not measured.
- Nothing here measures the integrated image with every lab fix, and nothing is hardware proof. No bench access happened.
- Measurement directories stay in lane scratch and can be removed; `large.sha256` files record what is not copied. `check` needs them, and round 2's are under the `845-a738c` scratch.
- Scripts are in `scripts/`; `receipts/INDEX.md` is generated from the files present.
