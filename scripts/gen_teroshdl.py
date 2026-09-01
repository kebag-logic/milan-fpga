#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate one validated, self-contained TerosHDL HTML reference."""

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
DEFAULT_OUTPUT = Path("/tmp/milan-teroshdl-doc")
DOCUMENT_TITLE = "Milan FPGA HDL reference"
DOCUMENT_SCHEMA = "teroshdl-html-v1"
DOCUMENT_VERSION = "2.0.3"
SOURCE_SUFFIXES = frozenset((".sv", ".v", ".svh"))
PARSED_SUFFIXES = frozenset((".sv", ".v"))
KNOWN_OMISSIONS = frozenset({
    ("hdl/common/axi_stream_if.sv", "interface", "axi_stream_if"),
    ("hdl/ieee1722/aaf/KL_aaf_latency_taps.sv",
     "module", "KL_aaf_latency_taps"),
})
KNOWN_DIAGRAM_FALLBACKS = frozenset()
DECLARATION_RE = re.compile(
    r"(?m)^[ \t]*(module|package|interface)[ \t]+"
    r"(?:automatic[ \t]+)?([A-Za-z_][A-Za-z0-9_$]*)\b")
SECTION_RE = re.compile(
    r'<h1 id="(?:entity|package)-[^"]+">'
    r'(Entity|Package):\s*([^<]+)</h1>')
DIAGRAM_MARKER = '<h2 id="diagram">Diagram</h2>'
SVG_TAG_RE = re.compile(r"<(/?)svg\b[^>]*?>", re.IGNORECASE | re.DOTALL)
GRAPHIC_TAGS = frozenset({
    "circle", "ellipse", "image", "line", "path", "polygon", "polyline",
    "rect", "text", "use",
})
PRINT_STYLE = '''\
<style id="milan-render-safety">
svg { max-width: 100%; height: auto; }
@media print {
  h1[id^="entity-"], h1[id^="package-"] { break-before: page; }
  h1, h2, h3 { break-after: avoid-page; }
  svg, table { break-inside: avoid; }
}
</style>
'''
SUMMARY_FIELDS = {
    "found": re.compile(r"Files found:\s*(\d+)"),
    "processed": re.compile(r"Files processed successfully:\s*(\d+)"),
    "unprocessed": re.compile(r"Unprocessed files:\s*(\d+)"),
}
REVISION_RE = re.compile(r"Project revision [^<\r\n]*<br><br>")
SHA_RE = re.compile(r"[0-9a-f]{40}")
ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
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
    """Expected TerosHDL coverage derived from current sources."""

    files_found: int
    files_processed: int
    files_unprocessed: int
    supported: tuple
    omissions: tuple


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
        raise GenerationError("TerosHDL exception inventory changed; "
                              + "; ".join(details))

    return Census(
        files_found=len(files),
        files_processed=len(parsed),
        files_unprocessed=len(files) - len(parsed),
        supported=tuple(sorted(supported)),
        omissions=tuple(sorted(omissions)),
    )


def tool_environment():
    """Return the stable Node environment required by this release."""
    environment = os.environ.copy()
    option = "--no-experimental-fetch"
    options = environment.get("NODE_OPTIONS", "").split()
    if option not in options:
        options.append(option)
    environment["NODE_OPTIONS"] = " ".join(options)
    return environment


def run_process(command, root, environment):
    """Run one tool command and return combined diagnostics."""
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


def verify_tool(documenter, root, environment):
    """Require the dependency version locked by this repository."""
    output = run_process([documenter, "--version"], root, environment)
    versions = [line.strip() for line in output.splitlines()
                if re.fullmatch(r"\d+\.\d+\.\d+", line.strip())]
    if versions != [DOCUMENT_VERSION]:
        raise GenerationError(
            f"TerosHDL version must be {DOCUMENT_VERSION}; found "
            f"{versions or 'no semantic version'}")


def verify_summary(output, census):
    """Match TerosHDL's completion summary against source discovery."""
    clean = ANSI_RE.sub("", output)
    expected = {
        "found": census.files_found,
        "processed": census.files_processed,
        "unprocessed": census.files_unprocessed,
    }
    for name, pattern in SUMMARY_FIELDS.items():
        matches = pattern.findall(clean)
        if len(matches) != 1:
            raise GenerationError(
                f"TerosHDL summary field {name!r} appeared {len(matches)} times")
        observed = int(matches[0])
        if observed != expected[name]:
            raise GenerationError(
                f"TerosHDL summary {name}={observed}; expected "
                f"{expected[name]}")


