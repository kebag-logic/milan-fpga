#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate one validated, self-contained first-party HDL reference."""

# TWO HALVES LIVE ELSEWHERE, and this file stays the only entry point for
# both. `gen_hdl_reference_comments` is the lexical `//!` reader: pure text,
# no parser, no filesystem, so it can be read and exercised on a machine where
# the pinned wheel is not installed, and it is imported below.
# `gen_hdl_reference_selftest` holds the `--selftest` arms and is imported only
# when that flag is passed, which is also why this docstring is one line: it is
# argparse's description, and `--help` says what the tool does, not how it is
# laid out.

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_hdl_reference_comments import (  # noqa: E402
    declaration_docs,
    description_paragraphs,
    doc_comments,
    item_description,
    strip_comments,
)


#: `(path, kind, name)`: the identity `Declaration.key` returns, and the shape
#: the exception inventory and every coverage comparison are keyed by.
DeclarationKey = tuple[str, str, str]
#: Parser objects - `pyslang` syntax nodes, tokens, trees and source managers -
#: are annotated `Any` on purpose. The wheel is an optional dependency imported
#: inside `load_parser`, and Python evaluates an annotation at `def` time, so
#: naming one of its classes in a signature would make importing this module
#: fail wherever the parser is not installed - which is every caller of the
#: pure-text half, and the self-test's own missing-parser arm.
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = Path("/tmp/milan-hdl-reference")
DOCUMENT_TITLE = "Milan FPGA HDL reference"
DOCUMENT_SCHEMA = "hdl-reference-html-v1"
PARSER_NAME = "pyslang"
PARSER_VERSION = "11.0.0"
SOURCE_SUFFIXES = frozenset((".sv", ".v", ".svh"))
PARSED_SUFFIXES = frozenset((".sv", ".v"))
KNOWN_OMISSIONS = frozenset({
    ("hdl/common/axi_stream_if.sv", "interface", "axi_stream_if"),
    ("hdl/ieee1722/aaf/KL_aaf_latency_taps.sv",
     "module", "KL_aaf_latency_taps"),
})
DECLARATION_RE = re.compile(
    r"(?m)^[ \t]*(module|package|interface)[ \t]+"
    r"(?:automatic[ \t]+)?([A-Za-z_][A-Za-z0-9_$]*)\b")
SECTION_RE = re.compile(
    r'<h1 id="(?:module|package)-[^"]+">'
    r'(Module|Package):\s*([^<]+)</h1>')
SVG_TAG_RE = re.compile(r"<(/?)svg\b[^>]*?>", re.IGNORECASE | re.DOTALL)
GRAPHIC_TAGS = frozenset({
    "circle", "ellipse", "image", "line", "path", "polygon", "polyline",
    "rect", "text", "use",
})
PROCESS_KINDS = {
    "AlwaysBlock": "always",
    "AlwaysCombBlock": "always_comb",
    "AlwaysFFBlock": "always_ff",
    "AlwaysLatchBlock": "always_latch",
    "FinalBlock": "final",
    "InitialBlock": "initial",
}
SENSITIVITY_RE = re.compile(r"@\s*(?:\*|\((?:[^()]|\([^()]*\))*\))")
BLOCK_LABEL_RE = re.compile(r"\bbegin\s*:\s*([A-Za-z_$][A-Za-z0-9_$]*)")
DOCUMENT_STYLE = '''\
<style id="milan-reference-style">
body { margin: 0 auto; max-width: 1080px; padding: 24px 45px;
  font-family: system-ui, sans-serif; line-height: 1.5; color: #17233c;
  background: #ffffff; }
h1 { border-bottom: 2px solid #275d9b; padding-bottom: 0.3em; }
h2 { border-bottom: 1px solid #c6cbd1; padding-bottom: 0.2em; }
table { border-collapse: collapse; width: 100%; margin-bottom: 16px; }
th, td { border: 1px solid #c6cbd1; padding: 6px 13px; text-align: left; }
th { background: #eef5ff; }
tr:nth-child(2n) td { background: #f6f8fa; }
code { background: #eef1f5; padding: 0.15em 0.35em; border-radius: 3px; }
nav ul { columns: 3; list-style: none; padding-left: 0; }
nav a { text-decoration: none; color: #275d9b; }
</style>
'''
PRINT_STYLE = '''\
<style id="milan-render-safety">
svg { max-width: 100%; height: auto; }
@media print {
  h1[id^="module-"], h1[id^="package-"] { break-before: page; }
  h1, h2, h3 { break-after: avoid-page; }
  svg, table { break-inside: avoid; }
}
</style>
'''
REVISION_NOTICE = '''\
<section aria-label="Reference scope">
<p>Generated from first-party HDL sources.</p>
<ul>
<li>Modules include ports and diagrams.</li>
<li>Packages include source-derived details.</li>
<li>Interfaces lack standalone sections.</li>
<li>Additional file declarations require source review.</li>
<li>Tables cover top-level declarations only.</li>
</ul>
</section>
'''
SHA_RE = re.compile(r"[0-9a-f]{40}")
TIMESTAMP_RE = re.compile(
    r"\b(?:Generated|Rendered) (?:on|at)\b|Project revision")
