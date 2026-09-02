#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate one validated, self-contained first-party HDL reference."""

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from unittest import mock


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
    def key(self):
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


def strip_comments(source):
    """Blank comments while preserving lines and quoted strings."""
    result = []
    index = 0
    state = "code"
    while index < len(source):
        char = source[index]
        following = source[index + 1] if index + 1 < len(source) else ""
        if state == "line":
            if char == "\n":
                result.append(char)
                state = "code"
            else:
                result.append(" ")
        elif state == "block":
            if char == "*" and following == "/":
                result.extend((" ", " "))
                index += 1
                state = "code"
            else:
                result.append("\n" if char == "\n" else " ")
        elif state == "string":
            result.append(char)
            if char == "\\" and following:
                result.append(following)
                index += 1
            elif char == '"':
                state = "code"
        elif char == "/" and following == "/":
            result.extend((" ", " "))
            index += 1
            state = "line"
        elif char == "/" and following == "*":
            result.extend((" ", " "))
            index += 1
            state = "block"
        else:
            result.append(char)
            if char == '"':
                state = "string"
        index += 1
    return "".join(result)


def doc_comments(source):
    """Map line numbers to documentation comments outside strings.

    Returns {line: (owns_line, text)} for every `//!` comment, where
    owns_line is True when no code precedes the comment on its line.
    """
    stripped = strip_comments(source)
    comments = {}
    for number, (raw, bare) in enumerate(
            zip(source.splitlines(), stripped.splitlines()), start=1):
        start = None
        for index in range(len(raw) - 1):
            if (raw[index:index + 2] == "//"
                    and bare[index:index + 2] == "  "):
                start = index
                break
        if start is None or raw[start:start + 3] != "//!":
            continue
        comments[number] = (not bare[:start].strip(),
                           raw[start + 3:].strip())
    return comments


def leading_docs(comments, line):
    """Collect the contiguous documentation block above one line."""
    collected = []
    cursor = line - 1
    while cursor in comments and comments[cursor][0]:
        collected.append(comments[cursor][1])
        cursor -= 1
    return tuple(reversed(collected))


PREAMBLE_RE = re.compile(r"^(?:`.*|import\s[^;]*;)$")


def declaration_docs(comments, bare_lines, line):
    """Find the description block above one declaration.

    Blank lines, compiler directives, and package imports may
    separate the block; any other code ends the search.
    """
    cursor = line - 1
    while cursor >= 1:
        entry = comments.get(cursor)
        if entry is not None and entry[0]:
            return leading_docs(comments, cursor + 1)
        bare = bare_lines[cursor - 1].strip() if cursor <= len(bare_lines) else ""
        if bare and not PREAMBLE_RE.fullmatch(bare):
            return ()
        cursor -= 1
    return ()


def description_paragraphs(lines):
    """Join documentation lines into blank-line-split paragraphs."""
    paragraphs = []
    current = []
    for line in lines:
        if line:
            current.append(line)
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return tuple(paragraphs)


def item_description(comments, first_line, name_line):
    """Prefer a same-line comment, then the block above the item."""
    trailing = comments.get(name_line)
    if trailing is not None and not trailing[0]:
        return trailing[1]
    above = leading_docs(comments, first_line)
    return " ".join(part for part in above if part)


def declarations_in(root, path):
    """Return declarations found outside source comments."""
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise GenerationError(f"cannot read {path}: {exc}") from exc
    relative = path.relative_to(root).as_posix()
    return tuple(Declaration(relative, match.group(1), match.group(2))
                 for match in DECLARATION_RE.finditer(strip_comments(source)))


def source_census(root, known_omissions=KNOWN_OMISSIONS):
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


def load_parser():
    """Import the pinned parser or refuse with its install path."""
    try:
        import pyslang
    except ImportError as exc:
        raise GenerationError(
            "the pinned parser is unavailable; install "
            "tools/hdl_reference/requirements.txt") from exc
    return verify_parser(pyslang)


def verify_parser(module):
    """Require the parser release locked by this repository."""
    version = getattr(module, "__version__", None)
    if version != PARSER_VERSION:
        raise GenerationError(
            f"{PARSER_NAME} version must be {PARSER_VERSION}; "
            f"found {version!r}")
    return module


def include_directories(root):
    """Return every directory holding HDL sources or headers."""
    hdl_root = root / "hdl"
    return tuple(sorted({str(path.parent) for path in hdl_root.rglob("*")
                         if path.is_file()
                         and path.suffix.lower() in SOURCE_SUFFIXES}))


def parse_file(parser, root, incdirs, path):
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


