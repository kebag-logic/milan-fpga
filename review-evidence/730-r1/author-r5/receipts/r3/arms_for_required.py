"""Every failing self-test arm for R632-2's K12, K13, K32 and K36 (anchors read from its mutants_r2.py, unchanged)."""
import pathlib, shutil, subprocess, sys
packet, pristine, scratch = (pathlib.Path(a) for a in sys.argv[1:4])
ns = {}
src = (packet / "scripts" / "mutants_r2.py").read_text()
exec(src.split("def run_one")[0].replace("PACKET = pathlib.Path(sys.argv[1]).resolve()", "PACKET = None").replace("PRISTINE = pathlib.Path(sys.argv[2]).resolve()", "PRISTINE = None").replace('JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8', "JOBS = 1").replace('SANDBOX = PACKET / "scripts" / "sandbox.sh"', "").replace('PROBE = PACKET / "scripts" / "probe_r2.py"', ""), ns)
for ident, _probe, what, old, new in ns["MUTANTS"]:
    if ident not in ("K12", "K13", "K32", "K36"):
        continue
    tree = scratch / ident
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(pristine, tree)
    target = tree / "scripts" / "act_ci.py"
    text = target.read_text()
    assert text.count(old) == 1, ident
    target.write_text(text.replace(old, new))
    result = subprocess.run([str(packet / "scripts" / "sandbox.sh"), str(tree), "python3", "-I", "scripts/act_ci.py", "--selftest"], capture_output=True, text=True, timeout=900)
    print(f"{ident} rc={result.returncode} - {what}")
    for line in result.stdout.splitlines():
        if line.startswith("  FAIL"):
            print("   ", line.strip()[:140])
    shutil.rmtree(tree)
