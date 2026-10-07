[R529] NEGATIVE - exact head 8b78a8fd36864246336c71c061ac4f21d629952f

Independent delta verdict recorded before reading prior review findings or other reviewer reports. All five lenses have been applied. Public executable-evidence reconciliation and prior-finding disposition will be added before final delivery.

R529-3-F1: MINOR; Docs, Tests; sw/firmware/ctrl/maap/README.md:155. The executable reproduction command sets CTRL_RV32_CC, which the merged selector no longer reads (sw/firmware/gtest/fw_rv32.py:31). MILAN_RV32_CC is the supported selector. The independent selector probe demonstrates that the documented variable is ignored, so the intended compiler may not be used or the required arm may refuse. Required outcome: update the command to MILAN_RV32_CC and verify compiler selection with competing or absent fallback candidates. This changes executable validation input, so it is not purely prose residue.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | maap.c assertion guards, test_maap.cpp link-bounce case, F2 assignment, #678, runtime headers and compiler flags | R529-3 delta; untouched protocol behavior carried from R529-2 subject to public reconciliation | 8b78a8fd36864246336c71c061ac4f21d629952f |
| RTL | CLEAN | Base/head and prior-head diffs; unchanged MAAP RTL and CSR interface; imported AAF gate is exact dev; maap differential 12/12 | R529-3 delta; R529-2 unchanged F2 interfaces subject to public reconciliation | 8b78a8fd36864246336c71c061ac4f21d629952f |
| Robustness | CLEAN | Debug/release guard controls; Begin/down/up/down/up preference; SDK runtime and hosted-assert plants; one/two-interface mailbox runs | R529-3 delta; R529-2 unchanged behavior subject to public reconciliation | 8b78a8fd36864246336c71c061ac4f21d629952f |
| Tests | UNCLEAN | Three conflict resolutions, exact catalog preservation (192+1), 198 obligations, four partitions; focused receipts; README selector | R529-3; open R529-3-F1 | 8b78a8fd36864246336c71c061ac4f21d629952f |
| Docs | UNCLEAN | ctrl README ten-arm correction; MAAP proof limits; RV32 README versus stale command at maap/README.md:155 | R529-3; open R529-3-F1 | 8b78a8fd36864246336c71c061ac4f21d629952f |

R529-3 FINISHED
