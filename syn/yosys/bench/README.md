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
- **[Results](#results)** — The 2026-09-04 campaign on one machine: netlist invariance across four allocators, the allocator table with RSS beside wall, where the time goes and the front-end share, the whole gate serial and sharded, the rebuilt-Yosys, huge-page, host and re-parse levers, the result-cache costing, and a go/no-go per lever.

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

Measured 2026-09-04 with this harness on one machine, from the campaign
recorded under the issue. Every figure below is the median of 3 trials with its
min-max unless starred, and every batch states its concurrency.

### Machine and tools

- machine: AMD EPYC 9554P (`znver4`), presented as 128 single-core vCPUs by a
  `kvm` hypervisor, 72.7 GiB RAM, kernel 7.2.2, THP `always`/defrag `madvise`,
  `/tmp` a 250 GiB tmpfs
- `yosys 0.66` (distribution build of upstream tag `v0.66`, `g++ 16.1.1`,
  `-O2 … -O3`, external ABC), `sv2v v0.0.13`, glibc 2.44
- jemalloc 5.3.1, mimalloc 3.5.1, gperftools (tcmalloc) 2.18.1, all as
  `LD_PRELOAD` drop-ins through `malloc.sh`'s selection rules
- machine load before every batch is on each record (1.4 to 2.5, from the
  campaign's own earlier cells)

### Netlist invariance

One matched batch of four allocators per top, `write_rtlil` appended to the
gate's program:

| top | cells | wires | `write_rtlil` sha256, all four allocators |
| --- | ---: | ---: | --- |
| `KL_crf_rx` | 30 104 | 21 235 | `d5287ce6e8b5b834…` (6 329 152 bytes) |
| `KL_pp_shadow` | 1 133 318 | 808 050 | `fe6bd6e35f180b4e…` |
| `milan_datapath` | 1 610 463 | 1 146 704 | `ab84e1b99194b0a5…` |

Byte-identical under glibc, jemalloc, mimalloc and tcmalloc on every top. The
allocator is a speed knob only; nothing else in this section is conditional.

### Allocator

Three trials per cell, each trial one matched batch of the four allocators
(concurrency 4):

| top | allocator | wall s | CPU s | peak RSS MiB | wall vs glibc | RSS vs glibc |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `milan_datapath` | glibc | 452.9 (451.6-456.6) | 508.8 | 2 810 | - | - |
| | jemalloc | 300.5 (300.3-300.9) | 346.3 | 2 761 | **-33.7%** | -1.8% |
| | mimalloc | 313.8 (313.2-313.9) | 356.5 | 2 551 | -30.7% | -9.2% |
| | tcmalloc | 332.4 (332.3-332.6) | 427.9 | 2 379 | -26.6% | -15.3% |
| `KL_pp_shadow` | glibc | 223.8 (223.1-225.1) | 261.1 | 1 888 | - | - |
| | jemalloc | 157.3 (157.3-157.6) | 190.0 | 1 927 | **-29.7%** | +2.1% |
| | mimalloc | 163.4 (163.3-163.4) | 192.1 | 1 672 | -27.0% | -11.4% |
| | tcmalloc | 175.1 (174.2-175.1) | 239.1 | 1 569 | -21.8% | -16.9% |
| `KL_crf_rx` | glibc | 3.64 (3.61-3.68) | 4.01 | 117 | - | - |
| | jemalloc | 3.19 (3.17-3.23) | 3.53 | 250 | -12.4% | +113% |
| | mimalloc | 3.16 (3.14-3.18) | 3.52 | 177 | -13.2% | +51% |
| | tcmalloc | 3.37 (3.32-3.42) | 3.89 | 129 | -7.4% | +10% |

Two lone runs of `milan_datapath` at concurrency 1 (one trial each, starred in
the report): glibc 454.5 s, jemalloc 298.4 s (-34.3%). Three glibc+jemalloc
pairs at concurrency 2 give 460.1 s and 300.7 s (-34.6%) on `milan_datapath`
and 226.8 s and 156.8 s (-30.9%) on `KL_pp_shadow`. Concurrency 1, 2 and 4
agree within 2%, so a matched batch costs nothing measurable on this machine
and the batched medians stand.

The win is a CPU reduction (509 s to 346 s on `milan_datapath`), grows with
design size, and leaves peak RSS within 2% on the two heavy tops. jemalloc
doubles the RSS of the 4-second top, from 117 to 250 MiB, which is the
size-dependence the issue warned about and is irrelevant to a shard pool's
budget. mimalloc is within 3 points of jemalloc and saves 9-11% RSS on the
heavy tops; tcmalloc is the slowest of the three and saves the most memory.

### Where the time goes

`milan_datapath`, glibc, median of the three timed trials:

| pass | seconds | share of wall | calls |
| --- | ---: | ---: | ---: |
| `abc` | 132.0 | 29.1% | 1 |
| `opt_dff` | 105.2 | 23.2% | 76 |
| `opt_clean` | 90.6 | 20.0% | 82 |
| `opt_expr` | 61.0 | 13.5% | 424 |
| `opt_muxtree` | 25.8 | 5.7% | 204 |
| `opt_merge` | 18.5 | 4.1% | 80 |
| `techmap` | 12.8 | 2.8% | 1 |
| `read_verilog` | 2.6 | 0.6% | 1 |

The `opt*` family is about two thirds of the run and `abc` most of the rest.
The whole front end, `sv2v` plus `read_verilog`, is 10.8 s of 461 s on
`milan_datapath` (**2.3%**), 6.2 s of 229 s on `KL_pp_shadow` (2.7%), and
0.24 s of 3.9 s on the small top. Over the complete 48-top inventory `sv2v`
takes 26.1 s in total and emits 2.7 MB of Verilog. That is the entire prize any
front end can win, for every top together.

### Whole gate

`syn/yosys/run.sh --no-structural`, the full 48-top inventory, 48 pass in every
configuration:

| configuration | wall | vs serial |
| --- | ---: | ---: |
| serial, glibc (`YOSYS_MALLOC=none`) | 856.9 s (14m17s) | - |
| 8 shards in parallel, glibc | 488.2 s (8m08s) | -43.0% |
| 8 shards in parallel, jemalloc (the shipping default) | **310.1 s** (5m10s) | **-63.8%** |

Sharding buys 1.76x and cannot buy more: `milan_datapath` alone is 453 s under
glibc, so the 8-shard glibc gate sits 35 s above that one process. The
allocator lifts the floor itself, to 300 s, and the sharded gate follows it to
310 s. That is the measured ceiling #270 inherits: the gate cannot finish
faster than its longest top, and today that top is 300 s.

### Rebuilt Yosys

The same upstream tag `v0.66` (`86f2ddeb`) built here twice with `g++ 16.2.1`,
external ABC and LTO off, through the project's own `Makefile.conf`:
**stock** with the distribution's exact flags (`-march=x86-64 -mtune=generic
-O2 … -O3`, hardening on), and **native** with `-march=native -O3
-fomit-frame-pointer -fno-semantic-interposition` and the hardening flags
dropped. (`-ljemalloc` was passed to the native link and discarded by the
toolchain's `--as-needed`, so both binaries use glibc unless preloaded; that
isolates the flag effect, and the preload gives the allocator effect.)

Reproduction first: under each rebuilt binary the whole 48-top gate passes and
every `cells=` record equals the distribution binary's, all 48 of 48. The
`write_rtlil` netlist of `KL_gptp_shadow` differs from the distribution
binary's in exactly 78 lines: the `# Generated by Yosys` banner (compiler and
flags) and 38 pairs of `\src` attributes that spell the bundled `techmap.v`
under the install prefix instead of `/usr/share/yosys`. Cells (203 960) and
wires (145 614) are equal, and the stock and native netlists differ from each
other by the same 78 lines only. Each binary reproduces its own digest.

Timing, glibc+jemalloc as one matched batch (concurrency 2), three trials:

| top | binary | glibc wall s | jemalloc wall s | jemalloc vs distribution |
| --- | --- | ---: | ---: | ---: |
| `milan_datapath` | distribution 0.66-1 | 460.1 (458.5-464.6) | 300.7 (300.0-302.2) | - |
| | stock (distro flags, built here) | 434.3 (433.6-439.9) | 269.4 (269.3-270.1) | **-10.4%** |
| | native (tuned flags) | 436.6 (434.0-442.6) | 271.2 (270.3-271.4) | -9.8% |
| `KL_pp_shadow` | distribution 0.66-1 | 226.8 (226.0-227.0) | 156.8 (156.0-157.2) | - |
| | stock | 216.9 (214.5-220.6) | 143.8 (142.6-144.8) | **-8.3%** |
| | native | 215.5 (213.8-217.5) | 142.5 (141.8-145.1) | -9.1% |

Building the same commit here with the distribution's own flags is already
5-10% faster than the packaged binary; that gain is compiler version and build
configuration, not ISA tuning, because the tuned build lands within 1% of the
stock one on both tops. Peak RSS is 2-5% higher on the rebuilt binaries
(2 885 against 2 809 MiB on `milan_datapath` under glibc). The prize is real
but small next to the allocator's 34%, and adopting it means a digest-pinned
artefact that CI builds or downloads instead of `apt-get install yosys`; that
is the trade #287 already priced when it pinned the toolchain.

### Transparent huge pages

`KL_pp_shadow`, glibc and jemalloc as one matched batch (concurrency 2), three
trials with the machine's `THP always` policy and three under a
`PR_SET_THP_DISABLE` wrapper around the same `yosys` binary:

| configuration | wall s | peak RSS MiB |
| --- | ---: | ---: |
| glibc, THP on | 225.1 (224.9-226.7) | 1 900 |
| glibc, THP off | 233.6 (233.4-234.6) | 1 895 |
| jemalloc, THP on | 156.9 (156.4-157.2) | 1 926 |
| jemalloc, THP off | 164.3 (163.9-164.5) | 1 378 |

Huge pages are worth 3.8% to glibc and 4.7% to jemalloc on this top, and
jemalloc pays 40% more peak RSS for them (1 378 to 1 926 MiB). That is the
ceiling of the memory-tuning family on this workload: single digits, traded
against the memory a shard pool needs. The policy is already `always`, so
there is nothing to switch on; a pool that runs out of memory has this 4.7% to
give back.

### Host and firmware

`systemd-detect-virt` reports `kvm`; the 64-core part is presented as 128
single-core sockets in one NUMA node with no `cpufreq` interface and no cache
topology. Nothing firmware-side is reachable from this guest. The two host-side
items usually proposed are already in place: the scratch path is RAM-backed
(`/tmp` is tmpfs and `run.sh` puts its `mktemp -d` there) and THP is `always`.
What remains is a request to the hypervisor owner, to be measured there before
it is reported as a result: CPU topology passthrough so a shard pool can see
real cores and L3 domains, 1 GiB huge-page backing for the guest (the lever
that matters for a 3 GiB single-process heap), vCPU pinning, and on the
firmware itself determinism/cTDP, C-state and DF C-state policy and SMT. The
kernel's `Safe RET`, TSA and Enhanced IBRS mitigations cost cycles on this
call-heavy workload but need a reboot and a security decision, so they stay a
hypothesis.

### The protocol-processor re-parse

The processor's own portability gate (`protocol-processor/syn/yosys/run.sh`:
one `sv2v` of the whole `hdl/` tree into `all.v`, then 32 `yosys` processes
that each `read_verilog all.v` before selecting their top, then one
`synth_xilinx` area check) as shipped, and the same script with
`read_verilog -defer`, three serial trials each on the pinned processor
(`e743dcdc`), all 33 checks passing in every run:

