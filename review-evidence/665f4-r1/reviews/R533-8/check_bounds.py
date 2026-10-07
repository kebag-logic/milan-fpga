#!/usr/bin/env python3
"""Independently evaluate the compiled pass macros and recompute the prose table."""
import json
from pathlib import Path
import shutil
import subprocess
import sys

root = Path.cwd()
packet = Path(__file__).resolve().parent
scratch = packet / "scratch/bounds"
scratch.mkdir(exist_ok=True)
code = r'''
#include <stdio.h>
#include "ctrl_app.h"
int main(void) {
    printf("%u %u %u %u %u %u\n", ADP_MBX_PASS_MAX, ACMP_MBX_PASS_MAX,
           MAAP_MBX_PASS_MAX, SRP_MBX_PASS_MAX,
           CTRL_LOOP_EVENTS_PER_PASS * (MBX_EV_WORDS + 2u), CTRL_APP_PASS_MAX);
    return 0;
}
'''
(scratch / "macros.c").write_text(code)
values = []
for interfaces in (1, 2):
    variant = scratch / f"ctrl-if{interfaces}"
    shutil.copytree(root / "sw/firmware/ctrl", variant, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__"))
    generated = scratch / f"gen-if{interfaces}"
    subprocess.run([sys.executable, "sw/mailbox/gen_mailbox.py", "--variant-interfaces",
                    str(interfaces), "--out", str(generated)], check=True)
    shutil.copyfile(generated / "mbx_contract.h", variant / "mbx/mbx_contract.h")
    include = ["-I" + str(variant / name) for name in
               ("app", "acmp", "adp", "loop", "maap", "mbx", "port")]
    binary = scratch / f"macros-if{interfaces}"
    subprocess.run(["cc", "-std=c11", *include, str(scratch / "macros.c"),
                    "-o", str(binary)], check=True)
    adp, acmp, maap, srp, shared, total = map(int, subprocess.check_output([str(binary)]).split())
    assert total == acmp + maap + srp - 2 * shared
    assert total == (3128 if interfaces == 1 else 3977)
    values.append(dict(interfaces=interfaces, adp=adp, acmp_including_adp=acmp,
                       maap=maap, srp=srp, shared_event_reads=shared, total=total))
doc = (root / "docs/design/MAILBOX_SPLIT.md").read_text()
rows = []
for label, passes in (("event", 2), ("ACMP", 10), ("ADP", 21), ("owed response", 8)):
    accesses = [v["total"] * (passes + 1) for v in values]
    microseconds = [(1000000 // a) / 100 for a in accesses]
    rendered = f"{accesses[0]:,} / {accesses[1]:,} | {microseconds[0]:.2f} / {microseconds[1]:.2f} us"
    assert rendered in doc, rendered
    rows.append(dict(input=label, taken_by_pass=passes, accesses=accesses,
                     microseconds_per_access_for_10ms=microseconds))
assert "only the one-interface event envelope fits T_svc = 10 ms" in doc
assert "Retry after owed transmission commits and retained reception completes or expires." in (
    root / "sw/firmware/ctrl/srp/README.md").read_text()
print(json.dumps({"compiled_macros": values, "recomputed_table": rows,
                  "doc_table_matches": True, "R532_7_R1_exact_fix_present": True}, indent=2))