def node_text(source_bytes, node):
    """Return one node's exact source text without any trivia.

    Parser offsets count bytes, so slicing happens on bytes and
    the exact slice is decoded afterwards.
    """
    span = node.sourceRange
    raw = source_bytes[span.start.offset:span.end.offset]
    return " ".join(raw.decode("utf-8", errors="replace").split())


def node_line(manager, node):
    """Return the line of one node's first token."""
    return manager.getLineNumber(node.getFirstToken().location)


def syntax_items(parser, node):
    """Iterate syntax children, skipping separator tokens."""
    return (item for item in node
            if isinstance(item, parser.syntax.SyntaxNode))


def declared_here(manager, path, node):
    """Report whether one member truly lives in the parsed file."""
    name = manager.getFileName(node.getFirstToken().location)
    return Path(name).resolve() == path.resolve()


def parameter_rows(parser, source_bytes, comments, manager, nodes):
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


def dimensions_text(source_bytes, declarator):
    """Render one declarator's unpacked dimensions, if any."""
    dimensions = getattr(declarator, "dimensions", None)
    if not dimensions:
        return ""
    parts = (node_text(source_bytes, item) for item in dimensions
             if hasattr(item, "sourceRange"))
    return " ".join(part for part in parts if part)


def port_type_text(source_bytes, header, declarator):
    """Render one ANSI port type from its header and dimensions."""
    header_text = node_text(source_bytes, header)
    trimmed = re.sub(r"^(?:input|output|inout|ref)\b", "", header_text).strip()
    suffix = dimensions_text(source_bytes, declarator)
    if suffix:
        trimmed = f"{trimmed} {suffix}".strip()
    return trimmed


def module_ports(parser, source_bytes, comments, manager, header):
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


def declarator_rows(parser, source_bytes, comments, manager, node, type_text):
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


def member_content(parser, source_bytes, comments, manager, path, members):
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


def extract_file(parser, root, incdirs, path):
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


def extract_reference(parser, root, census):
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


def diagram_marker(name):
    """Return one section's exact diagram heading."""
    return (f'<h2 class="diagram" id="diagram-{html.escape(name)}">'
            "Diagram</h2>")


def module_svg(name, ports):
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


def emit_table(name, heading, columns, rows):
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


def emit_list(name, heading, entries):
    """Render one facts list beneath its own heading."""
    if not entries:
        return ""
    anchor = f"{heading.lower()}-{html.escape(name)}"
    parts = [f'<h2 id="{anchor}">{heading}</h2>', "<ul>"]
    parts.extend(f"<li><code>{html.escape(entry)}</code></li>"
                 for entry in entries)
    parts.append("</ul>")
    return "\n".join(parts)


def emit_section(content):
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


def emit_document(contents, revision):
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


def parsed_sections(source):
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


def validate_svg(name, source):
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


def svg_blocks(source):
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


def validate_module_diagram(section):
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


def validate_html(source, census, revision, forbidden_paths=()):
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


def output_target(path, root):
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


def generate(root, target_path, revision, known_omissions=KNOWN_OMISSIONS):
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


def run_process(command, root, environment):
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


def git_revision(root):
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


def fixture_tree(base):
    """Create representative HDL declarations for self-tests."""
    root = base / "repo"
    hdl = root / "hdl"
    hdl.mkdir(parents=True)
    (hdl / "one.sv").write_text(textwrap.dedent('''\
        // module ignored_line;
        //! Collects one pulse per grant.
        //! It also mirrors the request stream.

        `default_nettype none

        module alpha #(
          //! synchroniser depth
          parameter int DEPTH = 2
        ) (
          input  wire  clk_i,
          //! request strobe
          input  wire  req_i,
          output logic ready_o //! grant strobe
        );
          //! grant shift register
          logic [DEPTH-1:0] grant_r;
          wire idle_w;
          localparam int WIDE = DEPTH * 2; //! doubled depth
          typedef logic [DEPTH-1:0] lane_t;
          // timing budget: 5 µs of settling
          string note = "module ignored_string;";
          function automatic logic mirror(input logic v);
            mirror = ~v;
          endfunction
          always_ff @(posedge clk_i) begin : grant_seq
            grant_r <= {grant_r[DEPTH-2:0], req_i};
          end
          always_comb ready_o = grant_r[DEPTH-1];
          `include "included.svh"
        endmodule
    '''), encoding="utf-8")
    (hdl / "included.svh").write_text(
        "localparam int FROM_INCLUDE = 9;\n", encoding="utf-8")
    (hdl / "defs.sv").write_text(
        "/* package ignored_block; */\npackage config_pkg; "
        "localparam int LANES = 4; endpackage\n",
        encoding="utf-8")
    (hdl / "bus.sv").write_text(
        "interface sample_if; endinterface\n", encoding="utf-8")
    (hdl / "double.sv").write_text(
        "module first (input wire a_i, output wire b_o);\n"
        "  first_child u_child (.a_i(a_i), .b_o(b_o));\n"
        "endmodule\n"
        "module second; endmodule\n",
        encoding="utf-8")
    (hdl / "legacy.v").write_text(
        "module legacy (input wire tick_i, output wire tock_o);\n"
        "  assign tock_o = tick_i;\n"
        "endmodule\n", encoding="utf-8")
    (hdl / "shared.svh").write_text(
        "`define SHARED 1\n", encoding="utf-8")
    known = frozenset({
        ("hdl/bus.sv", "interface", "sample_if"),
        ("hdl/double.sv", "module", "second"),
    })
    return root, known


