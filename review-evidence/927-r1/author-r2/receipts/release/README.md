# The release image

- `release-export.log`, `RUN-head.txt`, `IMAGES-head-338ece89.sha256`: the release export at 338ece89 (the shipping
  `endstation_ax7101_1x1_tdm8` recipe, clean tree before and after).
- `release-firmware.txt`: the firmware against round 1's base export: `bios.bin` and its disassembly byte-identical;
  `bios.elf` and `libmilan_baremetal.a` byte-identical once their debug sections are stripped.
- `release-pp_resource_gate.txt`: `syn/ooc/pp_resource_gate.py check --endpoint route-1x1 --shipping-selection` on
  the route (`../route/rel2-head-1x1-tdm8-release`): PASS.
