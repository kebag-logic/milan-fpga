#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The #437 and #516 shape set and GitHub's recorded rendering of each.

WHAT THE FIXTURE IS. `gen_toc_shapes.json` holds every page the two issues
are judged on. Acceptance 1 of #437 (as restated and amended on 2026-09-23)
names family one: a list item's paragraph resumed after a blank line, at
and past the item's content column, for bullet, ordered and two-digit
ordered items, followed by an inline and an unknown tag, with the nine
publicly described R86-5 shapes mapped (`r86_5`) and the boundaries that
already agreed. The set also carries the twelve unclosed-comment variants
of #516, every page the reviews on PR #515 published (R237-1 to R237-4 and
R238-1 to R238-3, `reconstructed` where a review gave a description and
not the bytes), the five family-two headings, the page of every case-table
arm the renderer answers differently from the old walk, and a synthetic
reproduction of every class of tracked-page difference. Each page was sent
to GitHub's Markdown API (`POST /markdown`, mode `gfm`) with `gh api`; the
exact request and response bytes, their SHA-256 and the UTC time are kept.

WHAT AN ARM HOLDS. For each shape, one arm checks the receipt: both hashes,
and that the request asked for exactly this page in `gfm` mode. A second
arm renders the page with the pinned renderer and requires the headings
`gen_toc.headings()` lists to be the headings GitHub rendered, by level and
text, in order, read from the recorded response with the same HTML parser.
That is acceptance 1 by construction: the committed set, checked against
the parser's output and against GitHub's recorded rendering at once. A
disagreement fails an arm. The one measured disagreement is written into
each shape it touches as `github_only`, with its reason, and an arm spells
it: GitHub opens a referenced footnote's section with a visually hidden
heading that the pinned cmark-gfm does not emit. Any other disagreement
fails.

