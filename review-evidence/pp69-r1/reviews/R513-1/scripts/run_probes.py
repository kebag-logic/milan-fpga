#!/usr/bin/env python3
"""Build reviewer-owned probes concurrently against unmodified exact-head RTL."""
import argparse, concurrent.futures, io, json, os, pathlib, subprocess, tarfile, time
p=argparse.ArgumentParser(); p.add_argument('--repo',required=True); p.add_argument('--verilator',required=True); a=p.parse_args()
packet=pathlib.Path(__file__).resolve().parents[1]; tree=packet/'scratch/probe-tree'; tree.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive','cb730a2f9dd7e4f60a03a38d4b47b569e68da8df'],cwd=a.repo))) as tf: tf.extractall(tree,filter='data')
path=tree/'tb/aecp_notify/port_tuple.hpp'; s=path.read_text(); extra=(packet/'scripts/registry_probe.hpp').read_text(); s=s.replace('int PortHarness::run() {',extra+'\nint PortHarness::run() {'); s=s.replace('  keyed_counters();','  keyed_counters();\n  reviewer_registry_probe(*this);'); path.write_text(s)
path=tree/'tb/pp_top/interface_phases.hpp'; s=path.read_text(); s=s.replace('io.d->rx_if_index_i = ifx;', 'io.d->rx_if_index_i = (i + 1 == f.size()) ? ifx : 1 - ifx;\n      if (i % 7 == 0) { io.d->rx_valid_i = 0; tick(); io.d->rx_valid_i = 1; }'); s=s.replace('    for (int i = 0; i < 4; ++i) tick();','    // No extra interframe clocks: allow the next complete frame immediately.'); extra=(packet/'scripts/top_probe.hpp').read_text(); s=s.replace('[[maybe_unused]] static void run_interfaces(H& h) {',extra+'\n[[maybe_unused]] static void run_interfaces(H& h) {'); s=s.replace('  p.registry_port_from_the_command();','  p.registry_port_from_the_command();\n  reviewer_queued_ports(p);'); path.write_text(s)
logs=packet/'receipts/probes'; logs.mkdir(exist_ok=True,parents=True); wrapper=packet/'scratch/bounded-verilator.py'
env=os.environ.copy(); env.update(VERILATOR=str(wrapper),R513_VERILATOR=str(pathlib.Path(a.verilator).resolve()),TMPDIR=str(packet/'scratch/tmp'),MAKEFLAGS='-j16',R513_COMPILE_JOBS='3')
def run(suite):
 cmd=['make','-j16','-C',str(tree/'tb'/suite),'interfaces','VERILATOR='+str(wrapper)]; start=time.monotonic()
 with (logs/(suite+'.log')).open('w') as f:
  f.write('command: '+repr(cmd)+'\n'); f.flush(); r=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT)
 (logs/(suite+'.rc')).write_text(str(r.returncode)+'\n'); row=dict(name=suite,rc=r.returncode,seconds=round(time.monotonic()-start,2)); print(json.dumps(row),flush=True); return row
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(run,['aecp_notify','pp_top']))
(logs/'results.json').write_text(json.dumps(results,indent=2)+'\n'); raise SystemExit(any(r['rc'] for r in results))
