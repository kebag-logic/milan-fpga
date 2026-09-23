#!/usr/bin/env bash
# Recreate the disposable inputs the packet scripts expect under scratch/:
# the reviewers' published probes (unmodified), the base sweep driver
# (483a133e, blob 2a02c7f3) and the warning-producing global Git config.
# Usage: prepare_scratch.sh CHECKOUT PACKET
set -eu
repo="$1"; packet="$2"; scratch="$packet/scratch"
mkdir -p "$scratch/review-probes" "$scratch/probe-tmp" "$scratch/devenv/git"
git -C "$repo" fetch -q origin 523-review-evidence
git -C "$repo" archive 4d13acca review-evidence/523-r1/reviews | tar -x -C "$scratch/review-probes"
git -C "$repo" show 483a133e:scripts/run_all_suites.sh > "$scratch/base-run_all_suites.sh"
git -C "$repo" show 483a133e:tb/verilator/gptp_shadow/mutants.py > "$scratch/base-mutants.py"
printf '[core]\n\tfsyncObjectFiles = true\n' > "$scratch/devenv/git/config"
