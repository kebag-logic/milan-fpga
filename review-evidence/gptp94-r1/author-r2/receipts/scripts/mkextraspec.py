"""Write the parent extras spec: the gPTP suites the companion touches.

usage: mkextraspec.py <out.json> <cwd> <head> <base>
The env prefix is the template's (as mkparentspec.py writes it) plus the
tsn-gen checkout at the parent CI pin.
"""
import json
import sys
from pathlib import Path

S = "<scratch>"
out, cwd, head, base = sys.argv[1:5]
env = ["env", f"PATH={S}/bin:<user-bin>:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
       "VERILATOR_ROOT=<home>/.local/share/containers/storage/overlay/"
       "9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff/usr/share/verilator",
       f"TMPDIR={S}/tmp", "HOME=<home>", f"TSN_GEN_ROOT={S}/ext/tsn-gen"]
cmds = [["make", "-C", "tb/verilator/gptp_plane"], ["make", "-C", "tb/verilator/gptp_txts"],
        ["make", "-C", "tb/verilator/gptp_tables"], ["make", "-C", "tb/verilator/tsn_fuzz", "ptp"],
        ["git", "status", "--porcelain"]]
Path(out).write_text(json.dumps(dict(cwd=cwd, head=head, base=base, commands=[env + c for c in cmds]), indent=1) + "\n")
print(out, len(cmds))
