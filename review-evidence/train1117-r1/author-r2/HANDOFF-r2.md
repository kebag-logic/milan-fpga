# HANDOFF, round 2: the flip train's composition (#665), [A794]

**Tip: `6ad5c259`** on `flip-train-1117` (local; nothing pushed or posted). Steps 7 and 8 are composed, with the
composition commit for THE STEP between them, under #665's ruling of 2026-11-17 (issuecomment-6950343235; decisions
1 to 3). Every frozen head so far is an ancestor of the tip: `d3e61e37`, `e1ecce20`, `394612c5`, `37255683`,
`1a1e6665`, `81c9a1a0`, `d06ded5a`, `0fdfdba7`. **Waiting for #934's and #936's heads**, which the manager names in a
later RESUME. Not cut, as ruled: the cut is taken at the final composed head only. No STOP condition was met (below).

## Commits this round

| Commit | What | Checks |
|---|---|---|
| `6a8126e4` | Step 7: merge #931 `d06ded5a` (head checked), the ledger by `own_point` as ruled (decision 1) | quick checks: all pass but `py_idiom` (fixed next) and the all-points flip check (the base's same eleven 8x8/2if findings); `test_ctrl_memory` PASS; `plat_ledger` PASS, 9 of 9 controls; the fixture 60.0 in all six arms. Shards: 0 FAIL (Phy.B12 only, at both interface counts: F4, the subject of decision 2), 1: 792 of 793 (the one escape is the plant into that failing B12 check), 2 PASS, 3 PASS |
| `b1af3b54` | Idiom gate: five SET_STREAM_INFO defects to `aecp_stream_info_mutants.py` in place (table identical, 361); three docstring items of `test_ctrl_memory.py` rewrapped | `py_idiom` PASS; `test_ctrl_memory` PASS |
| `03c92617` | THE STEP by decision 2; B12's two assertions, L5 and L6, four plants; ratchet by `fw_coverage.py --write` | quick checks: all pass but `py_idiom` (two lines, fixed next) and the flip check (base's eleven); `fw_coverage --check` PASS. Shards: 0 PASS, 2 PASS, 3 PASS; 1: 796 of 797, the escape a plant that did not build (fixed at `6ad5c259`) |
| `45708d9e`, `afbbde54` | Idiom gate: two plant rows rewrapped; the four new plants in their own function, spliced in place (table identical, 121) | `py_idiom` PASS |
| `31304b74` | Step 8: merge #932 `0fdfdba7` (head checked) | `test_ctrl_memory` PASS; `plat_ledger` PASS, 9 of 9; the fixture 60.0 in all six arms. The plain gate: the two Listener-copy suites fail one oracle check (below) |
| `eafe4a16` | Composition fix: #930's Listener-copy oracle with #925's declaration rule; ratchet regenerated | coverage-mode gate PASS; quick checks: all pass but the flip check (base's eleven); 1x1/1if flip check PASS (last 137.89 of 140 on the current statements); `fw_coverage --check` PASS. Shards: 0 PASS, 2 PASS, 3 PASS; 1 stopped by PID, superseded at the tip |
| `6ad5c259` | THE STEP's extra-step plant builds: its condition keeps `owes()` referenced | the plant alone (`--slice 614/797`): caught; shard 1 at the tip: **797 of 797 caught, PASS** |

Every conflicted file has a row in RESOLUTIONS.md. Round 1's rule holds for figures: each restated from the composed
tree by its tool at the step; ROM ledger entries at their measured tiles.

## Decision 1: the ledger by `own_point`

