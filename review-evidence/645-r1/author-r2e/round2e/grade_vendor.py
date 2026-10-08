from pathlib import Path
from collections import Counter
import hashlib,importlib.util,json,re,sys
w=Path(__file__).resolve().parent
root=w/"functional/route"
head="85db353400c6bf3965d279a9f5b5d47e08a0d1ed"
def slack(p):
 lines=p.read_text().splitlines();i=next(i for i,l in enumerate(lines) if "WNS(ns)" in l and "WHS(ns)" in l)
 v=next(l.split() for l in lines[i+1:i+6] if re.match(r"^\s*-?\d+\.\d+",l))
 return dict(WNS_ns=float(v[0]),TNS_ns=float(v[1]),setup_failing_endpoints=int(v[2]),WHS_ns=float(v[4]),THS_ns=float(v[5]),hold_failing_endpoints=int(v[6]),speed_file=next(l.strip() for l in lines if "Speed File" in l))
rows=[]
for directive in ("ExtraPostPlacementOpt","AltSpreadLogic_high","ExtraTimingOpt"):
 gate=w/"timing"/("ax7101" if directive=="ExtraPostPlacementOpt" else "ax7101-"+directive)/"gateware"
 rcfile=w/"logs"/(directive+"-implementation.rc")
 row=dict(directive=directive,process_rc=int(rcfile.read_text()) if rcfile.exists() else None,corners=[])
 iob=gate/"alinx_ax7101_iob_pack.rpt"
 if iob.exists():
  lines=iob.read_text().splitlines();row["iob"]={k:sum(l.startswith(k+" ") for l in lines) for k in ("PASS","FAIL","INERT")}
  row["gmii_rx"]= [l for l in lines if l.startswith("PASS ") and re.search(r"eth0_rx_(?:dv|data\[[0-7]\]):",l)]
 for corner in ("Slow","Fast"):
  for temp in (0,85):
   p=gate/("alinx_ax7101_signoff_"+corner+"_"+str(temp)+"C_timing.rpt")
   if p.exists():row["corners"].append(dict(corner=corner,power_temperature_C=temp,**slack(p)))
 logs=[w/"timing/ax7101/gateware/shipping-synthesis.vendor.log",gate/(directive+"-implementation.vendor.log")]
 warnings=[]
 for p in logs:
  if p.exists():
   warnings += [dict(path=str(p.relative_to(w)),line=i,text=l) for i,l in enumerate(p.read_text(errors="replace").splitlines(),1) if l.startswith("CRITICAL WARNING:")]
 row["critical_warning_codes"]=dict(Counter(re.search(r"\[([^]]+)\]",r["text"])[1] for r in warnings))
 (w/"timing"/(directive+"-critical-warnings.json")).write_text(json.dumps(warnings,indent=2)+"\n")
 row["bitstream_present"]=(gate/"alinx_ax7101.bit").is_file()
 row["manifest_present"]=(gate.parent/"flashboot_layout.json").is_file()
 p=w/"logs"/(directive+"-constraint-check.rc");row["constraints_rc"]=int(p.read_text()) if p.exists() else None
 row["passes_margin"]=bool(row["process_rc"]==0 and row["constraints_rc"]==0 and row["bitstream_present"] and row["manifest_present"] and row.get("iob",{}).get("FAIL",1)==0 and len(row.get("gmii_rx",[]))==9 and len(row["corners"])==4 and all(c["WNS_ns"]>=.030 and c["WHS_ns"]>=0 and c["TNS_ns"]==0 and c["THS_ns"]==0 for c in row["corners"]))
 rows.append(row)
good=[r for r in rows if r["passes_margin"]]
kept=max(good,key=lambda r:min(c["WNS_ns"] for c in r["corners"])) if good else None
summary=dict(head=head,rows=rows,kept=kept["directive"] if kept else None,rc=0 if kept else 1)
(w/"timing-summary.json").write_text(json.dumps(summary,indent=2)+"\n")
(w/"timing-grade.rc").write_text(str(summary["rc"])+"\n")
print(json.dumps(summary,indent=2))
raise SystemExit(summary["rc"])
