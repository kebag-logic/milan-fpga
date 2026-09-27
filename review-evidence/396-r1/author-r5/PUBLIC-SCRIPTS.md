# Public review script results

Head: `07f72ad640f99c43bc1354642ad4d7ed8ba410cc`.
All 35 public script files ran unchanged, including duplicate prior-round copies.
Their final bytes match the public blobs at `e3df1b3364391368ed05d84b44b653e46d51a62e`.
`commands.jsonl` records exact commands and heads; `review-script-provenance.json`
records hashes and public paths. Mutant nonzero exits are expected controls.
Invalid/unapplied anchors are never counted as kills.

| Script | rc | Result | Log |
|---|---|---|---|
| `R346-1-scripts-plan_omission_probe` | 0 | 240 omissions; zero accepted | [R346-1-scripts-plan_omission_probe.log](R346-1-scripts-plan_omission_probe.log) |
| `R346-1-scripts-planner_mutants` | 0 | 42 killed; 1 survived; 1 invalid/unapplied | [R346-1-scripts-planner_mutants.log](R346-1-scripts-planner_mutants.log) |
| `R346-2-scripts-eligibility_probe` | 0 | Contract probe completed; see log | [R346-2-scripts-eligibility_probe.log](R346-2-scripts-eligibility_probe.log) |
| `R346-2-scripts-plan_omission_probe` | 0 | 240 omissions; zero accepted | [R346-2-scripts-plan_omission_probe.log](R346-2-scripts-plan_omission_probe.log) |
| `R346-2-scripts-planner_mutants` | 0 | 42 killed; 1 survived; 1 invalid/unapplied | [R346-2-scripts-planner_mutants.log](R346-2-scripts-planner_mutants.log) |
| `R346-2-scripts-planner_mutants_r2` | 0 | 48 killed; 0 survived; 2 invalid/unapplied | [R346-2-scripts-planner_mutants_r2.log](R346-2-scripts-planner_mutants_r2.log) |
| `R346-3-scripts-adp_hold_probe` | 0 | Contract probe completed; see log | [R346-3-scripts-adp_hold_probe.log](R346-3-scripts-adp_hold_probe.log) |
| `R346-3-scripts-planner_mutants_r3` | 0 | 28 killed; 3 survived; 3 invalid/unapplied | [R346-3-scripts-planner_mutants_r3.log](R346-3-scripts-planner_mutants_r3.log) |
| `R346-3-scripts-r2_unchanged-eligibility_probe` | 0 | Contract probe completed; see log | [R346-3-scripts-r2_unchanged-eligibility_probe.log](R346-3-scripts-r2_unchanged-eligibility_probe.log) |
| `R346-3-scripts-r2_unchanged-plan_omission_probe` | 0 | 240 omissions; zero accepted | [R346-3-scripts-r2_unchanged-plan_omission_probe.log](R346-3-scripts-r2_unchanged-plan_omission_probe.log) |
| `R346-3-scripts-r2_unchanged-planner_mutants` | 0 | 42 killed; 1 survived; 1 invalid/unapplied | [R346-3-scripts-r2_unchanged-planner_mutants.log](R346-3-scripts-r2_unchanged-planner_mutants.log) |
| `R346-3-scripts-r2_unchanged-planner_mutants_r2` | 0 | 48 killed; 0 survived; 2 invalid/unapplied | [R346-3-scripts-r2_unchanged-planner_mutants_r2.log](R346-3-scripts-r2_unchanged-planner_mutants_r2.log) |
| `R347-1-scripts-audit_probe` | 0 | All six planted defects rejected | [R347-1-scripts-audit_probe.log](R347-1-scripts-audit_probe.log) |
| `R347-1-scripts-mutants` | 0 | 21 killed; 0 survived; 0 invalid/unapplied | [R347-1-scripts-mutants.log](R347-1-scripts-mutants.log) |
| `R347-2-scripts-audit_probe` | 0 | All six planted defects rejected | [R347-2-scripts-audit_probe.log](R347-2-scripts-audit_probe.log) |
| `R347-2-scripts-kill_attribution` | 0 | Named failures reported; source restored | [R347-2-scripts-kill_attribution.log](R347-2-scripts-kill_attribution.log) |
| `R347-2-scripts-mutants` | 0 | 21 killed; 0 survived; 0 invalid/unapplied | [R347-2-scripts-mutants.log](R347-2-scripts-mutants.log) |
| `R347-2-scripts-mutants_r2` | 0 | 22 killed; 0 survived; 0 invalid/unapplied | [R347-2-scripts-mutants_r2.log](R347-2-scripts-mutants_r2.log) |
| `R347-2-scripts-probe_r2` | 0 | Contract probe completed; see log | [R347-2-scripts-probe_r2.log](R347-2-scripts-probe_r2.log) |
| `R347-2-scripts-r346_attribution` | 0 | Named failures reported; source restored | [R347-2-scripts-r346_attribution.log](R347-2-scripts-r346_attribution.log) |
| `R347-2-scripts-run_gates` | 0 | Every nested gate rc 0 | [R347-2-scripts-run_gates.log](R347-2-scripts-run_gates.log) |
| `R347-3-scripts-clone_integrity` | 0 | Clean candidate; matching blobs and gitlinks | [R347-3-scripts-clone_integrity.log](R347-3-scripts-clone_integrity.log) |
| `R347-3-scripts-mutants_r3` | 0 | 23 killed; 0 survived; 3 invalid/unapplied | [R347-3-scripts-mutants_r3.log](R347-3-scripts-mutants_r3.log) |
| `R347-3-scripts-probe_r3` | 0 | Contract probe completed; see log | [R347-3-scripts-probe_r3.log](R347-3-scripts-probe_r3.log) |
| `R347-3-scripts-round2-audit_probe` | 0 | All six planted defects rejected | [R347-3-scripts-round2-audit_probe.log](R347-3-scripts-round2-audit_probe.log) |
| `R347-3-scripts-round2-kill_attribution` | 0 | Named failures reported; source restored | [R347-3-scripts-round2-kill_attribution.log](R347-3-scripts-round2-kill_attribution.log) |
| `R347-3-scripts-round2-mutants` | 0 | 21 killed; 0 survived; 0 invalid/unapplied | [R347-3-scripts-round2-mutants.log](R347-3-scripts-round2-mutants.log) |
| `R347-3-scripts-round2-mutants_r2` | 0 | 22 killed; 0 survived; 0 invalid/unapplied | [R347-3-scripts-round2-mutants_r2.log](R347-3-scripts-round2-mutants_r2.log) |
| `R347-3-scripts-round2-probe_r2` | 0 | Contract probe completed; see log | [R347-3-scripts-round2-probe_r2.log](R347-3-scripts-round2-probe_r2.log) |
| `R347-3-scripts-round2-r346_attribution` | 0 | Named failures reported; source restored | [R347-3-scripts-round2-r346_attribution.log](R347-3-scripts-round2-r346_attribution.log) |
| `R347-3-scripts-round2-run_gates` | 0 | Every nested gate rc 0 | [R347-3-scripts-round2-run_gates.log](R347-3-scripts-round2-run_gates.log) |
| `R347-3-scripts-tu_anchor_model` | 0 | Phase sweep completed | [R347-3-scripts-tu_anchor_model.log](R347-3-scripts-tu_anchor_model.log) |
| `R347-4-scripts-mutants_r4` | 0 | 16 killed; 0 survived; 0 invalid/unapplied | [R347-4-scripts-mutants_r4.log](R347-4-scripts-mutants_r4.log) |
| `R347-4-scripts-tu_anchor_model` | 0 | Phase sweep completed | [R347-4-scripts-tu_anchor_model.log](R347-4-scripts-tu_anchor_model.log) |
| `R347-4-scripts-tu_oracle_probe` | 0 | Part A PASS; Part B 6/6 PASS | [R347-4-scripts-tu_oracle_probe.log](R347-4-scripts-tu_oracle_probe.log) |
