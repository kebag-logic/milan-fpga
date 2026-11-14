# AX7101 (build.sh ax7101) elaborated at dev b7d69295 and at the lane head 1e604e1b, one clone path, no Vivado

elaboration outputs: 3875 files at b7d69295, 3875 at 1e604e1b (litex.log excluded).
sha256 of the two output hash lists: 0d6cb39912b43c695979e07f2432c4d976c6f3b4817371f3b2e3c364b69ce01a / 25704bb30af0fcefcfd6fe166bad070c1abcf9c128ba61e3e502fa97dcb669c7 (lists not kept: 400 KB each).

files whose bytes differ, and the comparison after removing what differs between any two elaborations:

| file | b7d69295 | 1e604e1b | compared |
|---|---|---|---|
| gateware/alinx_ax7101.v | 6c53b6fb06f31133 | 6c53b6fb06f31133 | body without the LiteX header and hierarchy comment |
| csr.csv | eb58d18619fe7e7f | eb58d18619fe7e7f | without the generated-on timestamp line |
| software/include/generated/soc.h | f1efc260a3b9e34c | f1efc260a3b9e34c | without the generated-on timestamp line |
| software/include/generated/csr.h | 8e94cbad4e75a6fd | 8e94cbad4e75a6fd | without the generated-on timestamp line |
| software/include/generated/mem.h | 5c210454b1facc1e | 5c210454b1facc1e | without the generated-on timestamp line |
| software/include/generated/git.h | 01ba4719c80b6fe9 | 01ba4719c80b6fe9 | without the generated-on timestamp line |

flashboot_layout.json (the one AX7101 output that changes):
```
8a9,10
>   "flash_device": "n25q128a13",
>   "flash_jedec_id": 2144792,
```

The hierarchy comment also differs between the b7d69295 release build and this re-elaboration of b7d69295:
hierarchy comment sha256: release 825010dda66d8b9f, re-elaboration 627ca1c674c04f14, head e63d68b01a680aca

build inputs read by the Vivado script and the builder (140 files: RTL, generated includes, hex, xdc, tcl): sources-b7d69295.sha256 and sources-1e604e1b.sha256, identical.
