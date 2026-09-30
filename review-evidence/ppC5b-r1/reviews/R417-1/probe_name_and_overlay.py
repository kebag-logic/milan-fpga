#!/usr/bin/env python3
"""Probe C (reviewer-owned, disposable): does a current-value overlay program
(E_RDESCCD) also carry a name SET_NAME stored?

The new overlay programs copy the descriptor prefix (which holds object_name
@4..@67) from the store's line with COPY_BUF, relying on the store having
patched the name table into the line at locate time, as E_RDESC does. No
section combines SET_NAME with a current-value SET on the same descriptor.
This adds ONE arm to a scratch copy of section AX, after RD1 (CLOCK_DOMAIN 0's
clock source is 1 there): the holder renames CLOCK_DOMAIN 0, then
READ_DESCRIPTOR of it must carry BOTH the new name @4 and clock_source_index 1
@70, byte-exact. Head RTL, aecp-dispatch target.
Usage: probe_name_and_overlay.py <clone> <scratch-dir> <verilator>
"""
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
sim = scratch / "tb" / "pp_top" / "sim_main.cpp"
s = sim.read_text()
anchor = "    rd_after_each_set();\n  }\n};\n"
assert s.count(anchor) == 1
add = (
    "    rd_after_each_set();\n"
    "    {  // PROBE: a renamed CLOCK_DOMAIN whose clock source is also set\n"
    "      const auto nm = NamePhase::name64(\"R417 probe name\");\n"
    "      ++seq;\n"
    "      const auto sn = ask(AEM_SET_NAME, NamePhase::name_body(0x0024, 0, 0, CFGIX, nm));\n"
    "      CHECK(st(sn) == AECP_SUCCESS, \"PROBE SET_NAME on CLOCK_DOMAIN 0 served (status %d)\",\n"
    "            st(sn));\n"
    "      auto d = image_desc(CFGIX, 0x0024, 0);\n"
    "      std::copy(nm.begin(), nm.end(), d.begin() + 4);\n"
    "      putbe(&d[70], 1, 2);\n"
    "      ++seq;\n"
    "      const auto r = ask(AEM_READ_DESCRIPTOR, rdesc(CFGIX, 0x0024, 0));\n"
    "      std::vector<uint8_t> pl(4, 0);\n"
    "      pl.insert(pl.end(), d.begin(), d.end());\n"
    "      const auto w = want(CTLR_MAC, CTLR_EID, AECP_SUCCESS, AEM_READ_DESCRIPTOR, pl);\n"
    "      CHECK(r == w, \"PROBE READ_DESCRIPTOR CLOCK_DOMAIN 0 carries the new name AND \"\n"
    "            \"clock_source_index 1, byte-exact\");\n"
    "      if (!r.empty() && r != w) { dump(\"got\", r); dump(\"exp\", w); }\n"
    "    }\n"
    "  }\n};\n")
s = s.replace(anchor, add)
sim.write_text(s)
bench = scratch / "tb" / "pp_top"
r = subprocess.run(["make", "-C", str(bench), "aecp-dispatch", "VERILATOR=" + verilator],
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
(scratch / "probe.log").write_text(r.stdout)
print(f"make rc={r.returncode}")
for line in r.stdout.splitlines():
    if line.startswith(("PROBE", "FAIL:", "AX:", "A5b+M9", "[build")) or "error" in line:
        print(line)
