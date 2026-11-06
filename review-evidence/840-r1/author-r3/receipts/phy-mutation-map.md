Existing assertion mapping at beb38447d07cceac5170ba0a35c7615f5714b7f7.

The driver checks the expected failure text before printing `caught`.
Source: `sw/firmware/nvm_hosttest/test_phy_firmware.py`; results: `gates/phy_firmware.log`.

| Planted mutant | Required failing words | Result |
|---|---|---|
| `phy_behind_the_writer` | `PHY boot path persistence disabled: the link-status CSR holds 0` | caught |
| `disabled_path_no_idle_hook` | `PHY boot path persistence disabled: 0 publication(s) in 1000 ms of console idle` | caught |
| `phy_never_armed` | `PHY boot path persistence disabled: the link-status CSR holds 0` | caught |
| `phy_off_the_writer_path` | `PHY boot path shipping: the link-status CSR holds 0` | caught |
| `phy_unguarded` | `PHY boot path identity mismatch: ` | caught |
| `advertise-100base-tx` | `no_100base_tx_advertised` | caught |
| `advertise-10base-t` | `no_10base_t_advertised` | caught |
| `advertise-100base-t4` | `no_100base_t4_advertised` | caught |
| `advertise-1000base-t-half` | `no_gigabit_half_duplex_advertised` | caught |
| `no-1000base-t-full` | `gigabit_full_duplex_advertised` | caught |
| `no-restart` | `auto_negotiation_restarted` | caught |
| `restart-first` | `restart_after_advertisement` | caught |
| `write-unread` | `no_write_before_its_read` | caught |
| `write-unread-ability` | `no_write_before_its_ability_read` | caught |
| `advertise-every-poll` | `advertised_once` | caught |
| `advertise-without-extended-status` | `no_write_without_extended_status` | caught |
| `advertise-without-1000base-t-full` | `no_write_without_1000base_t_full_ability` | caught |
| `gate-on-1000base-t-half` | `no_write_without_1000base_t_full_ability` | caught |
| `ability-reread-every-poll` | `ability_read_once` | caught |
| `no-register-4-write` | `no_10base_t_advertised` | caught |
| `clear-pause-bits` | `pause_bits_kept` | caught |
| `keep-reserved-bit-14` | `reserved_bit_14_cleared` | caught |
| `drop-master-slave` | `master_slave_kept` | caught |
| `keep-test-mode` | `test_mode_cleared` | caught |
| `restart-keeps-reset` | `reset_cleared` | caught |
| `restart-keeps-isolate` | `isolate_cleared` | caught |
| `no-auto-negotiation-enable` | `auto_negotiation_enabled` | caught |

The separate reviewer probes print actual assertion failures in `gates/r775_phy_mutants.log` and `gates/r776_phy_mutants.log`.
