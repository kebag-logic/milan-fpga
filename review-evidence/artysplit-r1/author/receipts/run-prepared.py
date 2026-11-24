import sys,json,hashlib,subprocess,fcntl
from pathlib import Path
r=Path("$VALIDATION_STORAGE/artysplit-a829/r4")
if sys.argv[1]=="boot":
    # The fixture and boot run sequentially inside this queue slot.
    # Completing the missing transmit cost first avoids waiting for a boot trace.
    subprocess.run([sys.executable,"-B",str(Path(__file__).resolve()),"two"],check=True)
    sys.path.insert(0,str(Path.cwd()/"tb/verilator/ctrl_split_boot"));import run
    d=r/"arty-boot";x=json.loads((d/"prepared.json").read_text())
    boot_lock=(r/'boot-fixture.lock').open('w')
    fcntl.flock(boot_lock,fcntl.LOCK_EX)
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    inputs={str(p):digest(p) for p in [d/'prepared.json',Path(x['executable']),
                                       *sorted((d/'soc/gateware').glob('*.init'))]}
    cache=d/'trace-cache.json'; reuse=False
    if cache.exists():
        prior=json.loads(cache.read_text())
        reuse=(prior.get('inputs')==inputs and run.saved_status(d)==0
               and all((d/name).exists() and digest(d/name)==value
                       for name,value in prior.get('outputs',{}).items())
               and set(prior.get('outputs',{}))=={'sim.log','transcript.txt',run.STATUS})
    if reuse:
        print('Regrading the completed, hash-matched preliminary boot trace',flush=True)
        findings,report=run.grade((d/'sim.log').read_text(),(d/'transcript.txt').read_text(),
                                 x['spec'],d/'baremetal',run.saved_status(d))
    else:
        findings,report=run.point(d,"endstation_arty_split",1,False,model=(Path(x["executable"]),x["spec"]))
        if run.saved_status(d)==0:
            cache.write_text(json.dumps(dict(inputs=inputs,outputs={name:digest(d/name)
                              for name in ('sim.log','transcript.txt',run.STATUS)}),indent=2)+'\n')
    (d/"preliminary-grade.json").write_text(json.dumps(dict(findings=findings,report=report),indent=2)+"\n")
    print("\n".join(report+findings));raise SystemExit(bool(findings))
sys.path.insert(0,str(Path.cwd()/"tb/verilator/ctrl_service_budget"))
# A caller from the owning queue waits here if a separate reserved slot is
# measuring the same fixture. A completed, hash-matched trace is regraded.
fixture_lock=(r/'two-fixture.lock').open('w')
fcntl.flock(fixture_lock,fcntl.LOCK_EX)
import run,build,scenario
out=r/"arm-two";spec=build.reused(out)
assert spec["mutation"]=="arty-measure-two-mrpdus" and spec["cpu_hz"]==80_000_000
g=next(g for g in scenario.srp_groups(scenario.point("arty-1x1",spec)) if g.name=="srp")
g.sys_hz=spec["sys_hz"]
d=out/"results";d.mkdir(exist_ok=True)
log=d/(g.name+'.log');script=d/(g.name+'.txt');saved=d/'results.json'
reuse=False
if saved.exists() and log.exists() and script.exists():
 prior=json.loads(saved.read_text())
 reuse=(not prior.get('refusals') and not prior.get('misses') and not prior.get('share_misses')
        and 'RESULT: PASS' in log.read_text()[-4000:]
        and prior.get('build')==spec['executable_sha256'] and script.read_text()==g.script()
        and prior.get('trace_sha256')==hashlib.sha256(log.read_bytes()).hexdigest())
if not reuse:log=run.run_group(out,d,g,"-")
else:print('Regrading the completed, hash-matched two-MRPDU fixture',flush=True)
results,refusals,misses=run.graded([g],[log],spec,d)
shares=run.share_misses(results)
record=run.summary("arty-1x1",spec["executable_sha256"],results,refusals,misses,shares)
record["trace_sha256"]=hashlib.sha256(log.read_bytes()).hexdigest()
record["measurement_fixture"]="Two-MRPDU admission; not a qualified firmware row"
(d/"results.json").write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps(dict(refusals=refusals,misses=misses,share=shares)))
raise SystemExit(bool(refusals or misses or shares))
