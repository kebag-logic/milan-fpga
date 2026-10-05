#!/usr/bin/env python3
"""Run a SoC constructor, record its exact source list, stop before build."""
import json, pathlib, runpy, sys
from litex.soc.integration.builder import Builder
destination, entry = pathlib.Path(sys.argv[1]), sys.argv[2]
sys.argv = [entry, *sys.argv[3:]]
sys.path.insert(0, str(pathlib.Path(entry).parent))
def capture(self, *args, **kwargs):
    platform = self.soc.platform
    destination.write_text(json.dumps({"sources": platform.sources,
        "verilog_include_paths": platform.verilog_include_paths}, indent=2)+"\n")
    raise SystemExit(0)
Builder.build = capture
runpy.run_path(entry, run_name="__main__")
