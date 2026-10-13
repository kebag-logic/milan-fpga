import csv,hashlib,json,re,subprocess,sys
from pathlib import Path
repo,packet=map(lambda s:Path(s).resolve(),sys.argv[1:3]);sys.path.insert(0,str(repo/"sw/firmware/ctrl/test"))
import ctrl_mutants
public=packet/"receipts/public-author";old="405dc68310a18f669049ffc10cc23eef7300dcff";target="70936b77dc41981e192438388cd0aced69954f18"
def git(*args):return subprocess.check_output(["git","-C",str(repo/"third_party/tsn-c-stack"),*args]).decode().strip()
proof=json.loads((public/"pin-proof.json").read_text())
files=git("diff","--name-only",old,target).splitlines()
allowed=set().union(*(set(p["files"]) for p in proof["prs"] if p["number"] in (19,20,25)))
assert set(files)<=allowed
assert git("rev-parse",target+"^{tree}")==git("rev-parse","f13c9c16^{tree}")
pre=git("diff","--name-only",old,"1ba27354","--","src","include").splitlines();assert pre==["src/adp.c"]
assert git("rev-parse","1ba27354^{tree}")==git("rev-parse","3c9ca52f^{tree}")
rows=list(csv.DictReader((public/"round2/mutations-control.csv").open()))
live={m.name for m in ctrl_mutants.MUTANTS};reported={r["name"] for r in rows};assert live==reported and len(rows)==len(live)==520
assert all(r["result"]=="CAUGHT" for r in rows)
log_names=[]
for n in range(1,5):
 receipt=json.loads((public/f"round2/evidence/control-{n}.json").read_text());assert receipt["rc"]==0
 log=(public/f"round2/evidence/control-{n}.log").read_text()
 assert "ESCAPED" not in log
 log_names += re.findall(r"^\[ok\] mutant ([^ ]+)",log,re.M)
assert len(log_names)==len(live) and set(log_names)==live
state=json.loads((public/"round2/final-state.json").read_text())
for f in state["changed_files"]: assert hashlib.sha256((repo/f["path"]).read_bytes()).hexdigest()==f["sha256"],f["path"]
images=json.loads((public/"round2/image-hashes.json").read_text())
result={"stack_old":old,"stack_target":target,"changed_paths":files,"all_paths_in_authorized_PR_file_sets":True,"pre_F3b_production_delta":pre,"target_tree_equals_reviewed_PR25_head":True,"PR23_tree_equals_reviewed_integration_head":True,"parent_control_table":len(live),"distinct_CAUGHT_names_in_sliced_logs":len(log_names),"source_evidence_hashes_match_head":len(state["changed_files"]),"image_table_rows":len(images),"independent_rebuild_of_images":False}
(packet/"receipts/evidence-audit.json").write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2))
