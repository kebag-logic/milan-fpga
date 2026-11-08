# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The eight NFR-SCOUT-03 hooks on the target core (#665): bounds, groups, ordering checks and plants.

A hook is a family of the CPU budget harness's measured paths (its probes,
scenario.Probe.family), plus the counter push, which that harness does not
run. Each path is graded against its hook's bound, min(T_svc, the family's
ceiling) plus any normative wait W (FR_NFR.md 3.4.1, the per-family rule of
the owner's decision of 2026-10-29 on #665), and its margin to the family's
normative timeout is recorded beside it. Those are the bounds in the tree at
this base; the amended bounds of the decisions of 2026-11-06 on #665 are a
column for information and grade nothing, until #810 brings them.

Each hook's ordering obligation is checked apart from the budget (#664,
ruling of 2026-10-06, item 4), on the same logs: a check reads the order of
the hook's outputs and the state they carry, never their latency. Each check
counts the instances it applied to, so a check that found nothing to apply
to is reported as not applied, never as passed.

Each hook has two plants, each a scratch copy of the firmware's tree with
one defect (hooks_build.planted): a late service, a spin in the hook's
service path that the hook's bound must catch, and an ordering defect that
the hook's ordering check must catch. Each names the group it runs in and
the words its finding must start with, and a late plant the path it delays,
which that finding must name.
"""
from __future__ import annotations

import dataclasses
import sys
from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_service_budget'))
import frames as f  # noqa: E402  the CPU budget harness's frames, read only
import grade  # noqa: E402  its grader, read only
import scenario  # noqa: E402  its stimulus, read only
from scenario import CH, MS, Group, Point, Probe  # noqa: E402

#: The project service budget, approved by the owner on 2026-10-29 (#665).
T_SVC_MS = 20.0
#: The measured swing of one pass's CPU cycles from data layout alone, 195,050 to 201,540 on the same records
#: (#665, ruling of 2026-11-04): a fit by less than it fits by chance, so a path within its bound by fewer CPU
#: cycles is a finding (NARROW), as a path over it is.
LAYOUT_SWING_CYCLES = 6490
#: The sink's TMR_DELAY, a draw of 0 to 1000 ms between discovering its talker and its PROBE_TX_COMMAND (Milan
#: v1.2 Table 5.29; tsn-c-stack acmp.h, ACMP_TMR_DELAY_MAX_MS).
TMR_DELAY_MAX_MS = 1000.0
#: Each family's normative timeout, against which the margin is recorded (FR_NFR.md 3.4.1): ADP's 2 s random
#: window (Milan v1.2 5.6.3.5.2); a discovery input's ACMP action and ACMP's transaction timeout, 200 ms
#: (Milan v1.2 5.5.2.3, Table 5.26); AECP's response, 240 ms (IEEE 1722.1-2021 9.3.2.6), which a notification
#: shares; MAAP's 500 ms probe interval (IEEE 1722-2016 B.3.4.2, Table B.8); MRP's shortest JoinTime, 180 ms
#: (IEEE 802.1Q-2018 10.7.11; Milan v1.2 Table 4.3).
NORMATIVE_MS = {'adp': 2000.0, 'disc': 200.0, 'acmp': 200.0, 'aecp': 240.0, 'notify': 240.0, 'maap': 500.0,
                'srp': 180.0}
#: A counter push's normative timing: counters update within 1 s (Milan v1.2 5.3.7.7, 5.3.8.10); a push is at
#: most one per descriptor per second (Milan v1.2 5.4.5.2, Table 5.22), the spacing its ordering check reads.
COUNTERS_NORMATIVE_MS = 1000.0
COUNTERS_SPACING_MS = 1000.0
#: GET_COUNTERS (IEEE 1722.1-2021 7.4.42) and the descriptor types whose counters the datapath serves
#: (mailbox.yaml, counters_changed): STREAM_INPUT, STREAM_OUTPUT, AVB_INTERFACE, CLOCK_DOMAIN.
GET_COUNTERS = 0x0029
COUNTER_TYPES = (0x0005, 0x0006, 0x0009, 0x0024)
#: A descriptor the counters source keeps no bit for, whose change posts COUNTERS_CHANGED with ALL set.
UNKEPT_TYPE = 0x0002
#: The bus cycles of a millisecond at the 100 MHz bus (the CPU budget harness's MS).
BUS_MS = MS
#: The amended bounds of the owner's decisions of 2026-11-06 on #665, for information: a table's column, never a
#: grade, as they reach the tree with #810 and this harness re-grades then. SRP/MRP's service is T_svc, no longer
#: min(T_svc, its ceiling). A notice queued behind others is within a bound #810 derives at its point's recipients
#: (Milan v1.2 5.3.4.2: 16 controllers per AVB interface), at most this ceiling, by the point's interfaces.
AMENDED_SRP_MS = 20.0
AMENDED_QUEUED_CEILING_MS = {1: 20.0, 2: 60.0}
#: The paths whose notices queue behind other descriptors' (the ALL push, as one path and per descriptor).
QUEUED_PATH = 'counters.all'


def bound_ms(family: str) -> float:
    """A family's bound: min(T_svc, its 10 % ceiling) (FR_NFR.md 3.4.1; #665, the owner's decision of
    2026-10-29)."""
    return min(T_SVC_MS, scenario.CEILING_MS[family])


def normative_ms(hook: str, family: str) -> float:
    """The normative timeout a path's margin is recorded against."""
    return COUNTERS_NORMATIVE_MS if hook == 'H-COUNTERS' else NORMATIVE_MS[family]


def amended_service_ms(r: dict, interfaces: int) -> float:
    """A graded path's service bound under the amended bounds, for information; its bound where they leave it."""
    if r['hook'] == 'H-SRP':
        return AMENDED_SRP_MS
    if r['path'].startswith(QUEUED_PATH):
        return AMENDED_QUEUED_CEILING_MS[interfaces]
    return bound_ms(r['family'])


def amended_ms(r: dict, interfaces: int) -> float:
    """A graded path's whole amended bound, for information: its service bound, and any W its own bound adds."""
    return r['bound_ms'] - bound_ms(r['family']) + amended_service_ms(r, interfaces)


@dataclasses.dataclass(frozen=True)
class Plant:
    """One planted defect: its edits, each (file in the firmware's tree, unique anchor, replacement), the group
    it runs in, the face arm it needs, the words its hook's finding starts with and, for a late plant, the path it
    delays, which that finding must name: a path its group already misses unplanted cannot catch it."""

    edits: tuple[tuple[str, str, str], ...]
    group: str
    words: str
    arm: str = 'idle'
    probe: str | None = None


#: A spin of 120,000 turns, each a load and a store of the counter in sram, well past every bound: 60,000 took
#: about 60 ms at the 50 MHz CPU, and a turn takes at least half as long at 100 MHz, the memory's latency in bus
#: cycles unchanged. The plants run at the product clock, 100 MHz.
SPIN = '\tfor (volatile uint32_t n = 0; n < 120000u; ++n) {\n\t}\n'


#: The notification loop of aecp.c's fan_out, which transmit calls while a notice is owed; the late plant spins once
#: before a fan-out's first recipient.
NOTIFY_LOOP = '\twhile (a->recipient < total) {'


