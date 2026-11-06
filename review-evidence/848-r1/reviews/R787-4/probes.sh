#!/bin/bash
# Sensitivity probes of the #848 acceptance on the merged tree; every probe resets the disposable clone first.
# usage: probes.sh <disposable clone> <head sha>
C=$1; H=$2; cd "$C" || exit 2
export PYTHONDONTWRITEBYTECODE=1
reset() { git reset -q --hard "$H"; git clean -qfdx; }
chk() { python3 scripts/docs_inventory.py --check >/tmp/r787_4_out 2>&1; rc=$?; printf '%-58s rc=%s want=%s %s\n' "$1" "$rc" "$2" "$([ "$rc" = "$2" ] && echo OK || echo UNEXPECTED)"; }
S=docs/reference/STRICTER_READINGS.md
reset; chk "control: untouched head" 0
reset; printf '\nOne added plain line.\n' >> $S; chk "add a line to the new #842 page" 0
reset; for f in $(git ls-files '*.md' | grep -v '^docs/DOCUMENTATION_AUDIT.md$'); do [ -f "$f" ] && printf '\nOne added plain line.\n' >> "$f"; done; chk "add a line to every tracked page" 0
reset; sed -i '1s/.*/# A changed title/' $S; chk "change the title of the new page" 1
reset; sed -i '3i Superseded by [the map](../README.md).' $S; chk "supersession banner on the new page (status change)" 1
reset; git rm -q $S; chk "remove the new page (page set)" 1
reset; printf '# New\n' > docs/reference/NEW_PAGE.md; git add docs/reference/NEW_PAGE.md; chk "add a tracked page (page set)" 1
reset; git show a578ceb561f4987e6ae4dacf1216e0d5d4d671f9:docs/DOCUMENTATION_AUDIT.md > docs/DOCUMENTATION_AUDIT.md; chk "audit from the merge commit, before regeneration" 1
reset; git status --short | wc -l
