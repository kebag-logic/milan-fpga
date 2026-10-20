#!/usr/bin/env python3
"""Reproduce focused campaigns from an exact source archive, with 16 build slots total."""
import concurrent.futures, io, os, pathlib, subprocess, sys, tarfile
repo, packet, verilator = map(pathlib.Path, sys.argv[1:])
repo, packet, verilator = repo.resolve(), packet.resolve(), verilator.resolve()
work = packet / "scratch" / "focused"
work.mkdir(parents=True, exist_ok=True)
source = work / "source"
source.mkdir(exist_ok=True)
head = "75db4b57cff47bb614d14dead084649a4c2aa2a3"
def extract(where, dest):
    data = subprocess.check_output(["git", "-C", str(where), "archive", head if where == repo else "HEAD"])
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(dest, filter="data")
extract(repo, source)
extract(repo / "third_party/verilog-axis", source / "third_party/verilog-axis")
wrapper = work / "verilator"
wrapper.write_text("#!/usr/bin/env python3\nimport os, sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i]=='-j': a[i+1]='8'\nos.execv(" + repr(str(verilator)) + ", [" + repr(str(verilator)) + "] + a)\n")
wrapper.chmod(0o755)
env = os.environ.copy()
env.update(VERILATOR=str(wrapper), TMPDIR=str(work), MAKEFLAGS="-j16", PYTHONUNBUFFERED="1")
def run(name, relative, script):
    with (packet / (name + ".log")).open("w") as log:
        log.write("source " + head + "\ncommand: python3 " + relative + "/" + script + "\n")
        log.flush()
        rc = subprocess.run([sys.executable, script], cwd=source / relative, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    (packet / (name + ".rc")).write_text(str(rc) + "\n")
    print(name, "rc", rc, flush=True)
    return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    futures = [pool.submit(run, "aaf-format-mutants", "tb/verilator/avtp_rxmon", "format_mutants.py"), pool.submit(run, "crf-mutants", "tb/verilator/crf_rx", "mutants.py")]
    codes = [f.result() for f in futures]
raise SystemExit(any(codes))
