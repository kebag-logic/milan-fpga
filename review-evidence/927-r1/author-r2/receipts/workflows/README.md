# Workflow jobs, step by step

Each job of `rtl-fast.yml`, `elaborate.yml` and `docs.yml` through `run_wf.py.txt` on a fresh clean clone of the
head, one log and one rc per `run:` step (kept in scratch); `verify_wf.py.txt` fails on any step with neither an rc of
0 nor a reason in `not_run.json.txt`. The runner, its not-run reasons and the verifier are #919's and #920's, with this
lane's branch and paths; the runner's HOME links the pinned RV32 SDK.

- `at-338ece89/`, `verify-338ece89.md`: the five batches (`launch_wf.sh.txt`, the shared session pool). The
  publication census was OOM-killed at 17:22 inside its 10 GB unit when its tools saw 128 CPUs (the pool's affinity
  widened mid-run); it was cut again by the 18:46 and 19:39 stops and rerun alone on 8 CPUs, as round 1's passing run
  (`census workers: 5 of 8`, peak 8.5 GB): `at-338ece89/publication-census/`.
- `at-0297a19a/`, `verify-0297a19a.md`: the five batches at the head (`launch_wf2.sh.txt`, each pinned to 8 CPUs).
- `docs-check-no-git` removes the clone's `.git` by design, so it leaves no `__DONE` marker; its steps' rcs are
  recorded.
