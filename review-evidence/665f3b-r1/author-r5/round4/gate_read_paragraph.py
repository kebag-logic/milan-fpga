"""Compare the policy page's gate-read paragraph with GATE_READ_DOCS.

The paragraph must link every registered page, link no other page under
docs/, and state no page count. Planted controls prove each refusal.
"""
import argparse
import ast
import posixpath
from pathlib import Path
import re

POLICY = "docs/testing/CI_WORKFLOWS.md"
OPENING = "pages under `docs/` are relevant because Python in a classifier-gated"
COUNT = re.compile(r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+pages\b", re.I)
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)\s]*)?\)")


def registered(source):
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "GATE_READ_DOCS" for t in node.targets):
            return [ast.literal_eval(item) for item in node.value.elts]
    raise SystemExit("GATE_READ_DOCS not found")


def paragraph(text):
    lines = text.splitlines()
    start = [n for n, line in enumerate(lines) if OPENING in line]
    if len(start) != 1:
        raise ValueError("opening sentence found %d times" % len(start))
    end = start[0]
    while end < len(lines) and lines[end].strip():
        end += 1
    return start[0] + 1, lines[start[0]:end]


def problems(text, pages):
    line, body = paragraph(text)
    found = []
    if COUNT.search(body[0]):
        found.append("line %d states a page count: %s" % (line, body[0].strip()))
    linked = set()
    for target in LINK.findall("\n".join(body)):
        path = posixpath.normpath(posixpath.join(posixpath.dirname(POLICY), target))
        if path.startswith("docs/") and path.endswith(".md"):
            linked.add(path)
    for path in sorted(set(pages) - linked):
        found.append("registered page not linked: " + path)
    for path in sorted(linked - set(pages)):
        found.append("linked page not registered: " + path)
    return line, sorted(linked), found


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repo", type=Path, required=True)
args = parser.parse_args()
text = (args.repo / POLICY).read_text()
pages = registered((args.repo / "scripts/ci_scope.py").read_text())
line, linked, found = problems(text, pages)
print("paragraph line", line, "registered", len(pages), "linked", len(linked))
for path in linked:
    print("  linked", path)
assert not found, found
print("live tree: OK")

opening = "These " + OPENING
controls = [
    ("restored stale count", text.replace(opening, "Seven " + OPENING), pages),
    ("correct count stated", text.replace(opening, "Eight " + OPENING), pages),
    ("digit count stated", text.replace(opening, "8 " + OPENING), pages),
    ("registered page unlinked", text.replace("[MAILBOX_SPLIT.md](../design/MAILBOX_SPLIT.md)", "MAILBOX_SPLIT.md"), pages),
    ("extra registration", text, pages + ["docs/design/NOT_A_READ_PAGE.md"]),
    ("registration removed", text, [p for p in pages if p != "docs/design/MAILBOX_SPLIT.md"]),
]
for name, mutated, mutated_pages in controls:
    assert mutated != text or mutated_pages != pages, name + ": mutation not applied"
    result = problems(mutated, mutated_pages)[2]
    print("control", name, "->", "refused" if result else "ACCEPTED", result)
    assert result, name + " escaped"
print("gate-read paragraph controls: %d/%d refused" % (len(controls), len(controls)))
