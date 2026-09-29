#!/usr/bin/env python3
"""Fault probes for the arm's two new build checks, run through the COMMITTED
mutants.py functions without touching the tree: a variant Makefile (a copy of
the committed one, one edit) is injected with `-f` into the arm's own make
command lines, and module constants are patched in memory.
  A  --no-print-directory removed from the DP_SRCS call only  -> makeflags check must FAIL
  B  --no-print-directory removed from the DP_VFLAGS call only -> makeflags check must FAIL
  C  both kept (committed Makefile via -f)                     -> makeflags check must PASS
  D  BUILD_TAIL_LINES = 0                                      -> build-break check must FAIL
  E  BUILD_MAKEFLAGS = "w", committed Makefile                 -> build('dp') still builds (Makefile fix alone)
  F  BUILD_MAKEFLAGS = "", both flags removed                  -> build('dp') still builds (env fix alone)
  G  BUILD_MAKEFLAGS = "w", both flags removed (the ddb07747 state) -> build('dp') fails; tail printed
Usage: check_fault_probe.py <capture_coherence dir> <workdir>"""
import importlib.util, sys
from pathlib import Path
suite, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
work.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location("m", suite / "mutants.py")
m = importlib.util.module_from_spec(spec); sys.argv = ["mutants.py"]; spec.loader.exec_module(m)
orig_run_child = m.run_child
committed = (suite / "Makefile").read_text()
SRCS_CALL = "$(shell $(MAKE) -s --no-print-directory -C $(DP_DIR) print-srcs"
VF_CALL = "$(shell $(MAKE) -s --no-print-directory -C $(DP_DIR) print-dp-vflags)"
assert committed.count(SRCS_CALL) == 1 and committed.count(VF_CALL) == 1

def variant(name, text):
    p = work / f"Makefile.{name}"; p.write_text(text); return p

def use_makefile(mk):
    def rc(cmd, cwd=None, env=None):
        if "-C" in cmd:
            i = cmd.index("-C"); cmd = cmd[:i + 2] + ["-f", str(mk)] + cmd[i + 2:]
        return orig_run_child(cmd, cwd=cwd, env=env)
    m.run_child = rc

def show(tag, result):
    ok, lines = result
    print(f"{tag}: check {'PASSES' if ok else 'FAILS'}")
    for ln in lines[:1] + [l for l in lines[1:] if "Entering" in l or "%Error" in l or "rror" in l][:4]:
        print("     ", ln[:240])

mk_full = variant("committed", committed)
mk_a = variant("no_npd_srcs", committed.replace(SRCS_CALL, SRCS_CALL.replace(" --no-print-directory", "")))
mk_b = variant("no_npd_vflags", committed.replace(VF_CALL, VF_CALL.replace(" --no-print-directory", "")))
mk_ab = variant("no_npd_both", committed.replace(SRCS_CALL, SRCS_CALL.replace(" --no-print-directory", ""))
                .replace(VF_CALL, VF_CALL.replace(" --no-print-directory", "")))
for tag, mk in (("A", mk_a), ("B", mk_b), ("C", mk_full)):
    d = work / tag; d.mkdir(exist_ok=True); use_makefile(mk); show(f"{tag} makeflags_result", m.makeflags_result(d))
use_makefile(mk_full)
d = work / "D"; d.mkdir(exist_ok=True); saved = m.BUILD_TAIL_LINES; m.BUILD_TAIL_LINES = 0
show("D build_break_result with BUILD_TAIL_LINES=0", m.build_break_result(d)); m.BUILD_TAIL_LINES = saved
d = work / "D2"; d.mkdir(exist_ok=True)
show("D2 build_break_result, committed constants (control)", m.build_break_result(d))
for tag, mk, flags in (("E", mk_full, "w"), ("F", mk_ab, ""), ("G", mk_ab, "w")):
    d = work / tag; d.mkdir(exist_ok=True); use_makefile(mk); m.BUILD_MAKEFLAGS = flags
    src = m.stage("dp", d, "src", m.DATAPATH.read_text())
    exe = m.build("dp", src, d, "b")
    print(f"{tag} build('dp') with BUILD_MAKEFLAGS={flags!r}, Makefile={mk.name}: {'built' if exe else 'FAILED'}")
    if not exe:
        for ln in m.build_tail(m.build_log(d, 'b'))[-6:]: print("     ", ln[:240])
