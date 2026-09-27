[A360] BASELINE REFERENCE, updated for #587 at the declared 50 MHz.

This updates the corrected #231 reference. The 1x1 figures remain unchanged; the 8x8 100 MHz figures remain labelled history. Historical page: [merged #231 baseline](https://github.com/kebag-logic/milan-fpga/blob/ac18b50968b12efe4d15c0a06301264b35656b31/docs/findings/PP_SHADOW_BASELINE.md).

Measured 50 MHz tree: `63fe4fb0164d798d44a6476001dc8b887cdd4609`. Updated page and evidence are in local commit `55079500483970ee244f12fa4c94401783f3df6f`, branch `587-8x8-baseline-50mhz`. The maintainer will publish that unpushed commit. Files: `docs/findings/PP_SHADOW_BASELINE.md`, `PP_SHADOW_BASELINE_50MHZ_INPUTS.json`, and `PP_SHADOW_BASELINE_50MHZ_RANKING.tsv`; recipe: `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.

Default-flow totals remain the fit baseline. Ownership attribution comes from the separate run preserving the `KL_pp_shadow` boundary, as decided in #231 (5846064333). Rebuilt wrapper names in the default flow include neighboring datapath logic.

| Integrated 8x8 measurement | Historical 100 MHz | Declared 50 MHz | Delta, 50 minus 100 MHz |
|---|---:|---:|---:|
| Default whole LUTs | 68,136 | 68,047 | -89 |
| Default whole WNS ns | -11.331 | -1.708 | +9.623 |
| Attribution wrapper LUTs | 29,489 | 28,955 | -534 |
| Attribution wrapper internal WNS ns | -10.846 | -1.700 | +9.146 |
| Attribution whole LUTs | 70,206 | 69,923 | -283 |

| Endpoint | Wrapper LUT, default / attribution | AECP LUT, default / attribution | Dynamic-state LUT, default / attribution |
|---|---:|---:|---:|
| Unchanged shipping 1x1 route, 50 MHz | 22,441 / 20,655 | 6,428 / 4,504 | 1,299 / 111 |
| Historical 8x8 synthesis, 100 MHz | 37,809 / 29,489 | 15,199 / 5,025 | 6,915 / 574 |
| Declared 8x8 synthesis, 50 MHz | 38,351 / 28,955 | 15,660 / 5,022 | 7,544 / 574 |

Use attribution rows for consumer analysis, and the default whole-design total for fit. The declared 50 MHz default build still exceeds the 63,400-LUT capacity by 4,647. There is no 8x8 placement or routing claim.

Both synthesis commands and all unchanged public boundary/load probes returned rc 0. Both exported clocks measure 20.000 ns; wrapper parameters bind 50 MHz and the 50-cycle microsecond divider. All recorded source and ROM hashes rechecked successfully, with zero missing-ROM diagnostics. The changed processor pin has identical HDL to the historical pin. Firmware and processor ROM hashes match history; the gPTP image changes with the clock.

At 50 MHz, dynamic-state raw LUT cells are 9,010 / 607 in default / attribution; external-only loads are 5,824 / 0. The attribution wrapper retains 518 external-only raw LUT cells; their load stems and the probe limits are recorded. The page includes complete resource counts and the separate whole-design attribution result.

All assigned local gates passed at the local head. Existing clock/conditional-constraint warnings and 46 inputs / 86 outputs without I/O delays limit timing claims. Independent review and publication remain pending; no hardware claim is made.

