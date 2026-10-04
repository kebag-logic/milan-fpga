| Reviewer | Control | probe rc, s | `tb/aecp_notify` | `tb/pp_top` |
|---|---|---|---|---|
| R452-1 | `clear_new_identity` | 0, 899 | FAIL (1: IX1) | PASS 10416/10416 |
| R452-1 | `last_chunk_ignored` | 0, 858 | FAIL (1: IX2) | PASS 10416/10416 |
| R452-1 | `no_clear` | 0, 907 | FAIL (1: IX1) | PASS 10416/10416 |
| R452-1 | `no_override` | 0, 881 | FAIL (3: IX4, IX6, IX6b) | PASS 10416/10416 |
| R452-1 | `no_set` | 0, 860 | FAIL (3: IX3, IX4, IX6b) | FAIL (384: U10a4, U10a5, U10a5.1, U10a5.10, U10a5.2, U10a5.11, ...) |
| R452-1 | `override_clr_only` | 0, 850 | FAIL (1: IX4) | PASS 10416/10416 |
| R452-1 | `override_set_only` | 0, 746 | FAIL (2: IX6, IX6b) | PASS 10416/10416 |
| R452-1 | `own_compare_new_row` | 0, 731 | FAIL (1: IX5) | PASS 10416/10416 |
| R452-1 | `register_not_reindexed` | 0, 751 | FAIL (5: IX3, IX4, IX5, IX6, IX6b) | FAIL (384: U10a4, U10a5, U10a5.1, U10a5.10, U10a5.2, U10a5.11, ...) |
| R452-1 | `stamp_without_valid` | 0, 672 | FAIL (1: TS3) | PASS 10416/10416 |
| R453-1 | `first_chunk_ignored` | 0, 662 | FAIL (1: IX2) | PASS 10416/10416 |
| R453-1 | `index_wrong_row` | 0, 668 | FAIL (2: IX3, IX6b) | FAIL (384: U10a4, U10a5, U10a5.1, U10a5.10, U10a5.2, U10a5.11, ...) |
| R453-1 | `key_swapped` | 0, 616 | FAIL (2: IX3, IX6b) | FAIL (384: U10a4, U10a5, U10a5.1, U10a5.10, U10a5.2, U10a5.11, ...) |
| R453-1 | `last_chunk_ignored` | 0, 611 | FAIL (1: IX2) | PASS 10416/10416 |
| R453-1 | `no_clear` | 0, 642 | FAIL (1: IX1) | PASS 10416/10416 |
| R453-1 | `no_override` | 0, 642 | FAIL (3: IX4, IX6, IX6b) | PASS 10416/10416 |
| R453-1 | `no_set` | 0, 650 | FAIL (3: IX3, IX4, IX6b) | FAIL (384: U10a4, U10a5, U10a5.1, U10a5.10, U10a5.2, U10a5.11, ...) |
| R453-1 | `override_clr_only` | 0, 626 | FAIL (1: IX4) | PASS 10416/10416 |
| R453-1 | `override_set_only` | 0, 622 | FAIL (2: IX6, IX6b) | PASS 10416/10416 |
| R453-1 | `own_vs_new_row` | 0, 607 | FAIL (1: IX5) | PASS 10416/10416 |
| R453-1 | `reindex_late` | 0, 619 | FAIL (1: IX4) | PASS 10416/10416 |
| R453-1 | `stamp_read_without_valid` | 0, 612 | FAIL (1: TS3) | PASS 10416/10416 |

22 of 22 controls fail a committed check
