#!/usr/bin/env python3
"""[R238] the navigation consumer on the F1 and F2 escape shapes.

For each page, `apply()` writes the Contents block under the base walk and
under the head walk; GitHub's renderer (cached with the probes) says which
headings the page really has. An entry whose anchor GitHub renders no
heading for is a dead link in generated navigation.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_render as probes  # noqa: E402

# The probe sits AFTER the sections: under the head walk the renderer's
# closing fence of C04/D03 is an opening fence, which would otherwise swallow
# every later section of the page.
HEAD_OF_PAGE = "# Page\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n"
PAGES = {
    "C04": HEAD_OF_PAGE + "- item\n\n  text\n  <span>\n```\n\n## Old\n```\n",
    "D03": HEAD_OF_PAGE + "- item\n> quote\n\n  text\n<span>\n```\n\n## Old\n```\n",
    "C01": HEAD_OF_PAGE + "- item\n\n  text\n  <span>\n## Old\n  </span>\n",
}


def entries(walk, text: str) -> list[str]:
    new = walk.apply(Path("page.md"), text)
    lines = (new or text).split("\n")
    return [l for l in lines if l.startswith("- **[")]


def main() -> int:
    cache = probes.load_cache()
    out = []
    for key, text in PAGES.items():
        shown = [s for _, s in probes.rendered_headings(probes.render(text, cache)["response"])]
        out.append(f"{key}: GitHub headings {shown}")
        for name, walk in (("base", probes.BASE), ("head", probes.HEAD)):
            out.append(f"  {name} Contents: {entries(walk, text)}")
    (probes.OUT / "receipts" / "navigation-consumer.txt").write_text("\n".join(out) + "\n")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
