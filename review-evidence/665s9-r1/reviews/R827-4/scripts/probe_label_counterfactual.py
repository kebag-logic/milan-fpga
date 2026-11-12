"""Counterfactual and presence probes for builder gate 23o's nvm_split label.

Run from a checkout of the composed tree:  python3 -B probe_label_counterfactual.py
In-memory patches only; no file in the checkout is edited.
  A. per config: which of gate 23o's labels build() writes in both placements.
  B. the split recipe alone writes a different nvm_split.json, gate labels
     WITHOUT nvm_split (the prior head's tuple): expected NOT caught.
  C. the same plant with the head's tuple: expected caught.
  D. the split recipe alone writes no nvm_split path: expected caught.
"""
import copy, dataclasses, importlib.util, sys, tempfile
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "sw" / "builder"))
spec = importlib.util.spec_from_file_location("test_builder", ROOT / "sw" / "builder" / "test_builder.py")
tb = importlib.util.module_from_spec(spec); sys.modules["test_builder"] = tb; spec.loader.exec_module(tb)
eb = tb.eb
HEAD = tb.RECIPE_SHAPE_ARTIFACTS
with tempfile.TemporaryDirectory() as tmp:
    for name, path in tb.CONFIGS.items():
        for pl in (None, "split"):
            r = eb.build(str(path), str(Path(tmp) / name / str(pl)), **({"placement": pl} if pl else {}))
            print(f"A {name} {pl or 'all-fabric'}: absent gate labels {[l for l in HEAD if l not in r['paths']]}")

def run(why, labels, deriver=None, build_wrap=None):
    real_d, real_b = eb._derive_artifacts, eb.build
    tb.RECIPE_SHAPE_ARTIFACTS = labels
    if deriver: eb._derive_artifacts = deriver(real_d)
    if build_wrap: eb.build = build_wrap(real_b)
    try:
        tb.test_placement_recipe(); print(f"{why}: gate 23o PASSED (not caught)")
    except AssertionError as exc:
        print(f"{why}: gate 23o FAILED (caught): {str(exc).splitlines()[1].strip()}")
    finally:
        eb._derive_artifacts, eb.build, tb.RECIPE_SHAPE_ARTIFACTS = real_d, real_b, HEAD

def bump(real):
    def f(config_path, placement=None):
        art = real(config_path, placement)
        if placement == "split":
            ch = copy.deepcopy(art.nvm_split); ch["blocks"][0]["count"] += 1
            art = dataclasses.replace(art, nvm_split=ch)
        return art
    return f

def drop_path(real):
    def f(config_path, outdir=None, **kw):
        r = real(config_path, outdir, **kw)
        if kw.get("placement") == "split":
            r["paths"].pop("nvm_split", None)
        return r
    return f

run("B prior-head labels, split nvm_split changed", tuple(l for l in HEAD if l != "nvm_split"), deriver=bump)
run("C head labels, split nvm_split changed", HEAD, deriver=bump)
run("D head labels, split writes no nvm_split path", HEAD, build_wrap=drop_path)
run("E head labels, unplanted", HEAD)
