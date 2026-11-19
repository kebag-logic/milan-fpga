# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""A STREAM_OUTPUT the split's face reports declaring, its whole observation completed by the AECP bridge (#943;
Milan v1.2 5.4.2.10.2, Tables 5.8, 5.11, 5.12; IEEE 1722.1-2021 7.4.15, 7.4.16): the arm that runs that completion,
the group that times its paths, and what its logs must show.

build.py's declaring-outputs variant (a scratch copy of the size fixture, never the formal image) is answering-ports'
fixture with two changes. Its ACMP source port is valid-destinations' (talker_window.py: each source's destination
valid once MAAP holds its interface's range, at base + n), and its stream observation answers as the face block's
does for a declaring output (aecp_face.c, stream): word 0's flags, STREAM_DEST_MAC_VALID among them, in a brief
observation as in a whole one, with the caller's brief kept. So every whole observation of a STREAM_OUTPUT, a
GET_STREAM_INFO's or a SET_STREAM_INFO's, answered or refused, solicited or a notice's, runs the bridge's completion
(ctrl_app_aecp.c, output), and a brief one, a running check's, does not. The bridge's ACMP owner is the fixture's
with its source port entered through completion_source, whose entry the testbench reports (ENTRY). ACMP's and SRP's
own calls of that port pass through the bridge too (ctrl_app_aecp.c interposes on ACMP's env), but none runs inside
an AECP record or a round of THE RETRY, so each entry inside one is one completion: the counts findings() holds.

The arm runs arm B's AECP groups as answering-ports builds them (aecp, aecp-fanout, aecp-largest-notice,
aecp-reboot), so their records are the same commands, and aecp-outputs:
- MAAP's ranges held, AECP_REGISTRATIONS controllers registered on every interface, then a PROBE_TX for source 0,
  answered SUCCESS: SRP declares its Talker and the bridge raises its STREAM_OUTPUT's GET_STREAM_INFO, which THE
  RETRY builds whole, completed, and sends to every registration (#936): a row (notify, its path DECLARED).
- a bridge's Listener Ready for output 0's stream on its interface, which SRP registers: REGISTERING from then on.
- GET_STREAM_INFO of every STREAM_OUTPUT, answered SUCCESS: each a row (aecp, GET).
- SET_STREAM_INFO of output 0 refused after its whole observation: NOT_SUPPORTED, a sub-command Milan v1.2 5.4.2.9
  does not support, and ENTITY_LOCKED, under another controller's lock (7.4.2): each a row (aecp, REFUSED).
- with the egress held (sim_main.cpp, txready), an accepted SET_STREAM_INFO (MSRP_ACC_LAT_VALID) whose response and
  notices to every registration are more than the AECP ring's room, and GET_STREAM_INFO of output 0 behind them: both
  rows run until HOLD_MS after the GET's commit releases the egress (FR_NFR.md 3.4.1: TX-ring backpressure consumes
  the budget) (notify, HELD_SET; aecp, HELD_GET).
Every row is held to its budget, every pass to the share and every THE RETRY round to its stated costs
(round_grade.py), as in every arm. record_classes.py holds each record of this arm that ran the completion to its
class's statement, and refuses a pass whose declaring-outputs leg at a point it holds ran none.

