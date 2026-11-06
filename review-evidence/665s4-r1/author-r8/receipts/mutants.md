| Mutant | File | Caught by | rc | plat checks green first | Failing words |
|---|---|---|---:|---:|---|
| head: ctrl_image_selftest (no mutant) | none | | 0 | | `ctrl_image self-test: 40 checks PASS` |
| head: stopped_at_link (no mutant) | none | | 0 | | `ctrl_plat_image.py endstation_ax7101_1x1_tdm8, 1 interface(s): exit 2; ELF present False; stopped_at_link True` |
| header-refusal-removed | `ctrl_plat_image.py` | plat: lacking csr.h | 1 | 4 | `AssertionError: ('lacks-csr', '      \|                     ^~~~~~~~~~~~~')` |
| csr-not-required | `ctrl_plat_image.py` | plat: lacking csr.h | 1 | 4 | `AssertionError: ('lacks-csr', '      \|                     ^~~~~~~~~~~~~')` |
| mem-not-required | `ctrl_plat_image.py` | plat: lacking mem.h | 1 | 5 | `AssertionError: ('lacks-mem', '      \|         ^~~~~~~~~~~~~~~~~~~')` |
| lone-json-accepted | `ctrl_plat_image.py` | plat: JSON-only | 1 | 6 | `AssertionError: ('lacks-json-only', 'collect2: error: ld returned 1 exit status')` |
| one-header-accepted | `ctrl_plat_image.py` | plat: lacking csr.h | 1 | 4 | `AssertionError: ('lacks-csr', '      \|                     ^~~~~~~~~~~~~')` |
| names-every-header | `ctrl_plat_image.py` | plat: lacking csr.h | 1 | 4 | `AssertionError: ('lacks-csr', "REFUSED: the flash map lacks generated/csr.h and generated/mem.h: a split platform image is never l` |
| complete-map-refused | `ctrl_plat_image.py` | plat: complete map | 1 | 3 | `AssertionError: REFUSED: the flash map lacks : a split platform image is never linked on the flash port's RV32 stand-ins; gen_flas` |
| fixture-json-only | `ctrl_image_selftest.py` | plat: complete map | 1 | 3 | `AssertionError: REFUSED: the flash map lacks generated/csr.h and generated/mem.h: a split platform image is never linked on the fl` |
| whole-refusal-after-compile | `ctrl_plat_image.py` | plat: no map, nothing left | 1 | 0 | `AssertionError: ('both-archives', 'went on before its refusal', ['0-mbx.o', '0-mbx.su', '1-ctrl_loop.o', '1-ctrl_loop.su', '10-acm` |
| header-refusal-after-compile | `ctrl_plat_image.py` | plat: lacking csr.h | 1 | 4 | `AssertionError: ('lacks-csr', '      \|                     ^~~~~~~~~~~~~')` |
| json-only-refused-after-compile | `ctrl_plat_image.py` | plat: JSON-only, nothing left | 1 | 6 | `AssertionError: ('lacks-json-only', 'went on before its refusal', ['0-mbx.o', '0-mbx.su', '1-ctrl_loop.o', '1-ctrl_loop.su', '10-a` |
| no-map-refusal-removed | `ctrl_plat_image.py` | plat: no map | 1 | 0 | `AssertionError: ('both-archives', 'collect2: error: ld returned 1 exit status')` |
| any-archive-to-all | `ctrl_plat_image.py` | plat: no map | 1 | 1 | `AssertionError: ('the-C-library-alone', 'collect2: error: ld returned 1 exit status')` |
| refused-with-a-map | `ctrl_plat_image.py` | plat: complete map | 1 | 3 | `AssertionError: REFUSED: no --flash-map: a split platform image is never linked on the flash port's RV32 stand-ins; gen_flash_port` |
| compile-only-refused | `ctrl_plat_image.py` | ctrl_runs.stopped_at_link | 1 | 0 | `ctrl_plat_image.py endstation_ax7101_1x1_tdm8, 1 interface(s): exit 2; ELF present False; stopped_at_link False` |
