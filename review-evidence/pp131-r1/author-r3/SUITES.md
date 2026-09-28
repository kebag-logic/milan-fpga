# Processor suite results at `cbbb5ac`

Entry point `./scripts/run_suites.sh` in a clean clone checked out at `cbbb5acc77e9e068c3313d78ed4c1e5e79299a71`, Verilator 5.050 (the pinned wrapper the manager's bank uses): rc 0, 563.0 s (run beside the parent gates and the synthesis, so slower than an idle box).

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
| `pp_top` | 7,875 | 0 | PASS |
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

Total: 1,016,016 checks, 0 failing, 33 suites. Round 2 at `2b38d68`: 1,016,000. The difference is `pp_top` +16 (7,859 to 7,875: D3O7 x2, D3R14 x5, D3R15 x4, D3R16 x3, D3R17 x2); every other suite's count is unchanged (`acmp_nvm` 353: its wrap ties the new `rs_agg_i` to 0).
