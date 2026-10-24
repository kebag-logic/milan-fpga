#!/usr/bin/env python3
"""Reproduce comment equivalence and observe mutation construction at build entry."""
import hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
repo,packet,simulator=map(lambda p:Path(p).resolve(),sys.argv[1:4])
scratch=packet/'scratch/inspection'; scratch.mkdir(parents=True,exist_ok=True)
rtl='hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv'
equiv={}
for rev in ['c7e87c8c87494f3444000b46954648ba1a94dcb8','c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83']:
    data=subprocess.check_output(['git','show',rev+':'+rtl],cwd=repo)
    source=scratch/(rev+'.sv'); source.write_bytes(data)
    out=subprocess.check_output([str(simulator),'-E','-P',str(source)])
    normalized=b''.join(line+b'\n' for line in out.splitlines() if line.strip())
    equiv[rev]={'sha256':hashlib.sha256(normalized).hexdigest(),'lines':len(normalized.splitlines())}
spec=importlib.util.spec_from_file_location('format_mutants',repo/'tb/verilator/avtp_rxmon/format_mutants.py')
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
records=[]
class AtBuild(Exception): pass
def intercept(source,mdir):
    record={'build_source':source.name,'generated_sources':[p.name for p in source.parent.glob('*.sv')],
            'engine_text':source.read_text().split('if (!fmt_ok_w) begin')[1].split('end')[0]}
    records.append(record)
    raise AtBuild
module.build=intercept
for name,pattern,replacement,ref_line,check in module.BOTH_COPIES:
    work=scratch/name.split(':')[0].replace(' ','_'); work.mkdir(exist_ok=True)
    try:
        module.run_mutant(module.RTL.read_text(),(name,pattern,replacement,check),work,(module.REF.read_text(),ref_line))
    except AtBuild: pass
    records[-1]['arm']=name
    records[-1]['reference_source_unchanged']=module.REF.read_bytes()==subprocess.check_output(['git','show','HEAD:tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv'],cwd=repo)
result={'preprocessor_equivalence':equiv,'mutation_build_entry_observations':records,
        'observation_limit':'Build intercepted before execution; this proves construction only. Real simulation results are separate receipts.'}
(packet/'delta_inspection.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
