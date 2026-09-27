"""Run the pinned packer unit test, then again with the body/key refusal removed.

Usage: packer_mutation.py <processor checkout> <scratch dir>
The clean run must pass and the mutant run must fail.
"""
import shutil, subprocess, sys
from pathlib import Path
src, scratch = Path(sys.argv[1]), Path(sys.argv[2])
test = "tb/desc_store/test_gen_desc_image.py"
gen = "hdl/aecp/desc/gen_desc_image.py"
def run(root):
    r = subprocess.run([sys.executable, "-B", str(root / test)], capture_output=True, text=True)
    print(r.stderr[-900:]); return r.returncode
print("== clean (pinned bytes, in place) =="); clean = run(src)
shutil.rmtree(scratch, ignore_errors=True)
for rel in (test, gen):
    (scratch / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src / rel, scratch / rel)
g = scratch / gen; s = g.read_text()
old = "        if (body_type, body_index) != (typ, idx):\n"
assert s.count(old) == 1
g.write_text(s.replace(old, "        if False:\n"))
print("== mutant (refusal disabled, scratch copy) =="); mut = run(scratch)
print(f"clean rc={clean} mutant rc={mut}")
sys.exit(0 if clean == 0 and mut != 0 else 1)
