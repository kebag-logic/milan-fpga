#!/usr/bin/env python3
"""Usage: pinned-python probe_rendered_comment.py REPO AUTHOR_PACKET OUTPUT.
Reproduce visible measurements swallowed by comment normalisation; no source edits.
"""
import ast, html, importlib.metadata, json, re, subprocess, sys
from pathlib import Path
import cmarkgfm, html5lib
from cmarkgfm.cmark import Options
repo,packet,out=map(lambda s:Path(s).resolve(),sys.argv[1:])
page=repo/"docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"; original=page.read_text()
needle="| Attribution | No loss in the network or the DUT | Every stage at the path\u0027s floor."
assert original.count(needle)==1
line=original[:original.index(needle)].count("\n")+1
forms={"unchanged":"", "plain":" CLOCK_DOMAIN 7 ppm.",
 "ordinary_comment":" CLOCK_DOMAIN 7<!-- -->ppm.",
 "short_comment":" CLOCK_DOMAIN 7<!-->ppm<!-- -->.",
 "short_dash_comment":" CLOCK_DOMAIN 7<!--->ppm<!-- -->.",
 "short_comment_unknown_unit":" CLOCK_DOMAIN 7<!-->furlongs<!-- -->."}
def visible(e):
 return (e.text or "")+"".join((visible(c) if isinstance(c.tag,str) else "")+(c.tail or "") for c in e)
ns={"re":re,"html":html}
module=ast.parse((packet/"tools/check_b16_figures.py").read_text())
selected=[]
for n in module.body:
 if isinstance(n,ast.FunctionDef) and n.name=="normalise":selected.append(n)
 elif isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id in ("ESCAPABLE","ENTITY","BLANK") for x in n.targets):selected.append(n)
exec(compile(ast.Module(body=selected,type_ignores=[]),"normaliser-extract","exec"),ns)
results=[]
for name,form in forms.items():
 d=out/"scratch"/"rendered-comment"/name;d.mkdir(parents=True,exist_ok=True)
 altered=original.replace(needle,needle+form);p=d/page.name;p.write_text(altered)
 (d/"README.md").write_bytes((page.parent/"README.md").read_bytes())
 h=cmarkgfm.github_flavored_markdown_to_html(altered,options=Options.CMARK_OPT_UNSAFE)
 v=visible(html5lib.parseFragment(h)); s=v.find("Every stage at the path\u0027s floor.")
 fragment=cmarkgfm.github_flavored_markdown_to_html(form.strip(),options=Options.CMARK_OPT_UNSAFE)
 result=subprocess.run([sys.executable,"-I",str(packet/"tools/check_b16_figures.py"),str(p),str(packet),str(d/"rows.tsv"),str(d/"cov.tsv"),"--repo",str(repo)],capture_output=True,text=True,timeout=180)
 (out/"receipts"/f"rendered-{name}.log").write_text(result.stdout+result.stderr)
 (out/"receipts"/f"rendered-{name}.rc").write_text(str(result.returncode)+"\n")
 results.append(dict(name=name,source_line=line,insertion=form,rendered_html=fragment,normalised_fragment="".join(ns["normalise"](form,[("page",line)]*len(form))[0]),visible_fragment=visible(html5lib.parseFragment(fragment)),full_page_visible_context=v[s:s+210],rc=result.returncode,stdout=result.stdout,categories=[x for x in (d/"cov.tsv").read_text().splitlines() if f":{line}\t" in x]))
record=dict(versions={n:importlib.metadata.version(n) for n in ("cmarkgfm","html5lib")},checker_sha256=__import__("hashlib").sha256((packet/"tools/check_b16_figures.py").read_bytes()).hexdigest(),results=results)
(out/"receipts/rendered-comment.json").write_text(json.dumps(record,indent=2)+"\n")
assert [r["rc"] for r in results]==[0,1,1,0,0,0]
for r in results:print(r["name"],r["rc"],repr(r["visible_fragment"]))
print("REPRODUCED: three visible unsupported measurements passed")
