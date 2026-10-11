#!/usr/bin/env python3
"""The real split SoC export of a linked probe with its reset PT_LOAD emptied, cut to one word, or kept."""
import json
import struct
import sys
from pathlib import Path

tree, out = map(Path, sys.argv[1:])
out.mkdir(parents=True)
sys.path.insert(0, str(tree / "sw/litex"))
import ctrl_memory as cm  # noqa: E402
import test_ctrl_memory as test  # noqa: E402

cc = test.fw_rv32.compiler()
assert cc is not None, "RV32 compiler required"
(out / "linked").mkdir()
firmware = test.link(cc, out / "linked", (tree / "sw/firmware/ctrl/plat/ctrl_split.ld").read_text())
raw = firmware.read_bytes()
original = cm.read_elf(firmware)
field = test.filesz_at(raw, original.entry)
want = [f"{w:08x}" for w in cm.rom_words(original)[:8]]
for label, size in (("valid control", None), ("reset segment emptied", 0), ("reset segment cut to one word", 4)):
    data = bytearray(raw)
    if size is not None:
        struct.pack_into("<I", data, field, size)
    path = out / (label.replace(" ", "-") + ".elf")
    path.write_bytes(bytes(data))
    result = test.soc_case(out, label, ["--ctrl-mailbox", "--ctrl-firmware", str(path)], None)
    inits = sorted(result["out"].glob("gateware/*_rom_bank*.init"),
                   key=lambda p: int(p.stem.rsplit("bank", 1)[1]))
    words = [w for p in inits for w in p.read_text().split()][:8]
    print(json.dumps({"case": label, "rc": result["rc"], "rule": result.get("rule"),
                      "refusal": result.get("refusal"), "error": result.get("error"),
                      "verilog": len(result["verilog"]), "init_files": len(result["inits"]),
                      "first_eight_rom_words": words, "reset_words_kept": words == want}))
