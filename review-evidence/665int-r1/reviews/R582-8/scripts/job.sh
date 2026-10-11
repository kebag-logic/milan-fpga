#!/usr/bin/env bash
# job.sh NAME CMD... : run CMD in the candidate clone, logging to
# logs/NAME.log and writing its exit status to logs/NAME.rc.
# Usage: CLONE=<candidate clone> PACKET=<packet dir> job.sh NAME CMD...
set -u
name=$1; shift
: "${CLONE:?}" "${PACKET:?}"
mkdir -p "$PACKET/logs"
log="$PACKET/logs/$name.log"; rcf="$PACKET/logs/$name.rc"
rm -f "$rcf"
{
  printf '# job %s\n# cwd %s\n# head %s\n# start %s\n# argv:' "$name" "$CLONE" \
    "$(git -C "$CLONE" rev-parse HEAD)" "$(date -u +%FT%TZ)"
  printf ' %q' "$@"; printf '\n'
} > "$log"
cd "$CLONE" || exit 2
start=$(date +%s)
"$@" >> "$log" 2>&1
rc=$?
printf '# end %s elapsed %ss rc %s\n' "$(date -u +%FT%TZ)" "$(( $(date +%s) - start ))" "$rc" >> "$log"
echo "$rc" > "$rcf"
