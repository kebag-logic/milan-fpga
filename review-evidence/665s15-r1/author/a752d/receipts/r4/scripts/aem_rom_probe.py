"""The legacy AEM ROM (the builder's model check against the 16-bit store) at the three points, and at 32x32 with the
shipping 1x1 TDM8 audio interface in place of the 8x8's TDM32, everything else the 32x32 config's. Prints each
point's AEM_ROM_BYTES_C, descriptor count and AUDIO_CLUSTER count, or the refusal's words.
usage: python3 -I aem_rom_probe.py TREE SCRATCH"""
import re, sys, yaml
from pathlib import Path
tree, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "sw/builder"))
import endstation_builder as eb
a32 = yaml.safe_load((tree / "configs/endstation_ax7101_32x32.yaml").read_text())
t1 = yaml.safe_load((tree / "configs/endstation_ax7101_1x1_tdm8.yaml").read_text())
a32["audio_interface"] = t1["audio_interface"]
a32["entity"]["name"] = "Milan FPGA 32x32 TDM8 probe"
probe = scratch / "endstation_probe_32x32_tdm8.yaml"
probe.write_text(yaml.safe_dump(a32))
points = [("1x1/1if", tree / "configs/endstation_ax7101_1x1_tdm8.yaml"), ("8x8/2if", tree / "configs/endstation_ax7101_8x8.yaml"),
          ("32x32/2if", tree / "configs/endstation_ax7101_32x32.yaml"), ("32x32 on the 1x1 TDM8 interface", probe)]
for label, path in points:
    cfg = eb.load_config(str(path))
    overlay = eb.emit_aem_overlay(cfg)
    try:
        svh = eb.emit_aem_rom_svh(cfg, overlay)
        rom = re.search(r"AEM_ROM_BYTES_C\s*=\s*(\d+)", svh)
        print(f"{label}: AEM_ROM_BYTES_C {rom.group(1) if rom else 'absent'} of the 65536-byte store")
    except Exception as exc:
        print(f"{label}: REFUSED {type(exc).__name__}: {exc}")
