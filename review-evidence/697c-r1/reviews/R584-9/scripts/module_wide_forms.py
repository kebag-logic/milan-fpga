"""R584-9: planted forms appended to the end of each pin-proof module (outside the helper and outside what decides
the pin); each line prints whether the census names a line of the plant. Writes nothing.
Usage: python3 -I module_wide_forms.py <checkout>"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
from ctrl_pin import PROOF, ROOT, census, git_env  # noqa: E402

FORMS = [  # (label, planted text: a line of it the census must name, expected: named | not named)
    ("aliased os, attribute system", "import os as o\nX = o.system", "named"),
    ("from os import posix_spawnp as ps", "from os import posix_spawnp as ps", "named"),
    ("from os import execv", "from os import execv", "named"),
    ("import pty", "import pty", "named"),
    ("import asyncio.subprocess as asp", "import asyncio.subprocess as asp", "named"),
    ("from asyncio import create_subprocess_shell as c", "from asyncio import create_subprocess_shell as c", "named"),
    ("__import__ of a computed module name", "X = __import__('sub' + 'process')", "named"),
    ("import importlib", "import importlib", "named"),
    ("eval of a string", "X = eval('1')", "named"),
    ("compile of a string", "X = compile('1', 'x', 'eval')", "named"),
    ("getattr with a computed name", "X = getattr(os, 'sys' + 'tem')", "named"),
    ("os reached through shutil", "X = shutil.os.spawnl", "named"),
    ("os.fork", "X = os.fork", "named"),
    ("wildcard import", "from os import *", "named"),
    ("dunder attribute", "X = type(os).__dict__", "named"),
    ("import builtins", "import builtins", "named"),
    ("vars() subscript", "X = vars(os)['system']", "named"),
    ("os.popen", "X = os.popen", "named"),
    ("asyncio.create_subprocess_exec attribute", "import asyncio\nX = asyncio.create_subprocess_exec", "named"),
    # outside the listed names: the stated limit "a route of Python's own ... that none of the refused names opens"
    ("multiprocessing (outside the list)", "import multiprocessing", "not named"),
    ("_posixsubprocess.fork_exec (outside the list)", "import _posixsubprocess\nX = _posixsubprocess.fork_exec",
     "not named"),
    ("concurrent.futures.ProcessPoolExecutor (outside the list)",
     "from concurrent.futures import ProcessPoolExecutor", "not named"),
    ("ctypes C library system by subscript (outside the list)", "import ctypes\nX = ctypes.CDLL(None)['system']",
     "not named"),
]
base = {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8") for p in PROOF}
for rel in base:
    for label, plant, expected in FORMS:
        texts = dict(base)
        line = texts[rel].count("\n") + 2
        texts[rel] = texts[rel] + "\n" + plant + "\n"
        lines = {f"{rel}:{n} " for n in range(line, line + plant.count("\n") + 1)}
        found = [f for f in census(texts, git_env()) if any(f.startswith(at) for at in lines)]
        got = "named" if found else "not named"
        print(f"[{'as expected' if got == expected else 'UNEXPECTED'}] {rel.rsplit('/', 1)[1]}: {label}: {got}"
              f"{': ' + found[0] if found else ''}")