def normalize_html(source, revision):
    """Replace unstable boilerplate with exact source provenance."""
    if not SHA_RE.fullmatch(revision):
        raise GenerationError(f"invalid source revision: {revision!r}")
    old_heading = "<h1>Documentation for: </h1>"
    if source.count(old_heading) != 1:
        raise GenerationError("TerosHDL emitted an unexpected document heading")
    if len(REVISION_RE.findall(source)) != 1:
        raise GenerationError("TerosHDL emitted an unexpected revision field")

    notice = (
        f"Source revision <code>{html.escape(revision)}</code><br><br>\n"
        '<section aria-label="Reference scope">\n'
        '<p>Generated from first-party HDL sources.</p>\n'
        '<ul>\n'
        '<li>Modules include ports and diagrams.</li>\n'
        '<li>Packages include source-derived details.</li>\n'
        '<li>Interfaces lack standalone sections.</li>\n'
        '<li>Additional file declarations require source review.</li>\n'
        '</ul>\n'
        '</section>\n')
    normalized = source.replace(
        old_heading, f"<h1>{DOCUMENT_TITLE}</h1>", 1)
    normalized = REVISION_RE.sub(notice, normalized, count=1)
    normalized = normalized.replace(
        "<title>TerosHDL</title>", f"<title>{DOCUMENT_TITLE}</title>")
    if "</head>" not in normalized:
        raise GenerationError("TerosHDL emitted no document head")
    normalized = normalized.replace("</head>", PRINT_STYLE + "</head>", 1)
    return normalized


def parsed_sections(source):
    """Return generated declaration sections."""
    matches = tuple(SECTION_RE.finditer(source))
    sections = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        kind = "module" if match.group(1) == "Entity" else "package"
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
    heading_count = section.body.count(DIAGRAM_MARKER)
    if heading_count != 1:
        raise GenerationError(
            f"HTML module {section.name} has {heading_count} diagram headings")
    diagram = section.body.split(DIAGRAM_MARKER, 1)[1]
    next_heading = diagram.find("<h2")
    if next_heading >= 0:
        diagram = diagram[:next_heading]
    svgs = svg_blocks(diagram)
    if len(svgs) != 1:
        raise GenerationError(
            f"HTML module {section.name} has {len(svgs)} SVG diagrams")
    validate_svg(section.name, svgs[0])


def module_ports(root, declaration):
    """Extract ANSI port names for a compatibility diagram."""
    path = root / declaration.path
    try:
        source = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
    except OSError as exc:
        raise GenerationError(f"cannot read fallback source {path}: {exc}") from exc
    match = re.search(
        rf"(?m)^[ \t]*module[ \t]+{re.escape(declaration.name)}\b", source)
    if match is None:
        raise GenerationError(
            f"fallback module declaration vanished: {declaration.name}")
    header_end = source.find(");", match.end())
    if header_end < 0:
        raise GenerationError(
            f"fallback module header is incomplete: {declaration.name}")
    header = source[match.end():header_end]
    ports = []
    for line in header.splitlines():
        direction = re.match(r"^[ \t]*(input|output|inout)\b", line)
        if direction is None:
            continue
        names = re.findall(r"[A-Za-z_][A-Za-z0-9_$]*", line)
        if len(names) < 2:
            raise GenerationError(
                f"fallback port cannot be parsed: {declaration.name}")
        ports.append((direction.group(1), names[-1]))
    if not ports:
        raise GenerationError(
            f"fallback module has no ANSI ports: {declaration.name}")
    names = [name for _, name in ports]
    if len(names) != len(set(names)):
        raise GenerationError(
            f"fallback module has duplicate ports: {declaration.name}")
    return tuple(ports)


