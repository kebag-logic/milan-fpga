[R516] POSITIVE - exact head 72d3780d23a0b96362f8ae64059311b866ff5776

R516-3, independent composition acceptance for issue #673 / PR #681.
The composed tree introduces no defect beyond the reviewed sources.
All five lenses are CLEAN within this composition scope.
No BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION remains open.
This verdict does not grant final merge acceptance.

Candidate tree: `286ad25c56908e8d1987ae90db41a474c70a6fba`.
First parent: `28cdb5891b2b2d8a79b94a5bc2fb703c9fa8c721`.
Reviewed PR source: `793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df`.
Their common base is `bd884631684ccf5060339efa92263d5c3e5c262c`.
Observed live dev is `6a05347d4e2ec1dcb37d4e5806c7767537de3ce0`.
Its tree and the candidate's first-parent tree both equal
`638460d733e73eedf8e4aa9844d1f04766157528`.
The assigned predecessor tree therefore matches observed live dev.
The manager must still check dev again at the merge turn.

Reconstruction followed the requested order: operating rules, documentation
index, public acceptance and scope decisions, verification authorities,
diff/history, then public executable evidence. The independent verdict and
five-lens ledger were written in `receipts/independent-pass.md` before reading
the four prior public review reports. No private implementation material,
management files or other checkout was read.

