#!/usr/bin/env bash
# End-to-end: the shipped em-dash gate (scripts/check_em_dash.py --base) on real
# Git commits, for a page whose em-dash heading GitHub hides inside an open raw
# comment. Variant "spoof" adds a raw <h2> carrying an UPPER-CASE copy of the
# renderer's position attribute; variant "control" is identical without it.
# Usage: emdash_spoof_e2e.sh <python-with-lock> <source-repo> <workdir>
set -euo pipefail
py=$(realpath -s "$1"); src=$2; work=$(realpath -m "$3")
rm -rf "$work"; mkdir -p "$work"
for variant in control spoof; do
  repo="$work/$variant"; mkdir -p "$repo"
  git -C "$src" archive HEAD scripts tools/markdown | tar -x -C "$repo"
  cd "$repo"
  git init -q --initial-branch=main
  git -c user.name=probe -c user.email=probe@example.invalid add -A
  git -c user.name=probe -c user.email=probe@example.invalid commit -qm "scripts"
  "$py" - "$variant" <<'PY'
import sys
variant = sys.argv[1]
def page(contents):
    head = ["# Page", ""]
    toc = ["## Contents", "",
           "- **[Alpha](#alpha)** -- What alpha holds.",
           "- **[Old — heading](#old--heading)** -- Copied.",
           "- **[Beta](#beta)** -- What beta holds.",
           "- **[Gamma](#gamma)** -- What gamma holds.", ""] if contents else []
    body = ["## Alpha", "", "Body.", "", "SPOOF", "", "<span>", "<!--", "",
            "## Old — heading", "", "<!-- -->", "", "## Beta", "", "Body.", "",
            "## Gamma", "", "Body.", ""]
    lines = head + toc + body
    at = lines.index("## Old — heading") + 1
    width = len(lines[at - 1].encode())
    spoof = f'<h2 DATA-SOURCEPOS="{at}:1-{at}:{width}">x</h2>'
    if variant == "spoof":
        lines[lines.index("SPOOF")] = spoof
    else:
        i = lines.index("SPOOF"); del lines[i:i + 2]
    return "\n".join(lines)
open("P.base.md", "w").write(page(False)); open("P.head.md", "w").write(page(True))
PY
  cp P.base.md P.md; rm -f P.base.md
  git -c user.name=probe -c user.email=probe@example.invalid add P.md
  git -c user.name=probe -c user.email=probe@example.invalid commit -qm base
  base=$(git rev-parse HEAD)
  mv P.head.md P.md
  git -c user.name=probe -c user.email=probe@example.invalid commit -qam head
  echo "===== variant: $variant (base $base, head $(git rev-parse HEAD))"
  echo "--- added lines:"; git diff -U0 "$base" HEAD -- P.md | grep '^+[^+]' || true
  echo "--- headings() at base and head:"
  "$py" -c "import sys; sys.path.insert(0,'scripts'); import gen_toc,subprocess; b=subprocess.run(['git','show','$base:P.md'],capture_output=True,text=True).stdout; print('base', gen_toc.headings(b)); print('head', gen_toc.headings(open('P.md').read()))"
  echo "--- check_em_dash.py --base $base:"
  set +e; "$py" scripts/check_em_dash.py --base "$base"; rc=$?; set -e
  echo "rc=$rc"
  cd - >/dev/null
done
