#!/usr/bin/env python3
"""R394-4 negative probes of the arm's two new build checks. Each probe copies the suite
directory beside itself (same depth, so every relative path resolves), applies text edits
(each pattern required exactly once), imports the COPY's mutants.py, optionally overrides a
module constant, and runs the named committed check(s) unchanged. Prints each check's lines.

  python3 r394_neg.py <suite-dir> <probe-name> <check>[,<check>] [file::old::new ...] [CONST=pyexpr ...]
  check: makeflags | break | build_dp
"""
import ast
import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

suite = Path(sys.argv[1]).resolve()
name, checks = sys.argv[2], sys.argv[3].split(",")
copy = suite.parent / f"cc_r394_{name}"
shutil.rmtree(copy, ignore_errors=True)
shutil.copytree(suite, copy, ignore=shutil.ignore_patterns("obj_*", "*.hex"))
for f in ("ltn_rom.hex", "ucode.hex"):
    if (suite / f).is_file():
        shutil.copy2(suite / f, copy / f)
overrides = {}
for spec in sys.argv[4:]:
    if "::" in spec:
        fn, old, new = spec.split("::")
        old, new = old.encode().decode("unicode_escape"), new.encode().decode("unicode_escape")
        p = copy / fn
        t = p.read_text()
        n = t.count(old)
        if n != 1:
            sys.exit(f"edit pattern appears {n} times in {fn}: {old!r}")
        p.write_text(t.replace(old, new))
        print(f"edit {fn}: {old!r} -> {new!r}")
    else:
        k, v = spec.split("=", 1)
        overrides[k] = ast.literal_eval(v)
s = importlib.util.spec_from_file_location("cc_mutants", copy / "mutants.py")
m = importlib.util.module_from_spec(s)
sys.argv = [str(copy / "mutants.py")]
s.loader.exec_module(m)
for k, v in overrides.items():
    print(f"override {k} = {v!r}")
    setattr(m, k, v)
rc = 0
with tempfile.TemporaryDirectory(prefix=f"r394neg-{name}-") as td:
    work = Path(td)
    ok, lines = m.rom_images_result(work)
    for c in checks:
        if c == "makeflags":
            ok, lines = m.makeflags_result(work)
        elif c == "break":
            ok, lines = m.build_break_result(work)
        elif c == "build_dp":
            src = m.stage("dp", work, "plain", m.DATAPATH.read_text())
            exe = m.build("dp", src, work, "plain")
            ok, lines = bool(exe), [f"build('dp') with MAKEFLAGS={m.BUILD_MAKEFLAGS!r} -> {'built' if exe else 'None'}"]
        print(f"== {c}: {'PASS' if ok else 'FAIL'}")
        print("\n".join(lines))
        rc |= 0 if ok else 1
shutil.rmtree(copy)
sys.exit(rc)
