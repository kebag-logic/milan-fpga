# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The records that register a peer's Talkers (#977): every STREAM_INPUT bound, then its Talker registered, at every
point, in the default (none) arm.

ACMP binds a STREAM_INPUT once its talker answers the probe (Milan v1.2 5.5.3.5.18 step 4); the binding's receive
filter then takes that StreamID's Talker declarations (srp_mbx.c interested_msrp), each an lwSRP attribute, a Registrar
and an indication. Two groups, each after the link settles and every sink is bound to its own stream:

- srp-register, on every interface, srp.register_advertise: one MRPDU declaring a Talker Advertise for each
  STREAM_INPUT, one vector of them (each value its predecessor's plus one, IEEE 802.1Q-2018 35.2.2.8.4), every one
  JoinIn: each Registrar MT to IN (Table 10-4), each attribute created, its indication and its observation.
- srp-register-burst, on interface 0: the fastest registering burst the MRP state machines allow, on every receive
  channel's flood at its contract rate (save_window.arrivals). A peer's participant transmits at most three MRPDUs in
  any 1.5 x JoinTime (IEEE 802.1Q-2018 10.7.11), JoinTime at least 180 ms (Milan v1.2 Table 4.3), so the burst is
  TRIPLES triples of MRPDUs, each triple's first at least WINDOW_MS after the previous triple's first. Each MRPDU
  declares every STREAM_INPUT's Talker JoinIn, the kinds alternating Advertise, Failed, Advertise...: a JoinIn of one
  kind replaces a registered other (35.2.6; lwSRP's attr_replaces) and the replaced one leaves at once (Milan v1.2
  4.2.7.2.2), so every record of the burst registers every input anew. The last triple's first MRPDU is the peer's
  LeaveAll (10.7.4.3, 10.8.2.5) on the kind registered then and its re-declaration of every input after it, the
  alternation resuming in the next. Each triple arrives LEAD_MS before one of ACMP's flood bursts, and the SRP flood
  burst after it carries three records fewer, so SRP's bucket admits every record as the flood alone does. Each
  triple's records are probes of their own (srp.register_burst, each to its pass's end within T_svc: the drain charges
  a registering record its registrations, so it may wait for a slice that holds it, #977's ruling of 2026-11-23,
  item 4), and its third is also the start of our MRPDU's row (srp.register_tx: the Listener declarations the
  registrations change, sent at the participant's next transmit opportunity, a JoinTime's wait). The last record
  of ACMP's and of AECP's first flood burst at or after each triple are those channels' rows under it
  (acmp.register_burst, aecp.register_burst: a channel's last record of its burst), each to its response.
"""
from __future__ import annotations

import answers
import frames as f
import scenario

NAME = 'srp-register'
#: The talker the group's Talkers are declared by, and their streams: stream k's StreamID and destination are the
#: first's plus k, as a vector increments them (35.2.2.8.4).
STREAM = 0x0C0D0E0F10020000
STREAM_DA = 0x91E0F000FD00
VID = 2
#: The settle after the link comes up: the startup declarations' builds (the fixture's sources declare nothing, #895).
SETTLE_MS = 200
#: A binding's settle: its PROBE_TX, the answer and the Listener declaration it makes.
BIND_MS = 100
#: The settle after the probes: the passes after the records and the declarations they owe.
AFTER_MS = 300
#: The wait past a Leave for its Registrars' leave timers to run out: lwSRP's LeaveTime, 60 centiseconds
#: (MRP_LEAVE_TIME_CS; IEEE 802.1Q-2018 10.7.11), with the passes after it.
LEAVE_MS = 900
#: The burst: a peer's three MRPDUs in any 1.5 x JoinTime (IEEE 802.1Q-2018 10.7.11) at Milan's shortest JoinTime,
#: 180 ms (Milan v1.2 Table 4.3): a triple at most every WINDOW_MS. TRIPLES triples, the last opening with a LeaveAll.
JOIN_MIN_MS = 180
WINDOW_MS = 1.5 * JOIN_MIN_MS
TRIPLES = 3
#: A triple arrives this long before an ACMP flood burst, in ms: that burst's records queue behind the registering
#: records' slices (tier 1 waits for the slice running, ctrl_loop.c THE TIERS).
LEAD_MS = 1.0
#: MAAP's PROBEs and ANNOUNCE before the flood's MAAP records copy one (scenario.announced), from the link's settle.
ANNOUNCED_MS = 2000
#: Our MRPDU's normative wait: a declaration leaves at its participant's next transmit opportunity, a JoinTime
#: (IEEE 802.1Q-2018 10.7.4.1, Table 10-7), as the srp group's Domain row states.
JOIN_WAIT_MS = 200.0


def talker(k: int) -> bytes:
    """Stream k's Talker Advertise FirstValue (35.2.2.8.2): StreamID, DataFrameParameters, TSpec, PriorityAndRank,
    AccumulatedLatency."""
    return (f.be(STREAM + k, 8) + f.be(STREAM_DA + k, 6) + f.be(VID, 2) + f.be(224, 2) + f.be(1, 2) +
            bytes((0x70,)) + f.be(100_000, 4))


#: Where a flood record's sequence_id is in its frame, the Ethernet header's 14 octets included: an ACMPDU's after
#: its control header, StreamID, three entity IDs, two unique IDs, destination MAC and count (IEEE 1722.1-2021
#: 8.2.1), an AEM command's after its control header, target and controller entity IDs (9.2.1.1).
SEQ_AT = {'acmp': 62, 'aecp': 34}
#: A Talker Failed's FailureInformation: a bridge's ID and Insufficient Bandwidth (35.2.2.8.7, Table 35-6).
BRIDGE_ID = 0x80000E0E0E0E0E01
FAILURE = 1


def talker_failed(k: int) -> bytes:
    """Stream k's Talker Failed FirstValue (35.2.2.8.2): the Advertise's fields and the FailureInformation."""
    return talker(k) + f.be(BRIDGE_ID, 8) + bytes((FAILURE,))


def declared(first: int, count: int, event: int = 1, leave_all: bool = False, failed: bool = False) -> bytes:
    """One MRPDU declaring streams first .. first + count - 1, one vector of them, every one the same event."""
    message = f.mrp_message(2 if failed else 1, talker_failed(first) if failed else talker(first), [event] * count,
                            leave_all=leave_all)
    return f.msrp(scenario.TALKER_A_MAC, [message])


def burst(n: int) -> list[list[bytes]]:
    """The burst's MRPDUs, a list a triple: every input's Talker JoinIn, the kinds alternating from Advertise, so each
    record replaces the kind the one before registered; the last triple's first MRPDU is the peer's LeaveAll on the
    kind registered then and its re-declaration of every input (Registrars IN to LV and back to IN, Table 10-4), the
    alternation resuming after it."""
    out, failed = [], False
    for t in range(TRIPLES):
        triple = []
        for r in range(3):
            leave_all = t == TRIPLES - 1 and r == 0
            if leave_all:
                failed = not failed
            triple.append(declared(0, n, failed=failed, leave_all=leave_all))
            failed = not failed
        out.append(triple)
    return out


def answer(i: int, k: int) -> str:
    """The talker's PROBE_TX_RESPONSE naming stream k (8.2.1)."""
    acmp_ch = scenario.CH['acmp']
    return (f'reply {i} {acmp_ch} 15:{f.ACMP["PROBE_TX"]:02x} 6={scenario.TALKER_A_MAC:012x} '
            f'15={f.ACMP["PROBE_TX_RESPONSE"]:02x} 16={44:04x} 18={STREAM + k:016x} '
            f'54={STREAM_DA + k:012x} 66={VID:04x}')


def bind_every(g: scenario.Group, p: scenario.Point) -> None:
    """Every STREAM_INPUT bound to its own stream, sink k on interface k mod the interfaces."""
    acmp, ms = scenario.CH['acmp'], scenario.MS
    for k in range(p.sinks):
        i = k % p.interfaces
        g.add(f'frame {i} {scenario.acmp_cmd(p, "BIND_RX", k, 0x6000 + k).hex()}',
              f'wait tx {acmp} 2 within {40 * ms}', 'wait quiet 3 within 2000000', answer(i, k),
              f'wait cycles {BIND_MS * ms}', 'wait quiet 3 within 2000000')


def burst_group(p: scenario.Point) -> scenario.Group:
    """srp-register-burst: the burst on interface 0 on every channel's flood (the module's docstring)."""
    import save_window
    srp, acmp, aecp, ms, n = scenario.CH['srp'], scenario.CH['acmp'], scenario.CH['aecp'], scenario.MS, p.sinks
    run_ms = WINDOW_MS * TRIPLES + 2 * JOIN_WAIT_MS + 60
    flood = save_window.arrivals(p, run_ms)
    at = {channel: sorted({w for w, c, _ in flood if c == channel}) for channel in ('srp', 'acmp', 'aecp')}
    # each triple LEAD_MS before an ACMP flood burst, its first at least a refill burst into the flood (the SRP
    # bucket holds its three tokens), each at least WINDOW_MS after the previous one; the SRP flood burst after a
    # triple carries three records fewer, so the channel's bucket admits every record as the flood alone does
    starts = []
    for _ in range(TRIPLES):
        floor = starts[-1] + WINDOW_MS if starts else at['srp'][1]
        starts.append(next(a for a in at['acmp'] if a - LEAD_MS >= floor) - LEAD_MS)
    dropped = {next(w for w in at['srp'] if w > t): 3 for t in starts}
    rows = {}
    for t, start in enumerate(starts):
        for channel in ('acmp', 'aecp'):
            first = next(w for w in at[channel] if w >= start)
            rows[max(k for k, (w, c, _) in enumerate(flood) if c == channel and w == first)] = t
    mrpdus, events = burst(n), []
    for t, start in enumerate(starts):
        for r in range(3):
            events.append((start, 'srp', f'frame 0 {mrpdus[t][r].hex()}', (t, r)))
    probes = []
    for index, (when, channel, step) in enumerate(flood):
        if dropped.get(when) and channel == 'srp':
            dropped[when] -= 1
            continue
        events.append((when, channel, step, rows.get(index)))
    events.sort(key=lambda e: e[0])
    g = scenario.Group(f'{NAME}-burst', sim_ms=650 + max(ANNOUNCED_MS, (BIND_MS + 100) * n) + int(run_ms) + AFTER_MS
                       + 1000)
    scenario.ready(g, p)
    g.add(f'wait cycles {SETTLE_MS * ms}', 'wait quiet 3 within 2000000')
    bind_every(g, p)
    g.add(f'wait cycles {max(0, ANNOUNCED_MS - (BIND_MS + 100) * n - SETTLE_MS) * ms}', 'wait quiet 3 within 2000000',
          'mark burst')
    cycles_at = 0
    for when, channel, step, which in events:
        steps = [step]
        if channel == 'srp' and which is not None:
            t, r = which
            name = f'srp.register_burst.t{t}.r{r}.if0'
            probes.append(scenario.Probe(name, 'a registering record of the burst', 'srp', f'rxc:{srp}',
                                         [f'pass_end:{srp}'], until='burst_end'))
            steps = [f'mark {name}', scenario.tagged(step, name)]
            if r == 2:
                tx = f'srp.register_tx.t{t}.if0'
                probes.append(scenario.Probe(tx, 'our MRPDU after a registering triple (JoinTime wait)', 'srp',
                                             f'rxc:{srp}:{name}', [f'tx:{srp}'], wait_ms=JOIN_WAIT_MS,
                                             until='burst_end'))
                steps = [f'mark {name}', f'mark {tx}', scenario.tagged(step, name)]
        elif which is not None:
            seq = int.from_bytes(bytes.fromhex(step.split()[2])[SEQ_AT[channel]:SEQ_AT[channel] + 2], 'big')
            name = f'{channel}.register_burst.t{which}.if0'
            expect = answers.acmp('GET_RX_STATE_RESPONSE') if channel == 'acmp' else answers.aem(0x0004)
            ch = acmp if channel == 'acmp' else aecp
            probes.append(scenario.Probe(name, f"{channel.upper()}'s last record of its burst at a registering triple",
                                         channel, f'rxc:{ch}', [f'resp:{ch}:{seq:x}'], until='burst_end',
                                         expect=expect))
            steps = [f'mark {name}', scenario.tagged(step, name)]
        cycles = round(when * ms)
        if cycles > cycles_at:
            g.add(f'wait cycles {cycles - cycles_at}')
            cycles_at = cycles
        g.add(*steps)
    g.probes.extend(probes)
    g.add(f'wait cycles {round(run_ms * ms) - cycles_at}', 'wait quiet 3 within 2000000', 'mark burst_end',
          f'wait cycles {AFTER_MS * ms}', 'wait quiet 3 within 2000000')
    return g


def bind_first(g: scenario.Group, p: scenario.Point, count: int) -> None:
    """The first `count` STREAM_INPUTs bound to their own streams, as bind_every binds them all."""
    acmp, ms = scenario.CH['acmp'], scenario.MS
    for k in range(count):
        i = k % p.interfaces
        g.add(f'frame {i} {scenario.acmp_cmd(p, "BIND_RX", k, 0x6000 + k).hex()}',
              f'wait tx {acmp} 2 within {40 * ms}', 'wait quiet 3 within 2000000', answer(i, k),
              f'wait cycles {BIND_MS * ms}', 'wait quiet 3 within 2000000')


def record_values(p: scenario.Point) -> int:
    """V at the point's shape (srp_mbx.h SRP_RECORD_VALUES, poll_grade.record_values)."""
    import poll_grade
    import shape_costs
    return poll_grade.record_values(shape_costs.Shape(p.interfaces, p.sources, p.sinks))


def leave_all_shape(n: int, failed: bool) -> bytes:
    """One MRPDU in the shape lwSRP sends at a LeaveAll (mrp_mad.c): its Talker Message opens with a vector of no
    values, LeaveAll set and its FirstValue zero (IEEE 802.1Q-2018 10.8.2.8), then one single-value vector for each of
    streams 0 .. n - 1, each JoinIn, then the Message's EndMark."""
    value = talker_failed if failed else talker
    vectors = f.be(0x2000, 2) + bytes(len(value(0)))
    for k in range(n):
        vectors += f.be(1, 2) + value(k) + bytes((1 * 36,))
    vectors += b'\0\0'
    message = bytes((2 if failed else 1, len(value(0)))) + f.be(len(vectors), 2) + vectors
    return f.msrp(scenario.TALKER_A_MAC, [message])


def population_groups(p: scenario.Point) -> list[scenario.Group]:
    """The registering records #977's ruling of 2026-11-27 (item 5) measures, each on interface 0 after the link
    settles: srp-register-population, the bound and the kept a record registers together at V (a vector of V + 3
    Talkers from the bound streams, with enough sinks bound that the bound and the kept fill V); srp-register-leaveall,
    with every input bound and its Talker Advertise registered, a LeaveAll MRPDU in lwSRP's own shape declaring every
    input's Talker Failed, each replacing the kind registered (35.2.6); srp-register-swap, the same, then one MRPDU of
    each input's Lv of the registered kind with New of the other; srp-register-lv, the same registered, then one MRPDU
    of each input's Lv alone; srp-register-leavetime, the same left until the leave timers the one record started run
    out, in one centisecond (10.7.11); srp-register-both, every input's JoinIn of both kinds in one MRPDU, the Failed
    replacing the Advertise (35.2.6), at twice V's charge; srp-register-both-owed, the same record with a binding change
    owed as it arrives, two inputs' UNBIND_RX just ahead of it, so the delivery of the pass before the record's makes
    one change and leaves the other owed (#977's ruling of 2026-11-27 on the alone records, item 4: the record's pass
    makes none); and srp-register-messages, every input bound, then one MRPDU
    of eight Listener Messages before one Talker Advertise Message for each input, past the eight Messages the drain
    reads one by one (#977's ruling of 2026-11-27, item 5, and its ruling on round 9's STOP, item 4)."""
    srp, ms, n = scenario.CH['srp'], scenario.MS, p.sinks
    v = record_values(p)
    out = []

    def group(name: str, bound: int, extra_ms: int = 0) -> scenario.Group:
        """The group on interface 0 after the link settles, its first `bound` inputs bound."""
        g = scenario.Group(f'{NAME}-{name}',
                           sim_ms=650 + SETTLE_MS + (BIND_MS + 100) * bound + 400 + AFTER_MS + extra_ms + 500)
        scenario.ready(g, p)
        g.add(f'wait cycles {SETTLE_MS * ms}', 'wait quiet 3 within 2000000')
        bind_first(g, p, bound)
        return g

    def probe(g: scenario.Group, name: str, what: str, frame: bytes) -> None:
        """FRAME on interface 0 as the group's probe NAME, its record held to its own charge."""
        g.probe(scenario.Probe(f'srp.{name}.if0', what, 'srp', f'rxc:{srp}', [f'pass_end:{srp}']),
                f'frame 0 {frame.hex()}', wait=f'cycles {30 * ms}')

    bound = n if n < v else n // 3
    g = group('population', bound)
    probe(g, 'register_population', 'the bound and the kept together at V', declared(0, v + 3))
    g.add(f'wait cycles {AFTER_MS * ms}', 'wait quiet 3 within 2000000')
    out.append(g)
    for name in ('leaveall', 'swap'):
        g = group(name, n)
        probe(g, f'register_{name}_advertise', "every input's Talker Advertise, bound, before the record measured",
              declared(0, n))
        g.add('wait quiet 3 within 2000000')
        if name == 'leaveall':
            probe(g, 'register_leaveall', "a LeaveAll MRPDU in lwSRP's shape, every input replaced",
                  leave_all_shape(n, True))
        else:
            swap = f.msrp(scenario.TALKER_A_MAC, [f.mrp_message(1, talker(0), [5] * n),
                                                   f.mrp_message(2, talker_failed(0), [0] * n)])
            probe(g, 'register_swap', "every input's Lv of the registered kind with New of the other", swap)
        g.add(f'wait cycles {AFTER_MS * ms}', 'wait quiet 3 within 2000000')
        out.append(g)
    # every input's Lv of the registered kind alone (Table 10-4: IN to LV), and the same left to its leave timers,
    # which the one record starts together, so they run out in one centisecond (10.7.11); then every input's JoinIn of
    # both kinds in one MRPDU, the second replacing the first (35.2.6) (#977's ruling on round 9's STOP, item 4)
    for name, extra in (('lv', 0), ('leavetime', LEAVE_MS)):
        g = group(name, n, extra)
        probe(g, f'register_{name}_advertise', "every input's Talker Advertise, bound, before the record measured",
              declared(0, n))
        g.add('wait quiet 3 within 2000000')
        probe(g, f'register_{name}', "every input's Lv of the registered kind alone",
              f.msrp(scenario.TALKER_A_MAC, [f.mrp_message(1, talker(0), [5] * n)]))
        g.add(f'wait cycles {(AFTER_MS + extra) * ms}', 'wait quiet 3 within 2000000')
        out.append(g)
    both = f.msrp(scenario.TALKER_A_MAC, [f.mrp_message(1, talker(0), [1] * n),
                                          f.mrp_message(2, talker_failed(0), [1] * n)])
    for name, owed in (('both', 0), ('both-owed', 2)):
        g = group(name, n)
        g.add(*(f'frame 0 {scenario.acmp_cmd(p, "UNBIND_RX", k, 0x6100 + k).hex()}' for k in range(n - owed, n)))
        probe(g, f'register_{name.replace("-", "_")}', "every input's JoinIn of both kinds in one MRPDU" +
              (', a binding change owed' if owed else ''), both)
        g.add(f'wait cycles {AFTER_MS * ms}', 'wait quiet 3 within 2000000')
        out.append(g)
    g = group('messages', n)
    listeners = [f.mrp_message(3, f.be(STREAM + 0x100 + k, 8), [1], four_packed=[2]) for k in range(8)]
    talkers = [f.mrp_message(1, talker(k), [1]) for k in range(n)]
    probe(g, 'register_messages', 'eight Listener Messages before a Talker Message for each input',
          f.msrp(scenario.TALKER_A_MAC, listeners + talkers))
    g.add(f'wait cycles {AFTER_MS * ms}', 'wait quiet 3 within 2000000')
    out.append(g)
    return out


def groups(p: scenario.Point) -> list[scenario.Group]:
    """The groups: srp-register, every probe on every interface, srp-register-burst on interface 0, and the population
    groups (population_groups)."""
    srp, ms, n = scenario.CH['srp'], scenario.MS, p.sinks
    g = scenario.Group(NAME, sim_ms=650 + SETTLE_MS + (BIND_MS + 100) * n + 100 * p.interfaces + AFTER_MS + 500)
    scenario.ready(g, p)
    g.add(f'wait cycles {SETTLE_MS * ms}', 'wait quiet 3 within 2000000')
    bind_every(g, p)
    for i in range(p.interfaces):
        g.probe(scenario.Probe(f'srp.register_advertise.if{i}', 'Talker Advertise RX for every input, bound',
                               'srp', f'rxc:{srp}', [f'pass_end:{srp}']),
                f'frame {i} {declared(0, n).hex()}', wait=f'cycles {30 * ms}')
    g.add(f'wait cycles {AFTER_MS * ms}', 'wait quiet 3 within 2000000')
    return [g, burst_group(p), *population_groups(p)]
