"""mutate.py <tree> <name> <r2-ctrl_loop.h>: apply one named gate-41 mutant to a disposable copy; each edit applies once.
m1: 66b4def3's ctrl_loop.h restored (the host row inside THE SHAPES' chain).
mA: the guard loses its shape test (any CTRL_HOST_PLATFORM build takes the host header); the gate's guard text follows,
    so only the compile checks can catch it. The host header's own #error on the shape is removed too.
mB: a host bound (CTRL_LOOP_TX_MS) that is not the 1x1/1if row's.
mC: the host header loses one figure (CTRL_LOOP_TX_MS).
mD: the host header's figures are left in it AND restated inside THE SHAPES' chain as a (1, 1, 2) #elif row."""
import sys
from pathlib import Path

tree, name, r2 = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
loop = tree / "sw/firmware/ctrl/loop/ctrl_loop.h"
host = tree / "sw/firmware/ctrl/host/ctrl_loop_host.h"
gate = tree / "sw/builder/test_builder.py"
GUARD = "#if defined(CTRL_HOST_PLATFORM) && CTRL_LOOP_SHAPE(1u, 1u, 2u)\n"


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    assert text.count(old) == 1, f"{name}: {old!r} occurs {text.count(old)} times in {path.name}"
    path.write_text(text.replace(old, new))


if name == "m1":
    loop.write_text(r2.read_text())
elif name == "mA":
    edit(loop, GUARD, "#if defined(CTRL_HOST_PLATFORM)\n")
    edit(gate, "HOST_SHAPE_GUARD = ('#if defined(CTRL_HOST_PLATFORM) && CTRL_LOOP_SHAPE(1u, 1u, 2u)\\n'",
         "HOST_SHAPE_GUARD = ('#if defined(CTRL_HOST_PLATFORM)\\n'")
    edit(host, '#elif !CTRL_LOOP_SHAPE(1u, 1u, 2u)\n#error "ctrl_loop_host.h: the host platform\'s shape is (1, 1, 2) alone"\n', "")
elif name == "mB":
    edit(host, "#define CTRL_LOOP_TX_MS 35u\n", "#define CTRL_LOOP_TX_MS 36u\n")
elif name == "mC":
    edit(host, "#define CTRL_LOOP_TX_MS 35u\n", "")
elif name == "mD":
    rows = "".join(l + "\n" for l in host.read_text().splitlines()
                   if l.startswith("#define CTRL_LOOP_") and not l.startswith("#define CTRL_LOOP_HOST_H"))
    unlisted = '#else\n#error "THE SHAPES: the shape'
    edit(loop, unlisted, "#elif CTRL_LOOP_SHAPE(1u, 1u, 2u)\n" + rows + unlisted)
else:
    sys.exit(f"unknown mutant {name}")
print(f"{name}: applied")
