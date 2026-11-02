"""Run check_doc_style.analyze() over one page at two commits and report findings
on the lines the second commit changed, plus a planted control that must be caught.

Usage: python3 -I style_delta_probe.py <repo> <base> <head> <page>
"""
import importlib.util, subprocess, sys

repo, base, head, page = sys.argv[1:5]
spec = importlib.util.spec_from_file_location("cds", f"{repo}/scripts/check_doc_style.py")
cds = importlib.util.module_from_spec(spec)
sys.modules["cds"] = cds
spec.loader.exec_module(cds)

def show(rev):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{page}"],
                          capture_output=True, text=True, check=True).stdout

diff = subprocess.run(["git", "-C", repo, "diff", "-U0", base, head, "--", page],
                      capture_output=True, text=True, check=True).stdout
changed = set()
for line in diff.splitlines():
    if line.startswith("@@"):
        plus = line.split("+")[1].split(" ")[0]
        start, _, n = plus.partition(",")
        n = int(n) if n else 1
        changed.update(range(int(start), int(start) + n))
print("changed lines at head:", sorted(changed))
text = show(head)
lines = text.splitlines()
blocks = cds.prose_blocks(text)
def owner(ln):
    """First line of the prose block holding line ln, or None for a table row."""
    starts = {b.line for b in blocks}
    i = ln
    while i >= 1 and lines[i - 1].strip():
        if i in starts:
            return i
        i -= 1
    return None
owners = {}
for ln in sorted(changed):
    o = owner(ln)
    owners[ln] = o
    print(f"line {ln}: {'prose block from line %d' % o if o else 'not prose (table row)'}")
keys = {o for o in owners.values() if o}
hits = [f for f in cds.analyze(text) if f.line in keys or f.line in changed]
print("findings on changed blocks at head:", len(hits))
for f in hits:
    print("  ", f.line, f.reason, f.text[:120])
base_all = len(cds.analyze(show(base)))
head_all = len(cds.analyze(text))
print(f"whole-page findings: base {base_all}, head {head_all}")
# control: plant an over-long sentence at line 368's paragraph
planted = lines[:]
idx = 367
planted[idx] = "Taking ten milliseconds as the gap between two polls gives a buffer of 128 bytes."
ctl = [f for f in cds.analyze("\n".join(planted) + "\n") if f.line == owners[368]]
print("control planted at 368 caught:", bool(ctl), [c.reason for c in ctl])
