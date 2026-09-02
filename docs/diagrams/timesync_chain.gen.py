#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the source-checked fabric time-ownership diagram."""

from __future__ import annotations

import hashlib
import html
import json
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, replace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from png_artifact import (  # noqa: E402
    render_svg_png,
    reviewed_png_current,
    update_pixel_manifest,
    zero_raster_bytes,
)


BASE = ROOT / "docs" / "diagrams" / "timesync_chain"
MANIFEST = ROOT / "docs" / "diagrams" / "PNG_MANIFEST.json"
ARTIFACT_NAME = "docs/diagrams/timesync_chain.png"
SOURCE_NAME = "docs/diagrams/timesync_chain.drawio"
DRAWIO_HASH_KEY = "Milan-Drawio-SHA256"
WIDTH = 1600
HEIGHT = 900
RASTER_WIDTH = 2400

FEATURE_FILE = ROOT / "docs" / "reference" / "milan_feature_status.json"
FEATURE_IDS = (
    "gptp.fabric-product-owner",
    "crf.media-clock-consumption",
)
SOURCE_TOKENS = {
    "hdl/milan/milan_datapath.sv": (
        "parameter bit GPTP_PLANE_EN_P = 1'b1",
        "always_ff @(posedge axis_clk) begin : media_clk_resolve",
        "pp_aecp_clk_src_index_w == AEM_CRF_CLKSRC_C",
        "KL_media_grid_align #(",
        "KL_gptp_shadow #(",
        "KL_gptp_txstamp #(",
        "timestamp_counter #(",
    ),
    "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv": (
        "module KL_gptp_shadow #(",
        "assign beat_w = rx_tvalid_i & rx_tready_i",
        "input  wire [3:0]  txts_type_i",
        "output logic        pub_commit_o",
        "output wire         pub_disc_o",
    ),
    "hdl/ieee8021as/gptp_plane/KL_gptp_txstamp.sv": (
        "module KL_gptp_txstamp #(",
        "assign beat_w = tx_tvalid_i & tx_tready_i",
        "output logic [15:0] ts_seq_o",
        "output logic [3:0]  ts_type_o",
    ),
    "hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv": (
        "assign ts_uncertain_o = (~sync_ok_w) | hold_w | disc_p_w",
        "assign as_capable_o = as_cap_w",
    ),
    "sw/builder/endstation_builder.py": (
        '"board.features.fabric_gptp: false is retired (#259): the "',
        'argv += ["--fabric-gptp"]',
    ),
}


@dataclass(frozen=True)
class Facts:
    pin: str
    gptp_status: str
    media_status: str


@dataclass(frozen=True)
class Node:
    x: int
    y: int
    width: int
    height: int
    title: str
    lines: tuple[str, ...]
    fill: str
    stroke: str
    dashed: bool = False


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    label: str
    dashed: bool = False
    route: tuple[tuple[int, int], ...] = ()
    label_at: tuple[int, int] | None = None


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def feature_statuses(path: Path = FEATURE_FILE) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    features = data.get("features") if isinstance(data, dict) else None
    if not isinstance(features, list):
        raise ValueError("feature ledger lacks a features list")
    statuses = {
        item.get("id"): item.get("status")
        for item in features
        if isinstance(item, dict)
    }
    missing = [feature for feature in FEATURE_IDS if feature not in statuses]
    if missing:
        raise ValueError("feature ledger lacks: " + ", ".join(missing))
    return {feature: str(statuses[feature]) for feature in FEATURE_IDS}


def source_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for relative, tokens in SOURCE_TOKENS.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"{relative}: source evidence is missing")
            continue
        text = path.read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                errors.append(f"{relative}: missing evidence token: {token}")
    return errors


def gitlink_pin() -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--stage", "--", "gptp-processor"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.split()
    if len(result) < 4 or result[0] != "160000" or result[2] != "0":
        raise ValueError("gptp-processor is not one stage-zero gitlink")
    return result[1]


def read_facts() -> Facts:
    errors = source_errors()
    if errors:
        raise ValueError("; ".join(errors))
    statuses = feature_statuses()
    if statuses[FEATURE_IDS[0]] != "implemented":
        raise ValueError("fabric-owner feature is not implemented")
    if statuses[FEATURE_IDS[1]] != "implemented":
        raise ValueError("media-consumption feature is not implemented")
    return Facts(
        gitlink_pin(),
        statuses[FEATURE_IDS[0]],
        statuses[FEATURE_IDS[1]],
    )


