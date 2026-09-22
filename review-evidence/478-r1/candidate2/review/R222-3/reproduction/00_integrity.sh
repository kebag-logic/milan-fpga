#!/usr/bin/env bash
# R222-3 read-only integrity snapshot of the review clone.
# Usage: 00_integrity.sh <clone> <out-file>
# Records HEAD, tree, parents, index==HEAD-tree equality, per-entry raw-byte
# blob and on-disk kind/mode equality, and the three required submodule pins.
# Uses GIT_OPTIONAL_LOCKS=0 so no status call refreshes an index.
set -euo pipefail
clone=$1
out=$2
export GIT_OPTIONAL_LOCKS=0
export GIT_NO_REPLACE_OBJECTS=1
g() { git -C "$clone" "$@"; }
{
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "clone: <review-clone>"
  echo "HEAD: $(g rev-parse HEAD)"
  echo "tree: $(g rev-parse 'HEAD^{tree}')"
  echo "parents: $(g rev-parse HEAD^1) $(g rev-parse HEAD^2)"
  echo "symbolic-ref: $(g symbolic-ref -q HEAD || echo detached)"
  idx=$(g ls-files -s | sha256sum | cut -d' ' -f1)
  echo "index-listing-sha256: $idx"
  echo "index-entries: $(g ls-files -s | wc -l)"
  echo "unmerged-entries: $(g ls-files -u | wc -l)"
  # index (stage 0) must equal HEAD tree exactly: mode, oid, path
  a=$(g ls-files -s | awk '{print $1" "$2" "$4}' | sha256sum | cut -d' ' -f1)
  b=$(g ls-tree -r --full-tree HEAD | awk '{split($0,t,"\t"); split(t[1],m," "); print m[1]" "m[3]" "t[2]}' | sha256sum | cut -d' ' -f1)
  echo "index-vs-HEAD-tree: $([ "$a" = "$b" ] && echo EQUAL || echo DIFFERENT) ($a / $b)"
  # per-entry raw bytes, kind and mode on disk
  bad=0; n=0
  while IFS=$'\t' read -r meta path; do
    mode=${meta%% *}; rest=${meta#* }; oid=${rest%% *}
    n=$((n+1))
    f="$clone/$path"
    case "$mode" in
      160000)
        [ -d "$f" ] || { echo "MISMATCH kind(gitlink not dir) $path"; bad=$((bad+1)); } ;;
      120000)
        if [ -L "$f" ]; then
          h=$(printf '%s' "$(readlink "$f")" | git hash-object --no-filters --stdin)
          [ "$h" = "$oid" ] || { echo "MISMATCH symlink-target $path"; bad=$((bad+1)); }
        else echo "MISMATCH kind(not symlink) $path"; bad=$((bad+1)); fi ;;
      100644|100755)
        if [ -f "$f" ] && [ ! -L "$f" ]; then
          h=$(git hash-object --no-filters "$f")
          [ "$h" = "$oid" ] || { echo "MISMATCH blob $path"; bad=$((bad+1)); }
          if [ -x "$f" ]; then dm=100755; else dm=100644; fi
          [ "$dm" = "$mode" ] || { echo "MISMATCH mode $path disk=$dm index=$mode"; bad=$((bad+1)); }
        else echo "MISMATCH kind(not regular) $path"; bad=$((bad+1)); fi ;;
      *) echo "UNEXPECTED mode $mode $path"; bad=$((bad+1)) ;;
    esac
  done < <(g ls-files -s)
  echo "entries-checked: $n mismatches: $bad"
  echo "porcelain-status-lines (untracked excluded): $(g status --porcelain --untracked-files=no | wc -l)"
  echo "untracked-files: $(g status --porcelain --untracked-files=normal | grep -c '^??' || true)"
  for s in protocol-processor gptp-processor third_party/verilog-axis; do
    pin=$(g ls-tree HEAD "$s" | awk '{print $3}')
    head=$(git -C "$clone/$s" rev-parse HEAD)
    dirty=$(git -C "$clone/$s" status --porcelain --untracked-files=no | wc -l)
    echo "submodule $s pin=$pin checkout=$head match=$([ "$pin" = "$head" ] && echo yes || echo NO) tracked-dirty-lines=$dirty"
  done
  echo "external: $(g submodule status external)"
  echo "gitmodules-blob: $(g rev-parse HEAD:.gitmodules)"
} > "$out" 2>&1
cat "$out"
