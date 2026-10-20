# Round 1b sweep attempts that produced no verdict

| Attempt | What happened |
|---|---|
| `reset-cut-r1b` | the sweep at `4605409b`, cut by the host reset after 22 of 63 suites (all 22 PASS). No verdict; re-run from the start. |
| `s0-refused-nohup`, `s1-refused-nohup` | the re-run, first launch: started under `nohup`, so the runner's own preflight "hard-HUP" cancellation control timed out (SIGHUP ignored and inherited), the same cause as round 1's `sweep-attempts/sweep1-refused-nohup`. No suite started. Relaunched without `nohup`. |
| `s1-reset-cut-2` | the relaunched sweep at `4605409b`, run as two shards. Shard 0/2 finished (rc 0, 32/32, kept as `sweep-head/s0/`). Shard 1/2 was cut by the second host reset after 21 of 31 suites, all 21 PASS (`runner.out`). No verdict; shard 1/2 re-run from the start as `sweep-head/s1/`. |
