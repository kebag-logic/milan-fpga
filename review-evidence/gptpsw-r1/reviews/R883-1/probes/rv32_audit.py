"""Reviewer probe (R883-1): build gptp.c and gptp_mbx.c for the split's RV32IM hart with the gate's own flags and
list the undefined symbols (no float, libm or multiply/divide helper may appear). Usage (from the repository root):
  MILAN_RV32_CC=<riscv32-linux-gcc> python3 -I <this> <repo> <outdir>"""
import os, subprocess, sys
from pathlib import Path
repo, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest")]
import ctrl_build, fw_rv32  # noqa: E402
cc = fw_rv32.compiler()
inc = fw_rv32.includes(cc)
out.mkdir(parents=True, exist_ok=True)
ctrl = repo / "sw/firmware/ctrl"
incs = [f"-I{ctrl / d}" for d in ("gptp", "mbx", "loop", "port")] + [f"-I{repo / 'third_party/tsn-c-stack/include'}"]
bad = 0
for src in ("gptp/gptp.c", "gptp/gptp_mbx.c"):
    obj = out / (Path(src).stem + ".o")
    r = subprocess.run([cc, *ctrl_build.SPLIT_RV32_FLAGS, *inc, *incs, "-c", str(ctrl / src), "-o", str(obj)],
                       capture_output=True, text=True)
    if r.returncode:
        print(f"{src}: build failed\n{r.stderr}"); bad = 1; continue
    und = subprocess.run([cc.removesuffix("gcc") + "nm", "-u", str(obj)], capture_output=True, text=True).stdout.split()
    und = sorted(s for s in und if s != "U")
    stray = sorted(set(und) & fw_rv32.MULDIV_HELPERS)
    flt = sorted(s for s in und if s.endswith(("df3", "sf3", "didf", "sfdf2", "dfsf2")) or s in ("exp", "log2", "llround"))
    size = subprocess.run([cc.removesuffix("gcc") + "size", str(obj)], capture_output=True, text=True).stdout.strip().splitlines()[-1]
    print(f"{src}: undefined {und}; muldiv helpers {stray}; float/libm {flt}; size(text data bss) {size.split()[:3]}")
    bad |= bool(stray or flt)
print("flags:", " ".join(ctrl_build.SPLIT_RV32_FLAGS))
print("RESULT:", "FAIL" if bad else "PASS")
sys.exit(bad)
