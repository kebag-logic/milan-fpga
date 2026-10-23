The docs workflow's gate steps at 24a292a0 (round 8), their run: bodies executed literally (scripts/round7/docs_steps.py,
as in rounds 7, 7b and 7c), GNU Make 4.3 first on PATH, CPython 3.12.3 (a venv with the workflow's pinned requirements), the
shipping SDK for the builder legs. Driver: scripts/round8/docs_run.sh (round 7b's with the scratch directory moved). The
clean clone's third_party/tsn-c-stack origin was set to its .gitmodules URL before the run (tsn-c-stack-origin.txt); the
clone's origin/dev is e5b480a3, the live dev tip (origin-dev-and-head.txt), which the added-line em-dash gate diffs against.

docs/                 44 steps: 42 rc 0, 2 skipped by rule (all.out, receipts.json). gate_41's log is over 200 KB and is
                      recorded by sha256 and size (docs/large_logs.sha256).
docs-leg1-litex/      builder leg 1 again with MILAN_LITEX_PYTHON set: rc 0.
docs-md312/           the five markdown gates (7, 8, 9, 43, 45) on CPython 3.12.3: 5 of 5 rc 0.
docs-nogit/           the no-git step's two gates (docs_check.py, check_feature_status.py) on a git-archive export of
                      24a292a0 without submodules: both rc 0.
Skipped: gate_42 (it executes the candidate's act_ci.py on the host; AGENTS.md section 5 allows the candidate copy only
inside the disposable CI job), docs-check-no-git/ci_step_3 (rm -rf .git; its two gates are docs-nogit/).