findings() reads the arm's logs (run.py fails the run on any): each AECP record of a whole observation of a
STREAM_OUTPUT ran one completion, each map edit's and each of the largest legal command's ran none (its check is
brief), THE RETRY's rounds ran the declared Talker's, and every GET_STREAM_INFO of a STREAM_OUTPUT that left in
aecp-outputs, response or notice, carries what the completion answers: STREAM_DEST_MAC_VALID, the output's MAAP
address (the pool's, base + n on its interface), REGISTERING for output 0 alone once its Listener is registered, and
no REGISTERING_FAILED (a Listener Ready). build.py's PLANTS put each of its findings there: the completion never run
(none of the evidence), a brief observation completed (the map edits' records), and the completion dearer by a
planted loop (the records record_classes.py holds, over their statement).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import answers
import frames as f
import long_notice
import reboot_group
import scenario
import talker_window

NAME = 'declaring-outputs'
GROUP = 'aecp-outputs'
#: The test-only entry each completion makes (the bridge's ACMP owner's source port), which build.VARIANT_ENTRIES
#: has the testbench report.
ENTRY = 'completion_source'
#: The flags the stream observation answers for a STREAM_OUTPUT: STREAM_FORMAT_VALID, STREAM_ID_VALID,
#: MSRP_ACC_LAT_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID (IEEE 1722.1-2021 Table 7-131), a declaring one.
DECLARING = 0xF2000000
DEST_MAC_VALID, REGISTERING_FAILED, REGISTERING = 0x10000000, 0x00000040, 0x00000001
#: The fixture's edits, applied after answering-ports': valid-destinations' source port, the face's stream answer for
#: a declaring output, and the bridge's ACMP owner entering the source port through completion_source.
ANSWERING_STREAM = ('static bool b_stream(void *ctx, unsigned i, uint16_t t, uint16_t n, struct aecp_stream_info *v)\n'
                    '{ (void)ctx; (void)i; (void)t; (void)n; memset(v, 0, sizeof *v); return true; }\n')
FIXTURE_EDITS = (
    *talker_window.FIXTURE_EDITS,
    (ANSWERING_STREAM,
     "// A STREAM_OUTPUT the face reports declaring (#943): word 0's flags, STREAM_DEST_MAC_VALID among them, in a\n"
     "// brief observation as in a whole one, the caller's brief kept, as the face block's stream port answers.\n"
     'static bool b_stream(void *ctx, unsigned i, uint16_t t, uint16_t n, struct aecp_stream_info *v)\n'
     '{\n    (void)ctx; (void)i; (void)n;\n    const bool brief = v->brief;\n    memset(v, 0, sizeof *v);\n'
     f'    v->brief = brief;\n    v->flags = t == 6u ? 0x{DECLARING:08x}u : 0u;\n    return true;\n}}\n'),
    ('static const struct acmp_env image_env = {NULL,locked,source,stream,notice,notice};\n',
     'static const struct acmp_env image_env = {NULL,locked,source,stream,notice,notice};\n'
     "// The AECP bridge's ACMP owner (#943): the fixture's, its source port entered through completion_source, whose\n"
     "// entry the testbench reports; inside an AECP record or a round, each is one completion of a STREAM_OUTPUT.\n"
     f'void {ENTRY}(void);\n__attribute__((noinline)) void {ENTRY}(void) {{ __asm__ volatile(""); }}\n'
     'static void bridge_source(void *ctx, unsigned n, struct acmp_source_state *out)\n'
     f'{{ {ENTRY}(); source(ctx, n, out); }}\n'
     'static const struct acmp_env bridge_env = {NULL,locked,bridge_source,stream,notice,notice};\n'),
    ('    aecp_nvm_init(&image_state,&image_aecp.core,image_names,AECP_ENTITY_NAME_RUNS,\n',
     '    image_aecp_bridge.acmp_owner=&bridge_env;\n'
     '    aecp_nvm_init(&image_state,&image_aecp.core,image_names,AECP_ENTITY_NAME_RUNS,\n'),
)
#: The rows' paths.
DECLARED, GET, REFUSED = 'aecp_outputs.declared', 'aecp_outputs.get_stream_info', 'aecp_outputs.set_stream_info'
HELD_SET, HELD_GET = 'aecp_outputs.held_set_stream_info', 'aecp_outputs.held_get_stream_info'
#: How long the egress stays held past the held GET_STREAM_INFO's frame, in ms: its response and the SET's last
#: notices wait for it, within their rows' budget.
HOLD_MS = 4
#: The output whose Listener SRP registers, and the PROBE_TX that declares its Talker.
LISTENED, SEQ = 0, 0x5d00
#: The AEM command types and status codes the checks read (IEEE 1722.1-2021 Table 7-126, 7-127).
SET_STREAM_INFO, GET_STREAM_INFO = 0x000E, 0x000F
#: The statuses a STREAM_INFO command is answered with after its whole observation (aecp_commands.c,
#: stream_info): SUCCESS, ENTITY_LOCKED, BAD_ARGUMENTS (a latency's top bit), NOT_SUPPORTED, STREAM_IS_RUNNING.
WHOLE_STATUSES = (0, 3, 7, 11, 12)
#: The pool of MAAP's dynamic allocations (IEEE 1722-2016 Table B.9), its top four octets.
MAAP_POOL = 0x91E0F000


def groups(p: scenario.Point, spec: dict) -> list[scenario.Group]:
    """Arm B's AECP groups as answering-ports builds them, then aecp-outputs."""
    ports = {**spec, 'variant': 'answering-ports'}
    return [*scenario.aecp_groups(p, ports), *scenario.aecp_fanout_groups(p, ports), *long_notice.groups(p, ports),
            *reboot_group.groups(p, ports), group(p, spec)]


def interface_of(build: dict, output: int) -> int:
    """A STREAM_OUTPUT's AVB interface, the descriptor's avb_interface_index (aecp_commands.c, observe)."""
    return int.from_bytes(scenario.descriptor_value(build, 6, output)[126:128], 'big')


def group(p: scenario.Point, build: dict) -> scenario.Group:
    """aecp-outputs (the module's docstring)."""
    ms, aecp, acmp = scenario.MS, scenario.CH['aecp'], scenario.CH['acmp']
    g = scenario.Group(GROUP, sim_ms=5000)
    scenario.ready(g, p)
    g.add(f'wait cycles {2600 * ms}', 'wait quiet 3 within 2000000')    # MAAP's ranges (talker_window.declared)
    controllers = [scenario.FANOUT_CONTROLLER + n for n in range(scenario.registrations())]
    seq = [0x5c00]

    def frame(controller: int, command_type: int, payload: bytes) -> bytes:
        """An AEM command from that controller, its sequence_id the next."""
        seq[0] += 1
        return f.aem_command(f.Aem(p.entity_id, controller, scenario.CTL_MAC, p.mac, seq[0]), command_type, payload)

    for i in range(p.interfaces):
        for ctl in controllers:
            g.add(f'frame {i} {frame(ctl, 0x0024, bytes(4)).hex()}', f'wait tx {aecp} 1 within {50 * ms}',
                  'wait quiet 3 within 2000000')
    everyone = tuple((ctl, i) for i in range(p.interfaces) for ctl in controllers)
    i = interface_of(build, LISTENED)
    g.probe(scenario.Probe(f'{DECLARED}.if{i}', "a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's "
                           'notice, completed, to every registration (#936, #943)', 'notify', f'rxc:{acmp}',
                           [f'resp:{acmp}:{SEQ:x}', f'notify:{aecp}:000f:6:{LISTENED}'], recipients=everyone,
                           expect=answers.acmp('PROBE_TX_RESPONSE', 'SUCCESS'), path=DECLARED),
            f'frame {i} {scenario.talker_cmd(p, "PROBE_TX", LISTENED, SEQ).hex()}',
            wait=f'tx {aecp} {len(everyone)} within {200 * ms}')
    g.add(f'frame {i} {scenario.listener_ready(p).hex()}', f'wait cycles {20 * ms}', 'wait quiet 3 within 2000000')

    def command(name: str, path: str, controller: int, body: tuple[int, bytes], status: str, at: int) -> None:
        """One AEM command, its command_type and payload, on interface at: a row to its response."""
        command_type = body[0]
        sent = frame(controller, *body)
        g.probe(scenario.Probe(f'{path}.{name}.if{at}', answers.refused(f'{name.upper()} of a declaring STREAM_OUTPUT',
                                                                        status), 'aecp', f'rxc:{aecp}',
                               [f'resp:{aecp}:{seq[0]:x}'], expect=answers.aem(command_type, status), path=path),
                f'frame {at} {sent.hex()}', wait=f'tx {aecp} 1 within {50 * ms}')

    for n in range(p.sources):
        command(f'get_stream_info_o{n}', GET, scenario.CTL1, (GET_STREAM_INFO, f.be(6, 2) + f.be(n, 2)), 'SUCCESS',
                interface_of(build, n))
    target = f.be(6, 2) + f.be(LISTENED, 2)
    latency = lambda value: (target + f.be(0x2000_0000, 4) + bytes(16) + f.be(value, 4)).ljust(84, b'\0')  # noqa: E731
    command('set_stream_info_stream_id', REFUSED, scenario.CTL1,
            (SET_STREAM_INFO, (target + f.be(0x4000_0000, 4)).ljust(84, b'\0')), 'NOT_SUPPORTED', i)
    lock = f.be(0, 4) + f.be(0, 8) + f.be(0, 2) + f.be(0, 2)
    g.add(f'frame {i} {frame(scenario.CTL1, 0x0001, lock).hex()}',
          f'wait tx {aecp} {1 + len(everyone)} within {200 * ms}', 'wait quiet 3 within 2000000')
    command('set_stream_info_locked', REFUSED, scenario.CTL2, (SET_STREAM_INFO, latency(2_000_000)), 'ENTITY_LOCKED',
            i)
    g.add(f'frame {i} {frame(scenario.CTL1, 0x0001, f.be(1, 4) + lock[4:]).hex()}',
          f'wait tx {aecp} {1 + len(everyone)} within {200 * ms}', 'wait quiet 3 within 2000000')
    end = f'{GROUP}.held.end'
    held_set = scenario.Probe(f'{HELD_SET}.if{i}', 'SET_STREAM_INFO of a declaring STREAM_OUTPUT, its notices past '
                              "the AECP ring's room behind a held egress", 'notify', f'rxc:{aecp}',
                              [f'resp:{aecp}:{seq[0] + 1:x}', f'notify:{aecp}:000e:6:{LISTENED}'],
                              recipients=everyone, expect=answers.aem(SET_STREAM_INFO), until=end, path=HELD_SET)
    g.add('txready 0')
    g.probes.append(held_set)
    sent = frame(scenario.CTL2, SET_STREAM_INFO, latency(3_000_000))
    g.add(f'mark {held_set.name}', scenario.tagged(f'frame {i} {sent.hex()}', held_set.name))
    held_get = scenario.Probe(f'{HELD_GET}.if{i}', 'GET_STREAM_INFO of a declaring STREAM_OUTPUT behind a held egress',
                              'aecp', f'rxc:{aecp}', [f'resp:{aecp}:{seq[0] + 1:x}'],
                              expect=answers.aem(GET_STREAM_INFO), until=end, path=HELD_GET)
    g.probes.append(held_get)
    sent = frame(scenario.CTL1, GET_STREAM_INFO, target)
    g.add(f'mark {held_get.name}', scenario.tagged(f'frame {i} {sent.hex()}', held_get.name))
    g.add(f'wait cycles {HOLD_MS * ms}', 'txready 1', 'wait quiet 3 within 50000000', f'mark {end}')
    return scenario.paced(g, aecp)


def stream_infos(tx: list, aecp: int) -> list[tuple[int, int, bool, int, int, int]]:
    """Each GET_STREAM_INFO of a STREAM_OUTPUT that left on AECP's channel: (interface, descriptor_index,
    unsolicited, flags, stream_dest_mac, flags_ex), from the response's fields (IEEE 1722.1-2021 7.4.16.2)."""
    out = []
    for _, ch, interface, fr in tx:
        if ch != aecp or len(fr) < 90 or fr[14] != 0xFB or fr[15] & 0x0F != 1:
            continue
        if (fr[36] << 8 | fr[37]) & 0x7FFF != GET_STREAM_INFO or fr[38:40] != b'\x00\x06':
            continue
        out.append((interface, int.from_bytes(fr[40:42], 'big'), bool(fr[36] & 0x80), int.from_bytes(fr[42:46], 'big'),
                    int.from_bytes(fr[66:72], 'big'), int.from_bytes(fr[86:90], 'big')))
    return out


def answer_findings(infos: list[tuple[int, int, bool, int, int, int]], listened_from: int | None = None) -> list[str]:
    """What is wrong with the GET_STREAM_INFOs of STREAM_OUTPUTs that left: each must carry STREAM_DEST_MAC_VALID and
    a MAAP pool address, base + n with one base on each interface, REGISTERING for output LISTENED alone and only from
    the infos' position listened_from (None: never), and no REGISTERING_FAILED."""
    out, bases = [], {}
    for k, (interface, n, unsolicited, flags, dest, flags_ex) in enumerate(infos):
        what = f"output {n}'s {'notice' if unsolicited else 'response'} on if{interface}"
        if not flags & DEST_MAC_VALID or dest >> 16 != MAAP_POOL or not dest & 0xFFFF:
            out.append(f'{what}: stream_dest_mac {dest:012x}, flags {flags:08x}: not a MAAP address the completion '
                       'answers')
        elif bases.setdefault(interface, dest - n) != dest - n:
            out.append(f'{what}: stream_dest_mac {dest:012x}, not its interface\'s base + {n}')
        registering = n == LISTENED and listened_from is not None and k >= listened_from
        if bool(flags_ex & REGISTERING) != registering or flags & REGISTERING_FAILED:
            out.append(f'{what}: flags_ex {flags_ex:08x}, flags {flags:08x}: REGISTERING '
                       f'{"expected" if registering else "unexpected"}, REGISTERING_FAILED never')
    return out


def records(log: object, sys_hz: int, cpu_hz: int, aecp: int) -> list[tuple[int | None, int | None, int, int]]:
    """Each AECP record (aecp_mbx.c, frame, a SPAN line) as record_classes.py names it, the first solicited response
    committed in it or before the next record: (command_type, descriptor_type, status, completions inside it)."""
    spans = [(int(r[0]), int(r[2])) for kind, *r in log.traced if kind == 'SPAN' and r[-1] == 'aecp_mbx:frame']
    entries = sorted(c for c, name in log.entries if name == ENTRY)
    answered = sorted((c, (fr[36] << 8 | fr[37]) & 0x7FFF, int.from_bytes(fr[38:40], 'big'), fr[16] >> 3)
                      for c, ch, _, fr in log.tx
                      if ch == aecp and len(fr) >= 40 and fr[15] & 1 and not (fr[15] & 0x0F == 1 and fr[36] & 0x80))
    out = []
    for k, (start, cycles) in enumerate(spans):
        stop = spans[k + 1][0] if k + 1 < len(spans) else None
        hit = next((a[1:] for a in answered if a[0] >= start and (stop is None or a[0] < stop)), (None, None, None))
        end = start + cycles * sys_hz // cpu_hz
        out.append((*hit, sum(1 for c in entries if start <= c <= end)))
    return out


def rounds_completing(log: object, sys_hz: int, cpu_hz: int) -> int:
    """How many completions THE RETRY's rounds (ctrl_loop.c, round_of, a SPAN line) ran."""
    spans = [(int(r[0]), int(r[2])) for kind, *r in log.traced if kind == 'SPAN' and r[-1] == 'ctrl_loop:round_of']
    entries = [c for c, name in log.entries if name == ENTRY]
    return sum(1 for start, cycles in spans for c in entries if start <= c <= start + cycles * sys_hz // cpu_hz)


def record_findings(group: str, named: list[tuple[int | None, int | None, int | None, int]]) -> list[str]:
    """What is wrong with a group's records: a whole observation of a STREAM_OUTPUT, answered or refused after it,
    whose record ran no completion or more than one; and any other answered record that ran one, a map edit's, the
    largest legal command's or a running check's (their observations are brief)."""
    out = []
    for command, kind, status, ran in named:
        whole = command in (GET_STREAM_INFO, SET_STREAM_INFO) and kind == 6
        if whole and status in WHOLE_STATUSES and ran != 1:
            out.append(f'{group}: a {"GET" if command == GET_STREAM_INFO else "SET"}_STREAM_INFO of a STREAM_OUTPUT '
                       f'(status {status}) whose record ran {ran} completion(s), not one')
        elif not whole and command is not None and ran:
            out.append(f'{group}: a brief observation completed: a record of command 0x{command:04x} ran {ran} '
                       'completion(s)')
    return out


def findings(spec: dict, out: Path, groups: list) -> list[str]:
    """What the arm's logs must show (the module's docstring), each failure a line; nothing for another arm."""
    if spec.get('variant') != NAME:
        return []
    import grade
    aecp, lines, names = scenario.CH['aecp'], [], {g.name for g in groups}
    for name in sorted(names):
        log = grade.parse((out / f'{name}.log').read_text(errors='replace'), spec['sys_hz'], spec['cpu_hz'])
        named = records(log, spec['sys_hz'], spec['cpu_hz'], aecp)
        lines += record_findings(name, named)
        if name != GROUP:
            continue
        ran = {(c, s) for c, k, s, n in named if k == 6 and n == 1}
        lines += [f'{GROUP}: no record of {what} ran the completion' for what, want in (
            ('a GET_STREAM_INFO answered SUCCESS', (GET_STREAM_INFO, 0)),
            ('a SET_STREAM_INFO answered SUCCESS', (SET_STREAM_INFO, 0)),
            ('a SET_STREAM_INFO refused ENTITY_LOCKED', (SET_STREAM_INFO, 3)),
            ('a SET_STREAM_INFO refused NOT_SUPPORTED', (SET_STREAM_INFO, 11))) if want not in ran]
        if not rounds_completing(log, spec['sys_hz'], spec['cpu_hz']):
            lines.append(f"{GROUP}: no round of THE RETRY ran the completion (the declared Talker's notice)")
        infos = stream_infos(log.tx, aecp)
        listener = next((k for k, info in enumerate(infos) if not info[2]), None)  # the first GET's, after the MRPDU
        lines += [f'{GROUP}: {line}' for line in answer_findings(infos, listener)]
        if not any(not info[2] for info in infos) or not any(info[2] for info in infos):
            lines.append(f'{GROUP}: no GET_STREAM_INFO of a STREAM_OUTPUT left as a response and as a notice')
        print(f'DECLARING {GROUP}: {sum(n for *_, n in named)} completion(s) in {sum(1 for *_, n in named if n)} '
              f'record(s), {rounds_completing(log, spec["sys_hz"], spec["cpu_hz"])} in rounds of THE RETRY, '
              f'{len(infos)} GET_STREAM_INFO(s) of a STREAM_OUTPUT left')
    for line in lines:
        print('DECLARING', line)
    return lines


def fixture_findings(edits: tuple[tuple[str, str], ...] = FIXTURE_EDITS) -> list[str]:
    """What is wrong with the arm's fixture: its stream observation must keep the caller's brief across its memset
    (a brief observation that leaves it cleared is completed, R872-1-F2), answer a STREAM_OUTPUT declaring, and the
    bridge's ACMP owner must enter the source port through ENTRY."""
    stream = next((new for old, new in edits if old == ANSWERING_STREAM), '')
    out = []
    kept = 'brief = v->brief' in stream and \
        -1 < stream.find('memset(v, 0, sizeof *v);') < stream.find('v->brief = brief;')
    if not kept:
        out.append("the arm's stream observation does not keep the caller's brief across its memset")
    if f'0x{DECLARING:08x}u' not in stream:
        out.append("the arm's stream observation does not answer a STREAM_OUTPUT declaring")
    if not any('image_aecp_bridge.acmp_owner=&bridge_env;' in new for _, new in edits) or not any(
            f'{{ {ENTRY}(); source(ctx, n, out); }}' in new for _, new in edits):
        out.append(f"the bridge's ACMP owner does not enter the source port through {ENTRY}")
    return out


def checks() -> list[tuple[str, bool, str]]:
    """The harness self-test's checks of this arm (record_classes.checks): its fixture as findings() needs it, and
    each planted answer and record refused by answer_findings and record_findings, the sound ones passed."""
    out = []

    def check(name: str, found: list[str], want: bool) -> None:
        """One check: whether the findings are there as wanted."""
        out.append((name, bool(found) == want, '; '.join(found) or 'none'))
    check("the declaring arm's fixture keeps brief and enters the source port through its entry", fixture_findings(),
          False)
    cleared = tuple((old, new.replace('    v->brief = brief;\n', '')) for old, new in FIXTURE_EDITS)
    check("the declaring arm refuses a fixture that clears brief (R872-1-F2's)", fixture_findings(cleared), True)
    base = 0x91E0F0000100
    sound = [(0, 0, True, DECLARING, base, 0), (0, 0, False, DECLARING, base, REGISTERING),
             (0, 1, False, DECLARING, base + 1, 0)]
    check('the declaring answers pass a sound set', answer_findings(sound, 1), False)
    for name, k, column, value in (('stream_dest_mac 0', 1, 4, 0), ('another base', 2, 4, base + 7),
                                   ("another output's REGISTERING", 2, 5, REGISTERING),
                                   ("the Listener's REGISTERING lost", 1, 5, 0),
                                   ('REGISTERING_FAILED for a Listener Ready', 1, 3, DECLARING | REGISTERING_FAILED),
                                   ('no STREAM_DEST_MAC_VALID', 0, 3, DECLARING & ~DEST_MAC_VALID)):
        planted = [list(info) for info in sound]
        planted[k][column] = value
        check(f'the declaring answers refuse {name}', answer_findings([tuple(i) for i in planted], 1), True)
    good = [(GET_STREAM_INFO, 6, 0, 1), (SET_STREAM_INFO, 6, 11, 1), (0x002D, 15, 0, 0), (None, None, None, 1)]
    check('the declaring records pass a sound set', record_findings('g', good), False)
    for name, record in (('a GET_STREAM_INFO that ran no completion', (GET_STREAM_INFO, 6, 0, 0)),
                         ('a refused SET_STREAM_INFO that ran two', (SET_STREAM_INFO, 6, 3, 2)),
                         ('a map edit that completed its brief check', (0x002D, 15, 0, 1)),
                         ("a SET_CONFIGURATION's running check completed", (0x0006, 0, 0, 1))):
        check(f'the declaring records refuse {name}', record_findings('g', [*good, record]), True)
    return out


#: The planted defects build.py builds for this arm, as its MUTATIONS: (file under the control firmware, anchor,
#: replacement, control groups, variant). The completion never run; a brief observation completed; the completion
#: dearer by a loop of DEARER iterations.
DEARER = 1000
GATE = '\t} else if (!v->brief && (v->flags & 0x10000000u) != 0u) {\n'
PLANTS = {
    'completion-unexecuted': ('app/ctrl_app_aecp.c', GATE,
                              '\t} else if (index == UINT16_MAX && !v->brief && (v->flags & 0x10000000u) != 0u) {\n',
                              f'aecp-fanout,{GROUP}', NAME),
    'brief-completed': ('app/ctrl_app_aecp.c', GATE, '\t} else if ((v->flags & 0x10000000u) != 0u) {\n',
                        f'aecp-fanout,{GROUP}', NAME),
    'completion-dearer': ('app/ctrl_app_aecp.c', '\tif (index >= a->n_sources) return false;\n',
                          '\tif (index >= a->n_sources) return false;\n'
                          f'\tfor (volatile unsigned k = 0; k < {DEARER}u; ++k) {{\n\t}}\n',
                          f'aecp-fanout,{GROUP}', NAME),
}
#: Each plant's finding, which verdict requires: the evidence absent, a brief record completed, a record held over.
CONTROLS = {'completion-unexecuted': ' ran 0 completion(s), not one',
            'brief-completed': 'a brief observation completed', 'completion-dearer': 'over the other record'}


def verdict(args: argparse.Namespace, out: Path, late: list, refusals: list) -> int:
    """A declaring-outputs plant's exit status: caught where its finding is there by its words, from findings()
    (late) for the first two, from record_classes.py's hold of this leg's records for the dearer completion."""
    words = CONTROLS[args.mutation]
    if args.mutation == 'completion-dearer':
        import record_classes
        lines = [line for line in record_classes.findings([record_classes.read_leg(out)[0]], None)[0] if words in line]
    else:
        lines = [line for line in late if words in line]
    caught = bool(lines) and not refusals
    print(f'CONTROL {args.mutation} {"caught" if caught else "ESCAPED"}: {len(lines)} finding(s) {words!r} '
          f'({"; ".join(lines[:3]) or "none"}), {len(refusals)} refusal(s)')
    return 0 if caught else 1
