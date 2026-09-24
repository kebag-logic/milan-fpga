import datetime
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tarfile
import time

ROOT = Path("$LANES/387-media-rebase")
OUT = Path(__file__).resolve().parent
HEAD = "e68c1b1ac08c8b1e12a28e281b266d06f881e402"
DEV = "57456af96b3127b9d309a995bbbd35a6113ce52d"
results = []

def run(name, command, cwd=ROOT, env=None):
    log = OUT / (name + ".log")
    print("START " + name + ": " + shlex.join(command), flush=True)
    started = time.monotonic()
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with log.open("w") as stream:
        stream.write("Head: " + HEAD + "\nDirectory: " + str(cwd) + "\nCommand: " + shlex.join(command) + "\n\n")
        stream.flush()
        try:
            proc = subprocess.run(["rtk", "proxy", *command], cwd=cwd, env=env,
                                  stdout=stream, stderr=subprocess.STDOUT, timeout=14400)
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            stream.write("\nTIMEOUT after 14400 seconds\n")
            rc = 124
    result = dict(name=name, command=command, cwd=str(cwd), head=HEAD, rc=rc,
                  elapsed_seconds=round(time.monotonic()-started, 2), started_utc=stamp,
                  log=log.name)
    results.append(result)
    (OUT / "gate-results.json").write_text(json.dumps(results, indent=2) + "\n")
    print("DONE " + name + ": rc=" + str(rc) + " in " + str(result["elapsed_seconds"]) + " s", flush=True)
    lines = log.read_text(errors="replace").splitlines()
    for line in lines[-10:]:
        print(line, flush=True)
    return rc

assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == HEAD
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip()
archive = OUT / "merge-head.tar"
subprocess.run(["rtk", "proxy", "git", "archive", "--format=tar", "--output="+str(archive), HEAD], cwd=ROOT, check=True, timeout=1800)
export = OUT / "no-git-export"
export.mkdir(exist_ok=False)
with tarfile.open(archive) as source:
    source.extractall(export, filter="data")
no_git_env = dict(os.environ, GIT_CEILING_DIRECTORIES=str(OUT))
assert subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=export, env=no_git_env,
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0
run("docs-check", ["python3", "scripts/docs_check.py"])
run("docs-check-no-git", ["python3", "scripts/docs_check.py"], export, no_git_env)
run("feature-status-no-git", ["python3", "scripts/check_feature_status.py"], export, no_git_env)
run("em-dash", ["python3", "scripts/check_em_dash.py", "--base", DEV])
run("doc-style", ["python3", "scripts/check_doc_style.py"])
run("toc", ["python3", "scripts/gen_toc.py", "--check"])
run("doc-paths", ["python3", "scripts/check_doc_paths.py"])
run("module-matrix", ["python3", "docs/traceability/gen_module_matrix.py", "--check"])
run("xvlog", ["python3", "scripts/xvlog_gate.py", "--check"])
run("rtl-source-lists", ["python3", "scripts/check_rtl_source_lists.py"])
run("behave", ["behave", "--no-capture", "-f", "plain"], ROOT / "tests")
run("diff-check", ["git", "diff", "--check"])
run("gmstep", ["make", "-C", "tb/verilator/milan_dp", "gmstep"])
run("tkdiag", ["make", "-C", "tb/verilator/tkdiag"])
run("mmcm-servo", ["make", "-C", "tb/verilator/mmcm_servo"])
print("FINAL " + json.dumps({r["name"]:r["rc"] for r in results}), flush=True)
sys.exit(int(any(r["rc"] != 0 for r in results)))
