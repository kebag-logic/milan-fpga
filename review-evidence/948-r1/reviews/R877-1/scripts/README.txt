Round R877-1 probe and job scripts (reviewer-owned, disposable).
- run_job.sh NAME CMD...   run CMD from the reviewed clone, log to receipts/NAME.log and rc to receipts/NAME.rc
- status.sh [N]            summarize every job's rc and last verdict lines
- gates.sh                 the focused read-only docs/quality gates (run from the clone root)
- probeA_make.py SRC OUT   instrumented depacketizer copy (occupancy monitors); built with
                           make -C tb/verilator/avtp_rxmon fanout-build DEPKT_SRC=OUT FO_MDIR=<dir>
- probeB_make.py SRC OUT   milan_datapath.sv with the shared 5.3.8.7 stop gate planted; built with the
                           build-nxn8 recipe (make -n build-nxn8 DP_SRC=OUT, --Mdir moved to a scratch dir)
