[R571] POSITIVE - exact head 8c3e892c2b7130d88d16fb6a26136856975e1ea9

R571-6, external independent delta review of issue #621 / PR #707. Reviewed tree: `04f38ab729f09b4f1185f7f91416995868308ff8`. All five lenses are CLEAN for this merge delta. No open BLOCKER, MAJOR or MINOR is attributable to it. One existing wording RESIDUE and the prior optional suggestions remain. This verdict does not authorize merge or discharge candidate validation.

The merge has ordered parents `2cf985f3206dd519d80142fd2479afe24c3051f6` and `cfadd767a7ad47aaee68de655e1066cc000fb8a0`. The latter is both the requested source comparison base and the live dev tip observed during review. PR head and closing references were read independently; the head matches and `closingIssuesReferences` is empty (`receipts/pr-state.json`, `receipts/live-dev.log`).

I reconstructed AGENTS.md, CONTRIBUTING.md and docs/README.md, then the public issue scope and decisions, requirements and interfaces, the requested `cfadd767..8c3e892c` diff and history, and public executable evidence. No private author material, other checkout, management directory, or current parallel review was consulted. My independent verdict and ledger were written in `receipts/independent-verdict.txt` before reading prior reviewer reports. Prior public findings were reconciled afterwards.

The governing scope is [the assignment](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6084306147): reproduce and fix grandmaster-driven signed 10 ms steps, prove the failure arm, and check public counters and media effects. The physical repeat belongs to a later lane. [The capture ruling](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6087415319) and [final receipt ruling](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6089776382) govern the separate grading and refresh changes. [The runtime ruling](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6101380300) requires the suite split without removed coverage, and [the runner-test ruling](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6103886503) freezes its assertions and adds the dynmap inventory item. These were checked against REQ-PTP-05/07/08, REQ-VER-01/04, `docs/design/GPTP_PLANE.md:97`, `docs/integration/INTEGRATION_GUIDE.md:109`, and the pinned donor's `docs/INTEGRATION.md:192`.

The plain-merge comparison passes. `scripts/verify_tree.py` independently invokes `git merge-tree --write-tree` with the full parent SHAs. Its conflict tree is `be5d933340fa93077fa34154bedf8cdc7612e478`. Exactly these paths differ between that tree and the published head:

- `docs/diagrams/PNG_MANIFEST.json`
- `docs/diagrams/submodule_boundaries.drawio`
- `docs/diagrams/submodule_boundaries.png`

The boundary SVG already equals the plain merge. There is no extra source, recipe, test, documentation prose, mode or gitlink resolution hidden in this merge. The earlier raw replay in `receipts/merge-tree.log` uses `HEAD^1`/`HEAD^2` labels; those labels change conflict-marker blobs and therefore its temporary tree ID, not this comparison's result.

I viewed both committed PNGs. The boundary diagram legibly shows gPTP `7dda9c3b4d65`, lwSRP `08ee86e812a0`, protocol processor `2ad2f845dd58`, stream primitives `48ff7a7e2ef7`, and unused external import `efeb541ae5fe`, matching all five gitlinks. The merged boundary source and decoded raster pass their generator and provenance checks. Its manifest entry describes the combined tree, with source digest `b4a3a7c7...` and raster digest `5cfd36ac...`. All three `timesync_chain` blobs and its manifest entry are byte-identical to `2cf985f3`; its displayed gPTP pin is `7dda9c3b4d65`. Every other manifest entry equals dev. See `receipts/tree-verification.log` and `receipts/visual-review.txt`.

[R571] PASS Conformance - `REQUIREMENTS.md:154`; `docs/design/GPTP_PLANE.md:97`; donor `docs/INTEGRATION.md:192`; `tb/verilator/gptp_plane/sim_phc_step.cpp:261`; `tb/verilator/milan_dp/sim_gmstep.cpp:952` - the merge preserves the signed-step, consistent-delay, completed-exchange liveness, public-counter and media expectations. The source range changes no parent product RTL relative to dev; its adopted donor is unchanged from the prior reviewed head. Physical acceptance remains expressly deferred and the PR cannot auto-close the issue.

