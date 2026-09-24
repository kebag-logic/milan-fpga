"""Run from the processor repository root after building tb/pp_top.

Only tb/pp_top/ucode.hex is temporarily changed. The tracked generator and
RTL remain untouched. Logs are written beside this evidence script.
"""
import hashlib
import json
from pathlib import Path
import runpy
import subprocess

root = Path.cwd()
out = Path(__file__).resolve().parent
suite = root / 'tb/pp_top'
rom_path = suite / 'ucode.hex'
original = rom_path.read_bytes()
gen = runpy.run_path(str(root / 'hdl/aecp/ucode/gen_ucode.py'))
words = [int(line, 16) for line in original.decode().splitlines()]
assert words == gen['rom'], 'Start with the unmodified generated ROM'
mutations = [
    ('success-mutant', gen['E_NOTIMPL'],
     gen['u']('SET_STATUS', imm=gen['ST_OK'])),
    ('features-mutant', gen['E_MVUINFO'] + 5,
     gen['u']('MOVE', rd=6, imm=3)),
]
records = []
try:
    for name, index, replacement in mutations:
        changed = words.copy()
        changed[index] = replacement
        assert changed[index] != words[index]
        assert sum(a != b for a, b in zip(changed, words)) == 1
        rom_path.write_text(''.join(f'{word:012x}\n' for word in changed))
        log = out / (name + '.log')
        with log.open('w') as stream:
            result = subprocess.run(['./obj_dir/Vpp_top_sim'], cwd=suite,
                                    stdout=stream, stderr=subprocess.STDOUT,
                                    timeout=1800)
        lines = log.read_text().splitlines()
        failures = [line for line in lines if 'FAIL' in line]
        assert result.returncode != 0, f'{name} survived'
        if name == 'success-mutant':
            for ct in range(1, 6):
                assert any(f'M4: MVU 0x{ct:04x} must answer ' in line
                           for line in failures), (name, ct, failures)
                assert any(f'M4: MVU 0x{ct:04x} NOT_IMPLEMENTED echo ' in line
                           for line in failures), (name, ct, failures)
            assert not any('M4:' in line and ('frame length' in line or
                           'retain command cdl' in line) for line in failures)
        else:
            assert any('M2: features_flags' in line for line in failures)
        record = dict(name=name, word=index, original=f'{words[index]:012x}',
                      mutant=f'{replacement:012x}', rc=result.returncode,
                      failures=failures, log=log.name)
        records.append(record)
        (out / 'mutation-results.json').write_text(json.dumps(records, indent=2) + '\n')
        print(json.dumps(record), flush=True)
finally:
    rom_path.write_bytes(original)
    assert rom_path.read_bytes() == original
    print('Original ROM restored; sha256=' + hashlib.sha256(original).hexdigest(),
          flush=True)
