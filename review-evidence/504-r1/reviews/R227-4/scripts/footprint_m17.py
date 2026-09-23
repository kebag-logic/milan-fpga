#!/usr/bin/env python3
"""R227-4: re-measure R227-3-S1 M17 (the footprint's last word computed one
byte short) at the exact head. Imports a tree's test_builder, optionally
applies the M17 edit to the imported function's source in memory, and
reports the words a misaligned `sw` at X-2 (the shipped class probe) and at
X-3 are judged at. Usage: footprint_m17.py <sw/builder dir> [--m17]"""
import json
import sys
sys.path.insert(0, sys.argv[1])
import test_builder as tb  # noqa: E402

if "--m17" in sys.argv:
    source = open(tb.__file__, encoding="utf-8").read()
    old = "((address + width - 1) & ~3) + 4, 4)"
    assert source.count(old) == 1
    namespace = dict(vars(tb))
    start = source.index("def rv32_footprint_words(")
    end = source.index("def _rv32_forget_overlap(")
    exec(source[start:end].replace(old, "((address + width - 2) & ~3) + 4, 4)"),
         namespace)
    tb.rv32_footprint_words = namespace["rv32_footprint_words"]
window = 0x9000_0000
for label, base in (("shipped probe: misaligned sw at X-2", window - 2),
                    ("odd offset: misaligned sw at X-3", window - 3),
                    ("odd offset: misaligned sw at X-1", window - 1)):
    run = tb.rv32_run(tb.rv32_functions(
        f"probe:\n\tli a4,{tb._rv32_s32(base)}\n\tsw a5,0(a4)\n\tret\n")["probe"], {})
    words = [hex(address) for _at, (address, _v) in run["stores"]]
    print(json.dumps({"variant": "M17" if "--m17" in sys.argv else "head",
                      "probe": label, "words": words,
                      "reaches_window_word": hex(window) in words}))
