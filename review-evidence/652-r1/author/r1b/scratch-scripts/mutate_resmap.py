"""Plant one defect per arm into an in-memory copy of a resmap module; its self-test must go red."""
import contextlib, io, sys, types
from pathlib import Path
REPO = Path("$LANES/652-builder-names")
sys.path.insert(0, str(REPO / "syn/resmap"))
sys.path.insert(0, str(REPO / "syn/ooc"))
MUTANTS = [
 ("yosys_sweep", "a traceback read as a refusal",
  ' and not any(line.startswith("Traceback") for line in lines)', ""),
 ("yosys_sweep", "any exit with one refusal line read as a refusal",
  "if rc == 1 and len(refusals) == 1", "if len(refusals) == 1"),
 ("yosys_sweep", "a variant with no outcome taken as built",
  '        raise PlanError(f"{point[\'name\']}: shape {shape} has no builder outcome; run the shapes command first")',
  '        return ""'),
 ("yosys_sweep", "run prices a builder-refused point",
  "        if line:\n            print(f\"point {point['name']}: not priced",
  "        if False:\n            print(f\"point {point['name']}: not priced"),
 ("yosys_sweep", "summary ignores a receipt for a refused point",
  'if line and (directory / "receipt.json").is_file():', "if False:"),
 ("yosys_sweep", "summary drops the builder record",
  '            summary[point["name"]] = {"builder": {"refusal": line}}\n', ""),
 ("yosys_sweep", "the plan accepts any expectation",
  'if spec.get("expect", "built") not in ("built", "refused"):', "if False:"),
 ("resmap_models", "a builder refusal not read as a refusal",
  '    if builder is not None:\n        return [builder["refusal"]]\n', ""),
 ("resmap_models", "an unpriced point given a marginal",
  'name == reference or "hierarchical" not in summary.get(name, {}):', "name == reference or name not in summary:"),
 ("resmap_tables", "builder refusals labelled as guards",
  '"builder" if name in builder else "elaboration guard"', '"elaboration guard"'),
]
red = 0
for module, label, old, new in MUTANTS:
    path = REPO / "syn/resmap" / f"{module}.py"
    text = path.read_text()
    assert text.count(old) == 1, (module, label)
    mod = types.ModuleType(module)
    mod.__file__ = str(path)
    sys.modules[module] = mod
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            exec(compile(text.replace(old, new), str(path), "exec"), mod.__dict__)
            rc = mod.selftest()
    except Exception as exc:  # a crash is red too, but say so
        rc, out = 1, io.StringIO(f"crashed: {type(exc).__name__}: {exc}")
    finally:
        del sys.modules[module]
    first = next((l for l in out.getvalue().splitlines() if "FAILED" in l or "crashed" in l), "")
    print(f"{'RED  ' if rc else 'GREEN'} {module}: {label} :: {first[:160]}")
    red += bool(rc)
print(f"{red}/{len(MUTANTS)} planted defects turned their self-test red")
sys.exit(0 if red == len(MUTANTS) else 1)
