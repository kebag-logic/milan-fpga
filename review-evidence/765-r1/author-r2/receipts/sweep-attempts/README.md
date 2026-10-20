# Sweep attempts that produced no verdict

| Attempt | What happened |
|---|---|
| `sweep1-refused-nohup`, `sweep2-refused-nohup` | `run_all_suites.sh` refused in its own preflight: the "hard-HUP" cancellation control timed out. The runner had been started under `nohup`, so SIGHUP was ignored and inherited; the control cannot kill a process that ignores it. No suite started. Relaunched without `nohup`. |
| `sweep3-cancelled-sv2v` | stopped by this lane after its first suite, to put the CI-pinned sv2v 0.0.12 ahead of the host's 0.0.13 on PATH. |
| `../sweep-first-91aaa6bd-cancelled` | the first full run, at `91aaa6bd`: 48 suites passed and `milan_dp` failed (the stimulus finding in HANDOFF.md). Stopped after 49 suites once the fix was in hand; the final sweep reran every suite at `cc71db3a`. |

An earlier launch under CPython 3.12.3 refused before the preflight:
`scripts/owned_process.py` needs `os.pidfd_open`, which that build lacks.

The runner's `preflight/check_merge_containment.log` is not copied for any
attempt (kept in scratch); no claim here rests on it.
