[A314] REVIEW READY

Commit: `b02af0480d3a3061df24683d522799d1759f7c33` (local, unpublished; branch `559-capture-copy`).

Changed: pin the capture measurement step's exact name, position 28, keys and canonical command in `scripts/ci_events.py`; update the 50-step inventory and shifted controls; document it in `docs/testing/CI_WORKFLOWS.md`. Only those two files changed.

Validation: all requested gates returned 0 at this head. The workflow contract passes 1,655 items and its self-test passes 2,197 arms. Commands:

```sh
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/act_ci.py --selftest
python3 scripts/check_nvm_capture.py
python3 -B scripts/docs_check.py
GIT_DIR=/dev/null python3 -B scripts/docs_check.py
python3 scripts/check_em_dash.py --base a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4
python3 scripts/check_doc_style.py
python3 scripts/check_doc_style.py --selftest
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_doc_paths.py
python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest
python3 scripts/check_sh_idiom.py
python3 scripts/check_sh_idiom.py --selftest
git diff --check
git diff --check 31808e6525a83955bc4322ac8ac6871f9e6b10e6 HEAD
```

All earlier mutation controls remain. Four added controls reject removal, reordering, renaming and `if: false`. The new step also passes the existing replacement, swallowed-failure, appended-command, `continue-on-error` and missing-record controls. All nine refusals name the expected defect. The capture gate's four explicit `--mutation` variants each return the expected rc 1.

Both documentation modes report zero findings. The no-Git mode uses the filesystem inventory and reports its expected inventory-parity skip. The initial em-dash run refused a missing dependency; installing the locked Markdown requirements outside the output directory resolved it, and the final run passed.

Acceptance: round 3 scope met. Round 2 measurements, capture gate logic, workflow and other documentation are unchanged. HANDOFF.md includes file/line references, mutation diagnostics and the gate table; PR-BODY.md is the full updated body in the assigned output directory.

Open risks/questions: none for this correction. Independent re-review and exact-head hosted acceptance remain.
