#!/usr/bin/env bash
S=<data>/tmp/pp185-a647; L=<data>/lanes/pp185-ctl
"$S/scripts/proc_gates.sh" "$L" "$S/r1b/head"
"$S/scripts/campaigns2.sh" "$L" "$S/r1b/head-campaigns" aecp_cmds name_state maap adp elab_guards
