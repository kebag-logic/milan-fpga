#!/usr/bin/env python3
"""Render a WaveDrom timing diagram (chronogram): .json -> .svg + .png.

Usage:
    ~/litex-milan/venv/bin/python3 scripts/gen_wavedrom.py docs/diagrams/<name>.json [--width=1600]

The committed, easily-modifiable master is the WaveDrom ``.json`` (the standard
timing-diagram source format); the ``.svg``/``.png`` renders are committed next
to it — never hand-edit a render. Requires the ``wavedrom`` package (present in
the LiteX venv; ``pip install wavedrom`` elsewhere) and ``rsvg-convert``.
"""
import subprocess
import sys
from pathlib import Path

import wavedrom


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
    subprocess.run(["rsvg-convert", "-w", str(width), str(out_svg),
                    "-o", str(out_png)], check=True)
    print(f"wrote {out_svg} and {out_png}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
