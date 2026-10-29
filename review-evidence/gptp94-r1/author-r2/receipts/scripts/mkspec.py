"""Write one gate spec for the recorded-gates runner.

usage: mkspec.py <list> <out.json> <cwd> <head> <base>
<list> is a name in LISTS below. Commands carry the same env prefix.
"""
import json
import sys
from pathlib import Path

S = "<scratch>"
VROOT = ("<home>/.local/share/containers/storage/overlay/"
         "9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/"
         "diff/usr/share/verilator")
ENV = ["env",
       f"PATH={S}/bin:<user-bin>:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
       f"VERILATOR_ROOT={VROOT}",
       f"TMPDIR={S}/tmp",
       "HOME=<home>",
       "VERILATOR_JOBS=8",
       "MAKEFLAGS=-j8"]

REPO_FAST = [
    ["make", "contract"],
    ["make", "-C", "tb/verilator/ucpu"],
    ["make", "-C", "tb/verilator/parser"],
    ["make", "-C", "tb/verilator/engine", "run"],
    ["make", "-C", "tb/verilator/gaskets"],
    ["make", "-C", "tb/tsngen"],
    ["make", "-C", "bench/arty", "test"],
    ["make", "lint"],
    ["make", "docs"],
    ["make", "diagrams-check"],
    ["python3", "syn/ooc/check_ooc_clock.py", "--selftest"],
    ["make", "ooc"],
    ["git", "diff", "--exit-code", "--stat"],
]
REPO_ARM = [
    ["make", "-C", "tb/verilator/engine", "mutants"],
    ["git", "diff", "--exit-code", "--stat"],
]
LISTS = {"repo-fast": REPO_FAST, "repo-arm": REPO_ARM}

name, out, cwd, head, base = sys.argv[1:6]
cmds = LISTS[name]
# make's own -j flag in MAKEFLAGS would parallelise the recipes of the
# repository Makefiles, which run their suites in order; keep it off there
env = [e for e in ENV if not e.startswith("MAKEFLAGS")]
spec = dict(cwd=cwd, head=head, base=base, commands=[env + c for c in cmds])
Path(out).write_text(json.dumps(spec, indent=1) + "\n")
print(out, len(cmds))
