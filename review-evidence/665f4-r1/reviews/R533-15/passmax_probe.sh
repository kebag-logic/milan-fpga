#!/usr/bin/env bash
# Print CTRL_APP_THREE_PASS_MAX / CTRL_APP_PASS_MAX / MAAP_MBX_PASS_MAX at MBX_N_IF=1 and 2 from a ctrl tree copy.
set -eu
CTRL=$1; S=$2
for n in 1 2; do
  rm -rf "$S/if$n"; cp -r "$CTRL" "$S/if$n"
  sed -i "s/^#define MBX_N_IF 1u$/#define MBX_N_IF ${n}u/" "$S/if$n/mbx/mbx_contract.h"
  incs=$(find "$S/if$n" -name '*.h' -printf '-I%h\n' | sort -u)
  printf '#include "ctrl_app.h"\n#include <stdio.h>\nint main(void){printf("IF=%%u three=%%u four=%%u maap=%%u\\n",(unsigned)MBX_N_IF,(unsigned)CTRL_APP_THREE_PASS_MAX,(unsigned)CTRL_APP_PASS_MAX,(unsigned)MAAP_MBX_PASS_MAX);return 0;}\n' > "$S/p$n.c"
  cc -std=c11 $incs "$S/p$n.c" -o "$S/p$n" && "$S/p$n"
done
