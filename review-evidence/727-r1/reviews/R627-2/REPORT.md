[R627] POSITIVE - exact head 61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3

External independent review R627-2 of issue #727 / PR #728. All five lenses are CLEAN. No open BLOCKER, MAJOR or MINOR remains. Round-1 F1 is resolved, including the three required mutation reproductions. This source-review verdict does not discharge hosted acceptance 3 or authorize merge.

Reviewed tree: `8fd4dbd4f35e3892f7df8f2e404302e3658d443d`. Source base: `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`. Full scope: the six-commit, two-file diff from that base; the round-2 delta from `a57d384dc697249c2a69f80079b676875d4f7560` comprises three commits. Only `scripts/suite_shards.py` and `docs/testing/CI_WORKFLOWS.md` change.

The public contract was reconstructed in the requested order: AGENTS.md/CONTRIBUTING.md, docs/README.md, the [frozen assignment](https://github.com/kebag-logic/milan-fpga/issues/727#issuecomment-6121794007) and [round-2 decision](https://github.com/kebag-logic/milan-fpga/issues/727#issuecomment-6126048117), REQUIREMENTS.md:305 and interface authorities, then the complete diff/history and [published executable evidence](https://github.com/kebag-logic/milan-fpga/tree/b98797c2089896573d5c56b8e16ee0d1df712fa1/review-evidence/727-r1). `receipts/independent-verdict.md` records my independent verdict and ledger before reading either prior review's finding body. No private author material or another reviewer's current-round report was read. Review start: [R627-2](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6126299951).

**Measurements and assignment.**

All 62 `SUITE_SECONDS` entries and five `WORKER_OVERHEAD_SECONDS` entries match independent decimal-timestamp arithmetic on the hosted logs. `--measure` was also executed and agrees. `receipts/suite-measurements.csv` records every suite's source log, start/end timestamps, exact window and rounded value; `overhead-measurements.csv` records setup, tail, log span and rounded overhead. Original logs are included.

The five successful workers of dev run `38217650945` supply the figures except `maap`. Its completed window in job `114677344710`, run `38208503834`, is `1374.1774735` seconds, rounded upward to `1375`. The worker's later cancellation does not invalidate that completed window; its incomplete log supplies no overhead. The assignment's approximately 1380-second figure therefore does not supersede its measured-window rule. The `tree-maap-1380` probe also passes. Dev's superseded `maap` value is 185 seconds. Overheads are exactly `(83, 115, 80, 93, 80)`; each first-suite window excludes setup.

An independent longest-first allocator reproduces every owner and load. The actual driver lists contain the complete 62-suite filesystem inventory once. Four process hash seeds (0, 1, 2, 12345) and 30 shuffled inventories preserve the assignment. Serial/default output equals the base selector's lexical selection; the scheduled physical suite stays separate. Tables and five list outputs equal round 1 byte-for-byte. Workflow, suite driver and tally-reader bytes equal the source base.

| Worker | Suites | Predicted seconds including overhead | Bound | Spare seconds |
|---|---:|---:|---:|---:|
| 0/5 | 15 | 4204 | 4320 | 116 |
| 1/5 | 16 | 4205 | 4320 | 115 |
| 2/5 | 14 | 4203 | 4320 | 117 |
| 3/5 | 16 | 4205 | 4320 | 115 |
| 4/5 | 1 | 2877 | 4320 | 1443 |

`milan_dp` remains alone on 4/5; `tsn_fuzz` stays on 1/5 and `chmap_capture` on 3/5, matching `rtl.yml:208-222` and its setup steps. Acceptance 1, 2 and 4 are supported. Acceptance 3 requires the manager's actual PR-head worker measurements.

**Round-2 control results.**

The published R626-1 `mutate.py` was downloaded unmodified, checked against its public Git blob and executed with `--jobs 8` in disposable trees. All 29 cases ran without replacement drift. Its SHA-256 and each result appear in `receipts/mutation-summary.json`; raw results are in `r626-mutants.log`.

| Required case | Result | Named failing control |
|---|---|---|
| `tree-head` | rc 0, PASS | All eleven planted-defect controls `[ok]` |
| `headroom-75-percent` | rc 1 | Only the new 36-second arm ESCAPED; 5400 s applied at 120 minutes |
| `headroom-100-percent` | rc 1 | Only that arm ESCAPED; 7200 s applied |
| `bound-formula-div10` | rc 1 | Only that arm ESCAPED; 43200 s applied |
| `table-zero-duration-allowed` | rc 1 | Only the zero-duration arm ESCAPED |
| `worker-count-mirrored-5` | rc 1 | Only the six-worker arm ESCAPED |

At `scripts/suite_shards.py:605-611`, the independent expectation is literally `{minutes: minutes * 36 for minutes in applied}`. It reads neither `bound_seconds` nor `HEADROOM_PERCENT`. The applied bounds come from the actual workflow and two altered timeouts; the pristine result is `{116: 4176, 117: 4212, 120: 4320}`. Source inspection and an AST check verify that independence.

The original required controls also detect their defects. Missing-duration admission escapes both missing-entry arms; deleting the stale comparison escapes the stale arm; mirroring the timeout escapes the tightened-timeout arm and new law check. Dropping overhead, checking only the mean, or refusing equality escapes the relevant heavy/boundary control. Pin removal/movement, dedicated-worker removal and wrong measurement start/rounding fail their checks. Separate entry-point faults refuse missing, stale, zero and heavy durations, a 116-minute timeout, six workers and missing workflow. Missing/stale sharded selections exit 2; their serial selections still enumerate successfully.

**Prior findings, explicitly reconciled.**

The [R626-1 findings](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6125953320) and [R627-1 findings](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6126041660) were read after the independent pass and preliminary verdict. No formal or inline reviews exist in the inspected public snapshot.

| Prior ID | Severity; all attributable lenses | Disposition | Artifact, authority/evidence, impact, required outcome and verification |
|---|---|---|---|
| R626-1/F1 = R627-1-F1 | MINOR; Tests | RESOLVED | `suite_shards.py:605-611`; round-2 item 1 requires an independent 60% expectation. Silent policy loosening is now detected. All three required mutants exit 1 with the new arm ESCAPED; pristine exits 0. Required outcome met. |
| R626-1/R1 = R627-1-R1 | RESIDUE; Docs | RESOLVED | `CI_WORKFLOWS.md:191-196` now names the dev-run provenance and separate `maap` PR-run exception. Only summary wording changes. Compared against table provenance; documentation checks pass. |
| R627-1-R2 | RESIDUE; Docs | RESOLVED in current PR body and published replacement | `receipts/public-pr-body.md`, Known limitations, and published `author-r2/PR-BODY.md` say: `Overheads assume warm Verilator and Yosys caches; worker 1's overhead includes the tsn-gen build.` This matches unchanged `rtl.yml:278-292`, with no figure change. Historical receipts remain historical; the public correction supplies their disposition. |
| R626-1/R2 | RESIDUE; Docs | RETAINED for #495 by explicit round-2 item 4 | `rtl.yml:136-137` still says `four hashed workers`. Exact fix: `four workers balanced by measured hosted time (#727)`. Impact is stale comment wording only; executed configuration remains correct. Manager carries it to #495/residue tracking. Verify a comment-only change with no workflow key or command changed. |
| R626-1/S1 | SUGGESTION; Robustness, Tests | RETAINED, optional | `suite_shards.py:541-545,651-654`; filename-based fixture detection permits head-arm skipping. The `head-arms-skipped` mutant still returns 0. Normal checkout entry points run the head arms and missing workflow fails. Optional outcome: explicit fixture opt-out or detection from checkout inputs. Verify fixture compatibility and mandatory head checks in real checkouts. No supported-path defect was found. |
| R626-1/S2 | SUGGESTION; Tests | RESOLVED | `suite_shards.py:585-588,613-620` now plants zero duration and worker drift. Both faults are refused; weakening either guard yields its own ESCAPED arm and rc 1. Optional round-2 item 3 is met. |

No new blocking or minor finding is added. The retained residue changes no measurement, test, code, generated artifact, verdict, conformance/clause claim or privacy rule. The optional suggestion does not leave a lens unclean.

**Independent lens results.**

[R627] PASS Conformance - `suite_shards.py:90-158,204-311`, frozen issue #727 acceptance, `rtl.yml:148`, measurement CSVs and `assignment.json` - Checked all figures, placement, completeness, owners and 60% arithmetic against the public contract. Hosted acceptance 3 remains reserved.

[R627] PASS RTL - `review-diff.patch`, `run_all_suites.sh:168-189,291`, `suite_tally.py:398`, `rtl.yml:208-222`, canonical ownership script in `ci_events.py` - CLI/refusal/discovery/preflight and setup integration persist. No HDL, testbench, firmware, clock/reset/CDC/FSM or gitlink artifact changes. Major suites query datapath source/flag lists and build their own objects; `milan_dp_gm_steps/Makefile:31` invokes the isolated leg already measured cold on its earlier worker. No assignment-dependent warm-artifact requirement was found in the examined Makefiles.

[R627] PASS Robustness - `suite_shards.py:188-200,258-408,568-645`, `fault-*.log`, `selection-*.log`, `r626-mutants.log`, `cancellation.log` - Checked table disagreement, positive durations, job-key parsing, missing workflow, worker drift, exact-bound/one-second-over behavior, heavy growth, altered pin weights, malformed/failed timing input, incomplete logs and cancellation integration.

[R627] PASS Tests - `suite_shards.py:489-718`, especially `:605-620`, `mutation-summary.json`, `review-probes.log`, `focused-gates.json` - Independent expectations agree; required mutations expose named controls and F1 is resolved. Workflow check/self-test passes 1821 items and 2530 arms. Tally, cancellation, Python idiom and test-evidence gates pass. Surviving advisory mutants are documented below, never counted as detected.

[R627] PASS Docs - `suite_shards.py:1-48`, `CI_WORKFLOWS.md:183-210,325-328`, current PR body and documentation receipts - The refresh shell ran verbatim and reproduced the dev tables. Its prose explicitly retains the separate `maap` figure until dev measures #696. Policy describes the actual algorithm and former hash placement accurately. Requested R1/R2 corrections are present.

**Reviewer-owned completion ledger.**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen assignment; tables/balance/bound; measurement CSVs/logs; independent assignment | R627-2 | 61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3 |
| RTL | CLEAN | Full diff; driver/tally/workflow interfaces; cross-suite Makefiles; byte/index/gitlink audit | R627-2 | 61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3 |
| Robustness | CLEAN | Entry-point faults; 29-case campaign; timeout/count/pin/boundary/log controls; cancellation | R627-2 | 61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3 |
| Tests | CLEAN | Independent 36-second law; required escapes; measurement/assignment oracles; integration gates | R627-2 | 61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3 |
| Docs | CLEAN | Policy diff; executed refresh docstring; corrected PR body; public evidence; documentation gates | R627-2 | 61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3 |

**Execution and restoration.**

Recorded selector, workflow check/self-test, tally self-test, cancellation, Python idiom, test-evidence, documentation/style/path and whitespace checks pass. Two initial renderer-dependent checks returned 2 because a pinned dependency was absent; both pass in an isolated environment installed from hash-locked requirements. Both refusal and successful rerun receipts remain. No shared installation changed.

Run from the exact-head checkout, setting `packet` to the packet location:

```sh
export TMPDIR="$packet/scratch" PYTHONDONTWRITEBYTECODE=1
python3 "$packet/scripts/review_probes.py" "$PWD" "$packet"
sh "$packet/scripts/refresh_verbatim.sh"
python3 "$packet/scripts/measurements.py" "$PWD" "$packet"
python3 -I "$packet/scripts/r626_mutate.py" "$PWD" "$packet/scratch/r626-mutants" --jobs 8
python3 "$packet/scripts/focused_gates.py" "$PWD" "$packet"
python3 -m venv "$packet/scratch/markdown-env"
"$packet/scratch/markdown-env/bin/python" -m pip install --no-cache-dir --require-hashes -r tools/markdown/requirements.txt
python3 "$packet/scripts/pinned_docs.py" "$PWD" "$packet"
python3 "$packet/scripts/verify_checkout.py" "$PWD" "$packet"
```

Downloads require repository read access. The focused-gate driver can initially return nonzero for missing renderer dependencies; `pinned_docs.py` provides their isolated rerun. Independent child processes are bounded and joined; no detached work remains. One preliminary help-option invocation unexpectedly executed cancellation fixtures in the default temporary directory. It finished and its fixture directory was verified absent; none of that invocation's output is counted as evidence. The recorded cancellation run used packet scratch. A malformed reviewer fixture replacement was repaired before final fault receipts; no syntax failure counts as detection.

No source fix, commit, push, GitHub write, merge or other-checkout edit occurred. Final verification hashes raw tracked bytes against commit blobs, checks modes, compares index records/stages, rejects hidden index flags and proves required registered submodule heads. It covers 1295 parent blobs, 214 axis blobs, 562 protocol-processor blobs and 104 gPTP-processor blobs. Parent status is empty. Required gitlinks are axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, protocol processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`, gPTP processor `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`. Nothing required restoring in the checkout.

**Real limits and pending manager duties.**

- The table is one dev sample plus #696's substituted completed window. Four workers retain only 115-117 seconds of margin against 72 minutes. Prediction does not guarantee runtime under runner/cache variation.
- `head-arms-skipped` and `nondeterministic-tie` survive the 29-case campaign. The first is retained optional S1. The second is a publicly documented coverage limit: an in-process comparison cannot detect hash-seed-dependent ties. The actual head uses lexical ties and passed four process seeds. Neither surviving mutant is counted as detected or as a current incorrect assignment.
- Source-head execution evidence is the author's published gate record and these focused receipts. **No manager source bank runs at this exact head, and none is claimed or inferred.** Full parent/processor, synthesis/builder banks, simulation suite builds, host workflow orchestration and local workflow replicas were not run here.
- At `2026-10-12T14:39:14Z`, exact-head rtl-full run `38262957309` had all five Verilator workers in progress. Four Yosys worker contexts reported success; Physical gPTP was explicitly skipped. All four workflows remained in progress. `receipts/hosted-snapshot.json` distinguishes executed, pending and skipped contexts; successful worker contexts do not establish completed aggregates or acceptance 3.
- The manager owns hosted acceptance 3: each actual PR-head worker must complete within 4320 seconds and predicted versus measured values must be published. Required hosted contexts and local-replica acceptance remain manager duties.
- At the merge turn the manager must build and validate the current-dev candidate, including builder and native banks, and publish receipts. Supplied live dev is `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`. Source checks here are distinct from that final validation and claim no already-tested candidate.
- The manager must reconcile both independent ledgers, wait for outstanding rounds, carry the comment residue to #495, obtain required merge authorization, perform post-merge containment and close the issue/project item only when the full bar is met.
- Physical calibration was NOT RUN. Field skips, static checks and simulated evidence provide no hardware proof.

`MANIFEST.sha256` enumerates publishable scripts and receipts with packet-relative paths. `scratch/` is excluded from publication.

R627-2 FINISHED
