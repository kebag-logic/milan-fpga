	.file	"milan_baremetal.c"
	.option pic
	.attribute arch, "rv32i2p1_m2p0_a2p1_zicsr2p0_zifencei2p0"
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.local	aem_loaded
	.comm	aem_loaded,4,4
	.globl	aem_view
	.set	aem_view,aem_loaded
	.align	2
	.type	milan_reg, @function
milan_reg:
.LFB6:
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
	li	a5,-1879048192
	add	a5,a4,a5
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
.LFE6:
	.size	milan_reg, .-milan_reg
	.align	2
	.type	milan_read, @function
milan_read:
.LFB7:
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
	lw	a0,-20(s0)
	call	milan_reg
	mv	a5,a0
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
.LFE7:
	.size	milan_read, .-milan_read
	.align	2
	.type	milan_write, @function
milan_write:
.LFB8:
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
	sw	a1,-24(s0)
	lw	a0,-20(s0)
	call	milan_reg
	mv	a4,a0
	lw	a5,-24(s0)
	sw	a5,0(a4)
#APP
# 76 "/tmp/milan-census-s8bsel5_/milan_baremetal.c" 1
	fence iorw, iorw
# 0 "" 2
#NO_APP
	nop
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE8:
	.size	milan_write, .-milan_write
	.section	.rodata
	.align	2
.LC0:
	.string	"TAI_NS=0x%08lx%08lx\n"
	.text
	.align	2
	.type	print_tod, @function
print_tod:
.LFB9:
	.cfi_startproc
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	sw	a0,-24(s0)
	sw	a1,-20(s0)
	lw	a3,-20(s0)
	srli	a4,a3,0
	li	a5,0
	lw	a5,-24(s0)
	mv	a2,a5
	mv	a1,a4
	lla	a0,.LC0
	call	printf@plt
	nop
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE9:
	.size	print_tod, .-print_tod
	.align	2
	.type	gettime_ns, @function
gettime_ns:
.LFB10:
	.cfi_startproc
	addi	sp,sp,-64
	.cfi_def_cfa_offset 64
	sw	ra,60(sp)
	sw	s0,56(sp)
	sw	s2,52(sp)
	sw	s3,48(sp)
	sw	s4,44(sp)
	sw	s5,40(sp)
	sw	s6,36(sp)
	sw	s7,32(sp)
	sw	s8,28(sp)
	sw	s9,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	.cfi_offset 18, -12
	.cfi_offset 19, -16
	.cfi_offset 20, -20
	.cfi_offset 21, -24
	.cfi_offset 22, -28
	.cfi_offset 23, -32
	.cfi_offset 24, -36
	.cfi_offset 25, -40
	addi	s0,sp,64
	.cfi_def_cfa 8, 0
	li	a1,4
	li	a0,1312
	call	milan_write
	li	a0,128
	call	cdelay@plt
