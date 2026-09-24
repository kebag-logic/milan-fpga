	.file	"nest.c"
	.option pic
	.attribute arch, "rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0_zifencei2p0"
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.align	2
	.globl	f
	.type	f, @function
f:
.LFB0:
	.cfi_startproc
	li	a5,-1879048192
	li	a4,1
	sw	a4,1536(a5)
	ret
	.cfi_endproc
.LFE0:
	.size	f, .-f
	.ident	"GCC: (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0"
	.section	.note.GNU-stack,"",@progbits
