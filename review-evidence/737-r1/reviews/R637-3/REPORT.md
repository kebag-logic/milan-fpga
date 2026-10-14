[R637] POSITIVE - exact head 84ee9ea119b548b4982d2c0988d8753a2ce4d0cf

External independent review, R637-3, issue #737 / PR #739. Exact tree: `4d44778bb1074178effb49e07480a33d95e8fd6d`. All five lenses were applied. No BLOCKER, MAJOR or MINOR remains in the assigned source delta. This is a source-review verdict, not acceptance of hosted timing, a signed build, or authorization to merge.

The review reconstructs the operating contracts, documentation index, frozen issue and public decisions, requirements/interfaces, source history and diff, then public executable evidence. The full comparison is `fa7347fc59173f90e4feec2df207692e6e6e72ec..84ee9ea119b548b4982d2c0988d8753a2ce4d0cf`; the focused delta is `2658a64c408bf87ae36574f36a6deeb34b2f297f..84ee9ea119b548b4982d2c0988d8753a2ce4d0cf`. Prior public findings were reconciled after the independent delta pass. No private author material or other checkout was used.

Governing authorities are the [round-three assignment](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6176299708), [author READY](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6180445253), original assignment `6160775078`, driver ruling `6160937413`, topology ruling `6161122704`, fail-fast rulings `6161180121` and `6162403147`, CPU rulings `6166855177` and `6167288337`, and round-two rulings `6169768594`, `6169805715` and `6172868895`. `REQUIREMENTS.md` section 8, `CONTRIBUTING.md`, `docs/testing/CI_SIGNATURE.md`, `docs/testing/CI_WORKFLOWS.md` and the driver/receipt interfaces remain authoritative. Image adoption, signing, evaluated skip authentication and trigger migration remain outside this fixes-only delta.

