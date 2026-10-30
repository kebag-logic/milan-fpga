#!/usr/bin/env bash
cd <parent> || exit 2
date +%s > <parent-runs>/ooc/ooc-head.start
env PATH=<tool>/sv2v-v0.0.12:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin ./syn/yosys/ooc.sh KL_pp_shadow > <parent-runs>/ooc/ooc-head.log 2>&1
echo $? > <parent-runs>/ooc/ooc-head.rc
date +%s > <parent-runs>/ooc/ooc-head.end
