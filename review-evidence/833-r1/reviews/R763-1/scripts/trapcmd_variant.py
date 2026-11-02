#!/usr/bin/env python3
"""Make a copy of the shell-window control whose trap runs an external command.

Usage: trapcmd_variant.py SRC_SCRIPTS_DIR OUT_SCRIPTS_DIR
The trap becomes `sleep 1.5 && echo trapped > marker; exit 143`, so the marker
only appears if the trap's own child command is allowed to finish (the
production sweep's EXIT trap runs `rm`, an external command).
"""
import shutil, sys
from pathlib import Path
src, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for f in ("owned_process.py", "test_suite_cancellation.py", "process_test_support.py"):
    shutil.copyfile(src / f, out / f)
t = (out / "test_suite_cancellation.py").read_text()
old = """script = (f"trap 'echo trapped > \\"{marker}\\"; exit 143' TERM\\n\""""
new = """script = (f"trap 'sleep 1.5 && echo trapped > \\"{marker}\\"; exit 143' TERM\\n\""""
assert t.count(old) == 1, old
(out / "test_suite_cancellation.py").write_text(t.replace(old, new))
print("variant written")
