# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The hook harness's portable self-test (#665): its rules on synthetic logs, then each rule replaced in turn.

It needs Python and PyYAML only: no build, no simulation. CHECKS are the
named checks. Each restates what it pins (the bounds, the normative
timeouts, the clock labels), so a changed table fails, and each ordering
check is run on a clean log, which it must apply to and pass, and on a
defective one, which it must report by its hook's words. MUTANTS then
replaces one rule each (unittest.mock.patch), and the check named beside it
must fail; a mutant no check catches fails the self-test.
"""
from __future__ import annotations

import dataclasses
import io
import sys
import tempfile
from collections.abc import Callable
from contextlib import AbstractContextManager, ExitStack, redirect_stdout
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hooks  # noqa: E402
import hooks_build  # noqa: E402
# Those two put the CPU budget harness first, and it has a run.py of its own.
sys.path.insert(0, str(HERE))
import run  # noqa: E402
import grade  # noqa: E402  the CPU budget harness's grader, read only
import scenario  # noqa: E402
from scenario import CH, Group, Probe  # noqa: E402
import frames as f  # noqa: E402

MS = hooks.BUS_MS
#: The path grade and the slack as written, which mutants wrap.
HOOK_ROW = run.hook_row
SLACK = run.slack_cycles
HELD_ROW = run.held_row
SUMMARY = run.summary
GRADE_ALL = run.grade_all
MAIN = run.main
COUNTERS_GROUPS = hooks.counters_groups
AGING_GROUP = hooks.aging_group
#: The plants as written, which a mutant strips.
PLANTS = hooks.plants()
#: What a check's synthetic log carries, fixed here so a mutant of the rule reading it meets a well-formed log.
PROBE_TX = f.ACMP['PROBE_TX']
FACE_COMMIT = min(hooks.face_commit_words({'interfaces': 1}))
#: The product clocks (the owner's decision of 2026-10-30 on #665): the split CPU on sys, at the bus's 100 MHz.
CPU_HZ = SYS_HZ = 100_000_000
#: The bounds the owner's decision of 2026-10-29 on #665 gives, restated.
BOUNDS = {'adp': 20.0, 'disc': 20.0, 'acmp': 20.0, 'aecp': 20.0, 'notify': 20.0, 'maap': 20.0, 'srp': 18.0}
NORMATIVE = {'adp': 2000.0, 'disc': 200.0, 'acmp': 200.0, 'aecp': 240.0, 'notify': 240.0, 'maap': 500.0,
             'srp': 180.0}
FAMILIES = {'adp': 'H-ADP', 'disc': 'H-DISC', 'acmp': 'H-ACMP', 'aecp': 'H-AECP', 'notify': 'H-NOTIFY',
            'maap': 'H-MAAP', 'srp': 'H-SRP'}
#: The shipping point, and a served-descriptor list for hooks-counters: the real one needs a build's descriptors.
POINT = scenario.Point('1x1', 'endstation_ax7101_1x1_tdm8', 1, 1, 2, 1, 1)
SERVED = [(5, 0), (5, 1), (6, 0), (9, 0), (0x24, 0)]
#: The fields that label the held push's row, and their values, whether the push was sent or not.
HELD_FIELDS = ('hook', 'group', 'probe', 'path', 'family', 'interface')
HELD_LABELS = ('H-COUNTERS', 'hooks-counters', 'counters.held.if0', 'counters.held', 'notify', 0)


class Failed(AssertionError):
    """A named check's failure."""


def expect(ok: bool, what: str) -> None:
    """Fail the running check with what, unless ok."""
    if not ok:
        raise Failed(what)


def log(**fields: object) -> grade.Log:
    """A synthetic parsed log at the product clocks."""
    out = grade.Log(SYS_HZ, CPU_HZ)
    for name, value in fields.items():
        setattr(out, name, value)
    return out


