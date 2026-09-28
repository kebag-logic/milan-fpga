#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Console service must not arm a writer rejected by identity or shape."""
from pathlib import Path
import subprocess

import test_nvm_firmware as nvm

PRECONDITIONS = {
    "shape": ("return count == NVM_N_REC && bytes == NVM_AREA_RAW &&",
              "return 0 && count == NVM_N_REC && bytes == NVM_AREA_RAW &&", "persistence disabled"),
    "identity": ("if (id != MILAN_ID_MAGIC) {", "if (1) {", "identity mismatch"),
}
LINES = ("", "unknown_command", "milan_status", "milan_nvm", "milan_nvm commit",
         "milan_nvm wipe", "milan_gettime", "milan_settime 1 0", "milan_utc 1 0 37")


def grade(cfg: Path, work: Path, source: str) -> list[str]:
    """Plant rejected startup inputs and exercise every Milan command and Enter."""
    findings = []
    for state, (old, new, message) in PRECONDITIONS.items():
        if source.count(old) != 1:
            raise RuntimeError("disabled-writer precondition anchor changed: " + state)
        bench = nvm.make_bench(cfg, work / state, source.replace(old, new))
        for line in LINES:
            for elapsed in ("0", "2500"):
                raw, summary, _ = nvm.run(bench, "--boot", "--uart", line,
                                        "--uart", line, "--idle-ms", elapsed)
                if message not in raw:
                    raise RuntimeError("disabled-writer precondition was not reached: " + state)
                if any(summary[key] != 0 for key in ("hb", "backed", "stale")):
                    findings.append(f"disabled writer {state} answered {line!r} after {elapsed} ms")
        print(f"disabled-writer {cfg.stem} {state}: 18 console cases; "
              + ("FAIL" if any(state in item for item in findings) else "hb=0 backed=0 stale=0"))
    return findings


def self_test(cfg: Path, work: Path, source: str) -> list[str]:
    """Removing startup admission must fail both independent disabled states."""
    anchor = "\tif (!nvm_started)\n\t\treturn;\n"
    if source.count(anchor) != 1:
        raise RuntimeError("writer admission mutation anchor changed")
    got = grade(cfg, work, source.replace(anchor, ""))
    for state in PRECONDITIONS:
        if not any("disabled writer " + state in item for item in got):
            return ["unguarded service escaped disabled-writer " + state]
    print("disabled-writer mutant: caught in both states")
    return []


def check_link_guard(bench: nvm.Bench) -> None:
    """Removing only the host BIOS marker must make product firmware fail linking."""
    stripped = bench.work / "host-no-dispatch-marker.o"
    subprocess.run(["objcopy", "--strip-symbol=bios_dispatch_hook_required",
                    str(bench.work / "host.o"), str(stripped)], check=True, timeout=120)
    result = subprocess.run(["gcc", str(stripped), str(bench.work / "fw.o"),
                             "-o", str(bench.work / "no-dispatch-marker")],
                            capture_output=True, text=True, timeout=120)
    if result.returncode == 0 or "bios_dispatch_hook_required" not in result.stderr:
        raise RuntimeError("missing BIOS dispatch patch escaped link guard")
    print("dispatch patch link guard: missing marker refused")
