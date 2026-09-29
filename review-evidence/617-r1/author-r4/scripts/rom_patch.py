#!/usr/bin/env python3
"""Apply the ROM-image preparation change to a capture_coherence mutants.py (path given)."""
import sys
from pathlib import Path

p = Path(sys.argv[1])
s = p.read_text()
edits = [
    ('#: the build break the arm plants to prove a failed build shows its cause: a\n',
     '#: the dp harness\'s processor ROM images, which every dp build lists as\n'
     '#: prerequisites in the suite directory: made once, before the builds run side\n'
     '#: by side, so no two builds generate them at once\n'
     'ROM_IMAGES = ("ltn_rom.hex", "ucode.hex")\n'
     '#: the build break the arm plants to prove a failed build shows its cause: a\n'),
    ('class Unit(NamedTuple):\n',
     'def rom_images_result(work: Path) -> Result:\n'
     '    """The dp harness\'s ROM images (ROM_IMAGES), made once before any build\n'
     '    starts; a failure prints its output, and no build can use them."""\n'
     '    tag = "rom_images"\n'
     '    rc, out = run_child(["make", "-s", "-C", str(HERE), *ROM_IMAGES],\n'
     '                        env={**os.environ, "MAKEFLAGS": BUILD_MAKEFLAGS})\n'
     '    build_log(work, tag).write_text(out)\n'
     '    if rc == 0:\n'
     '        return True, []\n'
     '    return False, ["[FAIL] the dp harness\'s ROM images could not be made; no dp build can run",\n'
     '                   *build_tail(build_log(work, tag))]\n'
     '\n'
     '\n'
     'class Unit(NamedTuple):\n'),
    ('    with tempfile.TemporaryDirectory(prefix="capture-coherence-mutants-") as td:\n'
     '        verdicts = run_units(arm_units(Path(td)), len(os.sched_getaffinity(0)))\n',
     '    with tempfile.TemporaryDirectory(prefix="capture-coherence-mutants-") as td:\n'
     '        made, lines = rom_images_result(Path(td))\n'
     '        if not made:\n'
     '            emit(lines)\n'
     '            return 1\n'
     '        verdicts = run_units(arm_units(Path(td)), len(os.sched_getaffinity(0)))\n'),
    ('the units finish in. Every build runs with MAKEFLAGS emptied (BUILD_MAKEFLAGS)\n',
     'the units finish in; the dp harness\'s ROM images are made once, before any\n'
     'build starts. Every build runs with MAKEFLAGS emptied (BUILD_MAKEFLAGS)\n'),
]
for a, b in edits:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
p.write_text(s)
print("patched", p)
