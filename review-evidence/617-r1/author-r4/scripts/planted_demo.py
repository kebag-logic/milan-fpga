"""Grade a mutant whose edit plants a syntax error in the dp leg's datapath, through a suite's own
mutants.py grade_mutant(): what the arm prints for a build that fails."""
import importlib.util, sys, tempfile
from pathlib import Path
suite = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("cc_mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec); sys.argv = [str(suite / "mutants.py")]; spec.loader.exec_module(m)
edit = (("  logic media_tick_q_r;", "  logic media_tick_q_r  planted_break;"),)
with tempfile.TemporaryDirectory(prefix="planted-", dir="$VALIDATION_STORAGE/617-a434-work/tmp") as td:
    m.grade_mutant("dp", Path(td), "planted build break (a syntax error in the datapath)", edit, m.TORN)
