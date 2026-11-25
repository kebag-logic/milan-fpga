# Round 7 receipts (#1003, head `9c62539365fea8316dae2b9fd7c68defeff5cb31`, unchanged)

About 65 KB of text in total; no file is over 7 KB.

The local runs were on the 96-vCPU VM, in the session pool 64-95, because `cpu_ranges.py pick` returned no
range. Builds went through the shared compiler cache. Round-6 hosted artifacts were reused from
`/data-2/milan/tmp/cicd-a839/r6/hosted/cmp/{old,new}`: run 45481508309 and run 45528738040.

## hosted/

- `merge-commits-from-worker-logs.txt`: each run's checkout step, naming the merge it tested.
  - 45481508309: `dd5cf579` = `45d5c35a` into `2509db68`.
  - 45528738040: `241f036e` = `9c625393` into `e608f8d8`.
- `merge-trees-diff.txt`: the two merge trees differ in 43 files. 18 are the PR's own (`45d5c35a..9c625393`); the
  other 25 are each #995's (`e608f8d8`, committed 01:33Z).
- `milan_dp-runA-vs-runB.txt`: both runs' 26 `milan_dp` case receipts, (outcome, rc, `output_sha256`), with each
  receipt's head, tree and shard. Only `gptp` and `gptp-lat` differ.
- `gptp_shadow-verdicts-runA-vs-runB.txt`: `gptp_shadow`'s verdict lines in both runs. 326 → 424 checks and four
  new #106/#107 mutants, from #995.

## local/

- `trees.txt`: every local tree's commit, tree id, parents and gPTP pin, and the tree ids of the two hosted
  merges. It also holds the base's file list from `2509db68` to `e608f8d8` and the gPTP processor's HDL changes
  from `1616fc8f` to `1213ac5b`.
- `build-sha256.txt`: per tree (B0, H0, O0, B1, H1, O1), the sha256 of `ucode.hex`, `ltn_rom.hex`,
  `gptp_ucode.hex`, `gptp_lat_ucode.hex`, both binaries and both Verilator outputs. Within each base they are
  identical.
- `direct-runs.txt`: the 28 direct runs, one row each: tree, base, head, pin, round (q/m/l), case, CPUs, wall,
  rc, the output's sha256 in the receipt's form, the `[#207]` pointers and the tally.
- `gptp{,-lat}.{old,new}-pin.out`: one whole output of each case on each pin. These are B0's and B1's round-M
  runs; stderr was empty.
- `pieces/`: the twelve piece receipts (P4O0, P8H0 on `2509db68`; P4B1, P8B1, P4H1, P8H1 on `e608f8d8`; legs 0
  and 1 under 4 and 8 legs), and `times.txt` with their walls.
- `receipts-old-pin.txt`, `receipts-new-pin.txt`: hosted receipts beside the local pieces, case by case. There are
  0 differences in either.
- `progress.txt`: every unit's completion line, in order.

## tools/

These are the scripts behind the results above:

- `mktree.sh`: a clone with the head merged into the base, as `refs/pull/N/merge`;
- `build.sh`;
- `execs.sh` (round Q) and `execs2.sh` (rounds M and L, stdout and stderr kept apart);
- `piece.sh`: the CI driver per shard;
- `rcpt.py`: the receipt tables;
- `runs_table.sh`;
- `env.sh`.
