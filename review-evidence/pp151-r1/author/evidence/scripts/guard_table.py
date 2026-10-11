"""Per-guard, per-front-end markdown table from guards.py logs.
usage: guard_table.py <verilator+yosys012 log> <yosys013 log> <xsim+synth log>"""
import re, sys
logs = {"v12": open(sys.argv[1]).read(), "y13": open(sys.argv[2]).read(), "viv": open(sys.argv[3]).read()}
row = {}
order = []
pat = re.compile(r"^(?:FAIL: )?(GUARD|ELAB )\s?(\w+) (\S+) (.*?): (.*)$", re.M)
for key, text in logs.items():
    for kind, fe, name, case, words in pat.findall(text):
        if name not in row:
            row[name] = {}; order.append(name)
        if fe == "yosys" and key == "y13":
            fe = "yosys13"
        row[name][(kind.strip(), fe)] = (case, words)
def vmsg(words):
    m = re.match(r"%Warning-USERFATAL: \S+?:\d+:\d+: (.*)", words)
    return m.group(1) if m else None
def short(fe, words, ref):
    w = re.sub(r"\[/\S+/hdl/", "[hdl/", words)
    if fe == "verilator":
        m = re.match(r"%Warning-USERFATAL: (\S+?):(\d+):\d+: (.*)", w)
        return f"`%Warning-USERFATAL` :{m.group(2)} \"{m.group(3)}\"" if m else w
    if fe in ("yosys", "yosys13"):
        return f"`` {w} ``"
    m = re.match(r"ERROR: \[(VRFC 10-8279|Synth 8-6058)\] (?:\$fatal : |Synth Error: )(.*?)\s+\[(\S+):(\d+)\]$", w)
    if not m:
        return w
    text = "same text" if m.group(2).strip() == (ref or "").strip() else f"\"{m.group(2).strip()}\""
    return f"`[{m.group(1)}]` :{m.group(4)}, {text}"
inv = dict(re.findall(r"^inventory (\S+): (hdl/\S+)$", logs["v12"], re.M))
print("| # | Guard (its task's file:line) | Violating case | Verilator 5.050 lint | sv2v 0.0.12 + Yosys 0.66 | sv2v 0.0.13 + Yosys 0.66 | xelab | synth_design -rtl | Nearest passing case: elaborates in |")
print("|---:|---|---|---|---|---|---|---|---|")
for i, name in enumerate(order, 1):
    r = row[name]
    case = r[("GUARD", "verilator")][0]
    passing = r[("ELAB", "verilator")][0]
    ok = [fe for fe in ("verilator", "yosys", "yosys13", "xsim", "synth") if r.get(("ELAB", fe), ("", ""))[1] == "elaborates"]
    ref = vmsg(r[("GUARD", "verilator")][1])
    cells = [short(fe, r.get(("GUARD", fe), ("", "MISSING"))[1], ref) for fe in ("verilator", "yosys", "yosys13", "xsim", "synth")]
    print(f"| {i} | `{name}` ({inv.get(name, '?')}) | {case} | " + " | ".join(cells) + f" | {passing}: {len(ok)} of 5 |")
