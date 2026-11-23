"""Apply one named gate-41 mutant to a copy of an extracted tree: mutant.py <tree> <name> <round2-ctrl_loop.h>.
Each edit must apply exactly once."""
import sys
from pathlib import Path

tree, name, round2 = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
loop = tree / "sw/firmware/ctrl/loop/ctrl_loop.h"
host = tree / "sw/firmware/ctrl/host/ctrl_loop_host.h"
rows = "".join(l + "\n" for l in host.read_text().splitlines()
               if l.startswith("#define CTRL_LOOP_") and not l.startswith("#define CTRL_LOOP_HOST_H"))


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    assert text.count(old) == 1, f"{name}: {old!r} occurs {text.count(old)} times in {path.name}"
    path.write_text(text.replace(old, new))


if name == "m1-round2-placement":      # restore 66b4def3's ctrl_loop.h: the host row inside THE SHAPES' chain
    loop.write_text(round2.read_text())
elif name == "m2-figures-beside-chain":   # the host figures stated in ctrl_loop.h, outside the chain
    edit(loop, '#include "../host/ctrl_loop_host.h"\n', rows)
elif name == "m3-guard-without-macro":    # the guard drops CTRL_HOST_PLATFORM
    edit(loop, "#if defined(CTRL_HOST_PLATFORM) && CTRL_LOOP_SHAPE(1u, 1u, 2u)\n", "#if CTRL_LOOP_SHAPE(1u, 1u, 2u)\n")
    edit(tree / "sw/builder/test_builder.py", "HOST_SHAPE_GUARD = ('#if defined(CTRL_HOST_PLATFORM) && CTRL_LOOP_SHAPE(1u, 1u, 2u)\\n'",
         "HOST_SHAPE_GUARD = ('#if CTRL_LOOP_SHAPE(1u, 1u, 2u)\\n'")
elif name == "m3b-guard-macro-always-true":  # the guard's macro test always true; the gate's guard text follows it
    edit(loop, "#if defined(CTRL_HOST_PLATFORM) && CTRL_LOOP_SHAPE(1u, 1u, 2u)\n", "#if 1 && CTRL_LOOP_SHAPE(1u, 1u, 2u)\n")
    edit(tree / "sw/builder/test_builder.py", "HOST_SHAPE_GUARD = ('#if defined(CTRL_HOST_PLATFORM) && CTRL_LOOP_SHAPE(1u, 1u, 2u)\\n'",
         "HOST_SHAPE_GUARD = ('#if 1 && CTRL_LOOP_SHAPE(1u, 1u, 2u)\\n'")
elif name == "m4-host-figure-not-1x1":    # a host figure that is not the 1x1/1if row's
    edit(host, "#define CTRL_LOOP_SLICE_US 950u\n", "#define CTRL_LOOP_SLICE_US 900u\n")
else:
    sys.exit(f"unknown mutant {name}")
print(f"{name}: applied")
