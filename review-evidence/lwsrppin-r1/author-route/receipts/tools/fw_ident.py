"""fw_ident.py <side dir> <repo>: what firmware the side's routed image embeds.

Prints the image manifest's ctrl_firmware record, the sha256 of the linked ELF (route8/image), of the copy the recipe's
--ctrl-firmware path names in the repo, of each rom bank init and the export's top Verilog, the lwSRP gitlink the
repo is at, and the .text bytes the link map assigns to lwSRP's mrp_mad.o (the pin adds 60 B of .text).
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

side, repo = Path(sys.argv[1]), Path(sys.argv[2])
w = side / "route8"


def sha(path: Path) -> str:
    """The file's sha256, hex."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


man = json.loads((w / "split/image_manifest.json").read_text())
print("manifest ctrl_firmware:", json.dumps(man["ctrl_firmware"]))
print("manifest bitstream:", json.dumps(man.get("bitstream")))
print("image ELF   ", sha(w / "image/ctrl_app.elf"), w / "image/ctrl_app.elf")
fw = repo / "sw/builder/out/endstation_ax7101_8x8/ctrl_app.elf"
print("recipe ELF  ", sha(fw), fw)
for p in sorted((w / "split/gateware").glob("alinx_ax7101_rom_bank*.init")) + [w / "split/gateware/alinx_ax7101.v"]:
    print("export      ", sha(p), p.name, p.stat().st_size)
git = ["git", "-C", str(repo)]
print("repo HEAD   ", subprocess.run(git + ["rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip())
print("lwSRP HEAD  ", subprocess.run(git[:2] + [str(repo / "third_party/lwSRP"), "rev-parse", "HEAD"],
                                     capture_output=True, text=True).stdout.strip())
text = 0
lines = (w / "image/ctrl_app.map").read_text().splitlines()
for i, line in enumerate(lines):
    joined = line if "mrp_mad.o" in line else ""
    if not joined and i + 1 < len(lines) and "mrp_mad.o" in lines[i + 1] and line.strip().startswith(".text"):
        joined = line + " " + lines[i + 1]
    m = re.match(r"\s*(\.text\S*)\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+\S*mrp_mad\.o", joined)
    if m:
        text += int(m[3], 16)
print("mrp_mad.o .text bytes", text)
