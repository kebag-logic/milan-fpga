#!/usr/bin/env bash
# Removed adapter ops / events and in-processor counter nodes still named in the docs.
# Usage: stale_names.sh <clone>
cd "$1" || exit 1
git grep -nE "READ_AS_PATH|INPUT_CONFIGURE|INPUT_ENABLE|INPUT_DISABLE|INPUT_START|INPUT_STOP|OUTPUT_STATUS|OUTPUT_SET_PT_OFFSET|SET_INPUT_FORMAT|SET_OUTPUT_FORMAT|GET_MCR_DEFAULTS|MC_LOCKED|AS_CAPABLE_CHANGE|PATH_CHANGE|gm_changed_tick|adp_gm_tick|mclk\.SET|avtp\.INPUT|avtp adapters|mclk adapters|ctrs\[\"counters\"\]|adapters --> ctrs|events to counters" -- docs hdl tb ':!docs/00_MILAN_COMPLIANCE_REVIEW.md' | cut -c1-240
