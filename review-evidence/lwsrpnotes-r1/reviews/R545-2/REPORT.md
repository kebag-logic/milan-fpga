[R545] POSITIVE - exact head f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152

External independent review, round R545-2, for [issue #16](https://github.com/kebag-logic/lwSRP/issues/16) and [PR #15](https://github.com/kebag-logic/lwSRP/pull/15).
Tree: `e7c4cf6a8fb382e5260f5fc9674c21c286289841`.
No open BLOCKER, MAJOR, or MINOR remains. All five lenses are CLEAN for this delta. R544-1-S1/S2 remain nonblocking suggestions.

The sole commit after `ced667d8ee35929ab5f9e77a1c5396e173a693d8` changes exactly three prose lines in two files.
The manager guide now reports 87 tests with 19901 default and 19889 Milan assertions; the tester guide reports 94 reversals.
Fresh runner summaries and the actual driver inventory agree with every corrected figure.
Nothing else changed in this round: see [round-2 diff](receipts/round-2.diff), [full diff](receipts/full.diff), and [history](receipts/history.txt).

**Scope and independent reconstruction.**

I read the supplied review instructions, CONTRIBUTING.md, README and the documentation guides, then the frozen acceptance and public scope.
There is no repository AGENTS.md. Issue #16 has no comments; PR #15's manager notices freeze the review heads and require independent reviews before merge.
The [public start](https://github.com/kebag-logic/lwSRP/pull/15#issuecomment-6038440539) identifies this head and tree.
The linked parent scope decisions require upstream note tests, both profiles, no production-source change, and separate manager candidate validation.

The applicable authority is issue #16's four acceptance items, its [IEEE 802.1Q-2018 reference](https://standards.ieee.org/ieee/802.1Q/6844/), and the configuration/observation contracts in `src/include/shish_lan/mrp.h:307,409,417`.
I inspected the unchanged Applicant guard and table in `src/core/mrp_mad.c:207,223,506`, and the guide's stated link-mode conditions.
I then independently examined the complete base-to-head diff and history, followed by the specified public evidence.
The [independent verdict and ledger](receipts/independent-verdict-and-ledger.md) were written before reading prior public review findings.
No private author material, management checkout, lane scratchpad, or other review report informed that pass.

| Frozen acceptance | Artifact and result at this head |
| --- | --- |
| Note 4: VP and VO, both link-mode values | `tests/unit/integration_test.c:324,352`: VO becomes AO on shared links and remains VO on point-to-point links; VP becomes AP or remains VP respectively. |
| Note 5: AA/rIn, both values | `applicant_receive_conditions_follow_link_mode` establishes AA, then checks AA on shared links and QA on point-to-point links. |
| Named reversals fail the tests in both profiles | Three relevant cases at `tests/check_reversals.py:74-81`, with required names at lines 185-189; all six fresh executions meet their required failure records. |
| Nothing changes in src/ | Exact source equality to `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`, checked independently. |

The new VP regression retains a Registrar registration assertion, so merely discarding receive processing cannot satisfy it.
Each link-mode iteration owns and destroys its application. The state snapshot requires exactly one attribute.
No test, production source, build definition, interface, register map, RTL input, generated artifact, or gitlink changed in round 2.

**Executed evidence.**

| Check | Result | Receipts |
| --- | --- | --- |
| Default Debug build, unit target and runner | rc 0; 87 tests, 19901 assertions | [Runner](receipts/OFF-unit.log), [target](receipts/OFF-ctest.log), OFF configure/build logs |
| Milan Debug build, unit target and runner | rc 0; 87 tests, 19889 assertions | [Runner](receipts/ON-unit.log), [target](receipts/ON-ctest.log), ON configure/build logs |
| Reversal inventory | 94 entries, all names unique; required note-test mappings match | [Inventory](receipts/inventory.json) |
| Three note reversals, default | Each mutant compiles, fails its required named regression, and is restored; final positive check rc 0 | [Summary](receipts/focused-reversals-OFF.log), [commands](receipts/reversals-OFF/commands.json) and per-case raw logs |
| Three note reversals, Milan | Same outcomes; final positive check rc 0 | [Summary](receipts/focused-reversals-ON.log), [commands](receipts/reversals-ON/commands.json) and per-case raw logs |
| Sentence check | rc 0; 975 fragments, zero over limit | [Log](receipts/sentences.log) |
| Reference check and self-test | rc 0; zero unlinked references, 79 controls pass | [References](receipts/references.log), [controls](receipts/references-self-test.log) |
| Links | rc 0; 354 local links and 20 external URLs, zero failures | [Log](receipts/links.log) |
| Graph rendering | rc 0; all 27 graphs rendered | [Log](receipts/graphs.log) |
| Whitespace | rc 0 | [Log](receipts/whitespace.log) |
| Final integrity | 60 tracked blobs, modes and index entries match; detached head/tree exact; clean checkout; zero gitlinks | [Audit](receipts/checkout-final.json) |

For each profile, `point-to-point-condition` fails both note tests; `pending-point-to-point-condition` fails the VP test; `shared-in-condition` fails the existing VO/AA test.
Every behavioral mutant build returns 0 and its test command returns 8. The [receipt audit](receipts/receipt-audit.json) checks names on actual failure records.
The full 94-case campaigns were not repeated: this delta changes no driver or test bytes. The count is verified directly from the same driver used by both profiles.

**Prior findings, resolved or retained.**

The prior [internal findings](https://github.com/kebag-logic/lwSRP/pull/15#issuecomment-6038397736) and [external finding](https://github.com/kebag-logic/lwSRP/pull/15#issuecomment-6038429517) were read only after the independent verdict and ledger were written.

| ID | Severity; all attributable lenses | Artifact, authority, impact and required outcome | Verification and disposition |
| --- | --- | --- | --- |
| R544-1-F1 | MINOR; Docs, Tests | `doc/manager.md:56-57`; stale measurements contradicted the executable evidence and CONTRIBUTING's evidence requirements. Required 87 tests with 19901/19889 assertions. | Both fresh runner summaries match the corrected lines; documentation checks pass. RESOLVED. |
| R544-1-F2 | MINOR; Docs, Tests | `doc/tester.md:193`; 93 understated the driver's case count and issue #16's reversal evidence. Required 94. | Actual CASES contains 94 unique entries, with no profile-specific pruning; corrected prose and checks agree. RESOLVED. |
| R545-1-F1 | MINOR; Docs, Tests | Same three locations and measurements; original external attribution was Docs, with Tests also attributable through the shared measurement defect. Required all three corrections. | The complete requested correction is the exact three-line delta, independently measured above. RESOLVED. |

These were measurement defects, not wording-only RESIDUE. There is no new RESIDUE finding.

- **R544-1-S1 — SUGGESTION — Tests, Conformance — RETAINED.** Artifact: `src/core/mrp_mad.c:507-509` and the note tests at `tests/unit/integration_test.c:324,352`. The prior public finding reports that extending the point-to-point rJoinIn suppression to every Applicant state escapes the suite. Its authority is Table 10-3's unaffected AA/rJoinIn cell. Impact: a future overly broad guard could escape these tests; this does not violate issue #16's frozen VO/VP and AA/rIn acceptance. Suggested outcome: add a point-to-point AA/rJoinIn-to-QA control and a reversal that over-applies note 4. Verification: the new control passes normally and fails that compiling mutant in both profiles. This additional mutant was not rerun in this documentation delta; the suggestion is carried forward explicitly.
- **R544-1-S2 — SUGGESTION — Docs — RETAINED.** Artifact: PR #15 body, the note-4/note-5 bullets. The body can identify the existing VO/AA test and the newly added VP test more precisely. Authority/evidence: the test names and full diff above. Impact: readers cannot immediately distinguish existing coverage from the added regression; acceptance remains satisfied. Suggested exact addition: “The existing `applicant_receive_conditions_follow_link_mode` covers VO/rJoinIn and AA/rIn; the new `pending_applicant_joinin_obeys_note_four` covers VP/rJoinIn.” Verification: compare that mapping with the two registered tests and their required reversals.

**Reviewer-owned ledger.**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Frozen issue acceptance; public scope; link-mode documentation; mrp.h contracts; unchanged Applicant guard/table; both note regressions and six focused mutation executions | R545-2, independent delta assessment | f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152 |
| RTL | CLEAN | Complete base-to-head and round-2 diffs; tree, source, mode, index and gitlink audits establish no RTL or production-interface impact | R545-2, independent scope audit | f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152 |
| Robustness | CLEAN | Test lifecycle, exact attribute snapshot and continued Registrar processing; successful mutant builds, required failures, restored passes and byte audits | R545-2, fresh focused execution | f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152 |
| Tests | CLEAN | Both 87-test runners; 19901/19889 measured assertions; 94-case inventory; three reversals per profile; reconciled evidence figures | R545-2, fresh execution and inventory | f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152 |
| Docs | CLEAN | CONTRIBUTING, README, guides, PR body and exact prose delta; all doc/tools checks; prior finding closure; S2 retained | R545-2, fresh checks and reconciliation | f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152 |

**Public evidence, limits and pending manager duties.**

The two files in the [specified public bundle](https://github.com/kebag-logic/milan-fpga/tree/03b25f532812ccc40a75c96cb91ec643af22e108/review-evidence/lwsrpnotes-r1) match their published manifest hashes.
They summarize round-1 unit and full reversal outcomes at `ced667d8`; they do not contain complete raw manager-bank logs.
The supplied manager source static/builder and native-bank passes remain manager evidence, distinct from this reviewer's executions.
The [final public inventory](receipts/public-final-inventory.json) confirms the published PR head and zero issue comments, submitted reviews, and inline comments.

At this exact head, hosted APIs return zero workflow runs, zero check runs and zero statuses: [runs](receipts/hosted-runs.json), [checks](receipts/hosted-checks.json), [statuses](receipts/hosted-status.json).
There is no executed or skipped hosted job to count as a pass. The manager owns hosted and trusted local-workflow acceptance.

This is a documentation delta review, not a renewed whole-library standards certification. The full standard text was not reread; no clause claim changed.
Both relevant profiles and named reversals were executed, but scenarios, sanitizers, the full 94-case campaigns, embedded checks and parent banks were not rerun.
The unit framework was built in packet scratch from public release 1.7.0, resolved commit `feeb85ed48d163f6b7b0011a6d8e6043951541e4`.
Independent commands ran concurrently as waited-for foreground processes. Profile builds used a shared lock and at most 16 compiler workers; each reversal driver used its unchanged two-worker build.
No RTL build or hardware action was needed. Physical calibration NOT RUN. Field skips are not hardware proof.

The manager must obtain the second independent positive review, retain the full completion bar, decide follow-up handling for S1/S2, and publish this packet.
The manager builds and validates the final current-dev candidate at the merge turn, using the supplied source base `a4cbe41de1c80d43f26e0d348cbdb45075273a4f` and live dev `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`.
This source-head verdict does not certify that candidate, a parent dependency update, merge readiness by itself, or hardware deployment.
Merge and post-merge containment remain manager duties.

No source fix, commit, push, GitHub write, merge, shared installation, or other-checkout edit was performed.
The checkout has no `.gitmodules` or submodule gitlinks; there are no submodule pins to restore here.
All disposable trees are under scratch/ and excluded from publication. [Reproduction instructions](REPRODUCE.md), portable scripts and raw receipts are listed in MANIFEST.sha256.

R545-2 FINISHED
