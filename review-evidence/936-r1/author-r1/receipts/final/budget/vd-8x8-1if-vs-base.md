Original file: <scratch>/budget/final/vd-8x8-1if-vs-base.md
Original size: 1939 bytes
Original sha256: 9e0a2889e38e47a8f1f77dde9a121403a6313106698dd0bd72c31218a7f603a9

# `valid-destinations` at 8x8/1if: the final image against the base 70f4056f

Both runs: `run.py --point 8x8-1if --variant valid-destinations` on a clean clone (the final image built at
b496c99e, which 7cfb8a04 changes no input of: every image the fixture and the ledger build is identical there by
sha256; the base at 70f4056f), groups `srp-talker` and `srp-talker-loss`.
Each grade is the harness's own (`run-console.txt`, `base-70f4056f/vd-8x8-1if-console.txt`).

| | Base 70f4056f | Final |
|---|---|---|
| groups, refusals, budget misses | 2, 0, 0 (0 of 19 instances, 0 of 10 paths) | 2, 0, 0 (0 of 19 instances, 0 of 10 paths) |
| the Talker declare and withdraw rows | all within 220 ms | all within 220 ms, at most 189.423 ms |
| `STATED` a tier-2 slice of THE TRANSMIT's build (THE TIERS' 90,000) | 1, 91,604 CPU cycles | 1, 92,226 |
| `STATED` a build-one pass (the 1x1/1if 73,500) | 18, 81,352 to 91,604 | 16, 81,473 to 92,226 |
| `STATED` THE RETRY's round of 0 notices and 1 refused attempt (the one-interface 11,900) | none; the longest round 2,174 | 21, 11,922 to 12,537 (16 in `srp-talker`, 5 in `srp-talker-loss`) |

The tier-2 slice and the build-one passes are over their stated costs at the base too, as 8x8/1if reports the costs it
takes past the one-interface ones (`ctrl_service_budget/README.md`).

The rounds are new with #936. Each is THE RETRY attempting a STREAM_OUTPUT's GET_STREAM_INFO notice (`aecp.c` `scan`,
command 15). The fixture's gather window does not answer in this arm (`aecp_face.c` `gsi`: `mbx_win_read` not OK, so
`stream` returns false), so the attempt is refused and AECP's backoff retries it (`AECP_RETRY_MAX_MS`). Only the
`answering-*` arms answer the window; there the retried notice is built and timed (`notice-retried`, at most 8.301 ms
at 1x1/1if and 8.246 at 8x8/1if against 20 ms). At 1x1/1if the same arm's rounds are at most 9,015 cycles, within
11,900, and print no `STATED` line.
