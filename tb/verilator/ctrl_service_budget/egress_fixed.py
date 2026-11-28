# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure the 100 Mb/s egress row's fixed path on the converted MII chain, and hold egress_mii.MII_FIXED_NS to it.

egress_fixed_main.cpp sends one frame at a time through tb/verilator/gptp_txts/generated/mac_tx_chain_mii.v, the
shipping MAC transmit chain on the board's MII stages as sw/litex/gen_mac_tx_model.py converts it, and prints for
each length and each of 8 x 8 clock phases the chain's latency from its boundary's last beat to the last nibble at
its pads, less the frame's wire time. The stated figure is the largest, rounded up to 10 ns; the run exits 1 unless
MII_FIXED_NS is exactly that.

With SYS_HZ the bench's sys clock is that frequency instead of the Arty 1x1's 80 MHz, its period a whole number of
ps, and the run reports the most against the stated figure: exit 1 when it is over, 0 when it is within. The
datapath (50 MHz) and MII (25 MHz) clocks are unchanged. A SYS_HZ that is not a positive whole number of Hz with a
whole-ps period is refused with this usage, exit 2. `--selftest` plants each defect of the argument, build and report
paths with a stub in place of the simulator, so it needs no Verilator.

usage: python3 -I egress_fixed.py BUILD_DIR [SYS_HZ] | --selftest
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # egress_mii beside it, under -I too

import egress_mii  # noqa: E402

CHAIN = HERE.parents[1] / 'verilator/gptp_txts/generated/mac_tx_chain_mii.v'
#: The least frame, one under it the padding covers, the SR stream's, gPTP's longest, an odd length, the largest.
LENGTHS = (14, 60, 64, 90, 127, 512, 1514)


def build(build_dir: Path, sys_ps: int = 12500) -> Path:
    """Verilate the converted chain with the bench at a sys period, ps; the executable."""
    build_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(['verilator', '--cc', '--exe', '--build', '-O3', '-Wno-fatal', '--top-module', 'mac_tx_chain_mii',
                    '--Mdir', str(build_dir), '-CFLAGS', f'-O2 -std=c++17 -DEGRESS_FIXED_SYS_PS={sys_ps}', str(CHAIN),
                    str(HERE / 'egress_fixed_main.cpp'), '-o', 'Vmac_tx_chain_mii'],
                   check=True, stdout=subprocess.DEVNULL)
    return build_dir / 'Vmac_tx_chain_mii'


def measured(binary: Path) -> dict[int, int]:
    """The largest fixed path at each length, ps."""
    out: dict[int, int] = {}
    text = subprocess.run([str(binary), *map(str, LENGTHS)], check=True, capture_output=True, text=True).stdout
    for line in text.splitlines():
        _, length, _, _, ps = line.split()
        out[int(length)] = max(out.get(int(length), 0), int(ps))
    return out


def sys_period(text: str) -> int | None:
    """The sys period in ps of a SYS_HZ argument, or None when it is not a positive whole Hz with a whole-ps period."""
    if not text.isdigit() or int(text) <= 0 or 10**12 % int(text):
        return None
    return 10**12 // int(text)


def over(ps: int) -> bool:
    """Whether a fixed path, ps, is over the stated figure."""
    return ps > egress_mii.MII_FIXED_NS * 1000


