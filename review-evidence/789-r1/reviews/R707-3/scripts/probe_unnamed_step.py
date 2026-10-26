"""Edge probe: fast_tool_emission on an emitted step with neither name nor uses, and on two differing top-level keys
of mixed type. Usage: python3 probe_unnamed_step.py <clone at head>"""
import copy, sys
sys.path.insert(0, sys.argv[1] + "/scripts")
from ci_gate_workflows import ROOT, generate, load_template
from ci_fast_tool_selftest import fast_tool_emission
template = load_template(ROOT, "rtl-fast")
generated = generate("rtl-fast", template)
unnamed = sum(1 for job in generated["jobs"].values() for s in job["steps"] if "name" not in s and "uses" not in s)
print("emitted steps with neither name nor uses at head:", unnamed)
for label, edit in (("unnamed run step added to verilator-lint",
                     lambda w: w["jobs"]["verilator-lint"]["steps"].append({"run": "true\n"})),
                    ("trigger and env both changed",
                     lambda w: (w.__setitem__(True, {"push": None}), w["env"].__setitem__("X", "1")))):
    changed = copy.deepcopy(generated)
    edit(changed)
    try:
        print(label, "->", fast_tool_emission(template, changed))
    except Exception as error:
        print(label, "-> raised", type(error).__name__ + ":", error)
