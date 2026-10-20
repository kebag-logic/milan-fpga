# Base route provenance (round 1b)

These files are copied from the PR #767 lane's ([A652]) round-2b candidate
route of commit `eef90b4238b6c19b679b44adc6f09362809be153`, that lane's
published head. Round 1b of this lane merges that commit into
`765-unsupported-format`, so it is this lane's base. Host paths are replaced
by placeholders; nothing else is changed. It was not re-run here.

Same recipe (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, shipping AX7101 1x1,
`pp_baseline.py --single-thread-synthesis`; this lane's export script is
identical to that lane's apart from its paths), Vivado v2026.1 SW Build 6511674
on the same host, same submodule pins (`submodules.txt` identical). The two
exports have identical memory init files, `.xdc` and build script; the
`.tcl` files differ only in their paths, and `alinx_ax7101.v` only in its
paths, LiteX's generation timestamp and the order of LiteX's comment tree.

`alinx_ax7101_timing.rpt` (not copied, over 200 KB): SHA-256
`92526027b73badf98c426acc14cf93f7b14820dd2084d180835f3519fbbaf70f`,
1,316,045 bytes.
