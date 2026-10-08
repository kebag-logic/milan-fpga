/* SPDX-License-Identifier: CERN-OHL-W-2.0 */
/* Size-only flat RAM layout; board reset/vector/loader integration is separate. */
ENTRY(main)
SECTIONS {
    . = 0x10000000;
    __image_start = .;
    .text : { *(.text .text.*) }
    .rodata : { *(.rodata .rodata.* .srodata .srodata.*) }
    .data : { *(.data .data.* .sdata .sdata.* .got .got.*) }
    .bss (NOLOAD) : { *(.bss .bss.* .sbss .sbss.* COMMON) }
    . = ALIGN(16);
    .stack (NOLOAD) : { . += 8192; }
    __image_end = .;
    /DISCARD/ : { *(.eh_frame .eh_frame.* .comment) }
}
