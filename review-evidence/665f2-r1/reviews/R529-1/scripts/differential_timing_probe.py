#!/usr/bin/env python3
"""Probe whether the differential detects a nonconformant probe delay."""
import argparse,json,pathlib,shutil,sys
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);a=p.parse_args();src=a.source.resolve();pkt=a.packet.resolve()
sys.path.insert(0,str(src/"sw/firmware/ctrl/test"))
import maap_differential as md
out=pkt/"scratch"/"differential-timing"; copy=out/"ctrl"
shutil.copytree(md.CTRL,copy,ignore=shutil.ignore_patterns("__pycache__"),dirs_exist_ok=True)
f=copy/"maap/maap.c";original=f.read_text()
old="m->last_delay_ms = base + MAAP_SERVICE_MS + 1u + draw(m, variation - 2u * MAAP_SERVICE_MS - 1u);"
new="m->last_delay_ms = announce ? base + MAAP_SERVICE_MS + 1u + draw(m, variation - 2u * MAAP_SERVICE_MS - 1u) : 1u;"
assert original.count(old)==1;f.write_text(original.replace(old,new))
outcome=md.differential(out/"build",copy)
log=outcome.log.replace(str(src),"<source>").replace(str(pkt),"<packet>")
(pkt/"receipts/differential-timing-escape.log").write_text(log)
record={"mutation":"Set every probe delay to 1 ms; retain announcement delay expression", "differential_rc":outcome.rc, "expected":"differential rejects delay outside strict 500/600 ms", "escaped":outcome.rc==0}
(pkt/"receipts/differential-timing-escape.json").write_text(json.dumps(record,indent=2)+"\n")
print(record)
raise SystemExit(0 if outcome.rc==0 else 1)
