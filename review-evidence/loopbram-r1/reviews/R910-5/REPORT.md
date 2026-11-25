[R910] POSITIVE - exact head 09201d35d7ea720b3ba205da185ba35c159ec24a

External independent review R910-5 of issue #979 / PR #987. Tree: `a3b3dca8a55b738e714ada4662a309a50118a481`.

The budget-table and selector-docstring corrections are present and correct. New public evidence closes R910-4-F1 / R909-6-N1 (current enabled routing) and R910-4-F2 (review-head attribution). No BLOCKER, MAJOR or MINOR remains from this review or the reconciled findings. Two wording residues and existing optional suggestions remain. This verdict does not authorize merge or certify the final current-dev candidate.

**Scope and independence**

The brief's delta description is stale. `c413d33a..HEAD` changes **210 files, 12,434 insertions and 1,270 deletions**. The one documentation commit is `1516b2ffe321337858389ec8e42897f8a80644bb`: two Markdown files, three insertions and one deletion. It precedes merge `7049c524` and three follow-up commits. R910-4 covered that later composition at this exact head. No source changed since; the new material is public evidence. `scope.txt` records both ranges and history.

Context was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the [frozen issue and option-B ruling](https://github.com/kebag-logic/milan-fpga/issues/979#issuecomment-7096503041), REQ-VER-01..04, the input-loopback design/interface authorities and [#818](https://github.com/kebag-logic/milan-fpga/issues/818). `independent-pass.md` records my initial verdict and five-lens ledger before reading historical review reports. No concurrent review report, private author material or private management directory was read. No source edit or GitHub write occurred.

Unchanged implementation coverage is carried from R910-4 at the **same head**, with prior findings checked at their causes. This is not a fresh whole-repository implementation or standards audit.

**Documentation and executable checks**

- `docs/testing/CI_WORKFLOWS.md:685-694` matches all eight named `suite_timeout` arms in `scripts/run_all_suites.sh:292-303`. The two loopback suites and `reboot_ctrl` each have 300-second defaults. Their provisional status and selector-docstring basis are explicit; the loopback row records cold-run evidence and owed hosted replacement.
- Every non-default arm has a table row. `mmcm_servo` uses the 1800-second default. Therefore “every other default suite” is true. The historical documentation commit changes no timeout or test behavior.
- `docs/testing/TESTING.md:469` contains the exact R909-4-R1 fix: “Both are provisional under the new-suite steps in the selector's docstring: each figure in `scripts/suite_shards.py` is 300 s.” This was line 442 before the merge. The selector contract exists at `scripts/suite_shards.py:14-20`.
- Local hygiene passes: zero findings across 226 Markdown and 1,958 scrubbed text files; scrub controls 23/23 and routing controls 4/4. Documentation style passes for 25 documents. Whitespace checking passes.
- The first em-dash check refused missing dependencies, exit 2. With hash-pinned Markdown dependencies installed in a disposable scratch environment, it passes: zero findings over 1,024 added lines in 32 pages, controls 339/339. Both receipts are retained; refusal is not called success.

Reproduction: `python3 check_docs.py <checkout>`. Reproduce the successful renderer-dependent arm with `<scratch-venv>/bin/python scripts/check_em_dash.py --base c413d33a`, after installing `tools/markdown/requirements.txt` with `--require-hashes`. Results are in `docs-results.json`, `docs-*.log`, their return-code files and `whitespace.*`.

**Public evidence and route closure**

Evidence: [publication e55f3f33](https://github.com/kebag-logic/milan-fpga/tree/e55f3f332e8b629a5f933ff3908492ec2e72975a/review-evidence/loopbram-r1). All **64 selected files** from `author-r6b` and `author-r8` match the top-level manifest's published-byte SHA256 values. `evidence-integrity.json` names every file/hash. The publication commit is **unsigned**, according to its public verification record. No detached signature accompanies the selected manifest. This is content-hash and source-binding verification, not a signature claim.

`author-r8/receipts/source-binding.json.txt` names this head/tree, current HDL subtree `244c59e030d9078054fc88744f22e4e3e7d59246`, seven source subtrees and current gitlinks. Start/end identities agree with the clone. The two input manifests list 161 and 165 inputs; **138 checkout input hashes per shape** independently match local bytes. Generated inputs were not regenerated here: their published before/after binding is retained with that limit.

`check_routes.py` compares all **24 raw corner-summary tables** with the summary, checks complete routing and zero routing errors for all six routes, and verifies selected floors. Raw utilization reports and route scripts were inspected. The recipe retains the prescribed placement directives and AggressiveExplore physical optimization/routing. Temperature labels are not claimed as independent timing models.

| Enabled shape | Selected directive | Minimum setup / hold ns | LUT / FF | RAMB36 / RAMB18 | Slices / DSP | Routable = routed nets |
|---|---|---|---|---|---|---|
| 1x1/1if | AltSpreadLogic_high | +0.147 / +0.036 | 32669 / 42821 | 65 / 35 | 14225 / 13 | 73564 |
| 8x8/1if | AltSpreadLogic_high | +0.309 / +0.036 | 48485 / 54965 | 94 / 33 | 15792 / 13 | 97416 |

Both selections meet +0.030 ns setup and nonnegative hold at every corner. Setup, hold and pulse-width failing endpoints are zero. All six routes complete with zero routing errors. The unselected 1x1 ExtraTimingOpt result is +0.020 ns setup and correctly remains a floor miss.

The ordinary enabled 8x8 export still refuses its 70.5-tile control allocation against 56 tiles. The measurement export is separate. The current 59.5-tile ledger leaves +11.0 tiles of S14 debt, or +14.5 over the default budget. No product guard or ceiling was relaxed. These are author source-head implementation receipts, not a manager source bank, bitstream or hardware measurement.

Reproduce: `python3 fetch_evidence.py`, then `python3 check_routes.py <checkout>`. Downloaded evidence stays below `scratch/` and is not republished here.

**Prior public findings**

Historical reports were read after the independent pass, including [R910-4](https://github.com/kebag-logic/milan-fpga/pull/987#issuecomment-7168877833), [R909-6](https://github.com/kebag-logic/milan-fpga/pull/987#issuecomment-7168980620) and their cited earlier findings. Original lens assignments are retained. Author closure labels alone do not establish closure.

| Findings and lenses | Disposition and cause-level evidence |
|---|---|
| R910-4-F1 MAJOR, Conformance/RTL/Tests; R909-6-N1 MINOR, Conformance/RTL | **RESOLVED.** Current source/input bindings, both shapes, three directives each, 24 raw corners, resource reports and allocator refusal audited above. This restores the current coverage previously lost for R910-2-F2 / R909-2-N2. |
| R910-4-F2 MINOR, Docs | **RESOLVED.** `author-r8/REVIEW-READY.md:7`, `HANDOFF-r8.md:22`, `PR-BODY.md:87-88` explicitly correct the attribution: R909-5 at `1516b2ffe321337858389ec8e42897f8a80644bb`; R910-3 at `9acb9b828b29aba71bd51303a4836f86c2278267`. Both match public verdict lines. Historical files remain historical; this ledger does not reuse their error. |
| R909-4-N1 MINOR, Docs; R909-4-R1 RESIDUE, Docs | **Corrections retained and independently checked.** Complete timeout table and exact selector-docstring sentence above. |
| R909-2-N1 BLOCKER; R909-3-N1 MINOR, Tests/Docs | **Resolution retained.** Both suites remain registered/provisional with explicit 300-second arms. Same-head planner evidence remains valid; hosted workers now execute both suites successfully. Replacing estimates remains a manager duty. |
| R910-1-F1 MAJOR, Tests; R909-1-F3 MAJOR, Conformance/Tests | **Resolution retained.** Enabled production command handling, logical-map integration and both-shape connection/invalidation plants remain unchanged since R910-4; inspected `input_loopback_dp/mutants.py:24-47`. |
| R910-2-F1 MAJOR, Conformance/Tests | **Resolution retained.** `input_loopback_dp/sim_main.cpp:600-647` still grades each stream before phase reset and after clipping. Nine held-output plants require all four named failures. |
| R909-1-F1 BLOCKER, Tests/Docs | **Resolution retained.** Queue/parent mutation repairs and exact-head evidence were covered by R910-4; source is unchanged. No fresh full campaign run is claimed. |
| R909-1-F2 MAJOR, Conformance/RTL/Tests | **Resolution retained with limits.** Disabled ports/instance boundaries, optional generate branches and shared mapping writer are unchanged at this same head. Historical canonical comparisons and current default artifact/image equality retain their separate scopes. No new whole-chip disabled identity measurement is inferred. |
| R909-1-F4 MINOR, Tests/Robustness/Docs | **Permitted documentation resolution retained.** Leaf README:51-54, design and parameter contract explicitly identify five guards as untested in isolation. No mutation guarantee is inferred. |
| R909-1-F5 MINOR, RTL/Robustness; R909-1-F6 MINOR, RTL/Robustness/Tests | **Resolution retained.** Unchanged eight-page retention, lead-greater-than-two refusal, derived timestamp window and signed-ramp bounds. No oscillator/hardware claim added. |
| R909-1-F7 MINOR, Docs/RTL | **Resolution retained.** Queue/capture banners and packed-field contracts unchanged since the exact-head review. |
| R909-2-N3 MINOR, Tests/Docs | **Resolution retained.** TESTING.md:380-381 retains parent controls, explicit campaign and affected artifacts. |
| R909-1-R1/R2/R3; R910-1-R1; R909-2-R1, RESIDUE, Docs | **Corrections retained.** Design attribution/public pointer/fresh-measurement wording, builder row order and bind-only guard qualification remain corrected. |
| R909-1-S1, Docs; R909-2-S1, Tests; R909-2-S2, Docs/Tests | **Addressed disposition retained.** Split NAME-capacity disclosure, both-shape connection plants and canonical-input reproducibility limit remain. |
| R909-4-S3, Docs | **Addressed for current publication.** Post-normalization hashes exist and selected files verify. Original-byte hashes are not substituted for published-byte hashes. |

**Retained wording residues**

**R909-5-R1 - RESIDUE - Docs - `docs/testing/CI_WORKFLOWS.md:680-682`.** Authority/evidence: the introduction says hosted worst case plus margin sets every named entry, but rows correctly distinguish provisional entries. Impact: introductory wording only; no number, check or row basis changes. Required exact fix: “The measured hosted worst case plus a stated margin sets each named entry, except a provisional one, which keeps its own arm until its hosted window is measured:” Verification: read the revised preamble, preserve numeric rows and rerun documentation checks. Does not unclean a lens.

**R909-6-R1 - RESIDUE - Docs - `docs/testing/TESTING.md:478`.** Authority/evidence: “its N1 decision” leaves a review-finding label in authoritative prose. Impact: wording provenance only; count and policy unchanged. Required exact fix: “So #979 adds a twenty-seventh worker, as the selector's new-suite steps provide when a provisional figure leaves a worker over its budget.” Verification: compare the sentence and retain the 27-worker count and 1276-second bound. Does not unclean a lens. The historical documentation correction adds no source comments; R910-4's unchanged source-comment assessment stands.

**Retained optional suggestions**

Every following item is SUGGESTION, remains optional and leaves coverage clean. Artifacts are unchanged; no new execution is implied.

| IDs; lenses | Artifact and evidence | Impact; suggested outcome; verification |
|---|---|---|
| R909-2-S3; Tests | `input_loopback_dp/run.py:34-38`, reduced-frequency recipe | Release-clock parent behavior remains outside proof; optionally add that leg and require the same wire assertions. |
| R909-2-S4; RTL | `KL_render_queue.sv:821`, final map-read scheduling | Unused one-past read remains cleanup; avoid it and verify final destination/copy deadline. |
| R909-3-S1; Tests | `input_loopback_dp/sim_main.cpp:44-45,609`, 48-word peak equals bound | Scheduling changes may trip zero headroom; document latency meaning or justify a revised bound while preserving missing-output detection. |
| R909-3-S2; Robustness/Tests | `input_loopback_dp/sim_main.cpp:639,747`, uncapped walk waits | A stalled-walk plant can hang standalone campaigns; cap waits with a named failure and test stopped-walk behavior. |
| R909-3-S3; Docs | `INPUT_MAPPED_LOOPBACK.md:65-71`, sensitivity only in PR/receipts | Improve post-merge discoverability; link dated current routes, checking against all six results rather than presenting old figures as current. |
| R910-3-S1; Robustness/Tests/Docs | `input_loopback/sim_main.cpp:21-30`, conversion lacks range checks | Oversized ad hoc controls can wrap; reject range/domain errors and test unset, valid, malformed and overflow inputs. Fixed published bounds cases are unaffected. |
| R909-4-S1; Tests/Docs | Historical cold receipts; TESTING.md:472-473 | Preserve wall-clock/CPU-set/load evidence for those claims and compare it with the cited runs. This review does not retroactively authenticate those details. |
| R909-4-S2; Tests | Builder `--list`; deferred imports in `test_input_loopback.py:17-22` | Later eager imports may regress inventory without submodules; add a permanent submodule-free control and compare all 114 names. |
| R909-5-S1; Docs | CI_WORKFLOWS.md:687, “from cold local runs” | Clarify cold runs justify timeout margin while the driver arm supplies the planner figure; verify against TESTING.md:469-474. |
| R909-5-S2 / R909-6-S1; Docs | `suite_shards.py:150-151`, “step 3” | Replace with “the module docstring's new-suite contract” and verify it resolves. This wording predates the reviewed delta. |
| R909-6-S2; Tests | Loopback fixtures omit same-stream fan-out to two inputs | Optionally bind one stream to two inputs and grade both selected channels on the wire; require a missing recipient to fail. |

**Hosted evidence**

All four runs completed successfully on 2026-11-25 and identify PR head `09201d35d7ea720b3ba205da185ba35c159ec24a`:

| Run | Executed evidence |
|---|---|
| [rtl-fast 45657606423](https://github.com/kebag-logic/milan-fpga/actions/runs/45657606423) | All 19 listed jobs succeeded, including `rtl-fast`. |
| [elaborate 45657606201](https://github.com/kebag-logic/milan-fpga/actions/runs/45657606201) | Five gate jobs and aggregate succeeded. |
| [docs 45657606171](https://github.com/kebag-logic/milan-fpga/actions/runs/45657606171) | `docs-gates-0..2`, `docs-check`, `docs-check-no-git`, `wire-accountability` executed successfully. |
| [rtl-full 45657606190](https://github.com/kebag-logic/milan-fpga/actions/runs/45657606190) | 27 simulation shards, four synthesis shards, preflight, eight case unions and both exhaustive aggregates succeeded. Physical gPTP skipped. |

The full workflow has 48 jobs; pagination was checked. Aggregate ownership/SHA reconciliation steps executed successfully. Skipped cache-install steps are not confused with skipped test jobs. Physical-gPTP skipping supplies no physical proof.

Worker logs identify checkout `649acf4c775dd7e9bfbdf81f5d7a3d91782cd327`, the hosted merge of this head into `5de21ff3661436ea5598718aca36934361e35340`. These are exact-PR-head-associated results, not the final current-dev candidate. Workers 15 and 14 record `PASS input_loopback` and `PASS input_loopback_dp`; timestamped excerpts are retained. Hosted suite windows are now available for the manager's provisional-estimate reconciliation. Hosted/replica acceptance remains with the manager.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #979/#818; design:397-413; timeout table; current source-bound routes; unchanged integration causes | R910-5 closures/recheck; R910-4 unchanged scope | 09201d35d7ea720b3ba205da185ba35c159ec24a |
| RTL | CLEAN | Current subtree/input hashes; six routes and selected floors; unchanged queue/capture/parent contracts | R910-5 route closure; R910-4 unchanged implementation | 09201d35d7ea720b3ba205da185ba35c159ec24a |
| Robustness | CLEAN | Eight timeout arms/default; per-stream phases/plants; five-guard limits; unselected route miss preserved | R910-5 bounded recheck; R910-4 unchanged scope | 09201d35d7ea720b3ba205da185ba35c159ec24a |
| Tests | CLEAN | Docs receipts; 64-file audit; 24 raw timing summaries; hosted execution records; unchanged scoreboard/plants | R910-5 evidence closure; R910-4 unchanged test scope | 09201d35d7ea720b3ba205da185ba35c159ec24a |
| Docs | CLEAN, two residues carried | CI_WORKFLOWS:680-694; TESTING:468-479; author-r6b/r8; corrected verdict attribution; docs gates | R910-5 | 09201d35d7ea720b3ba205da185ba35c159ec24a |

**Limits and pending manager duties**

- No manager source bank was run or inferred. Source execution evidence remains published author receipts and the identified hosted jobs. No full local simulation, processor, synthesis or builder bank, compiler build, implementation run, hardware operation, container run, host orchestrator or sub-agent was used.
- Physical calibration is **NOT RUN**. Field skips, simulation and implementation timing are not hardware proof. No bitstream or board result is claimed. Enabled 8x8 remains refused S14 debt.
- The manager must construct the actual current-dev candidate, run required builder/native banks, re-establish routes if physical dependencies change, and link exact-candidate receipts. Supplied live-dev `e275d7950ef3385753e6a15d2e191ba855b171ed` is not treated as a completed candidate; refresh the actual base at merge time.
- The manager owns hosted/local-replica acceptance and replacement of provisional estimates using the available windows, including reboot's separate history. Carry residues/suggestions, obtain the other independent review, wait for every review round, and apply remaining completion/containment rules and explicit merge authorization.
- `verify_checkout.py <checkout>` verifies 1,983 superproject blobs and 120/868/67/100/214 blobs in five initialized submodules directly against pinned bytes/modes, with matching indexes. Required gitlinks match; the uninitialized `external` gitlink is preserved. HEAD/tree match and tracked status is clean. No tracked restoration was needed.
- `MANIFEST.sha256` lists publishable receipts/scripts relative to this packet. Scratch downloads/dependencies are excluded. Only listed files and this report are intended for publication.

R910-5 FINISHED
