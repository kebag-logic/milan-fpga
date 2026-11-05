"""Write one gate spec for the recorded-gates runner.

usage: mkspec.py <list> <out.json> <cwd> <head> <base>
<list> is a name in LISTS below. Every command carries the same env prefix:
the pinned Verilator 5.050 behind a wrapper mapping "-j 0" to "-j 8", and
TMPDIR on the scratch disk.
"""
import json
import sys
from pathlib import Path

S = "<scratch>"
HOME = "<home>"
VROOT = (HOME + "/.local/share/containers/storage/overlay/"
         "9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/"
         "diff/usr/share/verilator")
ENV = ["env",
       f"PATH={S}/bin:{HOME}/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
       f"VERILATOR_ROOT={VROOT}",
       f"TMPDIR={S}/tmp",
       f"HOME={HOME}",
       "VERILATOR_JOBS=8"]

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
spec = dict(cwd=cwd, head=head, base=base, commands=[ENV + c for c in LISTS[name]])
Path(out).write_text(json.dumps(spec, indent=1) + "\n")
print(out, len(LISTS[name]))