def fallback_svg(root, declaration):
    """Render an accessible SVG from current module ports."""
    ports = module_ports(root, declaration)
    inputs = [name for direction, name in ports if direction == "input"]
    outputs = [name for direction, name in ports if direction != "input"]
    rows = max(len(inputs), len(outputs), 1)
    height = 100 + rows * 34
    box_top = 42
    box_height = height - 52
    title_id = f"fallback-title-{declaration.name}"
    parts = [
        (f'<p><svg xmlns="http://www.w3.org/2000/svg" '
         f'viewBox="0 0 960 {height}" role="img" '
         f'aria-labelledby="{html.escape(title_id)}" '
         'data-diagram-source="source-ports">'),
        f'<title id="{html.escape(title_id)}">Port diagram for '
        f'{html.escape(declaration.name)}</title>',
        '<style>text{font:18px sans-serif;fill:#17233c}'
        '.box{fill:#eef5ff;stroke:#275d9b;stroke-width:3}'
        '.wire{stroke:#275d9b;stroke-width:2}</style>',
        (f'<rect class="box" x="330" y="{box_top}" width="300" '
         f'height="{box_height}" rx="18"/>'),
        (f'<text x="480" y="76" text-anchor="middle" font-weight="700">'
         f'{html.escape(declaration.name)}</text>'),
    ]
    for index, name in enumerate(inputs):
        y = 116 + index * 34
        parts.append(f'<line class="wire" x1="300" y1="{y}" x2="330" y2="{y}"/>')
        parts.append(
            f'<text x="292" y="{y + 6}" text-anchor="end">'
            f'{html.escape(name)}</text>')
    for index, name in enumerate(outputs):
        y = 116 + index * 34
        parts.append(f'<line class="wire" x1="630" y1="{y}" x2="660" y2="{y}"/>')
        parts.append(
            f'<text x="668" y="{y + 6}">{html.escape(name)}</text>')
    parts.append("</svg></p>")
    return "".join(parts)


def add_fallback_diagrams(source, census, root,
                          known_fallbacks=KNOWN_DIAGRAM_FALLBACKS):
    """Fill only recorded TerosHDL compatibility gaps."""
    matches = tuple(SECTION_RE.finditer(source))
    sections = parsed_sections(source)
    supported = {(item.kind, item.name): item for item in census.supported}
    allowed = frozenset(known_fallbacks)
    replacements = []
    for index, (key, section) in enumerate(sections.items()):
        if section.kind != "module" or svg_blocks(section.body):
            continue
        declaration = supported.get(key)
        if declaration is None or declaration.key not in allowed:
            continue
        if section.body.count(DIAGRAM_MARKER) != 1:
            continue
        body_start = matches[index].end()
        position = body_start + section.body.index(DIAGRAM_MARKER) + len(DIAGRAM_MARKER)
        replacements.append((position, declaration, fallback_svg(root, declaration)))
    for position, _, diagram in reversed(replacements):
        source = source[:position] + diagram + source[position:]
    return source, tuple(item.name for _, item, _ in replacements)


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
    if "Project revision" in source:
        raise GenerationError("generated HTML retains a generated timestamp")
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


def generate(root, target_path, documenter, revision,
             known_omissions=KNOWN_OMISSIONS,
             known_fallbacks=KNOWN_DIAGRAM_FALLBACKS):
    """Generate, validate, then atomically publish one reference."""
    target = output_target(target_path, root)
    census = source_census(root, known_omissions)
    environment = tool_environment()
    verify_tool(documenter, root, environment)
    stage = Path(tempfile.mkdtemp(prefix=f".{target.name}.",
                                  dir=target.parent))
    published = False
    try:
        command = [
            documenter,
            "--recursive",
            "-o", "html",
            "--self_contained",
            "--symbol_verilog", "!",
            "-s", "all",
            "-c", "all",
            "-p", "all",
            "-f", "all",
            "--outpath", str(stage),
            "--input", "hdl",
        ]
        diagnostics = run_process(command, root, environment)
        verify_summary(diagnostics, census)
        generated = tuple(sorted(path.relative_to(stage).as_posix()
                                 for path in stage.rglob("*") if path.is_file()))
        if generated != ("index.html",):
            raise GenerationError(
                f"TerosHDL output set changed: {list(generated)}")
        index = stage / "index.html"
        source = index.read_text(encoding="utf-8")
        normalized = normalize_html(source, revision)
        normalized, fallbacks = add_fallback_diagrams(
            normalized, census, root, known_fallbacks)
        validate_html(normalized, census, revision,
                      (root.resolve(), stage.resolve(), target.resolve()))
        index.write_text(normalized, encoding="utf-8")
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
    print(f"TerosHDL schema: {DOCUMENT_SCHEMA}")
    print(f"Source revision: {revision}")
    print(f"Supported sections: {len(census.supported)} "
          f"({module_count} modules, {package_count} packages)")
    print(f"Module diagrams: {module_count}")
    print(f"Source-derived fallback diagrams: {len(fallbacks)}")
    print("Known limitations:")
    for omission in census.omissions:
        print(f"  - {omission.path}: {omission.kind} {omission.name}")
    print(f"Wrote: {target / 'index.html'}")
    return census


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


