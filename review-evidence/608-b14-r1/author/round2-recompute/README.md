# Round 2 recomputes, lane B14 (issue #608)

These are the records behind the "Round 2 recomputes" paragraph of `docs/findings/B14_BENCH_5603C353.md` and the claims it supports.
The round 2 records (marked r2) were written on 2026-10-10 between 09:21 and 09:36 UTC and are copied here byte for byte.
Round 3 (marked r3) added the comparison with `item3/cycles.tsv`, the input check and the rerun script, and re-ran everything.
No bench access was used in either round.

The packet these scripts read is `review-evidence/608-b14-r1/author/` at archive commit `c848925d2e88a98e7f31b663e5dd4f342b765487` (author tree `da8818cbd06f40ae65abdf075ebab2e46a95b56f`).
Paths below are relative to this folder.

| File | Round | What it is | Page claim it backs |
|---|---|---|---|
| `scripts/ta_lv_recheck.py` | r2 | Decodes ACMP and MSRP from the raw item 3 tap captures, timed by the tap's own counter | Item 3 withdrawal times |
| `outputs/ta_lv_all.txt` | r2 | Its output for all 101 captures, for the DUT's CRF stream `0200000000010001` | The DUT's Talker Advertise `Lv` in cycles 1, 2 and 42 only: 0.0390, 0.0951 and 0.3184 s after the bridge's `Lv` |
| `scripts/ta_lv_vs_cycles.py`, `outputs/ta_lv_vs_cycles.txt` | r3 | Compares that output with `item3/cycles.tsv`, cycle by cycle | The bridge's `Lv` after the response agrees in 101 of 101 cycles; the largest difference is 0.498 us, because the re-decode prints to the microsecond. The Talker Advertise `Lv` agrees with `dut_ta_lv_in_hold` in all 101 |
| `scripts/final_vs_asfound.py`, `outputs/final_vs_asfound.txt` | r2 | Compares the 08:23 final read with the 15 as-found rows | 15 of 15 equal at the final read |
| `scripts/inventory_rows.py`, `outputs/inventory_rows.txt` | r2 | Recounts the 06:22 and 08:23:49 inventories row by row, by category | 44 of 44 equal: 2 descriptor counts, 18 formats, 18 connection states, 2 clock sources, 4 maps |
| `scripts/slip_ledger.py`, `outputs/slip_ledger.txt` | r2 | Accounts for every `SLIP_LB` frame by phase | The 73-frame `SLIP_LB` table in item 8 |
| `inputs/snapshot-prebind.jsonl`, `inputs/snapshot-final.jsonl` | raw | The 06:22 and 08:23:49 inventory snapshots, byte for byte. They hold roles, stream formats, connection counts, clock sources and map digests, and no station address or entity identifier | Inputs of `final_vs_asfound.py` and `inventory_rows.py` |
| `inputs/raw-inputs.tsv`, `scripts/inputs_vs_index.py`, `outputs/inputs_check.txt` | r3 | Every raw input with its SHA-256, size and the archived raw-index line that lists it | The inputs are the files the archived raw index lists |
| `scripts/run_all.sh`, `outputs/rerun-r3.txt` | r3 | Re-runs everything and compares with `outputs/` byte for byte | All outputs reproduce |
| `MANIFEST.sha256` | r3 | SHA-256 of every other file in this folder | - |

## Inputs not included

The 101 item 3 tap captures are not here.
They total 89,799,919 bytes, 780,258 to 901,138 bytes each, above the packet's file size limit.
Their frames also carry station addresses and entity identifiers that the packet masks.
`inputs/raw-inputs.tsv` names each capture by SHA-256 and size and gives its line in `raw-index/item3.jsonl`.
Round 3 re-hashed all 103 raw inputs, and every digest equals the archived raw index.

Round 2 listed the same 103 digests in `raw-inputs.sha256` under the lane host's paths.
`inputs/raw-inputs.tsv` replaces it with the paths as the archived raw index publishes them.

## Rerun

```sh
scripts/run_all.sh <packet-author-dir> <out-dir>              # needs only the archived packet
scripts/run_all.sh <packet-author-dir> <out-dir> <raw-root>   # also re-decodes the captures
```

`<packet-author-dir>` is `review-evidence/608-b14-r1/author/` extracted from the archive commit above.
The script exits non-zero if any output differs from `outputs/`.
