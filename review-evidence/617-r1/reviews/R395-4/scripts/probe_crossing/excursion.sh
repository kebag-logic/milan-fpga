#!/usr/bin/env bash
# excursion.sh LOG...: per log, over the placements that slipped, the largest
# excursion of the close to the far side of its engagement point (the "+N" of
# "moved -a..+N" at negative rates, the "-a" at positive ones) and the latest
# last-slip column.
for f in "$@"; do
  awk -v F="$(basename "$f")" '/engaged/ && !/ 0 repeats/ {
      match($0, /moved (-?[0-9]+)\.\.\+?(-?[0-9]+)/, m); lo=-m[1]; hi=m[2];
      match($0, /last slip col (-?[0-9]+)/, c);
      n++; if (hi>mh) mh=hi; if (lo>ml) ml=lo; if (c[1]>mc) mc=c[1] }
    END { printf "%s: slipping %d, max +excursion %d, max -excursion %d, latest last-slip col %d\n", F, n, mh, ml, mc }' "$f"
done
