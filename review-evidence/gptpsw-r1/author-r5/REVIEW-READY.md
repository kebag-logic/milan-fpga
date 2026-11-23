[A814] REVIEW READY

Commit: `165476c755e4728a044c12ea6bc33ce0a0a9d28f` (local `opt-gptp-sw-1`; not pushed).
PR #966, base `dev-soft-core-optimisation`.

Corrected R883-3-F1/F2 and R884-3-F1 in two documentation files:

- `SPLIT_CONTROL_MEMORY.md:141` and `:142` now identify `image_gptp` as 1,104/2,152 B,
  matching the executable ledger; the limits remain 59.0/64.0 RAMB36.
- `GPTP_SOFTWARE.md:153` states that plain images exclude the firmware gPTP owner,
  while the shared hot-list relearn changes both variants' layout. The adjacent comparison
  records plain ROM growth of 8 B at 1x1/1if and 8x8/2if, from `a6323318` to `631dc544`.

Validation on the committed tree:

- `python3 scripts/docs_check.py`, `python3 scripts/check_doc_style.py`,
  `python3 scripts/check_doc_paths.py`, `python3 scripts/docs_inventory.py --check`: PASS.
- Existing memory rule/ledger and mapper tests via `receipts/run_ledger_tests.py`: PASS,
  150 assertions; all 16 ledger plants and three mapper mutants caught.
- `plat_ledger.py --build-dir <prior-images> --regrade --self-test`: PASS,
  five original `631dc544` images and nine controls. No new image build is claimed.
- `check_em_dash.py --base 8267b895`: PASS, 5 added lines and 339/339 controls.
- The committed diff equals the tested worktree diff; all executable inputs equal `8267b895`.

Evidence: round5 `HANDOFF-r5.md`, `receipts/INDEX.md` and updated `PR-BODY.md`.
Independent Docs re-review is pending. The source-comment residue remains on the manager's
checklist, outside this documentation-only scope. No push or PR edit performed.
