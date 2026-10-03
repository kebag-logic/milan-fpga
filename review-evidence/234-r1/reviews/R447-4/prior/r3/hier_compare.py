#!/usr/bin/env python3
"""Compare pp_baseline_rank.hierarchy() output of two revisions on real reports, byte for byte.

Usage: hier_compare.py <old pp_baseline_rank.py> <new pp_baseline_rank.py> <report>...
Prints one line per report: sha256 of the old and new JSON dump, and SAME or DIFF.
"""
import hashlib, importlib.util, json, sys
from pathlib import Path

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

old, new = load(sys.argv[1], "old_rank"), load(sys.argv[2], "new_rank")
bad = 0
for report in sys.argv[3:]:
    outs = []
    for module in (old, new):
        try:
            rows = module.hierarchy(Path(report))
            text = json.dumps(rows, sort_keys=False)
            try:
                text += json.dumps(module.ranking(rows, "KL_pp_shadow" if "ooc" in report else "alinx_ax7101/milan_datapath/pp_shadow"))
            except ValueError as error:
                text += f"ranking ValueError {error}"
        except ValueError as error:
            text = f"ValueError {error}"
        outs.append(hashlib.sha256(text.encode()).hexdigest()[:16] + f" rows={text.count('LUT_rank') if False else len(text)}")
    same = outs[0] == outs[1]
    bad += not same
    print(f"{'SAME' if same else 'DIFF'} old={outs[0]} new={outs[1]} {report.split('234-a516/')[-1]}")
print(f"reports {len(sys.argv) - 3} differing {bad}")
sys.exit(1 if bad else 0)
