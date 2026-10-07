#!/bin/sh
# Usage: spdx_sweep.sh <repo> <rev>
# For every tracked blob at <rev>, print the first line number containing an
# SPDX-License-Identifier (or NONE), its identifier, and the path.
set -eu
repo=$1; rev=$2
git -C "$repo" ls-tree -r --full-tree "$rev" | while read -r mode type obj path; do
    if [ "$type" != blob ]; then
        printf '%s\t%s\t%s\t%s\n' "$mode" "$type" "-" "$path"
        continue
    fi
    hit=$(git -C "$repo" cat-file blob "$obj" | grep -n -m1 'SPDX-License-Identifier' || true)
    if [ -z "$hit" ]; then
        printf '%s\tNONE\t-\t%s\n' "$mode" "$path"
    else
        ln=${hit%%:*}
        id=$(printf '%s' "$hit" | sed 's/.*SPDX-License-Identifier: *\([A-Za-z0-9.+-]*\).*/\1/')
        printf '%s\tline%s\t%s\t%s\n' "$mode" "$ln" "$id" "$path"
    fi
done
