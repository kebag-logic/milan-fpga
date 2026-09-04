# Yosys single-process bench

What one `yosys` process costs on one top of the portability gate, and
whether a lever moves it
([#286](https://github.com/kebag-logic/milan-fpga/issues/286)). The gate
([`../README.md`](../README.md)) cannot finish faster than its longest top,
and that top is one single-threaded process. This harness measures that
process reproducibly, so one figure can be compared with another: every record
states the machine, the tool versions, the input digest, the trial and the
concurrency it ran at.

## Contents

- **[What it measures](#what-it-measures)** — One cell, one record, and the six rules behind them: staging from `run.sh --emit` only, the gate's own program with relative paths, what each run records, allocators resolved through `malloc.sh` and refused when absent, no number without proof, and concurrency on the record.
- **[Reproduce a cell](#reproduce-a-cell)** — The exact commands for the invariance oracle, a timed batch of at least 3 trials, a lone-process run, and the report; where the output goes and what the heavy tops cost.
- **[Records and the report](#records-and-the-report)** — Every field a per-trial JSON carries, and how `--report` groups them into `median (min-max)` rows compared only against glibc at the same concurrency, with `MISMATCH` and the below-3-trials star.
- **[Self-test](#self-test)** — The ten fixture arms, each planting the defect it guards, and what they do not need.
- **[Results](#results)** — Deliberately empty: the campaign fills it in, and the issue's first-pass figures are not repeated here.

## What it measures

One cell is one top under one allocator; one record is one trial of a cell.

- **Staging, as the gate does it.** The `define=`/`incdir=`/`src=` record
  comes from `run.sh --emit TOP` and from nowhere else; `sv2v` lowers it into
  `<out>/work/TOP/TOP.v` beside the three ROM images `run.sh` generates. The
  sha256 of that file is the **input digest** on every record.
- **The gate's program.** `yosys -d -p "read_verilog TOP.v; synth -top TOP;
  hierarchy -check; stat -top TOP; tee -q -o <run>.stat.json stat -top TOP
  -json"`, run from the work directory. The self-test compares this text with
  the line in [`../run.sh`](../run.sh); the one difference is relative paths,
  so a netlist digest does not depend on where the checkout lives.
- **Per run:** wall, user and system seconds and peak RSS (`/usr/bin/time -f
  '%e %U %S %M'`, or `wait4` rusage where GNU time is absent), the `-d`
  per-pass `Time spent` table, the `stat -json` cell and wire counts and, with
  `--rtlil`, the sha256 and size of a `write_rtlil` netlist.
- **Named allocators.** `glibc` (LD_PRELOAD actively unset), `jemalloc`,
  `mimalloc`, `tcmalloc`, or `name=/path/to/lib.so`. Each is found on the
  loader's path and passed through `select_malloc` in
  [`../malloc.sh`](../malloc.sh), so an absent or unloadable library is
  refused, never measured as glibc under another name.
- **No number without proof.** A non-zero exit, an `ERROR:` line, no
  top-level `hierarchy` pass after `synth`, no `End of script.`, no per-pass
  table or no design count leaves a record marked `failed` with every timing
  field null.
- **Concurrency on the record.** `--batch` starts every variant of a top at
  once, as one matched batch; each record states the concurrency it ran at,
  and the report compares only cells taken at the same concurrency.

## Reproduce a cell

Requirements: `yosys`, `sv2v`, `python3`, the submodules checked out, and
whichever allocator libraries you name. Run from the repository root.

```sh
# the netlist-invariance oracle: one matched batch, all four allocators
python3 syn/yosys/bench/yosys_bench.py --top KL_crf_rx --batch --rtlil --trials 1
# timing: at least 3 trials, one matched batch per trial
python3 syn/yosys/bench/yosys_bench.py --top KL_crf_rx --batch --trials 3
# a lone process (concurrency 1): a different number, not comparable with a batch
python3 syn/yosys/bench/yosys_bench.py --top KL_crf_rx --alloc glibc,jemalloc --trials 3
# the table
python3 syn/yosys/bench/yosys_bench.py --report --markdown bench.md
```

Output goes to `out/` beside the harness (gitignored); `--out DIR` moves it.
`--stage-only` stages and digests without running; `--top` may be repeated;
`YOSYS_SYNTH` is honoured as in `run.sh`. The heavy tops (`milan_datapath`,
`KL_pp_shadow`) take minutes per run and up to 3 GiB each, and a batch of four
runs four at once. A `write_rtlil` netlist is tens of MB for a mid-sized top.

## Records and the report

One JSON file per trial under `<out>/records/`: top, variant, library and
package version, trial, batch id, concurrency, the 1-minute load before start,
the exact program and its shape, input digest and `sv2v` argv, tool versions,
machine (CPU model, vCPUs, virtualisation, RAM, kernel, THP policy), status and
reason, exit code, timing, counts, the pass table and the netlist digest.

`--report` groups records by machine and tools, then by top, input digest and
program, and prints one row per variant and concurrency: trials ok/run,
concurrency, wall, CPU and peak RSS as `median (min-max)`, wall against the
glibc row at the same concurrency, cells, wires and the netlist digest, which
reads `MISMATCH` when a cell's trials disagree. A row below 3 OK trials is
starred and is not a publishable figure.

## Self-test

```sh
python3 syn/yosys/bench/yosys_bench.py --selftest
```

Ten arms, each planting the defect it guards: the emit record, the `-d` table
against the one-line summary, the GNU time line, every refusal in the verdict,
null numbers on a failed run, digest equality and the `MISMATCH` column,
allocator refusal, the report arithmetic, the program against `run.sh`'s own
line, and the record round-trip. It needs neither yosys, sv2v nor an allocator
library.

## Results

**Not yet measured.** The measurement campaign of
[#286](https://github.com/kebag-logic/milan-fpga/issues/286) fills this
section in: the allocator comparison on `milan_datapath`, `KL_pp_shadow` and
one small top, with the record directory, the rendered report and the netlist
digests for each. Until then the figures in the issue are the hand-taken first
pass, and this page carries none of them.
