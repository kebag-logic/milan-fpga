#!/usr/bin/env bash
# compare_out.sh <campaign>: per-arm receipts in out/base/<c> vs out/head/<c>; compares each
# common receipt's sorted failing-check lines (FAIL ...), and lists receipts present on one side
c="$1"; B=<scratch>/r2/out/base/$c; H=<scratch>/r2/out/head/$c
[ -d "$B" ] && [ -d "$H" ] || { echo "$c: missing output dir"; exit 1; }
common=0; same=0; diffs=()
while IFS= read -r rel; do
  [ -f "$H/$rel" ] || continue
  common=$((common + 1))
  if diff -q <(grep -E '(^|[^A-Za-z])FAIL[: ]' "$B/$rel" | sed -E 's/(all\.v|sim_main\.cpp|\.sv|\.cpp|\.hpp):[0-9]+/\1:N/g' | sort) \
             <(grep -E '(^|[^A-Za-z])FAIL[: ]' "$H/$rel" | sed -E 's/(all\.v|sim_main\.cpp|\.sv|\.cpp|\.hpp):[0-9]+/\1:N/g' | sort) > /dev/null; then
    same=$((same + 1))
  else
    diffs+=("$rel")
  fi
done < <(cd "$B" && find . -type f \( -name '*.log' -o -name '*.txt' -o -name '*.json' \) | sort)
onlyb=$(comm -23 <(cd "$B" && find . -type f | sort) <(cd "$H" && find . -type f | sort) | wc -l)
onlyh=$(comm -13 <(cd "$B" && find . -type f | sort) <(cd "$H" && find . -type f | sort) | wc -l)
echo "$c: $common common receipts, $same identical failing sets; only-base $onlyb, only-head $onlyh; differing: ${diffs[*]:-none}"