def fake_html(revision_time="2026-08-31 12:34:56",
              drop_section=None, drop_svg=None, extra=""):
    """Build a small documenter fixture for mutation tests."""
    svg = ('<p><svg xmlns="http://www.w3.org/2000/svg" '
           'viewBox="0 0 40 20"><rect width="40" height="20"/></svg></p>')
    rows = []
    for kind, name in (("module", "alpha"), ("package", "config_pkg"),
                       ("module", "first"), ("module", "legacy")):
        if name == drop_section:
            continue
        label = "Entity" if kind == "module" else "Package"
        diagram = ""
        if kind == "module":
            diagram = DIAGRAM_MARKER
            if name != drop_svg:
                diagram += svg
        rows.append(
            f'<h1 id="{label.lower()}-{name}">{label}: {name}</h1>{diagram}')
    return (
        "<html><head><title>TerosHDL</title></head><body>\n"
        "<h1>Documentation for: </h1>\n"
        f"Project revision {revision_time}<br><br>\n"
        + "\n".join(rows) + extra + "\n</body></html>\n")


def write_fake_documenter(path, document, version=DOCUMENT_VERSION,
                          summary=True, fail=False, extra_file=False,
                          summary_counts=(6, 5, 1)):
    """Create an executable documenter fixture."""
    script = f'''\
#!/usr/bin/env python3
import pathlib
import sys

if "--version" in sys.argv:
    print({version!r})
    raise SystemExit(0)
if {fail!r}:
    print("injected generation failure")
    raise SystemExit(7)
args = sys.argv[1:]
out = pathlib.Path(args[args.index("--outpath") + 1])
out.mkdir(parents=True, exist_ok=True)
(out / "index.html").write_text({document!r}, encoding="utf-8")
if {extra_file!r}:
    (out / "unexpected.txt").write_text("unexpected", encoding="utf-8")
if {summary!r}:
    print("Files found: " + str({summary_counts[0]}))
    print("Files processed successfully: " + str({summary_counts[1]}))
    print("Unprocessed files: " + str({summary_counts[2]}))
'''
    path.write_text(script, encoding="utf-8")
    path.chmod(0o755)


def fixture_tree(base):
    """Create representative HDL declarations for self-tests."""
    root = base / "repo"
    hdl = root / "hdl"
    hdl.mkdir(parents=True)
    (hdl / "one.sv").write_text(textwrap.dedent('''\
        // module ignored_line;
        module alpha (
          input wire clk_i,
          output logic ready_o
        );
          string note = "module ignored_string;";
        endmodule
    '''), encoding="utf-8")
    (hdl / "defs.sv").write_text(
        "/* package ignored_block; */\npackage config_pkg; endpackage\n",
        encoding="utf-8")
    (hdl / "bus.sv").write_text(
        "interface sample_if; endinterface\n", encoding="utf-8")
    (hdl / "double.sv").write_text(
        "module first; endmodule\nmodule second; endmodule\n",
        encoding="utf-8")
    (hdl / "legacy.v").write_text(
        "module legacy; endmodule\n", encoding="utf-8")
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


def _failed_publication(root, target, documenter, revision, known):
    """Inject an atomic publication failure."""
    with mock.patch.object(os, "replace", side_effect=OSError("injected")):
        generate(root, target, documenter, revision, known)


def _mocked_git_revision(root, outputs):
    """Run provenance logic against controlled Git answers."""
    module = sys.modules[__name__]
    with mock.patch.object(module, "run_process", side_effect=outputs):
        git_revision(root)


