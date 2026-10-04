# #232 area lane: the author's lockstep bench, published (round 2; R453-1 F2)

The bench that backed "every output of `KL_aecp_notify` is cycle-identical to `main`'s"
in rounds 1 and 1b, with its control diffs and every run's summary line. Since round 2
the guarantee no longer rests on it: `tb/aecp_notify` sections IX and TS grade the three
dependencies, and `notify_mutants.py` plants the reviewers' faults as killed controls.
Paths are shown as `$SCRATCH` (the lane's scratch directory) and `$PINNED_VERILATOR`.

## Bench (`bench/`)

- `gen_wrap.py` writes `lockstep_top`: `main`'s `KL_aecp_notify.sv`, renamed
  `KL_aecp_notify_ref` (`ref/`), and the candidate file, side by side with the same
  inputs every cycle. Every output in `outputs.txt` and each instance's internal
  `rx_cmd_hit_w` are compared before and after every clock edge.
- `tb_lockstep.cpp` drives it: seeds 1 to 4 protocol-shaped (registry handshakes, a
  timer model echoing the arms, probe and PRNG handshakes, resets mid-run), seeds 5 to 8
  every input at random. Arguments: seed, cycles, `N_CTRL`, random mode.
- `build.sh` builds one candidate at one shape; `runall.sh` the five shapes of R1b.3;
  `controls.sh` the seven round-1b controls; `runrev.sh` the two reviewer edits below.
- `sources.sha256`: the reference (`main` `5c71928a`, byte-equal to `f4167536` and
  `83999eba`; sha256 `e7e127cf...f3f2`), its renamed copy, and the two candidates
  (`6e950fea`, `3ab2e4da`).

## Runs (`runs/`; one summary line per run, and the rc files)

| Shape `N_CTRL/N_IN/N_OUT` | Runs x cycles | Mismatches |
|---|---|---:|
| 16/2/2, 16/9/9, 2/1/1, 16/2/2 with identify, 5/8/8 | 5 x 8 x 1,000,000 | 0 in each of the 40 runs (`r1b-runs.txt`) |

## Controls, corrected (16/2/2, 8 runs of 1,000,000 cycles each)

R453-1 found one round-1b row whose label does not match its edit. The edit planted as
"comparator only in the set cycle" was `assign ix_busy_w = ix_set_r;`. `ix_busy_w` gates
the index write as well as the compare, so the edit drops the clear too: it is a
superset of `no_clear`, which is why its count sits next to `no_clear`'s. The table
below gives each round-1b control its edit (`controls-r1b/*.diff`), and adds the
reviewers' own two edits (`controls-r2/*.diff`, written by R452-1's `plant.py`
unchanged), run on the same bench in round 2.

| Control | Edit | Mismatches | Runs caught |
|---|---|---:|---:|
| `no_override` | the match mux reads the index in both rewrite cycles | 118,069 | 8 of 8 |
| `no_clear` | the index write enable is `ix_set_r`: the old identity is never cleared | 14,840,381 | 8 of 8 |
| `no_set` | `ix_set_r <= 1'b0`: the new identity is never set | 10,944,924 | 8 of 8 |
| **`override_set_only` (round 1b's file), corrected label: "the rewrite window cut to the set cycle: no clear, and the compare only in the set cycle"** | `ix_busy_w = ix_set_r` | 14,848,035 | 8 of 8 |
| `last_chunk_ignored` | `ix_hit_w[i] = &ch_w[N_IXC_C-2:0]` | 545,407 | 4 of 8 |
| `refresh_not_reindexed_claim_too`: REGISTER not re-indexed | `ix_clr_r <= 1'b1` removed from `N_APPLY` | 10,945,711 | 8 of 8 |
| `stamp_unread_valid`: a stamp read without its valid bit | `(!ctr_sent_r[c]` -> `(1'b0` | 161,278 | 7 of 8 |
| `override_set_only`, the reviewers' edit (round 2) | the match mux's `(ix_busy_w &&` -> `(ix_set_r &&`; the index write untouched | 8 | 4 of 8 (seeds 5 to 8, random inputs; 0 in the protocol-shaped seeds) |
| `own_compare_new_row`, the reviewers' edit (round 2) | `ix_own_w` compares `wr_row_r`, not `ix_wr_row_w` | 4,611 | 8 of 8 |

So this bench reaches the true `override_set_only` only through its random-input
seeds, as R453-1 predicted: its protocol-shaped stimulus aims no reset at the rewrite
window. Round 2's committed check IX6 drives exactly that case and kills the edit (2
failing checks); IX5 kills `own_compare_new_row`, and TS3 the stamp edit.
