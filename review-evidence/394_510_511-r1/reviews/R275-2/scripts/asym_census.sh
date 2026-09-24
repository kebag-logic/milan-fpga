#!/usr/bin/env bash
# Census of delayAsymmetry-like identifiers in the parent product tree and the
# pinned gPTP processor, at the exact head under review. Read-only.
# Usage: asym_census.sh <parent-checkout>
set -u
repo=${1:?parent checkout}
cd "$repo" || exit 2
echo "# head $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
pin=$(git ls-files -s gptp-processor | awk '{print $2}')
echo "# gptp-processor gitlink $pin; checkout $(git -C gptp-processor rev-parse HEAD)"
echo "## parent: identifier-shaped asymmetry names in hdl sw configs avdecc scripts tb (no svg)"
git grep -n -I -i -E 'delay_?asym|asym_|cfg_asym|asymmetry_ns|delayasymmetry' -- hdl sw configs avdecc scripts tb ':!*.svg'
echo "exit=$?"
echo "## parent: builder gptp key whitelist (_known_gp)"
git grep -n -E '_known_gp' -- sw/builder
echo "exit=$?"
echo "## gptp-processor pinned commit: files naming asym (any case), svg excluded"
git -C gptp-processor grep -I -i -l 'asym' "$pin" -- . ':!*.svg'
echo "exit=$?"
echo "## gptp-processor pinned commit: asym in hdl syn scripts tb bench Makefile"
git -C gptp-processor grep -n -I -i 'asym' "$pin" -- hdl syn scripts tb bench Makefile
echo "exit=$?"
