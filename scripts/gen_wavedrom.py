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
The shared manifest pins reviewed decompressed rasters.
Renderer changes require regeneration and visual review.
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
    update_pixel_manifest,
    verify_pixel_manifest,
)

try:
    import wavedrom
except ImportError:                                          # pragma: no cover
    sys.exit("gen_wavedrom: the 'wavedrom' package is missing — "
             "python3 -m venv /tmp/wd && /tmp/wd/bin/pip install wavedrom, "
             "then run this script with /tmp/wd/bin/python3")


PNG_HASH_KEY = "WaveDrom-SVG-SHA256"
PNG_SOURCE_HASH_KEY = "Milan-WaveDrom-JSON-SHA256"
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "diagrams" / "PNG_MANIFEST.json"
TRACKED_RASTERS = {
    "docs/diagrams/wd_axis_backpressure.png": (
        "docs/diagrams/wd_axis_backpressure.json"
    ),
    "docs/diagrams/wd_cdc_handshake.png": (
        "docs/diagrams/wd_cdc_handshake.json"
    ),
}


def tracked_names(output: Path, source: Path) -> tuple[str, str] | None:
    """Return manifest names for a published WaveDrom pair."""
    try:
        artifact_name = output.resolve().relative_to(ROOT).as_posix()
        source_name = source.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return None
    if TRACKED_RASTERS.get(artifact_name) != source_name:
        return None
    return artifact_name, source_name


def tag_png(path: Path, svg: str, source: Path) -> None:
    """Stamp the raster with the SVG and JSON digests --check later reads back."""
    set_text_fields(
        path,
        {
            PNG_HASH_KEY: hashlib.sha256(svg.encode("utf-8")).hexdigest(),
            PNG_SOURCE_HASH_KEY: source_digest(source),
        },
    )


def render_svg(src: Path, background: str | None) -> str:
    """The WaveDrom render, with an opaque backdrop injected when one is asked
    for - the default render is transparent and unreadable on a dark page."""
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
    """Rasterise the SVG through rsvg-convert at `width`, then tag the PNG."""
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
    """Prove the three raster controls still fail loudly: the metadata
    round-trip, a valid PNG whose pixels changed, and a damaged CRC."""
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
        manifest = Path(directory) / "manifest.json"
        update_pixel_manifest(
            manifest,
            "fixture.png",
            "fixture.json",
            path,
            source_path,
        )
        original = path.read_bytes()
        wrong_raster = b"".join(b"\0" + b"\xff" * 6 for _row in range(3))
        path.write_bytes(
            encode_chunks(
                [
                    Chunk(b"IHDR", header),
                    Chunk(b"IDAT", zlib.compress(wrong_raster)),
                    Chunk(b"IEND", b""),
                ]
            )
        )
        try:
            verify_pixel_manifest(
                manifest,
                "fixture.png",
                "fixture.json",
                path,
                source_path,
            )
        except ValueError as error:
            if "raster differs" not in str(error):
                print(f"gen_wavedrom selftest: wrong pixel error: {error}")
                return 1
        else:
            print("gen_wavedrom selftest: valid wrong raster escaped")
            return 1
        path.write_bytes(original)
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
    print(
        "gen_wavedrom selftest: OK "
        "(metadata, checksum, and raster-manifest controls)"
    )
    return 0


def main() -> int:
    """Render one diagram or --check it; 1 when a render is stale, 2 on a bad
    option."""
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
                names = tracked_names(out_png, src)
                if names is None:
                    committed_info = inspect_png(out_png)
                else:
                    committed_info = verify_pixel_manifest(
                        MANIFEST,
                        names[0],
                        names[1],
                        out_png,
                        src,
                    )
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
    names = tracked_names(out_png, src)
    if names is not None:
        update_pixel_manifest(
            MANIFEST,
            names[0],
            names[1],
            out_png,
            src,
        )
    print(f"wrote {out_svg} and {out_png}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
