[A280]

Parent source base: `573f0052a0e4412e81f0845438fcec2086ce5d55`; original processor pin `09f9bf3846511f8388d995126502ed92eaa65213`.

Control: processor `a8f8ce810ddba1816cd129d0afcd71e6e02ade1b`, local parent commit `9947af735f2228c7780c44ba98eadb368f5efd04`.
Candidate: processor `29840136bb2d21bc0fbe92c7c533368f40837ff6`, local parent commit `dd8b228b1c1949b10af3b98aab398265477c0775`.

Both commits change only the processor gitlink. Nothing was pushed. The parent is left clean at the candidate commit with its processor checkout matching the committed gitlink.

| Gate | Control rc | Candidate rc |
|---|---:|---:|
| C++ idiom | 0 | 0 |
| Python idiom | 0 | 0 |
| Front-end ratchet | 0 | 0 |
| RTL source lists | 0 | 0 |
| Processor source check and self-test | 0 | 0 |
| Builder | 0 | 0 |
| Consumer simulation | 0 | 0 |

Consumer simulation: 371 checks, zero failures at each pin. The front-end gate has the same four allowed findings at each pin. There are no failing commands to attribute to the older-pin gap.

The builder reports one unrun arm at both pins: historical resource calibration, because its reference placement report is absent. This shared missing-input limitation is not a pin regression or hardware evidence. The other builder arms pass.

Exact commands, return codes, elapsed times, pins and matching front-end findings are in `parent-comparison.json`. Full output is in the seven `control-*.log` and seven `candidate-*.log` files.
