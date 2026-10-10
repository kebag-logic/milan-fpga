#!/usr/bin/env python3
"""R583-4: run the firmware gate's srpcmp arm as the gate calls it, then against planted comparators.
Usage: python3 -I r583_4_srpcmp_arm.py <tree> <scratch-dir>. Plants are written only under <scratch-dir>."""
import shutil, sys
from pathlib import Path
tree, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
test = tree / "sw/firmware/ctrl/test"
sys.path.insert(0, str(test))
import ctrl_arms  # noqa: E402
o = ctrl_arms.arm_srpcmp()
print(f"tracked comparator: arm rc={o.rc if hasattr(o, 'rc') else o[1]}\n{o.log if hasattr(o, 'log') else o[2]}")
src = (test / "srp_wire_compare.py").read_text()
plants = {
    "exit-1": src.replace("def main() -> int:\n", "def main() -> int:\n    raise SystemExit(1)\n", 1),
    "control-reported-failed": src.replace('"packing_only": "PASS"', '"packing_only": "FAIL"', 1)
        if '"packing_only": "PASS"' in src else None,
    "no-plants-reported": src.replace('"five_value_vector": "PASS", "plants": results}', '"five_value_vector": "PASS", "plants": []}', 1),
}
bad = 0
for name, text in plants.items():
    if text is None or text == src:
        print(f"[skip] {name}: fixture not found in comparator source"); continue
    d = scratch / f"srpcmp-{name}"; shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    (d / "srp_wire_compare.py").write_text(text)
    ctrl_arms.SRP_COMPARE = d / "srp_wire_compare.py"
    o = ctrl_arms.arm_srpcmp()
    rc = o.rc if hasattr(o, "rc") else o[1]
    print(f"[{'caught' if rc else 'ESCAPED'}] planted {name}: arm rc={rc}")
    bad += not rc
sys.exit(1 if bad or (o is None) else 0)
