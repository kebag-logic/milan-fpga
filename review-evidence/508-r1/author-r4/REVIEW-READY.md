[A299] REVIEW READY

Commit: `9d66cfe0dc87ffe4a5f45691d5c86b041b050b38` (local, unpushed).
Branch: `508-pp-pin-adopt`. PR #560, amended round 4.

The [amended assignment](https://github.com/kebag-logic/milan-fpga/issues/508#issuecomment-5826348330) is implemented in exactly five files, with six lines replaced:

- `tb/verilator/milan_dp/README.md:488` names F06.13 and F05.5 and links both through GitHub blobs pinned to `990f96526bb89356c963a260ebbdcf2a77e6623a`, retaining `#fig-06-lineage` and `#fig-05-settled`. Both fragment targets and figure labels were verified at that pin.
- The campaign descriptions in `CHANGELOG.md:57`, `tb/verilator/milan_dp/Makefile:451-452`, `scripts/measure_test_evidence.py:620`, and `docs/testing/TESTING.md:267` now agree with eight mutant arms, eight additional elaborations and nine runs.

Validation: every assigned command returned rc 0 at this exact committed head, in the foreground without shell pipelines:

```text
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
python3 scripts/docs_check.py
env GIT_DIR=/nonexistent-508-a299-git python3 scripts/docs_check.py
python3 scripts/check_doc_paths.py
python3 scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
python3 scripts/check_py_idiom.py
git diff --check
git diff --check 224ec0e9a9fa129924bf8f0433cf70b4140f7bd2 9d66cfe0dc87ffe4a5f45691d5c86b041b050b38
```

Archive proof: `git archive` of the new head was extracted without submodule content. All four gitlink directories were verified empty or absent. `python3 scripts/docs_check.py` returned **0 findings, rc 0**, over 165 Markdown files and 861 scrubbed text files, both without Git metadata and using the clean lane's index for Git inventory (`GIT_DIR=<lane-git-dir> GIT_WORK_TREE=<archive>`). Archive contents supplied every scanned file. No additional checkout was created.

The anchor gate reproduced 168 links; path validation resolved 842 paths; the evidence self-test passed 101/101; the em-dash gate reported zero findings with 339/339 controls. Both no-Git runs explicitly skip inventory parity. Budgets remain unchanged.

Acceptance: both assigned fixes are implemented and locally verified. The committed diff matches only the specified replacements; the working tree is clean, and the processor pin and behavior are unchanged. The commit message has one line, no body and no trailers.

`HANDOFF.md`, the full updated `PR-BODY.md`, command receipts and the scope/archive proofs are written in the assigned output directory. The PR body retains `Closes #508`.

Open handoff items: independent delta reviews by R306 and R307, publication, and hosted checks at the new head. No push, PR edit or merge was performed.
