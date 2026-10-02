#!/bin/sh
# git apply --check every campaign patch of tb/pp_top against a pristine export
# of the head; report offsets/fuzz. Usage: patch_apply_check.sh REPO WORKDIR
set -u
REPO="$1"; W="$2"
rm -rf "$W"; mkdir -p "$W"
git -C "$REPO" archive 4a40b1798e463d09aafd74632408003229bcc673 | tar -x -C "$W"
rc=0
for p in "$W"/tb/pp_top/aecp_dispatch_mutations/*.patch "$W"/tb/pp_top/mutations/*.patch; do
  [ -f "$p" ] || continue
  if out=$(cd "$W" && git apply --check -v "$p" 2>&1); then
    off=$(printf '%s\n' "$out" | grep -c "applied .*offset\|with fuzz" || true)
    echo "OK $(basename "$(dirname "$p")")/$(basename "$p") offset_or_fuzz_hunks=$off"
  else
    echo "REFUSED $(basename "$(dirname "$p")")/$(basename "$p")"; printf '%s\n' "$out" | sed 's/^/    /'; rc=1
  fi
done
exit $rc
