"""Plant the #763 store defect into a copy of ctrl_nvm and run every store suite binary at the shipping shape."""
import shutil
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import test_ctrl_nvm as t
import fw_gtest
from nvm_bench import TREE, ROOT
work = Path(sys.argv[2])
shutil.rmtree(work, ignore_errors=True)
shape = t.prepare(ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", work / "shape")
tree = work / "tree"
shutil.copytree(TREE, tree, ignore=shutil.ignore_patterns("__pycache__"))
old = "\tif (nvm_all_erased(rec, NVM_REC_HDR)) {"
new = "\tif (nvm_all_erased(rec, NVM_REC_HDR) || nvm_all_erased(rec + NVM_REC_HDR, r.plen)) {"
store = tree / "nvm_store.c"
text = store.read_text()
assert text.count(old) == 1
store.write_text(text.replace(old, new))
exes = t.build(shape, work / "build", fw_gtest.Build(jobs=4), tree)
failed = []
for binary in t.binaries(shape):
    ok, log = t.run_suite(exes[binary.name], t.fixture_of(shape, binary))
    (work / (binary.name + ".log")).write_text(log)
    print(binary.name, "ok" if ok else "FAILED", [l for l in log.splitlines() if l.startswith(("==", "RESULT"))])
    if not ok:
        failed.append(binary.name)
print("store suites failing under the plant:", failed or "none")
