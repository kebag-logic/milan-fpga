# Disposable review mutants: copy sw/firmware/ctrl (+ ctrl_nvm) to a scratch
# directory, plant one textual defect, run the full AECP app arm at the given
# interface count, and report whether any test fails (caught) and which.
# usage: python3 -B review_mutants.py REPO OUTROOT NAME IF
import re, shutil, sys
from pathlib import Path
repo = Path(sys.argv[1]).resolve(); root = Path(sys.argv[2]).resolve(); name = sys.argv[3]; ifs = int(sys.argv[4])
PLANTS = {
    "wait-bound-past-cadence": ("aecp/aecp.h", "#define AECP_WAIT_MS 100u", "#define AECP_WAIT_MS 130u"),
    "owed-change-not-refused": ("aecp/aecp.c", "a->refusing = a->waiting || a->unlocked || !applied(a);",
                                "a->refusing = a->waiting || a->unlocked;"),
    "record-not-reset": ("aecp/aecp.c", "\tif (!a->refusing) {\n\t\ta->kept = 0;\n\t}\n", ""),
    "held-interface-not-restored": ("aecp/aecp.c", "a->response_interface = a->held_interface;",
                                    "a->response_interface = 0;"),
}
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import aecp_arms, fw_gtest
from ctrl_build import CTRL, STACK, Tree, Refusal
src = root / name / "ctrl"
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
shutil.copytree(CTRL.parent / "ctrl_nvm", src.parent / "ctrl_nvm", dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("test", "__pycache__", "*.pyc"))
path, old, new = PLANTS[name]
t = src / path; text = t.read_text()
assert text.count(old) == 1, f"{name}: {text.count(old)} sites"
t.write_text(text.replace(old, new))
tree = Tree(src, root / name / "build", root / name / "reuse", fw_gtest.Build(jobs=4), STACK.resolve())
try:
    r = aecp_arms.core_arm(tree, repo / "configs/endstation_ax7101_1x1_tdm8.yaml", ifs, "app", "*")
    failed = sorted(set(re.findall(r"\[  FAILED  \] (\S+) \(", r.log)))
    (root / f"{name}.log").write_text(r.log)
    print(f"{name} if{ifs}: rc={r.rc} {'CAUGHT' if r.rc else 'ESCAPED'} failing={failed}")
except Refusal as e:
    print(f"{name} if{ifs}: build refused (counts as caught by compile): {str(e)[:300]}")
