# Issue #396 - round 4 handoff

Author: [A362]
Status: assigned local work complete and ready for independent re-review.

## Repository and assignment

- Origin: `https://github.com/kebag-logic/milan-fpga.git`, verified before edits.
- Physical worktree: `$LANES/396-release-gates`.
- Branch: `396-release-gates`.
- Starting head: `8153576af6d739427b54f6c40299b0e57bc481ae`.
- Current head: `54d9beea2888bd07369e67e5cb025d1405d03495`.
- One local commit: `Anchor release uncertainty at the last recorded discontinuity`.
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5855792297
- Internal report: https://github.com/kebag-logic/milan-fpga/pull/586#issuecomment-5855777031
- External report: https://github.com/kebag-logic/milan-fpga/pull/586#issuecomment-5855789830

The complete issue body and all eleven comments were read, as were both full
round-3 reports and the current PR body. The earlier decisions were retained
except where round 4 expressly replaces the uncertainty anchor.
`standards-and-context.md` records source checks and supporting context.

The assignment permits desk items 1, 2 and 5 only.
Bench items 3 and 4 remain open. There is no unresolved desk decision.
No push, PR modification, merge, hardware action, other checkout, submodule
edit, firmware edit, RTL edit or builder edit was performed.
The assigned final action is one new REVIEW READY comment with the head.

## Change list

| File:line | Change and purpose |
|---|---|
| `REQUIREMENTS.md:262` | Require an event within each uncertainty interval; anchor at the last recorded discontinuity before clearing; identify accepted event kinds and resolution provenance; link round 4 |
| `docs/testing/TESTING.md:915` | State the same anchor in the evidence row and procedure; distinguish the project's minimum interpretation; explain sync and timestamp evidence |
| `docs/testing/TESTING.md:936` | Document the observation oracle and the 0.62-second pass / 0.8-second failure examples |
| `docs/testing/TESTING.md:955` | Clarify that actual discharge and configured hold both constrain a cold cut |
| `tb/tools/torture_campaign.py:3390` | Align the operator-facing uncertainty assertion with the decision |
| `tb/tools/torture_campaign.py:3534` | Add a pure observation oracle over a complete wire interval and recorded event timestamps |
| `tb/tools/torture_campaign.py:3575` | Emit the last-event origin, accepted event kinds and capture-resolution source |
| `tb/tools/torture_campaign.py:4988` | Pin the omitted CLI power-off hold to eight seconds |
| `tb/tools/torture_campaign.py:5136` | Pin the new argument contract, chained-event outcomes, evidence boundaries and assertion phrases |
| `tb/tools/torture_release_mutants.py:47` | Add ten mutation controls while retaining the previous nine |
| `tests/features/torture_campaign_plan.feature:414` | Exercise the assigned chained-event and uncorrelated cases in the feature suite |
| `tests/steps/torture_release_steps.py:262` | Check the emitted contract and call the observation oracle with independent expected outcomes |

## Decision and suggestion disposition

| Item | Implementation and evidence |
|---|---|
| External F1 / round-4 items 1-2 | One anchor in requirements, testing row, assertion and args. GM at 0 plus step at 0.2: clear 0.62 PASS; clear 0.8 FAIL; no event FAIL, with 0.001-second resolution |
| External S1 | Key uncertainty/ADP phrases and CLI default pinned. New controls kill changes to the five-second prose bound, uncorrelated failure, pre-cut ADP anchor, charged off time and CLI default |
| External S2 | 0.25 seconds is stated as the standard's duration and the project's minimum interpretation |
| External S3 | Text clarifies the effective minimum as the longer of configured hold and verified discharge; elapsed time alone cannot prove a cold cut |
| External S4 | Text and args require wire-capture and correlated event-timestamp resolution, excluding periodic counter cadence; no unassigned numeric ceiling introduced |

The numeric oracle uses the plan's emitted holdover bound and measured
observation resolution. Its caller supplies complete capture evidence and
only accepted discontinuity kinds on the same correlated clock. It does not
perform hardware acquisition or attest timestamp provenance.

## Results

| Check | Result |
|---|---|
| Origin and starting head | Exact match |
| Planner self-test | 52 tests passed |
| Plan feature | 77 scenarios / 326 steps passed, none skipped |
| Full torture tier | 222 scenarios / 871 steps passed; 172 scenarios excluded by tags |
| Release mutation driver | Clean baseline; all 19 defects killed by named tests; source unchanged |
| Feature-status controls | 46/46; zero findings |
| Documentation | Zero findings; 850 cited paths resolve; contents and style pass |
| Source quality | Pass without ratchet changes |
| Area coverage | Soak and power complete |
| Whitespace | Worktree, round-4 delta and full lane delta clean |

## Gate table

All gates below ran at `54d9beea2888bd07369e67e5cb025d1405d03495`.
Commands ran in the foreground, with captured return codes and no gate pipeline,
from the physical worktree above. `$MDPY` is
`/tmp/396-a362-markdown/bin/python`, installed from the hash-locked
`tools/markdown/requirements.txt`. The environment is outside this packet.
`gates.json` retains exact arguments, head, duration and log names.

