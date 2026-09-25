import json, os, pathlib, shlex, subprocess, sys, time
import yaml
root=pathlib.Path('$LANES/400-403-declaration-truth')
out=pathlib.Path('$MANAGEMENT/2026-09-23/400-403-a323')
work=pathlib.Path('$VALIDATION_STORAGE/400-403-a323-work')
env=os.environ.copy()
env.update(PATH='$WORKSPACE_HOME/litex-milan/venv/bin:'+env['PATH'], PYTHONPATH='$VALIDATION_STORAGE/517-a321-env/lib/python3.14/site-packages:$VALIDATION_TOOLS/md-venv-40cdefe08ebd/lib/python3.14/site-packages:/usr/lib/python3.14/site-packages', PYTHONHASHSEED='0', TMPDIR=str(work), RUNNER_TEMP=str(work), PIP_NO_INDEX='1')
steps=yaml.safe_load((root/'.github/workflows/docs.yml').read_text())['jobs']['docs-check']['steps']
replacements={
 'Build the validated HDL reference': ['python3 scripts/gen_hdl_reference.py --selftest','python3 scripts/gen_hdl_reference.py --output $VALIDATION_STORAGE/400-403-a323-hdl-reference'],
 'Install the python gate dependencies': ['python3 -c "import yaml; print(yaml.__version__)"'],
 'Install the pinned Markdown renderer': ['python3 -c "import importlib.metadata as m; print({n:m.version(n) for n in [\'cmarkgfm\',\'html5lib\',\'cffi\',\'pycparser\',\'six\',\'webencodings\']})"'],
 'Install diagram gate dependencies': ['rsvg-convert --version','python3 -c "import importlib.metadata as m; assert m.version(\'wavedrom\') == \'2.0.3.post3\'; print(m.version(\'wavedrom\'))"'],
 'Added-line em-dash gate': ['python3 scripts/check_em_dash.py --base 220cb5a34507bb79bbf976b031bb55eb05543d6f'],
 'Install the pinned sv2v release': ['sv2v --version'],
 'Install and verify the pinned RV32 SDK': ['python3 scripts/ci_rv32_sdk_selftest.py','python3 scripts/ci_rv32_sdk.py --destination $VALIDATION_STORAGE/504-manager-r1/sdk-install --verify-only'],
 'Compiler-absent firmware controls': ['python3 sw/builder/test_firmware_compiler.py --selftest','python3 sw/builder/test_firmware_compiler.py --absent --audit '+str(out/'rv32-absent.jsonl')],
 'End-station builder gates': ['python3 $VALIDATION_STORAGE/400-403-a323-builder.py sdk'],
 'SoC source-list gate (Vivado would fail 40 min in without this)': ['python3 scripts/check_soc_sources.py','python3 scripts/check_soc_sources.py --selftest','command -v tclsh','python3 sw/litex/iob_pack_selftest.py'],
 'Local act runner contract gate': ['sudo -n docker run --rm --pull never --network none --cap-drop ALL --security-opt no-new-privileges --user '+str(os.getuid())+':'+str(os.getgid())+' --mount type=bind,src='+str(root)+',dst=/candidate,readonly --workdir /candidate catthehacker/ubuntu:full-latest python3 scripts/act_ci.py --selftest'],
}
plan=[]
for i,step in enumerate(steps,1):
 if 'run' not in step:continue
 name=step['name']
 commands=replacements.get(name, [s for s in step['run'].splitlines() if s.strip()])
 for j,cmd in enumerate(commands,1):
  plan.append(dict(id=f'docs-{i:02d}-{j:02d}',step=name,command=cmd,setup_substitution=name in replacements))
(out/'docs-command-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
start=int(sys.argv[1]) if len(sys.argv)>1 else 0
stop=int(sys.argv[2]) if len(sys.argv)>2 else len(plan)
results_path=out/'docs-results.json'
results=json.loads(results_path.read_text()) if results_path.exists() else []
for n,item in enumerate(plan):
 if not start<=n<stop:continue
 label=item['id']; log=out/(label+'.log')
 print('START',n,label,item['command'],flush=True)
 begin=time.time()
 with log.open('w') as f:
  f.write('COMMAND '+item['command']+'\n');f.flush()
  proc=subprocess.run(['bash','-euo','pipefail','-c',item['command']],cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=14400)
 result=dict(item,rc=proc.returncode,seconds=round(time.time()-begin,3),log=log.name)
 results.append(result); results_path.write_text(json.dumps(results,indent=2)+'\n')
 with (out/'HANDOFF.md').open('a') as f:f.write(f"\nGate `{label}`: rc {proc.returncode}; log `{log.name}`.\n")
 print('END',label,'rc',proc.returncode,'seconds',result['seconds'],flush=True)
 if proc.returncode:raise SystemExit(proc.returncode)