def main(argv: list[str]) -> int:
    """Build, measure and compare with the stated figure."""
    if argv == ['--selftest']:
        return selftest()
    sys_ps = sys_period(argv[1]) if len(argv) == 2 else 12500
    if len(argv) not in (1, 2) or argv[0].startswith('-') or sys_ps is None:
        print(__doc__)
        return 2
    worst = measured(build(Path(argv[0]), sys_ps))
    for length, ps in sorted(worst.items()):
        print(f'length {length}: fixed path at most {ps / 1000:.1f} ns over 64 clock phases')
    stated = -(-max(worst.values()) // 10_000) * 10
    if len(argv) == 2:
        print(f'REPORT at sys {argv[1]} Hz: the most is {max(worst.values()) / 1000:.1f} ns, '
              f'{"OVER" if over(max(worst.values())) else "within"} the stated {egress_mii.MII_FIXED_NS} ns')
        return int(over(max(worst.values())))
    ok = stated == egress_mii.MII_FIXED_NS
    print(f'{"PASS" if ok else "FAIL"}: the most is {max(worst.values()) / 1000:.1f} ns, stated {stated} ns; '
          f'egress_mii.MII_FIXED_NS is {egress_mii.MII_FIXED_NS} ns')
    return int(not ok)


def controls() -> list[tuple[str, bool]]:
    """Each control and whether it held: the arguments, the period the build passes the bench, and the report's
    verdict, with the simulator replaced by a stub that records the build and answers a planted fixed path."""
    me = sys.modules[__name__]
    seen: list[list[str]] = []
    answer = {'ps': 300_000}

    def fake_run(argv: list[str], **kw: object) -> subprocess.CompletedProcess:
        """The verilator build, recorded, or the bench, answering every length at the planted figure."""
        seen.append([str(a) for a in argv])
        out = '' if argv[0] == 'verilator' else ''.join(f'FIXED {n} 0 0 {answer["ps"]}\n' for n in LENGTHS)
        return subprocess.CompletedProcess(argv, 0, out, '')

    import contextlib
    import io
    import tempfile
    from unittest.mock import patch

    def run(argv: list[str]) -> tuple[int, str]:
        """main() on argv, its output captured."""
        text = io.StringIO()
        with patch.object(me.subprocess, 'run', fake_run), contextlib.redirect_stdout(text):
            return main(argv), text.getvalue()

    out = []
    with tempfile.TemporaryDirectory() as tmp:
        for bad in ('0', '-1', 'abc', '3', '1e8'):
            rc, text = run([tmp, bad])
            out.append((f'SYS_HZ {bad!r} is refused with the usage, exit 2', rc == 2 and 'usage:' in text))
        seen.clear()
        rc, text = run([tmp, '100000000'])
        flags = ' '.join(next((a for a in seen if a[0] == 'verilator'), []))
        out.append(('SYS_HZ 100000000 builds the bench at a 10000 ps sys period',
                    '-DEGRESS_FIXED_SYS_PS=10000' in flags))
        out.append(('300.0 ns at 100 MHz is reported within the stated figure, exit 0',
                    rc == 0 and 'REPORT at sys 100000000 Hz: the most is 300.0 ns, within' in text))
        answer['ps'] = egress_mii.MII_FIXED_NS * 1000 + 1
        rc, text = run([tmp, '100000000'])
        out.append(('a fixed path 1 ps over the stated figure is reported OVER, exit 1', rc == 1 and 'OVER' in text))
        seen.clear()
        answer['ps'] = 312_500
        rc, text = run([tmp])
        flags = ' '.join(next((a for a in seen if a[0] == 'verilator'), []))
        out.append(("no SYS_HZ builds the bench at the Arty 1x1's 12500 ps", '-DEGRESS_FIXED_SYS_PS=12500' in flags))
        out.append(('312.5 ns, stated 320 ns, passes the default run', rc == 0 and text.rstrip().endswith('320 ns')))
        answer['ps'] = 322_500
        rc, _ = run([tmp])
        out.append(('a measurement that rounds to another stated figure fails the default run', rc == 1))
    return out


#: Each defect a control must catch.
MUTANTS = {
    'SYS_HZ read without its whole-ps check': lambda me: patch_attr(me, 'sys_period', lambda t: 10**12 // max(
        int(float(t)), 1) if t.lstrip('-').replace('.', '').replace('e', '').isdigit() else None),
    'the bench built at the default period whatever SYS_HZ': lambda me: patch_attr(
        me, 'build', lambda d, sys_ps=12500, real=build: real(d, 12500)),
    'a report over the stated figure read as within': lambda me: patch_attr(me, 'over', lambda ps: False),
}


def patch_attr(me: object, name: str, value: object):
    """A context that sets one module attribute and restores it."""
    from unittest.mock import patch
    return patch.object(me, name, value)


def selftest() -> int:
    """Every control on the shipping code, then each mutant caught by at least one."""
    me = sys.modules[__name__]
    failed = 0
    for name, ok in controls():
        print(f'{"PASS" if ok else "FAIL"} {name}')
        failed += not ok
    for name, plant in MUTANTS.items():
        with plant(me):
            caught = [c for c, ok in controls() if not ok]
        print(f'{"CAUGHT" if caught else "ESCAPED"} {name}' + (f': {caught[0]}' if caught else ''))
        failed += not caught
    print(f'egress_fixed selftest: {"PASS" if not failed else "FAIL"}, {len(MUTANTS)} mutants, {failed} failure(s)')
    return int(bool(failed))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
