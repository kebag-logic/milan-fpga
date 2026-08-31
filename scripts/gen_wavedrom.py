#!/usr/bin/env python3
"""Render a WaveDrom timing diagram: .json -> .svg + .png.

Usage:
    python3 scripts/gen_wavedrom.py docs/diagrams/<name>.json [--width=1600]
    python3 scripts/gen_wavedrom.py docs/diagrams/<name>.json --check
    python3 scripts/gen_wavedrom.py docs/diagrams/<name>.json --background=white

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
import tempfile
from pathlib import Path

try:
    import wavedrom
except ImportError:                                          # pragma: no cover
    sys.exit("gen_wavedrom: the 'wavedrom' package is missing — "
             "python3 -m venv /tmp/wd && /tmp/wd/bin/pip install wavedrom, "
             "then run this script with /tmp/wd/bin/python3")


def render_svg(src: Path, background: str | None) -> str:
    svg = wavedrom.render(src.read_text(encoding="utf-8")).tostring()
    if background is None:
        return svg
    rectangle = (
        f'<rect width="100%" height="100%" fill="{background}"/>'
    )
    return svg.replace(">", ">" + rectangle, 1)


def render_png(
    svg: str,
    width: int,
    output: Path,
    background: str | None,
) -> None:
    with tempfile.TemporaryDirectory(prefix="wavedrom-") as directory:
        temporary_svg = Path(directory) / "diagram.svg"
        temporary_svg.write_text(svg, encoding="utf-8")
        command = ["rsvg-convert"]
        if background is not None:
            command.extend(["-b", background])
        command.extend(
            ["-w", str(width), str(temporary_svg), "-o", str(output)]
        )
        subprocess.run(command, check=True)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = Path(sys.argv[1])
    width = 1600
    checking = False
    background = None
    for arg in sys.argv[2:]:
        if arg.startswith("--width="):
            width = int(arg.split("=", 1)[1])
        elif arg == "--check":
            checking = True
        elif arg.startswith("--background="):
            background = arg.split("=", 1)[1]
            if not background:
                print("gen_wavedrom: background cannot be empty")
                return 2
        else:
            print(f"gen_wavedrom: unknown option: {arg}")
            return 2
    svg = render_svg(src, background)
    out_svg = src.with_suffix(".svg")
    out_png = src.with_suffix(".png")
    if shutil.which("rsvg-convert") is None:
        print("gen_wavedrom: 'rsvg-convert' is missing")
        return 1
    if checking:
        with tempfile.TemporaryDirectory(prefix="wavedrom-check-") as directory:
            candidate_png = Path(directory) / "diagram.png"
            render_png(svg, width, candidate_png, background)
            stale = []
            if not out_svg.is_file() or out_svg.read_text(encoding="utf-8") != svg:
                stale.append(str(out_svg))
            if not out_png.is_file() or out_png.read_bytes() != candidate_png.read_bytes():
                stale.append(str(out_png))
        if stale:
            print("gen_wavedrom: stale: " + ", ".join(stale))
            return 1
        print(f"WaveDrom current: {src}")
        return 0
    out_svg.write_text(svg, encoding="utf-8")
    render_png(svg, width, out_png, background)
    print(f"wrote {out_svg} and {out_png}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
