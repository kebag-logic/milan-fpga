# PHY mutants at the head and the assertion each must fail

Round-4 additions are marked. The planted edits are in `sw/firmware/nvm_hosttest/test_phy_firmware.py`.

| Mutant | Failing words | Added in round 4 |
|---|---|---|
| `advertise-100base-tx` | `no_100base_tx_advertised` |  |
| `advertise-10base-t` | `no_10base_t_advertised` |  |
| `advertise-100base-t4` | `no_100base_t4_advertised` |  |
| `advertise-1000base-t-half` | `no_gigabit_half_duplex_advertised` |  |
| `no-1000base-t-full` | `gigabit_full_duplex_advertised` |  |
| `no-restart` | `auto_negotiation_restarted` |  |
| `restart-first` | `restart_after_advertisement` |  |
| `write-unread` | `no_write_before_its_read` |  |
| `nak-reg4-not-checked` | `no_write_before_its_register_4_read` | yes |
| `nak-reg0-not-checked` | `no_write_before_its_register_0_read` | yes |
| `write-unread-ability` | `no_write_before_its_ability_read` |  |
| `advertise-every-poll` | `advertised_once` |  |
| `advertise-without-extended-status` | `no_write_without_extended_status` |  |
| `advertise-without-1000base-t-full` | `no_write_without_1000base_t_full_ability` |  |
| `gate-on-1000base-t-half` | `no_write_without_1000base_t_full_ability` |  |
| `ability-reread-every-poll` | `ability_read_once` |  |
| `no-register-4-write` | `no_10base_t_advertised` |  |
| `clear-pause-bits` | `pause_bits_kept` |  |
| `keep-reserved-bit-14` | `reserved_bit_14_cleared` |  |
| `drop-master-slave` | `master_slave_kept` |  |
| `keep-test-mode` | `test_mode_cleared` |  |
| `restart-keeps-reset` | `reset_cleared` |  |
| `restart-keeps-isolate` | `isolate_cleared` |  |
| `no-auto-negotiation-enable` | `auto_negotiation_enabled` |  |
| `force-pause-on` | `pause_bits_kept` | yes |
| `force-manual-master` | `master_slave_kept` | yes |
| `force-manual-config-only` | `master_slave_kept` | yes |
| `force-bit-4.0` | `selector_kept` | yes |
| `drop-bit-4.0` | `selector_kept` | yes |
| `force-bit-4.1` | `selector_kept` | yes |
| `drop-bit-4.1` | `selector_kept` | yes |
| `force-bit-4.2` | `selector_kept` | yes |
| `drop-bit-4.2` | `selector_kept` | yes |
| `force-bit-4.3` | `selector_kept` | yes |
| `drop-bit-4.3` | `selector_kept` | yes |
| `force-bit-4.4` | `selector_kept` | yes |
| `drop-bit-4.4` | `selector_kept` | yes |
| `force-bit-4.10` | `pause_bits_kept` | yes |
| `drop-bit-4.10` | `pause_bits_kept` | yes |
| `force-bit-4.11` | `pause_bits_kept` | yes |
| `drop-bit-4.11` | `pause_bits_kept` | yes |
| `force-bit-9.10` | `master_slave_kept` | yes |
| `drop-bit-9.10` | `master_slave_kept` | yes |
| `force-bit-9.11` | `master_slave_kept` | yes |
| `drop-bit-9.11` | `master_slave_kept` | yes |
| `force-bit-9.12` | `master_slave_kept` | yes |
| `drop-bit-9.12` | `master_slave_kept` | yes |
| `no-publish` | `publishes > before` | |
| `defer-recovery` | `status_word == expected` | |
| `late-sample` | `no_10base_t_advertised` | |
| `ack-ignored` | `status_word == expected` | |

47 advertisement mutants, 4 poll mutants and 5 boot-path mutants.
