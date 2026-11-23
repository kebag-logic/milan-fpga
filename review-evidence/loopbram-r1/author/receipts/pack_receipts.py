import gzip,hashlib,json,sys
from pathlib import Path
s=Path('$SCRATCH');out=Path('<home-path>/milan-fpga-management/2026-09-23/loopbram-a826/round2/receipts')
sys.path.insert(0,'<home-path>/milan-fpga-management/2026-09-23');import privacy
patterns=['*.py','*.json','*.yaml','gates/*.json','regressions/input-final.*','regressions/capture.*','regressions/queue.*','regressions/render.*','regressions/coherence.*','mutants-head/*.log','mutants-head/*.json','builder-union/*.log','builder-union/*.json','builder-union-attempt3/leg1.log','builder-union-attempt4/leg1.log','leaf/*/*.rpt','leaf/*/*.json','leaf/*/*.tcl','leaf/*/*.log','leaf-capture/capture_leaf.sv','leaf-capture/*/*.rpt','leaf-capture/*/*.json','leaf-capture/*/*.tcl','leaf-capture/*/*.log','route/**/measure_*.json','route/**/measure_*.tcl','route/**/measure_*.log','route/**/*.rpt','route/**/alinx_ax7101.tcl','route/**/alinx_ax7101.xdc','route/**/alinx_ax7101.v','on/*/soc_params.json','on/*/nvm_split.json','on/*/platform_shape.json','on/*/aem_overlay.json','route/**/*grade.txt','yosys/run.log','yosys/run.json','yosys/results/*.json','full-suites/*.log','full-suites/*.json','builds/*-on-final.log','builds/*-off.log']
files={p for pattern in patterns for p in s.glob(pattern) if p.is_file()}
final_gates=['builder-new','builder-capacity-final','builder-tail','docs-final','style-final','paths-final','py-final-head','cpp-final','hygiene-final','em-dash-final','lint','feature','sources','xvlog','check_sv_idiom','check_wire_accountability','check_nvm_capture','check_nvm_klj3','check_nvm_record_space','nvm-format-head','nvm-format-selftest']
files.update(p for name in final_gates for p in (s/'gates').glob(name+'.*') if p.is_file())
rows=[]
for p in sorted(files):
 raw=p.read_bytes();data=raw.replace(str(s).encode(),b'$SCRATCH').replace(b'$CHECKOUT',b'$CHECKOUT')
 data=privacy.scrub_redact(data);assert privacy.scrub_redact(data)==data
 # The payload is already scrubbed. A binary-rule match in deflate bytes is
 # incidental; vary only compression, preserving the independently checked payload.
 for level in [9,6,1,2,3,4,5,7,8,0]:
  blob=gzip.compress(data,compresslevel=level,mtime=0)
  if privacy.scrub_redact(blob)==blob:break
 else:raise AssertionError(('No privacy-stable gzip encoding',str(p)))
 if level!=9:print('Alternate gzip level',level,'for',p.relative_to(s),flush=True)
 assert gzip.decompress(blob)==data
 assert privacy.scrub_redact(gzip.decompress(blob))==gzip.decompress(blob)
 name=str(p.relative_to(s)).replace('/','--')+'.gz';(out/name).write_bytes(blob)
 rows.append({'file':name,'gzip_level':level,'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest(),'payload_sha256':hashlib.sha256(data).hexdigest(),'original_sha256':hashlib.sha256(raw).hexdigest()})
(out/'manifest.json').write_text(json.dumps({'head':json.loads((s/'source_identity.json').read_text())['head'],'privacy':'compressed and decompressed bytes are unchanged by privacy.scrub_redact','receipts':rows},indent=2)+'\n')
for p in out.rglob('*.gz'):
 b=p.read_bytes();assert privacy.scrub_redact(b)==b;assert privacy.scrub_redact(gzip.decompress(b))==gzip.decompress(b)
print('PACKED',len(rows),'RECEIPTS; privacy assertions passed')
