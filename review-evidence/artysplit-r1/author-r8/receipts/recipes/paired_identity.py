"""Step 1 and step 2 side by side: each variant's native executable, firmware ELF and flash image, and each case's
stimulus, every hash computed here from that step's own files.

Step 1 is the census built at f7b90e3b7 (r7/step1/final-census); step 2 the one built at 74f942be5 (r7/final-census).
The step-2 stimulus is the script the step-2 build's scenario writes (run.all_groups), not the copied step-1 file.
"""
import hashlib, json, sys
from pathlib import Path
root = Path.cwd()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import build, run, scenario
S1 = Path('$VALIDATION_STORAGE/r7/step1/final-census'); S2 = Path('$VALIDATION_STORAGE/r7/final-census')
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
manifest = json.loads((S1 / 'manifest.json').read_text())
variants, cases, same = [], [], True
for variant, wanted in manifest['groups'].items():
    a, b = (json.loads((s / variant / 'build.json').read_text()) for s in (S1, S2))
    row = dict(variant=variant,
               executable=[sha(S1 / variant / 'native/Vsim'), sha(S2 / variant / 'native/Vsim')],
               executable_recorded=[a['executable_sha256'], b['executable_sha256']],
               elf=[sha(a['elf']), sha(b['elf'])],
               flash_image=[a.get('flash_image'), b.get('flash_image')], xip=[a.get('xip'), b.get('xip')])
    same &= row['executable'][0] == row['executable'][1] == row['executable_recorded'][0] == row['executable_recorded'][1]
    same &= row['elf'][0] == row['elf'][1] and row['flash_image'] == [None, None]
    variants.append(row)
    groups = {g.name: g for g in run.all_groups(scenario.point('arty-1x1', b), b)}
    for name in wanted:
        pair = [sha(S1 / variant / 'results' / (name + '.txt')), hashlib.sha256(groups[name].script().encode()).hexdigest()]
        same &= pair[0] == pair[1]
        cases.append(dict(case=f'{variant}/{name}', stimulus=pair))
record = dict(steps=['f7b90e3b781812863b87256d4b349ee2154d480b', '74f942be516b84915f7d982fe1e3c65b497c227a'],
              flash_note=('flash_image is null at both steps: build.build writes a separate flash image only for an '
                          'XIP core (core.xip, xip_image); these native census builds are not XIP, so the firmware is '
                          'in the ROM init files the native executable is built from.'),
              variants=variants, cases=cases, identical=same)
Path(sys.argv[1]).write_text(json.dumps(record, indent=1) + '\n')
lines = ['| Variant | Executable step 1 | Executable step 2 | ELF step 1 | ELF step 2 | Flash |', '|---|---|---|---|---|---|']
lines += [f"| {v['variant']} | `{v['executable'][0]}` | `{v['executable'][1]}` | `{v['elf'][0]}` | "
          f"`{v['elf'][1]}` | null / null |" for v in variants]
Path(sys.argv[2]).write_text('\n'.join(lines) + '\n')
print('IDENTICAL' if same else 'DIFFERENT', len(variants), 'variants', len(cases), 'stimuli')
