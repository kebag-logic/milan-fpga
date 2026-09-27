"""Build the full enumeration probe using the library build definitions."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
b = Path.home() / "la_avdecc-build"
s = Path.home() / "la_avdecc-src"
p = Path("/tmp/117-a373")
lines = (b / "build.ninja").read_text().splitlines()
flags = next(l.split(" = ", 1)[1].split() for l in lines if "FLAGS =" in l and "ENABLE_AVDECC_FEATURE_CBR" in l and "la_avdecc_controller_static_STATICS" not in l)
defines = [v for v in flags if v.startswith("-D") and "STATICS" not in v]
assert {"-DENABLE_AVDECC_FEATURE_REDUNDANCY", "-DENABLE_AVDECC_FEATURE_JSON", "-DENABLE_AVDECC_FEATURE_CBR"} <= set(defines)
args = ["g++", "-std=c++17", "-O2", "-Wall", *defines, "-I" + str(s / "include"), "-I" + str(s / "externals/3rdparty/json/include"), "-I" + str(Path.home() / "la_avdecc-probe/include"), str(p / "enum_probe.cpp"), "-L" + str(b / "src"), "-L" + str(b / "src/controller"), "-lla_avdecc_controller_cxx", "-lla_avdecc_cxx", "-lpthread", "-Wl,-rpath," + str(b / "src") + ":" + str(b / "src/controller"), "-o", str(p / "enum_probe")]
redact = lambda text: text.replace(str(Path.home()), "$HOME")
print("BUILD_FLAGS " + json.dumps([redact(x) for x in args]), flush=True)
r = subprocess.run(args, capture_output=True, text=True, timeout=45)
print(redact(r.stdout + r.stderr))
if r.returncode:
 sys.exit(r.returncode)
for args in (["git", "-C", str(s), "describe", "--tags", "--always", "--dirty"], ["git", "-C", str(s), "rev-parse", "HEAD"], ["git", "-C", str(s), "status", "--short"], ["g++", "--version"], ["ldd", str(p / "enum_probe")]):
 r = subprocess.run(args, capture_output=True, text=True, timeout=5, check=True)
 print(redact(r.stdout + r.stderr))
for f in (p / "enum_probe.cpp", p / "enum_probe", b / "src/libla_avdecc_cxx.so.4.3.1.1", b / "src/controller/libla_avdecc_controller_cxx.so.4.3.1.1"):
 print(json.dumps({"artifact": f.name, "size": f.stat().st_size, "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}))
