# env.sh: the gate environment of round 4 (sourced)
S=<scratch>
LITEX=<litex venv>
V=<tools>/pinned-verilator-5.050
SDK=$S<home-path>/host/bin
export HOME=$S/home TMPDIR=$S/tmp VERILATOR=$V/verilator PYTHONHASHSEED=0
export PATH=$V:<tools>/sv2v-v0.0.12:<tools>/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TSN_GEN_ROOT=<tools>/tsn-gen-deca300c
export GIT_ALLOW_PROTOCOL=file:https
