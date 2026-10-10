#!/usr/bin/env python3
"""Reviewer probes for ctrl_boundary.py (#697, review round R584-5).

Runs the gate's own main() path up to its judgement (the pin, the stack's own gate build and the image
builders under the gate's capture, the given captures, held(), derive(), configurations()), then judges each
probe below exactly as the gate's --selftest judges a control: planted() copies, control_capture() (a probe's
planted builder runs through the capture), judge(..., control=probe). A probe is CAUGHT when a finding or a
refusal holds its needle, else ESCAPED (every finding printed). K0 is the harness's own positive control.

usage: python3 -B boundary_probes.py <checkout> [--capture DIR]... [--without verilator] [--only NAME-PREFIX]...
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("checkout", type=Path)
ap.add_argument("--capture", type=Path, action="append")
ap.add_argument("--without", action="append", default=[])
ap.add_argument("--only", action="append", default=[])
args = ap.parse_args()
HERE = args.checkout.resolve() / "sw/firmware/ctrl/test"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "gtest"))

import ctrl_boundary as cb  # noqa: E402
import ctrl_capture  # noqa: E402
import fw_rv32  # noqa: E402
from ctrl_build import CTRL, STACK, Refusal, stack_pin  # noqa: E402
from ctrl_capture import Capture, CaptureError  # noqa: E402
from ctrl_configs import configurations, derive, held, makefiles  # noqa: E402
from ctrl_pin import named_compilers  # noqa: E402
from ctrl_plants import ANCHOR, PY, Plant, under_mode  # noqa: E402
from ctrl_runs import captures, owned  # noqa: E402

EXAMPLE = "includes tsn-c-stack/examples/adp_port.h"
REAL = ('import shutil\nREAL = shutil.which("gcc", path=os.pathsep.join(os.environ["PATH"].split(os.pathsep)[1:]))\n')


def mode(name: str, macro: str, run: str) -> Plant:
    """A planted builder compiles with `macro` in some driver form; the ADP adapter reaches a stack example's
    header only under it."""
    return replace(under_mode(name, macro, f"-D{macro}", run), needle=f"adp/adp_mbx.c {EXAMPLE}", shared=False)


def aecp(name: str, condition: str) -> Plant:
    """The AECP image header reaches a stack example's header only under `condition`, a macro (or value) only
    the AECP wire comparison's C++ compile gives today (aecp_wire.py)."""
    anchor = '#include "aecp_model.h"\n'
    return Plant(name, "ctrl", "aecp/aecp_image.h", anchor, anchor + f"#if {condition}\n#include \"adp_port.h\"\n"
                 "#endif\n", f"aecp/aecp_image.h {EXAMPLE}")


PROBES = (
    replace(under_mode("K0 harness control: a mode the capture records (CTRL_REENTRY_ASSERT)",
                       "CTRL_REENTRY_ASSERT", "-DCTRL_REENTRY_ASSERT", ""), needle=f"adp/adp_mbx.c {EXAMPLE}",
            shared=False),
    aecp("V1 a mode only aecp_wire.py gives (PP_TOP_TIM_DEFAULTS)", "defined(PP_TOP_TIM_DEFAULTS)"),
    aecp("V2 a mode only aecp_wire.py --interfaces 2 gives (PP_TOP_IF2)", "defined(PP_TOP_IF2)"),
    aecp("V3 a value only aecp_wire.py --interfaces 2 gives (AECP_WIRE_INTERFACES=2)",
         "defined(AECP_WIRE_INTERFACES) && AECP_WIRE_INTERFACES > 1"),
    mode("F1 -Wp,-D passes a mode to the preprocessor", "CTRL_R584_WP",
         PY + 'cc("cc", "-Wp,-DCTRL_R584_WP", "-c", "planted.c", "-o", "planted.o")\n'),
    mode("F2 -Xpreprocessor -D passes a mode", "CTRL_R584_XP",
         PY + 'cc("cc", "-Xpreprocessor", "-DCTRL_R584_XP", "-c", "planted.c", "-o", "planted.o")\n'),
    mode("F3 --define-macro=NAME", "CTRL_R584_LONG",
         PY + 'cc("cc", "--define-macro=CTRL_R584_LONG", "-c", "planted.c", "-o", "planted.o")\n'),
    mode("F4 --define-macro NAME", "CTRL_R584_LONG2",
         PY + 'cc("cc", "--define-macro", "CTRL_R584_LONG2", "-c", "planted.c", "-o", "planted.o")\n'),
    mode("F5 a response file holds the mode", "CTRL_R584_RSP",
         PY + 'open(os.path.join(WORK, "planted.rsp"), "w").write("-DCTRL_R584_RSP\\n")\n'
              'cc("cc", "@planted.rsp", "-c", "planted.c", "-o", "planted.o")\n'),
    mode("F6 -imacros of a file the builder writes defines the mode", "CTRL_R584_IMACROS",
         PY + 'open(os.path.join(WORK, "modes.h"), "w").write("#define CTRL_R584_IMACROS 1\\n")\n'
              'cc("cc", "-imacros", "modes.h", "-c", "planted.c", "-o", "planted.o")\n'),
    mode("F7 a shell command runs a compiler by its own path", "CTRL_R584_SHABS",
         PY + REAL + 'cc(REAL + " -DCTRL_R584_SHABS -c planted.c -o planted.o", shell=True)\n'),
)


def main() -> int:
    without = frozenset(args.without)
    rv32 = fw_rv32.compiler()
    probes = [p for p in PROBES if not args.only or any(p.name.startswith(o) for o in args.only)]
    results = []
    with tempfile.TemporaryDirectory(prefix="r584-5-probes-") as tmp:
        work = Path(tmp)
        print(f"tsn-c-stack at {stack_pin()}", flush=True)
        mine = work / "capture"
        said, refused = cb.stack_gate(False, work / "stack-gate-build", mine)
        given = captures(args.capture, work, without)
        owned(mine, work / "images")
        env = ctrl_capture.install(mine)
        named = [record for makefile in makefiles() for record in named_compilers(makefile, env)]
        base = sum(given[1:], given[0]) + ctrl_capture.load(mine) + Capture((), (), (), tuple(named))
        held(base, without)
        universe = derive(base)
        print(f"universe: {len(universe)} modes: {sorted(universe)}", flush=True)
        if refused:
            print(f"the stack's own gate refused: {refused}")
        for probe in probes:
            trees = cb.planted(probe, work / "plants")
            try:
                capture = cb.control_capture(probe, trees, base, work / "plant-run")
                findings = cb.judge(trees, rv32, work / "plants-build", capture, control=probe, without=without)
            except (Refusal, CaptureError) as exc:
                findings = [f"REFUSED: {exc}"]
            shutil.rmtree(work / "plants-build", ignore_errors=True)
            caught = any(probe.needle in f for f in findings)
            verdict = "CAUGHT" if caught else "ESCAPED"
            shown = next((f for f in findings if probe.needle in f), "")
            print(f"[{verdict}] {probe.name}: {shown or (findings or ['no finding: the gate passes'])}", flush=True)
            results.append(verdict)
    print(f"probes: {results.count('CAUGHT')} caught, {results.count('ESCAPED')} escaped of {len(results)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
