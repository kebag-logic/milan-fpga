"""R220 probes: targeted vacuity of the #407 arms and weakened-checker mutants.

Loads scripts/ci_events.py from the checkout as a module (no file edits),
monkeypatches the #407 comparison in memory only, and runs the #407 arms.
"""
import sys, pathlib, importlib.util, copy, collections, re
root = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("ci_events_r220", root / "scripts/ci_events.py")
ce = importlib.util.module_from_spec(spec); spec.loader.exec_module(ce)
pristine = ce.parse_world(ce.read_tree(root))
assert not ce.check(pristine).findings, "pristine must be clean"
arms = ce._carrier_script_arms(pristine)
print("407 workflow arms:", len(arms))
labels = [a[0] for a in arms]
assert len(set(labels)) == len(labels), "labels not unique"
all_labels = [a[0] for a in ce._mutations(pristine)]
print("all mutation arms:", len(all_labels), "unique:", len(set(all_labels)))

def run(arms_):
    miss = []
    for name, mut, want in arms_:
        w = copy.deepcopy(pristine); mut(w)
        f = ce.check(w).findings
        if not any(want in x for x in f):
            miss.append(name)
    return miss

orig = ce.check_carrier_script
real_miss = run(arms)
print("real checker misses:", len(real_miss))

def lever(n): return n.rsplit(" ", 1)[-1]

def with_cmp(cmp):
    def patched(c, path, what, step, entry):
        canonical = entry.get("run")
        recorded = (isinstance(canonical, tuple) and bool(canonical)
                    and all(isinstance(l, str) for l in canonical))
        c.item(recorded, path, f"{what} must record a canonical normalized `run` script")
        if not recorded:
            return
        lines = ce.normalize_script(step["run"])
        c.item(cmp(tuple(lines), canonical), path,
               f"{what} script is not the canonical form: " + ce.script_difference(lines, canonical))
    return patched

mutants = {
    "M0 comparison removed (no-op)": lambda c, *a, **k: None,
    "M1 order-insensitive (sorted equality)": with_cmp(lambda g, w: sorted(g) == sorted(w)),
    "M2 first line only": with_cmp(lambda g, w: g[:1] == w[:1]),
    "M3 length only": with_cmp(lambda g, w: len(g) == len(w)),
    "M4 canonical is a prefix (appended lines allowed)": with_cmp(lambda g, w: g[:len(w)] == w),
    "M5 strip trailing '|| true' before comparing": with_cmp(
        lambda g, w: tuple(re.sub(r" \|\| true$", "", l) for l in g) == tuple(re.sub(r" \|\| true$", "", l) for l in w)),
    "M6 ignore --selftest/--self-test/--check flags": with_cmp(
        lambda g, w: tuple(re.sub(r" --(self-test|selftest|check)(?= |$)", "", l) for l in g) == tuple(re.sub(r" --(self-test|selftest|check)(?= |$)", "", l) for l in w)),
    "M7 last line only": with_cmp(lambda g, w: g[-1:] == w[-1:]),
    "M8 compare only python3 lines": with_cmp(
        lambda g, w: tuple(l for l in g if l.startswith("python3")) == tuple(l for l in w if l.startswith("python3"))),
    "M9 docs.yml only (elaborate unchecked)": None,
}
for name, patched in mutants.items():
    if name.startswith("M9"):
        def patched(c, path, what, step, entry):
            if path == ce.DOCS:
                orig(c, path, what, step, entry)
    ce.check_carrier_script = patched
    try:
        pristine_findings = ce.check(pristine).findings
        miss = run(arms)
    finally:
        ce.check_carrier_script = orig
    by = collections.Counter(lever(m) for m in miss)
    print(f"{name}: pristine findings={len(pristine_findings)}; arms missed={len(miss)} of {len(arms)} "
          f"-> selftest {'RED (mutant detected)' if miss or pristine_findings else 'GREEN (mutant SURVIVES)'}; by lever {dict(by)}")
