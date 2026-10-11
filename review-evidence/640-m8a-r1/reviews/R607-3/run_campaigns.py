#!/usr/bin/env python3
"""Run the permitted aggregate and independent memory probes, retaining raw receipts."""
import argparse, concurrent.futures, hashlib, importlib.util, json, os, pathlib, subprocess
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--python',required=True);ap.add_argument('--sdk',type=pathlib.Path,required=True);ap.add_argument('--verilator',type=pathlib.Path,required=True);a=ap.parse_args()
p=pathlib.Path(__file__).resolve().parent;s=p/'scratch';raw=s/'raw';raw.mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(s),PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0',MILAN_LITEX_PYTHON=a.python,MILAN_RV32_CC=str(a.sdk/'bin/riscv32-linux-gcc'),MAKEFLAGS='-j16',LITEX_SIM_TIMEOUT='900')
env['PATH']=str(a.verilator.parent)+':'+str(pathlib.Path(a.python).parent)+':'+env['PATH']
env['JAVA_TOOL_OPTIONS']=f'-Xmx3g -XX:ActiveProcessorCount=8 -Dsbt.global.base={s}/sbt-global -Dsbt.boot.directory={s}/sbt-boot -Dsbt.ivy.home={s}/ivy -Dcoursier.cache={s}/coursier'
env['COURSIER_CACHE']=str(s/'coursier')
# Keep upstream JVM artifacts in this packet, with an explicit memory/CPU ceiling.
probe=p/'public-evidence/reviews/R607-2'
commands=[('aggregate',['bash','scripts/run_litex_sims.sh',str(s/'sims')]),
 ('elf-loads',[a.python,str(probe/'probe_elf_loads.py'),str(a.repo),str(s/'elf-loads')]),
 ('bus-scoreboard',[a.python,str(probe/'probe_memory_bus.py'),str(a.repo)])]
def run(name,cmd):
 with (raw/f'{name}.log').open('w') as f:
  print('COMMAND',json.dumps(cmd),file=f,flush=True)
  rc=subprocess.run(cmd,cwd=a.repo,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=1100).returncode
 (raw/f'{name}.rc').write_text(str(rc)+'\n');print(name,rc,flush=True);return [name,rc]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(lambda row:run(*row),commands))
# The old reproducer asserts the old defect; rc 1 now is expected and must be read with its refusal/output fields.
results.append(run('load-soc-original',[a.python,str(probe/'probe_load_soc.py'),str(a.repo),str(s/'load-soc-original')]))
(s/'campaigns.json').write_text(json.dumps(results,indent=2)+'\n')
