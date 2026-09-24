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
	la	a5,csr_id
	lw	a5,0(a5)
	li	a0,0
	ret
	.cfi_endproc
.LFE11:
	.size	mismatch, .-mismatch
	.ident	"GCC: (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0"
	.section	.note.GNU-stack,"",@progbits
