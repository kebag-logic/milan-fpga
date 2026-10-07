#!/usr/bin/env python3
"""Reviewer control: ctrl_image.measure() at the shipping shape with the helpers removed and a REAL libgcc.a
linked in their place must refuse: the pinned SDK's own (ilp32d, at the link) and another build's soft-float
libgcc with M instructions (by the audit). Usage: real_library_controls.py REPO WORK CC OTHER_LIBGCC"""
import sys
from pathlib import Path
from unittest.mock import patch

repo, work, cc, other = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import ctrl_image  # noqa: E402
import subprocess  # noqa: E402

none = work / "none.c"
work.mkdir(parents=True, exist_ok=True)
none.write_text("int image_no_helpers(void);\nint image_no_helpers(void)\n{\n\treturn 0;\n}\n")
pinned = subprocess.run([cc, "-print-libgcc-file-name"], capture_output=True, text=True, check=True).stdout.strip()
fail = 0
for label, lib in (("pinned SDK libgcc.a", pinned), ("other local build libgcc.a", other)):
    with patch.object(ctrl_image, "HELPERS", none), patch.object(ctrl_image, "LIBRARIES", (lib,)):
        try:
            img = ctrl_image.measure(cc, repo / "sw/firmware", ctrl_image.SHAPES[0], work / label.replace(" ", "-"))
            print(f"ESCAPED {label}: measured {img.sections}")
            fail = 1
        except ctrl_image.Refusal as exc:
            print(f"REFUSED {label}: {str(exc).splitlines()[0][-300:]}")
sys.exit(fail)
