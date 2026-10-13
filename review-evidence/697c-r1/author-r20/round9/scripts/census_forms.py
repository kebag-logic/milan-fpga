"""Forms a Git command can be started in, planted into the pin proof's texts; the census must name each but the
one assembled at run time (its stated limit). usage: python3 -B census_forms.py <checkout>"""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import ctrl_pin
texts = {p.relative_to(root).as_posix(): p.read_text() for p in ctrl_pin.PROOF}
pin_rel = "sw/firmware/ctrl/test/ctrl_pin.py"
anchor = "    listed = git(directory, "
assert texts[pin_rel].count(anchor) == 1
forms = {
    "a command list": 'run(["git", "-C", str(directory), "status"])\n',
    "a shell line": 'subprocess.run("git -C . status", shell=True)\n',
    "a program found on PATH": 'subprocess.run([shutil.which("git"), "status"])\n',
    "a program by its path": 'subprocess.run(["/usr/bin/git", "status"])\n',
    "a Python program": 'run([sys.executable, "-c", "import subprocess; subprocess.run([\'git\', \'status\'])"])\n',
    "an f-string": 'run(f"git -C {directory} status".split())\n',
    "a name assembled at run time (the stated limit)": 'run(["g" + "it", "status"])\n',
}
for what, line in forms.items():
    planted = dict(texts)
    planted[pin_rel] = texts[pin_rel].replace(anchor, "    " + line + anchor, 1)
    found = ctrl_pin.census(planted, ctrl_pin.git_env())
    print(f"{'NAMED' if found else 'NOT SEEN'}: {what}: {found[0] if found else ''}")
print("as the checkout holds it:", ctrl_pin.proof_census() or "no finding")
