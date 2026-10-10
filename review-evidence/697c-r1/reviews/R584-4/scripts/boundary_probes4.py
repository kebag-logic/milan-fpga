#!/usr/bin/env python3
"""R584-4 boundary probes: plant a defect in a disposable copy of the checkout, run the real gate
(ctrl_boundary.py --require-rv32, no self-test) there, then restore the copy's exact head bytes.

Usage: python3 -I boundary_probes4.py <disposable-checkout-copy> <out-dir> [probe ...]

Each probe is a list of edits ("+path" = new file with the given text; "path" = replace the single
occurrence of `old` with `new`). Verdicts:
  CAUGHT   the gate exits non-zero and its output holds the probe's needle
  REFUSED  the gate exits non-zero for another reason (its first FAIL/REFUSED line is printed)
  ESCAPED  the gate exits 0 (PASS) although the plant is a boundary defect or an unread form
  PASSES   expected-pass probe passed
After every probe the copy is reset (git checkout + clean of the probe's new files) and verified clean.
"""
import subprocess
import sys
from pathlib import Path

copy = Path(sys.argv[1]).resolve()
outdir = Path(sys.argv[2]).resolve()
only = set(sys.argv[3:])
CTRL = "sw/firmware/ctrl/"
T = CTRL + "test/"

FAKE_CXX = '#ifdef __cplusplus\n#include "acmp_fake.hpp"\n#endif\n'
EXAMPLE_CXX = '#ifdef __cplusplus\n#include "adp_port.h"\n#endif\n'
MBX_MODE = (CTRL + "adp/adp_mbx.c", '#include "adp_mbx.h"\n',
            '#include "adp_mbx.h"\n#ifdef CTRL_R584_PAT\n#include "adp_port.h"\n#endif\n')
MODE_NEEDLE = "adp/adp_mbx.c includes tsn-c-stack/examples/adp_port.h"
R584_NEEDLE = "maap/maap_r584.h includes tsn-c-stack/tests/acmp_fake.hpp"
EX_NEEDLE = "adp/adp_r584.h includes tsn-c-stack/examples/adp_port.h"
PY = '"""A planted builder of sw/firmware/ctrl."""\nfrom pathlib import Path\nimport shutil\nimport subprocess\n'
MK = "# A planted builder of sw/firmware/ctrl.\n"
BENCH = [("+" + CTRL + "adp/adp_r584.h", EXAMPLE_CXX), ("+" + T + "probe_r584/bench.cpp", '#include "adp_r584.h"\n')]

