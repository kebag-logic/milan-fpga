#!/usr/bin/env python3
import concurrent.futures,hashlib,json,pathlib,subprocess,sys
p=pathlib.Path(sys.argv[1]).resolve();rows=json.loads((p/'receipts/round8-probe-sources.json').read_text())
def fetch(row):
 rev,path=row['source'].split('/blob/',1)[1].split('/',1)
 target=p/'scratch/prior-public'/path.split('/reviews/',1)[1];target.parent.mkdir(parents=True,exist_ok=True)
 data=subprocess.check_output(['gh','api','repos/kebag-logic/milan-fpga/contents/'+path+'?ref='+rev,'-H','Accept: application/vnd.github.raw+json'])
 assert hashlib.sha256(data).hexdigest()==row['sha256'];target.write_bytes(data)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(fetch,rows))
print('Four published round-8 probe scripts verified')
