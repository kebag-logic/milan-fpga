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

import sys
import tempfile
from collections.abc import Callable
from contextlib import AbstractContextManager, ExitStack
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hooks  # noqa: E402
import hooks_build  # noqa: E402
import run  # noqa: E402
import grade  # noqa: E402  the CPU budget harness's grader, read only
import scenario  # noqa: E402
from scenario import CH, Group, Probe  # noqa: E402
import frames as f  # noqa: E402

MS = hooks.BUS_MS
#: The path grade as written, which two mutants wrap.
HOOK_ROW = run.hook_row
#: The bounds the owner's decision of 2026-10-29 gives (#665, issuecomment-6495692075), restated.
BOUNDS = {'adp': 20.0, 'disc': 20.0, 'acmp': 20.0, 'aecp': 20.0, 'notify': 20.0, 'maap': 20.0, 'srp': 18.0}
NORMATIVE = {'adp': 2000.0, 'disc': 200.0, 'acmp': 200.0, 'aecp': 240.0, 'notify': 240.0, 'maap': 500.0,
             'srp': 180.0}
FAMILIES = {'adp': 'H-ADP', 'disc': 'H-DISC', 'acmp': 'H-ACMP', 'aecp': 'H-AECP', 'notify': 'H-NOTIFY',
            'maap': 'H-MAAP', 'srp': 'H-SRP'}


class Failed(AssertionError):
    """A named check's failure."""


def expect(ok: bool, what: str) -> None:
    """Fail the running check with what, unless ok."""
    if not ok:
        raise Failed(what)


def log(**fields: object) -> grade.Log:
    """A synthetic parsed log at the product clocks."""
    out = grade.Log(100_000_000, 50_000_000)
    for name, value in fields.items():
        setattr(out, name, value)
    return out


