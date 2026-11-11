"""Run sw/builder/test_builder.py from the current directory with its hard-coded
native RV32 compiler path mapped to a pinned compiler, recording every mapped
argv. Usage: builder_pinned_cc.py <pinned-gcc> <test_builder args...>"""
import json
import os
import runpy
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

pinned = sys.argv[1]
native = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
records = Path(os.environ.get("CC_MAP", "builder_cc_map.jsonl")).resolve()
real_run = subprocess.run


def mapped_run(args, *positional, **keyword):
    if isinstance(args, (list, tuple)) and args and str(args[0]) == native:
        actual = [pinned, *args[1:]]
        result = real_run(actual, *positional, **keyword)
        with records.open("a") as fh:
            fh.write(json.dumps({"requested": list(map(str, args)), "executed": actual,
                                 "exit_code": result.returncode}) + "\n")
        return result
    return real_run(args, *positional, **keyword)


print(f"compiler mapping: {native} -> {pinned}", flush=True)
sys.argv = ["sw/builder/test_builder.py", *sys.argv[2:]]
with patch("subprocess.run", mapped_run):
    runpy.run_path("sw/builder/test_builder.py", run_name="__main__")
