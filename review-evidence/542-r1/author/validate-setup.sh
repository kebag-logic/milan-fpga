cd $LANES/542-notify-pointer/tb/verilator/milan_dp
V=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator
make VERILATOR=$V ltn_rom.hex ucode.hex gptp_ucode.hex
# one leg's build line exactly as `make run` issues it, joined onto one line
recipe() { make -n VERILATOR=$V VERILATOR_JOBS=8 run \
             | sed -e ':a' -e '/\\$/N; s/\\\n//; ta' | grep -E -- "-o Vmilan_dp_$1\$"; }
# build leg $1 into Mdir obj_$1_$2, with the extra Verilator arguments in $3
variant() { local c; c=$(recipe "$1"); c=${c/--Mdir obj_$1/--Mdir obj_$1_$2}
            c=${c/ -o Vmilan_dp_$1/ $3 -o Vmilan_dp_$1}; eval "$c"; }
LEVER='-CFLAGS -DNOTIFY_REALLOC_TB=1'
ASAN='-CFLAGS "-fsanitize=address -fsanitize-recover=address -fno-omit-frame-pointer -g" -LDFLAGS "-fsanitize=address -fsanitize-recover=address"'
export ASAN_OPTIONS=halt_on_error=0:suppress_equal_pcs=0:detect_leaks=1

