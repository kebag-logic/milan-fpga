#!/usr/bin/env bash
# Verifies a checkout is byte-identical to its HEAD: index matches the tree,
# every tracked regular file and symlink hashes to its index blob with the
# index mode, the required gitlinks are checked out at their pins, and nothing
# untracked or ignored remains. Usage: verify_restore.sh <checkout>
set -u
cd "$1" || exit 2
bad=0
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
[ "$(git write-tree)" = "$(git rev-parse 'HEAD^{tree}')" ] && echo "index tree == HEAD tree" || { echo "INDEX DIFFERS"; bad=1; }
n=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; blob=${rest%% *}
  case $mode in
    160000) continue ;;
    120000) got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin); [ -L "$path" ] || got=notlink ;;
    100755) got=$(git hash-object --no-filters -- "$path"); [ -x "$path" ] || got=badmode ;;
    100644) got=$(git hash-object --no-filters -- "$path"); [ -x "$path" ] && got=badmode ;;
  esac
  n=$((n+1))
  [ "$got" = "$blob" ] || { echo "MISMATCH $mode $path"; bad=1; }
done < <(git ls-files -s)
echo "tracked entries hashed: $n"
for sub in gptp-processor protocol-processor third_party/verilog-axis; do
  pin=$(git ls-tree HEAD "$sub" | awk '{print $3}')
  head=$(git -C "$sub" rev-parse HEAD)
  dirty=$(git -C "$sub" status --porcelain=v1 --ignored | wc -l)
  echo "$sub pin=$pin checkout=$head extra=$dirty"
  [ "$pin" = "$head" ] && [ "$dirty" = 0 ] || bad=1
done
extra=$(git status --porcelain=v1 --ignored | wc -l)
echo "superproject untracked/ignored/modified entries: $extra"
[ "$extra" = 0 ] || bad=1
echo "RESULT: $([ $bad = 0 ] && echo RESTORED || echo NOT-RESTORED)"
exit $bad
