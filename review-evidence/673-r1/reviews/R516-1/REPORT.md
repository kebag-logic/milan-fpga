[R516] NEGATIVE - exact head 26bd6334a7b8b2a8582b36ae4729a71620546c14

# R516-1 internal independent review: issue #673 / PR #681

- Head: `26bd6334a7b8b2a8582b36ae4729a71620546c14`, tree `c3d52b1b166c11e9afaddc8fae0741d7dfad84d2` (verified in the clone).
- Base and live dev: `bd884631684ccf5060339efa92263d5c3e5c262c`. One commit, one-line message, no trailers.
- Diff: `docs/testing/CI_WORKFLOWS.md`, `scripts/measure_test_evidence.py`, `scripts/measure_test_evidence_selftest.py`, `scripts/run_all_suites.sh`. No `.github/`, `tb/`, `hdl/`, `scripts/suite_shards.py` or gitlink change.
- Authorities read: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #673 body, assignment 6015580138, STOP 6015714944, ruling 6015726285, the PR #681 body, and the published packet `review-evidence/673-r1` at `ff501049` (author HANDOFF.md / PR-BODY.md; sha256 values match its MANIFEST.json).

**Verdict basis.** The code change, the mirror, the selftest and the measured envelope are correct. I reproduced every published figure independently from the hosted logs. One MINOR Docs finding is open: four authoritative documents outside the diff still state the pre-#673 suite limits. One wording RESIDUE is in the PR body.

## Findings

### R516-F1 MINOR - Docs - stale per-suite limit statements outside the diff

- Artifacts at head (receipt `receipts/stale_limit_statements.txt`):
  - `docs/testing/TESTING.md:169`: "The default driver permits 1800 seconds per suite, and 3600 seconds for `milan_dp`."
  - `docs/testing/RUNNING_TESTS.md:83-85`: "each with an 1800-second deadline except `milan_dp`, which has 3600 seconds".
  - `tb/verilator/milan_dp/README.md:309`: "Every other default suite retains its 1800-second deadline; `milan_dp` has 3600 seconds".
  - `tb/verilator/milan_dp_gptp/README.md:31`: "The historical `milan_dp` suite has its own 3600-second budget."
- Authority/evidence: AGENTS.md section 5 says to update authoritative documentation when behavior changes. The section 6 `Docs` lens requires changed contracts to appear in authoritative docs. docs/README.md routes "Choose verification layers" to TESTING.md and "Run complete gates" to RUNNING_TESTS.md. At head, `scripts/run_all_suites.sh:246-252` sets `milan_dp` 4800 s, `milan_dp_mclk` 3600 s and `capture_coherence` 2400 s. None of the four files is in the diff (`git diff --stat` is empty for them).
- Impact: these are stated figures, not just wording. A reader of the testing guide, the run guide or the suite READMEs gets the wrong deadline for three suites, including the 3600 s `milan_dp` value that this PR replaced. The new figures appear only in CI_WORKFLOWS.md, the driver comment and the checker.
- Required outcome: every listed statement gives the head limits (`milan_dp` 4800 s, `milan_dp_mclk` 3600 s, `capture_coherence` 2400 s, others 1800 s) or points to the CI_WORKFLOWS.md table. Each cites the #673 ruling where it cited decision 5820240308 for the current value. The "54 suites" count at RUNNING_TESTS.md:83 predates this PR; I counted 60 default-shard suites at head. It is noted but not required here.
- Verification: `rg -n "1800-second deadline except|3600 seconds for .milan_dp|own 3600-second budget|milan_dp. has 3600" docs tb/verilator --glob '*.md'` returns 4 lines at this head and must return none at the corrected head. The docs, TOC, anchor and em-dash gates stay rc 0.

### R516-F2 RESIDUE - Docs (PR body wording only) - stale handoff sentences in the PR #681 body

