# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The wire-timing grader's controls (#665, #868), on synthetic logs, with no build, and its plants on real logs.

A synthetic log is wire_main.cpp's output for two draws, written from the
frames the stimulus sends and the answers a correct entity gives: each bind
answered and its PROBE_TX's answer handled, each AEM command answered, MAAP's
acquisition (four PROBEs on three probe expiries, then the ANNOUNCE on the
last) and ADP's startup ENTITY_AVAILABLE, each commit leaving KL_mbx (MTX)
before the MAC. The announce log adds a second ANNOUNCE and ADP's periodic
ENTITY_AVAILABLEs over 34 s. Each clean log must pass. Each control then
changes one thing and must be graded by its own words: refused, or a finding.
shifted-clock is #868 item 4's grader with a shifted clock: the clean log
graded at another clock, which the clock check refuses before any figure is
converted; egress-past-reserve is its egress delay planted past the 11 ms
reserve.

plants() is the same pair on a real run's log, which run.py grades after
every run: the first timer-driven PROBE moved one millisecond past the reserve
at the MAC, and the log graded at a shifted clock.
"""
from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import wire_grade as g  # noqa: E402
import wire_scenario as s  # noqa: E402

f = s.f
SYS_HZ = 100_000_000
MS = SYS_HZ // 1000
ENTITY, ENTITY_MAC = 0x020000FFFE000001, 0x020000000001
POINT = s.budget.Point('1x1', 'endstation_ax7101_1x1_tdm8', 1, ENTITY, ENTITY_MAC, 2, 2)
CH = {name: n for n, name in enumerate(g.CHANNELS)}
#: Where the synthetic acquisition draws its intervals (ms): three probe intervals, then the announce interval.
PROBE_DRAWS = (558, 519, 513)
ANNOUNCE_DRAW = 31_000
#: ADP's startup delay deadline and its periodic delays (ms), Milan v1.2 5.6.3.5.2 and Table 5.50.
ADP_STARTUP = 404
ADP_DELAYS = (1200, 3000, 0, 2500, 3999)


def acmp_frame(kind: int, seq: int, sa: int) -> str:
    """An ACMP frame of one message type and sequence_id, as hex."""
    return f.acmp(kind, sa, f.Acmp(controller=s.CTL1, talker=s.budget.TALKER_A, listener=ENTITY, talker_uid=1,
                                   sequence=seq)).hex()


def answered(command: bytes, status: int = 0) -> str:
    """An AECP command's response: its message_type the response's (0 to 1, 6 to 7), with a status."""
    frame = bytearray(command)
    frame[15] = (frame[15] & 0xF0) | g.AECP_RESPONSE_OF[frame[15] & 0x0F]
    frame[16] = (frame[16] & 0x07) | (status << 3)
    return bytes(frame).hex()


class Synth:
    """A synthetic log: its lines, and each channel's commits so far."""

    def __init__(self, ms_count: int) -> None:
        self.lines = [f'MS {k * MS} {k}' for k in range(1, ms_count)] + [f'READY {2 * MS}']
        self.heads = dict.fromkeys(range(len(g.CHANNELS)), 0)

    def send(self, at: int, channel: str, frame: str, size: int = 60) -> None:
        """A commit at `at`, the frame's last byte out of KL_mbx 100 cycles on, and its first and last beat at
        the MAC."""
        ch = CH[channel]
        self.heads[ch] += 20
        self.lines += [f'TXC {at} {ch} {self.heads[ch]}', f'MTX {at + 100} 0 {ch}', f'TXW {at + 36} {at + 136} '
                       f'{size} {frame}']

    def arm(self, at: int, slot: int, deadline: int, op: int = 1) -> None:
        """A TMR_CMD write of one slot: an arm (op 1) or a cancel (op 2), with the last deadline written."""
        self.lines.append(f'TMR {at} {(op << 30) | (1 << 8) | slot:08x} {deadline}')

    def text(self) -> list[str]:
        """The lines in cycle order, the tally last."""
        body = sorted(self.lines, key=lambda ln: int(ln.split()[1]))
        return body + ['SUMMARY sys=40000000', '== ctrl_wire_timing: checks: 1   failures: 0 ==']


