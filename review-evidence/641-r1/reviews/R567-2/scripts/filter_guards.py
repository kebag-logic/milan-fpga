#!/usr/bin/env python3
"""Check the original filter guards and removal sensitivity without a build."""
import argparse, hashlib, json, os, subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--work',type=Path,required=True);ap.add_argument('--verilator',required=True);a=ap.parse_args()
root=a.repo.resolve();work=a.work.resolve();work.mkdir(parents=True,exist_ok=True)
version=subprocess.check_output([a.verilator,'--version'],text=True).strip();assert 'Verilator 5.050 ' in version
print(version);print('launcher_sha256='+hashlib.sha256(Path(a.verilator).read_bytes()).hexdigest())
filter=root/'hdl/ieee8021q/filtering/rx_mac_filter.sv';tcam=filter.with_name('tcam.sv')
text=filter.read_text();start=text.index('  if (TDATA_WIDTH < 48) begin : gen_guard_dmac_in_beat0');end=text.index('  // -----------------------------------------------------------------------',start)
mutant=work/'rx_mac_filter.sv';mutant.write_text(text[:start]+text[end:])
cases=['TDATA_WIDTH=32','TDATA_WIDTH=52','NUM_ENTRIES=0','ACTION_WIDTH=0']
base=[a.verilator,'--lint-only','-Werror-USERERROR','--top-module','rx_mac_filter','--Mdir',str(work/'obj'),str(tcam)]
for name,path in [('exact',filter),('guards-deleted',mutant)]:
 for case in cases:
  r=subprocess.run([*base,str(path),'-G'+case],cwd=work,capture_output=True,text=True,timeout=60)
  (work/(name+'-'+case.replace('=','-')+'.log')).write_text(r.stdout+r.stderr)
  caught=r.returncode!=0 and 'USERERROR' in r.stderr and ('rx_mac_filter: '+case+' ') in r.stderr
  assert caught==(name=='exact'),(name,case,r.returncode,r.stderr)
  print(name,case,'rc='+str(r.returncode),'own_diagnostic='+str(caught))
r=subprocess.run([*base,str(filter),'-Wno-DECLFILENAME','-Wno-UNUSEDSIGNAL','-Wno-UNUSEDPARAM'],cwd=work,capture_output=True,text=True,timeout=60)
assert r.returncode==0,r.stderr
print('legal default rc=0; four original refusals and four guard-removal controls PASS')
