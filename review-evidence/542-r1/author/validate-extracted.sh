cd tb/verilator/milan_dp
V=verilator                              # Verilator 5.050
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

# 1. the gate legs, unchanged recipes (make run builds and runs the whole suite)
for l in notify nxn nxn8; do variant $l plain ""; ./obj_${l}_plain/Vmilan_dp_$l | tail -2; done
eval "$(recipe sim | sed 's| -o Vmilan_dp_sim| --Mdir obj_sim_plain -o Vmilan_dp_sim|')" && ./obj_sim_plain/Vmilan_dp_sim | tail -3

# 2. the FIXED checks under the lever, and under the lever with AddressSanitizer
variant notify lever "$LEVER" && ./obj_notify_lever/Vmilan_dp_notify | grep '#542 lever\|checks:'
variant nxn    lever "$LEVER" && ./obj_nxn_lever/Vmilan_dp_nxn       | grep '#542 lever\|checks:'
variant notify asan  "$LEVER $ASAN" && ./obj_notify_asan/Vmilan_dp_notify > obj_notify_asan/run.log 2>&1; \
  grep -c 'AddressSanitizer' obj_notify_asan/run.log; grep 'checks:' obj_notify_asan/run.log

# 3. the same lever against the OLD checks (the fix commit reverse-applied)
(cd "$(git rev-parse --show-toplevel)" && git diff 766b6a149 6c5fa5566 | git apply -R)
variant notify oldlever "$LEVER" && ./obj_notify_oldlever/Vmilan_dp_notify | grep 'FAIL\]\|checks:'
variant nxn    oldlever "$LEVER" && ./obj_nxn_oldlever/Vmilan_dp_nxn       | grep 'FAIL\]\|checks:'
variant notify oldasan  "$LEVER $ASAN" && ./obj_notify_oldasan/Vmilan_dp_notify > obj_notify_oldasan/run.log 2>&1; \
  grep -c 'heap-use-after-free on address' obj_notify_oldasan/run.log
git checkout HEAD -- sim_nxn.cpp
