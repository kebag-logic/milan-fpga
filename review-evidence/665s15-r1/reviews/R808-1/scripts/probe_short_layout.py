"""Probe: compile acmp_mbx.c (on a copy of the control tree) against the 32x32 shape layout and against that layout one
sink entry short (17 -> 16), with ACMP at 33 sinks/sources, MBX_ENTRY_ORDINAL from the generated header.
usage: python3 -I probe_short_layout.py TREE OUTDIR"""
import subprocess, sys
from pathlib import Path
tree, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "sw/mailbox"))
import gen_mailbox
from mailbox_model import with_shape
contract = gen_mailbox.load()
cfg = tree / "configs/endstation_ax7101_32x32.yaml"
good, src, snk = gen_mailbox.shape_variant(contract, cfg, 2)
short = with_shape(contract, 2, good.pub_sources, good.pub_sinks - 1)
cc = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
rc_all = {}
for label, variant in (("shape", good), ("short", short)):
    d = out / label
    import shutil
    shutil.copytree(tree / "sw/firmware/ctrl", d, dirs_exist_ok=True)
    texts = gen_mailbox.generate(variant)
    hdr = next(p for p in texts if p.endswith("mbx_contract.h"))
    (d / "mbx" / "mbx_contract.h").write_text(texts[hdr])
    inc = [f"-I{d/x}" for x in ("mbx","host","port","loop","adp","maap","acmp","app","srp","aecp","test")] + [f"-I{tree/'third_party/tsn-c-stack/include'}", f"-I{tree/'sw/firmware/gtest/rv32_include'}"]
    for f in ("acmp/acmp_mbx.c",):
        r = subprocess.run([cc, "-march=rv32i", "-mabi=ilp32", "-ffreestanding", "-std=c11", "-fsyntax-only",
                            "-DACMP_MAX_SINKS=33u", "-DACMP_MAX_SOURCES=33u", "-DCTRL_MBX_BASE=0x80000000u", *inc,
                            str(d / f)], capture_output=True, text=True)
        rc_all[(label, f)] = r.returncode
        print(f"{label} {f}: rc={r.returncode} entries={variant.bound_talkers}/{variant.pub_sinks}")
        for line in r.stderr.splitlines():
            if "static assertion" in line or "error" in line: print("   ", line.split(str(tree))[-1][:220])
ok = rc_all[("shape", "acmp/acmp_mbx.c")] == 0 and rc_all[("short", "acmp/acmp_mbx.c")] != 0
print("PROBE", "firmware link refuses the short layout and accepts the shape's" if ok else "UNEXPECTED")
