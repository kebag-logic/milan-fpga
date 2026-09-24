#!/usr/bin/env python3
"""[R312] probe: plant map-length defects into an in-memory copy of the
shipping firmware text and grade it with the repository's own host bench
(test_nvm_firmware.make_bench + grade) at the 8x8 shape. The tree is not
edited. Run from the repository root; work dir is argv[1]."""
import sys
from pathlib import Path
sys.path.insert(0, "sw/firmware/nvm_hosttest")
import test_nvm_firmware as t
work = Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)
text = t.FIRMWARE.read_text()
cfg = Path("configs/endstation_ax7101_8x8.yaml").resolve()
PLANTS = {
  "control": ("", ""),
  # backend table only: output tables programmed with the old 9-entry length
  "rebase_old_len": ("unsigned int flen = REC_HDR + NVM_MAP_ENTRY * entries;",
                     "unsigned int flen = REC_HDR + NVM_MAP_ENTRY * (dir ? 9u : entries);"),
  # decode/staging only: per-record payload length from the old 9 entries
  "decode_old_len": ("return NVM_MAP_ENTRY * nvm_mapout_entries[index & 0xfu];",
                     "return NVM_MAP_ENTRY * 9u;"),
}
rc = 0
for label, (old, new) in PLANTS.items():
    if old and text.count(old) != 1:
        print(f"{label}: anchor count {text.count(old)}"); rc = 2; continue
    sub = work / label; sub.mkdir(exist_ok=True)
    bench = t.make_bench(cfg, sub, text.replace(old, new) if old else text)
    got = t.grade(bench)
    print(f"{label}: {len(got)} finding(s)" + (f"; first: {got[0][:200]}" if got else ""))
sys.exit(rc)
