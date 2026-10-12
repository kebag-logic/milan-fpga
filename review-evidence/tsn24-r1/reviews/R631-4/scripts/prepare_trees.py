#!/usr/bin/env python3
import argparse,io,pathlib,subprocess,tarfile
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);a=p.parse_args()
for rev,name in [("1ba273540abbdf51ea5d235c0a7e81c0bcb5d475","base"),("f13c9c16c2b300d158f980dd7c7f071dcb84df5b","head-export")]:
 dest=a.packet/"scratch"/name
 if dest.exists():raise SystemExit("Refusing to overwrite existing disposable export: "+str(dest))
 dest.mkdir(parents=True)
 raw=subprocess.check_output(["git","-C",str(a.source),"archive",rev])
 with tarfile.open(fileobj=io.BytesIO(raw)) as t:t.extractall(dest,filter="data")
