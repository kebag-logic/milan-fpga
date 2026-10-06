[R517] POSITIVE - exact head 26bd6334a7b8b2a8582b36ae4729a71620546c14

R517-1, external independent review of issue #673 / PR #681. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains. One prose-only RESIDUE belongs on the manager's checklist. This verdict covers the source revision; merge acceptance remains pending.

Reviewed tree: `c3d52b1b166c11e9afaddc8fae0741d7dfad84d2`. Source base: `bd884631684ccf5060339efa92263d5c3e5c262c`. The single implementation commit changes four files, with 73 insertions and 17 deletions. The exact [source diff](receipts/source.diff) contains the three suite limits, checker mirrors, corresponding budget mutation cases, and CI policy text. It changes no RTL, interface, workflow, job timeout, shard assignment, suite check/count, campaign, or submodule pin.

Context was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue and public scope decisions, REQ-VER-03/04 and CI policy, then the diff/history and public evidence. The [assignment](https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6015580138) and [ruling](https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6015726285) authorize the three changes and exclude the physical-rate scheduling follow-up. No private implementation material or other review report was consulted. The [independent verdict and ledger](receipts/independent-verdict.md) were written before retrieving prior review endpoints.

The timing basis was independently reconstructed from the frozen ten-run survey. All 39 downloaded log hashes match the [published evidence](https://github.com/kebag-logic/milan-fpga/tree/ff5010496ab2c4efdd8a7e89b36463f7d5fb0ee4/review-evidence/673-r1) after its documented removal of terminal escapes. There are 425 completed verdict windows in 38 logs; 36 complete job inventories supply overhead measurements. Every current default shard member has a measured window. The seven suites exceeding 60%, and the three default suites exceeding 80%, match the published tables. Partial cancelled jobs supply only finished windows, never overhead estimates. Raw selected timestamp lines, job metadata, hashes, every computed window and maxima are retained in [measurement-analysis.json](receipts/measurement-analysis.json), [measurement-fetch.json](receipts/measurement-fetch.json), and `receipts/hosted/`.

| Changed suite | Old limit -> new limit | Largest observed window | Hosted run / job |
|---|---|---|---|
| capture_coherence | 1800 -> 2400 s | 1642.280 s PASS | [37429204551 / 112155955445](https://github.com/kebag-logic/milan-fpga/actions/runs/37429204551/job/112155955445) |
| milan_dp_mclk | 1800 -> 3600 s | 1800.008 s TIMEOUT, UNKNOWN | [37430728685 / 112160880744](https://github.com/kebag-logic/milan-fpga/actions/runs/37430728685/job/112160880744) |
| milan_dp | 3600 -> 4800 s | 3509.562 s PASS | [37424768281 / 112142195163](https://github.com/kebag-logic/milan-fpga/actions/runs/37424768281/job/112142195163) |

The largest completed `milan_dp_mclk` sample in this window is 1084.530 s, run 37424768281 / job 112142195210. Its timeout is not a successful completion bound. The ruling explicitly authorizes 3600 s subject to the measured envelope.

The unchanged `.github/workflows/rtl.yml:152` allows 120 minutes per default shard. The acceptance ceiling is therefore 6480 s. Independently summed sibling maxima and maximum complete-job overhead reproduce every affected row in `docs/testing/CI_WORKFLOWS.md:212`:

| Shard | Raised limits | Other suite maxima | Maximum overhead | Envelope | Remaining of 7200 s | Overhead run / job |
|---|---:|---:|---:|---:|---:|---|
| 1/5 | 2400 s | 3381.779 s | 117.580 s | 5899.359 s | 1300.641 s / 18.06% | 37424768281 / 112142195196 |
| 2/5 | 3600 s | 2517.453 s | 86.448 s | 6203.901 s | 996.099 s / 13.83% | 37429204551 / 112155955407 |
| 4/5 | 4800 s | 0 s | 89.438 s | 4889.438 s | 2310.562 s / 32.09% | 37424768281 / 112142195163 |

[R517] PASS Conformance - `scripts/run_all_suites.sh:246`, `docs/testing/CI_WORKFLOWS.md:190`, issue ruling 6015726285, measurement receipts - all authorized limits and mirrored expectations match; survey thresholds and all affected 10% envelopes are satisfied. `milan_dp_gptp` remains 5400 s, and the PR body explicitly assigns its job-level follow-up to the manager.

[R517] PASS RTL - `receipts/source.diff`, `.github/workflows/rtl.yml:147`, `scripts/suite_shards.py:77`, `receipts/integrity-after.log` - the diff leaves RTL, clocks, reset/CDC, datapath interfaces, inventory ownership and gitlinks unchanged. Scheduling still serializes each worker's suites and isolates `milan_dp` on 4/5. No new hardware behavior requires an RTL proof in this change.

[R517] PASS Robustness - `scripts/run_all_suites.sh:246`, `:386`, `:423`; `receipts/limit-probes.json`; `receipts/cancellation.log` - unset/empty overrides retain defaults; explicit, zero and fractional overrides pass through; similarly named suites retain the default. Real loop definitions pass the selected limits to the launch boundary. Controlled 124/137 results remain UNKNOWN/92, ordinary and masked failures remain failures, and cancellation controls pass. Measured margins are sufficient under the ruling, with future slowdown explicitly unbounded.

[R517] PASS Tests - `scripts/measure_test_evidence.py:662`, `scripts/measure_test_evidence_selftest.py:284`, `receipts/evidence-selftest.log`, `receipts/focused-results.json` - the checker pins all five budget values and selected names; all 105 self-test cases pass. Ten independent budget/name/binding mutations each modify a unique live occurrence and are rejected. Forty shell selection cases and five loop verdict cases pass. These probes use disposable launch fixtures; they do not claim RTL execution.

[R517] PASS Docs - `docs/testing/CI_WORKFLOWS.md:167`, `:190`, `:212`, PR #681 body, public evidence at ff5010496ab2c4efdd8a7e89b36463f7d5fb0ee4 - cited run/job IDs, elapsed windows, arithmetic and scope match the primary records. Historical measurements, timeout UNKNOWNs, unavailable survey logs, overrides and the deferred follow-up are accurately distinguished. Documentation checks pass. The wording residue below does not alter these claims.

Finding **R517-1-D1**: **RESIDUE**, attributable lens **Docs**, artifact **PR #681 body, Status, second paragraph**.

- Authority/evidence: [PR body snapshot](receipts/pr-body-snapshot.md) says, "This body is prepared for handoff; the branch has not been pushed and no PR has been created." The [published PR metadata](receipts/source-snapshot.json) identifies this open PR at the exact reviewed head.
- Impact: stale handoff-stage wording only. It changes no measurement, figure, verdict, test, code, generated artifact, conformance/clause claim or privacy rule.
- Required exact fix: replace that sentence with "Published as PR #681 for independent review."
- Verification: re-read the PR body after the manager applies the wording correction. This remains RESIDUE and leaves Docs CLEAN under the assigned owner rule.

Reviewer-owned completion ledger:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #673 assignment/ruling; run_all_suites.sh:246; CI_WORKFLOWS.md:190; measurement-analysis.json | R517-1 | 26bd6334a7b8b2a8582b36ae4729a71620546c14 |
| RTL | CLEAN | source.diff; rtl.yml:147; suite_shards.py:77; integrity-after.log | R517-1 | 26bd6334a7b8b2a8582b36ae4729a71620546c14 |
| Robustness | CLEAN | run_all_suites.sh:246,386,423; limit-probes.json; cancellation.log; measurement-analysis.json | R517-1 | 26bd6334a7b8b2a8582b36ae4729a71620546c14 |
| Tests | CLEAN | measure_test_evidence.py:662; measure_test_evidence_selftest.py:284; evidence-selftest.log; focused-results.json | R517-1 | 26bd6334a7b8b2a8582b36ae4729a71620546c14 |
| Docs | CLEAN | CI_WORKFLOWS.md:167,190,212; PR body; public evidence; docs-check.log; doc-paths.log; doc-style.log | R517-1 | 26bd6334a7b8b2a8582b36ae4729a71620546c14 |

Prior public findings: none found. After the independent verdict was written, the PR discussion had only two review-start comments, with zero formal reviews and zero inline review comments. There is no earlier finding to resolve or retain. The snapshot is retained in [public-findings-reconciliation.json](receipts/public-findings-reconciliation.json).

All eleven focused commands returned 0: evidence check/self-test, shell syntax, shard/tally self-tests, cancellation, documentation check/path/style, workflow policy check and diff whitespace check. [focused-results.json](receipts/focused-results.json) records each exact argument vector, exit code and elapsed time; adjacent `.log` and `.rc` files retain the receipts. Independent checks ran concurrently in a foreground supervisor, with six workers; network retrieval used eight workers. No build, shared installation, hardware access, source edit or GitHub write occurred.

To reproduce from this packet, pass the exact-head clone and packet paths as positional arguments:

```sh
sha256sum -c MANIFEST.sha256
python3 scripts/verify_tree.py "$REVIEW_CLONE"
python3 scripts/fetch_measurements.py "$PACKET"
python3 scripts/analyze_measurements.py "$REVIEW_CLONE" "$PACKET"
python3 scripts/run_focused.py "$REVIEW_CLONE" "$PACKET"
python3 scripts/probe_limits.py "$REVIEW_CLONE" "$PACKET"
python3 scripts/verify_tree.py "$REVIEW_CLONE"
```

Verify the delivered manifest before rerunning commands; reruns regenerate receipts. Fetching needs read-only public repository access. Offline arithmetic can run directly from the published `receipts/hosted/` inputs. Disposable trees and full downloaded logs remain under `scratch/`, which is excluded from publication. The five loop transcripts replace their disposable root with `$PROBE_ROOT`; hosted timestamp receipts preserve the selected raw lines.

Real limits and pending manager duties:

- This is source review at the stated head. The manager's reported full source static/builder and native banks were not rerun. The public builder record reports rc 0 with calibration NOT RUN; its hashes and result table are evidence of that report, not a fresh execution by this reviewer. Physical calibration NOT RUN and field skips provide no hardware proof. No physical suite or RTL build was run during this review.
- Historical timing envelopes cannot bound future runner or cache-miss delays. Seven active-job logs were unavailable when the survey was frozen. No timeout sample proves successful completion.
- The hosted snapshot recorded at 2026-10-06T13:03:21Z shows several executed successes, ongoing required work, and the physical gPTP context explicitly skipped. The four workflow runs are still in progress; no overall hosted acceptance is claimed. [hosted-head-snapshot.json](receipts/hosted-head-snapshot.json) distinguishes each status. The manager owns hosted and local workflow acceptance.
- The final candidate must be built against then-current live `dev`, even though source base and assigned live dev were both `bd884631684ccf5060339efa92263d5c3e5c262c`. Complete the candidate gates, remaining independent review, review-flight closure, explicit merge authorization, post-merge containment, issue closure and project completion under CONTRIBUTING.md.
- Open and schedule the `milan_dp_gptp` job-level follow-up between merge rounds, as the ruling and PR body require. Carry R517-1-D1 to the residue checklist. This review made no public changes.

Final integrity: all 1110 superproject blobs, their modes and index entries match the reviewed commit. The three required submodules match their gitlinks and all tracked bytes/modes/index entries: axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce` (214 blobs), protocol processor `ead8036035affd53ef4b29979190f2f4f67084c0` (558), gPTP processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` (104). Before/after integrity receipts are identical; working tree status is clean. No restoration was needed because source bytes were never modified.

R517-1 FINISHED
