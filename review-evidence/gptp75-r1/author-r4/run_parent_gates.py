"""Run the six assigned consumer gates against the committed local gitlink."""
from pathlib import Path
import subprocess
import sys

out = Path(__file__).resolve().parent
parent = "$LANES/gptp75-parent-consumer"
gates = [
    ("parent-cpp", ["python3", "scripts/check_cpp_idiom.py"]),
    ("parent-python", ["python3", "scripts/check_py_idiom.py"]),
    ("parent-xvlog", ["python3", "scripts/xvlog_gate.py", "--check"]),
    ("parent-source-lists", ["python3", "scripts/check_rtl_source_lists.py"]),
    ("parent-builder", ["python3", "sw/builder/test_builder.py"]),
    ("parent-shadow", ["make", "-C", "tb/verilator/gptp_shadow", "-j8"]),
]
for label, command in gates:
    subprocess.run([sys.executable, str(out / "run_gate.py"), label, parent, *command], check=True, timeout=10900)
