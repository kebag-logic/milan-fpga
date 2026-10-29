"""Write parent consumer specs from the manager template, command for command.

usage: mkparentspec.py <template.json> <out.json> <cwd> <head> <base> <index,...>
The template's PATH entry is replaced by this lane's tool path (the pinned
Verilator 5.050 behind a wrapper that maps "-j 0" to "-j 8"); TMPDIR and
HOME are added; every other argument is the template's own.
"""
import json
import sys
from pathlib import Path

S = "<scratch>"
tpl, out, cwd, head, base, idx = sys.argv[1:7]
commands = json.loads(Path(tpl).read_text())["commands"]
want = [int(i) for i in idx.split(",")]
cmds = []
for i in want:
    c = list(commands[i - 1])
    assert c[0] == "env" and c[1].startswith("PATH=") and c[2].startswith("VERILATOR_ROOT=")
    c[1] = f"PATH={S}/bin:<user-bin>:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin"
    c[3:3] = [f"TMPDIR={S}/tmp", "HOME=<home>"]
    cmds.append(c)
spec = dict(cwd=cwd, head=head, base=base, commands=cmds, index=want)
Path(out).write_text(json.dumps(spec, indent=1) + "\n")
print(out, want)
