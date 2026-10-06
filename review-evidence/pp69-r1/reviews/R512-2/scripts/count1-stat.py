#!/usr/bin/env python3
"""Focused count-one registry statistics comparison; never invokes a full bank."""
import argparse,concurrent.futures,json,pathlib,subprocess
p=argparse.ArgumentParser();p.add_argument('--packet',type=pathlib.Path,required=True);a=p.parse_args();packet=a.packet.resolve()
def run(label):
 tree=packet/'scratch'/('count1-'+label);out=packet/'receipts'/('stat-'+label);out.mkdir(exist_ok=True)
 with (tree/'notify.v').open('w') as f:subprocess.run(['sv2v','hdl/common/pp_pkg.sv','hdl/aecp/KL_aecp_notify.sv'],cwd=tree,stdout=f,check=True)
 script='read_verilog -sv notify.v; hierarchy -check -top KL_aecp_notify; proc; opt_clean; tee -o '+str(out/'stat.json')+' stat -json'
 with (out/'run.log').open('w') as f:r=subprocess.run(['yosys','-Q','-T','-p',script],cwd=tree,stdout=f,stderr=subprocess.STDOUT)
 (out/'run.rc').write_text(str(r.returncode)+'\n');assert r.returncode==0;return json.loads((out/'stat.json').read_text())
with concurrent.futures.ThreadPoolExecutor(2) as pool:base,head=list(pool.map(run,['base','head']))
b=base['modules']['\\KL_aecp_notify'];h=head['modules']['\\KL_aecp_notify'];diff={k:{'base':b[k],'head':h[k]} for k in b if b[k]!=h[k]};same=b['num_cells_by_type']==h['num_cells_by_type'] and b['num_cells']==h['num_cells']
x={'module':'KL_aecp_notify','count':1,'base':'e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8','head':'75c4eee4589e9317aca3d07b91f94a38b4cc86af','cell_counts_identical':same,'differences':diff};(packet/'receipts/count1-stat-comparison.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x,indent=2));raise SystemExit(not same)
