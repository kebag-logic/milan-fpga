#!/bin/sh
# [R383] Redact local absolute paths and the host name from a receipt (stdin -> stdout).
# Packet dir = this script's directory; tree = $R383_TREE (default: current directory).
# Temporary-directory prefixes are shown as <tmp>/.
packet=$(cd "$(dirname "$0")" && pwd); tree=${R383_TREE:-$(pwd)}
sed -e "s#$packet#<packet>#g" -e "s#$tree#<tree>#g" \
    -e "s#$HOME#<home>#g" -e "s#$(hostname)#<host>#g" -e "s#/tmp/#<tmp>/#g"
