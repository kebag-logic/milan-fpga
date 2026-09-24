from pathlib import Path
import subprocess
import sys

output = Path(__file__).resolve().parent
phase = sys.argv[1]
parent = "$LANES/pp113-parent-consumer"
commands = [
    ("cpp", ["python3", "scripts/check_cpp_idiom.py"]),
    ("python", ["python3", "scripts/check_py_idiom.py"]),
    ("xvlog", ["python3", "scripts/xvlog_gate.py", "--check"]),
    ("source-lists", ["python3", "scripts/check_rtl_source_lists.py"]),
    ("pp-srcs", ["python3", "scripts/pp_srcs.py", "--check", "--selftest"]),
    ("builder", ["python3", "sw/builder/test_builder.py"]),
    ("consumer", ["make", "-C", "tb/verilator/pp_shadow", "-j8"]),
]
failures = 0
for label, command in commands:
    rc = subprocess.run([sys.executable, str(output / "run_gate.py"),
                         phase + "-" + label, parent, *command],
                        timeout=15000, check=False).returncode
    failures += rc != 0
print(f"{phase}: {len(commands) - failures}/{len(commands)} gates passed", flush=True)
sys.exit(bool(failures))
