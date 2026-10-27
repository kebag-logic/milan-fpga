"""Write the three consumer-gate specs for one committed parent snapshot, from
the manager template: A = template commands 1-13 and 15 in <clone-a>, B =
template command 14 (milan_dp_gptp) in <clone-b>, C = tsn_fuzz ptp in
<clone-c>. Each clone must be at <head>. usage:
final-specs.py <template> <out-dir> <head> <clone-a> <clone-b> <clone-c>"""
import json
import sys
from pathlib import Path

tpl, out, head, a, b, c = sys.argv[1:7]
spec = json.loads(Path(tpl).read_text())
cmds = spec["commands"]
assert len(cmds) == 15 and cmds[13][-1] == "tb/verilator/milan_dp_gptp", cmds[13]
env = cmds[0][:3]
fuzz = env + ["TSN_GEN_ROOT=<management>/tools/tsn-gen-deca300c",
              "make", "-C", "tb/verilator/tsn_fuzz", "ptp"]
base = "97aab1d0f28bd753a3e11df6278d5cac54f964dd"
for name, cwd, commands in (("final-a", a, cmds[:13] + cmds[14:]),
                            ("final-b", b, [cmds[13]]),
                            ("final-c", c, [fuzz])):
    Path(out, name + ".json").write_text(json.dumps(
        dict(cwd=cwd, head=head, base=base, commands=commands), indent=1) + "\n")
    print(name, len(commands))
