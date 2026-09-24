#!/usr/bin/env python3
"""Write disposable mutated copies of milan_datapath.sv for composition probes.

Each probe applies one exact, single-occurrence text substitution to the
candidate's milan_datapath.sv and writes the copy under <out>/<name>.sv with
a .diff beside it. The tracked file is never touched: the suite is pointed at
the copy with DP_SRC.

  P1 swap-mr-tu      exchange the MEDIA_RESET and TIMESTAMP_UNCERTAIN tally
                     bindings at the KL_crf_rx instance (a permuted port map)
  P2 dirty-open      leave KL_crf_rx's Table 5.22 dirty pulse unconnected
                     (the pre-#529 state of that one port)
  P3 pend-stuck      the arbiter's STREAM_INPUT pending-clear loop stops
                     below the CRF row, so that row never leaves pending
                     (a CRF row that keeps pushing every second)

Usage: make_probes.py <candidate milan_datapath.sv> <out-dir>
"""
import difflib
import sys
from pathlib import Path

PROBES = {
    "P1-swap-mr-tu": [
        ("    .mr_cnt_o    (crf_mrcnt_w),\n    .tu_cnt_o    (crf_tucnt_w),\n",
         "    .mr_cnt_o    (crf_tucnt_w),\n    .tu_cnt_o    (crf_mrcnt_w),\n"),
    ],
    "P3-pend-stuck": [
        ("    for (int unsigned s = 0; s < PP_CTR_SIN_N_C; s++) begin\n",
         "    for (int unsigned s = 0; s < PP_CTR_SIN_N_C - 1; s++) begin\n"),
    ],
    "P2-dirty-open": [
        # the now-undriven wire would trip -Werror-UNDRIVEN, so main() ties
        # it to zero right after the instance
        ("    .dirty_p_o      (crf_dirty_p_w)\n", "    .dirty_p_o      ()\n"),
    ],
}


def main() -> int:
    src = Path(sys.argv[1]).read_text()
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for name, subs in PROBES.items():
        text = src
        for old, new in subs:
            if new is None:
                continue
            n = text.count(old)
            if n != 1:
                print("%s: pattern occurs %d times, refusing" % (name, n))
                return 2
            text = text.replace(old, new)
        if name == "P2-dirty-open":
            anchor = "    .dirty_p_o      ()\n  );\n"
            if text.count(anchor) != 1:
                print("%s: anchor occurs %d times, refusing" % (name, text.count(anchor)))
                return 2
            text = text.replace(anchor, anchor + "  assign crf_dirty_p_w = 1'b0;  // probe P2\n")
        (out / (name + ".sv")).write_text(text)
        d = difflib.unified_diff(src.splitlines(True), text.splitlines(True),
                                 "a/hdl/milan/milan_datapath.sv", "b/" + name + ".sv")
        (out / (name + ".diff")).write_text("".join(d))
        print("%s written" % name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