`product_point`, `Ledgered.product`, #933's refusals of the two 8x8 two-interface images (in `product_facts`, the SoC
build's rows, section 3) and its flag plants are removed as ruled. **The ruling names two flag plants; #933 had three**
("the platform's two-interface entry a product entry", "the size fixture's entry a product entry", and "the platform's
one-interface entry not a product entry"). The third sets the same removed field, so it cannot exist without it; the
one-interface image's planning stays held by #931's facts and plants. #933's four `product_point` mutants and their
property go with their target; #931's three `own_point` mutants hold the same defects for `own_point`. Kept: the
unledgered refusal past 56 and every other test and plant of both PRs (the product image refused half a tile past and
with another `ctrl_plat`; both unlinked-override controls of `plat_ledger.py`). `ctrl_plat_image.py`'s link without
`--ledgered-point` follows the product build, by `own_point`.

The entries are the measured tiles (S14 debt by the owner's rule of 2026-11-15; not a STOP):

| Entry | Round 1 tip (stated / measured) | Step 7 | Step 8 (the tip) | Refused at |
|---|---|---|---|---|
| `8x8-two-interfaces` (the size fixture) | 59.5 / - | 60.0 (rom 129,920 to 130,424 B) | 60.0 (rom 130,472 to 130,968 B, 104 B left in the worst arm) | 60.5 |
| `platform-8x8-two-interfaces` | 61.0 / 61.5 | 62.0, `ctrl_plat` 20,672 B | 62.5, `ctrl_plat` 21,504 B, `sram` a 57th granule | 63.0 |
| `platform-8x8-one-interface` | 56.5 / 57.0 | 57.5, `ctrl_plat` 18,496 B | 57.5, `ctrl_plat` 18,944 B, 232 B of `rom` left | 58.0 |

The round-1 tip's own `plat_ledger` run fails on round 1's provisional figures (its images measured 61.5 and 57.0,
`ctrl_plat` 17,856 / 19,392 / 18,496 / 20,672 B); step 7 restates them. The 1x1 points stay within 56 (44.5, 45.5).
**Watch at the final head**: the fixture has 104 B of `rom` left in 60.0 (answering-ports arm), so #934's or #936's
growth may take it to 60.5; by the rule that is debt, not a STOP. The physical fit and timing floor are checked at the
final head; no RTL, gateware or submodule changed this round.

## Decision 2: THE STEP

Implemented as ruled (RESOLUTIONS.md has the files): `nvm_store_owed()`; with no centisecond step owed an owed PHY
frame takes the call and the store takes no extra step there; the centisecond's step keeps its first place; never a
save's step and a frame in one call. The saves' stated worst cases are not restated. B12 keeps every assertion and
gains the two ruled ones; L5 (a save spanning four poll periods: a loss and a return each published within one period)
and L6 (a probe that always misses: the save durable within its stated slowest pace, (CTRL_LOOP_STEP_AGE + 1)
centiseconds a step). **Four plants, not two**: the two ruled ones (a frame yielding to the extra step, caught by L5; a
frame beside the extra step, caught by B12's step-count assertion), and two more because every test of
`test_plat_boot.cpp` must be named by a plant (`plat_mutants.SOURCES`: L6's) and B12's second new assertion must be
shown to fail. The control campaign is 797 (793 + 4). The size fixture, which the CPU budget harness builds, links no
PHY and drops `nvm_store_owed` at link, so its image at `03c92617` is byte-identical to step 7's: no CPU budget row
moves, as the ruling expected.

## Step 8's composition fix

#930's `srp_listeners.cpp` holds each settled step of the copied run to a registrar walk, its expected declaration by
the rule before #925 (Failed whenever both kinds are registered). With #925's ruled rule (the latest registered kind
decides) both Listener-copy suites failed that one check at 1x1/1if and 8x8/1if, while the copied-against-reference
differential passed: the behaviours agree, the oracle was stale. It now takes the expected declaration by #925's rule
from the walked kinds and the sink's `latest_kind`. No design question: #925's rule is ruled, #930's equality is
unchanged.

## Decision 3: attribution (not a cut)

Measured at 1x1/1if, arm A's `aecp-largest-notice`, `acmp-notk` and `datapath-events` and the answering-every-port
arm's `notice-burst-5`, `notice-burst-7` and `notice-every-7` (round 1's probe: where the record and the four events
were dearest), built as `run.py` builds by default, at every step head, the THE STEP commit and #931 alone. Committed
instructions come from a scratch-only aid (`attribution/patch_sim.py`: a side file per run, the log byte-for-byte
unchanged). It is cycle-neutral: #931's head built without it gives the same 21 record spans, cycle for cycle
(receipts/attribution/out/neutrality.txt), and its 92,489 cycles are #931's own figure for arm A. Cells are cycles /
committed instructions (by the rule, us; **bold** over the statement the composition carries: the long record 975 us,
event.AECP 75, event.MAAP 165, the datapath events 35). "Image" is arm A's ELF sha256.

| Head | Step | Image | Largest record: cycles / instr (us) | CPI | Its pass: rom refills / fetch wait | event.AECP | event.MAAP | AS_PATH_CHANGED | AVB_INFO_CHANGED |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| `cb96336d` | dev-soft-core | `554b04f7` | 86,499 / 20,774 (910) | 4.164 | 289 / 24,125 | 7,005 / 1,053 (75) | 13,887 / 2,751 (150) | 2,792 / 362 (30) | 3,002 / 366 (35) |
| `43b954e6` | 1: #881 | `c508959a` | 84,769 / 20,770 (895) | 4.081 | 304 / 25,127 | 6,331 / 1,025 (70) | 15,591 / 2,751 (165) | 2,863 / 362 (35) | 3,261 / 366 (35) |
| `877c99e4` | 2: #914 | `81c58dbc` | 84,976 / 20,770 (895) | 4.091 | 269 / 21,957 | 6,629 / 1,048 (70) | 14,995 / 2,751 (160) | 3,185 / 362 (35) | 3,387 / 366 (**40**) |
| `9c0e1974` | 3: #918 | `81c58dbc` | 84,976 / 20,770 (895) | 4.091 | 269 / 21,957 | 6,629 / 1,048 (70) | 14,995 / 2,751 (160) | 3,185 / 362 (35) | 3,387 / 366 (**40**) |
| `22a82038` | 4: #935 | `81c58dbc` | 84,976 / 20,770 (895) | 4.091 | 269 / 21,957 | 6,629 / 1,048 (70) | 14,995 / 2,751 (160) | 3,185 / 362 (35) | 3,387 / 366 (**40**) |
| `2078c438` | 5: #933 | `81c58dbc` | 84,976 / 20,770 (895) | 4.091 | 269 / 21,957 | 6,629 / 1,048 (70) | 14,995 / 2,751 (160) | 3,185 / 362 (35) | 3,387 / 366 (**40**) |
| `7c28f53f` | 6: #938 | `271ed3df` | 107,445 / 20,775 (**1130**) | 5.172 | 307 / 25,227 | 7,696 / 1,054 (**85**) | 15,737 / 2,751 (**170**) | 3,325 / 362 (35) | 3,602 / 366 (**40**) |
| `6a8126e4` | 7: #931 | `cac9c105` | 99,468 / 22,208 (**1045**) | 4.479 | 335 / 28,222 | 7,519 / 1,048 (**80**) | 15,744 / 2,751 (**170**) | 3,571 / 362 (**40**) | 3,480 / 366 (**40**) |
| `03c92617` | THE STEP | `cac9c105` | 99,468 / 22,208 (**1045**) | 4.479 | 335 / 28,222 | 7,519 / 1,048 (**80**) | 15,744 / 2,751 (**170**) | 3,571 / 362 (**40**) | 3,480 / 366 (**40**) |
| `eafe4a16` | 8: #932 | `0af211aa` | 95,392 / 22,202 (**1005**) | 4.297 | 314 / 26,562 | 6,125 / 1,025 (65) | 13,679 / 2,751 (145) | 2,681 / 362 (30) | 3,130 / 366 (35) |
| `d06ded5a` | #931 alone | `600cc8cf` | 92,489 / 22,192 (975) | 4.168 | 310 / 25,742 | 5,873 / 1,036 (65) | 13,685 / 2,751 (145) | 3,131 / 362 (35) | 3,183 / 366 (35) |

Where each event was dearest: AS_PATH_CHANGED none/datapath-events; AVB_INFO_CHANGED none/datapath-events; event.AECP
aep/notice-burst-5, aep/notice-burst-7; event.MAAP aep/notice-burst-5, none/acmp-notk

Findings:

- **Instructions are flat; cycles follow placement.** The largest record commits 20,770 to 20,775 instructions from
  the base to step 6 and 22,202 to 22,208 from step 7. Its cycles go 86,499, 84,769, then 84,976 at steps 2 to 5 (one
  image), **107,445 at step 6 for 20,775 instructions** (CPI 5.17), 99,468 at step 7 and 95,392 at step 8. The four
  events commit nearly the same instructions at every head (event.AECP 1,025 to 1,054, event.MAAP 2,751,
  AS_PATH_CHANGED 362, AVB_INFO_CHANGED 366) within 29 of each other, while their cycles move by up to a third
  (AS_PATH_CHANGED 2,681 to 3,571).
- **The one work increase is #923's commit**: +1,433 instructions on the record at step 7 (+1,418 at #931 alone),
  about 6,200 cycles at the record's CPI. Steps 1, 2, 6 and 8 each move every figure in the table with at most 28
  instructions' change on these paths; steps 3 to 5 and the THE STEP commit leave arm A's image byte-identical.
- **At step 8, the tip's image, the four events are within their statements** (event.AECP 65 us of 75, event.MAAP
  145 of 165, the datapath events 30 and 35 of 35). **Only the largest record is over: 95,392 cycles, 1,005 us by the
  rule against 975**, 2,535 cycles past the 92,857 that 975 holds. Graded with that figure alone on a scratch copy
  (receipts/attribution/out/flip-1x1-step8-long-record-1005.*), one 1x1/1if row goes over, **txL 49.07 ms against
  49**; the last queued notice is 137.89 ms (140) and ACMP 29.91 (30). Round 1's three over rows came from the probe's
  five restatements (step 7's image, reproduced here exactly).
- `ctrl_split.ld` and `ctrl_split_hot.txt` are unchanged by every frozen head (`git diff cb96336d <head>` empty for
  all eight), so the hot list orders a code base that has moved under it. The pass carrying the record refills 307 to
  335 rom lines at steps 6 to 8 against 269 at steps 2 to 5.
- So placement decides these rows. The ruling's second cut, the hot list relearned from traces by its recorded
  procedure, addresses it directly; the first, less work in the record path, has #923's 1,433 instructions to work
  on, about 2.4 times the 2,535-cycle excess at step 8. Every figure is still the final head's, after #934 and #936,
  as ruled: the probe decides nothing.

## STOP conditions

None met. Firmware failures this round were each resolved as a composition fix: the known B12 failure (decision 2,
`03c92617`), the Listener-copy oracle (`eafe4a16`), and a plant of mine that did not build (`6ad5c259`). No fit or
timing-floor check was due this round. The ledger's rises are S14 debt by rule. No design decision is open; the
three-versus-two flag plants and the four-versus-two THE STEP plants are reported above as consequences, not choices.

## Notes

- 8x8/1if's one-row edit with #923's commit is unmeasured (`edit_rows.PACED['8x8/1if']` keeps #914's 335), owed at the
  final head with every figure.
- The all-points flip check fails only on the base's eleven 8x8/2if findings at every head (receipts compare them).
- `git rerere` recorded step 7's and step 8's resolutions late, at the next commit; a replay would carry
  `test_ctrl_memory.py`'s rewrapped docstring with step 7.
- Units' CPU pins did not hold (the host resets task affinity; every process showed 0-95), so each was re-pinned from
  its booking (`bin/repin.sh`); the host ran oversubscribed, which slows wall time and moves no simulated cycle.
- Receipts are under `receipts/`, indexed in INDEX.md; files over 200 KB are stubs with their size and sha256.
