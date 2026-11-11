"""sweep_spec.py <head> <out.json> <logs>: the full-sweep spec for native-shards.py: the pinned tools, Make's
--no-print-directory, scratch TMPDIR, cwd the lane (each shard clones it at <head>)."""
import json
import sys

head, out, logs = sys.argv[1:4]
tools = ("<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<scratch-root>/a662/make43/bin:"
         "<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin")
gt = "<tools>/gtest-1.14.0"
cmd = ["env", f"PATH={tools}", "VERILATOR=<tools>/pinned-verilator-5.050/verilator",
       "TSN_GEN_ROOT=<mgmt>/tools/tsn-gen-deca300c",
       f"PKG_CONFIG_PATH={gt}/lib/pkgconfig", f"LD_LIBRARY_PATH={gt}/lib",
       "TMPDIR=<scratch>/tmp-sweep", "MAKEFLAGS=-j4 --no-print-directory", "PYTHONHASHSEED=0",
       "bash", "scripts/run_all_suites.sh", logs, "--wait"]
json.dump({"cwd": "<lane>", "head": head, "base": "46c971fa", "commands": [cmd]},
          open(out, "w"), indent=1)
print(out)
