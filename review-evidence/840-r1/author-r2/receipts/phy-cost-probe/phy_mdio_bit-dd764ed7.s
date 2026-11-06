slli	a0,a0,0x1
slli	a1,a1,0x2
or	a1,a1,a0
lui	a5,0xf0001
sw	a1,-2048(a5)
lw	a0,-2044(a5)
ori	a4,a1,1
sw	a4,-2048(a5)
sw	a1,-2048(a5)
andi	a0,a0,1
ret
