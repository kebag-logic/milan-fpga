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

White-background PNG files carry their source SVG hash.
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

try:
    import wavedrom
except ImportError:                                          # pragma: no cover
    sys.exit("gen_wavedrom: the 'wavedrom' package is missing — "
             "python3 -m venv /tmp/wd && /tmp/wd/bin/pip install wavedrom, "
             "then run this script with /tmp/wd/bin/python3")


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_HASH_KEY = "WaveDrom-SVG-SHA256"


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    body = kind + payload
    checksum = zlib.crc32(body)
    return struct.pack(">I", len(payload)) + body + struct.pack(">I", checksum)


def png_metadata(path: Path) -> tuple[tuple[int, int], dict[str, str]]:
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("missing PNG signature")
    position = len(PNG_SIGNATURE)
    dimensions = None
    fields: dict[str, str] = {}
    while position < len(data):
        if position + 12 > len(data):
            raise ValueError("truncated PNG chunk")
        length = struct.unpack(">I", data[position:position + 4])[0]
        end = position + 12 + length
        if end > len(data):
            raise ValueError("truncated PNG payload")
        kind = data[position + 4:position + 8]
        payload = data[position + 8:position + 8 + length]
        stored_crc = struct.unpack(">I", data[position + 8 + length:end])[0]
        if stored_crc != zlib.crc32(kind + payload):
            raise ValueError("invalid PNG checksum")
        if kind == b"IHDR" and len(payload) == 13:
            dimensions = struct.unpack(">II", payload[:8])
        elif kind == b"tEXt" and b"\0" in payload:
            key, value = payload.split(b"\0", 1)
            fields[key.decode("latin-1")] = value.decode("latin-1")
        position = end
        if kind == b"IEND":
            break
    if dimensions is None:
        raise ValueError("missing PNG dimensions")
    return dimensions, fields


def tag_png(path: Path, svg: str) -> None:
    data = path.read_bytes()
    png_metadata(path)
    position = len(PNG_SIGNATURE)
    output = bytearray(PNG_SIGNATURE)
    tagged = False
    while position < len(data):
        length = struct.unpack(">I", data[position:position + 4])[0]
        end = position + 12 + length
        kind = data[position + 4:position + 8]
        output.extend(data[position:end])
        if kind == b"IHDR":
            digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()
            payload = PNG_HASH_KEY.encode("latin-1") + b"\0" + digest.encode("ascii")
            output.extend(png_chunk(b"tEXt", payload))
            tagged = True
        position = end
    if not tagged:
        raise ValueError("cannot tag PNG without IHDR")
    path.write_bytes(output)


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
    if background is not None:
        tag_png(output, svg)


def selftest() -> int:
    with tempfile.TemporaryDirectory(prefix="wavedrom-selftest-") as directory:
        path = Path(directory) / "fixture.png"
        header = struct.pack(">II5B", 2, 3, 8, 2, 0, 0, 0)
        content = PNG_SIGNATURE + png_chunk(b"IHDR", header) + png_chunk(b"IEND", b"")
        path.write_bytes(content)
        source = "<svg/>"
        tag_png(path, source)
        size, fields = png_metadata(path)
        expected = hashlib.sha256(source.encode("utf-8")).hexdigest()
        if size != (2, 3) or fields.get(PNG_HASH_KEY) != expected:
            print("gen_wavedrom selftest: metadata round-trip failed")
            return 1
        damaged = bytearray(path.read_bytes())
        damaged[-1] ^= 1
        path.write_bytes(damaged)
        try:
            png_metadata(path)
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
            render_png(svg, width, candidate_png, background)
            stale = []
            if not out_svg.is_file() or out_svg.read_text(encoding="utf-8") != svg:
                stale.append(str(out_svg))
            if background is None:
                if not out_png.is_file() or out_png.read_bytes() != candidate_png.read_bytes():
                    stale.append(str(out_png))
            else:
                expected_hash = hashlib.sha256(svg.encode("utf-8")).hexdigest()
                try:
                    candidate_size, _candidate_fields = png_metadata(candidate_png)
                    committed_size, committed_fields = png_metadata(out_png)
                except (OSError, ValueError):
                    stale.append(str(out_png))
                else:
                    if committed_size != candidate_size:
                        stale.append(str(out_png))
                    elif committed_fields.get(PNG_HASH_KEY) != expected_hash:
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