- Artifact: PR #681 body, "Status": "This body is prepared for handoff; the branch has not been pushed and no PR has been created." "How to validate": "self-test evidence is prepared for the future PR comment."
- Evidence: the branch is published and PR #681 exists at head `26bd6334a`.
- Impact: wording only. It changes no measurement, figure, verdict, test, code or claim.
- Exact fix: replace the first sentence with "The branch is published as PR #681 at that head." Replace the second with "self-test evidence is posted as a PR comment."

**Prior public findings.** No prior public review finding exists on PR #681 at this head. It has 2 comments, both review-start notices, and 0 reviews. The #673 thread has no review findings. Nothing needed to be resolved or retained.

## Lens results (all five applied at the exact head)

- **[R516] PASS Conformance** - `scripts/run_all_suites.sh:246-252`, `scripts/measure_test_evidence.py:669-678`, `scripts/measure_test_evidence_selftest.py:291-303`, PR #681 body, `docs/testing/CI_WORKFLOWS.md:170-222`. Checked against the #673 acceptance and ruling 6015726285:
  - The applied limits are exactly `milan_dp_mclk` 1800->3600, `capture_coherence` 1800->2400 and `milan_dp` 3600->4800.
  - `milan_dp_gptp` stays at 5400 s. The PR body files its job-level follow-up under "Known limitations / out of scope", with the 7281.997 s versus 7200 s numbers.
  - The hosted wall times are recorded on the PR with run and job ids.
  - No check, count, campaign, shard assignment or `.github` change. The diff name-status has 4 files, and `git diff --quiet` is empty for `.github scripts/suite_shards.py tb`.
  - Ownership at head (`receipts/shards_at_head.txt`) puts `capture_coherence` in 1/5, `milan_dp_mclk` in 2/5 and `milan_dp` alone in 4/5.
- **[R516] PASS RTL** - `git diff --name-status bd884631..26bd6334`: no HDL, testbench or gitlink change. The `gptp-processor` 5dce647a, `protocol-processor` ead80360 and `third_party/verilog-axis` 48ff7a7e gitlinks equal base (`receipts/restore_check.txt`).
  - The lens applies only to the CI timing interplay. `.github/workflows/rtl.yml:152` keeps `timeout-minutes: 120` (7200 s) for `verilator-shards`, and `:314` keeps it for `physical-gptp`.
  - Every affected shard's envelope stays under 6480 s (see Robustness).
- **[R516] PASS Robustness** - `receipts/survey_author_equivalent.txt`, `receipts/survey_all_logs.txt`, `receipts/probe_limits.txt`, `scripts/survey_envelope.py`.
  - I independently downloaded all 46 non-skipped job logs of the ten surveyed runs (sha256 in `receipts/jobs/hosted_log_sha256.txt`). Excluding the 7 jobs that finished after 12:00Z, which were active at survey time, reproduces every published figure exactly: 424 shard windows plus the physical-job window, 425 in total. Shard envelopes are 1/5 5899.359 s, 2/5 6203.901 s and 4/5 4889.438 s, and the suite maxima and job ids match.
  - Including the now-complete logs changes only shard 2/5: 6210.776 s, 13.74 % headroom, overhead from job 112236028394. That job timed `milan_dp_mclk` out again. Every affected shard still keeps at least 10 % headroom. Shard 2's worst observed real job time is 4406 s.
  - Override semantics probed live: unset or empty `SUITE_TIMEOUT` gives the defaults, an explicit value overrides every suite, and unknown names fall to 1800 s.
  - The exit-92 TIMEOUT and exit-90 tally contracts are still pinned by `runner_contract`.