THE FILE VIEW. That arm compares the text of whichever element carries a
heading's position, so a page that forged the position on an element of
its own agreed while the walk listed a label GitHub never shows (R238-4 F1
on PR #538). The fixture's `file_view` pages are recorded in the API's
`markdown` mode, the view GitHub gives a repository file, whose headings
carry their anchors. For each one an arm requires every heading
`gen_toc.headings()` lists, its text as a reader sees it and its anchor, to
be one GitHub shows, in order. They are the pages the walk withholds by
design, which the arm above cannot hold: the position attribute in each
spelling, and pages nested past the depth GitHub renders.

`em_dash_arms()` runs every shape that carries one `## Old` heading, and
every file-view page that carries one `## Old <em dash> heading`, through
the shipped em-dash gate on real Git commits, the consumer that decides an
exemption from these headings. Only data lives here: this module holds no
Markdown rule and imports no expression engine (`gen_toc._owner_guards`).
"""
import hashlib
import json
import tempfile
from pathlib import Path
from types import ModuleType

from gen_toc import headings, refusals, rendered_headings, strip_md
from gen_toc_renderer import anchored_headings_of, headings_of
from gen_toc_renderer_cases import FORGED

SHAPES = Path(__file__).resolve().with_name("gen_toc_shapes.json")
#: What every recorded request asked for, besides its page.
CONTEXT, MODE = "kebag-logic/milan-fpga", "gfm"
#: The mode of GitHub's file view, which the `file_view` pages were sent in.
FILE_VIEW = "markdown"
_HIDDEN_OLD = "\n## Old \u2014 heading\n"
#: Acceptance 1's family-one grid, spelled here and not read from the
#: fixture: every marker at and past its content column, each tag outside
#: and inside the item, and the boundaries that already agreed.
_MARKERS = ("bullet", "star", "ordered", "two-digit ordered")
_BOUNDARIES = ("one space", "four spaces", "block quote",
               "footnote definition two spaces",
               "footnote definition four spaces", "tab")


def load(part: str = "shapes") -> list[dict]:
    """Every recorded shape, or with `file_view` every page recorded in
    the file view, in the fixture's order."""
    return json.loads(SHAPES.read_text(encoding="utf-8"))[part]


def _sha256(data: bytes) -> str:
    """The hex SHA-256 of some bytes."""
    return hashlib.sha256(data).hexdigest()


def receipt_holds(shape: dict, mode: str = MODE) -> bool:
    """Whether a recorded rendering is what it says: both hashes match the
    bytes, the request asked for exactly this page in `mode` with this
    repository's context, and the headings written beside it are the ones
    the response carries, with their anchors in the file view."""
    request = shape["request_bytes"].encode("utf-8")
    response = shape["response_bytes"].encode("utf-8")
    read = anchored_headings_of if mode == FILE_VIEW else headings_of
    return (_sha256(request) == shape["request_sha256"]
            and _sha256(response) == shape["response_sha256"]
            and json.loads(request) == {"context": CONTEXT, "mode": mode,
                                        "text": shape["page"]}
            and [list(h) for h in read(shape["response_bytes"])]
            == shape["headings"])


def shown_in_file_view(text: str, shown: list[list]) -> bool:
    """Whether every heading `headings()` lists for a page is one of the
    headings its file view `shown`, in the same order: the same level, the
    text a reader sees (`strip_md`, blanks collapsed) and the same anchor.
    The walk may leave a heading out, which withholds; it may not list one
    GitHub does not show, or give one another anchor. A walk that runs out
    of stack on the page answers no."""
    rest = iter(tuple(heading) for heading in shown)
    try:
        return all((level, " ".join(strip_md(raw).split()), anchor) in rest
                   for level, raw, anchor in headings(text))
    except RecursionError:
        return False


def _coverage(shapes: list[dict]) -> list[tuple[str, str, object]]:
    """Arms over the set as a whole: what acceptance 1 and #516 name is
    in it, spelled here so that dropping a shape fails an arm."""
    names = {shape["name"] for shape in shapes}
    grid = [f"{marker} {where} column, {tag} tag {side}"
            for marker in _MARKERS for where in ("at", "past")
            for tag in ("inline", "unknown") for side in ("outside", "inside")]
    variants = [f"#516 {para} tag column {col} {form}"
                for para in ("first", "resumed") for col in (0, 1)
                for form in ("open", "close", "attribute")]
    mapped = [shape["r86_5"] for shape in shapes if shape.get("r86_5")]
    return [
        ("I437 family one covers every marker at and past its column, each "
         "tag outside and inside", "",
         lambda t: all(name in names for name in grid)),
        ("I437 family one covers the two-digit marker below its column", "",
         lambda t: {"two-digit ordered below column, inline tag outside",
                    "two-digit ordered below column, unknown tag outside"}
         <= names),
        ("I437 family one covers the boundaries that already agreed", "",
         lambda t: all(f"boundary {b}, {tag} tag" in names
                       for b in _BOUNDARIES for tag in ("inline", "unknown"))),
        ("I437 the nine R86-5 descriptions map to nine named shapes", "",
         lambda t: len(mapped) == len(set(mapped)) == 9),
        ("I437 the twelve #516 variants are in the set", "",
         lambda t: all(name in names for name in variants)),
        ("I437 every shape's name is its own", "",
         lambda t: len(names) == len(shapes)),
        ("I437 the one heading GitHub renders that the pinned renderer "
         "does not is its hidden footnote label, on the two shapes that "
         "reference a footnote", "",
         lambda t: [shape.get("github_only", {}).get("headings")
                    for shape in shapes if shape.get("github_only")]
         == [[[2, "Footnotes"]]] * 2),
    ]


def _view_coverage(views: list[dict]) -> list[tuple[str, str, object]]:
    """What the file view must carry, spelled here: the position attribute
    in every spelling the renderer's arms forge, and a page nested past
    GitHub's depth, whose file view drops a heading the walk would list."""
    pages = {view["page"] for view in views}
    return [
        ("I437 the file-view check refuses a heading the file view does "
         "not show, or shows with another text or anchor", "",
         lambda t: shown_in_file_view("## A\n", [[2, "A", "a"]])
         and not any(shown_in_file_view("## A\n", shown) for shown in (
             [], [[2, "B", "a"]], [[2, "A", "b"]], [[3, "A", "a"]]))),
        ("I437 the file view carries every forged spelling of the position "
         "attribute", "", lambda t: set(FORGED.values()) <= pages),
        ("I437 the file view carries a page GitHub cuts short by depth", "",
         lambda t: any(len(view["headings"]) == 1 and "## B\n" in view["page"]
                       for view in views)),
    ]


def shape_arms() -> list[tuple[str, str, object]]:
    """Two arms per recorded shape, two per file-view page, then the
    coverage arms of each."""
    shapes, views = load(), load("file_view")
    arms = []
    for shape in shapes:
        want = [tuple(h) for h in shape["headings"]]
        for extra in shape.get("github_only", {}).get("headings", []):
            want.remove(tuple(extra))
        arms.append((f"I437 receipt: {shape['name']}", shape["page"],
                     lambda t, s=shape: receipt_holds(s)))
        arms.append((f"I437 renders as GitHub does: {shape['name']}",
                     shape["page"],
                     lambda t, w=want: rendered_headings(t) == w))
    for view in views:
        arms.append((f"I437 file-view receipt: {view['name']}", view["page"],
                     lambda t, v=view: receipt_holds(v, FILE_VIEW)))
        arms.append((f"I437 lists only what the file view shows, label and "
                     f"anchor: {view['name']}", view["page"],
                     lambda t, v=view: shown_in_file_view(t, v["headings"])))
    return arms + _coverage(shapes) + _view_coverage(views)


def em_dash_rows() -> list[tuple[str, str, bool]]:
    """(name, base page, GitHub rendered it) for every shape carrying one
    `## Old` line and no other `Old`, that line taking an em dash, and for
    every file-view page carrying one `## Old <em dash> heading` as it is:
    whether GitHub rendered that heading decides whether a label copied
    from it may be exempt. The file view says so by its anchor."""
    rows = []
    for shape in load():
        page = shape["page"]
        if page.count("Old") != 1 or "\n## Old\n" not in "\n" + page:
            continue
        base = ("\n" + page).replace("\n## Old\n", _HIDDEN_OLD)[1:]
        rows.append((shape["name"], base, [2, "Old"] in shape["headings"]))
    for view in load("file_view"):
        page = view["page"]
        if page.count("Old") == 1 and _HIDDEN_OLD in "\n" + page:
            rows.append((f"file view: {view['name']}", page,
                         any(anchor == "old--heading"
                             for _, _, anchor in view["headings"])))
    return rows


def em_dash_arms(gate: ModuleType) -> tuple[list[str], int]:
    """Every `em_dash_rows()` page through the shipped gate, on real base
    and head commits. The head page carries a valid generated Contents
    block copying `Old <em dash> heading`, so the exemption is really
    asked: it holds exactly when GitHub rendered that heading at the base,
    and a base page the walk refuses exempts nothing."""
    rows, problems = em_dash_rows(), []
    heading = "## Old \u2014 heading\n"
    tail = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"
    navigation = ("## Contents\n\n"
                  "- **[Old \u2014 heading](#old--heading)** -- Copied.\n"
                  "- **[Alpha](#alpha)** -- What alpha holds.\n"
                  "- **[Beta](#beta)** -- What beta holds.\n"
                  "- **[Gamma](#gamma)** -- What gamma holds.\n\n")
    with tempfile.TemporaryDirectory(prefix="i437.emdash.") as tmp:
        repo = Path(tmp)
        gate._fixture_git(repo, "init", "-q", "--initial-branch=main")
        for index, (_, base, _) in enumerate(rows):
            (repo / f"s{index:03d}.md").write_bytes(base.encode("utf-8"))
        base_commit = gate._commit(repo, "I437 base")
        for index in range(len(rows)):
            (repo / f"s{index:03d}.md").write_text(
                "# Page\n\n" + navigation + heading + tail, encoding="utf-8")
        gate._commit(repo, "I437 head")
        for index, (name, base, rendered) in enumerate(rows):
            refused = bool(refusals(base))
            # (label refused, base refusal named, labels exempt)
            want = (not rendered or refused, refused,
                    int(rendered and not refused))
            verdict = gate.Verdict()
            path = f"s{index:03d}.md"
            gate.judge_page(repo, base_commit, gate.Change(path, path), verdict)
            # Only the label decision is scored: the heading line itself is
            # added or kept as Git's diff pairs it, which no rule here owns.
            got = (any("mirrors no heading" in note
                       for note in verdict.findings),
                   any("at column" in note for note in verdict.findings),
                   verdict.exempt)
            if got != want:
                problems.append(f"[I437 em dash: {name}] label refused, base "
                                f"refusal named, exempt: expected {want}, "
                                f"got {got}: {verdict.findings}")
    return problems, len(rows)
