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
from dataclasses import dataclass
from pathlib import Path


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
DECLARATION_RE = re.compile(
    r"(?m)^[ \t]*(module|package|interface)[ \t]+"
    r"(?:automatic[ \t]+)?([A-Za-z_][A-Za-z0-9_$]*)\b")
SECTION_RE = re.compile(
    r'<h1 id="(?:entity|package)-[^"]+">'
    r'(Entity|Package):\s*([^<]+)</h1>')
DIAGRAM_MARKER = '<h2 id="diagram">Diagram</h2>'
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
    """Return each declaration section and its diagram presence."""
    matches = tuple(SECTION_RE.finditer(source))
    sections = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        kind = "module" if match.group(1) == "Entity" else "package"
        key = (kind, html.unescape(match.group(2)).strip())
        if key in sections:
            raise GenerationError(f"duplicate HTML section: {key}")
        sections[key] = DIAGRAM_MARKER in source[match.end():end]
    return sections


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
    missing_diagrams = sorted(name for (kind, name), diagram in sections.items()
                              if kind == "module" and not diagram)
    if missing_diagrams:
        raise GenerationError(
            f"HTML modules lack diagrams: {missing_diagrams}")


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
             known_omissions=KNOWN_OMISSIONS):
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
              drop_section=None, drop_diagram=None, extra=""):
    """Build a small documenter fixture for mutation tests."""
    rows = []
    for kind, name in (("module", "alpha"), ("package", "config_pkg"),
                       ("module", "first"), ("module", "legacy")):
        if name == drop_section:
            continue
        label = "Entity" if kind == "module" else "Package"
        diagram = DIAGRAM_MARKER if kind == "module" and name != drop_diagram else ""
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
        module alpha;
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

        positive = base / "positive"
        census = generate(root, positive, tool("valid"), revision, known)
        assert len(census.supported) == 4
        assert DOCUMENT_TITLE in (positive / "index.html").read_text(encoding="utf-8")
        arms.append("valid generation")

        normalized_fixture = normalize_html(fake_html(), revision)
        expect_error(
            "render safeguard",
            lambda: validate_html(
                normalized_fixture.replace(PRINT_STYLE, ""), census, revision),
            "lacks rendering safeguards")
        arms.append("render safeguard")

        mutations = (
            ("wrong version",
             lambda: generate(root, base / "wrong-version",
                              tool("wrong-version-tool", version="9.9.9"),
                              revision, known),
             "version must be"),
            ("tool failure",
             lambda: generate(root, base / "tool-failure",
                              tool("failing-tool", fail=True), revision, known),
             "failed with exit"),
            ("missing summary",
             lambda: generate(root, base / "missing-summary",
                              tool("no-summary-tool", summary=False), revision, known),
             "summary field"),
            ("wrong summary",
             lambda: generate(root, base / "wrong-summary",
                              tool("wrong-summary-tool", summary_counts=(7, 5, 2)),
                              revision, known),
             "summary found="),
            ("missing section",
             lambda: generate(root, base / "missing-section",
                              tool("missing-section-tool",
                                   fake_html(drop_section="legacy")),
                              revision, known),
             "declaration coverage changed"),
            ("missing diagram",
             lambda: generate(root, base / "missing-diagram",
                              tool("missing-diagram-tool",
                                   fake_html(drop_diagram="alpha")),
                              revision, known),
             "lack diagrams"),
            ("extra section",
             lambda: generate(root, base / "extra-section",
                              tool("extra-section-tool", fake_html(extra=(
                                  '<h1 id="entity-surprise">Entity: surprise</h1>'
                                  + DIAGRAM_MARKER))), revision, known),
             "declaration coverage changed"),
            ("path leak",
             lambda: generate(root, base / "path-leak",
                              tool("path-leak-tool",
                                   fake_html(extra="file:///tmp/private/source.sv")),
                              revision, known),
             "absolute build path"),
            ("private name",
             lambda: generate(root, base / "private-name",
                              tool("private-name-tool", fake_html(extra=(
                                  "".join(chr(code) for code in
                                          (68, 83, 50, 48, 68))))),
                              revision, known),
             "private device name"),
            ("active content",
             lambda: generate(root, base / "active-content",
                              tool("active-content-tool",
                                   fake_html(extra="<script>alert(1)</script>")),
                              revision, known),
             "active content"),
            ("timestamp drift",
             lambda: generate(root, base / "timestamp-drift",
                              tool("timestamp-tool", fake_html(extra=(
                                  "Project revision 2000-01-01 00:00:00<br><br>"))),
                              revision, known),
             "unexpected revision field"),
            ("missing document head",
             lambda: generate(root, base / "missing-head",
                              tool("missing-head-tool",
                                   fake_html().replace("</head>", "")),
                              revision, known),
             "no document head"),
            ("extra output",
             lambda: generate(root, base / "extra-output",
                              tool("extra-output-tool", extra_file=True),
                              revision, known),
             "output set changed"),
            ("inside repository",
             lambda: generate(root, root / "generated",
                              tool("inside-tool"), revision, known),
             "outside the repository"),
        )
        for name, action, phrase in mutations:
            expect_error(name, action, phrase)
            arms.append(name)

        nonempty = base / "nonempty"
        nonempty.mkdir()
        marker = nonempty / "keep.txt"
        marker.write_text("keep", encoding="utf-8")
        expect_error(
            "non-empty preservation",
            lambda: generate(root, nonempty, tool("nonempty-tool"), revision, known),
            "not empty")
        assert marker.read_text(encoding="utf-8") == "keep"
        arms.append("non-empty preservation")

        failed_target = base / "failed-publish"
        expect_error(
            "failed publication",
            lambda: generate(root, failed_target,
                             tool("failed-publish-tool", fail=True), revision, known),
            "failed with exit")
        assert not failed_target.exists()
        arms.append("failed publication")

        new_interface = root / "hdl" / "new_interface.sv"
        new_interface.write_text(
            "interface surprise_if; endinterface\n", encoding="utf-8")
        expect_error(
            "exception growth",
            lambda: source_census(root, known),
            "new exceptions")
        new_interface.unlink()
        arms.append("exception growth")

        interface = root / "hdl" / "bus.sv"
        original = interface.read_text(encoding="utf-8")
        interface.write_text(
            "interface renamed_if; endinterface\n", encoding="utf-8")
        expect_error(
            "changed exception",
            lambda: source_census(root, known),
            "changed exceptions")
        interface.write_text(original, encoding="utf-8")
        arms.append("changed exception")

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
