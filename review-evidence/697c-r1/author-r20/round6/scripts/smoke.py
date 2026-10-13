"""Scratch: compile with every driver spelling under a capture, then read it back."""
import shutil, subprocess, sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve(); out = Path(sys.argv[2]).resolve()
sys.path[:0] = [str(tree / "sw/firmware/ctrl/test"), str(tree / "sw/firmware/gtest")]
import ctrl_capture, ctrl_configs
shutil.rmtree(out, ignore_errors=True); work = out / "work"; work.mkdir(parents=True)
cap = out / "cap"
(work / "planted.c").write_text("int x;\n"); (work / "planted.cpp").write_text('#include "gen.hpp"\n')
(work / "inc").mkdir(); (work / "inc/gen.hpp").write_text('#include "adp_mbx.h"\n')
(work / "f.rsp").write_text("-DFROM_RSP\n"); (work / "m.h").write_text("#define FROM_IMACROS 1\n")
(work / "src.rsp").write_text("-DHID planted.c\n")
(work / "pm.h").write_text("#define FROM_PCH 1\n"); (work / "pu.cpp").write_text("int y;\n")
cases = {
 "plain": ["cc", "-DPLAIN", "-c", "planted.c", "-o", "a.o"],
 "wp": ["cc", "-Wp,-DWP", "-c", "planted.c", "-o", "b.o"],
 "xp": ["cc", "-Xpreprocessor", "-DXP", "-c", "planted.c", "-o", "c.o"],
 "long=": ["cc", "--define-macro=LONGEQ", "-c", "planted.c", "-o", "d.o"],
 "long": ["cc", "--define-macro", "LONGSEP", "-c", "planted.c", "-o", "e.o"],
 "rsp": ["cc", "@f.rsp", "-c", "planted.c", "-o", "f.o"],
 "imacros": ["cc", "-imacros", "m.h", "-c", "planted.c", "-o", "g.o"],
 "rspsrc": ["cc", "@src.rsp", "-c"],
 "incdir": ["c++", "-fsyntax-only", "--include-directory", str(work / "inc"), "-I" + str(tree / "sw/firmware/ctrl/adp"), "-I" + str(tree / "sw/firmware/ctrl/mbx"), "-I" + str(tree / "third_party/tsn-c-stack/include"), "planted.cpp"],
 "undef": ["cc", "-UNDEBUG", "-std=c11", "-c", "planted.c", "-o", "h.o"],
 "noname": ["cc", "-D=1", "-c", "planted.c", "-o", "i.o"],
 "version": ["cc", "--version"],
 "link": ["cc", "a.o", "b.o", "-o", "prog"],
 "pchmake": ["c++", "-x", "c++-header", "pm.h", "-o", "pm.h.gch"],
 "pchuse": ["c++", "-include", "pm.h", "-c", "pu.cpp", "-o", "pu.o"],
 "mmio": ["cc", "-include" + str(tree / "sw/firmware/ctrl/test/mmio_window.h"), "-c", "planted.c", "-o", "j.o"],
}
for name, argv in cases.items():
    res = ctrl_capture.run(cap, argv, cwd=work, capture_output=True, text=True)
    if name == "pchmake":
        (work / "pm.h").write_text("#error the precompiled header must be used\n")
    print(f"{name}: rc={res.returncode} {res.stderr.strip()[:120]}")
c = ctrl_capture.load(cap)
for inv in c.invocations:
    made = inv.expansion
    print("---", inv.args[:4], "failed=", inv.failed, "error=", made and made.error, "first=", [e.mains for e in inv.first], "pch=", made and made.pch)
    if made and not made.error and not inv.failed:
        flags = [f for f in ctrl_configs.flags_of(inv) if not ctrl_configs.RESERVED.match(ctrl_configs.FLAG.fullmatch(f)[1])]
        print("   flags", flags)
        print("   first", ctrl_configs.read_first(inv))
        print("   dirs", made.dirs[:4], "sources", inv.sources[:2])
print("expansion reasons:")
for r in ctrl_configs.expanded(c, ctrl_configs.places((ctrl_configs.CTRL, ctrl_configs.STACK))):
    print("  ", r[:300])
print("read-first units:", ctrl_configs.read_first_units(c, (ctrl_configs.CTRL, ctrl_configs.STACK)))
print("modes:", ctrl_configs.modes_of(c))
