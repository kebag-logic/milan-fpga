#!/bin/sh
# ci_events_counts.sh REPO WORKDIR: ci_events.py --check and --selftest at the old dev base, both merge parents and the head.
REPO=$1; W=$2
for rev in c6bd08c6f52632c6d33d834ce842ac3cf63f29cc 5b4ea55160c5ee34263e24140f960c4f03d923bc dc4d06cbfec209cc2ff76806f4b49c51f46639ae 27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c; do
  d=$W/$rev; rm -rf "$d"; mkdir -p "$d"; git -C "$REPO" archive $rev | tar -x -C "$d"
  ( c=$(python3 -I "$d/scripts/ci_events.py" --check --root "$d" | tail -1); s=$(cd "$d" && python3 -I scripts/ci_events.py --selftest 2>&1 | tail -1); echo "$rev | $c | $s" ) &
done; wait
