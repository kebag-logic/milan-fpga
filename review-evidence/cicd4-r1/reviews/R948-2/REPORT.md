[R948] POSITIVE - exact head 6841c5e3be421dc59900b392b51cbc3c0a110471

Round R948-2, external delta review of PR #1019, relating to #1008.
Tree: `dbdf163a5c411ec9cb657608a0cb7535170d6261`.
Source base: `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`.
Previous reviewed head: `5b5b0765143593f05f5a85ecd4ab1d089d23a3e4`.

All five lenses were applied to the delta and its affected dependencies. The prior blocking findings are resolved. No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION finding is raised. This is source-review approval, not completion of #1008 or authorization to merge. The reading-order limitation below is material to the requested review procedure.

## Scope and public evidence

Read AGENTS.md, CONTRIBUTING.md, docs/README.md, [#1008 and its scope decisions](https://github.com/kebag-logic/milan-fpga/issues/1008), REQUIREMENTS.md REQ-VER-01 through REQ-VER-06, relevant CI policy sections, architecture ownership boundaries and dependency adoption records. The [corrected composition decision](https://github.com/kebag-logic/milan-fpga/pull/1003#issuecomment-7164094739) requires the timing re-key and re-deal; it does not waive the remaining acceptance criteria.

The first-parent delta contains **six commits**, including the merge of `4df125b8`; five are non-merge commits. The final commit adds the boundary classifier entry. The full source-base diff was distinguished from that delta and the already merged adoption. The PR retains `Relates to #1008` and discloses outstanding timing work. Acceptance 1 remains open: this review claims neither two complete qualifying hosted runs nor universal compliance with 1276 seconds.

The [round-one packet](https://github.com/kebag-logic/milan-fpga/tree/6be24f180ccc2c0ddda4b5d3ffa40ba09d7885e3/review-evidence/cicd4-r1/author) and [round-two packet](https://github.com/kebag-logic/milan-fpga/tree/9141378262c3331229a56c23d2c2fbb14cd87b48/review-evidence/cicd4-r2/author) supply public author evidence. `packet-verification.json` records successful SHA-256 verification of all 235 and 71 author files against their manifests' published-byte hashes. Neither archive commit contains a cryptographic commit signature. This proves published-byte integrity, not signature authentication or independent execution.

## Prior findings resolved at their causes

| Prior ID | Original severity and lenses | Disposition and independent evidence |
|---|---|---|
| R947-1-F1 | MINOR; Tests, Robustness | **Resolved.** `scripts/ci_events.py:3937` compares each campaign command's index/count with its matrix. All three COUNT+1 generator faults are refused. `scripts/ci_fast_legs_selftest.py:111` also rejects the altered generator. All 35 fast-leg contract arms pass. Removing the count checks makes all three COUNT+1 planted-arm assertions fail. |
| R947-1-F2 / R948-1-D1 | MINOR; Docs | **Resolved.** `docs/testing/CI_WORKFLOWS.md:3506` names `docs-gates-1` at 1302 seconds, explicitly 26 above 1276. Independently recomputed allowance 270, total 1572 seconds, 26.2 minutes and margin 228 seconds. |
| R947-1-F3 | MINOR; Docs | **Resolved.** `scripts/ci_gate_workflows.py:27` cites the policy's component-maxima rule: worker 3 at 1237 seconds, unchanged worker 1 at 1302. The obsolete 1046-second universal claim is gone. The comment separates 961 seconds of steps from 276 of setup. |
| R947-1-F4 | SUGGESTION; Tests | **Implemented and verified.** `test_ctrl_firmware.py:266` supplies `campaign_leg` to both `main()` and `test_ctrl_firmware_shards.py:42`. Removing this mapping in memory makes the control and AECP proofs fail. SRP continues to read its campaign selector directly. |
| R948-1-T1 | MINOR; Conformance, Tests, Docs | **Resolved.** Round two retains five original `census-leg-*.json` receipts, checksums, execution identity, replay command and output. Independently verified hashes/head/tree, unchanged reader bytes and union output against both published replay and original output. Nine faults are refused: failed arm, failed exit, lost rule witness, missing arm, missing leg, duplicate leg, wrong head, wrong tree and wrong inventory. |

The census receipts belong to `530149b5dd1a94cc5011b17c9bb28af54bc79be3`. They are not relabelled as current-head execution. Another control proves they are refused under the current head/tree identity. This review called the unchanged union reader directly against the live inventory with the recorded execution identity; it did not rebuild the census or rerun its CLI in a historic checkout. See `delta-probes.log` and `evidence-comparison.log`.

## Artifact-specific results

**[R948] PASS Conformance - #1008 acceptance 2-3; `.github/workflows/{rtl-fast,docs}.yml`; `scripts/suite_shards.py:108`; retained receipts.** Workflow bytes equal the previous reviewed head and current regeneration. Required contexts, timeouts, command ownership, cancellation and fork conditions retain their prior reviewed behavior. No timeout was raised. Independently re-compared historical logs: 844 control verdicts, 398 AECP verdicts and 662 SRP defect verdicts match the serial multisets, including first-failure detail. Each SRP leg retains both pin controls. These are historical comparisons, not merged-head campaign execution.

**[R948] PASS RTL - diff against `4df125b8`; `docs/reference/SUBMODULES.md:1071`; gitlinks; `ctrl_mutants.py`; campaign/census dispatch.** Production RTL, configurations, synthesis inputs, imported harnesses and pins equal the merged adoption's bytes. No additional clock/reset/CDC/interface edit exists above that adoption. Examined the signed-delay/public unsigned-clamp boundary, imported link-delay tests and ADP acceptance changes for scheduling dependencies. The enlarged control table is included by live enumeration: 847 defects deal as 212/212/212/211. AECP and SRP remain 199/199 and 332/330. Census host/rider grouping and reader are unchanged by this delta.

The imported base has its own [published candidate validation claim](https://github.com/kebag-logic/milan-fpga/pull/1016#issuecomment-7185882185), not a manager source bank at this head. Its [merge notice](https://github.com/kebag-logic/milan-fpga/pull/1016#issuecomment-7185903645) reports an unresolved post-merge audit; this review does not certify that audit's closure.

**[R948] PASS Robustness - `ci_events.py:3937`; `ci_fast_legs_selftest.py`; `test_ctrl_firmware_shards.py:168`; `census_legs.py:75`.** Exercised missing/duplicated work, wrong counts/index, repeated phase, unauthorized campaign selection, failure/cancellation propagation, lost rule evidence and identity mismatches. Failed census legs still fail the aggregate when their judge is skipped. Unchanged prior robustness coverage is retained; the previous exhaustive fault population was not rerun.

**[R948] PASS Tests - `probe_delta.py`; `compare_evidence.py`; `checks.json`; published gate logs.** Six focused groups passed: current event contract (2409 items), workflow byte check, fast-leg controls, scheduling controls, documentation gate and independent delta probes. The probes cover the count checker and its killing control, dispatch mapping, retained receipts and merged enumeration. The author's exact-head summary reports 40 successful commands and the full event self-test at 2409 items/6174 arms; selected underlying logs were checked. That full self-test was not repeated. `ctrl_configs.py:171` correctly classifies the fast-leg self-test as compiling no firmware: campaign calls are stood in for, and the independent text scan finds no unlisted program.

**[R948] PASS Docs - `CI_WORKFLOWS.md:3453`, `:3468`, `:3506`; `ci_gate_workflows.py:27`; PR body and receipt provenance.** All 27 policy rows and margins equal the live deal. Regular maximum: 1275 seconds on workers 0 and 25. Worker 26 retains the explicit 1530-second exception. Raw logs independently yield 672 and 679 seconds for `gptp_shadow` at pin `3ce71b76`; the larger value is correctly keyed. The later log carries the merged adoption's suite content. The earlier observation predates its final suite changes, so these do not prove two runs of final content; the PR discloses that limit. Added source comments contain no new prohibited lane, round, reviewer or issue-comment labels.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #1008, generated workflows, timing logs, historical verdict comparison, original census receipts | R948-2 | 6841c5e3be421dc59900b392b51cbc3c0a110471 |
| RTL | CLEAN | Diff against imported base, dependency map/gitlinks, control inventory, dispatch/census interfaces | R948-2 | 6841c5e3be421dc59900b392b51cbc3c0a110471 |
| Robustness | CLEAN | 35 contract arms, count/mapping faults, aggregate controls, nine retained-receipt faults | R948-2 | 6841c5e3be421dc59900b392b51cbc3c0a110471 |
| Tests | CLEAN | `checks.json`, `delta-probes.log`, `evidence-comparison.log`, published exact-head gate logs | R948-2 | 6841c5e3be421dc59900b392b51cbc3c0a110471 |
| Docs | CLEAN | Policy figures and 27 rows, generator comment, PR scope, receipt provenance, added comments | R948-2 | 6841c5e3be421dc59900b392b51cbc3c0a110471 |

## Limits and pending duties

**Reading-order disclosure:** the initial discussion response included prior-round review bodies before the independent diff pass finished. This breached the requested exposure order. No current-round peer report or private author material was read. Conclusions above have independent checks and falsification receipts, but this session cannot claim the requested strict prior-report isolation.

No campaign build, full parent/processor/gPTP/synthesis/builder bank, container replica, host replica orchestrator or its self-test, hardware operation, source fix, commit, push, GitHub write, author contact or sub-agent was used. No scoped compiler was invoked. Small checks ran concurrently as bounded children of a foreground command, and every child was awaited. Disposable outputs stay under this packet's `scratch/`.

`tree-integrity.json` verifies all 1987 parent tracked blobs against raw committed bytes and executable modes, all 1993 index entries against the tree, and all five initialized dependencies' heads, blobs, modes and indexes. The intentionally uninitialized external gitlink is retained. Tracked status is clean. Mutations were in memory; no source restoration was needed.

The manager still owns:

- Exact-head hosted and local-replica acceptance, distinguishing executed jobs from skipped contexts. This review makes no current-head hosted-success claim.
- Remaining #1008 overruns, a second complete timing observation and frozen acceptance closure. After-change runner-minute figures remain projections.
- Reconciliation of the imported base's publicly outstanding containment audit.
- Construction and full validation of the final current-dev candidate, including builder/native banks, exact candidate identity and published receipts. The supplied reference is `e275d7950ef3385753e6a15d2e191ba855b171ed`; use the actual current tip at merge time.
- All review rounds finishing, merge authorization, post-merge containment and issue/project disposition.

There is **no manager source bank at this exact head**. Source execution evidence is the author's published gate receipts. Physical calibration is **NOT RUN**. Field skips and desk checks are not hardware proof.

Portable scripts and publishable receipts are listed in `MANIFEST.sha256`. Only those files and this report are publication outputs; `scratch/` is excluded.

R948-2 FINISHED
