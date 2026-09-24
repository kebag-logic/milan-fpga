	.file	"forge_semantics.c"
	.option pic
	.attribute arch, "rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0_zifencei2p0"
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.align	2
	.globl	mismatch
	.type	mismatch, @function
mismatch:
.LFB11:
	.cfi_startproc
	li	a5,1296650240
	addi	a5,a5,-946
	la	a4,csr_id
	mv	a0,a5
	lw	a4,0(a4)
	sub	a0,a0,a5
	snez	a0,a0
	ret
	.cfi_endproc
.LFE11:
	.size	mismatch, .-mismatch
	.ident	"GCC: (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0"
	.section	.note.GNU-stack,"",@progbits
