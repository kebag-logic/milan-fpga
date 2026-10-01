#!/usr/bin/env bash
# Reviewer probe: in a disposable clone at the head, drop the
# aecp_dispatch_mutations line from .gitattributes and show that
# `git diff --check 0451d83d HEAD` then fails only on those patches.
# usage: attr_necessity_probe.sh <repo> <head> <scratch-dir>
set -uo pipefail
repo=$1; head=$2; work=$3/attr-probe
rm -rf "$work"; git clone -q "$repo" "$work"; cd "$work" || exit 1
git checkout -q "$head"
grep -v aecp_dispatch_mutations .gitattributes > .gitattributes.new && mv .gitattributes.new .gitattributes
git diff --check 0451d83d HEAD; echo "rc=$?"
