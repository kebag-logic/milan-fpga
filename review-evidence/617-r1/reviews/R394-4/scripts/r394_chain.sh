#!/bin/sh
# R394-4: make -C <probe dir> -> recipe -> r394_chain.py (the committed mutants.build('dp') and
# makeflags_result()), under whichever `make` is first on PATH.
#   sh r394_chain.sh <suite-dir> <workdir>
set -eu
here=$(cd "$(dirname "$0")" && pwd)
suite=$(cd "$1" && pwd); work=$2
mkdir -p "$work/probe"
printf 'all:\n\tpython3 %s %s %s\n' "$here/r394_chain.py" "$suite" "$(cd "$work" && pwd)/w" > "$work/probe/Makefile"
echo "## make: $(make --version | head -1)"
env -u MAKEFLAGS -u MAKELEVEL -u MFLAGS make -C "$work/probe"
