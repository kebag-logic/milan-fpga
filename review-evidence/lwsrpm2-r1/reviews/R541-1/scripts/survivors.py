# SPDX-License-Identifier: Apache-2.0
"""Check reported coverage gaps with single faults in a disposable exported tree."""
import argparse, hashlib, os, pathlib, subprocess, sys, tarfile, io
p = argparse.ArgumentParser()
p.add_argument('--source', type=pathlib.Path, required=True)
p.add_argument('--packet', type=pathlib.Path, required=True)
p.add_argument('--prefix', type=pathlib.Path, required=True)
p.add_argument('--jobs', type=int, default=16)
a=p.parse_args(); source=a.source.resolve(); packet=a.packet.resolve()
work=packet/'scratch/survivors'; work.mkdir(); tree=work/'source'; tree.mkdir(); build=work/'build'
archive=subprocess.check_output(['git','-C',str(source),'archive','HEAD'])
with tarfile.open(fileobj=io.BytesIO(archive)) as t: t.extractall(tree, filter='data')
runner=[sys.executable,str(packet/'scripts/run.py'),'--source',str(source),'--packet',str(packet)]
def run(label, cmd):
    return subprocess.run([*runner,'--label',label,'--',*map(str,cmd)]).returncode
if run('survivors-configure',['cmake','-S',tree,'-B',build,'-DCMAKE_PREFIX_PATH='+str(a.prefix.resolve()),'-DLWSRP_MILAN=OFF']): sys.exit(2)
mad='src/core/mrp_mad.c'; pdu='src/core/mrp_pdu.c'
cases=[
 ('local-rla',mad,'// 10.7.6.6: the committed sLA also signals rLA locally.\n        broadcast_event(app, ps, MRP_EVENT_RLA, port_id);','/* Removed committed local receive event. */'),
 ('omitted-txlaf',mad,'deliver_event(app, ps, a, MRP_EVENT_TXLAF, port_id);','/* Removed omitted-value event. */'),
 ('reserved-leaveall',pdu,'la > MRP_LA_ALL || need > end - off','need > end - off'),
 ('listener-ready',mad,'mrp_four_pack(bytes[len], 0, 0, 0)','mrp_four_pack(2, 0, 0, 0)'),
 ('leaveall-upper',mad,'ps->leaveall_cs / 2u - 1u','ps->leaveall_cs / 2u + 1u'),
 ('leaveall-wide',mad,'ps->leaveall_cs / 2u - 1u','ps->leaveall_cs - 1u'),
 ('reclaim-lo',mad,'a->appl == MRP_APPL_STATE_QO))','a->appl == MRP_APPL_STATE_QO || a->appl == MRP_APPL_STATE_LO))'),
 ('milan-redeclare',mad,'ev == MRP_EVENT_RLV &&','(ev == MRP_EVENT_RLV || ev == MRP_EVENT_REDECLARE) &&'),
 ('milan-txla',mad,'ev == MRP_EVENT_RLV &&','(ev == MRP_EVENT_RLV || ev == MRP_EVENT_TXLA) &&'),
 ('received-la-timer',mad,'la_event(rc->app, rc->ps, MRP_EVENT_RLA, rc->port_id);','/* Removed participant timer restart. */'),
]
originals={name:(tree/name).read_bytes() for _,name,_,_ in cases}
rows=[]
for label,name,old,new in cases:
    path=tree/name; original=originals[name]; text=original.decode()
    if text.count(old)!=1:
        print(label,'replacement count',text.count(old),flush=True);sys.exit(3)
    path.write_text(text.replace(old,new))
    try:
        built=run('survivor-'+label+'-build',['make','-C',build,'-j'+str(min(a.jobs,16))])
        tested=run('survivor-'+label+'-test',['ctest','--test-dir',build,'--output-on-failure','-V']) if built==0 else None
        rows.append((label,built,tested))
    finally: path.write_bytes(original)
restored=all((tree/name).read_bytes()==data for name,data in originals.items())
built=run('survivors-restored-build',['make','-C',build,'-j'+str(min(a.jobs,16))])
tested=run('survivors-restored-test',['ctest','--test-dir',build,'--output-on-failure']) if built==0 else None
out='# SPDX-License-Identifier: Apache-2.0\ncase build_rc test_rc\n'
for row in rows: out+=' '.join(map(str,row))+'\n'
out+=f'restored_bytes={restored} restored_build={built} restored_test={tested}\n'
(packet/'receipts/survivors-summary.log').write_text(out);print(out)
sys.exit(0 if restored and built==tested==0 and all(b==0 and t==(8 if label=='leaveall-wide' else 0) for label,b,t in rows) else 1)
