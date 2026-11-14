set f [open parts.txt w]
foreach p [get_cfgmem_parts] { if {[string match -nocase {*25q*128*} $p]} { puts $f $p } }
close $f
set B <scratch>/buildB
set O 0xa00000
write_cfgmem -force -format bin -interface spix4 -size 16 \
    -loadbit "up 0x0 $B/gateware/alinx_ax7101.bit" \
    -loaddata "up $O $B/aem_desc.bin" -file image_set.bin