LOCAL_PATH_RE = re.compile(
    r"(?:file://)?/(?:home|tmp|workspace|__w)(?:/|\\)", re.IGNORECASE)
ACTIVE_HTML_RE = re.compile(
    r"<\s*(?:script|iframe|object|embed|form)\b|"
    r"\s+on[a-z]+\s*=|javascript\s*:", re.IGNORECASE)
# Keep private identifiers absent from tracked text.
PRIVATE_DEVICE_RE = re.compile(
    r"\b" + "".join(chr(code) for code in (68, 83, 50, 48)) + r"D?\b",
    re.IGNORECASE)


class GenerationError(RuntimeError):
    """A refusal protecting reference completeness or user data."""


@dataclass(frozen=True, order=True)
class Declaration:
    """One source declaration and its repository path."""

    path: str
    kind: str
    name: str

    @property
    def key(self) -> DeclarationKey:
        """The identity two independent front ends are compared on."""
        return (self.path, self.kind, self.name)


@dataclass(frozen=True)
class Census:
    """Expected reference coverage derived from current sources."""

    files_found: int
    files_processed: int
    files_unprocessed: int
    supported: tuple
    omissions: tuple


@dataclass(frozen=True)
class Port:
    """One ANSI port with its rendered facts."""

    name: str
    direction: str
    type: str
    description: str


@dataclass(frozen=True)
class Row:
    """One generic table row of rendered source facts."""

    cells: tuple


@dataclass
class Content:
    """Rendered source facts for one supported declaration."""

    declaration: Declaration
    description: tuple = ()
    parameters: tuple = ()
    ports: tuple = ()
    signals: tuple = ()
    constants: tuple = ()
    types: tuple = ()
    processes: tuple = ()
    functions: tuple = ()
    instantiations: tuple = ()


@dataclass(frozen=True)
class Section:
    """One generated declaration section."""

    kind: str
    name: str
    body: str


def declarations_in(root: Path, path: Path) -> tuple[Declaration, ...]:
    """Return declarations found outside source comments."""
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise GenerationError(f"cannot read {path}: {exc}") from exc
    relative = path.relative_to(root).as_posix()
    return tuple(Declaration(relative, match.group(1), match.group(2))
                 for match in DECLARATION_RE.finditer(strip_comments(source)))


def source_census(root: Path,
                  known_omissions: frozenset[DeclarationKey] = KNOWN_OMISSIONS) -> Census:
    """Derive supported declarations and enforce known exceptions."""
    hdl_root = root / "hdl"
    if not hdl_root.is_dir():
        raise GenerationError(f"missing HDL source directory: {hdl_root}")
    files = tuple(sorted(path for path in hdl_root.rglob("*")
                         if path.is_file()
                         and path.suffix.lower() in SOURCE_SUFFIXES))
    parsed = tuple(path for path in files
                   if path.suffix.lower() in PARSED_SUFFIXES)
    if not files or not parsed:
        raise GenerationError("HDL source inventory is empty")

    supported = []
    omissions = []
    for path in parsed:
        declarations = declarations_in(root, path)
        if not declarations:
            raise GenerationError(
                f"supported source contains no declaration: "
                f"{path.relative_to(root).as_posix()}")
        first = declarations[0]
        if first.kind in ("module", "package"):
            supported.append(first)
        else:
            omissions.append(first)
        omissions.extend(declarations[1:])

    found = frozenset(item.key for item in omissions)
    expected = frozenset(known_omissions)
    if found != expected:
        missing = sorted(expected - found)
        unexpected = sorted(found - expected)
        details = []
        if missing:
            details.append(f"changed exceptions: {missing}")
        if unexpected:
            details.append(f"new exceptions: {unexpected}")
        raise GenerationError("reference exception inventory changed; "
                              + "; ".join(details))

    return Census(
        files_found=len(files),
        files_processed=len(parsed),
        files_unprocessed=len(files) - len(parsed),
        supported=tuple(sorted(supported)),
        omissions=tuple(sorted(omissions)),
    )


