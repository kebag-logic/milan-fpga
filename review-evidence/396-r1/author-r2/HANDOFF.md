# [A359] Round 2 handoff

Status: desk changes committed and ready for independent re-review.
All 12 required gates returned 0 at `24d32d549fa7470318a93984403a92423a63fa25`.
This is author validation evidence, not a review verdict or completion ledger.

| Artifact | Value |
|---|---|
| Issue | https://github.com/kebag-logic/milan-fpga/issues/396 |
| PR | https://github.com/kebag-logic/milan-fpga/pull/586 |
| Round-2 assignment | https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5854930205 |
| Worktree | `$LANES/396-release-gates` |
| Branch | `396-release-gates` |
| Verified origin | `https://github.com/kebag-logic/milan-fpga.git` |
| Starting head | `b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3` |
| Final head | `24d32d549fa7470318a93984403a92423a63fa25` |
| Commit subject | `fix: enforce release timing and qualification contracts` |
| Takeover | https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5854960348 |

## Change list

Round 2 changes five files. The cumulative PR also contains the original
CONTRIBUTING.md gate declaration and plan-step integration.

| File:line | Change |
|---|---|
| `REQUIREMENTS.md:250` | Correct clause anchors, T0/pre-cut expiry, provisional restoration bound, derived boot observation, qualification prerequisites and single-boot criterion |
| `docs/testing/TESTING.md:841` | Exact measurement formulas, eligibility semantics, explicit topology/inventory, and desk/bench evidence boundary |
| `tb/tools/torture_campaign.py:3323` | Sampling ceiling 60 s; restore and margin parameters; validated topology attestation |
| `tb/tools/torture_campaign.py:3367` | Corrected soak/power citations and distinct automatic/controller reconnect assertions |
| `tb/tools/torture_campaign.py:3456` | Refuse overlapping AAF/CRF indices |
| `tb/tools/torture_campaign.py:3491` | Common eligibility prerequisites and full explicit CLI topology checks |
| `tb/tools/torture_campaign.py:3510` | Complete UART/reset evidence oracle: one BIOS pass and zero extra restarts |
| `tb/tools/torture_campaign.py:3547` | Per-cycle T0 origins, captured ADP expiry, restore bound and derived boot window |
| `tb/tools/torture_campaign.py:4816` | Counter and AAF/CRF omissions in every repeat and direction; non-default parameters and snapshot policies |
| `tb/tools/torture_campaign.py:4970` | Eligibility boundaries, incomplete topology, overlap and repeated-boot controls |
| `tb/tools/torture_campaign.py:5375` | CLI restoration-bound and observation-margin parameters |
| `tests/features/torture_campaign_plan.feature:341` | Thirty omission examples plus non-default timing and repeated-boot scenarios |
| `tests/steps/torture_release_steps.py:118` | Updated defaults and independent scenario assertions |

## Assignment results

| Required outcome | Result and evidence |
|---|---|
| Automatic restore has a finite T0 bound | Provisional 30 s, inclusive; each persisted binding, both directions/CRF; non-default 19 s and 23 s tests |
| Pre-cut ADP expiry | Last pre-cut raw PDU plus host timestamp; decoded field multiplied by two; missing/expired capture fails; no readiness origin |
| Additional reconnect | CONNECT_RX success to first valid AVTP strictly below 1 s, only after automatic restoration succeeds |
| Boot observation | Restore bound plus named 5 s default margin; margin cannot extend any pass deadline; repeated BIOS pass fails |
| Citation corrections | Direct source-page extraction recorded in `standards-citations.md` |
| Eligibility | Interval <=60 s, binding inventory, explicit complete topology, plus area duration/count/phase minimums |
| Every repeat and each traffic kind | Both roles, descriptor kinds, AAF-only and CRF-only direction removal, including journal-commit repeat |
| Requested internal survivors | A04, A05, P01, P03, P07, C01 and C08 all killed; informational C09 also killed |
| External survivors | All 21 mutants killed, including every audit mutant |
| Desk acceptance items 1, 2, 5 | Implemented; required gates pass; independent re-review pending |
| Bench acceptance items 3, 4 | Open: exact-image campaigns and physical known-defect control were not run |

## Public review reproductions

The four scripts were extracted with `git show` from the public
`396-review-evidence` branch into `/tmp/396-a359-review` and run unchanged.
`review-script-provenance.json` records the source commit and byte hashes.
Exports and environments were kept under `/tmp`, outside the output directory.
The candidate worktree was never used as mutation scratch.

