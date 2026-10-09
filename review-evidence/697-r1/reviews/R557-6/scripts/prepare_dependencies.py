#!/usr/bin/env python3
import concurrent.futures, gzip, hashlib, json, pathlib, subprocess, sys, urllib.request
packet=pathlib.Path(sys.argv[1]).resolve(); work=packet/"scratch/dependencies"; work.mkdir(parents=True,exist_ok=True)
def fetch(url,path):
 if not path.exists(): urllib.request.urlretrieve(url,path)
 return path
base="https://archive.ubuntu.com/ubuntu/"
index=fetch(base+"dists/noble/main/binary-amd64/Packages.gz",work/"main.gz")
index2=fetch(base+"dists/noble/universe/binary-amd64/Packages.gz",work/"universe.gz")
packages={}
for path in (index,index2):
 for record in gzip.decompress(path.read_bytes()).decode().split("\n\n"):
  d=dict(line.split(": ",1) for line in record.splitlines() if ": " in line and not line.startswith(" "))
  if "Package" in d: packages[d["Package"]]=d
sdk=work/"llvm18"; sdk.mkdir(exist_ok=True)
wanted=["clang-18","libclang-cpp18","libllvm18","libclang1-18","libclang-common-18-dev","libtinfo6","libedit2","libxml2","libffi8","libz3-4","libicu74"]
def download(name):
 d=packages[name]; p=fetch(base+d["Filename"],work/pathlib.Path(d["Filename"]).name)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==d["SHA256"]
 return {"package":name,"version":d["Version"],"sha256":d["SHA256"],"url":base+d["Filename"]},p
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(download,wanted))
for row,p in results:
 members=subprocess.check_output(["ar","t",str(p)],text=True).splitlines(); member=next(x for x in members if x.startswith("data.tar"))
 archive=work/(p.name+".tar"); archive.write_bytes(subprocess.check_output(["ar","p",str(p),member]))
 subprocess.run(["tar","xf",str(archive),"-C",str(sdk)],check=True)
(packet/"receipts/dependencies.json").write_text(json.dumps([r for r,p in results],indent=2)+"\n")
source=work/"googletest"
if not source.exists(): subprocess.run(["git","clone","--quiet","https://github.com/google/googletest.git",str(source)],check=True)
subprocess.run(["git","-C",str(source),"checkout","--detach","f8d7d77c06936315286eb55f8de22cd23c188571"],check=True)
prefix=work/"gtest14"
subprocess.run(["cmake","-S",str(source),"-B",str(work/"gtest-build"),"-DCMAKE_BUILD_TYPE=Release","-DCMAKE_INSTALL_PREFIX="+str(prefix),"-DCMAKE_INSTALL_LIBDIR=lib"],check=True)
subprocess.run(["cmake","--build",str(work/"gtest-build"),"-j16"],check=True)
subprocess.run(["cmake","--install",str(work/"gtest-build")],check=True)
print("Prepared isolated Clang 18 and GoogleTest 1.14.0")
