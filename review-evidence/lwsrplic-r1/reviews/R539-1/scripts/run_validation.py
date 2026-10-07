#!/usr/bin/env python3
"""Run focused validation. Usage: run_validation.py CHECKOUT PACKET [--jobs N]."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tarfile

parser = argparse.ArgumentParser()
parser.add_argument("checkout", type=Path)
parser.add_argument("packet", type=Path)
parser.add_argument("--jobs", type=int, default=16)
parser.add_argument("--host-only", action="store_true")
parser.add_argument("--with-local-dependency", action="store_true")
a = parser.parse_args()
assert 1 <= a.jobs <= 16
repo, packet = a.checkout.resolve(), a.packet.resolve()
scratch = packet / "scratch"
source = scratch / "validation-source"
receipts = packet / "receipts"
raw = scratch / "raw"
for d in (source, receipts, raw):
    d.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PIP_DISABLE_PIP_VERSION_CHECK="1")
head = subprocess.check_output(["rtk", "proxy", "git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
assert head == "375dbe132c6f1498f2f3e714ce5905d34456c9d5"
archive = subprocess.check_output(["rtk", "proxy", "git", "-C", str(repo), "archive", head])
with tarfile.open(fileobj=io.BytesIO(archive)) as t:
    t.extractall(source, filter="data")
results = json.loads((receipts / "validation-index.json").read_text()) if (receipts / "validation-index.json").exists() else {}

def clean(text):
    text = text.replace(str(packet), "$PACKET").replace(str(repo), "$CHECKOUT")
    text = re.sub(r"/(?:home|Users)/[^/\s]+", "$USER_HOME", text)
    return text

def run(name, args, cwd=source, extra=None, timeout=480):
    options = dict(env)
    if extra:
        options.update(extra)
    result = subprocess.run(["rtk", "proxy", *args], cwd=cwd, env=options,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    (raw / (name + ".log")).write_bytes(result.stdout)
    output = result.stdout.decode(errors="replace")
    (receipts / (name + ".log")).write_text(clean(output))
    (receipts / (name + ".rc")).write_text(str(result.returncode) + "\n")
    results[name] = {"command": clean(" ".join(args)), "exit": result.returncode,
                     "raw_sha256": hashlib.sha256(result.stdout).hexdigest(),
                     "path_redacted": clean(output) != output}
    print(name, "exit", result.returncode, flush=True)
    return result.returncode

def host():
    configure = ["cmake", "-S", ".", "-B", "build", "-DCMAKE_BUILD_TYPE=Debug"]
    if a.with_local_dependency:
        configure += ["-DCGREEN_LIB=" + str(scratch / "unit-dependency-build/src/libcgreen.so"), "-DCGREEN_INCLUDE=" + str(scratch / "unit-dependency/include")]
    if run("configure", configure):
        return
    if run("build", ["make", "-C", "build", "-j" + str(a.jobs)]):
        return
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = [pool.submit(run, "ctest", ["ctest", "--test-dir", "build", "-V", "--output-on-failure"]),
                pool.submit(run, "unit-direct", ["./build/unit_tests"]),
                pool.submit(run, "scenarios", ["python3", "-m", "behave"])]
        for j in jobs:
            j.result()
    run("shell-execute", ["bash", "build.sh"])

def docs():
    for name, args in [
        ("local-links", ["python3", "doc/tools/check_links.py", "--local-only"]),
        ("sentences", ["python3", "doc/tools/check_sentences.py"]),
        ("references", ["python3", "doc/tools/check_references.py"]),
        ("reference-self-test", ["python3", "doc/tools/check_references.py", "--self-test"]),
        ("graph-script-help", ["python3", "doc/tools/render_mermaid.py", "--help"]),
    ]:
        run(name, args)

def parsers():
    run("shell-parse", ["bash", "-n", "build.sh"])
    run("scenario-parse", ["python3", "-m", "behave", "--dry-run"])
    code = "from pathlib import Path; fs=sorted(Path('.').rglob('*.py')); [compile(p.read_bytes(), str(p), 'exec') for p in fs if 'build' not in p.parts]; print('Tracked Python syntax: PASS')"
    run("python-parse", ["python3", "-c", code])
    code = "from pathlib import Path; import yaml; p=Path('zephyr/module.yml'); x=yaml.safe_load(p.read_text()); assert x == {'name':'lwsrp','build':{'cmake':'.','kconfig':'Kconfig.zephyr'}}; assert Path(x['build']['kconfig']).is_file(); assert (Path(x['build']['cmake'])/'CMakeLists.txt').is_file(); print('Module YAML parse and referenced paths: PASS')"
    run("module-parse", ["python3", "-c", code])
    deps = scratch / "parser-deps"
    if run("parser-dependency", ["python3", "-m", "pip", "install", "--target", str(deps), "kconfiglib==14.1.0"]):
        return
    code = "import kconfiglib; k=kconfiglib.Kconfig('Kconfig.zephyr'); s=k.syms['LWSRP']; assert s.type==kconfiglib.BOOL; assert s.str_value=='n'; s.set_value('y'); assert s.str_value=='y'; print('Kconfig parse and LWSRP n/y selection: PASS')"
    run("kconfig-parse", ["python3", "-c", code], extra={"PYTHONPATH":str(deps)})

with ThreadPoolExecutor(max_workers=3) as pool:
    for future in ([pool.submit(host)] if a.host_only else [pool.submit(host), pool.submit(docs), pool.submit(parsers)]):
        future.result()
(receipts / "validation-index.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
print("Completed", len(results), "checks; failures:", [k for k, v in results.items() if v["exit"]])
