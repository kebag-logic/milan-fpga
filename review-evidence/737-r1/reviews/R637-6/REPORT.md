[R637] POSITIVE - exact head 47fd0d3c510000e9412a1613a723b61d4ef2ae4a

External independent delta review R637-6, issue #737 / PR #739. Exact tree: `771055d82f5b90249c2610a6a20f1be36b15bf56`. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains in the reviewed delta. This is a source-head review, not acceptance of the future merge candidate or completion of hosted/act acceptance.

## Scope and independent evidence

Reviewed the five commits in `e3d25d964b5bbf0187290d0a357c6a6e4c5afd17..47fd0d3c510000e9412a1613a723b61d4ef2ae4a`, in the context of `fa7347fc59173f90e4feec2df207692e6e6e72ec..47fd0d3c510000e9412a1613a723b61d4ef2ae4a`. The full-range inventory includes previously merged dev changes; these are not new round-six product changes. The round-six delta contains eleven paths, no product HDL, firmware, driver assertions, dependency gitlinks or runner changes.

Authority: repository operating contract, CONTRIBUTING, docs index, issue acceptance and public scope decisions, REQ-VER-01 through REQ-VER-04, CI_WORKFLOWS and CI_SIGNATURE. In particular, [round-six assignment 6187562969](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6187562969), [driver ruling 6160937413](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160937413), and [builder/union ruling 6181778634](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6181778634) govern this change. [Fixes-only ruling 6169768594](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6169768594) leaves image adoption, authenticated build acceptance and RTL-trigger changes to follow-up work.

