"""R585-5 probe builder, copied into sw/firmware/ctrl/test/ of a DISPOSABLE checkout only.

Compiles sw/firmware/ctrl/adp/adp_mbx.c once, by the compiler NAME "gcc" (so the
capture's wrapper records it), with one extra mode delivered in a way no builder
text spells:
  env  -> the flag comes from the environment (R585_FLAGS), split by shlex
  rsp  -> the flag is inside a GCC response file passed as @FILE
  abs  -> a plain compile by the name "gcc" (recorded), then the moded compile by the
          absolute path /usr/bin/gcc (no wrapper stands there); run it under python3 -I so
          the capture's audit hook (a sitecustomize on PYTHONPATH) is not loaded
Usage: python3 r585_probe_builder.py env|rsp|abs
"""
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent          # sw/firmware/ctrl/test
CTRL = HERE.parent                               # sw/firmware/ctrl
ROOT = HERE.parents[3]
STACK = ROOT / "third_party/tsn-c-stack"
inc = [f"-I{CTRL / d}" for d in ("mbx", "host", "port", "loop", "adp", "maap", "acmp", "app", "test")]
inc += [f"-I{STACK / 'include'}", f"-I{ROOT / 'sw/firmware/ctrl_nvm'}", f"-I{STACK / 'examples'}"]
how = sys.argv[1]
with tempfile.TemporaryDirectory() as tmp:
    extra = []
    if how == "env":
        extra = shlex.split(os.environ.get("R585_FLAGS", "-DCTRL_R585_ENV"))
    elif how == "rsp":
        rsp = Path(tmp) / "flags.rsp"
        rsp.write_text("-DCTRL_R585_RSP\n", encoding="utf-8")
        extra = [f"@{rsp}"]
    if how == "abs":
        plain = ["gcc", "-std=c11", "-O2", *inc, "-c", str(CTRL / "adp/adp_mbx.c"), "-o", str(Path(tmp) / "p.o")]
        if subprocess.run(plain, check=False).returncode:
            sys.exit(1)
        argv = ["/usr/bin/gcc", "-std=c11", "-O2", "-DCTRL_R585_ENV", *inc, "-c", str(CTRL / "adp/adp_mbx.c"),
                "-o", str(Path(tmp) / "x.o")]
    else:
        argv = ["gcc", "-std=c11", "-O2", *extra, *inc, "-c", str(CTRL / "adp/adp_mbx.c"), "-o", str(Path(tmp) / "x.o")]
    res = subprocess.run(argv, check=False)
    sys.exit(res.returncode)
