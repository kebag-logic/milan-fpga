# R684-1 focused reproduction

Run from this packet directory. `REPO` is an initialized checkout of exact head
`a97aea01449492b1f640924f5a34726f602cabed`. `EVIDENCE` is the directory
`review-evidence/771-r1` extracted from public commit
`980703e623f3ee3b0249dc05466e5494f17ebe02`.

The scripts need the repository's native test dependencies. The firmware probe
uses its installed test framework and compilers, but no RV32 build or full bank.
The simulated tests used the verified 5.050 compiler at
`$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`; supply an equivalent executable
as `VERILATOR` on another host.

Read-only original-checkout checks:

```sh
python3 run_checks.py "$REPO"
python3 audit_adoption.py "$REPO" "$EVIDENCE"
python3 probe_acmpwalk.py "$REPO"
python3 verify_integrity.py "$REPO"
```

The ACMP probe runs only `arm_acmpwalk`, concurrently for the adopted oracle and a
historical-oracle attribution control (two builds, four jobs each). Expected
individual exits are 1 and 0; the driver exits 0 when this reproduction matches.
The historical oracle is extracted from the old processor git object, which must
be available locally. No source or index file in REPO is edited.

Make a separate exact-head checkout at `scratch/probe`, with initialized
protocol-processor, gptp-processor and third_party/verilog-axis submodules. This
checkout must be inside this packet's scratch directory. Never point the fault
probe at the reviewed checkout.

```sh
python3 regenerate_records.py "$PWD/scratch/probe"
python3 probe_gptp.py "$PWD/scratch/probe" "$VERILATOR"
python3 run_plane_legs.py "$PWD/scratch/probe" "$VERILATOR"
python3 verify_integrity.py "$PWD/scratch/probe"
```

`probe_gptp.py` runs 310 golden wrapper checks, then changes only the disposable
engine's append condition to false and expects five failures. It restores the
source in a finally block. The two dataplane legs are each 185 checks; they compile
concurrently under one `make -j16` with four jobs per compiler and then simulate
concurrently. They exercise the real engine datapath and both configured latency
values. No full bank or physical implementation is run.

Receipt map:

- `check-results.json` and named logs/rc files: eleven read-only gates.
- `adoption-audit.log`: published hashes, independent/sequential patch application,
  exact postimages, donor interfaces, record deltas/policies, image corners and
  sweep/docs tally checks.
- `regenerated-records.log`: ROM, port-contract and naming generator round trips.
- `shadow-*.log`, `shadow-probe-results.json`: golden/negative wrapper control.
- `plane-*.log`, `plane-results.json`: gptp and gptp-lat legs.
- `acmpwalk-*.raw.log`, `acmpwalk-results.json`: raw firmware reproduction and
  historical-model control. Path-normalized `.log` copies ease comparisons.
- `hosted-firmware-failure.log`: relevant verbatim hosted failure lines and URL.
- `hosted-snapshot.json`: executed, skipped, cancelled and pending job states;
  it is a point-in-time observation, not an acceptance verdict.
- `prior-findings-check.json`: public timeline checked only after the independent
  verdict and ledger were written.
- `integrity.log`, `probe-restoration.log`: original and disposable tracked bytes,
  modes, index and initialized gitlinks verified after probes.

Compiler build intermediates and extracted inputs are scratch-only. The published
simulation output is unfiltered; full raw ACMP output is supplied alongside its
path-normalized copy. The public author evidence is linked by immutable commit
and independently hash-checked, rather than duplicated into this packet.
