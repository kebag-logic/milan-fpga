# How the cause was traced

The base (`dd163e41`) at 8x8/1if, `aecp-largest-notice`, in the answering-ports and declaring-outputs arms: each
build's model run again on the group's script with the testbench's committed-PC trace
(`BUDGET_TRACE_AFTER=80900000 BUDGET_TRACE_PCS=700000`), which covers both passes over THE SHARE (the REMOVE's and the
ADD's taking passes, their PASS lines' start and cycles). `pass_funcs.py` attributes each pass's cycles to the
function holding each committed pc (the image's symbols); `call_cost.py` times each call of `aecp_stream_read` from
`aecp_map_command`, from its first commit to the next commit back in the caller. The traces are kept in scratch
(`traces.txt`: size and sha256).
