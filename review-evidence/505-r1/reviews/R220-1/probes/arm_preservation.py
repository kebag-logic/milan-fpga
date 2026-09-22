"""Compare base vs head mutation-arm populations (labels and expected fragments)."""
import sys, pathlib, importlib.util
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
base = load("/tmp/r220-pristine/base/scripts/ci_events.py", "ce_base")
head = load("/tmp/r220-pristine/head/scripts/ci_events.py", "ce_head")
pb = base.parse_world(base.read_tree(pathlib.Path("/tmp/r220-pristine/base")))
ph = head.parse_world(head.read_tree(pathlib.Path("/tmp/r220-pristine/head")))
ab = {n: w for n, _, w in base._mutations(pb)}
ah = {n: w for n, _, w in head._mutations(ph)}
removed = sorted(set(ab) - set(ah))
added = sorted(set(ah) - set(ab))
changed = sorted(n for n in set(ab) & set(ah) if ab[n] != ah[n])
print("base arms", len(ab), "head arms", len(ah))
print("removed", len(removed), removed[:5])
print("changed expected fragment", len(changed), changed[:5])
print("added", len(added), "all carrier-script-407:", all(a.startswith("carrier-script-407 ") for a in added))
# check-level: every base finding function still present
import inspect
fb = {n for n, o in vars(base).items() if inspect.isfunction(o)}
fh = {n for n, o in vars(head).items() if inspect.isfunction(o)}
print("functions removed:", sorted(fb - fh), "added:", sorted(fh - fb))
# specialized checks unchanged in source?
for fn in ["check_carrier_gate_step", "check_named_carrier_gate_step", "check_scope_step",
           "check_builder_dependencies", "_check_builder_sv2v", "check_docs", "check_elaborate",
           "pinned_step_keys", "normalize_script", "script_difference", "check_env_files",
           "check_key_allowlists", "check_inherited_env", "check_contract_step", "check_rtl_full"]:
    sb, sh = inspect.getsource(getattr(base, fn)), inspect.getsource(getattr(head, fn))
    print(f"  {fn}: {'unchanged' if sb == sh else 'CHANGED'}")
# constants unchanged
for k in ["CANONICAL_DOCS_GATE_SCRIPT","CANONICAL_IMPORTED_GPTP_GATE_SCRIPT","CANONICAL_EM_DASH_GATE_SCRIPT",
          "CANONICAL_WIRE_GATE_SCRIPT","CANONICAL_NO_GIT_GATE_SCRIPT","CANONICAL_ELAB_SCOPE_SCRIPT","SV2V_INSTALL",
          "BUILDER_RUNS","BUILDER_COMMAND","ENV_FILE_WRITERS","RTL_STEP_LISTS","RTL_SIBLING_STEP_LISTS",
          "INHERITED_STEP_ENV","STEP_KEYS","ACT_CI_SELFTEST","CANONICAL_CONTRACT_SCRIPT"]:
    print(f"  {k}: {'unchanged' if getattr(base,k) == getattr(head,k) else 'CHANGED'}")
# carrier lists: identical once the new 'run' records are stripped
def strip(d):
    return {k: tuple({kk: vv for kk, vv in e.items() if kk != "run"} for e in v) for k, v in d.items()}
print("CARRIER_STEP_LISTS identical apart from run records:", strip(head.CARRIER_STEP_LISTS) == base.CARRIER_STEP_LISTS)
rtl_run = [(k, i) for k, v in {**head.RTL_STEP_LISTS, **head.RTL_SIBLING_STEP_LISTS}.items() for i, e in enumerate(v) if "run" in e]
print("RTL entries carrying an inert run record:", rtl_run)
