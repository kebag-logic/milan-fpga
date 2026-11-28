# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""#878's Arty model gate: the (1,1,2) FPGA point at exactly 80 MHz and the (1,5,5) point at exactly 100 MHz.

This checks the stated costs and the rows derived from them. Measurement
completeness and the measured 2 ms share remain the service harness's gates;
a passing model alone does not qualify an image. Both points are held to the
same owner bounds; neither takes the other's costs.

usage: python3 -I arty_grade.py [--point arty-1x1|arty-4x4] [--selftest]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import load_grade
import paced_rows
import poll_grade
import queued_bound
import rows_tiers
import shape_costs

ROOT = Path(__file__).resolve().parents[3]
POINT = 'arty-1x1'
SHAPE = shape_costs.Shape(1, 1, 2)
#: Each Arty point, its shape and the configurations built at it: the 1x1 (its all-fabric twin and the split image)
#: and the 4x4/1if split image, four AAF streams and the CRF each way.
POINTS = {POINT: (SHAPE, ('endstation_arty_current', 'endstation_arty_split')),
          'arty-4x4': (shape_costs.Shape(1, 5, 5), ('endstation_arty_split_4x4',))}
CLOCK_HZ = 80_000_000
#: Each point's exact CPU and bus clock: the 1x1's 80 MHz ruling, and 100 MHz for the 4x4 (the 800 MHz VCO / 8).
CLOCKS = {POINT: CLOCK_HZ, 'arty-4x4': 100_000_000}
LOAD_CEILING = 0.70
OWNER_MS = {'txL': 49, 'last': 140, 'ACMP': 30}


def owner_findings(load: float, rows: dict[str, float | None]) -> list[str]:
    """The settled owner bounds. A row with no finite solution also fails."""
    out = [f'OWNER load: {load:.6f} exceeds {LOAD_CEILING:.2f}'] if load > LOAD_CEILING else []
    for name, bound in OWNER_MS.items():
        value = rows[name]
        if value is None or value > bound:
            out.append(f'OWNER {name}: {value} ms exceeds {bound} ms')
    return out


def inspect(root: Path = ROOT, point: str = POINT) -> tuple[dict, list[str]]:
    """The point's own model and statements, refusing an absent cost basis."""
    sys.path.insert(0, str(root / 'sw/builder'))
    import endstation_builder as eb
    shape, configs = POINTS[point]
    out = []
    for config in configs:
        cfg = eb.load_config(root / 'configs' / f'{config}.yaml')
        if cfg['constraints']['sys_clk_hz'] != CLOCKS[point]:
            out.append(f'{config}: CPU (sys domain) clock is not exactly {CLOCKS[point]} Hz')
        if cfg['constraints']['milan_clk_hz'] != 50_000_000:
            out.append(f'{config}: datapath clock is not 50000000 Hz')
        if shape_costs.of_config(root / 'configs' / f'{config}.yaml', 1, root) != shape:
            out.append(f'{config}: the shape is not {tuple(shape)}')
    if point in load_grade.NEAREST:
        out.append('Arty takes another point\'s measured costs through NEAREST')
    required = (
        ('pin costs', load_grade.STATED_US, point),
        ('current-pin costs', load_grade.STATED_US_DONOR, point),
        ('poll costs', poll_grade.STATED_US, shape),
        ('datapath costs', rows_tiers.DATAPATH_US, point),
        ('long record', rows_tiers.LONG_RECORD_US, point),
    )
    out += [f'Arty has no own {name}' for name, table, key in required if key not in table]
    listed = shape_costs.at(shape, root)
    out += [f'Arty has no own {name}' for name in
            ('CTRL_LOOP_STEP_PASS_US', 'CTRL_LOOP_TICK_US', 'AECP_NOTICE_US', 'AECP_PACE_MS')
            if name not in listed]
    if out:
        return {'status': 'UNQUALIFIED', 'point': point, 'cpu_hz': CLOCKS[point], 'shape': list(shape)}, out
    inputs = rows_tiers.point_inputs(root, point)
    terms = load_grade.load(root, point, load_grade.STATED_US)
    load = sum(terms.values())
    rows = {name: value for name, (value, _) in rows_tiers.rows(root, point, rows_tiers.BUILT, inputs).items()}
    out += owner_findings(load, rows)
    out += shape_costs.findings(root)
    out += load_grade.srp_unit(root)
    out += rows_tiers.broken(root, rows_tiers.BUILT, (point,))
    out += rows_tiers.findings(root, rows_tiers.BUILT, (point,))
    out += rows_tiers.tx_statements(root, (point,))
    out += paced_rows.statements(root, point=point)
    out += queued_bound.statements(root, point=point)
    chosen, margin = rows_tiers.slice_choice(root, point)
    if inputs.slice_us != chosen:
        out.append(f'Arty slice {inputs.slice_us} us is not the rule\'s {chosen} us')
    if inputs.h['CTRL_LOOP_SHARE_US'] != 2000:
        out.append('Arty THE SHARE is not 2000 us')
    record = dict(status='FAIL' if out else 'PASS', evidence='stated-cost model only', point=point,
                  cpu_hz=CLOCKS[point], shape=list(shape), load=load, load_terms=terms, rows_ms=rows,
                  slice_us=inputs.slice_us, slice_margin=margin, pace_ms=inputs.pace_ms)
    return record, out


def checks() -> list[tuple[str, bool, str]]:
    """Boundary controls independently exercise each settled owner bound."""
    on = dict(OWNER_MS)
    tests = [('Arty owner bounds accept equality', not owner_findings(LOAD_CEILING, on), 'exact bounds')]
    for name in OWNER_MS:
        changed = {**on, name: on[name] + 0.01}
        caught = any(f'OWNER {name}:' in f for f in owner_findings(LOAD_CEILING, changed))
        tests.append((f'Arty owner gate refuses a larger {name}', caught, '0.01 ms over'))
        caught = any(f'OWNER {name}:' in f for f in owner_findings(LOAD_CEILING, {**on, name: None}))
        tests.append((f'Arty owner gate refuses an unbounded {name}', caught, 'no finite solution'))
    caught = any('OWNER load:' in f for f in owner_findings(LOAD_CEILING + 0.000001, on))
    tests.append(('Arty owner gate refuses load over 0.70', caught, '0.000001 over'))
    shapes = [shape_costs.of_config(ROOT / 'configs' / f'{c}.yaml', 1, ROOT) for c in POINTS['arty-4x4'][1]]
    tests.append(('the Arty 4x4 configuration states the (1,5,5) shape', shapes == [POINTS['arty-4x4'][0]],
                  str(shapes)))
    tests.append(('the two Arty points are different shapes',
                  POINTS[POINT][0] != POINTS['arty-4x4'][0], 'no point takes the other\'s costs'))
    return tests


def main(argv: list[str]) -> int:
    """Print the model and findings, or run its owner-bound controls."""
    if argv == ['--selftest']:
        tests = checks()
        for name, ok, detail in tests:
            print(f'{"PASS" if ok else "FAIL"} {name}: {detail}')
        return int(any(not ok for _, ok, _ in tests))
    point = POINT
    if argv[:1] == ['--point'] and len(argv) == 2 and argv[1] in POINTS:
        point, argv = argv[1], []
    if argv:
        print(__doc__)
        return 2
    record, found = inspect(point=point)
    print(json.dumps(record, indent=2))
    for line in found:
        print('REFUSED', line)
    return int(bool(found))


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