| variant | wall s | peak RSS MiB |
| --- | ---: | ---: |
| A, as shipped: 32 processes, each parses all 38 modules | 65.0 (64.9-65.1) | 3 745 |
| C, `read_verilog -defer` | 33.8 (33.6-33.9) | 3 757 |

`-defer` halves the whole script; the peak RSS belongs to the final
`synth_xilinx` step and is the same either way. This is the one place in the
tree where `-defer` is the right instrument, because it is the one place that
re-reads modules it will not use; `run.sh` here stages one top per `sv2v`
output and gains nothing from it (README, "Runtime levers"). The change lives
in the processor repository, behind its issue #25, which should first complete
the six tops that array does not elaborate.

### Result cache

Not measured: a cache is a design, not a lever to time. A top whose `sv2v`
output digest, Yosys version string and exact program string are all unchanged
would be skipped; on the common PR that is 46 or more of the 48 tops, so the
gate would take the time of the tops the PR touched. Its cost is the trust
surface: under #270's rules the seed must be read-only and trusted, the
per-head state writable only by the run, and no candidate may write a shared
cache, which means the cache key must include the Yosys binary digest as well
as its version string, and a hit must still re-check the recorded `cells=`
against the stored record. That is
[#350](https://github.com/kebag-logic/milan-fpga/issues/350), not a change to
this gate.

### Go and no-go

| lever | verdict | evidence | follow-up |
| --- | --- | --- | --- |
| allocator preload | **go, adopted** | -33.7% on the heaviest top, gate 488 s to 310 s, netlists byte-identical, RSS neutral on heavy tops | landed as `run.sh`'s default (`malloc.sh`); mimalloc stays the documented alternative where RSS is tight |
| shard parallelism | measured, hand to #270 | 1.76x at 8 shards, floor = `milan_datapath` (300 s under jemalloc) | #270 |
| result cache | go | largest remaining win on the common PR; trust rules costed above | [#350](https://github.com/kebag-logic/milan-fpga/issues/350) |
| front end (Verific, yosys-slang) | **no-go** as a speed lever | 2.3% of the critical path, 26 s over the whole inventory; Verific is commercial-only | yosys-slang only as a robustness lane |
| rebuilt Yosys | adopt-behind-an-option, not now | -8 to -10% under jemalloc from the build itself, 0% from `-march=native`; every `cells=` reproduced; netlist differs in banner and bundled paths only | fold into #287's pinned-toolchain artefact if a digest-pinned build ever replaces the package; no separate issue |
| transparent huge pages | no-go as a lever | already on; worth 4-5%, at +40% RSS under jemalloc | none; a memory-bound pool may switch it off per process |
| host and firmware | not measurable here | guest with no topology or firmware reach | written request to the host owner |
| protocol-processor re-parse | go, in the processor repository | its gate halves (65.0 to 33.8 s) with `read_verilog -defer`, 33 of 33 checks green | protocol-processor #25 (complete the tops array first) |
