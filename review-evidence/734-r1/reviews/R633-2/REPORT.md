[R633] NEGATIVE - exact head 33ac35b54648ef919227c5dd8b9abc97fa6bedbd

Round R633-2, external review of issue #734 / PR #735. Tree `42ffc92e382df24433ffc80333174e7d03ab4006`; source base `a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0`. All five lenses were applied. One new MAJOR remains open: the runner's documented standalone, isolated self-test invocation fails. The corrected live-base selectors passed the focused checks, including restored RTL.

Scope follows the [frozen issue](https://github.com/kebag-logic/milan-fpga/issues/734), [assignment](https://github.com/kebag-logic/milan-fpga/issues/734#issuecomment-6151273761), and [round-2 decision](https://github.com/kebag-logic/milan-fpga/issues/734#issuecomment-6151933918). Authorities read were AGENTS.md, CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md:305-317, and docs/testing/CI_WORKFLOWS.md. The complete eight-file diff and both commits were examined, including `0519ff36..33ac35b5`. Public execution evidence came from [the pinned evidence tree](https://github.com/kebag-logic/milan-fpga/tree/872d08f828de11c7e3b4919afd3d75cce3c2f999/review-evidence/734-r1). No manager source bank at this head is claimed.

**Finding R633-2-F1: MAJOR. Lenses: Conformance, RTL, Robustness, Tests, Docs.**

Artifact: `scripts/act_ci.py:6201`, :6205, :6218, :15143; `docs/testing/CI_WORKFLOWS.md:1571-1593`. RTL attribution covers the runner architecture and interface contract.

Authority/evidence: the documented installation copies only the audited runner, makes it non-writable, and runs `python3 -I <installed>/act_ci.py --selftest --worktree <candidate>`. The policy explicitly supports a flat install without a copied repository shape and requires isolated imports. The new unconditional `selftest_scope_event` imports the sibling `ci_scope_history` module. Isolated mode excludes that sibling from the import path; a flat installation does not contain it at all. The call also uses `ROOT` for history and workflow reads instead of the explicit `shipping_root` supplied by `--worktree`.

Reproduced inside disposable unprivileged jobs, without host runner execution:

| Invocation | Result | Receipt |
|---|---|---|
| Base runner, copied alone with mode 0555; `python3 -I /work/act_ci.py --selftest --worktree /src` | PASS, rc 0 | `receipts/runner-flat-parent.log`, `.json`, `.rc` |
| Exact-head runner, identical installation and arguments | FAIL, rc 1, `ModuleNotFoundError: No module named 'ci_scope_history'` | `receipts/runner-flat-head.log`, `.json`, `.rc` |
| Exact-head repository runner with `python3 -I scripts/act_ci.py --selftest` | Same failure | `receipts/runner-isolated-python.log`, `.json`, `.rc` |
| Exact-head ordinary CI invocation, `python3 scripts/act_ci.py --selftest` | PASS, 552 checks | `receipts/runner-selftest.log`, `.json`, `.rc` |

Impact: the supported isolated installation cannot complete its offline construction and negative-control gate. The ordinary CI invocation does not detect this regression, and the authoritative supported-invocation claim is false at this head. This is an execution/interface defect, so it is not wording residue. No live replay failure is asserted.

Required outcome: preserve the documented standalone audited-file interface, isolated imports, and the explicit candidate-worktree selection while exercising the new scope controls. Do not grant candidate Python host import authority to obtain a pass. Verification: the exact documented non-writable flat-install command must pass in a disposable boundary, and a control must detect loss of standalone/isolated support. Retain the ordinary self-test and all live-base history controls.

**Prior findings explicitly reconciled at this head.**

| Prior ID | Disposition | Evidence |
|---|---|---|
| R632-1-F1, BLOCKER, all five lenses | RESOLVED | Hosted first-parent comparison in all three selectors; replay unique merge base against the verified live ref. Current REV and REV+E retain `hdl/x.sv`. `receipts/prior-probe.log`, `receipts/independent-scope-final.log`, and 42 killing scope mutations. |
| R632-1-F2, MINOR, Docs | RESOLVED | CI_WORKFLOWS.md:663-691 lists the four decision bindings and their expressions; :778 has four fast bindings; :877-881 lists the three elaboration bindings. Matches the workflow mappings and CI-events records. |
| R633-1-D1, RESIDUE, Docs | RESOLVED | The same corrected decision-variable lists and counts resolve the duplicate wording finding. |
| R632-1-F3, SUGGESTION, Tests | RETAINED | Removing `failures += history_selftest(ROOT)` at ci_scope.py:524 still lets both its self-test and CI-events check pass. Reproduced in a disposable clone: `receipts/history-wiring-suggestion.log`. |

The retained suggestion's authority/evidence is the executable-history claim at CI_WORKFLOWS.md:199 and the mutation above. Impact: the history checks can become disconnected without those two gates detecting it. Optional outcome: independently guard the history invocation or its executed population. Verification: the disconnection mutation should fail. It remains optional and does not independently unclean a lens. The earlier criss-cross observation is addressed: the replay now requests all merge bases and rejects ambiguity; hosted scope uses the concrete merge's first parent.

**Finding R633-2-D1: RESIDUE. Lens: Docs.** Artifact: PR #735 body, Status, recorded in `public/pr-body.md`. Evidence: the published PR head is `33ac35b54648ef919227c5dd8b9abc97fa6bedbd`, but the live body still says “The new commit is local and unpushed.” Impact: stale publication wording only. Exact fix: delete that sentence. Verification: read the updated body against the published head. This does not affect the verdict or lens cleanliness; the manager may carry it on the residue checklist.

**Behavior and verification results.**

The three actual YAML step bodies were executed independently, using explicit path and relevance expectations. The reviewer extractor uses the parsed workflow mappings; it removes only the recursive classifier self-test call. The complete classifier self-test was separately executed.

- Hosted scope at `rtl.yml:115-126`, `rtl-fast.yml:47-58`, and `elaborate.yml:104-115` compares `GITHUB_SHA^1` with `GITHUB_SHA`, with rename detection disabled. Each checkout explicitly requests full history. Missing merge objects fail the step.
- Replay scope uses `PR_BASE_REF` and `PR_HEAD_SHA` bound to the event. `act_ci.py:1838` fetches full base/head history and checks the fetched base against `run.validation_base`. The unchanged payload keeps the recorded oid as metadata. Missing, unrelated and ambiguous replay ancestry fails without a docs-only output.
- REV and REV+E were constructed with actual dev merges, an RTL restoration, and a later documentation edit. The independent hosted fixtures force a two-parent synthetic merge and verify its first parent. Both hosted and replay paths are exactly `docs/a.md` and `hdl/x.sv`, with `rtl=true`.
- Documentation, RTL, mixed, RTL deletion, rename into documentation, a gate-read documentation page, a documentation-shaped gitlink, and empty-delta cases all match their explicit expectations. Draft RTL stays relevant while deferring exhaustive execution. Fast push rewinds keep the endpoint comparison; unknown push bases enumerate tracked files. Full and elaboration non-PR paths remain unconditional.
- B16 was reproduced from real objects: `49da9fd9` versus `f1b2489f` gives 64 endpoint paths with default rename detection, 65 with `--no-renames`, and two merge-base paths. Against the actual landing merge's first parent `e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c`, both hosted and replay selectors list only `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and `docs/findings/README.md`; all three publish `rtl=false`.
- The unchanged public `probe_scope.py` was run verbatim, then its unchanged functions were called with explicit current/previous revision constants. Its nine current-head outcomes were graded separately because the original program always exits zero. The original REV case permits a fast-forward; the independent probes above additionally verify a true synthetic merge.

| Gate or probe | Result | Receipt |
|---|---|---|
| `ci_scope.py --selftest` | PASS; 180 assertions, 42 killing scope mutations | `receipts/ci-scope.*` |
| `ci_events.py --check` and `--selftest` | PASS; 2021 contract items, 2846 arms | `receipts/ci-events.*` |
| Ordinary contained `act_ci.py --selftest` | PASS; 552 assertions | `receipts/runner-selftest.*` |
| Isolated standalone runner interface | FAIL; R633-2-F1 | `receipts/runner-flat-head.*` |
| Independent selector probes | PASS; 95 executions | `receipts/independent-scope-final.*`, `scripts/scope_audit.py` |
| Unchanged prior probe and current-head grading | PASS; nine current-head cases | `receipts/prior-probe.*`, `scripts/probe_scope.py`, `scripts/replay_prior_probe.py` |
| Documentation, paths, style, generated contents, em-dashes, Python idiom, source-list and evidence-reader checks and controls | PASS; each invoked command exits 0 | `receipts/documentation.*` |
| Five linked image pairs, source base versus head | PASS; every ELF byte identical | `receipts/linked-images-final.*`, `receipts/linked-image-hashes.json` |
| Linked-image audit controls | PASS; 33 checks | `receipts/image-controls-final.*` |
| Public receipt and source-integrity audit | PASS | `receipts/final-audit-pass.*`, `receipts/public-evidence-audit.json`, `receipts/tree-integrity.json` |

All five image sizes match between base and head: 50752, 50752, 50744, 50768 and 50776 bytes for the five shapes listed in `linked-image-hashes.json`. The pinned SDK archive digest was verified. The reviewer compiler identifies Buildroot 2021.11-18033-g83947c7bb6; the public author receipt identifies Buildroot 2026.05. Absolute ELF hashes differ between those environments, so only reviewer base/head byte identity is claimed. No firmware, HDL, configuration, synthesis input, requirement or submodule pin changed in this PR.

The source-bound public record matches all seven listed file digests at the exact head. Twenty-one selected round-2 receipts match the publisher's manifest. Publication redactions are accounted for using `published_sha256`; original receipt hashes are checked against `original_sha256`. Author receipts remain author evidence. No other reviewer's positive verdict supplies evidence for this verdict.

The reviewer-owned ledger is:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R633-2-F1) | Issue #734 acceptance and round-2 decision; REQUIREMENTS.md:314; three selectors; CI_WORKFLOWS.md:1571-1593; standalone runner receipts | R633-2 | 33ac35b54648ef919227c5dd8b9abc97fa6bedbd |
| RTL | UNCLEAN (R633-2-F1, runner architecture/interface) | act_ci.py:1838, :2375, :6201, :15143; installed runner interface; full.diff; unchanged product trees and five image pairs in tree-integrity.json and linked-image-hashes.json | R633-2 | 33ac35b54648ef919227c5dd8b9abc97fa6bedbd |
| Robustness | UNCLEAN (R633-2-F1) | REV/REV+E, missing/unrelated/ambiguous ancestry, deletion, rename, pointer, empty, push and draft probes; standalone import failure | R633-2 | 33ac35b54648ef919227c5dd8b9abc97fa6bedbd |
| Tests | UNCLEAN (R633-2-F1) | ci_scope_history.py; ci_events.py canonical forms and mutations; act_ci.py:6199; 95 independent executions, unchanged prior probe, contained self-tests and base/head install control | R633-2 | 33ac35b54648ef919227c5dd8b9abc97fa6bedbd |
| Docs | UNCLEAN (R633-2-F1) | CI_WORKFLOWS.md:168-206, :663-691, :877-881, :1521-1595; build_event docstring; public issue/PR and audited receipts; supported invocation contradicted by execution | R633-2 | 33ac35b54648ef919227c5dd8b9abc97fa6bedbd |

