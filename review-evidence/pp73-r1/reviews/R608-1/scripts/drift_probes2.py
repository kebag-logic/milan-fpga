#!/usr/bin/env python3
"""Second probe set: table defects the generator also reads, applied to the FILE
(end to end), compared with the self-test's in-memory form.
usage: python3 -I drift_probes2.py <clean-head-export> <scratch-dir> <receipt-dir>"""
import json, shutil, subprocess, sys
from pathlib import Path
SRC, SCRATCH, OUT = (Path(a).resolve() for a in sys.argv[1:4])
TABLE = "hdl/aecp/ucode/aecp_commands.json"
def tbl(fn):
    def go(r):
        p = r / TABLE; t = json.loads(p.read_text(encoding="utf-8")); fn(t)
        p.write_text(json.dumps(t, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return go
def cmd(t, n): return next(c for c in t["commands"] if c["name"] == n)
GATE = ["python3", "-B", "scripts/check_aecp_commands.py"]
PROBES = [
  ("p5c_aem_message_AA", tbl(lambda t: cmd(t, "GET_NAME").update(message="AA")), GATE),
  ("p5d_aem_message_AA_write", tbl(lambda t: cmd(t, "GET_NAME").update(message="AA")), GATE + ["--write"]),
  ("p5e_mvu_message_AAU_as_selftest", tbl(lambda t: cmd(t, "GET_MILAN_INFO").update(message="AAU")), GATE),
  ("p8_entry_unplaced_file", tbl(lambda t: cmd(t, "GET_CLOCK_SOURCE")["entries"].append("SCFGRUN2")), GATE),
  ("p9_status_code_NO_RESOURCES_9_file", tbl(lambda t: t["status_codes"]["NO_RESOURCES"].update(code=9)), GATE),
]
OUT.mkdir(parents=True, exist_ok=True); rows = []
for name, fn, argv in PROBES:
    d = SCRATCH / name
    if d.exists(): shutil.rmtree(d)
    shutil.copytree(SRC, d, symlinks=True); fn(d)
    r = subprocess.run(argv, cwd=d, capture_output=True, text=True)
    (OUT / f"{name}.txt").write_text(f"probe: {name}\ncommand: {' '.join(argv)}\nrc: {r.returncode}\n--- stdout\n{r.stdout}--- stderr\n{r.stderr}", encoding="utf-8")
    rows.append(f"{name}\trc={r.returncode}")
(OUT / "SUMMARY2.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8"); print("\n".join(rows))