def maap_frame(kind: int) -> str:
    """One of this entity's MAAPDUs (IEEE 1722-2016 B.2), as hex."""
    return f.maap(kind, ENTITY_MAC, (0x91E0F0000100, 8)).hex()


def acquisition(log: Synth, announces: int = 1, probe_draws: tuple[int, ...] = PROBE_DRAWS,
                late_arm_ms: int = 0) -> None:
    """MAAP on interface 0: the first PROBE at 40 ms with the next deadline armed before its commit, as the
    firmware arms it; each expiry's PROBE; the last expiry's PROBE and ANNOUNCE; then each announce interval.
    late_arm_ms: the first expiry's next deadline armed that long after its PROBE left, from that millisecond."""
    slot = g.MAAP_FIRST_SLOT_IFS
    now, deadline = 40, 40 + probe_draws[0]
    log.arm(now * MS + 10, slot, deadline)
    log.send(now * MS + 50, 'maap', maap_frame(g.MAAP_PROBE))
    for n, draw in enumerate((*probe_draws[1:], ANNOUNCE_DRAW)):
        late = late_arm_ms if n == 0 else 0
        now, deadline = deadline, deadline + late + draw
        log.arm(now * MS + 2000 + late * MS, slot, deadline)
        log.send(now * MS + 3000, 'maap', maap_frame(g.MAAP_PROBE))
    log.send(now * MS + 3500, 'maap', maap_frame(g.MAAP_ANNOUNCE))
    for _ in range(announces - 1):
        now, deadline = deadline, deadline + ANNOUNCE_DRAW
        log.arm(now * MS + 2000, slot, deadline)
        log.send(now * MS + 3000, 'maap', maap_frame(g.MAAP_ANNOUNCE))


def advertising(log: Synth, delays: tuple[int, ...] = (), advertise_ms: int = g.ADP_ADVERTISE_MS,
                late_cycles: int = 400, twice: bool = False) -> None:
    """ADP on interface 0: the startup delay, its ENTITY_AVAILABLE and the advertise timer armed after it; then
    each advertise expiry's delay and its ENTITY_AVAILABLE (Milan v1.2 5.6.3.5)."""
    available = f.adp(f.ADP_AVAILABLE, ENTITY, ENTITY_MAC, f.Adp(valid_time=10)).hex()
    log.arm(5 * MS, 0, ADP_STARTUP)
    expiry = ADP_STARTUP
    for delay in (None, *delays):
        if delay is not None:
            log.arm(expiry * MS + 300, 0, expiry + delay)
            expiry += delay
        log.send(expiry * MS + late_cycles, 'adp', available, size=82)
        if twice and delay is not None:   # the same expiry's ENTITY_AVAILABLE sent a second time, a millisecond on
            log.send(expiry * MS + late_cycles + MS, 'adp', available, size=82)
            twice = False
        log.arm(expiry * MS + late_cycles + 1000, 0, expiry + advertise_ms)
        expiry += advertise_ms


