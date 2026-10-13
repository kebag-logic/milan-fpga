# R628-6 receipt recipes

The report identifies the reviewed head and source base.
`MANIFEST.sha256` is the publication allowlist; `scratch/` is excluded.
Receipt paths are normalized to `$PACKET`, `$CLONE`, `$HOME` and
`$VALIDATION_TOOLS`. Values, check names and verdicts are unchanged.

Set these paths before using the recipes:

```sh
export CLONE=/path/to/detached-review-clone
export PACKET=/path/to/726-r628-6-packet
export VERILATOR=/path/to/verified-verilator-5.050
export PINNED_VERILATOR="$VERILATOR"
export PYTHONDONTWRITEBYTECODE=1
export TMPDIR="$PACKET/scratch"
mkdir -p "$TMPDIR"
cd "$CLONE"
"$VERILATOR" --version
```

Run each command in the foreground and retain its return code.
The fixture drivers build with two workers. No command below needs a
full repository bank, hardware, a container or a shared install.

Audit saved measurements without rebuilding:

```sh
python3 "$PACKET/scripts/audit_receipts.py" "$PACKET"
python3 "$PACKET/scripts/verify_tree.py" "$CLONE" \
  12f00129349c889e6dbbb7de11529ab38c9d164d \
  e0a0682e5c703755d1e1e003967d70f66d5c0757
```

Reproduce clean packet/cadence measurements. Use shapes 1 and 8 and
conditions `uncertain` and `frames-only` for the four combinations:

```sh
MAKEFLAGS=" -w" python3 tb/verilator/milan_dp/stream_counters.py \
  --shape 1 --output-condition uncertain --work "$PACKET/scratch/repro-clean-1"
make -j16 -C tb/verilator/milan_dp counters
```

Run a shipped mutation using `--variant` instead of the clean default.
The driver itself requires both named detection and omission escape.
`REPORT.md` lists all variants; egress-stall also runs at shape 8.

```sh
python3 tb/verilator/milan_dp/stream_counters.py \
  --shape 1 --variant egress-stall --work "$PACKET/scratch/repro-egress-1"
python3 tb/verilator/milan_dp/stream_counter_f5.py \
  --shape 1 --variant late --work "$PACKET/scratch/repro-f5-late"
```

The unchanged earlier probes accept these arguments:

```sh
python3 "$PACKET/probes/reproduce_contract.py" "$CLONE"
python3 "$PACKET/probes/probe_xside_law.py" "$CLONE"
python3 "$PACKET/probes/probe_snapshot.py" "$CLONE" "$PACKET"
python3 "$PACKET/probes/probe_counters.py" "$CLONE" sched-1600 1 \
  "$PACKET/scratch/repro-sched-1600"
sh "$PACKET/scripts/rerun_fixture.sh" "$PACKET/scratch/repro-sched-1600" \
  omit.log COUNTERS_OMIT_CHECK=CADENCE
```

Repeat the last pair for `sched-2000` and `egress-stall`, shapes 1 and 8.
Expected failures are only CADENCE: eight at shape 1, thirty-six at shape 8.
The original probe prints the result; inspect the named groups, not merely
its process return code. Omission must print `RESULT: PASS` without failures.

Other reviewer controls:

```sh
python3 "$PACKET/scripts/probe726.py" "$CLONE" aaf-guard 1 \
  "$PACKET/scratch/repro-aaf-guard" uncertain CADENCE
python3 "$PACKET/scripts/probe_snapshot_guard.py" "$CLONE" "$PACKET"
sh "$PACKET/scripts/probe_tkdiag.sh" "$CLONE" \
  "$PACKET/scratch/repro-start-drop" tx-start-drop
sh "$PACKET/scripts/rerun_fixture.sh" "$PACKET/scratch/repro-clean-1" \
  shift_1000000.log COUNTERS_WINDOW_SHIFT=1000000
```

For the focused style/source gates, use `scripts/run_gates.sh` with the
clone and an output directory under scratch. TOC and em-dash commands
require the repository's pinned Markdown dependencies. The initial missing
dependency returns and the later successful retries remain in the ledger.
The report distinguishes those local commands from the successful hosted
documentation job and its 55 executed steps.
