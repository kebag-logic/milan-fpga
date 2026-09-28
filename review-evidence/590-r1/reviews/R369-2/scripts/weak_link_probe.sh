#!/bin/sh
# Reviewer probe: a weak BIOS hook in main.o, the strong product hook in a
# library linked with --whole-archive (LiteX ALWAYS_LINK_LIBS), and the same
# library linked without it. Prints which definition the dispatch call reaches.
set -eu
w=$1; mkdir -p "$w"; cd "$w"
cat > main.c <<'C'
#include <stdio.h>
int hook_owner;
void __attribute__((weak)) command_dispatch_hook(void) { hook_owner = 0; }
int main(void) { hook_owner = -1; command_dispatch_hook(); printf("hook_owner=%d\n", hook_owner); return 0; }
C
cat > fw.c <<'C'
extern int hook_owner;
void command_dispatch_hook(void) { hook_owner = 1; }
int fw_command_table_entry = 7; /* pulled by whole-archive, as define_command sections are */
C
gcc -c main.c fw.c
ar rcs libmilan_baremetal.a fw.o
gcc main.o -L. -Wl,--whole-archive -lmilan_baremetal -Wl,--no-whole-archive -o whole
gcc main.o -L. -lmilan_baremetal -o plain
printf 'whole-archive: '; ./whole
printf 'plain archive (member not otherwise referenced): '; ./plain
