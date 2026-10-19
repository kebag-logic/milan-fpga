#!/usr/bin/env bash
S=$VALIDATION_STORAGE/pp185-a647; L=$LANES/pp185-ctl
"$S/scripts/campaigns2.sh" "$L" "$S/r1b/head-campaigns" aecp_dispatch notify aecp ctr gsi name_wr acmp d3
