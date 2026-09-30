"""Tabulate one AX7101 place sweep: per seed and declared corner, and the refusal gate.

Usage: sweep_table.py <work dir> <tag> <out.json>

For each seed directory build_ax7101_{asl,eto,eppo}_<tag> it reads, without
rewriting anything:
- each `gateware/*_signoff_{Slow,Fast}_{0C,85C}_timing.rpt` Design Timing Summary
  (WNS, TNS, WHS, THS and their failing-endpoint counts);
- the refusal gate of #607 (docs/integration/BUILDING.md section 5): the launch
  log's `[constraints] ... no 12-4739, 20-1307 or 12-5201 diagnostics` line
  (the gate's own pass verdict) and its layout line, `gateware/vivado.log` census of 12-4739, 20-1307, 12-5201 and
  CRITICAL WARNING lines, `flashboot_layout.json` present, an unquarantined
  `.bit` (no `.bit.rejected`);
- the clock-interaction rows naming the Ethernet clocks;
- `*_utilization_place.rpt` Slice LUTs, Slice Registers, Slice, Block RAM Tile, DSPs.
The floor is WNS >= +0.030 ns and WHS >= 0 at every declared corner.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

FLOOR_WNS = 0.030
CORNERS = [f'{m}_{t}' for m in ('Slow', 'Fast') for t in ('0C', '85C')]
SEEDS = {'asl': 'AltSpreadLogic_high', 'eto': 'ExtraTimingOpt', 'eppo': 'ExtraPostPlacementOpt'}
REFUSAL_IDS = ('12-4739', '20-1307', '12-5201')


def summary(rpt):
    text = rpt.read_text(errors='replace')
    at = text.index('Design Timing Summary')
    rows = [line.split() for line in text[at:at + 2000].splitlines()]
    nums = next(r for r in rows if len(r) >= 12 and re.fullmatch(r'-?\d+\.\d+', r[0]))
    return dict(wns=float(nums[0]), tns=float(nums[1]), tns_fail=int(nums[2]),
                whs=float(nums[4]), ths=float(nums[5]), ths_fail=int(nums[6]))


def util(rpt):
    out = {}
    for line in rpt.read_text(errors='replace').splitlines():
        cells = [c.strip() for c in line.split('|')]
        if len(cells) > 3 and cells[1] in ('Slice LUTs', 'Slice Registers', 'Slice',
                                           'Block RAM Tile', 'DSPs') and cells[1] not in out:
            out[cells[1]] = cells[2]
    return out


def seed(work, tag, short):
    d = work / f'build_ax7101_{short}_{tag}'
    gw = d / 'gateware'
    row = dict(seed=short, directive=SEEDS[short], dir=str(d))
    launch = work / f'build_ax7101_{short}_{tag}.launch.log'
    ltext = launch.read_text(errors='replace') if launch.exists() else ''
    row['launch_published_layout'] = '[milan] flash-boot layout' in ltext
    row['launch_traceback'] = 'Traceback (most recent call last)' in ltext
    #: the refusal gate's own verdict line (sw/litex/clock_constraints.py
    #: check_implementation_log), printed only when it found no diagnostic
    row['launch_constraints_pass'] = bool(re.search(
        r'^\[constraints\] \S+vivado\.log: no 12-4739, 20-1307 or 12-5201 diagnostics$', ltext, re.M))
    log = gw / 'vivado.log'
    text = log.read_text(errors='replace') if log.exists() else ''
    row['vivado_log'] = log.exists()
    row['refusal_ids'] = {i: len(re.findall(rf' {re.escape(i)}\]', text)) for i in REFUSAL_IDS}
    row['critical_warnings'] = len(re.findall(r'^CRITICAL WARNING', text, re.M))
    row['flashboot_layout'] = (d / 'flashboot_layout.json').exists()
    bits = sorted(p.name for p in gw.glob('*.bit'))
    rejected = sorted(p.name for p in gw.glob('*.bit.rejected'))
    row['bit'] = bits
    row['bit_rejected'] = rejected
    if bits:
        raw = (gw / bits[0]).read_bytes()
        row['bit_sha256'] = hashlib.sha256(raw).hexdigest()
        row['bit_bytes'] = len(raw)
    row['refusal_gate_accepts'] = (row['flashboot_layout'] and bool(bits) and not rejected
                                   and row['vivado_log'] and row['launch_published_layout']
                                   and row['launch_constraints_pass']
                                   and not row['launch_traceback']
                                   and not any(row['refusal_ids'].values()))
    row['corners'] = {}
    for c in CORNERS:
        rpt = next(iter(gw.glob(f'*_signoff_{c}_timing.rpt')), None)
        row['corners'][c] = summary(rpt) if rpt else None
    done = [v for v in row['corners'].values() if v]
    row['worst_wns'] = min(v['wns'] for v in done) if len(done) == 4 else None
    row['worst_whs'] = min(v['whs'] for v in done) if len(done) == 4 else None
    row['meets_floor'] = (len(done) == 4 and row['worst_wns'] >= FLOOR_WNS
                          and row['worst_whs'] >= 0.0)
    ci = next(iter(gw.glob('*_signoff_clock_interaction.rpt')), None)
    if ci:
        row['eth_interaction'] = [' '.join(line.split()) for line in ci.read_text(errors='replace').splitlines()
                                  if 'eth' in line.lower() and ('Max Delay' in line or 'Timed' in line
                                                                or 'Unsafe' in line)]
    up = next(iter(gw.glob('*_utilization_place.rpt')), None)
    row['utilization_place'] = util(up) if up else None
    return row


def main():
    work, tag, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    rows = [seed(work, tag, s) for s in SEEDS]
    result = dict(tag=tag, floor_wns_ns=FLOOR_WNS, floor_whs_ns=0.0, seeds=rows,
                  any_seed_meets_floor_and_accepted=any(r['meets_floor'] and r['refusal_gate_accepts']
                                                        for r in rows))
    out.write_text(json.dumps(result, indent=2) + '\n')
    print('| Seed | Directive | ' + ' | '.join(f'{c} WNS / WHS' for c in CORNERS)
          + ' | Worst WNS | Worst WHS | Floor | Refusal gate |')
    print('|---|---|' + '---|' * (len(CORNERS) + 4))
    for r in rows:
        cells = []
        for c in CORNERS:
            v = r['corners'][c]
            cells.append(f"{v['wns']:+.3f} / {v['whs']:+.3f}" if v else 'n/a')
        worst = (f"{r['worst_wns']:+.3f}" if r['worst_wns'] is not None else 'n/a',
                 f"{r['worst_whs']:+.3f}" if r['worst_whs'] is not None else 'n/a')
        print(f"| {r['seed']} | {r['directive']} | " + ' | '.join(cells)
              + f" | {worst[0]} | {worst[1]} | {'meets' if r['meets_floor'] else 'below'} | "
              + ('accepted' if r['refusal_gate_accepts'] else 'REFUSED/absent') + ' |')
    print('any seed meets the floor and is accepted:', result['any_seed_meets_floor_and_accepted'])


if __name__ == '__main__':
    main()
