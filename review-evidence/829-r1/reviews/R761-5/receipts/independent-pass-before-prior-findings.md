# Independent composition pass (written before reading prior findings)
Candidate 4871df3f6eed1cbc5a399e18372b60a04cb32387 (tree 2b2118df), parents dev 503bc97c and PR head b9628c89.
- `git merge-tree --write-tree 503bc97cd b9628c896` = 2b2118dfc57f2625850838e13ca25c63d7196fd7 = candidate tree: pure merge, no conflict, no extra edits.
- PR base (merge-base) 1f29f189; one predecessor on dev's first-parent line since then: PR #828 (#640), 23 files, all Markdown docs, no code.
- Files changed by both: REQUIREMENTS.md, docs/design/GPTP_PLANE.md. Hunks are disjoint (REQUIREMENTS: #828 at sec. 1/4/7 ownership text, PR at the egress scope note; GPTP_PLANE: #828 lines 6-7, PR at the delay formula and a new H3 section).
- Semantic interaction: #828 makes gPTP ownership fabric "until F6" and keeps "PHC and timestamps in fabric, on both ports". The PR changes only timestamp/egress-correction RTL and docs, which stay in fabric in both regimes; the PR adds no unqualified ownership claim.
- #828's MARK_II_AREA_PLAN rows for KL_gptp_gmii_launch / u_txret / u_gptp_shadow are dated measurements pinned to source commit 40b77bbd (not on dev); the PR's gate on gmii_tready_i does not falsify a dated measurement.
- Requirement IDs: none cited by the PR's added lines; #828 removes no requirement ID. PR's only new cross-page anchor (GPTP_PLANE.md#the-100-mbs-mii-shape) resolves.
- Code readers of the two overlapping docs (test_builder.py, sim_main.cpp, sim_gptp.cpp, check_tap_purity.sh, torture_campaign.py, DOC_MAP.gen.py) only mention them in comments or labels; none parses their contents. Doc gates that do parse them were run (receipts/*.log).
- Builder gate labels 1g/1h are unique in test_builder.py; no doc inventory lists them.
Result: no composition finding.
