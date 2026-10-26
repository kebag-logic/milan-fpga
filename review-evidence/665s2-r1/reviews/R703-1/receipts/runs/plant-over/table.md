### 1x1

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| LINK_UP | `adp.link_up.if0` | 5,281 | 0.106 | 10 | 200 | fits | 248,452 | 88 (11) | 0.886 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 43,255 | 0.865 | 10 | 200 | fits | 101,078 | 46 (39) | 0.870 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 520,125 | 10.402 | 10 | 200 | MISS T_svc | 586,419 | 37 (31) | 0.809 |
