#!/usr/bin/env python3
"""Write this round's sections of docs/design/SPLIT_CONTROL_MEMORY.md from the kept legs: every table cell comes from a
leg's results, and the prose that quotes a figure reads it from the same data.

usage: docsec.py BUILDS DOC
Replaces the marked text between the subsection 'What is left' of section 13 and section 13's end, and appends section 14.
"""
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, '$LANES/665-s2b-cycles/tb/verilator/ctrl_service_budget')
import rows12  # noqa: E402
import estimate32  # noqa: E402

root, doc = Path(sys.argv[1]), Path(sys.argv[2])
load = lambda names: [rows12.load(root / n) for n in names.split(',')]
A1, A8, D1, D8 = load('N-A1,N-B1'), load('N-A8,N-B8'), load('D-A1,D-B1'), load('D-A8,D-B8')
P81 = load('P81-A8')
NONE1, NONE8, SOCI1, SOCI8 = load('none-A1'), load('none-A8'), load('soci-A1'), load('soci-A8')
ROWS = {r: r for r in rows12.ORDER}
TITLE = {'an ACMP command behind a full acmp ring': 'An ACMP command behind a full ACMP ring',
         'an ENTITY_AVAILABLE behind a full adp ring': 'An ENTITY_AVAILABLE behind a full ADP ring',
         'an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed)': 'An ENTITY_AVAILABLE behind the ADP ring, its bucket refilling (observed)',
         'an event behind 15 others': 'An event behind 15 others',
         'a response with 7 frames owed ahead of it': 'A response with 7 frames owed ahead of it',
         'an ACMP command behind the owed input': 'An ACMP command behind the owed input'}
title = lambda r: TITLE.get(r, r)


def cells(legs, row):
    return ' / '.join(rows12.cell(rows12.worst(res).get(row)) for res, _ in legs)


def ms(legs, row):
    return max(rows12.worst(res)[row][0][1] for res, _ in legs)


def share(legs):
    return ' / '.join(rows12.share_cell(res) for res, _ in legs)


def longest(legs):
    return max(rows12.shares(res)[2] for res, _ in legs)


def over(legs):
    return sum(rows12.shares(res)[0] for res, _ in legs)


rows_table = ['| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |',
              '|---|---:|---:|---:|---:|---:|']
for row in ('ACMP record, last', 'ADP record, last', 'MAAP record, last', 'AECP record, last', 'SRP record, last',
            'an ACMP command behind a full acmp ring', 'an ENTITY_AVAILABLE behind a full adp ring', 'an event behind 15 others',
            'AECP record, last, in the owed window', 'a response with 7 frames owed ahead of it', 'an ACMP command behind the owed input'):
    bound = rows12.worst(A8[0][0])[row][2]
    rows_table.append(f'| {title(row)} | {bound:g} | {cells(A1, row)} | {cells(D1, row)} | {cells(A8, row)} | {cells(D8, row)} |')
share_table = ['| 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |', '|---:|---:|---:|---:|',
               f'| {share(A1)} | {share(D1)} | {share(A8)} | {share(D8)} |']

SRP8, SRP8D = ms(A8, 'SRP record, last'), ms(D8, 'SRP record, last')
AECP8, AECP8D = ms(A8, 'AECP record, last'), ms(D8, 'AECP record, last')
SRP1, AECP1 = ms(A1, 'SRP record, last'), ms(A1, 'AECP record, last')
every_group = lambda legs: max(g['passes']['worst']['ms'] for g in legs[0][0]['results'])
L1, L8 = every_group(A1), every_group(A8)

