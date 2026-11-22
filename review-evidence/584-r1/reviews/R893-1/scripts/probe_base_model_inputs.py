"""Run the AECP Inputs.* tests at the 8x8 config from an exported tree whose builder and 8x8 config are the base
(dd163e41) ones, every other file the head. Run from that tree root: python3 -I probe_base_model_inputs.py <outdir>"""
import sys
from pathlib import Path
sys.path.insert(0, "sw/firmware/ctrl/test")
import aecp_arms as a, fw_gtest
out = Path(sys.argv[1])
tree = a.Tree(a.CTRL, out, out / "reuse", fw_gtest.Build(jobs=8), Path("third_party/tsn-c-stack").resolve())
r = a.core_arm(tree, a.ROOT / "configs/endstation_ax7101_8x8.yaml", selected=a.INPUTS)
print(r.log); print("rc", r.rc)
