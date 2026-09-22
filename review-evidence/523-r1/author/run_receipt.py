#!/usr/bin/env python3
"""Record exact author commands, relevant environment and unfiltered output."""
import datetime, json, os, pathlib, subprocess, sys, time
out = pathlib.Path(__file__).resolve().parent
label, *argv = sys.argv[1:]
assert label and argv
logs = out / "receipts" / label
logs.mkdir(parents=True, exist_ok=False)
env = dict(os.environ)
env["VERIFICATION_TEST_LOGS"] = str(logs / "fixtures")
receipt = dict(argv=argv, cwd=str(pathlib.Path.cwd()),
    environment={k:v for k,v in env.items() if k in
      ("PATH", "PYTHONPATH", "PYTHONHOME", "VERILATOR", "VERILATOR_ROOT", "VERILATOR_JOBS", "MAKEFLAGS",
       "SUITE_TIMEOUT", "SUITE_SWEEP_LOCK", "VERIFICATION_TEST_LOGS")},
    started=datetime.datetime.now(datetime.timezone.utc).isoformat())
for name, args in (("head", ["rev-parse", "HEAD"]), ("tree", ["rev-parse", "HEAD^{tree}"]),
                   ("status", ["status", "--porcelain=v1"]), ("index", ["ls-files", "--stage"])):
    receipt[name] = subprocess.check_output(["git", "--no-optional-locks", *args], text=True)
(logs / "receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
start=time.monotonic()
with (logs / "output.log").open("wb") as stream:
    result=subprocess.run(argv, env=env, stdout=stream, stderr=subprocess.STDOUT, check=False)
receipt.update(exit=result.returncode, elapsed_seconds=time.monotonic()-start,
               ended=datetime.datetime.now(datetime.timezone.utc).isoformat())
(logs / "receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(dict(label=label, exit=result.returncode, elapsed=receipt["elapsed_seconds"], log=str(logs/"output.log"))))
print((logs / "output.log").read_text()[-12000:])
sys.exit(result.returncode)
