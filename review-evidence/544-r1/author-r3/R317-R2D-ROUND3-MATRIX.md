# R317-R2D-ROUND3-MATRIX

Head: `8383e929fab3ff57a768c88b8b1ff9b568afcf14`.

ASM: unit allowlist; SAMPLE: prior absence rule; MACRO: replacement rule.
OTHER: full refusal retained in the corresponding JSON receipt.

| Case | r317-cases_544_r2d-sdk | r317-cases_544_r2d-sdk-disconnected | r317-cases_544_r2d-absent | r317-cases_544_r2d-absent-disconnected |
|---|---|---|---|---|
| CTRL unchanged firmware | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| PLAIN extension address | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| PLAIN asm immediate output | REFUSED:SAMPLE | REFUSED:ASM | ACCEPTED | ACCEPTED |
| PLAIN choose lvalue | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| PLAIN generic lvalue | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| PLAIN real lvalue | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| PLAIN extension lvalue | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| PLAIN asm tied output | REFUSED:SAMPLE | REFUSED:ASM | ACCEPTED | ACCEPTED |
