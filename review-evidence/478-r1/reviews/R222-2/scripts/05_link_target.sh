#!/usr/bin/env bash
# The corrected row-8 link target at the head: it must name the repository the
# protocol-processor gitlink comes from, the exact gitlink commit, the L10
# document at that commit, and a fragment that is the (unique) GitHub anchor of
# the section holding L10. Then confirm what a reader actually gets from
# GitHub, unauthenticated, including a byte comparison of the served raw file
# with the pinned blob. Read-only; network reads only to public github.com.
set -uo pipefail
R=$VALIDATION_STORAGE/reviews/r222-478-r2
S=${SCRATCH:-/tmp/r222-478-r2-scratch}
HEAD_C=1496558d82cf35fc98dda0e781b2a1be643c301a
P="$S/git-sub/protocol-processor"
DOC=docs/ENDSTATION_BUILDER.md

url=$(git -C "$R" show "$HEAD_C:$DOC" | sed -n '963p' | grep -oE '\(https://github\.com/[^)]*07_memory_maps\.md#[^)]*\)' | tr -d '()')
echo "row-8 link (line 963): $url"
pin=$(git -C "$R" ls-tree "$HEAD_C" protocol-processor | awk '{print $3}')
sub_url=$(git -C "$R" config -f <(git -C "$R" show "$HEAD_C:.gitmodules") submodule.protocol-processor.url)
echo "gitlink: $pin"
echo ".gitmodules url: $sub_url"
python3 - "$url" "$pin" "$sub_url" <<'PY'
import re, sys
url, pin, sub = sys.argv[1:]
m = re.fullmatch(r"https://github\.com/([^/]+)/([^/]+)/blob/([0-9a-f]{40})/(.+?)#(.+)", url)
assert m, "unexpected URL shape"
owner, repo, sha, path, frag = m.groups()
sm = re.fullmatch(r"https://github\.com/([^/]+)/(.+?)(?:\.git)?", sub)
print(f"owner/repo in link = {owner}/{repo}; in .gitmodules = {sm.group(1)}/{sm.group(2)}; same = {(owner, repo) == sm.groups()}")
print(f"commit in link = {sha}; equals gitlink = {sha == pin}")
print(f"path = {path}; fragment = {frag}")
PY
blob=$(git -C "$P" rev-parse "$pin:docs/architecture/07_memory_maps.md")
echo "pinned blob of docs/architecture/07_memory_maps.md at $pin: $blob"

echo "## anchors of the pinned page, by the repository's own GitHub slug (scripts/gen_toc.py anchor())"
git -C "$P" show "$pin:docs/architecture/07_memory_maps.md" > "$S/07_memory_maps.pinned.md"
( cd "$S/git-sub" && python3 - "$S/07_memory_maps.pinned.md" <<'PY'
import re, sys
sys.path.insert(0, "scripts")
from gen_toc import anchor
seen = {}
text = open(sys.argv[1], encoding="utf-8").read().split("\n")
fence = False; hits = []; l10 = None; heads = []
for i, line in enumerate(text, 1):
    if line.lstrip().startswith("```"):
        fence = not fence; continue
    if fence: continue
    m = re.match(r"(#{1,6})\s+(.*?)\s*#*\s*$", line)
    if m:
        a = anchor(m.group(2), seen); heads.append((i, a))
        if a == "31-descriptor-tree": hits.append(i)
    if line.startswith("| L10 |"): l10 = i
print("heading lines with anchor 31-descriptor-tree:", hits)
nxt = [i for i, _ in heads if hits and i > hits[0]]
print("L10 row line:", l10, "; next heading after 3.1 at line:", nxt[0] if nxt else None,
      "; L10 inside section 3.1:", bool(hits and l10 and hits[0] < l10 < (nxt[0] if nxt else 10**9)))
PY
)
echo "## what GitHub serves, unauthenticated"
code=$(curl -s -o /dev/null -w '%{http_code}' -L "$url"); echo "GET $url -> HTTP $code"
raw=$(python3 -c 'import re,sys; o,r,s,p=re.fullmatch(r"https://github\.com/([^/]+)/([^/]+)/blob/([0-9a-f]{40})/([^#]+)#.*", sys.argv[1]).groups(); print(f"https://raw.githubusercontent.com/{o}/{r}/{s}/{p}")' "$url")
curl -s -f -o "$S/07_memory_maps.served.md" "$raw"; echo "GET $raw -> exit $?"
echo "served raw file git blob: $(git hash-object --no-filters "$S/07_memory_maps.served.md") (pinned $blob)"
page_has_anchor=$(curl -s -L "$url" | grep -c 'id="user-content-31-descriptor-tree"\|31-descriptor-tree' || true)
echo "served blob page mentions the 31-descriptor-tree anchor: $page_has_anchor occurrence(s)"
old="https://github.com/kebag-logic/milan-fpga/blob/$HEAD_C/protocol-processor/docs/architecture/07_memory_maps.md"
echo "control, the round-1 relative target as the rendered parent page resolves it: GET $old -> HTTP $(curl -s -o /dev/null -w '%{http_code}' -L "$old")"
