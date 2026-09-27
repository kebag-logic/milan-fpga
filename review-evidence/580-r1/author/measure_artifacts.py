"""Measure generated files at the current processor pin; compare both runs."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path('$LANES/580-pp-pin-16be6768')
OUT = Path(__file__).resolve().parent
WORK = Path('$VALIDATION_STORAGE/580-a366')
label = sys.argv[1]
pp = ROOT / 'protocol-processor'
assert subprocess.check_output(['git', '-C', str(pp), 'rev-parse', '--show-toplevel'], text=True).strip() == str(pp)
pin = subprocess.check_output(['git', '-C', str(pp), 'rev-parse', 'HEAD'], text=True).strip()
result = {'pin': pin, 'configs': {}}
for cfg in sorted((ROOT/'configs').glob('endstation_*.yaml')):
    dest = WORK / label / cfg.stem
    dest.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, 'sw/builder/endstation_builder.py', str(cfg.relative_to(ROOT)),
                    '-o', str(dest/'builder')], cwd=ROOT, check=True, timeout=600)
    generated = dest/'builder'/cfg.stem
    subprocess.run([sys.executable, 'avdecc/gen_aemi_image.py', '--overlay', str(generated/'aem_overlay.json'),
                    '--line-bytes', '576', '-o', str(dest/'aem.bin'), '-m', str(dest/'aem.map'),
                    '--json', str(dest/'aem.json')], cwd=ROOT, check=True, timeout=600)
    records = {}
    for path in sorted(dest.rglob('*')):
        if path.is_file():
            data = path.read_bytes()
            records[str(path.relative_to(dest))] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    result['configs'][cfg.stem] = records
(OUT/(label+'-artifacts.json')).write_text(json.dumps(result, indent=2)+'\n')
if label == 'new':
    old = json.loads((OUT/'old-artifacts.json').read_text())
    assert old['configs'] == result['configs'], 'artifact hashes or paths changed'
    for cfg, records in result['configs'].items():
        for path in records:
            assert (WORK/'old'/cfg/path).read_bytes() == (WORK/'new'/cfg/path).read_bytes(), (cfg,path)
    print('PASS: all five configurations have byte-identical AEM images and builder outputs')
print(json.dumps(result, indent=2))
