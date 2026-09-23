# Shared environment for the R258-1 probes. Source it; it sets only the
# variables below. PACKET defaults to this script's parent directory, the
# review clone to a sibling of the packet, and PIN_BIN (the directory whose
# `verilator` is the pinned 5.050) must be supplied or be the default below.
PACKET=${PACKET:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}
REVIEWS=${REVIEWS:-$(dirname "$PACKET")}
CLONE=${CLONE:-$REVIEWS/r258-1-gptp68}
PIN_BIN=${PIN_BIN:-$(dirname "$REVIEWS")/tmp/372-manager-candidate1/pinned-tool-bin}
HEAD_SHA=77c34e904eba2446755d13e1bf4763d1652c3ca7
BASE_SHA=c1b617435824929a790739ea8585c3fe1a328cc0
PARENT_SHA=574c29fa111c74e5e5ed63e4670aff1f492e28e2
PATH="$PIN_BIN:$PATH"
export PACKET REVIEWS CLONE PIN_BIN HEAD_SHA BASE_SHA PARENT_SHA PATH
