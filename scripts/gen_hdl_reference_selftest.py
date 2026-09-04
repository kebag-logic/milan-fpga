#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Fixture arms for ``scripts/gen_hdl_reference.py`` -- one arm per refusal.

This is the ``--selftest`` half of the HDL reference generator, kept beside it
rather than inside it: every arm builds its own throwaway source tree, and the
positive arm's document is the only thing any of them share.  Run them through
the generator, which is the only supported entry point:

    python3 scripts/gen_hdl_reference.py --selftest

``run_selftest()`` raises on the first arm that fails to refuse, so the
generator's own ``main`` turns it into the same ``REFUSED`` line and exit 2 a
failed generation produces; a clean run prints the arm count.

WHY THE ARMS PATCH ``reference`` AND NOT THIS MODULE.  Two arms replace a
function the generator calls internally (``run_process``, ``extract_file``).
The binding that has to change is the one ``generate`` and ``git_revision``
look up, which lives in the generator's namespace -- so the patches name the
generator module object, and ``gen_hdl_reference.main`` registers itself under
its import name before importing this file so that object is the running one
and not a second copy of it.
"""

import os
import re
import sys
import tempfile
import textwrap
from collections.abc import Callable, Sequence
from pathlib import Path
from types import ModuleType
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gen_hdl_reference as reference  # noqa: E402
from gen_hdl_reference import (  # noqa: E402
    DOCUMENT_TITLE,
    PRINT_STYLE,
    Content,
    DeclarationKey,
    GenerationError,
    declarations_in,
    diagram_marker,
    emit_document,
    extract_file,
    extract_reference,
    generate,
    git_revision,
    include_directories,
    load_parser,
    output_target,
    parse_file,
    source_census,
    svg_blocks,
    validate_html,
    validate_svg,
    verify_parser,
)


def fixture_tree(base: Path) -> tuple[Path, frozenset[DeclarationKey]]:
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


def expect_error(name: str, action: Callable[[], object], phrase: str) -> None:
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
    module = reference
    with mock.patch.object(module, "run_process", side_effect=outputs):
        git_revision(root)


def _missing_parser():
    """Import the parser while its module is unavailable."""
    with mock.patch.dict(sys.modules, {"pyslang": None}):
        load_parser()


def _disagreeing_extraction(root, target, revision, known):
    """Drop one extracted declaration behind the census's back."""
    module = reference
    original = extract_file

    def dropping(parser: ModuleType, tree_root: Path,
                 incdirs: Sequence[str], path: Path) -> tuple[Content, ...]:
        """Extract as usual, then hide `legacy` from the census check."""
        contents = original(parser, tree_root, incdirs, path)
        return tuple(item for item in contents
                     if item.declaration.name != "legacy")

    with mock.patch.object(module, "extract_file", dropping):
        generate(root, target, revision, known)


def _selftest_positive(arms, root, known, base, revision):
    """Positive generation: what a clean fixture tree's document must contain."""
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
    return census


def _selftest_source_refusals(rejects, root, base, known):
    """Refusals reached before a parser exists: the tree, and the parser pin."""
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


def _selftest_extraction_refusals(rejects, root, base, known, revision):
    """Refusals raised while extracting one file's declarations."""
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
    return parser


def _selftest_document_refusals(rejects, emitted, validates, revision, alpha_marker):
    """Refusals the emitted document's own validation raises."""
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


def _selftest_diagram_refusals(rejects, emitted, validates, alpha_marker):
    """Refusals the per-module diagram and section checks raise."""
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


def _selftest_output_refusals(rejects, root, base, known, revision):
    """Refusals about where the document may be published."""
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


def _selftest_census_refusals(rejects, root, base, known, revision):
    """Refusals about the source census and the HDL provenance."""
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


def run_selftest() -> None:
    """Exercise positive generation and independent refusal arms."""
    revision = "1" * 40
    arms = []
    with tempfile.TemporaryDirectory(prefix="hdl-reference-selftest-") as raw:
        base = Path(raw)
        root, known = fixture_tree(base)

        def rejects(name: str, action: Callable[[], object],
                    phrase: str) -> None:
            """Run one refusal arm and count it as covered."""
            expect_error(name, action, phrase)
            arms.append(name)

        census = _selftest_positive(arms, root, known, base, revision)
        _selftest_source_refusals(rejects, root, base, known)
        parser = _selftest_extraction_refusals(rejects, root, base, known, revision)

        contents, _ = extract_reference(parser, root, source_census(root, known))
        emitted = emit_document(contents, revision)

        def validates(document: str,
                      forbidden_paths: Sequence[Path] = ()) -> None:
            """Validate a mutated document against the real census."""
            return validate_html(document, census, revision, forbidden_paths)

        alpha_marker = diagram_marker("alpha")
        _selftest_document_refusals(
            rejects, emitted, validates, revision, alpha_marker)
        _selftest_diagram_refusals(rejects, emitted, validates, alpha_marker)
        _selftest_output_refusals(rejects, root, base, known, revision)
        _selftest_census_refusals(rejects, root, base, known, revision)

    print(f"HDL reference self-test: {len(arms)}/{len(arms)} arms passed")
