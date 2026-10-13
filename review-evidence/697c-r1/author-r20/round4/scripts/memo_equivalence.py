"""For every boundary control (and the checkout), the findings of a judgement that reuses the run's
preprocessings equal those of one that reuses nothing (scratch evidence for the memo). Both judge in full:
no control stops at its finding here."""
import sys, time, tempfile, shutil
from pathlib import Path
tree = sys.argv[1]
sys.path[:0] = [tree + "/sw/firmware/ctrl/test", tree + "/sw/firmware/gtest"]
import ctrl_boundary as b, fw_rv32, dataclasses
rv32 = fw_rv32.compiler()
work = Path(tempfile.mkdtemp(prefix="memo-eq-"))
shared = b.MEMO
none = lambda self, argv, unit: None
original = b.Judgement.lookup

def full(plant, trees, reuse):
    b.MEMO = shared if reuse else b.Memo()
    b.Judgement.lookup = original if reuse else none
    try:
        return sorted(b.judge(trees, rv32, work / "build", control=dataclasses.replace(plant, needle="")))
    except b.Refusal as exc:
        return [f"REFUSED: {exc}"]
    finally:
        shutil.rmtree(work / "build", ignore_errors=True)
        b.MEMO, b.Judgement.lookup = shared, original

differ = 0
for plant in (b.BASE, *b.PLANTS):
    trees = b.planted(plant, work / "plants")
    t = time.time()
    memo = full(plant, trees, True)
    counts = shared.made[-1].counts if shared.made else {}
    fresh = full(plant, trees, False)
    same = memo == fresh
    differ += not same
    print(f"[{'same' if same else 'DIFFER'}] {len(memo)} finding(s), memo {counts}, {time.time() - t:.0f} s: {plant.name}",
          flush=True)
    if not same:
        print("  memo only:", sorted(set(memo) - set(fresh)))
        print("  fresh only:", sorted(set(fresh) - set(memo)))
print(f"memo equivalence: {differ} control(s) differ of {1 + len(b.PLANTS)}")
shutil.rmtree(work)
sys.exit(1 if differ else 0)
