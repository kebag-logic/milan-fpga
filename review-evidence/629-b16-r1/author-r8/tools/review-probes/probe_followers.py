#!/usr/bin/env python3
"""Independent closed-follower probes. Usage: probe_followers.py REPO AUTHOR_PACKET OUTPUT"""
import concurrent.futures, json, subprocess, sys
from pathlib import Path
repo,packet,out=map(lambda s:Path(s).resolve(),sys.argv[1:])
page=repo/"docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
original=page.read_text(); needle="| Attribution | No loss in the network or the DUT | Every stage at the path\u0027s floor."
assert original.count(needle)==1
line=original[:original.index(needle)].count("\n")+1
forms={
 "unchanged":"",
 "plain_furlongs":" CLOCK_DOMAIN 7 furlongs.",
 "code_descriptor_furlongs":" `CLOCK_DOMAIN 7` furlongs.",
 "code_lane_furlongs":" `B16` furlongs.",
 "code_directory_furlongs":" `author-r5/` furlongs.",
 "code_directory_word":" `author-r5/` bananas.",
 "code_directory_ms":" `author-r5/` ms.",
 "code_commit_furlongs":" `5603c353` furlongs.",
 "code_hashfield_furlongs":" `original_sha256` furlongs.",
 "code_packet_furlongs":" `629-b16-a603` furlongs.",
 "code_file_furlongs":" `b9_thdn.py` furlongs.",
 "code_directory_comment":" `author-r5/`<!-- -->furlongs.",
 "code_directory_entity":" `author-r5/`&#32;furlongs.",
 "literal_descriptor_comment":" CLOCK_DOMAIN 7<!-- -->furlongs.",
 "link_identifier_furlongs":" [CLOCK_DOMAIN 7](#b16c-attribution) furlongs.",
 "identifier_bold_unit":" CLOCK_DOMAIN 7 **furlongs**.",
 "identifier_tag_unit":" CLOCK_DOMAIN 7 <span>furlongs</span>.",
 "identifier_word_after_and":" CLOCK_DOMAIN 7 and furlongs.",
 "identifier_adjacent_unlisted":" CLOCK_DOMAIN 7furlongs.",
 "unbound_digit":" The residual was 7 furlongs.",
 "malformed_comment":" CLOCK_DOMAIN 7<!-->furlongs<!-- -->.",
 "html_code_comment":" <code>CLOCK_DOMAIN 7<!-- -->furlongs</code>.",
}
def run(item):
 name,form=item; d=out/"scratch"/"own-followers"/name
 d.mkdir(parents=True,exist_ok=True)
 p=d/page.name;p.write_text(original.replace(needle,needle+form))
 (d/"README.md").write_bytes((page.parent/"README.md").read_bytes())
 args=[sys.executable,"-I",str(packet/"tools/check_b16_figures.py"),str(p),str(packet),str(d/"rows.tsv"),str(d/"cov.tsv"),"--repo",str(repo),"--show","12"]
 result=subprocess.run(args,capture_output=True,text=True,timeout=180)
 (out/"receipts"/f"own-{name}.log").write_text(result.stdout+result.stderr)
 (out/"receipts"/f"own-{name}.rc").write_text(str(result.returncode)+"\n")
 return dict(name=name,insertion=form,line=line,rc=result.returncode,stdout=result.stdout,stderr=result.stderr,
  categories=[s for s in (d/"cov.tsv").read_text().splitlines() if f":{line}\t" in s])
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex: results=list(ex.map(run,forms.items()))
(out/"receipts/own-followers.json").write_text(json.dumps(results,indent=2)+"\n")
for r in results: print(r["name"],r["rc"],r["stdout"].splitlines()[0])
