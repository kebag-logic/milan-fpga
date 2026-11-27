"""repoint_anchors.py <checkout> <old-rev>: move each Markdown source anchor (#Ln or #Ln-Lm) to the line its target
line moved to between <old-rev> and the working tree, by a line alignment of the two files. Fails if a target line
was itself changed."""
import difflib
import re
import subprocess
import sys
from pathlib import Path

root, old_rev = Path(sys.argv[1]), sys.argv[2]
ANCHOR = re.compile(r"\((?P<pre>(?:\.\./)*)(?P<path>src/[^)#\s]+)#L(?P<a>\d+)(?:-L(?P<b>\d+))?\)")
maps = {}


def line_map(path):
    if path not in maps:
        old = subprocess.run(["git", "-C", str(root), "show", f"{old_rev}:{path}"], capture_output=True, text=True,
                             check=True).stdout.splitlines()
        new = (root / path).read_text().splitlines()
        m = {}
        for block in difflib.SequenceMatcher(None, old, new, autojunk=False).get_matching_blocks():
            for k in range(block.size):
                m[block.a + k + 1] = block.b + k + 1
        maps[path] = m
    return maps[path]


moved = 0
pages = sorted(set(root.glob("*.md")) | set((root / "doc").rglob("*.md")))
for page in pages:
    text = page.read_text()

    def fix(match):
        global moved
        m = line_map(match["path"])
        a = int(match["a"])
        if a not in m:
            raise SystemExit(f"{page}: {match.group(0)}: its target line changed")
        out = f"({match['pre']}{match['path']}#L{m[a]}"
        if match["b"]:
            b = int(match["b"])
            if b not in m:
                raise SystemExit(f"{page}: {match.group(0)}: its range end changed")
            out += f"-L{m[b]}"
        out += ")"
        moved += out != match.group(0)
        return out

    new_text = ANCHOR.sub(fix, text)
    if new_text != text:
        page.write_text(new_text)
print(f"anchors moved: {moved}")
