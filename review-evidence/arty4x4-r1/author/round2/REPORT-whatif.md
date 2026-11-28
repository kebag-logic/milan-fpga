# Arty split: desk what-ifs by the unchanged rule (round 2)

[A863]. Desk only: no new firmware, no route, no commit to the product path. Branch `arty-4x4-1127` stays at round 1's head `11f903bd4`.
Every number below comes from round 1's census and round 9's 1x1 census, through the rule as it stands: costs are measured cycles plus 5 %, rounded up to 5 us, and the row search is the slice, pace and queued-notice rules with the owner bounds.
Owner bounds: load 0.70, ACMP 30 ms, txL 49 ms, last notice 140 ms, THE SHARE 2 ms.

## Method

`tools/whatif.py` generalises round 1's `derive4.py` (round 9's `derive-own.py`).
- **Inputs.** It takes measured cycles per stated cost and the retry fit's cycles (cold start, refused attempt, notice).
  - N = 1 is **measured**: round 9's merged 1x1 census at `aa53840d9`, the maxima the installed 1x1 row was derived from.
  - N = 4 is **measured**: this lane's 4x4 census at the same base, 159 cases.
  - N = 2 and 3 are **interpolated**, linearly in N between the two, cost by cost.
  - Both measured sets apply #969's disposition, as at every point.
- **Counts.** The shape's counts are exact for each N: N AAF each way, the CRF input, and the CRF output once N >= 2 (Milan v1.2 7.2.3). Counter descriptors are sources + sinks + 2. `AECP_NOTICES_MOST` is evaluated from `aecp.h` at those descriptor counts.

| Shape | Sources / sinks | Counter descriptors | Notices |
|---|---|---:|---:|
| 1x1 | 1 / 2 | 5 | 10 |
| 2x2 | 3 / 3 | 8 | 16 |
| 3x3 | 4 / 4 | 10 | 20 |
| 4x4 | 5 / 5 | 12 | 24 |

- **The clock** scales time only: cycles are unchanged and each cost is restated by the rule at that clock. That is the owner's stated assumption. It is optimistic for work that waits on the 50 MHz datapath or on the flash, whose waits in CPU cycles grow with a faster CPU; no census at 100 MHz exists.
- **Every cost table** the row model reads is the what-if's: the load column, the poll items, the datapath events, the long record and notice, LINK and the paced class. No other point's costs enter.
- **Validation.** The tool reproduces both measured derivations exactly:
  - 1x1 at 80 MHz: round 9's installed row, (queued 125 ms, pace 10 ms, slice 1250 us), load 0.5014, ACMP 29.84, txL 48.90, last 117.58 ms.
  - 4x4 at 80 MHz: round 1's NO QUALIFIED MODEL, load 0.5781, least ACMP 37.39, txL 58.71, last 201.93 ms.

## 1. 2x2/1if and 3x3/1if at 80 MHz

| Shape | Costs | Rows that qualify | Best row (queued, pace, slice) | ACMP, ms | txL, ms | last, ms | Load | THE SHARE, ms |
|---|---|---:|---|---:|---:|---:|---:|---:|
| 1x1 | measured | 2 | 125, 10, 1250 | 29.84 | 48.90 | 117.58 | 0.501 | 1.794 |
| **2x2** | interpolated | **0** | 140, 12, 1050 (nearest) | 34.10 | 53.23 | 147.01 | 0.527 | 1.828 |
| **3x3** | interpolated | **0** | 125, 13, 1150 (nearest) | 36.02 | 56.87 | 172.72 | 0.553 | 1.862 |
| 4x4 | measured | 0 | 125, 13, 1200 (nearest) | 37.39 | 58.71 | 201.93 | 0.578 | 1.897 |

The interpolated shapes rest on an assumption, so they are bounded by giving every cost one endpoint's measurement at that shape's own counts:

