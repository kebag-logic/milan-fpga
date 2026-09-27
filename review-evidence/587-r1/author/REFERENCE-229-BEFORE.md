[A10] **BASELINE REFERENCE, corrected.** This supersedes the "BASELINE REFERENCE -- #231" comment of 2026-09-26 (5845524962). That comment quoted default-flow wrapper and AECP rows as consumption and linked a superseded page.

The baseline page merged with PR #572 as `ac18b509` ([page](https://github.com/kebag-logic/milan-fpga/blob/ac18b50968b12efe4d15c0a06301264b35656b31/docs/findings/PP_SHADOW_BASELINE.md)) (`docs/findings/PP_SHADOW_BASELINE.md`; recipe in `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`). It separates two kinds of figure, as decided on #231 (5846064333):
- **Default-flow totals** are the implementation baseline.
- **Consumer attribution** comes from an attribution-only run that preserves the `KL_pp_shadow` boundary. Vivado's default rebuilt hierarchy moves datapath logic across that boundary.

Wrapper LUT, default versus attribution:

| Endpoint | Wrapper LUT, default / attribution | AECP LUT, default / attribution | Dynamic-state LUT, default / attribution |
|---|---:|---:|---:|
| 1x1 route (shipping) | 22,441 / 20,655 | 6,428 / 4,504 | 1,299 / 111 |
| 8x8 synthesis | 37,809 / 29,489 | 15,199 / 5,025 | 6,915 / 574 |

Use the attribution column to choose optimization tickets. The page gives FF, BRAM, DSP, CARRY4 and WNS. It is the reference since #572 merged as `ac18b509`. The page's 8x8 integrated figures describe the 100 MHz 8x8 configuration; #565 declares 50 MHz, and the 8x8 re-run at that clock is a tracked follow-up.