def nodes(facts: Facts) -> dict[str, Node]:
    blue = ("#E3F2FD", "#1565C0")
    gold = ("#FFF8E1", "#F9A825")
    green = ("#E8F5E9", "#2E7D32")
    purple = ("#F3E5F5", "#6A1B9A")
    orange = ("#FFF3E0", "#EF6C00")
    grey = ("#ECEFF1", "#546E7A")
    return {
        "peer": Node(35, 140, 175, 100, "802.1AS peer", ("Ethernet wire",), *grey),
        "rx": Node(250, 125, 245, 130, "Parent RX seam", ("accepted MAC beats", "first-beat PHC time"), *blue),
        "engine": Node(
            545,
            115,
            300,
            150,
            "Fabric gPTP engine",
            (f"pin {facts.pin[:12]}", "protocol, timers, servo"),
            *blue,
        ),
        "tx": Node(895, 125, 245, 130, "Parent TX seam", ("byte-to-wide transport", "valid-ready backpressure"), *blue),
        "mac": Node(1190, 140, 175, 100, "MAC boundary", ("actual TX acceptance",), *grey),
        "phc": Node(150, 350, 300, 135, "PHC counter", ("network nanoseconds", "rate and phase controls"), *gold),
        "publish": Node(535, 350, 310, 135, "Atomic publication", ("GM, parent, path", "delay, flags, commit"), *purple),
        "consumers": Node(900, 350, 310, 135, "Public consumers", ("CSR and protocol", "AVTP tu and status"), *purple),
        "stamp": Node(1260, 350, 285, 135, "MAC-boundary timestamp", ("first accepted TX beat", "sequence plus type"), *gold),
        "avtp": Node(115, 650, 330, 135, "AVTP timeline", ("PHC dates AAF and CRF", "tu reports uncertainty"), *orange),
        "crf": Node(565, 650, 330, 135, "CRF measurement", ("remote phase and rate", "selection reaches root"), *green),
        "media": Node(1070, 635, 380, 165, "Media clock lineage", ("INTERNAL: free-run", "CRF: steered and aligned"), *green),
        "select": Node(
            920,
            525,
            245,
            100,
            "CRF steering gates",
            (f"status: {facts.media_status}", "rate and grid loops"),
            *green,
        ),
    }


EDGES = (
    Edge("peer", "rx", "RX", route=((210, 190), (250, 190)), label_at=(230, 180)),
    Edge("rx", "engine", "", route=((495, 190), (545, 190))),
    Edge("engine", "tx", "bytes", route=((845, 190), (895, 190)), label_at=(870, 180)),
    Edge("tx", "mac", "TX", route=((1140, 190), (1190, 190)), label_at=(1165, 180)),
    Edge("phc", "rx", "PHC time", True, ((300, 350), (300, 255)), (340, 305)),
    Edge("engine", "phc", "rate / phase", True, ((620, 265), (620, 310), (450, 310), (450, 418)), (535, 300)),
    Edge("engine", "publish", "commit", False, ((695, 265), (695, 350)), (730, 315)),
    Edge("publish", "consumers", "state", False, ((845, 418), (900, 418)), (872, 408)),
    Edge("mac", "stamp", "accepted TX", False, ((1277, 240), (1277, 350)), (1320, 305)),
    Edge("stamp", "engine", "return tuple", False, ((1402, 350), (1402, 290), (800, 290), (800, 265)), (1100, 280)),
    Edge("phc", "avtp", "presentation time", True, ((300, 485), (300, 650)), (360, 575)),
    Edge("phc", "crf", "common time", True, ((450, 450), (500, 450), (500, 610), (730, 610), (730, 650)), (620, 600)),
    Edge("media", "crf", "internal events", False, ((1070, 718), (895, 718)), (982, 708)),
    Edge("crf", "select", "rate error", True, ((895, 680), (940, 680), (940, 625)), (985, 642)),
    Edge("select", "media", "steer / align", True, ((1165, 575), (1260, 575), (1260, 635)), (1212, 565)),
)


