[A615] REVIEW READY — PR #738, round 4

Commit: `e355f789b4f59b86083809299134557ca47bbcfb` on `737-ci-image` (local only; no push).

Implemented the assignment and amendments 6170435035, 6170543242 and 6170640746. The reached-construct census was committed before implementation. Commands now require positive executable/subcommand/argument forms; the shell, Make and Python readers resolve the censused forms and refuse unsupported variants by name. Controls cover the R638-3 and R639-3 findings in both generation and comparison modes, including default temporary directories and a checkout below `/tmp`.

Selection corrections cover literal default goals, unique pattern stems, alternate Makefiles, workflow directories, scoped subshells/functions, pinned inline programs and literal Make shell expressions. Literal dollar or marker text cannot satisfy a runtime argument allowance. Existing workflows derive exactly the same 45 tool/pin/installation-provenance records as `e6b86814`; 328 inputs and 269 located residue entries are now bound.

Validation: all 13 source gates, three Markdown checks and ten rebuilt-image checks passed, rc 0. The source gates were repeated after generating the lock. Principal reproduction commands (environment prerequisites are in the image guide):

```sh
python3 scripts/ci_tool_inventory.py --check
python3 scripts/ci_tool_inventory_selftest.py
python3 scripts/ci_inventory_patterns_selftest.py
python3 ci/image/build_selftest.py
python3 ci/image/integrity_selftest.py
python3 ci/image/privacy_selftest.py
python3 ci/image/privacy_patch_selftest.py
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/check_doc_paths.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base e6b86814
python3 scripts/check_em_dash.py --selftest
git diff --check
python3 ci/image/build.py --work "$IMAGE_WORK/first" --no-cache --defer-lock
python3 ci/image/build.py --work "$IMAGE_WORK/first" --check-lock --verify-archive "$IMAGE_WORK/first/image.tar"
python3 ci/image/build.py --work "$IMAGE_WORK/second" --no-cache --defer-lock
python3 ci/image/build.py --work "$IMAGE_WORK/second" --check-lock --verify-archive "$IMAGE_WORK/second/image.tar"
```

Both final-source cold builds returned zero and matched in manifest, configuration and all 14 layers. Only the pinned base was cached. Docker build times: 400,411 ms and 436,056 ms. Size: 3,931,071,698 bytes. Offline smoke: rc 0 in 37.021 seconds; all tool version and functional checks passed. Both exports passed archive authentication and privacy provenance checks with 526 public-source allowances.

Manifest: `sha256:86d7aa16e7d2464baf8e0d246434982838c8174de8c8fa610608cce5b23b5e6c`.
Configuration: `sha256:62b56e1ab52dce1a1914e8469429c014e69a465e74e0bdb9a7d8bf4a626b2776`.
Recipe: `e689418be8fe7e7857c291d940d96d1edfedf5958879431bfe3fcece5a3728c7`.
The generated lock changes only the overall recipe digest; the image remains byte-identical to the accepted round-three image.

`HANDOFF.md` and `PR-BODY.md` are updated in the handoff packet. Final receipts: `round4-final-gates.json`, `round4-rebuilt-image.json`, `round4-lock.json`, `round4-second-archive.json`, `round4-cold-comparison.json` and `round4-build-artifacts.json`. Large exports and logs remain in scratch and are represented by SHA-256 and size. Intermediate failures and preliminary builds are retained and explicitly superseded.

Acceptance: the round-four implementation and local validation are ready for independent re-review. The tree is clean; origin remains at `e6b86814`. No workflow, firmware behavior, linked image, existing product-test assertion or gitlink changed. The previously accepted grouped campaign remains historical evidence. Declared runtime assembly still requires manual review; hosted/act adoption, publication, independent verdicts and merge remain outstanding. No push or PR modification occurred.
