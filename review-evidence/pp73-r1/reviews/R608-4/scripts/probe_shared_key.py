# R608-4 probe: a shared_entries key admits a command-owned first entry to
# echo_entries, which then exempts that program's non-SUCCESS answer sizes.
# Usage: python3 -I probe_shared_key.py TREE
import copy
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(TREE / "scripts"))
from aecp_gate.gate import check  # noqa: E402
from aecp_gate.inputs import GateError, Inputs, load  # noqa: E402
from aecp_gate.record import split_group  # noqa: E402


def run(name, fn):
    inp = Inputs(copy.deepcopy(B.table), dict(B.texts), copy.deepcopy(B.ucode),
                 copy.deepcopy(B.record), B.root, dict(B.swept), copy.deepcopy(B.registry))
    try:
        fn(inp)
        got = check(inp)
    except GateError as exc:
        got = [f"  (gate refused: {exc})"]
    print(f"== {name} :: {len(got)} finding(s)")
    for g in got[:6]:
        print(g)


def drift(inp):
    progs = split_group(inp.record, "AEM", 0x0007)
    ans = progs["GCFG"]["answers"]
    print("   GCFG answers before:", ans)
    ans["2"] = "echo"   # NO_SUCH_DESCRIPTOR at the command's own length, not cdl 16


def admit(inp):
    inp.table["shared_entries"]["GCFG"] = "probe"
    inp.table["echo_entries"].append("GCFG")


B = load(TREE)
run("S0 GET_CONFIGURATION NO_SUCH_DESCRIPTOR answered at the echo length", drift)
run("S1 same, with GCFG listed in shared_entries and echo_entries", lambda i: (drift(i), admit(i)))
run("S2 GCFG listed in shared_entries and echo_entries, no drift", admit)
