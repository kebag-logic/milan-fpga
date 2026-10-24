# How the R691-1 receipts were produced

Every command ran in a disposable copy, never in the reviewed clone. `<PKT>` is
this packet's root and `<TOOLS>` the host's tool root. `VERILATOR` is the pinned
5.050 wrapper (`receipts/verilator-identity.txt`). Each job was started detached
with `scripts/bg.sh NAME DIR CMD...`, which writes `receipts/NAME.{log,rc,start,end}`.
Then `scripts/wait.sh` polled for the jobs in the foreground.

Trees:

- `headgit`: a local clone of the reviewed clone, detached at 33d3010c.
- `base`, `head`: `git archive` of 93fb0b2d and 33d3010c.
- Each test job ran in its own copy of `headgit`.

| Receipt | Directory | Command |
|---|---|---|
| `rom-ident` | scratch | `python3 -B {head,base}/hdl/aecp/ucode/gen_ucode.py -o {head,base}-ucode.hex`; `sha256sum`; `cmp` |
| `make-check` | headgit | `make check` |
| `aecp-cmds-run` | copy/tb/aecp_cmds | `make run VERILATOR=$VERILATOR` |
| `aecp-cmds-record` | same copy | `make record`, then `git diff --exit-code -- tb/aecp_cmds/decode.json` |
| `aecp-cmds-mutants` | copy/tb/aecp_cmds | `python3 -B mutants.py --output OUT --verilator $VERILATOR --jobs 4` (results: `aecp-cmds-mutants.results.json`) |
| `pptop-aecp-dispatch` | copy/tb/pp_top | `make aecp-dispatch VERILATOR=$VERILATOR` |
| `pptop-run` | copy/tb/pp_top | `make run VERILATOR=$VERILATOR` |
| `aecp-dispatch-gavb-arms` | copy/tb/pp_top | `python3 -B aecp_dispatch_mutants.py --output OUT --only <the ten GET_AVB_INFO arms> --verilator $VERILATOR --jobs 4` (results: `aecp-dispatch-gavb-arms.results.json`) |
| `probe-order`, `probe-noecho` | copy | `python3 -I scripts/probe_edits.py {order,noecho} COPY`, then `make -C tb/aecp_cmds run` and `make -C tb/pp_top aecp-dispatch` (planted diffs: `probe-*.diff`) |
| `milan-dp-{base,head}` | scratch parent | a shallow clone of milan-fpga at dev a032c6d6 with submodules initialised. `head` has one local commit (never pushed, push URL disabled) moving the protocol-processor gitlink to 33d3010c. Command: `make -j8 -C tb/verilator/milan_dp SIM_JOBS=2 VERILATOR_JOBS=2 VERILATOR=$VERILATOR`. Logs gzipped. `milan-dp.summary.txt` compares the sorted, time-normalised check lines |
| `ooc-record-digests-head` | scratch parent (head) | `./syn/yosys/ooc.sh --record-rom-digests`, which adds rows for 33d3010c identical to 93fb0b2d's |
| `ooc-pptop-{base,head}` | scratch parents | `./syn/yosys/ooc.sh protocol_processor_top`, after adding the one list row `"protocol_processor_top\|$PP_DERIVED"` after `KL_pp_shadow` in `syn/yosys/ooc.sh` |
| `clone-integrity.txt` | reviewed clone | HEAD, tree, index tree, a clean status with ignored files shown, index modes and blobs equal to HEAD, and worktree blob hashes |
| `hosted-checks.txt` | — | read-only `gh api .../commits/33d3010c/check-runs` |