def svg(facts: Facts) -> str:
    diagram_nodes = nodes(facts)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" font-family="Helvetica,Arial,sans-serif">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#FAFAFA"/>',
        '<defs><marker id="arrow" markerWidth="12" markerHeight="12" '
        'refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" '
        'fill="#455A64"/></marker></defs>',
        '<text x="35" y="48" font-size="28" font-weight="bold" fill="#263238">'
        'Fabric time ownership and integration</text>',
        '<text x="35" y="78" font-size="17" fill="#546E7A">'
        f'Product owner: {esc(facts.gptp_status)}. Media consumption: '
        f'{esc(facts.media_status)}.</text>',
        '<text x="35" y="112" font-size="15" font-weight="bold" fill="#1565C0">'
        'NETWORK TIME</text>',
        '<text x="35" y="325" font-size="15" font-weight="bold" fill="#B26A00">'
        'TIMESTAMP AND PUBLICATION BOUNDARIES</text>',
        '<text x="35" y="620" font-size="15" font-weight="bold" fill="#2E7D32">'
        'PRESENTATION AND MEDIA BOUNDARY</text>',
    ]
    for edge in EDGES:
        dash = ' stroke-dasharray="7,6"' if edge.dashed else ""
        route = " L".join(f"{x},{y}" for x, y in edge.route)
        lines.append(
            f'<path d="M{route}" '
            f'fill="none" stroke="#455A64" stroke-width="2" '
            f'marker-end="url(#arrow)"{dash}/>'
        )
        if edge.label and edge.label_at is not None:
            lines.append(
                f'<text x="{edge.label_at[0]}" y="{edge.label_at[1]}" '
                f'text-anchor="middle" font-size="12" fill="#37474F">'
                f'{esc(edge.label)}</text>'
            )
    for identifier, node in diagram_nodes.items():
        dash = ' stroke-dasharray="8,6"' if node.dashed else ""
        lines.extend(
            [
                f'<rect id="{identifier}" x="{node.x}" y="{node.y}" '
                f'width="{node.width}" height="{node.height}" rx="12" '
                f'fill="{node.fill}" stroke="{node.stroke}" stroke-width="2.5"{dash}/>',
                f'<text x="{node.x + node.width / 2}" y="{node.y + 34}" '
                f'text-anchor="middle" font-size="17" font-weight="bold" '
                f'fill="#212121">{esc(node.title)}</text>',
            ]
        )
        for index, detail in enumerate(node.lines):
            lines.append(
                f'<text x="{node.x + node.width / 2}" '
                f'y="{node.y + 62 + index * 23}" text-anchor="middle" '
                f'font-size="14" fill="#37474F">{esc(detail)}</text>'
            )
    lines.extend(
        [
            '<text x="35" y="865" font-size="12" fill="#78909C">'
            'Sources: milan_datapath, KL_gptp_shadow, KL_gptp_txstamp, '
            'KL_ptp_clock_validity, feature ledger, and exact Gitlink.</text>',
            '</svg>',
        ]
    )
    return "\n".join(lines) + "\n"


def drawio(facts: Facts) -> str:
    diagram_nodes = nodes(facts)
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    annotations = (
        (
            "title",
            "Fabric time ownership and integration",
            35,
            25,
            900,
            45,
            "fontSize=24;fontStyle=1;fontColor=#263238;",
        ),
        (
            "status",
            f"Product owner: {facts.gptp_status}. "
            f"Media consumption: {facts.media_status}.",
            35,
            65,
            900,
            28,
            "fontSize=15;fontColor=#546E7A;",
        ),
        (
            "network-boundary",
            "NETWORK TIME",
            35,
            95,
            260,
            28,
            "fontSize=13;fontStyle=1;fontColor=#1565C0;",
        ),
        (
            "timestamp-boundary",
            "TIMESTAMP AND PUBLICATION BOUNDARIES",
            35,
            310,
            420,
            28,
            "fontSize=13;fontStyle=1;fontColor=#B26A00;",
        ),
        (
            "media-boundary",
            "PRESENTATION AND MEDIA BOUNDARY",
            35,
            610,
            390,
            28,
            "fontSize=13;fontStyle=1;fontColor=#2E7D32;",
        ),
        (
            "sources",
            "Sources: milan_datapath, KL_gptp_shadow, KL_gptp_txstamp, "
            "KL_ptp_clock_validity, feature ledger, and exact Gitlink.",
            35,
            840,
            1250,
            25,
            "fontSize=11;fontColor=#78909C;",
        ),
    )
    for identifier, value, x, y, width, height, text_style in annotations:
        style = "text;html=1;align=left;verticalAlign=middle;" + text_style
        cells.append(
            f'<mxCell id="{identifier}" value="{esc(value)}" style="{style}" '
            f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" '
            f'width="{width}" height="{height}" as="geometry"/></mxCell>'
        )
    for identifier, node in diagram_nodes.items():
        details = "<br>".join(node.lines)
        label = f"<b>{node.title}</b><br><br>{details}"
        style = (
            "rounded=1;whiteSpace=wrap;html=1;verticalAlign=middle;"
            "align=center;fontSize=15;strokeWidth=2;"
            f"fillColor={node.fill};strokeColor={node.stroke};"
            + ("dashed=1;" if node.dashed else "")
        )
        cells.append(
            f'<mxCell id="n-{identifier}" value="{esc(label)}" style="{style}" '
            f'vertex="1" parent="1"><mxGeometry x="{node.x}" y="{node.y}" '
            f'width="{node.width}" height="{node.height}" as="geometry"/>'
            '</mxCell>'
        )
    for index, edge in enumerate(EDGES):
        style = (
            "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;"
            "endFill=1;strokeWidth=2;fontSize=12;labelBackgroundColor=#FFFFFF;"
            + ("dashed=1;" if edge.dashed else "")
        )
        geometry = '<mxGeometry relative="1" as="geometry">'
        if len(edge.route) > 2:
            geometry += '<Array as="points">' + "".join(
                f'<mxPoint x="{x}" y="{y}"/>'
                for x, y in edge.route[1:-1]
            ) + '</Array>'
        geometry += '</mxGeometry>'
        cells.append(
            f'<mxCell id="e-{index}" value="{esc(edge.label)}" style="{style}" '
            f'edge="1" parent="1" source="n-{edge.source}" target="n-{edge.target}">'
            f'{geometry}</mxCell>'
        )
    body = "".join(cells)
    return (
        '<mxfile host="app.diagrams.net"><diagram name="fabric-time">'
        f'<mxGraphModel dx="1600" dy="900" grid="1" gridSize="10" '
        f'guides="1" page="1" pageScale="1" pageWidth="{WIDTH}" '
        f'pageHeight="{HEIGHT}" math="0" shadow="0"><root>{body}</root>'
        '</mxGraphModel></diagram></mxfile>\n'
    )


