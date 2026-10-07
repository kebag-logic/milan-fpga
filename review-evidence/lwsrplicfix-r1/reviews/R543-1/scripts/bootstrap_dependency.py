#!/usr/bin/env python3
"""Build the public unit-test dependency into packet scratch only."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
import urllib.request

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("packet", type=Path)
args = p.parse_args()
packet = args.packet.resolve()
scratch = packet / "scratch"
source, build, prefix = [scratch / name for name in ("cgreen-src", "cgreen-build", "cgreen-prefix")]
archive = scratch / "cgreen-1.7.0.tar.gz"
url = "https://api.github.com/repos/cgreen-devs/cgreen/tarball/1.7.0"
if not archive.exists():
    with urllib.request.urlopen(url, timeout=120) as response:
        archive.write_bytes(response.read())
sha = hashlib.sha256(archive.read_bytes()).hexdigest()
with tarfile.open(archive) as tar:
    root = tar.getmembers()[0].name.split("/")[0]
if not source.exists():
    source.mkdir(parents=True)
    subprocess.run(["tar", "-xf", str(archive), "--strip-components=1", "-C", str(source)], check=True)
(packet / "receipts/dependency-provenance.json").write_text(json.dumps(dict(url=url, archive_sha256=sha, archive_root=root, version="1.7.0"), indent=2)+"\n")
commands = [
    ("dependency-configure", ["cmake", "-S", str(source), "-B", str(build), "-G", "Unix Makefiles", "-DCMAKE_BUILD_TYPE=Release", "-DCMAKE_INSTALL_PREFIX=" + str(prefix), "-DCMAKE_INSTALL_LIBDIR=lib", "-DCGREEN_WITH_UNIT_TESTS=OFF", "-DCGREEN_WITH_LIBXML2=OFF"]),
    ("dependency-build", ["make", "-C", str(build), "-j16"]),
    ("dependency-install", ["cmake", "--install", str(build)]),
]
for name, command in commands:
    with (packet / "receipts" / (name + ".log")).open("w") as out:
        out.write("Command: " + json.dumps(command) + "\n")
        out.flush()
        rc = subprocess.run(command, stdout=out, stderr=subprocess.STDOUT, timeout=540).returncode
    (packet / "receipts" / (name + ".rc")).write_text(str(rc)+"\n")
    print(name, "rc=" + str(rc), flush=True)
    if rc:
        raise SystemExit(rc)
