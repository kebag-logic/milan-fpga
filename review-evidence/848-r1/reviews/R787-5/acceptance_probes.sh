#!/bin/sh
# #848 acceptance on a disposable clone. Usage: acceptance_probes.sh REPO HEAD WORKDIR
repo=$1; head=$2; work=$3
fresh() { rm -rf "$work"; git clone -q --no-checkout --shared "$repo" "$work"; git -C "$work" checkout -q --detach "$head"; }
check() { (cd "$work" && python3 scripts/docs_inventory.py --check >/dev/null 2>&1; echo "$1: --check rc $?"); }
fresh; (cd "$work" && git ls-files -z '*.md' | xargs -0 -I{} sh -c 'printf "\nAdded line.\n" >> "$1"' _ {}; git checkout -q -- docs/DOCUMENTATION_AUDIT.md); check "a line appended to every tracked Markdown page"
fresh; (cd "$work" && printf '\nOne added line.\n' >> REQUIREMENTS.md); check "a line appended to a listed page"
fresh; (cd "$work" && git rm -q docs/testing/TESTING.md); check "unlisted page removed"
fresh; (cd "$work" && sed -i '1s/.*/# Retitled page/' docs/reference/STRICTER_READINGS.md); check "unlisted page retitled"
fresh; (cd "$work" && python3 - <<'PY'
from pathlib import Path
p = Path("docs/reference/STRICTER_READINGS.md")
text = p.read_text(encoding="utf-8").split("\n")
text.insert(1, "\n> Superseded by [the map](SUBMODULES.md).\n")
p.write_text("\n".join(text), encoding="utf-8")
PY
); check "status change through a banner on an unlisted page"
rm -rf "$work"
