#!/usr/bin/env python3
"""Reviewer probe (R238-5): forged position spellings and depth pages.

Usage: python probe_forge_e2e.py <repo-root>

For each base page, reports:
  - headings() as the walk lists them, and refusals() count;
  - the shipped em-dash gate's answer on real Git commits when the head page
    carries a generated Contents block copying `Old <em dash> heading`:
    (label refused, base refusal named, exempt count).
Every base page below hides `## Old <em dash> heading` from GitHub (an open
raw comment, an open quoted value, or depth of 256 or more), except the
CONTROL rows, where GitHub shows it and the exemption must hold, and the
MARGIN rows (depth 201 to 255), where GitHub shows it but the documented
depth limit withholds it: those must exempt nothing (withhold only).
"""
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "scripts"))
import check_em_dash as gate  # noqa: E402
from gen_toc import headings, refusals  # noqa: E402
from gen_toc_renderer import render  # noqa: E402

DASH = "—"
SECTIONS = ("# Page\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\n"
            "Body.\n\n")
HIDDEN = f"<span>\n<!--\n\n## Old {DASH} heading\n</span>\n"


def hidden_pos(prefix: str) -> str:
    """The position cmark-gfm gives the Old heading in SECTIONS+prefix+HIDDEN,
    found by rendering the page with the forging element neutralised."""
    lines = (SECTIONS + prefix + HIDDEN).split("\n")
    n = next(i for i, l in enumerate(lines, 1) if l.startswith("## Old"))
    return f"{n}:1-{n}:{len(f'## Old {DASH} heading'.encode())}"


def forged(tag_line: str) -> str:
    pos = hidden_pos(tag_line.replace("@P@", "0:0-0:0"))
    return SECTIONS + tag_line.replace("@P@", pos) + HIDDEN


ROWS = []
# Raw tag spellings, every letter-case pattern tried plus tag-name case.
for spelled in ("DATA-SOURCEPOS", "Data-Sourcepos", "dAtA-sOuRcEpOs",
                "data-sourcePOS", "DATA-sourcepos"):
    for tag in ("h2", "H2"):
        ROWS.append((f"raw <{tag} {spelled}>", forged(
            f'<{tag} {spelled}="@P@">x</{tag}>\n\n'), False))
# Unquoted and single-quoted attribute value.
ROWS.append(("raw unquoted value upper", forged(
    "<h2 DATA-SOURCEPOS=@P@>x</h2>\n\n"), False))
ROWS.append(("raw single-quoted value mixed", forged(
    "<h2 Data-SourcePos='@P@'>x</h2>\n\n"), False))
# Inline raw tag inside a paragraph.
ROWS.append(("inline raw tag upper in a paragraph", forged(
    'text <h2 DATA-SOURCEPOS="@P@">x</h2> more\n\n'), False))
# Text spellings read as attributes of a raw tag left open in a quoted value.
for how, word in (("decimal reference", "&#100;ata-sourcepos"),
                  ("hex reference upper X", "&#X44;ata-sourcepos"),
                  ("hex reference lower", "&#x64;ata-sourcepos"),
                  ("reference mid-word", "data-sour&#99;epos"),
                  ("backslash escape", "data\\-sourcepos"),
                  ("upper text", "DATA-SOURCEPOS"),
                  ("reference, upper rest", "&#68;ATA-SOURCEPOS")):
    ROWS.append((f"text via {how}", forged(
        f"<h2 title='\n\nz' {word}=@P@ y\n\n"), False))
