# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The long-window CPU load of every source at its stated arrival bound, by the response-time method's own terms
(#665; docs/design/SPLIT_CONTROL_MEMORY.md section 13), at 1x1/1if, 8x8/2if and 32x32/2if, held to a stated ceiling.

The load is the work the sources bring per millisecond of a window long enough that their bursts no longer count:
each source's arrival rate, from a contract rate (sw/mailbox/mailbox.yaml, read from the tree) or a protocol timer
(each clause below, its value read from the tree where the tree states it), times its stated cost. A pass's own cost
(its events' fixed part and its polls' base) is not a source, so it is not a term: it is reported beside the load.
At or above 1.0 no ordering of the work bounds a row; CEILING leaves room for the rows (the round 24 ruling, item 2:
0.70 at 8x8/2if and 32x32/2if). No term is kept as a margin: each has its source, and one without a source fails.

The terms (per millisecond):
  rec.<channel>  aecp, acmp, adp, maap: one record a refill, the fabric's limiter (mailbox.yaml `rate`), per channel
                 and not per stream, so the same at every shape; the burst is a window's first records, not a rate.
  srp            SRP's records, one a refill as rec.<channel>'s, or its retries of a record its participant refused
                 for storage (srp_mbx.c, the poll: one attempt a poll while one waits, for at most SRP_RX_RETRY_MS
                 after its arrival, and no other SRP record taken meanwhile, srp_mbx.c's ready). The retry's own rule
                 bounds it by the passes, not by a rate: the loop runs back to back (ctrl_loop_run), so while one
                 waits every pass retries it. SRP's channel brings the larger of its records and its retries, never
                 both: its records' rate, or the retries' share of a pass that carries one, the retained record's
                 cost over that pass's own cost and its.
  item.reclaim   lwSRP's reclaim of an interface's freed attributes (mrp_reclaim, entered after an SRP record or a
                 build left one to free): two participants a record or a build.
  item.aecp      AECP's owed response, a completed command's notification or a probe: one an AECP record, and one a
                 registration a probe's 250 ms retry (aecp.c; Milan v1.2 5.4.5.3), every interface's registrations.
  item.acmp      ACMP's owed frame: one an ACMP record, one an ADP record (a bound talker's ENTITY_AVAILABLE, Milan
                 v1.2 5.6.4.1) and one a sink's TMR_NO_RESP (Milan v1.2 5.5.2.3, Table 5.26: ACMP_TMR_NO_RESP_MS).
  ticks          a TICK a centisecond (mailbox.yaml tick_ms), each its consumers at the larger of their measured and
                 their stated cost (ctrl_loop.h, CTRL_LOOP_TICK_US).
  item.walk      an interface's registrar walk, at most one an interface a centisecond of lwSRP's timers, and one a
                 build's declaration.
  builds         THE TRANSMIT's builds, one a JoinTime a participant (IEEE 802.1Q-2018 10.7.4.1, Table 10-7; Milan v1.2
                 Table 4.3; srp_mbx.c, SRP_JOIN_CS): the interfaces' builds of both MRPDUs or twice as many of one,
                 whichever costs more.
  item.mrpdu     an MRPDU a build's ring had no room for (A3 of ctrl_loop.h): at most two a build.
  steps          THE STEP: one aged step each CTRL_LOOP_STEP_AGE + 1 centiseconds (ctrl_loop.h).
  timers         each timer slot at its own expiry rate, the sinks that can be due within a window at their timers:
                 ADP's (one an ADP record, which re-arms its delay, Milan v1.2 5.6.3.5.3; each bound sink's discovery
                 aging at the least valid time, 2 s, IEEE 1722.1-2021 6.2.2.5), ACMP's (a sink's TMR_NO_RESP, Milan
                 v1.2 5.5.2.3, Table 5.26), MAAP's probe (IEEE 1722-2016 B.3.4.2, Table B.8: MAAP_PROBE_BASE_MS less
                 MAAP_PROBE_VARIATION_MS) and AECP's (a registration's probe retry, 250 ms, Milan v1.2 5.4.5.3; a
                 descriptor's COUNTERS_CHANGED once a holdoff_ms, Milan v1.2 5.4.5.2, Table 5.22, mailbox.yaml).
  gm             the grandmaster event, coalesced (mailbox.yaml): at most one an interface an Announce and one a peer
                 delay exchange, each at its message interval (IEEE 802.1AS-2011 10.7.2.2, initialLogAnnounceInterval
                 0: 1 s; 11.5.2.2, initialLogPdelayReqInterval 0: 1 s), and one an announce receipt timeout (10.7.3.2,
                 announceReceiptTimeout 3 intervals).