def run_selftest():
    """Exercise positive generation and independent refusal arms."""
    revision = "1" * 40
    arms = []
    with tempfile.TemporaryDirectory(prefix="teroshdl-selftest-") as raw:
        base = Path(raw)
        root, known = fixture_tree(base)

        def tool(name, document=None, **options):
            path = base / name
            write_fake_documenter(
                path, fake_html() if document is None else document, **options)
            return str(path)

        def rejects(name, action, phrase):
            expect_error(name, action, phrase)
            arms.append(name)

        fallback = frozenset({("hdl/one.sv", "module", "alpha")})
        positive = base / "positive"
        census = generate(
            root, positive, tool("valid", fake_html(drop_svg="alpha")),
            revision, known, fallback)
        assert len(census.supported) == 4
        positive_html = (positive / "index.html").read_text(encoding="utf-8")
        assert DOCUMENT_TITLE in positive_html
        assert 'data-diagram-source="source-ports"' in positive_html
        arms.append("valid generation")

        normalized_fixture = normalize_html(fake_html(), revision)

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
            "missing executable",
            lambda: run_process(
                [str(base / "absent-documenter")], root, tool_environment()),
            "cannot execute")
        rejects(
            "wrong version",
            lambda: generate(root, base / "wrong-version",
                             tool("wrong-version-tool", version="9.9.9"),
                             revision, known),
            "version must be")
        rejects(
            "tool failure",
            lambda: generate(root, base / "tool-failure",
                             tool("failing-tool", fail=True), revision, known),
            "failed with exit")
        rejects(
            "missing summary",
            lambda: generate(root, base / "missing-summary",
                             tool("no-summary-tool", summary=False), revision, known),
            "summary field")
        rejects(
            "wrong summary",
            lambda: generate(root, base / "wrong-summary",
                             tool("wrong-summary-tool", summary_counts=(7, 5, 2)),
                             revision, known),
            "summary found=")

        rejects(
            "invalid requested revision",
            lambda: normalize_html(fake_html(), "not-a-revision"),
            "invalid source revision")
        rejects(
            "unexpected document heading",
            lambda: normalize_html(
                fake_html().replace("Documentation for:", "Changed"), revision),
            "unexpected document heading")
        rejects(
            "unexpected revision field",
            lambda: normalize_html(
                fake_html(extra=(
                    "Project revision 2000-01-01 00:00:00<br><br>")), revision),
            "unexpected revision field")
        rejects(
            "missing document head",
            lambda: normalize_html(fake_html().replace("</head>", ""), revision),
            "no document head")

        def validates(document, forbidden_paths=()):
            return validate_html(document, census, revision, forbidden_paths)

        duplicate = normalized_fixture + (
            '<h1 id="entity-alpha-copy">Entity: alpha</h1>'
            + DIAGRAM_MARKER
            + '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1">'
              '<rect width="1" height="1"/></svg>')
        rejects("duplicate section", lambda: validates(duplicate),
                "duplicate HTML section")
        rejects(
            "missing visible title",
            lambda: validates(normalized_fixture.replace(
                f"<h1>{DOCUMENT_TITLE}</h1>", "<h1>Missing</h1>")),
            "lacks its visible title")
        rejects(
            "missing browser title",
            lambda: validates(normalized_fixture.replace(
                f"<title>{DOCUMENT_TITLE}</title>", "<title>Missing</title>")),
            "lacks its browser title")
        rejects(
            "missing provenance",
            lambda: validates(normalized_fixture.replace(revision, "2" * 40)),
            "lacks exact source provenance")
        rejects(
            "render safeguard",
            lambda: validates(normalized_fixture.replace(PRINT_STYLE, "")),
            "lacks rendering safeguards")
        rejects(
            "retained timestamp",
            lambda: validates(normalized_fixture + "Project revision stale"),
            "retains a generated timestamp")
        rejects(
            "absolute path leak",
            lambda: validates(normalized_fixture + "file:///tmp/private/source.sv"),
            "absolute build path")
        sealed = Path("/sealed/generation")
        rejects(
            "generation directory leak",
            lambda: validates(normalized_fixture + str(sealed), (sealed,)),
            "generation directory")
        private_name = "".join(chr(code) for code in (68, 83, 50, 48, 68))
        rejects(
            "private name",
            lambda: validates(normalized_fixture + private_name),
            "private device name")
        rejects(
            "active content",
            lambda: validates(normalized_fixture + "<script>alert(1)</script>"),
            "active content")
        rejects(
            "missing section",
            lambda: validates(normalize_html(
                fake_html(drop_section="legacy"), revision)),
            "declaration coverage changed")
        extra_section = (
            '<h1 id="entity-surprise">Entity: surprise</h1>' + DIAGRAM_MARKER
            + '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1">'
              '<rect width="1" height="1"/></svg>')
        rejects(
            "extra section",
            lambda: validates(normalize_html(
                fake_html(extra=extra_section), revision)),
            "declaration coverage changed")
        rejects(
            "heading without SVG",
            lambda: validates(normalize_html(fake_html(drop_svg="legacy"), revision)),
            "has 0 SVG diagrams")
        rejects(
            "duplicate diagram heading",
            lambda: validates(normalized_fixture.replace(
                DIAGRAM_MARKER, DIAGRAM_MARKER + DIAGRAM_MARKER, 1)),
            "has 2 diagram headings")
        valid_svg = ('<svg xmlns="http://www.w3.org/2000/svg" '
                     'viewBox="0 0 40 20"><rect width="40" height="20"/></svg>')
        rejects(
            "malformed SVG",
            lambda: validates(normalized_fixture.replace(
                valid_svg,
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1">'
                '<rect></svg>', 1)),
            "malformed SVG")
        rejects(
            "SVG without viewBox",
            lambda: validates(normalized_fixture.replace(
                ' viewBox="0 0 40 20"', "", 1)),
            "SVG lacks a viewBox")
        rejects(
            "empty SVG",
            lambda: validates(normalized_fixture.replace(
                '<rect width="40" height="20"/>', "<metadata/>", 1)),
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

        fallback_root = base / "fallback-fixtures"
        fallback_hdl = fallback_root / "hdl"
        fallback_hdl.mkdir(parents=True)
        rejects(
            "unreadable fallback source",
            lambda: module_ports(
                fallback_root,
                Declaration("hdl/missing.sv", "module", "missing")),
            "cannot read fallback source")
        vanished = fallback_hdl / "vanished.sv"
        vanished.write_text("module present(); endmodule\n", encoding="utf-8")
        rejects(
            "vanished fallback declaration",
            lambda: module_ports(
                fallback_root,
                Declaration("hdl/vanished.sv", "module", "absent")),
            "declaration vanished")
        incomplete = fallback_hdl / "incomplete.sv"
        incomplete.write_text("module incomplete (input wire clk_i\n",
                              encoding="utf-8")
        rejects(
            "incomplete fallback header",
            lambda: module_ports(
                fallback_root,
                Declaration("hdl/incomplete.sv", "module", "incomplete")),
            "header is incomplete")
        bad_port = fallback_hdl / "bad_port.sv"
        bad_port.write_text("module bad_port (\ninput,\n); endmodule\n",
                            encoding="utf-8")
        rejects(
            "unparseable fallback port",
            lambda: module_ports(
                fallback_root,
                Declaration("hdl/bad_port.sv", "module", "bad_port")),
            "port cannot be parsed")
        no_ports = fallback_hdl / "no_ports.sv"
        no_ports.write_text("module no_ports (); endmodule\n", encoding="utf-8")
        rejects(
            "fallback without ports",
            lambda: module_ports(
                fallback_root,
                Declaration("hdl/no_ports.sv", "module", "no_ports")),
            "has no ANSI ports")
        duplicates = fallback_hdl / "duplicates.sv"
        duplicates.write_text(
            "module duplicates (\ninput wire same,\noutput logic same\n);\n"
            "endmodule\n", encoding="utf-8")
        rejects(
            "duplicate fallback ports",
            lambda: module_ports(
                fallback_root,
                Declaration("hdl/duplicates.sv", "module", "duplicates")),
            "has duplicate ports")

        rejects(
            "extra output",
            lambda: generate(root, base / "extra-output",
                             tool("extra-output-tool", extra_file=True),
                             revision, known),
            "output set changed")
        rejects(
            "inside repository",
            lambda: generate(root, root / "generated",
                             tool("inside-tool"), revision, known),
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
            lambda: generate(root, nonempty, tool("nonempty-tool"), revision, known),
            "not empty")
        assert marker.read_text(encoding="utf-8") == "keep"

        failed_target = base / "failed-publish"
        rejects(
            "failed publication",
            lambda: _failed_publication(
                root, failed_target, tool("failed-publish-tool"), revision, known),
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

    print(f"TerosHDL generator self-test: {len(arms)}/{len(arms)} arms passed")


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help=f"empty destination outside the repository (default: {DEFAULT_OUTPUT})")
    parser.add_argument(
        "--documenter", default="teroshdl-hdl-documenter",
        help="path to the locked documenter executable")
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
        generate(ROOT, args.output, args.documenter, revision)
        return 0
    except (GenerationError, AssertionError) as exc:
        print(f"gen_teroshdl: REFUSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
