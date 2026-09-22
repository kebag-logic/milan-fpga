import collections,json,pathlib,re
OUT=pathlib.Path('$WORKSPACE_HOME/milan-fpga-management/2026-09-22/504-r1-r227')
summary={'head':'3d90958f3a82ca2a9617112c107a22f332117e17','modes':{}}
for name,want in (('compiled',208),('absent',182)):
 text=(OUT/'raw'/f'gate-{name}.log').read_text();assert f'{want}/{want} mutations rejected' in text;assert '46/46 RTL mutation variants elaborated' in text;assert '17/17 legitimate firmware edits and 4/4 legitimate Makefile edits accepted' in text
 records=[json.loads(l) for l in (OUT/'raw'/f'{name}-argv.jsonl').read_text().splitlines()];compiles=[r for r in records if '-std=gnu99' in (r.get('actual_argv') or [])];assert len(compiles)==(212 if name=='compiled' else 0)
 assert all(r['requested_argv'][1:]==r['actual_argv'][1:] for r in records if r.get('actual_argv'))
 summary['modes'][name]={'hostile_refusals':want,'firmware_positives':17,'makefile_positives':4,'rtl_variants':46,'actual_firmware_compiles':len(compiles),'summary':text.splitlines()[-1],'compiler_record_count':len(records),'compiler_returncodes':dict(collections.Counter(r.get('returncode') for r in records)),'assembly_arch':dict(collections.Counter(r.get('assembly_arch') for r in records if 'assembly_arch' in r))}
 if name=='absent':assert 'GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations' in text
 else:assert 'GATE 1b PASS; 0 NOT RUN; 212 actual firmware compiler invocations' in text
summary['hosted']={}
for name in ('docs-check','elaborate'):
 text=(OUT/'public'/f'hosted-{name}.log').read_text()
 for required in ['SDK fresh installation: verified','SDK archive verified:','compiler argv[0]=/home/runner/br-milan-rv32/host/bin/riscv32-linux-gcc','161/161 non-RTL mutations','7/7 hostile shapes','17/17 legitimate firmware edits','c0b2b7cc067ece28e3124f94ccd9ee45c91b85e3']:
  assert required in text,(name,required)
 summary['hosted'][name]={'fresh_download_digest_relocation_verify':True,'actual_absolute_selector_adopted':True,'hosted_cache_hit_observed':False,'counted_non_RTL_hostile':161,'unelaborated_RTL_variants':46,'ineffective_make_control_skipped':1,'checkout':'c0b2b7cc067ece28e3124f94ccd9ee45c91b85e3'}
 if name=='docs-check':assert '135/135 non-RTL mutations' in text and 'GATE 1b PASS; 3 NOT RUN; 0 actual firmware compiler invocations' in text;summary['hosted'][name]['absent_counted_non_RTL_hostile']=135
print(json.dumps(summary,indent=2))
