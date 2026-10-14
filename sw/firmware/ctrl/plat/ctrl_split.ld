/* SPDX-FileCopyrightText: 2026 Kebag Logic */
/* SPDX-License-Identifier: CERN-OHL-W-2.0 */
/* ctrl_split.ld - the control firmware in the split placement's block RAM
 * (#640 M8a). The firmware owns the reset entry: _start is the first word of
 * rom, the CPU's reset address. rom holds the load image (.text, .rodata and
 * the initial values of .data); sram holds .data, .bss and the stack.
 * regions.ld is sw/litex/ctrl_memory.py's, the one statement of the map, and
 * the SoC sizes both regions' block RAM from the image this script links. */
OUTPUT_ARCH(riscv)
ENTRY(_start)
INCLUDE regions.ld

SECTIONS
{
	.text : { KEEP(*(.text.start)) *(.text .text.*) } > rom
	.rodata : ALIGN(4) { *(.rodata .rodata.* .srodata .srodata.*) } > rom
	.data : ALIGN(4)
	{
		_fdata = .;
		*(.data .data.* .sdata .sdata.*) *(.got .got.plt)
		. = ALIGN(4);
		_edata = .;
	} > sram AT > rom
	_fdata_rom = LOADADDR(.data);
	.bss (NOLOAD) : ALIGN(4)
	{
		_fbss = .;
		*(.bss .bss.* .sbss .sbss.* COMMON)
		. = ALIGN(4);
		_ebss = .;
	} > sram
	.stack (NOLOAD) : ALIGN(16)
	{
		. += 8192;
		_stack_top = .;
	} > sram
	/DISCARD/ : { *(.comment) *(.note .note.*) *(.eh_frame .eh_frame.*) }
}
