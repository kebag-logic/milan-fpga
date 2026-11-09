# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The wire-timing stimulus (#665, #868): each draw's frames at the MAC boundary, in wire_main.cpp's script.

The frames and identities are the CPU budget harness's (frames.py and
scenario.py, imported read only): a controller (CTL1) binds this entity's
STREAM_INPUT 0 to a remote talker (TALKER_A), and the talker answers the
PROBE_TX the bind causes with scenario.probe_answer's PROBE_TX_RESPONSE. The
testbench sends that answer a turnaround after the command's last byte has
left: the talker's and the network's own time, which differs per draw so that
the answer meets the entity's loop at a different phase each time (Draw).

Script steps (wire_main.cpp):
  link <0|1>                         the PHY's link level
  wait ready | ms <n> | cycles <n> | now <ms>
  frame <tag> <hex>                  a frame offered at the MAC boundary
  reply <tag> <cycles> <off>:<byte>... <off>=<hex>...
                                     answer each transmitted frame that matches;
                                     a rule replaces the one of its tag
  mark <label>
  end
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_service_budget'))
import frames as f  # noqa: E402  the CPU budget harness's frame builders, read only
import scenario as budget  # noqa: E402  its identities and the talker's answer, read only

#: Each draw's spacing: the bind waits BIND_WAIT_MS, then the unbind UNBIND_WAIT_MS. Each draw's bind starts
#: PHASE_STEP_CYCLES later in a millisecond than the one before, and the talker's turnaround (bus cycles from the
#: PROBE_TX's last byte out to its answer's first byte in) is TURNAROUND_STEP_CYCLES longer, both modulo one
#: millisecond, so the draws sample the loop's phase at both inputs. The turnaround stays under 1 ms.
BIND_WAIT_MS = 60
UNBIND_WAIT_MS = 40
PHASE_STEP_CYCLES = 7919
TURNAROUND_STEP_CYCLES = 6007
MS_CYCLES = 100_000
#: Settling after the ready line, before the first draw: the boot's last publications and the link's first frames.
SETTLE_MS = 30


@dataclass(frozen=True)
class Draw:
    """One bind, probe and unbind: its sequence_ids, its phase offset and the talker's turnaround."""
    index: int
    bind_seq: int
    unbind_seq: int
    phase_cycles: int
    turnaround_cycles: int


def draws(n: int) -> list[Draw]:
    """N draws, each with its own sequence_ids and phase."""
    return [Draw(k, 0x4100 + 2 * k, 0x4101 + 2 * k, (k * PHASE_STEP_CYCLES) % MS_CYCLES,
                 (k * TURNAROUND_STEP_CYCLES) % MS_CYCLES) for k in range(n)]


def probe_reply(turnaround_cycles: int) -> str:
    """The talker's answer as a reply rule: a PROBE_TX from this entity (an AVTP control frame, subtype 0xFC,
    message_type 0) answered with scenario.probe_answer's PROBE_TX_RESPONSE patches, after the turnaround."""
    terms = budget.probe_answer(0).split()[3:]   # drop 'reply <interface> <channel>'
    match = ['12:22', '13:f0', '14:fc'] + [t for t in terms if ':' in t]
    patch = [t for t in terms if '=' in t]
    return ' '.join(['reply', 'talker-probe-tx-response', str(turnaround_cycles), *match, *patch])


def limit_ms(n: int) -> int:
    """The run's time limit: the boot's bound (the split boot simulation's) and every draw, with a margin."""
    return 2000 + n * (BIND_WAIT_MS + UNBIND_WAIT_MS + 2) + SETTLE_MS


def script(p: budget.Point, n: int) -> str:
    """The stimulus for N draws at one point."""
    lines = ['# ctrl_wire_timing: ACMP bind, probe and unbind draws (#868 item 1)', 'link 1', 'wait ready',
             f'wait ms {SETTLE_MS}', 'mark draws']
    for d in draws(n):
        bind = budget.acmp_cmd(p, 'BIND_RX', 0, d.bind_seq)
        unbind = budget.acmp_cmd(p, 'UNBIND_RX', 0, d.unbind_seq)
        lines += [f'wait cycles {d.phase_cycles}', probe_reply(d.turnaround_cycles),
                  f'frame acmp-bind-{d.index} {bind.hex()}',
                  f'wait ms {BIND_WAIT_MS}', f'frame acmp-unbind-{d.index} {unbind.hex()}', f'wait ms {UNBIND_WAIT_MS}']
    lines += ['mark end', 'end']
    return '\n'.join(lines) + '\n'


def identity(spec: dict) -> budget.Point:
    """The point's identity from its image's generated entity header (the CPU budget harness's point())."""
    return budget.point(spec['point'], {'elf': spec['elf'], 'shape': spec['shape'], 'interfaces': spec['interfaces']})


# The frames the grader decodes: ACMP's message types (IEEE 1722.1-2021 Table 8-1, Milan v1.2 5.5.2).
ACMP = f.ACMP
CTL1 = budget.CTL1