def late(path: str, anchor: str, group: str, hook: str, probe: str) -> Plant:
    """A late service of the path `probe`: the spin, then the anchor."""
    return Plant(((path, anchor, SPIN + anchor),), group, f'LATE {hook}', probe=probe)


@dataclasses.dataclass(frozen=True)
class Hook:
    """One NFR-SCOUT-03 hook: its families, its normative clauses, its ordering obligation, its check and its two
    plants."""

    name: str
    families: tuple[str, ...]
    clauses: str
    ordering: str
    check: str
    late: Plant
    order: Plant


HOOKS: dict[str, Hook] = {h.name: h for h in (
    Hook('H-ADP', ('adp',), 'Milan v1.2 5.6.3.5; IEEE 1722.1-2021 6.2',
         'an ENTITY_AVAILABLE carries the grandmaster in force when it is built: after a grandmaster change, the '
         'first ENTITY_AVAILABLE carries the new one (Milan v1.2 5.6.3.5.7; IEEE 1722.1-2021 6.2.2.16)',
         'adp_grandmaster',
         late('adp/adp_mbx.c', '\tadp_rx(&i->adp, f->bytes, f->len);\n}', 'control', 'H-ADP', 'control.discover.if0'),
         Plant((('adp/adp_mbx.c', '\t(void)ctx;\n\t*gm_id = mbx_gm_id(interface, domain);\n}',
                 '\tstatic uint64_t before[MBX_N_IF];\n\t(void)ctx;\n\tuint64_t now = mbx_gm_id(interface, domain);'
                 '\n\t*gm_id = before[interface];\n\tbefore[interface] = now;\n}'),),
               'hooks-order-adp', 'ORDER H-ADP')),
    Hook('H-DISC', ('disc',), 'Milan v1.2 5.6.4, Table 5.54; 5.5.2.3, Table 5.26',
         'discovery records are applied in their arrival order: a bound talker\'s ENTITY_DEPARTING then '
         'ENTITY_AVAILABLE leaves its sink discovered, so the sink\'s PROBE_TX_COMMAND follows the ENTITY_AVAILABLE '
         '(Milan v1.2 5.6.4.5.1, 5.6.4.5.3, Table 5.54)',
         'discovery_order',
         late('acmp/acmp_mbx.c', '\t\tacmp_adp_rx(&m->acmp, f->interface, f->bytes, f->len);\n\t\treturn;',
              'hooks-late-disc', 'H-DISC', 'hooks-late-disc.entity_departing.if0'),
         Plant((('acmp/acmp_mbx.c',
                 '\tstruct acmp_mbx *m = ctx;\n\tif ((f->bytes[ACMP_HEADER_BYTES + 1u] & 0x0Fu) <= '
                 'ACMP_ADP_MSG_ENTITY_DEPARTING) {\n\t\tacmp_adp_rx(&m->acmp, f->interface, f->bytes, f->len);\n'
                 '\t\treturn;\n\t}',
                 '\tstruct acmp_mbx *m = ctx;\n\tstatic struct mbx_frame held[MBX_N_IF];\n'
                 '\tstatic bool holding[MBX_N_IF];'
                 '\n\tunsigned type = f->bytes[ACMP_HEADER_BYTES + 1u] & 0x0Fu;\n'
                 '\tif (type == ACMP_ADP_MSG_ENTITY_DEPARTING && f->interface < MBX_N_IF && !holding[f->interface]) {\n'
                 '\t\theld[f->interface] = *f;\n\t\tholding[f->interface] = true;\n\t\treturn;\n\t}\n'
                 '\tif (type <= ACMP_ADP_MSG_ENTITY_DEPARTING) {\n'
                 '\t\tacmp_adp_rx(&m->acmp, f->interface, f->bytes, f->len);\n'
                 '\t\tif (f->interface < MBX_N_IF && holding[f->interface]) {\n'
                 '\t\t\tholding[f->interface] = false;\n'
                 '\t\t\tacmp_adp_rx(&m->acmp, f->interface, held[f->interface].bytes, held[f->interface].len);\n'
                 '\t\t}\n\t\treturn;\n\t}'),),
               'acmp-disc', 'ORDER H-DISC')),
    Hook('H-ACMP', ('acmp',), 'Milan v1.2 5.5.2.3, Table 5.26; IEEE 1722.1-2021 8.2',
         'the commands of one controller are answered in their arrival order, the owed responses first in first out '
         '(MAILBOX_SPLIT.md, ACMP service latency)',
         'acmp_order',
         late('acmp/acmp_mbx.c', '\tacmp_rx(&m->acmp, f->interface, f->bytes, f->len);\n}', 'hooks-late-acmp',
              'H-ACMP', 'hooks-late-acmp.get_rx_state.if0'),
         Plant((('acmp/acmp_mbx.c',
                 '\tstruct acmp_mbx *m = ctx;\n\tacmp_rx(&m->acmp, f->interface, f->bytes, f->len);\n}',
                 '\tstruct acmp_mbx *m = ctx;\n\tstatic struct mbx_frame held;\n\tstatic bool holding;\n'
                 '\tif (!holding) {\n\t\theld = *f;\n\t\tholding = true;\n\t\treturn;\n\t}\n'
                 '\tacmp_rx(&m->acmp, f->interface, f->bytes, f->len);\n\tholding = false;\n'
                 '\tacmp_rx(&m->acmp, held.interface, held.bytes, held.len);\n}'),),
               'hooks-order-acmp', 'ORDER H-ACMP')),
    Hook('H-AECP', ('aecp',), 'IEEE 1722.1-2021 9.3.2.6; Milan v1.2 5.4.3.4',
         'every face value a response promises is committed before that response (ARCHITECTURE_HW_SW_SPLIT.md '
         'section 1; Milan v1.2 5.4.5.2; IEEE 1722.1-2021 7.5.2): a lock, clock source or identify change commits '
         'the face block between the command\'s receive commit and its response',
         'face_before_response',
         late('aecp/aecp_mbx.c', '\taecp_rx(&m->core, f->interface, f->bytes, f->len);\n}', 'hooks-late-aecp',
              'H-AECP', 'hooks-late-aecp.read_descriptor.if0'),
         Plant((('aecp/aecp_face.c',
                 '\t\t\tpublish(f, i, settings, i == home ? stream : NULL, kind == AECP_CHANGE_CONFIGURATION);',
                 '\t\t\tf->owed[i] = true;'),
                ('aecp/aecp.c', '((AECP_WAITS >> cmd) & 1u) != 0u && !applied(a)) {',
                 '((AECP_WAITS >> cmd) & 1u) != 0u && false) {')),
               'aecp', 'ORDER H-AECP')),
    Hook('H-NOTIFY', ('notify',), 'Milan v1.2 5.4.5.2, Table 5.22; IEEE 1722.1-2021 7.5.2',
         'the successful command\'s response is committed before any of its notifications (Milan v1.2 5.4.5.2; '
         'IEEE 1722.1-2021 7.5.2; FR_NFR.md 3.4.1)',
         'response_before_notice',
         Plant((('aecp/aecp.c', NOTIFY_LOOP, '\tif (a->recipient == 0u) {\n' + SPIN.replace('\t', '\t\t')
                 + '\t}\n' + NOTIFY_LOOP),), 'hooks-late-notify', 'LATE H-NOTIFY',
               probe='hooks-late-notify.set_name.if0'),
         Plant((('aecp/aecp.c', 'static bool transmit(struct aecp *a)\n{\n\tif (a->response_owed) {\n',
                 'static bool transmit(struct aecp *a)\n{\n\tstatic uint8_t solicited[AECP_FRAME_BYTES];\n'
                 '\tstatic size_t solicited_bytes;\n\tstatic unsigned solicited_interface;\n\tstatic bool reorder;\n'
                 '\tif (a->response_owed && a->notify && !reorder) {\n'
                 '\t\tmemcpy(solicited, a->response, a->response_bytes);\n'
                 '\t\tsolicited_bytes = a->response_bytes;\n\t\tsolicited_interface = a->response_interface;\n'
                 '\t\treorder = true;\n\t}\n\tif (a->response_owed && !reorder) {\n'),
                ('aecp/aecp.c', '\treturn a->notify && fan_out(a);\n}',
                 '\tif (a->notify && fan_out(a)) {\n\t\treturn true;\n\t}\n\tif (reorder) {\n'
                 '\t\tmemcpy(a->response, solicited, solicited_bytes);\n\t\ta->response_bytes = solicited_bytes;\n'
                 '\t\ta->response_interface = solicited_interface;\n\t\tif (!send(a)) {\n\t\t\treturn true;\n\t\t}\n'
                 '\t\treorder = false;\n\t\ta->response_owed = false;\n\t}\n\treturn false;\n}')),
               'aecp-fanout', 'ORDER H-NOTIFY')),
    Hook('H-COUNTERS', ('notify',), 'Milan v1.2 5.4.5.2, Table 5.22; 5.3.7.7, 5.3.8.10',
         'a descriptor\'s counter pushes to one recipient leave at least 1 s apart at the wire, and a change '
         'while the push is held is coalesced into one later push (Milan v1.2 5.4.5.2, Table 5.22)',
         'counter_spacing',
         Plant((('app/ctrl_app_aecp.c',
                 '\tif (e->type == MBX_EV_TYPE_COUNTERS_CHANGED && !e->every) {\n',
                 '\tif (e->type == MBX_EV_TYPE_COUNTERS_CHANGED && !e->every) {\n' + SPIN),),
               'hooks-counters', 'LATE H-COUNTERS', 'answering', 'counters.first.if0'),
         Plant((('aecp/aecp.c', '(bit == 3u && (e->awaiting_output || (e->counter_sent && !due(a->now, '
                 'e->counter_at)))))', '(bit == 3u && e->awaiting_output))'),),
               'hooks-counters', 'ORDER H-COUNTERS', 'answering')),
    Hook('H-MAAP', ('maap',), 'IEEE 1722-2016 B.3.4.2, B.3.6.6, Table B.8; Milan v1.2 4.3.3.1',
         'the talker DA gate is published before the allocation is reported to the CSR window (maap_mbx.c, range; '
         'Milan v1.2 4.3.3.1): every report the core makes follows its interface\'s DA_GATE publication',
         'maap_gate_before_report',
         late('maap/maap_mbx.c', '\trefresh_demand(m);\n\tmaap_rx(&m->ifs[f->interface].core, f->bytes, f->len);',
              'hooks-late-maap', 'H-MAAP', 'hooks-late-maap.defend.if0'),
         Plant((('maap/maap_mbx.c',
                 '\tm->published_gate[interface] = declaring(m, interface, count, valid);\n'
                 '\t(void)mbx_pub_da_gate(interface, m->published_gate[interface]);\n'
                 '\tm->allocation(m->allocation_ctx, interface, base, count, valid);\n',
                 '\tm->published_gate[interface] = declaring(m, interface, count, valid);\n'
                 '\tm->allocation(m->allocation_ctx, interface, base, count, valid);\n'
                 '\t(void)mbx_pub_da_gate(interface, m->published_gate[interface]);\n'),),
               'maap', 'ORDER H-MAAP')),
    Hook('H-SRP', ('srp',), 'IEEE 802.1Q-2018 10.7.4, 10.7.11, Table 10-7; Milan v1.2 4.2.7.1.1, Table 4.3',
         'the adopted Domain is published (SR_DOMAIN) before the MRPDUs that carry it (srp_mbx.c, change_domain; '
         'MAILBOX_SPLIT.md, contract 2.2): every MRPDU committed after an adopting Domain record follows its '
         'interface\'s SR_DOMAIN publication with ADOPTED set',
         'domain_before_mrpdu',
         late('srp/srp_mbx.c', '    if (!apply_receive(m,frame)) {\n        m->pending_rx = *frame;',
              'hooks-late-srp', 'H-SRP', 'hooks-late-srp.listener_ready.if0'),
         Plant((('srp/srp_mbx.c',
                 '    // The adopted Domain, before the declarations that carry it (SR_DOMAIN).\n'
                 '    (void)mbx_pub_domain(i->index,true,i->domain.priority,i->domain.vid);\n',
                 '    plant_domain_owed[i->index] = true;\n'),
                ('srp/srp_mbx.c', 'static int send_pdu(void *ctx, uint8_t port, const uint8_t *pdu, size_t len)\n{\n',
                 'static bool plant_domain_owed[MBX_N_IF];\n\n'
                 'static int send_pdu(void *ctx, uint8_t port, const uint8_t *pdu, size_t len)\n{\n'),
                ('srp/srp_mbx.c', '    m->owed_len = 0;\n    ++m->transmitted;\n    return 0;\n',
                 '    m->owed_len = 0;\n    ++m->transmitted;\n'
                 '    if (plant_domain_owed[s->interface->index]) {\n'
                 '        plant_domain_owed[s->interface->index] = false;\n'
                 '        (void)mbx_pub_domain(s->interface->index,true,s->interface->domain.priority,'
                 's->interface->domain.vid);\n    }\n    return 0;\n')),
               'srp', 'ORDER H-SRP')),
)}
#: A family's hook; H-COUNTERS shares the notification family and is told apart by its probes' names.
FAMILY_HOOK = {'adp': 'H-ADP', 'disc': 'H-DISC', 'acmp': 'H-ACMP', 'aecp': 'H-AECP', 'notify': 'H-NOTIFY',
               'maap': 'H-MAAP', 'srp': 'H-SRP'}
