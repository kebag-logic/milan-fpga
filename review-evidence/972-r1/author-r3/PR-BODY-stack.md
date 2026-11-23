[A820]

## Status

Local validation passed at `55852269db3554900d2b71e6f9a7b153cff69e14`.
`970-gm-change-draw-kind` -> `main`; correction review pending for PR #36.

Relates to kebag-logic/milan-fpga#970 and kebag-logic/milan-fpga#972.
Executor: `[A820]`. Independent reviewers: `[R891]` and `[R892]`.

## Description

The GM_CHANGE check in WAITING now requires exactly one fresh delay draw of the correct kind.
MFDISC-01 and Milan v1.2 5.6.3.5.7 require the transition to DELAY with a new TMR_DELAY drawn from 0 to 4 s.
Reusing the previous draw could satisfy the old kind and bound checks because that previous draw also came from 0 to 4 s.

- A2 in `AdpCore.A0toA2Schedule` captures the draw count before `adp_gm_change` and requires `a.draws == draws + 1u`, `ADP_DRAW_DELAY`, DELAY state and an armed delay equal to that draw, bounded by literal 4,000 ms.
- Two registered plants prove the assertion detects the wrong startup draw kind and a re-arm using `last_draw_ms` without drawing again. Both fail with `A2 GM_CHANGE in WAITING: DELAY with a 0..4 s draw (5.6.3.5.7)`.
- TESTS and TRACEABILITY are regenerated; VERIFICATION records 475 core plants, 479 total. The changelog records behavior without a review label.

The branch starts at `715589c1`. Production source, headers and delay constants are unchanged, so the parent repository needs no pin change.

## Validation

```sh
python3 scripts/validate.py --work <work>/validate --jobs 8 --graphs
python3 scripts/baremetal.py --work <work>/baremetal --jobs 8
```

| Check | Result |
|---|---|
| Full validation at `5585226`, including graphs | 28/28 gates pass; 479 CAUGHT, 0 ESCAPED, 0 ERROR |
| Bare-metal builds | Debug and Release pass |
| No-draw plant applied at `61a504e` | Escapes: all 10 test binaries pass |
| Same plant at `5585226` | Caught by A2 with the required failure message |
| Tracked tree before/after validation | Clean and unchanged |
| Production source/header diff from `715589c1` | Empty |

Expected result: all gates pass and both registered GM_CHANGE plants are caught.
The draws remain 0 to 4 s for LINK_UP, DISCOVER, TMR_ADVERTISE and GM_CHANGE in WAITING, and 0 to 2 s for startup with link up.
