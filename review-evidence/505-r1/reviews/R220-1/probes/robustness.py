"""R220 robustness probes of the #407 comparison, in memory only."""
import sys, pathlib, importlib.util, copy
root = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("ce_r220", root / "scripts/ci_events.py")
ce = importlib.util.module_from_spec(spec); spec.loader.exec_module(ce)
P = ce.parse_world(ce.read_tree(root))
def steps(w, path, jid): return ce._job_steps(w, path, jid)
def idx(w, path, jid, name): return next(i for i, s in enumerate(steps(w, path, jid)) if s.get("name") == name)
def probe(label, edit, expect_fragment=None, expect_clean=False):
    w = copy.deepcopy(P); edit(w)
    f = ce.check(w).findings
    ok = (not f) if expect_clean else any(expect_fragment in x for x in f)
    print(f"[{'PASS' if ok else 'FAIL'}] {label}: {len(f)} finding(s)")
    for x in f[:3]:
        print("        ", x[:260])
    return ok
D, EL = ce.DOCS, ce.ELABORATE
res = []
# 1 appended hostile line to an early non-gate step (overwrites a later gate's script)
def e1(w):
    i = idx(w, D, "docs-check", "Install the python gate dependencies")
    steps(w, D, "docs-check")[i]["run"] += "\nprintf 'import sys\\nsys.exit(0)\\n' > scripts/check_py_idiom.py\n"
res.append(probe("appended line overwriting a later gate's script", e1, "step 4 (`Install the python gate dependencies`) script is not the canonical form: line 2 must be None"))
# 2 reorder two lines of the Python idiom gate
def e2(w):
    i = idx(w, D, "docs-check", "Python idiom gate")
    steps(w, D, "docs-check")[i]["run"] = "python3 scripts/check_py_idiom.py --selftest\npython3 scripts/check_py_idiom.py\n"
res.append(probe("Python idiom lines reordered", e2, "step 34 (`Python idiom gate`) script is not the canonical form: line 1 must be"))
# 3 middle command moved inside the tclsh fallback block (runs only when tclsh is absent)
def e3(w):
    i = idx(w, D, "docs-check", "SoC source-list gate (Vivado would fail 40 min in without this)")
    s = steps(w, D, "docs-check")[i]
    s["run"] = s["run"].replace("  sudo apt-get install -y --no-install-recommends tcl\n}\npython3 sw/litex/iob_pack_selftest.py",
                                "  sudo apt-get install -y --no-install-recommends tcl\n  python3 sw/litex/iob_pack_selftest.py\n}")
    assert "iob_pack_selftest.py\n}" in s["run"], s["run"]
res.append(probe("SoC gate selftest moved inside the tclsh fallback block", e3, "step 24 (`SoC source-list gate"))
# 4 middle command swallowed (not the last line) in a multi-command gate
def e4(w):
    i = idx(w, D, "docs-check", "Per-page contents gate")
    s = steps(w, D, "docs-check")[i]
    s["run"] = s["run"].replace("python3 scripts/gen_toc.py --verify-anchors", "python3 scripts/gen_toc.py --verify-anchors || true")
res.append(probe("middle command of Per-page contents gate swallowed", e4, "step 40 (`Per-page contents gate`) script is not the canonical form: line 2 must be"))
# 5 NBSP inside a body -> fail closed with the refusal line
def e5(w):
    i = idx(w, D, "docs-check", "Doc cited-path gate")
    steps(w, D, "docs-check")[i]["run"] = "python3 scripts/check_doc_paths.py"
res.append(probe("NBSP between words", e5, "step 38 (`Doc cited-path gate`) script is not the canonical form: line 1 must be 'python3 scripts/check_doc_paths.py' (found '<<refused>>"))
# 6 CRLF line endings
def e6(w):
    i = idx(w, EL, "elaborate", "Install LiteX at the pinned revisions")
    steps(w, EL, "elaborate")[i]["run"] = "python3 -m pip install --quiet pyyaml\r\npython3 -m pip install --quiet -r sw/litex/litex_pins.txt\r\n"
res.append(probe("CRLF line endings", e6, "(`Install LiteX at the pinned revisions`) script is not the canonical form"))
# 7 empty body
def e7(w):
    i = idx(w, EL, "elaborate", "Apply the toolchain patch series")
    steps(w, EL, "elaborate")[i]["run"] = ""
