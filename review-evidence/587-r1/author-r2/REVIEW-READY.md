[A365] REVIEW READY

Commit: `ce65430125a3c800138d5206dd481ba060cb2328` (one local commit on `587-8x8-baseline-50mhz`; not pushed).

Changed: address R350-1 F1 / R351-F1 with checkout-root normalization and a reproducible digest; address F2 / S1 with historical clock and processor-pin labels; take S2's area-budget pointer update. Three documentation/evidence files changed. No re-measurement.

Validation at this head, all rc 0:
- `python3 syn/ooc/pp_baseline.py --selftest`
- `python3 syn/ooc/pp_baseline_mutants.py` (control passes; all 28 removals killed)
- `python3 scripts/docs_check.py`
- `GIT_DIR=/dev/null python3 scripts/docs_check.py`
- `python3 scripts/check_em_dash.py --base 63fe4fb0`
- `python3 scripts/check_doc_style.py`
- `python3 scripts/gen_toc.py --check`
- `python3 scripts/gen_toc.py --verify-anchors`
- `python3 scripts/check_doc_paths.py`
- `git diff --check` and `git diff --check 63fe4fb0 HEAD`

Unchanged public reviewer scripts from `587-review-evidence` at `fd86bc2c2938e44bc46705999a665ed21e76e4a2` also pass: normalized digest on both fresh exports, page figures, ranking, history and input hashes. Both fresh exports yield `38f6c8dd93ba018d009875412b82dd9f34e2149244eda20ab1e2f81d3f85f575` with literal `$REPO`. Historical numeric rows remain intact. Additional source-inventory, bare-metal and entity-shape checks pass.

Acceptance evidence: retained default 50 MHz result is 68,047 LUTs, delta -89 from 100 MHz, WNS -1.708 ns. All original figures and measurement input/report hashes are unchanged. The #229 reference update remains manager-owned after merge.

Handoff and full replacement body: `587-a365/HANDOFF.md` and `587-a365/PR-BODY.md` in the assigned output directory. Worktree and initialized submodules are clean. Manager publication and independent round-2 review remain pending; this comment is evidence, not a review verdict.
