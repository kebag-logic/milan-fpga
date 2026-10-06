#!/usr/bin/env python3
"""Remove each binding filter in memory and require its new control to fail."""
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
sys.path.insert(0, str(root / "sw/firmware/gtest"))
import fw_rv32_selftest as subject

cc = str(packet / "scratch/sdk/bin/riscv32-linux-gcc")
os.environ["MILAN_RV32_CC"] = cc
for arm in ("ctrl", "nvm"):
    if arm == "ctrl":
        original = subject.ctrl_arms.run
        def no_filter(argv, **kwargs):
            return original([x for x in argv if x != "--extern-only"], **kwargs)
        context = patch.object(subject.ctrl_arms, "run", no_filter)
    else:
        original = subject.nvm_rv32._tool
        def no_filter(compiler, name, *args):
            return original(compiler, name, *(x for x in args if x != "--extern-only"))
        context = patch.object(subject.nvm_rv32, "_tool", no_filter)
    with tempfile.TemporaryDirectory(dir=packet / "scratch", prefix="sensitivity-") as tmp:
        try:
            with context:
                subject.runtime_cases(cc, Path(tmp))
        except AssertionError:
            import traceback
            frames = traceback.extract_tb(sys.exc_info()[2])
            expected = 107 if arm == "ctrl" else 132
            # Require the failure to be the new masked-dependency assertion.
            assert any(f.filename.endswith("fw_rv32_selftest.py") and
                       "assert" in (f.line or "") and
                       ("__unexpected_service" in (f.line or "")) for f in frames), frames
            print(f"PASS: removing {arm} external-only filter breaks its new same-name static control")
        else:
            raise AssertionError(f"{arm}: removed binding filter escaped")
print("PASS: both new controls detect removal of their respective binding filter")