res.append(probe("empty body", e7, "(`Apply the toolchain patch series`) script is not the canonical form: line 1 must be 'sw/litex/patches/apply.sh' (found None)"))
# 8 non-string run (list) -> identity refusal, never silently accepted
def e8(w):
    i = idx(w, D, "wire-accountability", "Fetch the engine authority the builder derives from")
    steps(w, D, "wire-accountability")[i]["run"] = ["git submodule update --init gptp-processor"]
res.append(probe("non-string run value", e8, "job `wire-accountability` step 2 must be the step named"))
# 9 comment line appended (benign but still refused: comments are canonical)
def e9(w):
    i = idx(w, D, "docs-check-no-git", "Strip git metadata, then run the docs gate")
    steps(w, D, "docs-check-no-git")[i]["run"] += "# harmless note\n"
res.append(probe("comment line appended", e9, "job `docs-check-no-git` step 2 (`Strip git metadata, then run the docs gate`) script is not the canonical form: line 4 must be None"))
# 10 whitespace inside a quoted word is normalized away (pre-existing item-7 property) -> accepted
def e10(w):
    i = idx(w, D, "docs-check", "Install the pinned sv2v release")
    s = steps(w, D, "docs-check")[i]
    assert 'echo "${sha256}  /tmp/sv2v.zip"' in s["run"]
    s["run"] = s["run"].replace('echo "${sha256}  /tmp/sv2v.zip"', 'echo "${sha256}     /tmp/sv2v.zip"')
res.append(probe("extra blanks inside a quoted word (pre-existing normalization equivalence)", e10, expect_clean=True))
# 11 malformed records in production tables: list, empty tuple, non-str element, raw str
for label, bad in (("list record", ["python3 scripts/check_py_idiom.py", "python3 scripts/check_py_idiom.py --selftest"]),
                   ("empty tuple record", ()), ("non-str element", ("python3 scripts/check_py_idiom.py", 7)),
                   ("raw string record", "python3 scripts/check_py_idiom.py\npython3 scripts/check_py_idiom.py --selftest")):
    saved = ce.CARRIER_STEP_LISTS[(D, "docs-check")]
    lst = [dict(e) for e in saved]; lst[33]["run"] = bad
    ce.CARRIER_STEP_LISTS[(D, "docs-check")] = tuple(lst); ce.STEP_LISTS[(D, "docs-check")] = tuple(lst)
    try:
        f = ce.check(P).findings
    finally:
        ce.CARRIER_STEP_LISTS[(D, "docs-check")] = saved; ce.STEP_LISTS[(D, "docs-check")] = saved
    ok = any("step 34 (`Python idiom gate`) must record a canonical normalized `run` script" in x for x in f)
    print(f"[{'PASS' if ok else 'FAIL'}] malformed production record ({label}) fails closed: {len(f)} finding(s)")
    res.append(ok)
# 12 record deleted from the PRODUCTION table: --check refuses AND the arms are still derived
saved = ce.CARRIER_STEP_LISTS[(EL, "elaborate")]
lst = [dict(e) for e in saved]; lst[12].pop("run")
ce.CARRIER_STEP_LISTS[(EL, "elaborate")] = tuple(lst); ce.STEP_LISTS[(EL, "elaborate")] = tuple(lst)
try:
    f = ce.check(P).findings
    arms = [a for a in ce._carrier_script_arms(P) if a[0].startswith("carrier-script-407 elaborate step 13 ")]
    misses = []
    for name, mut, want in arms:
        w = copy.deepcopy(P); mut(w)
        if not any(want in x for x in ce.check(w).findings):
            misses.append(name)
finally:
    ce.CARRIER_STEP_LISTS[(EL, "elaborate")] = saved; ce.STEP_LISTS[(EL, "elaborate")] = saved
ok = any("step 13 (`Elaboration gates`) must record a canonical normalized `run` script" in x for x in f) and len(arms) == 3 and len(misses) == 2
print(f"[{'PASS' if ok else 'FAIL'}] production record for elaborate step 13 deleted: --check findings={len(f)}; arms still derived={len(arms)}; body arms now missing={len(misses)} {misses}")
res.append(ok)
print("ALL PASS" if all(res) else "SOME FAIL")
