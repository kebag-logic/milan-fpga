# Workflow jobs at 394612c5, step by step

The jobs this round touches ran through `run_wf.py.txt`, each on its own fresh clean clone of 394612c5: every
job of `docs.yml` (the docs gates, the Python idiom gate among them), `rtl-fast.yml`'s `changes` and `rtl.yml`'s
`full-ci-gate` (both run `scripts/ci_scope.py --selftest` and classify the change), and `elaborate.yml`'s two gate
jobs (their scope step runs `ci_scope.py`). The steps come from the workflow files in that clone, one log and one
rc per `run:` step (`logs/`). `verify_wf_jobs.py.txt` is round 2's `verify_wf.py.txt` restricted to the named jobs
(`--only`); it fails on any step of them with neither an rc of 0 nor a reason in `not_run.json`. Result:
`verify-394612c5.md`, 77 steps rc 0, 49 not run with a reason, 0 bad. The batches' own lines are `batch-*.log`.

- Job venv: the elaborate gate jobs ran with the host's LiteX venv; every other job with the pinned gates venv
  (the same releases as the hosted `PIP_CONSTRAINT`, on this host's CPython).
- RV32 SDK: the runner's `$HOME/br-milan-rv32` links the host's pinned SDK, as in round 2.
- Not run this round: the other jobs of these workflows (the Verilator and Yosys suites, the firmware jobs, the
  elaboration itself), which nothing this round changed reaches but `gen_mailbox.py`'s variant path, run here by
  the mailbox suite and the firmware gate (`../mbx/`, `../firmware/`); round 2's every-job run at 8f73ade5 stands
  for the rest.
