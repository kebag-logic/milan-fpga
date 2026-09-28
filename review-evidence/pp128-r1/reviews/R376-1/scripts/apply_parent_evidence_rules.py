#!/usr/bin/env python3
"""Apply the parent's measure_test_evidence.py detectors (loaded read-only by
path) to individual processor suite files. Usage: <gate.py> <file>..."""
import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("mte", sys.argv[1])
mte = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mte)
for f in sys.argv[2:]:
    p = Path(f)
    text, suffix = p.read_text(errors="replace"), mte.file_suffix(str(p))
    rel = "protocol-processor/" + "/".join(p.parts[-3:])
    print(f"{rel}: wall_clock={mte.uses_wall_clock(text, suffix)} "
          f"dut_source_reader={mte.reads_dut_source(text, suffix)} "
          f"disposition={'recorded' if rel in mte.DUT_READER_DISPOSITIONS else 'NONE'}")
