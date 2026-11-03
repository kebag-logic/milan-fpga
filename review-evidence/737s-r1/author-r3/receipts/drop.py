"""Copy the real leg receipts, dropping one named simulation's verdict row from one leg (control, #737)."""
import json, sys
from pathlib import Path
src, dst, leg, name = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
for n in range(3):
    data = json.loads((src / f"litex-leg-{n}.json").read_text())
    if n == leg and name:
        before = len(data["results"])
        data["results"] = [row for row in data["results"] if row["simulation"] != name]
        assert len(data["results"]) == before - 1
    (dst / f"litex-leg-{n}.json").write_text(json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n")
