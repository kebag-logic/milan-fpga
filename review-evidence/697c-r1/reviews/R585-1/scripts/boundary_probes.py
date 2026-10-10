#!/usr/bin/env python3
"""Reviewer probes of the TSN stack boundary (ctrl_boundary.py) beyond its own controls.

Each probe plants one include into COPIES (never the checkout or the submodule):
the ctrl tree copied as ctrl_boundary's own controls copy it, and a clone of the
stack at its gitlink. It then asks (1) ctrl_boundary.judge() on the copies and,
for a stack plant, (2) the stack's own scripts/check_boundary.py run from the
planted clone. A probe is CAUGHT when either refuses it.
usage: boundary_probes.py <repo> <work> [--rv32]
"""
import shutil, subprocess, sys
from pathlib import Path

repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import ctrl_boundary as cb  # noqa: E402
import fw_rv32  # noqa: E402

rv32 = fw_rv32.compiler() if "--rv32" in sys.argv else None
STACK_REL = "third_party/tsn-c-stack"
PROBES = (
    # (name, side, file, anchor, replacement)
    ("control: stack src includes mbx_hal.h unconditionally", "stack", "src/acmp.c",
     '#include "wire.h"\n', '#include "wire.h"\n#include "mbx_hal.h"\n'),
    ("stack src includes mbx_hal.h under CTRL_REENTRY_ASSERT (a macro the acmp arm defines)", "stack", "src/acmp.c",
     '#ifdef CTRL_REENTRY_ASSERT\n', '#ifdef CTRL_REENTRY_ASSERT\n#include "mbx_hal.h"\n'),
    ("stack src includes ctrl_debug.h under #ifndef NDEBUG (the debug arms' mode)", "stack", "src/maap.c",
     '#ifndef NDEBUG\n#include <assert.h>\n', '#ifndef NDEBUG\n#include <assert.h>\n#include "ctrl_debug.h"\n'),
    ("firmware adapter reaches the stack's tests/acmp_fake.hpp under CTRL_REENTRY_ASSERT (the acmp arm compiles the adapters with it)", "ctrl", "acmp/acmp_mbx.c",
     '#include "acmp_mbx.h"\n',
     '#include "acmp_mbx.h"\n#ifdef CTRL_REENTRY_ASSERT\n#include "../../../../third_party/tsn-c-stack/tests/acmp_fake.hpp"\n#endif\n'),
)


def stack_clone(dest):
    pin = cb.stack_gitlink()
    if dest.exists():
        shutil.rmtree(dest)
    subprocess.run(["git", "-c", "advice.detachedHead=false", "clone", "-q", "--no-hardlinks", str(repo / STACK_REL), str(dest)], check=True)
    subprocess.run(["git", "-c", "advice.detachedHead=false", "-C", str(dest), "checkout", "-q", pin], check=True)
    return dest


def plant(path, old, new):
    text = path.read_text()
    if old is None:
        lines = text.splitlines(keepends=True)
        idx = max(i for i, l in enumerate(lines) if l.startswith("#include")) + 1
        path.write_text("".join(lines[:idx]) + new + "".join(lines[idx:]))
        return
    assert text.count(old) == 1, (path, old)
    path.write_text(text.replace(old, new))


def main():
    rows = []
    for name, side, rel, old, new in PROBES:
        base = work / "probe"
        if base.exists():
            shutil.rmtree(base)
        base.mkdir(parents=True)
        # the planted copies sit side by side as ctrl_boundary's controls lay them out
        ctrl = base / "ctrl"
        shutil.copytree(cb.CTRL, ctrl, ignore=shutil.ignore_patterns("__pycache__"))
        stack = stack_clone(base / "tsn-c-stack")
        nvm_note = ""
        if side == "stack":
            plant(stack / rel, old, new)
        elif side == "ctrl":
            plant(ctrl / rel, old, new)
        findings = cb.judge(cb.Trees(ctrl, stack), rv32, base / "build")
        verdict_ctrl = "refused" if findings else "passes"
        verdict_stack = "n/a"
        if side == "stack":
            res = subprocess.run([sys.executable, "-I", str(stack / "scripts/check_boundary.py"), "--work",
                                  str(base / "stack-work"), "--jobs", "4"], capture_output=True, text=True)
            verdict_stack = "refused" if res.returncode else "passes"
        caught = "refused" in (verdict_ctrl, verdict_stack)
        rows.append((name, verdict_ctrl, verdict_stack, caught, findings[:1], nvm_note))
        print(f"[{'CAUGHT' if caught else 'ESCAPED'}] {name}: ctrl_boundary {verdict_ctrl}"
              f"{(': ' + findings[0]) if findings else ''}; the stack's own gate {verdict_stack}{nvm_note}",
              flush=True)
    shutil.rmtree(work / "probe", ignore_errors=True)


if __name__ == "__main__":
    main()
