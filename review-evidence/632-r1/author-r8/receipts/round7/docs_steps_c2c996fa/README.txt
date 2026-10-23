The docs workflow's gate steps at c2c996fa (round 7c), their run: bodies executed literally (scripts/round7/docs_steps.py,
as in rounds 7 and 7b), GNU Make 4.3 first on PATH, CPython 3.12.3 (a venv with the workflow's pinned requirements), the
shipping SDK for the builder legs. Driver: scripts/round7b/docs_run.sh. The clean clone's third_party/tsn-c-stack origin
was set to its .gitmodules URL before the run (tsn-c-stack-origin.txt).

docs/                 44 steps: 42 rc 0, 2 skipped by rule (all.out, receipts.json). Leg 0 (gate_25_0): all gates but
                      gate 1b's MAKEFLAGS += -e arm, which make 4.3 cannot express. Leg 1 (gate_25_1) under CI's
                      interpreter: the LiteX arms not run (no LiteX in that interpreter).
docs-leg1-litex/      builder leg 1 again with MILAN_LITEX_PYTHON set: rc 0, all but gate 11 (the Arty calibration tree).
docs-md312/           the five markdown gates (7, 8, 9, 43, 45) on CPython 3.12.3: 5 of 5 rc 0.
docs-nogit/           the no-git step's two gates (docs_check.py, check_feature_status.py) on a git-archive export of
                      c2c996fa without submodules: both rc 0.
Skipped: gate_42 (it executes the candidate's act_ci.py on the host; AGENTS.md section 5 allows the candidate copy only
inside the disposable CI job), docs-check-no-git/ci_step_3 (rm -rf .git; its two gates are docs-nogit/).