- **[R516] PASS Tests** - `scripts/measure_test_evidence_selftest.py:291-303` and `receipts/probe_limits.txt`.
  - The selftest passes 105/105 at head (`receipts/gates/python3_scripts_measure_test_evidence.py_--selftest.log`).
  - Each mutation tuple must change the text to pass, so all 12 mutations are effective. There is one per budget value and one per named arm.
  - Extra negative probes, all rejected by `runner_contract`: the base runner (pre-#673 limits), mclk 3600->3000, capture 2400->2399, milan_dp 4800->5400, a deleted mclk arm, `:-` changed to `:=`, and reordered arms. The head runner is accepted (8/8 expectations met).
  - `--check` rc 0. `test_suite_cancellation.py`, `suite_shards.py --selftest` and `suite_tally.py --selftest` rc 0.
- **Docs: UNCLEAN** under R516-F1.
  - Within the diff, `CI_WORKFLOWS.md:170-222` is arithmetically correct: 757.720 s / 31.6 %; 1290.438 s / 26.9 %; 18.06 / 13.83 / 32.09 %. It labels TIMEOUT windows honestly as cutoffs.
  - The docs gates pass: `docs_check`, `check_doc_paths`, `check_doc_style`, `gen_toc --check/--verify-anchors` and `check_em_dash --base bd884631`, all rc 0 with the pinned Markdown environment.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | run_all_suites.sh:246-252; measure_test_evidence.py:669-678; selftest:291-303; PR #681 body; ruling 6015726285; diff name-status | R516-1 | 26bd6334a7b8b2a8582b36ae4729a71620546c14 |
| RTL | CLEAN | diff name-status (no HDL/tb); gitlinks; rtl.yml:152,314 timeout-minutes | R516-1 | 26bd6334a7b8b2a8582b36ae4729a71620546c14 |
| Robustness | CLEAN | 46 hosted job logs re-derived (survey_*.txt); live suite_timeout override probe | R516-1 | 26bd6334a7b8b2a8582b36ae4729a71620546c14 |
| Tests | CLEAN | selftest 105/105; 8/8 extra checker probes; cancellation/shards/tally selftests | R516-1 | 26bd6334a7b8b2a8582b36ae4729a71620546c14 |
| Docs | UNCLEAN (R516-F1 MINOR open; R516-F2 RESIDUE) | CI_WORKFLOWS.md:170-222; TESTING.md:169; RUNNING_TESTS.md:83-85; milan_dp/README.md:309; milan_dp_gptp/README.md:31; PR body | R516-1 | 26bd6334a7b8b2a8582b36ae4729a71620546c14 |

If R516-F1 is fixed by a commit that touches only those four Markdown documents, nothing in the Conformance, RTL, Robustness or Tests scope changes, so their coverage above stays banked. Docs must be re-covered at the new head.

## Real limits

- I ran no builder bank, full suite sweep, Yosys or parent/PP/gPTP bank; those were excluded by the assignment. The manager's source static/builder/native banks are reported as passing at this head; I did not re-run them.
- No Docker/act run and no hardware. Physical calibration was NOT RUN. Field skips are not hardware proof.
- The hosted runs at this head (rtl-full 37466043282 and siblings) were still in progress at 13:02Z. Verilator shard 3/5 had completed with success. Physical gPTP was skipped on `pull_request`, not executed. I make no exact-head hosted claim.
- The envelope uses ten historical runs on other heads. As the PR states, it cannot bound future runner slowdowns. `milan_dp_mclk`'s largest completed window in the survey is 1084.530 s; 3600 s is the ruling's budget.
- With the system interpreter, the Markdown gates fail closed (rc 2) because the pinned renderer is absent. That is recorded in `receipts/gates/summary.tsv`. They pass with the pinned Markdown environment.

## Pending manager duties

- Carry R516-F2 to the residue checklist.
- Schedule the R516-F1 fix and the Docs re-cover at the new head.
- Open the `milan_dp_gptp` job-level follow-up named in the PR body.
- Own the hosted exact-head and act acceptance, the current-dev candidate merge, and post-merge containment.

## Receipts

Listed in `MANIFEST.sha256`:
- scripts: `scripts/survey_envelope.py`, `scripts/probe_limits.sh`
- hosted survey: `receipts/jobs/*`, `receipts/shards_at_head.txt`, `receipts/survey_*.txt`, `receipts/hosted_*_at_head.tsv`
- gates and probes: `receipts/gates/*`, `receipts/probe_limits.txt`, `receipts/stale_limit_statements.txt`
- clone check: `receipts/restore_check.txt`

The clone was not modified. The worktree, index and gitlinks equal the head tree, and `git status --ignored` is empty.

R516-1 FINISHED
