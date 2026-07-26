#!/usr/bin/env python3
"""Render a WaveDrom timing diagram (chronogram): .json -> .svg + .png.

Usage:
    python3 scripts/gen_wavedrom.py docs/diagrams/<name>.json [--width=1600]

The committed, easily-modifiable master is the WaveDrom ``.json`` (the standard
timing-diagram source format); the ``.svg``/``.png`` renders are committed next
to it — never hand-edit a render.

Two dependencies, neither of them project-specific:

* the ``wavedrom`` Python package — any interpreter will do, e.g.
  ``python3 -m venv /tmp/wd && /tmp/wd/bin/pip install wavedrom``;
* ``rsvg-convert`` (librsvg) on ``PATH``, for the ``.png``.

Rendering is deterministic: re-running over an unchanged ``.json`` reproduces
the committed ``.svg``/``.png`` byte for byte.
"""
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import wavedrom
except ImportError:                                          # pragma: no cover
    sys.exit("gen_wavedrom: the 'wavedrom' package is missing — "
             "python3 -m venv /tmp/wd && /tmp/wd/bin/pip install wavedrom, "
             "then run this script with /tmp/wd/bin/python3")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = Path(sys.argv[1])
    width = 1600
    for arg in sys.argv[2:]:
        if arg.startswith("--width="):
            width = int(arg.split("=", 1)[1])
    svg = wavedrom.render(src.read_text(encoding="utf-8"))
    out_svg = src.with_suffix(".svg")
    out_svg.write_text(svg.tostring(), encoding="utf-8")
    out_png = src.with_suffix(".png")
    if shutil.which("rsvg-convert") is None:
        return (f"gen_wavedrom: wrote {out_svg}, but 'rsvg-convert' (librsvg) is "
                f"not on PATH — install it and re-run to refresh {out_png}")
    subprocess.run(["rsvg-convert", "-w", str(width), str(out_svg),
                    "-o", str(out_png)], check=True)
    print(f"wrote {out_svg} and {out_png}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
