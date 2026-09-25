import json, os, pathlib, shlex, subprocess, time
root=pathlib.Path('$LANES/400-403-declaration-truth')
out=pathlib.Path('$MANAGEMENT/2026-09-23/400-403-a323')
points=[('8x8',50000000,'on'),('8x8',50000000,'off'),('1x1_tdm8',50000000,'on'),('1x1_tdm8',50000000,'off'),('8x8',100000000,'on'),('8x8',100000000,'off')]
env=os.environ.copy()
env.update(PATH='$VALIDATION_STORAGE/504-manager-r1/sdk-install/bin:$WORKSPACE_HOME/litex-milan/venv/bin:'+env['PATH'], LITEX_ENV_CC_TRIPLE='riscv32-linux', PYTHONHASHSEED='0', COURSIER_MODE='offline', SBT_OPTS='-Dsbt.offline=true')
results=[]
for shape,clock,arm in points:
 label=f'{shape}-{clock//1000000}-{arm}'
 build=pathlib.Path('$VALIDATION_STORAGE/400-403-a323-capture-'+label)
 cmd=['unshare','-Urn','python3','tb/verilator/nvm_capture_cpu/run.py','--shape','endstation_ax7101_'+shape,'--cpu-hz',str(clock),'--captures','16','--traffic',arm,'--build-dir',str(build)]
 log=out/('capture-'+label+'.log')
 print('START',label,flush=True)
 start=time.time()
 with log.open('w') as f:
  f.write('COMMAND '+shlex.join(cmd)+'\n'); f.flush()
  proc=subprocess.run(cmd,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=14400)
 result=dict(label=label,command=shlex.join(cmd),rc=proc.returncode,seconds=time.time()-start,build_dir=str(build),log=log.name)
 if (build/'measurement.json').exists():
  result['measurement']=json.loads((build/'measurement.json').read_text())
  (out/('measurement-'+label+'.json')).write_text(json.dumps(result['measurement'],indent=2)+'\n')
 if (build/'capture.log').exists():
  (out/('rows-'+label+'.log')).write_bytes((build/'capture.log').read_bytes())
 results.append(result)
 (out/'measurement-runs.json').write_text(json.dumps(results,indent=2)+'\n')
 with (out/'HANDOFF.md').open('a') as f:
  f.write(f"\nMeasurement `{label}`: rc {proc.returncode}; log `{log.name}`.\n")
 print('END',label,'rc',proc.returncode,'seconds',round(time.time()-start), 'maximum_ms',result.get('measurement',{}).get('maximum_ms'),flush=True)
 if proc.returncode:
  raise SystemExit(proc.returncode)
