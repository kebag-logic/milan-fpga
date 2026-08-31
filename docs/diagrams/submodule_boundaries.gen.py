#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the verified submodule-boundary diagram.

The generator reads every path, URL, and pin from Git.
Handwritten metadata only explains each dependency's role.

Usage:
    python3 docs/diagrams/submodule_boundaries.gen.py
    python3 docs/diagrams/submodule_boundaries.gen.py --check
    python3 docs/diagrams/submodule_boundaries.gen.py --selftest
"""

from __future__ import annotations

import configparser
import hashlib
import html
import shutil
import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass
from pathlib import Path
from pathlib import PurePosixPath


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from png_artifact import (  # noqa: E402
    render_svg_png,
    reviewed_png_current,
    update_pixel_manifest,
    zero_raster_bytes,
)


BASE = ROOT / "docs" / "diagrams" / "submodule_boundaries"
WIDTH = 1500
HEIGHT = 900
RASTER_WIDTH = 2400
DRAWIO_HASH_KEY = "Milan-Drawio-SHA256"
MANIFEST = ROOT / "docs" / "diagrams" / "PNG_MANIFEST.json"
ARTIFACT_NAME = "docs/diagrams/submodule_boundaries.png"
SOURCE_NAME = "docs/diagrams/submodule_boundaries.drawio"


@dataclass(frozen=True)
class Role:
    purpose: str
    wrapper: str
    path_label: str
    donor_gate: str
    root_gate: str
    status: str
    fill: str
    stroke: str


ROLES = {
    "protocol-processor": Role(
        "ADP, ACMP, AECP, and SRP engine",
        "hdl/milan/KL_pp_shadow.sv",
        "wrapper",
        "protocol-processor/scripts/run_suites.sh",
        "tb/verilator/pp_shadow",
        "ACTIVE CONTROL",
        "#E8F5E9",
        "#2E7D32",
    ),
    "gptp-processor": Role(
        "IEEE 802.1AS fabric engine",
        "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv",
        "wrapper",
        "make -C gptp-processor",
        "tb/verilator/gptp_shadow",
        "ACTIVE TIME",
        "#E3F2FD",
        "#1565C0",
    ),
    "third_party/verilog-axis": Role(
        "AXI-Stream FIFO and demultiplexer primitives",
        "hdl/ieee8021q/ts/traffic_queues.sv",
        "representative consumer",
        "upstream project evidence",
        "tb/verilator/queues",
        "ACTIVE VENDOR",
        "#FFF3E0",
        "#EF6C00",
    ),
    "external": Role(
        "Legacy Ethernet MAC implementation",
        "hdl/milan/milan_top.sv",
        "legacy root",
        "donor project evidence",
        "none; legacy top cannot elaborate",
        "LEGACY ONLY",
        "#ECEFF1",
        "#546E7A",
    ),
}


@dataclass(frozen=True)
class Submodule:
    path: str
    url: str
    pin: str
    role: Role


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def read_submodules() -> list[Submodule]:
    config = configparser.ConfigParser()
    config.read(ROOT / ".gitmodules")
    found: dict[str, str] = {}
    for section in config.sections():
        path = config.get(section, "path")
        found[path] = config.get(section, "url")

    if set(found) != set(ROLES):
        missing = sorted(set(found) - set(ROLES))
        stale = sorted(set(ROLES) - set(found))
        raise SystemExit(
            f"submodule role map disagrees: missing={missing}, stale={stale}"
        )

    modules = []
    for path in sorted(found):
        stage = git("ls-files", "--stage", "--", path).split()
        if len(stage) < 4 or stage[0] != "160000" or stage[2] != "0":
            raise SystemExit(f"{path}: expected one stage-0 gitlink")
        pin = stage[1]
        role = ROLES[path]
        wrapper = ROOT / role.wrapper
        if not wrapper.is_file():
            raise SystemExit(f"{path}: missing integration evidence {role.wrapper}")
        if role.root_gate.startswith("tb/") and not (ROOT / role.root_gate).is_dir():
            raise SystemExit(f"{path}: missing root gate {role.root_gate}")
        modules.append(Submodule(path, found[path], pin, role))
    return modules


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def module_positions() -> dict[str, tuple[int, int]]:
    return {
        "protocol-processor": (35, 135),
        "gptp-processor": (35, 500),
        "third_party/verilog-axis": (1045, 135),
        "external": (1045, 500),
    }


def svg(modules: list[Submodule]) -> str:
    positions = module_positions()
    by_path = {module.path: module for module in modules}
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
        f'height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" '
        'font-family="Helvetica,Arial,sans-serif">',
        '<rect width="1500" height="900" fill="#FAFAFA"/>',
        '<defs><marker id="arrow" markerWidth="12" markerHeight="12" '
        'refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" '
        'fill="#455A64"/></marker></defs>',
        '<text x="48" y="48" font-size="30" font-weight="bold" '
        'fill="#263238">Verified submodule boundaries</text>',
        '<text x="48" y="78" font-size="18" fill="#546E7A">'
        'Submodule paths and revisions come directly from Git.</text>',
    ]

    root_x, root_y, root_w, root_h = 540, 270, 420, 310
    lines.extend(
        [
            f'<rect x="{root_x}" y="{root_y}" width="{root_w}" '
            f'height="{root_h}" rx="16" fill="#F3E5F5" '
            'stroke="#6A1B9A" stroke-width="3"/>',
            '<text x="750" y="310" text-anchor="middle" font-size="22" '
            'font-weight="bold" fill="#4A148C">milan-fpga</text>',
            '<text x="750" y="342" text-anchor="middle" font-size="18" '
            'fill="#4A148C">integration and verification owner</text>',
            '<rect x="580" y="375" width="340" height="62" rx="9" '
            'fill="#FFFFFF" stroke="#7B1FA2"/>',
            '<text x="750" y="401" text-anchor="middle" font-size="18" '
            'font-weight="bold">milan_datapath.sv</text>',
            '<text x="750" y="424" text-anchor="middle" font-size="16">'
            'primary product boundary</text>',
            '<rect x="580" y="455" width="340" height="94" rx="9" '
            'fill="#FFFFFF" stroke="#7B1FA2"/>',
            '<text x="750" y="480" text-anchor="middle" font-size="18" '
            'font-weight="bold">Root integration tests</text>',
            '<text x="750" y="505" text-anchor="middle" font-size="16">'
            'Donor gates remain</text>',
            '<text x="750" y="527" text-anchor="middle" font-size="16">'
            'independently required.</text>',
        ]
    )

    connections = {
        "protocol-processor": ((455, 260), (540, 350), "wrapper"),
        "gptp-processor": ((455, 625), (540, 500), "wrapper"),
        "third_party/verilog-axis": ((1045, 260), (960, 350), "RTL"),
        "external": ((1045, 625), (960, 535), "legacy"),
    }
    for path, (start, end, label) in connections.items():
        dash = ' stroke-dasharray="9,7"' if path == "external" else ""
        sx, sy = start
        ex, ey = end
        middle = (sx + ex) // 2
        lines.append(
            f'<path d="M{sx},{sy} L{middle},{sy} L{middle},{ey} L{ex},{ey}" '
            f'fill="none" stroke="#455A64" stroke-width="2.5" '
            f'marker-end="url(#arrow)"{dash}/>'
        )
        lines.append(
            f'<text x="{middle}" y="{(sy + ey) // 2 - 7}" '
            f'text-anchor="middle" font-size="16" fill="#37474F">'
            f'{esc(label)}</text>'
        )

    for path, (x, y) in positions.items():
        module = by_path[path]
        role = module.role
        wrapper = PurePosixPath(role.wrapper)
        purpose_lines = textwrap.wrap(
            role.purpose,
            width=38,
            break_long_words=False,
            break_on_hyphens=False,
        )
        if len(purpose_lines) > 2:
            raise SystemExit(f"{path}: purpose needs more than two lines")
        purpose_y = y + (112 if len(purpose_lines) == 2 else 123)
        lines.extend(
            [
                f'<rect x="{x}" y="{y}" width="420" height="270" rx="13" '
                f'fill="{role.fill}" stroke="{role.stroke}" stroke-width="2.5"/>',
                f'<rect x="{x + 18}" y="{y + 17}" width="160" height="32" '
                f'rx="16" fill="{role.stroke}"/>',
                f'<text x="{x + 98}" y="{y + 39}" text-anchor="middle" '
                f'font-size="15" font-weight="bold" fill="#FFFFFF">'
                f'{esc(role.status)}</text>',
                f'<text x="{x + 18}" y="{y + 80}" font-size="20" '
                f'font-weight="bold" fill="#212121">{esc(path)}</text>',
                *[
                    f'<text x="{x + 18}" y="{purpose_y + index * 22}" '
                    f'font-size="16" fill="#37474F">{esc(line)}</text>'
                    for index, line in enumerate(purpose_lines)
                ],
                f'<text x="{x + 18}" y="{y + 162}" font-size="16" '
                f'fill="#37474F">pin {module.pin[:12]}</text>',
                f'<text x="{x + 18}" y="{y + 188}" font-size="16" '
                f'fill="#37474F">{esc(role.path_label)}:</text>',
                f'<text x="{x + 18}" y="{y + 209}" font-size="16" '
                f'fill="#37474F">{esc(wrapper.parent)}/</text>',
                f'<text x="{x + 18}" y="{y + 230}" font-size="16" '
                f'fill="#37474F">{esc(wrapper.name)}</text>',
                f'<text x="{x + 18}" y="{y + 254}" font-size="16" '
                f'fill="#37474F">test: {esc(role.root_gate)}</text>',
            ]
        )

    lines.extend(
        [
            '<rect x="190" y="785" width="1120" height="70" rx="12" '
            'fill="#FFFFFF" stroke="#78909C" stroke-width="2"/>',
            '<text x="750" y="813" text-anchor="middle" font-size="18" '
            'font-weight="bold" fill="#263238">Evidence rule</text>',
            '<text x="750" y="839" text-anchor="middle" font-size="17" '
            'fill="#455A64">Run donor suites before root integration suites.</text>',
            '</svg>',
        ]
    )
    return "\n".join(lines) + "\n"


def drawio(modules: list[Submodule]) -> str:
    positions = module_positions()
    by_path = {module.path: module for module in modules}
    module_ids = {
        path: "sub-" + path.replace("/", "-")
        for path in positions
    }
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']

    def vertex(
        ident: str,
        x: int,
        y: int,
        width: int,
        height: int,
        label: str,
        fill: str,
        stroke: str,
        font_size: int = 16,
    ) -> None:
        style = (
            "rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;"
            f"spacingTop=12;spacingLeft=12;fontSize={font_size};"
            "fontFamily=Helvetica;"
            f"fillColor={fill};strokeColor={stroke};strokeWidth=2;"
        )
        cells.append(
            f'<mxCell id="{ident}" value="{esc(label)}" style="{style}" '
            f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" '
            f'width="{width}" height="{height}" as="geometry"/></mxCell>'
        )

    vertex(
        "title",
        35,
        25,
        900,
        65,
        "<b>Verified submodule boundaries</b><br>"
        "Submodule paths and revisions come directly from Git.",
        "none",
        "none",
        22,
    )
    vertex(
        "root",
        540,
        270,
        420,
        310,
        "<b>milan-fpga</b><br>integration and verification owner<br><br>"
        "<b>milan_datapath.sv</b><br>primary product boundary<br><br>"
        "<b>Root integration tests</b><br>"
        "Donor gates remain<br>independently required.",
        "#F3E5F5",
        "#6A1B9A",
        18,
    )

    for path, (x, y) in positions.items():
        module = by_path[path]
        role = module.role
        wrapper = PurePosixPath(role.wrapper)
        label = (
            f"<b>{esc(role.status)}</b><br><br><b>{esc(path)}</b><br>"
            f"{esc(role.purpose)}<br><br>pin {module.pin[:12]}<br>"
            f"{esc(role.path_label)}:<br>{esc(wrapper.parent)}/<br>"
            f"{esc(wrapper.name)}<br>"
            f"test: {esc(role.root_gate)}"
        )
        vertex(module_ids[path], x, y, 420, 270, label, role.fill, role.stroke, 16)

    edges = [
        ("protocol-processor", "wrapper", False),
        ("gptp-processor", "wrapper", False),
        ("third_party/verilog-axis", "RTL", False),
        ("external", "legacy", True),
    ]
    for index, (path, label, dashed) in enumerate(edges, start=1):
        style = (
            "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;"
            "jettySize=auto;html=1;endArrow=block;endFill=1;strokeWidth=2;"
            "fontSize=16;fontFamily=Helvetica;labelBackgroundColor=#FFFFFF;"
            + ("dashed=1;" if dashed else "")
        )
        cells.append(
            f'<mxCell id="edge{index}" value="{esc(label)}" style="{style}" '
            f'edge="1" parent="1" source="{module_ids[path]}" target="root">'
            '<mxGeometry relative="1" as="geometry"/></mxCell>'
        )

    vertex(
        "evidence",
        190,
        785,
        1120,
        70,
        "<b>Evidence rule</b><br>"
        "Run donor suites before root integration suites.",
        "#FFFFFF",
        "#78909C",
        16,
    )

    body = "".join(cells)
    return (
        '<mxfile host="app.diagrams.net"><diagram name="submodules">'
        f'<mxGraphModel dx="1500" dy="900" grid="1" gridSize="10" '
        f'guides="1" page="1" pageScale="1" pageWidth="{WIDTH}" '
        f'pageHeight="{HEIGHT}" math="0" shadow="0"><root>{body}</root>'
        '</mxGraphModel></diagram></mxfile>\n'
    )


def check_or_write(path: Path, content: str, checking: bool) -> bool:
    if checking:
        return path.is_file() and path.read_text(encoding="utf-8") == content
    path.write_text(content, encoding="utf-8")
    return True


def check_or_write_png(
    svg_content: str,
    drawio_content: str,
    checking: bool,
) -> bool:
    output = BASE.with_suffix(".png")
    digest = hashlib.sha256(drawio_content.encode("utf-8")).hexdigest()
    fields = {DRAWIO_HASH_KEY: digest}
    if not checking:
        render_svg_png(svg_content, output, RASTER_WIDTH, fields)
        update_pixel_manifest(
            MANIFEST,
            ARTIFACT_NAME,
            SOURCE_NAME,
            output,
            BASE.with_suffix(".drawio"),
        )
        return True
    with tempfile.TemporaryDirectory(prefix="submodule-png-") as directory:
        candidate = Path(directory) / "submodule_boundaries.png"
        candidate_info = render_svg_png(
            svg_content,
            candidate,
            RASTER_WIDTH,
            fields,
        )
    return reviewed_png_current(
        MANIFEST,
        ARTIFACT_NAME,
        SOURCE_NAME,
        output,
        BASE.with_suffix(".drawio"),
        (candidate_info.width, candidate_info.height),
        fields,
    )


def selftest() -> int:
    """Prove the generator check rejects a valid wrong raster."""
    modules = read_submodules()
    svg_content = svg(modules)
    drawio_content = drawio(modules)
    digest = hashlib.sha256(drawio_content.encode("utf-8")).hexdigest()
    fields = {DRAWIO_HASH_KEY: digest}
    with tempfile.TemporaryDirectory(prefix="submodule-map-selftest-") as directory:
        fixture = Path(directory)
        manifest = fixture / "PNG_MANIFEST.json"
        source = fixture / "submodule_boundaries.drawio"
        output = fixture / "submodule_boundaries.png"
        candidate = fixture / "candidate.png"
        shutil.copy2(MANIFEST, manifest)
        shutil.copy2(BASE.with_suffix(".drawio"), source)
        shutil.copy2(BASE.with_suffix(".png"), output)
        candidate_info = render_svg_png(
            svg_content,
            candidate,
            RASTER_WIDTH,
            fields,
        )
        arguments = (
            manifest,
            ARTIFACT_NAME,
            SOURCE_NAME,
            output,
            source,
            (candidate_info.width, candidate_info.height),
            fields,
        )
        if not reviewed_png_current(*arguments):
            print("submodule diagram selftest: copied baseline failed")
            return 1
        output.write_bytes(zero_raster_bytes(output))
        if reviewed_png_current(*arguments):
            print("submodule diagram selftest: valid wrong raster escaped")
            return 1
    print("submodule diagram selftest: OK (valid wrong-raster control)")
    return 0


def main() -> int:
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    checking = sys.argv[1:] == ["--check"]
    if sys.argv[1:] not in ([], ["--check"]):
        print("usage: submodule_boundaries.gen.py [--check|--selftest]")
        return 2

    modules = read_submodules()
    svg_content = svg(modules)
    drawio_content = drawio(modules)
    outputs = {
        BASE.with_suffix(".svg"): svg_content,
        BASE.with_suffix(".drawio"): drawio_content,
    }
    stale = [
        str(path.relative_to(ROOT))
        for path, content in outputs.items()
        if not check_or_write(path, content, checking)
    ]
    if not check_or_write_png(svg_content, drawio_content, checking):
        stale.append(str(BASE.with_suffix(".png").relative_to(ROOT)))
    if stale:
        print("submodule diagram stale: " + ", ".join(stale))
        return 1
    if checking:
        print(
            f"submodule diagram: OK ({len(modules)} exact gitlinks, decoded PNG)"
        )
    else:
        written = [str(path.relative_to(ROOT)) for path in outputs]
        written.append(str(BASE.with_suffix(".png").relative_to(ROOT)))
        print("wrote " + " and ".join(written))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