def load_parser() -> ModuleType:
    """Import the pinned parser or refuse with its install path."""
    try:
        import pyslang
    except ImportError as exc:
        raise GenerationError(
            "the pinned parser is unavailable; install "
            "tools/hdl_reference/requirements.txt") from exc
    return verify_parser(pyslang)


def verify_parser(module: ModuleType) -> ModuleType:
    """Require the parser release locked by this repository."""
    version = getattr(module, "__version__", None)
    if version != PARSER_VERSION:
        raise GenerationError(
            f"{PARSER_NAME} version must be {PARSER_VERSION}; "
            f"found {version!r}")
    return module


def include_directories(root: Path) -> tuple[str, ...]:
    """Return every directory holding HDL sources or headers."""
    hdl_root = root / "hdl"
    return tuple(sorted({str(path.parent) for path in hdl_root.rglob("*")
                         if path.is_file()
                         and path.suffix.lower() in SOURCE_SUFFIXES}))


def parse_file(parser: ModuleType, root: Path,
               incdirs: Sequence[str], path: Path) -> tuple[Any, Any]:
    """Parse one file and refuse on any reported syntax error."""
    manager = parser.SourceManager()
    for directory in incdirs:
        manager.addUserDirectories(directory)
    tree = parser.syntax.SyntaxTree.fromFile(str(path), manager)
    errors = [item for item in tree.diagnostics if item.isError()]
    if errors:
        relative = path.relative_to(root).as_posix()
        raise GenerationError(
            f"cannot parse {relative}: {len(errors)} syntax errors")
    return tree, manager


def node_text(source_bytes: bytes, node: Any) -> str:
    """Return one node's exact source text without any trivia.

    Parser offsets count bytes, so slicing happens on bytes and
    the exact slice is decoded afterwards.
    """
    span = node.sourceRange
    raw = source_bytes[span.start.offset:span.end.offset]
    return " ".join(raw.decode("utf-8", errors="replace").split())


def node_line(manager: Any, node: Any) -> int:
    """Return the line of one node's first token."""
    return manager.getLineNumber(node.getFirstToken().location)


def syntax_items(parser: ModuleType, node: Any) -> Iterator[Any]:
    """Iterate syntax children, skipping separator tokens."""
    return (item for item in node
            if isinstance(item, parser.syntax.SyntaxNode))


def declared_here(manager: Any, path: Path, node: Any) -> bool:
    """Report whether one member truly lives in the parsed file."""
    name = manager.getFileName(node.getFirstToken().location)
    return Path(name).resolve() == path.resolve()


def parameter_rows(parser: ModuleType, source_bytes: bytes,
                   comments: dict[int, tuple[bool, str]], manager: Any,
                   nodes: Iterable[Any]) -> tuple[Row, ...]:
    """Render parameter declarations into table rows."""
    rows = []
    for node in nodes:
        if node.kind.name not in ("ParameterDeclaration",
                                  "TypeParameterDeclaration"):
            continue
        kind_type = getattr(node, "type", None)
        type_text = node_text(source_bytes, kind_type) if kind_type is not None else ""
        for declarator in syntax_items(parser, node.declarators):
            name = declarator.name.valueText
            initializer = getattr(declarator, "initializer", None)
            value = ""
            if initializer is not None:
                value = node_text(source_bytes, initializer).lstrip("= ").strip()
            description = item_description(
                comments, node_line(manager, node),
                manager.getLineNumber(declarator.name.location))
            rows.append(Row((name, type_text, value, description)))
    return tuple(rows)


def dimensions_text(source_bytes: bytes, declarator: Any) -> str:
    """Render one declarator's unpacked dimensions, if any."""
    dimensions = getattr(declarator, "dimensions", None)
    if not dimensions:
        return ""
    parts = (node_text(source_bytes, item) for item in dimensions
             if hasattr(item, "sourceRange"))
    return " ".join(part for part in parts if part)


def port_type_text(source_bytes: bytes, header: Any, declarator: Any) -> str:
    """Render one ANSI port type from its header and dimensions."""
    header_text = node_text(source_bytes, header)
    trimmed = re.sub(r"^(?:input|output|inout|ref)\b", "", header_text).strip()
    suffix = dimensions_text(source_bytes, declarator)
    if suffix:
        trimmed = f"{trimmed} {suffix}".strip()
    return trimmed


