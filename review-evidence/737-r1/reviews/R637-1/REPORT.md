[R637] NEGATIVE - exact head cf9c936697a06e44c41681bcc12dc612a3242eb2

External independent review R637-1 of issue #737 / PR #739. Tree: `a5eb619c5c9ead508e7189fd77527d84d2c4fdda`. All five lenses were applied. Two MAJOR findings and one MINOR remain open. This report neither approves merge nor accepts the pending hosted timing measurements.

Reconstruction followed the operating contracts, documentation index, public issue decisions, requirements/interface authorities, source diff/history, then public executable evidence. The reviewed range is `fa7347fc59173f90e4feec2df207692e6e6e72ec..cf9c936697a06e44c41681bcc12dc612a3242eb2`. The independent verdict and ledger were recorded before querying prior review findings. No other review report or private author material was used.

The governing scope is the [round-one assignment](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160775078), [driver ruling](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160937413), [signature design](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160962404), topology/STOP rulings `6161122704`, `6161771913`, `6162403147`, and the [fail-fast directive](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6161180121). The [CPU rules](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6166855177) enter this round through `6167284204`, corrected by [6167288337](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6167288337): sixteen CPUs normally, one named twelve-CPU fallback. Trigger removal and signature authentication under `6166823105` remain round two. Requirements `REQ-VER-01` through `REQ-VER-04`, CONTRIBUTING section 3, and the documented dependency boundaries remain applicable.

**R637-1-F1 - MAJOR - Conformance, Robustness, Tests, Docs**

Artifact: `scripts/ci_suite_pieces.py:69`, `tb/verilator/capture_coherence/mutants.py:341`, `tb/verilator/media_nco/Makefile:16`, `scripts/ci_gate_workflows_selftest.py:35`, `docs/testing/CI_WORKFLOWS.md:1944`.

The capture campaign's compiler budget does not reach every child build. The new scheduler runs up to four campaign workers and exports `VERILATOR_JOBS=cpus/4`. Its NCO control and mutant invoke the media-NCO Makefile, which still passes literal `-j 0`. That selects the entire process affinity rather than the divided worker budget. The NCO control belongs to leg `2/4`; the NCO mutant belongs to leg `0/4`.

Authority/evidence: the CPU ruling requires in-job parallelism to respect the job's CPU allocation. `nested-budget-probe.jsonl` records real Makefile dry runs: the junction and channel-map children consume budgets 1/3/4 for job widths 4/12/16, but the NCO child requests zero in every case. `compiler-affinity-probe.jsonl` independently observes the pinned compiler invoking make with 4/12/16 workers despite exported budgets 1/3/4. That probe substitutes make with an argument recorder; it proves dispatch behavior and performs no compilation or simulation. The existing CPU control stops at a mocked `subprocess.run`, so it reports bounded nested builds without examining these child commands.

Impact: an NCO build can consume the entire job compiler budget while other campaign builds remain active. This violates the nested concurrency bound and weakens the resource-sizing argument. No actual OOM or timing overrun is claimed by this probe. The documentation's assertion that the capture campaign divides the budget among all active builds is false for this consumer.

Required outcome: every build reached by the capture pool must honor the allocated per-worker budget, or admission must otherwise keep the combined compiler allocation within the job's CPUs. Preserve all cases and predicates. Update the control to inspect the real child recipes and keep the documentation accurate.

Verification: rerun `probe_nested_budget.py` and the compiler-dispatch observer; exercise every capture child at normal and fallback widths, including the NCO positive control and mutant. A deliberately budget-ignoring child must make the resource control fail. The current probe intentionally asserts the observed defect and must be updated to assert the corrected outcome during re-review.

**R637-1-F2 - MAJOR - Conformance, Robustness, Tests, Docs**

Artifact: `scripts/ci_runtime_workflows.py:116`, `scripts/ci_runtime_workflows.py:89`, `scripts/ci_fail_fast.py:58`; generated `ci-fail-fast` and `ci-manifest` jobs in all four workflows; `docs/testing/CI_WORKFLOWS.md:2567`.

A manifest-collector failure cannot trigger hosted cross-workflow cancellation. The generator computes the watcher's expected job names before adding the watcher and collector. The collector also depends on the watcher, so the watcher has finished before collection begins. The collector has read-only permissions and no cancellation path. A collection or upload failure can therefore leave other workflows at the same head running.

Authority/evidence: the fail-fast directive requires the first failed job to stop the same-repository run and sibling workflows. `fail-fast-probe.jsonl` exercises the production generator and `observe` function for all four graphs. An ordinary watched failure is detected. Adding a failed `Collect CI manifest` job instead returns completed/no failure for every graph. The collector is excluded in all four, and each collector waits for its watcher. Existing cancellation controls test selected job names and API requests but omit this generated-graph failure path. The watcher's own evidence steps also run after its cancellation step, leaving late failures there outside the observation loop.

Impact: failure of the evidence-collection path bypasses the promised early stop, wasting remaining work and failing the round-one cancellation contract. This does not establish a false successful manifest: incomplete or failed evidence is still refused.

