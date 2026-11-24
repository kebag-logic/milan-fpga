#!/usr/bin/env bash
# baremetal_probe.sh <clone-at-0acf24d9> <scratch-dir>: run the repository's bare-metal scope gate (#259) at the
# reviewed head and at its parent 44c56639 (a shared, never-written clone under <scratch-dir>), one log each.
set -u
clone=$(realpath "$1"); scratch=$(realpath -m "$2"); mkdir -p "$scratch"
( cd "$clone" && echo "head $(git rev-parse HEAD)" && python3 -B scripts/check_baremetal_only.py --check; echo "rc=$?" ) \
  > "$scratch/baremetal-head.log" 2>&1
rm -rf "$scratch/parent"
git clone -q --shared --no-checkout "$clone" "$scratch/parent"
( cd "$scratch/parent" && git checkout -q --detach 44c566399002db32bf8a6ad3ce719488d418bcb0 &&
  echo "head $(git rev-parse HEAD)" && python3 -B scripts/check_baremetal_only.py --check; echo "rc=$?" ) \
  > "$scratch/baremetal-parent.log" 2>&1
tail -n 2 "$scratch/baremetal-head.log" "$scratch/baremetal-parent.log"
