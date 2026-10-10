#!/usr/bin/env python3
"""Reviewer probes for the TSN stack boundary gate (ctrl_boundary.py) of PR #705.

Each probe runs in its own disposable copy of a pristine probe clone (the PR head with its
tsn-c-stack and lwSRP submodules initialised). A probe writes one plant: a firmware-side plant edits
the ctrl tree; a stack-side plant edits the submodule, commits it there and stages the new gitlink in
the copy, so the shared pin check accepts the stack and the boundary itself must name the plant. Then
the copy's own gate runs without --selftest. A probe expecting a refusal passes only when the gate
exits 1 with a finding holding the needle; a probe with needle None records whether the gate refused
at all (a gap probe).

Usage: boundary_probes.py <pristine probe clone> <work dir> <receipt json> [--jobs N] [--only NAME...]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

GATE = "sw/firmware/ctrl/test/ctrl_boundary.py"
STACK = "third_party/tsn-c-stack"

# (name, side, file, anchor, replacement, expected needle or None for a gap probe)
PROBES = [
    ("R585-1 escaped: include in the stack's CTRL_REENTRY_ASSERT region", "stack", "src/acmp.c",
     "#ifdef CTRL_REENTRY_ASSERT\n", "#ifdef CTRL_REENTRY_ASSERT\n#include \"mbx_hal.h\"\n",
     "host [-DCTRL_REENTRY_ASSERT]: the stack's src/acmp.c includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    ("R585-1 escaped: adapter reaches tests/acmp_fake.hpp by its search-path name", "ctrl", "acmp/acmp_mbx.c",
     "#include \"acmp_mbx.h\"\n",
     "#include \"acmp_mbx.h\"\n#ifdef CTRL_REENTRY_ASSERT\n#include \"acmp_fake.hpp\"\n#endif\n",
     "acmp/acmp_mbx.c includes tsn-c-stack/tests/acmp_fake.hpp"),
    ("R585-1 escaped: #ifndef NDEBUG include in a stack source", "stack", "src/maap.c",
     "#ifndef NDEBUG\n#include <assert.h>\n", "#ifndef NDEBUG\n#include <assert.h>\n#include \"ctrl_loop.h\"\n",
     "host [-UNDEBUG]: the stack's src/maap.c includes sw/firmware/ctrl/loop/ctrl_loop.h"),
    ("R584-1-S2: a stack test includes the mailbox HAL", "stack", "tests/test_maap_debug.cpp",
     "#include \"maap.h\"\n", "#include \"maap.h\"\n#include \"mbx_hal.h\"\n",
     "tests: the stack's tests/test_maap_debug.cpp includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    ("new: a stack test header includes the register-map contract", "stack", "tests/acmp_fake.hpp",
     "#include \"acmp.h\"\n", "#include \"acmp.h\"\n#include \"mbx_contract.h\"\n",
     "includes sw/firmware/ctrl/mbx/mbx_contract.h"),
    ("new: RV32-only include in a stack source", "stack", "src/adp.c", "#include <assert.h>\n",
     "#include <assert.h>\n#ifdef __riscv\n#include \"mbx_hal.h\"\n#endif\n",
     "rv32: the stack's src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    ("new: RV32-only firmware reach into a stack source", "ctrl", "adp/adp_mbx.c", "#include \"adp_mbx.h\"\n",
     "#include \"adp_mbx.h\"\n#ifdef __riscv\n#include \"../../../../third_party/tsn-c-stack/src/adp.c\"\n#endif\n",
     "firmware rv32: adp/adp_mbx.c includes tsn-c-stack/src/adp.c"),
    ("new: AECP saved-state mode reaches a stack source", "ctrl", "aecp/aecp_nvm.c", None, None,
     "aecp/aecp_nvm.c includes tsn-c-stack/src/maap.c"),
    ("gap: include under a shape value the image builder computes (IMAGE_SINKS > 1)", "ctrl",
     "test/rv32_image/image_main.c", None, None, None),
    ("gap: a mode a builder writes as two tokens", "stack", "src/maap.c", "#include \"maap.h\"\n",
     "#include \"maap.h\"\n#ifdef CTRL_TWO_TOKEN_MODE\n#include \"mbx_hal.h\"\n#endif\n", None),
]


def sh(argv: list[str], cwd: Path, timeout: int = 1500) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False,
                          env={"PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(cwd), "LC_ALL": "C",
                               "MILAN_RV32_CC": RV32})


def first_include_anchor(text: str) -> str:
    return next(line + "\n" for line in text.splitlines() if line.startswith("#include"))


def run_probe(probe: tuple, pristine: Path, work: Path) -> dict:
    name, side, rel, old, new, needle = probe
    copy = work / f"p{PROBES.index(probe):02d}"
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(pristine, copy, symlinks=True)
    root = copy / STACK if side == "stack" else copy / "sw/firmware/ctrl"
    target = root / rel
    text = target.read_text(encoding="utf-8")
    if old is None:
        old = first_include_anchor(text)
        if rel == "aecp/aecp_nvm.c":
            new = old + "#ifdef AECP_TEST_NVM\n#include \"../../../../third_party/tsn-c-stack/src/maap.c\"\n#endif\n"
        else:
            new = old + "#if IMAGE_SINKS > 1u\n#include \"../../../../../third_party/tsn-c-stack/examples/adp_port.h\"\n#error PROBE-REACHED\n#endif\n"
    if text.count(old) != 1:
        return {"probe": name, "error": f"anchor occurs {text.count(old)} times"}
    target.write_text(text.replace(old, new, 1), encoding="utf-8")
    if "two tokens" in name:
        (copy / "sw/firmware/ctrl/test/planted_two_token.py").write_text(
            '"""A builder that passes its mode as two arguments."""\nfrom ctrl_build import Tree\n'
            'FLAGS = ["-D", "CTRL_TWO_TOKEN_MODE"]\n', encoding="utf-8")
    if side == "stack":
        sub = copy / STACK
        for argv in (["git", "-c", "user.name=probe", "-c", "user.email=probe@invalid", "commit", "-qam", "probe"],):
            res = sh(argv, sub)
            if res.returncode:
                return {"probe": name, "error": res.stderr}
        sh(["git", "add", STACK], copy)
    res = sh([sys.executable, "-B", GATE, "--require-rv32"], copy)
    out = res.stdout + res.stderr
    fails = [ln.strip() for ln in out.splitlines() if "[FAIL]" in ln or "REFUSED" in ln]
    pin = next((ln.strip() for ln in out.splitlines() if ln.startswith("tsn-c-stack at")), "")
    if needle is None:
        verdict = "GAP-ESCAPED" if res.returncode == 0 else "REFUSED"
    else:
        verdict = "CAUGHT" if res.returncode == 1 and any(needle in f for f in fails) else "ESCAPED"
    (work / f"p{PROBES.index(probe):02d}.log").write_text(out, encoding="utf-8")
    shutil.rmtree(copy)
    return {"probe": name, "side": side, "file": rel, "needle": needle, "rc": res.returncode, "pin": pin,
            "verdict": verdict, "findings": fails, "summary": [ln for ln in out.splitlines()
                                                                if ln.startswith("ctrl_boundary:")]}


RV32 = ""


def main() -> int:
    global RV32
    ap = argparse.ArgumentParser()
    ap.add_argument("pristine", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("receipt", type=Path)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--rv32", required=True)
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()
    RV32 = args.rv32
    args.work.mkdir(parents=True, exist_ok=True)
    chosen = [p for p in PROBES if not args.only or any(o in p[0] for o in args.only)]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda p: run_probe(p, args.pristine.resolve(), args.work.resolve()), chosen))
    args.receipt.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    for r in results:
        print(f"[{r.get('verdict', 'ERROR')}] {r['probe']}: rc {r.get('rc')} {r.get('error', '')}")
        for f in r.get("findings", [])[:3]:
            print(f"      {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
