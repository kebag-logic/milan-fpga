# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The rows by every source under priority tiers (#894; #665, the decision of 2026-11-09, option B), beside
rows_grade.py's rows of the loop before the tiers, which this module does not change. The built design (BUILT, the tier
model at the tree's slice and orders, read from ctrl_loop.h, and AECP's owed-notice queue at each point's depth) is the
flip check's (flip_grade.py, --design built); its self-test plants a defect in each of its paths.

  built      THE TIERS as ctrl_loop.c builds them: BUILT, the default. Its rows are TIER_ROWS, each tier-1 channel's
             last record of its burst (CHANNEL_ROWS, #894's ruling of 2026-11-13, item 2: AECP's with its largest legal
             notice as well, R4L) and THE TRANSMIT's MRPDU (tx, at CTRL_LOOP_TX_BOUND_MS, item 1), each held.
  corrected  THE DRAIN as built before the tiers (rows_grade.demand, re-derived here and held equal to it with every
             correction off), with each count at its source's own rule: the retained retry at most once a centisecond
             and no more than SRP's records (srp_mbx.c, retry_spent, given back by the centisecond's consumer;
             load_grade.RETRY_RULE); SRP's records ahead of AECP's last one counted over the window less only that
             record; and the three coalesced datapath events counted (DATAPATH). Optionally the AECP passes at one
             record a pass (NOTIFY).
  tiers      TIERS below, at a Design: tier 2's slice length and the orders.

Every bound, cost and arrival rule not named here is rows_grade.py's (its docstring's source list). The bounds are
decision D's (rows_grade.BOUNDS): tier 1 20 ms, SRP 90 ms, the last queued notice 125 ms; the tier-1 channel rows'
FR_NFR.md 3.4.1's (CHANNEL_BOUNDS: R4L 20 ms, ACMP, ADP and MAAP 30 ms by the owner's decision of 2026-11-13, option
A); THE TRANSMIT's the MRP timer budget's 40 ms (bounds_at).