Authorities include [issue #673](https://github.com/kebag-logic/milan-fpga/issues/673),
the [assignment](https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6015580138),
the [scope ruling](https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6015726285),
the [correction decision](https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6016931581),
REQ-VER-01 through REQ-VER-04, and the CI workflow policy.
The correction decision and prior findings were reconciled after the independent pass.
`receipts/public-scope.md` retains the acceptance and decisions.

Source coverage carried here is
[R516-2](https://github.com/kebag-logic/milan-fpga/pull/681#issuecomment-6017267451)
and [R517-2](https://github.com/kebag-logic/milan-fpga/pull/681#issuecomment-6017292023),
both POSITIVE at `793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df`.
Their source acceptance is distinct from this composition verdict.

The source changes eight paths; the predecessor changes 92 from their common
base. Their intersection is exactly `docs/testing/CI_WORKFLOWS.md`.
The initially unspecified overlap is therefore not empty. History identifies
predecessor commits `36014e0b48f34e9074ea97e03c109c2552403b00` and
`7412748ebffaeac9d36c0e880812aa8ccc826c5f` as its firmware-unit contributors.
The actual predecessor merges are #664 at `16af003a`, firmware tests at
`6714181d`, and #667 at `6a05347d`.

`scripts/composition.py` verifies the complete tree union:

- A raw three-way merge of the shared document reproduces candidate bytes exactly.
- Its Fast feedback and Local commands sections equal the predecessor sections.
  Firmware-unit coverage, SDK ordering, declared skipped arms and local campaigns survive intact.
- Its Exhaustive validation section equals the reviewed PR source section.
  The timeout table, survey limitations and envelope arithmetic survive intact.
- The other seven paths have identical modes and object IDs to source:
  `docs/testing/RUNNING_TESTS.md`, `docs/testing/TESTING.md`,
  `scripts/measure_test_evidence.py`, `scripts/measure_test_evidence_selftest.py`,
  `scripts/run_all_suites.sh`, `tb/verilator/milan_dp/README.md`, and
  `tb/verilator/milan_dp_gptp/README.md`.
- Every other candidate entry equals the predecessor entry.
  All four gitlinks are unchanged across source, predecessor and candidate.

Semantic interactions were checked separately. The predecessor's
`scripts/measure_test_evidence_readers.py:21` registers
`tb/verilator/aaf/start_mutants.py`; the changed evidence checker imports that
registry at `scripts/measure_test_evidence.py:105` and accepts the candidate
inventory. The predecessor's workflow and updated `ci_events.py` retain their
firmware-unit, SDK, job-step and evidence-record bindings. The workflow check
and self-test pass against the composed policy. The classifier self-test also
passes with the predecessor's documentation readers. The source adds no
workflow or record-pin change.

The policy agrees with the executed shell function: `capture_coherence` 2400 s,
`milan_dp_mclk` 3600 s, `milan_dp` 4800 s, `milan_dp_gptp` 5400 s,
and other suites 1800 s. Eighteen probes cover unset, empty and explicit
overrides across six names. The three affected suites remain on shards 1/5,
2/5 and 4/5 respectively. Historical envelope sums remain 5899.359 s,
6203.901 s and 4889.438 s, all below 6480 s.
These arithmetic checks are not new timing measurements. The predecessor
changes AAF tests on shard 2/5; their runtime is not newly bounded here.
The policy identifies its historical window and explicitly disclaims future
runner or cache-miss bounds.

[R516] PASS Conformance - `docs/testing/CI_WORKFLOWS.md:194`, `scripts/run_all_suites.sh:245`, and `receipts/semantic_checks.log` - composition preserves the ruling's values, exclusions and sampled envelope arithmetic; executed defaults agree with the policy table.

[R516] PASS RTL - `receipts/candidate.diff`, `receipts/composition.log`, and `receipts/verify_tree.log` - composition adds no RTL, interface, clock/reset/CDC or gitlink change beyond the reviewed sources. Predecessor RTL is preserved exactly. This untouched source lens carries R516-2 and R517-2 coverage.

[R516] PASS Robustness - `scripts/run_all_suites.sh:393`, `:415`, `:442`, and `receipts/semantic_checks.log` - executable deadline dispatch and UNKNOWN/92 handling equal the reviewed source. No new failure path is introduced by composition. R516-2 and R517-2 coverage carries; this round confirms defaults/overrides and runs the evidence self-test.

[R516] PASS Tests - `scripts/measure_test_evidence.py:105`, `:669`, `scripts/measure_test_evidence_readers.py:21`, `scripts/measure_test_evidence_selftest.py:284`, `.github/workflows/rtl-fast.yml:246`, and `scripts/ci_events.py:2352` - the merged registry, runner contract and predecessor workflow pins agree. Candidate checks and planted self-test cases pass.

[R516] PASS Docs - `docs/testing/CI_WORKFLOWS.md:41`, `:194`, `:2299`, the four correction files below, and documentation receipts - both contributors' sections survive; contents and cross-page anchors resolve; deadline references and the 60-suite count agree with executable selection.

Reviewer-owned completion ledger:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composition touches policy/runner agreement: CI_WORKFLOWS.md:194; run_all_suites.sh:245; semantic_checks.log | R516-3 | 72d3780d23a0b96362f8ae64059311b866ff5776 |
| RTL | CLEAN | Composition does not touch this PR's RTL/interface scope: candidate.diff; composition.log; verify_tree.log prove preservation | Covered by source reviews R516-2 and R517-2; R516-3 identity proof | 793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df source; 72d3780d23a0b96362f8ae64059311b866ff5776 identity proof |
| Robustness | CLEAN | Composition does not alter executable timeout/failure scope: run_all_suites.sh:393/:415/:442; source identity and supplemental override probes | Covered by source reviews R516-2 and R517-2; R516-3 confirmation | 793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df source; 72d3780d23a0b96362f8ae64059311b866ff5776 confirmation |
| Tests | CLEAN | Composition touches registry/workflow integration: measure_test_evidence.py:105/:669; measure_test_evidence_readers.py:21; rtl-fast.yml:246; ci_events receipts | R516-3 | 72d3780d23a0b96362f8ae64059311b866ff5776 |
| Docs | CLEAN | Composition touches CI_WORKFLOWS.md:41/:194/:2299; source correction files; docs/TOC/anchor/punctuation receipts | R516-3 | 72d3780d23a0b96362f8ae64059311b866ff5776 |

Prior findings were read after the independent verdict and ledger. The final
census contains nine discussion comments, zero formal reviews and zero inline
comments. All four public reports were examined; they introduce only these
three distinct findings. `receipts/reconcile.log` verifies their continued
resolution against candidate bytes and the current PR body:

- **R516-F1; original MINOR; all attributable lenses: Docs; RESOLVED.**
  Artifacts: `docs/testing/TESTING.md:169`, `docs/testing/RUNNING_TESTS.md:83`,
  `tb/verilator/milan_dp/README.md:309`, `tb/verilator/milan_dp_gptp/README.md:31`.
  Authority: [original finding](https://github.com/kebag-logic/milan-fpga/pull/681#issuecomment-6016896997),
  REQ-VER-04 and decision 6016931581. Impact was incorrect deadline figures.
  Required outcome: current values or links to the policy and ruling, with
  60 default suites. The corrected files are source-identical. Verification:
  original search has no matches, selector returns 60 distinct suites, and
  documentation gates pass. Nothing remains to fix.
- **R516-F2; original RESIDUE; all attributable lenses: Docs; RESOLVED.**
  Artifact: PR #681 body, Status and How to validate. Authority: the same
  original report. Impact was obsolete publication-stage wording. Required
  outcome: remove unpublished-branch and future-comment statements.
  Verification: neither stale statement remains; the body identifies the
  published PR and links existing public evidence. Nothing remains to fix.
- **R517-1-D1; original RESIDUE; all attributable lenses: Docs; RESOLVED.**
  Artifact: PR #681 body, Status. Authority:
  [external original finding](https://github.com/kebag-logic/milan-fpga/pull/681#issuecomment-6016927103).
  Impact was the same stale publication wording. Required exact replacement:
  “Published as PR #681 for independent review.” Verification: that sentence
  remains present. Nothing remains to fix.

Focused execution at the candidate:

| Command or probe | Result |
|---|---|
| `python3 scripts/docs_check.py` | rc 0; zero findings, 198 Markdown and 1119 scrubbed text files |
| `python3 scripts/gen_toc.py --check` | rc 0; 138 contents lists |
| `python3 scripts/gen_toc.py --verify-anchors` | rc 0; 386 fragment links reproduced |
| `python3 scripts/check_em_dash.py --base 28cdb5891b2b2d8a79b94a5bc2fb703c9fa8c721` | rc 0; zero findings, 339/339 controls |
| `python3 scripts/ci_events.py --check` | rc 0; 1741 contract items across four workflows and policy |
| `python3 scripts/ci_events.py --selftest` | rc 0; 2352 arms |
| `python3 scripts/measure_test_evidence.py --check` | rc 0; runner contract and ratchets pass, zero unexplained readers |
| `python3 scripts/measure_test_evidence.py --selftest` | rc 0; 105 PASS, zero FAIL |
| `python3 scripts/ci_scope.py --selftest` | rc 0 |
| `python3 scripts/suite_shards.py --selftest` | rc 0 |
| `bash -n scripts/run_all_suites.sh`; driver `--list` | rc 0; 60 default suites |
| Packet composition, semantic and reconciliation scripts | rc 0; identity, 18 budget probes, integration and prior-finding checks pass |
| `git diff --check 28cdb589..HEAD` | rc 0 |

Initial TOC, anchor and punctuation attempts refused with rc 2 because a pinned
dependency was absent. Their logs retain those refusals. The repository's
hash-locked requirements were installed only under packet scratch. Only those
three checks were retried; all passed. Exact argument vectors, statuses and
elapsed times are in `receipts/gates.json` and `receipts/gates_retry.json`,
with adjacent raw logs and rc files. Independent checks used four concurrent
foreground waits. No job remains running.

Real limits and pending manager duties:

- No full suite, processor, synthesis, builder or native bank was run here.
  The assignment reports candidate builder 48/48 and native 5/5 at this head;
  these are manager-provided results, not this reviewer's executions.
  The examined [published source packet](https://github.com/kebag-logic/milan-fpga/tree/ff5010496ab2c4efdd8a7e89b36463f7d5fb0ee4/review-evidence/673-r1)
  records source `26bd6334` and calibration NOT RUN. Its handoff SHA-256
  matches its manifest. It does not itself contain candidate bank receipts.
  Preserve these evidence scopes when publishing final acceptance.
- Physical calibration NOT RUN and field skips provide no hardware proof.
  No physical run, hardware access or compiler invocation occurred here.
  Historical samples remain historical; a timeout never proves completion.
- No fresh hosted acceptance is claimed. The manager owns exact-head hosted
  and local workflow-replica acceptance, distinguishing executed jobs from
  skipped contexts. No workflow replica was invoked during this review.
- At merge time, confirm then-current dev and final candidate identity,
  complete required gates and publish their evidence, accept the source and
  composition ledger, ensure every review has ended, and obtain explicit
  merge authorization. After landing, perform containment, issue closure
  and the project Done transition.
- Keep the three prior findings resolved. Open or confirm and schedule the
  excluded `milan_dp_gptp` job-level follow-up between merge rounds.
  The manager publishes this packet; this review made no GitHub writes.

Final integrity proves all 1143 tracked superproject blobs, Git modes and
1147 stage-zero index entries match the exact candidate. Required initialized
submodules match their pins and all tracked bytes, modes and index:
protocol processor `ead8036035affd53ef4b29979190f2f4f67084c0` (558 blobs),
gPTP processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` (104), and
axis dependency `48ff7a7e2ef782cf778d47910cf85835c64b1bce` (214).
Optional `external` remains uninitialized; its unchanged gitlink
`efeb541ae5fe1e078332d8462dca2fc2d9cb8db5` is verified, with no execution claim.
Final status including ignored files is empty. No restoration was needed:
source bytes were never edited. No commit, push or merge occurred.

`MANIFEST.sha256` lists every publishable script and receipt plus this report
and `REPRODUCE.md`. Paths are packet-relative. Verify the manifest before
rerunning scripts, because reruns replace receipts. Disposable environments,
fetched material and merge inputs remain under unpublished `scratch/`.

R516-3 FINISHED
