# Open-toolchain synthesis check (Yosys) — device portability

This proves the Milan RTL is **vendor-neutral**: now that the Xilinx XPM primitives
are gone (the retired migration record remains in Git history),
every block maps to a **generic, device-independent** cell library with the
open-source [Yosys](https://yosyshq.net/yosys/) synthesizer — so it will build on
non-Xilinx FPGAs (Lattice ECP5/iCE40, Gowin, Efinix, ASIC flows, …), not just Vivado.

It complements the Verilator harnesses (`tb/verilator/`, which prove *behaviour*) by
proving *synthesizability on other devices*.

```sh
git submodule update --init third_party/verilog-axis   # required: several tops
                                                        # elaborate Forencich cores
cd syn/yosys
make            # generic synth (device-independent) of every top -> RESULT: PASS
make ecp5       # map to a real non-Xilinx device: Lattice ECP5 (TRELLIS_FF/LUT4)
```

## Contents

- **[How it works](#how-it-works)** — The two-stage pipeline and why each stage is there: sv2v converts the SystemVerilog Yosys cannot parse (interfaces, packages, assignment patterns), then `hierarchy -check` is what makes a PASS mean something — it fails on any surviving vendor primitive, so green = fully mapped to generic logic with nothing Xilinx-specific left.
- **[Tooling](#tooling)** — The two binaries you need and where to get them. No Xilinx tools are required, which is the point — this flow is the evidence that the RTL is not tied to one vendor's toolchain.
- **[Runtime levers](#runtime-levers)** — Why this gate is optimisation-bound and not parse-bound, which is the one fact that decides every speed question here: the jemalloc preload it now runs under (−45% on the heaviest top, −42% on the whole sharded gate, byte-identical netlist) and how to turn it off, and the measured reason `read_verilog -defer` is *not* used — it removes 85% of a step that is 0.5% of the run, and changes the cell count by 1.3% while doing it.
- **[Coverage](#coverage)** — What the tops actually span, and the standing rule that the `tops=()` array is the count while this prose is not.
- **[Notes](#notes)** — Two facts that stop you misreading the output: the concrete non-Xilinx targets (`synth_ecp5`, `synth_ice40`) with real cell counts, and why `axis_fifo` looks enormous — its 4096-deep default, which no instance in the design uses.
- **[ooc.sh — AREA measurement (a different question from run.sh)](#oocsh--area-measurement-a-different-question-from-runsh)** — `run.sh` asks *does it map*; this asks *what does it cost*, which is the only number an area lever may be judged on. Three traps it exists to avoid, and the third is the sharpest: `-flatten` can read a genuinely deleted block as **−1 LUT / −0 FF**, so a structural lever needs the hierarchy-preserving form as well. Ends with the honest caveat — these are estimates with a yosys→Vivado ratio between 0.25 and 0.86, and control sets are not measurable here at all.

## How it works
1. **[sv2v](https://github.com/zachjs/sv2v)** converts the SystemVerilog (interfaces,
   packages, assignment patterns) to Verilog-2005 — Yosys's built-in frontend does
   not handle SV interfaces. Interface-port modules (`traffic_classifier`,
   `traffic_queues`) are synthesised through their flat wrappers in `tb/verilator/*`.
2. **Yosys** runs `synth` (generic) then `hierarchy -check`. `hierarchy -check` fails
   if any **undefined / vendor primitive** remains, so a PASS means the module is
   fully mapped to generic logic (`$_AND_`, `$_DFF_`, `$_MUX_`, …) — nothing
   Xilinx-specific left.

## Tooling
- `yosys` (Arch: `pacman -S yosys`).
- `sv2v` on `PATH` — pinned prebuilt release from
  [github.com/zachjs/sv2v/releases](https://github.com/zachjs/sv2v/releases)
  (drop into `~/.local/bin`). No Xilinx tools required.

## Runtime levers

This gate is **optimisation-bound, not parse-bound**. `yosys -d` on
`milan_datapath` — 1,137,752 wires and 1,597,718 cells in one single-threaded
process — spends its time like this ([#286](https://github.com/kebag-logic/milan-fpga/issues/286)):

| pass | share |
| --- | ---: |
| `opt_dff` | 25% |
| `opt_clean` | 23% |
| `abc` | 16% |
| `opt_expr` | 14% |
| `opt_merge`, `opt_muxtree`, … | 9% |
| `read_verilog` | **0.5%** |

Everything below follows from that one table. **The front end is not the
cost**, so no front-end change — `-defer`, a faster parser, or a commercial
one — can move this gate much. `sv2v` over the *whole* 46-top inventory is
34.6 s.

### The allocator: on by default, worth ~45%

Yosys allocates constantly, and glibc's allocator is where a large share of
the `opt*` time goes. `run.sh` therefore preloads **jemalloc** for its `yosys`
children when the library is installed:

| scope | glibc | jemalloc |
| --- | ---: | ---: |
| `milan_datapath`, one process | 656.3 s | **361.5 s** (−44.9%) |
| `KL_pp_shadow`, one process | 273.9 s | 171.8 s (−37.3%) |
| whole gate, 8 shards, 46/46 pass | 616.2 s | **357.8 s** (−41.9%) |

Peak RSS *falls* as well (3033 → 2786 MiB on `milan_datapath`), so this does
not spend the memory a parallel shard run needs.

**It changes speed and never results**, and that was measured, not assumed:
`write_rtlil` after this gate's own program is byte-identical under glibc,
tcmalloc, jemalloc and mimalloc (`sha256 cc79dc89adbce892…`, 43,920,712 bytes
on `KL_gptp_shadow`).

It is optional in both directions — the tool requirement above is still just
`yosys` and `sv2v`, and a machine without jemalloc runs exactly as before:

```sh
YOSYS_MALLOC=none  ./run.sh     # system allocator
YOSYS_MALLOC=/path/to/lib.so ./run.sh
./run.sh --selftest-alloc       # check the selection rules; needs nothing else
```

A **named** library is refused rather than quietly ignored if it is absent, or
if the dynamic loader will not take it — an existing file that is not a shared
object counts. The loader drops such a preload by *ignoring* it: the process
still exits 0 and the complaint goes to stderr, which for a `yosys` child lands
in that top's log and is never read, so the check is that stderr stayed empty.
A relative path is made absolute first, because `yosys` runs from the gate's
own temporary directory and would otherwise resolve it there. All three cases
are the same defect: a run asked to reproduce one allocator reporting another
one's timing under its name.

`YOSYS_MALLOC=none` **unsets** `LD_PRELOAD` for the `yosys` child rather than
merely declining to set it, so it still means "system allocator" in a shell
that already exports one.

The header line prints which allocator was in effect, because a wall-clock
figure quoted from this output is only reproducible with it. The preload
reaches `yosys` and the `abc` it spawns; `sv2v` and the `python3` helpers are
left alone and keep whatever the caller's environment gives them.

The rules live in one place, [`malloc.sh`](malloc.sh), and `ooc.sh` below
sources the same file and honours the same `YOSYS_MALLOC` values. That flow
gains more, because `synth_xilinx -flatten` is the heavier program — 235.09 s
to 177.85 s over `KL_pp_shadow`, `KL_crf_rx` and `tcam` together (−24.3%),
with every reported area row identical to the digit. `run.sh --list` does
**not** source it: `check_list_hermetic.sh` proves `--list` reads nothing but
`run.sh` and `scripts/yosys_shards.py`, and that contract outranks the tidiness
of an unconditional `source`.

### `read_verilog -defer`: right instrument, wrong script

`-defer` postpones turning a parsed module into RTLIL until something
instantiates it. **It only pays where one file holding many modules is read
once per top**, so the reader spends time elaborating modules that top will
never use.

That is not this gate. `run.sh` gives every top its *own* `sv2v` output, built
from that top's own source list, so there is almost nothing to defer. Measured
on the two tops with the largest surplus — both are handed the entire
protocol-processor tree and instantiate a subset of it:

| top | plain | `-defer` | `read_verilog` step | cells |
| --- | ---: | ---: | ---: | ---: |
| `milan_datapath` | 353.5 s | 350.0 s (−1.0%) | 2.30 s → 0.26 s | 1,597,718 → 1,598,979 |
| `KL_pp_shadow` | 165.9 s | 166.4 s (+0.3%) | 0.89 s → 0.16 s | 1,133,318 → 1,148,270 |

`-defer` does what it says — it removes 82–89% of the `read_verilog` step —
and that step is 0.5% of the run, so the gate does not get faster. Worse, the
result is **not** the same netlist: +0.08% cells on `milan_datapath` and
+1.3% on `KL_pp_shadow`, because deferring changes which parameterised
specialisations exist by the time the `opt*` passes run. The same binary run
twice reproduces its own digest, so that is the flag and not run-to-run
variation.

So `run.sh` does **not** use `-defer`: it costs a changed answer and buys
nothing. The flag belongs in the control plane's own portability gate
(`syn/yosys/run.sh` inside the `protocol-processor` submodule), which lowers
its whole `hdl/` tree into a single `all.v` and then re-reads it once per top,
32 times — there it is 39.65 s → 10.31 s, and 1.25 s with a bounded process
pool. Before applying it there, read that repository's issue #25: six of its
modules are not in its `tops` array at all, so nothing ever elaborates them as
a top, and that array should be completed first.

One thing `-defer` does **not** cost, controlled on that gate by injecting a
fault into a module no top instantiates and running both forms over it:
coverage. A syntax error is caught either way — by `sv2v`, before Yosys reads
anything — and an instance of an undefined module is missed either way,
because nothing elaborates a module that is in no top. `-defer` postpones
elaboration; what provides elaboration coverage is the `tops` array, not the
reading mode.

The rule to carry to the next script: **`-defer` is a fix for re-reading, not
a fix for synthesis.** Check the `read_verilog` line in `yosys -d` output
before reaching for it.

## Coverage
47 tops as of 2026-08-31 (the `tops=()` array in `run.sh` is authoritative — that
array is the count, this prose is not; re-read it rather than trusting a number
here):

- the new open blocks (`tcam`, `rx_mac_filter`, `cdc_pulse`, `cdc_handshake`,
  `adp_tx_arbiter`),
- the control plane (`KL_pp_shadow`, `KL_pp_maap_shim`) — the protocol
  processor as this datapath instantiates it. The 1722.1/SRP tops it replaced
  (`adp_advertiser`, `KL_aecp_top`, the two ACMP contexts and their two
  wrappers, `KL_persist_journal`, `KL_lwsrp_top`) are gone with that RTL,
- the CSR (`milan_csr`),
- the de-Xilinx'd 802.1Q chain (`classifier_wrap`→`traffic_classifier`,
  `queues_wrap`→`traffic_queues`, `datapath_wrap`→`traffic_controller_802_1q`
  with its queues and shaping core) and the `ptp_ts_top` record stampers —
  both are stand-alone tops since `0x0002_0056`, because `milan_datapath` no
  longer instantiates them and their portability would otherwise go unproven,
- the CBS/PTP/RMON leaves,
- the vendored Forencich cores (`axis_fifo`, `axis_demux`, `axis_arb_mux` —
  kept as a portability check even though the queue egress now uses a plain
  grant-indexed mux instead of `axis_arb_mux`), and
- **`milan_datapath` itself** (the full integration wrapper).

The `avtp_stream_parser` gap noted here previously is **closed** — it is a top
in the array.

## Notes
- `synth_ecp5` (Lattice ECP5) and `synth_ice40` (iCE40) are concrete non-Xilinx
  targets — `make ecp5` maps e.g. `tcam`→~1.7 k `TRELLIS_FF`, `milan_csr`→~2.2 k.
- `axis_fifo`'s large cell count is its default `DEPTH=4096` RAM; instances in the
  design set a small depth.
- `run.sh --emit NAME` prints one top's inventory record (`top=` / `define=` /
  `incdir=` / `derived=` / `src=` lines) and exits. It exists so a second
  consumer does not have to read this script: the Vivado out-of-context flow
  (`syn/ooc/dp_srcs.py`) asks for the record instead of recognising the
  `tops=()` row and the `PP_SRCS` composition as text. A recogniser accepts
  what it has modelled and bash accepts something else, and four such
  disagreements were measured on the recognising version (PR #240). Anything
  printed is bash's own expansion of the row this script is about to
  synthesise, so an edit here moves both consumers or fails both.

## `ooc.sh` — AREA measurement (a different question from `run.sh`)

`run.sh` answers *"does this map to generic logic"* and gates on it.
`ooc.sh` answers *"what does it cost"*, which is the only number an area
lever may be judged on:

```sh
./ooc.sh                      # every top in its AREA list
./ooc.sh KL_chan_map_render   # just these
OOC_CHPARAM="N_STREAMS=8 AUDIO_IF_SLOTS_P=16" ./ooc.sh milan_datapath
OOC_TMP=/some/dir ./ooc.sh …  # keep the .v / .log / .json artefacts
```

It runs `sv2v` → `synth_xilinx -family xc7 -flatten` → `stat` and reports
`LUT1..6`, `FD[CPRS]E?`, `RAMB36E1`, `RAMB18E1`, `DSP48E1`.

**The exit status is the gate** (#245). What is enforced, exactly:

- All three control-plane `$readmemh` images (`ltn_rom.hex`, `ucode.hex`,
  `gptp_ucode.hex`) are
  generated into the run's own tmp dir, never the caller's, each into an
  EXCLUSIVELY created staging file (`mktemp`, never a predictable name a
  stale file could squat) and published by a checked rename only after
  validation; the published target must be a regular file, and a target a
  directory squats is a refusal. A generator failure is exit 2.
- The geometry packages are found IN the derived processor population
  (`scripts/pp_srcs.py`'s answer), never spelled as paths, and each
  geometry number comes from the ONE live declaration in its package,
  comments stripped and the name boundary-anchored; zero, duplicate or
  expression spellings refuse. Each image must hold exactly its ROM's
  geometry after `//`-comment stripping; wrong count, wrong width,
  `x`/`z` digits and an empty image are all exit 2. `$readmemh` part-fills
  a short image with X and yosys prices the X-ROM without a word.
- Each image's CONTENT must match the sha256 recorded for its current owning
  processor pin in [`rom_digests.tsv`](rom_digests.tsv): a
  correctly shaped wrong image (a regressed generator) prices wrong with
  every shape gate green, so shape alone is not protection. A pin bump
  re-records with `./ooc.sh --record-rom-digests`, and that diff is
  reviewed with the bump. An unrecorded pin is a refusal, not a guess.
- Publication is not the end of custody: each top's yosys run consumes an
  EXCLUSIVE read-only copy of both images in a fresh unpredictable
  `mktemp -d` run directory, and the copy is re-hashed against the
  validated digest before the run AND after yosys returns. The run
  directory itself is locked (write permission removed) from before the
  first hash until after the post-run hash, because rename authority is
  DIRECTORY write permission: a transient move-aside-and-restore during
  the read interval would beat both hashes otherwise. Every chmod status
  is taken. A published image swapped or deleted after validation (or
  between two requested tops, or under a running synthesis) is exit 2,
  and no row is emitted for bytes no ledger row vouches for.
- The ledger pins are the SUPERPROJECT's `protocol-processor` and
  `gptp-processor` gitlinks, never either checkout's own HEAD: an uninitialized, conflicted or
  mismatched checkout refuses in normal and record modes alike, so a
  stale checkout can neither record itself nor select a retained old
  row after a pin bump.
- A top failing `sv2v` or yosys sets a STICKY non-zero exit that no later
  passing top can launder; so does a report phase that cannot produce a
  real row: no top-named stat block, a final block mapping to zero xc7
  cells, a dead `awk`, or a missing/empty `write_json` artifact. The row
  is parsed from the LAST top-named block (a pristine log carries two:
  `synth_xilinx`'s internal final statistics, then the explicit `stat`),
  deterministically.
- A requested top the list does not carry is exit 2, not an empty header,
  and the names are checked BEFORE the pin read, the geometry parse and
  either generator: a typo must not cost two ROM generations, nor be
  answered with a ledger diagnostic for a top that does not exist.
- Cleanup is one `EXIT` trap, so a refusal never leaves the run's tmp tree
  behind - and never leaves a LOCKED run directory a later `rm -rf` cannot
  remove. `--record-rom-digests` rewrites the ledger without a pipe and
  refuses to install a file whose row count is not the rows retained plus
  the rows recorded: a dying `awk` used to silently delete every other
  pin's digests and still print success.
- The report's cell taxonomy refuses a distributed-RAM primitive it cannot
  price, rather than counting it as zero LUT6.

Not enforced: the numbers themselves stay yosys estimates (band rule
below), and dropping only the explicit `stat` is not refused, because
`synth_xilinx`'s own final statistics block is the same post-mapping
measurement. `ooc_selftest.py` drives every refusal above on planted
failures (`ARMS` in that file is the count; it asserts its own) covering
shape, content, staging, report, sticky-exit,
launch-directory, consumption-custody and read-interval mutations (the
published image swapped or deleted after publication, between two tops
and mid-run; the transient move-aside-and-restore blocked on the shipping
script and demonstrated on the mutant that forgets the directory lock; a
stale submodule checkout refused in normal and record modes and shown to
false-green under the retired checkout-keyed pin), plus a positive
`KL_pp_shadow` arm whose models assert the authoritative source
population, the exclusive locked per-top run directory, and both
canonical images as read-only copies hashing to the pin's ledger rows);
it runs in `rtl-fast.yml`, where
`scripts/ci_events.py` pins the invocation verbatim AND its step keys, in
  the job that fetches both processor submodules, after that fetch.
The suite refuses to run as root: its custody oracles are mode bits, which
uid 0 bypasses, so the arms would invert rather than fail.

Two traps this exists to avoid:

- **`-flatten` is not optional.** A hierarchical synth's `stat` counts
  *top-level* cells only, so a lever inside a submodule reads as exactly
  zero — which looks like a clean "no regression" and is not.
- **The SV defaults are not the ship shape.** `milan_datapath` defaults
  `N_STREAMS = 1`, which constant-folds the NxN engines away; measuring
  there reads as a free win. Use `OOC_CHPARAM`, or force the parameter
  defaults in a scratch copy of `hdl/` when `chparam` cannot re-elaborate
  the `sv2v` output (it cannot, for the interface-carrying tops).

**These are estimates, not Artix LUT6 counts.** The yosys→Vivado LUT ratio
measured against this tree's own two Vivado anchors is **0.31 … 0.71** —
see [the area budget](../../docs/design/AREA_BUDGET.md). Quote a
band, never a single figure, and never call an `ooc.sh` number a placement
result. **Flip-flops are the exception**: they convert one-for-one (the
`KL_pcm_lpf` row is 756 FF in both toolchains), which makes an FF count the
best available sanity check on an estimate.

**Run the hierarchical instrument too, and say so when they disagree.** The
same sources with **no** `-flatten` and `stat -top <mod>` sum each submodule
into its parent: no cross-boundary optimisation, so absolute numbers are
high, but the hierarchy survives and per-block attribution is possible
(`abc` renames every cell in a flattened netlist, so nothing there can be
traced back). The two instruments agreed within 11 % on the 2026-07-27 logic
levers and disagreed 8× on the LPF prune; the hierarchical one was believed,
because it reproduces the place report's FF and DSP columns exactly. When
they disagree, prefer the instrument that reproduces a known Vivado row.

### `-flatten` has a THIRD trap: it can read a real prune as zero

Measuring the 2026-07-27 optional-block prunes
([AREA_BUDGET](../../docs/design/AREA_BUDGET.md)) found a case where
`-flatten` is not merely noisy but **wrong**. Removing `rx_mac_filter` +
`tcam` from `milan_datapath` reads as **−1 LUT / −0 FF** in a flattened
whole-design `stat`, and removing `KL_pcm_lpf` as **−14 LUT / −0 FF** — while
`yosys hierarchy -top milan_datapath` proves neither module is in the design
any more, and the blocks carry 1 691 and 756 flip-flops respectively. **A
flip-flop total cannot be unchanged by deleting 1 691 flip-flops**, so that
number is an artefact of whole-design flattening, not a measurement.

Rule that follows: `-flatten` is the right instrument for a **logic** lever
(rewrite a cone, keep the block), because both sides contain the same blocks
and the mapping noise is symmetric. For a **structural** lever (delete a
block), also run the hierarchy-preserving form and read the per-module `stat`
of the block you removed:

```sh
yosys -p "read_verilog dp.v; synth_xilinx -family xc7 -top milan_datapath; \
          stat -top milan_datapath"
```

If the two disagree by more than the cross-boundary slack, trust the
hierarchical one and say so. The tier-1 leaf blocks (`KL_mmcm_drp_servo`,
`KL_aaf_latency_taps`, `KL_maap`, `KL_i2s_playback`, `rx_mac_filter`, `tcam`,
`KL_pcm_lpf`) are tops in `ooc.sh`'s array for exactly this cross-check —
a standalone OOC figure is the **upper bound** for a prune, because in
context a block shares decode and constants with its neighbours.

**These are estimates, not Artix LUT6 counts.** The yosys→Vivado ratio
measured against this tree's own place report ranges 0.25 (wide muxes,
shared serial arithmetic) to 0.86 (the whole flattened datapath) — see
[the area budget](../../docs/design/AREA_BUDGET.md). Quote a band, never a single figure, and
never call an `ooc.sh` number a placement result.
**Control sets are NOT measurable here.** A yosys proxy was tried and
discarded: counting `(clock, enable, set/reset)` triples over the `FD*` cells
of the flattened netlist reports **18 691** sets for `milan_datapath`'s
24 002 flops, against Vivado's **1 612** for the whole 56 k-flop design —
yosys keeps a private enable net per flop and never merges them the way
Vivado's `opt_design` does, so the proxy is ~12x wrong and its *delta* is
meaningless too. Use the build's own `report_control_sets` output
(`<board>_control_sets.rpt`), whose summary line
"Unused register locations in slices containing registers" is the actual
packing loss.
