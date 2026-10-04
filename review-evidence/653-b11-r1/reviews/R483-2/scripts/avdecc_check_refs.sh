#!/usr/bin/env bash
# Read the upstream la_avdecc STREAM_INPUT counter check at several refs.
# Usage: avdecc_check_refs.sh <scratch-dir>   (prints the receipt on stdout)
set -euo pipefail
dir=${1:?scratch dir}
url=https://github.com/L-Acoustics/avdecc.git
mkdir -p "$dir"
cd "$dir"
[ -d avdecc-refs/.git ] || git init -q avdecc-refs
cd avdecc-refs
git remote get-url origin >/dev/null 2>&1 || git remote add origin "$url"
echo "# upstream $url, fetched $(date -u +%FT%TZ)"
echo "# ls-remote of the refs read:"
git ls-remote "$url" refs/tags/v4.3.1.1 'refs/tags/v4.3.1.1^{}' refs/heads/main refs/heads/dev refs/tags/v4.3.0 'refs/tags/v4.3.0^{}' refs/tags/v4.1.0 'refs/tags/v4.1.0^{}'
for r in refs/tags/v4.3.1.1 refs/heads/main refs/heads/dev refs/tags/v4.3.0 refs/tags/v4.1.0; do
  git fetch -q --depth 1 --filter=blob:none origin "$r"
  c=$(git rev-parse 'FETCH_HEAD^{commit}')
  f=$(git show "$c:src/controller/avdeccControllerImpl.cpp")
  echo "== $r commit $c  avdeccControllerImpl.cpp sha256 $(printf '%s\n' "$f" | sha256sum | cut -d' ' -f1)"
  printf '%s\n' "$f" | grep -n -A7 'MediaUnlocked should either' | cut -c1-240
  echo "-- every MediaUnlocked under src/ at $r:"
  git grep -n 'MediaUnlocked' "$c" -- src | sed "s/^$c://" | cut -c1-160
done
