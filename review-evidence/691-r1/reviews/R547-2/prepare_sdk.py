#!/usr/bin/env python3
"""Extract the committed SDK pins into scratch, then apply the five-patch series.
Usage: python3 prepare_sdk.py REPO PACKET SDK_CACHE BASE_PYTHON
No source-cache or shared-environment writes are made.
"""
import io, os, pathlib, re, shlex, subprocess, sys, tarfile
repo, packet, cache = map(pathlib.Path, sys.argv[1:4])
base_python = sys.argv[4]
sdk = packet / "scratch/sdk"
sdk.mkdir(parents=True, exist_ok=True)
roots = []
for url in (repo / "sw/litex/litex_pins.txt").read_text().splitlines():
    if not url.startswith("git+"): continue
    match = re.fullmatch(r"git\+https://github.com/[^/]+/([^@]+?)(?:\.git)?@([0-9a-f]{40})", url)
    name, pin = match.groups()
    source, dest = cache / name, sdk / name
    subprocess.run(["git", "-C", str(source), "cat-file", "-e", pin + "^{commit}"], check=True)
    raw = subprocess.check_output(["git", "-C", str(source), "archive", pin], env={**os.environ, "GIT_NO_REPLACE_OBJECTS":"1"})
    dest.mkdir(exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        archive.extractall(dest, filter="data")
    roots.append(str(dest))
    print(name, pin, "extracted committed source", flush=True)
# The package pin intentionally excludes the CPU source; derive its separate pin.
core = (sdk / "litex/litex/soc/cores/cpu/vexiiriscv/core.py").read_text()
match = re.search(r'git_setup\(\s*"VexiiRiscv"\s*,\s*\w+\s*,\s*"([^\"]+)"\s*,\s*"([^\"]+)"\s*,\s*"([0-9a-f]{7,40})"', core)
assert match, "CPU source pin absent"
pin = match.group(3)
rel = pathlib.Path("pythondata_cpu_vexiiriscv/verilog/ext/VexiiRiscv")
source = cache / "pythondata-cpu-vexiiriscv" / rel
dest = sdk / "pythondata-cpu-vexiiriscv" / rel
dest.mkdir(parents=True, exist_ok=True)
raw = subprocess.check_output(["git", "-C", str(source), "archive", pin], env={**os.environ,"GIT_NO_REPLACE_OBJECTS":"1"})
with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
    archive.extractall(dest, filter="data")
print("Derived CPU source", pin, "extracted committed source", flush=True)
wrapper = packet / "scratch/sdk-python"
wrapper.write_text("#!/bin/sh\nexport PYTHONDONTWRITEBYTECODE=1\nexport PYTHONHASHSEED=0\nexport PYTHONPATH=" + shlex.quote(":".join(roots)) + "\nexec " + shlex.quote(base_python) + ' "$@"\n')
wrapper.chmod(0o755)
env = {**os.environ, "PYTHON":str(wrapper), "PYTHONDONTWRITEBYTECODE":"1"}
subprocess.run(["bash", str(repo / "sw/litex/patches/apply.sh")], env=env, check=True)
print("SDK: all pinned inputs freshly extracted; all five patches applied")
