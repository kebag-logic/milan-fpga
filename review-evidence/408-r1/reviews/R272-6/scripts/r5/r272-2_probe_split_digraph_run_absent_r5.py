#!/usr/bin/env python3
"""R272-2 probe: does gate 1b refuse a product-only cast store hidden behind a
`%:` digraph directive that a backslash-newline splits (%\<nl>:ifdef ...)?

The pinned GCC honours %\<nl>:ifdef as #ifdef (measured, gcc-spellings.json).
On dev the ordered cast set read every arm as text and refused this store.
At this head the cast set is retired; a store in #ifdef CSR_UART_BASE is only
caught if the readers find the conditional and per-selection grading forces
the arm to compile. If the split digraph evades the readers, the arm is never
graded, the census stub tree (no CSR_UART_BASE) drops it, and it slips.

Usage: probe_split_digraph.py <sdk-dir> <spelling>
  spelling in {control_hash, formfeed, split_digraph, plain_digraph}
Exit 0 => gate REFUSED the store; exit 7 => gate ACCEPTED it (reduction)."""
import sys, subprocess, tempfile, io, contextlib
from pathlib import Path
from unittest.mock import patch

sdk = Path(sys.argv[1]); spelling = sys.argv[2]
REPO = Path("$REVIEWS/r272-5-408")
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "sw/builder"))
import ci_rv32_sdk as sdklib
import test_builder as builder

fw_path = REPO / "sw/firmware/milan_baremetal/milan_baremetal.c"
real_fw = fw_path.read_text(encoding="utf-8")
raw_address = "0x90000600u"           # MILAN_CSR_BASE 0x90000000 + A_ADP_CTRL 0x600
uart_tail = "\tprint_tod(gettime_ns());\n}"
assert uart_tail in real_fw

store = f"\t*(volatile unsigned int *){raw_address} = 1u;"
if spelling == "control_hash":
    guard_open, guard_close = "#ifdef CSR_UART_BASE", "#endif"
elif spelling == "formfeed":
    guard_open, guard_close = "\f#ifdef CSR_UART_BASE", "\f#endif"
elif spelling == "plain_digraph":
    guard_open, guard_close = "%:ifdef CSR_UART_BASE", "%:endif"
elif spelling == "split_digraph":
    guard_open, guard_close = "%\\\n:ifdef CSR_UART_BASE", "%\\\n:endif"
else:
    raise SystemExit("bad spelling")

block = f"{guard_open}\n{store}\n{guard_close}"
hostile = real_fw.replace(uart_tail, block + "\n" + uart_tail, 1)
assert hostile != real_fw

selector = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
mapped = "/nonexistent/riscv32-linux-gcc"
real_run = subprocess.run
def run(argv, **kw):
    argv = [str(a) for a in argv]
    if argv and argv[0] == selector:
        argv = [mapped] + argv[1:]
    return real_run(argv, **kw)

real_read_text = Path.read_text
def read_text(self, *a, **k):
    if self.resolve() == fw_path.resolve():
        return hostile
    return real_read_text(self, *a, **k)

sdklib.verify(sdk)
with tempfile.TemporaryDirectory(prefix="probe-") as tmp:
    with patch.object(subprocess, "run", side_effect=run), \
         patch.object(Path, "read_text", read_text), \
         patch.object(sys, "argv", [__file__]), \
         patch.object(builder, "OUT", Path(tmp)), \
         patch.object(builder, "SKIPPED", []):
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                builder.test_baremetal_profile_contract()
        except (AssertionError, ValueError) as exc:
            msg = str(exc).replace("\n", " ")[:400]
            print(f"[{spelling}] REFUSED: {msg}")
            sys.exit(0)
        else:
            print(f"[{spelling}] ACCEPTED the hidden store -- gate passed")
            sys.exit(7)
