"""Round 10 receipts: each file redacted as the packer redacts, with its hash before and after (MANIFEST.json)."""
import hashlib, json, subprocess, sys
from pathlib import Path
sys.path.insert(0, '$VALIDATION_STORAGE/r10/tools')
import importlib.util
spec = importlib.util.spec_from_file_location('pack10', '$VALIDATION_STORAGE/r10/tools/pack10.py')
pack = importlib.util.module_from_spec(spec); spec.loader.exec_module(pack)
R = Path('$VALIDATION_STORAGE/r10'); OUT = Path('$LANE_TOOLS/artysplit-a829/round10/receipts')
ROOT = Path('$SOURCE')
F = R / 'final-census'
GROUPS = {
 'bind': [R/'bind-regrade.log', R/'save_time.py', R/'save-times.json'],
 'egress': [R/'egress/proto.py', R/'egress/all.json', R/'egress/all.log', R/'egress-fixed.log', R/'egress-selftest.log',
            R/'egress-structural.log', F/'egress-100.log', R/'extract-egress.log'],
 'census': [R/'census-w1.log', R/'census-w2.log', R/'census-w3.log', F/'completed.json', F/'manifest.json', R/'qualify.log',
            F/'qualification.json', F/'qualification-commands.json', F/'derived-model.json', F/'census.json',
            F/'merged-census.json', *sorted(F.glob('regrade-*.log')), F/'record-classes.log', F/'egress-ledger.log'],
 'derivation': [R/'derive/run.log', R/'derive/census.log', R/'derive/kept-grade.log', R/'derive/census.json',
                R/'derive/merged-census.json', R/'derive/derived-model.json'],
 'control-derivation': [R/'control/run.log', R/'control/census.log', R/'control/census-no-disposition.json',
                        R/'control/merged-no-disposition.json', R/'control/derive-no-disposition.json'],
 'extract': [R/'regrade-full.log', R/'extract.log', R/'extract-regrade.log', R/'extract-control.log',
             R/'scrub/r10-extract.log', R/'scrub/r10-extract.json', R/'scrub/r9-extract.json', R/'scrub/identity.py'],
 'builder': [R/'builder/builder-split.log', R/'builder/builder-split.json', R/'builder/compare.py', R/'builder/final.sh'],
 'validation': [R/'gates10.rc', *sorted(R.glob('gate-*.log')), R/'service-selftest.log', R/'service-selftest.json',
                *sorted(R.glob('service-selftest-[0-7].log')),
                *sorted((R/'selftest-attempt0').glob('*')), *sorted((R/'gates-fb4b456a4').glob('*'))],
 'recipes': [R/'run-census-window.py', R/'trial-case.py', R/'build-final-variant.py', R/'run-env.sh', R/'gates10.sh',
             R/'service-selftest.py', R/'derive/run.sh', R/'control/run.sh', *sorted((R/'tools').glob('*.py'))],
}
rows = []
for group, files in GROUPS.items():
    for src in files:
        raw = src.read_bytes(); pub = pack.scrub(raw)
        sub = 'attempt0-' if 'selftest-attempt0' in str(src) else ('gates-fb4b456a4-' if 'gates-fb4b456a4' in str(src) else '')
        name = sub + (src.parent.name + '-' if src.parent.name in ('derive', 'control') and group == 'recipes' else '') + src.name
        dst = OUT / group / name; dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(pub)
        assert len(pub) < 15_000_000, dst
        rows.append(dict(path=f'{group}/{name}', original_bytes=len(raw), original_sha256=hashlib.sha256(raw).hexdigest(),
                         bytes=len(pub), sha256=hashlib.sha256(pub).hexdigest()))
patch = subprocess.check_output(['git', 'log', '-p', '575118facfe226054fe3339878712a3e77bd73ab..HEAD'], cwd=ROOT)
(OUT / 'source').mkdir(exist_ok=True); (OUT / 'source/round10-commits.patch').write_bytes(pack.scrub(patch))
rows.append(dict(path='source/round10-commits.patch', original_bytes=len(patch), original_sha256=hashlib.sha256(patch).hexdigest(),
                 bytes=(OUT/'source/round10-commits.patch').stat().st_size, sha256=hashlib.sha256((OUT/'source/round10-commits.patch').read_bytes()).hexdigest()))
(OUT / 'MANIFEST.json').write_text(json.dumps(rows, indent=1) + '\n')
print('RECEIPTS', len(rows))
