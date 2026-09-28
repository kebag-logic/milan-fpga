#!/bin/sh
# R369-3 reviewer probe (S5): the patch-0006 link marker under the product
# BIOS link shape (-ffunction-sections, --gc-sections, the firmware archive
# linked with --whole-archive). BIOS main.o is built with and without the
# marker; firmware references it (a) from code reached through a kept init
# table and (b) only from a function nothing calls, to show whether section
# garbage collection could hide the reference.
set -u
w=$1; mkdir -p "$w"; cd "$w" || exit 2
cat > bios_0006.c <<'C'
#include <stdio.h>
void bios_dispatch_hook_required(void) {}
void __attribute__((weak)) command_dispatch_hook(void) {}
extern void (*const fw_init)(void);
int main(void) { fw_init(); command_dispatch_hook(); puts("linked-and-ran"); return 0; }
C
cat > bios_no0006.c <<'C'
#include <stdio.h>
extern void (*const fw_init)(void);
int main(void) { fw_init(); puts("linked-and-ran"); return 0; }
C
cat > fw_reached.c <<'C'
void bios_dispatch_hook_required(void);
static void nvm_boot(void) { bios_dispatch_hook_required(); }
void (*const fw_init)(void) = nvm_boot;
void command_dispatch_hook(void) {}
C
cat > fw_unreached.c <<'C'
void bios_dispatch_hook_required(void);
void unused_path(void) { bios_dispatch_hook_required(); }
static void nvm_boot(void) {}
void (*const fw_init)(void) = nvm_boot;
void command_dispatch_hook(void) {}
C
for f in bios_0006 bios_no0006 fw_reached fw_unreached; do gcc -O1 -ffunction-sections -fdata-sections -c $f.c -o $f.o || exit 2; done
for fw in fw_reached fw_unreached; do
  rm -f lib$fw.a; ar rcs lib$fw.a $fw.o
  for bios in bios_0006 bios_no0006; do
    if gcc $bios.o -L. -Wl,--whole-archive -l$fw -Wl,--no-whole-archive -Wl,--gc-sections -o $bios-$fw 2> $bios-$fw.err; then
      printf '%s + %s: LINKED; ' "$bios" "$fw"; ./$bios-$fw
    else
      printf '%s + %s: LINK REFUSED: %s\n' "$bios" "$fw" "$(grep -o 'undefined reference to .bios_dispatch_hook_required.' $bios-$fw.err | head -1)"
    fi
  done
done
