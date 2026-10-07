#!/usr/bin/env python3
"""Run the published command campaigns in disposable trees and retain receipts.

Usage: python3 scripts/run_review.py SOURCE PACKET
All child processes are joined before this foreground process returns.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import time

source, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
scratch = packet / "scratch"
receipts = packet / "receipts"
checkout = scratch / "command-source"
prefix = scratch / "dependency-prefix"
for p in (scratch, receipts, packet / "diagrams"):
    p.mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
env["PYTHONDONTWRITEBYTECODE"] = "1"
env["DOC_SCRATCH"] = str(packet)
env["CMAKE_PREFIX_PATH"] = str(prefix)
env["CPATH"] = str(prefix / "include")
env["LIBRARY_PATH"] = str(prefix / "lib")
env["LD_LIBRARY_PATH"] = str(prefix / "lib")
records = []

def clean(text):
    for old, new in sorted([(str(checkout), "<source>"), (str(packet), "<packet>"),
                            (str(source), "<review-checkout>"), (str(Path.home()), "<home>")],
                           key=lambda p: -len(p[0])):
        text = text.replace(old, new)
    return text

def run(name, command, cwd=None, timeout=540):
    start = time.monotonic()
    result = subprocess.run(command, cwd=cwd or checkout, env=env,
                            text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=timeout)
    elapsed = round(time.monotonic() - start, 3)
    (scratch / (name + ".raw.log")).write_text(result.stdout)
    (receipts / (name + ".log")).write_text(clean(result.stdout))
    (receipts / (name + ".rc")).write_text(str(result.returncode) + "\n")
    record = dict(name=name, command=[clean(x) for x in command], rc=result.returncode, seconds=elapsed)
    records.append(record)
    print(json.dumps(record), flush=True)
    return result.returncode

assert run("clone", ["git", "clone", "--shared", "--no-checkout", str(source), str(checkout)], scratch) == 0
assert run("checkout", ["git", "checkout", "--detach", "5f9b9d99e1d94485fc00a1b1539baf2ae861cb65"]) == 0
assert run("origin", ["git", "remote", "set-url", "origin", "https://github.com/kebag-logic/lwSRP.git"]) == 0

def checks():
    for name in ("sentences", "references", "links"):
        command = ["python3", "doc/tools/check_" + name + ".py"]
        if name == "links":
            command.append("--github-auth")
        run("docs-" + name, command)

def graphs():
    run("docs-render-published", ["python3", "doc/tools/render_mermaid.py", "--output", str(packet / "graphs")])

def builds():
    archive = scratch / "dependency.tar.gz"
    assert run("dependency-download", ["curl", "-fL", "--retry", "2", "https://api.github.com/repos/cgreen-devs/cgreen/tarball/1.7.0", "-o", str(archive)]) == 0
    dep = scratch / "dependency-source"
    dep.mkdir()
    with tarfile.open(archive) as tf:
        tf.extractall(dep, filter="data")
    dep = next(dep.iterdir())
    depbuild = scratch / "dependency-build"
    assert run("dependency-configure", ["cmake", "-S", str(dep), "-B", str(depbuild),
               "-DCMAKE_INSTALL_PREFIX=" + str(prefix), "-DCMAKE_INSTALL_LIBDIR=lib", "-DWITH_TESTS=OFF", "-DWITH_EXAMPLES=OFF"]) == 0
    assert run("dependency-build", ["make", "-j16"], depbuild) == 0
    assert run("dependency-install", ["cmake", "--install", str(depbuild)]) == 0
    commands = [
        ("configure", ["cmake", "-S", ".", "-B", "build", "-DCMAKE_BUILD_TYPE=Debug"]),
        ("build", ["cmake", "--build", "build", "--parallel", "2"]),
        ("ctest", ["ctest", "--test-dir", "build", "--output-on-failure"]),
        ("unit", ["./build/unit_tests"]),
        ("scenarios", ["behave"]),
        ("scenario-dry", ["behave", "--dry-run"]),
    ]
    for name, cmd in commands:
        run("published-" + name, cmd)
    text = (checkout / "doc/tester.md").read_text()
    block = text.split("~~~sh\n")[2].split("~~~")[0]
    compile_cmd, execution = block.rsplit("./build/mrp_pdu_tests", 1)
    assert not execution.strip()
    run("published-isolated-compile", ["bash", "-c", compile_cmd])
    run("published-isolated-run", ["./build/mrp_pdu_tests"])

try:
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(f) for f in (checks, graphs, builds)]
        for future in futures:
            future.result()
finally:
    (receipts / "commands.json").write_text(json.dumps(records, indent=2) + "\n")
