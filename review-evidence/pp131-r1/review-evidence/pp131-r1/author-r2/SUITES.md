# Processor suite results at `2b38d68`

Entry point `./scripts/run_suites.sh` in a clean clone checked out at `2b38d68e704e8a62fbeae8171c9195ca93728488`, Verilator 5.050 (the pinned wrapper the manager's bank uses): rc 0, 534.2 s.

| Suite | Checks | Failures | Result |
|---|---:|---:|---|
| `acmp_listener` | 2,544 | 0 | PASS |
| `acmp_nvm` | 353 | 0 | PASS |
| `acmp_talker` | 1,342 | 0 | PASS |
| `adp_engine` | 533 | 0 | PASS |
| `aecp_notify` | 10 | 0 | PASS |
| `ca_originator` | 16 | 0 | PASS |
| `desc_mem_guard` | 78 | 0 | PASS |
| `desc_store` | 584 | 0 | PASS |
| `dispatch` | 211 | 0 | PASS |
| `dyn_state` | 118 | 0 | PASS |
| `event_router` | 81 | 0 | PASS |
| `lsn_admit` | 18 | 0 | PASS |
| `maap` | 75 | 0 | PASS |
| `nvm_port` | 136 | 0 | PASS |
| `originator` | 104 | 0 | PASS |
| `pp_top` | 7,859 | 0 | PASS |
| `prng` | 76 | 0 | PASS |
| `release_merge` | 18 | 0 | PASS |
| `resp_buf` | 64 | 0 | PASS |
| `rx_slots` | 130 | 0 | PASS |
| `rx_validator` | 437 | 0 | PASS |
| `scoreboard` | 3,705 | 0 | PASS |
| `side_port` | 368 | 0 | PASS |
| `srp_admission` | 991,231 | 0 | PASS |
| `srp_decoder` | 190 | 0 | PASS |
| `srp_encoder` | 562 | 0 | PASS |
| `srp_stream_fsms` | 1,215 | 0 | PASS |
| `srp_top` | 1,987 | 0 | PASS |
| `timer_map` | 1,360 | 0 | PASS |
| `timer_service` | 48 | 0 | PASS |
| `tx_arbiter` | 66 | 0 | PASS |
| `tx_slots` | 95 | 0 | PASS |
| `ucpu` | 386 | 0 | PASS |

Total: 1,016,000 checks, 0 failing, 33 suites. Round 1 at `e1ae468`: 1,015,938. The difference is `pp_top` +18 (7,841 to 7,859: D3O5, D3O6, D3S10 backoff, D3R3b x2, D3R4 strobe, D3R4b, D3R5b x2, D3R8 deadline, D3R8b, D3R13 x3, plus the reshaped D3S10 checks) and `rx_validator` +44 (F28).
