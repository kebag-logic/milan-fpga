#!/usr/bin/env bash
# syn.sh <clone> <out> <gptp-flag>: Vivado SYNTHESIS ONLY of the 8x8/1if split image by the train gate's recipe
# (gate15 g8x8 argv.txt, its --eth-port e2 and flow flags), with the gate's own ctrl_app.elf so the firmware memory is
# identical across arms, and <gptp-flag> (--fabric-gptp or --no-fabric-gptp or --sw-gptp) in place of --fabric-gptp.
# The generated Tcl is cut after write_checkpoint of the synthesized design. Run inside vivado-slot.sh.
set -u
L=$1; O=$2; GF=$3; STEM=endstation_ax7101_8x8; G=<gate15-work>
T=<scratch>
mkdir -p "$O"; date -Iseconds > "$O.start"
C=$(taskset -cp $$ | sed 's/.*: //'); TH=$(python3 -c "import sys
n=0
for p in sys.argv[1].split(','):
    a,_,b=p.partition('-'); n+=int(b or a)-int(a)+1
print(min(n,int(__import__('os').environ.get('SYN_THREADS','16'))))" "$C")
echo "cpus $C threads $TH"
source $T/bin/env.sh
export HOME=<home>
source <xilinx>/2026.1/Vivado/settings64.sh
cd "$L"
echo "head $(git rev-parse HEAD); status $(git status --porcelain | tr '\n' ' ')"
/usr/bin/python3 sw/builder/endstation_builder.py configs/$STEM.yaml --placement split > "$O/builder.log" 2>&1 || { echo builder failed; echo 5 > "$O.rc"; exit 5; }
cp <gate15-clone>/sw/builder/out/$STEM/ctrl_app.elf sw/builder/out/$STEM/ctrl_app.elf
sha256sum sw/builder/out/$STEM/ctrl_app.elf
mapfile -t ARGV < "$G/argv.txt"
for i in "${!ARGV[@]}"; do [ "${ARGV[$i]}" = "--fabric-gptp" ] && ARGV[$i]=$GF; done
FLOW=(--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt)
cd sw/litex
echo "python3 milan_soc.py ${ARGV[*]} --eth-port e2 --entity-gen-dir $L/configs/generated/$STEM ${FLOW[*]} --no-compile-software --vivado-max-threads $TH --output-dir $O/b"
python3 milan_soc.py "${ARGV[@]}" --eth-port e2 --entity-gen-dir "$L/configs/generated/$STEM" "${FLOW[@]}" \
  --no-compile-software --vivado-max-threads "$TH" --output-dir "$O/b" > "$O/gen.log" 2>&1 || { echo gen failed; tail -20 "$O/gen.log"; echo 6 > "$O.rc"; exit 6; }
cd "$O/b/gateware"
n=$(grep -n "^write_checkpoint -force alinx_ax7101_synth.dcp" alinx_ax7101.tcl | cut -d: -f1)
head -n "$n" alinx_ax7101.tcl > synth_only.tcl
vivado -mode batch -nojournal -log synth.log -source synth_only.tcl > /dev/null 2>&1
rc=$?
echo "$rc" > "$O.rc"; date -Iseconds > "$O.end"
grep -A8 "Slice LUTs\*" alinx_ax7101_utilization_synth.rpt | head -9
echo "== END rc=$rc $(date -Iseconds)"
exit $rc