Not terms, each with its reason: a LINK change has no arrival rate (a row's definition, R5, counts one an interface);
THE RETRY's rounds drain a queue a datapath reset leaves, at most AECP_NOTICES_MOST, a burst and not a rate; a pass's
own cost is no source.

usage: python3 -I load_grade.py [--check] [--selftest]
  --check      print the load table and exit 1 if any point is over its ceiling
  --selftest   plant each control and exit 1 unless every one is refused
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
#: The ceiling a point's load is held to (the round 24 ruling, item 2); 1x1/1if is reported, not held.
CEILING = {'8x8/2if': 0.70, '32x32/2if': 0.70}
#: Each point's counts: interfaces, sinks an interface (counted all on each), registrations an interface
#: (aecp.h, AECP_REGISTRATIONS) and the descriptors with counters (each stream's, each AVB interface's and each clock
#: domain's; aecp.h, AECP_NOTICES_MOST's terms).
POINTS = {'1x1/1if': dict(n_if=1, sinks_per_if=2, registrations=16, counter_descriptors=6),
          '8x8/2if': dict(n_if=2, sinks_per_if=8, registrations=16, counter_descriptors=20),
          '32x32/2if': dict(n_if=2, sinks_per_if=16, registrations=16, counter_descriptors=68)}
#: The stated costs in microseconds at each point, each the most measured over every instance plus 5 %, rounded up to
#: 5 us (100 CPU cycles a microsecond on the split CPU at sys, 100 MHz). The polls' base and items at 1x1/1if and
#: 8x8/2if are poll_grade.py's, which the harness holds every measured pass to; THE TRANSMIT's builds and THE STEP's
#: pass are ctrl_loop.h's at 1x1/1if and 8x8/2if; the records', the events' and the centisecond's are the harness's
#: traced handlers' (docs/design/SPLIT_CONTROL_MEMORY.md section 14). 32x32/2if is measured on the 32x32 simulation
#: shape (#859), every cost its own.
STATED_US = {
    '1x1/1if': {'record.srp': 250, 'record.aecp': 200, 'record.acmp': 280, 'record.adp': 105, 'record.maap': 90,
                'event.ADP': 100, 'event.ACMP': 170, 'event.MAAP': 160, 'event.AECP': 60, 'event.TICK': 35,
                'event.GM': 35, 'centisecond': 120, 'events_none': 25},
    '8x8/2if': {'record.srp': 395, 'record.aecp': 255, 'record.acmp': 430, 'record.adp': 230, 'record.maap': 125,
                'event.ADP': 110, 'event.ACMP': 340, 'event.MAAP': 215, 'event.AECP': 95, 'event.TICK': 40,
                'event.GM': 35, 'centisecond': 390, 'events_none': 30},
    '32x32/2if': {}}
#: The least valid_time an ADPDU may carry, in ms: one unit of two seconds (IEEE 1722.1-2021 6.2.2.5), the
#: shortest a bound sink's discovery aging can run.
ADP_LEAST_VALID_MS = 2000
#: The grandmaster event's sources an interface, each once an interval, in ms: an Announce
#: (initialLogAnnounceInterval 0, IEEE 802.1AS-2011 10.7.2.2), a peer delay exchange (initialLogPdelayReqInterval
#: 0, 11.5.2.2) and an announce receipt timeout (announceReceiptTimeout 3 intervals, 10.7.3.2).
GM_INTERVALS_MS = (1000, 1000, 3000)
#: The poll items the load counts (poll_grade.py's names).
ITEMS = ('base', 'reclaim', 'retained', 'mrpdu', 'acmp', 'aecp', 'walk')
#: THE TRANSMIT's and THE STEP's stated costs (ctrl_loop.h), at a point the headers state them for.
HEADER_COSTS = ('CTRL_LOOP_BUILD_PASS_US', 'CTRL_LOOP_BUILD_ONE_PASS_US', 'CTRL_LOOP_STEP_PASS_US')


def macros(root: Path, n_if: int) -> dict[str, int]:
    """The integer constants the load reads from the tree, at that many interfaces."""
    text = ''.join((root / p).read_text() for p in (
        'sw/firmware/ctrl/loop/ctrl_loop.h', 'sw/firmware/ctrl/srp/srp_mbx.c', 'third_party/tsn-c-stack/include/acmp.h',
        'third_party/tsn-c-stack/include/maap.h'))
    found = {m[1]: m[2].split('//')[0].strip() for m in re.finditer(r'^#define (\w+) (.+)$', text, re.M)}

    def value(name: str) -> int:
        """A plain integer, or a ternary on the interface count, the two forms the read constants take."""
        body = found[name]
        plain = re.fullmatch(r'\(?(\d+)u?\)?', body)
        if plain:
            return int(plain[1])
        pick = re.fullmatch(r'\(MBX_N_IF == (\d+)u \? (\d+)u : (\d+)u\)', body)
        if pick is None:
            raise ValueError(f'{name} is {body!r}, neither an integer nor a ternary on MBX_N_IF')
        return int(pick[2] if n_if == int(pick[1]) else pick[3])
    names = (*HEADER_COSTS, 'CTRL_LOOP_TICK_US', 'CTRL_LOOP_STEP_AGE', 'SRP_RX_RETRY_MS', 'SRP_JOIN_CS',
             'ACMP_TMR_NO_RESP_MS', 'MAAP_PROBE_BASE_MS', 'MAAP_PROBE_VARIATION_MS')
    return {n: value(n) for n in names}


def probe_retry_ms(root: Path) -> int:
    """A registration's probe retry (aecp.c: its deadline now + this, Milan v1.2 5.4.5.3)."""
    return int(re.search(r'\.deadline = now\(a\) \+ (\d+)u;', (root / 'sw/firmware/ctrl/aecp/aecp.c').read_text())[1])


def contract(root: Path) -> dict:
    """Each receive channel's refill in ms, the TICK period and the counters' holdoff, from the mailbox contract."""
    y = yaml.safe_load((root / 'sw/mailbox/mailbox.yaml').read_text())
    holdoff = re.search(r'^\s+holdoff_ms: (\d+)', (root / 'sw/mailbox/mailbox.yaml').read_text(), re.M)
    return dict(refill={c['name']: c['rate']['refill_ms'] for c in y['channels']}, tick_ms=y['tick_ms'],
                holdoff_ms=int(holdoff[1]))


def stated(root: Path, point: str, table: dict | None = None) -> dict[str, float]:
    """A point's stated costs: the table's, the polls' (poll_grade.py) and the headers' where the table has none."""
    import poll_grade
    s = POINTS[point]
    c = dict((table or STATED_US)[point])
    if point in ('1x1/1if', '8x8/2if'):
        polls = poll_grade.stated_us(s['n_if'])
        for k in ITEMS:
            c.setdefault('base' if k == 'base' else f'item.{k}', polls[k])
        h = macros(root, s['n_if'])
        c.setdefault('build', h['CTRL_LOOP_BUILD_PASS_US'])
        c.setdefault('build_one', h['CTRL_LOOP_BUILD_ONE_PASS_US'])
        c.setdefault('step', h['CTRL_LOOP_STEP_PASS_US'])
    return c


def load(root: Path, point: str, table: dict | None = None) -> dict[str, float]:
    """Each term's CPU microseconds per millisecond of a long window (a share of the CPU, in thousandths)."""
    s, k, h = POINTS[point], contract(root), macros(root, POINTS[point]['n_if'])
    c, n_if, refill = stated(root, point, table), POINTS[point]['n_if'], contract(root)['refill']
    join_ms = 10 * h['SRP_JOIN_CS']
    both, one = n_if * c['build'], 2 * n_if * c['build_one']
    builds, n_builds = (both, n_if) if both >= one else (one, 2 * n_if)
    out = {f'rec.{ch}': c[f'record.{ch}'] / refill[ch] for ch in ('aecp', 'acmp', 'adp', 'maap')}
    # SRP's channel: its records, or a retained record's retries, never both (the retry's own rule)
    retry_share = 1000 * c['item.retained'] / (c['events_none'] + c['base'] + c['item.retained'])
    out['srp'] = max(c['record.srp'] / refill['srp'], retry_share)
    out['item.reclaim'] = c['item.reclaim'] * 2 * (1 / refill['srp'] + n_builds / join_ms)
    probe = probe_retry_ms(root)
    out['item.aecp'] = c['item.aecp'] * (1 / refill['aecp'] + n_if * s['registrations'] / probe)
    no_resp = h['ACMP_TMR_NO_RESP_MS']
    out['item.acmp'] = c['item.acmp'] * (1 / refill['acmp'] + 1 / refill['adp'] + n_if * s['sinks_per_if'] / no_resp)
    out['ticks'] = (c['event.TICK'] + max(c['centisecond'], h['CTRL_LOOP_TICK_US'])) / k['tick_ms']
    out['item.walk'] = c['item.walk'] * (n_if / k['tick_ms'] + n_builds / join_ms)
    out['builds'] = builds / join_ms
    out['item.mrpdu'] = 2 * n_builds * c['item.mrpdu'] / join_ms
    out['steps'] = c['step'] / (k['tick_ms'] * (h['CTRL_LOOP_STEP_AGE'] + 1))
    maap_ms = h['MAAP_PROBE_BASE_MS'] - h['MAAP_PROBE_VARIATION_MS']
    adp = c['event.ADP'] * (1 / refill['adp'] + s['sinks_per_if'] / ADP_LEAST_VALID_MS)
    acmp = c['event.ACMP'] * s['sinks_per_if'] / no_resp
    aecp = c['event.AECP'] * (n_if * s['registrations'] / probe + s['counter_descriptors'] / k['holdoff_ms'])
    out['timers'] = n_if * (adp + acmp + c['event.MAAP'] / maap_ms) + aecp
    out['gm'] = n_if * c['event.GM'] * sum(1 / ms for ms in GM_INTERVALS_MS)
    return {term: us / 1000 for term, us in out.items()}


def documented() -> set[str]:
    """The terms the module's docstring names, each with its source: a line of its term list."""
    terms = __doc__.split('The terms (per millisecond):')[1].split('Not terms')[0]
    found = set(re.findall(r'^  ([a-z][\w.<>]*) {2,}', terms, re.M))
    channels = re.search(r'^  rec\.<channel> +([a-z, ]+):', terms, re.M)
    return (found - {'rec.<channel>'}) | {f'rec.{ch.strip()}' for ch in channels[1].split(',')}


def unsourced(terms: dict[str, float]) -> list[str]:
    """Each term the load counts with no source in the term list: a term without a source is not kept."""
    return sorted(set(terms) - documented())


def pass_own_us(root: Path, point: str, table: dict | None = None) -> float:
    """A pass's own cost, reported beside the load: its events' fixed part and its polls' base."""
    c = stated(root, point, table)
    return c['events_none'] + c['base']


def findings(root: Path, table: dict | None = None, ceiling: dict | None = None) -> list[str]:
    """Each point over its ceiling, and each point whose table lacks a cost the load needs."""
    out = []
    for point, top in (ceiling or CEILING).items():
        try:
            total = sum(load(root, point, table).values())
        except KeyError as missing:
            out.append(f'{point}: no stated cost {missing}')
            continue
        for term in unsourced(load(root, point, table)):
            out.append(f'{point}: the term {term} has no source in the term list')
        if total > top:
            out.append(f'{point}: the load {total:.3f} is over its ceiling {top:.2f}')
    return out


def report(root: Path, table: dict | None = None) -> list[str]:
    """The load table: each point's total, its ceiling, its pass's own cost and every term by share."""
    lines = ['| Point | Load | Ceiling | A pass\'s own cost, us | Terms by share |', '|---|---:|---:|---:|---|']
    for point in POINTS:
        try:
            terms = load(root, point, table)
        except KeyError as missing:
            lines.append(f'| {point} | none | {CEILING.get(point, "reported")} | | no stated cost {missing} |')
            continue
        ranked = sorted(terms.items(), key=lambda t: -t[1])
        lines.append(f"| {point} | {sum(terms.values()):.3f} | {CEILING.get(point, 'reported')} | "
                     f"{pass_own_us(root, point, table):.0f} | " + ', '.join(f'{t} {v:.3f}' for t, v in ranked) + ' |')
    return lines


def controls(root: Path) -> list[str]:
    """Each planted defect the gate must refuse: the planted names that escaped."""
    base = {p: dict(STATED_US[p]) for p in STATED_US}
    fit = {p: 10.0 for p in CEILING}
    escaped = []
    # a point's load over its ceiling: a cost raised until the total passes it
    raised = {p: dict(v) for p, v in base.items()}
    raised['8x8/2if']['record.acmp'] = 100_000
    if not any('8x8/2if: the load' in f for f in findings(root, raised, {'8x8/2if': 0.70})):
        escaped.append('a cost over the ceiling')
    # a cost the load needs, missing from a point's table
    dropped = {p: dict(v) for p, v in base.items()}
    dropped['8x8/2if'].pop('event.ACMP')
    if not any("no stated cost 'event.ACMP'" in f for f in findings(root, dropped, fit)):
        escaped.append('a stated cost missing')
    # the retry's own rule: a retained record's retries counted once a record, not by the passes
    if not load(root, '8x8/2if', base)['srp'] > base['8x8/2if']['record.srp'] / contract(root)['refill']['srp'] / 1000:
        escaped.append('the retained retry counted once a record')
    # a timer slot counted at one an ordinary pass rather than at its expiry rate: the ACMP slot's term scales with
    # the sinks over TMR_NO_RESP, so doubling the sinks must double it
    one = load(root, '8x8/2if', base)['timers']
    POINTS['8x8/2if']['sinks_per_if'] *= 2
    try:
        two = load(root, '8x8/2if', base)['timers']
    finally:
        POINTS['8x8/2if']['sinks_per_if'] //= 2
    if not two > one:
        escaped.append('a timer slot counted per pass')
    # a term the load counts with no source in its term list (the round 24 ruling, item 5)
    if 'item.unsourced' not in unsourced({**load(root, '8x8/2if', base), 'item.unsourced': 0.0}):
        escaped.append('a term without a source')
    return escaped


#: The planted defects controls() plants, in its order.
CONTROLS = ('a cost over the ceiling', 'a stated cost missing', 'the retained retry counted once a record',
            'a timer slot counted per pass', 'a term without a source')


def ceiling_checks() -> list[tuple[str, bool, str]]:
    """The harness self-test's checks of this gate: every planted defect refused."""
    escaped = controls(ROOT)
    return [(f'the load gate refuses {name}', name not in escaped, 'escaped' if name in escaped else 'refused')
            for name in CONTROLS]


def main() -> int:
    """Print the load table and refuse a point over its ceiling, or plant each control and refuse an escape."""
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()
    rc = 0
    if args.selftest:
        escaped = controls(ROOT)
        for name in escaped:
            print(f'ESCAPED {name}')
        print(f'load gate: {len(CONTROLS) - len(escaped)} of {len(CONTROLS)} planted controls refused')
        rc |= bool(escaped)
    if args.check or not args.selftest:
        print('\n'.join(report(ROOT)))
        found = findings(ROOT)
        for line in found:
            print('OVER', line)
        print('RESULT: FAIL' if found else 'RESULT: PASS')
        rc |= bool(found)
    return rc


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.exit(main())
