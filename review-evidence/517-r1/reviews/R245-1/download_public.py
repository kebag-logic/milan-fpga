#!/usr/bin/env python3
import hashlib,json,sys,urllib.request
from pathlib import Path
here=Path(__file__).resolve().parent;dest=Path(sys.argv[1]).resolve()
for manifest in ('public-download-receipts.json','sample-download-receipts.json'):
    for item in json.loads((here/manifest).read_text()):
        data=urllib.request.urlopen(item['url'],timeout=120).read()
        assert hashlib.sha256(data).hexdigest()==item['sha256'],item['path']
        path=dest/'public'/item['path'].removeprefix('review-evidence/517-r1/')
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
print('All requested public bytes verified')
