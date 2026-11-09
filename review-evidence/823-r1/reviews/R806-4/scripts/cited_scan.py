"""List the page's prose citations of the form `token` in `path`, and whether the drift gate grades each."""
import re, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "scripts"))
import nvm_format_32x32_tables as t
page = (root / "docs/design/SAVED_STATE_FORMAT_32X32.md").read_text()
graded = {(a.token, t.shown(a.where)) for a in t.LAYERS + t.VERSION_CHAIN + t.CITED}
for m in re.finditer(r"`([^`\n]+)` in `([\w./-]+\.\w+)`", page):
    tok, path = m.group(1), m.group(2)
    f = root / path
    n = sum(tok in line for line in f.read_text().splitlines()) if f.exists() else -1
    print(f"{'GRADED' if (tok, path) in graded else 'UNGRADED'}\tlines={n}\t{path}\t{tok}")
