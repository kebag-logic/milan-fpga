#!/usr/bin/env python3
"""Reviewer-planted merge-sensitive defects, on disposable copies only."""
import argparse,sys,shutil,json
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True);a=ap.parse_args();r=a.root.resolve();p=a.packet.resolve();s=p/'scratch/probes';s.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(r/'sw/firmware/ctrl/test'));import ctrl_build as cb,ctrl_arms as arms,ctrl_mutants as mutants,fw_gtest
b=fw_gtest.Build(jobs=2);rows=[]
checks=[('adp-gptp-port-unprotected','adp/adp.c','port_active = true;\n\ta->ports->gptp','port_active = false;\n\ta->ports->gptp','reentry_release','AllPorts/AdpPortEntry.RefusesBeforeTouchingState/','each port callback is counted'),('adp-stop-port-unprotected','adp/adp.c','port_active = true;\n\ta->ports->timer_stop','port_active = false;\n\ta->ports->timer_stop','reentry_debug','AllPorts/AdpPortEntry.RefusesBeforeTouchingState/','each port callback asserts'),('maap-app-irq-lost','app/ctrl_app.c','mbx_irq_enable(mbx_place(channels,','mbx_irq_enable(mbx_place(1u << MBX_CH_ADP,','maap','MaapHost.AppWaitWakesForMaapWithinBudget','accepted MAAP wakes idle loop'),('maap-interface-one-poll-lost','maap/maap_mbx.c','owed = maap_poll(&m->ifs[k].core) || owed;','owed = maap_poll(&m->ifs[0].core) || owed;','maap_if2','MaapHost.InterfaceOneStallDrainsWithinBudget','interface 1 poll drains deferred output')]
for arm in dict.fromkeys(c[4] for c in checks):
 t=cb.Tree(r/'sw/firmware/ctrl',s/f'baseline-{arm}',s/'reuse',b);o=getattr(arms,'arm_'+arm)(t)
 (p/'receipts'/f'probe-positive-{arm}.log').write_text(o.log);assert o.rc==0,o.log
for name,path,old,new,arm,test,needle in checks:
 copy=s/name/'ctrl';shutil.copytree(r/'sw/firmware/ctrl',copy,ignore=shutil.ignore_patterns('__pycache__'),dirs_exist_ok=True)
 f=copy/path;text=f.read_text();assert text.count(old)==1;f.write_text(text.replace(old,new))
 t=cb.Tree(copy,s/name/'build',s/'reuse',b);o=getattr(arms,'arm_'+arm)(t);caught=mutants.caught(test,needle,o)
 (p/'receipts'/f'probe-{name}.log').write_text(o.log);rows.append(dict(name=name,path=path,old=old,new=new,arm=arm,test=test,needle=needle,rc=o.rc,caught=caught));print(rows[-1],flush=True)
(p/'receipts/probes.json').write_text(json.dumps(rows,indent=2)+'\n');assert all(row['caught'] for row in rows)
