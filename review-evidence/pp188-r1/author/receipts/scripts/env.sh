# scratch toolchain for lane pp188: pinned Verilator 5.050, sv2v 0.0.12,
# Yosys 0.33 (CI's Ubuntu package version), wavedrom 2.0.3.post3 venv
export PATH="<scratch>/bin:<scratch>/venv-wd/bin:$PATH"
export VERILATOR=<scratch>/bin/verilator
unset LD_PRELOAD
