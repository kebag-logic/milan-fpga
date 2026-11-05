#!/usr/bin/env python3
"""For each builder output dir under argv[2]: regenerate the gPTP ROM from the
MAC the firmware words carry (boot_policy.fabric_constants over that dir's
overlay and lwsrp table) at the milan clock and priority1 the build used,
and require byte-identity with the builder's gptp_ucode.hex. Then flip the
MAC by one bit and require a DIFFERENT ROM (the comparison can fail).
Usage: python3 -I gptp_rom_vs_fw_mac.py <repo> <builder out dir> <work dir>"""
import json, subprocess, sys
from pathlib import Path
repo, outdir, work = map(Path, sys.argv[1:4])
sys.path.insert(0, str(repo / "sw" / "litex"))
import boot_policy
gen = repo / "gptp-processor/hdl/ucode/gen_gptp_ucode.py"
work.mkdir(parents=True, exist_ok=True)
bad = 0
for d in sorted(p for p in outdir.iterdir() if (p / "aem_overlay.json").is_file()):
    rom = d / "gptp_ucode.hex"
    if not rom.is_file():
        print(f"NOROM {d.name}"); continue
    w = boot_policy.fabric_constants(json.loads((d / "aem_overlay.json").read_text()),
                                     json.loads((d / "lwsrp_table.json").read_text()))
    mac = int.from_bytes(w["MILAN_STATION_MAC_LO"].to_bytes(4, "little")
                         + w["MILAN_STATION_MAC_HI"].to_bytes(2, "little"), "big")
    argv = json.loads((d / "soc_params.json").read_text())["argv"]
    clk = int(float(argv[argv.index("--milan-clk-freq") + 1]))
    src = json.loads((d / "soc_params.json").read_text())["_source_config"]
    import yaml
    p1 = (yaml.safe_load(open(repo / src)) or {}).get("gptp", {}).get("priority1", 248)
    res = []
    for m in (mac, mac ^ 1 << 8):
        o = work / f"{d.name}_{m:012x}.hex"
        subprocess.run([sys.executable, str(gen), "-o", str(o), "--mac", f"0x{m:012x}",
                        "--p1", str(p1), "--clk-hz", str(clk)], check=True, capture_output=True)
        res.append(o.read_bytes() == rom.read_bytes())
    ok = res == [True, False]
    bad += not ok
    print(f"{'SAME' if ok else 'FAIL'} {d.name}: fw MAC {mac:012x}, clk {clk}, p1 {p1}; "
          f"ROM==regen(fw MAC) {res[0]}, ROM==regen(MAC^0x100) {res[1]}")
sys.exit(1 if bad else 0)
