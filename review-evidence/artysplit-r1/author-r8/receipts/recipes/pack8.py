"""Round 8 receipts outside the census extract: redacted text, each file's original and published hash."""
import hashlib, json, re, sys
from pathlib import Path
sys.path.insert(0, '$LANE_TOOLS')
import privacy
ROOT = Path('$SOURCE'); SCR = Path('$VALIDATION_STORAGE')
R = SCR / 'r8'; OUT = Path('$LANE_OUTPUT/round8/receipts')
def sha(b): return hashlib.sha256(b).hexdigest()
def scrub(data):
    data = data.replace(str(ROOT).encode(), b'$SOURCE').replace(str(SCR).encode(), b'$VALIDATION_STORAGE')
    data = data.replace(b'$LANE_OUTPUT', b'$LANE_OUTPUT')
    data = data.replace(b'$LANE_TOOLS', b'$LANE_TOOLS')
    data = data.replace(b'$XILINX', b'$XILINX').replace(b'$TOOLCHAIN', b'$TOOLCHAIN')
    data = data.replace(b'$HOME', b'$HOME').replace(b'$SHARED_STORAGE', b'$SHARED_STORAGE')
    data = re.sub(rb'(?m)^(\|?\s*Host\s*:) .*$', rb'\1 <build-host>', data)
    return privacy.scrub_redact(data)
GROUPS = {
 'proofs': [R/'extract.log', R/'extract-regrade.log', R/'extract-control.log', SCR/'r7/receipt-regrade.log',
            SCR/'r7/receipt-regrade-control.log', R/'proof-comparison.json'],
 'control-derivation': [R/'control/census-no-disposition.json', R/'control/merged-no-disposition.json',
                        R/'control/derive-no-disposition.json', R/'control/run.sh', R/'control/run.log',
                        R/'control/census.log', R/'control/merge.log'],
 'identity': [R/'paired-identity.json', R/'paired-identity.md'],
 'route-utilization': [R/'route-util/r7-route-utilization.rpt', R/'route-util/r7-route-utilization.rpt.hier',
                       R/'route-util/r6-route-utilization.rpt', R/'route-util/r6-route-utilization.rpt.hier',
                       R/'route-util/r7-identity.txt', R/'route-util/r6-identity.txt', R/'route-util/r7-vivado.log',
                       R/'route-util/r6-vivado.log', R/'route-util/report.tcl', R/'route-util/run.sh', R/'route-util/run.log'],
 'extract-floor': [R/'filtertest.log'],
 'gates': [R/'gates8.rc', *sorted(R.glob('gate-*.log')), R/'builder-split.log'],
 'recipes': [R/'tools/paired_identity.py', R/'tools/filtertest.py', R/'tools/pack8.py', R/'gates8.sh'],
}
rows = []
for group, files in GROUPS.items():
    for src in files:
        raw = src.read_bytes(); pub = scrub(raw)
        name = ('round7-' if '/r7/' in str(src) else '') + src.name
        dst = OUT / group / name; dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(pub)
        assert len(pub) < 15_000_000, dst
        rows.append(dict(path=f'{group}/{name}', original_bytes=len(raw), original_sha256=sha(raw),
                         bytes=len(pub), sha256=sha(pub)))
(OUT / 'MANIFEST.json').write_text(json.dumps(rows, indent=1) + '\n')
print('PACKED', len(rows))