def check_or_write(path: Path, content: str, checking: bool) -> bool:
    if checking:
        return path.is_file() and path.read_text(encoding="utf-8") == content
    path.write_text(content, encoding="utf-8")
    return True


def check_or_write_png(svg_content: str, drawio_content: str, checking: bool) -> bool:
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
    with tempfile.TemporaryDirectory(prefix="timesync-png-") as directory:
        candidate = Path(directory) / "timesync_chain.png"
        candidate_info = render_svg_png(svg_content, candidate, RASTER_WIDTH, fields)
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
    facts = read_facts()
    source_svg = svg(facts)
    changed_svg = svg(replace(facts, media_status="missing"))
    if source_svg == changed_svg or "status: implemented" not in source_svg:
        print("time-sync selftest: feature status did not affect output")
        return 1
    source_drawio = drawio(facts)
    try:
        ET.fromstring(source_drawio)
    except ET.ParseError as error:
        print(f"time-sync selftest: generated Draw.io is invalid: {error}")
        return 1
    for annotation in (
        "Product owner: implemented. Media consumption: implemented.",
        "TIMESTAMP AND PUBLICATION BOUNDARIES",
        "PRESENTATION AND MEDIA BOUNDARY",
        "KL_gptp_txstamp",
    ):
        if annotation not in source_drawio:
            print(f"time-sync selftest: Draw.io lacks annotation: {annotation}")
            return 1
    with tempfile.TemporaryDirectory(prefix="timesync-source-") as directory:
        fixture = Path(directory)
        for relative in SOURCE_TOKENS:
            target = fixture / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text((ROOT / relative).read_text(encoding="utf-8"), encoding="utf-8")
        if source_errors(fixture):
            print("time-sync selftest: copied source evidence failed")
            return 1
        relative = next(iter(SOURCE_TOKENS))
        victim = fixture / relative
        token = SOURCE_TOKENS[relative][0]
        victim.write_text(victim.read_text(encoding="utf-8").replace(token, "missing", 1), encoding="utf-8")
        if not source_errors(fixture):
            print("time-sync selftest: missing source token escaped")
            return 1
    digest = hashlib.sha256(drawio(facts).encode("utf-8")).hexdigest()
    fields = {DRAWIO_HASH_KEY: digest}
    with tempfile.TemporaryDirectory(prefix="timesync-raster-") as directory:
        fixture = Path(directory)
        manifest = fixture / "PNG_MANIFEST.json"
        source = fixture / "timesync_chain.drawio"
        output = fixture / "timesync_chain.png"
        candidate = fixture / "candidate.png"
        shutil.copy2(MANIFEST, manifest)
        shutil.copy2(BASE.with_suffix(".drawio"), source)
        shutil.copy2(BASE.with_suffix(".png"), output)
        candidate_info = render_svg_png(source_svg, candidate, RASTER_WIDTH, fields)
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
            print("time-sync selftest: copied raster failed")
            return 1
        output.write_bytes(zero_raster_bytes(output))
        if reviewed_png_current(*arguments):
            print("time-sync selftest: wrong raster escaped")
            return 1
    print("time-sync diagram selftest: OK (source, status, XML, raster)")
    return 0


def main() -> int:
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    checking = sys.argv[1:] == ["--check"]
    if sys.argv[1:] not in ([], ["--check"]):
        print("usage: timesync_chain.gen.py [--check|--selftest]")
        return 2
    try:
        facts = read_facts()
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"time-sync diagram: FAIL: {error}")
        return 1
    svg_content = svg(facts)
    drawio_content = drawio(facts)
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
        print("time-sync diagram stale: " + ", ".join(stale))
        return 1
    if checking:
        print("time-sync diagram: OK (RTL, features, Gitlink, decoded PNG)")
    else:
        print("wrote timesync_chain.drawio, timesync_chain.svg, and timesync_chain.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
