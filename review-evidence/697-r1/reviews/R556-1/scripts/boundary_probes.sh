#!/bin/sh
# Usage: boundary_probes.sh <disposable-clone>
# Plants each probe at the top of src/adp.c, runs the boundary gate and a C11 compile.
cd "$1" || exit 2
probe() {
  git checkout -q -- src include
  printf '%s\n' "$2" | cat - src/adp.c > t && mv t src/adp.c
  python3 scripts/check_boundary.py > gate.out 2>&1; g=$?
  gcc -std=c11 -Wall -Wextra -Werror -Iinclude -c src/adp.c -o /dev/null > cc.out 2>&1; c=$?
  printf '%-28s gate_rc=%s compile_rc=%s\n' "$1" "$g" "$c"
}
probe control-hash-unistd '#include <unistd.h>'
probe control-mailbox '#include "mbx.h"'
probe digraph-unistd '%:include <unistd.h>'
probe digraph-pthread '%:include <pthread.h>'
probe stdio-allowed '#include <stdio.h>'
probe stdlib-allowed '#include <stdlib.h>'
probe heap-via-macro '#include <stdlib.h>
#define TSN_GET malloc
static void *probe_heap(void) { return TSN_GET (4); }
void *probe_heap_ref(void) { return probe_heap(); }'
probe heap-via-pointer '#include <stdlib.h>
void *(*const probe_alloc)(size_t) = malloc;'
git checkout -q -- src include
rm -f gate.out cc.out
git status --short
