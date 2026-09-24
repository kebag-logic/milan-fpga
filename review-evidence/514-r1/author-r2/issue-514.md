[A10] Separate policy finding from #423's gPTP processor replay analysis.

## Objective and evidence

Decide and document whether linear replay containment certifies historical inclusion or retained content at the current target tip. Keep this separate from #423's new, bounded redundant-merge arm.

At parent dev 88e9276b2a220c716f64a843f7e1eb8f9265e896, an exact linear replay followed by an exact revert returns `contained`, exit 0. The existing `linear-patch-fallback` self-test also permits later edits. R242 reproduced this in fixture 30 and in the real gPTP processor's sibling PR61, whose replayed files were later edited by donor commit 0ac3e2c. This is the existing historical policy, not a new regression introduced by #423.

Evidence: [R242 report](https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5777123829), [immutable scripts and receipts](https://github.com/kebag-logic/milan-fpga/tree/badb350c0892fd5a6c771f24943463c9b1440c24/readiness-evidence/423/design/R242), and [gPTP processor PR61](https://github.com/Mister-M-alt/FPGA-gPTP/pull/61). R241 independently measured the historical/retention distinction in its published report on #423.

## Authority and scope

CONTRIBUTING section 2.1 step 7; REQUIREMENTS REQ-VER-04; AGENTS public task and completion contracts; `scripts/check_merge_containment.py::_linear_patches_contained` and `scripts/merge_containment_selftest_content.py`.

In scope: specify the intended public meaning of containment for linear replay; record treatment of exact and partial reversions, legitimate later extensions, replacements, modes and file kinds; then implement only changes authorized by that recorded choice. Explicitly distinguish historical inclusion, current retention and intentional supersession.

Out of scope: gPTP processor RTL or pin adoption, donor-history rewrites, changing #423's frozen acceptance, or waiving existing audits. The PP (protocol processor) uses the same parent audit tooling; no PP adoption or blanket historical clearance is implied.

## Acceptance and validation

1. Reproduce fixture 30 and the existing `linear-patch-fallback` arm, recording exact heads, verdict text and exits.
2. Publish the policy choice and its impact on existing positives before implementation. A changed expectation requires a documented contract decision, never a test-only weakening.
3. Add executable positive and negative examples for the chosen meaning, including later exact/partial reversion, legitimate extension and intentional supersession. The command must distinguish unsupported or unmeasurable cases without silently certifying them.
4. `python3 scripts/check_merge_containment.py --selftest` and the full applicable local, hosted, candidate and post-merge workflow pass. Two independent reviews cover all five lenses on the final head.
5. Authoritative wording and diagnostics tell a cold reader which claim each verdict makes.

## Readiness and ownership

Backlog: the linear policy choice remains open. Manager A10; executor and two independent reviewers are assigned before activation. Any implementation conflicts with #423 and other edits to the checker or its self-tests. #423 does not depend on this policy change: it preserves the existing linear arm and documents the asymmetry.

Duplicate check covered open and closed parent issues using containment/retention, linear replay, historical replay and `linear-patch-fallback`. #423 owns the redundant-merge case; closed #351 owns Git-version refusal, not retention policy. No existing dedicated linear-policy contract was found.
