#!/usr/bin/env bash
# Acceptance probes on a disposable clone of the exact head; the reviewed clone is never written.
# Usage: acceptance_probe.sh REPO SCRATCH_DIR
set -u
repo=$1
work=$2/accept
head=171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22

fresh() {
    rm -rf "$work"
    git clone -q --shared --no-checkout "$repo" "$work"
    git -C "$work" checkout -q "$head"
}
gate() {
    python3 -I "$work/scripts/docs_inventory.py" --check > "$work.out" 2>&1
    rc=$?
    echo "$1: rc=$rc $(grep -m1 -E 'STALE|OK|REFUSED' "$work.out" | cut -c1-90)"
}
pages() {
    git -C "$work" ls-files -z | python3 -I -c '
import sys
for p in sys.stdin.buffer.read().decode().split("\0"):
    n = p.rsplit("/", 1)[-1]
    if p and p != "docs/DOCUMENTATION_AUDIT.md" and (p.endswith(".md") or n.upper().startswith("README")):
        print(p)'
}

fresh
gate "unchanged head"
pages | while read -r p; do [ -f "$work/$p" ] && echo "Added line." >> "$work/$p"; done
gate "one line appended to every page"

fresh
pages | while read -r p; do
    [ -f "$work/$p" ] && { for _ in $(seq 1 500); do echo "x"; done >> "$work/$p"; }
done
gate "500 lines appended to every page"

for n in 1 6 7 15; do
    fresh
    pages | while read -r p; do
        [ -f "$work/$p" ] && { { for _ in $(seq 1 "$n"); do echo; done; cat "$work/$p"; } > "$work.tmp"; cp "$work.tmp" "$work/$p"; }
    done
    gate "$n blank line(s) prepended to every page"
    python3 -I "$work/scripts/docs_inventory.py" --write > /dev/null
    git -C "$work" diff --numstat -- docs/DOCUMENTATION_AUDIT.md | sed 's/^/    audit page numstat: /'
    git -C "$work" diff -U0 -- docs/DOCUMENTATION_AUDIT.md | grep -E '^\+\|' | awk -F'|' '{print $6}' | sort | uniq -c | sed 's/^/    status cells after: /'
done

fresh
printf '\n> Superseded by [A](../README.md).\n' >> "$work/docs/GLOSSARY.md"
sed -i '1a\\n> Superseded by [A](../README.md).' "$work/docs/GLOSSARY.md"
gate "banner in the first lines of a page"

fresh
echo '# New' > "$work/docs/NEW_PROBE.md"
git -C "$work" add docs/NEW_PROBE.md
gate "page added"

fresh
git -C "$work" rm -q docs/GLOSSARY.md
gate "page removed"
rm -rf "$work" "$work.out" "$work.tmp"