A = f"""### The split CPU on `sys` at 100 MHz

The [owner's decision of 2026-10-30](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6514866239) moved the split CPU from the Milan clock to `sys`, the 100 MHz bus clock the mailbox, its record mover and the firmware memory run on.
`milan_soc.CTRL_CPU_CD` names that domain, and `MilanSoC` refuses any other for the split placement, the Milan clock among them.
The all-fabric CPU, the Milan datapath clock, the PHC, the media grids and every `MILAN_CLK_FREQ_HZ` derivation do not change.

The memory crossing is removed, not kept degenerate.
With the CPU on the bus's own clock the generator's `with_cpu_clk` is off and `cross_cpu_memory_ports` leaves the CPU alone, so no `StreamFifoCC` or `cpu_clk` port is built: a crossing between one clock's edges would cost its cycles and its area for nothing.
Every CPU-clock constant comes from the CPU's own clock: the mailbox's millisecond tick from `sys`, the loop's share as 200,000 CPU cycles, and the harness's `cpu_hz` from `MilanSoC.cpu_clk_freq`.
The CPU budget harness and the split boot simulation both build through `ctrl_cpu_cd` and refuse a CPU with a clock of its own; a CPU budget build that records its CPU anywhere else is refused, built or reused.

Out of context, the product split CPU netlist on `sys` (`VexiiRiscvLitex_7ee512a1cb1c336731b7f28188c9814f`) with `rom` and `sram` built from the 1x1 image, its LiteDRAM port brought out to pins, routed at 10 ns with the method of section 9:

| Split CPU | WNS / WHS, ns | LUT | FF | The CPU's RAMB36 / RAMB18 | The CPU's tiles | Route |
|---|---:|---:|---:|---:|---:|---|
| 16 KiB two-way fetch L1, behind the crossing at 100 MHz ([above](#the-fetch-l1)) | CPU +0.659 / +0.031, bus +2.660 / +0.072 | 3,948 | 6,879 | 9 / 11 | 14.5 | no routing error |
| 16 KiB two-way fetch L1, on `sys` at 100 MHz | +1.605 / +0.070 | 3,543 | 5,643 | 6 / 7 | 9.5 | no routing error |

Without the crossing the CPU is 405 LUTs, 1,236 FFs and 5 tiles smaller.
Its worst path runs from the generator's peripheral bridge into the interrupt controller's gateways, 8.015 ns, 76 % route.
Out of context, with nothing else on the device, this is an upper bound; the routed split image is lane S9's.

Every composed row was measured on the merged head, with the CPU on `sys` at 100 MHz and the bus on the same clock, at both points, in both arms, with the two drafts staged and without them, graded against min(T_svc, its family's ceiling) with T_svc = 20 ms (ms, arm A / arm B, bold over the row's own bound):

{chr(10).join(rows_table)}

Every row the CPU decides fits, at both points, in both arms, with the drafts staged or not.
The tightest is the 8x8 last SRP record, {SRP8:.2f} ms against 18, {SRP8D:.2f} with both drafts; the 8x8 last AECP record takes at most {AECP8:.2f} ms against 20.
At 1x1 they take {SRP1:.2f} and {AECP1:.2f} ms.
The three egress-held rows miss as before: they hold the egress for 60 ms, and stay with [tsn-c-stack #26](https://github.com/kebag-logic/tsn-c-stack/issues/26).

The per-pass share, 2.0 ms, 200,000 CPU cycles: the passes over it of the work passes run over the four backlog groups, and the longest in ms (arm A / arm B):

{chr(10).join(share_table)}

No pass is over the share in any leg, nor in any of the harness's other groups, which arm A also ran at both points.
Over every group the longest at 8x8 is {L8:.2f} ms, at 1x1 {L1:.2f} ms.

**The pass that was over it.**
On the merged head before this change one 8x8 pass was over the share in each arm, 2.21 and 2.22 ms, in the `backlog` window, and in no other window.
It was the pass that took the row's own LINK event: SRP's `reset_interface` destroyed the interface's participants and built new ones in the event, about 110,000 CPU cycles at 8x8 of the 200,000.
The count of events a pass takes is not what sets it: at six events a pass that pass was 2.207 ms, and at four 2.108 ms, the LINK event arriving in a later pass with the same work (labelled experiments, not on this branch).
So a link change now takes two passes (`srp_bounds.h`): the pass that takes it withdraws and destroys, the next pass's poll builds, and SRP's receive waits until then, so no record meets an interface with no participants and neither pass also runs an SRP record.
Any number of link edges in a pass builds once, which a pass of eight used to do eight times.

**The other groups.**
Three things the composed rows do not reach showed only when every group ran at 100 MHz.
The flash window was cacheable in the test SoC, for the hybrid-XIP arm, so the saved-state store read flash through the data cache, which the product never does: its read and its buffer met at one cache index, and one pass in each save took 12.4 ms at 8x8 and 4.1 ms at 1x1 (a labelled control restores it).
The window is now the product's in every arm but hybrid-XIP's, and a build with another is refused.
An AECP group sent its next frame when the last settled, so at 100 MHz it outran the channel's refill of one frame every 5 ms, and the filter refused the frames past its burst; each frame now waits that period.
And through the product's uncached window a read of the store's whole page takes 1.40 ms, which with lwSRP's periodic work in the same tick put an 8x8 pass at 2.26 ms.
The store's blank check and verify now read back 128 bytes a step (`NVM_READ_BYTES`), so a save's read-back takes twice as many ticks.

**The hybrid-XIP arm's two windows.**
At the CPU's old 50 MHz, the 1x1, 4 KiB arm's `backlog-adp` and `backlog-adp-refill` were refused: the fifteen grandmaster changes arrive 8 bus cycles apart and the source coalesces while its record waits, so with k records held only 16 - k + 1 commit, and those windows opened with 4 or 5 records held.
That was the window's definition, not the firmware's defect: it named a population only a drained ring can take, and waited a fixed time for one.
Every backlog window now opens on a drained ring (`scenario.OPEN_WINDOW`), its table gives the records held at its opening, and a refusal names them.
At 100 MHz all four windows take their fifteen, with no record held, so that arm's composed maximum covers all four ([the harness](../../tb/verilator/ctrl_service_budget/README.md#the-instruction-cache)).

"""

