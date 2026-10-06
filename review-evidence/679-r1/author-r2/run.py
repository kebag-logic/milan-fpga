import os, signal, subprocess, sys, time
from pathlib import Path
root = Path(__file__).resolve().parent
label, *argv = sys.argv[1:]
env = dict(os.environ, TMPDIR=str(root), PYTHONDONTWRITEBYTECODE="1", PYTHONUNBUFFERED="1", PYTHON_CPU_COUNT="4", VERILATOR_JOBS="2", MAKEFLAGS="-j8")
start=time.monotonic()
with (root/(label+".log")).open("w") as log:
    process=subprocess.Popen(argv,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
    try:
        rc=process.wait(timeout=580)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid,signal.SIGTERM)
        process.wait(timeout=10)
        rc=124
        log.write("\nForeground time limit reached; process group terminated.\n")
(root/(label+".rc")).write_text(str(rc)+"\n")
print(label,"rc",rc,"seconds",round(time.monotonic()-start,1))
print((root/(label+".log")).read_text()[-5000:])
raise SystemExit(rc)
