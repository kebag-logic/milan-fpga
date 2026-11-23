"""Run ctrl_boundary's figure check and figure controls on a checkout's README for a given pin-control count.

Usage: python3 -I check_figures.py <checkout-root> <pin-controls>
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_boundary as cb  # noqa: E402

assert cb.ROOT.resolve() == root, (cb.ROOT, root)
page = cb.README.read_text(encoding="utf-8")
counts = cb.population(int(sys.argv[2]))
for what, sentence in cb.FIGURES:
    print(f"FIGURE {what}: page {sentence.findall(page)} self-test {counts[what]}")
found = cb.figures(page, counts)
bad, n = cb.figure_controls(page, counts)
print(f"figure findings={len(found)} {found}; figure controls={n} misbehaved={bad}")
print("FIGURES", "PASS" if not found and not bad else "FAIL")
sys.exit(1 if found or bad else 0)
