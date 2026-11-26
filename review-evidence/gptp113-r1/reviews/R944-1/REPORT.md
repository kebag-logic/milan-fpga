[R944] POSITIVE - exact head af11b3ef631eb44cdc1730cfb31bedda95c33dc5

Independent external review of issue #113 / PR #114, round R944-1. Base: `3009f9a2a2d69375211d8355490675879033d940`. Head tree: `de4e33ba9c752220bdb0567cb6b9b5ec6c7c7e2a`. No blocking findings or residue identified in the reviewed delta. One suggestion records inherited timing sensitivity.

The two commits preserve the runner's executable behavior, retain the scheduling test's coverage, and satisfy the frozen acceptance through focused local checks and audited public author receipts. This verdict covers the source head, not the final current-dev merge candidate.

Review basis and independence:

- The supplied repository instructions were applied. This checkout contains no tracked `AGENTS.md` or `CONTRIBUTING.md`. Read `docs/README.md`, the repository README, the test guide, source-evidence ledger and integration contract.
- [Issue #113](https://github.com/Mister-M-alt/FPGA-gPTP/issues/113) freezes two requirements: unchanged consumer budgets with passing ratchets, and preservation of PR #112's scheduling-test and four-pass behavior. Moving the host-process test outside the suite directory is explicitly in scope. RTL, microcode and engine behavior are excluded.
- The [consumer pin ruling](https://github.com/kebag-logic/milan-fpga/issues/1013#issuecomment-7178757153), [PR #112](https://github.com/Mister-M-alt/FPGA-gPTP/pull/112), issue #111, consumer Rule 12, both gate implementations, their population helper and budget files establish the relevant authorities. No interface or protocol-clause change is claimed.
- Independently examined the entire diff and both commits before opening the PR discussion for prior findings. `INDEPENDENT.md` records that initial verdict and five-lens ledger. No other reviewer report was used. The issue had no comments; the PR discussion returned two review-start comments and no prior FINDINGS, inline findings, review submissions or manager execution receipts. There is consequently no prior finding to retain or resolve.
- Public executable evidence came only from the [frozen author packet](https://github.com/kebag-logic/milan-fpga/tree/dcfe275da410b7caf1f914697cd2dc68fbd5349f/review-evidence/gptp113-r1/author). All 56 files were checked against both their published Git blobs and the packet's published SHA-256 values.

| lens | CLEAN/UNCLEAN | examined artifacts and evidence | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #113 criteria; consumer Rule 12 and both budgets; scope helper's pinned-submodule refusal; public `consumer-ratchets-af11b3e.log`; complete four-file diff | R944-1 | af11b3ef631eb44cdc1730cfb31bedda95c33dc5 |
| RTL | CLEAN | Unchanged `hdl/`, microcode generator, engine harness, generator arguments and four run/replay recipes; local contract and lint passes; public clean/abort real-engine pairs | R944-1 | af11b3ef631eb44cdc1730cfb31bedda95c33dc5 |
| Robustness | CLEAN | `pass_run.py` run/stop/replay and signal paths; runner AST equivalence; local baseline/head signal, status, budget and failure checks; three targeted fault probes | R944-1 | af11b3ef631eb44cdc1730cfb31bedda95c33dc5 |
| Tests | CLEAN | `tb/engine_passes_test.py:65`, `:191`, `:354`, `:367`, `:395`, `:433`; Makefile `passes-test` wiring; all six helper calls; 71/73 head and 72/73 base locally, with inherited timing failures isolated below; public 73/73 controls and 13/13 mutation pairs | R944-1 | af11b3ef631eb44cdc1730cfb31bedda95c33dc5 |
| Docs | CLEAN | `docs/TEST_DEVELOPER.md:25`; new test location and module documentation; runner docstrings; Makefile #111/#113 comments; local docs, diagrams and source-anchor gates | R944-1 | af11b3ef631eb44cdc1730cfb31bedda95c33dc5 |

Conformance evidence: the public consumer receipt identifies consumer `c34e7d8b06` plus local pin commit `f791fdea1f`, with `gptp-processor` at the reviewed head and `protocol-processor` at `801ef2283ec793e35a2590fc6593c90313a64041`. It records both gates exiting 0 and budgets unchanged. The published budget files corroborate zero undocumented/unannotated public functions, seven permitted overlong signatures, and three wall-clock suite files. The evidence counts are 69/77 unarmed suites, 10/10 unseeded sites, 0/0 unexplained DUT readers and 3/3 wall-clock suite files. The author also published 54/54 and 105/105 gate self-tests. These are author executions audited here; no independent consumer-wide rerun is claimed.

The issue's “eight parameters” describes the aggregate overlong-signature count imprecisely. The actual limit is six parameters; the helper previously had seven and now has six. The aggregate returns from eight to the unchanged budget of seven. The PR explains this correctly. The moved file still uses host time to test host scheduling, remains in `all` through `passes-test`, and retains every assertion and plan. It ceases to count as an RTL-suite source, as explicitly permitted by the issue.

Local executable evidence:

| Check | Result | Receipt |
|---|---|---|
| Runner AST, ignoring docstrings | Identical | `receipts/equivalence.log` |
| Moved test AST, after only the documented path/signature substitutions | Identical; six call sites never supplied the removed parameter | `receipts/equivalence.log` |
| Base and head `make -j16 -C tb/verilator/engine passes-test` | Both exit 2: base 72/73, head 71/73; timing sensitivity described below | `receipts/base-passes.*`, `receipts/head-passes.*` |
| Head docs, diagrams, contract and lint | Exit 0 | `receipts/head-docs-contract-lint.*` |
| Three targeted mutations, each with a control | Controls accepted; stopping, generator-signal and print-error defects rejected | `receipts/fault-probes.*` |
| Published packet and real-engine transcript audit | All hashes match; normalization independently recomputed | `receipts/audit.*` |

All 55 transcript/status comparisons passed at each layout, as did signal cleanup, unreadable transcripts, replay directories and no-core signal deaths. The clean run completed out of order at both layouts. The base failed the requirement that all four stubs start before the failure at `-j4`; the head failed the same requirement and the requirement that four short stubs actually overlap. Both enforce upper job bounds. These same assertions and stub durations existed before this delta; AST comparison confirms their preservation. Three isolated repetitions of the unchanged budget/fail-fast groups produced five assertion failures at the base and two at the head; the final head repetition passed all six checks. Both layouts exhibited the overlap failure, confirming the varying timing sensitivity. The local stop probe accepts either termination of an already running later pass or prevention of its start. Its initial narrower assumption was corrected in the disposable probe; this was not a source defect.

The author's real-engine clean pair exits 0/0 with 179 identical normalized lines, printing 2302, 2302, 2302 and 61 passing checks. Its planted pass-1 abort pair exits 2/2 with 64 identical normalized lines; passes 2 and 3 record `stopped` and signal 15 in both layouts. Recomputed normalization removes only the published compiler/banner categories; no verdict lines are hidden. All 13 published runner mutations have equal nonzero failing-check counts at both layouts, with passing controls. These real-engine pairs and the full 13-mutation campaign were audited, not rerun locally.

Finding R944-S1 — SUGGESTION; lenses: Tests, Robustness.

- Artifact: `tb/engine_passes_test.py:256` (short-stub overlap requirement) and `:278` (all-started requirement); the corresponding unchanged checks in base `tb/verilator/engine/passes_test.py`; `receipts/base-passes.log`, `receipts/head-passes.log`, and `receipts/timing-*.log`.
- Authority/evidence: #113 requires preserving PR #112 behavior. The unchanged test uses host sleeps of 0.6 seconds to demand peak overlap, and 0.1/0.2 seconds to demand that every later pass starts before cancellation. Under the observed host load, the head reached only two overlapping stubs in one sample, and both layouts correctly stopped one later pass before it started. All started processes ended. The runner and timing-check ASTs are unchanged.
- Impact: pre-existing false-negative scheduling checks on a loaded host; this prevents claiming a fully green independent `passes-test` run here. It is not an introduced runner or coverage regression and does not contradict the audited author controls.
- Required outcome: no change required for this narrowly scoped PR. Consider a separate follow-up to coordinate stub starts deterministically while retaining bounded hang detection, job-budget assertions, and fail-fast checks.
- Verification: retain successful serial/parallel transcript and signal comparisons and planted-defect rejection; exercise the timing checks under shared-host contention at both layouts. Preserve the failing local receipts rather than presenting them as passes.

Documentation and comment review found no new bench labels, lane names, review identifiers or issue-comment identifiers in source comments. The added text describes behavior and its reason in the existing #111/#113 context. The test guide points to the correct moved file. No new measurement, certification or hardware-proof claim is introduced.

Limits and pending manager duties:

- The exact-head hosted query returned zero check runs and zero commit statuses; its empty aggregate was `pending`. There is no executed or skipped hosted context to count as proof. Hosted acceptance remains the manager's responsibility.
- No manager source bank ran at this head, and none is inferred from the author receipts. No full parent, processor, synthesis or builder banks were run during this review.
- The manager must validate the final current-dev merge candidate with builder and native banks at the merge turn and publish those receipts on the PR. The reviewed source base is `3009f9a2a2d69375211d8355490675879033d940`; the supplied live-dev reference is `e275d7950ef3385753e6a15d2e191ba855b171ed`. This report does not validate that candidate or authorize bypassing its completion bar.
- Local core limits were hard-clamped to zero; the test correctly reported its nominal one-byte case as clamped. Other core-limit coverage is from the author receipts.
- Physical calibration: NOT RUN. Field skips provide no hardware proof. No hardware acceptance or protocol certification is implied.
- All probes used disposable trees under this packet's `scratch/`. The source checkout was never edited. Final verification matched all 123 tracked blobs, executable modes and index entries to the exact head and tree, with a clean worktree. This repository has no nested gitlinks. The consumer's two project pins above are evidenced by the author's receipt, not by a local consumer checkout.

Portable reproduction instructions are in `REPRODUCE.md`. Only `REPORT.md` and the files listed in `MANIFEST.sha256` are publishable; disposable trees are excluded. No source fixes, commits, pushes, external writes or merges were performed.

R944-1 FINISHED