| Gate | Command | rc | Evidence |
|---|---|---|---|
| planner-self-test | `python3 -B tb/tools/torture_campaign.py --self-test` | 0 | `planner-self-test.log` |
| behave-plan | `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 0 | `behave-plan.log` |
| behave-torture-tier | `python3 -B -m behave tests/features --tags=@torture -f progress` | 0 | `behave-torture-tier.log` |
| release-mutants | `python3 -B tb/tools/torture_release_mutants.py` | 0 | `release-mutants.log` |
| feature-status-selftest | `python3 -B scripts/check_feature_status.py --self-test` | 0 | `feature-status-selftest.log` |
| feature-status | `python3 -B scripts/check_feature_status.py` | 0 | `feature-status.log` |
| docs-check | `python3 -B scripts/docs_check.py` | 0 | `docs-check.log` |
| doc-paths | `python3 -B scripts/check_doc_paths.py` | 0 | `doc-paths.log` |
| doc-style | `python3 -B scripts/check_doc_style.py` | 0 | `doc-style.log` |
| py-idiom | `python3 -B scripts/check_py_idiom.py` | 0 | `py-idiom.log` |
| em-dash | `$MDPY -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31` | 0 | `em-dash.log` |
| gen-toc | `$MDPY -B scripts/gen_toc.py --check` | 0 | `gen-toc.log` |
| coverage-by-area | `python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power` | 0 | `coverage-by-area.log` |
| plan-json | `python3 -B tb/tools/torture_campaign.py --plan --areas soak,power --json` | 0 | `plan-json.log` |
| diff-check-worktree | `git diff --check` | 0 | `diff-check-worktree.log` |
| diff-check-base | `git diff ac18b50968b12efe4d15c0a06301264b35656b31 HEAD --check` | 0 | `diff-check-base.log` |
| diff-check-round4 | `git diff 8153576af6d739427b54f6c40299b0e57bc481ae HEAD --check` | 0 | `diff-check-round4.log` |

## Public script reproduction

Public source: `396-review-evidence` at
`0563bb47f92f36c1f37b9a310debe93dd2795a27`.
Each script was extracted with `git show` into temporary storage and executed
unchanged. Mutating scripts operate on disposable exports of the committed
head. Read-only probes use the physical worktree or its export.
No additional checkout was created. Exact commands and results are in
`review-script-results.json`; hashes are in `review-script-provenance.json`.
All 32 script files, including duplicate copies, have a final rc 0.
Both unchanged gate runners also report rc 0 for every nested gate.

| Suite | Result |
|---|---|
| Internal round 1, including duplicate copies | 42 killed, A08 informational survivor, C13 invalid |
| Internal round 2, including duplicate copies | 48 killed, no survivors, R13/R19 invalid |
| Internal round 3 | 28 killed, three optional/equivalent survivors, three invalid anchors |
| External round 1 | 21/21 killed |
| External round 2 | 22/22 killed |
| External round 3 | 23 killed, no applicable survivors, three unapplied old anchors |
| Omission probes | Each rejects all 240 omissions across three topologies |
| ADP hold probe | Zero unexpected results |
| All 32 public scripts | Final rc 0; unchanged bytes confirmed |
| Cycle transcription | At a 0.2-second step delay: clear 0.451-0.699 seconds after GM change, 0.251-0.499 seconds after the last step |

Invalid anchors are not kills. C13 names the superseded 480-second boot
literal; R13/R19 name superseded round-2 ADP text. Round-4 edits supersede
internal N20/N21/N23 and external M07/M08/M09. The new repository controls
kill the current origin/resolution/prose-bound mutations without editing any
public script. External M10/M15/M16/M19 now fail named self-tests.

The internal optional survivors remain N18 (equivalent hardcoded eight),
N24 (alternative ADP prose mutation), and S01 (redundant step oracle removal).
A08 remains the older informational generic-audit control. These are reported
as survivors, never counted as kills or as an independent review verdict.

The first external round-3 probe attempt exited 1 because its temporary export
omitted REQUIREMENTS.md and TESTING.md. The export was completed from the same
commit and the unchanged probe then returned 0. Both attempt records and the
initial setup-failure log are retained. No candidate change was required.

The cycle transcription's concluding prose describes the starting head's
first-event rule. Its numeric sweep, not that historical prose, is relevant
to the corrected rule. The round-2 external probe similarly retains obsolete
hardcoded ADP arithmetic; it is not a current-plan verdict.

## Open work and handoff state

The seven-day shipping-image soak, 200 cold cuts, physical negative control,
and retained bench evidence remain unperformed under acceptance items 3 and 4.
The manager must ratify the provisional restoration ceiling using #397/#75.
The bench must provide discharge, journal-window, wire and event instrumentation.
Desk checks do not qualify a release or discharge #70/#117.

Independent re-review of this head and required publication/merge validation
remain pending. This packet contains evidence, not approval or a review ledger.
`PR-BODY.md` is the full proposed replacement body; no PR edit was made.
Final integrity passes: clean worktree, exact one-commit parent, six allowed
changed paths, identical committed bytes, unchanged gitlinks and public scripts.
`final-integrity.json` records the tree and source hashes.
The packet contains no environment, packages, export or file over 200 KB.

The final public action is the prepared `[A362] REVIEW READY` comment on
issue #396 with the full head, after this packet is finalized.
The issue itself supplies the publication receipt. Work stops after posting.
