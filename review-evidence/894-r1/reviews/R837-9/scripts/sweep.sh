#!/bin/sh
# Usage: sweep.sh <repo> <tokens> -> every tracked text hit of a token as a
# whole number (not part of a longer number), path:line:token
repo=$1; tok=$2
cd "$repo" || exit 2
git ls-files -z | xargs -0 grep -I -n -o -w -F -f "$tok" 2>/dev/null |
  awk -F: '{print $1":"$2":"$3}' | sort -u | sort -t: -k1,1 -k2,2n -s
