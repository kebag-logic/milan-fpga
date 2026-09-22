"""P10: CARRIER_STEP_LISTS at HEAD minus the new `run` records equals BASE's;
RTL_STEP_LISTS / RTL_SEQUENCE_PINS / RTL_SIBLING_STEP_LISTS and every
canonical specialized script equal BASE; every carrier `run` entry at HEAD
records a non-empty tuple of strings and no `uses` entry records `run`."""
import copy, json, sys
from common import BASE, HEAD, load_module
b, h = load_module(BASE, "b10"), load_module(HEAD, "h10")
strip = copy.deepcopy(h.CARRIER_STEP_LISTS)
for spec in strip.values():
    for e in spec:
        e.pop("run", None)
out = {"carrier_lists_minus_run_equal_base": strip == b.CARRIER_STEP_LISTS}
for name in ("RTL_STEP_LISTS", "RTL_SEQUENCE_PINS", "RTL_SIBLING_STEP_LISTS", "ENV_FILE_WRITERS",
             "SV2V_INSTALL", "BUILDER_RUNS", "BUILDER_COMMAND", "CANONICAL_DOCS_GATE_SCRIPT",
             "CANONICAL_EM_DASH_GATE_SCRIPT", "CANONICAL_IMPORTED_GPTP_GATE_SCRIPT",
             "CANONICAL_WIRE_GATE_SCRIPT", "CANONICAL_NO_GIT_GATE_SCRIPT",
             "CANONICAL_ELAB_SCOPE_SCRIPT", "CANONICAL_CONTRACT_SCRIPT", "ACT_CI_SELFTEST"):
    out[f"{name}_equal_base"] = (getattr(h, name, "absent") == getattr(b, name, "absent"))
runs = uses_with_run = 0
bad = []
for (path, jid), spec in h.CARRIER_STEP_LISTS.items():
    for n, e in enumerate(spec, 1):
        if "uses" in e:
            uses_with_run += "run" in e
            continue
        runs += 1
        r = e.get("run")
        if not (isinstance(r, tuple) and r and all(isinstance(x, str) for x in r)):
            bad.append(f"{jid} step {n}")
out.update({"run_entries": runs, "run_entries_malformed": bad, "uses_entries_with_run": uses_with_run})
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(json.dumps(out, indent=1))
sys.exit(0 if all(v is True for k, v in out.items() if k.endswith("_equal_base")) and not bad and not uses_with_run else 1)
