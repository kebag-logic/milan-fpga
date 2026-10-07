#!/bin/sh
# Verify that a checkout and its initialised submodules hold exactly the committed
# bytes and modes, a stage-0-only index, no hidden index flags and no untracked
# or ignored files. Usage: verify_integrity.sh <checkout> <expected-head>
set -eu
root=$1; want=$2
check() {
    dir=$1
    printf '== %s\n' "$dir"
    printf 'HEAD %s\n' "$(git -C "$dir" rev-parse HEAD)"
    flags=$(git -C "$dir" ls-files -v | grep -v '^H ' || true)
    [ -z "$flags" ] || { printf 'hidden/abnormal index flags:\n%s\n' "$flags"; exit 1; }
    staged=$(git -C "$dir" ls-files -s | awk '$3 != 0' || true)
    [ -z "$staged" ] || { printf 'non-zero stage entries:\n%s\n' "$staged"; exit 1; }
    n=0
    git -C "$dir" ls-tree -r HEAD > "$tmp"
    while read -r mode type obj path; do
        if [ "$type" = commit ]; then continue; fi
        n=$((n+1))
        if [ "$mode" = 120000 ]; then
            [ -L "$dir/$path" ] || { echo "not a symlink: $path"; exit 1; }
            got=$(printf '%s' "$(readlink "$dir/$path")" | git hash-object --stdin)
        else
            [ -f "$dir/$path" ] && [ ! -L "$dir/$path" ] || { echo "not a file: $path"; exit 1; }
            got=$(git hash-object --no-filters "$dir/$path")
            if [ "$mode" = 100755 ]; then [ -x "$dir/$path" ] || { echo "mode lost: $path"; exit 1; }
            else [ ! -x "$dir/$path" ] || { echo "mode gained: $path"; exit 1; }; fi
        fi
        [ "$got" = "$obj" ] || { echo "blob mismatch: $path"; exit 1; }
    done < "$tmp"
    printf 'blobs verified %s\n' "$n"
    extra=$(git -C "$dir" status --porcelain --ignored --untracked-files=all --ignore-submodules=all)
    [ -z "$extra" ] || { printf 'untracked/ignored/modified:\n%s\n' "$extra"; exit 1; }
}
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
[ "$(git -C "$root" rev-parse HEAD)" = "$want" ] || { echo "head is not $want"; exit 1; }
check "$root"
git -C "$root" ls-tree -r HEAD | awk '$2 == "commit" {print $3, $4}' | while read -r pin path; do
    if [ -e "$root/$path/.git" ]; then
        got=$(git -C "$root/$path" rev-parse HEAD)
        [ "$got" = "$pin" ] || { echo "gitlink mismatch $path: $got != $pin"; exit 1; }
        idx=$(git -C "$root" ls-files -s -- "$path")
        printf 'gitlink %s %s index: %s\n' "$path" "$pin" "$idx"
        check "$root/$path"
    else
        printf 'gitlink %s %s (not initialised)\n' "$path" "$pin"
    fi
done
echo INTEGRITY OK
