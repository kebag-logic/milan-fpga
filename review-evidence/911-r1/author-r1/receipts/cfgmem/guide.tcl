set B <output>/handover
set O 0xa00000
write_cfgmem -force -format bin -interface spix4 -size 16 \
    -loadbit "up 0x0 $B/gateware/alinx_ax7101.bit" \
    -loaddata "up $O $B/aem_desc.bin" -file <scratch>/cfgmem/image_set.bin
