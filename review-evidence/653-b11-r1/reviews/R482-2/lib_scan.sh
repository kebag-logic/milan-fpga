#!/bin/sh
# R482-2: the controller library's STREAM_INPUT counter condition across public releases, and
# every path that stores a STREAM_INPUT counters update, at tag v4.3.1.1.
# Usage: lib_scan.sh <unpacked v4.3.1.1 tree> <unpacked dev-head tree> <work dir>
# Needs an authenticated read-only `gh` for the per-tag file fetches.
tag=$1; dev=$2; work=$3; mkdir -p "$work"
echo "== tag object and commit"
gh api repos/L-Acoustics/avdecc/git/ref/tags/v4.3.1.1 -q '.object.sha'
gh api repos/L-Acoustics/avdecc/git/tags/080ab851ba558e8502c5d44522a3012bee007440 -q '.object.sha'
echo "== tags (newest first, first 6)"; gh api 'repos/L-Acoustics/avdecc/tags?per_page=6' -q '.[].name'
echo "== dev head at scan time"; gh api repos/L-Acoustics/avdecc/commits/dev -q '.sha'
echo "== condition line per release (avdeccControllerImpl.cpp, STREAM_INPUT block)"
for t in v3.2.4 v3.4.1 v4.0.0 v4.1.0 v4.3.0; do
  gh api "repos/L-Acoustics/avdecc/contents/src/controller/avdeccControllerImpl.cpp?ref=$t" \
    -H 'Accept: application/vnd.github.raw' > "$work/impl-$t.cpp"
  printf '%s ' "$t"; grep -n -A4 'MediaUnlocked should either' "$work/impl-$t.cpp" | grep 'lockedValue != ' | tr -s '\t ' ' '
done
for d in "$tag" "$dev"; do
  printf '%s ' "$(basename "$d")"; grep -n -A4 'MediaUnlocked should either' "$d/src/controller/avdeccControllerImpl.cpp" | grep 'lockedValue != ' | tr -s '\t ' ' '
done
echo "== updateStreamInputCounters: tag vs dev body (diff; only the assert line expected)"
diff <(sed -n '/void ControllerImpl::updateStreamInputCounters/,/^}/p' "$tag/src/controller/avdeccControllerImpl.cpp") \
     <(sed -n '/void ControllerImpl::updateStreamInputCounters/,/^}/p' "$dev/src/controller/avdeccControllerImpl.cpp")
echo "== every caller of updateStreamInputCounters at the tag (the only store path)"
grep -rn 'updateStreamInputCounters(' "$tag/src" | sed "s#^$tag/##" | cut -c1-120
echo "== every StreamInputCounterValidFlag::MediaUnlocked reference at the tag"
grep -rn 'StreamInputCounterValidFlag::MediaUnlocked' "$tag/src" "$tag/include" | sed "s#^$tag/##" | cut -c1-140
echo "== Diagnostics fields at the tag (no counter-based diagnostic)"
sed -n '/struct Diagnostics/,/friend bool operator==/p' "$tag/include/la/avdecc/controller/internals/avdeccControlledEntity.hpp" | grep -E '^\s+(bool|std::)' | cut -c1-110
echo "== copied header at the tag"
sha256sum "$tag/include/la/avdecc/controller/internals/avdeccVirtualControlledEntityInterface.hpp" | sed "s#$tag/##"