COUNTERS_PREFIX = 'counters.'


def hook_of(row: dict) -> str:
    """The hook a graded path belongs to."""
    return 'H-COUNTERS' if row['probe'].startswith(COUNTERS_PREFIX) else FAMILY_HOOK[row['family']]


def plants() -> dict[str, tuple[str, Plant]]:
    """Every plant by name: <hook>-late and <hook>-order, each with its hook."""
    out = {}
    for hook in HOOKS.values():
        out[f'{hook.name.lower()[2:]}-late'] = (hook.name, hook.late)
        out[f'{hook.name.lower()[2:]}-order'] = (hook.name, hook.order)
    return out


# ---- the groups this harness adds ----------------------------------------------------------------

def registered(g: Group, p: Point, seq: list[int]) -> tuple[tuple[int, int], ...]:
    """The firmware's registration capacity on every interface, as the fan-out group registers it; the
    recipients."""
    controllers = [scenario.FANOUT_CONTROLLER + n for n in range(scenario.registrations())]
    for i in range(p.interfaces):
        for ctl in controllers:
            frame = f.aem_command(f.Aem(p.entity_id, ctl, scenario.CTL_MAC, p.mac, seq[0]), 0x0024, bytes(4))
            g.add(f'frame {i} {frame.hex()}', f'wait tx {CH["aecp"]} 1 within {50 * MS}', 'wait quiet 3 within 2000000')
            seq[0] += 1
    return tuple((ctl, i) for i in range(p.interfaces) for ctl in controllers)


