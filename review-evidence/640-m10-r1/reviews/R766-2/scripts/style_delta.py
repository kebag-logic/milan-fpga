"""Run check_doc_style.analyze() on a page at two commits and print the head's
findings that the base does not have (the delta's new style findings).
Usage: python3 -I style_delta.py <repo> <base> <head> <page>..."""
import subprocess, sys
repo, base, head, pages = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
sys.path.insert(0, f"{repo}/scripts")
import check_doc_style as s
def show(rev, page):
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{page}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""
total = 0
for page in pages:
    old = {(f.reason, f.text) for f in s.analyze(show(base, page))}
    new = [f for f in s.analyze(show(head, page)) if (f.reason, f.text) not in old]
    print(f"{page}: base findings {len(old)}, head-only findings {len(new)}")
    for f in new: print(f"  {page}:{f.line}: {f.reason}: {f.text[:160]}")
    total += len(new)
print("TOTAL head-only findings", total)
