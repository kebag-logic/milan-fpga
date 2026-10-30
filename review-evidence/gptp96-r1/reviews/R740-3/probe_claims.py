#!/usr/bin/env python3
"""Probe documented gate boundaries in an archived source tree; never edit source."""
import concurrent.futures, hashlib, importlib.util, json, os, pathlib, re, subprocess, sys, tarfile, io
P=pathlib.Path(__file__).resolve().parent
SOURCE=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else pathlib.Path.cwd()
HEAD="411b35fcc56d11c2361d861e7205307587a04a1d"
ROOT=P/"scratch/probe-tree"
ROOT.mkdir(parents=True,exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(["git","-C",str(SOURCE),"archive",HEAD]))) as tf:
    tf.extractall(ROOT,filter="data")
os.environ["TMPDIR"]=str(P/"scratch")
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location("reviewed_checker",ROOT/"scripts/check_docs.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
g=m.load_generator(ROOT)
ct=(ROOT/m.CONSTANTS_PAGE).read_text(); st=(ROOT/m.STATUS_PAGE).read_text(); rom=(ROOT/m.ROM_PAGE).read_text()
results=[]
def record(name,found,expected,needle=None):
    ok=bool(found)==expected and (needle is None or any(needle in s for s in found))
    results.append({"name":name,"expected_reject":expected,"findings":found,"expected_diagnostic":needle,"matches_claim":ok})
record("status-control",m.status_findings(ROOT,st),False)
row=next(s for s in st.splitlines() if "| `README.md`" in s)
for label,body,needle in [
("missing",st.replace(row,""),"no status row for README.md"),
("duplicate",st.replace(row,row+"\n"+row),"duplicate status row: README.md"),
("wrong-current",st.replace(row,row.replace("Current","Historical")),"expected 'Current'"),
("wrong-archive",st.replace("| Historical |","| Current |"),"expected 'Historical'"),
("missing-page",st.replace(row,row.replace("README.md","gone.md")),"status row names a missing page")]:
    record("status-"+label,m.status_findings(ROOT,body),True,needle)
record("constants-control",m.constant_findings(ct,g),False)
record("status-empty",m.status_findings(ROOT,"## Document status\n"),True,"no document status rows")
archive_row=next(s for s in st.splitlines() if "| `docs/history/v1/`" in s)
record("status-no-archive",m.status_findings(ROOT,st.replace(archive_row,"")),True,"no status row for docs/history/v1/")
record("constants-empty",m.constant_findings("## Protocol constants\n",g),True,"no protocol constant rows")
for name in m.CONSTANTS:
    line=next(s for s in ct.splitlines() if s.startswith("| `"+name+"` |"))
    old=line.split("|")[2];new=" "+str(getattr(g,name)+1)+" "
    record("constant-drift-"+name,m.constant_findings(ct.replace(line,line.replace("|"+old+"|","|"+new+"|",1)),g),True,name+" is")
row=next(s for s in ct.splitlines() if s.startswith("| `SYNC_RTO_MS_C` |"))
for label,body,needle in [
("deleted",ct.replace(row,""),"no protocol constant row for SYNC_RTO_MS_C"),
("unnamed",ct.replace(row,row.replace("`SYNC_RTO_MS_C`","SYNC_RTO_MS_C")),"no protocol constant row for SYNC_RTO_MS_C"),
("duplicate",ct.replace(row,row+"\n"+row),"duplicate constant row: SYNC_RTO_MS_C"),
("unknown",ct.replace(row,row.replace("SYNC_RTO_MS_C","ABSENT_C")),"is not a generator constant")]:
    record("constant-"+label,m.constant_findings(body,g),True,needle)
for value in ["**375**","-1","375 ms","3,75"]:
    record("constant-format-"+value,m.constant_findings(ct.replace(row,row.replace("| 375 |","| "+value+" |")),g),True,"not a plain decimal")
copy_cases=[("plain","375 ms",True),("hyphen","375-ms",True),("grouped","300,000 ms",True),("ns","20,000 ns",True),("ppm","200 ppm",True),("seconds","300 s",True),("us","20 us",True),("micro-sign","20 µs",True),("greek-mu","20 μs",True),("minute-digit","5 min",True),("minute-word","five minutes",True),("minute-hyphen","five-minute",True),("decimal-symbol","0.375 s",False),("unit-word","375 milliseconds",False),("no-unit-ordinal","248",False),("no-unit-depth","1,024 words",False),("fenced","```text\n375 ms\n```",False),("decimal-minute","0.5 minutes",False),("decimal-minute-short","1.5 min",False)]
for label,body,expected in copy_cases:
    record("copy-"+label,m.copy_findings({"docs/HDL_DEVELOPER.md":body},ct,g),expected,"restates" if expected else None)
record("copy-home",m.copy_findings({m.CONSTANTS_PAGE:ct.replace("## Integration checklist","375 ms\n\n## Integration checklist")},ct,g),False)
record("copy-after-home",m.copy_findings({m.CONSTANTS_PAGE:ct+"\n## Probe\n375 ms\n"},ct,g),True,"restates")
usage={"Shipping":m.rom_usage(ROOT),"Seeded regression":m.rom_usage(ROOT,"--seq-seed",hex(m.SEEDED_SEQ_SEED))}
record("rom-control",m.rom_findings(rom,usage),False)
for label,old,new,needle in [("shipping-drift","1,022 of 1,024","1,021 of 1,024","Shipping image reads"),("seeded-drift","1,023 of 1,024","1,022 of 1,024","Seeded regression image reads"),("free-drift","| 2 |","| 3 |","Shipping image reads"),("formatted","1,022 of 1,024","**1,022** of 1,024","is not plain"),("missing","| Shipping |","| Ship |","no ROM budget row for the Shipping")]:
    record("rom-"+label,m.rom_findings(rom.replace(old,new),usage),True,needle)
r=next(s for s in rom.splitlines() if s.startswith("| Shipping |"))
record("rom-duplicate",m.rom_findings(rom.replace(r,r+"\n"+r),usage),True,"duplicate ROM budget row")
record("rom-nondecimal",m.rom_findings(rom.replace("1,022 of", "1,02 of"),usage),True,"counts are not plain decimals")
(P/"claim-probes.json").write_text(json.dumps({"head":HEAD,"usage":usage,"probes":results},indent=2)+"\n")
print("Claim probes",len(results),"; contradictions:",[x["name"] for x in results if not x["matches_claim"]])
# Full-target controls and the factual documentation counterexample.
def run(name,cmd,cwd=ROOT):
    cp=subprocess.run(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (P/(name+".log")).write_text(cp.stdout);(P/(name+".rc")).write_text(str(cp.returncode)+"\n")
    return {"name":name,"command":cmd,"rc":cp.returncode}
checks=[run("docs-control",["make","-j16","docs"])]
integration=ROOT/m.CONSTANTS_PAGE; integration_original=integration.read_bytes()
integration.write_text(ct.replace("| Sync interval | 125 ms |", "| Sync interval | 124 ms |"))
checks.append(run("cadence-outside-gate",["make","-j16","docs"]))
integration.write_bytes(integration_original)
victim=ROOT/"docs/HDL_DEVELOPER.md";original=victim.read_bytes()
victim.write_bytes(original+b"\nWait 0.5 minutes.\n")
checks.append(run("decimal-minute-full-gate",["make","-j16","docs"]))
victim.write_bytes(original)
# A passing decimal-symbol control is asserted by the same docs sentence.
victim.write_bytes(original+b"\nWait 0.375 s.\n")
checks.append(run("decimal-symbol-full-gate",["make","-j16","docs"]))
victim.write_bytes(original)
# Silence only the duplicate constants diagnostic. The added arm must detect it.
checker=ROOT/"scripts/check_docs.py";saved=checker.read_text()
needle="findings.append(f\"{CONSTANTS_PAGE}: duplicate constant row: {name}\")"
assert saved.count(needle)==1
checker.write_text(saved.replace(needle,"pass"))
checks.append(run("duplicate-rule-muted",[sys.executable,"scripts/check_docs.py","--selftest"]))
checker.write_text(saved)
checks.append(run("docs-restored",["make","-j16","docs"]))
(P/"full-gate-probes.json").write_text(json.dumps(checks,indent=2)+"\n")
print("Full gates:",[(x["name"],x["rc"]) for x in checks])
assert [x["rc"] for x in checks]==[0,0,2,0,1,0]
assert "restates CEASE_MS_C" in (P/"decimal-minute-full-gate.log").read_text()
assert "duplicate constant row escaped" in (P/"duplicate-rule-muted.log").read_text()
