#!/usr/bin/env python3
"""R226-2: how well the new controls resist deletion (disposable copies only).

Usage: python3 -B maintenance.py <tree-root> <outdir>
M1 empties _OTHER_NAMES; M2 drops "xmp" from it; M3 deletes the six
I440-E-other-* label rows; M4 deletes one of them. Each edit must match once.
Both self-tests run on a fresh copy of <tree-root>/scripts per case.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

src = Path(sys.argv[1]).resolve() / "scripts"
out = Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
F = "gen_toc_closer_cases.py"
ROWS = ('        ("I440-E-other-div", "<pre>\\n</div>\\n", 1, 0),\n'
        '        ("I440-E-other-title", "<pre>\\n</title>\\n", 1, 0),\n'
        '        ("I440-E-other-xmp", "<pre>\\n</xmp>\\n", 1, 0),\n'
        '        ("I440-E-other-div-inline", "<pre>x</div>\\n", 1, 0),\n'
        '        ("I440-E-other-title-inline", "<pre>x</title>\\n", 1, 0),\n'
        '        ("I440-E-other-xmp-inline", "<pre>x</xmp>\\n", 1, 0),\n')
ONE = '        ("I440-E-other-xmp-inline", "<pre>x</xmp>\\n", 1, 0),\n'
CASES = [
    ("M1-empty-other-names", '_OTHER_NAMES = ("div", "title", "xmp")', "_OTHER_NAMES = ()"),
    ("M2-drop-xmp-from-other-names", '_OTHER_NAMES = ("div", "title", "xmp")', '_OTHER_NAMES = ("div", "title")'),
    ("M3-delete-six-label-rows", ROWS, ""),
    ("M4-delete-one-label-row", ONE, ""),
]
records = []
for cid, old, new in CASES:
    with tempfile.TemporaryDirectory(prefix="r226-2.maint.") as tmp:
        dst = Path(tmp) / "scripts"
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
        text = (dst / F).read_text()
        assert text.count(old) == 1, (cid, text.count(old))
        (dst / F).write_text(text.replace(old, new))
        rec = {"id": cid}
        for script in ("gen_toc.py", "check_em_dash.py"):
            res = subprocess.run([sys.executable, "-B", str(dst / script), "--selftest"],
                                 capture_output=True, text=True, cwd=tmp, timeout=900)
            log = res.stdout + res.stderr
            (out / f"{cid}.{script}.log").write_text(log + f"\nexit={res.returncode}\n")
            rec[script] = {"exit": res.returncode,
                           "tail": [l for l in log.splitlines() if l.strip()][-2:]}
        records.append(rec)
        print(cid, json.dumps({k: v for k, v in rec.items() if k != "id"}))
(out / "results.json").write_text(json.dumps(records, indent=1) + "\n")