def draws(log: Synth, response_cycles: int = 50_000, aecp_cycles: int = 80_000, interim: bool = False) -> None:
    """Two draws: a bind answered after response_cycles, its probe and the talker's answer handled, and an AEM
    command answered after aecp_cycles."""
    for k, at in enumerate((100 * MS, 200 * MS)):
        seq, probe_seq = 0x4100 + 2 * k, 0x10 + k
        log.lines.append(f'RXW {at} {at + 30} 60 acmp-bind-{k} {acmp_frame(f.ACMP["BIND_RX"], seq, s.budget.CTL_MAC)}')
        log.send(at + response_cycles - 136, 'acmp', acmp_frame(f.ACMP['BIND_RX_RESPONSE'], seq, ENTITY_MAC))
        log.send(at + response_cycles + 64, 'acmp', acmp_frame(f.ACMP['PROBE_TX'], probe_seq, ENTITY_MAC))
        log.lines.append(f'RXW {at + response_cycles + 300} {at + response_cycles + 330} 60 talker '
                         f'{acmp_frame(f.ACMP["PROBE_TX_RESPONSE"], probe_seq, s.budget.TALKER_A_MAC)}')
        # its own timeout, committed after the prompt answer's last byte in, as the bench measures it
        log.arm(at + response_cycles + 350, g.ACMP_FIRST_SLOT_IFS, at // MS + 200)
        log.arm(at + response_cycles + 5000, g.ACMP_FIRST_SLOT_IFS, at // MS + 10000)   # its handling
        cmd_at = at + 80 * MS
        name, command = s.aecp_command(POINT, k, 0x6100 + k)
        log.lines.append(f'RXW {cmd_at} {cmd_at + 30} {len(command)} aecp-{name}-{k} {command.hex()}')
        if interim:
            log.send(cmd_at + 1000, 'aecp', answered(command, g.AECP_IN_PROGRESS))
        log.send(cmd_at + aecp_cycles - 136, 'aecp', answered(command))


def clean(probe_draws: tuple[int, ...] = PROBE_DRAWS, late_arm_ms: int = 0, **changes: object) -> Synth:
    """The draws, MAAP's acquisition and ADP's startup advertisement over 1.8 s."""
    log = Synth(1800)
    draws(log, **changes)
    acquisition(log, probe_draws=probe_draws, late_arm_ms=late_arm_ms)
    advertising(log)
    return log


def announced(delays: tuple[int, ...] = ADP_DELAYS, **changes: object) -> Synth:
    """The draws over 37 s: two ANNOUNCEs one announce interval apart, and ADP's periodic advertising."""
    log = Synth(37_000)
    draws(log)
    acquisition(log, announces=2)
    advertising(log, delays, **changes)
    return log


def without(lines: list[str], what: Callable[[str], bool]) -> list[str]:
    """The lines `what` does not select."""
    return [ln for ln in lines if not what(ln)]


def is_bind_response(line: str) -> bool:
    """The first draw's BIND_RX_RESPONSE at the wire."""
    return line.startswith('TXW') and line.endswith(acmp_frame(f.ACMP['BIND_RX_RESPONSE'], 0x4100, ENTITY_MAC))


def is_aecp_response(line: str) -> bool:
    """The first draw's AEM response at the wire."""
    if not line.startswith('TXW'):
        return False
    data = bytes.fromhex(line.split()[4])
    return data[14] == 0xFB and int.from_bytes(data[34:36], 'big') == 0x6100


def late_commit(line: str) -> str:
    """The first ACMP commit moved past its frame's first byte out."""
    w = line.split()
    return f'TXC {int(w[1]) + 1000} 1 20' if w[0] == 'TXC' and w[2:] == ['1', '20'] else line


def moved(lines: list[str], select: Callable[[str], bool], cycles: int) -> list[str]:
    """The lines `select` picks with their two cycle stamps moved by `cycles`."""
    out = []
    for ln in lines:
        w = ln.split()
        out.append(' '.join([w[0], str(int(w[1]) + cycles), str(int(w[2]) + cycles), *w[3:]]) if select(ln) else ln)
    return out


def nth_maap(kind: int, n: int) -> Callable[[str], bool]:
    """The n-th MAAP frame of one type at the MAC."""
    seen = [0]

    def pick(line: str) -> bool:
        """Count the line if it is that type's MAAP frame; True at the n-th."""
        w = line.split()
        if not w or w[0] != 'TXW' or w[4][24:32] != f'22f0fe{kind:02x}':
            return False
        seen[0] += 1
        return seen[0] == n
    return pick


def slot_arm(slot: int, deadline: int) -> Callable[[str], bool]:
    """The arm of a slot with one deadline."""
    return lambda ln: ln.startswith('TMR') and (int(ln.split()[2], 16) & 0xFF) == slot and \
        ln.split()[3] == str(deadline)


def two_interfaces(lines: list[str], interface: int = 1) -> list[str]:
    """The clean log at two interfaces: before every commit, a frame of the same channel committed and leaving
    KL_mbx on interface 1 (to the bench), and every timer slot moved to the two-interface layout. Given
    interface 0 for those frames, the n-th commit of a channel pairs with the wrong frame at the MAC."""
    out, heads = [], dict.fromkeys(range(len(g.CHANNELS)), 10_000)
    for ln in lines[:-2]:
        w = ln.split()
        if w[0] == 'TXC':
            ch = int(w[2])
            heads[ch] += 1
            out += [f'TXC {int(w[1]) - 50} {ch} {heads[ch]}', f'MTX {int(w[1]) - 20} {interface} {ch}']
        if w[0] == 'TMR':
            value = int(w[2], 16)
            ln = f'TMR {w[1]} {(value & ~0xFF) | ((value & 0xFF) * 2):08x} {w[3]}'
        out.append(ln)
    return sorted(out, key=lambda ln: int(ln.split()[1])) + lines[-2:]


def late_command(lines: list[str], at_ms: int) -> list[str]:
    """The second draw's AEM command moved to `at_ms`, its response gone: the log ends within its bound or not."""
    out = []
    for ln in lines[:-2]:
        w = ln.split()
        if w[0] == 'RXW' and w[4].startswith('aecp-') and w[4].endswith('-1'):
            ln = ' '.join(['RXW', str(at_ms * MS), str(at_ms * MS + 30), *w[3:]])
        elif w[0] == 'TXW' and bytes.fromhex(w[4])[14] == 0xFB and int.from_bytes(bytes.fromhex(w[4])[34:36],
                                                                                    'big') == 0x6101:
            continue
        out.append(ln)
    return sorted(out, key=lambda ln: int(ln.split()[1])) + lines[-2:]


def inserted(lines: list[str], line: str) -> list[str]:
    """The log with one more line, in cycle order."""
    return sorted(lines[:-2] + [line], key=lambda ln: int(ln.split()[1])) + lines[-2:]


def extra_egress(lines: list[str]) -> list[str]:
    """An ACMP frame leaving KL_mbx with no commit."""
    return inserted(lines, 'MTX 999999999 0 1')


def cancelled(lines: list[str]) -> list[str]:
    """The first probe deadline cancelled before it came."""
    return inserted(lines, f'TMR {300 * MS} {(2 << 30) | 2:08x} 598')


#: Each control: its name, the log, the clock, the interfaces and ANNOUNCEs it is graded at, and the words its
#: refusal or finding must carry.
CONTROLS = (
    ('shifted-clock', lambda: clean().text(), 125_000_000, 1, 1, 'the clock is shifted'),
    ('drifted-milliseconds', lambda: [ln.replace(f'MS {7 * MS} 7', f'MS {7 * MS + 1} 7') for ln in clean().text()],
     SYS_HZ, 1, 1, 'the clock is shifted'),
    ('missing-response', lambda: without(clean().text(), is_bind_response), SYS_HZ, 1, 1, 'has no BIND_RX_RESPONSE'),
    ('late-response', lambda: clean(response_cycles=200 * MS).text(), SYS_HZ, 1, 1,
     'acmp.bind_rx: 200.0 ms is not under 200.0 ms'),
    # the handling's arm gone: the PROBE_TX's own timeout arm, after the answer, must not stand in for it
    ('unhandled-answer', lambda: without(clean().text(), slot_arm(1, 10_100)), SYS_HZ, 1, 1, 'was never handled'),
    ('handled-on-another-slot', lambda: [ln.replace(' 40000101 10100', ' 40000107 10100') for ln in clean().text()],
     SYS_HZ, 1, 1, 'was never handled'),
    ('frame-before-commit', lambda: [late_commit(ln) for ln in clean().text()], SYS_HZ, 1, 1, 'before its commit'),
    ('incomplete-model', lambda: without(clean().text(), lambda ln: ln.startswith('==')), SYS_HZ, 1, 1,
     'did not complete'),
    ('no-mailbox-egress', lambda: without(clean().text(), lambda ln: ln.startswith('MTX')), SYS_HZ, 1, 1,
     'no KL_mbx egress'),
    ('egress-without-commit', lambda: extra_egress(clean().text()), SYS_HZ, 1, 1, 'frames left KL_mbx after'),
    ('bench-frames-counted-as-interface-0', lambda: two_interfaces(clean().text(), interface=0), SYS_HZ, 2, 1,
     'never reached the MAC'),
    # AECP (#868 item 3)
    ('missing-aecp-response', lambda: without(clean().text(), is_aecp_response), SYS_HZ, 1, 1,
     'has no final response'),
    ('late-aecp-response', lambda: clean(aecp_cycles=240 * MS).text(), SYS_HZ, 1, 1,
     'aecp.response: 240.0 ms is not under 240.0 ms'),
    ('aecp-in-progress', lambda: clean(interim=True).text(), SYS_HZ, 1, 1, 'IN_PROGRESS answers'),
    # a command 300 ms before the log ends, unanswered: past its 240 ms bound, so a finding, never censored
    ('unanswered-before-the-end', lambda: late_command(clean().text(), 1499), SYS_HZ, 1, 1,
     'aecp-get_configuration-1 (sequence_id 0x6101) has no final response'),
    # MAAP (#868 items 2 and 4)
    ('egress-past-reserve', lambda: moved(clean().text(), nth_maap(g.MAAP_PROBE, 3), 11 * MS + 1), SYS_HZ, 1, 1,
     'maap.egress: 11.'),
    # the next deadline armed 11 ms after its PROBE left: every frame's egress and every draw in range, the
    # interval at the wire 11 ms past its draw
    ('interval-error-past-reserve', lambda: clean(late_arm_ms=11).text(), SYS_HZ, 1, 1, 'maap.interval_error: 11.'),
    ('probe-draw-outside-reserve', lambda: clean(probe_draws=(558, 519, 590)).text(), SYS_HZ, 1, 1,
     'MAAP: an interval drawn at 590 ms, outside the reserved 511 to 589 ms'),
    ('probe-interval-outside-clause', lambda: moved(clean().text(), nth_maap(g.MAAP_PROBE, 2), 42 * MS), SYS_HZ, 1,
     1, 'maap.probe_interval: 600.'),
    ('maap-frame-on-no-expiry', lambda: without(clean().text(), slot_arm(2, 598)), SYS_HZ, 1, 1,
     'left on no expired timer'),
    ('maap-expiry-cancelled', lambda: cancelled(clean().text()), SYS_HZ, 1, 1, 'left on no expired timer'),
    ('announce-interval-outside-clause', lambda: moved(announced().text(), nth_maap(g.MAAP_ANNOUNCE, 2), 1001 * MS),
     SYS_HZ, 1, 2, 'maap.announce_interval: 32'),
    ('no-announce-interval', lambda: without(announced().text(), nth_maap(g.MAAP_ANNOUNCE, 2)), SYS_HZ, 1, 2,
     'ANNOUNCEs left the MAC, the run asked for 2'),
    # ADP (#868 item 3)
    ('advertise-timer-not-5s', lambda: announced(advertise_ms=4999).text(), SYS_HZ, 1, 2, 'not 5000 ms'),
    ('adp-delay-outside-table', lambda: announced(delays=(4001, *ADP_DELAYS[1:3])).text(), SYS_HZ, 1, 2,
     'ADP: a delay drawn at 4001 ms, outside 0 to 4000 ms'),
    ('adp-egress-past-ceiling', lambda: announced(late_cycles=400 * MS).text(), SYS_HZ, 1, 2, 'adp.egress: 400.'),
    # the one fault only the period at the wire sees: the same expiry's ENTITY_AVAILABLE sent twice
    ('available-sent-twice', lambda: announced(twice=True).text(), SYS_HZ, 1, 2, 'adp.advertise_period: 1.000 ms'),
)
#: The clean logs, each graded at its interfaces and ANNOUNCEs, which must pass.
#: Each with the commands it must report as censored.
CLEAN = (('clean', lambda: clean().text(), 1, 1, []),
         ('clean-announce-interval', lambda: announced().text(), 1, 2, []),
         ('clean-two-interfaces', lambda: two_interfaces(clean().text()), 2, 1, []),
         # the log ends 49 ms after a command, unanswered: within its bound, censored and not a finding
         ('clean-censored-at-the-end', lambda: late_command(clean().text(), 1750), 1, 1, ['aecp-get_configuration-1']))


def outcome(lines: list[str], sys_hz: int, interfaces: int, announces: int) -> list[str]:
    """The grade's words: its refusal, or its findings."""
    try:
        return g.grade('\n'.join(lines) + '\n', sys_hz, 2, interfaces, announces)[1]
    except g.Refused as why:
        return [f'REFUSED: {why}']


def delayed_maap(text: str, sys_hz: int) -> str | None:
    """A real log with the first timer-driven MAAP PROBE's egress delayed past the reserve: its stamps at the MAC
    one millisecond more than the 11 ms reserve later (#868 item 4's planted egress delay); None for a log with no
    such PROBE."""
    shift = int((g.MAAP_RESERVE_MS + 1) * sys_hz // 1000)
    lines = text.splitlines()
    pick = nth_maap(g.MAAP_PROBE, 2)
    for n, line in enumerate(lines):
        if pick(line):
            w = line.split()
            lines[n] = ' '.join([w[0], str(int(w[1]) + shift), str(int(w[2]) + shift), *w[3:]])
            return '\n'.join(lines) + '\n'
    return None


def plants(text: str, sys_hz: int, draws: int, interfaces: int, announces: int) -> int:
    """Each plant on a real log, graded, with the words it must be graded by; the number that escaped."""
    escaped = 0
    for name, log, hz, wanted in (
            ('egress-past-reserve', delayed_maap(text, sys_hz), sys_hz, 'is not under 11.0 ms'),
            ('shifted-clock', text, sys_hz * 5 // 4, 'the clock is shifted')):
        if log is None:
            print(f'plant {name}: ESCAPED: the log has no timer-driven MAAP PROBE to plant it on')
            escaped += 1
            continue
        try:
            words = g.grade(log, hz, draws, interfaces, announces)[1]
        except g.Refused as why:
            words = [f'REFUSED: {why}']
        hit = [w for w in words if wanted in w and (name != 'egress-past-reserve' or w.startswith('maap.egress'))]
        print(f'plant {name}: {"caught" if hit else "ESCAPED"}: {hit[0] if hit else words[:1] or "no finding"}')
        escaped += not hit
    return escaped


def planted_deadline_load(text: str) -> str:
    """A loaded script whose ADP deadline load also carries one of ACMP's GET_RX_STATEs, a draw channel's record."""
    get = s.budget.acmp_cmd(POINT, 'GET_RX_STATE', 0, 0x7200).hex()
    lines = [f'{line} 0/{get}' if line.startswith('defload adp ') else line for line in text.splitlines()]
    return '\n'.join(lines) + '\n'


#: The stimulus's own control: no deadline load may reach a draw's channel (wire_scenario.deadline_loads_clear),
#: which run.py enforces on every script it writes.
SCRIPT_CONTROLS = (
    ('clean-loaded-script', lambda: s.script(POINT, 2, 3, True), ''),
    ('deadline-load-on-a-draw-channel', lambda: planted_deadline_load(s.script(POINT, 2, 3, True)),
     'the deadline load adp reaches the acmp channel'),
)


def main() -> int:
    """Every control; exit 1 when a clean log fails or any control escapes."""
    failed = 0
    for name, script, wanted in SCRIPT_CONTROLS:
        words = s.deadline_loads_clear(script())
        ok = not words if not wanted else any(wanted in w for w in words)
        print(f'control {name}: {("PASS" if not wanted else "caught: " + words[0]) if ok else "FAIL " + repr(words)}')
        failed += not ok
    for name, log, interfaces, announces, censored in CLEAN:
        result, words = g.grade('\n'.join(log()) + '\n', SYS_HZ, 2, interfaces, announces)
        if result['censored'] != censored:
            words = [*words, f"censored {result['censored']}, not {censored}"]
        print(f'control {name}: {"PASS" if not words else "FAIL " + repr(words)}')
        failed += bool(words)
    for name, log, sys_hz, interfaces, announces, wanted in CONTROLS:
        words = outcome(log(), sys_hz, interfaces, announces)
        caught = any(wanted in w for w in words)
        print(f'control {name}: {"caught" if caught else "ESCAPED"}: {words[0] if words else "no finding"}')
        failed += not caught
    total = len(SCRIPT_CONTROLS) + len(CLEAN) + len(CONTROLS)
    print(f'ctrl_wire_timing self-test: {total} controls, {failed} failed')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
