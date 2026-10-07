[R545] NEGATIVE - exact head ced667d8ee35929ab5f9e77a1c5396e173a693d8

Issue [#16](https://github.com/kebag-logic/lwSRP/issues/16) / PR [#15](https://github.com/kebag-logic/lwSRP/pull/15), external independent round R545-1.
Tree: `52d750190ca4c8835870598900ffb751cc85a31e`.
The frozen acceptance is satisfied. One MINOR documentation finding prevents a positive verdict.

The review followed the supplied instructions, then CONTRIBUTING, README and guides, public acceptance, the local standard and interfaces, diff/history, and public evidence.
No repository AGENTS.md was present. No private author material, management checkout, lane scratchpad, or another review report informed the independent pass.
The [independent verdict and ledger](receipts/independent-verdict.md) were written before examining earlier public findings.

The [review-start notice](https://github.com/kebag-logic/lwSRP/pull/15#issuecomment-6038102557) freezes this head and requires independent review before merge.
Public comment inventories returned no additional scope decisions or manager evidence comments.
The final inventory contains zero issue comments, two PR review-start notices, zero submitted reviews, and zero inline comments.

**Open finding R545-1-F1 — MINOR — attributable lenses: Docs.**

Artifacts: [doc/manager.md:56](https://github.com/kebag-logic/lwSRP/blob/ced667d8ee35929ab5f9e77a1c5396e173a693d8/doc/manager.md#L56), the following line, and [doc/tester.md:193](https://github.com/kebag-logic/lwSRP/blob/ced667d8ee35929ab5f9e77a1c5396e173a693d8/doc/tester.md#L193).

| Current claim | Exact-head result | Required correction |
| --- | --- | --- |
| Manager guide, OFF: 86 tests / 19885 assertions | 87 tests / 19901 assertions | Replace both stale figures. |
| Manager guide, ON: 86 tests / 19873 assertions | 87 tests / 19889 assertions | Replace both stale figures. |
| Tester guide: 93 reversals in both profiles | 94 in each profile | Change 93 to 94. |

Authority/evidence: the PR adds one test and one reversal. Its updated README and tester result rows already report the measured unit totals.
The [OFF unit receipt](receipts/OFF-ctest.log), [ON unit receipt](receipts/ON-ctest.log), and [reversal audit](receipts/reversal-audit.json) establish the current figures.
Impact: public descriptions of current test evidence conflict and omit this PR's added test and reversal.
Required outcome: apply all three corrections above and reconcile the current-result figures across the guides.
Verification: compare the corrected prose against both profile receipts and the 94-case inventory, then rerun documentation checks on the corrected head.
This is not RESIDUE: correction changes reported measurements and figures. No production defect or executable test gap was found within this scope.

**Acceptance and Conformance evidence.**

I read the local IEEE 802.1Q-2018 PDF, clause 10.7.7, Table 10-3, printed page 270.
The [standard review receipt](receipts/standard-review.json) records its digest and the independently derived state oracle without reproducing the standard.
The [published standard reference](https://standards.ieee.org/ieee/802.1Q/6844/) identifies the edition.

| Note / event / initial Applicant | PointToPointMAC false | PointToPointMAC true | Named upstream regression |
| --- | --- | --- | --- |
| 4 / rJoinIn / VO | AO | VO | `applicant_receive_conditions_follow_link_mode`, integration_test.c:324 |
| 4 / rJoinIn / VP | AP | VP | `pending_applicant_joinin_obeys_note_four`, integration_test.c:352 |
| 5 / rIn / AA | AA | QA | `applicant_receive_conditions_follow_link_mode`, integration_test.c:324 |

Both loops execute both Boolean values. The tests use full participants; selectable point-to-point subset mode is outside this issue's acceptance.
The wire vectors carry one VLAN value, 2. Event octets 36 and 72 encode JoinIn and In, respectively.
The existing test establishes AA through declaration and accepted transmission before injecting In.
The new test asserts VP before reception and checks both final Applicant state and registration on port zero.

I checked the public configuration, receive, declaration, transmit, and observation contracts in `src/include/shish_lan/mrp.h`.
The table entries and guard in `src/core/mrp_mad.c:207`, `:223`, and `:507` agree with the oracle.
MVRP exercises the shared Applicant implementation in both configured build profiles.

The [complete diff](receipts/head-diff.txt) changes only README.md, doc/tester.md, tests/check_reversals.py, and tests/unit/integration_test.c.
The [history](receipts/history.txt) contains two topic commits and the non-fast-forward merge.
Its parents are `72209a53a241cd5de4786d3e1b3aefcbdf5fa5d9` and source base `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`.
Both source trees have ID `f46e01d3bf1c753009479d32e69d00263ee124ed`; the source diff is empty.
The current main delta at `3626f1eaca76cb0ad3e4ea4335fe34e9eb5738f2` affects LICENSE only.
That comparison used the [public API receipt](receipts/main-compare.json), because the main object was absent locally.

**Robustness and executable evidence.**

Each link-mode iteration creates and destroys its own application. Its fixed vectors and configuration avoid timing and random-input dependencies.
The snapshot helper requires exactly one attribute. The VP test additionally verifies registration, preventing an ignored receive from satisfying its Applicant assertion alone.
The reversal runner starts from a passing baseline, rejects behavioral compilation failures, checks named failures, restores each mutation, and finishes with a passing suite.

| Check | OFF | ON | Receipt |
| --- | --- | --- | --- |
| Debug configure and shared 16-job build | PASS | PASS | [Build](receipts/build-both.log); configure logs |
| ctest: one registered target containing 87 C tests | 19901 assertions, rc 0 | 19889 assertions, rc 0 | [OFF](receipts/OFF-ctest.log), [ON](receipts/ON-ctest.log) |
| behave execution | 3 scenarios / 10 steps, rc 0 | 3 scenarios / 10 steps, rc 0 | [OFF](receipts/OFF-behave.log), [ON](receipts/ON-behave.log) |
| Entire unmodified reversal campaign | 94/94 detected, rc 0 | 94/94 detected, rc 0 | [OFF](receipts/OFF-reversals.log), [ON](receipts/ON-reversals.log) |
| Restored build and ctest | PASS | PASS | Per-profile `receipts/reversals/` logs and commands.json |

The reversal inventory comprises 90 behavioral mutations and four deliberate compiler, header, or embedded-link failures.
All behavioral mutants compiled successfully. All 61 explicit required-test mappings matched actual failure records in both profiles.
The four nonbehavioral cases produced their intended diagnostics; they are not counted as behavioral regression failures.

| Note-related reversal | Required failing tests | OFF / ON |
| --- | --- | --- |
| `point-to-point-condition` | `applicant_receive_conditions_follow_link_mode`; `pending_applicant_joinin_obeys_note_four` | Build rc 0; ctest rc 8; both names fail in each profile. |
| `pending-point-to-point-condition` | `pending_applicant_joinin_obeys_note_four` | Build rc 0; ctest rc 8; named test fails in each profile. |
| `shared-in-condition` | `applicant_receive_conditions_follow_link_mode` | Build rc 0; ctest rc 8; named test fails in each profile. |

The [independent receipt audit](receipts/reversal-audit-run.log) checks names on failure records, positive baselines, and restoration.
Every campaign command, return code, and raw log is retained under `receipts/reversals/OFF/` and `receipts/reversals/ON/`.

Documentation execution passed: 975 sentence/fragments, zero unlinked references, 79 reference controls, 354 local links, and 20 external links.
Both anonymous and repository-authenticated link checks passed. All 27 graphs rendered successfully and were visually inspected.
Those checks do not validate reported test totals, so F1 remains open despite their success.

**Prior findings and public evidence.**

No prior review FINDINGS were present on PR #15 when the final public inventory was taken.
After recording my independent verdict, I inspected the two linked parent findings that motivated issue #16.

| Prior finding | Disposition at this head | Exact-head evidence |
| --- | --- | --- |
| [R532-1-F2, part 3](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6032564515), unguarded note-4/5 regression behavior | RESOLVED within issue #16 scope | Six oracle cells pass; all three guard reversals fail the required names in both profiles. |
| [R533-2-F2](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6035155719), unpublished upstream test fix | RESOLVED | Exact public head is retrievable; source equivalence and independently executed positive/mutation receipts are established. |

Other parent findings concern a different review scope and are not adjudicated here.
The [disposition receipt](receipts/prior-finding-disposition.json) records this boundary.

I inspected the [specified public evidence bundle](https://github.com/kebag-logic/milan-fpga/tree/03b25f532812ccc40a75c96cb91ec643af22e108/review-evidence/lwsrpnotes-r1).
Its two published files match the manifest digests. They summarize author results and the PR description; they do not supply complete raw manager-bank logs.
The [publication receipt](receipts/publication-validation.json) confirms those hashes and the still-published exact head.
The [hosted inventory](receipts/hosted-exact-head.json) has zero check runs, zero statuses, and zero workflow runs.
Its aggregate status says pending because there are no contexts. There is no executed or skipped hosted job here to count as a pass.

**Reviewer-owned ledger.**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Issue #16; local Table 10-3 notes 4/5; mrp.h contracts; integration_test.c:324,352; unchanged Applicant table/guard; six-cell oracle | R545-1 | ced667d8ee35929ab5f9e77a1c5396e173a693d8 |
| RTL | CLEAN | Not applicable: complete diff and tracked tree inventory; no RTL change and no production-source change | R545-1 | ced667d8ee35929ab5f9e77a1c5396e173a693d8 |
| Robustness | CLEAN | Test lifecycle/vector/snapshot/registration checks; check_reversals.py baseline/build/failure/finally contracts; named-failure and restored-byte audit | R545-1 | ced667d8ee35929ab5f9e77a1c5396e173a693d8 |
| Tests | CLEAN | Both profile builds, 87-unit suites, executed scenarios, 94-case campaigns, named-failure receipts and restored passes | R545-1 | ced667d8ee35929ab5f9e77a1c5396e173a693d8 |
| Docs | UNCLEAN | CONTRIBUTING, README, all guides, PR body, public evidence, all doc/tools checks and graph inspection; open R545-1-F1 | R545-1 | ced667d8ee35929ab5f9e77a1c5396e173a693d8 |

**Integrity, limits, and manager duties.**

The [final integrity receipt](receipts/integrity.log) verifies all 60 tracked file blobs, Git modes, index entries, exact head/tree, and a clean worktree.
The exact tree has no submodule gitlinks or .gitmodules; there are no submodule entries to restore in this clone.
Both disposable reversal copies match the original tracked source, tests, and build-definition bytes and modes after restoration.
No source fix, commit, push, GitHub write, merge, shared installation, or other-checkout edit was performed.

The unit framework was built from public release 1.7.0 in packet scratch. Its resolved commit and archive digest are in [environment.json](receipts/environment.json).
Builds and independent checks ran concurrently under foreground supervisors, with a shared 16-job build limit.
The campaign driver has no jobs option and uses two build workers per profile. No heavy hardware build or RTL execution was needed.
[Portable reproduction instructions](REPRODUCE.md) accompany the scripts and raw receipts.

The scenario suite verifies operation return codes, not independently observed switch state; its existing limitation does not supply additional protocol coverage.
Full parent, processor, timing-protocol, synthesis, builder, container, host-CI, target, and hardware banks were not run by this reviewer.
The supplied manager source static/builder and native-bank passes remain manager evidence, distinct from these focused reviewer executions.
Physical calibration is NOT RUN. Field skips are not hardware proof.

The manager must resolve F1, obtain review coverage for the corrected head, and retain the full completion bar before merging.
The manager owns hosted/local-workflow acceptance and must distinguish executed jobs from skipped contexts.
The manager also builds and validates the final current-dev candidate at the merge turn.
The supplied source base is `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`; the supplied live dev is `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`.
This source-head review does not certify that unbuilt candidate or a parent dependency update.
The manager publishes this packet after terminal execution. No other reviewer result is adopted as this reviewer's verdict.

R545-1 FINISHED
