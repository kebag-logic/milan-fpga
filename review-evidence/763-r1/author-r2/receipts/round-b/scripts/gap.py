"""With one #763 defect planted in a copy, run the full AECP app arm without the new test."""
import shutil
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import aecp_arms
import aecp_mutants
import fw_gtest
from ctrl_build import CTRL, ROOT, Tree
work = Path(sys.argv[2])
name = sys.argv[3]
shutil.rmtree(work, ignore_errors=True)
src = work / "ctrl"
shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
shutil.copytree(CTRL.parent / "ctrl_nvm", work / "ctrl_nvm", ignore=shutil.ignore_patterns("test", "__pycache__", "*.pyc"))
d = next(d for d in aecp_mutants.DEFECTS if d.name == name)
target = src / d.path
text = target.read_text()
assert text.count(d.old) == 1
target.write_text(text.replace(d.old, d.new))
tree = Tree(src, work / "build", work / "reuse", fw_gtest.Build(jobs=4))
result = aecp_arms.core_arm(tree, ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", 2, "app",
                            "*:-Nvm.EmptyAndNonDefaultMapsSurviveTheRealStorePowerCycle")
(work.parent / (name + ".gap.log")).write_text(result.log)
print(name, "rc", result.rc, [l for l in result.log.splitlines() if l.startswith(("RESULT", "[  PASSED", "[  FAILED  ] ", "== "))])
