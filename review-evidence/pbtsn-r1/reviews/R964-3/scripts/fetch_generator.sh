#!/bin/sh
# Fetch the public descriptor generator at its pinned commit into an empty directory.
# Usage: fetch_generator.sh <empty-destination>
# Needs the `gh` client with read access to public repositories.  Fetches kebag-logic/milan-fpga at 58f7673b and
# two of its gitlinks: protocol-processor (801ef228), which the image builder imports from, and gptp-processor (1616fc8f).
# The gitlink ids are read from the milan-fpga tree, not assumed.
set -eu
dest=$1
mkdir -p "$dest"
[ -z "$(ls -A "$dest")" ] || { echo "destination must be empty" >&2; exit 2; }
commit=58f7673b8c57a80230e716bc1774ff9cc2f71ddc
gh api "repos/kebag-logic/milan-fpga/tarball/$commit" | tar -xz -C "$dest" --strip-components=1
link() { gh api "repos/kebag-logic/milan-fpga/git/trees/$commit" --jq ".tree[] | select(.path==\"$1\") | .sha"; }
pp=$(link protocol-processor)
gp=$(link gptp-processor)
gh api "repos/Mister-M-alt/protocol-processor-control-plane-avb-milan/tarball/$pp" | tar -xz -C "$dest/protocol-processor" --strip-components=1
gh api "repos/Mister-M-alt/FPGA-gPTP/tarball/$gp" | tar -xz -C "$dest/gptp-processor" --strip-components=1
echo "milan-fpga $commit; protocol-processor $pp; gptp-processor $gp"
