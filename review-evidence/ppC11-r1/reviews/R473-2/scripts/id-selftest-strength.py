#!/usr/bin/env python3
import pathlib,subprocess,os,sys
p=pathlib.Path(__file__).resolve().parents[1];root=p/'scratch/id-probe';script=root/'scripts/check-ids.py';pristine=script.read_text();os.environ['TMPDIR']=str(p/'scratch')
def run(label,args,want):
 r=subprocess.run(args,cwd=root,capture_output=True,text=True)
 print(label,'rc',r.returncode);print(r.stdout,end='');print(r.stderr,end='');assert r.returncode==want
mutants=[
 ('braces ignore members','yield line, f"{token}-{member}", "id"','yield line, token, "family"'),
 ('line break ignored','f"{token}-{broken.group(1)}" if broken else token','token'),
 ('optional omitted','yield line, f"{token}-{optional.group(1)}", "id"','pass'),
 ('sibling omitted','yield line, f"{token.rsplit(\'-\', 1)[0]}-{sibling.group(1)}", "id"','pass'),
 ('any numeric tail','token.endswith("-1")','token.rsplit("-", 1)[-1].isdigit()'),
 ('docs not scanned','SCAN_DIRS = ("docs", "hdl", "tb")','SCAN_DIRS = ("hdl", "tb")'),
 ('hdl not scanned','SCAN_DIRS = ("docs", "hdl", "tb")','SCAN_DIRS = ("docs", "tb")'),
 ('empty registry accepted','if not rows:','if False:'),
 ('duplicate registry accepted','if name in rows:','if False:'),
]
for label,old,new in mutants:
 assert old in pristine,label;script.write_text(pristine.replace(old,new,1));run(label,[sys.executable,str(script),'--selftest'],1);script.write_text(pristine)
case=root/'tb/reviewer-minus-one.txt';case.write_text('P-REVIEWER-MISSING-1\n')
mutated=pristine.replace('(token.endswith("-1") and token[:-2] in rows)','token.endswith("-1")')
script.write_text(mutated);run('minus-one mutant full make ids',['make','-j16','ids'],0)
script.write_text(pristine);run('original full make ids',['make','-j16','ids'],2)
case.unlink();script.write_text(pristine)
# Show that one required negative plant distinguishes the original from the mutant.
plant='    ({CASE: "P-REVIEWER-MISSING-1"}, ["P-REVIEWER-MISSING-1"]),\n'
for label,body,want in [('original with negative plant',pristine,0),('minus-one mutant with negative plant',mutated,1)]:
 script.write_text(body.replace('SELFTEST_CASES = (\n','SELFTEST_CASES = (\n'+plant,1));run(label,[sys.executable,str(script),'--selftest'],want)
script.write_text(pristine)
run('restored full make ids',['make','-j16','ids'],0)
