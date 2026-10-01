[A478] TAKEN

Round 5 for PR #628 (bench lane B5, #117 acceptance box 4, the audio continuity row), under the [A10] assignment (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5929901339). Docs only; no bench access.

Branch: `b5-bench-1001` at `e216dfe4f0cab7b0c7352d7973acb4d33c157f70`, local only.

Authoritative references: R424-4 (https://github.com/kebag-logic/milan-fpga/pull/628#issuecomment-5929893902) and R425-4 (https://github.com/kebag-logic/milan-fpga/pull/628#issuecomment-5929883759); the assignment's rulings 1 to 4; the evidence archive, branch `b5-review-evidence` at `9006c78e354d5a2f244fd606c55790a825304bd3`, and its `MANIFEST.json`; `.github/PULL_REQUEST_TEMPLATE.md` and CONTRIBUTING section 2.2.

Interpreted scope: (1) remove the byte sizes of the every-channel captures from the page, and any other size on the page from which the capture's channel count follows by division; keep their SHA-256; only those cells change. (2) At `:511-513` and in the PR body's Round 4 item 1, name only the masked input the reproduction commands read, `summary.json`. (3) Re-pin the archive paragraph to `9006c78e`, re-run steps 1 to 3 from that commit alone, and confirm both receipts reproduce byte for byte. (4) Rewrite the PR body in the repository's pull-request template, keeping the [A472] first line and "Refs #117", with no closing keyword. (5) List rounds 4 and 5 in the page header. Every measurement table otherwise byte-identical.

Validation plan: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9`, `check_doc_paths.py` in the pinned Markdown environment; `scripts/ci_scope.py --selftest`; `scripts/check_baremetal_only.py --check`; `scripts/check_feature_status.py --self-test`; `git diff --check`; a table diff against `e216dfe4`; a reproduction of steps 1 to 3 from `9006c78e` alone; a divisibility check of every byte size left on the page; a public-text scan of the diff and the output.

Blockers: none.

