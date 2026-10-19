#!/usr/bin/env python3
"""Plant 'an all-UNUSED payload reads as erased' into a scratch copy of the saved-state store and run every store
suite binary at the shipping 1x1 shape, to check the claim that no store suite catches it.

usage: store_gap.py <checkout> <work-dir> <out-dir>   (the checkout is only read)"""
import shutil
import sys
from pathlib import Path

checkout, work, out = (Path(a).resolve() for a in sys.argv[1:4])
sys.path[:0] = [str(checkout / "sw/firmware/ctrl_nvm/test"), str(checkout / "sw/firmware/gtest")]
import fw_gtest  # noqa: E402
import test_ctrl_nvm as t  # noqa: E402
from nvm_bench import TREE  # noqa: E402

shutil.rmtree(work, ignore_errors=True)
out.mkdir(parents=True, exist_ok=True)
shape = t.prepare(checkout / "configs/endstation_ax7101_1x1_tdm8.yaml", work / "shape")
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
    (out / (binary.name + ".log")).write_text(log)
    print(binary.name, "ok" if ok else "FAILED", [line for line in log.splitlines() if line.startswith("RESULT")])
    if not ok:
        failed.append(binary.name)
print("store suites failing under the plant:", failed or "none")
