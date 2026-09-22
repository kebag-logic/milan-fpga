[A169] Corrected-head command receipts.

Head: `2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7`
Tree: `568c5db2804f789015708358ad2a2d9c842c7cff`
Parent: `d81a302760b84f32d2aa019643f57682bb6e052c`
Parent tree: `4903a00f30752bc86a99e9bf112ff5ad01827c5d`

Every numbered command JSON records argv, shell rendering, working directory, UTC start/end, exact exit, expected exit and raw stdout/stderr. Its adjacent log contains stdout followed by stderr. The head/tree fields identify the source commit used to construct the copies, not a claim that a negative-control overlay is the committed tree. `30-boundary-proof.json` makes that distinction explicit.

`00-start-and-edit.json` records clean starting identity, the pre-edit TAKEN URL and the single byte-string replacement. `01-commit.json` records the pre-commit check, stage, one-line commit and clean committed identity. Those pre-commit results are not corrected-commit gate evidence. Corrected-commit gates are the separately numbered runs below.

Setup: a local transport clone at depth two, detached at the corrected full head, and a tar archive produced by `git archive` at the same full head. No submodule initialization command was run. The four Git submodule statuses are all prefixed `-`; in both copies the gitlink directories are absent or empty. No-Git mode has no .git path, and `git rev-parse --is-inside-work-tree` exits 128. Both population receipts verify 850 file blobs/executable modes against the committed tree, before execution and after restoring each negative control.

The old-link negative controls replace only the URL in a scratch copy and have file content tree `4903a00f30752bc86a99e9bf112ff5ad01827c5d`; their Git HEAD/index (where present) still identify the corrected commit. Both exit 1 with exactly the original broken link and no other finding. They are not corrected-head passes.

The no-Git docs check records its expected inventory-parity skip. Its 22 scrub and four routing controls pass; Git mode runs 23 scrub and four routing controls. No skipped arm is credited as executed.

The em-dash base is the immediate pre-correction head. This proves the bounded correction, not a complete branch/current-dev gate. The validator command invokes only the existing gate 36a rate-array/YAML comparison and its five drift controls; it does not run the complete builder suite or regenerate shipping images.

The GitHub target API result and decoded-blob verification are retained in `26-*`. Public review snapshots are in `27-*`, `28-*`, `29-*` and `31-*`; these are downloaded public comments/reviews, not private agent material.

The management-only reproduction script is `../verify.py`. Its four executed stages were `prepare`, `docs`, `target` and `focused`, each launched with `rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/478-link-author/verify.py <stage>` and each completed with exit 0. For a fresh reproduction, use the same script and head.json in a new packet directory with an empty receipts directory and no scratch directory. The retained scratch trees remain unchanged after validation. These reproduction artifacts add no production test.

