tools/area/area.sh (yosys synth_xilinx -family xc7 -flatten from the sv2v v0.0.12 lowering syn/yosys/run.sh uses):
- area-60094a2-out: the round 1 head, re-measured this round; equal to round 1's figures.
- area-ceb6a98-out: the round 2 HDL; hdl/ and syn/ of ceb6a98 equal the head 84f6d6a's (area-hdl-identity.txt), the
  last commit changing only docs and a README.
- area-84f6d6a-out: the head itself, on its clean clone; identical to area-ceb6a98-out, figure for figure.
- base-044cb25f-round1/SUMMARY.md: main's figures as round 1 measured them (unchanged code).
Each run's SUMMARY.md has the table; the .stat files are yosys's own stat output per shape.
