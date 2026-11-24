#!/usr/bin/env python3
"""Reconstruct the probe-name and generated source-closure audits from the reviewed tree."""
import pathlib,re,json,hashlib,sys
P=pathlib.Path(__file__).resolve().parents[1];repo=pathlib.Path(sys.argv[1]).resolve();rows=[]
for suite in ('crf_rx','mmcm_servo','aaf_clock_meter','maap'):
 d=repo/'tb/verilator'/suite
 probes={var:(mod,access) for access,mod,var in re.findall(r'(public_flat_\w+) -module "([^"]+)" -var "([^"]+)"',(d/'probes.vlt').read_text())}
 for f in sorted(d.glob('*')):
  if f.suffix not in ('.cpp','.h','.hpp'):continue
  for num,line in enumerate(f.read_text().splitlines(),1):
   if line.lstrip().startswith('//'):continue
   for name in re.findall(r'\w+__DOT__\w+',line):
    var=name.split('__DOT__')[-1]
    assert var in probes,(f,num,name)
    rows.append({'suite':suite,'source':str(f.relative_to(repo))+':'+str(num),'name':name,'probe':probes[var],'line':line.strip()})
(P/'receipts/probe-audit.json').write_text(json.dumps(rows,indent=2)+'\n')
for suite,names in {'crf_rx':['pdu_count_o','fmt_err_o'],'maap':['lfsr_r']}.items():
 for name in names:assert any(x['suite']==suite and x['name'].endswith('__DOT__'+name) and x['probe'][1]=='public_flat_rw' for x in rows)
T=P/'scratch/head';models=[]
for suite,dirs in {'crf_rx':['obj_dir','obj_discontinuity','obj_talker'],'mmcm_servo':['obj_phc'],'aaf_clock_meter':['obj_servo'],'maap':['obj_dir']}.items():
 for d in dirs:
  for f in (T/'tb/verilator'/suite/d).glob('*__verFiles.dat'):
   deps=[]
   for ln in f.read_text().splitlines():
    if not ln.startswith('S '):continue
    rel=ln.rsplit('"',2)[1]
    if rel.startswith('/') or not rel.endswith(('.sv','.v')):continue
    src=(f.parent.parent/rel).resolve();clean=re.sub(r'/\*.*?\*/|//[^\n]*','',src.read_text(),flags=re.S)
    defaults=re.findall(r'\binput\b[^,;)]*?=[^,;)]*',clean)
    deps.append({'path':str(src.relative_to(T)),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'defaulted_inputs':defaults})
   models.append({'suite':suite,'build':d,'dependencies':deps})
assert len(models)==6
assert not any(d['defaulted_inputs'] for m in models for d in m['dependencies'])
(P/'receipts/defaulted-port-audit.json').write_text(json.dumps(models,indent=2)+'\n')
print(f'PASS: {len(rows)} harness references, all writable probes rw; {len(models)} affected model closures without defaulted inputs')
