#!/usr/bin/env bash
# gate.sh <receipt-dir> <name> <workdir> <cmd...>: run one gate, recording its command (home and
# toolchain paths masked), start, end, log and rc
R=$1; n=$2; W=$3; shift 3
mkdir -p "$R"
echo "$*" | sed -e "s#$VALIDATION_TOOLS#<toolchain>#g" -e "s#$HOME#<home>#g" -e "s#$VALIDATION_STORAGE/scratch#<scratch>#g" > "$R/$n.cmd"
date +%s > "$R/$n.start"
(cd "$W" && "$@") > "$R/$n.log" 2>&1
rc=$?
echo $rc > "$R/$n.rc"; date +%s > "$R/$n.end"
echo "$n rc=$rc"
exit $rc
