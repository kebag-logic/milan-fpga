[A359] REVIEW READY

Commit: `24d32d549fa7470318a93984403a92423a63fa25` (local commit on `396-release-gates`; not pushed).
Refs #396. Round 2 desk acceptance items 1, 2 and 5 are ready for independent re-review. Bench items 3 and 4 remain open.

Changed:
- `REQUIREMENTS.md:250`, `docs/testing/TESTING.md:841`, and `tb/tools/torture_campaign.py:3323`: implement the recorded T0 timing decision, last pre-cut advertisement expiry, provisional 30-second automatic restoration bound, subsequent controller reconnect below one second, and a derived restoration-bound-plus-margin boot window.
- `tb/tools/torture_campaign.py:3367`: correct release assertion citations against directly extracted standards pages; distinguish sequence/uncertainty, asCapable, persistence, advertising, automatic restoration, and controller reconnect.
- `tb/tools/torture_campaign.py:3456`: refuse AAF/CRF overlap; require sampling <=60 seconds, stream-binding inventory and explicit complete topology for eligibility.
- `tb/tools/torture_campaign.py:3510`: add the single-boot assertion and observation oracle that rejects a repeated BIOS pass even when streaming later recovers.
- `tb/tools/torture_campaign.py:4816`, `tests/features/torture_campaign_plan.feature:341`, `tests/steps/torture_release_steps.py:118`: test every repeat, both roles, independent AAF/CRF omissions, non-default parameters, per-phase snapshots and eligibility boundaries.

Validation: all commands ran in the foreground from `$LANES/396-release-gates` at the commit above, with the pinned Markdown dependencies available. All required gates returned 0.

| Command | Result |
|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | rc 0; 47 tests |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | rc 0; 68 scenarios / 297 steps; none skipped |
| `python3 -B scripts/check_feature_status.py --self-test` | rc 0; 46/46, zero findings |
| `python3 -B scripts/docs_check.py` | rc 0; zero findings |
| `python3 -B scripts/check_doc_paths.py` | rc 0; 850 paths resolve |
| `python3 -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31` | rc 0; zero findings, 339/339 arms |
| `python3 -B scripts/gen_toc.py --check` | rc 0 |
| `python3 -B scripts/check_doc_style.py` | rc 0 |
| `python3 -B scripts/check_py_idiom.py` | rc 0; no ratchet increase |
| `python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power` | rc 0; both complete |
| `git diff --check` | rc 0 |
| `git diff ac18b50968b12efe4d15c0a06301264b35656b31 HEAD --check` | rc 0 |

All four scripts from public branch `396-review-evidence` were extracted with `git show`, verified byte-identical and run unchanged against this committed head or its disposable export:

| Reproduction | Result |
|---|---|
| Internal `planner_mutants.py` | rc 0; pristine gates 0/0; 42/44 killed, one survivor, one invalid anchor |
| Internal `plan_omission_probe.py` | rc 0; 240 omissions, three topologies, zero accepted |
| External `mutants.py` | rc 0; pristine gates 0/0; all 21 killed; source bytes restored |
| External `audit_probe.py` | rc 0; real audit rejects D1-D6 |

All seven required internal mutants A04, A05, P01, P03, P07, C01 and C08 are killed; informational C09 is also killed. A08 remains the prior report's informational false-red-only survivor. C13 is invalid because its `boot_observation_s=480` anchor was removed by the decision; it is not counted as killed. A separate control replacing the new derived window with 60 seconds is killed by both suites (expected rc 1 each), without modifying the public scripts.

Acceptance criteria: desk items 1, 2 and 5 implemented with the evidence above. Physical items 3 and 4 remain open. The #366 oracle has desk controls; its physical negative control has not been run.

Open risks/questions: `restore_bound_s=30` remains provisional and requires manager ratification from #397 and #75 measurements. The bench still supplies the power-strip hook, journal-window instrumentation and complete physical evidence. Eligibility is a configured-prerequisite check, not a measured release verdict. Independent re-review remains required; this comment makes no approval or lens-coverage claim.

`HANDOFF.md`, the full replacement `PR-BODY.md`, source-page citation receipt, command logs, script hashes and result tables are prepared in the assigned output directory. No firmware, RTL, builder or submodule changes; no push, PR edit, merge, hardware action or other checkout. Working tree clean.
