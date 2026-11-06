#!/usr/bin/env python3
"""For each page a 20-line insertion moved: what changed, and the smallest insertion at the top that moves it.

Usage: top20_explain_r787.py REPO PROBE_RECEIPT OUT
"""
import importlib.util, re, sys
from pathlib import Path
repo, receipt, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
spec = importlib.util.spec_from_file_location("inv", repo / "scripts/docs_inventory.py")
mod = importlib.util.module_from_spec(spec); sys.modules["inv"] = mod; spec.loader.exec_module(mod)
pages = [m.group(1) for m in re.finditer(r"^top20 \| (\S+) \| rc=1", receipt.read_text(), re.M)]
tree = mod.listing(repo)
lines = []
for page in sorted(pages):
    text = (repo / page).read_text(errors="replace")
    def view(t):
        return mod.audience_of(t, page), mod.status(t, page, {})
    base = view(text)
    margin = next(n for n in range(1, 40) if view("\n" * n + text) != base)
    new = view("\n" * margin + text)
    field = "audience" if new[0] != base[0] else "status"
    lines.append(f"{page} | margin {margin} | {field}: {base[0] if field == 'audience' else base[1]} -> {new[0] if field == 'audience' else new[1]}")
lines.append(f"pages {len(pages)}; smallest margin {min(int(re.search(r'margin (\d+)', l).group(1)) for l in lines)}")
Path(out).write_text("\n".join(lines) + "\n"); print("\n".join(lines))
