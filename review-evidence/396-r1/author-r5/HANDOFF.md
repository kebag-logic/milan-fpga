# Round 5 handoff

Role: [A364], author for issue #396 and PR #586.

## Candidate and scope

- Branch: `396-release-gates`.
- Starting head: `54d9beea2888bd07369e67e5cb025d1405d03495`.
- Candidate head: `07f72ad640f99c43bc1354642ad4d7ed8ba410cc`.
- One local commit: `fix: allow capture resolution at release uncertainty start`.
- Origin confirmed: `https://github.com/kebag-logic/milan-fpga.git`.
- Physical worktree: `$LANES/396-release-gates`.
- Desk acceptance items 1, 2 and 5 remain the assigned scope.
- Physical acceptance items 3 and 4 remain open.

Authority: [round-5 assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5856062292)
and [external round-4 report](https://github.com/kebag-logic/milan-fpga/pull/586#issuecomment-5856058686).
The issue body and all 13 comments were read, including every assignment.
The extracted full report matches the public review comment exactly.
Repository workflow, quality, testing and cited requirement entry points were read.
Cited Milan v1.2 and IEEE 1722/1722.1 clauses were extracted locally;
the clock-validity logic and both frame-launch latches were inspected read-only.

## Status

All 18 assigned gate invocations pass at the candidate head.
All 35 unchanged public review scripts pass, with historical qualifications below.
Independent re-review is still required. This packet carries evidence, no review verdict.

## Change list

| File:line | Change |
|---|---|
| `REQUIREMENTS.md:263` | Defines event containment as `[observed_start - observation_resolution_s, clear)`, identifies the observed start, and includes launch/correlation error in resolution. Links the round-5 decision. |
| `docs/testing/TESTING.md:915` | Aligns the evidence row and grading procedure with that window; gives passing/failing lag examples and preserves the last-event clearing deadline. |
| `docs/testing/TESTING.md:957` | Documents the existing rule's lack of a separate bound before the first event, with the review's example. Other soak assertions remain independent. |
| `tb/tools/torture_campaign.py:3390` | Carries the event window and resolution provenance in the assertion text. |
| `tb/tools/torture_campaign.py:3536` | Validates the original observed interval, then derives the inclusive event-window start by subtracting resolution. Leaves the clear edge exclusive. |
| `tb/tools/torture_campaign.py:3581` | Emits the explicit `tu_event_window` argument. |
| `tb/tools/torture_campaign.py:5184` | Adds nine independent start/clear boundary cases and preserves every earlier chain, missing-evidence and late-clear arm. |
| `tb/tools/torture_campaign.py:5204` | Tests the existing late-first-event interpretation, including a late-clear refusal. |
| `tb/tools/torture_release_mutants.py:78` | Adds six named behavioral mutations for missing/doubled allowance, inclusive/exclusive edges, assertion text and the plan argument. |
| `tests/features/torture_campaign_plan.feature:421` | Adds nine feature examples for lone-event containment. |
| `tests/steps/torture_release_steps.py:293` | Grades each independent example through the real oracle, using the emitted holdover bound. |

## Round 5 results

The event window starts at the earliest timestamp allowed by observation error.
The returned last-discontinuity timestamp stays the original recorded event.
Clearing still uses that event plus 0.5 seconds and recorded resolution.
Zero resolution remains valid. Missing or malformed evidence cannot pass.

| Control | Result | Evidence |
|---|---|---|
| Lone event half a resolution before observed start | PASS | Self-test and feature |
| Lone event twice a resolution before start | FAIL as required | Self-test and feature |
| Lone event exactly at start, positive or zero resolution | PASS | Self-test and feature |
| Lone event exactly one resolution before start | PASS | Self-test and feature |
| Lone event just outside that window | FAIL as required | Self-test and feature |
| Original -0.1-second event | FAIL as required | Original chain arm and new lone-event arm |
| Event exactly at clear or after clear | FAIL as required | Self-test and feature |
| External oracle probe, Part B | All six lags PASS | `R347-4-scripts-tu_oracle_probe.log` |
| External cycle/phase sweep | PASS | `R347-4-scripts-tu_anchor_model.log` and probe Part A |
| External T02 mutation | Killed by both suites | `R347-4-scripts-mutants_r4.log` |
| External round-4 mutation suite | 16 killed; zero survivors/invalid anchors | Same log |
| Repository mutation controls | 25 named behavioral kills | `release-mutants.log` |

The unchanged public T02 anchor still applies to the derived event-window start.
Its strict comparison fails both the zero-resolution and inclusive-boundary controls.
Informational I01 now subtracts resolution a second time; its kill proves that
additional allowance is refused. No public script was edited for either result.

Suggestion dispositions: S1 is taken as documentation and a test of existing
behavior; no new duration policy is introduced. S2's issue-comment pointer is
constrained by the explicit head-only notification instruction. The full change,
validation, acceptance and risks are provided in `PR-BODY.md` and this packet.

## Gate table

All commands ran in the foreground from the physical worktree, without piping
a gate. The actual interpreter, arguments, head, exit and log hash are in
`commands.jsonl`. A temporary environment outside this output directory provided
the hash-pinned Markdown requirements. The table uses `python3` for readability.

| Command | rc | Result | Log |
|---|---|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 0 | 54 tests passed | [planner-self-test.log](planner-self-test.log) |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 0 | 86 scenarios / 353 steps; no skips | [behave-plan.log](behave-plan.log) |
| `python3 -B -m behave tests/features --tags=@torture -f progress` | 0 | 231 scenarios / 898 steps; 172 scenarios excluded by tags | [behave-torture-tier.log](behave-torture-tier.log) |
| `python3 -B tb/tools/torture_release_mutants.py` | 0 | 25 named behavioral kills; pristine baseline passed | [release-mutants.log](release-mutants.log) |
| `python3 -B scripts/check_feature_status.py --self-test` | 0 | 46/46 controls; zero findings | [feature-status-selftest.log](feature-status-selftest.log) |
| `python3 -B scripts/check_feature_status.py` | 0 | Zero findings | [feature-status.log](feature-status.log) |
| `python3 -B scripts/docs_check.py` | 0 | Zero findings; 23/23 scrub controls; 4/4 routing controls | [docs-check.log](docs-check.log) |
| `python3 -B scripts/check_doc_paths.py` | 0 | 850 cited paths resolve | [doc-paths.log](doc-paths.log) |
| `python3 -B scripts/check_doc_style.py` | 0 | 22 current documents pass | [doc-style.log](doc-style.log) |
| `python3 -B scripts/check_py_idiom.py` | 0 | No new debt or ratchet changes | [py-idiom.log](py-idiom.log) |
| `python3 -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31` | 0 | Zero findings; 339/339 controls | [em-dash.log](em-dash.log) |
| `python3 -B scripts/gen_toc.py --check` | 0 | Pass | [gen-toc.log](gen-toc.log) |
| `python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power` | 0 | Both areas complete | [coverage-by-area.log](coverage-by-area.log) |
| `python3 -B tb/tools/torture_campaign.py --plan --areas soak,power --json` | 0 | Three diagnostic repeat contracts | [plan-json.log](plan-json.log) |
| `git diff --check` | 0 | Clean | [diff-worktree.log](diff-worktree.log) |
| `git diff ac18b50968b12efe4d15c0a06301264b35656b31 HEAD --check` | 0 | Clean | [diff-base.log](diff-base.log) |
| `git diff 8153576af6d739427b54f6c40299b0e57bc481ae HEAD --check` | 0 | Clean | [diff-round3.log](diff-round3.log) |
| `git diff 54d9beea2888bd07369e67e5cb025d1405d03495 HEAD --check` | 0 | Clean | [diff-round4.log](diff-round4.log) |

## Public review evidence

Scripts were fetched from `396-review-evidence` at
`e3df1b3364391368ed05d84b44b653e46d51a62e` and extracted with `git show` into
`/tmp/396-a364-review`. SHA-256 provenance is in `review-script-provenance.json`.
Mutating scripts operate on disposable exports in `/tmp/396-a364-validation`;
read-only probes and gate runners use the physical candidate worktree as required.
The public scripts remain byte-identical to their published blobs.

All 35 public script files completed with rc 0, including duplicate copies,
probes, attribution scripts and both gate runners. Every nested gate also
returned zero. Final byte comparisons match the published blobs exactly.
The full per-script table is in `PUBLIC-SCRIPTS.md`; exact commands are in
`commands.jsonl`.

| Public suite | Result |
|---|---|
| Internal round 1 | 42 killed; one informational survivor; one invalid anchor |
| Internal round 2 | 48 killed; zero survivors; two invalid anchors |
| Internal round 3 | 28 killed; three optional/equivalent survivors; three invalid anchors |
| External round 1 | 21/21 killed |
| External round 2 | 22/22 killed |
| External round 3 | 23 applicable mutations killed; three superseded anchors unapplied |
| External round 4 | 16/16 killed; zero survivors/invalid anchors; T02 killed by both suites |
| Omission probes | Every copy rejects all 240 omissions across three topologies |
| Audit probes | Every copy rejects all six planted defects |
| External wire-lag probe | Part A passes; Part B 6/6 PASS |
| Cycle models and gate runners | All rc 0; every nested gate rc 0 |

The historical generic-audit A08 survivor is informational. The internal
round-3 survivors are the equivalent eight-second CLI default, alternative
ADP prose, and a redundant feature-oracle removal. The removed boot literal,
superseded ADP strings and earlier uncertainty wording remain invalid anchors,
not kills. Current repository controls cover the replaced contracts.
The external round-3 script labels its three unapplied anchors as survivors
in its final count; all 23 applied mutations are killed.
The unchanged old ADP probe prints obsolete hardcoded arithmetic; it does not
evaluate the corrected T0 expression. Its output is retained as historical
probe behavior, not a finding against the corrected contract.


## Integrity and limitations

`final-integrity.json` records the candidate tree, six changed files and blob hashes.
The worktree is clean. There is exactly one commit on the requested starting head.
The commit has one subject line, no body and no trailers. Gitlinks are unchanged.
No firmware, RTL, builder or submodule edit occurred. No other checkout, push,
PR creation/edit, merge, delegation or hardware action was performed.
Temporary environments and exports are outside this output directory.
Every retained packet file is below 200 KB.

The only initial quality failure was one overlong mutation-table line.
It was split before the commit; the exact-head quality gate passes unchanged.
The system interpreter lacked the Markdown binding, so the pinned dependencies
were installed in a temporary environment before the final gates.

The 30-second restoration ceiling remains provisional pending #397/#75 measurements.
The physical soak, cold-cut campaign, known-defect control and retained bench evidence
remain open. The current rule has no separate pre-first-event duration bound and
no numeric resolution ceiling; measured capture/correlation provenance is required.
Independent review, publication, hosted evidence and merge validation remain external
follow-up work. Nothing in this packet claims physical release acceptance.

## Final notification

After the packet is complete, post `REVIEW-READY.md` to issue #396, then stop.
The replacement `PR-BODY.md` is prepared for the authorized publisher; it is not posted.