def expect_error(name, action, phrase):
    """Require one mutation arm to produce its named refusal."""
    try:
        action()
    except GenerationError as exc:
        if phrase not in str(exc):
            raise AssertionError(
                f"{name}: wrong refusal: {exc}; expected {phrase!r}") from exc
        return
    raise AssertionError(f"{name}: mutation was accepted")


def _unreadable_source(root):
    """Inject one source-read failure."""
    with mock.patch.object(Path, "read_text", side_effect=OSError("injected")):
        declarations_in(root, root / "hdl" / "one.sv")


def _failed_publication(root, target, revision, known):
    """Inject an atomic publication failure."""
    with mock.patch.object(os, "replace", side_effect=OSError("injected")):
        generate(root, target, revision, known)


def _mocked_git_revision(root, outputs):
    """Run provenance logic against controlled Git answers."""
    module = sys.modules[__name__]
    with mock.patch.object(module, "run_process", side_effect=outputs):
        git_revision(root)


def _missing_parser():
    """Import the parser while its module is unavailable."""
    with mock.patch.dict(sys.modules, {"pyslang": None}):
        load_parser()


def _disagreeing_extraction(root, target, revision, known):
    """Drop one extracted declaration behind the census's back."""
    module = sys.modules[__name__]
    original = extract_file

    def dropping(parser, tree_root, incdirs, path):
        contents = original(parser, tree_root, incdirs, path)
        return tuple(item for item in contents
                     if item.declaration.name != "legacy")

    with mock.patch.object(module, "extract_file", dropping):
        generate(root, target, revision, known)


