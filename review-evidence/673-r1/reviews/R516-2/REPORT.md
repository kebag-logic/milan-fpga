[R516] POSITIVE - exact head 793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df

R516-2, internal independent review of issue #673 / PR #681. All five lenses are CLEAN. R516-F1, R516-F2 and R517-1-D1 are resolved. No open finding or residue remains in this review. This verdict covers source review; manager-owned merge acceptance remains pending.

Reviewed tree: `4044003424303525864889c45788aeb8a48c8501`. Source base and observed live `dev`: `bd884631684ccf5060339efa92263d5c3e5c262c`. Parent: `26bd6334a7b8b2a8582b36ae4729a71620546c14`. The full diff changes eight files. Round 2 changes exactly four Markdown files; executable source is identical to the prior reviewed head. Both commit messages are single lines without trailers. See `receipts/source.diff`, `receipts/round2.diff` and `receipts/source-state.json`.

Reconstruction followed the assigned order: repository operating rules, documentation index, issue acceptance and public decisions, REQ-VER-01 through REQ-VER-04 and the CI/interface authorities, then diff/history and public executable evidence. The independent verdict and five-lens ledger were written before reading either prior public review report; `receipts/review-sequence.log` records that checkpoint. No private implementation material or another checkout was read.

Authorities: [issue #673](https://github.com/kebag-logic/milan-fpga/issues/673), [initial assignment](https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6015580138), [scope ruling](https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6015726285), [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6016931581), and [published source evidence](https://github.com/kebag-logic/milan-fpga/tree/ff5010496ab2c4efdd8a7e89b36463f7d5fb0ee4/review-evidence/673-r1). `receipts/issue-scope.md` preserves the frozen scope decisions.

Prior finding dispositions, checked after the independent pass:

- **R516-F1: RESOLVED; original severity MINOR; all attributable lenses: Docs.** Artifacts: `docs/testing/TESTING.md:169`, `docs/testing/RUNNING_TESTS.md:83-89`, `tb/verilator/milan_dp/README.md:309`, `tb/verilator/milan_dp_gptp/README.md:31`. Authority: AGENTS.md's changed-contract documentation rule and assignment 6016931581. The old statements gave incorrect current deadlines; all four now link to the authoritative policy table and cite #673. The run guide also states 60 default suites. Required outcome is met. Verification: the original review's exact search returns zero matches, the live selector returns 60 distinct default suites, and the documentation/contents/anchor/em-dash gates pass. See `receipts/prior-findings-check.log`, `receipts/focused-probe.log` and the documentation receipts.
- **R516-F2: RESOLVED; original severity RESIDUE; all attributable lenses: Docs.** Artifact: PR #681 body, Status and How to validate. Authority/evidence: the [prior finding](https://github.com/kebag-logic/milan-fpga/pull/681#issuecomment-6016896997) identified unpublished-branch and future-comment wording in an already published PR. Impact was wording only. Required outcome: describe the published PR and remove obsolete handoff-stage statements. The body now says “Published as PR #681 for independent review.” Its evidence section links the existing public issue handoff without claiming an unposted PR evidence comment. Verification: freshly fetched `receipts/pr-body.md` and `receipts/prior-findings-check.log`; both obsolete phrases are absent.
- **R517-1-D1: RESOLVED; original severity RESIDUE; all attributable lenses: Docs.** Artifact: PR #681 body, Status. Authority/evidence: the [external prior finding](https://github.com/kebag-logic/milan-fpga/pull/681#issuecomment-6016927103) names the same unpublished-branch sentence. Impact was wording only. Its exact requested replacement, “Published as PR #681 for independent review.”, is present. Verification: the same fresh PR-body receipt.

The final public finding census contains six discussion comments, zero formal reviews and zero inline review comments. Both prior reports were reconciled; no other public finding was present. See `receipts/prior-finding-sources.json`.

[R516] PASS Conformance - `scripts/run_all_suites.sh:245-253`, `scripts/measure_test_evidence.py:669-681`, `docs/testing/CI_WORKFLOWS.md:168-222`, and PR #681 body - checked against issue acceptance and ruling 6015726285. The three authorized defaults are 2400 s for `capture_coherence`, 3600 s for `milan_dp_mclk`, and 4800 s for `milan_dp`. The physical selection remains 5400 s; other suites remain 1800 s. No check, campaign, shard-assignment or job-timeout change occurs. Hosted wall times and the excluded physical-job follow-up remain recorded on the PR. Source and candidate acceptance obligations remain distinct.

[R516] PASS RTL - `receipts/source.diff`, `.github/workflows/rtl.yml:152,314`, `scripts/suite_shards.py:77`, and `receipts/integrity-final.log` - examined the complete changed-path population and unchanged integration boundaries. No RTL, clock/reset/CDC, module interface, suite executable or gitlink is changed. Existing serial shard execution and the dedicated datapath shard remain intact. Each affected measured envelope fits the unchanged 7200-second job allowance with at least 10% remaining.

[R516] PASS Robustness - `scripts/run_all_suites.sh:245-253,393-442`, `receipts/focused-probe.log`, and `receipts/measurements.log` - unset and empty overrides retain the expected defaults; explicit, fractional and zero overrides preserve existing behavior; an unknown suite gets 1800 s. A real 0.05-second deadline interrupts a disposable workload and returns UNKNOWN/92 with zero passes and zero failures. That fixture stubs tallying and proves deadline classification, not suite-check correctness. The unchanged tally and cancellation paths retain prior clean coverage. Timeout observations remain cutoffs, never successful completion bounds.

[R516] PASS Tests - `scripts/measure_test_evidence_selftest.py:284-311`, `scripts/measure_test_evidence.py:661-700`, and focused receipts - the live evidence check passes, with 105/105 self-test cases. Ten independent probes each change a unique budget/name/binding occurrence and produce the specific budget-contract refusal. Thirty shell selection cases pass. The live inventory contains 60 distinct default suites and one separate scheduled selection. No full suite or build bank was run.

[R516] PASS Docs - the four corrected files and lines listed under R516-F1, `docs/testing/CI_WORKFLOWS.md:168-222`, and `receipts/pr-body.md` - current values, links, suite count, historical measurements, scope and limitations agree. Documentation content, paths and style pass. With the pinned renderer, 136 contents lists pass, 348 cross-page fragment links reproduce, and the em-dash gate reports zero findings with 339/339 controls. Initial system-interpreter dependency refusals are preserved; the successful reruns use a disposable isolated installation of the repository's locked requirements.

The unchanged published timing basis was checked again without repeating the full prior survey. `scripts/check_measurements.py` verifies that the published maxima cover every current default suite, checks shard ownership, and recomputes all affected envelopes. Five original hosted logs independently confirm the three changed-suite windows and the three overhead maxima:

| Shard | Changed limit | Sibling maxima | Maximum overhead | Envelope | Remaining / 7200 s |
|---|---:|---:|---:|---:|---:|
| 1/5 | 2400 s | 3381.779 s | 117.580 s | 5899.359 s | 18.06% |
| 2/5 | 3600 s | 2517.453 s | 86.448 s | 6203.901 s | 13.83% |
| 4/5 | 4800 s | 0 s | 89.438 s | 4889.438 s | 32.09% |

The samples confirm `capture_coherence` PASS at 1642.280 s, `milan_dp` PASS at 3509.562 s, and `milan_dp_mclk` TIMEOUT at 1800.008 s. The receipt retains selected original timestamp lines, raw-log hashes and arithmetic. This round does not claim to have downloaded every log again. R516-1's broader unchanged survey coverage stands.

Reviewer-owned completion ledger:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue acceptance/rulings; run_all_suites.sh:245; measure_test_evidence.py:669; CI_WORKFLOWS.md:168; PR body; measurements.log | R516-2 | 793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df |
| RTL | CLEAN | source.diff; rtl.yml:152,314; suite_shards.py:77; integrity-final.log | R516-2 | 793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df |
| Robustness | CLEAN | run_all_suites.sh:245,393,423; focused-probe.log; measurements.log | R516-2 | 793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df |
| Tests | CLEAN | measure_test_evidence_selftest.py:284; evidence-check.log; evidence-selftest.log; focused-probe.log | R516-2 | 793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df |
| Docs | CLEAN | TESTING.md:169; RUNNING_TESTS.md:83; milan_dp/README.md:309; milan_dp_gptp/README.md:31; CI_WORKFLOWS.md:168; pr-body.md; documentation receipts | R516-2 | 793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df |

All receipt paths in the ledger are relative to `receipts/`; source paths retain their repository directories. The first four lenses were already clean at the parent. Their executable artifacts are unchanged, and this round independently reapplied them with the focused checks above. Docs is newly covered clean at the corrected head.

Real limits and pending manager duties:

- The manager-reported full source static/builder and native banks were not rerun here. The public builder record reports a completed bank with calibration NOT RUN. Physical calibration NOT RUN and field skips provide no hardware proof. No hardware, full parent/processor/physical suite bank, synthesis bank or builder bank was run during this review.
- Historical envelopes cannot bound future runner or cache-miss delays. The survey's unavailable logs and timeout samples retain their stated limitations. The physical-job scheduling follow-up is explicitly excluded by the ruling; the manager still must open and schedule it between merge rounds.
- `receipts/hosted-checks.json` distinguishes executed successes, in-progress work and the skipped physical gPTP context at this head. The default suite workers and several required contexts were still running when observed. This is no overall hosted acceptance. The manager owns hosted and local workflow-replica acceptance.
- The manager must validate the final candidate against then-current live `dev`, complete the independent external review and ensure no review remains in flight, obtain explicit merge authorization, then perform post-merge containment and issue/project closure. Observed source base and live `dev` are equal, but this review does not substitute for that merge-turn validation.

Final integrity independently hashes all 1110 tracked superproject blobs and checks their modes and exact stage-zero index. Required submodules also match their pinned commits, bytes, modes and index: protocol processor `ead8036035affd53ef4b29979190f2f4f67084c0` (558 blobs), gPTP processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` (104), and axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce` (214). Before/after integrity results agree. Status including ignored files is empty. No source restoration was needed; no source bytes were changed.

`MANIFEST.sha256` lists every publishable report, script and receipt. `receipts/commands.json` records focused command lines and exit statuses. Reproduce packet probes by passing the exact-head clone and packet directory to `scripts/focused_probe.py` and `scripts/check_measurements.py`; pass the clone to `scripts/verify_integrity.py`. Check the manifest before rerunning, because reruns replace receipts. Full downloaded logs, disposable fixtures and the isolated renderer environment remain under `scratch/` and are excluded from publication. No GitHub write, source commit, push or merge was performed.

R516-2 FINISHED
