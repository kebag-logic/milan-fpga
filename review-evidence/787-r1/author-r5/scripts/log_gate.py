"""log_gate.py <repo> <label=log>...: the #607 implementation-log check on each route log.

Calls the shipping check itself, `sw/litex/clock_constraints.check_implementation_log`, from the clean clone, on
each Vivado log; prints one verdict line per log, labelled (no host path), and exits 1 if any log is refused.
The check quarantines *.bit files beside a refused log; the baseline flow writes none."""
import sys
from pathlib import Path

repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "sw/litex"))
from clock_constraints import check_implementation_log  # noqa: E402

bad = 0
for arg in sys.argv[2:]:
    label, path = arg.split("=", 1)
    path = Path(path)
    lines = sum(1 for _ in path.open(errors="replace")) if path.exists() else 0
    try:
        check_implementation_log(path)
        print(f"#607 {label}: PASS, {lines} log lines, no 12-4739, 20-1307 or 12-5201 diagnostics")
    except (OSError, RuntimeError) as error:
        bad += 1
        print(f"#607 {label}: REFUSED: {str(error).replace(str(path.parent), '<run>')}")
sys.exit(1 if bad else 0)
