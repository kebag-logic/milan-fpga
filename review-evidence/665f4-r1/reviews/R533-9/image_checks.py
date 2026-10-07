#!/usr/bin/env python3
"""Rebuild four size fixtures using a verified SDK and recorded runtime inputs."""
import argparse, concurrent.futures, hashlib, json, os, subprocess, sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--archive',type=Path,required=True);ap.add_argument('--litex-root',type=Path,required=True);a=ap.parse_args()
p=Path(__file__).resolve().parent;repo=a.repo.resolve();work=p/'scratch/images';work.mkdir(exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(p/'scratch'))
def run(name,argv):
    with (p/(name+'.log')).open('w') as log:r=subprocess.run(argv,cwd=repo,stdout=log,stderr=subprocess.STDOUT,env=env,timeout=500)
    (p/(name+'.rc')).write_text(str(r.returncode)+'\n');assert r.returncode==0,name
    print(name,'PASS',flush=True)
run('sdk',[sys.executable,'-B','scripts/ci_rv32_sdk.py','--archive',str(a.archive),'--destination',str(work/'sdk')])
env['MILAN_RV32_CC']=str(work/'sdk/bin/riscv32-buildroot-linux-gnu-gcc')
lite=a.litex_root.resolve()
run('runtime',[sys.executable,'-B','sw/firmware/ctrl/test/ctrl_image_runtime.py','--picolibc',str(lite/'pythondata-software-picolibc/pythondata_software_picolibc/data'),'--compiler-rt',str(lite/'pythondata-software-compiler_rt/pythondata_software_compiler_rt/data'),'--litex-software',str(lite/'litex/litex/soc/software'),'--output',str(work/'runtime')])
def image(pair):
    shape,n=pair;label=f'image-{shape}-if{n}';out=work/label
    run(label,[sys.executable,'-B','sw/firmware/ctrl/test/ctrl_srp_image.py','--config',f'configs/{shape}.yaml','--interfaces',str(n),'--output',str(out),'--libc',str(work/'runtime/libc.a'),'--compiler-runtime',str(work/'runtime/libcompiler_rt.a')])
    return json.loads((out/'size.json').read_text())
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    results=list(ex.map(image,[(s,n) for s in ['endstation_ax7101_1x1_tdm8','endstation_ax7101_8x8'] for n in [1,2]]))
public=json.loads((p/'public/ROUND9-SIZES.json').read_text())['srp_images']
for result in results:
    expected=next(e for e in public if (e['shape'],e['interfaces'])==(result['shape'],result['interfaces']))
    for key in ['sections','static_storage','ram_sections','ram_span']:assert result[key]==expected[key],key
    actual=next(x['sha256'] for x in result['artifacts'] if x['name']=='ctrl_app.elf')
    wanted=next(x['sha256'] for x in expected['artifacts'] if x['name']=='ctrl_app.elf')
    assert actual==wanted
(p/'image-comparison.json').write_text(json.dumps({'all_four_elf_and_sections_match_public':True,'results':results},indent=2)+'\n')
print('All four ELF hashes, sections and static storage match the public head measurements',flush=True)
