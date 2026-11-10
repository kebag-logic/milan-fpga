# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The long-window CPU load of every source at its stated arrival bound, by the response-time method's own terms
(#665; docs/design/SPLIT_CONTROL_MEMORY.md section 13), at 1x1/1if, 8x8/2if and 32x32/2if, held to a stated ceiling.

The load is the work the sources bring per millisecond of a window long enough that their bursts no longer count:
each source's arrival rate, from a contract rate (sw/mailbox/mailbox.yaml, read from the tree) or a protocol timer
(each clause below, its value read from the tree where the tree states it), times its stated cost. A pass's own cost
(its events' fixed part and its polls' base) is not a source, so it is not a term: it is reported beside the load.
At or above 1.0 no ordering of the work bounds a row; CEILING leaves room for the rows (#665
issuecomment-6734415848, item 2: 0.70 at 8x8/2if and 32x32/2if). No term is kept as a margin: each has its source,
and one without a source fails.

The terms (per millisecond):
  rec.<channel>  aecp, acmp, adp, maap: one record a refill, the fabric's limiter (mailbox.yaml `rate`), per channel
                 and not per stream, so the same at every shape; the burst is a window's first records, not a rate.
  srp            SRP's records, one a refill as rec.<channel>'s, and its retries of a record its participant refused
                 for storage (srp_mbx.c, the poll, #665 issuecomment-6751196896, item 1): a retry only once a pool
                 returned a block or lwSRP reported an Applicant or Registrar change of the interface since the
                 refusal, and at most one a centisecond, a TICK dispatched since the last (mailbox.yaml tick_ms); no
                 other SRP record is taken while one waits (srp_mbx.c's ready), for at most SRP_RX_RETRY_MS. The
                 retries come at the TICK's rate whatever the records', so SRP's channel brings both. The rule's
                 lines are read from the tree (RETRY_RULE): a retry it does not bound has no source.
  item.reclaim   lwSRP's reclaim of an interface's freed attributes (mrp_reclaim, entered after an SRP record or a
                 build left one to free): two participants a record or a build.
  item.aecp      AECP's owed frame, by what each source sends (#665 issuecomment-6751196896, item 2): an AECP record's
                 response, to one recipient, with a command that changed something its notice to the registered
                 controllers, at most AECP_REGISTRATIONS an AVB interface (Milan v1.2 5.4.5.1; aecp.c, fan_out),
                 the larger of the two once a record; and a registration's probe, its own frame, once its 250 ms
                 retry (aecp.c; Milan v1.2 5.4.5.3), every interface's registrations.
  notices        each descriptor's COUNTERS_CHANGED notice, once a holdoff_ms (Milan v1.2 5.4.5.2, Table 5.22;
                 mailbox.yaml counters_changed), in THE RETRY's rounds, each a round's own at its stated costs
                 (aecp_mbx.h: AECP_ROUND_COLD_US and AECP_NOTICE_US, which round_grade.py holds every round to).
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
                 ADP's (its advertise timer once ADP_ADVERTISE_MS, Milan v1.2 5.6.3.5.9, Table 5.50; one an ADP
                 record, which re-arms its delay, Milan v1.2 5.6.3.5.3; each bound sink's discovery
                 aging at the least valid time, 2 s, IEEE 1722.1-2021 6.2.2.5), ACMP's (a sink's TMR_NO_RESP, Milan
                 v1.2 5.5.2.3, Table 5.26), MAAP's probe (IEEE 1722-2016 B.3.4.2, Table B.8: MAAP_PROBE_BASE_MS less
                 MAAP_PROBE_VARIATION_MS) and AECP's (a registration's probe retry, 250 ms, Milan v1.2 5.4.5.3; a
                 descriptor's COUNTERS_CHANGED once a holdoff_ms, Milan v1.2 5.4.5.2, Table 5.22, mailbox.yaml).
  gm             the grandmaster event, coalesced (mailbox.yaml): at most one an interface an Announce and one a peer
                 delay exchange, each at its message interval (IEEE 802.1AS-2011 10.7.2.2, initialLogAnnounceInterval
                 0: 1 s; 11.5.2.2, initialLogPdelayReqInterval 0: 1 s), and one an announce receipt timeout (10.7.3.2,
                 announceReceiptTimeout 3 intervals).

