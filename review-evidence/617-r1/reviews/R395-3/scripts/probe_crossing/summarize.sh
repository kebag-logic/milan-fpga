#!/usr/bin/env bash
# summarize.sh LOG: phases, failing phases, total checks/failures, net-nonzero
# and tail-slip placements, and the latest last-slip column.
f=$1
awk '/== capture_coherence: checks:/ {ph++; c+=$4; fl+=$6; if ($6>0) bad++}
     /repeats, .* skips; last slip col/ {
        n++;
        match($0, /([0-9]+) repeats, ([0-9]+) skips; last slip col (-?[0-9]+); tail slips ([0-9]+)/, m);
        if (m[1]!=m[2]) nz++; if (m[4]>0) ts++; if (m[1]>0||m[2]>0) sl++; if (m[3]>mx) mx=m[3] }
     END { printf "%s: phases %d, failing phases %d, checks %d, failures %d, placements %d, slipping %d, net-nonzero %d, tail-slip placements %d, latest last-slip col %d\n", FILENAME, ph, bad, c, fl, n, sl, nz, ts, mx }' "$f"
