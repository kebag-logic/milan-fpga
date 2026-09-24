[A246] REVIEW READY

Commit: `20b7bdaa307eba722ec6cc89d2683ba1636a0cb6` (local, not pushed).
Base: `3d2f3e3131c9db5898e1db9dd3e2a35149843109`.
Branch: `514-containment-retention`; clean. Two one-line commits, no bodies or trailers.

Changed: separate optional `--current-retention` result for exact linear replays, reusing #423's unchanged H/T measurements. Default historical verdicts are preserved. Retention is reported independently as `retained` or `UNKNOWN`; unsupported histories, supersession and failed measurements cannot become retention evidence. Updated CONTRIBUTING 2.1 step 7, related containment documentation and diagnostics.

Reproduction before edits: fixture 30 at source `9a9c1e7b26ff2d3439ef5c5ec439cc3a13c9a34a`, target `219aa2256e055e8a577f9899ac6d36bd8bd986e0`, and `linear-patch-fallback` at source `8c7f71d524a70c49ae12d4f9d38bfc6adf782077`, target `206dc8a16726a10e15dfe9946a51777139402daa`, both returned `contained/0`. Fixture 30 heads match the immutable R242 receipt. At this head both defaults still return `contained/0`; the option adds `UNKNOWN/1`, naming `mod.txt` and `linear`.

Validation at the exact head, all exit 0:
- `python3 scripts/check_merge_containment.py --selftest`: 778/778 (678 existing plus 100 added); no locale NOT RUN. The content module is integrated, with no separate entry point.
- `python3 scripts/docs_check.py`; `env GIT_DIR=/dev/null python3 scripts/docs_check.py`: zero findings, both discovery modes.
- `python3 scripts/check_em_dash.py --base 3d2f3e3131c9db5898e1db9dd3e2a35149843109` and `--selftest`.
- `python3 scripts/check_doc_style.py` and `--selftest`; `python3 scripts/gen_toc.py --check`, `--selftest`, `--verify-anchors`; `python3 scripts/check_doc_paths.py`.
- `python3 scripts/check_py_idiom.py` and `--selftest`; `git diff --check` and base-to-head diff check.

Examples cover exact/partial reversion, non-overlapping extension, intentional supersession, mode and file-kind changes, symlink/gitlink identity and reversion, deletion, binary changes, unavailable object measurements and unsupported histories. Every negative policy example rejects a mutant of the new arm. Reverted/superseded/mode/kind/binary examples change from `UNKNOWN/1` to `retained/0` when its T measurement is bypassed; removed shape/H guards are also killed.

Acceptance: AC1-3 and AC5 implementation evidence is recorded; the assigned local portion of AC4 passes. The handoff packet contains HANDOFF.md, proposed PR-BODY.md, reproducible scripts, exact heads/verdicts/exits, example/mutant and gate tables, and the full diff. No author approval is claimed. Independent reviews and the remaining publication, hosted, candidate and merge workflow are pending with the manager. No push, PR mutation, merge, hardware, delegated work or workflow replay was performed.

Open limits: optional retention is restricted to nonempty linear replay ranges; ancestry-only, squash-only and merge-shaped histories are explicitly unsupported. Legitimate overlapping extensions can remain UNKNOWN under the unchanged raw-retention rule.
