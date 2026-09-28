#!/usr/bin/env bash
# R368-3 probe: does a firmware archive linked --whole-archive with --gc-sections,
# whose init function is kept through a KEEP(.bios_init) table (as LiteX
# bios/linker.ld and init.h), fail by name when the BIOS lacks the 0006 marker?
# Usage: link_guard_rv32_probe.sh <workdir>
set -u
cd "$1"
CC="riscv64-elf-gcc -march=rv32i -mabi=ilp32 -Os -ffunction-sections -fdata-sections -nostdlib -nostartfiles"
cat > fw.c <<'C'
typedef void (*init_func)(void);
void bios_dispatch_hook_required(void);
void command_dispatch_hook(void);
static volatile int started;
static void nvm_boot(void) { bios_dispatch_hook_required(); started = 1; }
static void milan_init(void) { nvm_boot(); }
const init_func __bios_init_milan_init __attribute__((__used__)) __attribute__((__section__(".bios_init"))) = milan_init;
void command_dispatch_hook(void) { started = 2; }
C
for v in present missing; do
  if [ $v = present ]; then M='void bios_dispatch_hook_required(void){}'; else M=''; fi
  cat > main_$v.c <<C
typedef void (*init_func)(void);
extern init_func const __bios_init_start[]; extern init_func const __bios_init_end[];
void command_dispatch_hook(void);
void __attribute__((weak)) command_dispatch_hook(void) {}
$M
void _start(void) { for (const init_func *f = __bios_init_start; f != __bios_init_end; f++) (*f)(); for (;;) command_dispatch_hook(); }
C
done
cat > link.ld <<'L'
ENTRY(_start)
SECTIONS { . = 0x0; .text : { *(.text*) } .rodata : { PROVIDE_HIDDEN(__bios_init_start = .); KEEP(*(.bios_init)) PROVIDE_HIDDEN(__bios_init_end = .); *(.rodata*) *(.srodata*) } .data : { *(.data*) *(.sdata*) *(.sbss*) *(.bss*) } }
L
$CC -c fw.c -o fw.o && riscv64-elf-ar rcs libmilan_baremetal.a fw.o
for v in present missing; do
  $CC -c main_$v.c -o main_$v.o
  $CC -T link.ld -o $v.elf main_$v.o -L. -Wl,--start-group -Wl,--whole-archive -lmilan_baremetal -Wl,--no-whole-archive -Wl,--end-group -Wl,--gc-sections > $v.log 2>&1
  rc=$?
  echo "variant=$v rc=$rc undefined_marker=$(grep -c 'undefined reference to .bios_dispatch_hook_required' $v.log)"
  [ $rc = 0 ] && echo "  hook_resolved_to=$(riscv64-elf-nm $v.elf | grep -E ' command_dispatch_hook$')"
done
