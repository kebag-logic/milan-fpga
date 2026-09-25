	.file	"clobber_repro.c"
	.option pic
	.attribute arch, "rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0_zifencei2p0"
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.align	2
	.type	milan_clobber, @function
milan_clobber:
.LFB1:
	.cfi_startproc
#APP
# 12 "$REVIEWS/544-r317-2-packet/receipts/clobber/clobber_repro.c" 1
	li s0, 0x4d494c4e
	li s1, 0x4d494c4e
# 0 "" 2
#NO_APP
	ret
	.cfi_endproc
.LFE1:
	.size	milan_clobber, .-milan_clobber
	.section	.rodata.str1.4,"aMS",@progbits,1
	.align	2
.LC0:
	.string	"CSR ID=%08lx VERSION=%08lx\n"
	.align	2
.LC1:
	.string	"mismatch\n"
	.text
	.align	2
	.globl	milan_init
	.type	milan_init, @function
milan_init:
.LFB2:
	.cfi_startproc
	li	a5,-268435456
	addi	sp,sp,-16
	.cfi_def_cfa_offset 16
	sw	s0,8(sp)
	.cfi_offset 8, -8
	lw	s0,0(a5)
	lw	a2,4(a5)
	lla	a0,.LC0
	mv	a1,s0
	sw	ra,12(sp)
	.cfi_offset 1, -4
	call	printf@plt
	call	milan_clobber
	li	a5,1296650240
	addi	a5,a5,-946
	beq	s0,a5,.L4
	lw	s0,8(sp)
	.cfi_remember_state
	.cfi_restore 8
	lw	ra,12(sp)
	.cfi_restore 1
	lla	a0,.LC1
	addi	sp,sp,16
	.cfi_def_cfa_offset 0
	tail	printf@plt
.L4:
	.cfi_restore_state
	lw	s0,8(sp)
	.cfi_restore 8
	lw	ra,12(sp)
	.cfi_restore 1
	addi	sp,sp,16
	.cfi_def_cfa_offset 0
	tail	configure_fabric@plt
	.cfi_endproc
.LFE2:
	.size	milan_init, .-milan_init
	.ident	"GCC: (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0"
	.section	.note.GNU-stack,"",@progbits
