[A839]

Closes #111.

Run the engine suite's four passes at once, printing each in the serial order

Branch: `engine-run-passes-at-once` at `bbda770` on main `1213ac5` (#108), in a scratch clone of
Mister-M-alt/FPGA-gPTP. Not pushed. No FPGA-gPTP Issue exists for it: it comes from kebag-logic/milan-fpga's CICD
lane (#998, round 2 §3.4), where `make -C gptp-processor all` is the slowest unit of the native bank.

## What changes

`tb/verilator/engine/Makefile`, target `run`. The suite runs four passes against one build: shipping, the request
counter seeded above 16 bits, the Sync counter seeded above 16 bits, and priority1 255 with clockAccuracy 0xFE
(#82, #100). Each pass reads only its own ROM image, from its own directory, and none writes anything another
reads. So the recipe now:

1. builds the harness, as before;
2. writes the three seeded images first (the generator calls are unchanged; only their place moves);
3. starts the four passes together, each with its output in `obj_dir/pass<N>.out`;
4. waits for all four, then prints each pass's output in the old order under the old echo lines, and exits at the
   first failing pass in that order with that pass's status.

So the transcript is the serial one, byte for byte. An INT or a TERM to the recipe kills all four passes; the
traps are set before the first one starts. The stale comment "The suite runs THREE times" now says FOUR.
`docs/TEST_DEVELOPER.md` says the four passes run at once (four sentences in the guide's one-line style).

Nothing else changes: no check, image, generator argument, harness flag or mutant. `mutants`, `mutants-order-test`
and `mutants-jobs-test` do not use `run`'s recipe.

## Behaviour that differs, on failure only

- A generator that refuses a seeded image now stops the recipe before pass 0 prints, not between passes. Its
  message is the generator's own (its stdout stays discarded, as before; stderr shows).
- When pass N fails, the later passes have already run to completion; their outputs are not printed, as before,
  because the recipe stops at pass N.
- make's error line names the new recipe line: `make: *** [Makefile:65: run] Error <status>`.

## Measured (kebag-logic/milan-fpga's shared build host, 2026-11-24)

One run per variant, started 17:02 together. The serial run (main `1213ac5`) had one physical core. The parallel
run had four physical cores, one thread each, with the siblings left unused. Host load was 200-230 from other work
throughout. Pinned Verilator 5.050, g++ 16.2.1, ccache on PATH (#104).

| `make -C tb/verilator/engine run` | wall | CPU (user + sys) | cycles | instructions | exit |
|---|---:|---:|---:|---:|---:|
| main, serial | 2721.6 s | 817.7 s | 2.96 T | 7.52 T | 0 |
| this branch, passes at once | 974.6 s (2.79x faster) | 836.8 s (+2.3 %) | 3.01 T | 7.54 T | 0 |

The two transcripts are IDENTICAL after removing only host text: the checkout path inside the echoed build
commands and Verilator's statistics lines. That leaves 170 lines, every check line, figure and verdict byte for
byte, with no number masked. Round 2 measured an earlier form of this patch at 2757 s against 840 s, also
identical.

The recipe's TERM path, checked by hand: `make run` was started, the four passes were seen running, and make was
sent SIGTERM. make exited with `Error 143`, and all four simulators were gone 3 s later.

On fewer than four free cores the passes share them, so the run takes up to the serial time and never more:
total CPU is the same (+2.3 % above).

## How to validate

```sh
git checkout engine-run-passes-at-once
make -C tb/verilator/engine clean
make -C tb/verilator/engine run > /tmp/par.log 2>&1; echo "rc=$?"     # 0
git checkout 1213ac5 -- tb/verilator/engine/Makefile
make -C tb/verilator/engine clean
make -C tb/verilator/engine run > /tmp/ser.log 2>&1; echo "rc=$?"     # 0
git checkout engine-run-passes-at-once -- tb/verilator/engine/Makefile
diff <(grep -v -e '^- Verilator' -e 'g++' -e 'verilator --cc' /tmp/ser.log) \
     <(grep -v -e '^- Verilator' -e 'g++' -e 'verilator --cc' /tmp/par.log) && echo IDENTICAL
make docs lint                                                        # both exit 0 at this head
```

A failing pass still fails the run with its status, checked with a stub. After one real build, replace
`obj_dir/Vengine_sim` with a shell script that prints a line and exits 3 when run from `seedrun/`, and 0 elsewhere.
Then `make run`. The output is pass 0's lines, the request-counter echo line, pass 1's `[FAIL]` line, then
`make: *** [Makefile:65: run] Error 3`, with make exiting 2. Neither later pass's output nor its echo line prints.

## Not done here

- The parser arm (`tb/verilator/parser/mutants.py`, 34 mutants run one at a time with no ccache, ~465 s) has the
  shape #102/#104 fixed for the engine arm. Porting `in_list_order` and `compiler_env` there is a separate change.
- Nothing was pushed and no PR was opened; the owner of this repository decides.