def refilled_ms() -> int:
    """The longest any channel's token bucket takes to refill from empty, burst x refill_ms (KL_mbx_rx.sv), plus
    one period: a composed window opened after the registrations waits this long, so it opens on full buckets."""
    return max((ch.burst + 1) * ch.refill_ms for ch in scenario.CONTRACT.channels)


def counter_descriptors(build: dict) -> list[tuple[int, int]]:
    """Every (type, index) of the configuration in force whose counters the datapath serves."""
    return [(kind, index) for config, kind, index, _ in scenario.descriptors(build)
            if config == 0 and kind in COUNTER_TYPES]


def notify_end(kind: int, index: int) -> str:
    """The end marker of a GET_COUNTERS push of one descriptor to every recipient."""
    return f'notify:{CH["aecp"]}:{GET_COUNTERS:04x}:{kind}:{index}'


def counters_groups(p: Point, build: dict) -> list[Group]:
    """H-COUNTERS (FR_NFR.md 3.4.2), with the answering face only: the CTR window answers, and the testbench
    drives the counter-change event.

    Every registration is a recipient. A change of STREAM_INPUT 0's counters on interface 0 is pushed to every
    recipient (the first push). 100 ms later a change of a descriptor the source keeps no bit for posts ALL:
    every served descriptor may have moved, so each is pushed (the ALL push), but STREAM_INPUT 0, whose push is
    held until 1 s after its last departure and then sent (the held push, which run.py grades from that
    eligibility). The spacing check reads every push's departure.

    The ALL push is reported both ways until #665 decides between them: as one path, from the change to its last
    push, and as a path per descriptor, from the same change to that descriptor's last push. Every row's mark comes
    before the change, so each starts there; the last descriptor's row ties the whole push's, which is listed first.
    """
    aecp = CH['aecp']
    g = Group('hooks-counters', sim_ms=3600)
    scenario.ready(g, p)
    everyone = registered(g, p, [0x5600])
    served = counter_descriptors(build)
    g.probe(Probe('counters.first.if0', 'GET_COUNTERS push, a change (H-COUNTERS)', 'notify', 'pad:CTR:0',
                  [notify_end(5, 0)], recipients=everyone, path='counters.first'),
            'ctrchg 0 5 0', wait=f'tx {aecp} {len(everyone)} within {500 * MS}')
    g.add(f'wait cycles {100 * MS}')
    others = [(k, n) for k, n in served if (k, n) != (5, 0)]
    rows = [(Probe(f'counters.all.t{k}.i{n}.if0', f'GET_COUNTERS push, descriptor {k} {n} of ALL (H-COUNTERS)',
                   'notify', 'pad:CTR:0', [notify_end(k, n)], recipients=everyone, path=f'counters.all.t{k}.i{n}'), [])
            for k, n in others]
    whole = Probe('counters.all.if0', 'GET_COUNTERS push, every served descriptor (ALL; H-COUNTERS)', 'notify',
                  'pad:CTR:0', [notify_end(k, n) for k, n in others], recipients=everyone, path='counters.all')
    entries = [(whole, []), *rows]
    entries[-1][1].append(f'ctrchg 0 {UNKEPT_TYPE:x} 0')
    g.together(entries, [f'tx {aecp} {len(everyone) * len(others)} within {900 * MS}'])
    g.add(f'wait cycles {1300 * MS}', 'wait quiet 3 within 2000000')
    return [g]


def composed_rows() -> tuple[str, ...]:
    """The composed rows this harness adds: their windows carry the CPU budget harness's defined load."""
    return ('hooks-load-notify', 'hooks-load-counters')


def loaded_notify_group(p: Point) -> Group:
    """H-NOTIFY under the composed load: the AECP ring's burst is fifteen READ_DESCRIPTORs and, last, a SET_NAME
    from a controller outside the registrations, whose fan-out reaches every registration while every other
    channel carries its admitted burst and fifteen grandmaster changes fill the event ring."""
    aecp = CH['aecp']
    g = Group('hooks-load-notify', sim_ms=4500)
    scenario.ready(g, p)
    scenario.announced(g)
    everyone = registered(g, p, [0x5700])
    g.add(f'wait cycles {refilled_ms() * MS}', 'gap 1', 'mark composed')
    scenario.gm_run(g, p)
    scenario.composed_load(g, p, own='aecp')
    burst = scenario.admission('aecp', f.read_descriptor(f.Aem(p.entity_id, scenario.CTL1, scenario.CTL_MAC,
                                                                p.mac, 0), 0, 0))['at_once']
    for n in range(burst - 1):
        frame = f.read_descriptor(f.Aem(p.entity_id, scenario.CTL1, scenario.CTL_MAC, p.mac, 0x7300 + n), 0, 0)
        g.offer('aecp', f'frame 0 {frame.hex()}', frame)
    name = b'loaded'.ljust(64, b'\0')
    payload = f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + name
    frame = f.aem_command(f.Aem(p.entity_id, scenario.CTL2, scenario.CTL_MAC, p.mac, 0x73ff), 0x0010, payload)
    g.probe(Probe('hooks-load-notify.set_name.if0', 'SET_NAME fan-out under the composed load', 'notify',
                  f'rxc:{aecp}', [f'resp:{aecp}:73ff', f'notify:{aecp}:0010:0:0'], expect='aecp_response',
                  recipients=everyone, until='composed_end', path='aecp_fanout.set_name'),
            f'frame 0 {frame.hex()}', wait=f'tx {aecp} {burst + len(everyone)} within {900 * MS}',
            settle='quiet 3 within 50000000')
    g.load['aecp'] = g.load.get('aecp', 0) + 1
    g.add('mark composed_end')
    return g


def loaded_counters_group(p: Point) -> Group:
    """H-COUNTERS under the composed load (answering face): every channel's admitted burst, fifteen grandmaster
    changes, then the counter change, sixteenth on the event ring, pushed to every registration."""
    aecp = CH['aecp']
    g = Group('hooks-load-counters', sim_ms=4500)
    scenario.ready(g, p)
    scenario.announced(g)
    everyone = registered(g, p, [0x5800])
    g.add(f'wait cycles {refilled_ms() * MS}', 'gap 1', 'mark composed')
    scenario.gm_run(g, p)
    scenario.composed_load(g, p, own='')
    g.probe(Probe('counters.loaded.if0', 'GET_COUNTERS push under the composed load (H-COUNTERS)', 'notify',
                  'pad:CTR:0', [notify_end(5, 0)], recipients=everyone, until='composed_end',
                  path='counters.loaded'),
            'ctrchg 0 5 0', wait=f'tx {aecp} {16 + len(everyone)} within {900 * MS}',
            settle='quiet 3 within 50000000')
    g.add('mark composed_end')
    return g


