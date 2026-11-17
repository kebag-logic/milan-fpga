#!/usr/bin/env python3
"""Show that the split image's fabric gPTP engine ROM, as the builder writes it,
is the generator's image for clockAccuracy 0x22 and the #840 station MAC, and
differs from the image with 0xFE or with another MAC.

Usage: gptp_rom_identity.py <tree> <config.yaml> <built gptp_ucode.hex> <scratch dir>
"""
import hashlib
import subprocess
import sys
from pathlib import Path

tree, cfg_path, built, scratch = (Path(a).resolve() for a in sys.argv[1:5])
sys.path.insert(0, str(tree / "sw" / "builder"))
import endstation_builder as eb  # noqa: E402

cfg = eb.load_config(str(cfg_path)) if hasattr(eb, "load_config") else None
if cfg is None:
    sys.exit("no load_config in the builder")
args = eb.gptp_ucode_args(cfg)
print("builder args:", " ".join(args))
gen = tree / "gptp-processor" / "hdl" / "ucode" / "gen_gptp_ucode.py"


def image(extra_args, name):
    out = scratch / name
    subprocess.run([sys.executable, "-B", str(gen), "-o", str(out), *extra_args], check=True,
                   capture_output=True, text=True)
    return hashlib.sha256(out.read_bytes()).hexdigest()


def replace(a, key, val):
    a = list(a)
    a[a.index(key) + 1] = val
    return a


h_built = hashlib.sha256(built.read_bytes()).hexdigest()
h_22 = image(replace(args, "--clock-accuracy", "0x22"), "g22.hex")
h_fe = image(replace(args, "--clock-accuracy", "0xFE"), "gFE.hex")
h_mac = image(replace(args, "--mac", "0x020000000001"), "gmac_other.hex")
print("built          ", h_built)
print("gen 0x22 #840  ", h_22)
print("gen 0xFE #840  ", h_fe)
print("gen 0x22 other ", h_mac)
ok = (h_built == h_22 and h_built != h_fe and h_built != h_mac
      and "--clock-accuracy" in args and args[args.index("--clock-accuracy") + 1] == "0x22"
      and args[args.index("--mac") + 1] == "0x024b4c4b4c01")
print("RESULT", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
