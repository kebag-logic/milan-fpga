R598-2 independent pass, recorded before reading the prior review reports (R598-1, R599-1) on PR #722.
Exact head c0cba330fd485e52fcb90d5ccc69169edf9f0c2b, tree bd80ea775d965f843609b1282cce9920279c02f0.

Tentative verdict: POSITIVE (no open BLOCKER/MAJOR/MINOR found in the round-2 delta 988ec7f6..c0cba330).

Own items before reading prior findings:
- RES-A (PR body, Round 2 bullet on R598-1-F1): "These are the route gate's own sub-block figures" is true of the wrapper and u_pp only; the gate's scopes lie under milan_datapath/pp_shadow (syn/ooc/pp_resource_gate.py:108, :255-268), so csr -121 comes from the routed hierarchy report and about -227 is the remainder.
- RES-B (PR body, Description "Saving against the plan"): "nearly all of it in u_pp (-344 ...)" while u_pp's -344 exceeds the wrapper's -342.
- S-A (SUGGESTION): MARK_II_AREA_PLAN.md:1027 substitutes M5's measurement alone; live dev ac2c5e77 already carries M2's measured 34 against 200, so the merge-candidate ledger has two lanes below estimate.

Tentative ledger:
| lens | state | artifact |
|---|---|---|
| Conformance | CLEAN | round-2 assignment items 1-4 vs PR body + MARK_II_AREA_PLAN.md:538,1023-1027; arithmetic from published round-1 tables |
| RTL | CLEAN | hdl/common/csr/milan_csr.sv:1063-1072 vs :1159-2662; comment_only_probe.log |
| Robustness | CLEAN | comment_only_probe.log + pp_sensitivity_control.log (no behaviour change); csr_suite.log reset-values/lockstep |
| Tests | CLEAN | csr_suite.log (rc 0, lock1/lock8 5/5, lock_mutants 8/8); anchor counts 7/7 exactly once |
| Docs | CLEAN | MARK_II_AREA_PLAN.md:538,1023-1027; docs gates rc 0 under pinned renderer |
