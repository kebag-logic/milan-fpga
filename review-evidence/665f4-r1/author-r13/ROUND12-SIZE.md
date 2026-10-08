[A560]

# Round 12 linked size

Candidate: `efea74858dffc482820d4f19c26c38796a57ff75`.

| Shape | IF | Text | Read-only | BSS | Stack | RAM span | Round 11 delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| endstation_ax7101_1x1_tdm8 | 1 | 45828 | 2898 | 23440 | 8192 | 80368 | +464 |
| endstation_ax7101_1x1_tdm8 | 2 | 47112 | 2898 | 34808 | 8192 | 93024 | +448 |
| endstation_ax7101_8x8 | 1 | 45864 | 2898 | 38200 | 8192 | 95168 | +432 |
| endstation_ax7101_8x8 | 2 | 47240 | 2898 | 64328 | 8192 | 122672 | +432 |

Initialized data is zero in all four images. The added byte occupies existing
sink-structure padding, so BSS and the static arena do not grow.
RAM span includes alignment and the 8192-byte stack reservation.
That reservation does not prove a full call-chain bound.
The fixtures are linked for RV32I with the CI-pinned SDK, not booted images.
The existing per-pass bounds remain 3224/4073 mailbox accesses at IF=1/2.
Target CPU-cycle and physical-wire timing remain integration obligations.
Binary images, runtime libraries and maps are retained outside this packet;
size and SHA256 are recorded in ROUND12-SIZES.json.
