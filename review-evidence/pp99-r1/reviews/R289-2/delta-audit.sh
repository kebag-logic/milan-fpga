#!/usr/bin/env bash
# R289-2 delta audit: scope, byte-level shape of each change, author patch identity.
# Usage: delta-audit.sh CLONE AUTHOR_ROUND2_PATCH
set -u
C=$1; P=$2; B=663d50d65ff49c33b153107b2f79d6f3c5725799; H=9cde1c19dbfd859257be8e012d4455856fcfce3b
cd "$C" || exit 2
echo "head=$(git rev-parse HEAD) tree=$(git rev-parse HEAD^{tree})"
echo "## name-status $B..$H"; git diff --name-status $B $H
echo "## numstat"; git diff --numstat $B $H
echo "## summary (mode changes, empty = none)"; git diff --summary $B $H
echo "## whitespace check"; git diff --check $B $H; echo "rc=$?"
echo "## hdl/tb/syn/scripts/.github/Makefile untouched in round 2 (empty = untouched)"; git diff --stat $B $H -- hdl tb syn scripts .github Makefile
echo "## integrator.md: lines equal after normalising the 07 fragments"
diff <(git show $B:docs/guides/integrator.md | sed -E 's/07_memory_maps\.md#[a-z0-9-]+/07_memory_maps.md#X/g') \
     <(git show $H:docs/guides/integrator.md | sed -E 's/07_memory_maps\.md#[a-z0-9-]+/07_memory_maps.md#X/g'); echo "rc=$?"
echo "## 07: head minus the one added anchor line equals base"
diff <(git show $B:docs/architecture/07_memory_maps.md) <(git show $H:docs/architecture/07_memory_maps.md | grep -vx '<a id="sec-resp-memory"></a>'); echo "rc=$?"
echo "## 07 context of new anchor"; git show $H:docs/architecture/07_memory_maps.md | sed -n '213,217p' | cat -A | cut -c1-90
echo "## 09: head minus params row equals base"
diff <(git show $B:docs/architecture/09_verification.md) <(git show $H:docs/architecture/09_verification.md | grep -v '^| `params` |'); echo "rc=$?"
echo "## author round2.patch vs git diff (content lines only)"
diff <(grep -E '^[-+][^-+]' "$P") <(git diff $B $H | grep -E '^[-+][^-+]'); echo "rc=$?"
echo "## explicit-anchor style in 07 (existing <a id> lines)"; git show $H:docs/architecture/07_memory_maps.md | grep -n '^<a id=' | head -20
