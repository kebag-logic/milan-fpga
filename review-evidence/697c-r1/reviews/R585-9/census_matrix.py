#!/usr/bin/env python3
"""Portable, read-only AST census probes: ROOT is the candidate checkout."""
import argparse
import json
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("root", type=Path)
args = ap.parse_args()
sys.dont_write_bytecode = True
sys.path.insert(0, str(args.root.resolve() / "sw/firmware/ctrl/test"))
import ctrl_pin as p

texts = {f.relative_to(p.ROOT).as_posix(): f.read_text() for f in p.PROOF}
build = next(k for k in texts if k.endswith("ctrl_build.py"))
rows = []
clean = p.census(texts, p.git_env())
rows.append({"case": "clean", "expected": "accepted", "findings": clean, "pass": not clean})
for name, prepare, check, needle in p.census_arms():
    prepare()
    accepted, detail = check()
    rows.append({"case": name, "expected": "named refusal", "accepted": accepted,
                 "detail": detail, "pass": not accepted and needle in detail})

forms = {
    "subprocess import": "import subprocess",
    "subprocess alias": "import subprocess as process",
    "subprocess member alias": "from subprocess import Popen as process",
    "os.system alias": "from os import system as process",
    "os.system attribute": "import os as operating\noperating.system('true')",
    "os.popen": "os.popen('true')",
    "os.execvp": "os.execvp('true', ['true'])",
    "os.spawnv": "os.spawnv(os.P_WAIT, '/bin/true', ['true'])",
    "os.posix_spawn": "os.posix_spawn('/bin/true', ['true'], {})",
    "pty import alias": "import pty as process",
    "pty member alias": "from pty import spawn as process",
    "asyncio module": "import asyncio.subprocess as process",
    "asyncio alias": "from asyncio import create_subprocess_exec as process",
    "asyncio shell attribute": "import asyncio as a\na.create_subprocess_shell('true')",
    "indirect os": "shutil.os.system('true')",
    "eval": "eval('1')",
    "exec": "exec('pass')",
    "compile": "compile('pass', '<probe>', 'exec')",
    "dynamic import": "__import__('os')",
    "importlib": "import importlib as loader",
    "reflection": "getattr(os, 'sys' + 'tem')('true')",
    "wildcard": "from os import *",
    "qualified eval": "import inspect\nVALUE = inspect.builtins.eval('1')",
    "qualified exec": "import inspect\ninspect.builtins.exec('pass')",
    "qualified compile": "import inspect\nVALUE = inspect.builtins.compile('pass', '<probe>', 'exec')",
    "qualified importlib": "import pkgutil\nVALUE = pkgutil.importlib.import_module('os')",
}
for key in texts:
    for name, form in forms.items():
        changed = dict(texts)
        line = texts[key].count('\n') + 1
        changed[key] += form + '\n'
        found = p.census(changed, p.git_env())
        named = any(f.startswith(key + ':') and int(f.split(':')[1].split()[0]) >= line for f in found)
        rows.append({"case": Path(key).name + ': ' + name, "expected": "named refusal",
                     "line": line, "findings": found, "pass": named})

for form in ["eval('1')", "exec('pass')", "compile('pass', '<probe>', 'exec')",
             "__import__('os')", "import importlib"]:
    changed = dict(texts)
    anchor = '    import subprocess\n'
    assert texts[build].count(anchor) == 1
    line = texts[build][:texts[build].index(anchor)].count('\n') + 1
    changed[build] = texts[build].replace(anchor, '    ' + form + '\n' + anchor)
    found = p.census(changed, p.git_env())
    rows.append({"case": 'dynamic code inside helper: ' + form, "expected": "refused module-wide",
                 "line": line, "findings": found,
                 "pass": any(f.startswith(f'{build}:{line} ') for f in found)})

for row in rows:
    print(json.dumps(row, sort_keys=True))
bad = sum(not r['pass'] for r in rows)
print(f"RESULT: {len(rows)} cases, {len(rows)-bad} passed, {bad} escaped")
sys.exit(bool(bad))
