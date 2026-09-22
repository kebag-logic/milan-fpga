#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Lint every embedded ```mermaid and ```wavedrom block in the documentation.
#   mermaid  -> parse/render check via mmdc (headless chromium, --no-sandbox)
#   wavedrom -> strict-JSON check via python3 -m json.tool
#
# Strict mode is safe here because every status this script expects to be
# non-zero is already read in a condition: `mmdc` and `json.tool` are the two
# verdicts and both sit in an `if !`, and the `ls README.md` that may find
# nothing is inside the process substitution feeding `mapfile`, whose own
# status is what `set -e` sees.
set -euo pipefail
fail=0
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

# puppeteer config so mmdc's chromium runs in sandboxed/headless environments
printf '{"args":["--no-sandbox","--disable-gpu"]}\n' > "$tmpdir/puppeteer.json"

extract_blocks() { # $1=md-file $2=fence-tag $3=out-prefix
  awk -v tag="$2" -v pre="$3" '
    $0 ~ "^```"tag"[ \t]*$" { inblock=1; n++; out=pre "-" n ".txt"; next }
    inblock && /^```[ \t]*$/ { inblock=0; close(out); next }
    inblock { print > out }
  ' "$1"
}

mapfile -t mdfiles < <(find docs -name '*.md' | sort; ls README.md 2>/dev/null)

for f in "${mdfiles[@]}"; do
  base=$(printf '%s' "$f" | tr '/.' '__')   # unique per path (docs/README vs README)
  extract_blocks "$f" mermaid  "$tmpdir/mmd-$base"
  extract_blocks "$f" wavedrom "$tmpdir/wd-$base"
done

shopt -s nullglob

for m in "$tmpdir"/mmd-*.txt; do
  if ! mmdc --quiet -p "$tmpdir/puppeteer.json" -i "$m" -o "$tmpdir/out.svg" >/dev/null 2>"$tmpdir/err.log"; then
    echo "MERMAID FAIL: ${m#"$tmpdir"/}"
    head -4 "$tmpdir/err.log" | sed 's/^/    /'
    fail=1
  fi
done

for w in "$tmpdir"/wd-*.txt; do
  if ! python3 -m json.tool "$w" >/dev/null 2>&1; then
    echo "WAVEDROM FAIL (not strict JSON): ${w#"$tmpdir"/}"
    fail=1
  fi
done

n_mmd=$(find "$tmpdir" -name 'mmd-*.txt' | wc -l)
n_wd=$(find "$tmpdir" -name 'wd-*.txt' | wc -l)
echo "lint: $n_mmd mermaid + $n_wd wavedrom blocks checked, $( [ "$fail" -eq 0 ] && echo OK || echo FAILURES )"
exit "$fail"
