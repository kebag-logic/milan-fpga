# Steps run a second time on the same head, and why

Head `f3e902f2a96bb27eac6ed7780c70905af34f389e`. Each first log and rc is kept beside the second as `<step>.first-run.log` and `<step>.first-run.rc`.

| Step | First run | Cause | Second run |
|---|---|---|---|
| `rtl.full-ci-gate__target` | rc 1: `GITHUB_REF: unbound variable` | The runner set no `GITHUB_REF`; the step only prints it | rc 0, after the runner set `GITHUB_REF=refs/heads/823-nvm-format` (no PR exists) |
| `rtl.full-ci-gate__gate` | rc 0, but scoped `HEAD^1..HEAD` (the last commit's 4 files) | The checkout is the head, not GitHub's merge commit, and the runner did not set `ACT=true`, so the selector took its hosted path | rc 0 with `ACT=true`: the replay path, `git merge-tree` against the live base `a9d69c77`. The changed files equal `git diff a9d69c77 f3e902f2`, and `rtl=true run_full=true` |
| `elaborate.elaborate-gates-0__scope`, `elaborate.elaborate-gates-1__scope` | rc 0, same `HEAD^1..HEAD` scoping | Same | rc 0 with `ACT=true` |

The runner does not evaluate `if:` conditions; it runs every `run:` step not in `not_run.json`. So the first scoping skipped no step, and the second changes no other step's result. The jobs that started after the runner change also ran with `ACT=true` and `GITHUB_REF` set. Every job that started before it reads neither variable, except these four steps.

Each `__DONE` file keeps the job's first full run. The second runs above are steps run alone in the job's own clone.