def run_selftest():
    """Exercise positive generation and independent refusal arms."""
    revision = "1" * 40
    arms = []
    with tempfile.TemporaryDirectory(prefix="hdl-reference-selftest-") as raw:
        base = Path(raw)
        root, known = fixture_tree(base)

        def rejects(name, action, phrase):
            expect_error(name, action, phrase)
            arms.append(name)

        positive = base / "positive"
        census = generate(root, positive, revision, known)
        assert len(census.supported) == 4
        positive_html = (positive / "index.html").read_text(encoding="utf-8")
        assert DOCUMENT_TITLE in positive_html
        assert 'data-diagram-source="source-ports"' in positive_html
        assert ("Collects one pulse per grant. "
                "It also mirrors the request stream.") in positive_html
        assert "grant strobe" in positive_html
        assert "synchroniser depth" in positive_html
        assert "doubled depth" in positive_html
        assert "<td>WIDE</td><td>int</td><td>DEPTH * 2</td>" in positive_html
        assert "u_child: first_child" in positive_html
        assert "always_ff : grant_seq ( @(posedge clk_i) )" in positive_html
        #: the UTF-8 byte-slicing tooth ([R1] on PR #331: the first cut's
        #: fixture carried the multibyte character but asserted nothing
        #: PAST it, so reverting byte-slicing to code-point slicing kept
        #: the selftest green while corrupting every later span). These
        #: two sit AFTER the fixture's micro-sign and are byte-exact:
        #: under the revert they read "tring" and "unction ...".
        assert "<td>note</td><td>string</td>" in positive_html
        assert "function automatic logic mirror(input logic v)" in positive_html
        assert "FROM_INCLUDE" not in positive_html
        arms.append("valid generation")

        rejects(
            "unreadable source",
            lambda: _unreadable_source(root),
            "cannot read")

        missing_root = base / "missing-root"
        rejects(
            "missing HDL directory",
            lambda: source_census(missing_root, frozenset()),
            "missing HDL source directory")

        empty_root = base / "empty-root"
        (empty_root / "hdl").mkdir(parents=True)
        (empty_root / "hdl" / "only.svh").write_text(
            "`define ONLY 1\n", encoding="utf-8")
        rejects(
            "empty parsed inventory",
            lambda: source_census(empty_root, frozenset()),
            "inventory is empty")

        blank = root / "hdl" / "blank.sv"
        blank.write_text("`default_nettype none\n", encoding="utf-8")
        rejects(
            "source without declaration",
            lambda: source_census(root, known),
            "contains no declaration")
        blank.unlink()

        rejects(
            "missing parser",
            _missing_parser,
            "parser is unavailable")
        rejects(
            "wrong parser version",
            lambda: verify_parser(type("Stub", (), {"__version__": "9.9.9"})),
            "version must be")

        parser = load_parser()
        incdirs = include_directories(root)

        broken = root / "hdl" / "broken.sv"
        broken.write_text("module broken (\n", encoding="utf-8")
        rejects(
            "unparseable source",
            lambda: parse_file(parser, root, incdirs, broken),
            "cannot parse")
        broken.unlink()

        nonansi = root / "hdl" / "nonansi.sv"
        nonansi.write_text(
            "module nonansi (clk);\ninput clk;\nendmodule\n",
            encoding="utf-8")
        rejects(
            "non-ANSI port list",
            lambda: extract_file(parser, root, incdirs, nonansi),
            "unsupported port list")
        nonansi.unlink()

        explicit = root / "hdl" / "explicit.sv"
        explicit.write_text(
            "module explicit (input .p(sig));\nwire sig;\nendmodule\n",
            encoding="utf-8")
        rejects(
            "explicit port shape",
            lambda: extract_file(parser, root, incdirs, explicit),
            "unsupported port shape")
        explicit.unlink()

        undirected = root / "hdl" / "undirected.sv"
        undirected.write_text(
            "module undirected (wire stray);\nendmodule\n",
            encoding="utf-8")
        rejects(
            "port without direction",
            lambda: extract_file(parser, root, incdirs, undirected),
            "without a direction")
        undirected.unlink()

        duplicates = root / "hdl" / "duplicates.sv"
        duplicates.write_text(
            "module duplicates (input wire same, output logic same);\n"
            "endmodule\n", encoding="utf-8")
        rejects(
            "duplicate ports",
            lambda: extract_file(parser, root, incdirs, duplicates),
            "duplicate ports")
        duplicates.unlink()

        rejects(
            "parser and census disagreement",
            lambda: _disagreeing_extraction(
                root, base / "disagree", revision, known),
            "parser and census disagree")

        rejects(
            "invalid requested revision",
            lambda: emit_document((), "not-a-revision"),
            "invalid source revision")

        contents, _ = extract_reference(parser, root, source_census(root, known))
        emitted = emit_document(contents, revision)

        def validates(document, forbidden_paths=()):
            return validate_html(document, census, revision, forbidden_paths)

        alpha_marker = diagram_marker("alpha")
        duplicate = emitted + (
            '<h1 id="module-alpha">Module: alpha</h1>' + alpha_marker
            + '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1">'
              '<rect width="1" height="1"/></svg>')
        rejects("duplicate section", lambda: validates(duplicate),
                "duplicate HTML section")
        rejects(
            "missing visible title",
            lambda: validates(emitted.replace(
                f"<h1>{DOCUMENT_TITLE}</h1>", "<h1>Missing</h1>")),
            "lacks its visible title")
        rejects(
            "missing browser title",
            lambda: validates(emitted.replace(
                f"<title>{DOCUMENT_TITLE}</title>", "<title>Missing</title>")),
            "lacks its browser title")
        rejects(
            "missing provenance",
            lambda: validates(emitted.replace(revision, "2" * 40)),
            "lacks exact source provenance")
        rejects(
            "render safeguard",
            lambda: validates(emitted.replace(PRINT_STYLE, "")),
            "lacks rendering safeguards")
        rejects(
            "generated timestamp",
            lambda: validates(emitted + "Generated on a build host"),
            "generated timestamp")
        rejects(
            "legacy revision boilerplate",
            lambda: validates(emitted + "Project revision stale"),
            "generated timestamp")
        rejects(
            "absolute path leak",
            lambda: validates(emitted + "file:///tmp/private/source.sv"),
            "absolute build path")
        sealed = Path("/sealed/generation")
        rejects(
            "generation directory leak",
            lambda: validates(emitted + str(sealed), (sealed,)),
            "generation directory")
        private_name = "".join(chr(code) for code in (68, 83, 50, 48, 68))
        rejects(
            "private name",
            lambda: validates(emitted + private_name),
            "private device name")
        rejects(
            "active content",
            lambda: validates(emitted + "<script>alert(1)</script>"),
            "active content")

        legacy_start = emitted.index('<h1 id="module-legacy">')
        alpha_start = emitted.index('<h1 id="module-alpha">')
        body_end = emitted.index("</body>")
        rejects(
            "missing section",
            lambda: validates(
                emitted[:legacy_start] + emitted[alpha_start:]),
            "declaration coverage changed")
        extra_section = (
            '<h1 id="module-surprise">Module: surprise</h1>'
            + diagram_marker("surprise")
            + '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1">'
              '<rect width="1" height="1"/></svg>')
        rejects(
            "extra section",
            lambda: validates(emitted + extra_section),
            "declaration coverage changed")

        legacy_section = emitted[legacy_start:alpha_start]
        legacy_svg = svg_blocks(legacy_section)[0]
        rejects(
            "heading without SVG",
            lambda: validates(emitted.replace(legacy_svg, "", 1)),
            "has 0 SVG diagrams")
        rejects(
            "duplicate diagram heading",
            lambda: validates(emitted.replace(
                alpha_marker, alpha_marker + alpha_marker, 1)),
            "has 2 diagram headings")
        alpha_svg = svg_blocks(emitted[alpha_start:body_end])[0]
        rejects(
            "malformed SVG",
            lambda: validates(emitted.replace(
                alpha_svg,
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1">'
                '<rect></svg>', 1)),
            "malformed SVG")
        rejects(
            "SVG without viewBox",
            lambda: validates(emitted.replace(
                alpha_svg, re.sub(r' viewBox="[^"]*"', "", alpha_svg, count=1), 1)),
            "SVG lacks a viewBox")
        rejects(
            "empty SVG",
            lambda: validate_svg(
                "alpha",
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1">'
                "<metadata/></svg>"),
            "lacks graphical content")
        rejects(
            "non-SVG root",
            lambda: validate_svg(
                "alpha", '<g viewBox="0 0 1 1"><rect/></g>'),
            "lacks an SVG root")
        rejects(
            "unmatched SVG close",
            lambda: svg_blocks("</svg>"),
            "unmatched SVG close")
        rejects(
            "unclosed SVG",
            lambda: svg_blocks('<svg viewBox="0 0 1 1">'),
            "unclosed SVG element")

        rejects(
            "inside repository",
            lambda: generate(root, root / "generated", revision, known),
            "outside the repository")

        symlink = base / "output-symlink"
        symlink.symlink_to(base / "symlink-target")
        rejects(
            "symbolic output",
            lambda: output_target(symlink, root),
            "symbolic link")

        nondirectory = base / "output-file"
        nondirectory.write_text("preserve", encoding="utf-8")
        rejects(
            "nondirectory output",
            lambda: output_target(nondirectory, root),
            "not a directory")

        nonempty = base / "nonempty"
        nonempty.mkdir()
        marker = nonempty / "keep.txt"
        marker.write_text("keep", encoding="utf-8")
        rejects(
            "non-empty preservation",
            lambda: generate(root, nonempty, revision, known),
            "not empty")
        assert marker.read_text(encoding="utf-8") == "keep"

        failed_target = base / "failed-publish"
        rejects(
            "failed publication",
            lambda: _failed_publication(root, failed_target, revision, known),
            "cannot publish generated documentation")
        assert not failed_target.exists()

        new_interface = root / "hdl" / "new_interface.sv"
        new_interface.write_text(
            "interface surprise_if; endinterface\n", encoding="utf-8")
        rejects(
            "exception growth",
            lambda: source_census(root, known),
            "new exceptions")
        new_interface.unlink()

        interface = root / "hdl" / "bus.sv"
        original = interface.read_text(encoding="utf-8")
        interface.write_text(
            "interface renamed_if; endinterface\n", encoding="utf-8")
        rejects(
            "changed exception",
            lambda: source_census(root, known),
            "changed exceptions")
        interface.write_text(original, encoding="utf-8")

        rejects(
            "dirty HDL provenance",
            lambda: _mocked_git_revision(root, [" M hdl/one.sv\n"]),
            "HDL sources are dirty")
        rejects(
            "invalid Git revision",
            lambda: _mocked_git_revision(root, ["", "not-a-revision\n"]),
            "git returned an invalid revision")

    print(f"HDL reference self-test: {len(arms)}/{len(arms)} arms passed")


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help=f"empty destination outside the repository (default: {DEFAULT_OUTPUT})")
    parser.add_argument(
        "--selftest", action="store_true",
        help="run isolated mutation and refusal tests")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        if args.selftest:
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
