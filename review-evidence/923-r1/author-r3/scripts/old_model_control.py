#!/usr/bin/env python3
"""old_model_control.py <checkout> <scratch>: the Face tests on a scratch copy of test_aecp.cpp whose store model
suppresses a commit's write when its reply is lost (round 2's model). Each late-reply test must fail on the
store/map agreement words: a suppressed write never passes as an acknowledged edit."""
import os
import sys
from pathlib import Path
repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"] = str(scratch)
sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest")]
import aecp_arms
import fw_gtest
from ctrl_build import CTRL, STACK, Tree
text = (aecp_arms.HERE / "test_aecp.cpp").read_text()
new = "        if(verdict==2u&&!reserved){*reply=MBX_MODEL_SILENT;return 0;}\n"
assert text.count(new) == 1
(scratch / "test_aecp.cpp").write_text(text.replace(new, "        if(verdict==2u){(void)reserved;*reply=MBX_MODEL_SILENT;return 0;}\n"))
aecp_arms.HERE = scratch
tree = Tree(CTRL, scratch / "build", scratch / "reuse", fw_gtest.Build(jobs=4), STACK)
result = aecp_arms.core_arm(tree, repo / "configs/endstation_ax7101_1x1_tdm8.yaml", 2, "mailbox",
                            "Face.ALostReply*:Face.AnUnansweredEditFailsUntilItsCommitIsReserved")
print(result.log)
words = "GET_AUDIO_MAP and the datapath's store hold the same mappings"
want = ("Face.ALostReplyAfterTheReservedCommitLeavesTheStoreAndTheMapAgreeing",
        "Face.ALostReplyInTheRestoresCommitLeavesTheStoreAndTheMapAgreeing",
        "Face.AnUnansweredEditFailsUntilItsCommitIsReserved")
ok = all(f"[FAIL] {t}: {words}" in result.log for t in want)
print("CONTROL", "PASS: each late-reply test refuses the suppressed write" if ok else "FAIL: a suppressed write passed")
sys.exit(0 if ok else 1)
