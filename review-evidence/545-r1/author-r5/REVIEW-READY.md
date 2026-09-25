[A317] REVIEW READY

Commit: `4538d7c03dc4f56d7ed4c971603e15bda82050a8` (local, unpushed).

Changed:
- R301-3 F1: `tb/verilator/milan_dp/README.md:590` now states fourteen controls, derives eleven tabulated plus three slew controls, and links the executable inventory.
- R301-3 S1 / R300-3 S2: `scripts/measure_test_evidence.py:597` now names all eight servo defects, including both counting variants.

Validation at this head, all rc 0, foreground and unpiped:
- `python3 scripts/measure_test_evidence.py --check` and `--selftest` (101/101).
- `python3 -B scripts/docs_check.py` in both CI modes: Git and an exact committed archive without Git metadata; both report 0 findings. Only the expected no-Git inventory-parity arm is skipped.
- `python3 scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7` (0 findings, 339/339 arms).
- `python3 scripts/check_doc_style.py`, `python3 scripts/gen_toc.py --check`, `python3 scripts/gen_toc.py --verify-anchors`, `python3 scripts/check_doc_paths.py`, and `python3 scripts/check_py_idiom.py`.
- `git diff --check` and `git diff --check 864b36f5e9450ef64f75ca3f0d68c44330e447d7 HEAD`.

Acceptance: assignment items 1-2 met. Static inventory: 14 datapath controls (12 gmstep, 2 option-off) and 8 servo defects (5 + 3). Only the two assigned files changed; the evidence-reader syntax tree outside the disposition string is identical.

`HANDOFF.md` records file:line changes and the gate table. `PR-BODY.md` preserves the full current body, starts with `[A317]`, adds the docs round and retains `Closes #545`. Both are prepared in the assigned output directory.

Open risks/questions: none for this scoped text change. Independent Docs re-review remains pending. No push or PR edit was performed.
