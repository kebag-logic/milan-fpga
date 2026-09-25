"""Check the installed generator, without relying on cached interface metadata."""
from pathlib import Path
import shlex
import subprocess

from cpu_preflight import VexiiRiscv
import pythondata_cpu_vexiiriscv

scratch = Path("$VALIDATION_STORAGE/559-a307-cpu-preflight")
scratch.mkdir(parents=True, exist_ok=True)
source = Path(pythondata_cpu_vexiiriscv.data_location) / "ext/VexiiRiscv"
metadata = scratch / "product_cpu_metadata.py"
options = " ".join([VexiiRiscv.vexii_args, *VexiiRiscv._get_soc_args()])
argv = ["sbt", f"runMain vexiiriscv.soc.litex.PythonArgsGen {options} --python-file={metadata}"]
print("cwd:", source, flush=True)
print("command:", shlex.join(argv), flush=True)
result = subprocess.run(argv, cwd=source, timeout=600)
print("GENERATOR_RC:", result.returncode, flush=True)
if result.returncode:
    raise SystemExit(result.returncode)
print(metadata.read_text(), flush=True)
