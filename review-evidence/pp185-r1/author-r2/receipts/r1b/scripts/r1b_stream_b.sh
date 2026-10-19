#!/usr/bin/env bash
S=<data>/tmp/pp185-a647; L=<data>/lanes/pp185-ctl
"$S/scripts/campaigns2.sh" "$L" "$S/r1b/head-campaigns" aecp_dispatch notify aecp ctr gsi name_wr acmp d3
