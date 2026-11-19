import concurrent.futures,os,pathlib,subprocess,sys,time
root=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(__file__).resolve().parent
(out / "scratch" / "tmp").mkdir(parents=True, exist_ok=True)
jobs={"harness-selftest":["python3","-B","tb/verilator/ctrl_service_budget/run.py","--self-test"],"flip-1x1":["python3","-B","tb/verilator/ctrl_service_budget/flip_grade.py","--check","--point","1x1/1if"],"flip-8x8":["python3","-B","tb/verilator/ctrl_service_budget/flip_grade.py","--check","--point","8x8/1if"]}
def run(item):
    name,cmd=item; start=time.monotonic()
    with (out/(name+".log")).open("w") as log:
        log.write("Command: "+" ".join(cmd)+"\n");log.flush()
        r=subprocess.run(cmd,cwd=root,env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1","TMPDIR":str(out / "scratch" / "tmp")},stdout=log,stderr=subprocess.STDOUT,timeout=480)
    (out/(name+".rc")).write_text(str(r.returncode)+"\n")
    return name,r.returncode,round(time.monotonic()-start,2)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(run,jobs.items()))
for row in results: print(*row)
sys.exit(any(r[1] for r in results))