Not terms, each with its reason: a LINK change has no arrival rate (a row's definition, R5, counts one an interface);
THE RETRY's rounds otherwise drain a queue a datapath reset leaves, at most AECP_NOTICES_MOST, a burst and not a rate,
and AVB_INFO_CHANGED, AS_PATH_CHANGED and AMAP_LIVE_WRITE are coalesced events with no contract rate (mailbox.yaml);
a pass's own cost is no source.

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
#: The ceiling a point's load is held to (#665 issuecomment-6734415848, item 2); 1x1/1if is reported, not held.
CEILING = {'8x8/2if': 0.70, '32x32/2if': 0.70}
#: Each point's counts: interfaces, sinks an interface (counted all on each), registrations an interface
#: (aecp.h, AECP_REGISTRATIONS) and the descriptors with counters (each stream's, each AVB interface's and each clock
#: domain's; aecp.h, AECP_NOTICES_MOST's terms).
POINTS = {'1x1/1if': dict(n_if=1, sinks_per_if=2, registrations=16, counter_descriptors=6),
          '8x8/2if': dict(n_if=2, sinks_per_if=8, registrations=16, counter_descriptors=20),
          '32x32/2if': dict(n_if=2, sinks_per_if=16, registrations=16, counter_descriptors=68)}
#: The stated costs in microseconds at each point, each the most measured over every instance plus 5 %, rounded up to
#: 5 us (100 CPU cycles a microsecond on the split CPU at sys, 100 MHz). At 1x1/1if and 8x8/2if the polls' base and
#: items are poll_grade.py's, which the harness holds every measured pass to, and THE TRANSMIT's builds and THE STEP's
#: pass are ctrl_loop.h's; the records', the events', a centisecond's consumers' and a pass's events' fixed part are
#: this table's, the larger of two traced measurements: every group of arm A on bc98d727's image, and arm A's groups
#: but the save groups, with the answering-every-port arm's, on this image (docs/design/SPLIT_CONTROL_MEMORY.md
#: section 14). 32x32/2if is measured on the 32x32 simulation shape (#859), arm A's groups but the save groups, each
#: cost its own; no group stages a retained record's retry or an owed MRPDU at any point, so they are stated at an SRP
#: record's cost and at a build of one's, as poll_grade.py states them; the shape has no saved state, so THE STEP's
#: pass is stated at ctrl_loop.h's two-interface cost.
STATED_US = {
    '1x1/1if': {'record.srp': 250, 'record.aecp': 205, 'record.acmp': 280, 'record.adp': 105, 'record.maap': 90,
                'event.ADP': 105, 'event.ACMP': 180, 'event.MAAP': 160, 'event.AECP': 60, 'event.TICK': 40,
                'event.GM': 35, 'centisecond': 125, 'events_none': 25,
                'item.aecp.notice': 225, 'item.aecp.response': 50, 'item.aecp.probe': 50},
    '8x8/2if': {'record.srp': 395, 'record.aecp': 260, 'record.acmp': 435, 'record.adp': 235, 'record.maap': 125,
                'event.ADP': 110, 'event.ACMP': 340, 'event.MAAP': 215, 'event.AECP': 95, 'event.TICK': 40,
                'event.GM': 320, 'centisecond': 390, 'events_none': 30,
                'item.aecp.notice': 340, 'item.aecp.response': 65, 'item.aecp.probe': 65},
    '32x32/2if': {'record.srp': 860, 'record.aecp': 205, 'record.acmp': 980, 'record.adp': 735, 'record.maap': 205,
                  'event.ADP': 100, 'event.ACMP': 845, 'event.MAAP': 295, 'event.AECP': 55, 'event.TICK': 30,
                  'event.GM': 25, 'centisecond': 950, 'events_none': 20, 'base': 590, 'item.reclaim': 100,
                  'item.retained': 860, 'item.mrpdu': 7485, 'item.acmp': 665, 'item.aecp.notice': 345,
                  'item.aecp.response': 65, 'item.aecp.probe': 65, 'item.walk': 135,
                  'build': 10810, 'build_one': 7485, 'step': 1030}}
#: The least valid_time an ADPDU may carry, in ms: one unit of two seconds (IEEE 1722.1-2021 6.2.2.5), the
#: shortest a bound sink's discovery aging can run.
ADP_LEAST_VALID_MS = 2000
#: The grandmaster event's sources an interface, each once an interval, in ms: an Announce
#: (initialLogAnnounceInterval 0, IEEE 802.1AS-2011 10.7.2.2), a peer delay exchange (initialLogPdelayReqInterval
#: 0, 11.5.2.2) and an announce receipt timeout (announceReceiptTimeout 3 intervals, 10.7.3.2).
GM_INTERVALS_MS = (1000, 1000, 3000)
#: The poll items the load counts (poll_grade.py's names); AECP's owed frame is the table's, by what each source sends.
ITEMS = ('base', 'reclaim', 'retained', 'mrpdu', 'acmp', 'walk')
#: THE TRANSMIT's and THE STEP's stated costs (ctrl_loop.h), at a point the headers state them for.
HEADER_COSTS = ('CTRL_LOOP_BUILD_PASS_US', 'CTRL_LOOP_BUILD_ONE_PASS_US', 'CTRL_LOOP_STEP_PASS_US')
#: The retained receive's retry rule (#665 issuecomment-6751196896, item 1), each part as the tree states it, read with
#: its white space folded: the poll retries only once a pool returned a block or an Applicant or Registrar of the
#: interface moved since the refusal, and spends the centisecond's retry; the centisecond's consumer gives it back; a
#: refusal records what it saw; each change is marked and each return counted; and the poll is the only retry.
RETRY_RULE = {
    'a retry only once the refusal\'s inputs changed, one a centisecond':
        ('sw/firmware/ctrl/srp/srp_mbx.c', 'if (!i->moved && ctrl_pool_returned == m->pending_freed) { '
         'expire_receive(m); } else if (!m->retry_spent) { m->retry_spent = true; '
         'if (apply_receive(m,&m->pending_rx)) {'),
    'a centisecond\'s retry': ('sw/firmware/ctrl/srp/srp_mbx.c', 'shlan_timer_tick(); m->retry_spent = false;'),
    'what a refusal saw': ('sw/firmware/ctrl/srp/srp_mbx.c', '++m->refused; // What the refusal saw, after every '
                           'change of its own (poll). i->moved = false; m->pending_freed = ctrl_pool_returned; '
                           'return false;'),
    'each Applicant or Registrar change marked': ('sw/firmware/ctrl/srp/srp_mbx.c',
                                                  'i->reclaim = true; i->moved = true;'),
    'each returned block counted': ('sw/firmware/ctrl/port/ctrl_pool.c', 'bin->free_count++; ctrl_pool_returned++;'),
}


def macros(root: Path, n_if: int) -> dict[str, int]:
    """The integer constants the load reads from the tree, at that many interfaces."""
    text = ''.join((root / p).read_text() for p in (
        'sw/firmware/ctrl/loop/ctrl_loop.h', 'sw/firmware/ctrl/srp/srp_mbx.c', 'sw/firmware/ctrl/aecp/aecp_mbx.h',
        'third_party/tsn-c-stack/include/acmp.h', 'third_party/tsn-c-stack/include/maap.h',
        'third_party/tsn-c-stack/include/adp.h'))
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
             'ACMP_TMR_NO_RESP_MS', 'MAAP_PROBE_BASE_MS', 'MAAP_PROBE_VARIATION_MS', 'ADP_ADVERTISE_MS',
             'AECP_NOTICE_US', 'AECP_ROUND_COLD_US')
    return {n: value(n) for n in names}


