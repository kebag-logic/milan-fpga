#!/usr/bin/env python3
"""Render a WaveDrom timing diagram: .json -> .svg + .png.

Usage:
    python3 scripts/gen_wavedrom.py docs/diagrams/<name>.json [--width=1600]
    python3 scripts/gen_wavedrom.py docs/diagrams/<name>.json --check
    python3 scripts/gen_wavedrom.py docs/diagrams/<name>.json --background=white
    python3 scripts/gen_wavedrom.py --selftest

The committed, easily-modifiable master is the WaveDrom ``.json`` (the standard
timing-diagram source format); the ``.svg``/``.png`` renders are committed next
to it — never hand-edit a render.

Two dependencies, neither of them project-specific:

* the ``wavedrom`` Python package — any interpreter will do, e.g.
  ``python3 -m venv /tmp/wd && /tmp/wd/bin/pip install wavedrom``;
* ``rsvg-convert`` (librsvg) on ``PATH``, for the ``.png``.

SVG rendering is deterministic.

PNG files carry their JSON and generated-SVG hashes.
Raster bytes may vary across librsvg and font versions.
"""
import hashlib
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

from png_artifact import (
    Chunk,
    encode_chunks,
    inspect_png,
    set_text_fields,
    source_digest,
)

try:
    import wavedrom
except ImportError:                                          # pragma: no cover
    sys.exit("gen_wavedrom: the 'wavedrom' package is missing — "
             "python3 -m venv /tmp/wd && /tmp/wd/bin/pip install wavedrom, "
             "then run this script with /tmp/wd/bin/python3")


PNG_HASH_KEY = "WaveDrom-SVG-SHA256"
PNG_SOURCE_HASH_KEY = "Milan-WaveDrom-JSON-SHA256"


def tag_png(path: Path, svg: str, source: Path) -> None:
    set_text_fields(
        path,
        {
            PNG_HASH_KEY: hashlib.sha256(svg.encode("utf-8")).hexdigest(),
            PNG_SOURCE_HASH_KEY: source_digest(source),
        },
    )


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
    source: Path,
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
    tag_png(output, svg, source)


def selftest() -> int:
    with tempfile.TemporaryDirectory(prefix="wavedrom-selftest-") as directory:
        path = Path(directory) / "fixture.png"
        source_path = Path(directory) / "fixture.json"
        source_path.write_text('{"signal": []}\n', encoding="utf-8")
        header = struct.pack(">II5B", 2, 3, 8, 2, 0, 0, 0)
        raster = b"".join(b"\0" + b"\0" * 6 for _row in range(3))
        path.write_bytes(
            encode_chunks(
                [
                    Chunk(b"IHDR", header),
                    Chunk(b"IDAT", zlib.compress(raster)),
                    Chunk(b"IEND", b""),
                ]
            )
        )
        source = "<svg/>"
        tag_png(path, source, source_path)
        info = inspect_png(path)
        expected = hashlib.sha256(source.encode("utf-8")).hexdigest()
        if (
            (info.width, info.height) != (2, 3)
            or info.text.get(PNG_HASH_KEY) != expected
            or info.text.get(PNG_SOURCE_HASH_KEY) != source_digest(source_path)
        ):
            print("gen_wavedrom selftest: metadata round-trip failed")
            return 1
        damaged = bytearray(path.read_bytes())
        damaged[-1] ^= 1
        path.write_bytes(damaged)
        try:
            inspect_png(path)
        except ValueError:
            pass
        else:
            print("gen_wavedrom selftest: damaged checksum escaped")
            return 1
    print("gen_wavedrom selftest: OK (metadata and checksum controls)")
    return 0


def main():
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
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
            render_png(svg, width, candidate_png, background, src)
            stale = []
            if not out_svg.is_file() or out_svg.read_text(encoding="utf-8") != svg:
                stale.append(str(out_svg))
            expected_hash = hashlib.sha256(svg.encode("utf-8")).hexdigest()
            try:
                candidate_info = inspect_png(candidate_png)
                committed_info = inspect_png(out_png)
            except (OSError, ValueError):
                stale.append(str(out_png))
            else:
                if (
                    (committed_info.width, committed_info.height)
                    != (candidate_info.width, candidate_info.height)
                ):
                    stale.append(str(out_png))
                elif committed_info.text.get(PNG_HASH_KEY) != expected_hash:
                    stale.append(str(out_png))
                elif (
                    committed_info.text.get(PNG_SOURCE_HASH_KEY)
                    != source_digest(src)
                ):
                    stale.append(str(out_png))
        if stale:
            print("gen_wavedrom: stale: " + ", ".join(stale))
            return 1
        print(f"WaveDrom current: {src}")
        return 0
    out_svg.write_text(svg, encoding="utf-8")
    render_png(svg, width, out_png, background, src)
    print(f"wrote {out_svg} and {out_png}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
