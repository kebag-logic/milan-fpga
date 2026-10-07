#!/usr/bin/env python3
"""One CPU-option export at a given recipe source; one fresh process per case.

Usage: measure_cpu_option.py SOC_PY CPU XLEN OPTION DATA_DIR OUT_DIR RESULT_JSON
OPTION is one of none, fpu, l2 (8192), zero (explicit 0).
Builds the real MilanSoC (with_milan=False, AX7101 platform, 50 MHz) through the
LiteX Builder without software compilation or vendor tools, then records the raw
CPU netlist digest and a digest with // comments removed and the generated module
name replaced, so a name-only change cannot pass as a hardware change.
The CPU data package is redirected to DATA_DIR (an isolated copy).
"""
import hashlib, importlib.util, json, re, sys
from pathlib import Path

soc_py, cpu, xlen, option, data_dir, out_dir, result = sys.argv[1:]
xlen = int(xlen)
opts = {"none": {}, "fpu": {"with_fpu": True}, "l2": {"l2_bytes": 8192},
        "zero": {"l2_bytes": 0}}[option]
sys.path.insert(0, str(Path(soc_py).parent))
pkg = "pythondata_cpu_" + cpu
data_mod = __import__(pkg)
data_mod.data_location = data_dir
if cpu == "naxriscv":
    from litex.soc.cores.cpu.naxriscv import NaxRiscv
    orig = NaxRiscv.args_read
    def frozen(args, orig=orig):
        args.update_repo = "no"   # never touch git; sources are pinned copies
        return orig(args)
    NaxRiscv.args_read = staticmethod(frozen)
spec = importlib.util.spec_from_file_location("milan_soc_measure", soc_py)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
from litex.soc.integration.builder import Builder
rec = dict(cpu=cpu, xlen=xlen, option=option, soc=soc_py)
try:
    soc = mod.MilanSoC(mod.alinx_ax7101.Platform(), 50000000, cpu=cpu, xlen=xlen,
                       with_milan=False, **opts)
    Builder(soc, output_dir=out_dir, compile_software=False).build(run=False)
    name = soc.cpu.netlist_name
    raw = (Path(data_dir) / (name + ".v")).read_bytes()
    rtl = re.sub(rb"//[^\n]*", b"", raw).replace(name.encode(), b"CPU")
    rec.update(kind="export", netlist=name, bytes=len(raw),
               sha256=hashlib.sha256(raw).hexdigest(),
               rtl_sha256=hashlib.sha256(rtl).hexdigest())
except ValueError as exc:
    rec.update(kind="refused", reason=str(exc))
Path(result).write_text(json.dumps(rec, indent=1) + "\n")
print("RESULT", json.dumps(rec))