The five lenses are not released while F1 remains open. This does not reopen the resolved restored-RTL classification finding. The scope rule and its composition safeguard at CI_WORKFLOWS.md:191-196 agree with the round-2 decision; no new docs-only misclassification of contributed or restored RTL was found in this pass.

**Real limits and process record.** All executable candidate runner checks ran inside unprivileged disposable filesystem, process and network namespaces, with a read-only candidate and no host credentials, service sockets or capabilities. No host runner invocation, live PR replay, Docker execution, source edit, source commit, push, GitHub write, merge, private author access or sub-agent was used. Independent foreground commands ran concurrently and completed. No full parent/processor/gPTP/synthesis/builder bank ran; no hosted acceptance was claimed. Physical calibration NOT RUN. Field skips and linked images are not hardware proof.

There was a review-order deviation: prior public review comments contained full report text and were read after the independent diff pass but before this verdict and ledger were written. That does not meet the requested ledger-before-report ordering. The new finding is supported by the independent executable base/head comparison above. No private review or author material was read.

Initial review-environment failures are retained: `linked-images` and `image-controls` lacked a sandbox account entry for home-directory lookup; the final jobs supplied a disposable account entry. The first independent scope fixture staged an unrelated absent gitlink; the corrected fixture stages only its intended path. The initial public audit compared pre-publication hashes without the publisher's recorded redactions; the final audit checks both published and original identities correctly. None of these attempts changed the candidate or is counted as a source failure.

Final integrity checks verified all 1308 parent blobs, their tracked modes and complete index entries, plus pinned source bytes and index entries in the three required submodules. HEAD and tree match the assignment, and the worktree is clean. Required pins are protocol-processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`, gptp-processor `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`, and verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The inactive external/lwSRP gitlinks also match. No source restoration was needed.

**Pending manager duties.** Publish the report and listed receipts, route F1 for correction and re-review, carry the wording residue, and retain the optional wiring suggestion. Obtain both current-head independent reviews and finish all in-flight rounds. The manager owns trusted replay and hosted acceptance, distinguishing executed jobs from skipped contexts. At the merge turn, build and validate the current-dev candidate with builder and native banks and publish those receipts. The supplied source base and live dev are both `a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0`; no future candidate is pre-approved. Respect the 697c then 696 sequence, merge authorization, post-merge containment, and issue/board completion duties.

The final public review observation found no new comments, submitted reviews or inline findings beyond the reconciled comments; see `receipts/public-review-observation.json`.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable. Portable reproduction scripts and raw receipts are included; all disposable trees, SDK files and image binaries remain under unpublished `scratch/`.

R633-2 FINISHED
