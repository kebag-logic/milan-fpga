#!/bin/bash
# baremetal.py on a clean clone of COMMIT. usage: rv32_at.sh COMMIT OUT
set -u
C=$1 O=$2
. <scratch>/scripts/env.sh
rm -rf "$O"; mkdir -p "$O"
git clone -q --no-local <lanes>/tsn-c-stack-32-walk "$O/src" && git -C "$O/src" checkout -q --detach "$C" || exit 3
cd "$O/src" && python3 scripts/baremetal.py --work "$O/build-rv32" --jobs 16 > "$O/baremetal.log" 2>&1; echo $? > "$O/baremetal.rc"
