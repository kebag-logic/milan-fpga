#!/usr/bin/env python3
"""usage: make_sweep_spec.py <head> <base> <out.json>: the full-native spec native-shards.py shards."""
import json, sys
head, base, out = sys.argv[1:4]
S = "<scratch>"
cmd = ["env",
       "PATH=<data>/tools/pinned-verilator-5.050:<data>/tools/sv2v-v0.0.12:<data>/scratch/a662/make43/bin:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
       "VERILATOR=<data>/tools/pinned-verilator-5.050/verilator",
       "TSN_GEN_ROOT=<home>/milan-fpga-management/tools/tsn-gen-deca300c",
       f"TMPDIR={S}/tmp-sweep",
       "MAKEFLAGS=-j4 --no-print-directory",
       "bash", "scripts/run_all_suites.sh", f"{S}/unused/logs", "--wait"]
json.dump(dict(cwd="<lanes>/843-gptp-pin", head=head, base=base, commands=[cmd]), open(out, "w"), indent=1)
open(out, "a").write("\n")
