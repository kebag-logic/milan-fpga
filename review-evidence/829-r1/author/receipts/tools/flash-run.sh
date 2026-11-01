#!/usr/bin/env bash
# flash-run.sh <tree> <build> <out>: first write of a build over another image, under the bench lock. The recovery
# path: flash-images writes the AEM slot and flash writes offset 0, in that order, so the commit artifact goes last.
# A listen-only console capture runs across both writes and the boot that follows.
set -u
tree=$1 build=$2 out=$3
tools=$VALIDATION_STORAGE/583-a724b/tools
export TMPDIR=$VALIDATION_STORAGE/829-a725b/tmp
export ALLOW_NONATOMIC_FLASH=1 SERIAL=<jtag-serial> CABLE=digilent FPGA_PART=xc7a100tcsg324
export LAYOUT=$build/flashboot_layout.json BIT=$build/gateware/digilent_arty.bit EXPECTED_GPTP_OWNER=fabric
port=/dev/serial/by-id/<adapter>
echo "== START $(date -Iseconds) build=$build"
sha256sum "$BIT" "$LAYOUT" "$build/aem_desc.bin"
stty -F $port -a | tr ';' '\n' | grep -a -o -- '-\?hupcl'
python3 "$tools/console_log.py" "$port" "$out/console-flash.txt" 600 &
con=$!
cd "$tree" || exit 3
sw/litex/deploy.sh check-images; rc0=$?
echo "== check-images rc=$rc0 $(date -Iseconds)"
rc1=99; rc2=99
if [ "$rc0" = 0 ]; then
    sw/litex/deploy.sh flash-images; rc1=$?
    echo "== flash-images rc=$rc1 $(date -Iseconds)"
fi
if [ "$rc1" = 0 ]; then
    sw/litex/deploy.sh flash; rc2=$?
    echo "== flash rc=$rc2 $(date -Iseconds)"
fi
echo "$rc0 $rc1 $rc2" > "$out/flash.rc"
if [ "$rc2" = 0 ]; then
    timeout 60 tail --pid="$con" -f /dev/null
fi
kill "$con" 2>/dev/null
wait "$con" 2>/dev/null
echo "== END-OF-FLASH rcs=$rc0/$rc1/$rc2 $(date -Iseconds)"
