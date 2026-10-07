# SPDX-License-Identifier: Apache-2.0
import argparse,concurrent.futures
from common import *
p=argparse.ArgumentParser();p.add_argument("--jobs",type=int,default=4);a=p.parse_args()
config=SCRATCH/"browser.json";config.write_text(json.dumps({"args":["--no-sandbox"]})+"\n")
commands=[("sentences",["python3","doc/tools/check_sentences.py"]),("references",["python3","doc/tools/check_references.py"]),("reference-self-test",["python3","doc/tools/check_references.py","--self-test"]),("links",["python3","doc/tools/check_links.py","--github-auth"]),("graphs",["python3","doc/tools/render_mermaid.py","--output",SCRATCH/"graphs","--puppeteer-config",config])]
def task(x):return x[0],run(*x,expected=None)[0]
with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs,4)) as ex:
 results=list(ex.map(task,commands))
(PACKET/"receipts/docs-results.json").write_text(json.dumps(results,indent=2)+"\n")
assert all(r==0 for _,r in results),results
