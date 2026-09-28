"""Complete record and integration checks after the parent bank."""
from pathlib import Path
import subprocess
import sys

out = Path(__file__).resolve().parent
commands = [
    ("final-rom-record", ["bash", "syn/yosys/ooc.sh", "--record-rom-digests"]),
    ("final-boot-freeze", ["python3", "sw/litex/test_pp_boot_bus_freeze.py"]),
    ("final-timestamp", ["python3", "sw/litex/test_gptp_tx_timestamp.py"]),
    ("final-memory-cdc", ["python3", "sw/litex/test_cpu_memory_port_cdc.py"]),
    ("final-memory-bridge", ["python3", "sw/litex/test_pp_mem_bridge.py"]),
    ("final-diff-check", ["git", "diff", "54ce877371ee6e8878cf67294e86c2a8481b62f6", "HEAD", "--check"]),
]
failed = []
for name, command in commands:
    result = subprocess.run([sys.executable, str(out / "run_gate.py"), name, *command],
                            timeout=15000, check=False)
    if result.returncode:
        failed.append(name)
print("FAILED: " + repr(failed), flush=True)
raise SystemExit(bool(failed))
