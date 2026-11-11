#!/usr/bin/env bash
# replay-drive.sh: the CI replay of the final head: ready instances as their own units on ranges cpu_ranges.py picks
# (tick, at most 3 at once, while memory allows), until every instance has a result
until python3 <scratch>/tools/replay/ci_replay.py tick a91fb27dd39483e4694e193504da1dbe06208807 3; do sleep 120; done
echo "tick: every instance has a result"
