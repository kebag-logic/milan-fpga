#!/usr/bin/env python3
"""Generate the four-audience documentation map."""

from __future__ import annotations

import html
import hashlib
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from png_artifact import inspect_png, render_svg_png  # noqa: E402


BASE = ROOT / "docs" / "DOC_MAP"
WIDTH = 1840
HEIGHT = 1050
RASTER_WIDTH = 2400
DRAWIO_HASH_KEY = "Milan-Drawio-SHA256"


@dataclass(frozen=True)
class Step:
    path: str
    result: str


@dataclass(frozen=True)
class Persona:
    name: str
    question: str
    fill: str
    stroke: str
    steps: tuple[Step, ...]


PERSONAS = (
    Persona(
        "Implementation developer",
        "How do I change product code?",
        "#E3F2FD",
        "#1565C0",
        (
            Step("docs/guides/IMPLEMENTATION_DEVELOPER.md", "Own the product change"),
            Step("docs/overview/ARCHITECTURE.md", "Find the correct subsystem"),
            Step("docs/reference/SUBMODULES.md", "Respect imported ownership"),
            Step("docs/fpga/FPGA_DESIGN.md", "Locate RTL and harnesses"),
            Step("CONTRIBUTING.md", "Follow implementation gates"),
            Step("tb/verilator/README.md", "Run focused RTL evidence"),
        ),
    ),
    Persona(
        "Verification developer",
        "How do I prove behavior?",
        "#F3E5F5",
        "#6A1B9A",
        (
            Step("docs/guides/VERIFICATION_DEVELOPER.md", "Own independent evidence"),
            Step("docs/testing/TESTING.md", "Choose the correct layer"),
            Step("tb/verilator/README.md", "Use C++ cycle checks"),
            Step("tests/README.md", "Use Python behavior checks"),
            Step("docs/litex/LITEX_SOC.md", "Use Python integration checks"),
            Step("docs/testing/CI_WORKFLOWS.md", "Record exact-head evidence"),
        ),
    ),
    Persona(
        "System integrator",
        "How do I connect everything?",
        "#FFF3E0",
        "#EF6C00",
        (
            Step("docs/guides/SYSTEM_INTEGRATOR.md", "Own boundary correctness"),
            Step("docs/integration/INTEGRATION_GUIDE.md", "Wire datapath interfaces"),
            Step("docs/reference/REGISTER_MAP.md", "Implement the software ABI"),
            Step("docs/litex/LITEX_SOC.md", "Review the reference integration"),
            Step("docs/integration/BUILDING.md", "Build matched artifacts"),
            Step("docs/limitations/TROUBLESHOOTING.md", "Recover failed deployments"),
        ),
    ),
    Persona(
        "Project manager",
        "How do I judge readiness?",
        "#E8F5E9",
        "#2E7D32",
        (
            Step("docs/guides/PROJECT_MANAGER.md", "Use evidence-based decisions"),
            Step("docs/DOCUMENTATION_AUDIT.md", "Review documentation health"),
            Step("docs/testing/MILAN_V12_AUDIT_2026-08-16.md", "Review dated compliance evidence"),
            Step("docs/reference/MILAN_FEATURE_STATUS.md", "Check canonical feature status"),
            Step("REQUIREMENTS.md", "Check normative obligations"),
            Step("docs/MILAN_V12_ROADMAP.md", "Review remaining delivery work"),
        ),
    ),
)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def validate() -> None:
    missing = sorted(
        step.path
        for persona in PERSONAS
        for step in persona.steps
        if not (ROOT / step.path).is_file()
    )
    if missing:
        raise SystemExit("missing documentation paths: " + ", ".join(missing))
    if len({persona.name for persona in PERSONAS}) != 4:
        raise SystemExit("expected four distinct audiences")
    if any(len(persona.steps) != 6 for persona in PERSONAS):
        raise SystemExit("every audience needs six ordered steps")


def positions() -> dict[str, tuple[int, int]]:
    return {
        persona.name: (40 + index * 450, 250)
        for index, persona in enumerate(PERSONAS)
    }


def svg() -> str:
    output = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
        f'height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" '
        'font-family="Helvetica,Arial,sans-serif">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#FAFAFA"/>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" '
        'refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" '
        'fill="#607D8B"/></marker></defs>',
        '<text x="40" y="55" font-size="32" font-weight="bold" '
        'fill="#263238">Choose your documentation path</text>',
        '<text x="40" y="88" font-size="18" fill="#546E7A">'
        'Select your current responsibility.</text>',
        '<rect x="40" y="125" width="1760" height="82" rx="14" '
        'fill="#FFF8E1" stroke="#F9A825" stroke-width="2.5"/>',
        '<text x="920" y="158" text-anchor="middle" font-size="20" '
        'font-weight="bold" fill="#5D4037">Start with docs/guides/README.md</text>',
        '<text x="920" y="185" text-anchor="middle" font-size="17" '
        'fill="#5D4037">Then follow one lane downward.</text>',
    ]
    for persona in PERSONAS:
        x, y = positions()[persona.name]
        output.extend(
            [
                f'<rect x="{x}" y="{y}" width="410" height="100" rx="12" '
                f'fill="{persona.stroke}" stroke="{persona.stroke}"/>',
                f'<text x="{x + 20}" y="{y + 38}" font-size="21" '
                f'font-weight="bold" fill="#FFFFFF">{esc(persona.name)}</text>',
                f'<text x="{x + 20}" y="{y + 70}" font-size="16" '
                f'fill="#FFFFFF">{esc(persona.question)}</text>',
            ]
        )
        previous_bottom = y + 100
        for number, step in enumerate(persona.steps, start=1):
            box_y = y + 130 + (number - 1) * 102
            output.extend(
                [
                    f'<path d="M{x + 205},{previous_bottom} L{x + 205},{box_y - 6}" '
                    'stroke="#607D8B" stroke-width="2" '
                    'marker-end="url(#arrow)"/>',
                    f'<rect x="{x}" y="{box_y}" width="410" height="76" rx="10" '
                    f'fill="{persona.fill}" stroke="{persona.stroke}" '
                    'stroke-width="2"/>',
                    f'<circle cx="{x + 28}" cy="{box_y + 38}" r="17" '
                    f'fill="{persona.stroke}"/>',
                    f'<text x="{x + 28}" y="{box_y + 44}" text-anchor="middle" '
                    f'font-size="16" font-weight="bold" fill="#FFFFFF">{number}</text>',
                    f'<text x="{x + 56}" y="{box_y + 30}" font-size="14" '
                    f'font-weight="bold" fill="#212121">{esc(step.path)}</text>',
                    f'<text x="{x + 56}" y="{box_y + 55}" font-size="14" '
                    f'fill="#455A64">{esc(step.result)}</text>',
                ]
            )
            previous_bottom = box_y + 76
    output.extend(
        [
            '<rect x="240" y="1000" width="1360" height="38" rx="10" '
            'fill="#ECEFF1" stroke="#546E7A"/>',
            '<text x="920" y="1025" text-anchor="middle" font-size="16" '
            'fill="#37474F">Requirements outrank summaries. Executable evidence proves behavior.</text>',
            '</svg>',
        ]
    )
    return "\n".join(output) + "\n"


