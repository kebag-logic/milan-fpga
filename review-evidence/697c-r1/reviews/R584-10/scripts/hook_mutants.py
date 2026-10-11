"""Weaken the pin proof's audit hook in place, one mutant at a time, run only the hook's standing controls, and
restore the file. A sound control set lets at least one control escape per mutant.

Usage: python3 -B -I hook_mutants.py <checkout>
"""
import subprocess
import sys
from pathlib import Path

checkout = Path(sys.argv[1]).resolve()
target = checkout / "sw/firmware/ctrl/test/ctrl_build.py"
original = target.read_bytes()
MUTANTS = {
    "H0 none (the unmutated hook)": None,
    "H1 hook never installed": ("    sys.addaudithook(hook)\n", "    pass\n"),
    "H2 launches never judged": ("        elif event in starts:\n", "        elif False:\n"),
    "H3 dynamic code never judged": ("        elif event in dynamic or event", "        elif False and event"),
    "H4 helper environment unchecked": ("        if kind(env) is not mapping or env.get(\"GIT_NO_REPLACE_OBJECTS\") != \"1\":",
                                        "        if False:"),
    "H5 any program accepted from the helper": ("        if not (kind(given) is text and given == program)",
                                                "        if False and not (kind(given) is text and given == program)"),
    "H6 code replacement never judged": ("        elif event == \"object.__setattr__\"", "        elif False"),
}
RUN = """import sys
sys.path.insert(0, sys.argv[1] + "/sw/firmware/ctrl/test")
import ctrl_pin
arms = [("unplanted", ctrl_pin.unplanted, "")] + [(w, c, n) for w, _, c, n in ctrl_pin.census_arms()]
esc = 0
for what, check, needle in arms:
    accepted, detail = check()
    ok = accepted if not needle else not accepted
    esc += not ok
    print(("ok " if ok else "ESCAPED ") + what + ": " + detail[:160], flush=True)
print("ARMS", len(arms), "ESCAPED", esc, flush=True)
"""
try:
    for name, edit in MUTANTS.items():
        text = original.decode()
        if edit is not None:
            assert text.count(edit[0]) == 1, (name, text.count(edit[0]))
            text = text.replace(edit[0], edit[1])
        target.write_text(text, encoding="utf-8")
        res = subprocess.run([sys.executable, "-B", "-I", "-c", RUN, str(checkout)], capture_output=True, text=True,
                             timeout=1800)
        lines = (res.stdout + res.stderr).splitlines()
        summary = [ln for ln in lines if ln.startswith("ARMS")]
        print(f"=== {name}: rc {res.returncode} {summary[-1] if summary else lines[-1:] }", flush=True)
        for ln in lines:
            if ln.startswith("ESCAPED"):
                print("   ", ln[:200], flush=True)
finally:
    target.write_bytes(original)
print("restored", target.read_bytes() == original)
