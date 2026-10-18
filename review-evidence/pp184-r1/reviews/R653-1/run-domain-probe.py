#!/usr/bin/env python3
import pathlib,subprocess,os,sys
p=pathlib.Path(__file__).resolve().parent
s=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else p/'scratch/source'
b=p/'scratch/domain-probe';b.mkdir(exist_ok=True)
c=[os.environ.get('REVIEW_VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'),'--cc','--exe','--build','-j','2','--top-module','KL_srp_domain','--Mdir',str(b),'-Wno-fatal',str(s/'hdl/srp/KL_srp_domain.sv'),str(p/'domain-probe.cpp'),'-o','domain-probe']
with (p/'domain-probe-build.log').open('w') as f:r=subprocess.run(c,stdout=f,stderr=subprocess.STDOUT)
(p/'domain-probe-build.rc').write_text(str(r.returncode)+'\n')
if r.returncode:sys.exit(r.returncode)
with (p/'domain-probe.log').open('w') as f:r=subprocess.run([str(b/'domain-probe')],stdout=f,stderr=subprocess.STDOUT)
(p/'domain-probe.rc').write_text(str(r.returncode)+'\n');print((p/'domain-probe.log').read_text())

with (p/'documented-contract.log').open('w') as f:r=subprocess.run([str(b/'domain-probe'),'--documented-contract'],stdout=f,stderr=subprocess.STDOUT)
(p/'documented-contract.rc').write_text(str(r.returncode)+'\n');print((p/'documented-contract.log').read_text())
