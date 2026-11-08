#!/bin/sh
# Disposable mutation probes on an archive copy of the head: $1 = copy dir, $2 = original repo.
set -u
C="$1"; O="$2"
cd "$C" || exit 2
run() { python3 -I scripts/docs_inventory.py --check >/dev/null 2>&1; echo "$1 check rc=$?"; }
run "M0 pristine copy"
# M1: re-add removed D0-006 to the data file without regenerating the page
git -C "$O" show 1de759d3e4:scripts/docs_inventory.json > scripts/docs_inventory.json
run "M1 prior data file (15 entries back), page not regenerated"
# M2: regenerate with the prior data file -> page must equal prior head's page
python3 -I scripts/docs_inventory.py --write >/dev/null 2>&1; echo "M2 write rc=$?"
git -C "$O" show 1de759d3e4:docs/DOCUMENTATION_AUDIT.md | cmp -s - docs/DOCUMENTATION_AUDIT.md && echo "M2 regenerated page == prior head page" || echo "M2 regenerated page DIFFERS from prior head page"
# M3: back to head data, regenerate -> must equal head page byte for byte
git -C "$O" show HEAD:scripts/docs_inventory.json > scripts/docs_inventory.json
python3 -I scripts/docs_inventory.py --write >/dev/null 2>&1; echo "M3 write rc=$?"
git -C "$O" show HEAD:docs/DOCUMENTATION_AUDIT.md | cmp -s - docs/DOCUMENTATION_AUDIT.md && echo "M3 regenerated page == head page" || echo "M3 regenerated page DIFFERS from head page"
# M4: also drop D0-040 (which still has copy rows) and regenerate: copy rows must vanish (shows why it is kept)
python3 -I -c "
import json;p='scripts/docs_inventory.json';d=json.load(open(p))
d['findings']=[f for f in d['findings'] if f['id']!='D0-040'];json.dump(d,open(p,'w'),indent=1,ensure_ascii=False)"
python3 -I scripts/docs_inventory.py --write >/dev/null 2>&1; echo "M4 write rc=$?"
echo "M4 D0-040 rows after drop: $(grep -c '^| D0-040 |' docs/DOCUMENTATION_AUDIT.md)  at head: $(git -C "$O" show HEAD:docs/DOCUMENTATION_AUDIT.md | grep -c '^| D0-040 |')"
# M5: inject the fixed D0-006 statement back onto the page with head data -> check must fail? (entry removed, so no row: shows gate does not track removed text)
git -C "$O" show HEAD:scripts/docs_inventory.json > scripts/docs_inventory.json
git -C "$O" show HEAD:docs/DOCUMENTATION_AUDIT.md > docs/DOCUMENTATION_AUDIT.md
run "M5a restored"
printf '\nattribute'"'"'s 802.1Q 35.2.2.7.4 FourPackedEvents value\n' >> docs/reference/REGISTER_MAP.md
run "M5b reintroduced D0-006 wrong text on REGISTER_MAP.md"
