#!/usr/bin/env python3
"""Verify the locked archive and execute its revision function at two dates."""
import ast,datetime,hashlib,io,json,os,re,subprocess,sys,tarfile,urllib.request
from pathlib import Path
from unittest.mock import patch
repo=Path(sys.argv[1]);packet=Path(sys.argv[2]);work=packet/"scratch"/"verilator-revision";work.mkdir(parents=True,exist_ok=True)
row=next(r for r in json.loads((repo/"ci/image/sources.lock.json").read_text())["sources"] if r["tool"]=="verilator")
a=work/"source.tar.gz"
if not a.exists():
 with urllib.request.urlopen(row["url"]) as stream:a.write_bytes(stream.read())
assert a.stat().st_size==row["size"] and hashlib.sha256(a.read_bytes()).hexdigest()==row["sha256"]
with tarfile.open(a) as t:
 members=[m for m in t.getmembers() if m.name.endswith("/src/config_rev")]
 assert len(members)==1
 raw=t.extractfile(members[0]).read()
node=next(n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name=="get_rev")
code=compile(ast.Module(body=[node],type_ignores=[]),"locked-archive/src/config_rev","exec")
outputs=[]
for day in (14,15):
 class Clock:
  @staticmethod
  def now(tz):return datetime.datetime(2026,10,day,tzinfo=tz)
 scope={"os":os,"re":re,"datetime":Clock,"timezone":datetime.timezone}
 with patch.dict(os.environ,{},clear=True),patch("os.popen",side_effect=lambda cmd:io.StringIO("")):
  exec(code,scope);outputs.append(scope["get_rev"]())
assert outputs==["vUNKNOWN-built20261014","vUNKNOWN-built20261015"]
print(json.dumps({"source_url":row["url"],"source_sha256":row["sha256"],"function_sha256":hashlib.sha256(raw).hexdigest(),"method":"Exact archive get_rev() function; empty Git output as in source archive; only wall clock changed; no compilation", "revision_outputs":outputs,"same_source_different_embedded_version":True},indent=2))
