#!/usr/bin/env python3
"""Cross-check the published summaries and the source's diagram/ratchet identities."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);a=p.parse_args()
base=a.packet/'public/author/receipts'
files=sorted((base/'arms').glob('regrade-*.txt'));assert len(files)==16
for f in files:
 text=f.read_text()
 summary=next(x for x in text.splitlines() if 'groups graded, ' in x)
 assert ', 0 refusals,' in summary
 expected=7 if '-none-' in f.name or '-answering-ports-' in f.name else 0
 assert f', {expected} budget misses ' in summary
 assert ', 0 of ' in summary
 print(f.name,summary)
for f in sorted((a.packet/'public/author-text/fwgate').glob('*.log')):
 text=f.read_text();assert 'test_ctrl_firmware: PASS' in text and 'rc 0]' in text
 if 'fwgate-1-' in f.name: assert 'mutants: 851 of 851 caught' in text
 print(f.name,'PASS', '851 of 851 planted defects caught' if 'fwgate-1-' in f.name else '')
for f in sorted((base/'kept').glob('*09599524.txt')):
 assert 'kept_grade: PASS' in f.read_text();print(f.name,'PASS')
lines=(a.root/'tb/verilator/ctrl_service_budget/scenario.py').read_text().splitlines()
assert len(lines)==1000;print('scenario.py:',len(lines),'lines')
sys.path.insert(0,str(a.root/'scripts'))
import png_artifact
png='docs/diagrams/submodule_boundaries.png';source='docs/diagrams/submodule_boundaries.drawio'
info=png_artifact.verify_pixel_manifest(a.root/'docs/diagrams/PNG_MANIFEST.json',png,source,a.root/png,a.root/source)
print('PASS diagram manifest: decompressed raster',info.raster_sha256,'source',png_artifact.source_digest(a.root/source))
print('Firmware gate source transfer ea52ec11 -> reviewed head:')
out=subprocess.check_output(['git','-C',str(a.root),'diff','--name-only','ea52ec11..095995243bc354b8a41755f3fdfae343511cc668'],text=True)
assert out.strip()=='tb/verilator/ctrl_service_budget/scenario.py';print(out.strip())
print('PASS published summary consistency; original simulation logs and routed reports are not reconstructed by this check')
