| Parameter | Elaborated (leg) | Shipping (entity definition) | Verdict |
|---|---:|---:|---|
| `N_STREAMS` | 1 | 1 | same |
| `ADP_TALKER_SRC_C` | 2 | 2 | same |
| `ADP_LISTENER_SINK_C` | 2 | 2 | same |
| `CRF_SNK_IDX_C` | 1 | 1 | same |
| `MILAN_CLK_FREQ_HZ` | 100000000 | 50000000 | DIFFERS: verification fabric clock: the obj_ax1x1-geometry legs (ax1x1, aclk, dynmap) keep the 100 MHz default, which the [762-DP] 1 ms step assumes |
| `GPTP_PLANE_EN_P` | 0 | 1 | DIFFERS: direct option OFF (Makefile GPTP_OFF_VFLAGS); the fabric gPTP plane is obj_gptp / obj_ax1x1gptp |
| `TALKER_WIRE_CHANS_P` | 8 | 8 | same |
| `AUDIO_IF_SLOTS_P` | 8 | 8 | same |
| `AUDIO_IF_MASTER_P` | 1 | 1 | same |
| `AUDIO_IF_RENDER_SLOTS_P` | 0 | 8 | DIFFERS: render lane pruned in the obj_ax1x1 argv; the shipping TDM8 render lane is tb/verilator/milan_dp_render |
| `AUDIO_IF_I2S_PAIR_P` | 0 | 0 | same |
| `AUDIO_IF_WORD_BITS_P` | 32 | 32 | same |
| `AUDIO_IF_FS_HZ_P` | 48000 | 48000 | same |
| `AUDIO_IF_CLK_HZ_P` | 24576000 | 24576000 | same |
| `LOOPBACK_P` | 1 | 1 | same |
| `MCSERVO_P` | 1 | 1 | same |
| `LTAP_P` | 1 | 1 | same |
| `MAAP_P` | 1 | 1 | same |
| `I2SPB_P` | 0 | 0 | same |
| `RXFILT_P` | 1 | 1 | same |
| `LPF_P` | 0 | 0 | same |
| `DPROBES_P` | 1 | 1 | same |

19 same, 3 differ (0 unexplained)
