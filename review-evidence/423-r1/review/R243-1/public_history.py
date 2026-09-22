import hashlib, json, os, subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parent
source=Path("$VALIDATION_STORAGE/reviews/r243-423-r1")
sys.path.insert(0,str(source/"scripts")); import check_merge_containment as checker
repo=source/"gptp-processor"; os.chdir(repo)
records=[]
def git(*args):
 r=subprocess.run(["rtk","proxy","git","--no-replace-objects",*args],capture_output=True)
 if r.returncode: raise RuntimeError((args,r.returncode,r.stderr))
 return r.stdout
head="3db86812096830fada2f5f276fa5f4d9f37d1d14"
tips=["f0f1c055ee5226f08e656c27cb1bf4c355be11ae","c1b617435824929a790739ea8585c3fe1a328cc0"]
remote=git("ls-remote","https://github.com/Mister-M-alt/FPGA-gPTP.git","refs/heads/main");(root/"gptp-live-main.raw").write_bytes(remote)
pairs=[("9790ac736e6d10301ad814ffdf73dbe37b59768b","20927af74752620b2ad0f973e8be3203994b5547","d3d164b309e376ea06a3734e8452dd5668c4721d0462dc0656af05d6b3c155b3"),(head,"5602e70bb4cf70c2e0e39e846e26925e27659e32","fa20a2516a4d866a859506c5396779fb98bbafe943e4de2651e9ec252bca996f")]
for a,b,expected in pairs:
 patches=[git("diff","--no-ext-diff","--no-textconv","--no-renames",x+"^",x) for x in (a,b)]
 for x,data in zip((a,b),patches):(root/(x+".patch")).write_bytes(data)
 assert patches[0]==patches[1] and hashlib.sha256(patches[0]).hexdigest()==expected
 names=git("diff-tree","--no-commit-id","--name-only","--no-renames","-z","-r",a).split(b"\0")[:-1]
 entries=[]
 for name in names:
  values=[git("--literal-pathspecs","ls-tree","-z",x,"--",os.fsdecode(name)) for x in (a,b)]
  assert values[0]==values[1];entries.append(dict(path=os.fsdecode(name),entry=values[0].decode("utf8","surrogateescape")))
 assert checker._same_patch_postimage(a,b)==(True,None)
 records.append(dict(kind="historical-pair",source=a,replay=b,patch_sha256=expected,postimages=entries))
for tip in tips:
 rows=git("rev-list","--parents",tip+".."+head).decode().splitlines()
 merges=[r.split() for r in rows if len(r.split())>2];assert len(merges)==1
 merge,first,second=merges[0];assert len(merges[0])==3
 assert git("rev-list","--parents","--max-count=1",second).decode().split()==[second,first]
 assert git("rev-parse",merge+"^{tree}")==git("rev-parse",second+"^{tree}")
 assert checker._linear_patches_contained(head,tip)==(True,None)
 calls=[]; real=checker._git
 def tracked(*args):
  rc,out=real(*args);calls.append(dict(args=args,rc=rc,stdout=out));return rc,out
 checker._git=tracked
 try: result=checker.contained(head,tip)
 finally: checker._git=real
 assert result[0] is None and all(p in result[2] for p in ["tb/tsngen/mutants.py","tb/verilator/gaskets/mutants.py"])
 cli=subprocess.run(["rtk","proxy",sys.executable,"-B",str(source/"scripts/check_merge_containment.py"),"--no-fetch","--base",tip,head],capture_output=True)
 assert cli.returncode==1 and b"UNKNOWN" in cli.stdout
 (root/("gptp-"+tip+".stdout")).write_bytes(cli.stdout);(root/("gptp-"+tip+".stderr")).write_bytes(cli.stderr)
 mb=git("merge-base","--all",head,tip).decode().split();assert len(mb)==1
 names=git("diff","--no-ext-diff","--no-textconv","--no-renames","--name-only","-z",mb[0],head).split(b"\0")[:-1]
 entries=[]
 for name in names:
  vals=[git("--literal-pathspecs","ls-tree","-z",x,"--",os.fsdecode(name)) for x in (mb[0],tip,head)]
  entries.append(dict(path=os.fsdecode(name),ancestor=vals[0].decode(),tip=vals[1].decode(),branch=vals[2].decode()))
 records.append(dict(kind="real-tip",head=head,tip=tip,rows=rows,merge_base=mb,entries=entries,result=result,cli_exit=cli.returncode,calls=calls))
print(json.dumps(records,indent=2));(root/"public-history-data.json").write_text(json.dumps(records,indent=2)+"\n")
