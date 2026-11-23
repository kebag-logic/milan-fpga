[R897] NEGATIVE - exact head b7b351935f65416c8632c21dd13e08fb2e9c1d9c

Independent verdict and ledger recorded before reading prior review submissions or findings. All five lenses applied; final report will add the completed gate receipts and public-prior-finding reconciliation.

R897-1-F1, MINOR, Conformance / Robustness / Tests / Docs: `.github/workflows/rtl-fast.yml:1731` introduces an unescaped literal matrix-name key in `SKIPPED_MATRICES` on the non-matrix watcher. The documented expression evaluation changes the key to `firmware-boundary shard /`, which cannot match the raw skipped name. `scripts/ci_fail_fast.py:120` rejects the API response; `watch()` returns success with `observer_error=true` after one read, dropping subsequent monitoring. `probe_skipped_matrix.py` and `skipped-matrix.log` reproduce that path without network or hosted execution. Preserve the literal key through runtime expression evaluation and add an evaluated-env skipped-matrix/later-failure control. The required `rtl-fast` verdict remains fail-closed for failed shard results; this finding concerns watcher coverage.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #980 acceptance; template and generated workflow; ctrl_configs.py plan/union; probe.log; F1 | R897-1, applied, no clean coverage | b7b351935f65416c8632c21dd13e08fb2e9c1d9c |
| RTL | CLEAN | Full 11-file diff; unchanged product RTL, firmware C/C++, interfaces and gitlinks; ordered dispatch probe | R897-1 | b7b351935f65416c8632c21dd13e08fb2e9c1d9c |
| Robustness | UNCLEAN | ctrl_boundary.py arguments and refusal paths; capture loader; required verdict shell; skipped-matrix.log; F1 | R897-1, applied, no clean coverage | b7b351935f65416c8632c21dd13e08fb2e9c1d9c |
| Tests | UNCLEAN | test_ctrl_firmware_shards.py; baseline/head dispatch; ci_fail_fast_selftest.py:74; focused probes; F1 | R897-1, applied, no clean coverage | b7b351935f65416c8632c21dd13e08fb2e9c1d9c |
| Docs | UNCLEAN | CI_WORKFLOWS.md fast-feedback and raw-skipped-matrix contract; ctrl/README.md; public author receipts; F1 | R897-1, applied, no clean coverage | b7b351935f65416c8632c21dd13e08fb2e9c1d9c |

R897-1 FINISHED