Required outcome: provide a same-repository cancellation path for every generated job failure, including collection and late watcher failures, while retaining the fork write restriction and avoiding a dependency cycle. Align the documentation with the actual coverage.

Verification: plant a collector failure while another workflow remains active; require a cancellation request for that sibling. Cover ordinary-job failure, collector failure, watcher-tail failure, successful completion, and fork zero-write behavior using the generated graph. The manager should also retain a live hosted cancellation receipt. The current reproducer records the defect; re-review must invert its expected collector result.

**R637-1-F3 - MINOR - Conformance, Docs**

Artifact: `docs/testing/CI_WORKFLOWS.md:1567`, compared with `.github/ci-templates/elaborate.yml:158`, `.github/ci-templates/elaborate.yml:186`, and `docs/testing/CI_WORKFLOWS.md:2585`.

The elaboration section still says the Scala cache keeps a broad fallback and the pip cache uses a prefix fallback. Both fallbacks were removed by this PR. The later cache section correctly says there is no broad fallback.

Authority/evidence: issue #737 requires an accurate workflow policy and digest-bound caches. The template-to-base comparison and generated workflows show neither cache has `restore-keys`. This is an incorrect operational cache-policy claim, so it is not classified as wording-only RESIDUE.

Impact: the authoritative guide gives contradictory instructions about the cache trust and invalidation policy.

Required outcome: replace the stale paragraph with the exact version/source/recipe-key behavior, explicitly stating that neither Scala nor pip restores a prefix fallback; retain the generated CPU metadata's distinct input binding.

Verification: compare that paragraph with both generated elaboration workers and their templates. No code or test predicate needs to change for this finding.

**Evidence applied across the five lenses**

The template-to-base comparison preserves the original test command inventory and conditions; changes are scheduling, bounded job arguments, installation provenance and added evidence controls. Existing test timeouts are not raised. Generated workers use standard `ubuntu-latest`. Protected carrier names remain, with executed gate receipts and fail-closed dependency checks. The continuous media-clock history retains its state, waits and single-threaded execution under the explicit STOP ruling.

