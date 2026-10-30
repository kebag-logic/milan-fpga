#!/usr/bin/env python3
"""Plant PHY-only wiring; require the unchanged parent test to reject both omissions."""
import pathlib,subprocess,sys
source=pathlib.Path(sys.argv[1]).resolve();p=pathlib.Path(sys.argv[2]).resolve();v=sys.argv[3]
w=p/'scratch'/'wiring-probe';o=p/'mutation';o.mkdir(exist_ok=True)
def cmd(args,cwd,log):
 with log.open('a') as f:
  f.write('$ '+repr(args)+'\n');f.flush()
  return subprocess.run(args,cwd=cwd,stdout=f,stderr=subprocess.STDOUT).returncode
setup=o/'setup.log'
assert cmd(['git','clone','--shared',str(source),str(w)],source,setup)==0
assert cmd(['git','checkout','--detach','f99405af0b2caad46e84f50f8251ffbffaa80836'],w,setup)==0
for sub in ['gptp-processor','protocol-processor','third_party/verilog-axis','third_party/lwSRP','third_party/tsn-c-stack']:
 assert cmd(['git','config','submodule.'+sub+'.url',str(source/sub)],w,setup)==0
 assert cmd(['git','-c','protocol.file.allow=always','submodule','update','--init',sub],w,setup)==0
path=w/'hdl/milan/milan_datapath.sv';original=path.read_bytes()
needle=b'        .port_enabled_i  (eff_link_w),'
assert original.count(needle)==1
path.write_bytes(original.replace(needle,b'        .port_enabled_i  (i_link_up),'))
try:
 rc=cmd(['make','-j16','VERILATOR='+v,'VERILATOR_JOBS=12','gptp'],w/'tb/verilator/milan_dp',o/'phy-only.log')
 (o/'phy-only.rc').write_text(str(rc)+'\n')
 text=(o/'phy-only.log').read_text()
 expected=['#94 asCapable falls when LINK_CTRL[0] withdraws the link','#94 asCapable falls when the guard loses the receive clock']
 assert rc != 0
 assert all(('FAIL '+x+' got') in text for x in expected)
 assert '210 checks: 208 PASS, 2 FAIL' in text
 (o/'verdict.txt').write_text('KILLED: PHY-only wiring; LINK_CTRL[0] and guard loss checks both FAIL; 210 checks, 208 PASS, 2 FAIL.\n')
 print('PHY-only wiring mutant KILLED',flush=True)
finally:
 path.write_bytes(original)
 assert cmd(['git','diff','--exit-code','HEAD'],w,o/'restored.log')==0
