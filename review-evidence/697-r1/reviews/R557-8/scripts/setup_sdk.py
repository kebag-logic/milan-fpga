#!/usr/bin/env python3
import concurrent.futures, hashlib, json, pathlib, subprocess, sys, urllib.request
packet=pathlib.Path(sys.argv[1]).resolve()
work=packet/"scratch/sdk"
work.mkdir(parents=True,exist_ok=True)
urls=[
"https://archive.ubuntu.com/ubuntu/pool/main/libe/libedit/libedit2_3.1-20230828-1build1_amd64.deb",
"https://archive.ubuntu.com/ubuntu/pool/main/n/ncurses/libtinfo6_6.4+20240113-1ubuntu2_amd64.deb",
"https://archive.ubuntu.com/ubuntu/pool/universe/l/llvm-toolchain-18/clang-18_18.1.3-1ubuntu1_amd64.deb",
"https://archive.ubuntu.com/ubuntu/pool/universe/l/llvm-toolchain-18/libclang-common-18-dev_18.1.3-1ubuntu1_amd64.deb",
"https://archive.ubuntu.com/ubuntu/pool/main/l/llvm-toolchain-18/libclang-cpp18_18.1.3-1ubuntu1_amd64.deb",
"https://archive.ubuntu.com/ubuntu/pool/main/l/llvm-toolchain-18/libllvm18_18.1.3-1ubuntu1_amd64.deb",
"https://archive.ubuntu.com/ubuntu/pool/main/libx/libxml2/libxml2_2.9.14+dfsg-1.3ubuntu3_amd64.deb",
"https://archive.ubuntu.com/ubuntu/pool/main/i/icu/libicu74_74.2-1ubuntu3_amd64.deb",
"https://codeload.github.com/google/googletest/tar.gz/f8d7d77c06936315286eb55f8de22cd23c188571"]
def fetch(url):
 path=work/url.rsplit("/",1)[1]
 if not path.exists(): urllib.request.urlretrieve(url,path)
 return {"url":url,"file":path.name,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(fetch,urls))
root=work/"root";root.mkdir(exist_ok=True)
for row in rows:
 path=work/row["file"]
 if path.suffix==".deb":
  members=subprocess.check_output(["ar","t",str(path)],text=True).splitlines()
  member=next(x for x in members if x.startswith("data.tar"))
  data=subprocess.check_output(["ar","p",str(path),member])
  subprocess.run(["bsdtar","-xf","-","-C",str(root)],input=data,check=True)
 else:subprocess.run(["tar","-xf",str(path),"-C",str(work)],check=True)
(packet/"receipts/sdk-downloads.json").write_text(json.dumps(rows,indent=2)+"\n")
gtest=work/"googletest-f8d7d77c06936315286eb55f8de22cd23c188571"
subprocess.run(["cmake","-S",str(gtest),"-B",str(work/"gtest-build"),"-DCMAKE_BUILD_TYPE=Release","-DCMAKE_INSTALL_PREFIX="+str(work/"gtest"),"-DCMAKE_INSTALL_LIBDIR=lib"],check=True)
subprocess.run(["cmake","--build",str(work/"gtest-build"),"-j16"],check=True)
subprocess.run(["cmake","--install",str(work/"gtest-build")],check=True)
print("Scoped dependency preparation complete")
