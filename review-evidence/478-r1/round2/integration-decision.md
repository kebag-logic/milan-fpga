[A10] CORRECTED-HEAD VALIDATION PLAN

A169 completed the single PP reference correction at `2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7`, with Git/no-Git failure controls and the pinned target verified. The source is clean and unpushed; the published PR remains draft at d81a3027.

Before full corrected-head validation, integrate current dev `88e9276b2a220c716f64a843f7e1eb8f9265e896` into this isolated lane. #507 changes the Markdown tooling, disjoint from #478's three-file patch. Require the complete issue diff to remain byte-identical and the result to match git merge-tree. This lets one frozen tree receive the corrected-head and current-candidate local bar. Original author evidence remains attributed to 2b200948; none is relabeled.

R221-1 is NEGATIVE on d81 with the known F1; R222's old-head round remains in flight and must finish. No old-head review approves this integration or correction. After the new full40+5 bar passes, push the ready candidate, start the live-dev trusted replica before hosted inspection, and obtain independent corrected-head review and coverage. Any later dev move requires a fresh actual candidate.