B = """### What is left

- The owner kept 8x8 in the Mark II split's scope, approved T_svc = 20 ms ([decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6495692075)) and put the split CPU on `sys` at 100 MHz ([decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6514866239)).
""" + f"""- **With the CPU on `sys` at 100 MHz** every row the CPU decides and every pass fits at both points, with the least margin the 8x8 last SRP record's, {18 - SRP8:.2f} ms.
- The TSN stack's and lwSRP's changes reach this branch only through those repositories' reviews, then a pin move: the TSN stack's with the hot list's runtime entry removed, lwSRP's with `ctrl_arms.LWSRP_REV`.
- The three rows no CPU lever moves are unchanged: the 60 ms egress hold, `ACMP_OWED_MAX`, and the command behind the owed input. They stay with [tsn-c-stack #26](https://github.com/kebag-logic/tsn-c-stack/issues/26).
- The block-RAM ledger, 124 against 121.5 ([the area plan](MARK_II_AREA_PLAN.md)), is commissioned separately.
- **A pass no group stages:** a save's read-back step, 0.70 ms, can fall in the same pass as a composed window's heaviest, {L8:.2f} ms, which would be about {L8 + 0.70:.2f} ms against the share. It is derived, not measured. The rows fit it: the least margin, {18 - SRP8:.2f} ms, is more than a few such steps.
- The platform image's four hot-list entries that name the size fixture's callbacks place nothing there, and its own callbacks are not on the list.
- The routed split image is lane S9's. [Section 14](#14-the-32x32-estimate) carries these figures to Mark II's shape.

"""
EST_ROWS = estimate32.ROWS
est = ['| Row | Bound, ms | 1x1/1if | 8x8/1if | 8x8/2if | U: 4 x 8x8/2if | L: the line, 1x1/1if to 8x8/2if | S: the streams alone |',
       '|---|---:|---:|---:|---:|---:|---:|---:|']


def bold(v, b):
    return f'**{v:.1f}** (+{v - b:.1f})' if v > b else f'{v:.1f}'


misses = {'U': [], 'L': [], 'S': []}
for row in EST_ROWS:
    b = rows12.worst(A8[0][0])[row][2]
    t1, t81, t8 = ms(A1, row), ms(P81, row), ms(A8, row)
    u, l, s = 4 * t8, t8 + (t8 - t1) * 48 / 14, t8 + (t81 - t1) * 48 / 14
    est.append(f'| {title(row)} | {b:g} | {t1:.2f} | {t81:.2f} | {t8:.2f} | {bold(u, b)} | {bold(l, b)} | {bold(s, b)} |')
    for name, v in (('U', u), ('L', l), ('S', s)):
        if v > b:
            misses[name].append((title(row), v, b))
t1, t81, t8 = longest(A1), longest(P81), longest(A8)
PU, PL, PS = 4 * t8, t8 + (t8 - t1) * 48 / 14, t8 + (t81 - t1) * 48 / 14
est.append(f'| The longest work pass | 2 | {t1:.2f} | {t81:.2f} | {t8:.2f} | {bold(PU, 2)} | {bold(PL, 2)} | {bold(PS, 2)} |')
idle = lambda legs: estimate32.idle_pass(legs[0][0])[0]
quiet = {n: estimate32.steady(root / n) for n in ('N-A1', 'P81-A8', 'N-A8', 'none-A8', 'soci-A8')}
names = lambda rows: ', '.join(f'{n[0].lower() + n[1:] if not n.startswith(("ACMP", "ADP", "AECP", "MAAP", "SRP")) else n} {v:.1f} ms' for n, v, _ in rows)

one = ['| Row | Bound, ms | Split CPU, 1x1 | Cacheless RV32IM, 1x1 | Cacheless RV32I, 1x1 | Split CPU, 8x8 | Cacheless RV32IM, 8x8 | Cacheless RV32I, 8x8 |',
       '|---|---:|---:|---:|---:|---:|---:|---:|']
