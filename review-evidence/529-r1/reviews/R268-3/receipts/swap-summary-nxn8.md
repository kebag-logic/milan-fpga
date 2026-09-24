| port A | port B | quadlet A | | quadlet B | | tally | verdict |
|---|---|---|---|---|---|---|---|
| cnt_intr_o | seq_err_o | @8 red | @12 red | 3136/2 | KILLED both |
| cnt_locked_o | cnt_unlocked_o | @0 red | @4 red | 3136/4 | KILLED both |
| cnt_unlocked_o | cnt_intr_o | @4 red | @8 red | 3136/5 | KILLED both |
| early_cnt_o | pdu_count_o | @40 red | @44 red | 3136/2 | KILLED both |
| fmt_err_o | late_cnt_o | @32 red | @36 red | 3136/2 | KILLED both |
| late_cnt_o | early_cnt_o | @36 red | @40 red | 3136/2 | KILLED both |
| mr_cnt_o | tu_cnt_o | @16 red | @20 red | 3136/2 | KILLED both |
| seq_err_o | mr_cnt_o | @12 red | @16 red | 3136/3 | KILLED both |
| tu_cnt_o | fmt_err_o | @20 red | @32 red | 3136/2 | KILLED both |

9 of 9 exchanges red on both exchanged quadlets (nxn8)
