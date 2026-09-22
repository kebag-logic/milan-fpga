import json,os,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]); output=Path(sys.argv[2]); output.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(root/"scripts"))
import gen_toc as toc, check_em_dash as gate
assert toc.RAW_HTML_TAGS==("pre","script","style","textarea"),toc.RAW_HTML_TAGS
prefixes={f"{name}-{pos}":"<pre>"+("\n" if pos=="later" else "x")+f"</{name}>\n" for name in ("div","title","xmp","style") for pos in ("later","inline")}
heading="## Prior \u2014 topic\n";tail="\n## Alpha\n\nText.\n\n## Beta\n\nText.\n\n## Gamma\n\nText.\n"
gate._fixture_git(root,"init","-q","--initial-branch=main")
bases={}
for name,prefix in prefixes.items():
 text="# Fixture\n\n"+prefix+heading+tail;bases[name]=text
 (root/(name+".md")).write_text(text)
base=gate._commit(root,"synthetic base for review probe")
for name in prefixes:(root/(name+".md")).write_text("# Fixture\n\n"+heading+tail)

def cmd(args,label):
 r=subprocess.run(["rtk","proxy","python3","-B",*args],cwd=root,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1"))
 (output/(label+".log")).write_text(r.stdout+r.stderr)
 return dict(command=["rtk","proxy","python3","-B",*args],rc=r.returncode)
# Use the shipped generator to establish actual head provenance.
w=cmd(["scripts/gen_toc.py","--write",*[n+".md" for n in prefixes]],"generator-write");assert w["rc"]==0
for name in prefixes:
 f=root/(name+".md");f.write_text(f.read_text().replace(toc.TODO,"A preserved topic."))
head=gate._commit(root,"synthetic unwrapped headings for review probe")
check=cmd(["scripts/gen_toc.py","--check",*[n+".md" for n in prefixes]],"generator-check");assert check["rc"]==0
rows=[]
for name,text in bases.items():
 verdict=gate.Verdict(); gate.judge_page(root,base,gate.Change(name+".md",name+".md"),verdict)
 kinds=toc.blocks(text); line=text.split("\n").index(heading.strip())
 rows.append(dict(name=name,base_source=text,base_probe_kind=kinds[line],base_headings=toc.headings(text),findings=verdict.findings,exempt=verdict.exempt,judged=verdict.judged,head_source=(root/(name+".md")).read_text()))
cli=cmd(["scripts/check_em_dash.py","--base",base],"em-dash-cli")
(output/"results.json").write_text(json.dumps(dict(base=base,head=head,raw_html_tags=toc.RAW_HTML_TAGS,rows=rows,generator_write=w,generator_check=check,cli=cli),indent=2)+"\n")
print(json.dumps(dict(variant=root.name,cli_rc=cli["rc"],rows=[dict(name=r["name"],base_kind=r["base_probe_kind"],findings=len(r["findings"]),exempt=r["exempt"]) for r in rows]),indent=2))
