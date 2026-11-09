"""Probe: the 32x32 simulation config with the shipping 1x1 TDM8 audio interface (8 physical channels each way,
loopback lane on) instead of the 8x8's TDM32, built by the tree's builder into a scratch directory; prints the
legacy AEM ROM size against the 16-bit store, the packed image and the outcome.
usage: python3 -I probe_tdm8_32x32.py TREE SCRATCH"""
import sys, yaml, json
from pathlib import Path
tree, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "sw/builder"))
import endstation_builder as eb
a = yaml.safe_load((tree / "configs/endstation_ax7101_32x32.yaml").read_text())
t = yaml.safe_load((tree / "configs/endstation_ax7101_1x1_tdm8.yaml").read_text())
a["audio_interface"] = t["audio_interface"]
a["entity"]["name"] = "Milan FPGA 32x32 TDM8 probe"
cfgp = scratch / "endstation_probe_32x32_tdm8.yaml"
cfgp.write_text(yaml.safe_dump(a))
try:
    r = eb.build(str(cfgp), str(scratch / "out"))
    rom = Path(r["paths"]["aem_rom_svh"]).read_text() if "aem_rom_svh" in r["paths"] else ""
    import re
    m = re.search(r"AEM_ROM_BYTES_C = (\d+)", rom)
    print("built; legacy AEM ROM bytes:", m.group(1) if m else "not written", "| paths:", sorted(r["paths"]))
except Exception as exc:
    print("REFUSED:", type(exc).__name__, str(exc)[:600])
