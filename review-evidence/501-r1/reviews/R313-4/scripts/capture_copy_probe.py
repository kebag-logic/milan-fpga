#!/usr/bin/env python3
"""Reviewer probe (R313-2): what does one capture copy under the hold today?

Usage: python3 capture_copy_probe.py <tree-copy>

SAVED_STATE_SNAPSHOT_OWNERSHIP.md section 18 and UNRESOLVED 6 (this head)
say "Today only BINDING is materialized; maps are not copied yet." This
probe measures the shipping firmware's capture copy. It takes the tree's own
host bench (sw/firmware/nvm_hosttest/test_nvm_firmware.py), instruments a
COPY of milan_baremetal.c in memory only (per-record copy counters inside
nvm_capture(), printed once after the copy loop), builds it for each AX7101
shape and runs "--boot --uart 'milan_nvm commit'". No tracked file is
written; builds go to a temp dir.
"""
import re
import sys
import tempfile
from pathlib import Path

T = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(T / "sw/firmware/nvm_hosttest"))
sys.path.insert(0, str(T / "scripts"))
import test_nvm_firmware as h  # noqa: E402

fw = h.FIRMWARE.read_text()
COPY = ("\t\tif (copy) {\n\t\t\tfor (i = off; i < NVM_AREA_RAW; ++i) {\n"
        "\t\t\t\tif (i >= next) {\n\t\t\t\t\tbreak;\n\t\t\t\t}\n"
        "\t\t\t\tNVM_STG[KLJ2_HDR + i] = NVM_IMG[KLJ2_HDR + i];\n")
assert fw.count(COPY) == 1, "copy loop not found exactly once"
fw = fw.replace(COPY, COPY + "\t\t\t\tr313_bytes[rec.id]++;\n")
ENDLOOP = "\t/* the copy's loads complete before the attest strobe leaves */\n"
assert fw.count(ENDLOOP) == 1
fw = fw.replace(ENDLOOP,
                "\t{ unsigned int t = 0, m = 0, n = 0, j;\n"
                "\t  for (j = 0; j < 256u; ++j) { t += r313_bytes[j]; if (r313_bytes[j]) n++;\n"
                "\t    if (j >= 0x70u && j < 0x80u) m += r313_bytes[j]; }\n"
                "\t  printf(\"R313PROBE copied_bytes=%u records=%u maps_out_bytes=%u"
                " area_raw=%u\\n\", t, n, m, (unsigned int)NVM_AREA_RAW); }\n" + ENDLOOP, 1)
SIG = "static struct nvm_cap nvm_capture(void)\n"
assert fw.count(SIG) == 1
fw = fw.replace(SIG, "static unsigned int r313_bytes[256];\n" + SIG, 1)

rc = 0
with tempfile.TemporaryDirectory(prefix="r313cap.") as tmp:
    for stem in ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"):
        work = Path(tmp) / stem
        work.mkdir()
        bench = h.make_bench(T / "configs" / f"{stem}.yaml", work, fw)
        out, s, _ = h.run(bench, "--boot", "--uart", "milan_nvm commit")
        lines = [ln for ln in out.splitlines() if ln.startswith("R313PROBE")]
        print(f"{stem}: {lines[0] if lines else 'NO PROBE LINE'}; "
              f"arms={s.get('arms')} acks={s.get('acks')}")
        m = re.search(r"maps_out_bytes=(\d+)", lines[0]) if lines else None
        if not m:
            rc = 1
sys.exit(rc)
