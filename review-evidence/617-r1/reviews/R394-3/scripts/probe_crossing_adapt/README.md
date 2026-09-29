# Sub-cycle crossing probe, as re-run by R394-3

`make_probe.py`, `make_probe_fine.py` and `run_fine.sh` are byte copies of the other reviewer's round-2
probe scripts (R395-2 packet, `scripts/probe_crossing/`). They are used here unchanged, as tools.
`../run_fine_cols.sh` is `run_fine.sh` with the column count as an argument.

Build at a head (from `tb/verilator` of a tree of that head, Verilator 5.050 first on PATH):

```sh
mkdir cc_r395fine
cp capture_coherence/{Makefile,coherence_bench.hpp,coherence_wrap.sv,sim_main.cpp,mga_keepoff.py} cc_r395fine/
cd cc_r395fine
python3 make_probe.py sim_main.cpp probe_main.cpp
python3 make_probe_fine.py .
cp probe_fine.cpp sim_main.cpp
make -s build MDIR=obj_fine
bash run_fine.sh -50 -1 2 fine-m50.log      # likewise -60 -1 2 and +50 -1 3
bash ../run_fine_cols.sh -62 -1 2 1000 fine-m62-1000.log
```

The committed suite's own build recipe is used (`make build`), so the wrapper binds the datapath's
keep-off declaration through `mga_keepoff.py` exactly as the suite does.
