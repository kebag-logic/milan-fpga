[A322] REVIEW READY

Commit: `c6c65e803f9eb270a11dfd65fda5814fb0b0ea55` on `400-403-declaration-truth` (local, unpushed).

Round 4 items 1-3 are implemented: corrected MAAP/RX contract comments, removed the unread posture constant and allocation normalization, replaced the fixture VID assertion with an explicit exception, and aligned both suite banners and READMEs with their default recipes. Product behavior and executable Makefile lines are unchanged.

Byte proof: regenerated all five shipped configurations before and after; all 61 artifact files (612,061 bytes), including header copies and rendered sweep fragments, are byte-identical. Recursive diff and SHA-256 manifest comparison both returned 0.

Validation, all exit 0:

- Complete `python3 sw/builder/test_builder.py` in pinned-SDK and compiler-absent modes, both requiring elaboration; the SDK mode also requires RV32.
- `python3 sw/builder/test_declarations.py`.
- `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test`.
- `make -C tb/verilator/csr` and `make -C tb/verilator/pp_shadow`.
- `python3 scripts/check_baremetal_only.py --check`.
- `python3 -B scripts/docs_check.py` in both CI inventory modes.
- `python3 scripts/check_em_dash.py --base 5c78ce2e9d831e588e759b696ed549804327e4d8`.
- `python3 scripts/check_doc_style.py`, `python3 scripts/gen_toc.py --check`, `python3 scripts/gen_toc.py --verify-anchors`, `python3 scripts/check_doc_paths.py`, `python3 scripts/check_py_idiom.py`, and `python3 scripts/measure_test_evidence.py --check`.
- `git diff --check`, plus the committed delta check.

The requested stale-text search returned no matches. The fixture guard also passed six valid and sixteen invalid executions across normal and optimized Python.

Limits: the existing historical area-calibration report remains unavailable. Compiler-dependent arms are unmeasured only in the absent mode and covered by the separate SDK run. No elaboration arm was skipped for a toolchain reason. No-Git inventory parity is inapplicable by design.

`400-403-a322/HANDOFF.md` records file:line changes, manifests, commands, exits, and logs. `400-403-a322/PR-BODY.md` contains the full current body with the updated role prefix, Round 4, and both closing references. The worktree is clean. Independent re-review remains pending; no push or PR edit was performed.