def order_adp_group(p: Point) -> Group:
    """H-ADP's ordering check: a grandmaster change on every interface, then the ENTITY_AVAILABLE it causes after
    its delay (Milan v1.2 5.6.3.5.7, a draw of 0 to 4 s), twice."""
    adp = CH['adp']
    g = Group('hooks-order-adp', sim_ms=11000)
    scenario.ready(g, p, link=False)
    scenario.advertised(g, p)
    for n in (1, 2):
        for i in range(p.interfaces):
            g.add(f'gm {i} 0a0b0c0dfffe{n:02x}{i:02x} 0')
        g.add(f'wait tx {adp} {p.interfaces} within {4500 * MS}', 'wait quiet 3 within 2000000')
    return g


def order_acmp_group(p: Point) -> Group:
    """H-ACMP's ordering check: four GET_RX_STATEs from one controller back to back on every interface, then
    their four responses."""
    acmp = CH['acmp']
    g = Group('hooks-order-acmp', sim_ms=1500)
    scenario.ready(g, p)
    for i in range(p.interfaces):
        g.add(*[f'frame {i} {scenario.acmp_cmd(p, "GET_RX_STATE", i, 0x7400 + 16 * i + n).hex()}' for n in range(4)])
        g.add(f'wait tx {acmp} 4 within {300 * MS}', 'wait quiet 3 within 2000000')
    return g


#: The CPU budget harness's paths whose probe this harness measures again in its own group, with a window that
#: opens after the input's arm: on the platform image a sink can re-arm its aging timer after that harness's
#: mark, and its expiry then falls past that group's window. A refusal of the earlier probe is superseded only
#: where this harness's group measured the same path on the same interface (run.grade_all).
SUPERSEDED = {'acmp.tmr_no_adp': 'hooks-disc-aging'}


def aging_group(p: Point) -> Group:
    """H-DISC's aging (FR_NFR.md 3.4.2), as the CPU budget harness's acmp-disc reaches it: each interface's sink
    bound and its PROBE_TX answered, one interface at a time, and its talker discovered, so its one timer waits only
    on discovery; then an
    ENTITY_AVAILABLE with valid_time 1 (2 s, IEEE 1722.1-2021 6.2.2.5) from its RX_HEAD to TMR_NO_ADP armed, then
    that timer's expiry, from its armed deadline, to its action, with the window opened after the arm. A sink still
    waiting for its PROBE_TX_RESPONSE would keep its timer on that earlier deadline, and the arm would not be
    the ENTITY_AVAILABLE's."""
    acmp, adp = CH['acmp'], CH['adp']
    slot = lambda i: p.interfaces + i               # ACMP's slot of interface i (ctrl_app.h)
    avail = lambda valid, index: f.adp(f.ADP_AVAILABLE, scenario.TALKER_A, scenario.TALKER_A_MAC,
                                       f.Adp(valid_time=valid, talker_sources=1, talker_caps=0x4001,
                                             available_index=index))
    g = Group('hooks-disc-aging', sim_ms=4500)
    scenario.ready(g, p)
    ifs = range(p.interfaces)
    # One interface at a time: probe_answer replies to the newest PROBE_TX the firmware sent, on any interface.
    for i in ifs:
        bind = scenario.acmp_cmd(p, 'BIND_RX', i, 0x7600 + i)
        g.add(f'frame {i} {bind.hex()}', f'wait tx {acmp} 2 within {400 * MS}', 'wait quiet 3 within 2000000',
              scenario.probe_answer(i), 'wait quiet 3 within 2000000')
    g.add(*[f'frame {i} {avail(10, 0).hex()}' for i in ifs], 'wait quiet 3 within 2000000')
    for i in ifs:
        g.probe(Probe(f'hooks-disc-aging.available.if{i}', 'ENTITY_AVAILABLE from its RX_HEAD (H-DISC)', 'disc',
                      f'rxc:{adp}', [f'arm:{slot(i)}'], path='acmp.entity_available'),
                f'frame {i} {avail(1, 1).hex()}', wait=f'tmr {slot(i)} 1 within {400 * MS}')
    g.together([(Probe(f'hooks-disc-aging.tmr_no_adp.if{i}', 'TMR_NO_ADP (H-DISC)', 'disc', f'deadline:{slot(i)}',
                       [f'arm:{slot(i)}'], path='acmp.tmr_no_adp'), []) for i in ifs],
               [f'cycles {2100 * MS}', *[f'tmr {slot(i)} 1 within {800 * MS}' for i in ifs]])
    return g


def late_groups(p: Point) -> list[Group]:
    """One path of each hook with a wait long enough to see a late service end, for the late plants: the CPU
    budget harness's groups wait as long as their paths take unplanted. H-ADP's is that harness's own control
    group."""
    adp, acmp, aecp, maap, srp = (CH[c] for c in ('adp', 'acmp', 'aecp', 'maap', 'srp'))
    talker = f.adp(f.ADP_AVAILABLE, scenario.TALKER_A, scenario.TALKER_A_MAC,
                   f.Adp(valid_time=10, talker_sources=1, talker_caps=0x4001))
    gone = f.adp(f.ADP_DEPARTING, scenario.TALKER_A, scenario.TALKER_A_MAC,
                 f.Adp(valid_time=0, talker_sources=1, talker_caps=0x4001))
    out = []
    g = Group('hooks-late-disc', sim_ms=2500)
    scenario.ready(g, p)
    g.add(f'frame 0 {scenario.acmp_cmd(p, "BIND_RX", 0, 0x7500).hex()}', f'wait tx {acmp} 2 within {400 * MS}',
          'wait quiet 3 within 2000000', f'frame 0 {talker.hex()}', 'wait quiet 3 within 2000000')
    g.probe(Probe('hooks-late-disc.entity_departing.if0', 'ENTITY_DEPARTING from its RX_HEAD (H-DISC)', 'disc',
                  f'rxc:{adp}', [f'tmr:{p.interfaces}'], path='acmp.entity_departing'),
            f'frame 0 {gone.hex()}', wait=f'tmr {p.interfaces} 1 within {400 * MS}')
    out.append(g)
    g = Group('hooks-late-acmp', sim_ms=1500)
    scenario.ready(g, p)
    g.probe(Probe('hooks-late-acmp.get_rx_state.if0', 'GET_RX_STATE', 'acmp', f'rxc:{acmp}', [f'resp:{acmp}:7510'],
                  path='acmp.get_rx_state'),
            f'frame 0 {scenario.acmp_cmd(p, "GET_RX_STATE", 0, 0x7510).hex()}', wait=f'tx {acmp} 1 within {400 * MS}')
    out.append(g)
    g = Group('hooks-late-aecp', sim_ms=1500)
    scenario.ready(g, p)
    frame = f.read_descriptor(f.Aem(p.entity_id, scenario.CTL1, scenario.CTL_MAC, p.mac, 0x7520), 0, 0)
    g.probe(Probe('hooks-late-aecp.read_descriptor.if0', 'READ_DESCRIPTOR type 0', 'aecp', f'rxc:{aecp}',
                  [f'resp:{aecp}:7520'], path='aecp.read_descriptor.t0.i0.c0'),
            f'frame 0 {frame.hex()}', wait=f'tx {aecp} 1 within {400 * MS}')
    out.append(g)
    g = Group('hooks-late-notify', sim_ms=2000)
    scenario.ready(g, p)
    everyone = registered(g, p, [0x7530])
    name = b'late'.ljust(64, b'\0')
    frame = f.aem_command(f.Aem(p.entity_id, scenario.CTL2, scenario.CTL_MAC, p.mac, 0x75ff), 0x0010,
                          f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + name)
    g.probe(Probe('hooks-late-notify.set_name.if0', 'set_name', 'notify', f'rxc:{aecp}',
                  [f'resp:{aecp}:75ff', f'notify:{aecp}:0010:0:0'], recipients=everyone, path='aecp_fanout.set_name'),
            f'frame 0 {frame.hex()}', wait=f'tx {aecp} {1 + len(everyone)} within {400 * MS}')
    out.append(g)
    g = Group('hooks-late-maap', sim_ms=3500)
    scenario.ready(g, p)
    scenario.announced(g)
    g.probe(Probe('hooks-late-maap.defend.if0', 'conflicting PROBE -> DEFEND', 'maap', f'rxc:{maap}', [f'tx:{maap}'],
                  path='maap.defend'),
            scenario.maap_conflict(0), wait=f'tx {maap} 1 within {400 * MS}')
    out.append(g)
    g = Group('hooks-late-srp', sim_ms=3500)
    scenario.ready(g, p)
    scenario.announced(g)
    g.probe(Probe('hooks-late-srp.listener_ready.if0', 'Listener Ready RX (registrar; the fixture grants no licence)',
                  'srp', f'rxc:{srp}', [f'pass_end:{srp}'], path='srp.listener_ready'),
            f'frame 0 {scenario.listener_ready(p).hex()}', wait=f'cycles {400 * MS}')
    out.append(g)
    return out


