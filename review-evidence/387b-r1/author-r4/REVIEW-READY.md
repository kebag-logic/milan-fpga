[A283] REVIEW READY

Commit: `00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b` (local, unpushed; parent `0f003fab3303858ba4db955ad3c0512e67a8018b`).

Changed: only `docs/testing/TESTING.md`, `docs/testing/RUNNING_TESTS.md`, `tb/verilator/milan_dp_gptp/README.md`, and the `tb/verilator/milan_dp/render_mutants.py` docstring. All four current deadline statements say 3600 s under [decision 5820240308](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5820240308); the testing guide retains the recorded-samples link.

Scope proof: `git diff --stat 0f003fab3303858ba4db955ad3c0512e67a8018b 00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b` reports four files, +7/-5. Exact replacements were checked against the parent. The executable syntax tree is unchanged outside the module docstring. The workflow history and self-test file are byte-identical. `git grep -n -w 2700 -- docs scripts tb` leaves only the two historical lines and the planted mutation.

Validation: all commands below returned 0 at this head, in the foreground without pipelines:

```sh
python3 scripts/docs_check.py
# Repeated from an archive of this head without Git metadata.
python3 scripts/check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_doc_paths.py
python3 scripts/check_py_idiom.py
python3 -m py_compile tb/verilator/milan_dp/render_mutants.py
git diff --check
git diff --check 0f003fab3303858ba4db955ad3c0512e67a8018b 00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b
```

Both documentation modes reported zero findings over 165 Markdown files and 859 text files. The no-metadata mode reported its expected inventory-parity skip. The em-dash gate reported zero findings and 339/339 controls.

Acceptance: the [Round 4 assignment](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5821889812) is implemented; F1 from both reviews is ready for independent delta review. Acceptance 4 remains open under #117.

Handoff: `HANDOFF.md`, the full updated `PR-BODY.md`, the complete delta, scope proof, and gate receipts are prepared in the assigned output packet. The PR body preserves `Relates to #387` and the acceptance-4 note. No push or PR edit was made.

Open risks/questions: no new implementation question. Independent delta reviews, publication, and candidate validation remain pending.
