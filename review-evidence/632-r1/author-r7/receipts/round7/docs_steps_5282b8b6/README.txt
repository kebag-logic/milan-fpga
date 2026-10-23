The docs workflow's gate steps at 5282b8b6, their run: bodies executed literally (scripts/round7/docs_steps.py,
adapted from the #771 lane's replica), GNU Make 4.3 first on PATH, CPython 3.12.3 (a venv with the workflow's pinned
requirements), the shipping SDK installed at $HOME/br-milan-rv32/host by scripts/ci_rv32_sdk.py from the pinned archive.

docs/                 44 steps: 40 rc 0; the two builder legs refused at once ("source dependency origin differs:
                      third_party/tsn-c-stack": the clean clone's submodules came from the lane's checkouts, and
                      scripts/ci_case_receipts.py requires that submodule's origin to be its GitHub URL); 2 skipped.
docs-gate_25_0/       builder leg 0 again after `remote set-url origin <the .gitmodules URL>` in the clone's
                      tsn-c-stack: rc 0, all gates but 1 arm (gate 1b's MAKEFLAGS += -e mutation, which make 4.3
                      cannot express) pass.
docs-gate_25_1/       builder leg 1 the same way: rc 0, 16 arms not run (no LiteX in the CI interpreter).
docs-gate_25_1-litex/ builder leg 1 with MILAN_LITEX_PYTHON set: rc 0, all but gate 11 (the Arty calibration tree).
docs-md312/           the five markdown gates (7, 8, 9, 43, 45) again on CPython 3.12.3 with the pinned renderer:
                      5 of 5 rc 0 (docs/ ran them on the shared renderer venv).
docs-nogit/           the skipped docs-check-no-git step's two gates (docs_check.py, check_feature_status.py) on a
                      git-archive export of 5282b8b6, no .git: both rc 0.
Skipped: gate_42 (it executes the candidate's act_ci.py on the host; AGENTS.md section 5 allows the candidate copy
only inside the disposable CI job), docs-check-no-git/ci_step_3 (rm -rf .git; its two gates are docs-nogit/).
