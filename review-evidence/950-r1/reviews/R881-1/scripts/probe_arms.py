"""probe_arms.py <tree-root> <out> <file> <old> <new> <arm>...: plant one disposable defect in a tree copy (the old text
exactly once), then build and run the named arms of the control gate (platsinks8, platsinks1, platboot1, platboot2),
printing each arm's rc and its failed checks. The tree is a scratch copy; nothing else is touched."""
import sys
from pathlib import Path
root, out, rel, old, new = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], sys.argv[4], sys.argv[5]
arms = sys.argv[6:]
old, new = old.encode().decode("unicode_escape"), new.encode().decode("unicode_escape")
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
from ctrl_build import CTRL, STACK, Tree  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402
assert str(CTRL).startswith(str(root)), CTRL
target = CTRL / rel
text = target.read_text()
assert text.count(old) == 1, f"{rel}: {text.count(old)} planting sites"
target.write_text(text.replace(old, new))
print(f"planted {rel}: {old!r} -> {new!r}")
runs = {"platsinks8": lambda t: plat_arms.arm_platsinks(t, *plat_arms.SINK_SHAPES[0]),
        "platsinks1": lambda t: plat_arms.arm_platsinks(t, *plat_arms.SINK_SHAPES[1]),
        "platboot1": lambda t: plat_arms.arm_platboot(t, 1), "platboot2": lambda t: plat_arms.arm_platboot(t, 2)}
worst = 0
for arm in arms:
    tree = Tree(CTRL, out / arm, out / arm / "reuse", fw_gtest.Build(coverage=False, address_sanitizer=False, jobs=4),
                STACK)
    outcome = runs[arm](tree)
    fails = [l for l in outcome.log.splitlines() if "[FAIL]" in l or l.startswith("[  FAILED  ]")]
    print(f"{arm}: rc {outcome.rc}, {len(fails)} failure line(s)")
    for l in fails[:12]:
        print("   ", l[:300])
    worst = max(worst, outcome.rc)
raise SystemExit(worst)