def work(start: int, writes: list[tuple[int, int, int]]) -> grade.Pass:
    """A work pass starting at start with the given writes."""
    return grade.Pass(0, start, start // 2, 1000, {}, writes, {})


def row(family: str, ms: float, wait: float = 0.0, probe: str = 'x.if0', **more: object) -> dict:
    """A graded path as the CPU budget harness's grader writes it."""
    return dict(probe=probe, row='r', family=family, interface=0, path=[probe.rsplit('.', 1)[0], 0], ms=ms,
                cpu_cycles=round(ms * CPU_HZ / 1000), wait_ms=wait, **more)


# ---- the checks ---------------------------------------------------------------------------------

def check_bounds() -> None:
    """T_svc is 20 ms and every family's bound is min(T_svc, its ceiling); the normative timeouts are pinned."""
    expect(hooks.T_SVC_MS == 20.0, f'T_svc is {hooks.T_SVC_MS}')
    got = {k: hooks.bound_ms(k) for k in BOUNDS}
    expect(got == BOUNDS, f'bounds {got}')
    expect(hooks.NORMATIVE_MS == NORMATIVE, f'normative {hooks.NORMATIVE_MS}')
    expect(hooks.COUNTERS_NORMATIVE_MS == 1000.0 and hooks.COUNTERS_SPACING_MS == 1000.0, 'counter timing')


def check_srp_instance() -> None:
    """An SRP path of 18 to 20 ms is over its bound, though within T_svc."""
    expect(not run.hook_row(row('srp', 19.0), 'srp')['within'], 'a 19 ms SRP path fits')
    expect(run.hook_row(row('srp', 18.0), 'srp')['within'], 'an 18 ms SRP path misses')


def check_exact_bound() -> None:
    """A path at its bound fits; a hundredth of a microsecond more is over it; W adds to it; a path never served
    is over it; the margin is the normative timeout less W and the path."""
    expect(run.hook_row(row('aecp', 20.0), 'aecp')['within'], 'the exact bound misses')
    expect(not run.hook_row(row('aecp', 20.00001), 'aecp')['within'], 'past the bound fits')
    r = run.hook_row(row('srp', 210.0, wait=200.0), 'srp')
    expect(r['within'] and r['bound_ms'] == 218.0, f'W + bound: {r}')
    expect(not run.hook_row(row('acmp', 1.0, starved=True), 'backlog')['within'], 'a starved path fits')
    expect(not run.hook_row(row('acmp', 1.0, unanswered=True), 'backlog')['within'], 'an unanswered path fits')
    r = run.hook_row(row('srp', 10.0, wait=150.0), 'srp')
    expect(r['margin_ms'] == 20.0, f'margin {r["margin_ms"]}')


def check_hooks_map() -> None:
    """Each family is its hook; a counter push's probe is H-COUNTERS; a composed window's row is loaded."""
    for family, hook in FAMILIES.items():
        expect(hooks.hook_of(row(family, 1.0)) == hook, f'{family} is not {hook}')
    expect(hooks.hook_of(row('notify', 1.0, probe='counters.first.if0')) == 'H-COUNTERS', 'counters')
    expect(run.hook_row(row('aecp', 1.0), 'backlog')['loaded'], 'a backlog row is not loaded')
    expect(run.hook_row(row('notify', 1.0), 'hooks-load-notify')['loaded'], 'the loaded fan-out is not loaded')
    expect(not run.hook_row(row('aecp', 1.0), 'aecp')['loaded'], 'a lone path is loaded')
    expect(run.hook_row(row('notify', 1.0, probe='counters.x'), 'g')['normative_ms'] == 1000.0, 'counter timeout')


def check_clock_label() -> None:
    """The product clock is sys and the default; it is labelled the product's; the Milan clock, this base's
    wiring before the owner's decision of 2026-10-30, is labelled history, never the product's."""
    expect(hooks_build.CPU_CLOCKS[0] == 'sys', f'the default CPU clock is {hooks_build.CPU_CLOCKS[0]}')
    product = run.clock_label(dict(cpu_hz=CPU_HZ, sys_hz=SYS_HZ, product_cpu_hz=SYS_HZ, cpu_clock='sys'))
    milan = run.clock_label(dict(cpu_hz=50_000_000, sys_hz=SYS_HZ, product_cpu_hz=SYS_HZ, cpu_clock='milan'))
    expect('100 MHz on sys (the product split CPU clock)' in product and 'history' not in product, product)
    expect('history' in milan and 'not the product split CPU clock of 100 MHz' in milan and '50 MHz' in milan,
           milan)


def check_plants() -> None:
    """Each hook has one late and one ordering plant, with its words and its group, and every plant's edits
    apply to the checkout's firmware tree, each anchor once."""
    found = hooks.plants()
    expect(len(found) == 2 * len(hooks.HOOKS) == 16, f'{len(found)} plants')
    for name, (hook, plant) in found.items():
        kind = 'LATE' if name.endswith('-late') else 'ORDER'
        expect(plant.words == f'{kind} {hook}', f'{name}: {plant.words}')
        texts = hooks_build.plant_text(hooks_build.FIRMWARE, plant.edits)
        expect(set(texts) == {e[0] for e in plant.edits}, f'{name}: edits {sorted(texts)}')
        for path, text in texts.items():
            expect(text != (hooks_build.FIRMWARE / path).read_text(), f'{name}: {path} unchanged')
        expect(plant.arm == ('answering' if hook == 'H-COUNTERS' else 'idle'), f'{name}: arm {plant.arm}')


def check_testbench() -> None:
    """Every testbench addition's anchor occurs once in the CPU budget harness's testbench."""
    text = (hooks_build.BUDGET / 'sim_main.cpp').read_text()
    for anchor, _ in hooks_build.additions(dict(csr_base=0x9000_0000, csr_size=0x1_0000)):
        expect(text.count(anchor) == 1, f'{anchor.strip()!r} occurs {text.count(anchor)} times')


def check_split() -> None:
    """This harness's own lines are taken off before the CPU budget harness's parser; a counter change is a pad."""
    rest, own = hooks.split('MS 5 1 0 0\nCTRCHG 7 0 5 0\nCSRW 9 654\n')
    expect(rest == 'MS 5 1 0 0\n' and [w[0] for w in own] == ['CTRCHG', 'CSRW'], f'{rest!r} {own}')
    parsed, _ = hooks.parsed('CTRCHG 7 1 5 0\n', SYS_HZ, CPU_HZ)
    expect(parsed.pads == [(7, 'CTR', 1)], f'pads {parsed.pads}')


def adp_frame(gm: int, interface: int = 0) -> tuple[int, int, int, bytes]:
    """An ENTITY_AVAILABLE TX record carrying gm."""
    frame = bytearray(f.adp(f.ADP_AVAILABLE, 1, 2, f.Adp(gm_id=gm)))
    return (0, CH['adp'], interface, bytes(frame))


def check_adp_order() -> None:
    """H-ADP: an ENTITY_AVAILABLE after a grandmaster change carries the new grandmaster; one carrying the old is
    reported."""
    g = Group('g', steps=['gm 0 00000000000000aa 0'])
    pads = [(100, 'GM', 0)]
    good = log(pads=pads, tx=[(500, *adp_frame(0xAA)[1:])], passes=[work(400, [(500, 0, 0)])])
    bad = log(pads=pads, tx=[(500, *adp_frame(0x0)[1:])], passes=[work(400, [(500, 0, 0)])])
    ok, wrong = hooks.adp_grandmaster(good, g, [], {}), hooks.adp_grandmaster(bad, g, [], {})
    expect(ok.applied == 1 and not ok.findings, f'clean: {ok}')
    expect(wrong.findings and wrong.findings[0].startswith('ORDER H-ADP:'), f'defective: {wrong}')


def check_disc_order() -> None:
    """H-DISC: DEPARTING then AVAILABLE then a PROBE_TX before the next ADP record passes; without one it is
    reported, and a PROBE_TX after the next record does not count, when that record came later than the longest
    TMR_DELAY and its services (1040 ms); when it came sooner, a PROBE_TX after it leaves the instance undecided."""
    available = 2 * MS
    rxc = [(MS, CH['adp'], 0, 'acmp.entity_departing.if0', 82),
           (available, CH['adp'], 0, 'acmp.entity_available.if0', 82)]
    probe = bytearray(70)
    probe[14], probe[15] = 0xFC, PROBE_TX
    far, near = available + 1100 * MS, available + 500 * MS
    sent = lambda c: [(c, CH['acmp'], 0, bytes(probe))]
    record = lambda c: (c, CH['adp'], 0, '-', 82)
    spec = {'interfaces': 1}
    order = lambda x: hooks.discovery_order(x, Group('g'), [], spec)
    ok = order(log(rxc=[*rxc, record(far)], tx=sent(available + 600 * MS)))
    expect(ok.applied == 1 and not ok.findings and not ok.undecided, f'clean: {ok}')
    wrong = order(log(rxc=rxc))
    expect(wrong.findings and wrong.findings[0].startswith('ORDER H-DISC:'), f'defective: {wrong}')
    after = order(log(rxc=[*rxc, record(far)], tx=sent(far + 10 * MS)))
    expect(after.findings and after.findings[0].startswith('ORDER H-DISC:'), f'a probe after the next record: {after}')
    soon = order(log(rxc=[*rxc, record(near)], tx=sent(near + 100 * MS)))
    expect(soon.undecided == 1 and not soon.applied and not soon.findings,
           f'a probe after a next record inside the delay: {soon}')


def acmp_frames(seqs: list[int], response: bool) -> list[bytes]:
    """GET_RX_STATE commands (or their responses) from one controller with these sequence_ids."""
    msg = f.ACMP['GET_RX_STATE'] + (1 if response else 0)
    return [f.acmp(msg, 0x0A0B0C0D0E01, f.Acmp(controller=7, talker=1, listener=2, sequence=s)) for s in seqs]


def check_acmp_order() -> None:
    """H-ACMP: two overlapping commands answered in arrival order pass; answered the other way they are reported."""
    commands = acmp_frames([1, 2], False)
    g = Group('g', steps=[f'frame 0 {c.hex()}' for c in commands])
    rxc = [(100, CH['acmp'], 0, '-', len(commands[0])), (110, CH['acmp'], 0, '-', len(commands[1]))]
    resp = acmp_frames([1, 2], True)
    good = log(rxc=rxc, tx=[(200, CH['acmp'], 0, resp[0]), (300, CH['acmp'], 0, resp[1])])
    bad = log(rxc=rxc, tx=[(300, CH['acmp'], 0, resp[0]), (200, CH['acmp'], 0, resp[1])])
    ok, wrong = hooks.acmp_order(good, g, [], {}), hooks.acmp_order(bad, g, [], {})
    expect(ok.applied == 1 and not ok.findings, f'clean: {ok}')
    expect(wrong.findings and wrong.findings[0].startswith('ORDER H-ACMP:'), f'defective: {wrong}')


def aem_response(seq: int, unsolicited: bool = False, command: int = 0x0001) -> bytes:
    """A solicited (or unsolicited) AEM_RESPONSE of a command with this sequence_id."""
    frame = bytearray(f.aem_command(f.Aem(1, 2, 3, 4, seq), command, bytes(8)))
    frame[15] = (frame[15] & 0xF0) | 1
    if unsolicited:
        frame[36] |= 0x80
    return bytes(frame)


def check_aecp_order() -> None:
    """H-AECP: a face commit between a lock's receive commit and its response passes; a commit after it is
    reported."""
    g = Group('g', probes=[Probe('aecp.lock_entity.if0', 'lock', 'aecp', 'rxc:2', ['resp:2:10'])])
    rxc = [(100, CH['aecp'], 0, 'aecp.lock_entity.if0', 60)]
    tx = [(300, CH['aecp'], 0, aem_response(0x10))]
    good = log(rxc=rxc, tx=tx, writes=[(200, FACE_COMMIT, 1)])
    bad = log(rxc=rxc, tx=tx, writes=[(400, FACE_COMMIT, 1)])
    ok, wrong = (hooks.face_before_response(x, g, [], {'interfaces': 1}) for x in (good, bad))
    expect(ok.applied == 1 and not ok.findings, f'clean: {ok}')
    expect(wrong.findings and wrong.findings[0].startswith('ORDER H-AECP:'), f'defective: {wrong}')


def check_notify_order() -> None:
    """H-NOTIFY: a response before its notification passes; a notification before it is reported."""
    probe = Probe('n.set_name.if0', 'n', 'notify', 'rxc:2', ['resp:2:20', 'notify:2:0010:0:0'], recipients=((2, 0),))
    g = Group('g', probes=[probe])
    rxc = [(100, CH['aecp'], 0, 'n.set_name.if0', 60)]
    notice = bytearray(aem_response(0, True, 0x0010))
    notice[26:34] = (2).to_bytes(8, 'big')
    resp = aem_response(0x20, False, 0x0010)
    good = log(rxc=rxc, tx=[(200, CH['aecp'], 0, resp), (300, CH['aecp'], 0, bytes(notice))])
    bad = log(rxc=rxc, tx=[(300, CH['aecp'], 0, resp), (200, CH['aecp'], 0, bytes(notice))])
    ok, wrong = (hooks.response_before_notice(x, g, [], {}) for x in (good, bad))
    expect(ok.applied == 1 and not ok.findings, f'clean: {ok}')
    expect(wrong.findings and wrong.findings[0].startswith('ORDER H-NOTIFY:'), f'defective: {wrong}')


def counter_frame(recipient: int = 2, kind: int = 5, index: int = 0) -> bytes:
    """An unsolicited GET_COUNTERS of a descriptor, STREAM_INPUT 0 by default, to the recipient."""
    frame = bytearray(aem_response(0, True, hooks.GET_COUNTERS))
    frame[26:34] = recipient.to_bytes(8, 'big')
    frame[38:40], frame[40:42] = kind.to_bytes(2, 'big'), index.to_bytes(2, 'big')
    return bytes(frame)


def check_counter_spacing() -> None:
    """H-COUNTERS: pushes 1 s apart pass; 0.1 s apart they are reported."""
    fr = counter_frame()
    good = log(wire=[(0, CH['aecp'], 0, fr), (1000 * MS, CH['aecp'], 0, fr)])
    bad = log(wire=[(0, CH['aecp'], 0, fr), (100 * MS, CH['aecp'], 0, fr)])
    ok, wrong = (hooks.counter_spacing(x, Group('g'), [], {}) for x in (good, bad))
    expect(ok.applied == 1 and not ok.findings, f'clean: {ok}')
    expect(wrong.findings and wrong.findings[0].startswith('ORDER H-COUNTERS:'), f'defective: {wrong}')


def check_held_push() -> None:
    """The held push runs from its eligibility, 1 s after the first push's last departure, to its last
    recipient's commit."""
    fr = counter_frame()
    synthetic = (f'CTRCHG 0 0 5 0\nCTRCHG {100 * MS} 0 2 0\n')
    first, second, departed = 10 * MS, 1012 * MS, 11 * MS
    parsed = log(pads=[(0, 'CTR', 0), (100 * MS, 'CTR', 0)], tx=[(first, CH['aecp'], 0, fr),
                 (second, CH['aecp'], 0, fr)], wire=[(departed, CH['aecp'], 0, fr), (second + 5, CH['aecp'], 0, fr)])
    with patch.object(hooks, 'parsed', lambda t, s, c: (parsed, [])):
        held = hooks.held_push(synthetic, Group('hooks-counters'), {'sys_hz': SYS_HZ, 'cpu_hz': CPU_HZ})
    expect(held['eligible'] == departed + 1000 * MS and held['ms'] == 1.0, f'held {held}')
    expect(held['wait_ms'] == 911.0, f'wait {held["wait_ms"]}')


def check_maap_order() -> None:
    """H-MAAP: a report after a DA_GATE publication passes; a report before any is reported."""
    gate = scenario.pub_word(0, 'DA_GATE')
    passes = [work(10, [])]
    good = log(passes=passes, writes=[(50, gate, 1)])
    bad = log(passes=passes, writes=[(90, gate, 1)])
    own = [['CSRW', '60', '654'], ['CSRW', '61', '750'], ['CSRW', '62', '6cc'], ['CSRW', '70', '654'],
           ['CSRW', '71', '750']]
    ok, wrong = (hooks.maap_gate_before_report(x, Group('g'), own, {}) for x in (good, bad))
    expect(ok.applied == 1 and not ok.findings, f'clean: {ok}')
    expect(wrong.findings and wrong.findings[0].startswith('ORDER H-MAAP:'), f'defective: {wrong}')


def check_srp_order() -> None:
    """H-SRP: the adopted SR_DOMAIN before the next MRPDU passes; after it, it is reported."""
    word = scenario.pub_word(0, 'SR_DOMAIN')
    field = next(fl for r in scenario.CONTRACT.pub_registers if r.name == 'SR_DOMAIN' for fl in r.fields
                 if fl.name == 'ADOPTED')
    value = 1 << field.lsb
    rxc = [(100, CH['srp'], 0, 'srp.domain.if0', 60)]
    tx = [(300, CH['srp'], 0, bytes(60))]
    good = log(rxc=rxc, tx=tx, writes=[(200, word, value)])
    bad = log(rxc=rxc, tx=tx, writes=[(400, word, value)])
    ok, wrong = (hooks.domain_before_mrpdu(x, Group('g'), [], {'interfaces': 1}) for x in (good, bad))
    expect(ok.applied == 1 and not ok.findings, f'clean: {ok}')
    expect(wrong.findings and wrong.findings[0].startswith('ORDER H-SRP:'), f'defective: {wrong}')


def check_findings() -> None:
    """A path over its bound is a LATE finding by its hook; an ordering finding is kept by its hook."""
    rows = {'maap': [dict(row('maap', 25.0), status='measured')]}
    with patch.object(hooks, 'ordering', lambda t, g, s: {'H-MAAP': hooks.Checked(1, ['ORDER H-MAAP: x'])}):
        got = graded_with(rows, keep_ordering=True)
    expect(got['findings'][0].startswith('LATE H-MAAP: x.if0: 25.000 ms against its bound 20 ms'), got['findings'])
    expect('ORDER H-MAAP: x (maap)' in got['findings'], got['findings'])


def check_narrow() -> None:
    """A path within its bound by fewer CPU cycles than the layout swing (6,490) is a NARROW finding by its hook;
    by the swing or more it is none; a path over its bound is LATE, not NARROW."""
    expect(hooks.LAYOUT_SWING_CYCLES == 6490, f'the layout swing is {hooks.LAYOUT_SWING_CYCLES}')
    swing = hooks.LAYOUT_SWING_CYCLES * 1000 / CPU_HZ
    rows = {'maap': [dict(row('maap', 20.0 - swing + 1e-5, probe='under.if0'), status='measured'),
                     dict(row('maap', 20.0 - swing, probe='at.if0'), status='measured'),
                     dict(row('maap', 20.0, probe='bound.if0'), status='measured'),
                     dict(row('maap', 21.0, probe='over.if0'), status='measured')]}
    got = graded_with(rows)['findings']
    expect(any(x.startswith('NARROW H-MAAP: under.if0: ') and 'by 6,489 CPU cycles' in x for x in got), got)
    expect(any(x.startswith('NARROW H-MAAP: bound.if0: ') for x in got), got)
    expect(not any(': at.if0:' in x for x in got), got)
    expect(any(x.startswith('LATE H-MAAP: over.if0:') for x in got) and not any('NARROW H-MAAP: over' in x
                                                                               for x in got), got)


def graded_with(probes: dict[str, list[dict]], keep_ordering: bool = False) -> dict:
    """run.grade_all over groups whose grades are the given probe rows, with no ordering instances unless
    keep_ordering leaves the caller's patch of hooks.ordering in place."""
    class Text:
        """A log path stand-in."""

        def __init__(self, name: str) -> None:
            self.name = name

        def read_text(self) -> str:
            """The group's name: the patched grade looks its rows up by it."""
            return self.name
    with ExitStack() as stack:
        out = stack.enter_context(tempfile.TemporaryDirectory())
        stack.enter_context(patch.object(hooks, 'graded', lambda t, g, s: {'probes': probes[t]}))
        stack.enter_context(patch.object(hooks, 'held_push', lambda t, g, s: None))
        if not keep_ordering:
            stack.enter_context(patch.object(hooks, 'ordering', lambda t, g, s: {}))
        return run.grade_all([Group(n) for n in probes], [Text(n) for n in probes], {'cpu_hz': CPU_HZ}, Path(out))


def counters_group() -> Group:
    """hooks-counters at the shipping point, over SERVED."""
    with patch.object(hooks, 'counter_descriptors', lambda build: SERVED):
        return hooks.counters_groups(POINT, {})[0]


def plant_group(name: str) -> Group:
    """The group a late plant runs in."""
    made = [*scenario.control_groups(POINT), *hooks.late_groups(POINT), counters_group()]
    return next(g for g in made if g.name == name)


def plant_verdict(name: str, findings: list[str]) -> tuple[int, str]:
    """run.main's verdict on one plant, its build, simulation and grade replaced by the given findings: its exit
    status and its PLANT line."""
    plant = hooks.plants()[name][1]
    spec = dict(point='1x1', interfaces=1, arm=plant.arm, cpu_clock='sys', plant=None, cpu_hz=CPU_HZ, sys_hz=SYS_HZ,
                executable_sha256='0')
    graded = dict(rows=[], refusals=[], superseded=[], findings=findings,
                  checks={h: dict(applied=0, undecided=0, findings=[]) for h in hooks.HOOKS})
    printed = io.StringIO()
    with tempfile.TemporaryDirectory() as folder, ExitStack() as stack:
        for target, attribute, value in ((sys, 'argv', ['run.py', '--plant', name, '--build-dir', folder]),
                                         (hooks_build, 'build', lambda *a: spec),
                                         (scenario, 'point', lambda point, build: None),
                                         (hooks, 'groups', lambda p, build: [Group(plant.group)]),
                                         (run, 'run_group', lambda b, out, g: out / f'{g.name}.log'),
                                         (run, 'grade_all', lambda *a: graded)):
            stack.enter_context(patch.object(target, attribute, value))
        stack.enter_context(redirect_stdout(printed))
        status = run.main()
    return status, next((x for x in printed.getvalue().splitlines() if x.startswith('PLANT ')), '')


def check_plant_verdict() -> None:
    """A plant is reported caught only by a finding its defect causes. run.main, on what an unplanted run of each
    plant's group can report, every other path of the group over its bound under the plant's own words, says
    ESCAPED and exits 1; with the plant's own finding it says caught and exits 0. Each late plant names a path of
    its group, and that path alone catches it."""
    for name, (hook, plant) in hooks.plants().items():
        late_plant = name.endswith('-late')
        expect(late_plant == (plant.probe is not None), f'{name}: names the path {plant.probe}')
        paths = [p.name for p in plant_group(plant.group).probes] if late_plant else []
        expect(not late_plant or plant.probe in paths, f'{name}: {plant.probe} is no path of {plant.group}')
        words = plant.words if late_plant else f'LATE {hook}'
        others = [x for x in paths if x != plant.probe] + ['another.if0', *([f'{plant.probe}1'] if late_plant else [])]
        unplanted = [f'{words}: {x}: 27.581 ms against its bound 20 ms ({plant.group})' for x in others]
        status, line = plant_verdict(name, unplanted)
        expect(status == 1 and line == f'PLANT {name} ESCAPED: {run.plant_wanted(plant)} not found',
               f'{name}: reported caught with no plant applied, rc {status}: {line}')
        own = f'{plant.words}: {plant.probe or "the defect"}: 81.819 ms against its bound 20 ms ({plant.group})'
        status, line = plant_verdict(name, [*unplanted, own])
        expect(status == 0 and line == f'PLANT {name} caught: {own}', f'{name}: not caught, rc {status}: {line}')


def check_held_grade() -> None:
    """The held push has one service bound: W, the time it was held, is recorded beside it and never added. It fits
    at that bound and not past it, and its row reports the service that was graded. Its cycles are the CPU clock's,
    rounded up, and its margin is the 1 s counter update less W and the service, to the hundredth of a microsecond.
    It is a lone path of H-COUNTERS."""
    spec = dict(cpu_hz=50_000_000, sys_hz=SYS_HZ)
    held = lambda ms, span: dict(probe='counters.held.if0', eligible=1000 * MS, end=1000 * MS + span, ms=ms,
                                 wait_ms=900.0)
    at, past = run.held_row(held(20.0, 20 * MS), spec), run.held_row(held(20.00002, 20 * MS + 2), spec)
    expect(at['bound_ms'] == 20.0 and past['bound_ms'] == 20.0, f'the held bound includes W: {at["bound_ms"]}')
    expect(at['within'], 'a held push at its bound misses')
    expect(not past['within'], 'a held push past its bound fits')
    expect((at['ms'], past['ms']) == (20.0, 20.00002), f'the held row reports {at["ms"]} ms, not its service')
    expect(at['wait_ms'] == 900.0, f'the held W is not recorded: {at["wait_ms"]}')
    cycles = run.held_row(held(0.00003, 3), spec)['cpu_cycles']
    expect(cycles == 2, f'3 bus cycles are {cycles} at the 50 MHz CPU, not 2')
    expect(at['normative_ms'] == 1000.0, f'the held timeout is {at["normative_ms"]}')
    expect(at['margin_ms'] == 80.0, f'the held margin is {at["margin_ms"]}, not 1000 - 900 - 20')
    expect(past['margin_ms'] == 79.99998, f'the held margin is {past["margin_ms"]}, not 1000 - 900 - 20.00002')
    identity = tuple(at[k] for k in HELD_FIELDS)
    expect(identity == HELD_LABELS, f'held row {identity}')
    expect(not at['unbounded'] and not at['loaded'] and not at.get('missing'), f'held row classification {at}')


def check_missing_held() -> None:
    """A held push never sent is a row that never fits, at its one service bound, and a finding by name. It records
    no service, no W and no margin, under the labels of the held push."""
    with tempfile.TemporaryDirectory() as folder:
        out = Path(folder)
        text = out / 'input.log'
        text.write_text('')
        with patch.object(hooks, 'graded', return_value={'probes': []}), \
                patch.object(hooks, 'ordering', return_value={}), \
                patch.object(hooks, 'held_push', return_value=dict(probe='counters.held.if0', missing=True)):
            got = run.grade_all([Group('hooks-counters')], [text], dict(cpu_hz=CPU_HZ, sys_hz=SYS_HZ), out)
    expect('LATE H-COUNTERS: counters.held.if0: the held push was never sent' in got['findings'],
           f'a held push never sent is no finding: {got["findings"]}')
    r = got['rows'][0]
    expect(r['missing'] and r['unbounded'] and not r['within'] and r['slack_cycles'] == -1, f'a missing push fits: {r}')
    expect((r['bound_ms'], r['normative_ms'], r['ms'], r['loaded']) == (20.0, 1000.0, 0.0, False), f'missing row {r}')
    expect((r['cpu_cycles'], r['wait_ms'], r['margin_ms']) == (0, 0.0, 0.0),
           f'a push never sent records a service: {r}')
    identity = tuple(r[k] for k in HELD_FIELDS)
    expect(identity == HELD_LABELS, f'missing row {identity}')


def check_summary() -> None:
    """A hook's worst path is the longest service, W taken off, a path never served before any; alone and under the
    composed load apart, and only its own paths. Its counts are its own, a path over its bound no narrow fit, a path
    one cycle under the layout swing a narrow fit and a path at the swing none, and its ordering results and clauses
    are kept."""
    swing = hooks.LAYOUT_SWING_CYCLES * 1000 / CPU_HZ
    made = [run.hook_row(row(family, ms, wait=wait, probe=name, starved=starved), group)
            for name, family, ms, wait, starved, group in (
                ('fast', 'maap', 2.0, 0.0, False, 'maap'), ('slow', 'maap', 25.0, 0.0, False, 'maap'),
                ('waiting', 'maap', 210.0, 200.0, False, 'maap'),
                ('at-swing', 'maap', 20.0 - swing, 0.0, False, 'maap'),
                ('under-swing', 'maap', 20.0 - swing + 1e-5, 0.0, False, 'maap'),
                ('loaded', 'maap', 30.0, 0.0, False, 'backlog'), ('starved', 'maap', 1.0, 0.0, True, 'backlog'),
                ('other', 'srp', 500.0, 0.0, False, 'srp'), ('other-loaded', 'srp', 900.0, 0.0, True, 'backlog'))]
    for r in made:
        r['slack_cycles'] = run.slack_cycles(r, CPU_HZ)
    slack = {r['probe']: r['slack_cycles'] for r in made}
    expect((slack['at-swing'], slack['under-swing']) == (6490, 6489), f'the rows are not at the swing: {slack}')
    checks = {h: dict(applied=n + 2, undecided=n + 20, findings=[f'ORDER {h}']) for n, h in enumerate(hooks.HOOKS)}
    summaries = run.summary(dict(rows=made, checks=checks))
    got = summaries['H-MAAP']
    expect(got['worst']['alone']['probe'] == 'slow', f'the worst alone is {got["worst"]["alone"]["probe"]}, not slow')
    expect(got['worst']['loaded']['probe'] == 'starved',
           f'the worst under load is {got["worst"]["loaded"]["probe"]}, not the path never served')
    expect(summaries['H-ADP']['worst'] == {} and summaries['H-ADP']['paths'] == 0, 'a hook with no path has a worst')
    expect(got['paths'] == 7, f'{got["paths"]} paths, not 7')
    expect(got['misses'] == 3, f'{got["misses"]} misses, not 3')
    expect(got['narrow'] == 1, f'{got["narrow"]} narrow fits, not 1')
    n = list(hooks.HOOKS).index('H-MAAP')
    expect((got['applied'], got['undecided'], got['ordering_findings']) == (n + 2, n + 20, ['ORDER H-MAAP']),
           f'the ordering results are not kept: {got}')
    hook = hooks.HOOKS['H-MAAP']
    expect((got['ordering'], got['clauses']) == (hook.ordering, hook.clauses), 'the obligation or clauses are not kept')


def check_counter_rows() -> None:
    """The ALL push is reported both ways: as one path, ending at its last push, and as a path per descriptor, each
    ending at its own last push, all from the same change to the same recipients in the same window."""
    g = counters_group()
    others = [d for d in SERVED if d != (5, 0)]
    whole = next(p for p in g.probes if p.name == 'counters.all.if0')
    rows = {(k, n): next((p for p in g.probes if p.name == f'counters.all.t{k}.i{n}.if0'), None) for k, n in others}
    expect(whole.ends == [hooks.notify_end(k, n) for k, n in others], f'the ALL push ends at {whole.ends}')
    expect(None not in rows.values(), f'a descriptor has no row of its own: {rows}')
    expect(len([p for p in g.probes if p.path.startswith('counters.all')]) == len(others) + 1, 'more rows than paths')
    change = g.steps.index(f'ctrchg 0 {hooks.UNKEPT_TYPE:x} 0')
    for (k, n), p in rows.items():
        expect(p.ends == [hooks.notify_end(k, n)], f'{p.name} ends at {p.ends}')
        expect((p.start, p.family, p.recipients, p.until) == (whole.start, 'notify', whole.recipients, whole.until)
               and p.until, f'{p.name} is not the ALL push\'s path')
        expect(g.steps.index(f'mark {p.name}') < change, f'{p.name} opens after the change')
    expect(g.steps.index(f'mark {whole.name}') < change, 'the ALL push opens after the change')
    gaps = {(5, 1): 10 * MS, (6, 0): 30 * MS, (9, 0): 50 * MS, (0x24, 0): 70 * MS}
    grader = grade.Grader(log(pads=[(100, 'CTR', 0)], tx=[(100 + c, CH['aecp'], 0, counter_frame(2, k, n))
                                                          for (k, n), c in gaps.items()]))
    graded = lambda p: run.hook_row(dict(grade.grade_probe(grader, dataclasses.replace(p, recipients=((2, 0),)), 100,
                                                           1 << 62, {}), status='measured'), 'hooks-counters')
    first, later, all_of = graded(rows[(5, 1)]), graded(rows[(6, 0)]), graded(whole)
    expect((first['ms'], later['ms'], all_of['ms']) == (10.0, 30.0, 70.0), f'{first} {later} {all_of}')
    expect(first['within'] and not later['within'] and not all_of['within'], 'a row is not graded at its own bound')
    expect({first['hook'], later['hook'], all_of['hook']} == {'H-COUNTERS'}, 'a row is not H-COUNTERS\'')


def check_amended() -> None:
    """The amended column gives SRP T_svc, and a queued notice its point's ceiling, 20 ms at one interface and 60 ms
    at two; any other path its bound. It grades nothing: the same paths are over the same bounds, and a table says
    which bounds it graded by."""
    expect((hooks.AMENDED_SRP_MS, hooks.AMENDED_QUEUED_CEILING_MS) == (20.0, {1: 20.0, 2: 60.0}), 'the amended bounds')
    graded = graded_with({'srp': [dict(row('srp', 19.0, probe='srp.x.if0'), status='measured')],
                          'hooks-counters': [dict(row('notify', 40.0, probe='counters.all.if0'), status='measured'),
                                             dict(row('notify', 40.0, probe='counters.all.t5.i1.if0'),
                                                  status='measured'),
                                             dict(row('notify', 3.0, probe='counters.first.if0'), status='measured')],
                          'aecp-fanout': [dict(row('notify', 3.0, probe='aecp_fanout.set_name.if0'),
                                               status='measured')]})
    by = {r['probe']: r for r in graded['rows']}
    srp, whole, each, first = (by[x] for x in ('srp.x.if0', 'counters.all.if0', 'counters.all.t5.i1.if0',
                                               'counters.first.if0'))
    expect(hooks.amended_ms(srp, 1) == 20.0 and hooks.amended_ms(srp, 2) == 20.0, f'SRP {hooks.amended_ms(srp, 1)}')
    expect(hooks.amended_ms(run.hook_row(row('srp', 210.0, wait=200.0), 'srp'), 1) == 220.0, 'W left off the column')
    expect([hooks.amended_ms(x, n) for x in (whole, each) for n in (1, 2)] == [20.0, 60.0, 20.0, 60.0],
           'a queued notice\'s ceiling')
    expect(hooks.amended_ms(first, 2) == 20.0 and hooks.amended_ms(by['aecp_fanout.set_name.if0'], 2) == 20.0,
           'a path the decisions leave has another bound')
    held = run.held_row(dict(probe='counters.held.if0', eligible=0, end=MS, ms=1.0, wait_ms=900.0),
                        dict(cpu_hz=CPU_HZ, sys_hz=SYS_HZ))
    expect(hooks.amended_ms(held, 2) == 20.0, 'the column adds W the held bound does not')
    expect((srp['bound_ms'], srp['within'], whole['bound_ms'], whole['within']) == (18.0, False, 20.0, False),
           'the amended bounds graded a path')
    late = [x.split(':')[1].strip() for x in graded['findings'] if x.startswith('LATE ')]
    expect(sorted(late) == ['counters.all.if0', 'counters.all.t5.i1.if0', 'srp.x.if0'], f'findings {late}')
    spec = dict(interfaces=2, arm='idle', cpu_clock='sys', cpu_hz=CPU_HZ, sys_hz=SYS_HZ)
    text = run.table('8x8', spec, graded)
    expect('Graded against the bounds in the tree at this base.' in text, 'the table does not say which bounds graded')
    expect('| Bound at this base, ms | Amended bound, ms, for information |' in text, 'the path table\'s columns')
    expect('| 40.000 | 4,000,000 | 0 | 20 | 60 | NO |' in text, 'the path table\'s amended figure')
    expect('| Amended service bound, ms, for information |' in text, 'the hook table\'s column')
    line = next(x for x in text.splitlines() if x.startswith('| H-COUNTERS | 3 |'))
    expect('| 20, 60 |' in line, f'the hook table\'s amended figures: {line}')


def check_superseded() -> None:
    """An unmeasured probe of a path this harness measures again in its own group, on the same interface, is
    superseded; on another interface, or unmeasured there too beside a row of another path, it stays a refusal, and
    so does a path the table does not name, though that group measured it."""
    lost = dict(probe='acmp.tmr_no_adp.if1', path=['acmp.tmr_no_adp', 1], status='no start', reason='late')
    again = dict(row('disc', 2.0, probe='hooks-disc-aging.tmr_no_adp.if1'), path=['acmp.tmr_no_adp', 1],
                 interface=1, status='measured')
    other = dict(again, interface=0, path=['acmp.tmr_no_adp', 0])
    got = graded_with({'acmp-disc': [lost], 'hooks-disc-aging': [again]})
    expect(not got['refusals'] and len(got['superseded']) == 1, f'superseded: {got}')
    got = graded_with({'acmp-disc': [lost], 'hooks-disc-aging': [other]})
    expect(len(got['refusals']) == 1 and not got['superseded'], f'other interface: {got}')
    unnamed = ['acmp.bind_rx', 1]
    got = graded_with({'acmp-disc': [dict(lost, path=unnamed)], 'hooks-disc-aging': [dict(again, path=unnamed)]})
    expect(len(got['refusals']) == 1 and not got['superseded'], f'a path the table does not name: {got}')
    beside = dict(again, probe='hooks-disc-aging.available.if1', path=['acmp.entity_available', 1])
    own = dict(lost, probe='hooks-disc-aging.tmr_no_adp.if1')
    got = graded_with({'acmp-disc': [lost], 'hooks-disc-aging': [beside, own]})
    expect(len(got['refusals']) == 2 and not got['superseded'], f'another path: {got}')


def check_aging_group() -> None:
    """The aging group answers each sink's PROBE_TX before its input, and its window opens after the arm: its
    TMR_NO_ADP marks follow the ENTITY_AVAILABLE's wait for the arm, on every interface."""
    point = dataclasses.replace(POINT, label='8x8', shape='endstation_ax7101_8x8', interfaces=2)
    steps = hooks.aging_group(point).steps
    answered = [n for n, s in enumerate(steps) if s.startswith('reply ')]
    discovered = min(n for n, s in enumerate(steps) if s.startswith('mark hooks-disc-aging.available'))
    expect(len(answered) == 2 and max(answered) < discovered,
           f'the PROBE_TX answers {answered}, the input {discovered}')
    binds = [n for n, s in enumerate(steps) if s.startswith('frame ') and n < discovered
             and bytes.fromhex(s.split()[2])[15] & 0xF == f.ACMP['BIND_RX']]
    expect(len(binds) == 2 and binds[0] < answered[0] < binds[1] < answered[1],
           f'each sink is not answered before the next is bound: binds {binds}, answers {answered}')
    for i in range(2):
        mark = steps.index(f'mark hooks-disc-aging.tmr_no_adp.if{i}')
        frame = steps.index(f'mark hooks-disc-aging.available.if{i}')
        armed = next(n for n, s in enumerate(steps) if n > frame and s.startswith(f'wait tmr {2 + i} 1 '))
        expect(armed < mark, f'interface {i}: the window opens before the arm ({armed} > {mark})')


def check_buckets_full() -> None:
    """Each composed row of this harness opens its window after the registrations and a wait for every channel's
    token bucket to refill from empty (burst x refill_ms, mailbox.yaml)."""
    expect(hooks.refilled_ms() >= max(ch.burst * ch.refill_ms for ch in scenario.CONTRACT.channels),
           f'refill wait {hooks.refilled_ms()} ms')
    for make in (hooks.loaded_notify_group, hooks.loaded_counters_group):
        steps = make(POINT).steps
        opened = steps.index('mark composed')
        last = max(n for n, s in enumerate(steps) if s.startswith('frame ') and n < opened)
        waits = [s for s in steps[last:opened] if s.startswith('wait cycles ')]
        cycles = sum(int(s.split()[2]) for s in waits)
        expect(cycles >= hooks.refilled_ms() * MS, f'{make.__name__}: {cycles} bus cycles between the last '
                                                   f'registration and the window')


CHECKS: dict[str, Callable[[], None]] = {
    'bounds pinned': check_bounds, 'an 18 to 20 ms SRP path misses': check_srp_instance,
    'the exact bound fits and W adds': check_exact_bound, 'the hooks map': check_hooks_map,
    'the clock labels': check_clock_label, 'the plants apply': check_plants, 'the testbench additions apply':
    check_testbench, 'own lines are split off': check_split, 'H-ADP ordering': check_adp_order,
    'H-DISC ordering': check_disc_order, 'H-ACMP ordering': check_acmp_order, 'H-AECP ordering': check_aecp_order,
    'H-NOTIFY ordering': check_notify_order, 'H-COUNTERS spacing': check_counter_spacing,
    'the held push': check_held_push, 'H-MAAP ordering': check_maap_order, 'H-SRP ordering': check_srp_order,
    'findings by hook': check_findings, 'a fit under the layout swing is a finding': check_narrow,
    'a refusal is superseded only by its own path': check_superseded,
    'the aging window opens after the arm': check_aging_group,
    'a composed row opens on full buckets': check_buckets_full,
    'a plant is caught only by its own finding': check_plant_verdict, 'the held push\'s grade': check_held_grade,
    'a held push never sent': check_missing_held, 'the worst path and the counts': check_summary,
    'the ALL push both ways': check_counter_rows, 'the amended column grades nothing': check_amended,
}


# ---- the mutants --------------------------------------------------------------------------------

def mutant(target: object, name: str, value: object) -> Callable[[], AbstractContextManager]:
    """One rule replaced."""
    return lambda: patch.object(target, name, value)


def held_fields(change: Callable[[dict, dict, dict], dict],
                missing: bool = False) -> Callable[[], AbstractContextManager]:
    """The held push's row with the fields `change` gives, from the held push, the row as written and the spec: a
    measured push's, or with `missing` one never sent."""
    def changed(held: dict, spec: dict) -> dict:
        """The row as written, changed where the mutant applies."""
        r = HELD_ROW(held, spec)
        return {**r, **change(held, r, spec)} if bool(held.get('missing')) == missing else r
    return mutant(run, 'held_row', changed)


def summary_fields(change: Callable[[dict, dict], dict]) -> Callable[[], AbstractContextManager]:
    """Each hook's summary with the fields `change` gives, from that summary and the run's grade."""
    return mutant(run, 'summary', lambda g: {h: {**v, **change(v, g)} for h, v in SUMMARY(g).items()})


def worst_by(key: Callable[[dict], object]) -> Callable[[], AbstractContextManager]:
    """The summaries with each worst path chosen by `key`."""
    def top(g: dict, hook: str, part: str) -> dict:
        """The hook's path of that part `key` puts last."""
        return max((r for r in g['rows'] if r['hook'] == hook and r['loaded'] == (part == 'loaded')), key=key)
    return mutant(run, 'summary', lambda g: {h: {**v, 'worst': {k: top(g, h, k) for k in v['worst']}}
                                             for h, v in SUMMARY(g).items()})


def narrow_under(limit: int) -> Callable[[], AbstractContextManager]:
    """The summaries with each hook's narrow fits counted under `limit`, not the layout swing."""
    return mutant(run, 'summary', lambda g: {h: {**v, 'narrow': sum(r['within'] and r['slack_cycles'] < limit
                                                                    for r in g['rows'] if r['hook'] == h)}
                                             for h, v in SUMMARY(g).items()})


def counters_edited(edit: Callable[[Group], None]) -> Callable[[], AbstractContextManager]:
    """hooks-counters with `edit` made to its group."""
    def made(p: scenario.Point, build: dict) -> list[Group]:
        """The groups as written, edited."""
        out = COUNTERS_GROUPS(p, build)
        edit(out[0])
        return out
    return mutant(hooks, 'counters_groups', made)


def first_descriptor_only(g: Group) -> None:
    """The ALL push ends at its first descriptor."""
    g.probes = [dataclasses.replace(x, ends=x.ends[:1]) if x.path == 'counters.all' else x for x in g.probes]


def no_descriptor_rows(g: Group) -> None:
    """The ALL push has no row per descriptor."""
    g.probes = [x for x in g.probes if not x.path.startswith('counters.all.')]


def rows_end_with_the_push(g: Group) -> None:
    """Each descriptor's row ends where the ALL push does."""
    whole = next(x for x in g.probes if x.path == 'counters.all')
    g.probes = [dataclasses.replace(x, ends=whole.ends) if x.path.startswith('counters.all.') else x for x in g.probes]


def change_before_rows(g: Group) -> None:
    """The change comes before the rows' marks, so they open after it."""
    step = f'ctrchg 0 {hooks.UNKEPT_TYPE:x} 0'
    g.steps.remove(step)
    g.steps.insert(min(n for n, s in enumerate(g.steps) if s.startswith('mark counters.all')), step)


def graded_by_amended(r: dict, group: str) -> dict:
    """A path's verdict read from its amended bound at one interface, its bound as written: only SRP's verdict moves,
    so the rule that fails is the verdict's, not the column's arithmetic or the table's."""
    out = HOOK_ROW(r, group)
    return dict(out, within=not out['unbounded'] and out['ms'] <= hooks.amended_ms(out, 1))


def findings_by_amended(*arguments: object) -> dict:
    """A run's grade with a LATE finding only on a path over its amended bound, every verdict as written."""
    graded = GRADE_ALL(*arguments)
    over = {r['probe'] for r in graded['rows'] if r['ms'] > hooks.amended_ms(r, 2)}
    return dict(graded, findings=[x for x in graded['findings'] if not x.startswith('LATE ')
                                  or x.split(': ')[1] in over])


def row_as_the_tabled_path(r: dict, group: str) -> dict:
    """A path's row, its path read as the one the table has its group supersede: the rule's comparison of paths then
    compares nothing, and any row of that group on the refusal's interface supersedes it."""
    out = HOOK_ROW(r, group)
    return dict(out, path=next((path for path, by in hooks.SUPERSEDED.items() if by == group), out['path']))


def every_refusal_superseded(*arguments: object) -> dict:
    """A run's grade with every refusal superseded, with no regard to any row."""
    graded = GRADE_ALL(*arguments)
    return dict(graded, refusals=[], superseded=[*graded['superseded'], *graded['refusals']])


def window_before_arm(p: scenario.Point) -> Group:
    """The aging group as written, but for each TMR_NO_ADP mark, moved before its arm to beside the input's mark."""
    g = AGING_GROUP(p)
    for i in range(p.interfaces):
        mark = f'mark hooks-disc-aging.tmr_no_adp.if{i}'
        g.steps.remove(mark)
        g.steps.insert(g.steps.index(f'mark hooks-disc-aging.available.if{i}') + 1, mark)
    return g


HELD_GRADE, MISSING_HELD = 'the held push\'s grade', 'a held push never sent'
SUMMARY_CHECK, COUNTER_ROWS = 'the worst path and the counts', 'the ALL push both ways'
AMENDED, PLANT_VERDICT = 'the amended column grades nothing', 'a plant is caught only by its own finding'
MUTANTS: list[tuple[str, Callable[[], AbstractContextManager], str]] = [
    ('bound: a stale T_svc of 10 ms', mutant(hooks, 'T_SVC_MS', 10.0), 'bounds pinned'),
    ('bound: SRP graded against T_svc alone', mutant(hooks, 'bound_ms', lambda family: hooks.T_SVC_MS),
     'an 18 to 20 ms SRP path misses'),
    ('bound: the ceiling alone', mutant(hooks, 'bound_ms', lambda family: scenario.CEILING_MS[family]),
     'bounds pinned'),
    ('bound: the normative wait is not added', mutant(run, 'hook_row', lambda r, g: dict(
        HOOK_ROW(dict(r, wait_ms=0.0), g), wait_ms=r['wait_ms'])), 'the exact bound fits and W adds'),
    ('bound: the margin is taken from a timeout of zero', mutant(hooks, 'normative_ms', lambda hook, family: 0.0),
     'the exact bound fits and W adds'),
    ('map: the counter push is a notification', mutant(hooks, 'COUNTERS_PREFIX', '\0'), 'the hooks map'),
    ('map: no composed row of this harness is loaded', mutant(run, 'LOADED', grade.BACKLOG_ROWS), 'the hooks map'),
    ('label: the Milan clock labelled the product\'s (the earlier rule)', mutant(run, 'clock_label', lambda spec: (
        f'CPU {spec["cpu_hz"] / 1e6:g} MHz on sys (the product split CPU clock)')), 'the clock labels'),
    ('label: the Milan clock the default (the earlier rule)', mutant(hooks_build, 'CPU_CLOCKS', ('milan', 'sys')),
     'the clock labels'),
    ('split: the counter change is no pad', mutant(hooks, 'parsed', lambda t, s, c: (hooks.ORIGINAL_PARSE(
        hooks.split(t)[0], s, c), [])), 'own lines are split off'),
    ('H-ADP: the grandmaster is not checked', mutant(hooks, 'gm_steps', lambda g: []), 'H-ADP ordering'),
    ('H-DISC: the sink\'s PROBE_TX_COMMAND is never recognised', mutant(f, 'ACMP', {**f.ACMP, 'PROBE_TX': -1}),
     'H-DISC ordering'),
    ('H-DISC: the window never ends (the earlier rule ended it at the next tagged record)',
     mutant(hooks, 'next_adp_record', lambda log, i, after: 1 << 62), 'H-DISC ordering'),
    ('H-DISC: a window shorter than the sink\'s TMR_DELAY decides (the earlier rule)',
     mutant(hooks, 'disc_decided_ms', lambda: 0.0), 'H-DISC ordering'),
    ('H-ACMP: no response is matched to its command', mutant(hooks.grade, 'response_sequence', lambda fr: None),
     'H-ACMP ordering'),
    ('H-AECP: no face commit is recognised', mutant(hooks, 'face_commit_words', lambda spec: set()),
     'H-AECP ordering'),
    ('H-NOTIFY: the notification is not found', mutant(hooks.grade.Grader, 'recipients',
                                                        lambda self, *a: ({(2, 0): None}, [])), 'H-NOTIFY ordering'),
    ('H-COUNTERS: spacing of 0.1 s accepted', mutant(hooks, 'COUNTERS_SPACING_MS', 50.0), 'H-COUNTERS spacing'),
    ('H-COUNTERS: the held push from its change', mutant(hooks, 'COUNTERS_SPACING_MS', 0.0), 'the held push'),
    ('H-MAAP: no allocation report is recognised', mutant(hooks, 'MAAP_REPORT_START', (-1, -1, -1)),
     'H-MAAP ordering'),
    ('H-MAAP: every AAF_CTRL store is a report (earlier rule)', mutant(hooks, 'MAAP_REPORT_START', (0x654,)),
     'H-MAAP ordering'),
    ('H-SRP: the ADOPTED bit is never seen set', mutant(hooks, 'adopted', lambda v: False), 'H-SRP ordering'),
    ('plants: a plant edits nothing', mutant(hooks_build, 'plant_text', lambda src, edits: {}),
     'the plants apply'),
    ('supersede: the table names another group', mutant(hooks, 'SUPERSEDED', {'acmp.tmr_no_adp': 'acmp-disc'}),
     'a refusal is superseded only by its own path'),
    ('supersede: the table names a second path', mutant(hooks, 'SUPERSEDED', {**hooks.SUPERSEDED,
                                                                              'acmp.bind_rx': 'hooks-disc-aging'}),
     'a refusal is superseded only by its own path'),
    ('supersede: a row of another path supersedes a refusal', mutant(run, 'hook_row', row_as_the_tabled_path),
     'a refusal is superseded only by its own path'),
    ('supersede: every refusal is superseded', mutant(run, 'grade_all', every_refusal_superseded),
     'a refusal is superseded only by its own path'),
    ('aging: the window opens before the arm (the earlier rule)', mutant(hooks, 'aging_group', window_before_arm),
     'the aging window opens after the arm'),
    ('aging: the sink still waits for its PROBE_TX_RESPONSE (the earlier rule)', mutant(scenario, 'probe_answer',
                                                                                     lambda i, status=0: 'gap 20'),
     'the aging window opens after the arm'),
    ('aging: both sinks bound before either is answered (the earlier rule)', mutant(hooks, 'aging_group',
     lambda p: Group('hooks-disc-aging', steps=[*(f'frame {i} {scenario.acmp_cmd(p, "BIND_RX", i, 1).hex()}'
                                                  for i in range(2)), *(scenario.probe_answer(i) for i in range(2)),
                                                *(f'mark hooks-disc-aging.available.if{i}' for i in range(2)),
                                                *(f'wait tmr {2 + i} 1 within 1' for i in range(2)),
                                                *(f'mark hooks-disc-aging.tmr_no_adp.if{i}' for i in range(2))])),
     'the aging window opens after the arm'),
    ('buckets: the window opens right after the registrations (the earlier rule)', mutant(hooks, 'refilled_ms',
                                                                                     lambda: 0),
     'a composed row opens on full buckets'),
    ('findings: a path over its bound is not a finding', mutant(run, 'hook_row', lambda r, g: dict(
        HOOK_ROW(r, g), within=True)), 'findings by hook'),
    ('narrow: the layout swing is not applied', mutant(hooks, 'LAYOUT_SWING_CYCLES', 0),
     'a fit under the layout swing is a finding'),
    ('narrow: the slack counted at the 50 MHz CPU (the earlier clock)', mutant(run, 'slack_cycles', lambda r, hz: (
        SLACK(r, hz // 2))), 'a fit under the layout swing is a finding'),
    ('plant: any finding of the hook catches it (the earlier rule)', mutant(run, 'plant_findings', lambda p, found: [
        x for x in found if x.startswith(p.words + ':')]), PLANT_VERDICT),
    ('plant: any finding of its kind catches it', mutant(run, 'plant_findings', lambda p, found: [
        x for x in found if x.startswith(p.words.split()[0])]), PLANT_VERDICT),
    ('plant: a path that only starts with its own catches it', mutant(run, 'plant_findings', lambda p, found: [
        x for x in found if x.startswith(f'{p.words}: {p.probe}')]), PLANT_VERDICT),
    ('plant: a late plant names no path', mutant(hooks, 'plants', lambda: {
        k: (h, dataclasses.replace(p, probe=None)) for k, (h, p) in PLANTS.items()}), PLANT_VERDICT),
    ('plant: every run is caught', mutant(run, 'plant_findings', lambda p, found: [p.words]), PLANT_VERDICT),
    ('plant: an escape exits 0', mutant(run, 'main', lambda: MAIN() and 0), PLANT_VERDICT),
    ('held: W added to its bound', held_fields(lambda h, r, s: dict(
        bound_ms=r['bound_ms'] + h['wait_ms'], within=h['ms'] <= r['bound_ms'] + h['wait_ms'])), HELD_GRADE),
    ('held: the exact bound misses', held_fields(lambda h, r, s: dict(within=h['ms'] < r['bound_ms'])), HELD_GRADE),
    ('held: the verdict is relaxed by 1 ms', held_fields(lambda h, r, s: dict(within=h['ms'] <= r['bound_ms'] + 1)),
     HELD_GRADE),
    ('held: its row reports no time', held_fields(lambda h, r, s: dict(ms=0.0)), HELD_GRADE),
    ('held: its row reports a millisecond more', held_fields(lambda h, r, s: dict(ms=h['ms'] + 1)), HELD_GRADE),
    ('held: W is not recorded', held_fields(lambda h, r, s: dict(wait_ms=0.0)), HELD_GRADE),
    ('held: its cycles round down', held_fields(lambda h, r, s: dict(
        cpu_cycles=(h['end'] - h['eligible']) * s['cpu_hz'] // s['sys_hz'])), HELD_GRADE),
    ('held: its cycles are the bus\'s', held_fields(lambda h, r, s: dict(cpu_cycles=h['end'] - h['eligible'])),
     HELD_GRADE),
    ('held: its margin omits W', held_fields(lambda h, r, s: dict(margin_ms=round(r['normative_ms'] - h['ms'], 5))),
     HELD_GRADE),
    ('held: its margin is rounded to the millisecond', held_fields(lambda h, r, s: dict(
        margin_ms=round(r['margin_ms']))), HELD_GRADE),
    ('held: its timeout is the notification family\'s', held_fields(lambda h, r, s: dict(
        normative_ms=hooks.NORMATIVE_MS['notify'])), HELD_GRADE),
    ('held: it counts as under the composed load', held_fields(lambda h, r, s: dict(loaded=True)), HELD_GRADE),
    ('held: it counts as never served', held_fields(lambda h, r, s: dict(unbounded=True)), HELD_GRADE),
    ('held: it is H-NOTIFY\'s', held_fields(lambda h, r, s: dict(hook='H-NOTIFY')), HELD_GRADE),
    ('held: it names another probe', held_fields(lambda h, r, s: dict(probe='counters.first.if0')), HELD_GRADE),
    ('held missing: silently accepted', held_fields(lambda h, r, s: dict(missing=False, within=True, unbounded=False),
                                                    missing=True), MISSING_HELD),
    ('held missing: it fits', held_fields(lambda h, r, s: dict(within=True), missing=True), MISSING_HELD),
    ('held missing: it counts as served', held_fields(lambda h, r, s: dict(unbounded=False), missing=True),
     MISSING_HELD),
    ('held missing: its finding by name is dropped', held_fields(lambda h, r, s: dict(missing=False),
                                                                   missing=True), MISSING_HELD),
    ('held missing: its timeout is the notification family\'s', held_fields(lambda h, r, s: dict(
        normative_ms=hooks.NORMATIVE_MS['notify']), missing=True), MISSING_HELD),
    ('held missing: it records CPU cycles', held_fields(lambda h, r, s: dict(cpu_cycles=1), missing=True),
     MISSING_HELD),
    ('held missing: it records a W', held_fields(lambda h, r, s: dict(wait_ms=9.0), missing=True), MISSING_HELD),
    ('held missing: it records a margin', held_fields(lambda h, r, s: dict(margin_ms=5.0), missing=True), MISSING_HELD),
    ('held missing: it is another group\'s', held_fields(lambda h, r, s: dict(group='hooks-x'), missing=True),
     MISSING_HELD),
    ('held missing: it is another path\'s', held_fields(lambda h, r, s: dict(path='counters.x'), missing=True),
     MISSING_HELD),
    ('held missing: it is another interface\'s', held_fields(lambda h, r, s: dict(interface=1), missing=True),
     MISSING_HELD),
    ('held missing: it is another family\'s', held_fields(lambda h, r, s: dict(family='aecp'), missing=True),
     MISSING_HELD),
    ('summary: the fastest path is the worst', worst_by(lambda r: -r['ms']), SUMMARY_CHECK),
    ('summary: W is left in the service', worst_by(lambda r: (r['unbounded'], r['ms'])), SUMMARY_CHECK),
    ('summary: a path never served is not worst first', worst_by(lambda r: r['ms'] - r['wait_ms']), SUMMARY_CHECK),
    ('summary: alone and under load are not apart', mutant(run, 'summary', lambda g: SUMMARY(
        dict(g, rows=[dict(r, loaded=False) for r in g['rows']]))), SUMMARY_CHECK),
    ('summary: alone and under load are swapped', summary_fields(lambda v, g: dict(
        worst={'alone' if k == 'loaded' else 'loaded': r for k, r in v['worst'].items()})), SUMMARY_CHECK),
    ('summary: another hook\'s paths are its own', mutant(run, 'summary', lambda g: {
        h: SUMMARY(dict(g, rows=[dict(r, hook=h) for r in g['rows']]))[h] for h in hooks.HOOKS}), SUMMARY_CHECK),
    ('summary: a miss counts as a narrow fit', summary_fields(lambda v, g: dict(narrow=v['narrow'] + v['misses'])),
     SUMMARY_CHECK),
    ('summary: no narrow fit is counted', summary_fields(lambda v, g: dict(narrow=0)), SUMMARY_CHECK),
    ('summary: a fit by the swing itself is narrow', narrow_under(hooks.LAYOUT_SWING_CYCLES + 1), SUMMARY_CHECK),
    ('summary: a fit one cycle under the swing is not narrow', narrow_under(hooks.LAYOUT_SWING_CYCLES - 1),
     SUMMARY_CHECK),
    ('summary: no miss is counted', summary_fields(lambda v, g: dict(misses=0)), SUMMARY_CHECK),
    ('summary: the path count is every hook\'s', summary_fields(lambda v, g: dict(paths=len(g['rows']))),
     SUMMARY_CHECK),
    ('summary: the applied count is dropped', summary_fields(lambda v, g: dict(applied=0)), SUMMARY_CHECK),
    ('summary: the undecided count is dropped', summary_fields(lambda v, g: dict(undecided=0)), SUMMARY_CHECK),
    ('summary: the ordering findings are dropped', summary_fields(lambda v, g: dict(ordering_findings=[])),
     SUMMARY_CHECK),
    ('summary: the obligation is dropped', summary_fields(lambda v, g: dict(ordering='')), SUMMARY_CHECK),
    ('summary: the clauses are dropped', summary_fields(lambda v, g: dict(clauses='')), SUMMARY_CHECK),
    ('ALL: the push ends at its first descriptor', counters_edited(first_descriptor_only), COUNTER_ROWS),
    ('ALL: no descriptor has a row', counters_edited(no_descriptor_rows), COUNTER_ROWS),
    ('ALL: a descriptor\'s row ends at the whole push', counters_edited(rows_end_with_the_push), COUNTER_ROWS),
    ('ALL: a descriptor\'s row opens after the change', counters_edited(change_before_rows), COUNTER_ROWS),
    ('amended: SRP keeps its ceiling', mutant(hooks, 'AMENDED_SRP_MS', 18.0), AMENDED),
    ('amended: the ceiling at two interfaces is 20 ms', mutant(hooks, 'AMENDED_QUEUED_CEILING_MS', {1: 20.0, 2: 20.0}),
     AMENDED),
    ('amended: every counter push is queued', mutant(hooks, 'QUEUED_PATH', 'counters.'), AMENDED),
    ('amended: W is left off', mutant(hooks, 'amended_ms', lambda r, n: hooks.amended_service_ms(r, n)), AMENDED),
    ('amended: the column grades a path', mutant(run, 'hook_row', graded_by_amended), AMENDED),
    ('amended: a finding reads the column', mutant(run, 'grade_all', findings_by_amended), AMENDED),
    ('amended: the table does not say which bounds graded', mutant(run, 'BOUNDS_NOTE', ''), AMENDED),
    ('amended: the column repeats the bound', mutant(hooks, 'amended_ms', lambda r, n: r['bound_ms']), AMENDED),
]


def run_checks() -> dict[str, str | None]:
    """Every check's failure, None where it passed."""
    out = {}
    for name, check in CHECKS.items():
        try:
            check()
            out[name] = None
        except Failed as error:
            out[name] = str(error)
        except Exception as error:  # noqa: BLE001  a check that raises is a failure of that check
            out[name] = f'{type(error).__name__}: {error}'
    return out


def main() -> int:
    """The checks must pass; then every mutant must fail its named check."""
    results = run_checks()
    failed = {k: v for k, v in results.items() if v}
    for name, why in results.items():
        print(f'{"PASS" if why is None else "FAIL"} {name}{"" if why is None else ": " + why}')
    escaped = []
    for name, make, named in MUTANTS:
        with ExitStack() as stack:
            stack.enter_context(make())
            got = run_checks()
        caught = got[named] is not None
        escaped += [] if caught else [name]
        print(f'MUTANT {name}: {"caught by " + named if caught else "ESCAPED " + named}')
    print(f'ctrl_service_hooks self-test: {len(CHECKS) - len(failed)} of {len(CHECKS)} checks pass; '
          f'{len(MUTANTS) - len(escaped)} of {len(MUTANTS)} mutants caught')
    return 1 if failed or escaped else 0


if __name__ == '__main__':
    raise SystemExit(main())
