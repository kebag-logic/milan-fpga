#!/bin/bash
# copies.sh SRC_CLONE SCRATCH: make disposable clean clones of the head and the base, one per campaign.
set -eu
S=$1 W=$2
for n in head-validate head-rv32 head-probe base-probe; do
  rm -rf "$W/$n"; git clone -q --no-local "$S" "$W/$n"
done
for n in head-validate head-rv32 head-probe; do git -C "$W/$n" checkout -q --detach 61a504eec3ec3de828ccd80076212533ef58644b; done
git -C "$W/base-probe" checkout -q --detach 715589c1
for n in head-validate head-rv32 head-probe base-probe; do echo "$n $(git -C "$W/$n" rev-parse HEAD) $(git -C "$W/$n" rev-parse HEAD^{tree}) dirty=$(git -C "$W/$n" status --porcelain --untracked-files=all | wc -l)"; done