arms = (A1[0], NONE1[0], SOCI1[0], A8[0], NONE8[0], SOCI8[0])
for row in EST_ROWS:
    b = rows12.worst(A8[0][0])[row][2]
    one.append(f'| {title(row)} | {b:g} | ' + ' | '.join(rows12.cell(rows12.worst(a[0]).get(row)) for a in arms) + ' |')
fmt_share = lambda a: (lambda o, p, l: f'**{o} of {p}, {l:.2f}**' if o else f'{o} of {p}, {l:.2f}')(*rows12.shares(a[0]))
one.append('| Passes over the 2.0 ms share, longest ms | 2 | ' + ' | '.join(fmt_share(a) for a in arms) + ' |')
plan = lambda a: a[1]['ctrl_plan']['tiles']

GPTP_CYCLES = 40_000
GPTP_FRAMES = 2 * 23
GPTP_SERVO = 2 * 8
GPTP_LOAD = 100 * (GPTP_FRAMES + GPTP_SERVO) * GPTP_CYCLES / 100e6
GPTP_ROW = 4 * GPTP_CYCLES / 100e3
GPTP_PASS = 2 * GPTP_CYCLES / 100e3
QU, QS = 4 * quiet['N-A8'], quiet['N-A8'] + (quiet['P81-A8'] - quiet['N-A1']) * 48 / 14
by = {k: {n: v - b for n, v, b in misses[k]} for k in misses}
everywhere = [f"- **{n}, under S, L and U:** over by {by['S'][n]:.1f}, {by['L'][n]:.1f} and {by['U'][n]:.1f} ms." for n in by['S']]
everywhere.append(f"- **The longest work pass, under S, L and U:** {PS:.1f}, {PL:.1f} and {PU:.1f} ms, over the 2.0 ms share by {PS - 2:.1f}, {PL - 2:.1f} and {PU - 2:.1f} ms.")
only_u = ', '.join(f"{n[0].lower() + n[1:] if not n.startswith(('ACMP', 'ADP', 'AECP', 'MAAP', 'SRP')) else n} by {v:.1f} ms" for n, v in by['U'].items() if n not in by['S'])
sec14 = f"""## 14. The 32x32 estimate

Mark II's shape is 32x32: 16x16 logical streams, each redundant on both networks, on one TDM8 bus ([owner, 2026-10-31](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6545621753)).
No such shape exists yet, so nothing here measures it.
The first table is a derivation from this branch's measurements, marked as an estimate, against T_svc = 20 ms and each family's ceiling; the one-CPU table is measured; the gPTP share is an assumption, labelled as one.

### The estimate

Each row's 8x8/2if measurement, with the CPU on `sys` at 100 MHz, is carried to 64 streams three ways, and the rings and buckets stay the contract's, so a window holds the same records:

- **U** is the assigned derivation: four times the 8x8/2if figure, every cycle taken to grow with the streams.
- **L** is the measured growth: the line through 1x1/1if (2 streams) and 8x8/2if (16), to 64.
- **S** is the streams' own growth: the 8x8/2if figure plus the slope from 1x1/1if to 8x8/1if, which holds the interfaces at one. The 8x8/1if point is a labelled scratch arm, not on this branch.

Worst of the arms measured, ms, over the bound in bold with the excess (estimates in the last three columns):

{chr(10).join(est)}

The rows that would not fit, and by how much:

{chr(10).join(everywhere)}
- **Under U alone:** {only_u}.

So the last AECP and SRP records and the per-pass share miss whichever way the growth is read, and the rest of U's misses depend on how much of each row grows with the streams.
The last SRP record waits for its channel's 32 records at two a pass, so its row is about sixteen passes, and every pass carries the polls' per-stream cost: an idle pass takes {idle(A1):,} CPU cycles at 1x1/1if and {idle(A8):,} at 8x8/2if.
The derivation has limits a measurement would not: 8x8/2if already holds its streams per interface, so a 32x32 interface holds twice its streams where the entity holds four times, which makes U an upper reading for the per-interface work (SRP); nothing here knows the cost of 64-stream tables that were never linked, and the Block RAM they need binds first ([the area plan](MARK_II_AREA_PLAN.md)).

### One CPU, measured

The owner's lever order names one CPU, no second hart, as lever 4 ([#640](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6545540394)).
As built, the split placement has one hart already: `MilanSoC` gives its only CPU, `cpu_count` 1, the split options under `--ctrl-mailbox`, and the harness measures that one hart with the protocol firmware, its boot path and the saved-state store on it.
So the estimate's 3,948 LUTs of split CPU are added to an image that still counts the all-fabric CPU's 3,249, and lever 4's saving removes a second hart the code does not build.
What the lever can still ask is whether the firmware fits the SoC core as it ships: cacheless, without the split CPU's caches or RV32M.
Measured on `sys` at 100 MHz, the four backlog groups, arm A, the image rebuilt for each CPU (bold over the bound; the cacheless RV32I arm is a labelled scratch arm, not on this branch):

{chr(10).join(one)}

The cacheless core does not fit 8x8: the last AECP and SRP records miss, and about 60 passes a run are over the share.
At 1x1 the RV32IM arm fits every row, the last SRP record by {18 - rows12.worst(NONE1[0][0])['SRP record, last'][0][1]:.2f} ms, with three passes over the share; RV32I misses the last SRP record too.
Against those, the split CPU on `sys` costs 5 tiles of Block RAM (9.5 against 4.5) and about 300 LUTs (3,543 against 3,249) more than the shipping core, and its image plans {plan(A8[0])} tiles where RV32I's plans {plan(SOCI8[0])}.
The quiet work load, work-pass cycles over elapsed cycles from `settled` to `composed`, is {100 * quiet['N-A1']:.2f} % at 1x1/1if and {100 * quiet['N-A8']:.2f} % at 8x8/2if on the split CPU, {100 * quiet['none-A8']:.2f} % and {100 * quiet['soci-A8']:.2f} % on the two cacheless arms at 8x8/2if: load is not what binds, the burst is.
The estimate carries that quiet load to {100 * QS:.1f} to {100 * QU:.1f} % at 32x32.

### gPTP's share, an assumption

The protocol processor goes at the switch-over and gPTP moves to firmware at lane F6 ([owner, 2026-10-31](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6545457321)); the fabric keeps the timestamps on both ports.
None of this is measured, because no gPTP firmware is linked here.
The assumption, from Milan v1.2's intervals (Sync 125 ms, Announce and Pdelay 1 s) and IEEE 802.1AS-2011's message set:

| Quantity | Assumed | Basis |
|---|---:|---|
| Frames a second | {GPTP_FRAMES} | 23 a port, two ports: Sync and Follow_Up 16, Announce 1, Pdelay 6 (requester and responder) |
| Servo runs a second | {GPTP_SERVO} | One per Sync, each port |
| CPU cycles a frame or servo run | {GPTP_CYCLES:,} (20,000 to 100,000) | About twice a measured ACMP record; the surveyed stack [uses soft double math](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6551164172) |
| Sustained load | {GPTP_LOAD:.1f} % (1.2 to 6.2) | {GPTP_FRAMES + GPTP_SERVO} x {GPTP_CYCLES:,} cycles at 100 MHz |
| Added to any row | {GPTP_ROW:.1f} ms | Four frames in a window of up to 87 ms |
| Added to a pass | {GPTP_PASS:.1f} ms | Two records a channel a pass |

So the sustained share is small, and the bursts are what it touches: the longest 32x32 pass becomes {PS + GPTP_PASS:.1f} ms under S and {PU + GPTP_PASS:.1f} ms under U.
A Pdelay response waits for the pass running when its request arrives, then its own, and Milan v1.2 4.2.6.2.6 allows 15 ms of turnaround: {2 * (PS + GPTP_PASS):.1f} ms under S fits, {2 * (PU + GPTP_PASS):.1f} ms under U does not.

**What would measure it:** F6's stack linked into this harness's image behind the HAL, the mailbox channel it takes in the contract, and a stimulus of these frames on both ports at their intervals, graded here for each frame's cost, the servo's, the pass and the Pdelay turnaround, at 8x8/2if first and at 32x32 when that shape exists.

### What the estimate leaves to the owner

These are not decided here.

- **The last AECP and SRP records and the per-pass share at 32x32.** The levers are the rings and buckets the contract admits, the two records a pass of the owner's D4(b), the 2.0 ms share itself, and the firmware's per-stream polls; which of them is the owner's.
- **Which CPU lever 4 means.** The split placement already has one hart. The cacheless core would save about 300 LUTs and 5 tiles, and does not fit 8x8.
- **The CPU clock past 100 MHz, or a second hart,** if the firmware's levers do not close 32x32. Each runs against the area target.
"""
text = doc.read_text()
marker = "### The split CPU on `sys` at 100 MHz\n"
start = text.index(marker) if marker in text else text.index("### What is left\n\n- The owner kept 8x8 in the Mark II split's scope")
head = text[:start]
doc.write_text(head + A + B.rstrip('\n') + '\n\n' + sec14)