def work(start: int, writes: list[tuple[int, int, int]]) -> grade.Pass:
    """A work pass starting at start with the given writes."""
    return grade.Pass(0, start, start // 2, 1000, {}, writes, {})


def row(family: str, ms: float, wait: float = 0.0, probe: str = 'x.if0', **more: object) -> dict:
    """A graded path as the CPU budget harness's grader writes it."""
    return dict(probe=probe, row='r', family=family, interface=0, path=[probe.rsplit('.', 1)[0], 0], ms=ms,
                cpu_cycles=int(ms * 50_000), wait_ms=wait, **more)


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
    """The product clock is labelled the product's; the 100 MHz variant is labelled a variant, never the product's."""
    product = run.clock_label(dict(cpu_hz=50_000_000, sys_hz=100_000_000, product_cpu_hz=50_000_000,
                                   cpu_clock='product'))
    variant = run.clock_label(dict(cpu_hz=100_000_000, sys_hz=100_000_000, product_cpu_hz=50_000_000,
                                   cpu_clock='variant'))
    expect('product split CPU clock' in product and 'variant' not in product, product)
    expect('labelled variant, not the product' in variant and '50 MHz' in variant, variant)


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
    parsed, _ = hooks.parsed('CTRCHG 7 1 5 0\n', 100_000_000, 50_000_000)
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
    """H-DISC: DEPARTING then AVAILABLE then a PROBE_TX passes; without the PROBE_TX it is reported."""
    rxc = [(100, CH['adp'], 0, 'acmp.entity_departing.if0', 82), (200, CH['adp'], 0, 'acmp.entity_available.if0', 82)]
    probe = bytearray(70)
    probe[14], probe[15] = 0xFC, f.ACMP['PROBE_TX']
    good = log(rxc=rxc, tx=[(300, CH['acmp'], 0, bytes(probe))])
    ok, wrong = hooks.discovery_order(good, Group('g'), [], {'interfaces': 1}), hooks.discovery_order(
        log(rxc=rxc), Group('g'), [], {'interfaces': 1})
    expect(ok.applied == 1 and not ok.findings, f'clean: {ok}')
    expect(wrong.findings and wrong.findings[0].startswith('ORDER H-DISC:'), f'defective: {wrong}')


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
    word = min(hooks.face_commit_words({'interfaces': 1}))
    tx = [(300, CH['aecp'], 0, aem_response(0x10))]
    good = log(rxc=rxc, tx=tx, writes=[(200, word, 1)])
    bad = log(rxc=rxc, tx=tx, writes=[(400, word, 1)])
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


def counter_frame(recipient: int = 2) -> bytes:
    """An unsolicited GET_COUNTERS of STREAM_INPUT 0 to the recipient."""
    frame = bytearray(aem_response(0, True, hooks.GET_COUNTERS))
    frame[26:34] = recipient.to_bytes(8, 'big')
    frame[38:40], frame[40:42] = (5).to_bytes(2, 'big'), (0).to_bytes(2, 'big')
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
        held = hooks.held_push(synthetic, Group('hooks-counters'), {'sys_hz': 100_000_000, 'cpu_hz': 50_000_000})
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
        return run.grade_all([Group(n) for n in probes], [Text(n) for n in probes], {}, Path(out))


def check_superseded() -> None:
    """An unmeasured probe of a path this harness measures again in its own group, on the same interface, is
    superseded; on another interface, or unmeasured there too, it stays a refusal."""
    lost = dict(probe='acmp.tmr_no_adp.if1', path=['acmp.tmr_no_adp', 1], status='no start', reason='late')
    again = dict(row('disc', 2.0, probe='hooks-disc-aging.tmr_no_adp.if1'), path=['acmp.tmr_no_adp', 1],
                 interface=1, status='measured')
    other = dict(again, interface=0, path=['acmp.tmr_no_adp', 0])
    got = graded_with({'acmp-disc': [lost], 'hooks-disc-aging': [again]})
    expect(not got['refusals'] and len(got['superseded']) == 1, f'superseded: {got}')
    got = graded_with({'acmp-disc': [lost], 'hooks-disc-aging': [other]})
    expect(len(got['refusals']) == 1 and not got['superseded'], f'other interface: {got}')
    got = graded_with({'acmp-disc': [dict(lost, path=['acmp.bind_rx', 1])], 'hooks-disc-aging': [again]})
    expect(len(got['refusals']) == 1, f'another path: {got}')


def check_aging_group() -> None:
    """The aging group's window opens after the arm: its TMR_NO_ADP marks follow the ENTITY_AVAILABLE's wait for
    the arm, on every interface."""
    point = scenario.Point('8x8', 'endstation_ax7101_8x8', 2, 1, 2, 1, 1)
    steps = hooks.aging_group(point).steps
    for i in range(2):
        mark = steps.index(f'mark hooks-disc-aging.tmr_no_adp.if{i}')
        frame = steps.index(f'mark hooks-disc-aging.available.if{i}')
        armed = next(n for n, s in enumerate(steps) if n > frame and s.startswith(f'wait tmr {2 + i} 1 '))
        expect(armed < mark, f'interface {i}: the window opens before the arm ({armed} > {mark})')


CHECKS: dict[str, Callable[[], None]] = {
    'bounds pinned': check_bounds, 'an 18 to 20 ms SRP path misses': check_srp_instance,
    'the exact bound fits and W adds': check_exact_bound, 'the hooks map': check_hooks_map,
    'the clock labels': check_clock_label, 'the plants apply': check_plants, 'the testbench additions apply':
    check_testbench, 'own lines are split off': check_split, 'H-ADP ordering': check_adp_order,
    'H-DISC ordering': check_disc_order, 'H-ACMP ordering': check_acmp_order, 'H-AECP ordering': check_aecp_order,
    'H-NOTIFY ordering': check_notify_order, 'H-COUNTERS spacing': check_counter_spacing,
    'the held push': check_held_push, 'H-MAAP ordering': check_maap_order, 'H-SRP ordering': check_srp_order,
    'findings by hook': check_findings, 'a refusal is superseded only by its own path': check_superseded,
    'the aging window opens after the arm': check_aging_group,
}


# ---- the mutants --------------------------------------------------------------------------------

def mutant(target: object, name: str, value: object) -> Callable[[], AbstractContextManager]:
    """One rule replaced."""
    return lambda: patch.object(target, name, value)


MUTANTS: list[tuple[str, Callable[[], AbstractContextManager], str]] = [
    ('bound: a stale T_svc of 10 ms', mutant(hooks, 'T_SVC_MS', 10.0), 'bounds pinned'),
    ('bound: SRP graded against T_svc alone', mutant(hooks, 'bound_ms', lambda family: hooks.T_SVC_MS),
     'an 18 to 20 ms SRP path misses'),
    ('bound: the ceiling alone', mutant(hooks, 'bound_ms', lambda family: scenario.CEILING_MS[family]),
     'bounds pinned'),
    ('bound: the normative wait is not added', mutant(run, 'hook_row', lambda r, g: dict(
        HOOK_ROW(dict(r, wait_ms=0.0), g), wait_ms=r['wait_ms'])), 'the exact bound fits and W adds'),
    ('bound: the margin is not recorded', mutant(hooks, 'normative_ms', lambda hook, family: 0.0),
     'the exact bound fits and W adds'),
    ('map: the counter push is a notification', mutant(hooks, 'COUNTERS_PREFIX', '\0'), 'the hooks map'),
    ('map: no composed row of this harness is loaded', mutant(run, 'LOADED', grade.BACKLOG_ROWS), 'the hooks map'),
    ('label: the variant labelled the product\'s', mutant(run, 'clock_label', lambda spec: 'CPU (the product split '
     'CPU clock)'), 'the clock labels'),
    ('split: the counter change is no pad', mutant(hooks, 'parsed', lambda t, s, c: (hooks.ORIGINAL_PARSE(
        hooks.split(t)[0], s, c), [])), 'own lines are split off'),
    ('H-ADP: the grandmaster is not checked', mutant(hooks, 'gm_steps', lambda g: []), 'H-ADP ordering'),
    ('H-DISC: no probe is required', mutant(f, 'ACMP', {**f.ACMP, 'PROBE_TX': -1}), 'H-DISC ordering'),
    ('H-ACMP: overlapping commands are not compared', mutant(hooks.grade, 'response_sequence', lambda fr: None),
     'H-ACMP ordering'),
    ('H-AECP: no face commit is recognised', mutant(hooks, 'face_commit_words', lambda spec: set()),
     'H-AECP ordering'),
    ('H-NOTIFY: the notification is not found', mutant(hooks.grade.Grader, 'recipients',
                                                        lambda self, *a: ({(2, 0): None}, [])), 'H-NOTIFY ordering'),
    ('H-COUNTERS: spacing of 0.1 s accepted', mutant(hooks, 'COUNTERS_SPACING_MS', 50.0), 'H-COUNTERS spacing'),
    ('H-COUNTERS: the held push from its change', mutant(hooks, 'COUNTERS_SPACING_MS', 0.0), 'the held push'),
    ('H-MAAP: the publication is not looked for', mutant(hooks, 'MAAP_REPORT_START', (-1, -1, -1)),
     'H-MAAP ordering'),
    ('H-MAAP: every AAF_CTRL store is a report (earlier rule)', mutant(hooks, 'MAAP_REPORT_START', (0x654,)),
     'H-MAAP ordering'),
    ('H-SRP: the ADOPTED bit is never seen set', mutant(hooks, 'adopted', lambda v: False), 'H-SRP ordering'),
    ('plants: an anchor may occur twice', mutant(hooks_build, 'plant_text', lambda src, edits: {}),
     'the plants apply'),
    ('supersede: any later group supersedes a refusal', mutant(hooks, 'SUPERSEDED', {'acmp.tmr_no_adp': 'acmp-disc',
                                                                                  'acmp.bind_rx': 'hooks-disc-aging'}),
     'a refusal is superseded only by its own path'),
    ('aging: the window opens before the arm (the earlier rule)', mutant(hooks, 'aging_group', lambda p: Group(
        'hooks-disc-aging', steps=[*[f'mark hooks-disc-aging.available.if{i}' for i in range(2)],
                                   *[f'mark hooks-disc-aging.tmr_no_adp.if{i}' for i in range(2)],
                                   *[f'wait tmr {2 + i} 1 within 1' for i in range(2)]])),
     'the aging window opens after the arm'),
    ('findings: a path over its bound is not a finding', mutant(run, 'hook_row', lambda r, g: dict(
        HOOK_ROW(r, g), within=True)), 'findings by hook'),
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
