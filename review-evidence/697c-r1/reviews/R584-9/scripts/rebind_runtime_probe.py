"""R584-9 runtime probe for the helper rebound inside ctrl_build.py (E1 of census_escape_probe.py).

Usage: python3 -I rebind_runtime_probe.py <checkout> [--controls <work dir>]
The checkout must hold tsn-c-stack at its gitlink. Prints the census's findings on the checkout's pin-proof
modules, whether ctrl_build.git is still the helper, every argv the harness's runner (fw_gtest.run) starts while
stack_pin() decides the pin, and stack_pin's verdict. With --controls, also runs ctrl_pin.pin_controls with no
Makefile builder and prints its verdict lines."""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(root / "sw/firmware/gtest"))
import fw_gtest  # noqa: E402

started = []
real = fw_gtest.run


def logged(argv, *a, **k):
    started.append(list(argv))
    return real(argv, *a, **k)


fw_gtest.run = logged
import ctrl_build  # noqa: E402
import ctrl_pin  # noqa: E402

print("census findings:", ctrl_pin.proof_census())
print("ctrl_build.git is the helper defined as 'git':", getattr(ctrl_build.git, "__name__", None) == "git")
print("ctrl_build.git:", ctrl_build.git.__qualname__)
started.clear()
print("stack_pin:", ctrl_build.stack_pin())
print(f"runner starts during stack_pin: {len(started)}")
for argv in started:
    print("  runner argv:", argv[:4] + (["..."] if len(argv) > 4 else []))
if "--controls" in sys.argv:
    work = Path(sys.argv[sys.argv.index("--controls") + 1])
    work.mkdir(parents=True, exist_ok=True)
    bad, total = ctrl_pin.pin_controls(work, [])
    print(f"pin controls: {bad} misbehaved of {total}")