[R571] PASS RTL - donor `hdl/ucode/gen_gptp_ucode.py:834`, `:1298`, `:1727`; `tb/verilator/gptp_plane/gptp_plane_wrap.sv:37`; `hdl/milan/milan_datapath.sv`; `receipts/tree-verification.log` - inspected the step flag, rate seed, completion gate, request rearm and wrapper increment default. The donor still preserves the ratio and delay while invalidating crossed history. Both completion paths retain the epoch gate. No conflict resolution introduces HDL or changes the adopted donor. Imported dev RTL equals the plain merge; full integrated candidate execution remains the manager's duty.

[R571] PASS Robustness - `sim_phc_step.cpp:315`, `:336`, `:358`, `:373`; `scripts/check_nvm_capture.py:55`, `:131`; `test_sim_pool_backpressure.py:108`, `:132`; `receipts/backpressure-fixture.log` - crossing positions, delayed timestamps, real excessive delay, recovery, answered and unanswered silence cases remain present and byte-identical. The receipt cannot opt out of production timing. Executed runner controls cover interruption, failure propagation, output ordering, blocked consumers and child reaping. All 28 backpressure controls pass with the required relative fixture input; the default-location limitation is recorded below.

[R571] PASS Tests - `tb/verilator/milan_dp/Makefile:541`; `tb/verilator/milan_dp_gm_steps/Makefile:30`; `sim_gmstep.cpp:1286`; `test_sim_pool.py:863`; `scripts/suite_shards.py:189` - the twelve-leg ordinary recipe ends after the render controls, without a GM-step prerequisite or controls call. The separate suite invokes the full clean leg before five shortened default controls. The explicit campaign retains the full leg. These files, the phase-step campaign and the donor pin are byte-identical to `2cf985f3`. Executed runner tests pass 17/17, the shard landmark stays on worker 3/5, and CI ownership and test-evidence checks pass at this head.

[R571] PASS Docs - `docs/diagrams/submodule_boundaries.{drawio,svg,png}`; `timesync_chain.{drawio,svg,png}`; `PNG_MANIFEST.json`; `docs/reference/SUBMODULES.md:21`; `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1626` - viewed and source-checked the merged diagrams, verified the pinned interfaces and source links, and compared retained receipt figures with their prose. The recorded maxima remain 3.96728, 13.86318 and 10.42973 ms; the 8x8/50 MHz floor ratio is 3.5345 and margin 10.63682 ms. Required documentation checks pass. The status sentence below is wording residue only.

Executed validation at this head is recorded separately from earlier simulation receipts:

