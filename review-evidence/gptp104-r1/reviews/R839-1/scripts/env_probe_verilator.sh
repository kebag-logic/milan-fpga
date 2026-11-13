#!/bin/sh
# Stand-in for $(VERILATOR) in the engine Makefile's real `run` recipe:
# prints the OBJCACHE/CCACHE_* environment that recipe hands Verilator,
# then exits 3 so the recipe stops before anything is built.
printenv | grep -E '^(OBJCACHE|CCACHE_)' | sort | sed 's/^/  run recipe: /'
printf '  run recipe: OBJCACHE is [%s]\n' "${OBJCACHE-UNSET}"
exit 3