def module_ports(parser: ModuleType, source_bytes: bytes,
                 comments: dict[int, tuple[bool, str]], manager: Any,
                 header: Any) -> tuple[Port, ...]:
    """Extract ANSI ports; refuse shapes the reference cannot render."""
    port_list = header.ports
    if port_list is None:
        return ()
    if port_list.kind.name != "AnsiPortList":
        raise GenerationError(
            f"module {header.name.valueText} has an unsupported "
            f"port list: {port_list.kind.name}")
    ports = []
    direction = None
    for port in syntax_items(parser, port_list.ports):
        if port.kind.name != "ImplicitAnsiPort":
            raise GenerationError(
                f"module {header.name.valueText} has an unsupported "
                f"port shape: {port.kind.name}")
        token = getattr(port.header, "direction", None)
        value = token.valueText if token is not None else ""
        if value:
            direction = value
        if direction is None:
            raise GenerationError(
                f"module {header.name.valueText} has a port "
                "without a direction")
        name = port.declarator.name.valueText
        description = item_description(
            comments, node_line(manager, port),
            manager.getLineNumber(port.declarator.name.location))
        ports.append(Port(
            name=name,
            direction=direction,
            type=port_type_text(source_bytes, port.header, port.declarator),
            description=description,
        ))
    names = [port.name for port in ports]
    if len(names) != len(set(names)):
        raise GenerationError(
            f"module {header.name.valueText} has duplicate ports")
    return tuple(ports)


def declarator_rows(parser: ModuleType, source_bytes: bytes,
                    comments: dict[int, tuple[bool, str]], manager: Any,
                    node: Any, type_text: str) -> tuple[Row, ...]:
    """Render one declaration's declarators into table rows."""
    rows = []
    for declarator in syntax_items(parser, node.declarators):
        rendered = type_text
        suffix = dimensions_text(source_bytes, declarator)
        if suffix:
            rendered = f"{type_text} {suffix}".strip()
        description = item_description(
            comments, node_line(manager, node),
            manager.getLineNumber(declarator.name.location))
        rows.append(Row((declarator.name.valueText, rendered, description)))
    return tuple(rows)


