python3 sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/endstation_ax7101_8x8.yaml \
  --interfaces 2 --ledgered-point platform-8x8-two-interfaces --csr-csv "$SOC/csr.csv" --flash-map "$FLASH_MAP" \
  --output "$OUT" --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
