"""Tabulate ooc_cpu.sh's out-of-context runs: synthesis utilisation, routed utilisation and timing.

usage: ooc_report.py WORK [LABEL=NETLIST_STEM ...]
Reads each run directory's synth_util.rpt, route_util.rpt and timing.rpt as Vivado wrote them
and prints one Markdown row per run: Slice LUTs, LUT as memory, registers, RAMB36 and RAMB18
tiles after synthesis and after routing, and the routed WNS and WHS.
"""
import re
import sys
from pathlib import Path


def util(path: Path) -> dict:
    text = path.read_text()

    def field(name: str) -> float:
        m = re.search(rf'^\|\s*{re.escape(name)}\s*\|\s*([\d.]+)\s*\|', text, re.M)
        return float(m.group(1)) if m else 0.0
    return dict(lut=field('Slice LUTs*') or field('Slice LUTs') or field('CLB LUTs*'),
                lutram=field('LUT as Memory'), ff=field('Slice Registers') or field('Register as Flip Flop'),
                tiles=field('Block RAM Tile'), r36=field('RAMB36/FIFO*') or field('RAMB36/FIFO'),
                r18=field('RAMB18'))


def timing(path: Path) -> tuple[str, str]:
    text = path.read_text()
    m = re.search(r'WNS\(ns\)\s+TNS\(ns\).*?\n\s*-+.*?\n\s*([-\d.]+)\s+\S+\s+\S+\s+\S+\s+([-\d.]+)', text, re.S)
    return (m.group(1), m.group(2)) if m else ('-', '-')


def main() -> int:
    work = Path(sys.argv[1])
    labels = dict(a.split('=', 1)[::-1] for a in sys.argv[2:])
    print('| Netlist | Synthesis LUT / of which memory / FF / BRAM tiles (RAMB36, RAMB18) '
          '| Routed LUT / FF / BRAM tiles | Routed WNS / WHS, ns | rc |')
    print('|---|---:|---:|---:|---:|')
    for d in sorted(p for p in work.iterdir() if p.is_dir()):
        rc = (d / 'rc').read_text().strip() if (d / 'rc').exists() else 'running'
        s = util(d / 'synth_util.rpt') if (d / 'synth_util.rpt').exists() else None
        r = util(d / 'route_util.rpt') if (d / 'route_util.rpt').exists() else None
        wns, whs = timing(d / 'timing.rpt') if (d / 'timing.rpt').exists() else ('-', '-')
        name = labels.get(d.name, d.name)
        sc = f"{s['lut']:,.0f} / {s['lutram']:,.0f} / {s['ff']:,.0f} / {s['tiles']:g} ({s['r36']:g}, {s['r18']:g})" if s else '-'
        rc_ = f"{r['lut']:,.0f} / {r['ff']:,.0f} / {r['tiles']:g}" if r else '-'
        print(f'| {name} | {sc} | {rc_} | {wns} / {whs} | {rc} |')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
