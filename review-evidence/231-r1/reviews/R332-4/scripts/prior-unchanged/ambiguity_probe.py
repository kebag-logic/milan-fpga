#!/usr/bin/env python3
"""Reviewer probe: a synthetic export that binds PP_UCODE_HEX_P twice, the
second time to a one-word (partial) image. The pristine helper refuses it; the
helper with the inventory ambiguity guard removed accepts it, and the
maintained self-test (see extra_mutants.py) does not notice that removal.
usage: ambiguity_probe.py <path/to/syn/ooc/pp_baseline.py>"""
import importlib.util, sys, tempfile
from pathlib import Path

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def export(tmp):
    g = Path(tmp) / "gateware"; g.mkdir()
    decl, reads = [], []
    for p, pkg, d, w in (("PP_TROM_HEX_P", "pp_acmp_pkg.sv", "TROM_DEPTH_C", "TROM_W_C"),
                         ("PP_UCODE_HEX_P", "ucpu_pkg.sv", "UPC_W_C", "UCODE_W_C"),
                         ("GPTP_UCODE_HEX_P", "gptp_ucpu_pkg.sv", "UPC_W_C", "UCODE_W_C")):
        (g / pkg).write_text(f"parameter {d} = {'2' if d == 'TROM_DEPTH_C' else '1'};\nparameter {w} = 32;\n")
        (g / f"{p}.hex").write_text("12345678\nabcdef01\n")
        decl.append(f'.{p}("{g / (p + ".hex")}")'); reads.append(f"read_verilog {{{g / pkg}}}\n")
    (g / "partial.hex").write_text("12345678\n")
    decl.append(f'.PP_UCODE_HEX_P("{g / "partial.hex"}")')   # second, partial binding
    v = "\n".join(decl) + "\n"
    for n, words in (("rom", 2), ("sram", 4)):
        v += f'// Memory {n}: {words}-words x 32-bit\n$readmemh("alinx_ax7101_{n}.init", mem);\n'
        (g / f"alinx_ax7101_{n}.init").write_text("12345678\nabcdef01\n" if n == "rom" else "")
    (g / "alinx_ax7101.v").write_text(v)
    src = "".join(reads) + "# Add constraints\nsynth_design -top alinx_ax7101\n# Add pre-optimize commands\n# Bitstream generation\n"
    (g / "alinx_ax7101.tcl").write_text(src)
    return g, src

src = Path(sys.argv[1]).read_text()
guard = "        if len(matches) != 1 or len(packages) != 1:\n"
assert src.count(guard) == 1
with tempfile.TemporaryDirectory() as tmp:
    Path(tmp, "pristine.py").write_text(src)
    Path(tmp, "mutant.py").write_text(src.replace(guard, "        if False:\n"))
    for name in ("pristine", "mutant"):
        mod = load(Path(tmp, f"{name}.py"), name)
        with tempfile.TemporaryDirectory() as t2:
            g, s = export(t2)
            try:
                rows = mod.inventory(g, s)
                print(f"{name}\tACCEPTED\t{len(rows)} images; partial.hex inventoried: "
                      f"{any(r['path'].endswith('partial.hex') for r in rows)}")
            except ValueError as e:
                print(f"{name}\trefused\t{e}")
