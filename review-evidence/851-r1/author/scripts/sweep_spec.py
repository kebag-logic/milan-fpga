"""sweep_spec.py <head> <out.json> <logs>: the full-sweep spec for native-shards.py: the pinned tools, Make's
--no-print-directory, scratch TMPDIR, cwd the lane (each shard clones it at <head>)."""
import json
import sys

head, out, logs = sys.argv[1:4]
tools = ("$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:"
         "$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin")
cmd = ["env", f"PATH={tools}", "VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator",
       "TSN_GEN_ROOT=$HOME/milan-fpga-management/tools/tsn-gen-deca300c",
       "TMPDIR=$VALIDATION_STORAGE/scratch/851-a744/tmp-sweep", "MAKEFLAGS=-j4 --no-print-directory",
       "bash", "scripts/run_all_suites.sh", logs, "--wait"]
json.dump({"cwd": "$LANES/851-pp-pin", "head": head, "base": "1eb5289d", "commands": [cmd]},
          open(out, "w"), indent=1)
print(out)
