[A175] REVIEW READY

Local commit `059c3a60b8290873ed9fd14673f9981e8af754ce`, tree `600468436fb9435a6b15c41db0156e5304848cb6`, sole parent `60c5225fe5f93209bf313c51b7a722f25f9aaa7d`. Source is clean and unpublished.

Corrections retain R239's original IDs and **MINOR Docs** assignments:
- **F1:** guide distinguishes skipped reset completions from vacuous passes after release, explains reset inside the witness flag's `$past`, and scopes zero first-edge history to the measured 5.050 two-state setup.
- **F2:** guide, testing index, suite README and harness header agree on **15 equality / 2 floor / 4 presence** checks.
- **F3:** removed unsupported formal-tool claims; retained only simulation and no formal-tool execution.

Validation: these commands exited 0, each through `rtk proxy`:
```text
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/check_doc_paths.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_cpp_idiom.py
python3 scripts/check_sv_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_sh_idiom.py
python3 scripts/check_hygiene.py --check
python3 scripts/check_em_dash.py --base 60c5225fe5f93209bf313c51b7a722f25f9aaa7d
git diff --check 60c5225fe5f93209bf313c51b7a722f25f9aaa7d HEAD
```
Em-dash: zero findings over 29 added Markdown lines, 57/57 controls. Precommit receipts retain their execution identities and match committed bytes. Two receipt collectors hit index-lock contention; separate TOC-anchor/hygiene reruns passed, with earlier evidence retained.

Semantics were checked against [unchanged R239-1 public measurements](https://github.com/kebag-logic/milan-fpga/tree/7795e487048867fde07a224ec1a5885acfb4375b/review-evidence/372-r1/review/R239-1): reset R1 edges 9/10, pastprobe and both witness tables. Downloaded evidence matches immutable Git blobs; the changelog item is a fixed-version link/hash receipt. The supplied selector reports pinned 5.050 and matches R239's digest. **No simulation or formal run was repeated by A175.**

Only the four authorized paths changed. All 39,374 harness bytes from line 36's first `#include` onward, including line numbering, are unchanged; SHA256 `88da057b116caa9ca6fb3602e38ca94f205dc8e3234a7a0e9b820e7b8bce6339`. Other parent files, modes and gitlinks are unchanged; final 857-file blob/kind/mode and index checks pass.

Assigned text corrections are ready for re-review; acceptance and optional #495 scope are unchanged. F1/F2/F3 await reviewer disposition. R240 internal Codex and R239 external Opus own corrected-head coverage, including Tests/Robustness; Opus availability remains pending. Manager full validation, publication, act, hosted and completion duties remain pending. Factual `372-correction/HANDOFF.md`, `REVIEW-READY.md` and exact command/head/tree/exit/token receipts are prepared. This is executor evidence, not approval.
