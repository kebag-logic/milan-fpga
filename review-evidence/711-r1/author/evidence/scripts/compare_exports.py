"""Compare the base and candidate shipping exports file by file, and digest their measurement inputs.

Usage: python3 compare_exports.py SIDE_A SIDE_B REPORT_JSON
Absolute roots differ only by their side name (exp-base/exp-cand, res/base/res/cand: equal lengths),
so each side's roots are replaced by one placeholder before comparing; binary lengths are preserved.
The resource gate's own inputs() digest is computed for each prepared integrated script.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path('$SCRATCH')
SIDES = tuple(sys.argv[1:3])


def normalized(side, data):
    for old in (f'{ROOT}/exp-{side}', f'{ROOT}/res/{side}'):
        data = data.replace(old.encode(), old.replace(side, 'SIDE').encode())
    return data


def gate_module():
    spec = importlib.util.spec_from_file_location('gate', ROOT / 'exp-cand/syn/ooc/pp_resource_gate.py')
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(ROOT / 'exp-cand/syn/ooc'))
    spec.loader.exec_module(module)
    return module


def main():
    report = {'sides': list(SIDES), 'shapes': {}}
    gate = gate_module()
    ok = True
    for shape in ('ax7101', 'ax8x8'):
        trees = {s: ROOT / 'res' / s / shape for s in SIDES}
        files = {s: {p.relative_to(trees[s]) for p in trees[s].rglob('*') if p.is_file()} for s in SIDES}
        only = {s: sorted(map(str, files[s] - files[[t for t in SIDES if t != s][0]])) for s in SIDES}
        identical, normalized_equal, different = [], [], []
        for rel in sorted(files[SIDES[0]] & files[SIDES[1]]):
            b = (trees[SIDES[0]] / rel).read_bytes()
            c = (trees[SIDES[1]] / rel).read_bytes()
            if b == c:
                identical.append(str(rel))
            elif normalized(SIDES[0], b) == normalized(SIDES[1], c):
                normalized_equal.append(str(rel))
            else:
                different.append(str(rel))
        gateware = {s: trees[s] / 'gateware' for s in SIDES}
        rom = {s: hashlib.sha256((gateware[s] / 'alinx_ax7101_rom.init').read_bytes()).hexdigest() for s in SIDES}
        rom_bytes = {s: (gateware[s] / 'alinx_ax7101_rom.init').stat().st_size for s in SIDES}
        digests = {s: gate.inputs(gateware[s], (gateware[s] / 'baseline_integrated.tcl').read_text()) for s in SIDES}
        images = {s: json.loads((gateware[s] / 'baseline_images.json').read_text()) for s in SIDES}
        report['shapes'][shape] = {
            'files': {s: len(files[s]) for s in SIDES}, 'only': only,
            'identical': len(identical), 'equal_after_root_placeholders': normalized_equal,
            'different': different, 'rom_sha256': rom, 'rom_bytes': rom_bytes,
            'integrated_inputs_sha256': digests,
            'images': {s: [(Path(i['path']).name, i['bytes'], i['sha256']) for i in images[s]] for s in SIDES},
        }
        ok = ok and not different and not any(only.values()) and rom[SIDES[0]] == rom[SIDES[1]] \
            and digests[SIDES[0]] == digests[SIDES[1]]
        a, z = SIDES
        print(f"{shape}: {len(files[a])}/{len(files[z])} files, {len(identical)} identical, "
              f"{len(normalized_equal)} equal after root placeholders, {len(different)} different, "
              f"only {a} {len(only[a])}, only {z} {len(only[z])}")
        print(f"  ROM {rom[a]} ({rom_bytes[a]} B) / {rom[z]} ({rom_bytes[z]} B)")
        print(f"  integrated inputs {digests[a]} / {digests[z]}")
        report['shapes'][shape]['different'] = different
    report['verdict'] = 'identical' if ok else 'differs'
    Path(sys.argv[3]).write_text(json.dumps(report, indent=1) + '\n')
    print('verdict:', report['verdict'])
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
