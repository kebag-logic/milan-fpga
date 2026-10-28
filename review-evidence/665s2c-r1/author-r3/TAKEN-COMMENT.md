[A685e] TAKEN

Branch: `665-s2c-icache` (local, not pushed), on [A685d]'s REVIEW READY head `e0bb857a` (PR #796, base `dev-soft-core`). New commits go on top; the manager pushes.

Authoritative references: the round-3 assignment (issuecomment-6461736980); R713-2-F1 and R714-2-F1 on PR #796; NFR-SCOUT-01 as amended (`docs/reference/FR_NFR.md:321`, the owner's issuecomment-6434741232 corrected by issuecomment-6434744436); S2's round-6 file classification (`sw/firmware/ctrl/test/ctrl_configs.py`, `e0e1b464`).

Interpreted scope:
- Merge `origin/dev-soft-core` (`1a635a4c`, S2 merged as `6660a1a0`) into `665-s2c-icache` as a merge commit, no rebase. On a conflict S2's rules win and the cache's figures are re-stated against them.
- `docs/reference/FR_NFR.md:6`: the page summary states the amended NFR-SCOUT-01 as `:321` does, and the PR body's Status then matches the page.
- S2's round-6 classification: this PR adds no file to the harness. It changes three of the classified files (`build.py`, `selftest.py`, `split_soc.py`). I check that their reasons in `ctrl_configs.py` still describe what they compile, and edit a reason only if it no longer does. The hosted `firmware-boundary` step must pass when run locally.
- No change to firmware, firmware tests, the mailbox contract, the generator options or the all-fabric CPU.

Validation plan: the harness self-test and its mutants; `sw/builder/test_soc_options.py`; rtl-fast's `firmware-boundary` (`ctrl_boundary.py --require-rv32 --selftest --without verilator`) and `publication-census` (`publication_census.py --check --selftest`) steps run locally; `scripts/check_baremetal_only.py --check`; the docs workflow's check-mode gates; `cd tests && behave`. Also one real harness build at 1x1 with the cache (`--fetch-l1 64x1`), run to the measurement and compared with the PR's figures. Every gate runs in the foreground, unpiped, and must return rc 0.

Blockers: none.
