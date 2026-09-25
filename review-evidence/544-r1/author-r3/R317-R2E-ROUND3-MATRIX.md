# R317-R2E-ROUND3-MATRIX

Head: `8383e929fab3ff57a768c88b8b1ff9b568afcf14`.

ASM: unit allowlist; SAMPLE: prior absence rule; MACRO: replacement rule.
OTHER: full refusal retained in the corresponding JSON receipt.

| Case | r317-cases_544_r2e-sdk | r317-cases_544_r2e-sdk-disconnected | r317-cases_544_r2e-absent | r317-cases_544_r2e-absent-disconnected |
|---|---|---|---|---|
| CTRL unchanged firmware | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| LIM cast sample as a compound-literal element inside a call | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| LIM cast sample as the last compound-literal element inside a call | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| LIM cast sample as a compound-literal element, literal unparenthesized | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
