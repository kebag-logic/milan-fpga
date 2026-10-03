#!/usr/bin/env python3
"""Check that each round-1 prescribed replacement/append text appears verbatim
(whitespace and comment markers normalized) in the file at the head, and that
each replaced old text is gone. Run from the repository root."""
import re, sys
def flat(path):
    t = open(path, encoding="utf-8").read()
    t = re.sub(r"^\s*(//!?|#)\s?", "", t, flags=re.M)   # drop comment markers
    return re.sub(r"\s+", " ", t)
CASES = [
 ("hdl/top/protocol_processor_top.sv",
  "group 6's records, the channel maps, are the integrator's to persist (07 §5.1, the ruling on #83): it saves a port's set from map edit phase 5, and the processor writes and restores no map record.",
  "group 6 is the saved-state contract's map stage"),
 ("hdl/aecp/KL_aecp_engine.sv",
  "Phase 5 is also the integrator's map-persistence trigger (07 §5.1); the processor writes no map record.",
  "its map stage, not implemented here yet"),
 ("hdl/aecp/KL_aecp_nvm_writer.sv",
  "Channel maps are the integrator's (07 §5.1); this writer never writes or reads them.",
  "Channel maps are a later stage."),
 ("hdl/aecp/KL_aecp_nvm_writer.sv",
  "the maps are the integrator's, restored after restore_done_o and judged against the formats this walk restored (07 §5.1), so the format/map coupling is the integrator's",
  "reset EMPTY in this stage"),
 ("tb/pp_top/README.md",
  "maps are the integrator's, 07 §5.1",
  "maps are a later stage"),
]
APPEND = ("(delivered at the top by `tb/pp_top` section D3KR, issue #83: every record type both producers write, "
          "cut by `rst_n` at 32 seeded-random points each, `--cut-seed S` reruns one; this suite's own cuts stay fixed)")
rc = 0
for path, new, old in CASES:
    f = flat(path)
    ok_new = new in f; ok_old = old not in f
    print(f"{'OK ' if ok_new and ok_old else 'BAD'} {path}: new text present={ok_new}, old text gone={ok_old}")
    rc |= not (ok_new and ok_old)
n = flat("tb/nvm_port/README.md").count(APPEND)
print(f"{'OK ' if n == 2 else 'BAD'} tb/nvm_port/README.md: prescribed append present {n} times (expected 2)")
rc |= n != 2
sys.exit(rc)