def groups(p: Point, build: dict) -> list[Group]:
    """Every group of a build, longest first: the CPU budget harness's own (but the fixture's and the boot
    fault's), then this harness's; the counter groups with the answering face only."""
    out = [g for g in scenario.all_groups(p, build) if g.name not in ('fixture', 'boot-fault')]
    out += [loaded_notify_group(p), order_adp_group(p), order_acmp_group(p), aging_group(p), *late_groups(p)]
    if build.get('arm') == 'answering':
        out += [*counters_groups(p, build), loaded_counters_group(p)]
    return sorted(out, key=lambda g: -g.sim_ms)


# ---- grading the logs ----------------------------------------------------------------------------

#: This harness's own observation lines, which the CPU budget harness's parser does not know: the
#: counter-change event and a CPU store to the Milan CSR window (hooks_build.TESTBENCH).
OWN_LINES = ('CTRCHG', 'CSRW')


def split(text: str) -> tuple[str, list[list[str]]]:
    """The log without this harness's own lines, and those lines split."""
    keep, own = [], []
    for line in text.splitlines():
        (own.append(line.split()) if line.split(' ', 1)[0] in OWN_LINES else keep.append(line))
    return '\n'.join(keep) + '\n', own


def parsed(text: str, sys_hz: int, cpu_hz: int) -> tuple[grade.Log, list[list[str]]]:
    """The CPU budget harness's parse of a log, with each counter-change event as a pad (pad:CTR:<if>)."""
    rest, own = split(text)
    log = ORIGINAL_PARSE(rest, sys_hz, cpu_hz)
    log.pads.extend((int(w[1]), 'CTR', int(w[2])) for w in own if w[0] == 'CTRCHG')
    log.pads.sort()
    return log, own


ORIGINAL_PARSE = grade.parse


def graded(text: str, group: Group, spec: dict) -> dict:
    """The CPU budget harness's grade of one group's log, read through parsed(), with this harness's composed
    rows given the defined load of that harness's own rows that carry no LINK event (grade.defined_load)."""
    original = grade.defined_load

    def load(name: str) -> dict[str, int]:
        """This harness's composed rows' load, then the CPU budget harness's own."""
        return original('backlog-owed') if name in composed_rows() else original(name)
    with (patch.object(grade, 'parse', lambda t, s, c: parsed(t, s, c)[0]),
          patch.object(grade, 'COMPOSED_ROWS', (*grade.COMPOSED_ROWS, *composed_rows())),
          patch.object(grade, 'defined_load', load)):
        return grade.grade(text, group, spec['sys_hz'], spec['cpu_hz'])


# ---- the ordering checks -----------------------------------------------------------------------

@dataclasses.dataclass
class Checked:
    """One ordering check's result on one group: the instances it applied to, its findings, and the instances
    the log could not decide (neither applied nor passed)."""

    applied: int = 0
    findings: list[str] = dataclasses.field(default_factory=list)
    undecided: int = 0


def pass_start(log: grade.Log, cycle: int) -> int:
    """The start of the work pass that made the write at cycle, or the cycle itself when none did."""
    for p in log.passes:
        if any(c == cycle for c, _, _ in p.writes):
            return p.start_sys
    return cycle


def gm_steps(group: Group) -> list[tuple[int, int]]:
    """The (interface, grandmaster id) of each `gm` step, in script order."""
    return [(int(s.split()[1]), int(s.split()[2], 16)) for s in group.steps if s.startswith('gm ')]


def adp_grandmaster(log: grade.Log, group: Group, own: list[list[str]], spec: dict) -> Checked:
    """H-ADP: each ENTITY_AVAILABLE committed after a grandmaster change carries a grandmaster in force during
    the pass that built it (gptp_grandmaster_id, frame bytes 54 to 61, IEEE 1722.1-2021 6.2.2.16)."""
    out = Checked()
    changes = [(c, i) for c, k, i in log.pads if k == 'GM']
    steps = gm_steps(group)
    if len(changes) != len(steps):
        out.findings.append(f'ORDER H-ADP: {len(changes)} grandmaster changes observed, {len(steps)} in the script')
        return out
    history = [(c, i, gm) for (c, i), (_, gm) in zip(changes, steps)]
    for c, ch, i, frame in log.tx:
        if ch != CH['adp'] or len(frame) < 62 or frame[15] & 0xF != f.ADP_AVAILABLE:
            continue
        mine = [(cycle, gm) for cycle, k, gm in history if k == i]
        if not mine or mine[0][0] > c:
            continue
        start = pass_start(log, c)
        before = [gm for cycle, gm in mine if cycle <= start]
        allowed = {before[-1] if before else 0, *(gm for cycle, gm in mine if start < cycle <= c)}
        carried = int.from_bytes(frame[54:62], 'big')
        out.applied += 1
        if carried not in allowed:
            out.findings.append(f'ORDER H-ADP: the ENTITY_AVAILABLE committed at bus cycle {c} on interface {i} '
                                f'carries grandmaster {carried:016x}, not the one in force, {sorted(allowed)}')
    return out


def frames_received(log: grade.Log, group: Group, text_replies: list[bytes]) -> list[tuple[int | None, bytes]]:
    """Each frame the script sent, in order, with its receive commit (None when the filter refused it)."""
    sent = []
    replies = iter(text_replies)
    for s in group.steps:
        words = s.split()
        if words[0] == 'frame':
            sent.append(bytes.fromhex(words[2]))
        elif words[0] == 'reply':
            sent.append(next(replies, b''))
    commits = sorted(c for c, *_ in log.rxc)
    refused = sorted(end for end, *_ in log.refused)
    ends = sorted([(c, True) for c in commits] + [(e, False) for e in refused])
    out = []
    for frame, (cycle, committed) in zip(sent, ends):
        out.append((cycle if committed else None, frame))
    return out


