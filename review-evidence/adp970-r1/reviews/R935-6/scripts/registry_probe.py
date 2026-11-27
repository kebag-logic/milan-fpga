"""Static half of ctrl_configs.held(): every checkout module naming the firmware tree that is a program
must be in BUILDERS, PART_OF, OUTSIDE or SUITES. Usage: python3 -I registry_probe.py <checkout>."""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_configs as c  # noqa: E402
names = {b.path for b in c.BUILDERS}
bad, nonprog = [], []
texts = c.builder_texts()
for path, text in texts.items():
    n = c.rel(path)
    if n in names or n in c.OUTSIDE or n in c.SUITES or n in c.PART_OF:
        continue
    (bad if c.program(path, text) else nonprog).append(n)
stale = sorted(k for k in list(c.OUTSIDE) + list(c.SUITES) if not (root / k).exists())
print(f"builders-by-text {len(texts)}; OUTSIDE {len(c.OUTSIDE)}; SUITES {len(c.SUITES)}; PART_OF {len(c.PART_OF)}")
print("UNLISTED PROGRAMS:", bad or "none")
print("non-program, must compile in capture:", len(nonprog))
print("OUTSIDE/SUITES keys with no file:", stale or "none")
for k in ("tb/verilator/ctrl_service_budget/model_counts.py", "scripts/ci_fast_legs_selftest.py"):
    print("listed" if k in c.OUTSIDE else "MISSING", k, "| in builders-by-text:", any(c.rel(p) == k for p in texts))
sys.exit(1 if bad or stale else 0)
