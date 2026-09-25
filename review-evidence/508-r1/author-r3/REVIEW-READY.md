[A297] REVIEW READY

Commit: 224ec0e9a9fa129924bf8f0433cf70b4140f7bd2 (local, unpushed).
Branch: 508-pp-pin-adopt. PR #560, round 3.

Items 1-4 of the assignment are implemented in six files:

- The historical #530 changelog section is byte-identical to dev c266432dcb0cdd464205823a3d82cad260eedde2. Processor #116/#113 entries occur once, in the 990f9652 section.
- All nine processor citation spans resolve at 990f96526bb89356c963a260ebbdcf2a77e6623a. The proof compares the cited source text with the earlier references and checks the full lane's added citation inventory, including multiline ranges.
- G8 requires exactly two pushes per controller: registrar withdrawal, then settlement teardown. All four bodies are graded as PASSIVE, ACMP status zero, cleared failure fields, and equal to the solicited body. The first already sees teardown because responses read live owners. Sink 1 must remain quiet. The README and banner state both causes and the count.
- The duplicated-withdrawal mutant fails the named G8 count checks for both controllers: got 3, expected 2. It runs against a temporary processor copy, and its raw receipt is retained.

Validation: all required commands returned rc 0 at the exact local head:

```text
make -C tb/verilator/milan_dp notify gsi-mutants
make -C tb/verilator/milan_dp run
make -C tb/verilator/pp_shadow
python3 scripts/docs_check.py
env GIT_DIR=/nonexistent-508-a297-git python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_doc_paths.py
python3 scripts/xvlog_gate.py --check
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_port_contracts.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_test_evidence.py --check
git diff --check
git diff --check c266432dcb0cdd464205823a3d82cad260eedde2 HEAD
```

The notification leg passed 380/380; the campaign passed 9/9 controls (clean plus eight caught mutants). The complete default datapath run passed, including its built-in controls. The shadow suite passed 371/371. The citation/changelog proof and raw duplicate-mutant proof also returned zero. The HDL frontend ran with its four existing recorded findings; all budgets are unchanged. The em-dash and TOC checks used the locked Markdown dependencies. The no-git documentation mode skips only its Git inventory-parity arm.


Acceptance 2 follows the recorded decision in [5825732419](https://github.com/kebag-logic/milan-fpga/issues/508#issuecomment-5825732419); no state-oracle change was made.

HANDOFF.md, the full proposed PR-BODY.md, exact command/exit-code ledger, citation proof, raw duplicate-mutant receipt and per-command logs are in the assigned 508-a297 output directory. The public review-evidence scratch was deleted after reading. All submodule pins and source checkouts remain unchanged.

Open handoff items: delta reviews by R306 and R307, head publication, and hosted candidate evidence. No push, PR edit or merge was performed.
