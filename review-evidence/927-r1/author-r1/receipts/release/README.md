# The release image at base 70f4056f and head 1010aa6f

`release_export.sh` (tools/) runs the release ax7101 image's own recipe (`sw/litex/build.sh ax7101`'s `milan_soc.py`
command without `--build`, its shipping flow flags, firmware compiled) on a clean clone of each tree.

- `bios.bin`: `860d4771decf5b92bd167e57c690892d665eec8075902a3468b68e3b3f56041f` at both: byte-identical.
- `bios.elf`'s disassembly (objdump -d, no raw bytes): `3b1c5034ac017b1b89e1a5d4a2e54425c434af4f4652025f448bb296f3c38bd4` at both.
- `bios.elf` and `libmilan_baremetal.a` differ as files, in their debug sections only (they carry the clone's path):
  with `objcopy --strip-debug`, the ELF is `8cebfd66a483655d...` at both, and the archive's one member is identical.

The release firmware image is byte-identical. The release gateware is not: `KL_aaf_clock_meter`'s group reference
and the datapath's all-fabric elaboration change (identity/README.md). Its route (the M0s recipe's integrated
script, which `release_export.sh ... route` writes at the head) was not run in this round: the lane stopped at the
8x8/1if floor first.
