# Shared settings for the R282-2 probes. Override VERILATOR / PKT / CLONE to relocate.
: "${PKT:=$REVIEWS/539-r282-2-packet}"
: "${VERILATOR:=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator}"
: "${CLONE:=$REVIEWS/r282-2-539}"
HEAD_SHA=910b4fb5f104ac35e8cc1723a70de0d05672895d
BASE_SHA=26d855a9176d63625e6635a029a0c44e3d57ce9a
# at most 8 parallel jobs
VFLAGS_R='--cc --exe --build -j 8 -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE -Wno-PINCONNECTEMPTY -CFLAGS "-std=c++17 -O2 -Wall -Wextra"'
export PKT VERILATOR CLONE HEAD_SHA BASE_SHA VFLAGS_R
