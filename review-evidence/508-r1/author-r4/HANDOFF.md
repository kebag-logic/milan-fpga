[A299]

PR #560, issue #508, amended round 4 is implemented and locally validated.
Head: `9d66cfe0dc87ffe4a5f45691d5c86b041b050b38`.
Parent: `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2`.
Branch: `508-pp-pin-adopt`. The commit is local and unpushed.
Commit subject: `Fix pinned processor links and GSI campaign counts`.
The commit has one line, no body and no trailers. The working tree is clean.

Authority: [amended round-4 assignment](https://github.com/kebag-logic/milan-fpga/issues/508#issuecomment-5826348330), replacing the earlier round-4 scope; [R306-2](https://github.com/kebag-logic/milan-fpga/pull/560#issuecomment-5826344643) and [R307-2](https://github.com/kebag-logic/milan-fpga/pull/560#issuecomment-5826345263), findings F1 and F2.

Exactly five files changed, with six lines replaced:

- `tb/verilator/milan_dp/README.md:488`: F06.13 and F05.5 link to GitHub blobs at `990f96526bb89356c963a260ebbdcf2a77e6623a`, retaining `#fig-06-lineage` and `#fig-05-settled`. Both figure labels and fragment targets were checked against the pinned source. The interrupted session's uncommitted edit was replaced with this amended form.
- `CHANGELOG.md:57`: eight failing arms.
- `tb/verilator/milan_dp/Makefile:451-452`: eight additional elaborations and nine runs.
- `scripts/measure_test_evidence.py:620`: eight seam defects.
- `docs/testing/TESTING.md:267`: eight field and notification mutants.

`round4-final/scope-proof.json` confirms that each committed file equals its parent plus only the assigned replacements. It also checks eight mutation entries, the unchanged processor pin, the parent, branch, commit format and clean working tree. No behavior, recipe, gate, budget or submodule content changed.

Every command below returned rc 0 at the head above. Commands ran in the foreground without shell pipelines, with a 1200-second limit per gate. The locked Markdown dependencies were installed under this output directory and selected through `PYTHONPATH`; bytecode writes were disabled.

| Command | Result |
|---|---|
| `python3 scripts/gen_toc.py --verify-anchors` | 168 existing cross-page fragments reproduced |
| `python3 scripts/gen_toc.py --check` | OK; 107 contents lists, 17 pages below threshold |
| `python3 scripts/docs_check.py` | 0 findings; 165 Markdown files, 861 scrubbed text files; Git inventory |
| `env GIT_DIR=/nonexistent-508-a299-git python3 scripts/docs_check.py` | 0 findings; 165 Markdown files, 871 scrubbed text files; filesystem inventory |
| `python3 scripts/check_doc_paths.py` | 842 cited paths resolve |
| `python3 scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2` | 0 findings; 339/339 controls |
| `python3 scripts/measure_test_evidence.py --check` | PASS; existing budgets unchanged |
| `python3 scripts/measure_test_evidence.py --selftest` | 101 PASS, 0 FAIL |
| `python3 scripts/check_py_idiom.py` | PASS; 239 first-party modules |
| `git diff --check` | Clean |
| `git diff --check 224ec0e9a9fa129924bf8f0433cf70b4140f7bd2 9d66cfe0dc87ffe4a5f45691d5c86b041b050b38` | Committed delta clean |

The archive proof uses `git archive` of this exact head. Every gitlink directory is empty or absent: `external`, `gptp-processor`, `protocol-processor`, and `third_party/verilog-axis`. There is no `.git` in the extracted tree. No additional checkout was created.

Reproduction, with `<evidence>` and `<archive>` denoting output directories:

```sh
git archive --format=tar --output=<evidence>/head.tar 9d66cfe0dc87ffe4a5f45691d5c86b041b050b38
mkdir <archive>
tar -xf <evidence>/head.tar -C <archive>
cd <archive>
python3 scripts/docs_check.py
env GIT_DIR=<lane-git-dir> GIT_WORK_TREE=<archive> python3 scripts/docs_check.py
```

`<lane-git-dir>` is the lane's `git rev-parse --absolute-git-dir` result. The second archive invocation uses the clean lane index for inventory only; it reads document contents from the archive. Both archive invocations returned rc 0 with **0 findings, 165 Markdown files and 861 scrubbed text files**. The Git invocation passed 23/23 scrub controls and 4/4 routing controls. Both no-Git invocations passed 22/22 scrub controls and 4/4 routing controls; inventory parity is explicitly skipped because Git metadata is unavailable.

The definitive receipts are `round4-final/gates.jsonl`, its per-command logs, `round4-final/archive-shape.json`, and `round4-final/scope-proof.json`. `run-round4-gates.py` records the commands and environment. Older top-level logs predate the amended scope and are superseded by these receipts.

`PR-BODY.md` preserves the full current PR body, with the author prefix, current status and one-line Round 4 note updated; `Closes #508` remains. The PR itself was not edited.

Independent delta reviews by R306 and R307 remain pending. Publication and hosted evidence belong to the next handoff step. No push, PR edit, merge, additional checkout or delegation was performed. No review verdict is supplied by this author handoff.
