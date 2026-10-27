[A674e] TAKEN - round 5
Branch: `396-release-gate-plan`, round-4 head `85da3e4595871c1573c28b4d040b9e98463a41c9` on dev `e76a755a`. Round-5 commits go on top; nothing is rewritten.
Authoritative references: round-5 assignment issuecomment-6424374359 (items 1 to 5); R699-4 (PR #786 issuecomment-6424363636) G1 to G4 and R1, with its published probes; REQUIREMENTS.md REQ-VER-06; TESTING.md 6d; `AUDIO_COUNTER_LIMITS`.
Interpreted scope:
1. G3, by an invariant. On each channel, the signed sum of the DUT slips a reading reports must equal the net shift the capture's bytes decode, at every point where 64 clean samples fix the track. A reading that breaks this is rejected for a balanced one. Where none balances, the event is reported as an unclassified corruption at its sample, never as a slip that did not happen. The near-boundary cases that were exact at `4d69e192` are exact again. `r4_net_sweep.py` reports 0 unbalanced and `r4_regress_sweep.py` 0 regressions, both unmodified.
2. G1 and G2. I take the general reading where item 1 gives it. Otherwise each remaining exception is stated exactly (shape, distance, arm kind and mask class) in TESTING 6d, REQ-VER-06 and `counter_limits`. The "never hides", "either order" and "beside any one-word event" claims are narrowed to match, and each exception is pinned by a self-test arm. A void stays a release block.
3. The reviewer's composition sweeps become a self-test sweep: arm × corruption at d = -4..+4; slip before an excursion within 64 samples; both capture lengths. It passes only when every case is exact or a pinned exception.
4. G4: self-test arms that kill W03 and W07.
5. R1's wording, as written.
Scope: the grader, its self-test, and the documents named. I will STOP if item 1 changes a verdict anywhere outside the swept shapes.
Validation plan:
- `torture_campaign.py --self-test`.
- `torture_release_mutants.py`, with planted defects for each new rule.
- `cd tests && behave`.
- Under the pinned renderer: docs_check.py, gen_toc.py --check and --verify-anchors, check_em_dash.py --base origin/dev, check_doc_style.py and check_doc_paths.py.
- check_py_idiom.py and git diff --check.

All must return 0. I will rerun R699-4's probes unmodified: net sweep, regress sweep, arm-corruption sweep, `r4_probe.py`, `r4_cf_full.py` and `r4_reviewer_mutants.py`. Before and after, I will compare verdicts outside the swept shapes, using R699-3's and R700-3's earlier probes.
Blockers: none.
