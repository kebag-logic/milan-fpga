[A325] Parent parameter binding evidence

All 14 explicit processor bindings are documented, declared, and passed through unchanged. The inventory declares 24 parameters; the remaining 10 use their unchanged processor defaults.

| Parameter | Parent expression | Parent location |
|---|---|---|
| `N_STREAM_IN_P` | `N_STREAM_IN_P` | `hdl/milan/KL_pp_shadow.sv:1058` |
| `N_STREAM_OUT_P` | `N_STREAM_OUT_P` | `hdl/milan/KL_pp_shadow.sv:1059` |
| `SRP_DOM_DEF_VID_P` | `SRP_DOM_DEF_VID_P` | `hdl/milan/KL_pp_shadow.sv:1060` |
| `CLK_HZ_P` | `CLK_HZ_P` | `hdl/milan/KL_pp_shadow.sv:1061` |
| `TIM_DIV_US_P` | `TIM_DIV_US_P` | `hdl/milan/KL_pp_shadow.sv:1062` |
| `TIM_DIV_MS_P` | `TIM_DIV_MS_P` | `hdl/milan/KL_pp_shadow.sv:1063` |
| `TROM_HEX_P` | `TROM_HEX_P` | `hdl/milan/KL_pp_shadow.sv:1064` |
| `UCODE_HEX_P` | `UCODE_HEX_P` | `hdl/milan/KL_pp_shadow.sv:1065` |
| `DESC_BASE_P` | `DESC_BASE_P` | `hdl/milan/KL_pp_shadow.sv:1066` |
| `DESC_LINE_BYTES_P` | `DESC_LINE_BYTES_P` | `hdl/milan/KL_pp_shadow.sv:1067` |
| `DESC_IDX_ENTRIES_P` | `DESC_IDX_ENTRIES_P` | `hdl/milan/KL_pp_shadow.sv:1068` |
| `DESC_NAME_ENTRIES_P` | `DESC_NAME_ENTRIES_P` | `hdl/milan/KL_pp_shadow.sv:1069` |
| `DESC_MEM_TMO_CYC_P` | `DESC_MEM_TMO_CYC_P` | `hdl/milan/KL_pp_shadow.sv:1070` |
| `RESP_BASE_P` | `RESP_BASE_P` | `hdl/milan/KL_pp_shadow.sv:1071` |

Defaulted parameters: `N_AUDIO_UNIT_P`, `N_CLK_DOMAIN_P`, `N_CONTROL_P`, `RX_SLOTS_P`, `RX_SLOT_BYTES_P`, `TX_STD_SLOTS_P`, `TX_OVERSIZE_BYTES_P`, `NVM_RS_TMO_CYC_P`, `REG_TL_TIMEOUT_MS_P`, `LOCK_TIMEOUT_MS_P`.

Authorities: `protocol-processor/docs/guides/integrator.md:46`, `protocol-processor/hdl/top/protocol_processor_top.sv:72`, and the unchanged parent wrapper declaration. No inventory claim names a different parent default or override.
