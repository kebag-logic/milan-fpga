[A560]

# Round 13 coverage

Measured by `fw_coverage.py --check --jobs 4`; rc 0.
Raw execution counts precede the unchanged documented exclusions.
Every adjusted line and branch rate is 100%; no ratchet or exclusion changed.

| Source | Raw lines | Raw branches | Adjusted lines | Adjusted branches |
| --- | ---: | ---: | ---: | ---: |
| `sw/firmware/ctrl/acmp/acmp.c` | 742/742 | 348/348 | 100.00 | 100.00 |
| `sw/firmware/ctrl/acmp/acmp_mbx.c` | 73/73 | 26/26 | 100.00 | 100.00 |
| `sw/firmware/ctrl/acmp/acmp_nvm.c` | 38/38 | 10/10 | 100.00 | 100.00 |
| `sw/firmware/ctrl/adp/adp.c` | 204/206 | 95/102 | 100.00 | 100.00 |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/40 | 100.00 | 100.00 |
| `sw/firmware/ctrl/app/ctrl_app.c` | 42/43 | 40/44 | 100.00 | 100.00 |
| `sw/firmware/ctrl/app/ctrl_app_srp.c` | 82/82 | 62/62 | 100.00 | 100.00 |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 101/101 | 62/62 | 100.00 | 100.00 |
| `sw/firmware/ctrl/maap/maap.c` | 209/209 | 140/140 | 100.00 | 100.00 |
| `sw/firmware/ctrl/maap/maap_csr.c` | 39/39 | 18/18 | 100.00 | 100.00 |
| `sw/firmware/ctrl/maap/maap_mbx.c` | 98/98 | 60/60 | 100.00 | 100.00 |
| `sw/firmware/ctrl/mbx/mbx.c` | 189/189 | 74/74 | 100.00 | 100.00 |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 | 100.00 | 100.00 |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 | 100.00 | 100.00 |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 | 100.00 | 100.00 |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 | 100.00 | 100.00 |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 | 100.00 | 100.00 |
| `sw/firmware/ctrl/srp/srp_mbx.c` | 515/515 | 478/478 | 100.00 | 100.00 |
| `sw/firmware/ctrl/wire/wire.h` | 10/10 | 2/2 | 100.00 | 100.00 |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/199 | 106/110 | 100.00 | 100.00 |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/266 | 100.00 | 100.00 |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/64 | 100.00 | 100.00 |
