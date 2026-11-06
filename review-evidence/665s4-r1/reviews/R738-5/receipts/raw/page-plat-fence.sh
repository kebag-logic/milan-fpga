python3 sw/firmware/ctrl_nvm/plat/gen_flash_port.py --csr-csv "$SOC/csr.csv" \
  --csr-h "$SOC/software/include/generated/csr.h" --out "$FLASH_MAP"
python3 sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml \
  --csr-csv "$SOC/csr.csv" --flash-map "$FLASH_MAP" --output "$OUT" --libc "$RUNTIME/libc.a" \
  --compiler-runtime "$RUNTIME/libcompiler_rt.a"