The delta was independently examined before reconciling prior public findings. No private author handoff or scratchpad, management source bank, or current-round peer report was used. The cited public execution packet is [26dd882d, review-evidence/737-r1](https://github.com/kebag-logic/milan-fpga/tree/26dd882d2011d55693da7791a89670ec9d517bd3/review-evidence/737-r1); selected `author-r6` JSON receipts were checked against its `MANIFEST.json` published hashes.

Authentication limit: that packet has no signature/key artifact, and its commit reports `verified=false`, `reason=unsigned`. I verified published SHA-256 bindings, not a cryptographic signature. `receipts/packet-authentication.json` records this distinction. The current scoped implementation deliberately does not claim authenticated hosted/local equality.

## Assignment checks

### Builder partition and union

`ci_gate_workflows.py:68,110,119,128` derives the step inventory from the unchanged templates and preserves the docs preparation line. `.github/workflows/docs.yml:591,738` places builder leg 0 on `docs-gates-1` and leg 1 on `docs-gates-2`. Driver inventory inspection gives 103 gates: `test_baremetal_profile_contract` alone, then the remaining 102 in original order. The builder driver itself is byte-identical to round five.

`ci_builder_legs.py:66,142,190` and `ci_gate_receipts.py:63,120,165` take requirements from the template command. Docs carries only `--require-rv32`; elaboration carries both requirements. Every leg must carry exactly that command's flags, including the leg with no RV32 owner. Missing, duplicate, reordered, failed, wrong-head and wrong-inventory evidence is refused. Elaboration's ledger is judged only when that command requires it; docs retains legitimate NOT RUN rows instead of silently acquiring a stronger command. Missing builder receipts fail the actual aggregate verifier.

The exact-head author receipt `round6-final-validation.json` reports passing docs leg 0, leg 1 and an unsharded docs reference; its production comparison reports equal per-gate verdicts and equal NOT RUN ledger. The union binds the exact reviewed head/tree and digest `47dc3c6ac362ed2038a1ff6391ef54334cc0edb665870a0e5d3980ec3216988f`. Its two NOT RUN entries are the ineffective MAKEFLAGS control on that make implementation and physical utilization calibration without its report. Neither is hardware proof.

`round6-docs-controls.json` records two real planted controls at ancestor `26838a11`: the boot-contract plant fails the unsharded run and leg 0 while leg 1 passes; the FPU-refusal plant fails the unsharded run and leg 1 while leg 0 passes. A successful leg run without `--require-rv32` is rejected by the production aggregate, naming `test_baremetal_profile_contract`. Subsequent changes from that ancestor are documentation and a wording comment, not builder behavior. `round6-mutations.json` binds six killed implementation mutations to the final head.

The reviewer reran the committed `ci_gate_workflows_selftest.py`. It passes, including per-leg flag equality, docs-only requirements, missing-leg/gate and NOT RUN controls, mixed-scope refusal, preparation preservation and generated-graph controls. This is recorded in `receipts/pristine-gate-selftest.log`; no builder bank was rerun.

### Timing recomputation

The baseline API receipts independently confirm head `f62602531d415d6c1cae1374a3cc2938faf54049`:

- Docs run 38601263556: job 2682 s; builder 1400 s; contract 37 s; runner contract 102 s.
- Elaboration run 38601263659: job 2447 s; builder 1763 s; simulation aggregate 597 s; retained Verilator setup 2 s.

`audit_evidence.py` recomputes the assigned model from those windows and published local measurements. It independently sums the larger hosted/local value for every docs worker-zero command: 1246.806 s. Setup/post/gaps contribute 59 s, scheduling controls 28.331 s, and evidence allowance 60 s. The upload action is included in setup, not double-counted as a shell command.

The docs scale is `max(1400,1482.211,1443.720)/1443.720`. Measured legs are 1098.130/506.263 s; both exceed their lone-reference gate sums. The elaboration scale is `1763/1433.969`, applied to 1081.009/495.144 s. Full-precision arithmetic, followed by upward whole-second rounding, produces:

| Worker | Projection (s) | Own limit (s) | 60% bound (s) | Margin to bound (s) |
|---|---:|---:|---:|---:|
| docs-gates-0 | 1395 | 2700 | 1620 | 225 |
| docs-gates-1 | 1248 | 2700 | 1620 | 372 |
| docs-gates-2 | 1073 | 2700 | 1620 | 547 |
| elaborate-gates-0 | 1475 | 2700 | 1620 | 145 |
| elaborate-gates-1 | 1353 | 2700 | 1620 | 267 |

Each affected worker uses at most 54.63% of its limit. Adding the documented 270-second downstream allowance yields docs **1665 s / 27.75 min**, margin **135 s**, and elaboration **1745 s / 29.08 min**, margin **55 s**. These match `CI_WORKFLOWS.md:2703-2791` and the PR body. No additional elaboration split is required by this assigned model.

Recomputation through the current selector confirms the unchanged sixteen-worker projections: 1605, 1541, 1572, 1544, 1540, 1539, 1539, 1540, 1541, 1543, 1540, 1539, 1539, 1538, 1538 and 2032 seconds. The first fifteen have a 1620-second bound; the final continuous-history worker has its separately documented 2160-second bound. The explicit continuous-history exception remains above thirty minutes. This review does not turn the docs/elaboration projections into a claim that every actual workflow has met thirty minutes.

The final author bank ran several jobs on one CPU range and reports longer contended execution times. Those are disclosed execution evidence, not substituted for the assignment's round-five timing inputs. The scaling model, cold setup, hosted capacity, watcher tail and narrow elaboration margin still need actual readback. `receipts/evidence-audit.json` retains the arithmetic and each per-step maximum.

### Generator regression and documentation

`ci_gate_workflows_selftest.py:92` now checks the produced matrix, absence of the dedicated `milan_dp` arm, and the aggregate expectation against the generated worker count. It also plants an incorrect arm index, incorrect expectation, and a changed total with stale template text.

The reviewer executed `revert_probe.py`: pristine self-test rc 0; replace `ci_suite_workflows.py` with its `08adb21a` blob; regenerate; freshness rc 0; contract check rc 0; committed self-test **rc 1**, at the leftover dedicated arm assertion. Restored bytes then pass freshness. This directly resolves the demonstrated blind spot, rather than relying on a test that only notices stale generated output. Logs and return codes are in `receipts/revert-probe.json` and its named logs.

`TESTING.md:518`, `RUNNING_TESTS.md:84`, `tb/verilator/milan_dp/README.md:447` and `726_STREAM_COUNTERS.md:177` now describe the sixteen-worker case matrix and union artifacts. Read-only listing confirms 63 default suites, the documented worker-zero command, and `milan_dp_mclk__0` alone on worker 15. Remaining `/5` or `/6` references in these pages are dated measurements or explicitly described generator input, not current hosted commands.

The arm-count sentence correctly records **5,212 at e3d25d96**, and **5,215 after this change** because the second docs builder step adds three generated-graph controls. The current figure is an author-reported exact-head self-test result; the reviewer did not rerun the whole CI-event mutation census. The generator wording and the eight-successful-suites wording use the requested corrections. Historical round-five, round-four and round-three PR paragraphs now say that the coordinating role published their heads.

`scripts/act_ci.py` is byte-identical to `e3d25d96`, SHA-256 `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`. Neither it nor its self-test was executed by this reviewer.

## Prior findings disposition

Earlier clean coverage is carried only where the delta leaves the cause and dependencies intact. `receipts/prior-cause-retention.json` records unchanged prior-cause paths; the modified generator, receipt verifier and their tests were reapplied in this round.

| Prior IDs | Disposition at this head | Cause/evidence |
|---|---|---|
| R637-5-F1; R636-5-F1 | Resolved | Docs builder partition, conservative merged-head calculations and explicit workflow margins above. |
| R637-5-F2; R636-5-S1 | Resolved | Committed graph checks; reviewer generator-revert probe fails. |
| R636-5-F2 | Resolved | Three named test pages corrected; actual read-only suite listings agree. |
| R636-5-R1; R637-5-R2 | Resolved | Generator removes the arm; text names the worker that passed eight suites. |
| R637-5-R1; R636-5-R2; R637-4-R1; R636-4-R1; R636-3-R2 | Resolved | Live PR historical status paragraphs use the supplied publication correction. |
| R637-1-F1 | Remains resolved | Bounded media-NCO child recipe unchanged; current committed child-budget controls pass. |
| R637-1-F2; R636-1-F1/F2/F5; R637-2-F1/F3 | Remain resolved | Watcher, collector, terminal guard and runtime tests unchanged from cleared coverage; current generator preserves their paths. |
| R637-1-F3 | Remains resolved | CI_WORKFLOWS:1530 states neither cache accepts prefix fallback. |
| R636-1-B1; R637-2-F2 | Remain resolved | Inventory preparation check retained; current self-test removes or conditions each preparation and requires refusal. |
| R636-1-B2 | Remains resolved | Fixture identity fix unchanged in ci_case_receipts_selftest.py. |
| R636-1-F3; R636-2-F1 | Remain resolved | Own-limit policy, separate contract worker and separate synthesis tool build retained; docs placement recalculated here. |
| R636-1-F4; R636-2-F2 | Remain resolved within source sizing scope | Compiler/memory bounds, scoped measurements and runner unchanged; complete replay remains manager-owned. |
| R636-1-F6 | Remains resolved | Public round-two comparison provenance is retained; no case-driver changes in this delta. |
| R636-3-F1 | Remains resolved | Shared-deadline collector control unchanged from the cleared round-four fix. |
| R636-3-R1 | Resolved | CI_WORKFLOWS:2389 names Yosys and Verilator builds specifically. |
| R636-1-S1; R636-2-S4 | Resolved | Current mixed-scope refusal control runs and passes. |
| R636-1-S2; R636-2-S2; R636-2-S1 | Remain resolved | Skipped-step and real failed-outcome controls unchanged from cleared coverage. |
| R636-3-S1/S2/S3/S4 | Remain resolved | Conditional-preparation controls pass; non-transient error handling and bounded oracle recipe retained; elaboration span now recomputed. |
| R636-1-S5 | Retained as an execution limit | MAKEFLAGS control's NOT RUN row remains explicit in equal union ledgers; it is not silently counted as a tested arm. |
| R636-1-S3; R636-2-S3; R636-2-S5(a) | Retained for manager/follow-up | Hosted concurrency and cache-conditioned manifest equality remain acceptance/design limits, as public ruling 6176299708 records. |
| R636-2-S5(b) | Remains resolved | Observer-only failure separation retained, with incomplete evidence still refused. |

## Retained optional suggestions

No new blocking finding or wording residue was found. These prior optional items remain visible rather than disappearing from the ledger. They do not make any lens unclean.

- **R636-4-S1; SUGGESTION; Robustness, Docs.** Artifact: `scripts/ci_builder_legs.py:109,180`, `sw/builder/test_builder.py:24611`; final elaboration aggregate replay. Evidence: the reused verdict says recorded NOT RUN reasons are "listed above" although that aggregate log does not print them. Impact: a misleading log pointer; the ledger remains in evidence. Suggested outcome: print the ledger first or use union-specific wording. Verification: inspect a passing union with nonempty NOT RUN rows.
- **R636-4-S2; SUGGESTION; Robustness, Tests.** Artifact: `scripts/ci_suite_workflows.py:21`, `ci_gate_receipts.py:120`. Evidence: the construction check's reader list does not explicitly name the builder-inventory call; current aggregates do have preparation. Impact: less direct regression protection for this reader. Suggested outcome: include it in the preparation contract. Verification: remove that preparation in a planted graph and require generation to refuse it.
- **R636-4-S3; SUGGESTION; Tests.** Artifact: `sw/builder/test_builder.py:29157`. Evidence: the driver's unknown/repeated/out-of-order/empty selection refusals lack committed subprocess controls; union selection controls independently reject invalid evidence. Impact: defence-in-depth gap only. Suggested outcome: preserve the driver refusals with focused controls. Verification: each malformed selection exits before a gate executes.
- **R636-5-S2; SUGGESTION; Robustness, Tests.** Artifact: `scripts/ci_suite_workflows.py:109`, `ci_gate_workflows_selftest.py:102`. Evidence: direct generation removes its one expected dedicated arm but need not reject an additional stray arm itself. The newly committed generated-output assertion rejects any remaining `= milan_dp ;;` arm. Impact: direct generator refusal remains weaker than the complete gate. Suggested outcome: optionally refuse leftover arms during generation. Verification: plant a correct arm plus a second arm; require the generator itself to fail.
- **R636-1-S4; SUGGESTION; Docs, Robustness.** Artifact: `scripts/run_all_suites.sh` piece timeout selection. Evidence: a piece inherits the parent's deadline, so the total permitted time across pieces is larger; no parent deadline was raised. Impact: readers can confuse scheduling bounds with a tighter per-case bound. Suggested outcome: state that distinction in the workflow guide. Verification: wording agrees with inherited timeout selection and the separate worker headroom limits.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue rulings; REQ-VER-03/04; ci_builder_legs.py:142; ci_gate_receipts.py:63; generated docs leg commands; evidence-audit.json | R637-6 | 47fd0d3c510000e9412a1613a723b61d4ef2ae4a |
| RTL | CLEAN | delta.patch; unchanged product code/gitlinks; ci_gate_workflows.py:68,128; dependency/aggregate wiring; checkout-integrity.json | R637-6 | 47fd0d3c510000e9412a1613a723b61d4ef2ae4a |
| Robustness | CLEAN | ci_builder_legs.py:115,142,190; ci_gate_receipts.py:63; pristine-gate-selftest.log; published planted controls and mutation receipts | R637-6 | 47fd0d3c510000e9412a1613a723b61d4ef2ae4a |
| Tests | CLEAN | ci_gate_workflows_selftest.py:92,238,313,390; revert-probe.json and raw logs; round6-final-validation.json; default/worker listings | R637-6 | 47fd0d3c510000e9412a1613a723b61d4ef2ae4a |
| Docs | CLEAN | CI_WORKFLOWS:1429,2689; TESTING:518; RUNNING_TESTS:84; milan_dp/README:447; 726_STREAM_COUNTERS:177; live PR body; evidence limitations above | R637-6 | 47fd0d3c510000e9412a1613a723b61d4ef2ae4a |

## Real limits and pending manager duties

The source execution evidence is the author's published receipt set. No manager source bank exists or is inferred. It reports 38 worker-zero shell steps, docs builder legs, the CI-event step, a separate runner contract gate, the unsharded docs reference, the two elaboration builder legs, no-git and wire checks, with zero recorded memory events. The shell banks do not execute hosted upload actions. The elaboration aggregate replay explicitly substitutes the unchanged simulation aggregate's outcome; it is not a fresh simulation run. Raw round-six builder JSON/log bytes are represented by hashes and summary records in the public packet, so the reviewer cannot independently rehash those unavailable raw logs or replay their full per-gate comparison. Those limits do not become claims of additional execution.

At the captured exact-head API readback, most jobs were queued or running. `docs-check-no-git`, `wire-accountability`, `changes`, `full-ci-gate` and `bdd-conformance` had completed successfully. Physical gPTP was explicitly skipped. No completed full-workflow duration or successful exhaustive aggregate is inferred from that snapshot.

The manager still owns exact-head hosted/act acceptance, first-start/last-end workflow timing, required contexts, full replay/placement/memory evidence, capacity and cancellation readback, and the second independent review. The final current-dev merge candidate must receive its own builder and native bank validation and linked receipts. Source base is `fa7347fc59173f90e4feec2df207692e6e6e72ec`; supplied live dev is `f62602531d415d6c1cae1374a3cc2938faf54049`. This source verdict does not validate an unbuilt future candidate. Merge authorization, no reviews in flight, post-merge containment, documentation completion and issue/project closure remain required. Physical calibration NOT RUN and field skips are not hardware evidence.

No full parent, processor, gPTP, synthesis or builder bank was run. No source fix, commit, push, GitHub write, author contact, container/host-runner execution, shared installation, hardware operation or sub-agent was used. The foreground revert probe restored bytes and modes in a finally block. Final integrity checks verify all 1,369 root tracked blobs, all index entries, modes/types, all six root gitlinks, and the five initialized dependencies' tracked bytes/indexes at their pins. The unused external gitlink remains uninitialized. The worktree is clean.

Portable scripts: `revert_probe.py`, `audit_evidence.py`, `verify_integrity.py`, `verify_public_packet.py`. Invoke each with the repository path and packet path. `MANIFEST.sha256` lists publishable scripts and receipts relative to the packet. Scratch data is excluded.

R637-6 FINISHED
