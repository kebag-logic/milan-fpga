# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""A STREAM_OUTPUT's GET_STREAM_INFO notice when SRP declares or withdraws its Talker (#936; Milan v1.2 5.4.5.2,
Table 5.22; IEEE 1722.1-2021 7.5.2), timed from the event to its last recipient's commit against the asynchronous
notifications' row, 20 ms (FR_NFR.md 3.4.1: an immediate path runs from mailbox RX commitment, and the last required
recipient's commit ends a notification fan-out; backlog and TX-ring backpressure consume the budget).

build.py's talker-notices variant (a scratch copy of the size fixture, never the formal image) is valid-destinations'
fixture, the ACMP source port valid once MAAP holds the range (talker_window.py), with the face block's stream
observation answering zeroed values at every attempt, as answering-ports' does: so the notice is built at its first
attempt, and the row times the declaration's path to it.

Each group registers AECP_REGISTRATIONS controllers on every interface and starts a save, as notice_window's groups do,
then times two events, each a row on source 0's interface:
- the declaration: once MAAP holds the ranges, a PROBE_TX for source 0, answered SUCCESS. Its DA gate opens, the SRP
  delivery hands the gate to SRP, which declares the source's Talker and records it, the delivery takes the record,
  the AECP bridge raises its STREAM_OUTPUT's GET_STREAM_INFO and THE RETRY sends it to every registration. The row
  runs from the PROBE_TX's commit, the event, to the later of its response and its last recipient's notice (path
  notice.declared; Milan v1.2 5.4.5.2: a response precedes its notification).
- the withdrawal: a peer ANNOUNCEs the interface's range from a MAC for which compare_MAC is FALSE (talker_window), so
  MAAP restarts on a new range, its DA gate closes and SRP withdraws the Talker, recorded and noticed the same way. The
  row runs from the ANNOUNCE's commit to the last recipient's notice (path notice.withdrawn). The new range waits two
  LeaveAllTime periods, so no Advertise follows within the group.
