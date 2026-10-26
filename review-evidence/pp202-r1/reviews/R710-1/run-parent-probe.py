#!/usr/bin/env python3
import hashlib,json,pathlib,subprocess
OUT=pathlib.Path(__file__).resolve().parent
ROOT=OUT/'scratch/parent'
SRC=ROOT/'hdl/ieee1722/aaf/KL_aaf_packetizer.sv'
cmd=[str(OUT/'scoped-compiler.py'),'--cc','--exe','--build','-j','2','--top-module','KL_aaf_packetizer','-GN_TALKERS_P=2','-Wno-fatal','--Mdir',str(ROOT/'obj_probe'),str(SRC),str(OUT/'parent-probe.cpp'),'-o','parent_probe']
with (OUT/'parent-probe.log').open('w') as f:
    f.write('command: '+repr(cmd)+'\n');f.flush()
    build=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT).returncode
    run=subprocess.run([str(ROOT/'obj_probe/parent_probe')],stdout=f,stderr=subprocess.STDOUT).returncode if build==0 else None
result=dict(build_rc=build,run_rc=run,patched_source_sha256=hashlib.sha256(SRC.read_bytes()).hexdigest())
(OUT/'parent-probe-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
