# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The wire-timing grader's controls (#665, #868), on synthetic logs, with no build.

A synthetic log is wire_main.cpp's output for two draws, written from the
frames the stimulus sends and the answers a correct entity gives. The clean log
must pass. Each control then changes one thing and must be graded by its own
words: refused, or a finding. SHIFTED is #868 item 4's grader with a shifted
clock: the clean log graded at another clock, which the clock check refuses
before any figure is converted.
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


def acmp_frame(kind: int, seq: int, sa: int) -> str:
    """An ACMP frame of one message type and sequence_id, as hex."""
    return f.acmp(kind, sa, f.Acmp(controller=s.CTL1, talker=s.budget.TALKER_A, listener=ENTITY, talker_uid=1,
                                   sequence=seq)).hex()


def clean(response_cycles: int = 50_000) -> list[str]:
    """Two draws: a bind answered after response_cycles, its probe and the talker's answer handled."""
    lines = [f'MS {k * MS} {k}' for k in range(1, 400)]
    lines.append(f'READY {2 * MS}')
    commits = {1: 0}
    for k, at in enumerate((10 * MS, 110 * MS)):
        seq, probe_seq = 0x4100 + 2 * k, 0x10 + k
        lines.append(f'RXW {at} {at + 30} 60 acmp-bind-{k} {acmp_frame(f.ACMP["BIND_RX"], seq, s.budget.CTL_MAC)}')
        lines.append(f'TXC {at + response_cycles - 400} 1 {commits[1]}')
        lines.append(f'TXW {at + response_cycles - 100} {at + response_cycles} 60 '
                     f'{acmp_frame(f.ACMP["BIND_RX_RESPONSE"], seq, ENTITY_MAC)}')
        lines.append(f'TXC {at + response_cycles - 300} 1 {commits[1] + 1}')
        lines.append(f'TXW {at + response_cycles + 100} {at + response_cycles + 200} 60 '
                     f'{acmp_frame(f.ACMP["PROBE_TX"], probe_seq, ENTITY_MAC)}')
        lines.append(f'RXW {at + response_cycles + 300} {at + response_cycles + 330} 60 talker '
                     f'{acmp_frame(f.ACMP["PROBE_TX_RESPONSE"], probe_seq, s.budget.TALKER_A_MAC)}')
        # its own timeout, committed after the prompt answer's last byte in, as the bench measures it
        lines.append(f'TMR {at + response_cycles + 350} 40000101 {at // MS + 200}')
        lines.append(f'TMR {at + response_cycles + 5000} 40000201 {at // MS + 10000}')   # its handling
        commits[1] += 2
    lines += ['SUMMARY sys=40000000', '== ctrl_wire_timing: checks: 1   failures: 0 ==']
    return sorted(lines, key=lambda ln: int(ln.split()[1]) if ln.split()[1].isdigit() else 1 << 62)


def text(lines: list[str]) -> str:
    """A log's text from its lines."""
    return '\n'.join(lines) + '\n'


def without(lines: list[str], what: Callable[[str], bool]) -> list[str]:
    """The lines `what` does not select."""
    return [ln for ln in lines if not what(ln)]


def is_bind_response(line: str) -> bool:
    """The first draw's BIND_RX_RESPONSE at the wire."""
    return line.startswith('TXW') and line.endswith(acmp_frame(f.ACMP['BIND_RX_RESPONSE'], 0x4100, ENTITY_MAC))


def late_commit(line: str) -> str:
    """The first ACMP commit moved past its frame's first byte out."""
    w = line.split()
    return f'TXC {int(w[1]) + 1000} 1 0' if w[0] == 'TXC' and w[2:] == ['1', '0'] else line


#: Each control: its name, the log, the clock it is graded at, and the words its refusal or finding must carry.
CONTROLS = (
    ('shifted-clock', lambda: clean(), 125_000_000, 'the clock is shifted'),
    ('drifted-milliseconds', lambda: [ln.replace(f'MS {7 * MS} 7', f'MS {7 * MS + 1} 7') for ln in clean()], SYS_HZ,
     'the clock is shifted'),
    ('missing-response', lambda: without(clean(), is_bind_response), SYS_HZ, 'has no BIND_RX_RESPONSE'),
    ('late-response', lambda: clean(response_cycles=200 * MS), SYS_HZ, 'acmp.bind_rx: 200.0 ms is not under 200.0 ms'),
    # the handling's arm gone: the PROBE_TX's own timeout arm, after the answer, must not stand in for it
    ('unhandled-answer', lambda: without(clean(), lambda ln: ln.startswith('TMR') and ' 40000201 ' in ln), SYS_HZ,
     'was never handled'),
    ('handled-on-another-slot', lambda: [ln.replace(' 40000201 ', ' 40000200 ') for ln in clean()], SYS_HZ,
     'was never handled'),
    ('frame-before-commit', lambda: [late_commit(ln) for ln in clean()], SYS_HZ, 'before its commit'),
    ('incomplete-model', lambda: without(clean(), lambda ln: ln.startswith('==')), SYS_HZ, 'did not complete'),
)


def outcome(lines: list[str], sys_hz: int) -> list[str]:
    """The grade's words: its refusal, or its findings."""
    try:
        return g.grade(text(lines), sys_hz, 2)[1]
    except g.Refused as why:
        return [f'REFUSED: {why}']


def main() -> int:
    """Every control; exit 1 when the clean log fails or any control escapes."""
    failed = 0
    words = outcome(clean(), SYS_HZ)
    print(f'control clean: {"PASS" if not words else "FAIL " + repr(words)}')
    failed += bool(words)
    for name, log, sys_hz, wanted in CONTROLS:
        words = outcome(log(), sys_hz)
        caught = any(wanted in w for w in words)
        print(f'control {name}: {"caught" if caught else "ESCAPED"}: {words[0] if words else "no finding"}')
        failed += not caught
    print(f'ctrl_wire_timing self-test: {1 + len(CONTROLS)} controls, {failed} failed')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
