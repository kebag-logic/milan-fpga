#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,re
ap=argparse.ArgumentParser();ap.add_argument('--source',type=pathlib.Path,required=True);ap.add_argument('--packet',type=pathlib.Path,required=True);a=ap.parse_args();p=a.packet.resolve();w=p/'scratch';rows=[]
replace=[(str(a.source.resolve()),'$REVIEW_SOURCE'),(str(p),'$REVIEW_PACKET'),('$VALIDATION_TOOLS','$READ_ONLY_DEPENDENCIES'),('<home-path>/work/tsn-c-stack/tsn-c-stack','$HOSTED_SOURCE')]
def copy(f,d):
 b=f.read_bytes();text=b.decode();
 for old,new in replace:text=text.replace(old,new)
 text=re.sub(r'$VALIDATION_STORAGE/[^\s]+?/root', '$UNAVAILABLE_SDK',text)
 text=re.sub(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[^/\s]+/diff', '$SIMULATOR_INSTALL',text)
 out=p/'receipts'/d;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text)
 rows.append(dict(source=str(f.relative_to(w)),published=str(out.relative_to(p)),original_sha256=hashlib.sha256(b).hexdigest(),published_sha256=hashlib.sha256(out.read_bytes()).hexdigest()))
for source,dest in [('validation','environment-attempt'),('validation-sdk','validation')]:
 for f in (w/source).iterdir():
  if f.is_file() and f.suffix in ['.log','.rc','.json']:copy(f,pathlib.Path(dest)/f.name)
for prefix in ['validate','validate-sdk','rv32','rv32-base','escape','physical-original','physical-gap','gap','clang-sdk-build','clang-sdk-test','fabric-stock','fabric-edge-15000','fabric-edge-14999']:
 for ext in ['log','rc']:
  f=w/(prefix+'.'+ext)
  if f.exists():copy(f,pathlib.Path('commands')/f.name)
for name in ['physical-original','physical-gap','gap','escape']:
 for f in (w/name).glob('*.json'):copy(f,pathlib.Path(name)/f.name)
 for d in (w/name).iterdir():
  if d.is_dir():
   for f in d.glob('*.log'):copy(f,pathlib.Path(name)/d.name/f.name)
for f in (w/'complete-suites').rglob('*'):
 if f.is_file():copy(f,pathlib.Path('complete-suites')/f.relative_to(w/'complete-suites'))
for f in (w/'physical-entity').rglob('build.log'):copy(f,pathlib.Path('physical-entity')/f.parent.name/f.name)
for name in ['rv32','rv32-base']:
 copy(w/name/'results.json',pathlib.Path(name)/'results.json')
 for f in (w/name).glob('*/*.log'):copy(f,pathlib.Path(name)/f.relative_to(w/name))
for f in (w/'validation-sdk/mutations').glob('*/*.xml'):copy(f,pathlib.Path('mutations')/f.relative_to(w/'validation-sdk/mutations'))
for name in ['results.json','message-markers.json']:copy(w/'validation-sdk/mutations'/name,pathlib.Path('mutations')/name)
for name in ['gates.json','coverage.log','static-analysis.log','traceability.log','test-inventory.log']:copy(w/'public-author-r3/validation'/name,pathlib.Path('author')/name)
for name in ['source-snapshot.json','final-audit.json','sizes.json','complete-suite/results.json','large-artifacts.json']:copy(w/'public-author-r3'/name,pathlib.Path('author')/name)
for name in ['gates.json','coverage.log','static-analysis.log','traceability.log','test-inventory.log']:copy(w/'hosted/quality-evidence'/name,pathlib.Path('hosted')/name)
copy(w/'hosted/rv32-evidence/results.json',pathlib.Path('hosted/rv32-results.json'))
copy(w/'run-results.json',pathlib.Path('commands/run-results.json'))
(p/'receipts/receipt-provenance.json').write_text(json.dumps(rows,indent=2)+'\n');print('Collected',len(rows),'receipts with original and published digests')
