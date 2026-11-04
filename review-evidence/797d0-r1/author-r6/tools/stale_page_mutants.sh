#!/usr/bin/env bash
# stale_page_mutants.sh <head sha> <scratch dir>: plant stale-page mutants on fresh clones of the head and
# show `docs_inventory.py --check` fails each, then passes after `--write`. Each arm prints its rcs.
set -u
H=$1; S=$2; L=$LANES/797-d0-audit
arm() {
  name=$1; shift
  d=$S/$name; rm -rf "$d"
  git clone -q --shared --no-checkout "$L" "$d" && git -C "$d" -c advice.detachedHead=false checkout -q --detach "$H" || return 9
  ( cd "$d" && test "$(git rev-parse HEAD)" = "$H" && test -z "$(git status --porcelain)" ) || return 9
  ( cd "$d" && python3 scripts/docs_inventory.py --check > /dev/null 2>&1 ); echo "$name: clean head --check rc=$?"
  ( cd "$d" && eval "$*" )
  echo "$name: planted, git status: $(git -C "$d" status --porcelain | tr '\n' ' ')"
  ( cd "$d" && python3 scripts/docs_inventory.py --check > "$S/$name.check.out" 2>&1 ); echo "$name: planted --check rc=$?"
  sed -n 1,3p "$S/$name.check.out"
  ( cd "$d" && python3 scripts/docs_inventory.py --write > /dev/null 2>&1 ); echo "$name: --write rc=$?"
  ( cd "$d" && python3 scripts/docs_inventory.py --check > /dev/null 2>&1 ); echo "$name: after --write --check rc=$?"
  echo "$name: audit page diff after --write:"; git -C "$d" diff -U0 -- docs/DOCUMENTATION_AUDIT.md | grep '^[-+]|' | cut -c1-220
  echo
}
# A line appended to a page dev 604899c0's merge touched: the page's line count changes.
arm append-line "echo 'Planted line.' >> docs/testing/CI_WORKFLOWS.md"
# The D0-057 copy on docs/testing/TESTING.md, the row that moved 1810 -> 1818, reworded away: its copy row leaves and the page renders current.
arm d0-057-copy-removed "sed -i '1818s/is pinned at the Milan 2 ms DEFAULT/defaults to the Milan 2 ms/' docs/testing/TESTING.md"
# The D0-001 statement planted back onto REQUIREMENTS.md: its copy row returns, so the cross-page search still runs on the merged tree.
arm d0-001-copy "printf '\nADP, ACMP, AECP, MAAP and SRP default to bare-metal firmware.\n' >> REQUIREMENTS.md"