PROBES = {
    # R584-3's plant, re-applied through test_maap_differential.cpp, and two variants.
    "A1-r584-3-replant": ([("+" + CTRL + "maap/maap_r584.h", FAKE_CXX),
                           (T + "test_maap_differential.cpp", '#include "maap.h"\n',
                            '#include "maap.h"\n#include "maap_r584.h"\n')], R584_NEEDLE, False),
    "A2-r584-3-replant-angle": ([("+" + CTRL + "maap/maap_r584.h", FAKE_CXX),
                                 (T + "test_maap_differential.cpp", '#include "maap.h"\n',
                                  '#include "maap.h"\n#include <maap_r584.h>\n')], R584_NEEDLE, False),
    "A3-r584-3-replant-two-deep": ([("+" + CTRL + "maap/maap_r584.h", FAKE_CXX),
                                    ("+" + CTRL + "maap/maap_r584a.h", '#include "maap_r584.h"\n'),
                                    (T + "test_maap_differential.cpp", '#include "maap.h"\n',
                                     '#include "maap.h"\n#include "maap_r584a.h"\n')], R584_NEEDLE, False),
    # C++ sources: a literal name (control), a glob, a Makefile wildcard, a suffix comparison.
    "B0-control-literal-cpp-name": (BENCH + [("+" + T + "planted_r584.mk",
                                              MK + "all:\n\tg++ -c probe_r584/bench.cpp\n")], EX_NEEDLE, False),
    "B1-makefile-wildcard-cpp": (BENCH + [("+" + T + "planted_r584.mk",
                                           MK + "SRCS := $(wildcard probe_r584/*.cpp)\nall:\n\tg++ -c $(SRCS)\n")],
                                 EX_NEEDLE, False),
    "B2-python-glob-cpp": (BENCH + [("+" + T + "planted_r584.py",
                                     PY + 'SOURCES = sorted(Path(__file__).parent.glob("probe_r584/*.cpp"))\n')],
                           "probe_r584/*.cpp", False),
    "B3-python-suffix-compare": (BENCH + [("+" + T + "planted_r584.py",
                                           PY + 'SOURCES = [p for p in (Path(__file__).parent / "probe_r584")'
                                           '.iterdir() if p.suffix == ".cpp"]\n')], EX_NEEDLE, False),
    # A C++ source a builder writes: from an f-string, from str.format, copied from a template file.
    "C0-control-written-literal": ([BENCH[0], ("+" + T + "planted_r584.py",
                                    PY + 'Path("planted_r584.cpp").write_text("#include \\"adp_r584.h\\"\\n")\n')],
                                   EX_NEEDLE, False),
    "C1-written-fstring-include": ([BENCH[0], ("+" + T + "planted_r584.py",
                                    PY + 'HDR = "adp_r584.h"\n'
                                    'Path("planted_r584.cpp").write_text(f"#include \\"{HDR}\\"\\n")\n')],
                                   EX_NEEDLE, False),
    "C2-written-format-include": ([BENCH[0], ("+" + T + "planted_r584.py",
                                   PY + 'TEMPLATE = "#include \\"{}\\"\\n"\n'
                                   'Path("planted_r584.cpp").write_text(TEMPLATE.format("adp_r584" + ".h"))\n')],
                                  EX_NEEDLE, False),
    "C3-written-copied-template": ([BENCH[0], ("+" + T + "probe_r584.tpl", '#include "adp_r584.h"\n'),
                                    ("+" + T + "planted_r584.py",
                                     PY + 'shutil.copy(Path(__file__).parent / "probe_r584.tpl", "planted_r584.cpp")\n')],
                                   EX_NEEDLE, False),
    # -D forms: a literal (control), then forms that are neither a literal flag nor an f-string.
    "D0-control-literal-mode": ([MBX_MODE, ("+" + T + "planted_r584.mk", MK + "all:\n\tcc -DCTRL_R584_PAT -c x.c\n")],
                                MODE_NEEDLE, False),
    "D1-makefile-patsubst": ([MBX_MODE, ("+" + T + "planted_r584.mk",
                                         MK + "all:\n\tcc $(patsubst %,-D%,CTRL_R584_PAT) -c x.c\n")],
                             "planted_r584.mk", False),
    "D2-makefile-foreach": ([MBX_MODE, ("+" + T + "planted_r584.mk",
                                        MK + "all:\n\tcc $(foreach m,CTRL_R584_PAT,-D$(m)) -c x.c\n")],
                            "planted_r584.mk", False),
    "D3-python-shell-string": ([MBX_MODE, ("+" + T + "planted_r584.py",
                                           PY + 'subprocess.run("cc -DCTRL_R584_PAT -c x.c", shell=True)\n')],
                               "CTRL_R584_PAT", False),
    "D4-python-bare-then-ifexp": ([MBX_MODE, ("+" + T + "planted_r584.py",
                                              PY + 'X = True\nARGS = ["cc", "-D", "CTRL_R584_PAT" if X else "Y"]\n')],
                                  "planted_r584.py", False),
    "D5-python-format-flag": ([MBX_MODE, ("+" + T + "planted_r584.py",
                                          PY + 'ARGS = ["-D{}".format("CTRL_R584_PAT")]\n')], "planted_r584.py", False),
    "D6-makefile-bare-then-variable": ([MBX_MODE, ("+" + T + "planted_r584.mk",
                                                   MK + "M := CTRL_R584_PAT\nall:\n\tcc -D $(M) -c x.c\n")],
                                       "planted_r584.mk", False),
    "D7-python-shlex-joined-string": ([MBX_MODE, ("+" + T + "planted_r584.py",
                                                  PY + 'import shlex\nARGS = ["cc", *shlex.split("-O2 -DCTRL_R584_PAT")]\n')],
                                      "CTRL_R584_PAT", False),
}


def sh(cmd, **kw):
    return subprocess.run(cmd, cwd=copy, capture_output=True, text=True, **kw)


def apply(edits):
    for edit in edits:
        path, rest = edit[0], edit[1:]
        if path.startswith("+"):
            target = copy / path[1:]
            assert not target.exists(), target
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rest[0], encoding="utf-8")
        else:
            target = copy / path
            text = target.read_text(encoding="utf-8")
            assert text.count(rest[0]) == 1, (path, text.count(rest[0]))
            target.write_text(text.replace(rest[0], rest[1]), encoding="utf-8")


def restore():
    sh(["git", "checkout", "--", "."])
    sh(["git", "clean", "-fdq", "--", "sw/firmware"])
    st = sh(["git", "status", "--porcelain", "--untracked-files=all"]).stdout
    assert st == "", st


outdir.mkdir(parents=True, exist_ok=True)
restore()
rows = []
for name, (edits, needle, should_pass) in PROBES.items():
    if only and name not in only:
        continue
    apply(edits)
    try:
        res = sh([sys.executable, "sw/firmware/ctrl/test/ctrl_boundary.py", "--require-rv32"], timeout=900)
    finally:
        restore()
    text = res.stdout + res.stderr
    (outdir / f"{name}.log").write_text(text, encoding="utf-8")
    lines = [ln.strip() for ln in text.splitlines() if "[FAIL]" in ln or ln.startswith("REFUSED")]
    if res.returncode == 0:
        verdict = "PASSES" if should_pass else "ESCAPED"
    elif needle in text:
        verdict = "CAUGHT"
    else:
        verdict = "REFUSED"
    shown = next((ln for ln in lines if needle in ln), lines[0] if lines else text.strip().splitlines()[-1])
    rows.append(f"{verdict:8} {name}: rc {res.returncode}: {shown}")
    print(rows[-1], flush=True)
(outdir / "verdicts.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