| Shape at 80 MHz | Every cost at the 1x1's | Every cost at the 4x4's |
|---|---|---|
| 2x2 | **row**: ACMP 29.77, txL 48.46, last 135.08 ms | no row: least ACMP 36.79, txL 58.11 |
| 3x3 | no row: nearest ACMP 29.99, txL 48.73, last 137.84, but the pace and queued rules do not agree | no row: least ACMP 37.10, txL 58.41 |

**Reading.** At 80 MHz the per-stream costs decide it, not the counts.
- 2x2 has a row only if its costs stay within a few percent of the 1x1's, and even then with 0.23 ms of ACMP margin.
- At the linear interpolation it has none (ACMP 34.1 ms). Neither 3x3 nor 4x4 has one under any of the three cost assumptions.
- 2x2 at 80 MHz is undecided by the desk: only a 2x2 census decides it, and the desk expects a miss.

## 2. At a 100 MHz control CPU clock

| Shape | Costs | Rows that qualify | Rule's row (queued, pace, slice) | ACMP, ms | txL, ms | last, ms | Load | THE SHARE, ms |
|---|---|---:|---|---:|---:|---:|---:|---:|
| 1x1 | measured | 1 | 125, 3, 550 | 23.47 | 48.33 | 97.15 | 0.399 | 1.435 |
| 2x2 | interpolated | 1 | 125, 4, 600 | 24.21 | 45.61 | 112.35 | 0.424 | 1.462 |
| 3x3 | interpolated | 3 | 125, 4, 900 | 25.79 | 48.97 | 113.85 | 0.443 | 1.490 |
| **4x4** | measured | **1** | **125, 5, 1250** | **27.07** | **47.00** | **113.60** | **0.463** | **1.517** |

The bounds agree:
- 2x2 has a row at 100 MHz with every cost at the 1x1's (ACMP 23.10, txL 48.75) and at the 4x4's (ACMP 26.26, txL 46.19).
- So does 3x3: ACMP 23.31 / txL 48.97 with the 1x1's costs, ACMP 26.70 / txL 46.63 with the 4x4's.

**4x4 at 100 MHz:** one row meets every owner bound, with 2.9 ms of ACMP margin, 2.0 ms of txL, 26 ms of last notice, load 0.46 and THE SHARE at 1.52 ms. Only one candidate of 52 qualifies, and its txL margin is 4 %.
That row stands on "cycles unchanged". A 100 MHz census would have to confirm it before it is a row.

### Could the Arty split close timing at 100 MHz?

From round 1's three routes of the 4x4 image at 80 MHz (read, not re-routed). The sys domain (`clkout0`: the CPU, the bus and the mailbox, 12.5 ns) is the one 100 MHz tightens to 10.0 ns.

| Directive | sys WNS at 80 MHz | The five worst sys endpoints | Sixth-worst listed sys endpoint |
|---|---:|---|---:|
| ExtraPostPlacementOpt | +0.486 ns | VexiiRiscv DMA read-bridge aligner to the DMA bus pipe: 10 levels, 11.70 ns, 82 % routing | +2.518 ns |
| ExtraTimingOpt | +0.126 ns | Reset fan-out from one synchroniser (`FDPE_1`) into `KL_mbx`, `KL_mbx_cdc` and the SPI PHY's R pins, 0 levels | +4.507 ns |
| AltSpreadLogic_high | +0.065 ns | Reset fan-out into `KL_mbx_dma`'s buffer R pins, 0 levels | +4.243 ns |

- Every sys-to-datapath path is constrained as asynchronous; the inter-clock table times none. So a faster sys does not tighten the 50 MHz crossings.
- 100 MHz needs about 2.5 ns more on every sys path. In each placement only about five endpoints are short, a different family each time. Beyond them the reported sys slack is +2.5 ns (one directive) to +4.2 to +4.5 ns (two), and Vivado stops improving a path once it meets 12.5 ns.
- Against it:
  - The part is the -1 speed grade.
  - The 4x4 image fills 94 to 97 % of its slices.
  - The ExtraPostPlacementOpt family is a routing-dominated path inside the CPU.
  - #878's history: 100 MHz first missed (-0.822 ns, all `KL_mbx` on the bus clock). After S9's `KL_mbx` registration fix it met the floor at 1x1 (+0.378 ns). But the split CPU then ran on the 50 MHz datapath clock, not on sys; it has moved to sys since, so that pass does not cover the CPU.
