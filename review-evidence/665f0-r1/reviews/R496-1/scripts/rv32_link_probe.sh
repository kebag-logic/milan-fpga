#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# rv32_link_probe.sh - reviewer probe for PR #668 (#665 F0).
# Compiles the portable firmware set and the MMIO platform with the PR's own
# RV32I freestanding flags, then LINKS a complete image with -nostdlib: a probe
# main (static ctrl_app, static arena, ctrl_app_start, ctrl_loop_run), a _start,
# and probe definitions of exactly memcpy, memset and vsnprintf, plus libgcc.
# A heap or OS dependency would surface as an undefined symbol at the link.
# usage: rv32_link_probe.sh <tree> <outdir>
set -u
T=$(cd "$1" && pwd); O=$2; mkdir -p "$O"
CC=$HOME/br-milan-rv32/host/bin/riscv32-linux-gcc; P=${CC%gcc}
F="-march=rv32i -mabi=ilp32 -ffreestanding -fno-stack-protector -Os -std=c11 -Wall -Wextra -Werror -pedantic -DCTRL_MBX_BASE=0x90100000u -ffunction-sections -fdata-sections"
C=$T/sw/firmware/ctrl
INC="-I$C/mbx -I$C/wire -I$C/port -I$C/loop -I$C/adp -I$C/app"
SRCS="mbx/mbx.c loop/ctrl_loop.c port/ctrl_pool.c port/ctrl_debug.c port/shlan_port.c adp/adp.c adp/adp_mbx.c app/ctrl_app.c plat/mbx_plat_mmio.c"
cat > "$O/probe_main.c" <<'EOF'
#include <stdarg.h>
#include <stddef.h>
#include "ctrl_app.h"
/* probe-only libc: exactly the three functions the PR names */
void *memcpy(void *d, const void *s, size_t n) { unsigned char *a = d; const unsigned char *b = s; while (n--) *a++ = *b++; return d; }
void *memset(void *d, int c, size_t n) { unsigned char *a = d; while (n--) *a++ = (unsigned char)c; return d; }
int vsnprintf(char *s, size_t n, const char *f, va_list ap) { (void)ap; size_t i = 0; while (f[i] && i + 1 < n) { s[i] = f[i]; i++; } if (n) s[i] = 0; return (int)i; }
static const struct adp_entity entity = { .entity_id = 0x020000FFFE000001ull };
static const struct ctrl_pool_class classes[] = { {64u, 32u}, {256u, 16u}, {1024u, 4u} };
static _Alignas(CTRL_POOL_ALIGN) unsigned char arena[64u * 32u + 256u * 16u + 1024u * 4u + 3u * 64u];
static struct ctrl_app app;
int main(void)
{
	struct ctrl_app_config cfg = { &entity, 0u, arena, sizeof arena, classes, 3u, NULL, NULL };
	if (!ctrl_app_start(&app, &cfg)) return 1;
	ctrl_loop_run(&app.loop);
	return 0;
}
void _start(void) { (void)main(); for (;;) { } }
EOF
objs=""
for s in $SRCS; do o="$O/$(basename "$s" .c).o"; "$CC" $F $INC -c "$C/$s" -o "$o" || exit 1; objs="$objs $o"; done
"$CC" $F $INC -c "$O/probe_main.c" -o "$O/probe_main.o" || exit 1
"$CC" -march=rv32i -mabi=ilp32 -nostdlib -nostartfiles -static -Wl,--gc-sections -Wl,-e,_start \
    -Wl,-Ttext=0x0 -o "$O/probe.elf" $objs "$O/probe_main.o" -lgcc > "$O/link.log" 2>&1
echo "link rc=$?"; cat "$O/link.log"
[ -f "$O/probe.elf" ] || exit 1
echo "undefined symbols in the linked image: $(${P}nm -u "$O/probe.elf" | wc -l)"
echo "heap/OS symbols (malloc calloc realloc free sbrk _sbrk brk mmap printf puts write): $(${P}nm "$O/probe.elf" | awk '{print $NF}' | grep -cxE 'malloc|calloc|realloc|free|sbrk|_sbrk|brk|mmap|printf|puts|write|_write')"
echo "sections:"; ${P}size -A "$O/probe.elf" | grep -vE '^\.(comment|riscv|debug)'
echo "firmware objects only (text data bss):"; ${P}size -t $objs | tail -1
echo "largest bss/data symbols:"; ${P}nm -S --size-sort "$O/probe.elf" | grep -iE ' [bBdD] ' | tail -8
