"""Scratch: each round-15 protection removed in turn from a disposable clone's ctrl_build.py, then that clone's
configuration-relevant pin controls run (pin_subset15.py): which controls escape, and whether Git ran a program.

usage: config_mutants.py <disposable clone> <work> <scripts dir> [mutant prefix ...]
"""
import subprocess
import sys
from pathlib import Path

clone, work, scripts = (Path(a).resolve() for a in sys.argv[1:4])
build = clone / "sw/firmware/ctrl/test/ctrl_build.py"
CALL = "    configured(stack)\n"
LAZY = (', "GIT_NO_LAZY_FETCH": "1"}', "}")
MUTANTS = {
    "M0 none": [],
    "M1 the allowlist not checked": [(CALL, "")],
    "M2 no GIT_NO_LAZY_FETCH": [LAZY],
    "M3 neither": [(CALL, ""), LAZY],
    "M4 the allowlist reads the repository's own file only (--local)": [
        ('"config", "--list", "--show-scope", "-z"', '"config", "--list", "--show-scope", "--local", "-z"')],
    "M5 the allowlist by section only": [
        ('named = f"{section}.*.{variable}" if subsection else key',
         'named = next((k for k in STACK_CONFIG if k.startswith(section + ".")), key)')],
    "M6 each file hashed through Git (its attributes)": [
        ("    data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()\n",
         "    if not path.is_symlink():\n        return git(path.parent, \"hash-object\", path.name).stdout.strip()\n"
         "    data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()\n")],
    "M7 the allowlist checked after the objects are read": [
        (CALL, ""), ("    want = pinned_tree(stack, pin, algorithm)\n",
                     "    want = pinned_tree(stack, pin, algorithm)\n" + CALL)],
}
wanted = sys.argv[4:]
original = build.read_text(encoding="utf-8")
for name, edits in MUTANTS.items():
    if wanted and not any(name.startswith(w) for w in wanted):
        continue
    text = original
    for old, new in edits:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    build.write_text(text, encoding="utf-8")
    res = subprocess.run([sys.executable, "-I", "-B", str(scripts / "pin_subset15.py"), str(clone),
                          str(work / name[:2])], capture_output=True, text=True)
    lines = res.stdout.splitlines()
    print(f"== {name}: {lines[-1] if lines else res.stderr[-300:]}", flush=True)
    for line in lines:
        if line.startswith("[ESCAPED]"):
            print("  " + line[:300], flush=True)
build.write_text(original, encoding="utf-8")
print("restored:", build.read_text(encoding="utf-8") == original)
