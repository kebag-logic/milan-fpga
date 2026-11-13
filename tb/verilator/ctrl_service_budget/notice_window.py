# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The retried notice's row (#665, THE RETRY in ctrl_loop.h): a change notice whose observation port does not answer,
then answers, under the heaviest sustained input the budget stages, timed from the port's answer to its last
recipient's commit against its 20 ms (FR_NFR.md 3.4.1: no extra budget is granted at a retry).

build.py's answering-later variant (a scratch copy of the size fixture, never the formal image) keeps the face block's
stream observation unanswered, as the unmodified fixture has it, until an attempt at or after NOW_MS ANSWER_MS fails.
That attempt calls retry_port_answers, whose entry the testbench reports, and every later attempt answers. So the port
answers just after an attempt failed, and its notice's next retry is a whole backoff away, AECP_RETRY_MAX_MS (aecp.h),
the worst phase the spacing allows. The row starts at that entry (grade.Grader.start, entry:).

Each group registers AECP_REGISTRATIONS controllers on every interface, as aecp_fanout_groups does, so the notice fans
out to the firmware's capacity. A SET_NAME starts a save of the saved-state store, so its steps are in flight under the
load. A BIND_RX of STREAM_INPUT 0 (Milan v1.2 Table 5.22) leaves a GET_STREAM_INFO notice that the unanswered port
retries. From LOAD_MS the group holds save-starved's input until RUN_MS past ANSWER_MS: every receive channel at its
contract refill rate with its bursts (save_window.arrivals), and a grandmaster change as every pass starts
(sim_main.cpp's flood). So no pass takes nothing, and the retry is taken only by an aged step's pass or by a pass of
its own once it is CTRL_LOOP_RETRY_AGE_MS past its time (ctrl_loop.h). Group notice-retried-<k> binds k ms after
notice-retried-0. There are PHASES of them across the retry's spacing, so the answer meets the load's bursts at a
different phase in each.

The row is the notice's fan-out to every registration (grade.py, notify), graded against the notification family's
budget, 20 ms. A row over it fails the run whatever its options record (run.notice_misses). build.py's retry-ageless
plant removes the age limit, and so must put every group's row over its bound. Each channel's longest record under the
load is a row too (save_grade.held, from the mark notice.load).
"""
from __future__ import annotations

import re

import frames as f
import save_window
import scenario
import share

#: NOW_MS from which the variant's stream observation answers, after the attempt there or next fails.
ANSWER_MS = 3150
#: NOW_MS of the SET_NAME, the first BIND_RX (notice-retried-0) and the load's start.
SET_MS, BIND_MS, LOAD_MS = 1700, 3000, 3010
#: How long the load runs past ANSWER_MS, in ms: the longest bound by construction, with room for the row to show it.
RUN_MS = 80
#: The groups, one a millisecond across the retry's 8 ms spacing.
PHASES = 8
#: The row's path: run.notice_misses holds every instance of it to its bound.
PATH = 'notice.retried'
QUEUED = 'notice.queued'
BURST_MS = ANSWER_MS + 6
ROUND_MS = 2
#: The first sequence_id of the registrations.
SEQ = 0x5300


def names() -> list[str]:
    """The groups' names, at any point: build.py's retry-ageless plant runs them all."""
    return [f'notice-retried-{k}' for k in range(PHASES)]


def queued_ms(interfaces: int) -> int:
    """AECP_QUEUED_MS at that many interfaces (aecp_mbx.h, aecp.h, ctrl_loop.h): the bound every queued notice meets."""
    ctrl = scenario.ROOT / 'sw/firmware/ctrl'
    mailbox = (ctrl / 'aecp/aecp_mbx.h').read_text()
    one, two = re.search(r'#define AECP_QUEUED_PASSES \(MBX_N_IF == 1u \? (\d+)u : (\d+)u\)', mailbox).groups()
    spacing = int(re.search(r'#define AECP_RETRY_MAX_MS (\d+)u', (ctrl / 'aecp/aecp.h').read_text()).group(1))
    return spacing + int(one if interfaces == 1 else two) * int(share.share_ms())


def queued_first_ms(interfaces: int) -> int:
    """AECP_QUEUED_FIRST_MS at that many interfaces (aecp_mbx.h): the bound the first notice of a queue meets, T_svc at
    one interface and 22 ms at two (the maintainer's decision of 2026-11-08, FR_NFR.md 3.4.1)."""
    text = (scenario.ROOT / 'sw/firmware/ctrl/aecp/aecp_mbx.h').read_text()
    one, two = re.search(r'#define AECP_QUEUED_FIRST_MS \(MBX_N_IF == 1u \? (\d+)u : (\d+)u\)', text).groups()
    return int(one if interfaces == 1 else two)


def wait_ms(now_ms: int) -> str:
    """A step that waits for NOW_MS to reach now_ms (sim_main.cpp's `wait ms`)."""
    return f'wait ms {now_ms}'


def group(p: scenario.Point, k: int, load_ms: int = LOAD_MS) -> scenario.Group:
    """notice-retried-<k>: the registrations, a save, the bind k ms after BIND_MS, and the load past the answer."""
    ms, aecp, acmp = scenario.MS, scenario.CH['aecp'], scenario.CH['acmp']
    paced = f'wait cycles {scenario.CONTRACT.channels[aecp].refill_ms * ms}'
    load = save_window.arrivals(p, ANSWER_MS + RUN_MS - load_ms)
    offered = {name: sum(1 for _, channel, _ in load if channel == name) for name in scenario.CH}
    g = scenario.Group(f'notice-retried-{k}', sim_ms=ANSWER_MS + RUN_MS + 200,
                       save=dict(loaded=True, offered=offered, origin='notice.load'))
    scenario.ready(g, p)
    controllers = [scenario.FANOUT_CONTROLLER + n for n in range(scenario.registrations())]
    seq = SEQ
    for i in range(p.interfaces):
        for ctl in controllers:
            frame = f.aem_command(f.Aem(p.entity_id, ctl, scenario.CTL_MAC, p.mac, seq), 0x0024, bytes(4))
            g.add(paced, f'frame {i} {frame.hex()}', f'wait tx {aecp} 1 within {50 * ms}',
                  'wait quiet 3 within 2000000')
            seq += 1
    everyone = tuple((ctl, i) for i in range(p.interfaces) for ctl in controllers)
    g.add(wait_ms(SET_MS), f'frame 0 {save_window.set_name(p).hex()}',
          f'wait tx {aecp} {1 + len(everyone)} within {200 * ms}', 'wait quiet 3 within 2000000',
          wait_ms(BIND_MS + k), f'frame 0 {scenario.acmp_cmd(p, "BIND_RX", 0, 0x5f00).hex()}',
          f'wait tx {acmp} 2 within {20 * ms}', wait_ms(load_ms))
    probe = scenario.Probe(f'{g.name}.stream_info.if0', "a retried notice, from its port's answer (THE RETRY)",
                           'notify', 'entry:retry_port_answers', [f'notify:{aecp}:000f:5:0'], recipients=everyone,
                           until='notice.end', path=PATH)
    g.probes.append(probe)
    g.add(f'mark {probe.name}', 'mark notice.load', 'flood gm 1')
    at = 0
    for when, _, step in load:
        cycles = round(when * ms)
        if cycles > at:
            g.add(f'wait cycles {cycles - at}')
            at = cycles
        g.add(step)
    g.add(f'wait cycles {round((ANSWER_MS + RUN_MS - load_ms) * ms) - at}', 'flood gm 0',
          'wait quiet 3 within 2000000', 'mark notice.end')
    return g


def groups(p: scenario.Point) -> list[scenario.Group]:
    """Every phase's group."""
    return [group(p, k) for k in range(PHASES)]


def every_notice(build: dict) -> list[tuple[int, int, int]]:
    """Each notice the model can hold: (command_type, descriptor_type, descriptor_index), in aecp.c's scan order."""
    out = []
    for kind, commands in ((5, (15, 41)), (6, (15, 41)), (9, (39, 40, 41)), (36, (41,))):
        index = 0
        while True:
            try:
                scenario.descriptor_value(build, kind, index)
            except KeyError:
                break
            out += [(command, kind, index) for command in commands]
            index += 1
    return out


def notices_most(interfaces: int) -> int:
    """AECP_NOTICES_MOST at that many interfaces (aecp.h): the most notices a reset can leave pending."""
    text = (scenario.ROOT / 'sw/firmware/ctrl/aecp/aecp.h').read_text()
    one, two = re.search(r'#define AECP_NOTICES_MOST \(MBX_N_IF == 1u \? (\d+)u : (\d+)u\)', text).groups()
    return int(one if interfaces == 1 else two)


def every_group(p: scenario.Point, build: dict, k: int, name: str = 'notice-every',
                load_ms: int = LOAD_MS) -> scenario.Group:
    """notice-every-<k>: group(), with every notice the model holds pending at once, each its own row."""
    if len(every_notice(build)) != notices_most(p.interfaces):
        raise RuntimeError(f'the model holds {len(every_notice(build))} notices, not AECP_NOTICES_MOST at {p.label}')
    g = group(p, k, load_ms)
    g.name = f'{name}-{k}'
    aecp = scenario.CH['aecp']
    template = g.probes.pop()
    everyone = template.recipients
    probes = [scenario.Probe(f'{g.name}.notices.{command:x}.{kind}.{index}.if0',
                             "a queued notice, from its port's answer", 'notify', 'entry:retry_port_answers',
                             [f'notify:{aecp}:{command:04x}:{kind}:{index}'], recipients=everyone,
                             until='notice.end', path=QUEUED, wait_ms=queued_ms(p.interfaces) - scenario.T_SVC_MS)
              for command, kind, index in every_notice(build)]
    g.steps.remove(f'mark {template.name}')
    at = g.steps.index(wait_ms(load_ms))
    g.steps[at:at] = [f'mark {probe.name}' for probe in probes]
    g.probes.extend(probes)
    return g


def every_groups(p: scenario.Point, build: dict) -> list[scenario.Group]:
    """The arm's groups: every notice pending across the spacing, and again with the composed burst past the answer."""
    return ([every_group(p, build, k) for k in range(PHASES)] +
            [every_group(p, build, k, 'notice-burst', BURST_MS) for k in range(PHASES)])
