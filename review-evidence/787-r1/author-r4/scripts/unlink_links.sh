#!/usr/bin/env bash
# Remove the route clone's three artifact links after every Vivado run has ended.
# usage: unlink_links.sh <repo>
set -u
cd "$1" || exit 2
[ -L sw/builder/out ] && unlink sw/builder/out
[ -L configs/generated/ltn_rom.hex ] && unlink configs/generated/ltn_rom.hex
[ -L configs/generated/ucode.hex ] && unlink configs/generated/ucode.hex
git status --short
