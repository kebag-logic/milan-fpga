# R317-R2B-ROUND3-MATRIX

Head: `8383e929fab3ff57a768c88b8b1ff9b568afcf14`.

ASM: unit allowlist; SAMPLE: prior absence rule; MACRO: replacement rule.
OTHER: full refusal retained in the corresponding JSON receipt.

| Case | r317-cases_544_r2b-sdk | r317-cases_544_r2b-sdk-disconnected | r317-cases_544_r2b-absent | r317-cases_544_r2b-absent-disconnected |
|---|---|---|---|---|
| CTRL unchanged firmware | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| STORE auto sample | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER |
| STORE register sample | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER |
| STORE const sample | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER |
| STORE volatile sample | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER |
| STORE static sample | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER |
| ESC nested function in another function, no sample | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| ESC nested function in milan_init before the read | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| ESC nested function after guard naming the sample | REFUSED:SAMPLE | REFUSED:OTHER | ACCEPTED | ACCEPTED |
