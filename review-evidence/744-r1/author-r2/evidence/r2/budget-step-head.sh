set -euo pipefail
cpus="$(nproc)"
test "$cpus" -gt 0
kib="$(awk '$1 == "MemTotal:" && $3 == "kB" { print $2 }' /proc/meminfo)"
test "$kib" -gt 0
memory=$(( kib * 1024 ))
cgroup="/sys/fs/cgroup$(sed -n 's/^0:://p' /proc/self/cgroup)"
cgroup="${cgroup%/}"
while :; do
  if [ -d "$cgroup" ] && [ ! -x "$cgroup" ]; then
    echo "unsearchable cgroup $cgroup: its memory limit cannot be proved absent" >&2; exit 1
  fi
  if [ -e "$cgroup/memory.max" ]; then
    if ! limit="$(cat "$cgroup/memory.max")"; then
      echo "unreadable memory limit in $cgroup" >&2; exit 1
    fi
    case "$limit" in
      max) ;;
      ''|*[!0-9]*) echo "non-numeric memory limit in $cgroup: $limit" >&2; exit 1 ;;
      *) if [ "$limit" -lt "$memory" ]; then memory="$limit"; fi ;;
    esac
  fi
  if [ "$cgroup" = /sys/fs/cgroup ]; then break; fi
  cgroup="${cgroup%/*}"
done
census=$(( memory * 2 / (3 * 1242214400) ))
census=$(( census < cpus ? census : cpus ))
census=$(( census > 0 ? census : 1 ))
echo "census workers: $census of $cpus CPU(s) within $memory bytes of memory"
printf 'CI_CENSUS_JOBS=%s\n' "$census" >> "$GITHUB_ENV"