def replies_of(text: str) -> list[bytes]:
    """The frames the testbench built from `reply` steps, in order (REPLY lines)."""
    return [bytes.fromhex(line.split()[3]) for line in text.splitlines() if line.startswith('REPLY ')]


def next_adp_record(log: grade.Log, interface: int, after: int) -> int:
    """The receive commit of the interface's next ADP record after `after`, tagged or not; far past the run when
    there is none."""
    return min((c for c, k, inter, _, _ in log.rxc if k == CH['adp'] and inter == interface and c > after),
               default=1 << 62)


def disc_decided_ms() -> float:
    """The shortest window without a PROBE_TX_COMMAND that shows the sink never probed: the ENTITY_AVAILABLE's
    service, the longest TMR_DELAY, then the timer's service to the PROBE_TX_COMMAND, each service at its bound."""
    return TMR_DELAY_MAX_MS + 2 * bound_ms('disc')


def discovery_order(log: grade.Log, group: Group, own: list[list[str]], spec: dict) -> Checked:
    """H-DISC: after a bound talker's ENTITY_DEPARTING then ENTITY_AVAILABLE on an interface, a PROBE_TX_COMMAND
    to that talker is committed on that interface after the AVAILABLE and before the interface's next ADP record,
    tagged or not, which could rediscover the talker. The sink probes after its TMR_DELAY draw, so a window with no
    PROBE_TX_COMMAND decides the instance only when it is longer than disc_decided_ms(); a shorter one leaves it
    undecided, neither applied nor passed."""
    out = Checked()
    adp = CH['adp']
    for i in range(spec['interfaces']):
        records = sorted((c, tag) for c, k, inter, tag, _ in log.rxc if k == adp and inter == i
                         and tag in (f'acmp.entity_departing.if{i}', f'acmp.entity_available.if{i}'))
        for (c0, t0), (c1, t1) in zip(records, records[1:]):
            if not (t0.endswith(f'departing.if{i}') and t1.endswith(f'available.if{i}')):
                continue
            until = next_adp_record(log, i, c1)
            probes = [c for c, ch, inter, fr in log.tx if ch == CH['acmp'] and inter == i and c1 < c < until
                      and len(fr) > 16 and fr[14] == 0xFC and fr[15] & 0xF == f.ACMP['PROBE_TX']]
            if not probes and until - c1 <= disc_decided_ms() * BUS_MS:
                out.undecided += 1
                continue
            out.applied += 1
            if not probes:
                out.findings.append(f'ORDER H-DISC: after the ENTITY_DEPARTING at {c0} and the ENTITY_AVAILABLE at '
                                    f'{c1} on interface {i}, the sink never probed its talker: the departure was '
                                    'applied after the arrival')
    return out


def acmp_order(log: grade.Log, group: Group, own: list[list[str]], spec: dict) -> Checked:
    """H-ACMP: two commands from one controller on one interface, the second received before the first was
    answered, are answered in their arrival order."""
    out = Checked()
    text_replies = spec.get('_replies', [])
    commands = []
    for cycle, frame in frames_received(log, group, text_replies):
        if cycle is None or len(frame) < 64 or frame[14] != 0xFC or frame[15] & 1:
            continue
        commands.append((cycle, int.from_bytes(frame[26:34], 'big'), int.from_bytes(frame[62:64], 'big')))
    answers = {}
    for c, ch, inter, fr in log.tx:
        seq = grade.response_sequence(fr) if ch == CH['acmp'] else None
        if seq is not None and len(fr) > 33:
            answers.setdefault((inter, int.from_bytes(fr[26:34], 'big'), seq), c)
    by_key = {}
    for cycle, controller, seq in commands:
        interface = next((i for i, ctl, s in answers if ctl == controller and s == seq), None)
        if interface is not None:
            by_key.setdefault((interface, controller), []).append((cycle, seq, answers[(interface, controller, seq)]))
    for (interface, controller), rows in by_key.items():
        rows.sort()
        for (c0, s0, a0), (c1, s1, a1) in zip(rows, rows[1:]):
            if c1 >= a0:
                continue
            out.applied += 1
            if a1 < a0:
                out.findings.append(f'ORDER H-ACMP: on interface {interface} the command {s1:#06x} received at {c1} '
                                    f'after {s0:#06x} at {c0} was answered first ({a1} before {a0})')
    return out


#: AECP commands whose change commits the face's settings (aecp_face.c changed): LOCK_ENTITY, SET_CLOCK_SOURCE
#: and SET_CONTROL on IDENTIFY, by their probes' names.
FACE_SETTERS = ('lock_entity', 'unlock_entity', 'set_clock_source', 'set_control_identify_on',
                'set_control_identify_off')


