set -e
S=$REVIEWS/635-r438-1-packet/scratch/romgen; rm -rf $S; mkdir -p $S
for pin in b2db3a970cedbbff2f8ba813acb96122c442bc58 631eeb342ca1e3fa80e734077a56a943aee76ff1; do
  mkdir -p $S/$pin; git -C $REVIEWS/r438-1-635/protocol-processor archive $pin | tar -x -C $S/$pin
  ( cd $S/$pin && python3 hdl/acmp/rom/gen_ltn_rom.py -o $S/$pin.ltn_rom.hex >/dev/null && python3 hdl/aecp/ucode/gen_ucode.py -o $S/$pin.ucode.hex >/dev/null )
  echo "$pin ltn_rom.hex $(sha256sum < $S/$pin.ltn_rom.hex | cut -d' ' -f1)"
  echo "$pin ucode.hex $(sha256sum < $S/$pin.ucode.hex | cut -d' ' -f1)"
done
