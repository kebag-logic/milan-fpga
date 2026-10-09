#!/usr/bin/env python3
"""Retrieve only published executable scripts listed by immutable source URL."""
import concurrent.futures,json,pathlib,subprocess,sys
packet=pathlib.Path(sys.argv[1]).resolve();rows=json.loads((packet/"receipts/prior-script-sources.json").read_text())
def fetch(row):
 tail=row["source"].split("/blob/",1)[1];rev,path=tail.split("/",1)
 target=packet/"scratch/prior-public"/path.split("/reviews/",1)[1];target.parent.mkdir(parents=True,exist_ok=True)
 data=subprocess.check_output(["gh","api","repos/kebag-logic/milan-fpga/contents/"+path+"?ref="+rev,"-H","Accept: application/vnd.github.raw+json"])
 target.write_bytes(data)
 assert subprocess.check_output(["git","hash-object",str(target)],text=True).strip()==row["blob"]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(fetch,rows))
print(len(rows),"published script blobs verified")
