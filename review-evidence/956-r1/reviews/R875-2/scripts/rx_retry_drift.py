"""rx_retry_drift.py <checkout> <work> <variant>: SrpRetry.AnAttributeChangeAloneAllowsTheRetry with its hand driver
counting the iterations that leave a paused build (tx_resume != 0, tx_due == 0) undriven (variant 'count'), or driving
THE TRANSMIT while tx_owed is nonzero (variant 'owed'). Disposable copy; prints the arm's log."""
import shutil, sys
from pathlib import Path
root, work, variant = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import fw_gtest, ctrl_build, srp_arms  # noqa: E402
for n in ("ctrl", "ctrl_nvm"):
    if (work / n).exists():
        shutil.rmtree(work / n)
    shutil.copytree(root / "sw/firmware" / n, work / n)
t = work / "ctrl/test/srp_rx_retry.cpp"
s = t.read_text()
old = "        if(adapter.tx_due!=0u) loop.transmit(loop.transmit_ctx,CTRL_LOOP_BUILD_MOST);\n"
assert s.count(old) == 1
new = {"count": "        if(adapter.tx_due==0u && adapter.tx_resume!=0u) ++undriven;\n" + old,
       "owed": old.replace("adapter.tx_due!=0u", "adapter.tx_owed!=0u")}[variant]
s = s.replace(old, new)
s = s.replace("    ASSERT_TRUE(adapter.ifs[0].moved) << \"every Applicant",
              "    printf(\"PROBE undriven paused-build iterations %u\\n\",undriven);\n    ASSERT_TRUE(adapter.ifs[0].moved) << \"every Applicant") if variant == "count" else s
s = s.replace("    ASSERT_FALSE(adapter.ifs[0].moved);\n    for(unsigned n=0;n<300",
              "    ASSERT_FALSE(adapter.ifs[0].moved);\n    unsigned undriven=0;\n    for(unsigned n=0;n<300") if variant == "count" else s
t.write_text(s)
srp_arms.HERE = work / "ctrl/test"
tree = ctrl_build.Tree(work / "ctrl", work / "build", work / "reuse", fw_gtest.Build(jobs=4))
o = srp_arms.arm_srp(tree, (root / "third_party/lwSRP").resolve(), 1, test=("srp_rx_retry.cpp", "SrpRetry.AnAttributeChangeAloneAllowsTheRetry"))
print(o.log); sys.exit(o.rc)