def drawio() -> str:
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
        size: int,
        align: str = "left",
    ) -> None:
        style = (
            "rounded=1;whiteSpace=wrap;html=1;verticalAlign=middle;"
            f"align={align};spacingLeft=12;fontSize={size};fontFamily=Helvetica;"
            f"fillColor={fill};strokeColor={stroke};strokeWidth=2;"
        )
        cells.append(
            f'<mxCell id="{ident}" value="{esc(label)}" style="{style}" '
            f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" '
            f'width="{width}" height="{height}" as="geometry"/></mxCell>'
        )

    vertex(
        "title",
        40,
        25,
        1000,
        75,
        "<b>Choose your documentation path</b><br>Select your current responsibility.",
        "none",
        "none",
        24,
    )
    vertex(
        "start",
        40,
        125,
        1760,
        82,
        "<b>Start with docs/guides/README.md</b><br>Then follow one lane downward.",
        "#FFF8E1",
        "#F9A825",
        18,
        "center",
    )
    for persona_index, persona in enumerate(PERSONAS):
        x, y = positions()[persona.name]
        role_id = f"role-{persona_index}"
        vertex(
            role_id,
            x,
            y,
            410,
            100,
            f"<b>{persona.name}</b><br>{persona.question}",
            persona.stroke,
            persona.stroke,
            18,
        )
        previous_id = role_id
        for step_index, step in enumerate(persona.steps, start=1):
            box_y = y + 130 + (step_index - 1) * 102
            step_id = f"step-{persona_index}-{step_index}"
            vertex(
                step_id,
                x,
                box_y,
                410,
                76,
                f"<b>{step_index}. {step.path}</b><br>{step.result}",
                persona.fill,
                persona.stroke,
                14,
            )
            cells.append(
                f'<mxCell id="edge-{persona_index}-{step_index}" value="" '
                'style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;'
                'endArrow=block;endFill=1;strokeWidth=2;" edge="1" parent="1" '
                f'source="{previous_id}" target="{step_id}">'
                '<mxGeometry relative="1" as="geometry"/></mxCell>'
            )
            previous_id = step_id
    vertex(
        "authority",
        240,
        1000,
        1360,
        38,
        "Requirements outrank summaries. Executable evidence proves behavior.",
        "#ECEFF1",
        "#546E7A",
        16,
        "center",
    )
    return (
        '<mxfile host="app.diagrams.net"><diagram name="audiences">'
        f'<mxGraphModel dx="1840" dy="1050" grid="1" gridSize="10" '
        f'guides="1" page="1" pageScale="1" pageWidth="{WIDTH}" '
        f'pageHeight="{HEIGHT}" math="0" shadow="0"><root>'
        + "".join(cells)
        + '</root></mxGraphModel></diagram></mxfile>\n'
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
        return True
    with tempfile.TemporaryDirectory(prefix="doc-map-png-") as directory:
        candidate = Path(directory) / "DOC_MAP.png"
        candidate_info = render_svg_png(
            svg_content,
            candidate,
            RASTER_WIDTH,
            fields,
        )
        try:
            committed_info = inspect_png(output)
        except (OSError, ValueError):
            return False
    return (
        (committed_info.width, committed_info.height)
        == (candidate_info.width, candidate_info.height)
        and committed_info.text.get(DRAWIO_HASH_KEY) == digest
    )


def main() -> int:
    checking = sys.argv[1:] == ["--check"]
    if sys.argv[1:] not in ([], ["--check"]):
        print("usage: DOC_MAP.gen.py [--check]")
        return 2
    validate()
    svg_content = svg()
    drawio_content = drawio()
    outputs = (
        (BASE.with_suffix(".svg"), svg_content),
        (BASE.with_suffix(".drawio"), drawio_content),
    )
    stale = [path for path, content in outputs if not check_or_write(path, content, checking)]
    if not check_or_write_png(svg_content, drawio_content, checking):
        stale.append(BASE.with_suffix(".png"))
    if stale:
        for path in stale:
            print(f"stale documentation map: {path.relative_to(ROOT)}")
        return 1
    if checking:
        print("documentation map: OK (4 roles, 24 valid paths, decoded PNG)")
    else:
        print("wrote docs/DOC_MAP.svg, docs/DOC_MAP.drawio, and docs/DOC_MAP.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
