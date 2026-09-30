#!/usr/bin/env python3
"""Probe B (reviewer-owned, disposable): the response-buffer reservation at a
561-byte descriptor line.

Copies hdl/, tb/common and tb/pp_top of the reviewed clone into a scratch
tree, then in the COPY only:
  * binds protocol_processor_top.DESC_LINE_BYTES_P to 561 in pp_top_wrap.sv
    (the floor the engine's new elaboration check accepts);
  * makes the bench's response-memory model record every strobed byte offset
    it is asked to write (relative to RESP_BASE_P) and print the highest one
    per AX sub-section.
Then builds the `aecp-dispatch` target (A5b + M9 + AX) and prints the log
lines of interest. The documented reservation (integrator guide, 07 section
3.3.2, the top's RESP_BASE_P banner) is 16 + DESC_LINE_BYTES_P = 577 bytes.
Usage: probe_line561.py <clone> <scratch-dir> <verilator>
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

clone, scratch, verilator = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
if scratch.exists():
    shutil.rmtree(scratch)
for parts in (("hdl",), ("tb", "common"), ("tb", "pp_top")):
    shutil.copytree(clone.joinpath(*parts), scratch.joinpath(*parts),
                    ignore=shutil.ignore_patterns("obj_*", "*.hex", "__pycache__"))

wrap = scratch / "tb" / "pp_top" / "pp_top_wrap.sv"
w = wrap.read_text()
anchor = '      .UCODE_HEX_P  ("ucode.hex")\n  ) u_dut ('
assert w.count(anchor) == 1
w = w.replace(anchor, '      .UCODE_HEX_P  ("ucode.hex"),\n      .DESC_LINE_BYTES_P (561)\n  ) u_dut (')
wrap.write_text(w)

sim = scratch / "tb" / "pp_top" / "sim_main.cpp"
s = sim.read_text()
a1 = "  uint64_t rm_writes = 0;\n"
assert s.count(a1) == 1
s = s.replace(a1, a1 + "  int64_t probe_max_wr = -1;  // PROBE: highest strobed byte offset written\n")
a2 = "            if (k < rmem.size()) rmem[k] = uint8_t(rm_wdata >> (56 - 8 * i));\n"
assert s.count(a2) == 1
s = s.replace(a2, "            if (int64_t(k) > probe_max_wr) probe_max_wr = int64_t(k);\n" + a2)
# report the high-water mark after each AX sub-section
for fn in ("rd_before_any_set", "lk_the_entity_locked_arm", "ov_responses_above_cdl_524",
           "pg_the_page", "rd_after_each_set"):
    pat = f"    {fn}();\n"
    assert s.count(pat) == 1, fn
    s = s.replace(pat, pat + f'    printf("PROBE after {fn}: max response-buffer byte offset written = %lld '
                              f'(reservation 16 + 561 = 577 bytes: offsets 0..576)\\n", '
                              f"(long long)io.probe_max_wr);\n    io.probe_max_wr = -1;\n")
# AX's configuration-1 AUDIO_MAP 0 is 576 bytes, longer than a 561-byte line,
# which the store rightly refuses at boot; shrink it to 536 bytes (66 records)
# so the image is legal at this line. Only OV1/OV5 depend on it.
a3 = "      big_audio_map(0, 71),          // 576 B, the line: cdl 592, frame 618\n"
assert s.count(a3) == 1
s = s.replace(a3, "      big_audio_map(0, 66),          // PROBE: 536 B at a 561-byte line\n")
a4 = "        {CFG1, 0x0017, 1, 576, 0xFFFF, 576, 0},\n"
assert s.count(a4) == 1
s = s.replace(a4, "        {CFG1, 0x0017, 1, 536, 0xFFFF, 536, 0},\n")
sim.write_text(s)

bench = scratch / "tb" / "pp_top"
r = subprocess.run(["make", "-C", str(bench), "aecp-dispatch", "VERILATOR=" + verilator],
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
(scratch / "probe.log").write_text(r.stdout)
print(f"make rc={r.returncode}")
for line in r.stdout.splitlines():
    if (line.startswith("PROBE") or line.startswith("AX:") or line.startswith("A5b+M9")
            or re.match(r"FAIL: (PG|OV)", line) or "%Error" in line):
        print(line)
