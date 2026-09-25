# R317-R2C-ROUND3-MATRIX

Head: `8383e929fab3ff57a768c88b8b1ff9b568afcf14`.

ASM: unit allowlist; SAMPLE: prior absence rule; MACRO: replacement rule.
OTHER: full refusal retained in the corresponding JSON receipt.

| Case | r317-cases_544_r2c-sdk | r317-cases_544_r2c-sdk-disconnected | r317-cases_544_r2c-absent | r317-cases_544_r2c-absent-disconnected |
|---|---|---|---|---|
| CTRL unchanged firmware | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| PRIOR C08 macro (*(__extension__ &(x)) = MAGIC) | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| PRIOR C09 plain (*(__extension__ &(id)) = MAGIC) | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| PRIOR C10 macro asm li %0 output | REFUSED:SAMPLE | REFUSED:ASM | REFUSED:MACRO | ACCEPTED |
| PRIOR C11 plain asm li %0 output | REFUSED:SAMPLE | REFUSED:ASM | ACCEPTED | ACCEPTED |
