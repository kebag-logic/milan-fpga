[A738c] TAKEN
Branch: 845-adopt-pp-92100657, round 2 on top of `b16f0175ac402e124314a40d1ea9573e431684dc`, no rebase, no force
Authoritative references: the latest [A10] comment on this issue; R785-1 (PR #847 issuecomment-6688548787); R786-1 (issuecomment-6688327019); `docs/design/AREA_BUDGET.md`; `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`; Milan v1.2 5.5.3.5.48, Table 5.5, 5.4.2.10.1 Table 5.9
Interpreted scope: F1 records the growth in `docs/design/AREA_BUDGET.md` and on the pin page (route figures, gate state, the decision as pending), with the resource gate run in its own form on `route-1x1` and `ooc-1x1` and its exit code recorded, and no re-baseline. F2 states what a registered settled input does at a link change. F3 makes the group U comment state what row U states. F4 names the measured head in the PR body's Status and Description.
Validation plan: the docs gates, `docs_inventory.py --check` after regenerating through its generator, the resource gate's exit code, `git diff --check`, the privacy check at 0. No full sweep.
Blockers: none. The F1 owner decision is pending and is not mine to make.
