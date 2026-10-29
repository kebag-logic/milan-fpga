#!/usr/bin/env bash
cd <parent> || exit 2
date +%s > <runs>/ooc/ooc-head.start
env PATH=<tool>:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin ./syn/yosys/ooc.sh KL_pp_shadow > <runs>/ooc/ooc-head.log 2>&1
echo $? > <runs>/ooc/ooc-head.rc
date +%s > <runs>/ooc/ooc-head.end
