	.file	"clobber_repro.c"
	.option pic
	.attribute arch, "rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0_zifencei2p0"
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.align	2
	.type	milan_read, @function
milan_read:
.LFB0:
	.cfi_startproc
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	sw	a0,-20(s0)
	lw	a4,-20(s0)
	li	a5,-268435456
	add	a5,a4,a5
	lw	a5,0(a5)
	mv	a0,a5
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE0:
	.size	milan_read, .-milan_read
	.align	2
	.type	milan_clobber, @function
milan_clobber:
.LFB1:
	.cfi_startproc
	addi	sp,sp,-16
	.cfi_def_cfa_offset 16
	sw	ra,12(sp)
	sw	s0,8(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,16
	.cfi_def_cfa 8, 0
#APP
# 12 "$REVIEWS/544-r317-2-packet/receipts/clobber/clobber_repro.c" 1
	li s0, 0x4d494c4e
	li s1, 0x4d494c4e
# 0 "" 2
#NO_APP
	nop
	lw	ra,12(sp)
	.cfi_restore 1
	lw	s0,8(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 16
	addi	sp,sp,16
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE1:
	.size	milan_clobber, .-milan_clobber
	.section	.rodata
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
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	li	a0,0
	call	milan_read
	sw	a0,-20(s0)
	li	a0,4
	call	milan_read
	mv	a5,a0
	mv	a2,a5
	lw	a1,-20(s0)
	lla	a0,.LC0
	call	printf@plt
	call	milan_clobber
	lw	a4,-20(s0)
	li	a5,1296650240
	addi	a5,a5,-946
	beq	a4,a5,.L5
	lla	a0,.LC1
	call	printf@plt
	j	.L4
.L5:
	call	configure_fabric@plt
.L4:
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE2:
	.size	milan_init, .-milan_init
	.ident	"GCC: (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0"
	.section	.note.GNU-stack,"",@progbits