The six suite unions derive membership from driver/Makefile registrations. The reviewer reran verification over the [published execution receipts](https://github.com/kebag-logic/milan-fpga/tree/d0d8ceb4c5fa29f5990135baf56aa3f0dd48610b/review-evidence/737-r1), using inventories freshly emitted by this head. Full and sharded records agree on every recorded case verdict, process result, output digest and optional RESULT line. Independent dropped-result probes are refused for all six suites. The public comparison summary additionally records refusal when a case is removed from every claim and when output changes despite a recomputed digest.

| Suite | Cases | Legs | Published execution head |
|---|---:|---:|---|
| milan_dp | 19 | 4 | `e06f342f5c35ccd71c1902e32747422245407afa` |
| milan_dp_mclk | 31 | 4 | `9dd0817da6d3f771a3bd1db5eca0f2ba63d0695d` |
| capture_coherence | 31 | 4 | `068802530c138eb1fdfaada374de4ecf9cf860a7` |
| maap | 66 | 4 | `068802530c138eb1fdfaada374de4ecf9cf860a7` |
| milan_dp_render | 3 | 3 | `068802530c138eb1fdfaada374de4ecf9cf860a7` |
| pp_shadow | 4 | 4 | `e06f342f5c35ccd71c1902e32747422245407afa` |

These are retained-source comparisons, not new exact-head simulation runs. `public-case-audit.jsonl` records the checks. All six source-correspondence groups were independently compared using Git objects and are identical over their declared paths. The separately disclosed receipt/scheduling differences were read directly. Raw simulation stdout is not included in the public case packet; its digests and the author's production-reader results were examined, but the reviewer did not rehash unavailable stdout or rerun the full campaigns.

The [author's REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6168691299) and public gate receipts report sixteen suite workers, six unions, 62 parent-suite logs and 2,187,186 checks with zero in-suite failures, using retained worker head `9a76ed5cf99996f433c82bcfde2fdb01fc05d743`. The public 94-command receipt index, failed-attempt dispositions and source correspondence were examined. These are author source-validation receipts. There is no manager source bank at this head, and none is inferred.

For the RTL lens, the full diff leaves product HDL, firmware behavior and dependency gitlinks unchanged. The driver edits preserve the model sources, elaboration parameters and existing predicates; the media-clock C++ change only exposes checked values. No changed clock, reset, CDC, protocol state machine or external interface was found. The host concurrency findings above do not assert a product RTL defect.

The local dispatcher path was statically followed from externally supplied aligned ranges through admission, initial container options, executor cleanup and release. The twelve-wide fallback is named once in the runner and passed to the dispatcher. The monitor is read-only and checks unbooked placement, overlap and movement. The public dispatcher build receipt and repeated race-control results, runner self-test receipts and 44-case slot-proof receipt were read. Their receipt hashes identify the reviewed dispatcher inputs. No host runner, runner self-test, dispatcher runtime, container engine or privileged command was executed during this review.

Memory policy is four jobs, eight GiB each, with a 36-GiB isolated-slot cap. The documented samples are 5.41 GiB as the sum of four synthesis-shard peaks and 5.34 GiB for the publication census. These samples are not a universal worst-case bound, and F1 prevents accepting the claimed nested budget as complete.

Source-built tool keys bind release, immutable source commit and workflow recipe. Installation caches add package/source hashes and recipe digests without broad restoration. The generated workflow check and negative cache controls passed. The seven-section manifest implementation binds committed definitions and plans, transports actual outcomes, retains missing/cancelled work and refuses changed or incomplete comparisons. Canonical JSON controls reject duplicate keys and floats. Missing image provenance, authentication, evaluated skips and final collector outcomes remain explicitly incomplete; this round establishes no signed-build or actual hosted/local equality claim.

All 17 focused commands in `focused-results.json` returned zero. This includes 2,186 workflow contract items and 5,020 mutation controls, plus case/union, source-plan, manifest, runtime transport, cache and scheduling controls. The workflow mutation command completed in 555.095 seconds. These passes coexist with F1/F2 because their current controls miss the demonstrated paths. `run_focused.py` retains each command's own log and return code and joins a bounded four-worker foreground pool. The capture-control log has only its temporary directory prefix redacted; `receipt-redactions.json` retains both hashes.

**Hosted observations and manager-owned acceptance**

At the query recorded in `hosted-timing.json`, exact-head `gh run list` returned no runs, the branch query returned no runs, and PR #739's `statusCheckRollup` was empty. No run ID was available for `gh run view --json jobs`. `audit_hosted.py` performs that exact job readback and first-start/last-end calculation when a run becomes available. No executed or skipped job verdict can be inferred from the empty response.

| Workflow | First job start | Last job end | Measured span at this head |
|---|---|---|---|
| docs | unavailable | unavailable | NOT AVAILABLE |
| elaborate | unavailable | unavailable | NOT AVAILABLE |
| rtl-fast | unavailable | unavailable | NOT AVAILABLE |
| rtl-full | unavailable | unavailable | NOT AVAILABLE |

The PR's warm-cache projections are not substituted for measurements. The target of at most thirty minutes per workflow remains the manager's acceptance call, including the explicitly disclosed continuous-history exception. The trusted local replay uses the live-dev runner by design; its timing cannot validate this PR's new runner implementation.

After the independent verdict was written, the reviewer queried PR reviews, inline review comments and issue comments. There were zero reviews, zero inline review comments and only the two manager review-start comments. No prior public review FINDING was available to resolve or retain; `prior-findings-check.json` records this result.

**Reviewer-owned completion ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Issue rulings; generated workflows/templates; six inventories/unions; cache, CPU and manifest contracts; F1-F3 | R637-1 | `cf9c936697a06e44c41681bcc12dc612a3242eb2` |
| RTL | CLEAN | Full source diff; unchanged `hdl/`, product `sw/`, dependency pins; changed suite Makefiles/drivers and `sim_mclk.cpp`; source-correspondence Git comparisons | R637-1 | `cf9c936697a06e44c41681bcc12dc612a3242eb2` |
| Robustness | UNCLEAN | Admission/cleanup and placement monitor; nested child recipes; cancellation graphs; malformed/missing/duplicate receipts; incomplete manifest refusal; F1-F2 | R637-1 | `cf9c936697a06e44c41681bcc12dc612a3242eb2` |
| Tests | UNCLEAN | Seventeen focused controls; six published full/leg comparisons; dropped-case probes; actual child Makefile and compiler-dispatch observations; watcher probe; F1-F2 | R637-1 | `cf9c936697a06e44c41681bcc12dc612a3242eb2` |
| Docs | UNCLEAN | `CI_WORKFLOWS.md`, `CI_SIGNATURE.md`, public scope/PR/receipts and evidence limitations; F1-F3 | R637-1 | `cf9c936697a06e44c41681bcc12dc612a3242eb2` |

Limits and pending duties: no full parent, processor, gPTP, synthesis or builder bank was run by the reviewer. No actual simulation result is claimed from the compiler-dispatch probe. Physical calibration marked NOT RUN and field skips supply no hardware proof. The manager still owns hosted job readback/timing and acceptance, full trusted replay and memory receipts, live cancellation evidence, the current-dev merge candidate's builder/native banks, exact candidate validation, merge authorization and post-merge containment. The supplied live-dev base is `fa8209889411e8ca95757174c981f720dbcd95a2`; this source review is not validation of that future merge result. F1-F3 require correction and independent re-review before their lenses can become clean.

No source fixes, commits, pushes, GitHub writes, author contact or hardware operations occurred. `checkout-integrity.json` verifies the exact head/tree, 1,353 root tracked blobs, all tracked bytes/kinds/executable modes/index entries and all five required populated dependency pins and their tracked contents. The unused external dependency remains uninitialized with its recorded gitlink intact. Portable scripts and listed receipts are bound by `MANIFEST.sha256`; scratch content is excluded from publication.

R637-1 FINISHED
