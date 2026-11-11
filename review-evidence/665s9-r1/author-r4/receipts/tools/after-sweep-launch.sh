#!/usr/bin/env bash
# after-sweep-launch.sh: once every sweep shard is launched, elaborate-gates-1's next attempt in its own unit on a
# range cpu_ranges.py picks (ci_replay.py tick, at most one unit), then the elaborate jobs that need it, locally
S=<scratch>; H=ad2ed0e3ab3daa9697bdf42ae504b4504bfd04aa; R=$S/ci/ad2ed0e3ab3d
until grep -q "every shard launched" $S/sweep-watch.log; do sleep 60; done
until [ -f $R/jobs/elaborate__elaborate-gates-1/result.json ]; do
  python3 $S/tools/replay/ci_replay.py tick $H 1; sleep 120
done
python3 $S/tools/replay/ci_replay.py local $H
