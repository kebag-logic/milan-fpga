# R634-2 reproduction

Inputs: the published author packet `review-evidence/117-b19-r1/author-r2` at evidence commit
`633b6e33244545b0dd5a1ef9a01fb96a0209d35e` (EVID below), and the read-only cold-archive raw copy
(RAW below). Every script takes paths as arguments and writes nothing outside the current directory.

```sh
python3 -I scripts/verify_publication.py EVID/..            # receipts/publication-check.txt
python3 -I scripts/verify_raws.py EVID/RAW-ARTIFACTS.json RAW # receipts/raw-rehash.txt
# author's round-2 tools, copied out of the packet, run over RAW (receipts/rerun/)
python3 -I tools/r2_box3_model.py RAW PKT; python3 -I tools/r2_box3_grade.py PKT
python3 -I tools/r2_box3_grade.py PKT --selftest; python3 -I tools/r2_gm.py RAW PKT
python3 -I tools/r2_gm.py RAW PKT --selftest; python3 -I tools/r2_box4.py RAW PKT
# independent re-derivations (own parsers)
python3 -I scripts/probe_gm.py RAW            # receipts/probe_gm.txt
python3 -I scripts/probe_box4.py RAW          # receipts/probe_box4.txt
python3 -I scripts/probe_box3.py RAW          # receipts/probe_box3.txt
python3 -I scripts/probe_c1_margin.py RAW cycle01
python3 -I scripts/probe_phc_steps.py RAW     # receipts/probe_phc_steps.txt
python3 -I scripts/probe_host_identity.py RAW CHECKOUT
python3 -I scripts/probe_identity_text.py RAW FILE...
```

`receipts/correlation-regen.txt`: the round-1 `corr_analyze.py`, with only its hard-coded raw
root replaced by RAW, regenerates all six `bench/cycleNN/correlation.json` byte for byte.
Mutation receipts: `gm-mut.out` (a gm03 DUT poll set to as_capable 0, rc 1), `grade-mut.out`
(cycle 3 last Sync +8 ms, rc 1), `grade-mut3.out` (d_lo less 8 byte times, rc 1).