- **Plausible, not shown.** The listed paths need only reset replication and one CPU path to improve by about 2.4 ns, but the occupancy and the -1 grade make a pass uncertain. A 100 MHz route of the 4x4 image at the three directives would decide it.
- The clock plan allows it: 100 MHz divides the same 800 MHz VCO exactly by 8, so the exact-divider contract (`margin=0`) holds.
- The latency pair would need re-measuring at 100 MHz. #878 read a sum of 1,465 ns at a 100 MHz system clock against the tracked 1,509 ns at 80 MHz, because two of its ingress terms cross into sys.

## 3. 4x4 at 80 MHz: the cut a row needs

`tools/cuts.py`, applied to measured cycles; each cost is then restated by the rule at 80 MHz.

**A uniform cut of every measured cost: 13.9 %** (bisection to 0.25 %: every cost at 86.13 % of its cycles gives a row, at 86.38 % none). For comparison, 100 MHz with cycles unchanged is a 20 % cut of every time, which is why section 2 clears.

**The smallest set found: three costs** (a greedy search, 5 % steps, each step the cut that most narrows the gap to a qualifying row):

| Stated cost | Now, us | Needed, us | Cut, us | Cut |
|---|---:|---:|---:|---:|
| Ordinary AECP record (`record.aecp`) | 275 | 150 | 125 | 45 % |
| SRP record (`record.srp`, also the retained SRP item) | 375 | 280 | 95 | 25 % |
| Polls' base (`base`) | 290 | 215 | 75 | 25 % |

With those cuts, the rule's row is queued 140 ms, pace 10 ms, slice 1200 us: ACMP 28.57 ms, txL 48.78 ms, last notice 135.56 ms, load 0.496.
THE SHARE is kept at the measured 1.897 ms: a cut would shorten passes, so it can only fall.

The set is the greedy's and has not been shown minimal. Two checks bound it:
- **One cost alone:** cutting any one of the 13 most relevant costs by 50 % leaves no row.
- **Two costs:** no pair of them, each cut by 50 %, leaves a row either.
  - The closest pair is the ordinary AECP record with the SRP record: every owner bound is within reach, but no candidate satisfies the pace and queued rules together.
  - The 13: ordinary, paced and long AECP records, the paced SET_CONFIGURATION, SRP and ACMP records, the ACMP timer event, centisecond work, polls' base, one MRPDU build, the AECP item, the AECP notice and the retry notice (`receipts/pairs-4x4-80.txt`).

**Where the time goes.** These are the largest terms of the two rows at the rule's nearest candidate (125 ms, 13 ms, 1200 us):
- ACMP, 37.39 ms: passes 6.37, AECP records 6.33, ACMP's own 4.24, timers 4.07, AECP items 3.33.
- txL, 58.71 ms: AECP records 11.78, other channels' records 10.47, AECP items 10.14, passes 8.71, timers 4.96.

The same rows at the 1x1 are 29.84 and 48.90 ms. The four extra streams of each kind add their records, timers and notices through every term rather than through one.

## Per-stream costs, measured and interpolated

At 80 MHz, us by the rule; the 100 MHz column for 4x4 is the same cycles restated (cycles unchanged).

