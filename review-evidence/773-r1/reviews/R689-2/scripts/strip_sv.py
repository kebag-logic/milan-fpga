"""Compare a SystemVerilog file at two revisions after removing comments (string-literal aware).
usage: python3 -I strip_sv.py <repo> <rev-a> <rev-b> <path>   exit 0 iff the stripped texts are identical"""
import hashlib, re, subprocess, sys
repo, a, b, path = sys.argv[1:5]
TOK = re.compile(r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*.*?\*/', re.S)
def strip(t):
    t = TOK.sub(lambda m: m.group(0) if m.group(0).startswith('"') else (" " if m.group(0).startswith("/*") else ""), t)
    return "\n".join(l.rstrip() for l in t.splitlines() if l.strip())
out = {}
for r in (a, b):
    raw = subprocess.run(["git", "-C", repo, "show", f"{r}:{path}"], check=True, capture_output=True, text=True).stdout
    out[r] = (hashlib.sha256(raw.encode()).hexdigest(), hashlib.sha256(strip(raw).encode()).hexdigest())
    print(f"{r} raw {out[r][0][:16]} stripped {out[r][1][:16]}")
same = out[a][1] == out[b][1]
print(f"raw {'IDENTICAL' if out[a][0] == out[b][0] else 'DIFFERENT'}; comments stripped {'IDENTICAL' if same else 'DIFFERENT'}")
sys.exit(0 if same else 1)
