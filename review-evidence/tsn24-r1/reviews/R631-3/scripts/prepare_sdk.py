#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,shutil,subprocess
ap=argparse.ArgumentParser();ap.add_argument('--packet',type=pathlib.Path,required=True);ap.add_argument('--seed',type=pathlib.Path,required=True,help='Read-only extracted Clang 18.1.3 seed');a=ap.parse_args();p=a.packet.resolve();sdk=p/'scratch/sdk';shutil.copytree(a.seed,sdk,symlinks=True,dirs_exist_ok=True)
urls=[('universe/l/llvm-toolchain-18/','clang-tidy-18_18.1.3-1ubuntu1_amd64.deb'),('universe/l/llvm-toolchain-18/','libclang-rt-18-dev_18.1.3-1ubuntu1_amd64.deb'),('main/g/gcc-13/','libstdc++-13-dev_13.2.0-23ubuntu4_amd64.deb')];rows=[]
for path,name in urls:
 url='https://archive.ubuntu.com/ubuntu/pool/'+path+name;deb=p/'scratch'/name;subprocess.run(['curl','-fsSL',url,'-o',str(deb)],check=True);member=next(x for x in subprocess.check_output(['ar','t',str(deb)],text=True).splitlines() if x.startswith('data.tar'));data=subprocess.check_output(['ar','p',str(deb),member]);flag={'zst':'--zstd','xz':'-J','gz':'-z'}[member.split('.')[-1]];subprocess.run(['tar',flag,'-xf','-','-C',str(sdk)],input=data,check=True);rows.append(dict(package=name,url=url,sha256=hashlib.sha256(deb.read_bytes()).hexdigest()))
(p/'receipts/sdk-packages.json').write_text(json.dumps(rows,indent=2)+'\n')