.L8:
	li	a0,1332
	call	milan_read
	sw	a0,-60(s0)
	li	a0,1328
	call	milan_read
	sw	a0,-56(s0)
	li	a0,1332
	call	milan_read
	sw	a0,-52(s0)
	lw	a4,-60(s0)
	lw	a5,-52(s0)
	bne	a4,a5,.L8
	lw	a5,-52(s0)
	mv	s8,a5
	li	s9,0
	slli	s3,s8,0
	li	s2,0
	lw	a5,-56(s0)
	mv	s4,a5
	li	s5,0
	or	s6,s2,s4
	or	s7,s3,s5
	mv	a4,s6
	mv	a5,s7
	mv	a0,a4
	mv	a1,a5
	lw	ra,60(sp)
	.cfi_restore 1
	lw	s0,56(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 64
	lw	s2,52(sp)
	.cfi_restore 18
	lw	s3,48(sp)
	.cfi_restore 19
	lw	s4,44(sp)
	.cfi_restore 20
	lw	s5,40(sp)
	.cfi_restore 21
	lw	s6,36(sp)
	.cfi_restore 22
	lw	s7,32(sp)
	.cfi_restore 23
	lw	s8,28(sp)
	.cfi_restore 24
	lw	s9,24(sp)
	.cfi_restore 25
	addi	sp,sp,64
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE10:
	.size	gettime_ns, .-gettime_ns
	.align	2
	.type	settime_ns, @function
settime_ns:
.LFB11:
	.cfi_startproc
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	sw	s2,20(sp)
	sw	s3,16(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	.cfi_offset 18, -12
	.cfi_offset 19, -16
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	sw	a0,-24(s0)
	sw	a1,-20(s0)
	lw	a5,-24(s0)
	mv	a1,a5
	li	a0,1296
	call	milan_write
	lw	a5,-20(s0)
	srli	s2,a5,0
	li	s3,0
	mv	a5,s2
	mv	a1,a5
	li	a0,1300
	call	milan_write
	li	a1,1
	li	a0,1312
	call	milan_write
	nop
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	lw	s2,20(sp)
	.cfi_restore 18
	lw	s3,16(sp)
	.cfi_restore 19
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE11:
	.size	settime_ns, .-settime_ns
	.align	2
	.type	parse_u64, @function
parse_u64:
.LFB12:
	.cfi_startproc
	addi	sp,sp,-64
	.cfi_def_cfa_offset 64
	sw	ra,60(sp)
	sw	s0,56(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,64
	.cfi_def_cfa 8, 0
	sw	a0,-52(s0)
	sw	a1,-56(s0)
	la	a5,__stack_chk_guard
	lw	a4, 0(a5)
	sw	a4, -20(s0)
	li	a4, 0
	call	__errno_location@plt
	mv	a5,a0
	sw	zero,0(a5)
	addi	a5,s0,-36
	li	a2,0
	mv	a1,a5
	lw	a0,-52(s0)
	call	strtoull@plt
	sw	a0,-32(s0)
	sw	a1,-28(s0)
	call	__errno_location@plt
	mv	a5,a0
	lw	a4,0(a5)
	li	a5,34
	beq	a4,a5,.L12
	lw	a5,-52(s0)
	lbu	a5,0(a5)
	beq	a5,zero,.L12
	lw	a5,-36(s0)
	lbu	a5,0(a5)
	beq	a5,zero,.L13
.L12:
	li	a5,0
	j	.L15
.L13:
	lw	a3,-56(s0)
	lw	a4,-32(s0)
	lw	a5,-28(s0)
	sw	a4,0(a3)
	sw	a5,4(a3)
	li	a5,1
.L15:
	mv	a4,a5
	la	a5,__stack_chk_guard
	lw	a3, -20(s0)
	lw	a5, 0(a5)
	xor	a5, a3, a5
	li	a3, 0
	beq	a5,zero,.L16
	call	__stack_chk_fail@plt
.L16:
	mv	a0,a4
	lw	ra,60(sp)
	.cfi_restore 1
	lw	s0,56(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 64
	addi	sp,sp,64
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE12:
	.size	parse_u64, .-parse_u64
	.align	2
	.type	seconds_to_ns, @function
seconds_to_ns:
.LFB13:
	.cfi_startproc
	addi	sp,sp,-48
	.cfi_def_cfa_offset 48
	sw	ra,44(sp)
	sw	s0,40(sp)
	sw	s2,36(sp)
	sw	s3,32(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	.cfi_offset 18, -12
	.cfi_offset 19, -16
	addi	s0,sp,48
	.cfi_def_cfa 8, 0
	sw	a0,-24(s0)
	sw	a1,-20(s0)
	sw	a2,-32(s0)
	sw	a3,-28(s0)
	sw	a4,-36(s0)
	lw	a5,-28(s0)
	bne	a5,zero,.L18
	lw	a5,-28(s0)
	bne	a5,zero,.L23
	lw	a4,-32(s0)
	li	a5,1000001536
	addi	a5,a5,-1537
	bgtu	a4,a5,.L18
.L23:
	lw	a5,-32(s0)
	not	a6,a5
	lw	a5,-28(s0)
	not	a7,a5
	li	a2,1000001536
	addi	a2,a2,-1536
	li	a3,0
	mv	a0,a6
	mv	a1,a7
	call	__udivdi3@plt
	mv	a4,a0
	mv	a5,a1
	lw	a3,-20(s0)
	mv	a2,a5
	bgtu	a3,a2,.L18
	lw	a3,-20(s0)
	mv	a2,a5
	bne	a3,a2,.L20
	lw	a3,-24(s0)
	mv	a5,a4
	bleu	a3,a5,.L20
.L18:
	li	a5,0
	j	.L22
.L20:
	lw	a4,-20(s0)
	li	a5,1000001536
	addi	a5,a5,-1536
	mul	a4,a4,a5
	lw	a5,-24(s0)
	li	a3,0
	mul	a5,a5,a3
	add	a3,a4,a5
	lw	a4,-24(s0)
	li	a5,1000001536
	addi	a5,a5,-1536
	mul	a2,a4,a5
	mulhu	s3,a4,a5
	mv	s2,a2
	add	a5,a3,s3
	mv	s3,a5
	lw	a2,-32(s0)
	lw	a3,-28(s0)
	add	a4,s2,a2
	mv	a1,a4
	sltu	a1,a1,s2
	add	a5,s3,a3
	add	a3,a1,a5
	mv	a5,a3
	lw	a3,-36(s0)
	sw	a4,0(a3)
	sw	a5,4(a3)
	li	a5,1
.L22:
	mv	a0,a5
	lw	ra,44(sp)
	.cfi_restore 1
	lw	s0,40(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 48
	lw	s2,36(sp)
	.cfi_restore 18
	lw	s3,32(sp)
	.cfi_restore 19
	addi	sp,sp,48
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE13:
	.size	seconds_to_ns, .-seconds_to_ns
	.section	.rodata
	.align	2
	.type	nvm_mapin_entries, @object
	.size	nvm_mapin_entries, 16
nvm_mapin_entries:
	.zero	16
	.align	2
	.type	nvm_mapout_entries, @object
	.size	nvm_mapout_entries, 16
nvm_mapout_entries:
	.string	"\021"
	.string	""
	.string	""
	.string	""
	.string	""
	.string	""
	.string	""
	.string	""
	.string	""
	.string	""
	.string	""
	.string	""
	.string	""
	.string	""
	.string	""
	.align	2
	.type	nvm_blocks, @object
	.size	nvm_blocks, 72
nvm_blocks:
	.byte	0
	.byte	1
	.byte	0
	.zero	1
	.half	2
	.byte	1
	.byte	1
	.byte	0
	.zero	1
	.half	8
	.byte	2
	.byte	1
	.byte	0
	.zero	1
	.half	4
	.byte	10
	.byte	1
	.byte	0
	.zero	1
	.half	2
	.byte	18
	.byte	1
	.byte	0
	.zero	1
	.half	66
	.byte	32
	.byte	2
	.byte	0
	.zero	1
	.half	20
	.byte	48
	.byte	2
	.byte	0
	.zero	1
	.half	8
	.byte	64
	.byte	2
	.byte	0
	.zero	1
	.half	8
	.byte	80
	.byte	2
	.byte	0
	.zero	1
	.half	4
	.byte	96
	.byte	1
	.byte	1
	.zero	1
	.half	0
	.byte	112
	.byte	1
	.byte	2
	.zero	1
	.half	0
	.byte	-128
	.byte	31
	.byte	0
	.zero	1
	.half	64
	.align	2
.LC1:
	.string	"VD_OK"
	.align	2
.LC2:
	.string	"VD_MAGIC"
	.align	2
.LC3:
	.string	"VD_VER"
	.align	2
.LC4:
	.string	"VD_LEN"
	.align	2
.LC5:
	.string	"VD_CRC"
	.align	2
.LC6:
	.string	"VD_ENT"
	.align	2
.LC7:
	.string	"VD_SHAPE"
	.align	2
.LC8:
	.string	"VD_REC"
	.align	2
.LC9:
	.string	"VD_STALE"
	.align	2
.LC10:
	.string	"VD_BLANK"
	.align	2
.LC11:
	.string	"VD_INCOMPLETE"
	.align	2
.LC12:
	.string	"VD_ERASE"
	.align	2
.LC13:
	.string	"VD_PROGRAM"
	.align	2
.LC14:
	.string	"VD_VERIFY"
	.section	.data.rel.ro.local,"aw"
	.align	2
	.type	nvm_verdict_name, @object
	.size	nvm_verdict_name, 56
nvm_verdict_name:
	.word	.LC1
	.word	.LC2
	.word	.LC3
	.word	.LC4
	.word	.LC5
	.word	.LC6
	.word	.LC7
	.word	.LC8
	.word	.LC9
	.word	.LC10
	.word	.LC11
	.word	.LC12
	.word	.LC13
	.word	.LC14
	.local	nvm_started
	.comm	nvm_started,4,4
	.local	nvm_ready
	.comm	nvm_ready,4,4
	.local	nvm_retired
	.comm	nvm_retired,4,4
	.local	nvm_in_commit
	.comm	nvm_in_commit,4,4
	.local	nvm_seq
	.comm	nvm_seq,4,4
	.data
	.align	2
	.type	nvm_auth_slot, @object
	.size	nvm_auth_slot, 4
nvm_auth_slot:
	.word	-1
	.local	nvm_verdict_a
	.comm	nvm_verdict_a,4,4
	.local	nvm_verdict_b
	.comm	nvm_verdict_b,4,4
	.local	nvm_last_verdict
	.comm	nvm_last_verdict,4,4
	.local	nvm_commits_ok
	.comm	nvm_commits_ok,4,4
	.local	nvm_commits_failed
	.comm	nvm_commits_failed,4,4
	.local	nvm_captures_refused
	.comm	nvm_captures_refused,4,4
	.local	nvm_acks_refused
	.comm	nvm_acks_refused,4,4
	.local	nvm_hb_last
	.comm	nvm_hb_last,8,8
	.local	nvm_dirty_since
	.comm	nvm_dirty_since,8,8
	.text
	.align	2
	.type	nvm_slot, @function
nvm_slot:
.LFB14:
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
	li	a5,536870912
	add	a5,a4,a5
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
.LFE14:
	.size	nvm_slot, .-nvm_slot
	.align	2
	.type	nvm_rd32, @function
nvm_rd32:
.LFB15:
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
	lw	a5,-20(s0)
	lbu	a5,0(a5)
	andi	a5,a5,0xff
	mv	a4,a5
	lw	a5,-20(s0)
	addi	a5,a5,1
	lbu	a5,0(a5)
	andi	a5,a5,0xff
	slli	a5,a5,8
	or	a4,a4,a5
	lw	a5,-20(s0)
	addi	a5,a5,2
	lbu	a5,0(a5)
	andi	a5,a5,0xff
	slli	a5,a5,16
	or	a4,a4,a5
	lw	a5,-20(s0)
	addi	a5,a5,3
	lbu	a5,0(a5)
	andi	a5,a5,0xff
	slli	a5,a5,24
	or	a5,a4,a5
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
.LFE15:
	.size	nvm_rd32, .-nvm_rd32
	.align	2
	.type	nvm_crc32, @function
nvm_crc32:
.LFB16:
	.cfi_startproc
	addi	sp,sp,-48
	.cfi_def_cfa_offset 48
	sw	ra,44(sp)
	sw	s0,40(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,48
	.cfi_def_cfa 8, 0
	sw	a0,-36(s0)
	sw	a1,-40(s0)
	li	a5,-1
	sw	a5,-28(s0)
	sw	zero,-24(s0)
	j	.L29
.L33:
	lla	a5,nvm_ready
	lw	a5,0(a5)
	beq	a5,zero,.L30
	lw	a5,-24(s0)
	andi	a5,a5,255
	bne	a5,zero,.L30
	call	nvm_heartbeat_tick
.L30:
	lw	a4,-36(s0)
	lw	a5,-24(s0)
	add	a5,a4,a5
	lbu	a5,0(a5)
	andi	a5,a5,0xff
	mv	a4,a5
	lw	a5,-28(s0)
	xor	a5,a5,a4
	sw	a5,-28(s0)
	sw	zero,-20(s0)
	j	.L31
.L32:
	lw	a5,-28(s0)
	srli	a4,a5,1
	lw	a5,-28(s0)
	andi	a5,a5,1
	neg	a3,a5
	li	a5,-306675712
	addi	a5,a5,800
	and	a5,a3,a5
	xor	a5,a4,a5
	sw	a5,-28(s0)
	lw	a5,-20(s0)
	addi	a5,a5,1
	sw	a5,-20(s0)
.L31:
	lw	a4,-20(s0)
	li	a5,7
	bleu	a4,a5,.L32
	lw	a5,-24(s0)
	addi	a5,a5,1
	sw	a5,-24(s0)
.L29:
	lw	a4,-24(s0)
	lw	a5,-40(s0)
	bltu	a4,a5,.L33
	lw	a5,-28(s0)
	not	a5,a5
	mv	a0,a5
	lw	ra,44(sp)
	.cfi_restore 1
	lw	s0,40(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 48
	addi	sp,sp,48
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE16:
	.size	nvm_crc32, .-nvm_crc32
	.align	2
	.type	nvm_crc16, @function
nvm_crc16:
.LFB17:
	.cfi_startproc
	addi	sp,sp,-48
	.cfi_def_cfa_offset 48
	sw	ra,44(sp)
	sw	s0,40(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,48
	.cfi_def_cfa 8, 0
	sw	a0,-36(s0)
	sw	a1,-40(s0)
	mv	a5,a2
	sh	a5,-42(s0)
	sw	zero,-24(s0)
	j	.L36
.L41:
	lw	a4,-36(s0)
	lw	a5,-24(s0)
	add	a5,a4,a5
	lbu	a5,0(a5)
	andi	a5,a5,0xff
	slli	a5,a5,8
	slli	a5,a5,16
	srli	a5,a5,16
	lhu	a4,-42(s0)
	xor	a5,a5,a4
	sh	a5,-42(s0)
	sw	zero,-20(s0)
	j	.L37
.L40:
	lh	a5,-42(s0)
	bge	a5,zero,.L38
	lhu	a5,-42(s0)
	slli	a5,a5,1
	slli	a4,a5,16
	srli	a4,a4,16
	li	a5,4096
	addi	a5,a5,33
	xor	a5,a4,a5
	slli	a5,a5,16
	srli	a5,a5,16
	j	.L39
.L38:
	lhu	a5,-42(s0)
	slli	a5,a5,1
	slli	a5,a5,16
	srli	a5,a5,16
.L39:
	sh	a5,-42(s0)
	lw	a5,-20(s0)
	addi	a5,a5,1
	sw	a5,-20(s0)
.L37:
	lw	a4,-20(s0)
	li	a5,7
	bleu	a4,a5,.L40
	lw	a5,-24(s0)
	addi	a5,a5,1
	sw	a5,-24(s0)
.L36:
	lw	a4,-24(s0)
	lw	a5,-40(s0)
	bltu	a4,a5,.L41
	lhu	a5,-42(s0)
	mv	a0,a5
	lw	ra,44(sp)
	.cfi_restore 1
	lw	s0,40(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 48
	addi	sp,sp,48
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE17:
	.size	nvm_crc16, .-nvm_crc16
	.align	2
	.type	nvm_all_erased, @function
nvm_all_erased:
.LFB18:
	.cfi_startproc
	addi	sp,sp,-48
	.cfi_def_cfa_offset 48
	sw	ra,44(sp)
	sw	s0,40(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,48
	.cfi_def_cfa 8, 0
	sw	a0,-36(s0)
	sw	a1,-40(s0)
	sw	zero,-20(s0)
	j	.L44
.L47:
	lw	a4,-36(s0)
	lw	a5,-20(s0)
	add	a5,a4,a5
	lbu	a5,0(a5)
	andi	a4,a5,0xff
	li	a5,255
	beq	a4,a5,.L45
	li	a5,0
	j	.L46
.L45:
	lw	a5,-20(s0)
	addi	a5,a5,1
	sw	a5,-20(s0)
.L44:
	lw	a4,-20(s0)
	lw	a5,-40(s0)
	bltu	a4,a5,.L47
	li	a5,1
.L46:
	mv	a0,a5
	lw	ra,44(sp)
	.cfi_restore 1
	lw	s0,40(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 48
	addi	sp,sp,48
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE18:
	.size	nvm_all_erased, .-nvm_all_erased
	.align	2
	.type	nvm_block_plen, @function
nvm_block_plen:
.LFB19:
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
	sw	a1,-24(s0)
	lw	a5,-20(s0)
	lbu	a4,2(a5)
	li	a5,1
	bne	a4,a5,.L49
	lw	a5,-24(s0)
	andi	a5,a5,15
	lla	a4,nvm_mapin_entries
	add	a5,a4,a5
	lbu	a5,0(a5)
	slli	a5,a5,3
	j	.L50
.L49:
	lw	a5,-20(s0)
	lbu	a4,2(a5)
	li	a5,2
	bne	a4,a5,.L51
	lw	a5,-24(s0)
	andi	a5,a5,15
	lla	a4,nvm_mapout_entries
	add	a5,a4,a5
	lbu	a5,0(a5)
	slli	a5,a5,3
	j	.L50
.L51:
	lw	a5,-20(s0)
	lhu	a5,4(a5)
.L50:
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
.LFE19:
	.size	nvm_block_plen, .-nvm_block_plen
	.align	2
	.type	nvm_rec_after, @function
nvm_rec_after:
.LFB20:
	.cfi_startproc
	addi	sp,sp,-64
	.cfi_def_cfa_offset 64
	sw	ra,60(sp)
	sw	s0,56(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,64
	.cfi_def_cfa 8, 0
	sw	a0,-52(s0)
	sw	a1,-56(s0)
	li	a5,256
	sw	a5,-28(s0)
	sw	zero,-24(s0)
	sw	zero,-20(s0)
	sw	zero,-44(s0)
	sw	zero,-40(s0)
	j	.L53
.L57:
	lw	a4,-40(s0)
	mv	a5,a4
	slli	a5,a5,1
	add	a5,a5,a4
	slli	a5,a5,1
	lla	a4,nvm_blocks
	add	a5,a5,a4
	sw	a5,-36(s0)
	lw	a5,-36(s0)
	lbu	a5,0(a5)
	mv	a4,a5
	lw	a5,-56(s0)
	blt	a5,a4,.L54
	lw	a5,-56(s0)
	addi	a5,a5,1
	j	.L55
.L54:
	lw	a5,-36(s0)
	lbu	a5,0(a5)
.L55:
	sw	a5,-32(s0)
	lw	a5,-36(s0)
	lbu	a5,1(a5)
	beq	a5,zero,.L56
	lw	a5,-36(s0)
	lbu	a5,0(a5)
	mv	a4,a5
	lw	a5,-36(s0)
	lbu	a5,1(a5)
	add	a5,a4,a5
	lw	a4,-32(s0)
	bgeu	a4,a5,.L56
	lw	a5,-28(s0)
	lw	a4,-32(s0)
	bgeu	a4,a5,.L56
	lw	a5,-32(s0)
	sw	a5,-28(s0)
	lw	a5,-36(s0)
	sw	a5,-44(s0)
.L56:
	lw	a5,-40(s0)
	addi	a5,a5,1
	sw	a5,-40(s0)
.L53:
	lw	a4,-40(s0)
	li	a5,11
	bleu	a4,a5,.L57
	lw	a5,-44(s0)
	beq	a5,zero,.L58
	lw	a5,-28(s0)
	lw	a4,-44(s0)
	lbu	a4,0(a4)
	sub	a5,a5,a4
	mv	a1,a5
	lw	a0,-44(s0)
	call	nvm_block_plen
	mv	a5,a0
	sw	a5,-24(s0)
	li	a5,1
	sw	a5,-20(s0)
.L58:
	lw	a5,-52(s0)
	lw	a4,-28(s0)
	sw	a4,0(a5)
	lw	a4,-24(s0)
	sw	a4,4(a5)
	lw	a4,-20(s0)
	sw	a4,8(a5)
	lw	a0,-52(s0)
	lw	ra,60(sp)
	.cfi_restore 1
	lw	s0,56(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 64
	addi	sp,sp,64
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE20:
	.size	nvm_rec_after, .-nvm_rec_after
	.align	2
	.type	nvm_rec_lookup, @function
nvm_rec_lookup:
.LFB21:
	.cfi_startproc
	addi	sp,sp,-64
	.cfi_def_cfa_offset 64
	sw	ra,60(sp)
	sw	s0,56(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,64
	.cfi_def_cfa 8, 0
	sw	a0,-52(s0)
	sw	a1,-56(s0)
	lw	a5,-56(s0)
	sw	a5,-28(s0)
	sw	zero,-24(s0)
	sw	zero,-20(s0)
	sw	zero,-36(s0)
	j	.L61
.L63:
	lw	a4,-36(s0)
	mv	a5,a4
	slli	a5,a5,1
	add	a5,a5,a4
	slli	a5,a5,1
	lla	a4,nvm_blocks
	add	a5,a5,a4
	sw	a5,-32(s0)
	lw	a5,-32(s0)
	lbu	a5,0(a5)
	mv	a4,a5
	lw	a5,-56(s0)
	bltu	a5,a4,.L62
	lw	a5,-32(s0)
	lbu	a5,0(a5)
	mv	a4,a5
	lw	a5,-32(s0)
	lbu	a5,1(a5)
	add	a5,a4,a5
	lw	a4,-56(s0)
	bgeu	a4,a5,.L62
	lw	a5,-32(s0)
	lbu	a5,0(a5)
	mv	a4,a5
	lw	a5,-56(s0)
	sub	a5,a5,a4
	mv	a1,a5
	lw	a0,-32(s0)
	call	nvm_block_plen
	mv	a5,a0
	sw	a5,-24(s0)
	li	a5,1
	sw	a5,-20(s0)
.L62:
	lw	a5,-36(s0)
	addi	a5,a5,1
	sw	a5,-36(s0)
.L61:
	lw	a4,-36(s0)
	li	a5,11
	bleu	a4,a5,.L63
	lw	a5,-52(s0)
	lw	a4,-28(s0)
	sw	a4,0(a5)
	lw	a4,-24(s0)
	sw	a4,4(a5)
	lw	a4,-20(s0)
	sw	a4,8(a5)
	lw	a0,-52(s0)
	lw	ra,60(sp)
	.cfi_restore 1
	lw	s0,56(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 64
	addi	sp,sp,64
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE21:
	.size	nvm_rec_lookup, .-nvm_rec_lookup
	.align	2
	.type	nvm_shape_consistent, @function
nvm_shape_consistent:
.LFB22:
	.cfi_startproc
	addi	sp,sp,-64
	.cfi_def_cfa_offset 64
	sw	ra,60(sp)
	sw	s0,56(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,64
	.cfi_def_cfa 8, 0
	la	a5,__stack_chk_guard
	lw	a4, 0(a5)
	sw	a4, -20(s0)
	li	a4, 0
	sw	zero,-40(s0)
	sw	zero,-36(s0)
	addi	a5,s0,-32
	li	a1,-1
	mv	a0,a5
	call	nvm_rec_after
	j	.L66
.L67:
	lw	a5,-40(s0)
	addi	a5,a5,1
	sw	a5,-40(s0)
	lw	a4,-28(s0)
	lw	a5,-36(s0)
	add	a5,a4,a5
	addi	a5,a5,8
	sw	a5,-36(s0)
	lw	a5,-32(s0)
	mv	a4,a5
	addi	a5,s0,-64
	mv	a1,a4
	mv	a0,a5
	call	nvm_rec_after
	lw	a5,-64(s0)
	sw	a5,-32(s0)
	lw	a5,-60(s0)
	sw	a5,-28(s0)
	lw	a5,-56(s0)
	sw	a5,-24(s0)
.L66:
	lw	a5,-24(s0)
	bne	a5,zero,.L67
	lw	a4,-40(s0)
	li	a5,46
	bne	a4,a5,.L68
	lw	a4,-36(s0)
	li	a5,4096
	addi	a5,a5,-1446
	bne	a4,a5,.L68
	li	a5,1
	j	.L70
.L68:
	li	a5,0
.L70:
	mv	a4,a5
	la	a5,__stack_chk_guard
	lw	a3, -20(s0)
	lw	a5, 0(a5)
	xor	a5, a3, a5
	li	a3, 0
	beq	a5,zero,.L71
	call	__stack_chk_fail@plt
.L71:
	mv	a0,a4
	lw	ra,60(sp)
	.cfi_restore 1
	lw	s0,56(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 64
	addi	sp,sp,64
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE22:
	.size	nvm_shape_consistent, .-nvm_shape_consistent
	.align	2
	.type	nvm_frame, @function
nvm_frame:
.LFB23:
	.cfi_startproc
	addi	sp,sp,-64
	.cfi_def_cfa_offset 64
	sw	ra,60(sp)
	sw	s0,56(sp)
	sw	s1,52(sp)
	sw	s2,48(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	.cfi_offset 9, -12
	.cfi_offset 18, -16
	addi	s0,sp,64
	.cfi_def_cfa 8, 0
	sw	a0,-52(s0)
	sw	a1,-56(s0)
	sw	a2,-60(s0)
	la	a5,__stack_chk_guard
	lw	a4, 0(a5)
	sw	a4, -20(s0)
	li	a4, 0
	lw	a5,-56(s0)
	addi	a5,a5,3
	lbu	a5,0(a5)
	andi	a5,a5,0xff
	sw	a5,-44(s0)
	lw	a5,-56(s0)
	addi	a5,a5,4
	lbu	a5,0(a5)
	andi	a5,a5,0xff
	slli	a5,a5,8
	lw	a4,-56(s0)
	addi	a4,a4,5
	lbu	a4,0(a4)
	andi	a4,a4,0xff
	or	a5,a5,a4
	sw	a5,-40(s0)
	sw	zero,-36(s0)
	lw	a5,-56(s0)
	lbu	a5,0(a5)
	andi	a5,a5,0xff
	slli	a5,a5,8
	lw	a4,-56(s0)
	addi	a4,a4,1
	lbu	a4,0(a4)
	andi	a4,a4,0xff
	or	a4,a5,a4
	li	a5,4096
	addi	a5,a5,1826
	bne	a4,a5,.L73
	lw	a5,-56(s0)
	addi	a5,a5,2
	lbu	a5,0(a5)
	andi	a4,a5,0xff
	li	a5,2
	bne	a4,a5,.L73
	lw	a5,-40(s0)
	addi	a5,a5,8
	lw	a4,-60(s0)
	bgeu	a4,a5,.L74
.L73:
	lw	a5,-52(s0)
	lw	a4,-44(s0)
	sw	a4,0(a5)
	lw	a4,-40(s0)
	sw	a4,4(a5)
	lw	a4,-36(s0)
	sw	a4,8(a5)
	j	.L79
.L74:
	lw	a5,-56(s0)
	addi	s1,a5,8
	lw	s2,-40(s0)
	li	a5,65536
	addi	a2,a5,-1
	li	a1,6
	lw	a0,-56(s0)
	call	nvm_crc16
	mv	a5,a0
	mv	a2,a5
	mv	a1,s2
	mv	a0,s1
	call	nvm_crc16
	mv	a5,a0
	sh	a5,-46(s0)
	lhu	a4,-46(s0)
	lw	a5,-56(s0)
	addi	a5,a5,6
	lbu	a5,0(a5)
	andi	a5,a5,0xff
	slli	a5,a5,8
	lw	a3,-56(s0)
	addi	a3,a3,7
	lbu	a3,0(a3)
	andi	a3,a3,0xff
	or	a5,a5,a3
	beq	a4,a5,.L76
	lw	a5,-52(s0)
	lw	a4,-44(s0)
	sw	a4,0(a5)
	lw	a4,-40(s0)
	sw	a4,4(a5)
	lw	a4,-36(s0)
	sw	a4,8(a5)
	j	.L79
.L76:
	lw	a4,-44(s0)
	addi	a5,s0,-32
	mv	a1,a4
	mv	a0,a5
	call	nvm_rec_lookup
	lw	a5,-24(s0)
	beq	a5,zero,.L77
	lw	a4,-28(s0)
	lw	a5,-40(s0)
	bne	a4,a5,.L77
	li	a5,1
	j	.L78
.L77:
	li	a5,0
.L78:
	sw	a5,-36(s0)
	lw	a5,-52(s0)
	lw	a4,-44(s0)
	sw	a4,0(a5)
	lw	a4,-40(s0)
	sw	a4,4(a5)
	lw	a4,-36(s0)
	sw	a4,8(a5)
.L79:
	la	a5,__stack_chk_guard
	lw	a4, -20(s0)
	lw	a5, 0(a5)
	xor	a5, a4, a5
	li	a4, 0
	beq	a5,zero,.L80
	call	__stack_chk_fail@plt
.L80:
	lw	a0,-52(s0)
	lw	ra,60(sp)
	.cfi_restore 1
	lw	s0,56(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 64
	lw	s1,52(sp)
	.cfi_restore 9
	lw	s2,48(sp)
	.cfi_restore 18
	addi	sp,sp,64
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE23:
	.size	nvm_frame, .-nvm_frame
	.align	2
	.type	nvm_validate, @function
nvm_validate:
.LFB24:
	.cfi_startproc
	addi	sp,sp,-96
	.cfi_def_cfa_offset 96
	sw	ra,92(sp)
	sw	s0,88(sp)
	sw	s1,84(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	.cfi_offset 9, -12
	addi	s0,sp,96
	.cfi_def_cfa 8, 0
	sw	a0,-68(s0)
	la	a5,__stack_chk_guard
	lw	a4, 0(a5)
	sw	a4, -20(s0)
	li	a4, 0
	sw	zero,-52(s0)
	li	a5,-1
	sw	a5,-48(s0)
	li	a1,40
	lw	a0,-68(s0)
	call	nvm_all_erased
	mv	a5,a0
	beq	a5,zero,.L82
	li	a5,9
	j	.L83
.L82:
	lw	a0,-68(s0)
	call	nvm_rd32
	mv	a4,a0
	li	a5,843730944
	addi	a5,a5,-949
	beq	a4,a5,.L84
	li	a5,1
	j	.L83
.L84:
	lw	a5,-68(s0)
	addi	a5,a5,4
	mv	a0,a5
	call	nvm_rd32
	mv	a5,a0
	srli	a4,a5,16
	li	a5,2
	beq	a4,a5,.L85
	li	a5,2
	j	.L83
.L85:
	lw	a5,-68(s0)
	addi	a5,a5,16
	mv	a0,a5
	call	nvm_rd32
	sw	a0,-44(s0)
	lw	a4,-44(s0)
	li	a5,43
	bleu	a4,a5,.L86
	lw	a4,-44(s0)
	li	a5,65536
	bleu	a4,a5,.L87
.L86:
	li	a5,3
	j	.L83
.L87:
	lw	a5,-44(s0)
	addi	a5,a5,-4
	mv	a1,a5
	lw	a0,-68(s0)
	call	nvm_crc32
	mv	s1,a0
	lw	a5,-44(s0)
	addi	a5,a5,-4
	lw	a4,-68(s0)
	add	a5,a4,a5
	mv	a0,a5
	call	nvm_rd32
	mv	a5,a0
	beq	s1,a5,.L88
	li	a5,4
	j	.L83
.L88:
	lw	a5,-68(s0)
	addi	a5,a5,20
	mv	a0,a5
	call	nvm_rd32
	mv	a4,a0
	li	a5,287453184
	addi	a5,a5,836
	bne	a4,a5,.L89
	lw	a5,-68(s0)
	addi	a5,a5,24
	mv	a0,a5
	call	nvm_rd32
	mv	a4,a0
	li	a5,1432776704
	addi	a5,a5,1928
	beq	a4,a5,.L90
.L89:
	li	a5,5
	j	.L83
.L90:
	lw	a5,-68(s0)
	addi	a5,a5,28
	mv	a0,a5
	call	nvm_rd32
	mv	a4,a0
	li	a5,168497152
	addi	a5,a5,-1011
	bne	a4,a5,.L91
	lw	a5,-68(s0)
	addi	a5,a5,32
	mv	a0,a5
	call	nvm_rd32
	mv	a4,a0
	li	a5,16908288
	addi	a5,a5,772
	beq	a4,a5,.L92
.L91:
	li	a5,6
	j	.L83
.L92:
	lw	a5,-68(s0)
	addi	a5,a5,36
	mv	a0,a5
	call	nvm_rd32
	mv	a4,a0
	li	a5,2
	beq	a4,a5,.L93
	li	a5,7
	j	.L83
.L93:
	lw	a5,-68(s0)
	addi	a5,a5,12
	mv	a0,a5
	call	nvm_rd32
	sw	a0,-40(s0)
	li	a5,40
	sw	a5,-60(s0)
	lw	a5,-44(s0)
	addi	a5,a5,-4
	sw	a5,-36(s0)
	sw	zero,-56(s0)
	j	.L94
.L104:
	lla	a5,nvm_ready
	lw	a5,0(a5)
	beq	a5,zero,.L95
	lw	a5,-56(s0)
	andi	a5,a5,15
	bne	a5,zero,.L95
	call	nvm_heartbeat_tick
.L95:
	lw	a5,-60(s0)
	addi	a5,a5,8
	lw	a4,-36(s0)
	bgeu	a4,a5,.L96
	li	a5,3
	j	.L83
.L96:
	lw	a4,-68(s0)
	lw	a5,-60(s0)
	add	a5,a4,a5
	li	a1,8
	mv	a0,a5
	call	nvm_all_erased
	mv	a5,a0
	beq	a5,zero,.L98
	addi	a5,s0,-32
	lw	a1,-48(s0)
	mv	a0,a5
	call	nvm_rec_after
	lw	a5,-24(s0)
	bne	a5,zero,.L99
	li	a5,7
	j	.L83
.L99:
	lw	a4,-28(s0)
	lw	a5,-60(s0)
	add	a5,a4,a5
	addi	a5,a5,8
	lw	a4,-36(s0)
	bgeu	a4,a5,.L100
	li	a5,3
	j	.L83
.L100:
	lw	a5,-60(s0)
	addi	a5,a5,8
	lw	a4,-68(s0)
	add	a5,a4,a5
	lw	a4,-28(s0)
	mv	a1,a4
	mv	a0,a5
	call	nvm_all_erased
	mv	a5,a0
	bne	a5,zero,.L101
	li	a5,7
	j	.L83
.L98:
	lw	a4,-68(s0)
	lw	a5,-60(s0)
	add	a3,a4,a5
	lw	a4,-36(s0)
	lw	a5,-60(s0)
	sub	a4,a4,a5
	addi	a5,s0,-96
	mv	a2,a4
	mv	a1,a3
	mv	a0,a5
	call	nvm_frame
	lw	a5,-96(s0)
	sw	a5,-32(s0)
	lw	a5,-92(s0)
	sw	a5,-28(s0)
	lw	a5,-88(s0)
	sw	a5,-24(s0)
	lw	a5,-24(s0)
	beq	a5,zero,.L102
	lw	a5,-32(s0)
	mv	a4,a5
	lw	a5,-48(s0)
	blt	a5,a4,.L101
.L102:
	li	a5,7
	j	.L83
.L101:
	lw	a5,-32(s0)
	sw	a5,-48(s0)
	lw	a4,-28(s0)
	lw	a5,-60(s0)
	add	a5,a4,a5
	addi	a5,a5,8
	sw	a5,-60(s0)
	lw	a5,-52(s0)
	addi	a5,a5,1
	sw	a5,-52(s0)
	lw	a5,-56(s0)
	addi	a5,a5,1
	sw	a5,-56(s0)
.L94:
	lw	a4,-56(s0)
	lw	a5,-40(s0)
	bltu	a4,a5,.L104
	lw	a5,-60(s0)
	addi	a5,a5,-40
	andi	a5,a5,3
	li	a4,4
	sub	a5,a4,a5
	andi	a4,a5,3
	lw	a5,-60(s0)
	add	a5,a4,a5
	lw	a4,-36(s0)
	beq	a4,a5,.L105
	li	a5,3
	j	.L83
.L105:
	lw	a4,-52(s0)
	li	a5,46
	beq	a4,a5,.L106
	li	a5,10
	j	.L83
.L106:
	li	a5,0
.L83:
	mv	a4,a5
	la	a5,__stack_chk_guard
	lw	a3, -20(s0)
	lw	a5, 0(a5)
	xor	a5, a3, a5
	li	a3, 0
	beq	a5,zero,.L107
	call	__stack_chk_fail@plt
.L107:
	mv	a0,a4
	lw	ra,92(sp)
	.cfi_restore 1
	lw	s0,88(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 96
	lw	s1,84(sp)
	.cfi_restore 9
	addi	sp,sp,96
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE24:
	.size	nvm_validate, .-nvm_validate
	.align	2
	.type	nvm_seq_of, @function
nvm_seq_of:
.LFB25:
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
	lw	a5,-20(s0)
	addi	a5,a5,8
	mv	a0,a5
	call	nvm_rd32
	mv	a5,a0
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
.LFE25:
	.size	nvm_seq_of, .-nvm_seq_of
	.section	.rodata
	.align	2
	.type	nvm_hdr_const, @object
	.size	nvm_hdr_const, 40
nvm_hdr_const:
	.word	843729995
	.word	131072
	.word	0
	.word	46
	.word	2696
	.word	287454020
	.word	1432778632
	.word	168496141
	.word	16909060
	.word	2
	.text
	.align	2
	.type	nvm_hdr_word, @function
nvm_hdr_word:
.LFB26:
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
	sw	a1,-24(s0)
	lw	a4,-20(s0)
	li	a5,2
	beq	a4,a5,.L111
	lw	a3,-20(s0)
	li	a5,-858992640
	addi	a5,a5,-819
	mulhu	a5,a3,a5
	srli	a4,a5,3
	mv	a5,a4
	slli	a5,a5,2
	add	a5,a5,a4
	slli	a5,a5,1
	sub	a4,a3,a5
	lla	a3,nvm_hdr_const
	slli	a5,a4,2
	add	a5,a3,a5
	lw	a5,0(a5)
	j	.L113
.L111:
	lw	a5,-24(s0)
.L113:
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
.LFE26:
	.size	nvm_hdr_word, .-nvm_hdr_word
	.align	2
	.type	nvm_write_header, @function
nvm_write_header:
.LFB27:
	.cfi_startproc
	addi	sp,sp,-48
	.cfi_def_cfa_offset 48
	sw	ra,44(sp)
	sw	s0,40(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,48
	.cfi_def_cfa 8, 0
	sw	a0,-36(s0)
	sw	zero,-20(s0)
	j	.L115
.L116:
	lw	a5,-20(s0)
	srli	a5,a5,2
	lw	a1,-36(s0)
	mv	a0,a5
	call	nvm_hdr_word
	mv	a4,a0
	lw	a5,-20(s0)
	andi	a5,a5,3
	slli	a5,a5,3
	srl	a3,a4,a5
	lw	a4,-20(s0)
	li	a5,2138959872
	add	a5,a4,a5
	andi	a4,a3,0xff
	sb	a4,0(a5)
	lw	a5,-20(s0)
	addi	a5,a5,1
	sw	a5,-20(s0)
.L115:
	lw	a4,-20(s0)
	li	a5,39
	bleu	a4,a5,.L116
	nop
	nop
	lw	ra,44(sp)
	.cfi_restore 1
	lw	s0,40(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 48
	addi	sp,sp,48
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE27:
	.size	nvm_write_header, .-nvm_write_header
	.align	2
	.type	nvm_seal, @function
nvm_seal:
.LFB28:
	.cfi_startproc
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	li	a5,4096
	addi	a1,a5,-1404
	li	a0,2138959872
	call	nvm_crc32
	sw	a0,-20(s0)
	sw	zero,-24(s0)
	j	.L118
.L119:
	lw	a5,-24(s0)
	slli	a5,a5,3
	lw	a4,-20(s0)
	srl	a3,a4,a5
	lw	a4,-24(s0)
	li	a5,4096
	addi	a5,a5,-1404
	add	a4,a4,a5
	li	a5,2138959872
	add	a5,a4,a5
	andi	a4,a3,0xff
	sb	a4,0(a5)
	lw	a5,-24(s0)
	addi	a5,a5,1
	sw	a5,-24(s0)
.L118:
	lw	a4,-24(s0)
	li	a5,3
	bleu	a4,a5,.L119
	nop
	nop
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE28:
	.size	nvm_seal, .-nvm_seal
	.align	2
	.type	nvm_stage_blank_image, @function
nvm_stage_blank_image:
.LFB29:
	.cfi_startproc
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	sw	zero,-20(s0)
	j	.L121
.L122:
	lw	a4,-20(s0)
	li	a5,2138959872
	add	a5,a4,a5
	li	a4,-1
	sb	a4,0(a5)
	lw	a5,-20(s0)
	addi	a5,a5,1
	sw	a5,-20(s0)
.L121:
	lw	a4,-20(s0)
	li	a5,4096
	addi	a5,a5,-1401
	bleu	a4,a5,.L122
	sw	zero,-20(s0)
	j	.L123
.L124:
	lw	a4,-20(s0)
	li	a5,4096
	addi	a5,a5,-1406
	add	a4,a4,a5
	li	a5,2138959872
	add	a5,a4,a5
	sb	zero,0(a5)
	lw	a5,-20(s0)
	addi	a5,a5,1
	sw	a5,-20(s0)
.L123:
	lw	a4,-20(s0)
	li	a5,1
	bleu	a4,a5,.L124
	li	a0,0
	call	nvm_write_header
	call	nvm_seal
	nop
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE29:
	.size	nvm_stage_blank_image, .-nvm_stage_blank_image
	.align	2
	.type	nvm_csr_write, @function
nvm_csr_write:
.LFB30:
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
	sw	a1,-24(s0)
	lw	a1,-20(s0)
	li	a5,4096
	addi	a0,a5,-1740
	call	milan_write
	lw	a1,-24(s0)
	li	a5,4096
	addi	a0,a5,-1736
	call	milan_write
	nop
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE30:
	.size	nvm_csr_write, .-nvm_csr_write
	.align	2
	.type	nvm_rebase_backend, @function
nvm_rebase_backend:
.LFB31:
	.cfi_startproc
	addi	sp,sp,-48
	.cfi_def_cfa_offset 48
	sw	ra,44(sp)
	sw	s0,40(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,48
	.cfi_def_cfa 8, 0
	li	a5,2139025408
	addi	a1,a5,40
	li	a0,0
	call	nvm_csr_write
	li	a5,4096
	addi	a1,a5,-1444
	li	a0,1
	call	nvm_csr_write
	sw	zero,-44(s0)
	j	.L127
.L135:
	li	a5,1
	sw	a5,-32(s0)
	lw	a5,-44(s0)
	beq	a5,zero,.L128
	li	a5,48
	j	.L129
.L128:
	li	a5,32
.L129:
	sw	a5,-28(s0)
	sw	zero,-40(s0)
	sw	zero,-36(s0)
	j	.L130
.L134:
	lw	a5,-44(s0)
	beq	a5,zero,.L131
	lla	a4,nvm_mapout_entries
	lw	a5,-36(s0)
	add	a5,a4,a5
	lbu	a5,0(a5)
	j	.L132
.L131:
	lla	a4,nvm_mapin_entries
	lw	a5,-36(s0)
	add	a5,a4,a5
	lbu	a5,0(a5)
.L132:
	sw	a5,-24(s0)
	lw	a5,-24(s0)
	addi	a5,a5,1
	slli	a5,a5,3
	sw	a5,-20(s0)
	lw	a4,-28(s0)
	lw	a5,-36(s0)
	or	a3,a4,a5
	lw	a5,-20(s0)
	slli	a4,a5,16
	lw	a5,-40(s0)
	or	a5,a4,a5
	mv	a1,a5
	mv	a0,a3
	call	nvm_csr_write
	lw	a4,-40(s0)
	lw	a5,-20(s0)
	add	a5,a4,a5
	sw	a5,-40(s0)
	lw	a5,-36(s0)
	addi	a5,a5,1
	sw	a5,-36(s0)
.L130:
	lw	a4,-36(s0)
	lw	a5,-32(s0)
	bgeu	a4,a5,.L133
	lw	a4,-36(s0)
	li	a5,15
	bleu	a4,a5,.L134
.L133:
	lw	a5,-44(s0)
	addi	a5,a5,1
	sw	a5,-44(s0)
.L127:
	lw	a4,-44(s0)
	li	a5,1
	bleu	a4,a5,.L135
	nop
	nop
	lw	ra,44(sp)
	.cfi_restore 1
	lw	s0,40(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 48
	addi	sp,sp,48
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE31:
	.size	nvm_rebase_backend, .-nvm_rebase_backend
	.align	2
	.type	nvm_publish, @function
nvm_publish:
.LFB32:
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
	lla	a5,nvm_seq
	lw	a5,0(a5)
	mv	a1,a5
	li	a0,2
	call	nvm_csr_write
	lw	a5,-20(s0)
	andi	a5,a5,15
	ori	a5,a5,16
	mv	a1,a5
	li	a0,3
	call	nvm_csr_write
	nop
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE32:
	.size	nvm_publish, .-nvm_publish
	.align	2
	.type	phy_link_tick, @function
phy_link_tick:
.LFB33:
	.cfi_startproc
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	sw	a0,-24(s0)
	sw	a1,-20(s0)
	nop
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE33:
	.size	phy_link_tick, .-phy_link_tick
	.align	2
	.type	nvm_heartbeat_tick, @function
nvm_heartbeat_tick:
.LFB34:
	.cfi_startproc
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	lla	a5,nvm_started
	lw	a5,0(a5)
	beq	a5,zero,.L147
	call	gettime_ns
	sw	a0,-24(s0)
	sw	a1,-20(s0)
	lw	a0,-24(s0)
	lw	a1,-20(s0)
	call	phy_link_tick
	lla	a5,nvm_retired
	lw	a5,0(a5)
	bne	a5,zero,.L148
	lla	a5,nvm_hb_last
	lw	a2,0(a5)
	lw	a3,4(a5)
	mv	a5,a2
	or	a5,a5,a3
	beq	a5,zero,.L142
	lla	a5,nvm_hb_last
	lw	a4,0(a5)
	lw	a5,4(a5)
	lw	a3,-20(s0)
	mv	a2,a5
	bltu	a3,a2,.L142
	lw	a3,-20(s0)
	mv	a2,a5
	bne	a3,a2,.L146
	lw	a3,-24(s0)
	mv	a5,a4
	bltu	a3,a5,.L142
.L146:
	lla	a5,nvm_hb_last
	lw	a0,0(a5)
	lw	a1,4(a5)
	lw	a4,-24(s0)
	lw	a5,-20(s0)
	sub	a2,a4,a0
	mv	a6,a2
	sgtu	a6,a6,a4
	sub	a3,a5,a1
	sub	a5,a3,a6
	mv	a3,a5
	mv	a4,a2
	mv	a5,a3
	mv	a3,a5
	bne	a3,zero,.L142
	mv	a3,a5
	bne	a3,zero,.L138
	li	a5,249999360
	addi	a5,a5,639
	bleu	a4,a5,.L138
.L142:
	li	a1,1
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_write
	lla	a3,nvm_hb_last
	lw	a4,-24(s0)
	lw	a5,-20(s0)
	sw	a4,0(a3)
	sw	a5,4(a3)
	j	.L138
.L147:
	nop
	j	.L138
.L148:
	nop
.L138:
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE34:
	.size	nvm_heartbeat_tick, .-nvm_heartbeat_tick
	.align	2
	.globl	command_dispatch_hook
	.type	command_dispatch_hook, @function
command_dispatch_hook:
.LFB35:
	.cfi_startproc
	addi	sp,sp,-16
	.cfi_def_cfa_offset 16
	sw	ra,12(sp)
	sw	s0,8(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,16
	.cfi_def_cfa 8, 0
	call	nvm_heartbeat_tick
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
.LFE35:
	.size	command_dispatch_hook, .-command_dispatch_hook
	.align	2
	.type	nvm_spi_open, @function
nvm_spi_open:
.LFB36:
	.cfi_startproc
	addi	sp,sp,-16
	.cfi_def_cfa_offset 16
	sw	ra,12(sp)
	sw	s0,8(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,16
	.cfi_def_cfa 8, 0
	j	.L151
.L152:
	call	spiflash_master_rxtx_read@plt
.L151:
	call	spiflash_master_status_read@plt
	mv	a5,a0
	andi	a5,a5,2
	bne	a5,zero,.L152
	li	a5,65536
	addi	a0,a5,264
	call	spiflash_master_phyconfig_write@plt
	li	a0,1
	call	spiflash_master_cs_write@plt
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
.LFE36:
	.size	nvm_spi_open, .-nvm_spi_open
	.align	2
	.type	nvm_spi_xfer, @function
nvm_spi_xfer:
.LFB37:
	.cfi_startproc
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	mv	a5,a0
	sb	a5,-17(s0)
	nop
.L154:
	call	spiflash_master_status_read@plt
	mv	a5,a0
	andi	a5,a5,1
	beq	a5,zero,.L154
	lbu	a5,-17(s0)
	mv	a0,a5
	call	spiflash_master_rxtx_write@plt
	nop
.L155:
	call	spiflash_master_status_read@plt
	mv	a5,a0
	andi	a5,a5,2
	beq	a5,zero,.L155
	call	spiflash_master_rxtx_read@plt
	mv	a5,a0
	andi	a5,a5,0xff
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
.LFE37:
	.size	nvm_spi_xfer, .-nvm_spi_xfer
	.align	2
	.type	nvm_spi_close, @function
nvm_spi_close:
.LFB38:
	.cfi_startproc
	addi	sp,sp,-16
	.cfi_def_cfa_offset 16
	sw	ra,12(sp)
	sw	s0,8(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,16
	.cfi_def_cfa 8, 0
	li	a0,0
	call	spiflash_master_cs_write@plt
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
.LFE38:
	.size	nvm_spi_close, .-nvm_spi_close
	.align	2
	.type	nvm_flash_status, @function
nvm_flash_status:
.LFB39:
	.cfi_startproc
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	call	nvm_spi_open
	li	a0,5
	call	nvm_spi_xfer
	li	a0,0
	call	nvm_spi_xfer
	li	a0,0
	call	nvm_spi_xfer
	li	a0,0
	call	nvm_spi_xfer
	mv	a5,a0
	sb	a5,-17(s0)
	call	nvm_spi_close
	lbu	a5,-17(s0)
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
.LFE39:
	.size	nvm_flash_status, .-nvm_flash_status
	.align	2
	.type	nvm_flash_write_enable, @function
nvm_flash_write_enable:
.LFB40:
	.cfi_startproc
	addi	sp,sp,-16
	.cfi_def_cfa_offset 16
	sw	ra,12(sp)
	sw	s0,8(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,16
	.cfi_def_cfa 8, 0
	call	nvm_spi_open
	li	a0,6
	call	nvm_spi_xfer
	call	nvm_spi_close
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
.LFE40:
	.size	nvm_flash_write_enable, .-nvm_flash_write_enable
	.align	2
	.type	nvm_flash_command, @function
nvm_flash_command:
.LFB41:
	.cfi_startproc
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	mv	a5,a0
	sw	a1,-24(s0)
	sb	a5,-17(s0)
	call	nvm_spi_open
	lbu	a5,-17(s0)
	mv	a0,a5
	call	nvm_spi_xfer
	lw	a5,-24(s0)
	srli	a5,a5,16
	andi	a5,a5,0xff
	mv	a0,a5
	call	nvm_spi_xfer
	lw	a5,-24(s0)
	srli	a5,a5,8
	andi	a5,a5,0xff
	mv	a0,a5
	call	nvm_spi_xfer
	lw	a5,-24(s0)
	andi	a5,a5,0xff
	mv	a0,a5
	call	nvm_spi_xfer
	nop
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE41:
	.size	nvm_flash_command, .-nvm_flash_command
	.align	2
	.type	nvm_flash_wait, @function
nvm_flash_wait:
.LFB42:
	.cfi_startproc
	addi	sp,sp,-48
	.cfi_def_cfa_offset 48
	sw	ra,44(sp)
	sw	s0,40(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,48
	.cfi_def_cfa 8, 0
	sw	a0,-40(s0)
	sw	a1,-36(s0)
	call	gettime_ns
	sw	a0,-24(s0)
	sw	a1,-20(s0)
.L167:
	call	nvm_flash_status
	mv	a5,a0
	andi	a5,a5,1
	bne	a5,zero,.L163
	li	a5,1
	j	.L164
.L163:
	call	nvm_heartbeat_tick
	call	gettime_ns
	mv	a2,a0
	mv	a3,a1
	lw	a0,-24(s0)
	lw	a1,-20(s0)
	sub	a4,a2,a0
	mv	a6,a4
	sgtu	a6,a6,a2
	sub	a5,a3,a1
	sub	a3,a5,a6
	mv	a5,a3
	lw	a3,-36(s0)
	mv	a2,a5
	bltu	a3,a2,.L168
	lw	a3,-36(s0)
	mv	a2,a5
	bne	a3,a2,.L167
	lw	a3,-40(s0)
	mv	a5,a4
	bgeu	a3,a5,.L165
.L168:
	li	a5,0
	j	.L164
.L165:
	j	.L167
.L164:
	mv	a0,a5
	lw	ra,44(sp)
	.cfi_restore 1
	lw	s0,40(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 48
	addi	sp,sp,48
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE42:
	.size	nvm_flash_wait, .-nvm_flash_wait
	.align	2
	.type	nvm_slot_erase, @function
nvm_slot_erase:
.LFB43:
	.cfi_startproc
	addi	sp,sp,-48
	.cfi_def_cfa_offset 48
	sw	ra,44(sp)
	sw	s0,40(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,48
	.cfi_def_cfa 8, 0
	sw	a0,-36(s0)
	lw	a0,-36(s0)
	call	nvm_slot
	sw	a0,-20(s0)
	call	nvm_flash_write_enable
	lw	a1,-36(s0)
	li	a0,216
	call	nvm_flash_command
	call	nvm_spi_close
	li	a0,-794968064
	addi	a0,a0,768
	li	a1,0
	call	nvm_flash_wait
	mv	a5,a0
	bne	a5,zero,.L170
	li	a5,0
	j	.L171
.L170:
	sw	zero,-24(s0)
	j	.L172
.L174:
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	add	a5,a4,a5
	lbu	a5,0(a5)
	andi	a4,a5,0xff
	li	a5,255
	beq	a4,a5,.L173
	li	a5,0
	j	.L171
.L173:
	lw	a5,-24(s0)
	addi	a5,a5,1
	sw	a5,-24(s0)
.L172:
	lw	a4,-24(s0)
	li	a5,4096
	addi	a5,a5,-1401
	bleu	a4,a5,.L174
	li	a5,1
.L171:
	mv	a0,a5
	lw	ra,44(sp)
	.cfi_restore 1
	lw	s0,40(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 48
	addi	sp,sp,48
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE43:
	.size	nvm_slot_erase, .-nvm_slot_erase
	.align	2
	.type	nvm_slot_program, @function
nvm_slot_program:
.LFB44:
	.cfi_startproc
	addi	sp,sp,-48
	.cfi_def_cfa_offset 48
	sw	ra,44(sp)
	sw	s0,40(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,48
	.cfi_def_cfa 8, 0
	sw	a0,-36(s0)
	sw	zero,-28(s0)
	j	.L176
.L182:
	li	a5,4096
	addi	a4,a5,-1400
	lw	a5,-28(s0)
	sub	a5,a4,a5
	sw	a5,-24(s0)
	lw	a4,-24(s0)
	li	a5,256
	bleu	a4,a5,.L177
	li	a5,256
	sw	a5,-24(s0)
.L177:
	call	nvm_flash_write_enable
	lw	a4,-36(s0)
	lw	a5,-28(s0)
	add	a5,a4,a5
	mv	a1,a5
	li	a0,2
	call	nvm_flash_command
	sw	zero,-20(s0)
	j	.L178
.L179:
	lw	a4,-28(s0)
	lw	a5,-20(s0)
	add	a4,a4,a5
	li	a5,2138959872
	add	a5,a4,a5
	lbu	a5,0(a5)
	andi	a5,a5,0xff
	mv	a0,a5
	call	nvm_spi_xfer
	lw	a5,-20(s0)
	addi	a5,a5,1
	sw	a5,-20(s0)
.L178:
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	bltu	a4,a5,.L179
	call	nvm_spi_close
	li	a0,49999872
	addi	a0,a0,128
	li	a1,0
	call	nvm_flash_wait
	mv	a5,a0
	bne	a5,zero,.L180
	li	a5,0
	j	.L181
.L180:
	call	nvm_heartbeat_tick
	lw	a5,-28(s0)
	addi	a5,a5,256
	sw	a5,-28(s0)
.L176:
	lw	a4,-28(s0)
	li	a5,4096
	addi	a5,a5,-1401
	bleu	a4,a5,.L182
	li	a5,1
.L181:
	mv	a0,a5
	lw	ra,44(sp)
	.cfi_restore 1
	lw	s0,40(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 48
	addi	sp,sp,48
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE44:
	.size	nvm_slot_program, .-nvm_slot_program
	.align	2
	.type	nvm_slot_matches, @function
nvm_slot_matches:
.LFB45:
	.cfi_startproc
	addi	sp,sp,-48
	.cfi_def_cfa_offset 48
	sw	ra,44(sp)
	sw	s0,40(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,48
	.cfi_def_cfa 8, 0
	sw	a0,-36(s0)
	lw	a0,-36(s0)
	call	nvm_slot
	sw	a0,-20(s0)
	sw	zero,-24(s0)
	j	.L184
.L187:
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	add	a5,a4,a5
	lbu	a5,0(a5)
	andi	a4,a5,0xff
	lw	a3,-24(s0)
	li	a5,2138959872
	add	a5,a3,a5
	lbu	a5,0(a5)
	andi	a5,a5,0xff
	beq	a4,a5,.L185
	li	a5,0
	j	.L186
.L185:
	lw	a5,-24(s0)
	addi	a5,a5,1
	sw	a5,-24(s0)
.L184:
	lw	a4,-24(s0)
	li	a5,4096
	addi	a5,a5,-1401
	bleu	a4,a5,.L187
	li	a5,1
.L186:
	mv	a0,a5
	lw	ra,44(sp)
	.cfi_restore 1
	lw	s0,40(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 48
	addi	sp,sp,48
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE45:
	.size	nvm_slot_matches, .-nvm_slot_matches
	.align	2
	.type	nvm_slot_letter, @function
nvm_slot_letter:
.LFB46:
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
	li	a5,15597568
	bne	a4,a5,.L189
	li	a5,65
	j	.L190
.L189:
	lw	a4,-20(s0)
	li	a5,15663104
	bne	a4,a5,.L191
	li	a5,66
	j	.L190
.L191:
	li	a5,45
.L190:
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
.LFE46:
	.size	nvm_slot_letter, .-nvm_slot_letter
	.align	2
	.type	nvm_word_read, @function
nvm_word_read:
.LFB47:
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
	lw	a1,-20(s0)
	li	a5,4096
	addi	a0,a5,-1740
	call	milan_write
	li	a5,4096
	addi	a0,a5,-1736
	call	milan_read
	mv	a5,a0
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
.LFE47:
	.size	nvm_word_read, .-nvm_word_read
	.align	2
	.type	nvm_prefill_stage, @function
nvm_prefill_stage:
.LFB48:
	.cfi_startproc
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	lla	a5,nvm_auth_slot
	lw	a4,0(a5)
	li	a5,-1
	bne	a4,a5,.L196
	call	nvm_stage_blank_image
	j	.L195
.L196:
	sw	zero,-20(s0)
	j	.L198
.L199:
	lla	a5,nvm_auth_slot
	lw	a5,0(a5)
	mv	a0,a5
	call	nvm_slot
	mv	a4,a0
	lw	a5,-20(s0)
	add	a4,a4,a5
	lw	a3,-20(s0)
	li	a5,2138959872
	add	a5,a3,a5
	lbu	a4,0(a4)
	andi	a4,a4,0xff
	sb	a4,0(a5)
	lw	a5,-20(s0)
	addi	a5,a5,1
	sw	a5,-20(s0)
.L198:
	lw	a4,-20(s0)
	li	a5,4096
	addi	a5,a5,-1401
	bleu	a4,a5,.L199
.L195:
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE48:
	.size	nvm_prefill_stage, .-nvm_prefill_stage
	.align	2
	.type	nvm_capture, @function
nvm_capture:
.LFB49:
	.cfi_startproc
	addi	sp,sp,-128
	.cfi_def_cfa_offset 128
	sw	ra,124(sp)
	sw	s0,120(sp)
	sw	s2,116(sp)
	sw	s3,112(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	.cfi_offset 18, -12
	.cfi_offset 19, -16
	addi	s0,sp,128
	.cfi_def_cfa 8, 0
	la	a5,__stack_chk_guard
	lw	a4, 0(a5)
	sw	a4, -20(s0)
	li	a4, 0
	sw	zero,-80(s0)
	sw	zero,-76(s0)
	sw	zero,-96(s0)
	call	nvm_prefill_stage
	li	a1,8
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_write
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_read
	sw	a0,-92(s0)
	lw	a4,-92(s0)
	li	a5,65536
	and	a5,a4,a5
	beq	a5,zero,.L201
	lw	a4,-92(s0)
	li	a5,2097152
	and	a5,a4,a5
	beq	a5,zero,.L202
.L201:
	li	a1,32
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_write
	lw	a5,-80(s0)
	sw	a5,-72(s0)
	lw	a5,-76(s0)
	sw	a5,-68(s0)
	j	.L213
.L202:
	li	a0,5
	call	nvm_word_read
	mv	a5,a0
	sw	a5,-80(s0)
	li	a0,8
	call	nvm_word_read
	mv	a5,a0
	sw	a5,-52(s0)
	li	a0,9
	call	nvm_word_read
	mv	a5,a0
	sw	a5,-48(s0)
	li	a0,10
	call	nvm_word_read
	mv	a5,a0
	sw	a5,-44(s0)
	li	a0,11
	call	nvm_word_read
	mv	a5,a0
	sw	a5,-40(s0)
	li	a0,12
	call	nvm_word_read
	mv	a5,a0
	sw	a5,-36(s0)
	li	a0,13
	call	nvm_word_read
	mv	a5,a0
	sw	a5,-32(s0)
	li	a0,14
	call	nvm_word_read
	mv	a5,a0
	sw	a5,-28(s0)
	li	a0,15
	call	nvm_word_read
	mv	a5,a0
	sw	a5,-24(s0)
	addi	a5,s0,-64
	li	a1,-1
	mv	a0,a5
	call	nvm_rec_after
	j	.L204
.L211:
	lw	a5,-64(s0)
	srli	a4,a5,5
	addi	a5,s0,-52
	slli	a4,a4,2
	add	a5,a4,a5
	lw	a4,0(a5)
	lw	a5,-64(s0)
	andi	a5,a5,31
	srl	a5,a4,a5
	andi	a5,a5,1
	seqz	a5,a5
	andi	a5,a5,0xff
	sw	a5,-88(s0)
	lw	a4,-60(s0)
	lw	a5,-96(s0)
	add	a5,a4,a5
	addi	a5,a5,8
	sw	a5,-84(s0)
	lw	a5,-88(s0)
	beq	a5,zero,.L205
	lw	a5,-96(s0)
	sw	a5,-100(s0)
	j	.L206
.L210:
	lw	a4,-100(s0)
	lw	a5,-84(s0)
	bgeu	a4,a5,.L215
	lw	a5,-100(s0)
	andi	a5,a5,3
	bne	a5,zero,.L208
	lw	a4,-84(s0)
	lw	a5,-100(s0)
	sub	a4,a4,a5
	li	a5,3
	bleu	a4,a5,.L208
	lw	a4,-100(s0)
	li	a5,4096
	addi	a5,a5,-1450
	bgtu	a4,a5,.L208
	lw	a4,-100(s0)
	li	a5,2139025408
	addi	a5,a5,40
	add	a5,a4,a5
	mv	a3,a5
	lw	a4,-100(s0)
	li	a5,2138959872
	addi	a5,a5,40
	add	a5,a4,a5
	mv	a4,a5
	lw	a5,0(a3)
	sw	a5,0(a4)
	lw	a5,-100(s0)
	addi	a5,a5,4
	sw	a5,-100(s0)
	j	.L206
.L208:
	lw	a4,-100(s0)
	li	a5,4096
	addi	a5,a5,-1447
	bgtu	a4,a5,.L209
	lw	a5,-100(s0)
	addi	a4,a5,40
	li	a5,2139025408
	add	a4,a4,a5
	lw	a5,-100(s0)
	addi	a3,a5,40
	li	a5,2138959872
	add	a5,a3,a5
	lbu	a4,0(a4)
	andi	a4,a4,0xff
	sb	a4,0(a5)
.L209:
	lw	a5,-100(s0)
	addi	a5,a5,1
	sw	a5,-100(s0)
.L206:
	lw	a4,-100(s0)
	li	a5,4096
	addi	a5,a5,-1447
	bleu	a4,a5,.L210
	j	.L205
.L215:
	nop
.L205:
	lw	a5,-84(s0)
	sw	a5,-96(s0)
	lw	a5,-64(s0)
	mv	a4,a5
	addi	a5,s0,-128
	mv	a1,a4
	mv	a0,a5
	call	nvm_rec_after
	lw	a5,-128(s0)
	sw	a5,-64(s0)
	lw	a5,-124(s0)
	sw	a5,-60(s0)
	lw	a5,-120(s0)
	sw	a5,-56(s0)
.L204:
	lw	a5,-56(s0)
	bne	a5,zero,.L211
#APP
# 1217 "/tmp/milan-census-s8bsel5_/milan_baremetal.c" 1
	fence rw, rw
# 0 "" 2
#NO_APP
	li	a1,16
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_write
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_read
	mv	a4,a0
	li	a5,524288
	and	a5,a4,a5
	bne	a5,zero,.L212
	li	a1,32
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_write
	lw	a5,-80(s0)
	sw	a5,-72(s0)
	lw	a5,-76(s0)
	sw	a5,-68(s0)
	j	.L213
.L212:
	li	a5,1
	sw	a5,-76(s0)
	lw	a5,-80(s0)
	sw	a5,-72(s0)
	lw	a5,-76(s0)
	sw	a5,-68(s0)
.L213:
	lw	a4,-72(s0)
	lw	a5,-68(s0)
	mv	s2,a4
	mv	s3,a5
	mv	a2,s2
	mv	a3,s3
	la	a5,__stack_chk_guard
	lw	a4, -20(s0)
	lw	a5, 0(a5)
	xor	a5, a4, a5
	li	a4, 0
	beq	a5,zero,.L214
	call	__stack_chk_fail@plt
.L214:
	mv	a0,a2
	mv	a1,a3
	lw	ra,124(sp)
	.cfi_restore 1
	lw	s0,120(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 128
	lw	s2,116(sp)
	.cfi_restore 18
	lw	s3,112(sp)
	.cfi_restore 19
	addi	sp,sp,128
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE49:
	.size	nvm_capture, .-nvm_capture
	.section	.rodata
	.align	2
.LC15:
	.string	"Milan NVM: commit (%s) deferred, the capture was not attested.\n"
	.align	2
.LC16:
	.string	"Milan NVM: commit (%s) deferred, the attested capture reads %s.\n"
	.align	2
.LC17:
	.string	"Milan NVM: commit (%s) seq %lu to slot %c FAILED: %s; released, not acknowledged.\n"
	.align	2
.LC18:
	.string	"Milan NVM: commit (%s) seq %lu -> slot %c, %u B, verified; acknowledgement REFUSED, the captured work stays owned.\n"
	.align	2
.LC19:
	.string	"Milan NVM: commit (%s) seq %lu -> slot %c, %u B, capture %lu acknowledged.\n"
	.text
	.align	2
	.type	nvm_commit, @function
nvm_commit:
.LFB50:
	.cfi_startproc
	addi	sp,sp,-64
	.cfi_def_cfa_offset 64
	sw	ra,60(sp)
	sw	s0,56(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,64
	.cfi_def_cfa 8, 0
	sw	a0,-52(s0)
	lla	a5,nvm_seq
	lw	a5,0(a5)
	addi	a5,a5,1
	sw	a5,-32(s0)
	lla	a5,nvm_auth_slot
	lw	a4,0(a5)
	li	a5,15597568
	bne	a4,a5,.L217
	li	a5,15663104
	j	.L218
.L217:
	li	a5,15597568
.L218:
	sw	a5,-28(s0)
	lla	a5,nvm_in_commit
	li	a4,1
	sw	a4,0(a5)
	call	nvm_capture
	mv	a4,a0
	mv	a5,a1
	sw	a4,-24(s0)
	sw	a5,-20(s0)
	lw	a5,-20(s0)
	bne	a5,zero,.L219
	lw	a1,-52(s0)
	lla	a0,.LC15
	call	printf@plt
	lla	a5,nvm_captures_refused
	lw	a5,0(a5)
	addi	a4,a5,1
	lla	a5,nvm_captures_refused
	sw	a4,0(a5)
	lla	a5,nvm_dirty_since
	li	a3,0
	li	a4,0
	sw	a3,0(a5)
	sw	a4,4(a5)
	lla	a5,nvm_in_commit
	sw	zero,0(a5)
	li	a5,0
	j	.L228
.L219:
	lw	a0,-32(s0)
	call	nvm_write_header
	call	nvm_seal
	li	a0,2138959872
	call	nvm_validate
	sw	a0,-36(s0)
	lw	a5,-36(s0)
	beq	a5,zero,.L221
	li	a1,32
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_write
	lla	a4,nvm_verdict_name
	lw	a5,-36(s0)
	slli	a5,a5,2
	add	a5,a4,a5
	lw	a5,0(a5)
	mv	a2,a5
	lw	a1,-52(s0)
	lla	a0,.LC16
	call	printf@plt
	lla	a5,nvm_dirty_since
	li	a3,0
	li	a4,0
	sw	a3,0(a5)
	sw	a4,4(a5)
	lla	a5,nvm_in_commit
	sw	zero,0(a5)
	li	a5,0
	j	.L228
.L221:
	li	a1,4
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_write
	lw	a0,-28(s0)
	call	nvm_slot_erase
	mv	a5,a0
	bne	a5,zero,.L222
	li	a5,11
	sw	a5,-36(s0)
	j	.L223
.L222:
	lw	a0,-28(s0)
	call	nvm_slot_program
	mv	a5,a0
	bne	a5,zero,.L224
	li	a5,12
	sw	a5,-36(s0)
	j	.L223
.L224:
	lw	a0,-28(s0)
	call	nvm_slot
	mv	a5,a0
	mv	a0,a5
	call	nvm_validate
	mv	a5,a0
	bne	a5,zero,.L225
	lw	a0,-28(s0)
	call	nvm_slot
	mv	a5,a0
	mv	a0,a5
	call	nvm_seq_of
	mv	a4,a0
	lw	a5,-32(s0)
	bne	a5,a4,.L225
	lw	a0,-28(s0)
	call	nvm_slot_matches
	mv	a5,a0
	bne	a5,zero,.L223
.L225:
	li	a5,13
	sw	a5,-36(s0)
.L223:
	lla	a5,nvm_last_verdict
	lw	a4,-36(s0)
	sw	a4,0(a5)
	lla	a5,nvm_dirty_since
	li	a3,0
	li	a4,0
	sw	a3,0(a5)
	sw	a4,4(a5)
	lla	a5,nvm_in_commit
	sw	zero,0(a5)
	lw	a5,-36(s0)
	beq	a5,zero,.L226
	lw	a5,-36(s0)
	ori	a5,a5,16
	mv	a1,a5
	li	a0,3
	call	nvm_csr_write
	li	a1,32
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_write
	lla	a5,nvm_commits_failed
	lw	a5,0(a5)
	addi	a4,a5,1
	lla	a5,nvm_commits_failed
	sw	a4,0(a5)
	lw	a0,-28(s0)
	call	nvm_slot_letter
	mv	a5,a0
	mv	a3,a5
	lla	a4,nvm_verdict_name
	lw	a5,-36(s0)
	slli	a5,a5,2
	add	a5,a4,a5
	lw	a5,0(a5)
	mv	a4,a5
	lw	a2,-32(s0)
	lw	a1,-52(s0)
	lla	a0,.LC17
	call	printf@plt
	li	a5,0
	j	.L228
.L226:
	lla	a5,nvm_seq
	lw	a4,-32(s0)
	sw	a4,0(a5)
	lla	a5,nvm_auth_slot
	lw	a4,-28(s0)
	sw	a4,0(a5)
	lw	a1,-32(s0)
	li	a0,2
	call	nvm_csr_write
	li	a1,16
	li	a0,3
	call	nvm_csr_write
	lw	a5,-24(s0)
	slli	a5,a5,16
	ori	a5,a5,2
	mv	a1,a5
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_write
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_read
	mv	a4,a0
	li	a5,1048576
	and	a5,a4,a5
	beq	a5,zero,.L227
	lla	a5,nvm_acks_refused
	lw	a5,0(a5)
	addi	a4,a5,1
	lla	a5,nvm_acks_refused
	sw	a4,0(a5)
	lw	a0,-28(s0)
	call	nvm_slot_letter
	mv	a5,a0
	mv	a3,a5
	li	a5,4096
	addi	a4,a5,-1400
	lw	a2,-32(s0)
	lw	a1,-52(s0)
	lla	a0,.LC18
	call	printf@plt
	li	a5,0
	j	.L228
.L227:
	lla	a5,nvm_commits_ok
	lw	a5,0(a5)
	addi	a4,a5,1
	lla	a5,nvm_commits_ok
	sw	a4,0(a5)
	lw	a0,-28(s0)
	call	nvm_slot_letter
	mv	a5,a0
	mv	a3,a5
	lw	a5,-24(s0)
	li	a4,4096
	addi	a4,a4,-1400
	lw	a2,-32(s0)
	lw	a1,-52(s0)
	lla	a0,.LC19
	call	printf@plt
	li	a5,1
.L228:
	mv	a0,a5
	lw	ra,60(sp)
	.cfi_restore 1
	lw	s0,56(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 64
	addi	sp,sp,64
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE50:
	.size	nvm_commit, .-nvm_commit
	.section	.rodata
	.align	2
.LC20:
	.string	"dirty"
	.text
	.align	2
	.type	nvm_service, @function
nvm_service:
.LFB51:
	.cfi_startproc
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	call	nvm_heartbeat_tick
	lla	a5,nvm_ready
	lw	a5,0(a5)
	beq	a5,zero,.L241
	lla	a5,nvm_in_commit
	lw	a5,0(a5)
	bne	a5,zero,.L241
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_read
	sw	a0,-28(s0)
	lw	a5,-28(s0)
	andi	a5,a5,256
	bne	a5,zero,.L233
	lla	a5,nvm_dirty_since
	li	a3,0
	li	a4,0
	sw	a3,0(a5)
	sw	a4,4(a5)
	j	.L229
.L233:
	lw	a5,-28(s0)
	andi	a5,a5,1024
	bne	a5,zero,.L242
	call	gettime_ns
	sw	a0,-24(s0)
	sw	a1,-20(s0)
	lla	a5,nvm_dirty_since
	lw	a2,0(a5)
	lw	a3,4(a5)
	mv	a5,a2
	or	a5,a5,a3
	beq	a5,zero,.L235
	lla	a5,nvm_dirty_since
	lw	a4,0(a5)
	lw	a5,4(a5)
	lw	a3,-20(s0)
	mv	a2,a5
	bltu	a3,a2,.L235
	lw	a3,-20(s0)
	mv	a2,a5
	bne	a3,a2,.L237
	lw	a3,-24(s0)
	mv	a5,a4
	bgeu	a3,a5,.L237
.L235:
	lla	a3,nvm_dirty_since
	lw	a4,-24(s0)
	lw	a5,-20(s0)
	sw	a4,0(a3)
	sw	a5,4(a3)
	j	.L229
.L237:
	lla	a5,nvm_dirty_since
	lw	a0,0(a5)
	lw	a1,4(a5)
	lw	a4,-24(s0)
	lw	a5,-20(s0)
	sub	a2,a4,a0
	mv	a6,a2
	sgtu	a6,a6,a4
	sub	a3,a5,a1
	sub	a5,a3,a6
	mv	a3,a5
	mv	a4,a2
	mv	a5,a3
	mv	a3,a5
	bne	a3,zero,.L240
	mv	a3,a5
	bne	a3,zero,.L229
	li	a5,1000001536
	addi	a5,a5,-1537
	bleu	a4,a5,.L229
.L240:
	lla	a0,.LC20
	call	nvm_commit
	j	.L229
.L241:
	nop
	j	.L229
.L242:
	nop
.L229:
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE51:
	.size	nvm_service, .-nvm_service
	.align	2
	.type	nvm_pick_slot, @function
nvm_pick_slot:
.LFB52:
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
	sw	a1,-24(s0)
	sw	a2,-28(s0)
	sw	a3,-32(s0)
	lw	a5,-20(s0)
	bne	a5,zero,.L244
	lw	a5,-28(s0)
	bne	a5,zero,.L244
	lw	a4,-24(s0)
	lw	a5,-32(s0)
	sub	a5,a4,a5
	blt	a5,zero,.L245
	li	a5,15597568
	j	.L247
.L245:
	li	a5,15663104
	j	.L247
.L244:
	lw	a5,-20(s0)
	bne	a5,zero,.L248
	li	a5,15597568
	j	.L247
.L248:
	lw	a5,-28(s0)
	bne	a5,zero,.L249
	li	a5,15663104
	j	.L247
.L249:
	li	a5,-1
.L247:
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
.LFE52:
	.size	nvm_pick_slot, .-nvm_pick_slot
	.section	.rodata
	.align	2
.LC21:
	.string	"Milan NVM: the device face did not go idle before the repeated window load."
	.text
	.align	2
	.type	nvm_wait_dev_idle, @function
nvm_wait_dev_idle:
.LFB53:
	.cfi_startproc
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	call	gettime_ns
	sw	a0,-24(s0)
	sw	a1,-20(s0)
	j	.L252
.L255:
	call	nvm_heartbeat_tick
	call	gettime_ns
	mv	a2,a0
	mv	a3,a1
	lw	a0,-24(s0)
	lw	a1,-20(s0)
	sub	a4,a2,a0
	mv	a6,a4
	sgtu	a6,a6,a2
	sub	a5,a3,a1
	sub	a3,a5,a6
	mv	a5,a3
	mv	a3,a5
	bne	a3,zero,.L256
	mv	a3,a5
	bne	a3,zero,.L252
	li	a5,-1294966784
	addi	a5,a5,-512
	bgtu	a4,a5,.L256
	j	.L252
.L256:
	lla	a0,.LC21
	call	puts@plt
	j	.L251
.L252:
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_read
	mv	a5,a0
	andi	a5,a5,16
	bne	a5,zero,.L255
.L251:
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE53:
	.size	nvm_wait_dev_idle, .-nvm_wait_dev_idle
	.align	2
	.type	nvm_restore_ended, @function
nvm_restore_ended:
.LFB54:
	.cfi_startproc
	addi	sp,sp,-16
	.cfi_def_cfa_offset 16
	sw	ra,12(sp)
	sw	s0,8(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,16
	.cfi_def_cfa 8, 0
	li	a5,4096
	addi	a0,a5,-1756
	call	milan_read
	mv	a4,a0
	li	a5,65536
	addi	a5,a5,4
	and	a5,a4,a5
	snez	a5,a5
	andi	a5,a5,0xff
	mv	a0,a5
	lw	ra,12(sp)
	.cfi_restore 1
	lw	s0,8(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 16
	addi	sp,sp,16
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE54:
	.size	nvm_restore_ended, .-nvm_restore_ended
	.section	.rodata
	.align	2
.LC22:
	.string	"Milan NVM: the restore walk did not sequence in time."
	.text
	.align	2
	.type	nvm_restore_walk, @function
nvm_restore_walk:
.LFB55:
	.cfi_startproc
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	call	gettime_ns
	sw	a0,-24(s0)
	sw	a1,-20(s0)
	li	a5,4096
	addi	a0,a5,-1760
	call	milan_read
	mv	a5,a0
	ori	a5,a5,2
	mv	a1,a5
	li	a5,4096
	addi	a0,a5,-1760
	call	milan_write
	j	.L260
.L263:
	call	nvm_heartbeat_tick
	call	gettime_ns
	mv	a2,a0
	mv	a3,a1
	lw	a0,-24(s0)
	lw	a1,-20(s0)
	sub	a4,a2,a0
	mv	a6,a4
	sgtu	a6,a6,a2
	sub	a5,a3,a1
	sub	a3,a5,a6
	mv	a5,a3
	mv	a3,a5
	bne	a3,zero,.L264
	mv	a3,a5
	bne	a3,zero,.L260
	li	a5,-1294966784
	addi	a5,a5,-512
	bgtu	a4,a5,.L264
	j	.L260
.L264:
	lla	a0,.LC22
	call	puts@plt
	j	.L262
.L260:
	call	nvm_restore_ended
	mv	a5,a0
	beq	a5,zero,.L263
.L262:
	li	a5,4096
	addi	a0,a5,-1760
	call	milan_read
	mv	a5,a0
	andi	a5,a5,-3
	mv	a1,a5
	li	a5,4096
	addi	a0,a5,-1760
	call	milan_write
	nop
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE55:
	.size	nvm_restore_walk, .-nvm_restore_walk
	.align	2
	.type	nvm_fill_window, @function
nvm_fill_window:
.LFB56:
	.cfi_startproc
	addi	sp,sp,-48
	.cfi_def_cfa_offset 48
	sw	ra,44(sp)
	sw	s0,40(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,48
	.cfi_def_cfa 8, 0
	sw	a0,-36(s0)
	lw	a4,-36(s0)
	li	a5,-1
	beq	a4,a5,.L266
	lw	a0,-36(s0)
	call	nvm_slot
	sw	a0,-20(s0)
	sw	zero,-24(s0)
	j	.L267
.L268:
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	add	a4,a4,a5
	lw	a3,-24(s0)
	li	a5,2139025408
	add	a5,a3,a5
	lbu	a4,0(a4)
	andi	a4,a4,0xff
	sb	a4,0(a5)
	lw	a5,-24(s0)
	addi	a5,a5,1
	sw	a5,-24(s0)
.L267:
	lw	a4,-24(s0)
	li	a5,4096
	addi	a5,a5,-1401
	bleu	a4,a5,.L268
	j	.L272
.L266:
	call	nvm_stage_blank_image
	sw	zero,-24(s0)
	j	.L270
.L271:
	lw	a4,-24(s0)
	li	a5,2138959872
	add	a4,a4,a5
	lw	a3,-24(s0)
	li	a5,2139025408
	add	a5,a3,a5
	lbu	a4,0(a4)
	andi	a4,a4,0xff
	sb	a4,0(a5)
	lw	a5,-24(s0)
	addi	a5,a5,1
	sw	a5,-24(s0)
.L270:
	lw	a4,-24(s0)
	li	a5,4096
	addi	a5,a5,-1401
	bleu	a4,a5,.L271
.L272:
	nop
	lw	ra,44(sp)
	.cfi_restore 1
	lw	s0,40(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 48
	addi	sp,sp,48
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE56:
	.size	nvm_fill_window, .-nvm_fill_window
	.align	2
	.type	nvm_load_window, @function
nvm_load_window:
.LFB57:
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
	call	nvm_rebase_backend
	lw	a0,-20(s0)
	call	nvm_fill_window
#APP
# 1418 "/tmp/milan-census-s8bsel5_/milan_baremetal.c" 1
	fence rw, rw
# 0 "" 2
#NO_APP
	li	a1,64
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_write
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_read
	mv	a4,a0
	li	a5,4096
	addi	a5,a5,-2048
	and	a5,a4,a5
	seqz	a5,a5
	andi	a5,a5,0xff
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
.LFE57:
	.size	nvm_load_window, .-nvm_load_window
	.section	.rodata
	.align	2
.LC23:
	.string	"%d"
	.align	2
.LC24:
	.string	"1"
	.align	2
.LC25:
	.string	"Milan NVM: the record set does not match the generated shape; persistence disabled."
	.align	2
.LC26:
	.string	"Milan NVM: the backend does not carry saved-state contract 3 (tag %02lx); the writer is disabled.\n"
	.align	2
.LC27:
	.string	"Milan NVM: no window load was accepted in this boot; the writer stays retired until the next reset."
	.align	2
.LC28:
	.string	"Milan NVM: writer restarted on a live backend; re-attached, the window is not reloaded."
	.align	2
.LC29:
	.string	"Milan NVM: the window went live without a validated load; the writer stays disabled until the next reset."
	.align	2
.LC30:
	.string	"Milan NVM: the backend refused %u window load(s); accepted at attempt %u.\n"
	.align	2
.LC31:
	.string	"Milan NVM: the backend refused %u window load(s) and the window then went live; the writer is disabled until the next reset.\n"
	.align	2
.LC32:
	.string	"Milan NVM: the backend refused %u window loads; the window is not validated and the writer is disabled until the next reset.\n"
	.align	2
.LC33:
	.string	"Milan NVM: slot A %s seq %lu, slot B %s seq %lu; offered %c seq %lu (%s), %u B at 0x%08x; walk done=%lu fail=%lu blank=%lu backed=%lu closed=%lu rolled_back=%lu cause=%lu/%lu.\n"
	.text
	.align	2
	.type	nvm_boot, @function
nvm_boot:
.LFB58:
	.cfi_startproc
	addi	sp,sp,-96
	.cfi_def_cfa_offset 96
	sw	ra,92(sp)
	sw	s0,88(sp)
	sw	s1,84(sp)
	sw	s2,80(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	.cfi_offset 9, -12
	.cfi_offset 18, -16
	addi	s0,sp,96
	.cfi_def_cfa 8, 0
	sw	zero,-44(s0)
	sw	zero,-40(s0)
	sw	zero,-36(s0)
	lla	a2,aem_view
	lla	a1,.LC23
	lla	a0,.LC24
	call	__isoc99_sscanf@plt
	call	bios_dispatch_hook_required@plt
	call	nvm_shape_consistent
	mv	a5,a0
	bne	a5,zero,.L276
	lla	a0,.LC25
	call	puts@plt
	call	nvm_restore_ended
	mv	a5,a0
	bne	a5,zero,.L301
	call	nvm_restore_walk
	j	.L301
.L276:
	lla	a5,nvm_started
	li	a4,1
	sw	a4,0(a5)
	li	a0,15597568
	call	nvm_slot
	mv	a5,a0
	mv	a0,a5
	call	nvm_validate
	mv	a4,a0
	lla	a5,nvm_verdict_a
	sw	a4,0(a5)
	li	a0,15663104
	call	nvm_slot
	mv	a5,a0
	mv	a0,a5
	call	nvm_validate
	mv	a4,a0
	lla	a5,nvm_verdict_b
	sw	a4,0(a5)
	lla	a5,nvm_verdict_a
	lw	a5,0(a5)
	bne	a5,zero,.L279
	li	a0,15597568
	call	nvm_slot
	mv	a5,a0
	mv	a0,a5
	call	nvm_seq_of
	mv	a5,a0
	j	.L280
.L279:
	li	a5,0
.L280:
	sw	a5,-32(s0)
	lla	a5,nvm_verdict_b
	lw	a5,0(a5)
	bne	a5,zero,.L281
	li	a0,15663104
	call	nvm_slot
	mv	a5,a0
	mv	a0,a5
	call	nvm_seq_of
	mv	a5,a0
	j	.L282
.L281:
	li	a5,0
.L282:
	sw	a5,-28(s0)
	lla	a5,nvm_verdict_a
	lw	a4,0(a5)
	lla	a5,nvm_verdict_b
	lw	a5,0(a5)
	lw	a3,-28(s0)
	mv	a2,a5
	lw	a1,-32(s0)
	mv	a0,a4
	call	nvm_pick_slot
	sw	a0,-24(s0)
	lw	a4,-24(s0)
	li	a5,-1
	beq	a4,a5,.L283
	lw	a4,-24(s0)
	li	a5,15597568
	bne	a4,a5,.L284
	lw	a5,-32(s0)
	j	.L285
.L284:
	lw	a5,-28(s0)
.L285:
	lla	a4,nvm_seq
	sw	a5,0(a4)
	sw	zero,-48(s0)
	j	.L286
.L283:
	lla	a5,nvm_seq
	sw	zero,0(a5)
	lla	a5,nvm_verdict_a
	lw	a4,0(a5)
	li	a5,9
	beq	a4,a5,.L287
	lla	a5,nvm_verdict_a
	lw	a5,0(a5)
	j	.L288
.L287:
	lla	a5,nvm_verdict_b
	lw	a5,0(a5)
.L288:
	sw	a5,-48(s0)
.L286:
	lla	a5,nvm_auth_slot
	lw	a4,-24(s0)
	sw	a4,0(a5)
	lla	a5,nvm_last_verdict
	lw	a4,-48(s0)
	sw	a4,0(a5)
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_read
	sw	a0,-20(s0)
	lw	a5,-20(s0)
	srli	a4,a5,24
	li	a5,195
	beq	a4,a5,.L289
	lw	a0,-24(s0)
	call	nvm_fill_window
	call	nvm_rebase_backend
	lw	a0,-48(s0)
	call	nvm_publish
	lw	a5,-20(s0)
	srli	a5,a5,24
	mv	a1,a5
	lla	a0,.LC26
	call	printf@plt
	j	.L290
.L289:
	lw	a5,-20(s0)
	andi	a5,a5,8
	bne	a5,zero,.L291
	lw	a5,-20(s0)
	andi	a5,a5,4
	bne	a5,zero,.L291
	lla	a5,nvm_retired
	li	a4,1
	sw	a4,0(a5)
	lla	a0,.LC27
	call	puts@plt
	j	.L290
.L291:
	lw	a5,-20(s0)
	andi	a5,a5,8
	bne	a5,zero,.L292
	li	a1,32
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_write
	lw	a0,-48(s0)
	call	nvm_publish
	lla	a5,nvm_ready
	li	a4,1
	sw	a4,0(a5)
	lla	a0,.LC28
	call	puts@plt
	j	.L290
.L292:
	li	a5,4096
	addi	a0,a5,-1756
	call	milan_read
	mv	a5,a0
	andi	a5,a5,4
	beq	a5,zero,.L294
	lla	a5,nvm_retired
	li	a4,1
	sw	a4,0(a5)
	lla	a0,.LC29
	call	puts@plt
	j	.L290
.L297:
	lw	a0,-24(s0)
	call	nvm_load_window
	sw	a0,-40(s0)
	lw	a5,-44(s0)
	addi	a5,a5,1
	sw	a5,-44(s0)
	lw	a5,-40(s0)
	bne	a5,zero,.L295
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_read
	mv	a5,a0
	andi	a5,a5,8
	bne	a5,zero,.L295
	li	a5,1
	sw	a5,-36(s0)
	j	.L296
.L295:
	lw	a5,-40(s0)
	bne	a5,zero,.L294
	lw	a4,-44(s0)
	li	a5,3
	bgtu	a4,a5,.L294
	call	nvm_wait_dev_idle
.L294:
	lw	a5,-40(s0)
	bne	a5,zero,.L296
	lw	a4,-44(s0)
	li	a5,3
	bleu	a4,a5,.L297
.L296:
	lw	a5,-40(s0)
	beq	a5,zero,.L298
	lw	a0,-48(s0)
	call	nvm_publish
	lla	a5,nvm_ready
	li	a4,1
	sw	a4,0(a5)
	lw	a4,-44(s0)
	li	a5,1
	bleu	a4,a5,.L290
	lw	a5,-44(s0)
	addi	a5,a5,-1
	lw	a2,-44(s0)
	mv	a1,a5
	lla	a0,.LC30
	call	printf@plt
	j	.L290
.L298:
	lla	a5,nvm_retired
	li	a4,1
	sw	a4,0(a5)
	lw	a5,-36(s0)
	beq	a5,zero,.L299
	lw	a1,-44(s0)
	lla	a0,.LC31
	call	printf@plt
	j	.L290
.L299:
	lw	a1,-44(s0)
	lla	a0,.LC32
	call	printf@plt
.L290:
	call	nvm_restore_ended
	mv	a5,a0
	bne	a5,zero,.L300
	call	nvm_restore_walk
.L300:
	li	a5,4096
	addi	a0,a5,-1756
	call	milan_read
	sw	a0,-20(s0)
	lla	a5,nvm_verdict_a
	lw	a5,0(a5)
	lla	a4,nvm_verdict_name
	slli	a5,a5,2
	add	a5,a4,a5
	lw	s1,0(a5)
	lla	a5,nvm_verdict_b
	lw	a5,0(a5)
	lla	a4,nvm_verdict_name
	slli	a5,a5,2
	add	a5,a4,a5
	lw	s2,0(a5)
	lw	a0,-24(s0)
	call	nvm_slot_letter
	mv	a5,a0
	mv	t4,a5
	lla	a5,nvm_seq
	lw	t1,0(a5)
	lla	a4,nvm_verdict_name
	lw	a5,-48(s0)
	slli	a5,a5,2
	add	a5,a4,a5
	lw	t3,0(a5)
	lw	a5,-20(s0)
	srli	a5,a5,2
	andi	a5,a5,1
	lw	a4,-20(s0)
	srli	a4,a4,3
	andi	a4,a4,1
	lw	a3,-20(s0)
	srli	a3,a3,7
	andi	a3,a3,1
	lw	a2,-20(s0)
	srli	a2,a2,6
	andi	a2,a2,1
	lw	a1,-20(s0)
	srli	a1,a1,16
	andi	a1,a1,1
	lw	a0,-20(s0)
	srli	a0,a0,17
	andi	a0,a0,1
	lw	a6,-20(s0)
	srli	a6,a6,18
	andi	a6,a6,7
	lw	a7,-20(s0)
	srli	a7,a7,21
	andi	a7,a7,3
	sw	a7,36(sp)
	sw	a6,32(sp)
	sw	a0,28(sp)
	sw	a1,24(sp)
	sw	a2,20(sp)
	sw	a3,16(sp)
	sw	a4,12(sp)
	sw	a5,8(sp)
	li	a5,2139025408
	sw	a5,4(sp)
	li	a5,4096
	addi	a5,a5,-1400
	sw	a5,0(sp)
	mv	a7,t3
	mv	a6,t1
	mv	a5,t4
	lw	a4,-28(s0)
	mv	a3,s2
	lw	a2,-32(s0)
	mv	a1,s1
	lla	a0,.LC33
	call	printf@plt
	lla	a0,nvm_service
	call	set_idle_hook@plt
	j	.L275
.L301:
	nop
.L275:
	lw	ra,92(sp)
	.cfi_restore 1
	lw	s0,88(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 96
	lw	s1,84(sp)
	.cfi_restore 9
	lw	s2,80(sp)
	.cfi_restore 18
	addi	sp,sp,96
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE58:
	.size	nvm_boot, .-nvm_boot
	.align	2
	.type	configure_fabric, @function
configure_fabric:
.LFB59:
	.cfi_startproc
	addi	sp,sp,-16
	.cfi_def_cfa_offset 16
	sw	ra,12(sp)
	sw	s0,8(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,16
	.cfi_def_cfa 8, 0
	li	a0,1536
	call	milan_read
	mv	a5,a0
	andi	a5,a5,-2
	mv	a1,a5
	li	a0,1536
	call	milan_write
	li	a5,4096
	addi	a0,a5,-1760
	call	milan_read
	mv	a5,a0
	andi	a5,a5,-2
	mv	a1,a5
	li	a5,4096
	addi	a0,a5,-1760
	call	milan_write
	li	a5,287453184
	addi	a1,a5,836
	li	a0,1540
	call	milan_write
	li	a5,1432776704
	addi	a1,a5,1928
	li	a0,1544
	call	milan_write
	li	a5,168497152
	addi	a1,a5,-1011
	li	a0,1548
	call	milan_write
	li	a5,16908288
	addi	a1,a5,772
	li	a0,1552
	call	milan_write
	li	a1,3
	li	a0,264
	call	milan_write
	li	a1,512
	li	a0,268
	call	milan_write
	li	a0,256
	call	milan_read
	mv	a5,a0
	ori	a5,a5,8
	mv	a1,a5
	li	a0,256
	call	milan_write
	li	a1,1
	li	a0,1792
	call	milan_write
	li	a5,131072
	addi	a1,a5,1
	li	a0,1620
	call	milan_write
	li	a1,2
	li	a0,1668
	call	milan_write
	li	a1,19
	li	a0,1664
	call	milan_write
	li	a1,513
	li	a0,1740
	call	milan_write
	li	a1,3
	li	a0,1872
	call	milan_write
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
.LFE59:
	.size	configure_fabric, .-configure_fabric
	.section	.rodata
	.align	2
.LC34:
	.string	"Milan baremetal: fabric entity enabled; UART diagnostics ready."
	.text
	.align	2
	.type	entity_advertise, @function
entity_advertise:
.LFB60:
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
	lw	a5,-20(s0)
	beq	a5,zero,.L306
	li	a5,4096
	addi	a0,a5,-1760
	call	milan_read
	mv	a5,a0
	ori	a5,a5,1
	mv	a1,a5
	li	a5,4096
	addi	a0,a5,-1760
	call	milan_write
	li	a0,1536
	call	milan_read
	mv	a5,a0
	ori	a5,a5,1
	mv	a1,a5
	li	a0,1536
	call	milan_write
	lla	a0,.LC34
	call	puts@plt
	j	.L303
.L306:
	nop
.L303:
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE60:
	.size	entity_advertise, .-entity_advertise
	.section	.rodata
	.align	2
.LC35:
	.string	"Milan baremetal: AEM image missing at QSPI +0x%08x; entity disabled.\n"
	.align	2
.LC36:
	.string	"Milan baremetal: AEM CRC failed (expected %08lx, got %08lx); entity disabled.\n"
	.align	2
.LC37:
	.string	"Milan baremetal: AEM %u B copied QSPI +0x%08x -> 0x%08x, CRC %08lx.\n"
	.text
	.align	2
	.type	load_aem_image, @function
load_aem_image:
.LFB61:
	.cfi_startproc
	addi	sp,sp,-32
	.cfi_def_cfa_offset 32
	sw	ra,28(sp)
	sw	s0,24(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,32
	.cfi_def_cfa 8, 0
	li	a5,551550976
	sw	a5,-28(s0)
	li	a5,2138046464
	sw	a5,-24(s0)
	lw	a5,-28(s0)
	lbu	a5,0(a5)
	andi	a4,a5,0xff
	li	a5,65
	bne	a4,a5,.L308
	lw	a5,-28(s0)
	addi	a5,a5,1
	lbu	a5,0(a5)
	andi	a4,a5,0xff
	li	a5,69
	bne	a4,a5,.L308
	lw	a5,-28(s0)
	addi	a5,a5,2
	lbu	a5,0(a5)
	andi	a4,a5,0xff
	li	a5,77
	bne	a4,a5,.L308
	lw	a5,-28(s0)
	addi	a5,a5,3
	lbu	a5,0(a5)
	andi	a4,a5,0xff
	li	a5,73
	beq	a4,a5,.L309
.L308:
	li	a1,14680064
	lla	a0,.LC35
	call	printf@plt
	li	a5,0
	j	.L310
.L309:
	sw	zero,-32(s0)
	j	.L311
.L312:
	lw	a4,-28(s0)
	lw	a5,-32(s0)
	add	a4,a4,a5
	lw	a3,-24(s0)
	lw	a5,-32(s0)
	add	a5,a3,a5
	lbu	a4,0(a4)
	andi	a4,a4,0xff
	sb	a4,0(a5)
	lw	a5,-32(s0)
	addi	a5,a5,1
	sw	a5,-32(s0)
.L311:
	lw	a4,-32(s0)
	li	a5,4096
	bltu	a4,a5,.L312
#APP
# 1640 "/tmp/milan-census-s8bsel5_/milan_baremetal.c" 1
	fence rw, rw
# 0 "" 2
#NO_APP
	li	a1,4096
	li	a0,2138046464
	call	crc32@plt
	sw	a0,-20(s0)
	lw	a4,-20(s0)
	li	a5,-559038464
	addi	a5,a5,-273
	beq	a4,a5,.L313
	lw	a2,-20(s0)
	li	a5,-559038464
	addi	a1,a5,-273
	lla	a0,.LC36
	call	printf@plt
	li	a5,0
	j	.L310
.L313:
	lw	a4,-20(s0)
	li	a3,2138046464
	li	a2,14680064
	li	a1,4096
	lla	a0,.LC37
	call	printf@plt
	li	a5,1
.L310:
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
.LFE61:
	.size	load_aem_image, .-load_aem_image
	.section	.rodata
	.align	2
.LC38:
	.string	"Milan baremetal: CSR ID=%08lx VERSION=%08lx, RV32I machine mode, no MMU/cache.\n"
	.align	2
.LC39:
	.string	"Milan baremetal: CSR identity mismatch; fabric remains disabled."
	.text
	.align	2
	.type	milan_init, @function
milan_init:
.LFB62:
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
	lla	a0,.LC38
	call	printf@plt
	lw	a4,-20(s0)
	li	a5,1296650240
	addi	a5,a5,-946
	beq	a4,a5,.L315
	lla	a0,.LC39
	call	puts@plt
	j	.L314
.L315:
	call	configure_fabric
	call	load_aem_image
	mv	a4,a0
	lla	a5,aem_loaded
	sw	a4,0(a5)
	call	nvm_boot
	lla	a5,aem_loaded
	lw	a5,0(a5)
	mv	a0,a5
	call	entity_advertise
.L314:
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE62:
	.size	milan_init, .-milan_init
	.section	.data.rel.ro.local
	.align	2
	.type	milan_init_i, @object
	.size	milan_init_i, 4
milan_init_i:
	.word	milan_init
	.section	.rodata
	.align	2
.LC40:
	.string	"loaded"
	.align	2
.LC41:
	.string	"disabled"
	.align	2
.LC42:
	.string	"ID=%08lx VERSION=%08lx PTP_CTRL=%08lx ADP_CTRL=%08lx PP_CTRL=%08lx PP_STAT=%08lx AEM=%s\n"
	.align	2
.LC43:
	.string	"GPTP_GM=%08lx%08lx GPTP_PARENT=%08lx%08lx PDELAY_NS=%lu AS_PATH_COUNT=%lu AS_PATH_GEN=%lu CLKV_STAT=%08lx SYNC=%lu ASCAPABLE=%lu TU=%lu GPTP_LAT=%08lx\n"
	.text
	.align	2
	.type	milan_status_handler, @function
milan_status_handler:
.LFB63:
	.cfi_startproc
	addi	sp,sp,-112
	.cfi_def_cfa_offset 112
	sw	ra,108(sp)
	sw	s0,104(sp)
	sw	s1,100(sp)
	sw	s2,96(sp)
	sw	s3,92(sp)
	sw	s4,88(sp)
	sw	s5,84(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	.cfi_offset 9, -12
	.cfi_offset 18, -16
	.cfi_offset 19, -20
	.cfi_offset 20, -24
	.cfi_offset 21, -28
	addi	s0,sp,112
	.cfi_def_cfa 8, 0
	sw	a0,-68(s0)
	sw	a1,-72(s0)
	li	a0,1572
	call	milan_read
	sw	a0,-64(s0)
	li	a0,1576
	call	milan_read
	sw	a0,-60(s0)
	li	a0,1840
	call	milan_read
	sw	a0,-56(s0)
	li	a0,1844
	call	milan_read
	sw	a0,-52(s0)
	li	a0,1764
	call	milan_read
	sw	a0,-48(s0)
	li	a0,2020
	call	milan_read
	sw	a0,-44(s0)
	li	a0,1916
	call	milan_read
	sw	a0,-40(s0)
	li	a0,2032
	call	milan_read
	sw	a0,-36(s0)
	li	a0,0
	call	milan_read
	mv	s1,a0
	li	a0,4
	call	milan_read
	mv	s2,a0
	li	a0,1280
	call	milan_read
	mv	s3,a0
	li	a0,1536
	call	milan_read
	mv	s4,a0
	li	a5,4096
	addi	a0,a5,-1760
	call	milan_read
	mv	s5,a0
	li	a5,4096
	addi	a0,a5,-1756
	call	milan_read
	mv	a4,a0
	lla	a5,aem_loaded
	lw	a5,0(a5)
	beq	a5,zero,.L318
	lla	a5,.LC40
	j	.L319
.L318:
	lla	a5,.LC41
.L319:
	mv	a7,a5
	mv	a6,a4
	mv	a5,s5
	mv	a4,s4
	mv	a3,s3
	mv	a2,s2
	mv	a1,s1
	lla	a0,.LC42
	call	printf@plt
	lw	a5,-44(s0)
	andi	a1,a5,15
	lw	a5,-44(s0)
	srli	a5,a5,4
	andi	a0,a5,15
	lw	a5,-40(s0)
	srli	a5,a5,1
	andi	a5,a5,1
	lw	a4,-40(s0)
	srli	a4,a4,16
	andi	a4,a4,1
	lw	a3,-40(s0)
	andi	a3,a3,1
	lw	a2,-36(s0)
	sw	a2,16(sp)
	sw	a3,12(sp)
	sw	a4,8(sp)
	sw	a5,4(sp)
	lw	a5,-40(s0)
	sw	a5,0(sp)
	mv	a7,a0
	mv	a6,a1
	lw	a5,-48(s0)
	lw	a4,-56(s0)
	lw	a3,-52(s0)
	lw	a2,-64(s0)
	lw	a1,-60(s0)
	lla	a0,.LC43
	call	printf@plt
	call	gettime_ns
	mv	a4,a0
	mv	a5,a1
	mv	a0,a4
	mv	a1,a5
	call	print_tod
	nop
	lw	ra,108(sp)
	.cfi_restore 1
	lw	s0,104(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 112
	lw	s1,100(sp)
	.cfi_restore 9
	lw	s2,96(sp)
	.cfi_restore 18
	lw	s3,92(sp)
	.cfi_restore 19
	lw	s4,88(sp)
	.cfi_restore 20
	lw	s5,84(sp)
	.cfi_restore 21
	addi	sp,sp,112
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE63:
	.size	milan_status_handler, .-milan_status_handler
	.section	.data.rel.ro.local
	.align	2
	.type	milan_status_c, @object
	.size	milan_status_c, 4
milan_status_c:
	.word	milan_status_handler
	.text
	.align	2
	.type	nvm_arg_is, @function
nvm_arg_is:
.LFB64:
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
	sw	a1,-24(s0)
	j	.L321
.L323:
	lw	a5,-20(s0)
	addi	a5,a5,1
	sw	a5,-20(s0)
	lw	a5,-24(s0)
	addi	a5,a5,1
	sw	a5,-24(s0)
.L321:
	lw	a5,-20(s0)
	lbu	a5,0(a5)
	beq	a5,zero,.L322
	lw	a5,-20(s0)
	lbu	a4,0(a5)
	lw	a5,-24(s0)
	lbu	a5,0(a5)
	beq	a4,a5,.L323
.L322:
	lw	a5,-20(s0)
	lbu	a5,0(a5)
	bne	a5,zero,.L324
	lw	a5,-24(s0)
	lbu	a5,0(a5)
	bne	a5,zero,.L324
	li	a5,1
	j	.L326
.L324:
	li	a5,0
.L326:
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
.LFE64:
	.size	nvm_arg_is, .-nvm_arg_is
	.section	.rodata
	.align	2
.LC44:
	.string	"writer retired"
	.align	2
.LC45:
	.string	"writer disabled"
	.align	2
.LC46:
	.string	"writer live"
	.align	2
.LC47:
	.string	"NVM: slot A %s seq %lu, slot B %s seq %lu, authoritative %c, image seq %lu, %u records, %u B at 0x%08x, %s\n"
	.align	2
.LC48:
	.string	"NVM: PP_NVM_STAT=%08lx backed=%lu dirty=%lu stale=%lu valid=%lu commit_busy=%lu dev_busy=%lu pend=%lu unres=%lu load_pend=%lu load_acc=%lu reload_ref=%lu verdict=%s; commits ok=%u failed=%u captures refused=%u acks refused=%u last=%s\n"
	.align	2
.LC49:
	.string	"NVM: unresolved records, their last verified bytes stand:"
	.align	2
.LC50:
	.string	" 0x%02x"
	.text
	.align	2
	.type	nvm_print_status, @function
nvm_print_status:
.LFB65:
	.cfi_startproc
	addi	sp,sp,-112
	.cfi_def_cfa_offset 112
	sw	ra,108(sp)
	sw	s0,104(sp)
	sw	s1,100(sp)
	sw	s2,96(sp)
	sw	s3,92(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	.cfi_offset 9, -12
	.cfi_offset 18, -16
	.cfi_offset 19, -20
	addi	s0,sp,112
	.cfi_def_cfa 8, 0
	li	a0,15597568
	call	nvm_slot
	mv	a5,a0
	mv	a0,a5
	call	nvm_validate
	sw	a0,-56(s0)
	li	a0,15663104
	call	nvm_slot
	mv	a5,a0
	mv	a0,a5
	call	nvm_validate
	sw	a0,-52(s0)
	lw	a5,-56(s0)
	bne	a5,zero,.L328
	li	a0,15597568
	call	nvm_slot
	mv	a5,a0
	mv	a0,a5
	call	nvm_seq_of
	mv	a5,a0
	j	.L329
.L328:
	li	a5,0
.L329:
	sw	a5,-48(s0)
	lw	a5,-52(s0)
	bne	a5,zero,.L330
	li	a0,15663104
	call	nvm_slot
	mv	a5,a0
	mv	a0,a5
	call	nvm_seq_of
	mv	a5,a0
	j	.L331
.L330:
	li	a5,0
.L331:
	sw	a5,-44(s0)
	li	a5,4096
	addi	a0,a5,-1732
	call	milan_read
	sw	a0,-40(s0)
	lla	a4,nvm_verdict_name
	lw	a5,-56(s0)
	slli	a5,a5,2
	add	a5,a4,a5
	lw	s1,0(a5)
	lla	a4,nvm_verdict_name
	lw	a5,-52(s0)
	slli	a5,a5,2
	add	a5,a4,a5
	lw	s2,0(a5)
	lla	a5,nvm_auth_slot
	lw	a5,0(a5)
	mv	a0,a5
	call	nvm_slot_letter
	mv	a5,a0
	mv	a3,a5
	lla	a5,nvm_seq
	lw	a4,0(a5)
	lla	a5,nvm_ready
	lw	a5,0(a5)
	bne	a5,zero,.L332
	lla	a5,nvm_retired
	lw	a5,0(a5)
	beq	a5,zero,.L333
	lla	a5,.LC44
	j	.L335
.L333:
	lla	a5,.LC45
	j	.L335
.L332:
	lla	a5,.LC46
.L335:
	sw	a5,8(sp)
	li	a5,2139025408
	sw	a5,4(sp)
	li	a5,4096
	addi	a5,a5,-1400
	sw	a5,0(sp)
	li	a7,46
	mv	a6,a4
	mv	a5,a3
	lw	a4,-44(s0)
	mv	a3,s2
	lw	a2,-48(s0)
	mv	a1,s1
	lla	a0,.LC47
	call	printf@plt
	lw	a5,-40(s0)
	srli	a5,a5,6
	andi	t6,a5,1
	lw	a5,-40(s0)
	srli	a5,a5,8
	andi	t0,a5,1
	lw	a5,-40(s0)
	srli	a5,a5,9
	andi	t2,a5,1
	lw	a5,-40(s0)
	srli	a5,a5,7
	andi	s1,a5,1
	lw	a5,-40(s0)
	srli	a5,a5,10
	andi	s2,a5,1
	lw	a5,-40(s0)
	srli	a5,a5,4
	andi	s3,a5,1
	lw	a5,-40(s0)
	srli	a5,a5,22
	andi	a5,a5,1
	lw	a4,-40(s0)
	srli	a4,a4,23
	andi	a4,a4,1
	lw	a3,-40(s0)
	srli	a3,a3,3
	andi	a3,a3,1
	lw	a2,-40(s0)
	srli	a2,a2,2
	andi	a2,a2,1
	lw	a1,-40(s0)
	srli	a1,a1,11
	andi	a1,a1,1
	lw	a0,-40(s0)
	srli	a0,a0,12
	andi	a0,a0,15
	lla	a6,nvm_verdict_name
	slli	a0,a0,2
	add	a0,a6,a0
	lw	a0,0(a0)
	lla	a6,nvm_commits_ok
	lw	a6,0(a6)
	lla	a7,nvm_commits_failed
	lw	a7,0(a7)
	lla	t1,nvm_captures_refused
	lw	t1,0(t1)
	lla	t3,nvm_acks_refused
	lw	t3,0(t3)
	lla	t4,nvm_last_verdict
	lw	t4,0(t4)
	lla	t5,nvm_verdict_name
	slli	t4,t4,2
	add	t4,t5,t4
	lw	t4,0(t4)
	sw	t4,40(sp)
	sw	t3,36(sp)
	sw	t1,32(sp)
	sw	a7,28(sp)
	sw	a6,24(sp)
	sw	a0,20(sp)
	sw	a1,16(sp)
	sw	a2,12(sp)
	sw	a3,8(sp)
	sw	a4,4(sp)
	sw	a5,0(sp)
	mv	a7,s3
	mv	a6,s2
	mv	a5,s1
	mv	a4,t2
	mv	a3,t0
	mv	a2,t6
	lw	a1,-40(s0)
	lla	a0,.LC48
	call	printf@plt
	lw	a4,-40(s0)
	li	a5,8388608
	and	a5,a4,a5
	beq	a5,zero,.L342
	lla	a0,.LC49
	call	printf@plt
	sw	zero,-64(s0)
	j	.L337
.L341:
	lw	a5,-64(s0)
	addi	a5,a5,8
	mv	a0,a5
	call	nvm_word_read
	sw	a0,-36(s0)
	sw	zero,-60(s0)
	j	.L338
.L340:
	lw	a5,-60(s0)
	lw	a4,-36(s0)
	srl	a5,a4,a5
	andi	a5,a5,1
	beq	a5,zero,.L339
	lw	a5,-64(s0)
	slli	a4,a5,5
	lw	a5,-60(s0)
	add	a5,a4,a5
	mv	a1,a5
	lla	a0,.LC50
	call	printf@plt
.L339:
	lw	a5,-60(s0)
	addi	a5,a5,1
	sw	a5,-60(s0)
.L338:
	lw	a4,-60(s0)
	li	a5,31
	bleu	a4,a5,.L340
	lw	a5,-64(s0)
	addi	a5,a5,1
	sw	a5,-64(s0)
.L337:
	lw	a4,-64(s0)
	li	a5,7
	bleu	a4,a5,.L341
	li	a0,10
	call	putchar@plt
.L342:
	nop
	lw	ra,108(sp)
	.cfi_restore 1
	lw	s0,104(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 112
	lw	s1,100(sp)
	.cfi_restore 9
	lw	s2,96(sp)
	.cfi_restore 18
	lw	s3,92(sp)
	.cfi_restore 19
	addi	sp,sp,112
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE65:
	.size	nvm_print_status, .-nvm_print_status
	.section	.rodata
	.align	2
.LC51:
	.string	"commit"
	.align	2
.LC52:
	.string	"NVM: the writer is disabled on this build."
	.align	2
.LC53:
	.string	"console"
	.align	2
.LC54:
	.string	"wipe"
	.align	2
.LC55:
	.string	"erased"
	.align	2
.LC56:
	.string	"ERASE FAILED"
	.align	2
.LC57:
	.string	"NVM: slot A %s, slot B %s; the staged image is unchanged, reboot to observe a blank boot.\n"
	.align	2
.LC58:
	.string	"milan_nvm [commit|wipe]"
	.text
	.align	2
	.type	milan_nvm_handler, @function
milan_nvm_handler:
.LFB66:
	.cfi_startproc
	addi	sp,sp,-48
	.cfi_def_cfa_offset 48
	sw	ra,44(sp)
	sw	s0,40(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,48
	.cfi_def_cfa 8, 0
	sw	a0,-36(s0)
	sw	a1,-40(s0)
	lw	a5,-36(s0)
	bne	a5,zero,.L344
	call	nvm_print_status
	j	.L343
.L344:
	lw	a4,-36(s0)
	li	a5,1
	bne	a4,a5,.L346
	lw	a5,-40(s0)
	lw	a5,0(a5)
	lla	a1,.LC51
	mv	a0,a5
	call	nvm_arg_is
	mv	a5,a0
	beq	a5,zero,.L346
	lla	a5,nvm_ready
	lw	a5,0(a5)
	bne	a5,zero,.L347
	lla	a0,.LC52
	call	puts@plt
	j	.L343
.L347:
	lla	a0,.LC53
	call	nvm_commit
	j	.L343
.L346:
	lw	a4,-36(s0)
	li	a5,1
	bne	a4,a5,.L349
	lw	a5,-40(s0)
	lw	a5,0(a5)
	lla	a1,.LC54
	mv	a0,a5
	call	nvm_arg_is
	mv	a5,a0
	beq	a5,zero,.L349
	li	a0,15597568
	call	nvm_slot_erase
	sw	a0,-24(s0)
	call	nvm_heartbeat_tick
	li	a0,15663104
	call	nvm_slot_erase
	sw	a0,-20(s0)
	lla	a5,nvm_auth_slot
	li	a4,-1
	sw	a4,0(a5)
	lw	a5,-24(s0)
	beq	a5,zero,.L350
	lla	a5,.LC55
	j	.L351
.L350:
	lla	a5,.LC56
.L351:
	lw	a4,-20(s0)
	beq	a4,zero,.L352
	lla	a4,.LC55
	j	.L353
.L352:
	lla	a4,.LC56
.L353:
	mv	a2,a4
	mv	a1,a5
	lla	a0,.LC57
	call	printf@plt
	j	.L343
.L349:
	lla	a0,.LC58
	call	puts@plt
.L343:
	lw	ra,44(sp)
	.cfi_restore 1
	lw	s0,40(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 48
	addi	sp,sp,48
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE66:
	.size	milan_nvm_handler, .-milan_nvm_handler
	.section	.data.rel.ro.local
	.align	2
	.type	milan_nvm_c, @object
	.size	milan_nvm_c, 4
milan_nvm_c:
	.word	milan_nvm_handler
	.text
	.align	2
	.type	milan_gettime_handler, @function
milan_gettime_handler:
.LFB67:
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
	sw	a1,-24(s0)
	call	gettime_ns
	mv	a4,a0
	mv	a5,a1
	mv	a0,a4
	mv	a1,a5
	call	print_tod
	nop
	lw	ra,28(sp)
	.cfi_restore 1
	lw	s0,24(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 32
	addi	sp,sp,32
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE67:
	.size	milan_gettime_handler, .-milan_gettime_handler
	.section	.data.rel.ro.local
	.align	2
	.type	milan_gettime_c, @object
	.size	milan_gettime_c, 4
milan_gettime_c:
	.word	milan_gettime_handler
	.section	.rodata
	.align	2
.LC59:
	.string	"milan_settime <tai-seconds> [nanoseconds]"
	.text
	.align	2
	.type	milan_settime_handler, @function
milan_settime_handler:
.LFB68:
	.cfi_startproc
	addi	sp,sp,-64
	.cfi_def_cfa_offset 64
	sw	ra,60(sp)
	sw	s0,56(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	addi	s0,sp,64
	.cfi_def_cfa 8, 0
	sw	a0,-52(s0)
	sw	a1,-56(s0)
	la	a5,__stack_chk_guard
	lw	a4, 0(a5)
	sw	a4, -20(s0)
	li	a4, 0
	li	a5,0
	li	a6,0
	sw	a5,-40(s0)
	sw	a6,-36(s0)
	lw	a5,-52(s0)
	ble	a5,zero,.L356
	lw	a4,-52(s0)
	li	a5,2
	bgt	a4,a5,.L356
	lw	a5,-56(s0)
	lw	a5,0(a5)
	addi	a4,s0,-48
	mv	a1,a4
	mv	a0,a5
	call	parse_u64
	mv	a5,a0
	beq	a5,zero,.L356
	lw	a4,-52(s0)
	li	a5,2
	bne	a4,a5,.L357
	lw	a5,-56(s0)
	addi	a5,a5,4
	lw	a5,0(a5)
	addi	a4,s0,-40
	mv	a1,a4
	mv	a0,a5
	call	parse_u64
	mv	a5,a0
	beq	a5,zero,.L356
.L357:
	lw	a0,-48(s0)
	lw	a1,-44(s0)
	lw	a2,-40(s0)
	lw	a3,-36(s0)
	addi	a5,s0,-32
	mv	a4,a5
	call	seconds_to_ns
	mv	a5,a0
	bne	a5,zero,.L358
.L356:
	lla	a0,.LC59
	call	puts@plt
	j	.L355
.L358:
	lw	a4,-32(s0)
	lw	a5,-28(s0)
	mv	a0,a4
	mv	a1,a5
	call	settime_ns
	call	gettime_ns
	mv	a4,a0
	mv	a5,a1
	mv	a0,a4
	mv	a1,a5
	call	print_tod
.L355:
	la	a5,__stack_chk_guard
	lw	a4, -20(s0)
	lw	a5, 0(a5)
	xor	a5, a4, a5
	li	a4, 0
	beq	a5,zero,.L360
	call	__stack_chk_fail@plt
.L360:
	lw	ra,60(sp)
	.cfi_restore 1
	lw	s0,56(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 64
	addi	sp,sp,64
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE68:
	.size	milan_settime_handler, .-milan_settime_handler
	.section	.data.rel.ro.local
	.align	2
	.type	milan_settime_c, @object
	.size	milan_settime_c, 4
milan_settime_c:
	.word	milan_settime_handler
	.section	.rodata
	.align	2
.LC60:
	.string	"milan_utc <utc-seconds> <nanoseconds> <tai-minus-utc>"
	.align	2
.LC61:
	.string	"UTC applied with TAI-UTC=%lu s; "
	.text
	.align	2
	.type	milan_utc_handler, @function
milan_utc_handler:
.LFB69:
	.cfi_startproc
	addi	sp,sp,-80
	.cfi_def_cfa_offset 80
	sw	ra,76(sp)
	sw	s0,72(sp)
	sw	s2,68(sp)
	sw	s3,64(sp)
	.cfi_offset 1, -4
	.cfi_offset 8, -8
	.cfi_offset 18, -12
	.cfi_offset 19, -16
	addi	s0,sp,80
	.cfi_def_cfa 8, 0
	sw	a0,-68(s0)
	sw	a1,-72(s0)
	la	a5,__stack_chk_guard
	lw	a4, 0(a5)
	sw	a4, -20(s0)
	li	a4, 0
	lw	a4,-68(s0)
	li	a5,3
	bne	a4,a5,.L362
	lw	a5,-72(s0)
	lw	a5,0(a5)
	addi	a4,s0,-64
	mv	a1,a4
	mv	a0,a5
	call	parse_u64
	mv	a5,a0
	beq	a5,zero,.L362
	lw	a5,-72(s0)
	addi	a5,a5,4
	lw	a5,0(a5)
	addi	a4,s0,-56
	mv	a1,a4
	mv	a0,a5
	call	parse_u64
	mv	a5,a0
	beq	a5,zero,.L362
	lw	a5,-72(s0)
	addi	a5,a5,8
	lw	a5,0(a5)
	addi	a4,s0,-48
	mv	a1,a4
	mv	a0,a5
	call	parse_u64
	mv	a5,a0
	beq	a5,zero,.L362
	lw	a4,-64(s0)
	lw	a5,-60(s0)
	not	s2,a4
	not	s3,a5
	lw	a4,-48(s0)
	lw	a5,-44(s0)
	mv	a2,a5
	mv	a3,s3
	bgtu	a2,a3,.L362
	mv	a2,a5
	mv	a3,s3
	bne	a2,a3,.L367
	mv	a5,s2
	bgtu	a4,a5,.L362
.L367:
	lw	a2,-64(s0)
	lw	a3,-60(s0)
	lw	a0,-48(s0)
	lw	a1,-44(s0)
	add	a4,a2,a0
	mv	a6,a4
	sltu	a6,a6,a2
	add	a5,a3,a1
	add	a3,a6,a5
	mv	a5,a3
	sw	a4,-32(s0)
	sw	a5,-28(s0)
	lw	a2,-56(s0)
	lw	a3,-52(s0)
	addi	a5,s0,-40
	mv	a4,a5
	lw	a0,-32(s0)
	lw	a1,-28(s0)
	call	seconds_to_ns
	mv	a5,a0
	bne	a5,zero,.L364
.L362:
	lla	a0,.LC60
	call	puts@plt
	j	.L361
.L364:
	lw	a4,-40(s0)
	lw	a5,-36(s0)
	mv	a0,a4
	mv	a1,a5
	call	settime_ns
	lw	a4,-48(s0)
	lw	a5,-44(s0)
	mv	a5,a4
	mv	a1,a5
	lla	a0,.LC61
	call	printf@plt
	call	gettime_ns
	mv	a4,a0
	mv	a5,a1
	mv	a0,a4
	mv	a1,a5
	call	print_tod
.L361:
	la	a5,__stack_chk_guard
	lw	a4, -20(s0)
	lw	a5, 0(a5)
	xor	a5, a4, a5
	li	a4, 0
	beq	a5,zero,.L366
	call	__stack_chk_fail@plt
.L366:
	lw	ra,76(sp)
	.cfi_restore 1
	lw	s0,72(sp)
	.cfi_restore 8
	.cfi_def_cfa 2, 80
	lw	s2,68(sp)
	.cfi_restore 18
	lw	s3,64(sp)
	.cfi_restore 19
	addi	sp,sp,80
	.cfi_def_cfa_offset 0
	jr	ra
	.cfi_endproc
.LFE69:
	.size	milan_utc_handler, .-milan_utc_handler
	.section	.data.rel.ro.local
	.align	2
	.type	milan_utc_c, @object
	.size	milan_utc_c, 4
milan_utc_c:
	.word	milan_utc_handler
	.globl	__udivdi3
	.ident	"GCC: (Buildroot 2026.05) 14.3.0"
	.section	.note.GNU-stack,"",@progbits
