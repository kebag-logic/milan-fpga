"""Each rule of the pin proof's audit hook (ctrl_build.audited and its environment judge) removed in turn, and the
helper's environment inheriting the caller's again, in a disposable checkout: which of the hook's standing controls
(ctrl_pin.census_arms) and the inherited-environment controls (ctrl_pin_env.inherited_arms) escape, and whether the
unmodified proof still passes. A rule a control holds must make at least one control escape when removed.
Usage: python3 -I hook_mutants.py <disposable checkout> [mutant name prefix ...]"""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
chosen = sys.argv[2:]
build = root / "sw/firmware/ctrl/test/ctrl_build.py"
EXACT = ("if key != captured and env.get(key) != want.get(key):", "if False:")
MUTANTS = {
    "H0 none": [],
    "H1 the helper's own code not required": [("caller is None or caller.f_code is not code or", "caller is None or")],
    "H2 the program not checked": [("if not (kind(given) is text and given == program)",
                                    "if False and not (kind(given) is text and given == program)")],
    "H3 GIT_NO_REPLACE_OBJECTS not checked": [('if env.get("GIT_NO_REPLACE_OBJECTS") != "1":', "if False:")],
    "H4 the graft file not checked": [("        if not under:\n", "        if False:\n")],
    "H5 the decision not a scope": [("(frame.f_code.co_name in decision and frame.f_globals is proof[0])", "False")],
    "H6 a proof module's top level not a scope": [('(loading and frame.f_code.co_name == "<module>" and ours(frame))',
                                                   "False")],
    "H7 the proof's own dynamic code not refused": [("if ours(frame_at(1)) or running(False):", "if running(False):")],
    "H8 dynamic code while deciding not refused": [("if ours(frame_at(1)) or running(False):", "if ours(frame_at(1)):")],
    "H9 an import of importlib not refused": [('event == "import" and kind(args[0]) is text and',
                                               'False and kind(args[0]) is text and')],
    "H10 a function's code replaceable": [('elif event == "object.__setattr__"', "elif False")],
    "H11 thread starts not refused": [(', "_thread.start_new_thread", "_thread.start_joinable_thread"', "")],
    "H12 the collector's lists not refused": [('"gc.get_objects", ', "")],
    "H13 a trace function not refused": [('"sys.settrace", ', "")],
    "H14 the proof's files not its code": [("        if frame.f_code.co_filename in files:\n            return True\n", "")],
    "H15 a refusal not written first": [('write(2, f"{said}{message}\\n".encode(errors="backslashreplace"))', "pass")],
    "H16 no hook installed": [("    sys.addaudithook(hook)\n", "    pass\n")],
    "H17 a module's registration ignored": [("            proof.append(frame_at(1).f_globals)\n", "            pass\n")],
    "H18 keys and values not required plain str": [("if kind(key) is not text or kind(value) is not text:", "if False:")],
    "H19 the environment not required exactly the proof's own": [EXACT],
    "H20 fork_exec's entries not required each a key given once": [("if size(env) != given:", "if False:")],
    "H21 the helper inherits the caller's environment (as at aca5e8af)": [
        ("return dict(GIT_ENVIRONMENT)", 'return {**os.environ, "GIT_NO_REPLACE_OBJECTS": "1", "GIT_GRAFT_FILE": NO_GRAFTS}')],
    "H22 H21, and the environment not required exactly the proof's own": [
        ("return dict(GIT_ENVIRONMENT)", 'return {**os.environ, "GIT_NO_REPLACE_OBJECTS": "1", "GIT_GRAFT_FILE": NO_GRAFTS}'),
        EXACT],
    "H23 the helper inherits the caller's environment under the proof's own settings, and H19": [
        ("return dict(GIT_ENVIRONMENT)", "return {**os.environ, **GIT_ENVIRONMENT}"), EXACT],
    "H24 a capture's builders' names not let through": [("if key != captured and env.get(key)", "if env.get(key)")],
}
RUN = '''import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import ctrl_pin
from ctrl_build import stack_gitlink
ok, said = ctrl_pin.unplanted()
print(f"clean: {'passes' if ok else 'REFUSED ' + said}", flush=True)
work = Path(sys.argv[2])
work.mkdir(parents=True, exist_ok=True)
pin = stack_gitlink()
clone = ctrl_pin.Clone(work, pin)
texts = {p.relative_to(ctrl_pin.ROOT).as_posix(): p.read_text(encoding="utf-8") for p in ctrl_pin.PROOF}
arms = ctrl_pin.census_arms() + ctrl_pin.inherited_arms(clone.path, pin, work,
                                                        lambda s, e: ctrl_pin.proof_run(texts, s, e))
import subprocess
here = Path(sys.argv[1])
captured = subprocess.run([sys.executable, "-B", str(here / "ctrl_capture.py"), "--out", str(work / "capture"), "--",
                           sys.executable, "-B", str(here / "ctrl_build.py"), "--stack-pin"], capture_output=True,
                          text=True)
if captured.returncode:
    print(f"escaped: the pin check under a capture [{(captured.stdout + captured.stderr).strip()[-160:]}]", flush=True)
for name, spoil, check, needle in arms:
    clone.fresh()
    spoil()
    accepted, detail = check()
    if (accepted if not needle else (not accepted and needle in detail)) is False:
        print(f"escaped: {name.removeprefix('the audit hook, ')} [{detail[:160]}]", flush=True)
'''
original = build.read_text(encoding="utf-8")
for name, edits in MUTANTS.items():
    if chosen and not any(name.startswith(c + " ") for c in chosen):
        continue
    text = original
    missing = [old for old, _ in edits if text.count(old) != 1]
    if missing:
        print(f"{name}: ANCHOR {missing[0]!r} occurs {text.count(missing[0])} times, not run", flush=True)
        continue
    for old, new in edits:
        text = text.replace(old, new)
    build.write_text(text, encoding="utf-8")
    try:
        res = subprocess.run([sys.executable, "-I", "-B", "-c", RUN, str(build.parent), str(root.parent / "work")],
                             capture_output=True, text=True, timeout=1800)
    finally:
        build.write_text(original, encoding="utf-8")
    lines = (res.stdout + res.stderr).strip().splitlines()
    escaped = [ln.removeprefix("escaped: ") for ln in lines if ln.startswith("escaped: ")]
    clean = next((ln for ln in lines if ln.startswith("clean: ")), f"clean: no line (exit {res.returncode}): "
                 f"{lines[-1] if lines else ''}")
    verdict = "CAUGHT" if escaped or not clean.endswith("passes") else "NOT CAUGHT"
    if name.startswith("H0 "):
        verdict = "BASELINE " + ("clean" if not escaped and clean.endswith("passes") else "BROKEN")
    print(f"{verdict}  {name}: {clean}; {len(escaped)} escaped", flush=True)
    for ln in escaped:
        print(f"    {ln}", flush=True)
print(f"restored {build.read_text(encoding='utf-8') == original}")
