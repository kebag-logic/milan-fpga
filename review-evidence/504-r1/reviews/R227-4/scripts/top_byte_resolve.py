#!/usr/bin/env python3
"""R227-4: ask the resolver (alone) where each function in a compiled
assembly file stores. Usage: top_byte_resolve.py <sw/builder dir> <asm>"""
import json
import sys
sys.path.insert(0, sys.argv[1])
import test_builder as tb  # noqa: E402
functions = tb.rv32_functions(open(sys.argv[2], encoding="utf-8").read())
for name in ("frame_top_byte", "static_top_byte", "frame_one_past",
             "static_one_past"):
    run = tb.rv32_run(functions[name], {})
    print(json.dumps({"function": name, "stores": [
        repr(address) if not isinstance(address, int) else hex(address)
        for _at, (address, _v) in run["stores"]]}))
