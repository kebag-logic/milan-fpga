"""List every in-page anchor link in a Markdown page whose target heading does not exist (GitHub slug rules, simplified)."""
import re, sys
page = sys.argv[1]
text = open(page, encoding="utf-8").read()
slugs = set()
for h in re.findall(r"^#{1,6}\s+(.*)$", text, re.M):
    s = re.sub(r"[^\w\- ]", "", h.strip().lower().replace("`", "")).replace(" ", "-")
    slugs.add(s)
bad = [(n + 1, a) for n, line in enumerate(text.splitlines()) for a in re.findall(r"\]\(#([^)]+)\)", line) if a not in slugs]
for b in bad:
    print("missing anchor", page, *b)
print("checked", page, "anchors-missing", len(bad))
sys.exit(1 if bad else 0)
