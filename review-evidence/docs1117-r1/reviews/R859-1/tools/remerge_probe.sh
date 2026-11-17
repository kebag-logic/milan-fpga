#!/bin/bash
# Probe the CONTRIBUTING.md 2.3 claim "git show --remerge-diff <merge> shows one merge's resolution exactly".
# Builds a throwaway repo: base, member A, member B; B conflicts with A in f.txt; the composition merge resolves
# the conflict and also slips an unrelated edit into g.txt (an "evil" change) and leaves a clean-merged h.txt.
set -euo pipefail
d=$(mktemp -d "${1:-/tmp}/remerge.XXXX"); cd "$d"; git init -q -b base .
G="git -c user.name=p -c user.email=p@invalid"
printf 'a\nb\nc\n' > f.txt; printf 'g1\n' > g.txt; printf 'h1\n' > h.txt; $G add .; $G commit -qm base
$G switch -qc A; sed -i 's/b/b-from-A/' f.txt; $G commit -qam A
$G switch -q base; $G switch -qc B; sed -i 's/b/b-from-B/' f.txt; printf 'h1\nh2-from-B\n' > h.txt; $G commit -qam B
$G switch -q base; $G switch -qc comp; $G merge -q --no-ff A -m "merge A"
$G merge -q --no-ff B -m "merge B" >/dev/null 2>&1 || true
printf 'a\nb-from-A-and-B\nc\n' > f.txt; printf 'g1\ng2-evil\n' > g.txt; $G add f.txt g.txt h.txt; $G commit -qm "merge B"
echo "== git $(git --version | cut -d' ' -f3); git show --remerge-diff HEAD (merge B):"
git show --remerge-diff --format='commit %s' HEAD
echo "== plain git show HEAD (combined diff) for contrast:"
git show --format='commit %s' HEAD
echo "== remerge-diff of the clean merge A:"
git show --remerge-diff --format='commit %s' HEAD^1
