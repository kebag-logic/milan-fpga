import pathlib,sys,json,subprocess,os,time,concurrent.futures
p=pathlib.Path(__file__).resolve().parent;root=pathlib.Path(sys.argv[1]).resolve();family=sys.argv[2]
plan=json.loads((p/'public'/('round5-'+family+'-steps.json')).read_text())
env=dict(os.environ);env['TMPDIR']=str(p/'scratch');env['CI_IMAGE_SHFMT']=str(p/'scratch/shfmt');env['PYTHONDONTWRITEBYTECODE']='1'
env['PATH']=str(p/'scratch/reference/bin')+':'+env.get('REVIEW_VERILATOR_DIR','')+':'+env['PATH'];env['MAKEFLAGS']='-j16';env['RUNNER_TEMP']=str(p/'scratch');env['GITHUB_WORKSPACE']=str(root)
(p/'gate-logs').mkdir(exist_ok=True)
# Disallow banks and orchestration explicitly excluded by the review assignment.
def run(pair):
 i,row=pair;cmd=row['command'];s=' '.join(cmd);r={'index':i,'job':row['job'],'step':row['step'],'command':cmd}
 if 'act_ci.py' in s or 'test_builder.py' in s or 'install_dir' in s:
  return {**r,'status':'NOT RUN','reason':'Explicit review restriction on orchestration self-test/full builder bank'}
 if any(x in s for x in ('publication_census.py','ctrl_boundary.py','test_ctrl_firmware.py','test_ctrl_nvm.py','fw_coverage.py','fw_rv32_selftest.py')):
  return {**r,'status':'NOT RUN','reason':'Full native bank left to published receipts; unavailable local reference compiler and test libraries'}
 if s.startswith('syn/yosys/run.sh') or 'syn/yosys/' in s:
  return {**r,'status':'NOT RUN','reason':'Full synthesis bank prohibited; host synthesis executable differs from image pin'}
 if 'ci_rv32_sdk.py --destination' in s:
  return {**r,'status':'NOT RUN','reason':'Shared destination installation prohibited; published installer receipt inspected'}
 cmd=[a.replace('${EVIDENCE}',str(p/'scratch')).replace('${GITHUB_WORKSPACE}',str(root)) for a in cmd]
 if cmd[0]=='make':cmd.insert(1,'-j16')
 if cmd[0]=='behave':cmd=['python3','-m','behave',*cmd[1:]]
 logfile=p/'gate-logs'/f'{family}-{i:03}.log';started=time.monotonic()
 with logfile.open('w') as out:
  try:proc=subprocess.run(cmd,cwd=root/row.get('directory','.'),env=env,stdout=out,stderr=subprocess.STDOUT,timeout=540);rc=proc.returncode
  except subprocess.TimeoutExpired:rc=124
  except OSError as e:out.write(str(e));rc=127
 r.update(rc=rc,status='PASS' if rc==0 else 'FAILED',seconds=round(time.monotonic()-started,3),log=str(logfile.relative_to(p)))
 print(family,i,rc,flush=True);return r
# Python gates can mutate shared fixtures; sequential execution per workflow.
results=[]
for pair in enumerate(plan):
 results.append(run(pair));(p/(family+'-gate-results.json')).write_text(json.dumps(results,indent=2)+'\n')
print(family,'completed',len(results),flush=True)