| Cost | 1x1 (measured) | 2x2 (interpolated) | 3x3 (interpolated) | 4x4 (measured) | 4x4 at 100 MHz |
|---|---:|---:|---:|---:|---:|
| `record.srp` | 300 | 325 | 350 | 375 | 300 |
| `record.aecp` | 290 | 285 | 280 | 275 | 220 |
| `record.aecp.paced` | 335 | 395 | 460 | 520 | 415 |
| `record.aecp.long` | 1105 | 1120 | 1130 | 1145 | 915 |
| `record.acmp` | 245 | 255 | 260 | 265 | 215 |
| `record.adp` | 125 | 130 | 135 | 140 | 110 |
| `record.maap` | 125 | 135 | 145 | 150 | 120 |
| `event.ACMP` | 175 | 185 | 195 | 205 | 165 |
| `event.MAAP` | 165 | 175 | 180 | 190 | 155 |
| `event.ADP` | 95 | 95 | 95 | 95 | 75 |
| `event.AECP` | 85 | 90 | 95 | 100 | 80 |
| `event.LINK` | 205 | 220 | 235 | 250 | 200 |
| `centisecond` | 160 | 185 | 215 | 245 | 200 |
| `base` | 235 | 255 | 270 | 290 | 230 |
| `build` | 1035 | 1030 | 1030 | 1025 | 820 |
| `build_one` | 660 | 690 | 720 | 750 | 600 |
| `step` | 1060 | 1060 | 1060 | 1060 | 850 |
| `item.aecp` | 200 | 190 | 185 | 175 | 140 |
| `item.aecp_long` | 385 | 385 | 390 | 390 | 315 |
| `item.acmp` | 60 | 65 | 70 | 75 | 60 |
| `item.withdraw` | 95 | 105 | 115 | 125 | 100 |
| `item.rebuild` | 255 | 250 | 245 | 240 | 190 |
| `tx.aecp.notice` | 205 | 205 | 200 | 200 | 160 |
| `tx.aecp.response` | 50 | 50 | 55 | 55 | 45 |
| `events_none` | 40 | 40 | 40 | 45 | 35 |
| `event.TICK` | 50 | 50 | 45 | 45 | 40 |
| `event.GM` | 40 | 40 | 45 | 45 | 35 |
| retry cold | 130 | 135 | 145 | 150 | 120 |
| retry attempt | 30 | 30 | 30 | 30 | 25 |
| retry notice | 230 | 230 | 230 | 235 | 185 |

The costs that grow most from 1x1 to 4x4, in measured cycles:
- the paced AECP record (an accepted SET_CONFIGURATION), +60 %;
- centisecond work, +58 %;
- the registrar walk item, +64 %;
- one MRPDU build, +39 %;
- the polls' base, +31 %;
- the SRP record, +28 %.
A few shrink slightly (the ordinary AECP record, the AECP item, the rebuild). That is measurement spread between two images, and the interpolation keeps it.

## Recorded

- **Milan v1.2 5.4.2.7.** SET_STREAM_FORMAT may refuse only with STREAM_IS_RUNNING, or BAD_ARGUMENTS when mapped channels would vanish. "In all other cases a PAAD-AE shall return SUCCESS." A bandwidth refusal of an advertised format is not available.
  So formats that do not fit the 100 Mb/s class-A limit four-up are **left out of the advertised set, not refused**. The 4x4 image advertises 2-channel 48 kHz Stream Outputs, the 48 kHz family on Stream Inputs, and no 96 or 192 kHz Stream Input format.
  At 2x2 or 3x3 the same rule would admit more: two or three 8-channel 96 kHz inputs fit the limit, where four do not. This what-if does not re-derive those envelopes.
- **Latency pair.** The 4x4 configuration carries the board's 1409/100 ns pair. The builder suite registers it as the board's measured 1,509 ns sum (#829), which was measured on the 1x1 image at 80 MHz, not on the 4x4. The PHY, MII path and clock are the same. At 100 MHz the pair needs a new measurement (above).

## Files

- `tools/whatif.py`, `tools/cuts.py` (copies in `receipts/tools/`).
- `receipts/`: the eight shape and clock results, the eight bound runs, and the cut search.
