/* SPDX-FileCopyrightText: 2026 Kebag Logic */
/* SPDX-License-Identifier: CERN-OHL-W-2.0 */
/* image_start.S - the measured image's reset entry (ctrl_image.py): the stack
 * at the top of block RAM, .bss cleared, then main. .data needs no copy: the
 * bitstream loads block RAM with the image. */
	.section .text.start, "ax"
	.global _start
_start:
	lla	sp, _stack_top
	lla	t0, _bss_start
	lla	t1, _bss_end
1:	bgeu	t0, t1, 2f
	sw	zero, 0(t0)
	addi	t0, t0, 4
	j	1b
2:	call	main
3:	j	3b
