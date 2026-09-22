import json,signal,subprocess,sys,tempfile
from pathlib import Path
sys.path.insert(0,"scripts")
from test_suite_cancellation import fixture,start
from owned_process import OwnedProcesses
from process_test_support import write
failures=[]
with tempfile.TemporaryDirectory() as scratch, OwnedProcesses():
    parent=Path(scratch)
    root,p=fixture(parent,"preflight-stale")
    p.env["PROBE_MODE"]="preflight"
    write(root/"logs/omega.log","OLD COMPLETED RUN\n")
    write(root/"logs/preflight/old.log","OLD PREFLIGHT\n")
    start(p);data=p.ready();p.signal(signal.SIGTERM);code,output=p.finish()
    row=dict(exit=code,stale_suite_log=(root/"logs/omega.log").exists(),stale_preflight_log=(root/"logs/preflight/old.log").exists())
    p.save(row)
    if row["stale_suite_log"] or row["stale_preflight_log"]:failures.append("stale logs survive preflight cancellation")
    root,p=fixture(parent,"relative-output")
    with (p.control/"driver.log").open("wb") as stream:
        p.process=subprocess.Popen(["bash",str(root/"scripts/run_all_suites.sh"),str(Path(root.name)/"logs")],
                                   cwd=parent,env=p.env,start_new_session=True,stdout=stream,stderr=subprocess.STDOUT)
    code,output=p.finish();p.save(dict(exit=code,relative_output=True))
    if code!=0:failures.append("relative outdir fails after prerequisite cd")
print(json.dumps(dict(failures=failures)))
sys.exit(bool(failures))
