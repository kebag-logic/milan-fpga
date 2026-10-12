[R627] NEGATIVE - exact head a57d384dc697249c2a69f80079b676875d4f7560

External independent review, round R627-1, of issue #727 / PR #728. All five lenses were applied. One open MINOR in Tests makes the verdict NEGATIVE: the self-test accepts mutations that loosen the required 60% bound. The prior public finding was independently reproduced and is retained. The other four lenses are CLEAN. Prose-only RESIDUE items belong on the manager's residue checklist. This verdict does not discharge hosted acceptance 3.

Reviewed tree: `a2fada192e36369be7fb6202c8f9618021c31c77`. Source base: `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`. Three commits change only `scripts/suite_shards.py` and `docs/testing/CI_WORKFLOWS.md`. Workflow, suite driver, RTL, testbenches, firmware and gitlinks are unchanged.

The contract was reconstructed from `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`, [issue #727 and its frozen assignment](https://github.com/kebag-logic/milan-fpga/issues/727#issuecomment-6121794007), `REQUIREMENTS.md:305`, the workflow's ownership interfaces and the CI policy. The diff and history were examined independently before consulting the [published executable evidence](https://github.com/kebag-logic/milan-fpga/tree/ba5d7c36446b4c2b0a05c708cacb4a43c6330288/review-evidence/727-r1). No private implementation material was read. An initial independent verdict and ledger were written before reading any other review report; `receipts/reconciliation-start.json` records their hash before the public reconciliation. The final verdict incorporates the separately reproduced prior finding below. Review start: [public assignment](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6125710127).

**Measurements and acceptance evidence.**

All 62 suite figures and five overheads match independent measurements of the hosted logs, rounded upward. The committed `--measure` was also executed. A separate decimal-timestamp oracle checked every figure. [suite-measurements.csv](receipts/suite-measurements.csv) records each suite's input file, start/end lines, exact elapsed time and committed value. [overhead-measurements.csv](receipts/overhead-measurements.csv) records setup, tail, endpoints and rounded overhead. Original hosted logs are included.

The five dev logs are from run `38217650945`. The exception is `maap`, from job `114677344710` of run `38208503834`: `1374.1774735` seconds rounds to the committed `1375`. The issue's approximately `1380` seconds is consistent with that window. Its completed window remains usable even though that job later cancelled; its incomplete log supplies no overhead. Dev's superseded `maap` value is `185` seconds. The overheads are exactly `(83, 115, 80, 93, 80)`. `milan_dp` starts at its `shard:` line: `2796.1684725` seconds rounds to `2797`, with setup counted separately.

An independent heap allocator reproduces every owner and load. Fifty shuffled inventories produce the same map. All five real driver `--list` outputs contain the 62-suite filesystem inventory exactly once. The serial/default lists equal the base's lexical selection. The scheduled physical suite stays separate. `milan_dp` is alone on 4/5, `tsn_fuzz` stays on 1/5, and `chmap_capture` on 3/5, matching the unchanged workflow's ownership checks and setup.

| Worker | Suite count | Predicted seconds including overhead | Workflow-derived bound | Spare seconds |
|---|---:|---:|---:|---:|
| 0/5 | 15 | 4204 | 4320 | 116 |
| 1/5 | 16 | 4205 | 4320 | 115 |
| 2/5 | 14 | 4203 | 4320 | 117 |
| 3/5 | 16 | 4205 | 4320 | 115 |
| 4/5 | 1 | 2877 | 4320 | 1443 |

The workflow text supplies `timeout-minutes: 120` and `matrix.total: [5]`; the gate derives the 4320-second bound. The docstring's refresh shell ran verbatim, with temporary/cache storage confined to scratch. It exits 0 and reproduces the dev tables. The documented instruction to retain the separate `maap` measurement remains necessary until dev measures #696. See [refresh-verbatim.sh](receipts/refresh-verbatim.sh), [refresh-verbatim.log](receipts/refresh-verbatim.log), [measure-dev.log](receipts/measure-dev.log) and [measure-maap.log](receipts/measure-maap.log).

Acceptance 1, 2 and 4 are supported. Acceptance 3 remains the manager's hosted duty: every actual PR-head worker must take at most 4320 seconds, with predicted versus measured values recorded publicly. Prediction is not that measurement.

**Independent lens results.**

[R627] PASS Conformance - `scripts/suite_shards.py:90`, `:158`, `:204`, `:253`, `:286`; `.github/workflows/rtl.yml:148`; receipts `suite-measurements.csv`, `overhead-measurements.csv`, `assignment.json` - Checked the frozen assignment's measured table, inventory, deterministic split, setup ownership, dedicated worker and workflow-derived bound. All 67 figures match their logs. Workflow blob equality establishes the unchanged-workflow restriction. Hosted acceptance 3 is reserved above.

[R627] PASS RTL - `receipts/review-diff.patch`; `scripts/run_all_suites.sh:168`, `:291`, `:449`; `.github/workflows/rtl.yml:214`; `scripts/suite_tally.py:398`; `scripts/ci_events.py` canonical ownership contract - Reviewed discovery, selection, preflight, worker setup and aggregate integration. Lexical execution order and serial selection persist; the unchanged discovery interface still serves tally readers. No external caller of removed `shard_owner` remains. The complete two-file diff establishes that no hardware clock, reset, CDC, width, protocol or FSM artifact changed. Driver/workflow blob equality is independently verified.

[R627] PASS Robustness - `scripts/suite_shards.py:187`, `:253`, `:329`, `:564`, `:625`, `:719`; receipts `fault-*.log`, `selection-*.log`, `cancellation.log` - Disposable actual-entry-point probes refuse missing/stale durations, a heavier real suite, reduced timeout, worker-count drift and missing workflow. Self-test exits 1 for each; sharded selection exits 2 for table disagreement. Serial selection still enumerates without a duration table. Checked invalid shard forms, exact-bound/one-second-over behavior, pin stability, malformed/failed timing inputs and intentionally incomplete logs without overhead. Existing cancellation controls pass with the changed selector.

[R627] MINOR Tests - `scripts/suite_shards.py:77`, `:281`, `:585`, `:643`; receipts `prior-f1-reproduction.json` and `prior-f1-*.log` - F1 below remains open. Independent owner/measurement oracles and real driver lists pass. The four assigned controls detect their named guard mutants; removed pins and first-suite setup mischarging also fail. The CI contract self-test passes 1821 items and 2530 arms, and selector/tally/cancellation integration remains green. Those results do not cover the missing independent check of the 60% policy itself.

[R627] PASS Docs - `scripts/suite_shards.py:2`, `:27`; `docs/testing/CI_WORKFLOWS.md:183`, `:320`; public assignment, PR body and executable evidence; receipts `refresh-verbatim.log`, `docs-check.log`, `doc-style.log`, `doc-paths.log`, `toc-check-pinned.log`, `em-dash-pinned.log` - Checked balancing/gate descriptions, executed refresh recipe, replaced hash landmarks and explicit limits against the code. The two prose-only corrections below do not change any measurement, figure, gate, verdict, generated artifact, conformance claim or privacy rule. The workflow's inherited "four hashed workers" comment is knowingly retained under acceptance 2; it is not relied on as algorithm authority.

**Findings and public dispositions.**

- **R627-1-F1**, retained from **R626-1/F1**. Severity **MINOR**. All attributable lenses: **Tests**. Artifacts: `scripts/suite_shards.py:77`, `:281`, `:585`, `:598`, `:643`; [prior public finding](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6125953320); [independent reproduction](receipts/prior-f1-reproduction.json).
  Authority/evidence: issue #727 fixes the bound at 60% of the workflow's timeout. AGENTS.md's Tests lens requires defect-detecting controls. The tightened-timeout and heavy-duration controls derive their expected limits from the same `bound_seconds()` / `HEADROOM_PERCENT` inputs as the gate. Separate disposable copies with `HEADROOM_PERCENT = 75`, `HEADROOM_PERCENT = 100`, or division by `10` instead of `100` all return exit 0, `selftest: PASS`, and no ESCAPED arm. Their printed bounds are respectively 5400, 7200 and 43200 seconds; pristine is 4320.
  Impact: a one-token regression can relax the policy while every worker's ownership self-test and the serial preflight remain green. The present implementation uses the correct 60%; this is a regression-test weakness, not an incorrect current prediction. Required outcome: add an independent self-test expectation for the mandated 60% calculation, retaining the workflow timeout as the authoritative input. Both a loosened percentage and a loosened arithmetic formula must be detected. Verification: rerun `scripts/reproduce_prior_f1.py`'s four cases against the corrected head, updating its expected outcomes: pristine must remain exit 0; all three mutants must exit 1 with a named failed/ESCAPED control. Re-run the selector and affected integration gates. Tests remains UNCLEAN until fixed and re-reviewed.

- **R627-1-R1**, severity **RESIDUE**, all attributable lenses **Docs**. Artifact: `docs/testing/CI_WORKFLOWS.md:191`, the sentence ending "measured from one dev run."
  Authority/evidence: precise provenance at `scripts/suite_shards.py:86` and `receipts/suite-measurements.csv` already records `maap` from the separate #696 run. Impact: the summary omits this documented exception; all figures and acceptance results remain correct. Required outcome / exact fix: replace `each worker's job overhead, measured from one dev run.` with `each worker's job overhead. All figures come from one dev run, except` and the next line `` `maap`, measured on #696's hosted run. `` Verification: compare the revised summary with unchanged table provenance and rerun touched documentation checks.

- **R627-1-R2**, severity **RESIDUE**, all attributable lenses **Docs**. Artifact: [PR #728](https://github.com/kebag-logic/milan-fpga/pull/728), Known limitations bullet beginning "Overheads assume warm Verilator, Yosys and tsn-gen caches"; repeated in published `author/HANDOFF.md:443`.
  Authority/evidence: `.github/workflows/rtl.yml:288` always clones and builds the field generator on worker 1, without a cache step. Its measured 115-second overhead already includes this. Impact: only the cache explanation is inaccurate; no measurement or prediction changes. Required outcome / exact fix: use `Overheads assume warm Verilator and Yosys caches; worker 1's overhead includes the tsn-gen build.` in the PR bullet. Preserve the historical receipt and attach its wording correction. Verification: compare with unchanged setup steps and confirm unchanged duration/prediction figures.

Both corrections are wording-only descriptions of already-correct evidence, within the supplied RESIDUE rule. Neither defers a code, test, measurement or compliance defect.

The final public reconciliation also retains these dispositions from the linked R626-1 comment. There are no formal review submissions or inline review comments in the final snapshot; the prior findings are in that conversation comment.

| Prior ID | Disposition at this head | Evidence, impact, required outcome and verification |
|---|---|---|
| R626-1/F1 | RETAINED, MINOR, Tests; R627-1-F1 above | Independently reproduced; no source fix exists at this head. |
| R626-1/R1 | RETAINED, RESIDUE, Docs; R627-1-R1 above | Same provenance wording correction; exact figures already match. |
| R626-1/R2 | RETAINED, RESIDUE, Docs | `.github/workflows/rtl.yml:136` still says `four hashed workers`. Exact wording fix: `four workers balanced by measured hosted time (#727)`. Acceptance 2 freezes this file, so the manager must decide when to apply the prose-only correction. Verify that no workflow key or executed command changes. |
| R626-1/S1 | RETAINED, optional SUGGESTION, Robustness and Tests | `scripts/suite_shards.py:541` and `:628`: the filename-based checkout predicate permits head-arm skipping for the cancellation fixture. Consider an explicit fixture opt-out or checking actual checkout inputs. Verify fixture compatibility and that a real checkout always runs the head arms. This optional mutant was not re-executed here; its public receipt remains the evidence, and normal supported entry points were checked independently. |
| R626-1/S2 | RETAINED, optional SUGGESTION, Tests | `scripts/suite_shards.py:197` and `:278`: add in-self-test plants for zero duration and a mirrored worker count. Verify each is caught and each corresponding guard mutant escapes its control. These optional guard mutants were not re-executed here; the six-worker tree fault was independently refused. |

Suggestions do not leave lenses unclean. Retaining F1 does. No prior finding is treated as resolved merely by this report or by moving it to another work item.

**Reviewer-owned completion ledger.**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen #727 assignment; table/balance/bound; workflow; measurement CSVs; assignment oracle | R627-1 | a57d384dc697249c2a69f80079b676875d4f7560 |
| RTL | CLEAN | Complete diff; unchanged driver, setup workflow and tally interfaces; byte/index/gitlink audit | R627-1 | a57d384dc697249c2a69f80079b676875d4f7560 |
| Robustness | CLEAN | Missing/stale/heavy/timeout/worker-count/workflow faults; boundary/pin controls; cancellation | R627-1 | a57d384dc697249c2a69f80079b676875d4f7560 |
| Tests | UNCLEAN (F1) | Actual lists; independent heap/decimal oracles; nine detected mutants, three surviving bound mutants; selector/tally/CI self-tests | R627-1 | a57d384dc697249c2a69f80079b676875d4f7560 |
| Docs | CLEAN | Docstring and executed recipe; policy diff; public evidence; documentation gates; R1/R2 residue | R627-1 | a57d384dc697249c2a69f80079b676875d4f7560 |

**Execution and reproduction.**

Set `packet` and `checkout` to the packet and exact-head checkout paths. Run the programs from the checkout. All disposable state belongs under `scratch/`:

```sh
python3 "$packet/scripts/focused_checks.py" "$checkout" "$packet"
python3 "$packet/scripts/refresh_receipts.py" "$checkout" "$packet"
python3 "$packet/scripts/audit_measurements.py" "$checkout" "$packet"
python3 -m venv "$packet/scratch/markdown-env"
TMPDIR="$packet/scratch" "$packet/scratch/markdown-env/bin/python" -m pip install --no-cache-dir --require-hashes -r tools/markdown/requirements.txt
python3 "$packet/scripts/static_checks.py" "$checkout" "$packet"
python3 "$packet/scripts/verify_checkout.py" "$checkout" "$packet"
python3 "$packet/scripts/reproduce_prior_f1.py" "$checkout" "$packet"
```

Public downloads require repository read access. The unmodified selector, CI contract check/self-test, tally self-test, cancellation test, Python idiom gate, test-evidence ratchet, whitespace and documentation checks pass. Two initial documentation checks exited 2 because the pinned renderer was absent; both pass with the isolated pinned environment. Both initial and corrected receipts are retained. No shared installation changed.

| Required control | Source-head result | Defeated guard | Mutant result |
|---|---|---|---|
| Missing duration | Gate and sharded selection `[ok]` | Missing entries admitted at zero cost | Both controls ESCAPED, exit 1 |
| Stale duration | `[ok]` | Stale-entry comparison removed | ESCAPED, exit 1 |
| Workflow timeout | 116-minute bound rejected; 117-minute bound accepted | Bound mirrored from 120 minutes | 116-minute control ESCAPED, exit 1 |
| Heavy duration | Exact bound accepted; one second above and balanced growth rejected | Overhead dropped, mean-only limit, inclusive comparison or disabled bound | Corresponding controls ESCAPED, exit 1 |

Additional pin-removal and measurement-start mutants fail their named controls. Tree faults are separately checked through the CLI. An initially malformed disposable mutation expression was corrected before collecting final mutation receipts; no syntax failure counts as detection evidence.

The F1 reproduction script exits successfully when it confirms the defect at this reviewed head: all three invalid bound mutants survive the source self-test. Its success is evidence of the finding, not a passing implementation gate.

Final integrity checks compare raw bytes and modes with the reviewed tree, plus index equality. They cover 1295 parent blobs, 214 axis blobs, 562 protocol-processor blobs and 104 gPTP processor blobs. Registered required submodules match the gitlinks: axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, protocol processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`, gPTP processor `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`. No tracked bytes, modes or index entries were altered by this review.

**Limits and pending manager duties.**

- One dev sample plus #696's substituted window establishes a prediction, not a bound over runner variation or cold caches. Four workers have only 115-117 seconds of acceptance margin.
- Full parent/processor/synthesis/builder banks were not run here. Source-head execution evidence is the executor's published gate record plus these focused receipts. No manager source bank was run or inferred at this head.
- The manager owns hosted acceptance 3, required executed exact-head contexts and local workflow-replica acceptance. Skipped contexts are not executed jobs; a status snapshot supplies no unobserved success.
- Final public metadata (`receipts/final-head-runs.json`, `final-head-checks.json`, observation time in `reconciliation-start.json`) shows all four workflows still in progress. All five Verilator shard jobs are in progress, while Physical gPTP is explicitly skipped. `full-ci-gate`, the four Yosys shard jobs, lint, elaboration smoke, BDD and some documentation contexts show success; these do not constitute completed exhaustive aggregate evidence or acceptance 3.
- The manager must construct and validate the final current-dev merge candidate at the merge turn, including builder and native banks, then publish receipts. Source validation here is distinct from that candidate. No already-tested candidate is claimed.
- F1 requires a source correction and independent re-review. The manager must reconcile both review ledgers, carry the retained residue items, wait for outstanding rounds, obtain required merge authorization, perform post-merge containment, and close the issue/project work item when complete. No merge is cleared by this NEGATIVE verdict.
- Physical calibration was NOT RUN. Field skips and static or simulated evidence provide no hardware proof.
- No GitHub write, source fix, commit, push, merge, hardware access or host workflow orchestration occurred. Disposable copies and installations are confined to unpublished `scratch/`. `MANIFEST.sha256` enumerates publishable packet files.

R627-1 FINISHED