def probe_retry_ms(root: Path) -> int:
    """A registration's probe retry (aecp.c: its deadline now + this, Milan v1.2 5.4.5.3)."""
    return int(re.search(r'\.deadline = now\(a\) \+ (\d+)u;', (root / 'sw/firmware/ctrl/aecp/aecp.c').read_text())[1])


def retry_unbounded(root: Path, texts: dict[str, str] | None = None) -> list[str]:
    """Each part of the retry rule the tree does not state, and a second retry site: a retry it does not bound."""
    def folded(path: str) -> str:
        """The file's text (or its planted copy), its white space folded."""
        return ' '.join(((texts or {}).get(path) or (root / path).read_text()).split())
    out = [name for name, (path, line) in RETRY_RULE.items() if line not in folded(path)]
    if folded('sw/firmware/ctrl/srp/srp_mbx.c').count('apply_receive(m,&m->pending_rx)') != 1:
        out.append('the poll the only retry')
    return out


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
    # SRP's channel: its records, and a retained record's retries at the TICK's rate (the retry's own rule)
    out['srp'] = c['record.srp'] / refill['srp'] + c['item.retained'] / k['tick_ms']
    out['item.reclaim'] = c['item.reclaim'] * 2 * (1 / refill['srp'] + n_builds / join_ms)
    probe = probe_retry_ms(root)
    # AECP's owed frame by what each source sends: a record's response, or a command's with its notice; a probe's frame
    record_frame = max(c['item.aecp.response'], c['item.aecp.notice'])
    out['item.aecp'] = record_frame / refill['aecp'] + n_if * s['registrations'] * c['item.aecp.probe'] / probe
    out['notices'] = s['counter_descriptors'] * (h['AECP_ROUND_COLD_US'] + h['AECP_NOTICE_US']) / k['holdoff_ms']
    no_resp = h['ACMP_TMR_NO_RESP_MS']
    out['item.acmp'] = c['item.acmp'] * (1 / refill['acmp'] + 1 / refill['adp'] + n_if * s['sinks_per_if'] / no_resp)
    out['ticks'] = (c['event.TICK'] + max(c['centisecond'], h['CTRL_LOOP_TICK_US'])) / k['tick_ms']
    out['item.walk'] = c['item.walk'] * (n_if / k['tick_ms'] + n_builds / join_ms)
    out['builds'] = builds / join_ms
    out['item.mrpdu'] = 2 * n_builds * c['item.mrpdu'] / join_ms
    out['steps'] = c['step'] / (k['tick_ms'] * (h['CTRL_LOOP_STEP_AGE'] + 1))
    maap_ms = h['MAAP_PROBE_BASE_MS'] - h['MAAP_PROBE_VARIATION_MS']
    adp = c['event.ADP'] * (1 / refill['adp'] + 1 / h['ADP_ADVERTISE_MS'] + s['sinks_per_if'] / ADP_LEAST_VALID_MS)
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