def member_content(
        parser: ModuleType, source_bytes: bytes,
        comments: dict[int, tuple[bool, str]], manager: Any, path: Path,
        members: Iterable[Any],
) -> tuple[tuple[Row, ...], tuple[Row, ...], tuple[Row, ...],
           tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """Collect table and list rows from one declaration body.

    Members pulled in by `include directives belong to another
    source buffer, so their offsets index another file; they are
    excluded rather than rendered from the wrong text.
    """
    signals = []
    constants = []
    types = []
    processes = []
    functions = []
    instantiations = []
    for member in members:
        if not declared_here(manager, path, member):
            continue
        kind = member.kind.name
        if kind == "DataDeclaration":
            type_text = node_text(source_bytes, member.type)
            signals.extend(declarator_rows(
                parser, source_bytes, comments, manager, member, type_text))
        elif kind == "NetDeclaration":
            net = getattr(member, "netType", None)
            parts = [net.valueText] if net is not None else []
            data_type = getattr(member, "type", None)
            if data_type is not None:
                parts.append(node_text(source_bytes, data_type))
            type_text = " ".join(part for part in parts if part)
            signals.extend(declarator_rows(
                parser, source_bytes, comments, manager, member, type_text))
        elif kind == "ParameterDeclarationStatement":
            constants.extend(parameter_rows(
                parser, source_bytes, comments, manager, (member.parameter,)))
        elif kind == "TypedefDeclaration":
            description = item_description(
                comments, node_line(manager, member),
                manager.getLineNumber(member.name.location))
            types.append(Row((member.name.valueText,
                              node_text(source_bytes, member.type), description)))
        elif kind in PROCESS_KINDS:
            body = node_text(source_bytes, member)
            sensitivity = SENSITIVITY_RE.search(body)
            label = BLOCK_LABEL_RE.search(body)
            entry = PROCESS_KINDS[kind]
            if label is not None:
                entry = f"{entry} : {label.group(1)}"
            if sensitivity is not None:
                entry = f"{entry} ( {sensitivity.group(0)} )"
            processes.append(entry)
        elif kind == "FunctionDeclaration":
            prototype = member.prototype
            functions.append(node_text(source_bytes, prototype))
        elif kind == "HierarchyInstantiation":
            target = member.type.valueText
            for instance in syntax_items(parser, member.instances):
                decl = getattr(instance, "decl", None)
                label = decl.name.valueText if decl is not None else "unnamed"
                instantiations.append(f"{label}: {target}")
    return (tuple(signals), tuple(constants), tuple(types),
            tuple(processes), tuple(functions), tuple(instantiations))


def extract_file(parser: ModuleType, root: Path,
                 incdirs: Sequence[str], path: Path) -> tuple[Content, ...]:
    """Extract every top-level declaration one file truly holds."""
    tree, manager = parse_file(parser, root, incdirs, path)
    source_bytes = path.read_bytes()
    source = source_bytes.decode("utf-8", errors="replace")
    comments = doc_comments(source)
    bare_lines = strip_comments(source).splitlines()
    relative = path.relative_to(root).as_posix()
    kind_words = {
        "ModuleDeclaration": "module",
        "PackageDeclaration": "package",
        "InterfaceDeclaration": "interface",
    }
    contents = []
    for member in tree.root.members:
        word = kind_words.get(member.kind.name)
        if word is None or not declared_here(manager, path, member):
            continue
        header = member.header
        declaration = Declaration(relative, word, header.name.valueText)
        content = Content(declaration=declaration)
        content.description = declaration_docs(
            comments, bare_lines, node_line(manager, member))
        if word == "module":
            if header.parameters is not None:
                content.parameters = parameter_rows(
                    parser, source_bytes, comments, manager,
                    syntax_items(parser, header.parameters.declarations))
            content.ports = module_ports(
                parser, source_bytes, comments, manager, header)
        if word in ("module", "package"):
            (content.signals, content.constants, content.types,
             content.processes, content.functions,
             content.instantiations) = member_content(
                parser, source_bytes, comments, manager, path, member.members)
        contents.append(content)
    return tuple(contents)


def extract_reference(
        parser: ModuleType, root: Path, census: Census,
) -> tuple[tuple[Content, ...], set[DeclarationKey]]:
    """Extract content and prove both front ends agree exactly."""
    hdl_root = root / "hdl"
    incdirs = include_directories(root)
    contents = []
    for path in sorted(hdl_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in PARSED_SUFFIXES:
            continue
        contents.extend(extract_file(parser, root, incdirs, path))
    parsed_keys = {item.declaration.key for item in contents}
    census_keys = {item.key for item in census.supported}
    census_keys.update(item.key for item in census.omissions)
    if parsed_keys != census_keys:
        missing = sorted(census_keys - parsed_keys)
        unexpected = sorted(parsed_keys - census_keys)
        raise GenerationError(
            f"parser and census disagree; missing={missing}; "
            f"unexpected={unexpected}")
    supported = {item.key for item in census.supported}
    by_key = {item.declaration.key: item for item in contents}
    return tuple(by_key[item.key] for item in census.supported), supported


def diagram_marker(name: str) -> str:
    """Return one section's exact diagram heading."""
    return (f'<h2 class="diagram" id="diagram-{html.escape(name)}">'
            "Diagram</h2>")


def module_svg(name: str, ports: Sequence[Port]) -> str:
    """Render an accessible structural SVG from extracted ports."""
    inputs = [port.name for port in ports if port.direction == "input"]
    outputs = [port.name for port in ports if port.direction != "input"]
    rows = max(len(inputs), len(outputs), 1)
    height = 100 + rows * 34
    box_top = 42
    box_height = height - 52
    title_id = f"diagram-title-{name}"
    parts = [
        (f'<p><svg xmlns="http://www.w3.org/2000/svg" '
         f'viewBox="0 0 960 {height}" role="img" '
         f'aria-labelledby="{html.escape(title_id)}" '
         'data-diagram-source="source-ports">'),
        f'<title id="{html.escape(title_id)}">Port diagram for '
        f'{html.escape(name)}</title>',
        '<style>text{font:18px sans-serif;fill:#17233c}'
        '.box{fill:#eef5ff;stroke:#275d9b;stroke-width:3}'
        '.wire{stroke:#275d9b;stroke-width:2}</style>',
        (f'<rect class="box" x="330" y="{box_top}" width="300" '
         f'height="{box_height}" rx="18"/>'),
        (f'<text x="480" y="76" text-anchor="middle" font-weight="700">'
         f'{html.escape(name)}</text>'),
    ]
    for index, port in enumerate(inputs):
        y = 116 + index * 34
        parts.append(f'<line class="wire" x1="300" y1="{y}" x2="330" y2="{y}"/>')
        parts.append(
            f'<text x="292" y="{y + 6}" text-anchor="end">'
            f'{html.escape(port)}</text>')
    for index, port in enumerate(outputs):
        y = 116 + index * 34
        parts.append(f'<line class="wire" x1="630" y1="{y}" x2="660" y2="{y}"/>')
        parts.append(
            f'<text x="668" y="{y + 6}">{html.escape(port)}</text>')
    parts.append("</svg></p>")
    return "".join(parts)


def emit_table(name: str, heading: str, columns: Sequence[str],
               rows: Sequence[Row]) -> str:
    """Render one facts table beneath its own heading."""
    if not rows:
        return ""
    anchor = f"{heading.lower()}-{html.escape(name)}"
    parts = [f'<h2 id="{anchor}">{heading}</h2>', "<table>", "<thead><tr>"]
    parts.extend(f"<th>{html.escape(column)}</th>" for column in columns)
    parts.append("</tr></thead>")
    parts.append("<tbody>")
    for row in rows:
        cells = "".join(f"<td>{html.escape(cell)}</td>"
                        for cell in row.cells)
        parts.append(f"<tr>{cells}</tr>")
    parts.append("</tbody></table>")
    return "\n".join(parts)


def emit_list(name: str, heading: str, entries: Sequence[str]) -> str:
    """Render one facts list beneath its own heading."""
    if not entries:
        return ""
    anchor = f"{heading.lower()}-{html.escape(name)}"
    parts = [f'<h2 id="{anchor}">{heading}</h2>', "<ul>"]
    parts.extend(f"<li><code>{html.escape(entry)}</code></li>"
                 for entry in entries)
    parts.append("</ul>")
    return "\n".join(parts)


def emit_section(content: Content) -> str:
    """Render one declaration section from extracted facts."""
    declaration = content.declaration
    name = declaration.name
    label = "Module" if declaration.kind == "module" else "Package"
    parts = [
        f'<h1 id="{label.lower()}-{html.escape(name)}">'
        f"{label}: {html.escape(name)}</h1>",
        "<ul><li><strong>File</strong>: "
        f"<code>{html.escape(declaration.path)}</code></li></ul>",
    ]
    if declaration.kind == "module":
        parts.append(diagram_marker(name))
        parts.append(module_svg(name, content.ports))
    paragraphs = description_paragraphs(content.description)
    if paragraphs:
        anchor = f"description-{html.escape(name)}"
        parts.append(f'<h2 id="{anchor}">Description</h2>')
        parts.extend(f"<p>{html.escape(paragraph)}</p>"
                     for paragraph in paragraphs)
    parts.append(emit_table(
        name, "Parameters", ("Name", "Type", "Value", "Description"),
        content.parameters))
    if content.ports:
        rows = tuple(Row((port.name, port.direction, port.type,
                          port.description)) for port in content.ports)
        parts.append(emit_table(
            name, "Ports", ("Name", "Direction", "Type", "Description"),
            rows))
    parts.append(emit_table(
        name, "Signals", ("Name", "Type", "Description"), content.signals))
    parts.append(emit_table(
        name, "Constants", ("Name", "Type", "Value", "Description"),
        content.constants))
    parts.append(emit_table(
        name, "Types", ("Name", "Definition", "Description"), content.types))
    parts.append(emit_list(name, "Processes", content.processes))
    parts.append(emit_list(name, "Functions", content.functions))
    parts.append(emit_list(name, "Instantiations", content.instantiations))
    return "\n".join(part for part in parts if part)


def emit_document(contents: Sequence[Content], revision: str) -> str:
    """Render the complete self-contained reference document."""
    if not SHA_RE.fullmatch(revision):
        raise GenerationError(f"invalid source revision: {revision!r}")
    links = []
    for content in contents:
        declaration = content.declaration
        label = "module" if declaration.kind == "module" else "package"
        links.append(
            f'<li><a href="#{label}-{html.escape(declaration.name)}">'
            f"{html.escape(declaration.name)}</a></li>")
    parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{DOCUMENT_TITLE}</title>",
        DOCUMENT_STYLE,
        PRINT_STYLE,
        "</head>",
        "<body>",
        f"<h1>{DOCUMENT_TITLE}</h1>",
        f"Source revision <code>{html.escape(revision)}</code><br><br>",
        REVISION_NOTICE,
        '<nav aria-label="Contents"><ul>',
        "\n".join(links),
        "</ul></nav>",
        "\n".join(emit_section(content) for content in contents),
        "</body>",
        "</html>",
    ]
    return "\n".join(parts) + "\n"


def parsed_sections(source: str) -> dict[tuple[str, str], Section]:
    """Return generated declaration sections."""
    matches = tuple(SECTION_RE.finditer(source))
    sections = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        kind = "module" if match.group(1) == "Module" else "package"
        name = html.unescape(match.group(2)).strip()
        key = (kind, name)
        if key in sections:
            raise GenerationError(f"duplicate HTML section: {key}")
        sections[key] = Section(kind, name, source[match.end():end])
    return sections


def validate_svg(name: str, source: str) -> None:
    """Require one parseable SVG containing graphical content."""
    try:
        root = ET.fromstring(source)
    except ET.ParseError as exc:
        raise GenerationError(
            f"HTML module {name} contains malformed SVG: {exc}") from exc
    if root.tag.rsplit("}", 1)[-1] != "svg":
        raise GenerationError(f"HTML module {name} lacks an SVG root")
    if "viewBox" not in root.attrib:
        raise GenerationError(f"HTML module {name} SVG lacks a viewBox")
    tags = {item.tag.rsplit("}", 1)[-1] for item in root.iter()}
    if not tags.intersection(GRAPHIC_TAGS):
        raise GenerationError(
            f"HTML module {name} SVG lacks graphical content")


def svg_blocks(source: str) -> tuple[str, ...]:
    """Extract balanced SVG elements, including nested SVGs."""
    blocks = []
    depth = 0
    start = None
    for match in SVG_TAG_RE.finditer(source):
        closing = bool(match.group(1))
        self_closing = match.group(0).rstrip().endswith("/>")
        if closing:
            if depth == 0:
                raise GenerationError("generated HTML has an unmatched SVG close")
            depth -= 1
            if depth == 0:
                blocks.append(source[start:match.end()])
                start = None
        elif self_closing:
            if depth == 0:
                blocks.append(match.group(0))
        else:
            if depth == 0:
                start = match.start()
            depth += 1
    if depth:
        raise GenerationError("generated HTML has an unclosed SVG element")
    return tuple(blocks)


def validate_module_diagram(section: Section) -> None:
    """Require one structural diagram beneath one heading."""
    marker = diagram_marker(section.name)
    heading_count = section.body.count(marker)
    if heading_count != 1:
        raise GenerationError(
            f"HTML module {section.name} has {heading_count} diagram headings")
    diagram = section.body.split(marker, 1)[1]
    next_heading = diagram.find("<h2")
    if next_heading >= 0:
        diagram = diagram[:next_heading]
    svgs = svg_blocks(diagram)
    if len(svgs) != 1:
        raise GenerationError(
            f"HTML module {section.name} has {len(svgs)} SVG diagrams")
    validate_svg(section.name, svgs[0])


def validate_html(source: str, census: Census, revision: str,
                  forbidden_paths: Sequence[Path] = ()) -> None:
    """Prove title, provenance, privacy, sections, and diagrams."""
    if f"<h1>{DOCUMENT_TITLE}</h1>" not in source:
        raise GenerationError("generated HTML lacks its visible title")
    if f"<title>{DOCUMENT_TITLE}</title>" not in source:
        raise GenerationError("generated HTML lacks its browser title")
    if f"Source revision <code>{revision}</code>" not in source:
        raise GenerationError("generated HTML lacks exact source provenance")
    if source.count('id="milan-render-safety"') != 1:
        raise GenerationError("generated HTML lacks rendering safeguards")
    if TIMESTAMP_RE.search(source):
        raise GenerationError("generated HTML carries a generated timestamp")
    if LOCAL_PATH_RE.search(source):
        raise GenerationError("generated HTML leaks an absolute build path")
    leaked = [str(path) for path in forbidden_paths if str(path) in source]
    if leaked:
        raise GenerationError("generated HTML leaks its generation directory")
    if PRIVATE_DEVICE_RE.search(source):
        raise GenerationError("generated HTML contains a private device name")
    if ACTIVE_HTML_RE.search(source):
        raise GenerationError("generated HTML contains active content")

    sections = parsed_sections(source)
    expected = {(item.kind, item.name) for item in census.supported}
    actual = set(sections)
    if actual != expected:
        missing = sorted(expected - actual)
        unexpected = sorted(actual - expected)
        raise GenerationError(
            f"HTML declaration coverage changed; missing={missing}; "
            f"unexpected={unexpected}")
    for section in sections.values():
        if section.kind == "module":
            validate_module_diagram(section)


def output_target(path: Path, root: Path) -> Path:
    """Resolve a safe, empty destination outside the repository."""
    expanded = path.expanduser().absolute()
    if expanded.is_symlink():
        raise GenerationError("output cannot be a symbolic link")
    target = expanded.resolve()
    repository = root.resolve()
    if target == repository or repository in target.parents:
        raise GenerationError("output must remain outside the repository")
    if target.exists():
        if not target.is_dir():
            raise GenerationError("output already exists and is not a directory")
        if any(target.iterdir()):
            raise GenerationError("output directory is not empty")
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def generate(root: Path, target_path: Path, revision: str,
             known_omissions: frozenset[DeclarationKey] = KNOWN_OMISSIONS) -> Census:
    """Generate, validate, then atomically publish one reference."""
    target = output_target(target_path, root)
    census = source_census(root, known_omissions)
    parser = load_parser()
    contents, _ = extract_reference(parser, root, census)
    document = emit_document(contents, revision)
    stage = Path(tempfile.mkdtemp(prefix=f".{target.name}.",
                                  dir=target.parent))
    published = False
    try:
        validate_html(document, census, revision,
                      (root.resolve(), stage.resolve(), target.resolve()))
        (stage / "index.html").write_text(document, encoding="utf-8")
        if target.exists():
            target.rmdir()
        os.replace(stage, target)
        published = True
    except OSError as exc:
        raise GenerationError(f"cannot publish generated documentation: {exc}") from exc
    finally:
        if not published:
            shutil.rmtree(stage, ignore_errors=True)

    module_count = sum(item.kind == "module" for item in census.supported)
    package_count = sum(item.kind == "package" for item in census.supported)
    print(f"HDL reference schema: {DOCUMENT_SCHEMA}")
    print(f"Parser: {PARSER_NAME} {PARSER_VERSION}")
    print(f"Source revision: {revision}")
    print(f"Supported sections: {len(census.supported)} "
          f"({module_count} modules, {package_count} packages)")
    print(f"Module diagrams: {module_count}")
    print("Known limitations:")
    for omission in census.omissions:
        print(f"  - {omission.path}: {omission.kind} {omission.name}")
    print(f"Wrote: {target / 'index.html'}")
    return census


def run_process(command: Sequence[str], root: Path,
                environment: dict[str, str]) -> str:
    """Run one command and return combined diagnostics."""
    try:
        completed = subprocess.run(
            command, cwd=root, env=environment, text=True,
            capture_output=True, check=False)
    except OSError as exc:
        raise GenerationError(f"cannot execute {command[0]}: {exc}") from exc
    diagnostics = completed.stdout + completed.stderr
    if completed.returncode:
        tail = "\n".join(diagnostics.splitlines()[-12:])
        raise GenerationError(
            f"{command[0]} failed with exit {completed.returncode}:\n{tail}")
    return diagnostics


def git_revision(root: Path) -> str:
    """Return HEAD only when the documented HDL matches it."""
    environment = os.environ.copy()
    dirty = run_process(
        ["git", "status", "--porcelain", "--untracked-files=all", "--", "hdl"],
        root, environment)
    if dirty.strip():
        raise GenerationError("HDL sources are dirty; provenance is ambiguous")
    revision = run_process(["git", "rev-parse", "HEAD"], root, environment).strip()
    if not SHA_RE.fullmatch(revision):
        raise GenerationError(f"git returned an invalid revision: {revision!r}")
    return revision


def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    """Parse the destination and the self-test switch."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help=f"empty destination outside the repository (default: {DEFAULT_OUTPUT})")
    parser.add_argument(
        "--selftest", action="store_true",
        help="run isolated mutation and refusal tests")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Generate or self-test, turning every refusal into exit 2."""
    args = parse_args(argv)
    try:
        if args.selftest:
            # Registered under the import name FIRST, and only then imported
            # from: two arms patch a binding this module owns, so the arms and
            # this `except` clause have to be looking at the object running
            # here rather than at a second copy imported beside `__main__`.
            sys.modules.setdefault("gen_hdl_reference", sys.modules[__name__])
            from gen_hdl_reference_selftest import run_selftest
            run_selftest()
            return 0
        revision = git_revision(ROOT)
        generate(ROOT, args.output, revision)
        return 0
    except (GenerationError, AssertionError) as exc:
        print(f"gen_hdl_reference: REFUSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
