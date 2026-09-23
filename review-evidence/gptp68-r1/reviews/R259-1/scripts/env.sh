# Source me. Pins the reviewer's tool environment. Required from the caller:
#   REVIEW_CLONE  exact-head donor clone (FPGA-gPTP 77c34e90)
#   PINNED_BIN    directory holding the Verilator 5.050 wrapper
# PKT defaults to this packet (the directory above scripts/).
PKT=${PKT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}
: "${REVIEW_CLONE:?set REVIEW_CLONE to the exact-head donor clone}"
: "${PINNED_BIN:?set PINNED_BIN to the Verilator 5.050 wrapper directory}"
export PATH="$PINNED_BIN:/usr/local/bin:/usr/bin:/bin"
export VERILATOR_ROOT="$(verilator --getenv VERILATOR_ROOT)"
HEAD_SHA=77c34e904eba2446755d13e1bf4763d1652c3ca7
BASE_SHA=c1b617435824929a790739ea8585c3fe1a328cc0
PARENT_DEV=574c29fa111c74e5e5ed63e4670aff1f492e28e2
