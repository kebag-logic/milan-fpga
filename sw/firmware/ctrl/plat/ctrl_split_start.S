/* SPDX-FileCopyrightText: 2026 Kebag Logic */
/* SPDX-License-Identifier: CERN-OHL-W-2.0 */
/* ctrl_split_start.S - the control firmware's reset entry in the split
 * placement (#640 M8a, ctrl_split.ld). No BIOS runs first: the stack goes at
 * the top of its reservation, .data is copied from its initial values in rom
 * and .bss is cleared, so a CPU reset re-enters with the state of power-on.
 * Then main; a return from it parks the hart. */
	.section .text.start, "ax"
	.global _start
_start:
	lla	sp, _stack_top
	lla	t0, _fdata_rom
	lla	t1, _fdata
	lla	t2, _edata
1:	bgeu	t1, t2, 2f
	lw	t3, 0(t0)
	sw	t3, 0(t1)
	addi	t0, t0, 4
	addi	t1, t1, 4
	j	1b
2:	lla	t0, _fbss
	lla	t1, _ebss
3:	bgeu	t0, t1, 4f
	sw	zero, 0(t0)
	addi	t0, t0, 4
	j	3b
4:	call	main
5:	j	5b
