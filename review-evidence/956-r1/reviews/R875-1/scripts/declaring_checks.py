"""Run declaring_outputs.checks() (the arm's self-test controls) from a checkout and report each (reviewer receipt)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]).resolve() / "tb/verilator/ctrl_service_budget"))
import declaring_outputs  # noqa: E402
rows = declaring_outputs.checks()
bad = [r for r in rows if not r[1]]
for name, ok, detail in rows:
    if 'order' in name or "Listener" in name or 'third notice' in name or "another output's notice" in name:
        print(("PASS " if ok else "FAIL ") + name)
print(f"declaring_outputs.checks: {len(rows)} checks, {len(bad)} failed")
sys.exit(1 if bad else 0)