| Script / control | Exit | Result | Receipt |
|---|---|---|---|
| Internal `planner_mutants.py` | 0 | Pristine gates 0/0; 44 mutants: 42 killed, 1 survived, 1 invalid | `internal-mutants.log` |
| Internal `plan_omission_probe.py` | 0 | 240 omissions over three topologies; zero accepted | `omission-probe.log` |
| External `mutants.py` | 0 | Pristine gates 0/0; 21/21 killed; exported source restored byte-for-byte | `external-mutants.log` |
| External `audit_probe.py` | 0 | Real audit rejects D1-D6; deliberately broken audit variants admit the expected defects | `audit-probe.log` |
| Supplemental current boot-window mutant | 0 runner | Hardcoded 60 s killed by both gates (each expected rc 1); export restored | `supplemental-boot-mutation.log` |

A08 is the internal report's informational false-red-only generic-coverage
mutant; it still survives and was not among the seven mandated kills.
C13 is invalid because its old `boot_observation_s=480` source anchor was
removed by the round-2 decision. It is not counted as killed. The separate
current-contract boot mutation above supplies the replacement check without
editing either public mutation script.

Reproduction commands, from the physical worktree:

```sh
python3 -B /tmp/396-a359-review/planner_mutants.py $LANES/396-release-gates /tmp/396-a359-internal-mutants
python3 -B /tmp/396-a359-review/plan_omission_probe.py $LANES/396-release-gates
python3 -B /tmp/396-a359-review/mutants.py /tmp/396-a359-external-tree
python3 -B /tmp/396-a359-review/audit_probe.py /tmp/396-a359-external-tree
```

The external tree is a `git archive` export of the final head's `tb/tools`,
`tests` and `scripts`. Full command arrays and return codes are also in
`review-results.json`. Script exit 0 alone is not a mutation verdict; the
individual results above were inspected.

## Required gate table

All commands ran in the foreground from the physical worktree, with no gate
piped. `python3` resolved to `/tmp/396-a359-docenv/bin/python3`, a disposable
environment containing the hash-pinned `tools/markdown/requirements.txt`
dependencies and the existing behavior-test dependency. No gate required a
source change or weakened threshold to pass. `gates.json` records head,
commands, timings and receipts.

| Command | Exit | Result | Receipt |
|---|---|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 0 | 47 tests passed | `planner-selftest.log` |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 0 | 68 scenarios / 297 steps passed; none skipped | `plan-feature.log` |
| `python3 -B scripts/check_feature_status.py --self-test` | 0 | 46/46 controls passed; zero findings | `feature-status-selftest.log` |
| `python3 -B scripts/docs_check.py` | 0 | Zero findings | `docs-check.log` |
| `python3 -B scripts/check_doc_paths.py` | 0 | 850 paths resolve | `doc-paths.log` |
| `python3 -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31` | 0 | Zero findings; 339/339 test arms | `em-dash.log` |
| `python3 -B scripts/gen_toc.py --check` | 0 | TOC check passed | `toc.log` |
| `python3 -B scripts/check_doc_style.py` | 0 | 22 current documents passed | `doc-style.log` |
| `python3 -B scripts/check_py_idiom.py` | 0 | No ratchet increase | `python-idiom.log` |
| `python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power` | 0 | Both release areas complete | `area-coverage.log` |
| `git diff --check` | 0 | Clean | `diff-worktree.log` |
| `git diff ac18b50968b12efe4d15c0a06301264b35656b31 HEAD --check` | 0 | Clean | `diff-base.log` |

## Remaining work and limits

The 30 s bound remains provisional pending the manager's #397 boot-to-entity-
enabled and #75 restart measurements. The power-strip adapter, journal-window
instrumentation and physical captures remain bench responsibilities. The
boot oracle consumes complete observations; no hardware adapter was added.
Eligibility checks configured prerequisites, not descriptor truth, successful
campaign execution, or timing-bound ratification.

No firmware, RTL, builder, submodule or other lane changed. No push, PR edit,
merge, hardware action, or additional checkout was performed. The working
tree is clean. The commit subject has no body or trailers. Hosting, local CI
replication after a later push, independent re-review and any eventual merge
remain subsequent work. Existing unrelated citation/input-parsing concerns
remain outside this assignment as recorded in the public review.

`PR-BODY.md` is the full replacement body for the manager to apply.
`REVIEW-READY.md` is the final issue comment prepared for posting.