| Receipt | Exit | Exact command |
|---|---:|---|
| [02-clone](02-clone.json) | 0 | `rtk proxy git clone --no-local --no-checkout --depth 2 --single-branch --branch 478-audio-unit-rate-bound $CANDIDATE $WORKSPACE_HOME/milan-fpga-management/2026-09-22/478-link-author/scratch/git` |
| [03-checkout](03-checkout.json) | 0 | `rtk proxy git checkout --detach 2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7` |
| [04-git-head-tree](04-git-head-tree.json) | 0 | `rtk proxy git rev-parse HEAD 'HEAD^{tree}'` |
| [05-git-clean](05-git-clean.json) | 0 | `rtk proxy git status --porcelain=v1 --untracked-files=all` |
| [06-git-submodules](06-git-submodules.json) | 0 | `rtk proxy git submodule status` |
| [07-archive](07-archive.json) | 0 | `rtk proxy git archive --format=tar --output=$WORKSPACE_HOME/milan-fpga-management/2026-09-22/478-link-author/scratch/corrected.tar 2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7` |
| [08-no-git-proof](08-no-git-proof.json) | 128 | `rtk proxy git rev-parse --is-inside-work-tree` |
| [09-git-before-tree](09-git-before-tree.json) | 0 | `rtk proxy git ls-tree -r 2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7` |
| [10-no-git-before-tree](10-no-git-before-tree.json) | 0 | `rtk proxy git ls-tree -r 2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7` |
| [11-git-docs-corrected](11-git-docs-corrected.json) | 0 | `rtk proxy python3 scripts/docs_check.py` |
| [11-no-git-docs-corrected](11-no-git-docs-corrected.json) | 0 | `rtk proxy python3 scripts/docs_check.py` |
| [12-git-docs-old-link](12-git-docs-old-link.json) | 1 | `rtk proxy python3 scripts/docs_check.py` |
| [12-no-git-docs-old-link](12-no-git-docs-old-link.json) | 1 | `rtk proxy python3 scripts/docs_check.py` |
| [13-git-after-restore-tree](13-git-after-restore-tree.json) | 0 | `rtk proxy git ls-tree -r 2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7` |
| [13-no-git-after-restore-tree](13-no-git-after-restore-tree.json) | 0 | `rtk proxy git ls-tree -r 2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7` |
| [14-doc-paths](14-doc-paths.json) | 0 | `rtk proxy python3 scripts/check_doc_paths.py` |
| [15-doc-style](15-doc-style.json) | 0 | `rtk proxy python3 scripts/check_doc_style.py` |
| [16-toc-check](16-toc-check.json) | 0 | `rtk proxy python3 scripts/gen_toc.py --check` |
| [17-toc-anchors](17-toc-anchors.json) | 0 | `rtk proxy python3 scripts/gen_toc.py --verify-anchors` |
| [18-em-dash](18-em-dash.json) | 0 | `rtk proxy python3 scripts/check_em_dash.py --base d81a302760b84f32d2aa019643f57682bb6e052c` |
| [19-issue478-validator-selftest](19-issue478-validator-selftest.json) | 0 | `rtk proxy python3 -B -c 'import sys; sys.path.insert(0, '"'"'sw/builder'"'"'); import test_builder; test_builder.test_pp_shadow_audio_unit_rates_match_config()'` |
| [20-diff-check](20-diff-check.json) | 0 | `rtk proxy git diff --check d81a302760b84f32d2aa019643f57682bb6e052c 2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7` |
| [21-final-copy-clean](21-final-copy-clean.json) | 0 | `rtk proxy git status --porcelain=v1 --untracked-files=all` |
| [22-final-lane-clean](22-final-lane-clean.json) | 0 | `rtk proxy git status --porcelain=v1 --untracked-files=all` |
| [23-final-lane-head-tree](23-final-lane-head-tree.json) | 0 | `rtk proxy git rev-parse HEAD 'HEAD^{tree}'` |
| [24-changed-paths](24-changed-paths.json) | 0 | `rtk proxy git diff --name-only d81a302760b84f32d2aa019643f57682bb6e052c 2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7` |
| [25-final-commit](25-final-commit.json) | 0 | `rtk proxy git show -s --format=fuller 2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7` |
| [26-pinned-target](26-pinned-target.json) | 0 | `rtk proxy gh api 'repos/Mister-M-alt/protocol-processor-control-plane-avb-milan/contents/docs/architecture/07_memory_maps.md?ref=424c688fa2205b934a7689a58f2aa766420f2326'` |
| [27-public-comments](27-public-comments.json) | 0 | `rtk proxy gh api repos/kebag-logic/milan-fpga/issues/512/comments --paginate --slurp` |
| [28-public-reviews](28-public-reviews.json) | 0 | `rtk proxy gh api repos/kebag-logic/milan-fpga/pulls/512/reviews --paginate --slurp` |
| [29-public-inline-comments](29-public-inline-comments.json) | 0 | `rtk proxy gh api repos/kebag-logic/milan-fpga/pulls/512/comments --paginate --slurp` |
| [30-corrected-doc](30-corrected-doc.json) | 0 | `rtk proxy git show 2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7:docs/ENDSTATION_BUILDER.md` |
| [30-corrected-tree](30-corrected-tree.json) | 0 | `rtk proxy git ls-tree -r 2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7` |
| [30-parent-doc](30-parent-doc.json) | 0 | `rtk proxy git show d81a302760b84f32d2aa019643f57682bb6e052c:docs/ENDSTATION_BUILDER.md` |
| [30-parent-tree](30-parent-tree.json) | 0 | `rtk proxy git ls-tree -r d81a302760b84f32d2aa019643f57682bb6e052c` |
| [30-parent](30-parent.json) | 0 | `rtk proxy git rev-parse '2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7^'` |
| [31-latest-public-comments](31-latest-public-comments.json) | 0 | `rtk proxy gh api repos/kebag-logic/milan-fpga/issues/512/comments --paginate --slurp` |
| [32-review-ready-publication](32-review-ready-publication.json) | 0 | `rtk proxy gh pr comment 512 --repo kebag-logic/milan-fpga --body-file $WORKSPACE_HOME/milan-fpga-management/2026-09-22/478-link-author/REVIEW-READY.md` |
| [33-stop-branch](33-stop-branch.json) | 0 | `rtk proxy git branch --show-current` |
| [33-stop-clean](33-stop-clean.json) | 0 | `rtk proxy git status --porcelain=v1 --untracked-files=all` |
| [33-stop-head-tree](33-stop-head-tree.json) | 0 | `rtk proxy git rev-parse HEAD 'HEAD^{tree}'` |