def findings(root: Path, table: dict | None = None, ceiling: dict | None = None,
             texts: dict[str, str] | None = None) -> list[str]:
    """Each point over its ceiling, each point whose table lacks a cost the load needs, and a term without its
    source: one the term list does not name, or SRP's retries where the tree states no rule that bounds them."""
    out = [f'the term srp has no source: srp_mbx.c states no {part}' for part in retry_unbounded(root, texts)]
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
    # the retry's own rule: a retained record is retried once a centisecond at most, whatever its records, so SRP's
    # channel brings its records and those retries both (one of them alone is not the rule)
    c8, k = stated(root, '8x8/2if', base), contract(root)
    rule = c8['record.srp'] / k['refill']['srp'] + c8['item.retained'] / k['tick_ms']
    if not load(root, '8x8/2if', base)['srp'] >= rule / 1000 - 1e-9:
        escaped.append('the retained retry counted once a record')
    # the retry's source: a tree whose poll retries with nothing changed, or every pass a change allows, states no rule
    # that bounds the retries, so the term srp has none (#665 issuecomment-6751196896, item 1)
    srp = (root / 'sw/firmware/ctrl/srp/srp_mbx.c').read_text()
    for name, old, new in (('a retry with nothing changed',
                            'if (!i->moved && ctrl_pool_returned == m->pending_freed) {', 'if (false) {'),
                           ('a retry every pass', '                m->retry_spent = true;\n', '')):
        planted = {'sw/firmware/ctrl/srp/srp_mbx.c': srp.replace(old, new)}
        refused = any('the term srp has no source' in f for f in findings(root, base, fit, planted))
        if srp.count(old) != 1 or not refused:
            escaped.append(name)
    # a timer slot counted once an ordinary pass rather than at its expiry rate: ACMP's slot brings each sink's
    # TMR_NO_RESP once ACMP_TMR_NO_RESP_MS, so doubling the sinks adds at least that many more expiries
    one = load(root, '8x8/2if', base)['timers']
    s = POINTS['8x8/2if']
    s['sinks_per_if'] *= 2
    try:
        two = load(root, '8x8/2if', base)['timers']
    finally:
        s['sinks_per_if'] //= 2
    acmp = s['n_if'] * s['sinks_per_if'] * base['8x8/2if']['event.ACMP'] / macros(root, 2)['ACMP_TMR_NO_RESP_MS']
    if not two - one >= acmp / 1000 - 1e-9:
        escaped.append('a timer slot counted per pass')
    # AECP's owed frame charged by what each source sends (#665 issuecomment-6751196896, item 2): a probe costs its own
    # frame, so a dearer probe raises the term by every registration's retries of it and a dearer notice by the records'
    # share alone; one charge for every source (round 24's notice to 32 recipients) moves both together
    raised = {p: dict(v) for p, v in base.items()}
    raised['8x8/2if']['item.aecp.probe'] += 1000
    probes = POINTS['8x8/2if']['n_if'] * POINTS['8x8/2if']['registrations'] / probe_retry_ms(root)
    up = load(root, '8x8/2if', raised)['item.aecp'] - load(root, '8x8/2if', base)['item.aecp']
    noticed = {p: dict(v) for p, v in base.items()}
    noticed['8x8/2if']['item.aecp.notice'] += 1000
    more = load(root, '8x8/2if', noticed)['item.aecp'] - load(root, '8x8/2if', base)['item.aecp']
    if abs(up - probes) > 1e-9 or abs(more - 1 / contract(root)['refill']['aecp']) > 1e-9:
        escaped.append('one owed-frame charge for every AECP source')
    # a term the load counts with no source in its term list (#665 issuecomment-6734415848, item 5)
    if 'item.unsourced' not in unsourced({**load(root, '8x8/2if', base), 'item.unsourced': 0.0}):
        escaped.append('a term without a source')
    return escaped


