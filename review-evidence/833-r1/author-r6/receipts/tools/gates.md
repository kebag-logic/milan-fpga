| Gate | Result |
|---|---|
| Every `run:` step of `.github/workflows/docs.yml`, each job on a fresh clone of this head | Verifier rc 0: 64 steps rc 0, 31 not run with the round 1 reason unchanged (hosted-only or apt), 0 bad. Tree clean after each job. Builder legs in it: `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`, as in rounds 1 to 5 |
| `python3 scripts/test_suite_cancellation.py` | rc 0, `suite cancellation: PASS`, with `trap_finished: True` for the shell window. The stated seconds' passes are 5, 29, 12, 32 and 52, the stubborn parent's SIGKILL is in pass 9 and the vanishing verdict in pass 49. The reused identity shows `signalled: False, through_handle: True` |
| `python3 scripts/test_suite_cancellation.py --mutants` | rc 0, `owned-process mutants: PASS (74 mutants, 70 with a control that must fail)`. `--matrix`: 825 runs in 3 parts, each PASS |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | rc 0, `mutant lifecycle: PASS` |
| `cd tests && behave` | rc 0: 14 features, 508 scenarios, 2330 steps passed, 0 failed |
| `git diff --check 1f29f189 HEAD` | rc 0 |
| Full sweep | Not rerun: round 6 changes only files round 1 changed. It ran at `d4d8cff9`: 65 of 65 suites, rc 0 on all 4 shards |
