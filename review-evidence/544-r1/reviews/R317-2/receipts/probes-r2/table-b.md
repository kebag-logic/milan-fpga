| case | r2b-head-sdk | r2b-head-sdk-disconnect | r2b-base-sdk | r2b-head-absent |
|---|---|---|---|---|
| CTRL unchanged firmware | ACC | ACC | ACC | ACC |
| STORE auto sample | REF:other | REF:other | REF:other | REF:other |
| STORE register sample | REF:other | REF:other | REF:other | REF:other |
| STORE const sample | REF:other | REF:other | REF:other | REF:other |
| STORE volatile sample | REF:other | REF:other | REF:other | REF:other |
| STORE static sample | REF:other | REF:other | REF:other | REF:other |
| ESC nested function in another function, no sample | REF:SAMPLE | ACC | ACC | ACC |
| ESC nested function in milan_init before the read | REF:SAMPLE | ACC | ACC | ACC |
| ESC nested function after guard naming the sample | REF:SAMPLE | REF:other | REF:other | ACC |