Public source evidence was read at [evidence commit 8fc0bb24](https://github.com/kebag-logic/milan-fpga/tree/8fc0bb247606c9eb1eeeebc57e26a4df1f549790/review-evidence/737-r1/author-r3). `public-receipt-index.json` binds the nine receipts used below by URL, size and SHA-256. Source-head gate receipts are the author's. There is no manager source bank at this exact head.

## Findings and prior-finding resolution

No new finding. No wording-only RESIDUE was added by this round.

| Prior finding | Disposition at this head | Cause-level evidence |
|---|---|---|
| R637-2-F1, MAJOR, Conformance/RTL/Robustness/Tests | Resolved | `ci_workflow_plan.py:121`, `ci_runtime_evidence.py:127` and `ci_fail_fast.py:108` share the committed raw-to-expanded mapping. Both readers refuse invalid raw status/conclusion/steps and overlap in either order. `runtime_evidence.log` exercises the retained hosted shape through the production collector entry point and graph; `observer-probe.log` independently checks raw observations. Skips become skipped legs and incomplete evidence, never successful execution or cancellation. |
| R637-2-F2, BLOCKER, Conformance/RTL/Robustness/Tests | Resolved | `ci_suite_workflows.py:14` and `:21`, `ci_runtime_workflows.py:109`, `ci_gate_workflows.py:154`: all thirteen generated inventory readers receive unconditional pinned preparation before reading. Removing preparation from each reader is refused in `gate_workflows.log`. `fresh.log` and `fresh-result.json` start with all submodules absent, execute the generated preparation, and pass all six inventories through production collection. |
| R637-2-F3, MAJOR, Conformance/RTL/Robustness/Tests/Docs | Resolved | `ci_runtime_evidence.py:196` and `:213`, `ci_fail_fast.py:138` and `:162`, `ci_runtime_workflows.py:79` and `:109`: exhausted observer reads return zero with explicit output, retain unknown results and cannot authorize cancellation. The collector has 900 seconds against a shared 600-second read budget. `observer-results.json` covers both entry points; genuine terminal failures still request sibling and own-run cancellation. The documented behavior now matches. |
| R636-2-F1, MAJOR, Conformance/RTL/Robustness/Tests/Docs | Resolved for the assigned worker-sizing correction | `ci_gate_workflows.py:24`, `:60`, `:127`; `ci_events.py:4387`, `:8834`; `ci_suite_workflows.py:68`; workflow policy worker table. Both contract gates occupy their own source-derived worker, all 5,209 arms pass, and cold Yosys preparation is a prerequisite outside synthesis workers. Every recorded worker projection fits its own 60% bound. Whole-workflow acceptance remains pending, as detailed below. |
| R636-2-F2, MINOR, RTL/Robustness/Docs | Resolved | `ci_runtime_workflows.py:29`, all source-build template recipes, workflow policy resource paragraph, public `round3-source-sizing.json`. The eight-compiler bound is consumed by the recipes. Both tools at both CPU widths have zero memory events and at least 38.713% cap reserve. Recipe input digests match this head. |
| R636-2-S1, S2, S4 | Resolved | `probe_controls.py` removes each production guard in memory. All three current self-tests fail at their intended assertions; `mutation-results.json` and three raw logs retain the failures. |
| R636-2-S5(b) | Resolved | Watcher observer exhaustion now returns success with explicit observer output. An independent collection probe confirms that its unknown result survives a successful API job conclusion. |
| R636-2-S3 and S5(a) | Retained optional follow-up | Hosted concurrency capacity and cache-hit/miss execution differences remain on the #495 checklist under assignment item 7. They grant no authenticated-equivalence claim here. |

Earlier findings were also checked for regression at their causes:

| Earlier finding | Disposition | Current evidence |
|---|---|---|
| R637-1-F1, nested capture compilers | Remains resolved | Actual child Makefile recipes consume the divided budget at 4/12/16 CPUs; the unlimited-child negative control fails (`gate_workflows.log`). `ci_suite_pieces.py:70` bounds the capture pool and child environment. |
| R637-1-F2, collector and watcher-tail cancellation | Remains resolved | Collector included in watcher expectations; collector does not depend on watcher; terminal guard depends on both. `fail_fast.log` covers all generated graphs and fork restrictions. Independent tail probes retain eight genuine-failure cancellation cases. |
| R637-1-F3, cache-policy documentation | Remains resolved | `CI_WORKFLOWS.md:1582` and `:2777` consistently require exact installation keys without broad fallback; `ci_install_workflows.py` and its controls agree. The separately documented synthesis-result cache is a different cache. |
| R636-1-B1, missing inventory prerequisites | Resolved through R637-2-F2 | Fresh collector preparation and thirteen reader-removal controls cover the downstream cause as well as original union/aggregate consumers. |
| R636-1-B2, ambient fixture identity | Remains resolved | Receipt fixtures use the shared explicit-identity commit helper; receipt controls pass. |
| R636-1-F1/F2, skipped matrices and observer errors | Resolved through R637-2-F1/F3 | Shared mappings, negative forms, bounded retries, explicit observer outputs, incomplete manifests and zero-write probes. |
| R636-1-F3, borrowed timeout/headroom | Remains resolved | `suite_shards.py --selftest` passes worker-specific bounds and bound-removal controls; round-three gate and Yosys sizing closes the remaining worker cases. |
| R636-1-F4, resource evidence | Remains resolved, including R636-2-F2 | Public prior workload receipts are supplemented by the four bounded source-build measurements; current code retains 8 GiB/job and four-job admission. Concurrent slot peak remains a replay duty. |
| R636-1-F5, untested failure conclusions | Remains resolved | `ci_fail_fast_selftest.py:148` separately tests failure/cancelled/timed_out/action_required. Independent terminal probes also exercise all four. |
| R636-1-F6, nonpublic comparison source | Remains resolved at the publication cause | Public `round2-case-evidence/comparison-summary.json` binds all six comparisons to fetchable `cf9c936697a06e44c41681bcc12dc612a3242eb2`. This delta changes no suite driver. These earlier comparisons are not represented as current-dev candidate execution. |
| R636-1-S1/S2/S3 | S1/S2 resolved; S3 retained optional | Same causes as R636-2-S4/S2/S3 above. |
| R636-1-S4/S5 | S4 documented; S5 retained optional | `run_all_suites.sh:398` explicitly states that pieces retain the parent suite timeout. Hosted/replay observation of MAKEFLAGS-sensitive controls remains a manager check; existing NOT RUN arms are disclosed and not promoted to coverage. |

## Independent executable evidence

The focused checks ran concurrently under one foreground driver, at most four independent checks at once. No full product, synthesis, builder or parent bank was run. No host orchestrator or its self-test was executed.

`focused-results.json` records the commands, exits and elapsed seconds. All nineteen intended checks pass after correcting one review invocation: the first bare-metal check omitted its required `--check` flag and exited 2; `baremetal-corrected.log` records the proper invocation returning zero with 0 findings across 1,331 tracked first-party files. That usage error is retained, not counted as a source defect.

- `ci_events.py --check`, `ci_gate_workflows.py --check`, evidence-pin checking and `suite_shards.py --selftest` pass.
- `ci_events.py --selftest` passes 2,186 contract items and 5,209 arms in **182.589 seconds**. This is reviewer-local timing, not a hosted result. The changed optimization regenerates the mutated workflow for each generated arm; it does not remove the arm or relax the ordinary full-tree contract.
- Gate, case, make-case, MAAP, capture, suite-piece, suite-collection, fail-fast, runtime-evidence, installation-cache, workflow-plan and manifest controls pass.
- `fresh-result.json`: the generated submodule preparation succeeds from an unprepared checkout. Inventories contain **19 / 31 / 31 / 66 / 3 / 4 cases** for datapath, media-clock, capture, MAAP, render and protocol-shadow respectively. Synthetic unions exercise dependency availability and transport only. No suite was executed by this probe; its manifest is incomplete and equality is refused.
- `observer-results.json`: **14 outage injections** cover collector and watcher for 403, 429, 500, 502, 503, timeout and retry-budget exhaustion. Every case returns zero, emits observer output and performs zero writes. Virtual waits reach 360/480 seconds, beyond the old collector allowance. Collector manifests remain incomplete and cannot compare equal. A watcher-error receipt remains unknown even when API collection reports that job successful.
- Eight genuine terminal-failure cases still issue cancellation requests. Malformed raw matrix observations and raw/expanded overlap in both orders are refused. The retained graph controls cover complete raw-skipped runs with no fabricated success.
- S1/S2/S4 guard-removal probes each return 1 at the expected assertion. Their unmutated self-tests return zero.

The round-three `git diff --check` passes. The full-range check reports whitespace only inside unchanged unified-diff context in `ci/act/fail-fast.patch`; those leading context markers are patch syntax, not introduced round-three source whitespace. Both outputs are retained in `diff-check-results.json` and the associated logs.

Reproduction scripts accept the reviewed checkout as their first argument. `fetch_public.py` retrieves the pinned public receipts required by `audit_source.py`. `probe_fresh.py` expects a new `scratch/fresh-checkout` destination. All disposable clones, fixture repositories and generated probe data stay under `scratch/`, which is excluded from publication.

## Worker budgets, resources and timing risk

`source-audit.json` checks all 26 published worker projections against their own bounds and rechecks the arithmetic. These are projections supported by recorded measurements, not observed hosted after-times.

| Worker | Projected seconds | Own 60% bound | Margin |
|---|---:|---:|---:|
| docs-gates-0 | 922 | 1620 | 698 |
| docs-gates-1 | 1506 | 1620 | 114 |
| docs-gates-2 | 553 | 1620 | 1067 |
| elaborate-gates-0 | 1561 | 1620 | 59 |
| elaborate-gates-1 | 713 | 1620 | 907 |
| yosys-tool, cold | 720 | 1044 | 324 |
| yosys-shards 0/4 | 554 | 1044 | 490 |
| yosys-shards 1/4, 2/4, 3/4 | 85 / 92 / 91 | 1044 | 959 / 952 / 953 |

Docs worker zero recomputes to `2039 - 1065 - 37 - 99 + 23.699 + 60 = 921.699` seconds. The contract worker uses the conservative public 316.686-second self-test, 113.654 seconds for both runner-contract invocations, two checking seconds and 120 seconds of setup/evidence allowance: 552.34 seconds, rounded up to 553. Every original gate remains assigned exactly once. Existing worker timeouts are unchanged in this delta. The collector's explicit 3-to-15-minute change is the separately authorized observer-budget correction, not a timing-target workaround.

The source-build receipts bind current template and budget-generator bytes. Accepted peaks are 4,811,259,904 / 4,793,225,216 bytes for Verilator at 16/12 CPUs and 5,264,482,304 / 5,117,616,128 bytes for Yosys. All use eight compilers, return zero, and record zero memory events. Their recorded intervals do not overlap. Reserve is 43.990% / 44.200% / 38.713% / 40.423%. Unrestricted builds are explicitly rejected sizing counterexamples. Capture remains the largest accepted class at 6,047,100,928 bytes, leaving 29.602% of the 8-GiB cap. Four caps plus 4 GiB overhead equal 36 GiB; the sum of separate peaks is not a measured concurrent slot peak.

**The docs 30-minute target is not proved.** The published shipping-width projection is 1,776 seconds including aggregate, collector, one watcher interval and terminal guard. Substituting the later contended, single-child builder measurements produces the author's 1,802–1,806-second estimate. That is a real acceptance risk, not harmless wording. I do not treat it as a confirmed source defect: the measurements use a different concurrency/CPU-sharing setup, and the assignment explicitly leaves hosted wall-clock acceptance to the manager. The worker itself still fits 1,620 seconds under either figure. No exception to the 30-minute docs target is granted. A hosted overrun must be addressed or explicitly decided by the owner before acceptance.

The exact-head hosted query returned no workflow runs (`hosted-runs.json`). Consequently this report claims neither executed hosted jobs nor successful skipped contexts. The public author bank binds this head and records 40 docs-check steps, the separate no-metadata docs step, and 20 rtl-fast steps across twelve jobs, all zero. Its setup is preinstalled and its measurements are not workflow spans. No manager source execution is inferred from those receipts.

## Host trust boundary and bare-metal correction

The audited runner bytes hash to **`f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`**. `source-audit.json` verifies all three helper pins and proves the runner AST differs from round two only in the helper-pin assignment. The changed planner helper adds raw matrix mappings from safe, committed workflow data; it introduces no repository command execution or candidate imports.

Static re-audit covered trusted/installed runner validation (`act_ci.py:1280`), credential-free Git setup and exact fetched refs (`:1130`, `:1832`), workflow/action restrictions (`:2038`), controlled environment (`:1607`), container launch restrictions (`:4718`), evidence directory/helper staging and isolated reader launch (`:5756`–`:5818`), and cleanup/integrity sequencing (`:5819`). Candidate workflows and bounded JSON archive members remain data on the host; the three digest-pinned readers are staged privately and run with isolated imports. `ci_runtime_evidence_selftest.py` independently exercises candidate import poisoning and modified-helper refusal without running the host orchestrator. No escape was found in this audit. Full live containment and runner acceptance remain manager duties.

Commit `0fd126de4` changes two host-OS prose lines and derives the archive name with `GO_ARCHIVE.format(sys.platform)` in `build_ci_act.py:58`. On the supported build host it selects the same `go1.25.0.linux-amd64.tar.gz`. The SHA-256 pin is unchanged, so another platform does not gain authorization for different archive bytes. The bare-metal gate's bytes are unchanged, and its check and controls pass. The public dispatcher receipt records the same binary digest as round two: `4d30fb23a2d2485ea7a48c6c679d4dd3b482eafe73d55c1ec544842f96bbd3f5`. This is checked public build evidence; I did not rebuild or run the dispatcher.

## Reviewer-owned coverage ledger

Each CLEAN entry covers the assigned delta at this exact head and retains the explicit execution limits below.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue rulings; REQUIREMENTS section 8; CI_SIGNATURE; generated workflow inventories/unions; `ci_suite_workflows.py:21`; `ci_runtime_evidence.py:127`; fresh and observer receipts; source budget projections against the frozen worker rule | R637-3 | 84ee9ea119b548b4982d2c0988d8753a2ce4d0cf |
| RTL | CLEAN | Architecture/dependency/failure paths in `ci_gate_workflows.py:127`, `ci_runtime_workflows.py:109`, `ci_suite_workflows.py:68`, `ci_fail_fast.py:108`; pinned host reader boundary; CPU/compiler consumers and worker limits. Delta contains no HDL or firmware behavior change; full-range product changes are imported by the earlier dev merge, not introduced here | R637-3 | 84ee9ea119b548b4982d2c0988d8753a2ce4d0cf |
| Robustness | CLEAN | `ci_fail_fast.py:62`, `:108`, `:138`, `:162`; collector shared read deadline; malformed/overlap/refusal paths; production-entry outage and genuine-tail probes; four bounded source-build memory receipts | R637-3 | 84ee9ea119b548b4982d2c0988d8753a2ce4d0cf |
| Tests | CLEAN | 5,209 CI contract arms; thirteen preparation-removal controls; gate union/driver controls; raw-skip/observer entry-point controls; independent S1/S2/S4 guard removals and expected failures; exact-head author gate receipts with their limits | R637-3 | 84ee9ea119b548b4982d2c0988d8753a2ce4d0cf |
| Docs | CLEAN | `CI_WORKFLOWS.md:2347`, `:2644`, `:2731`, `:2789`; CI_SIGNATURE implementation boundary; current PR body and READY; current projections, reserves, observer semantics and explicit incomplete/authentication limits compared with code and receipts | R637-3 | 84ee9ea119b548b4982d2c0988d8753a2ce4d0cf |

## Limits and pending manager duties

- This review does not accept the full issue or final current-dev merge candidate. The source base is `fa7347fc59173f90e4feec2df207692e6e6e72ec`; the assigned live dev is `f62602531d415d6c1cae1374a3cc2938faf54049`. The manager must construct the candidate from current dev at the merge turn, run its builder and native banks, and link the exact candidate receipts on the PR. No such source bank is claimed here.
- Manager-owned replay/hosted acceptance remains: audited runner installation and content pin, full concurrent replay, per-job/workflow wall clocks and concurrent slot peak, exact required contexts, hosted no-op/full paths and live cancellation. Readback must distinguish executed jobs from skipped contexts and resolve any docs/elaboration overrun.
- Signing, pinned image/action provenance and conditional-skip equivalence are follow-up work under the public scope decisions. These collectors deliberately produce incomplete evidence where proof is missing. A review PASS does not convert that evidence into an authenticated build.
- The accepted continuous media-clock history exception remains explicit. Physical calibration is NOT RUN; field skips and software gates provide no hardware proof. Existing builder NOT RUN arms are not counted as coverage.
- No source fixes or source commits, pushes, GitHub writes, merges, author contact, delegation, privilege, shared installation, Docker execution or hardware access occurred. Full product/source-build banks were not repeated. No scoped Verilator executable was used, so no new compiler identity or simulation result is claimed.
- Final `audit_source.py` checks all **1,357 tracked parent blobs** directly against Git object bytes and executable modes, checks the complete index against the tree, and verifies every required initialized submodule at its gitlink with clean status. The optional `external` gitlink remains uninitialized. Head and tree remain exactly as assigned.

Only `REPORT.md` and files listed by `MANIFEST.sha256` are publishable. Scratch trees are excluded.

R637-3 FINISHED
