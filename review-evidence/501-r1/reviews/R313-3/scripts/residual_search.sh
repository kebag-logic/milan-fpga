#!/usr/bin/env bash
# Reviewer probe (R313-3): list every sentence in the current docs that names
# an owner or trigger for the capture-hold measurement, or restates the
# withdrawn "maps are not copied" premise.
# Usage: residual_search.sh <tree-root>
set -u
cd "$1" || exit 2
echo "head=$(git rev-parse HEAD)"
echo "--- capture-hold / #559 / withdrawn-obligation references"
grep -rn -i -E 'capture[- ]hold (measurement|obligation)|issues/559|#559|5823590638|5823589125|donor (acceptance )?obligation' docs README.md REQUIREMENTS.md
echo "--- withdrawn premise wording"
grep -rn -i -E 'maps are not (copied|materiali)|no materialized map copy|only BINDING is materiali' docs README.md REQUIREMENTS.md
echo "--- every processor #61/#83 obligation line"
grep -rn -E '#61/#83' docs README.md REQUIREMENTS.md
exit 0
