[A264] REVIEW READY

Commit: `39a0171c8c39e68065b14b9178b30d708a9f7645`, local branch `546-crf-talker-step`, from dev `57456af96b3127b9d309a995bbbd35a6113ce52d`.

Changed: `KL_crf_rx` discards crossing rate history on accepted `tu` edges, timestamp jumps, or sequence gaps. The event timestamp seeds a fresh 256-interval history. A validity wire gates the servo's sample input, preserving its integrator and lock state; the servo's own guard logic is unchanged. The unmarked-jump threshold is derived as ceil(2 ms * 300 / 999900) + two PHC quantization bounds, rounded upward: 2048 ns. No CSR bit or counter added; time-sync, recovery, register and test documentation updated.

Acceptance evidence:
- Receiver suite: 13,836 original checks, 1,658 discontinuity checks and 19 connected-loop checks, all passing.
- The GM-change scenarios step both ends by +150 us and -150 us. The servo remains LOCKED on every observed clock; no receiver unlock is counted. The integrator is unchanged for the marked positive step and varies only 0.020 ppm through unmarked negative-step recovery.
- All four receiver mutants fail named checks: tu ignored (9 failures), jump backstop removed (32), refill one interval short (17), and accept-edge validity delayed (2). The separate ignored-servo-validity mutant fails U13's trim and lock checks.

Validation: `make -C tb/verilator/crf_rx`, its `mutants` target, `make -C tb/verilator/mmcm_servo` (82/82 unit, 8/8 rails, 113/113 PHC steps), `make -C tb/verilator/mmcm_servo_autorepair` (47/47), and the default `make -C tb/verilator/milan_dp run VERILATOR_JOBS=4`: all rc 0. Both CI documentation modes, `check_em_dash --base 57456af96b3127b9d309a995bbbd35a6113ce52d`, documentation style/TOC/paths/matrix, actual front-end analysis, RTL source lists, C++/Python/SV idioms, RTL lint, test-evidence gate, `cd tests && behave --no-capture -f plain` (344 scenarios), and `git diff --check`: all rc 0.

Mapped area: receiver 355 -> 433 LUT and 509 -> 544 FF; servo 862 -> 864 LUT, FF unchanged. Total +80 LUT, +35 FF, +22 CARRY4; BRAM/DSP unchanged.

`HANDOFF.md`, `PR-BODY.md`, the source diff/hashes, gate table, mutant receipts and area logs are in the assigned output packet. Local worktree clean. No push, PR operation, merge or hardware activity. Independent review, hosted checks and publication remain with the manager. Local PHC slew handling remains #545's separate lane.
