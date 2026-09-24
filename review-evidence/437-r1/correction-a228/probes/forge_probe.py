"""Probe: can a page make the HTML parse read the renderer's position
attribute on an element it wrote, without spelling the attribute in
lower case?  Usage: forge_probe.py <repo>"""
import sys
sys.path.insert(0, sys.argv[1] + "/scripts")
import gen_toc as g
import gen_toc_renderer as r

EM = "—"
HIDDEN = f"<span>\n<!--\n\n## Old {EM} heading\n</span>\n"
SECTIONS = "## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n\n"


def old_position(draft):
    lines = draft.split("\n")
    return next(n.position for n in r.render(draft).nodes
                if n.kind == "heading" and "Old" in lines[n.first - 1])


def forged(spell):
    """A raw h2 carrying the hidden heading's position, the attribute
    written by `spell(position)`."""
    draft = f"# Page\n\n{SECTIONS}FORGE\n\n{HIDDEN}"
    # Aim with the attribute spelled harmlessly, so every line keeps its
    # place, then spell it as the case does.
    probe = draft.replace("FORGE", spell("0:0-0:0").replace("sourcepos", "xourcepos")
                          .replace("SOURCEPOS", "XOURCEPOS").replace("SourcePos", "XourcePos"))
    return draft.replace("FORGE", spell(old_position(probe)))


CASES = {
    "control": lambda p: "Plain.",
    "lower (guarded)": lambda p: f'<h2 data-sourcepos="{p}">x</h2>',
    "upper": lambda p: f'<h2 DATA-SOURCEPOS="{p}">x</h2>',
    "mixed": lambda p: f'<h2 Data-SourcePos="{p}">x</h2>',
    # A raw h2 left open in a single-quoted value; the paragraph closes the
    # quote and spells the attribute through a character reference.
    "charref in text": lambda p: f"<h2 title='\n\nz' &#100;ata-sourcepos={p} y",
    "backslash in text": lambda p: f"<h2 title='\n\nz' data\\-sourcepos={p} y",
}

for name, spell in CASES.items():
    page = forged(spell)
    if "-v" in sys.argv:
        print(repr(page))
    got = [(lvl, raw) for lvl, raw, _ in g.headings(page)]
    print(f"{name:22} lower-case in text: {r.POSITION in page!s:5} "
          f"lists Old: {any('Old' in raw for _, raw in got)!s:5} {got}")
