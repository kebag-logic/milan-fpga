# Datapath recipe results

The initial full make invocation timed out during compilation. Its two gPTP
legs each completed 182 checks with zero failures. Remaining recipe commands
were executed separately from the unchanged Makefile dry-run list.

| Step | Leg | Return code | Last result |
|---:|---|---:|---|
| 16 | Default datapath | 0 | milan_datapath: 236 checks, 0 failures |
| 17 | Notification | 0 | checks: 423   failures: 0 |
| 18 | CRF licence | 0 | checks: 416   failures: 0 |
| 19 | Dynamic map | 0 | checks: 162   failures: 0 |
| 20 | NxN | 0 | checks: 1967   failures: 0 |
| 21 | Divergent descriptor shape | 0 | checks: 1969   failures: 0 |
| 22 | Eight-stream shape | 0 | checks: 3751   failures: 0 |
| 23 | Four-channel shape | 0 | checks: 1967   failures: 0 |
| 24 | Filter-disabled shape | 0 | milan_datapath: 236 checks, 0 failures |
| 25 | Pruned shape | 0 | checks: 33   failures: 0 |
| 26 | Shipping shape | 0 | milan_datapath: 233 checks, 0 failures |
| 27 | Audio-clock full regression | 124 | No completed verdict |
| 28 | Render mutation campaign | 0 | 6 checks: 6 PASS, 0 FAIL |
| 29 | Shipping counter fixture | 0 | 1x1 clean run.log: rc=0, failures=0 |
| 30 | Largest counter fixture | 0 | 8x8 clean run.log: rc=0, failures=0 |

The short-deadline audio-clock attempts are incomplete. The final original
executable completed in a persistent foreground session with short polling:
exit 0, media_aclk: 193 checks, 0 failures. Its evidence is aclk-final-run.log and
aclk-final-run.rc. The optional two-thread experiment was stopped without a
verdict. No incomplete attempt is counted as a gate pass.

The copied datapath_steps.py accepts the suite and evidence directories as
arguments and executes the indexed commands without modifying the checks.