def face_commit_words(spec: dict) -> set[int]:
    """The host-port word of every interface's F_COMMIT (contract 2.3)."""
    contract = scenario.CONTRACT
    offset = {r.name: r.offset for r in contract.face_registers}['F_COMMIT']
    return {(contract.face_base + i * contract.face_stride + offset) // 4 for i in range(spec['interfaces'])}


def face_before_response(log: grade.Log, group: Group, own: list[list[str]], spec: dict) -> Checked:
    """H-AECP: a face-setting command's response is committed after a face commit made since its receive commit."""
    out = Checked()
    words = face_commit_words(spec)
    for probe in group.probes:
        if probe.name.split('.')[1] not in FACE_SETTERS:
            continue
        resp = next((e for e in probe.ends if e.startswith('resp:')), None)
        start = next((c for c, k, i, tag, _ in log.rxc if tag == probe.name), None)
        if resp is None or start is None:
            continue
        seq = int(resp.split(':')[2], 16)
        answer = next((c for c, ch, i, fr in log.tx if c > start and ch == CH['aecp']
                       and grade.response_sequence(fr) == seq), None)
        if answer is None:
            continue
        out.applied += 1
        if not any(start <= c <= answer for c, w, _ in log.writes if w in words):
            out.findings.append(f'ORDER H-AECP: {probe.name}: its response at {answer} precedes any face commit since '
                                f'its receive commit at {start}')
    return out


def response_before_notice(log: grade.Log, group: Group, own: list[list[str]], spec: dict) -> Checked:
    """H-NOTIFY: each fan-out's solicited response is committed before the first of its notifications."""
    out = Checked()
    grader = grade.Grader(log)
    for probe in group.probes:
        resp = next((e for e in probe.ends if e.startswith('resp:')), None)
        notice = next((e for e in probe.ends if e.startswith('notify:')), None)
        start = next((c for c, k, i, tag, _ in log.rxc if tag == probe.name), None)
        if resp is None or notice is None or start is None:
            continue
        ch, seq = int(resp.split(':')[1]), int(resp.split(':')[2], 16)
        answer = next((c for c, k, i, fr in log.tx if c > start and k == ch and grade.response_sequence(fr) == seq),
                      None)
        found, _ = grader.recipients(notice, probe, start, 1 << 62)
        sent = [c for c in found.values() if c is not None]
        if answer is None or not sent:
            continue
        out.applied += 1
        if min(sent) < answer:
            out.findings.append(f'ORDER H-NOTIFY: {probe.name}: a notification at {min(sent)} precedes its response '
                                f'at {answer}')
    return out


def counter_pushes(log: grade.Log) -> dict[tuple[int, int, int, int], list[int]]:
    """Every GET_COUNTERS push at the wire, by (descriptor type, index, recipient, interface): its departures."""
    out: dict[tuple[int, int, int, int], list[int]] = {}
    for c, ch, i, fr in log.wire:
        if ch == CH['aecp'] and grade.causal(fr, GET_COUNTERS, int.from_bytes(fr[38:40], 'big') if len(fr) > 41
                                             else -1, int.from_bytes(fr[40:42], 'big') if len(fr) > 41 else -1):
            key = (int.from_bytes(fr[38:40], 'big'), int.from_bytes(fr[40:42], 'big'),
                   int.from_bytes(fr[26:34], 'big'), i)
            out.setdefault(key, []).append(c)
    return out


def counter_spacing(log: grade.Log, group: Group, own: list[list[str]], spec: dict) -> Checked:
    """H-COUNTERS: one descriptor's pushes to one recipient leave at least COUNTERS_SPACING_MS apart."""
    out = Checked()
    for (kind, index, ctl, i), cycles in counter_pushes(log).items():
        for a, b in zip(cycles, cycles[1:]):
            out.applied += 1
            if b - a < COUNTERS_SPACING_MS * BUS_MS:
                out.findings.append(f'ORDER H-COUNTERS: descriptor {kind:#06x} {index} to {ctl:016x} on interface {i}: '
                                    f'pushes {(b - a) / BUS_MS:.3f} ms apart at the wire, under '
                                    f'{COUNTERS_SPACING_MS:g} ms')
    return out


#: The CSR window's first three words of a MAAP allocation report, in maap_csr.c's order: AAF_CTRL and
#: CRFT_CTRL with their enable cleared, then MAAP_CTRL. The report ends by writing AAF_CTRL and CRFT_CTRL again,
#: so a report is told by its first three stores, never by AAF_CTRL alone. Only interface 0's reports reach the
#: window: the datapath has one (plat/README.md, The ports).
MAAP_REPORT_OFFSET = 0x654
MAAP_REPORT_START = (MAAP_REPORT_OFFSET, 0x750, 0x6CC)


def maap_reports(own: list[list[str]], after: int) -> list[int]:
    """The bus cycle of each MAAP allocation report's first store after `after`."""
    stores = [(int(w[1]), int(w[2], 16)) for w in own if w[0] == 'CSRW' and int(w[1]) > after]
    width = len(MAAP_REPORT_START)
    return [stores[n][0] for n in range(len(stores) - width + 1)
            if tuple(o for _, o in stores[n:n + width]) == MAAP_REPORT_START]


def maap_gate_before_report(log: grade.Log, group: Group, own: list[list[str]], spec: dict) -> Checked:
    """H-MAAP: each allocation report the core makes after the loop's first pass follows an interface-0 DA_GATE
    publication made since the previous report."""
    out = Checked()
    gate = scenario.pub_word(0, 'DA_GATE')
    first = log.passes[0].start_sys if log.passes else 1 << 62
    since = first
    for c in maap_reports(own, first):
        out.applied += 1
        if not any(since <= w < c for w, word, _ in log.writes if word == gate):
            out.findings.append(f'ORDER H-MAAP: the allocation report at {c} follows no DA_GATE publication since '
                                f'{since}')
        since = c
    return out


#: SR_DOMAIN's ADOPTED field (contract 2.2).
def adopted(value: int) -> bool:
    """Whether an SR_DOMAIN word has ADOPTED set."""
    field = next(fl for r in scenario.CONTRACT.pub_registers if r.name == 'SR_DOMAIN' for fl in r.fields
                 if fl.name == 'ADOPTED')
    return bool((value >> field.lsb) & ((1 << field.width) - 1))


def domain_before_mrpdu(log: grade.Log, group: Group, own: list[list[str]], spec: dict) -> Checked:
    """H-SRP: after an adopting Domain record on an interface, its first MRPDU follows an SR_DOMAIN publication
    with ADOPTED set."""
    out = Checked()
    for i in range(spec['interfaces']):
        rx = next((c for c, k, inter, tag, _ in log.rxc if tag == f'srp.domain.if{i}'), None)
        if rx is None:
            continue
        word = scenario.pub_word(i, 'SR_DOMAIN')
        pub = next((c for c, w, v in log.writes if w == word and c > rx and adopted(v)), None)
        sent = next((c for c, ch, inter, _ in log.tx if ch == CH['srp'] and inter == i and c > rx), None)
        if sent is None:
            continue
        out.applied += 1
        if pub is None or pub > sent:
            out.findings.append(f'ORDER H-SRP: the MRPDU committed at {sent} on interface {i} after the Domain record '
                                f'at {rx} precedes its SR_DOMAIN publication ({pub})')
    return out


CHECKS: dict[str, Callable[[grade.Log, Group, list[list[str]], dict], Checked]] = {
    'adp_grandmaster': adp_grandmaster, 'discovery_order': discovery_order, 'acmp_order': acmp_order,
    'face_before_response': face_before_response, 'response_before_notice': response_before_notice,
    'counter_spacing': counter_spacing, 'maap_gate_before_report': maap_gate_before_report,
    'domain_before_mrpdu': domain_before_mrpdu,
}


def ordering(text: str, group: Group, spec: dict) -> dict[str, Checked]:
    """Every hook's ordering check on one group's log."""
    log, own = parsed(text, spec['sys_hz'], spec['cpu_hz'])
    context = {**spec, '_replies': replies_of(text)}
    return {hook.name: CHECKS[hook.check](log, group, own, context) for hook in HOOKS.values()}


def held_push(text: str, group: Group, spec: dict) -> dict | None:
    """H-COUNTERS' held push: STREAM_INPUT 0's push the ALL change caused, held until 1 s after the first push's
    last departure (Milan v1.2 Table 5.22). Its service runs from that eligibility, W the time it was held after
    the change, to its last recipient's commit; None when the group made no such push."""
    if group.name != 'hooks-counters':
        return None
    log, _ = parsed(text, spec['sys_hz'], spec['cpu_hz'])
    changes = sorted(c for c, k, i in log.pads if k == 'CTR')
    pushes = [(c, fr) for c, ch, i, fr in log.tx if ch == CH['aecp'] and grade.causal(fr, GET_COUNTERS, 5, 0)]
    wires = sorted(c for (kind, index, _, _), cycles in counter_pushes(log).items() if (kind, index) == (5, 0)
                   for c in cycles)
    if len(changes) < 2:
        return None
    first = [c for c, _ in pushes if changes[0] <= c < changes[1]]
    second = [c for c, _ in pushes if c > changes[1]]
    departed = [c for c in wires if c < changes[1]]
    if not first or not second or not departed:
        return dict(probe='counters.held.if0', missing=True)
    recipients = len(first)
    if len(second) < recipients:
        return dict(probe='counters.held.if0', missing=True)
    eligible = max(changes[1], max(departed) + int(COUNTERS_SPACING_MS * BUS_MS))
    end = second[recipients - 1]
    return dict(probe='counters.held.if0', change=changes[1], eligible=eligible, end=end,
                wait_ms=round((eligible - changes[1]) / BUS_MS, 5), ms=round((end - eligible) / BUS_MS, 5))
