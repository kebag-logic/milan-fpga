"""Compare the full top-level declaration to the assigned base."""
from pathlib import Path
import re
import subprocess
base = "939c143333d11e2378a514f1c7b6abd4c3259bfd"
name = "hdl/top/protocol_processor_top.sv"
old = subprocess.check_output(["git", "show", f"{base}:{name}"], text=True)
new = Path(name).read_text()
def declaration(source):
    source = re.sub(r"/\*.*?\*/|//[^\n]*", "", source, flags=re.S)
    start = source.index("module protocol_processor_top")
    end = source.index(");", start) + 2
    return re.sub(r"\s+", "", source[start:end])
assert declaration(old) == declaration(new), "top-level declaration changed"
print("PASS: every top-level parameter and port matches the assigned base")
