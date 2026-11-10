"""Each 33-sink plant of tests/mutations.json (acmp-wide-*) built into the 16-sink ACMP test binary (the campaign's
`acmp` arm flags) on a copy of a tsn-c-stack tree: every test passing there shows that only the 33-sink binary
detects the plant. usage: python3 -I wide_plants_at16.py TREE WORK"""
import json, os, shutil, subprocess, sys
from pathlib import Path
tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
g = Path("$TOOLS/gtest-1.14.0")
flags = ["-O0", "-g", "-Wall", "-Wextra", "-Werror", "-DNDEBUG", "-DCTRL_REENTRY_ASSERT"]
for m in json.loads((tree / "tests/mutations.json").read_text()):
    if not m["name"].startswith("acmp-wide-"):
        continue
    d = work / m["name"]
    shutil.rmtree(d, ignore_errors=True)
    for sub in ("src", "include", "tests"):
        shutil.copytree(tree / sub, d / sub)
    target = d / m["path"]
    text = target.read_text()
    assert text.count(m["old"]) == 1, m["name"]
    target.write_text(text.replace(m["old"], m["new"]))
    cmds = [["gcc", "-std=c11", *flags, f"-I{d / 'include'}", "-c", str(d / "src/acmp.c"), "-o", str(d / "acmp.o")],
            ["g++", "-std=c++20", "-O0", "-g", f"-I{d / 'include'}", f"-I{d / 'tests'}", f"-I{g / 'include'}", "-c",
             str(d / "tests/test_acmp.cpp"), "-o", str(d / "t.o")],
            ["g++", "-std=c++20", f"-I{g / 'include'}", "-c", str(d / "tests/main.cpp"), "-o", str(d / "m.o")],
            ["g++", str(d / "acmp.o"), str(d / "t.o"), str(d / "m.o"), str(g / "lib/libgmock.a"), str(g / "lib/libgtest.a"),
             "-lpthread", "-o", str(d / "acmp_tests")]]
    for c in cmds:
        subprocess.run(c, check=True)
    r = subprocess.run([str(d / "acmp_tests")], capture_output=True, text=True)
    summary = [line for line in r.stdout.splitlines() if "PASSED" in line or "FAILED" in line]
    print(f"{m['name']} in the 16-sink acmp_tests: rc={r.returncode} {' | '.join(summary[:3])}")
