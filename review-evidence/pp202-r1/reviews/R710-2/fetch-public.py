#!/usr/bin/env python3
"""Reproduce the selected immutable public evidence downloads; no writes to GitHub."""
import concurrent.futures,json,pathlib,urllib.parse,urllib.request
p=pathlib.Path(__file__).resolve().parent
base='https://raw.githubusercontent.com/kebag-logic/milan-fpga/015d2d6a83eeedc6af5bc3be992b43cf93d2610e/review-evidence/pp202-r1/'
mapping={'public-manifest.json':'MANIFEST.json','public-handoff.md':'author-r3/HANDOFF.md','public-parent.patch':'author-r3/parent-src-stream-id-wiring.patch'}
mapping.update({'public/'+x['path']:'author-r3/'+x['path'] for x in json.loads((p/'selected-receipts.json').read_text())})
def fetch(pair):
    local,remote=pair
    with urllib.request.urlopen(base+urllib.parse.quote(remote,safe='/'),timeout=60) as r: data=r.read()
    f=p/local;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
    return local
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    results=list(ex.map(fetch,mapping.items()))
print('downloaded',len(results),'files; run verify-public.py')