| Command or check | Result | Receipt |
|---|---|---|
| `python3 scripts/docs_check.py` | rc 0; zero findings, 204 Markdown and 1260 text files | `receipts/docs-check.log` |
| `python3 scripts/check_em_dash.py --base cfadd767a7ad47aaee68de655e1066cc000fb8a0` | rc 0 | `receipts/em-dash.log` |
| `python3 scripts/gen_toc.py --check` | rc 0; 144 annotated contents lists | `receipts/toc-check.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | rc 0; 472 links | `receipts/toc-anchors.log` |
| `python3 scripts/check_doc_paths.py` | rc 0 | `receipts/doc-paths.log` |
| `python3 scripts/ci_events.py --check` and `--selftest` | rc 0 each; selftest 1749 contract items, 2374 arms | `receipts/ci-events-*.log` |
| `python3 scripts/measure_test_evidence.py --check` and `--selftest` | rc 0 each; 105/105 selftests | `receipts/test-evidence*.log` |
| `python3 scripts/check_submodule_docs.py` | rc 0 | `receipts/submodule-docs.log` |
| `python3 scripts/check_diagram_pngs.py` and `--selftest` | rc 0 each; six rasters, 28 mutation controls | `receipts/diagram-pngs*.log` |
| Both diagram generators, `--check` | rc 0 each | `receipts/submodule-diagram.log`, `receipts/timesync-diagram.log` |
| `python3 scripts/suite_shards.py --selftest` | rc 0 | `receipts/suite-shards.log` |
| `python3 tb/verilator/milan_dp/test_sim_pool.py` | rc 0; 17/17 | `receipts/sim-pool.log` |
| Unchanged backpressure tests with exact `recipe.py` available relative to their fixtures | rc 0; 28/28 | `receipts/backpressure-fixture.log` |
| `python3 scripts/check_nvm_capture.py` | rc 0 | `receipts/capture-receipt.log` |
| Its five mutations: bytes, records, clock, ignore-off-timing, receipt-opt-out | expected rc 1 each, for the named refusal | `receipts/capture-mutation-*.log` |
| Raw parent/submodule blobs, modes, index, merge comparison and gitlinks | rc 0 | `receipts/tree-verification.log` |

The first Markdown-dependent invocations refused the absent pinned renderer (rc 2). Dependencies were installed with the repository hash lock into packet scratch only; all three reruns passed. Initial refusals are retained as `*.initial.log`/`.rc`. The initial backpressure invocation passed its 14 direct controls, then reproduced the public #720 setup wait because its temporary Makefile could not find `../nvm_capture_cpu/recipe.py`. It was stopped with SIGTERM and is NOT counted as a pass. `scripts/backpressure_fixture.py` supplies that exact tracked recipe beside the scratch case directories and calls the unchanged test's `run()`; it does not fix source or the default invocation. The manager's runner-test ruling explicitly excludes that pre-existing defect and absent CI wiring from this lane. Neither is represented as resolved.

Independent checks ran concurrently through a joined foreground driver, at most three focused commands at once. There were no heavy builds or detached shell jobs. Disposable fixtures and dependency installations are exclusively under `scratch/`. The retained scripts reproduce the focused checks and merge proof. To replay the final check set, install `tools/markdown/requirements.txt` with `--require-hashes --target <packet>/scratch/markdown-deps`, then run `python3 <packet>/scripts/run_checks.py <clone> <packet>`, `resolution_checks.py` with the same arguments, and `verify_tree.py <clone>`. A fresh output packet preserves the original receipts.

Public source evidence was examined after the independent diff pass. Ten selected executable receipts from [public evidence commit 02d43fb7](https://github.com/kebag-logic/milan-fpga/tree/02d43fb7f99d31b7c0a03dcf9534f779b50f9480/review-evidence/621-r1) were verified against that tree's published manifest. They show the original approximately two-second outages, the corrected 49-check early regression, three early rejected defects, 190 integration checks, twenty integration controls and the nine-pair capture invariant. These are historical source receipts, not runs performed by this review or simulations of `8c3e892c`. Later public author comments [6097029581](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6097029581) and [6104107297](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6104107297) record the extended 62-check/eight-arm campaign and corrected runner tests. Their relevant source files remain identical here. `receipts/published-r1-verification.txt` records the hashes; `receipts/public-scope-and-evidence.json` retains the cited public comments. No manager source bank is claimed or inferred at this head.

Prior public findings are explicitly disposed as follows. Original severities and all assigned lenses are retained; resolution is against current bytes, with historical executions clearly distinguished.

| Finding | Severity; lenses | Disposition at this head and evidence |
|---|---|---|
| R570-1-F1 = R571-1-F1 | BLOCKER / MAJOR; Tests, Docs | Source defect RESOLVED. `measure_test_evidence_readers.py:113` retains the accurate disposition; exact-head check and 105/105 selftest pass. Fresh hosted completion is still a manager duty, not claimed here. |
| R570-1-F2 | MINOR; Robustness, Tests | RESOLVED. `production_spec` forces production grading; all five mutation controls reject, including receipt-opt-out. |
| R570-1-F3 = R571-1-F3 | MINOR; Docs | RESOLVED. The capture page and receipt are unchanged from the reviewed parent and their figures/provenance agree, as independently checked above. |
| R570-1-F4 = R571-1-F2 | MINOR; Tests | RESOLVED, retained by exact blob identity. `sim_phc_step.cpp:358` requires four unanswered requests after an answered crossing; both deletion plants remain in `phc_step.py`. The author publicly executed the rejected plants; no fresh simulation is claimed. |
| R570-1-F5 | MINOR; Conformance, Docs | RESOLVED. Live closing references are empty and the body says Relates to #621. |
| R571-2-F1 | MINOR; Tests | RESOLVED, retained by exact blob identity. `sim_phc_step.cpp:373` covers an unanswered crossing; the three-after-crossing expectation, credit-on-step plant and cease-only positive control remain. The later public author receipt records the discriminating result. |
| R570-4-F1 | MINOR; Tests | RESOLVED. Both runner-test files and recipe are intact; 17/17 and relocated 28/28 executed at this head. Negative assertions reject the removed prerequisite, banner and controls, and dynmap remains in the twelve-leg inventory. |
| R570-1-R1 / R571-1-R1; R570-4-R1 | RESIDUE; Docs | Original requested wording was applied; superseded by the still-stale subsequent status sentence below. |
| R571-2-RES-1 and RES-2 | RESIDUE; Docs | RESOLVED. Six controls/five distinct defects and narrowed drift attribution are retained in the campaign, reader disposition, GPTP_PLANE and capture page. |
| R570-5-R1 = R571-5-RES-1 | RESIDUE; Docs | RETAINED as R571-6-RES-1 below. |

Prior optional suggestions remain carried, without affecting CLEAN coverage:

| IDs | All attributable lenses | Retained subject/artifact |
|---|---|---|
| R570-1-S1; R571-5-S1 | Tests, Robustness | Non-unity peer-rate coverage for retained ratio; `sim_phc_step.cpp:187` and donor interface contract. |
| R570-1-S2 | Docs | Changelog entry for this pin/behavior. |
| R570-1-S3; R571-1-S2 | RTL | Explicit ROM headroom documentation; donor generator. |
| R570-1-S4; R571-1-S1 | Conformance, Robustness | Software settime lies outside the grandmaster-driven step flag contract. |
| R570-1-S5 | Docs | Default phase-step campaign description in TESTING's gptp_plane row. |
| R571-1-S3 | Robustness | Repeated steps crossing every exchange; retained-delay limitation. |
| R570-2-S1; R571-2-S1 | Conformance, Docs | Fourth-versus-fifth lost-response reading; donor threshold and PR limitation. |
| R571-2-S2 | Tests | Duplicate deletion controls remain; the proposed additional distinct credit-without-completion defect has since been added. Retained as optional inventory cleanup only. |
| R571-3-S1 | Tests, Robustness | A response-only crossing arm, withholding its Follow_Up; `sim_phc_step.cpp:373`. |
| R570-3-S1 | Tests, Robustness | Explicit nonzero timestamp assertion in crossing-order checks. |
| R571-4-S1 | Docs | Existing suite-count prose in RUNNING_TESTS and the suite index. |
| R571-4-S2 | Docs | Replace clearly labeled runtime projections with dated hosted observations. |
| R571-4-S3 | Tests | A regression check that the separate suite still runs the full clean leg. |
| R570-4-S1 | Tests | Check that the short flag removes only the intended phase. |

R571-6-RES-1 - RESIDUE - ALL attributable lenses: Docs.
Artifact: PR #707 body, Status paragraph (`receipts/pr-body-snapshot.txt`), retaining "The round 4 head `2cf985f3` is local and unpushed."
Authority/evidence: the live PR head is the published merge `8c3e892c`; prior R570-5-R1/R571-5-RES-1 already identified the stale sentence. The owner rule permits wording-only residue.
Impact: obsolete publication-status wording; no measurement, figure, verdict, test, code, generated artifact, conformance or clause claim changes.
Required outcome / exact fix: replace the two status sentences beginning "The runtime-round head is pushed" and "The round 4 head" with "The review head `8c3e892c` is published; hosted results at it are the manager's to confirm."
Verification: read the live body after the manager applies the wording. Carry this to the residue checklist; it does not leave Docs unclean.

Reviewer-owned completion ledger:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue frozen scope/rulings; REQUIREMENTS:154; donor INTEGRATION:192; GPTP_PLANE:97; sim_phc_step:261/358/373; sim_gmstep:952; PR closing references | R571-6 | 8c3e892c2b7130d88d16fb6a26136856975e1ea9 |
| RTL | CLEAN | Plain merge comparison; donor generator:834/1298/1727 and gitlink; gptp_plane_wrap:37; merged milan_datapath; raw blob/index proof | R571-6 | 8c3e892c2b7130d88d16fb6a26136856975e1ea9 |
| Robustness | CLEAN | Crossing/silence arms; capture production guard and five negative controls; runner failure/cancellation/output cases; relocated 28/28 backpressure checks; PNG mutation controls | R571-6 | 8c3e892c2b7130d88d16fb6a26136856975e1ea9 |
| Tests | CLEAN | Both suite Makefiles; sim_gmstep:1286; test_sim_pool:863 (17/17); backpressure test:108/132; shard landmark:189; CI and evidence selftests | R571-6 | 8c3e892c2b7130d88d16fb6a26136856975e1ea9 |
| Docs | CLEAN | Both viewed PNGs and generated sources; PNG_MANIFEST; SUBMODULES; capture receipt/page; all requested document and generator gates; live PR wording residue | R571-6 | 8c3e892c2b7130d88d16fb6a26136856975e1ea9 |

This ledger covers the requested manager-merge delta with retained earlier fixes. It is not a claim that all newly imported dev functionality received a new full review or that complete integration banks ran in this session.

Real limits and pending manager duties:

- No full parent, processor, gPTP, synthesis, builder or resource bank ran. No simulator build or hardware access was used. The cited standard's full clause text was not reopened; the delta does not change its existing interpretation. Physical calibration is NOT RUN. Physical-rate simulation and field skips are not hardware proof.
- The raw-byte audit verifies 1284 parent blobs, 104 gPTP blobs, 562 protocol-processor blobs and 214 stream-primitive blobs, with exact modes/index and recorded gitlinks. The unused external and lwSRP checkouts are uninitialized; their exact gitlinks were verified, not their working-tree bytes. No source edit, commit, push, merge or GitHub write occurred.
- Exact-head hosted snapshot (`receipts/hosted-checks.json`): successful executed jobs included docs-check-no-git, wire-accountability, changes, bdd-conformance, verilator-lint, full-ci-gate and Yosys shard 2/4. Other documentation, elaboration, firmware and long-shard jobs were queued or in progress. Physical gPTP was SKIPPED. The completed long aggregates and rtl-fast verdict were not established by this snapshot. This review does not poll them to acceptance.
- The manager owns hosted/act acceptance, the required suite runtime confirmation, the donor's merge bar, and final current-dev candidate validation with builder and native banks. No manager source bank exists at this exact head. Source evidence and final candidate evidence are distinct. Source base and observed live dev are both `cfadd767a7ad47aaee68de655e1066cc000fb8a0`; because it is already a parent of this head, an unchanged-base candidate can have this same tree, but that identity is not a bank result. Record final candidate IDs and link its receipts when produced; revalidate if dev moves.
- Wait for every independent review to finish, meet the full merge bar and obtain explicit maintainer merge authorization. Perform post-merge containment. Preserve issue #621 for the later physical repeat, carry the wording residue and optional suggestions, and retain #720's separately scoped default-fixture/CI-wiring limitation.

Only REPORT.md and files listed in MANIFEST.sha256 are publication material. Scratch is excluded. Every selected receipt has a relative path and SHA-256 in the manifest.

R571-6 FINISHED
