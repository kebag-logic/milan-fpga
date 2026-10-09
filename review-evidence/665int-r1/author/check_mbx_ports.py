"""The KL_mbx instance a --ctrl-mailbox export generates binds exactly KL_mbx's ports.

Usage: check_mbx_ports.py <generated-top.v> <KL_mbx.sv>
"""
import re
import sys
from pathlib import Path

top, rtl = Path(sys.argv[1]).read_text(), Path(sys.argv[2]).read_text()
inst = re.search(r"^KL_mbx\b[^;]*?\(\n(.*?)\n\);", top, re.S | re.M)
if inst is None:
    sys.exit("no KL_mbx instance in the generated top")
bound = re.findall(r"^\s*\.(\w+)\s*\(", inst.group(1), re.M)
header = rtl[rtl.index("module KL_mbx"):rtl.index(");", rtl.index("module KL_mbx"))]
ports = re.findall(r"^\s*(?:input|output)\s+(?:logic|wire)?\s*(?:\[[^\]]*\]\s*)?(\w+)", header, re.M)
missing, extra = sorted(set(ports) - set(bound)), sorted(set(bound) - set(ports))
pub = sorted(p for p in bound if p.startswith("pub_"))
print(f"instance binds {len(bound)} port(s); KL_mbx declares {len(ports)}; publication ports bound: {pub}")
print(f"missing {missing} extra {extra}")
sys.exit(1 if missing or extra or len(bound) != len(set(bound)) else 0)