#: Each arrival bound's period the load reads from the tree, and the terms it sets: halving the period must raise
#: those terms, so a term that does not read its source is refused (each arrival bound's plant).
PERIODS = {'refill.aecp': ('rec.aecp', 'item.aecp'), 'refill.acmp': ('rec.acmp', 'item.acmp'),
           'refill.adp': ('rec.adp', 'item.acmp', 'timers'), 'refill.maap': ('rec.maap',),
           'refill.srp': ('srp', 'item.reclaim'), 'tick_ms': ('ticks', 'item.walk', 'steps', 'srp'),
           'holdoff_ms': ('timers', 'notices'), 'SRP_JOIN_CS': ('builds', 'item.mrpdu', 'item.reclaim', 'item.walk'),
           'CTRL_LOOP_STEP_AGE': ('steps',), 'ACMP_TMR_NO_RESP_MS': ('item.acmp', 'timers'),
           'MAAP_PROBE_BASE_MS': ('timers',), 'ADP_ADVERTISE_MS': ('timers',), 'probe': ('item.aecp', 'timers')}


def halved(name: str) -> tuple:
    """The module's readers with one period halved, as (macros, contract, probe_retry_ms)."""
    m0, c0, p0 = macros, contract, probe_retry_ms

    def m(root: Path, n_if: int) -> dict[str, int]:
        """macros, the period halved if it is one of the headers'."""
        out = m0(root, n_if)
        if name in out:
            out[name] = max(0, out[name] // 2) if name == 'CTRL_LOOP_STEP_AGE' else out[name] / 2
        return out

    def c(root: Path) -> dict:
        """contract, the period halved if it is one of the contract's."""
        out = c0(root)
        if name.startswith('refill.'):
            out['refill'] = dict(out['refill'], **{name[7:]: out['refill'][name[7:]] / 2})
        elif name in out:
            out[name] = out[name] / 2
        return out
    return m, c, (lambda root: p0(root) / 2) if name == 'probe' else p0


def period_controls(root: Path) -> list[str]:
    """Each arrival bound whose halved period leaves its terms' load unchanged: a term not read from its source."""
    escaped = []
    point = '8x8/2if'
    before = load(root, point)
    for name, terms in PERIODS.items():
        g = globals()
        saved = g['macros'], g['contract'], g['probe_retry_ms']
        g['macros'], g['contract'], g['probe_retry_ms'] = halved(name)
        try:
            after = load(root, point)
        finally:
            g['macros'], g['contract'], g['probe_retry_ms'] = saved
        if not sum(after[k] for k in terms) > sum(before[k] for k in terms):
            escaped.append(f'the period {name} not read')
    return escaped


#: The planted defects controls() plants, in its order.
CONTROLS = ('a cost over the ceiling', 'a stated cost missing', 'the retained retry counted once a record',
            'a retry with nothing changed', 'a retry every pass', 'one owed-frame charge for every AECP source',
            'a timer slot counted per pass', 'a term without a source')


def ceiling_checks() -> list[tuple[str, bool, str]]:
    """The harness self-test's checks of this gate: every planted defect refused."""
    escaped = controls(ROOT) + period_controls(ROOT)
    names = (*CONTROLS, *(f'the period {name} not read' for name in PERIODS))
    return [(f'the load gate refuses {name}', name not in escaped, 'escaped' if name in escaped else 'refused')
            for name in names]


def main() -> int:
    """Print the load table and refuse a point over its ceiling, or plant each control and refuse an escape."""
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()
    rc = 0
    if args.selftest:
        escaped = controls(ROOT) + period_controls(ROOT)
        for name in escaped:
            print(f'ESCAPED {name}')
        total = len(CONTROLS) + len(PERIODS)
        print(f'load gate: {total - len(escaped)} of {total} planted controls refused')
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
