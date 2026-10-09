#!/usr/bin/env python3
import concurrent.futures,hashlib,io,json,os,pathlib,shutil,subprocess,sys,tarfile
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(sys.argv[2]).resolve(); work=packet/"scratch/prior"; work.mkdir(parents=True,exist_ok=True)
repo=packet/"scratch/public-evidence"; rev="fc3d8ef2f113c6ca8bfdfcc6355d6c82d2747856"
provenance=json.loads((packet/"receipts/prior-provenance.json").read_text())
for name in ("independent_comment_probes.py","needle_ownership_probes.py"):
 rel="R557-4/scripts/"+name; source="review-evidence/697-r1/reviews/"+rel; target=packet/"scripts/prior"/rel
 target.write_bytes(subprocess.check_output(["git","-C",str(repo),"show",rev+":"+source]))
 provenance.append({"file":str(target.relative_to(packet)),"source_commit":rev,"source_path":source,"blob":subprocess.check_output(["git","-C",str(repo),"rev-parse",rev+":"+source],text=True).strip()})
for row in provenance:
 path=packet/row["file"]; row["sha256"]=hashlib.sha256(path.read_bytes()).hexdigest(); row["unchanged"]=subprocess.check_output(["git","hash-object",str(path)],text=True).strip()==row["blob"]
(packet/"receipts/prior-provenance.json").write_text(json.dumps(provenance,indent=2)+"\n")
pristine=work/"pristine"; pristine.mkdir(exist_ok=True)
data=subprocess.check_output(["git","-C",str(root),"archive","HEAD"])
with tarfile.open(fileobj=io.BytesIO(data)) as tar: tar.extractall(pristine,filter="data")
legacy=work/"R557-5"; (legacy/"scripts").mkdir(parents=True,exist_ok=True); (legacy/"receipts").mkdir(exist_ok=True); (legacy/"scratch").mkdir(exist_ok=True)
(legacy/"scratch/clang18").symlink_to(packet/"scratch/dependencies/llvm18",target_is_directory=True)
for name in ("independent_probes.py","preservation_and_probe.py"): shutil.copyfile(packet/"scripts/prior/R557-5/scripts"/name,legacy/"scripts"/name)
adapter=work/"adapter"; adapter.mkdir(exist_ok=True); git=adapter/"git"
git.write_text("#!/usr/bin/env python3\nimport subprocess,sys\na=sys.argv[1:]\nif a==[\"checkout\",\"-q\",\"--detach\",\"60c911b92825a720044e78bed540752c7dd0368e\"]:\n print(\"Review adapter: historical checkout retargeted to exact published head 6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5\",file=sys.stderr)\n a[-1]=\"6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5\"\nsys.exit(subprocess.run([\"/usr/bin/git\",*a]).returncode)\n"); git.chmod(0o755)
py=sys.executable
scripts=packet/"scripts/prior"
commands=[
 ("R556-3-comments",[py,str(scripts/"R556-3/scripts/comment_probes.py"),str(root)]),
 ("R556-3-needles",[py,str(scripts/"R556-3/scripts/needle_probes.py"),str(root)]),
 ("R556-4-comments",[py,str(scripts/"R556-4/scripts/comment_bypass_probe.py"),str(pristine),str(work/"r5564")]),
 ("R556-4-fragments",[py,str(scripts/"R556-4/scripts/needle_default_fragments.py"),str(root)]),
 ("R556-4-specificity",[py,str(scripts/"R556-4/scripts/needle_specificity.py"),str(root),str(packet/"scratch/suites/linux/mutations")]),
 ("R556-5-hidden",[py,str(scripts/"R556-5/probes/hidden_text_probe.py"),str(root),str(work/"r5565-hidden")]),
 ("R556-5-tree",["sh",str(scripts/"R556-5/probes/plant_tree_probe.sh"),str(root),str(work/"r5565-tree")]),
 ("R557-4-full",[py,str(scripts/"R557-4/scripts/full_comment_bypass.py"),"--repo",str(root),"--work",str(work/"r5574-full"),"--output",str(work/"r5574-full.json")]),
 ("R557-4-comments",[py,str(scripts/"R557-4/scripts/independent_comment_probes.py"),"--repo",str(root),"--work",str(work/"r5574-comments")]),
 ("R557-4-ownership",[py,str(scripts/"R557-4/scripts/needle_ownership_probes.py"),"--repo",str(root),"--output",str(work/"r5574-ownership.json")]),
 ("R557-5-controls",[py,str(legacy/"scripts/independent_probes.py"),str(root)]),
 ("R557-5-full",[py,str(legacy/"scripts/preservation_and_probe.py"),str(root)]),
]
out=packet/"receipts/prior"; out.mkdir(exist_ok=True)
def run(item):
 name,argv=item; env=dict(os.environ)
 if name=="R556-5-tree": env["PATH"]=str(adapter)+os.pathsep+env["PATH"]
 with (out/(name+".log")).open("w") as log: result=subprocess.run(argv,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
 (out/(name+".rc")).write_text(str(result.returncode)+"\n"); print(name,result.returncode,flush=True)
 return {"name":name,"rc":result.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: rows=list(pool.map(run,commands))
head=subprocess.check_output(["git","-C",str(work/"r5565-tree/tree"),"rev-parse","HEAD"],text=True).strip()
(packet/"receipts/prior-replay.json").write_text(json.dumps({"results":rows,"plant_tree_effective_head":head,"adapter":"Only the historical hard-coded detached checkout is retargeted. Original published script bytes are unchanged. All probe payloads and gate calls are unchanged."},indent=2)+"\n")
