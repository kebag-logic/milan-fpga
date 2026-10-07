#!/usr/bin/env python3
import argparse,contextlib,os,pathlib,sys
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);a=p.parse_args();src=a.source.resolve();pkt=a.packet.resolve()
sys.path.insert(0,str(src/"sw/firmware/ctrl/test"))
import maap_differential as md
raw=pkt/"scratch/differential-controls.raw.log"
with raw.open("w") as f,contextlib.redirect_stdout(f),contextlib.redirect_stderr(f):
 rc=md.sensitivity(pkt/"scratch/differential-controls")
text=raw.read_text().replace(str(src),"<source>").replace(str(pkt),"<packet>").replace(str(pathlib.Path.home()),"<home>")
(pkt/"receipts/differential-controls.log").write_text(text)
(pkt/"receipts/differential-controls.rc").write_text(str(rc)+"\n")
print(text[-2000:]);raise SystemExit(rc)
