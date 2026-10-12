"""Run the boundary controls only, each with its wall time and the memo's counts (scratch)."""
import sys, time, tempfile
from pathlib import Path
tree = sys.argv[1]
sys.path[:0] = [tree + "/sw/firmware/ctrl/test", tree + "/sw/firmware/gtest"]
import ctrl_boundary as b, fw_rv32, shutil
rv32 = fw_rv32.compiler()
work = Path(tempfile.mkdtemp(prefix="controls-"))
t0 = time.time(); b.derive(); b.variants(); print(f"setup {time.time() - t0:.1f}", flush=True)
start = time.time()
for plant in (b.BASE, *b.PLANTS):
    t = time.time()
    trees = b.planted(plant, work / "plants")
    tc = time.time() - t
    try:
        findings = b.judge(trees, rv32, work / "plants-build", control=plant)
    except b.Refusal as exc:
        findings = [f"REFUSED: {exc}"]
    shutil.rmtree(work / "plants-build", ignore_errors=True)
    ok = (not findings) if not plant.needle else any(plant.needle in f for f in findings)
    c = b.MEMO.made[-1].counts if b.MEMO.made else {}
    print(f"{time.time() - t:6.1f}s copy {tc:4.1f} {'ok' if ok else 'ESCAPED'} {c} {plant.name[:70]}", flush=True)
print(f"controls {time.time() - start:.1f}")
t = time.time(); b.PREPROCESSED.clear()
f = b.judge(b.Trees(b.CTRL, b.STACK), rv32, work / "checkout")
print(f"checkout {time.time() - t:.1f} {sum(b.PREPROCESSED)} {b.MEMO.made[-1].counts} {f}")
shutil.rmtree(work)
