https://github.com/kebag-logic/milan-fpga/issues/423
Containment cannot certify an exact replay containing a redundant merge commit
[A0] Replayed merge topology produces an unresolved containment verdict

Objective: decide and implement a narrowly bounded proof for replayed merge topology in `scripts/check_merge_containment.py`, preserving fail-closed behavior for actual stranded work and differing postimages. No product RTL or protocol behavior changes.

Observed with the trusted script at root commit 9888273763da1688644e12b40a07596ee295d4b6 against FPGA-gPTP main f0f1c055ee5226f08e656c27cb1bf4c355be11ae: the recent-PR sweep reports PR62 STRANDED with three commits outside main. Manual proof finds no missing implementation patch:

- Original 3db86812096830fada2f5f276fa5f4d9f37d1d14 and main replay 5602e70bb4cf70c2e0e39e846e26925e27659e32 have byte-identical raw patches and all three changed-file postimages. Patch SHA-256 fa20a2516a4d866a859506c5396779fb98bbafe943e4de2651e9ec252bca996f.
- Its predecessor 9790ac736e6d10301ad814ffdf73dbe37b59768b and main replay 20927af74752620b2ad0f973e8be3203994b5547 likewise have byte-identical patches and all five changed-file postimages. Patch SHA-256 d3d164b309e376ea06a3734e8452dd5668c4721d0462dc0656af05d6b3c155b3.
- The intervening old merge f27b455 has the same tree as its incoming parent 9790ac7 and adds no tree delta. Main contains the replays through merges 377b8c428b226a796adde099fe07152151fd6c5d and 676d2f6be46b2775b8a008800d394c9855a5efc3.

The generic audit remains exit 1. This issue records the limitation; it does not waive a gate or declare arbitrary merge commits equivalent.

Authority and entry points: CONTRIBUTING.md section 2.1 step 7; `scripts/check_merge_containment.py` merge and patch/postimage paths; existing selftests. Evidence repository: https://github.com/Mister-M-alt/FPGA-gPTP/pull/62.

Proposed acceptance for readiness review:
1. Reconstruct the public history and a minimal offline fixture reproducing the same failure.
2. Define the exact safe equivalence criterion before implementation. A merge containing additional resolution work must remain uncontained unless that work is independently proved present.
3. A positive replay fixture passes; missing linear work, missing merge-resolution work, whitespace-different postimages and later reversions remain refused or explicitly unresolved under the existing policy.
4. Existing selftests and all applicable root gates pass; two completed independent reviews cover all five lenses on the final head.

Status: Ready under the [recorded bounded G1 + H + T decision](https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5777210218). Actual gPTP processor PR62 and overlapping later edits remain explicitly unresolved; historical replay alone does not satisfy the new arm. Existing linear-arm retention policy is tracked separately in #514. Executor A171 (Codex), independent internal reviewer R243 (Codex), external reviewer R244 (Opus), manager A10. The sole author slot must be free before activation; no production source has been edited for this finding.

