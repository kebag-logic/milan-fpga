# scratch toolchain for lane pp193 round 2: pinned Verilator 5.050 (build -j 0 -> -j 2),
# sv2v 0.0.12, Yosys 0.33 (the CI portability job's package), wavedrom 2.0.3.post3
export PATH="<scratch>/bin:<scratch>/venv-wd/bin:$PATH"
export VERILATOR=<scratch>/bin/verilator
unset LD_PRELOAD
export TMPDIR=<scratch>/r2/tmp
