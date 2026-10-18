#!/usr/bin/env python3
"""Read-only exact-source checks and public receipt-index reproduction."""
import concurrent.futures, hashlib, json, os, re, subprocess, sys
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
S=P/"scratch"; S.mkdir(exist_ok=True)
def call(args,cwd=ROOT):
 return subprocess.run(["rtk","proxy",*args],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
def run_log(name,args,cwd=ROOT):
 r=call(args,cwd); (P/(name+".log")).write_bytes(r.stdout); (P/(name+".rc")).write_text(str(r.returncode)+"\n"); return name,r.returncode
jobs=[("contract",["make","-j16","contract"]),("docs",["make","-j16","docs"])]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 out=dict(ex.map(lambda x:run_log(*x),jobs))
def normalized(ref):
 b=call(["git","show",ref+":hdl/top/KL_gptp_engine.sv"]).stdout.decode()
 b=re.sub(r"/\*.*?\*/","",b,flags=re.S); b=re.sub(r"//[^\n]*","",b)
 m=re.search(r"module\s+KL_gptp_engine(.*?)\);",b,re.S)
 return "\n".join(" ".join(l.split()) for l in m[1].splitlines() if l.strip())+"\n"
refs=["b9ade3a63d1b2292d75eb9b1809647e6439542a0","85373de08a5c35487f260087ac8ceaf7a3789cdc","8f3c376d1e07d2f1417889ae2ac590c71b8cb910","e4869fd0c42889b2ac806587cc5c78afb1c33461"]
ports={r:hashlib.sha256(normalized(r).encode()).hexdigest() for r in refs}
(P/"interface-check.json").write_text(json.dumps({"declaration_sha256":ports,"all_equal":len(set(ports.values()))==1},indent=2)+"\n")
rom=[]
for label,args,mac in [("default",[],0x02a1b2c3d4e5),("custom",["--mac","0x021122334455","--clk-hz","125000000"],0x021122334455),("request-seed",["--clk-hz","2000000","--cease-ms","3000","--seq-seed","0x200000"],0x02a1b2c3d4e5),("sync-seed",["--clk-hz","2000000","--cease-ms","3000","--sync-seq-seed","0x10000"],0x02a1b2c3d4e5)]:
 f=S/(label+".hex"); result=call(["python3","hdl/ucode/gen_gptp_ucode.py",*args,"-o",str(f)])
 words=[int(w,16) for w in f.read_text().split()]; cid=(words[1022]<<32)|words[1023]; expected=((mac>>24)<<40)|(0xfffe<<24)|(mac&0xffffff)
 rom.append({"case":label,"rc":result.returncode,"sha256":hashlib.sha256(f.read_bytes()).hexdigest(),"words":len(words),"cid":hex(cid),"expected":hex(expected),"pass":cid==expected,"generator_summary":result.stdout.decode().splitlines()[0].split(": ",1)[-1]})
tracked=call(["git","ls-files","*gptp_ucode.hex"]).stdout.decode().splitlines()
rom.append({"tracked_images":{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in tracked}})
(P/"rom-check.json").write_text(json.dumps(rom,indent=2)+"\n")
packet=S/"public/author-r2"
name,rc=run_log("published-index-verifier",["python3",str(packet/"receipts/scripts/verify_receipts.py"),str(packet)])
# Independently check only the in-directory table, as the published scope explicitly requires.
body=(packet/"RECEIPTS.md").read_text().split("## Kept in scratch",1)[0]
rows={m[0]:(int(m[1]),m[2]) for m in re.findall(r"^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|",body,re.M)}
files={str(f.relative_to(packet)):f for f in packet.rglob("*") if f.is_file() and f.name!="RECEIPTS.md"}
bad=sorted(set(rows)^set(files))
for f in set(rows)&set(files):
 b=files[f].read_bytes()
 if (len(b),hashlib.sha256(b).hexdigest())!=rows[f]:bad.append(f)
(P/"independent-index-check.json").write_text(json.dumps({"published_files":len(files),"published_rows":len(rows),"mismatches":bad,"supplied_verifier_rc":rc,"scratch_rows_excluded":3},indent=2)+"\n")
(P/"local-checks.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"gates":out,"interfaces_equal":len(set(ports.values()))==1,"rom_cases_pass":all(r.get("pass",True) for r in rom),"index_mismatches":bad,"supplied_verifier_rc":rc},indent=2))