# Depth: the heading after a nest GitHub cuts short, and controls just inside.
OLD = f"## Old {DASH} heading\n"
ROWS += [
    ("MARGIN depth 201 block quotes then Old", "# Page\n\n" + ">" * 200 + " x\n\n"
     + SECTIONS[8:] + OLD, "margin"),
    ("depth 256 block quotes then Old", "# Page\n\n" + ">" * 255 + " x\n\n"
     + SECTIONS[8:] + OLD, False),
    ("MARGIN depth 101 list levels then Old", "# Page\n\n" + "".join(
        "  " * i + "- a\n" for i in range(101)) + "\n" + SECTIONS[8:] + OLD,
     "margin"),
    ("depth 129 list levels then Old", "# Page\n\n" + "".join(
        "  " * i + "- a\n" for i in range(129)) + "\n" + SECTIONS[8:] + OLD,
     False),
    ("MARGIN depth 201 raw divs then Old", "# Page\n\n" + "<div>" * 201 + "\n\n"
     + SECTIONS[8:] + OLD, "margin"),
    ("depth 1500 block quotes then Old", "# Page\n\n" + ">" * 1500 + " x\n\n"
     + SECTIONS[8:] + OLD, False),
    ("CONTROL depth 200 block quotes then Old", "# Page\n\n" + ">" * 199
     + " x\n\n" + SECTIONS[8:] + OLD, True),
    ("CONTROL 199 raw divs, headings inside at depth 200", "# Page\n\n"
     + "<div>" * 199 + "\n\n" + SECTIONS[8:] + OLD, True),
    ("MARGIN 200 raw divs, headings inside at depth 201 (GitHub shows; the "
     "documented depth limit withholds)", "# Page\n\n" + "<div>" * 200
     + "\n\n" + SECTIONS[8:] + OLD, "margin"),
    ("CONTROL plain page with Old", SECTIONS + OLD, True),
    # A raw attribute name spelled with a reference is NOT the attribute:
    # HTML decodes no reference in a name, so the page is read normally.
    ("CONTROL raw reference in a tag's name is no forge",
     SECTIONS + '<h2 &#100;ata-sourcepos="1:1-1:1">x</h2>\n\n' + OLD, True),
]


def main() -> int:
    heading = f"## Old {DASH} heading\n"
    tail = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"
    nav = ("## Contents\n\n"
           f"- **[Old {DASH} heading](#old--heading)** -- Copied.\n"
           "- **[Alpha](#alpha)** -- What alpha holds.\n"
           "- **[Beta](#beta)** -- What beta holds.\n"
           "- **[Gamma](#gamma)** -- What gamma holds.\n\n")
    bad = 0
    with tempfile.TemporaryDirectory(prefix="r238.forge.") as tmp:
        repo = Path(tmp)
        gate._fixture_git(repo, "init", "-q", "--initial-branch=main")
        for i, (_, base, _) in enumerate(ROWS):
            (repo / f"p{i:02d}.md").write_text(base, encoding="utf-8")
        base_commit = gate._commit(repo, "base")
        for i in range(len(ROWS)):
            (repo / f"p{i:02d}.md").write_text("# Page\n\n" + nav + heading
                                               + tail, encoding="utf-8")
        gate._commit(repo, "head")
        for i, (name, base, shown) in enumerate(ROWS):
            listed = [(r, a) for _, r, a in headings(base)]
            old_listed = any(a == "old--heading" for _, a in listed)
            ref = len(refusals(base))
            verdict = gate.Verdict()
            path = f"p{i:02d}.md"
            gate.judge_page(repo, base_commit, gate.Change(path, path), verdict)
            refused = any("mirrors no heading" in f for f in verdict.findings)
            named = any("at column" in f for f in verdict.findings)
            if shown is True:
                ok = verdict.exempt == 1 and not refused and old_listed
            else:  # hidden by GitHub, or withheld by a documented limit
                ok = verdict.exempt == 0 and refused and not old_listed
            bad += not ok
            print(f"{'OK  ' if ok else 'FAIL'} {name}: GitHub shows Old="
                  f"{shown}; walk lists Old={old_listed}; headings="
                  f"{len(listed)}; refusals={ref}; gate: label refused="
                  f"{refused}, base refusal named={named}, exempt="
                  f"{verdict.exempt}")
    print(f"probe_forge_e2e: {len(ROWS) - bad}/{len(ROWS)} as expected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
