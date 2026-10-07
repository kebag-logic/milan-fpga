"""Emit both GMII capture placement fixtures WITHOUT the behavioural/structural gates.

Usage: <litex-python> -I emit_fixtures_unchecked.py <repo-at-head> <out-dir>
Used only to place the pre-patch (0007 reversed) receiver through the committed
driver, to see whether the compact fixture alone reproduces the original fragility.
"""
import runpy
import sys
from pathlib import Path

repo, out = Path(sys.argv[1]), Path(sys.argv[2])
mod = runpy.run_path(str(repo / "sw/litex/test_gmii_rx_capture.py"), run_name="probe")
out.mkdir(parents=True, exist_ok=True)
for defect, name in ((False, "capture"), (True, "reset_before_d")):
    (out / f"{name}.v").write_text(mod["convert_capture"](defect))
print("emitted", sorted(p.name for p in out.iterdir()))
