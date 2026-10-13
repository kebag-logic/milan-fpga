"""Each rule of the pin proof's audit hook (ctrl_build.audited) removed in turn, in a disposable checkout: which of
the hook's standing controls (ctrl_pin.census_arms) escape, and whether the unmodified proof still passes. A rule a
control holds must make at least one control escape when removed.
Usage: python3 -I hook_mutants.py <disposable checkout>"""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
build = root / "sw/firmware/ctrl/test/ctrl_build.py"
MUTANTS = {
    "H1 the helper's own code not required": ("caller is None or caller.f_code is not code or", "caller is None or"),
    "H2 the program not checked": ("if not (kind(given) is text and given == program)", "if False and not (kind(given) is text and given == program)"),
    "H3 GIT_NO_REPLACE_OBJECTS not checked": ('env.get("GIT_NO_REPLACE_OBJECTS") != "1"', "False"),
    "H4 the graft file not checked": ("return None if under else", "return None if True else"),
    "H5 the decision not a scope": ("(frame.f_code.co_name in decision and frame.f_globals is proof[0])", "False"),
    "H6 a proof module's top level not a scope": ('(loading and frame.f_code.co_name == "<module>" and ours(frame))', "False"),
    "H7 the proof's own dynamic code not refused": ("if ours(frame_at(1)) or running(False):", "if running(False):"),
    "H8 dynamic code while deciding not refused": ("if ours(frame_at(1)) or running(False):", "if ours(frame_at(1)):"),
    "H9 an import of importlib not refused": ('event == "import" and kind(args[0]) is text and', 'False and kind(args[0]) is text and'),
    "H10 a function's code replaceable": ('elif event == "object.__setattr__"', "elif False"),
    "H11 thread starts not refused": (', "_thread.start_new_thread", "_thread.start_joinable_thread"', ""),
    "H12 the collector's lists not refused": ('"gc.get_objects", ', ""),
    "H13 a trace function not refused": ('"sys.settrace", ', ""),
    "H14 the proof's files not its code": ("        if frame.f_code.co_filename in files:\n            return True\n", ""),
    "H15 a refusal not written first": ('write(2, f"{said}{message}\\n".encode(errors="backslashreplace"))', "pass"),
    "H16 no hook installed": ("    sys.addaudithook(hook)\n", "    pass\n"),
    "H17 a module's registration ignored": ("            proof.append(frame_at(1).f_globals)\n", "            pass\n"),
}
RUN = '''import sys
sys.path.insert(0, sys.argv[1])
import ctrl_pin
ok, said = ctrl_pin.unplanted()
print(f"clean: {'passes' if ok else 'REFUSED ' + said}")
for name, _, check, needle in ctrl_pin.census_arms():
    accepted, detail = check()
    if accepted or needle not in detail:
        print(f"escaped: {name.removeprefix('the audit hook, ')}")
'''
original = build.read_text(encoding="utf-8")
for name, (old, new) in MUTANTS.items():
    if original.count(old) != 1:
        print(f"{name}: ANCHOR occurs {original.count(old)} times, not run")
        continue
    build.write_text(original.replace(old, new), encoding="utf-8")
    try:
        res = subprocess.run([sys.executable, "-I", "-B", "-c", RUN, str(build.parent)], capture_output=True,
                             text=True, timeout=900)
    finally:
        build.write_text(original, encoding="utf-8")
    lines = (res.stdout + res.stderr).strip().splitlines()
    escaped = [ln.removeprefix("escaped: ") for ln in lines if ln.startswith("escaped: ")]
    clean = next((ln for ln in lines if ln.startswith("clean: ")), f"clean: no line (exit {res.returncode})")
    verdict = "CAUGHT" if escaped or not clean.endswith("passes") else "NOT CAUGHT"
    print(f"{verdict}  {name}: {clean}; {len(escaped)} escaped: {'; '.join(escaped)}")