Each event comes k ms into a load of RUN_MS, group talker-notice-<k>: every receive channel at its contract refill rate
with its bursts (save_window.arrivals), the event's own channel from one refill period after the event, so its bucket
admits the burst whole, and a grandmaster change as every pass starts (sim_main.cpp's flood), as notice_window's load.
SRP's channel carries a Listener Ready for another entity's stream, the same size as the one save_window sends: a
Listener Ready for source 0's own stream would hold its DA gate open by itself (Milan v1.2 4.3.3.1) and declare it
before the event. There are PHASES groups, one a millisecond, so the event meets the bursts at a different phase in
each.

A row over its 20 ms fails the run whatever its options record, and so does a row with no notice (run.notice_misses,
the probe's refusal). build.py's declared-notice-dropped and declared-notice-delayed plants must put every group's two
rows there, each by its reason.
"""
from __future__ import annotations

import argparse

import answers
import frames as f
import notice_window
import save_window
import scenario
import talker_window

#: The fixture's edits: valid-destinations' ACMP source port, and the face block's stream observation answering.
FIXTURE_EDITS = (*talker_window.FIXTURE_EDITS,
                 ('#include "wire.h"\n', '#include "wire.h"\n#include <string.h>\n'),
                 ('static struct aecp_face image_face;\n',
                  'static struct aecp_face image_face;\n'
                  "// A declared or withdrawn Talker's notice (#936): the stream observation answers every attempt.\n"
                  'static bool n_stream(void *ctx, unsigned i, uint16_t t, uint16_t n, struct aecp_stream_info *v)\n'
                  '{ (void)ctx; (void)i; (void)t; (void)n; memset(v, 0, sizeof *v); return true; }\n'),
                 ('    aecp_face_init(&image_face,&image_platform);\n',
                  '    aecp_face_init(&image_face,&image_platform);\n    image_face.ports.stream=n_stream;\n'))
#: NOW_MS of the SET_NAME, the declaration's load and the withdrawal's.
SET_MS, DECLARE_MS, WITHDRAW_MS = 1700, 3000, 3600
#: How long each load runs past its start, in ms: notice_window's, past the bound with room for the row to show it.
RUN_MS = notice_window.RUN_MS
#: The groups, one a millisecond into the load.
PHASES = 8
#: The source whose Talker is declared and withdrawn, and the rows' paths, which run.notice_misses holds.
SOURCE = 0
DECLARED, WITHDRAWN = 'notice.declared', 'notice.withdrawn'
PATHS = (DECLARED, WITHDRAWN)
#: The PROBE_TX's sequence_id.
SEQ = 0x5e00
#: The stream SRP's channel carries Listener Ready for under the load: another entity's, BRIDGE_MAC's first.
OTHER_STREAM = scenario.BRIDGE_MAC << 16


def names() -> list[str]:
    """The groups' names, at any point: the plants run them all."""
    return [f'talker-notice-{k}' for k in range(PHASES)]


#: The talker arms build.py builds (scratch copies of the size fixture, never the formal image): valid-destinations
#: (#895, talker_window.py) and talker-notices (#936), valid-destinations with the stream observation answering.
VARIANTS = {'valid-destinations': list(talker_window.FIXTURE_EDITS), 'talker-notices': list(FIXTURE_EDITS)}
#: The planted defects build.py builds for this arm, as its MUTATIONS: (file under sw/firmware/ctrl, anchor,
#: replacement, control groups, variant). The dropped notice: the AECP bridge raises no STREAM_OUTPUT's GET_STREAM_INFO
#: from SRP's record, so neither row of a group has a notice to end at. The late notice: the bridge holds SRP's record
#: 25 ms from the pass that first sees it, so both rows of every group are committed past their 20 ms.
PLANTS = {
    'declared-notice-dropped': ('app/ctrl_app_aecp.c', '\t\t\t\taecp_changed(&c->aecp->core, 6, n, 1u);\n',
                                '\t\t\t\t(void)n;\n', ','.join(names()), 'talker-notices'),
    'declared-notice-delayed': ('app/ctrl_app_aecp.c', '\tuint32_t noticed = c->app->srp_noticed;\n',
                                '\tstatic uint32_t held_since;\n\tstatic bool holding;\n'
                                '\tuint32_t noticed = c->app->srp_noticed;\n'
                                '\tif (noticed != 0u && !holding) {\n\t\tholding = true;\n'
                                '\t\theld_since = c->aecp->core.now;\n\t}\n'
                                '\tif (noticed != 0u && c->aecp->core.now - held_since < 25u) {\n'
                                '\t\tnoticed = 0u;\n\t}\n'
                                '\tholding = holding && noticed == 0u;\n',
                                ','.join(names()), 'talker-notices'),
}
#: Each plant's finding, which run.verdict requires of both rows of every group: no notice to end at, or a notice
#: later than its bound.
CONTROLS = {'declared-notice-dropped': 'missing', 'declared-notice-delayed': 'late'}


def other_listener() -> bytes:
    """A bridge's Listener Ready for another entity's stream (IEEE 802.1Q-2018 35.2.2.8), as listener_ready's."""
    return f.msrp(scenario.BRIDGE_MAC, [f.mrp_message(3, f.be(OTHER_STREAM, 8), [1], four_packed=[2])])


def loaded(g: scenario.Group, p: scenario.Point, probe: scenario.Probe, channel: str, event: str, k: int) -> None:
    """The event k ms into a load of RUN_MS, its own channel's load from one refill period after it, and the end mark
    that bounds the row's search."""
    ms = scenario.MS
    own = scenario.listener_ready(p).hex()
    other = other_listener().hex()
    if len(own) != len(other):
        raise ValueError("the other stream's Listener Ready is not the size of the load's")
    refill = scenario.CONTRACT.channels[scenario.CH[channel]].refill_ms
    timeline = [(when, step.replace(own, other) if name == 'srp' else step)
                for when, name, step in save_window.arrivals(p, RUN_MS) if name != channel]
    timeline += [(k + refill + when, step) for when, name, step in save_window.arrivals(p, RUN_MS - k - refill)
                 if name == channel]
    timeline.append((k, scenario.tagged(event, probe.name)))
    g.probes.append(probe)
    g.add(f'mark {probe.name}', 'flood gm 1')
    at = 0
    for when, step in sorted(timeline, key=lambda a: a[0]):
        cycles = round(when * ms)
        if cycles > at:
            g.add(f'wait cycles {cycles - at}')
            at = cycles
        g.add(step)
    g.add(f'wait cycles {round(RUN_MS * ms) - at}', 'flood gm 0', 'wait quiet 3 within 2000000',
          f'mark {probe.until}')


def group(p: scenario.Point, k: int) -> scenario.Group:
    """talker-notice-<k>: the registrations, a save, then the declaration and the withdrawal, each k ms into a load."""
    ms, aecp, acmp, maap = scenario.MS, scenario.CH['aecp'], scenario.CH['acmp'], scenario.CH['maap']
    if talker_window.reversed_mac(talker_window.PEER_MAC) >= talker_window.reversed_mac(p.mac):
        raise ValueError(f'the peer {talker_window.PEER_MAC:012x} does not take the range of {p.mac:012x} (B.3.6.4)')
    paced = f'wait cycles {scenario.CONTRACT.channels[aecp].refill_ms * ms}'
    g = scenario.Group(f'talker-notice-{k}', sim_ms=WITHDRAW_MS + RUN_MS + 400)
    scenario.ready(g, p)
    controllers = [scenario.FANOUT_CONTROLLER + n for n in range(scenario.registrations())]
    seq = notice_window.SEQ
    for i in range(p.interfaces):
        for ctl in controllers:
            frame = f.aem_command(f.Aem(p.entity_id, ctl, scenario.CTL_MAC, p.mac, seq), 0x0024, bytes(4))
            g.add(paced, f'frame {i} {frame.hex()}', f'wait tx {aecp} 1 within {50 * ms}',
                  'wait quiet 3 within 2000000')
            seq += 1
    everyone = tuple((ctl, i) for i in range(p.interfaces) for ctl in controllers)
    g.add(notice_window.wait_ms(SET_MS), f'frame 0 {save_window.set_name(p).hex()}',
          f'wait tx {aecp} {1 + len(everyone)} within {200 * ms}', 'wait quiet 3 within 2000000')
    i = SOURCE % p.interfaces
    notice = f'notify:{aecp}:000f:6:{SOURCE}'
    declared = scenario.Probe(f'{g.name}.declared.if{i}', "a Talker declared, from its PROBE_TX's commit to its "
                              "STREAM_OUTPUT's notice to every registration (#936)", 'notify', f'rxc:{acmp}',
                              [f'resp:{acmp}:{SEQ:x}', notice], expect=answers.acmp('PROBE_TX_RESPONSE', 'SUCCESS'),
                              recipients=everyone, until=f'{g.name}.declared.end', path=DECLARED)
    g.add(notice_window.wait_ms(DECLARE_MS))
    loaded(g, p, declared, 'acmp', f'frame {i} {scenario.talker_cmd(p, "PROBE_TX", SOURCE, SEQ).hex()}', k)
    withdrawn = scenario.Probe(f'{g.name}.withdrawn.if{i}', "a Talker withdrawn as MAAP loses its range, from the "
                               "ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936)",
                               'notify', f'rxc:{maap}', [notice], recipients=everyone,
                               until=f'{g.name}.withdrawn.end', path=WITHDRAWN)
    g.add(notice_window.wait_ms(WITHDRAW_MS))
    loaded(g, p, withdrawn, 'maap',
           f'reply {i} {maap} 15:{f.MAAP_ANNOUNCE:02x} on={i} 6={talker_window.PEER_MAC:012x}', k)
    return g


def groups(p: scenario.Point) -> list[scenario.Group]:
    """Every phase's group."""
    return [group(p, k) for k in range(PHASES)]


def declared_verdict(args: argparse.Namespace, groups: list, refusals: list, late: list) -> int:
    """A talker-notice plant's exit status (talker_notice.PLANTS): caught where both rows of every group fail their
    check for the plant's reason, each named by its row: no notice to end at for the dropped notice, a notice later
    than its bound for the delayed one."""
    want = sorted(p.name for g in groups for p in g.probes if p.path in PATHS)
    if CONTROLS[args.mutation] == 'missing':
        named = sorted(r.partition(':')[0] for r in refusals if ': no end: no notification to ' in r)
        caught = named == want and len(named) == len(refusals)
        reason = 'with no notice'
    else:
        named = sorted(m.partition(':')[0] for m in late if " after its event's commit, over its bound " in m)
        caught = named == want and not refusals
        reason = 'with their notice later than its bound'
    print(f'CONTROL {args.mutation} {"caught" if caught else "ESCAPED"}: {len(named)} of {len(want)} '
          f'talker-notice row(s) {reason} ({", ".join(named) or "none"}), {len(refusals)} refusal(s)')
    return 0 if caught else 1