usage: python3 -I rows_tiers.py [--model {built,corrected,tiers}] [--slice US ...] [--tier1 ORDER] [--tier2 ORDER]
                                [--aecp RULE] [--cap N] [--quota A/B/C/D] [--long RULE] [--no-datapath]
                                [--point POINT] [--terms] [--selftest]
  --model        built (the default), corrected (THE DRAIN before the tiers, each count at its source's rule) or tiers
  --slice        tier 2's slice length in microseconds, repeated for a sweep (default REFERENCE's)
  --cap, --quota the others' cap a pass, or each tier-1 channel's quota (AECP, ACMP, ADP, MAAP) under aecp-quota or wrr
  --long         the rule for a notice longer than a slot: buffer (the tree's) or slot-552
  --no-datapath  leave the three coalesced datapath events out, to show what they add (never a bound)
  --terms        print every term of every row, not only the three largest
  --selftest     plant each control and exit 1 unless every one is refused
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path
from typing import Callable, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import load_grade  # noqa: E402
import rows_grade  # noqa: E402
from tier1_rows import (CHANNEL_BOUNDS, LONG_NOTICE_BYTES, QUOTA_ORDERS, TIER1, aecp_passes,  # noqa: E402
                        channel_passes, channel_row, quota_fits, tier1_busy, tier1_records, tx_passes)

BOUNDS, POINTS, ROOT = rows_grade.BOUNDS, rows_grade.POINTS, load_grade.ROOT

TIERS = """THE TIERS (#665, the decision of 2026-11-09: a tier-1 record is served before any tier-2 work; tier-2 work
runs in slices of at most a stated length, with tier 1 checked between two slices). A pass, in this order:
  1. events, as built (ctrl_loop.c:252, events first): the TICK and its centisecond consumers, the timer slots, the
     grandmaster event and the three datapath events, each coalesced, one a source an ordinary pass at most;
  2. tier 1: the first queued notice once its retry is due (a round of one, AECP_ROUND_COLD_US + AECP_NOTICE_US),
     then the records of AECP, ACMP, ADP and MAAP. `turn`: each channel its cap a pass (CTRL_LOOP_RX_PER_PASS, one in
     a pass that dispatched a centisecond), as built. `aecp-first`: no other tier-1 channel's record is taken while an
     AECP record waits, and AECP's go past the cap while tier 1 has spent less than CTRL_LOOP_DRAIN_US in the pass;
  3. tier 2, only when no tier-1 record waits (a ring's occupancy: an AECP record its owed notice holds still holds tier
     2 off): one slice of at most slice_us. A slice takes a unit only while what it has left holds the unit's stated
     cost; a unit dearer than the slice resumes in the next (#665, the decision of 2026-11-09, item 2: THE TRANSMIT's
     build and THE RETRY's round). `srp-first`: THE TRANSMIT's build and an owed MRPDU, then SRP's records and its
     retained retry (THE DRAIN), a link change's withdrawal and rebuild, then THE RETRY's rounds. `turn`: the build, SRP
     and the rounds take slices in turn;
  4. the polls' base, ACMP's and AECP's owed frames (tier 1's own output, A3) and SRP's walk and reclaim (under 65 us
     each, the room the next SRP record needs), each counted as rows_grade counts it.
THE STEP stays a pass given whole, as built: its age limit is its own bound, and a flash step does not divide.
Tier 1's further orders, each a design the tier model solves and none built (#894's ruling of 2026-11-13, item 3):
`aecp-quota`, AECP first while the pass's tier-1 time less the others' quotas holds, then each other channel its quota
whatever AECP holds; `wrr`, every tier-1 channel at most its weight a pass, in turn; `others-first`, ACMP, ADP and MAAP
first, each its cap then one each in turn, and AECP past its cap only once they hold none.
AECP's records: `notify`, the tree's rule, one a pass at worst, since a command that changes state leaves its notice
owed and aecp_ready refuses the next record until the poll sends it (aecp.c:277-280); `cap`, a further change, AECP
takes its next record while a command's notice is owed. A notice longer than a slot of the owed-notice queue
(`buffer`, the tree's slot: AECP_OWED_BYTES) waits in the response buffer under the notify rule; `slot-552` sizes a
slot to the largest legal notice (LONG_NOTICE_BYTES), so every notice is queued. The tree's slot holds it (#894, the
owner's decision of 2026-11-13, option A), so at this tree the two rules give the same rows.
The rows: R4, R5 and R6 as rows_grade defines them; the first and the last queued notice are solved too, from the
first notice's port answer: its retry falls due within AECP_RETRY_MAX_MS (the spacing), then its window. The first is
tier 1's first work; the last waits for all the queue's rounds, a round a slice, behind tier 1 and, `srp-first`,
behind every tier-2 unit that arrives in its window."""

#: The coalesced datapath events (mailbox.yaml event_types 6 to 8; its event rule: a source that fires again before
#: its record is posted posts once), and each one's sources: AVB_INFO_CHANGED and AS_PATH_CHANGED an interface each
#: (the record's IF), AMAP_LIVE_WRITE the one live audio map. None has a contract rate, so a window bounds each source
#: by its coalescing, one an ordinary pass. The AECP application's sink takes all three (ctrl_app_aecp.c:174-179).
DATAPATH = {'AVB_INFO_CHANGED': 'interface', 'AS_PATH_CHANGED': 'interface', 'AMAP_LIVE_WRITE': 'entity'}
#: Each datapath event's stated cost in us, its take and every sink's work: the most the CPU budget harness measured
#: over its datapath-events group at the point (the testbench's datapath change pads, split_soc.DATAPATH_PADS), plus
#: 5 %, rounded up to 5 us, as every stated cost, the larger of each image's measurement and the one before it (#894:
#: the datapath events' sink cost, measured, and measured again on the image under THE TIERS).
DATAPATH_US = {'1x1/1if': {'AVB_INFO_CHANGED': 35, 'AS_PATH_CHANGED': 30, 'AMAP_LIVE_WRITE': 25},
               '8x8/2if': {'AVB_INFO_CHANGED': 35, 'AS_PATH_CHANGED': 35, 'AMAP_LIVE_WRITE': 25}}
#: The five rows decision D bounds, the slice rule's (slice_choice).
TIER_ROWS = ('R4', 'R5', 'R6', 'first', 'last')
#: Each channel the loop serves and its rows (#894's ruling of 2026-11-13, item 2): a tier-1 channel's last record of
#: its burst beside the composed burst, AECP's also with every command of its burst answered by the largest legal
#: notice (R4L), and THE DRAIN's channel's R5 and R6. served() reads the channels from the loop's bindings.
CHANNEL_ROWS = {'aecp': ('R4', 'R4L'), 'acmp': ('ACMP',), 'adp': ('ADP',), 'maap': ('MAAP',), 'srp': ('R5', 'R6')}
#: The rows the tier model adds beside TIER_ROWS, in their order: the tier-1 channels' and THE TRANSMIT's MRPDU.
ADDED_ROWS = ('R4L', 'ACMP', 'ADP', 'MAAP', 'tx')
#: The MRP timer budget's bound on THE TRANSMIT's MRPDU, in ms (#894's ruling of 2026-11-13, item 1; ctrl_loop.h,
#: CTRL_LOOP_TX_BOUND_MS, which the tree must state): JoinTime's 200 ms plus it within Milan v1.2 Table 4.3's 240.
TX_BUDGET_MS = 40
TIER1_ROWS = ('R4', 'R4L', 'ACMP', 'ADP', 'MAAP', 'first')
TIER1_ORDERS = ('turn', 'aecp-first', 'aecp-quota', 'wrr', 'others-first')
TIER2_ORDERS = ('srp-first', 'turn')
AECP_RULES = ('notify', 'cap', 'queue')
LONG_RULES = ('buffer', 'slot-552')
#: That notice's cost to the registered controllers in us, a stated input and not a measurement: no group of the CPU
#: budget harness sends one. A notice over AECP_FAN_BYTES is sent a recipient at a time (aecp.c, fan_out), each charged
#: the most measured AECP poll sending one frame (poll.aecp_one_frame: 4,216 cycles at 1x1/1if, 5,945 at 8x8/2if), to
#: every registration but the requester's (15 and 31), plus 5 %, rounded up to 5 us. A long command's own record is
#: charged record.aecp, measured on shorter ones.
LONG_NOTICE_US = {'1x1/1if': 665, '8x8/2if': 1940}
#: The terms a tier-1 row may not carry: tier 2's work, for which only the one slice its window opens on stands.
TIER2_TERMS = ('srp', 'item.retained', 'item.mrpdu', 'builds', 'rounds', 'item.withdraw', 'item.rebuild')
#: Each term these models count and its source: rows_grade's list, the three datapath events, and the tier model's.
SOURCES = {**rows_grade.SOURCES, 'records': (*rows_grade.SOURCES['records'], 'own'), 'datapath': ('datapath',),
           'tier 1: the first queued notice': ('notice',), 'tier 2: the slice a window opens on': ('slice',),
           'the retry spacing': ('spacing',)}


class Inputs(NamedTuple):
    """A point's inputs: rows_grade's (header constants, stated costs, counts, rates, TICK period), the retry spacing,
    AECP_RETRY_MAX_MS (aecp.h), and the built design's: its slice, CTRL_LOOP_SLICE_US (ctrl_loop.h), and the owed-notice
    queue's depth an integrator gives AECP at the point, AECP_MBX_OWED_SLOTS (aecp_mbx.h); THE TRANSMIT's bound and its
    stated figure (CTRL_LOOP_TX_BOUND_MS, CTRL_LOOP_TX_MS, ctrl_loop.h) and the queue's slot, AECP_OWED_BYTES."""

    h: dict
    c: dict
    s: dict
    rate: dict
    tick_ms: int
    spacing_ms: int
    slice_us: int = 0
    owed: int = 0
    tx_bound: int = TX_BUDGET_MS
    tx_stated: int = 0
    slot: int = 0


#: The built design's constants and where each is read: the slice, the owed-notice queue's depth at each point, THE
#: TRANSMIT's bound and stated figure, and the queue's slot.
BUILT_NAMES = {'CTRL_LOOP_SLICE_US': 'sw/firmware/ctrl/loop/ctrl_loop.h',
               'AECP_MBX_OWED_SLOTS': 'sw/firmware/ctrl/aecp/aecp_mbx.h',
               'CTRL_LOOP_TX_BOUND_MS': 'sw/firmware/ctrl/loop/ctrl_loop.h',
               'CTRL_LOOP_TX_MS': 'sw/firmware/ctrl/loop/ctrl_loop.h',
               'AECP_OWED_BYTES': 'sw/firmware/ctrl/aecp/aecp.h'}


def built_constants(root: Path, n_if: int, texts: dict[str, str] | None = None) -> tuple[int, ...]:
    """BUILT_NAMES' constants at that many interfaces, in its order, each `(MBX_N_IF == 1u ? a : b)` or a number, the
    burst a name of the mailbox contract (MBX_CH_AECP_RATE_BURST, mailbox.yaml)."""
    burst = rows_grade.contract(root)[0]['aecp'][0]
    out = []
    for name, path in BUILT_NAMES.items():
        text = (texts or {}).get(path) or (root / path).read_text()
        body = re.search(rf'^#define {name} (.+)$', text, re.M)[1].split('//')[0].strip()
        body = re.sub(r'(\d+)u\b', r'\1', body).replace('MBX_CH_AECP_RATE_BURST', str(burst))
        pick = re.fullmatch(r'\(MBX_N_IF == 1 \? (\d+) : (\d+)\)', body)
        out.append(int(pick[1] if n_if == 1 else pick[2]) if pick else int(body))
    return tuple(out)


def point_inputs(root: Path, point: str, texts: dict[str, str] | None = None) -> Inputs:
    """A point's inputs, rows_grade's read from the tree, the retry spacing and the built design's constants."""
    spacing = re.search(r'^#define AECP_RETRY_MAX_MS (\d+)u', (root / 'sw/firmware/ctrl/aecp/aecp.h').read_text(), re.M)
    base = rows_grade.point_inputs(root, point)
    costs = {**base.c, **{f'event.{kind}': us for kind, us in DATAPATH_US[point].items()},
             'item.aecp.long': LONG_NOTICE_US[point]}
    return Inputs(base.h, costs, *base[2:], int(spacing[1]), *built_constants(root, base.s['n_if'], texts))


def as_tiers(base: rows_grade.Inputs) -> Inputs:
    """rows_grade's inputs as these models read them: the datapath events' stated costs at the point of their
    interfaces, the retry spacing of aecp.h's AECP_RETRY_MAX_MS (8 ms) and no built constants."""
    point = next(p for p in POINTS if load_grade.POINTS[p]['n_if'] == base.s['n_if'])
    costs = {**base.c, **{f'event.{kind}': us for kind, us in DATAPATH_US[point].items()},
             'item.aecp.long': LONG_NOTICE_US[point]}
    return Inputs(base.h, costs, *base[2:], 8)


def bounds_at(i: Inputs) -> dict[str, float]:
    """Every row's bound in ms at a point: decision D's, the channel rows' and THE TRANSMIT's, the header's."""
    return {**BOUNDS, **CHANNEL_BOUNDS, 'tx': i.tx_bound}


def served(root: Path, texts: dict[str, str] | None = None) -> tuple[tuple[str, ...], str]:
    """The channels the loop serves, each a module's ctrl_loop_bind_rx of a contract channel in the firmware's sources
    (not its tests), named as mailbox.yaml names them, and THE DRAIN's channel (drain_ch)."""
    firmware = root / 'sw/firmware/ctrl'
    files = {str(p.relative_to(root)): p.read_text() for p in sorted(firmware.glob('*/*.c'))
             if p.parent.name not in ('test', 'host')}
    files.update(texts or {})
    text = '\n'.join(files.values())
    bound = sorted({m.lower() for m in re.findall(r'ctrl_loop_bind_rx\(\s*\w+\s*,\s*MBX_CH_([A-Z]+)\s*,', text)})
    drain = re.findall(r'drain_ch = MBX_CH_([A-Z]+) \+ 1u;', text)
    return tuple(bound), (drain[0].lower() if len(drain) == 1 else '')


def unrowed(root: Path, model: Design, points: tuple[str, ...] = POINTS,
            texts: dict[str, str] | None = None) -> list[str]:
    """Each channel the loop serves that has no row at a point by `model`, and a tier-1 channel list that is not the
    loop's: every bound channel but THE DRAIN's is tier 1's."""
    channels, drain = served(root, texts)
    out = [] if set(channels) - {drain} == set(TIER1) and drain else \
        [f'the tier-1 channels {", ".join(TIER1)} are not the loop\'s, {", ".join(c for c in channels if c != drain)}']
    for point in points:
        held = rows(root, point, model)
        out += [f'{point}: the channel {ch} the loop serves has no row' for ch in channels
                if not CHANNEL_ROWS.get(ch) or any(r not in held for r in CHANNEL_ROWS[ch])]
    return out


def datapath_sources(s: dict) -> int:
    """The coalesced datapath sources at a point: two an interface and the live audio map."""
    return sum(s['n_if'] if kind == 'interface' else 1 for kind in DATAPATH.values())


def datapath_pass_us(c: dict, s: dict) -> float:
    """What the datapath events cost an ordinary pass at most: each source once, at its event's stated cost."""
    return sum((s['n_if'] if where == 'interface' else 1) * c[f'event.{kind}'] for kind, where in DATAPATH.items())


class Fix(NamedTuple):
    """The corrected model's corrections, each a count at its source's own rule; all off is rows_grade.demand."""

    retained: bool = True
    window: bool = True
    datapath: bool = True
    notify: bool = False


CORRECTED = Fix()
AS_BUILT = Fix(False, False, False, False)


def built(row: str, i: Inputs, w_ms: float, fix: Fix) -> dict[str, float]:
    """rows_grade.demand's terms (THE DRAIN as built) with the corrections `fix` turns on, in microseconds."""
    h, c, s, rate, tick_ms = i[:5]
    out = {}
    n_if, cap = s['n_if'], h['CTRL_LOOP_RX_PER_PASS']

    def arrive(ch: str) -> int:
        """The channel's records in the window: its burst and a record a refill."""
        return rate[ch][0] + math.floor(w_ms / rate[ch][1])
    ticks = math.floor(w_ms / tick_ms) + 1
    out['ticks'] = ticks * (c['event.TICK'] + max(c['centisecond'], h['CTRL_LOOP_TICK_US']))
    link, burst = row == 'R5', rate['srp'][0]
    aecp_passes = 0
    if row == 'R4':
        out['aecp'] = rate['aecp'][0] * c['record.aecp']
        aecp_passes = math.ceil(rate['aecp'][0] / cap) + ticks
        if fix.notify:
            aecp_passes = max(aecp_passes, rate['aecp'][0])
        # SRP's records arriving while the burst is served, all ahead: as built the window less the burst's work;
        # corrected less only the row's own record, the one a record arriving later cannot precede
        draining = max(0.0, w_ms - (c['record.aecp'] if fix.window else out['aecp']) / 1000)
        out['srp'] = (burst + math.floor(draining / rate['srp'][1])) * c['record.srp']
    else:
        out['srp'] = burst * c['record.srp']
    cost_b, count_b = rows_grade.builds(h, s)
    passes, timers, events = 1, 0.0, 0.0
    held = (n_if + 1) if link else 0
    for _ in range(60):
        timers = rows_grade.timer_us(s, c, w_ms, passes, rate)
        events = out['ticks'] + timers
        drained = math.ceil((out['srp'] + events) / h['CTRL_LOOP_DRAIN_US'])
        n = (aecp_passes + 1 + drained) if row == 'R4' else (1 + drained + held)
        if n == passes:
            break
        passes = n
    out['timers'] = timers
    if row == 'R4':
        out['others'] = sum(min(arrive(o), passes * cap) * c[f'record.{o}'] for o in rows_grade.OTHERS if o != 'aecp')
    else:
        light = math.floor(events / max(1, h['CTRL_LOOP_DRAIN_US'] - cap * c['record.srp'])) + held
        out['others'] = sum(min(arrive(o), light * cap) * c[f'record.{o}'] for o in rows_grade.OTHERS)
    gm = sum(math.floor(w_ms / ms) + 1 for ms in load_grade.GM_INTERVALS_MS)
    out['gm'] = n_if * min(passes, gm) * c['event.GM']
    out['builds'] = cost_b
    out['steps'] = (math.floor(w_ms / (10 * (h['CTRL_LOOP_STEP_AGE'] + 1))) + 1) * h['CTRL_LOOP_STEP_PASS_US']
    srp_in = arrive('srp')
    out['item.walk'] = min(passes * n_if, n_if * (ticks + count_b)) * c['item.walk']
    out['item.reclaim'] = min(2 * n_if * passes, 2 * (srp_in + count_b)) * c['item.reclaim']
    # the retained retry: as built one a pass; corrected at most one a centisecond dispatched (the retry's own rule)
    out['item.retained'] = min(passes, srp_in, *((ticks,) if fix.retained else ())) * c['item.retained']
    out['item.mrpdu'] = min(passes, 2 * count_b) * c['item.mrpdu']
    out['item.acmp'] = min(passes, arrive('acmp') + arrive('adp') + n_if * s['sinks_per_if']) * c['item.acmp']
    out['item.aecp'] = min(passes, arrive('aecp') + n_if * s['registrations']) * c['item.aecp']
    if link:
        out['item.withdraw'] = n_if * c['item.withdraw']
        out['item.rebuild'] = n_if * c['item.rebuild']
        out['links'] = n_if * c['event.LINK']
    out['passes'] = passes * (c['events_none'] + c['base'])
    out['rounds'] = rows_grade.rounds_us(h, w_ms)[0]
    if fix.datapath:
        out['datapath'] = passes * datapath_pass_us(c, s)
    return out


class Design(NamedTuple):
    """A tier design (TIERS): tier 2's slice in microseconds (0: the tree's at each point, CTRL_LOOP_SLICE_US, resolved
    by at_point), tier 1's and tier 2's order, AECP's rule, and whether the datapath events are counted (a report's
    choice, to show what they add; every bound counts them); the others' cap a pass (0: CTRL_LOOP_RX_PER_PASS), each
    tier-1 channel's quota a pass in TIER1's order under QUOTA_ORDERS (aecp-quota's AECP 0: the time the others' leave),
    and the rule for a notice longer than a slot (LONG_RULES)."""

    slice_us: int
    tier1: str = 'turn'
    tier2: str = 'srp-first'
    aecp: str = 'notify'
    datapath: bool = True
    cap: int = 0
    quota: tuple[int, ...] = ()
    long: str = 'buffer'

    def label(self) -> str:
        """The design as the tables name it."""
        shown = f'{self.slice_us} us' if self.slice_us else 'CTRL_LOOP_SLICE_US'
        return (f'slice {shown}, tier 1 {self.tier1}, tier 2 {self.tier2}, AECP {self.aecp}' +
                (f', cap {self.cap}' if self.cap else '') +
                (f', quotas {"/".join(map(str, self.quota))}' if self.quota else '') +
                ('' if self.long == LONG_RULES[0] else f', long notices {self.long}') +
                ('' if self.datapath else ', datapath events left out'))


def at_point(model: Fix | Design, i: Inputs) -> Fix | Design:
    """The model with the point's slice where it takes the tree's (a Design whose slice_us is 0)."""
    return model._replace(slice_us=i.slice_us) if isinstance(model, Design) and not model.slice_us else model


def smallest_slice(i: Inputs) -> int:
    """The smallest slice the code could take: an SRP record's apply, which THE DRAIN takes whole (ctrl_loop.c,
    service_rx) and lwSRP cannot divide."""
    return int(i.c['record.srp'])


def resumed(i: Inputs, slice_us: int) -> list[str]:
    """The tier-2 units dearer than the slice, each of which must resume across slices: THE TRANSMIT's build and THE
    RETRY's round by the ruling (#665's decision of 2026-11-09, item 2); any other is a further change the design asks
    for."""
    h, c = i.h, i.c
    units = {'an SRP record': c['record.srp'], 'a retained retry': c['item.retained'],
             "a link change's withdrawal": c['item.withdraw'], "a link change's rebuild": c['item.rebuild'],
             'an MRPDU (THE TRANSMIT, item 2)': c['build_one'],
             'a round of one notice (THE RETRY, item 2)': h['AECP_ROUND_COLD_US'] + h['AECP_NOTICE_US']}
    return [f'{name} ({us:g} us)' for name, us in units.items() if us > slice_us]


def slices(n: int, unit_us: float, slice_us: int) -> int:
    """The slices n units of a stated cost take: as many whole a slice as it holds, or each resumed over as many slices
    as its cost needs."""
    if n <= 0:
        return 0
    if unit_us > slice_us:
        return n * math.ceil(unit_us / slice_us)
    return math.ceil(n / math.floor(slice_us / unit_us))


def round_slices(h: dict, notices: int, slice_us: int) -> tuple[float, int]:
    """THE RETRY's rounds for that many notices, a round a slice, each its cold start and as many notices as the slice
    holds under CTRL_LOOP_SHARE_MARGIN_US, what round_of tells the client (one resumed across slices where it holds
    none): their cost and their slices."""
    cold, each = h['AECP_ROUND_COLD_US'], h['AECP_NOTICE_US']
    room = slice_us - h['CTRL_LOOP_SHARE_MARGIN_US']
    if notices <= 0:
        return 0.0, 0
    per = math.floor((room - cold) / each) if room >= cold + each else 0
    if per == 0:
        return notices * (cold + each), notices * math.ceil((cold + each) / slice_us)
    rounds = math.ceil(notices / per)
    return rounds * cold + notices * each, rounds


def tiered(row: str, i: Inputs, w_ms: float, d: Design) -> dict[str, float]:
    """Each source's work in microseconds in a window of w_ms before the row's work is done, under the tiers."""
    h, c, s, rate, tick_ms = i[:5]
    n_if, slice_us = s['n_if'], d.slice_us

    def arrive(ch: str) -> int:
        """The channel's records in the window: its burst and a record a refill."""
        return rate[ch][0] + math.floor(w_ms / rate[ch][1])
    out = {}
    ticks = math.floor(w_ms / tick_ms) + 1
    out['ticks'] = ticks * (c['event.TICK'] + max(c['centisecond'], h['CTRL_LOOP_TICK_US']))
    notice = h['AECP_ROUND_COLD_US'] + h['AECP_NOTICE_US']
    # tier 1's first work, the first queued notice: ahead of R4 (every notice queued) and of every tier-2 row
    out['notice'] = notice
    # the one tier-2 slice running as the row's window opens
    out['slice'] = slice_us
    cost_b, count_b = rows_grade.builds(h, s)
    srp_in = arrive('srp')
    # an ordinary pass's SRP slice ends CTRL_LOOP_SLICE_US after the pass started, its events' fixed part first, and
    # starts a record only while it has the record's stated cost left (ctrl_loop.c)
    per_slice = max(1, math.floor((slice_us - c['events_none']) / c['record.srp']))
    p_aecp = aecp_passes(i, d, ticks, notice)
    passes, timers, tier2 = 1, 0.0, {}
    for _ in range(80):
        timers = rows_grade.timer_us(s, c, w_ms, passes, rate)
        tier2 = {}
        if channel_row(row, d):
            n = channel_passes(row, i, d, ticks, notice, arrive)
        elif row == 'R4':
            n = p_aecp + 1
        elif row == 'first':
            n = 2
        elif row == 'tx':
            n = tx_passes(i, d, ticks, notice, arrive)
        else:
            # tier 2 ahead of the row's last unit: SRP's rows their own burst; the last notice every unit arriving
            retained = min(passes, ticks, srp_in)
            records = rate['srp'][0] if row != 'last' else srp_in
            mrpdu = min(passes, 2 * count_b)
            srp_slices = slices(records + retained, c['record.srp'], slice_us - c['events_none'])
            n2 = slices(count_b, cost_b / count_b, slice_us) + slices(mrpdu, c['item.mrpdu'], slice_us) + srp_slices
            tier2 = {'srp': records * c['record.srp'], 'item.retained': retained * c['item.retained'],
                     'builds': cost_b, 'item.mrpdu': mrpdu * c['item.mrpdu']}
            if row == 'R5':
                n2 += slices(n_if, c['item.withdraw'], slice_us) + slices(n_if, c['item.rebuild'], slice_us)
                tier2.update({'item.withdraw': n_if * c['item.withdraw'], 'item.rebuild': n_if * c['item.rebuild']})
            us, k = round_slices(h, s['notices'] - 1, slice_us)
            if row == 'last':
                tier2['rounds'] = us
                if d.tier2 == 'turn':
                    # the build and SRP take a slice in turn with the rounds: no more of them than the rounds' slices
                    ahead = k * slice_us
                    for key in ('builds', 'item.mrpdu', 'srp', 'item.retained'):
                        tier2[key] = min(tier2[key], ahead)
                        ahead -= tier2[key]
                    n2 = k + min(n2, k)
                else:
                    n2 += k
            elif d.tier2 == 'turn':
                # the rounds take a slice in turn with SRP's: no more of them than SRP's slices
                taken = min(k, srp_slices)
                tier2['rounds'] = min(us, taken * slice_us)
                n2 += taken
            n = tier1_busy(i, d) + ticks + n2 + 1
        if n == passes:
            break
        passes = n
    out['timers'] = timers
    out.update(tier1_records(row, i, d, passes, arrive))
    if row not in (*TIER1_ROWS, 'tx'):
        out.update(tier2)
    gm = sum(math.floor(w_ms / ms) + 1 for ms in load_grade.GM_INTERVALS_MS)
    out['gm'] = n_if * min(passes, gm) * c['event.GM']
    out['steps'] = (math.floor(w_ms / (10 * (h['CTRL_LOOP_STEP_AGE'] + 1))) + 1) * h['CTRL_LOOP_STEP_PASS_US']
    if row in (*TIER1_ROWS, 'tx'):
        # SRP's walk and reclaim, by their sources in the window: lwSRP's centiseconds and the slice's records
        out['item.walk'] = min(passes * n_if, n_if * ticks) * c['item.walk']
        out['item.reclaim'] = min(2 * n_if * passes, 2 * per_slice) * c['item.reclaim']
    else:
        out['item.walk'] = min(passes * n_if, n_if * (ticks + count_b)) * c['item.walk']
        out['item.reclaim'] = min(2 * n_if * passes, 2 * (srp_in + count_b)) * c['item.reclaim']
    out['item.acmp'] = min(passes, arrive('acmp') + arrive('adp') + n_if * s['sinks_per_if']) * c['item.acmp']
    # AECP's owed frames, R4L's each the largest legal notice (LONG_NOTICE_US)
    each = max(c['item.aecp'], c['item.aecp.long']) if row == 'R4L' else c['item.aecp']
    out['item.aecp'] = min(passes, arrive('aecp') + n_if * s['registrations']) * each
    if row == 'R5':
        out['links'] = n_if * c['event.LINK']
    out['passes'] = passes * (c['events_none'] + c['base'])
    if d.datapath:
        out['datapath'] = passes * datapath_pass_us(c, s)
    return out


def solve(row: str, i: Inputs, model: Fix | Design,
          dropped: str | None = None) -> tuple[float | None, dict[str, float]]:
    """The row's W in ms, in steps of 0.01, with its terms in microseconds, by `model` (a Fix or a Design); None if
    none under 2,000 ms. Under the tiers the queued notices' W opens AECP_RETRY_MAX_MS (spacing) before their window;
    by the corrected model they are the tree's derived bounds, as rows_grade reads them. `dropped` is left out."""
    if isinstance(model, Fix) and row in ('first', 'last'):
        name = 'AECP_QUEUED_FIRST_MS' if row == 'first' else 'AECP_QUEUED_MS'
        return float(i.h[name]), {name: i.h[name] * 1000.0}
    model = at_point(model, i)
    spacing = i.spacing_ms if row in ('first', 'last') and dropped != 'spacing' else 0
    w, d = 0.01, {}
    while w < 2000:
        terms = built(row, i, w, model) if isinstance(model, Fix) else tiered(row, i, w, model)
        d = {k: v for k, v in terms.items() if k != dropped}
        if spacing:
            d['spacing'] = spacing * 1000.0
        total = sum(d.values()) / 1000
        if total <= w + spacing:
            return w + spacing, d
        w = max(w + 0.01, math.ceil((total - spacing) * 100) / 100)
    return None, d


def rows(root: Path, point: str, model: Fix | Design, i: Inputs | None = None,
         dropped: str | None = None) -> dict[str, tuple[float | None, dict[str, float]]]:
    """Each row's W in ms by `model`, with its terms in ms: TIER_ROWS, and under the tiers ADDED_ROWS too, among them
    the MRPDU a join, periodic or LeaveAll timer owes, from the centisecond that owes it to its build (tx: THE
    TRANSMIT, tier 2's first unit, held to CTRL_LOOP_TX_BOUND_MS, #894's ruling of 2026-11-13, item 1)."""
    i = i or point_inputs(root, point)
    out = {}
    for row in (*TIER_ROWS, *(ADDED_ROWS if isinstance(model, Design) else ())):
        w, d = solve(row, i, model, dropped)
        out[row] = (w, {k: v / 1000 for k, v in d.items()})
    return out


def findings(root: Path, model: Fix | Design, points: tuple[str, ...] = POINTS,
             bounds: dict | None = None) -> list[str]:
    """Each row over its tier's bound by `model` at each point, with its largest term."""
    out = []
    for point in points:
        i = point_inputs(root, point)
        for row, (w, terms) in rows(root, point, model, i).items():
            top = max(terms, key=terms.get)
            b = (bounds or bounds_at(i))[row]
            if w is None or w > b:
                shown = 'no W under 2,000 ms' if w is None else f'{w:.2f} ms'
                out.append(f'{point} {row}: {label(at_point(model, i))} {shown}, over its '
                           f'bound {b} ms; the largest term {top} '
                           f'{terms[top]:.2f} ms')
    return out


def long_counted(i: Inputs, w: float, terms: dict[str, float]) -> bool:
    """Whether R4L's terms charge each of AECP's owed frames the largest legal notice (LONG_NOTICE_US)."""
    passes = round(terms['passes'] * 1000 / (i.c['events_none'] + i.c['base']))
    sent = min(passes, i.rate['aecp'][0] + math.floor(w / i.rate['aecp'][1]) + i.s['n_if'] * i.s['registrations'])
    return abs(terms.get('item.aecp', 0.0) * 1000 - sent * max(i.c['item.aecp'], i.c['item.aecp.long'])) < 1e-6


def tx_statements(root: Path, points: tuple[str, ...] = POINTS, texts: dict[str, str] | None = None) -> list[str]:
    """Each way ctrl_loop.h's statement of THE TRANSMIT's MRPDU is not the model's: its bound not the timer budget's
    (TX_BUDGET_MS), or its figure, CTRL_LOOP_TX_MS, under the built design's tx row rounded up to the ms."""
    out = []
    for point in points:
        i = point_inputs(root, point, texts)
        if i.tx_bound != TX_BUDGET_MS:
            out.append(f'{point}: CTRL_LOOP_TX_BOUND_MS states {i.tx_bound} ms, not the timer budget\'s {TX_BUDGET_MS}')
        w = solve('tx', i, BUILT)[0]
        if w is None or i.tx_stated < math.ceil(w - 1e-9):
            out.append(f'{point}: CTRL_LOOP_TX_MS states {i.tx_stated} ms, under the built design\'s tx row '
                       f'{"none" if w is None else f"{w:.2f}"} ms')
    return out


def label(model: Fix | Design) -> str:
    """A model as the tables name it."""
    if isinstance(model, Design):
        return f'under the tiers ({model.label()})'
    on = [name for name, v in model._asdict().items() if v]
    return 'as built' if not on else f'corrected ({", ".join(on)})'


def broken(root: Path, model: Fix | Design, points: tuple[str, ...] = POINTS) -> list[str]:
    """Each way a model breaks its own rules: a term with no source, a retained retry past one a centisecond, SRP's
    window cut by more than the row's record, an uncounted datapath source; and under the tiers a slice under the
    smallest the code could take, a tier-2 term in a tier-1 row, a row without its one slice at the slice's length, a
    tier-1 row without the first queued notice, an order TIERS does not state, quotas not one a tier-1 channel or over
    the pass's tier-1 time, R4L without its largest legal notice, or a channel the loop serves without its rows."""
    out = []
    if isinstance(model, Design):
        if model.tier1 not in TIER1_ORDERS or model.tier2 not in TIER2_ORDERS or model.aecp not in AECP_RULES or \
                model.long not in LONG_RULES:
            return [f'the design {model.label()} names an order TIERS does not state']
        if (model.tier1 in QUOTA_ORDERS) != (len(model.quota) == len(TIER1)) or min(model.quota, default=1) < 0 or \
                (model.tier1 == 'wrr' and min(model.quota, default=1) < 1):
            return [f'the design {model.label()} does not give each tier-1 channel a quota, or gives one where its '
                    'order has none']
        out += unrowed(root, model, points)
        if [slices(1, 1215, 405), slices(5, 250, 1300), slices(0, 365, 365), slices(13, 365, 1300)] != [3, 1, 0, 5]:
            out.append('the slices a unit takes are not counted as TIERS states')
    known = {k for keys in SOURCES.values() for k in keys} | {'AECP_QUEUED_FIRST_MS', 'AECP_QUEUED_MS'}
    whole = model
    for point in points:
        i = point_inputs(root, point)
        model = at_point(whole, i)
        if isinstance(model, Design) and model.slice_us < smallest_slice(i):
            out.append(f'{point}: a slice of {model.slice_us} us is under the smallest the code could take, '
                       f'{smallest_slice(i)} us')
            continue
        if isinstance(model, Design) and not quota_fits(i, model) and (model.cap or model.quota):
            out.append(f'{point}: the quotas of {model.label()} are over the pass\'s tier-1 time')
            continue
        for row, (w, terms) in rows(root, point, model, i).items():
            out += [f'{point} {row}: the term {k} has no source' for k in terms if k not in known]
            if row in ('first', 'last') and isinstance(model, Fix):
                continue
            ticks = math.floor((w or 2000) / i.tick_ms) + 1
            if (isinstance(model, Design) or model.retained) and \
                    terms.get('item.retained', 0.0) * 1000 > ticks * i.c['item.retained'] + 1e-6:
                out.append(f'{point} {row}: the retained retry counted past one a centisecond')
            passes = round(terms['passes'] * 1000 / (i.c['events_none'] + i.c['base']))
            if model.datapath and abs(terms.get('datapath', 0.0) * 1000 - passes * datapath_pass_us(i.c, i.s)) > 1e-6:
                out.append(f'{point} {row}: a datapath source not counted at one a pass')
            if isinstance(model, Fix) and model.window and row == 'R4':
                draining = (w or 2000) - i.c['record.aecp'] / 1000
                if abs(terms['srp'] * 1000 - (i.rate['srp'][0] + math.floor(draining / i.rate['srp'][1])) *
                       i.c['record.srp']) > 1e-6:
                    out.append(f'{point} R4: SRP\'s window cut by more than the row\'s own record')
            if isinstance(model, Design):
                if row in TIER1_ROWS:
                    out += [f'{point} {row}: a tier-1 row carries tier 2\'s {k}' for k in TIER2_TERMS if terms.get(k)]
                    if not terms.get('notice'):
                        out.append(f'{point} {row}: the first queued notice is not counted')
                if abs(terms.get('slice', 0.0) * 1000 - model.slice_us) > 1e-6:
                    out.append(f'{point} {row}: its one slice is not the slice\'s length')
                if row == 'R4L' and not long_counted(i, w or 2000, terms):
                    out.append(f'{point} R4L: an owed frame of AECP\'s not the largest legal notice')
    if load_grade.retry_unbounded(root):
        out.append('the retained retry\'s rule is not the tree\'s (load_grade.RETRY_RULE)')
    return out


def report(root: Path, model: Fix | Design, points: tuple[str, ...] = POINTS, every: bool = False) -> list[str]:
    """Each row at each point by `model`: its W, bound, residual, ordinary passes and its largest (or every) term."""
    lines = [f'Model: {label(model)}', '',
             '| Point | Row | W, ms | Bound, ms | Residual, ms | Passes | ' +
             ('Terms, ms |' if every else 'Largest terms, ms |'), '|---|---|---:|---:|---:|---:|---|']
    for point in points:
        i = point_inputs(root, point)
        bound = bounds_at(i)
        for row, (w, terms) in rows(root, point, model, i).items():
            ranked = sorted(terms.items(), key=lambda t: -t[1])
            top = ', '.join(f'{k} {v:.3f}' for k, v in (ranked if every else ranked[:3]))
            shown, residual = ('none under 2,000', '') if w is None else (f'{w:.2f}', f'{w - bound[row]:+.2f}')
            passes = round(terms.get('passes', 0.0) * 1000 / (i.c['events_none'] + i.c['base']))
            lines.append(f'| {point} | {row} | {shown} | {bound[row]} | {residual} | {passes or ""} | {top} |')
        if isinstance(model, Design) and not quota_fits(i, model):
            lines.append(f'| {point} | | the other tier-1 channels\' caps are over the pass\'s tier-1 time, so the '
                         'channel rows credit a take a pass may cut: each a lower bound | | | | |')
        more = resumed(i, at_point(model, i).slice_us) if isinstance(model, Design) else []
        if more:
            lines.append(f'| {point} | | units resumed across slices: {"; ".join(more)} | | | | |')
    return lines


#: The design the controls plant against: the ruling's own orders at the current per-pass cap, CTRL_LOOP_DRAIN_US.
REFERENCE = Design(1300)
#: The built design (#894; ctrl_loop.h, THE TIERS): AECP first in tier 1, SRP first in tier 2, AECP's owed-notice
#: queue at each point's depth, at the tree's slice, CTRL_LOOP_SLICE_US. The flip check's design (flip_grade.py).
BUILT = Design(0, 'aecp-first', 'srp-first', 'queue')
#: The grid the slice is chosen on, in us: the tier model's first sweep's (#894, the ruling of 2026-11-12: the slice
#: with the largest least relative margin over the five rows at 1x1/1if).
SLICE_GRID_US = 50
#: The models whose rows the controls hold, each named in the controls.
HELD = (('corrected', CORRECTED), ('tiers', REFERENCE), ('built', BUILT))


def least_margin(rows_at: dict[str, tuple[float | None, dict]], bounds: dict | None = None) -> float:
    """The least of a point's rows' margins relative to their bounds, (bound - W) / bound; -1 for a row with no W:
    decision D's five rows (the slice rule's, TIER_ROWS), or with `bounds` every row it names."""
    held = bounds or BOUNDS
    return min((held[row] - w) / held[row] if w is not None else -1.0 for row, (w, _) in rows_at.items()
               if row in held)


def slice_choice(root: Path, point: str = '1x1/1if') -> tuple[int, float]:
    """The slice of the built design's orders and rule with the largest least relative margin at the point, on
    SLICE_GRID_US from the smallest the code could take to CTRL_LOOP_DRAIN_US, and that margin; the shorter on a tie."""
    i = point_inputs(root, point)
    first = math.ceil(smallest_slice(i) / SLICE_GRID_US) * SLICE_GRID_US
    best = None
    for us in range(first, i.h['CTRL_LOOP_DRAIN_US'] + 1, SLICE_GRID_US):
        m = least_margin(rows(root, point, BUILT._replace(slice_us=us), i))
        if best is None or m > best[1]:
            best = (us, m)
    return best
#: The planted defects controls() plants beside each row's, in its order.
CONTROLS = ('the as-built model not rows_grade.demand', 'the retained retry counted once a pass',
            "SRP's window cut by the AECP burst's whole work", 'a datapath source left out',
            'a tier-2 term in a tier-1 row', 'a row without its slice', 'a slice charged at other than its length',
            'a slice under the smallest the code could take', 'a term without a source',
            'the first queued notice left out of R4', 'a unit dearer than the slice charged one slice',
            'an order TIERS does not state', "rows_grade's default not the as-built model",
            'the slice length not read', 'the retry rule not read from the tree',
            "the built design's slice not the rule's", "the owed-notice queue's depth not counted",
            "R4L's owed frames not the largest legal notice", 'a channel the loop serves without its rows',
            "the tier-1 channels not the loop's", "THE TRANSMIT's stated figure under its row",
            "THE TRANSMIT's bound not the timer budget's", "a quota design over the pass's tier-1 time",
            'a design whose quotas are not its order\'s')


def control_names(root: Path) -> tuple[str, ...]:
    """The controls controls() plants, in its order."""
    names = []
    for tag, model in HELD:
        for point in POINTS:
            for row, (w, terms) in rows(root, point, model).items():
                if isinstance(model, Fix) and row in ('first', 'last'):
                    continue
                names.append(f'{tag} {point} {row} over its bound')
                if w is not None:
                    names.append(f'{tag} {point} {row} within its bound')
                    names += [f'{tag} {point} {row}: the source {k} not counted' for k, v in terms.items() if v > 0]
    return (*names, *CONTROLS)


def row_controls(root: Path) -> list[str]:
    """Each held row's planted defects not refused: its bound a hundredth under W and over it, and each source left
    out, which must shorten W."""
    escaped = []
    for tag, model in HELD:
        for point in POINTS:
            i = point_inputs(root, point)
            for row, (w, terms) in rows(root, point, model, i).items():
                if isinstance(model, Fix) and row in ('first', 'last'):
                    continue
                name = f'{point} {row}:'
                under = dict(bounds_at(i), **{row: (w or 2000) - 0.01})
                over = dict(bounds_at(i), **{row: (w or 2000) + 0.01})
                if not any(f.startswith(name) for f in findings(root, model, (point,), under)):
                    escaped.append(f'{tag} {point} {row} over its bound')
                if w is not None and any(f.startswith(name) for f in findings(root, model, (point,), over)):
                    escaped.append(f'{tag} {point} {row} within its bound')
                for term in (k for k, v in terms.items() if v > 0 and w is not None):
                    if not solve(row, i, model, dropped=term)[0] < w:
                        escaped.append(f'{tag} {point} {row}: the source {term} not counted')
        if broken(root, model):
            escaped.append(f'the {tag} model breaks its own rules at this tree')
    return escaped


def drift(root: Path) -> list[str]:
    """Each solved row whose as-built terms (built() with every correction off) differ from rows_grade.demand's at the
    W rows_grade solves."""
    out = []
    for point in POINTS:
        i = point_inputs(root, point)
        base = rows_grade.Inputs(*i[:5])
        for row in rows_grade.SOLVED:
            w, _ = rows_grade.solve(row, base)
            if built(row, i, w, AS_BUILT) != rows_grade.demand(row, base, w):
                out.append(f'{point} {row}')
    return out


def default_holds(root: Path) -> list[str]:
    """Each way rows_grade.rows() at its defaults is not the as-built model: a tier or correction term in a default
    row, or a solved row's W other than rows_grade.solve's."""
    out = []
    for point in POINTS:
        i = rows_grade.point_inputs(root, point)
        held = rows_grade.rows(root, point, inputs=i)
        out += [f'{point} {row}' for row, (_, terms) in held.items() for k in ('slice', 'notice', 'datapath')
                if k in terms]
        out += [f'{point} {row}' for row in rows_grade.SOLVED if held[row][0] != rows_grade.solve(row, i)[0]]
    return out


#: Each planted change of a model's terms, by the control it is, with the model it is planted in: change(row, inputs,
#: w, model, terms) returns the planted terms.
PLANTS: dict[str, tuple[Fix | Design, Callable]] = {
    'the retained retry counted once a pass': (CORRECTED, lambda row, i, w, m, t: dict(
        t, **{'item.retained': max(t['item.retained'], round(t['passes'] / (i.c['events_none'] + i.c['base'])) *
                                   i.c['item.retained'])})),
    "SRP's window cut by the AECP burst's whole work": (CORRECTED, lambda row, i, w, m, t: dict(
        t, srp=(i.rate['srp'][0] + math.floor(max(0.0, w - t['aecp'] / 1000) / i.rate['srp'][1])) *
        i.c['record.srp']) if row == 'R4' else t),
    'a datapath source left out': (REFERENCE, lambda row, i, w, m, t: dict(t, datapath=t['datapath'] * 2 / 3)),
    'a tier-2 term in a tier-1 row': (REFERENCE, lambda row, i, w, m, t: dict(
        t, srp=i.rate['srp'][0] * i.c['record.srp']) if row == 'R4' else t),
    'a row without its slice': (REFERENCE, lambda row, i, w, m, t: {k: v for k, v in t.items() if k != 'slice'}),
    'a slice charged at other than its length': (REFERENCE, lambda row, i, w, m, t: dict(t, slice=2000.0)),
    'a term without a source': (REFERENCE, lambda row, i, w, m, t: dict(t, margin=100.0)),
    'the first queued notice left out of R4': (REFERENCE, lambda row, i, w, m, t: {
        k: v for k, v in t.items() if row != 'R4' or k != 'notice'}),
    "R4L's owed frames not the largest legal notice": (BUILT, lambda row, i, w, m, t: dict(
        t, **{'item.aecp': t['item.aecp'] * i.c['item.aecp'] / i.c['item.aecp.long']}) if row == 'R4L' else t),
}


def plant_controls(root: Path) -> list[str]:
    """Each planted change of a model's terms (PLANTS) its own rules do not refuse."""
    from unittest import mock
    me = sys.modules[__name__]
    escaped = []
    for name, (model, change) in PLANTS.items():
        fn = 'built' if isinstance(model, Fix) else 'tiered'
        first = getattr(me, fn)
        with mock.patch.object(me, fn, lambda row, i, w, m, f=first, g=change: g(row, i, w, m, f(row, i, w, m))):
            if not broken(root, model):
                escaped.append(name)
    return escaped


def tree_controls(root: Path) -> list[str]:
    """The planted defects of what the models read: the as-built derivation, the slice, the orders, rows_grade's
    default and the retry rule in the tree, each that is not refused."""
    from unittest import mock
    me = sys.modules[__name__]
    escaped = []
    if drift(root):
        escaped.append('the as-built derivation differs from rows_grade.demand at this tree')
    original = me.built
    with mock.patch.object(me, 'built', lambda row, i, w, f: {k: v for k, v in original(row, i, w, f).items()
                                                               if k != 'gm'}):
        if not drift(root):
            escaped.append('the as-built model not rows_grade.demand')
    small = Design(smallest_slice(point_inputs(root, '1x1/1if')))
    if not broken(root, small._replace(slice_us=small.slice_us - 1), ('1x1/1if',)):
        escaped.append('a slice under the smallest the code could take')
    with mock.patch.object(me, 'slices', lambda n, unit_us, slice_us: math.ceil(n / max(1, slice_us // unit_us))
                           if n > 0 else 0):
        if not broken(root, REFERENCE, ('1x1/1if',)):
            escaped.append('a unit dearer than the slice charged one slice')
    if not broken(root, REFERENCE._replace(tier1='aecp-last')):
        escaped.append('an order TIERS does not state')
    if default_holds(root):
        escaped.append("rows_grade's default is not the as-built model at this tree")
    with mock.patch.object(rows_grade, 'demand', lambda row, inputs, w: tiered(row, as_tiers(inputs), w, REFERENCE)):
        if not default_holds(root):
            escaped.append("rows_grade's default not the as-built model")
    # the slice read: R4 at the smallest slice is shorter than at the reference's, and a model that charges the
    # reference's slice whatever the design is refused by its own rule
    if not rows(root, '1x1/1if', small)['R4'][0] < rows(root, '1x1/1if', REFERENCE)['R4'][0]:
        escaped.append('the slice length not read')
    first = me.tiered
    with mock.patch.object(me, 'tiered', lambda row, i, w, d: first(row, i, w, REFERENCE)):
        if not broken(root, small, ('1x1/1if',)):
            escaped.append('the slice length not read')
    # the built design's slice is the rule's (the largest least relative margin at 1x1/1if), read from ctrl_loop.h: a
    # header whose slice is another is refused
    loop = 'sw/firmware/ctrl/loop/ctrl_loop.h'
    stated = '#define CTRL_LOOP_SLICE_US (MBX_N_IF == 1u ? 1200u : 1300u)'
    other = (root / loop).read_text().replace(stated, '#define CTRL_LOOP_SLICE_US (MBX_N_IF == 1u ? 1250u : 1300u)')
    tree = built_constants(root, 1)[0]
    if slice_choice(root)[0] != tree or built_constants(root, 1, {loop: other})[0] == tree or \
            stated not in (root / loop).read_text():
        escaped.append("the built design's slice not the rule's")
    # condition (c): the model counts the owed-notice queue's depth, read from aecp_mbx.h: a shallower queue lengthens
    # R4, and none is the tree's rule before it (notify)
    mailbox = 'sw/firmware/ctrl/aecp/aecp_mbx.h'
    text = (root / mailbox).read_text()
    depth = '#define AECP_MBX_OWED_SLOTS (MBX_N_IF == 1u ? MBX_CH_AECP_RATE_BURST : 0u)'
    def at(d: str) -> float:
        """R4 at 1x1/1if with the queue's depth stated as d."""
        return rows(root, '1x1/1if', BUILT, point_inputs(root, '1x1/1if', {mailbox: text.replace(depth, d)}))['R4'][0]
    deep = rows(root, '1x1/1if', BUILT)['R4'][0]
    shallow = at('#define AECP_MBX_OWED_SLOTS (MBX_N_IF == 1u ? 4u : 0u)')
    none = at('#define AECP_MBX_OWED_SLOTS (MBX_N_IF == 1u ? 0u : 0u)')
    notify = rows(root, '1x1/1if', BUILT._replace(aecp='notify'))['R4'][0]
    if text.count(depth) != 1 or not deep < shallow < none or none != notify:
        escaped.append("the owed-notice queue's depth not counted")
    escaped += channel_controls(root)
    # the retained retry's rule is read from the tree: a copy of srp_mbx.c whose centisecond never gives it back
    path = 'sw/firmware/ctrl/srp/srp_mbx.c'
    text = (root / path).read_text()
    with mock.patch.object(load_grade, 'retry_unbounded', lambda r, texts=None, f=load_grade.retry_unbounded: f(
            r, {path: text.replace('m->retry_spent = false;', 'm->retry_spent = m->retry_spent;')})):
        if 'm->retry_spent = false;' not in text or not broken(root, CORRECTED, ('1x1/1if',)):
            escaped.append('the retry rule not read from the tree')
    return escaped


def channel_controls(root: Path) -> list[str]:
    """The planted defects of the channel rows, THE TRANSMIT's statement and the quota designs, each not refused."""
    from unittest import mock
    escaped = []
    one = ('1x1/1if',)
    # a channel bound in a module's source has its rows, and the tier-1 channels are the loop's (#894's ruling of
    # 2026-11-13, item 2: the list derived from the firmware)
    path = 'sw/firmware/ctrl/maap/maap_mbx.c'
    text = (root / path).read_text()
    more = {path: text + '\nvoid planted(struct ctrl_loop *l) { ctrl_loop_bind_rx(l, MBX_CH_FOO, 0, 0); }\n'}
    with mock.patch.dict(CHANNEL_ROWS, {'maap': ()}):
        dropped = broken(root, BUILT, one)
    if not unrowed(root, BUILT, one, more) or not dropped:
        escaped.append('a channel the loop serves without its rows')
    srp = 'sw/firmware/ctrl/srp/srp_mbx.c'
    moved = {srp: (root / srp).read_text().replace('drain_ch = MBX_CH_SRP + 1u;', 'drain_ch = MBX_CH_MAAP + 1u;')}
    if moved[srp] == (root / srp).read_text() or not unrowed(root, BUILT, one, moved):
        escaped.append("the tier-1 channels not the loop's")
    # ctrl_loop.h states THE TRANSMIT's figure at or over its row and its bound at the timer budget's
    loop = 'sw/firmware/ctrl/loop/ctrl_loop.h'
    header = (root / loop).read_text()
    figure, bound = '#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 29u : 90u)', '#define CTRL_LOOP_TX_BOUND_MS 40u'
    under = {loop: header.replace(figure, '#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 28u : 90u)')}
    if figure not in header or tx_statements(root, one) or not tx_statements(root, one, under):
        escaped.append("THE TRANSMIT's stated figure under its row")
    if bound not in header or not tx_statements(root, one, {loop: header.replace(bound, bound[:-3] + '90u')}):
        escaped.append("THE TRANSMIT's bound not the timer budget's")
    if not broken(root, Design(1200, 'wrr', quota=(4, 4, 4, 4)), one):
        escaped.append("a quota design over the pass's tier-1 time")
    if not broken(root, Design(1200, 'wrr'), one) or not broken(root, BUILT._replace(quota=(1, 1, 1, 1)), one):
        escaped.append('a design whose quotas are not its order\'s')
    return escaped


def controls(root: Path) -> list[str]:
    """Each planted defect that is not refused: the planted names that escaped."""
    return row_controls(root) + plant_controls(root) + tree_controls(root)


def main() -> int:
    """Print the rows by a model, or plant each control and refuse an escape."""
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--model', choices=('built', 'corrected', 'tiers'), default='built')
    ap.add_argument('--slice', type=int, action='append', dest='slices')
    ap.add_argument('--tier1', choices=TIER1_ORDERS, default=TIER1_ORDERS[0])
    ap.add_argument('--tier2', choices=TIER2_ORDERS, default=TIER2_ORDERS[0])
    ap.add_argument('--aecp', choices=AECP_RULES, default=AECP_RULES[0])
    ap.add_argument('--cap', type=int, default=0)
    ap.add_argument('--quota', type=lambda s: tuple(int(n) for n in s.split('/')), default=())
    ap.add_argument('--long', choices=LONG_RULES, default=LONG_RULES[0])
    ap.add_argument('--no-datapath', action='store_true')
    ap.add_argument('--point', choices=POINTS)
    ap.add_argument('--terms', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()
    points = (args.point,) if args.point else POINTS
    if args.selftest:
        escaped = controls(ROOT)
        for name in escaped:
            print(f'ESCAPED {name}')
        total = len(control_names(ROOT))
        print(f'rows_tiers: {total - len(escaped)} of {total} planted controls refused')
        return 1 if escaped else 0
    models = [CORRECTED._replace(datapath=not args.no_datapath, notify=args.aecp == 'notify')] \
        if args.model == 'corrected' else \
        [BUILT._replace(slice_us=us, datapath=not args.no_datapath) for us in args.slices or [BUILT.slice_us]] \
        if args.model == 'built' else \
        [Design(us, args.tier1, args.tier2, args.aecp, not args.no_datapath, args.cap, args.quota, args.long)
         for us in args.slices or [REFERENCE.slice_us]]
    rc = 0
    for model in models:
        wrong = broken(ROOT, model, points)
        if wrong:
            print('\n'.join(f'REFUSED {b}' for b in wrong))
            rc = 1
            continue
        print('\n'.join(report(ROOT, model, points, args.terms)))
        found = findings(ROOT, model, points)
        print('\n'.join(f'OVER {f}' for f in found) or 'every row within its bound')
        print()
        rc |= bool(found)
    return rc


if __name__ == '__main__':
    sys.exit(main())
