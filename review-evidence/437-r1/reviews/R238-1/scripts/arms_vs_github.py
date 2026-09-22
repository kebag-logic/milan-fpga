#!/usr/bin/env python3
"""[R238] the shipped I437 arms against GitHub's renderer.

Builds each shipped probe arm's exact page the way `container_arms()` does,
renders it (cached with the probes), and compares the arm's recorded
`visible` flag with whether GitHub renders `Old`; the five limitation pages
must render a heading the walk omits.
"""
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_render as probes  # noqa: E402

sys.modules["gen_toc"] = probes.HEAD
sys.path.insert(0, str(probes.SCRATCH / "clone-head" / "scripts"))
containers = importlib.import_module("gen_toc_container_cases")


def main() -> int:
    cache = probes.load_cache()
    lines, wrong = [], 0
    for name, prefix, tag, visible in containers.probe_rows():
        text = f"{prefix}\n<{tag}>\n## Old\n</{tag}>\n\n## Real\n"
        shown = [s for _, s in probes.rendered_headings(probes.render(text, cache)["response"])]
        ok = ("Old" in shown) == visible and "Real" in shown
        wrong += not ok
        lines.append(f"{'ok   ' if ok else 'WRONG'} I437 {name}: arm visible={visible}, "
                     f"GitHub {shown}")
    for name, text in [("equals setext", "Alpha\n===\n"), ("hyphen setext", "text\n---\n"),
                       ("single hyphen setext", "text\n-\n"), ("quoted heading", "> ## Q\n"),
                       ("list heading", "- item\n\n  ## Inner\n")]:
        shown = [s for _, s in probes.rendered_headings(probes.render(text, cache)["response"])]
        ok = bool(shown) and probes.HEAD.headings(text) == []
        wrong += not ok
        lines.append(f"{'ok   ' if ok else 'WRONG'} I437 limitation {name}: GitHub {shown}, "
                     f"walk {probes.HEAD.headings(text)}")
    lines.insert(0, f"{len(lines)} shipped I437 page arms, {wrong} disagree with GitHub")
    (probes.OUT / "receipts" / "arms-vs-github.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
