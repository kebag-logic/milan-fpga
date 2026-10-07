/* SPDX-FileCopyrightText: 2026 Kebag Logic */
/* SPDX-License-Identifier: CERN-OHL-W-2.0 */
/* image.ld - the measured image in one block-RAM region (#640 D4 drops DDR3;
 * #665 6030870481 gives the firmware about 128 KB of it). The stack takes the
 * top of the region and is not part of the image. */
OUTPUT_ARCH(riscv)
ENTRY(_start)

MEMORY
{
	bram (rwx) : ORIGIN = 0x00000000, LENGTH = 128K
}

SECTIONS
{
	.text : { KEEP(*(.text.start)) *(.text .text.*) } > bram
	.rodata : ALIGN(4) { *(.rodata .rodata.* .srodata .srodata.*) } > bram
	.data : ALIGN(4) { *(.data .data.* .sdata .sdata.*) *(.got .got.plt) } > bram
	.bss (NOLOAD) : ALIGN(4)
	{
		_bss_start = .;
		*(.bss .bss.* .sbss .sbss.* COMMON)
		. = ALIGN(4);
		_bss_end = .;
	} > bram
	_stack_top = ORIGIN(bram) + LENGTH(bram);
	/DISCARD/ : { *(.comment) *(.note .note.*) *(.eh_frame .eh_frame.*) }
}
