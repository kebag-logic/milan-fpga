# Profiling on the Milan board — method, and the misaligned-usercopy case study

*2026-07-10. How `perf` runs on this SoC, how kernel addresses get symbolized without
kallsyms, and — as a worked example — the exact chain of evidence that led from "RX is
CPU-bound" to "83 % of the app hart is one misaligned copy loop", including how each
conclusion was checked.*

## 1. What profiling this board can and cannot do

- **perf itself is cross-built** from the kernel tree
  (`br-milan-output/build/linux-7.0.11/tools/perf`), served from the peer
  (`wget peer:8000/perf`), static, ~4 MB.
- **Sampling is timer-based only.** The SBI PMU exposes counters but the `sscof`
  extension is absent, so hardware-event *sampling* (cache-miss sampling, precise IP)
  is unavailable: `perf record -F <hz>` interrupts on the timer and records the
  interrupted PC. Practical rates: 250–300 Hz (higher adds overhead on a 100 MHz
  core; 250 Hz × 2 harts × 12 s ≈ 3 000 samples/hart, plenty for a >5 % signal).
- **No kallsyms** (`CONFIG_KALLSYMS` is off to fit the kernel in the QSPI slot), so
  every kernel sample prints as `[k] 0xffffffff8....` — a raw address. Symbolization
  happens **offline on the host** (§3).
- **No call graphs worth trusting**: `-g` needs frame pointers (userland is built
  `-O2` without them; kernel likewise) — use flat profiles and read *loops* out of
  address clusters instead (§4).
- Console discipline: `dmesg -n 1` first (printk floods the 115200 UART otherwise);
  perf writes its data file to `/tmp`, reports are generated on the board
  (`perf report --stdio`) and only the text is pulled over the console.

## 2. Measurement protocol (what was actually run)

```sh
# workload: steady-state receive, 8 flows (past slow-start — short cells lie;
# the peer-side tx_bytes time-series is the sustain metric, see the analysis doc)
for i in 1..8: recv_spin 192.168.127.2 5202 4400$i 25 0 &
sleep 3                                    # skip the slow-start transient
perf record -a -F 250 -o /tmp/p8.data -- sleep 12
```

Then **two reports, one per hart**:

```sh
perf report -i /tmp/p8.data --stdio -C 0   # cpu0 = the softirq/NAPI hart
perf report -i /tmp/p8.data --stdio -C 1   # cpu1 = where the apps mostly land
```

The per-hart split *is* the decomposition: on this system the single IRQ line pins
all NAPI/GRO/TCP-rcv softirq work to cpu0, while the `recv()` syscall work (the
copy) runs on whichever hart the app occupies. Comparing the two columns separates
"stack cost" from "delivery-to-app cost" with no extra tooling. A `/proc/stat`
snapshot pair (1 s apart) cross-checks the split: cpu0 was ~100 % softirq,
cpu1 ~100 % `sys` — consistent with the sample distribution.

One more attribution detail: a sample line like

```
17.48%  recv_spin  [unknown]  [k] 0xffffffff805d9eb8
```

reads as *kernel* code (`[k]`) executed **in `recv_spin`'s context** — i.e. inside
its `recv()` syscall — not softirq work. That distinction (process-attributed kernel
samples vs `swapper`/softirq-attributed ones) is what proves the hot loop belongs to
the app's copy path rather than to NAPI.

## 3. Symbolizing without kallsyms

`System.map` from the host kernel build holds every text symbol. The helper
(`scratchpad/symbolize.py`) does a classic nearest-preceding-symbol resolve:

1. parse `System.map`, keep `t/T/w/W` symbols, sort by address;
2. for each perf line `PCT ... [k] 0xADDR`, `bisect` the sorted list to find the
   greatest symbol ≤ ADDR, emit `name+offset`;
3. **sum percentages per symbol** (a hot loop shows up as many distinct PCs — the
   aggregation is what turns "eight 5–17 % lines" into "one 83 % function").

Caveat that makes this valid: the kernel is not relocatable here (no KASLR on this
config), so `System.map` addresses equal runtime addresses. If that ever changes,
one anchor symbol printed at boot re-bases the map.

## 4. Reading the raw histogram *before* symbols: address-cluster shape

The unsymbolized cpu1 report already told most of the story:

```
17.5%  [k] 0xffffffff805d9eb8      12.7%  [k] 0xffffffff805d9ec8
15.7%  [k] 0xffffffff805d9ec4      11.0%  [k] 0xffffffff805d9ec0
10.7%  [k] 0xffffffff805d9eb4       5.7%  [k] 0xffffffff805d9eb0
 5.2%  [k] 0xffffffff805d9ecc       4.6%  [k] 0xffffffff805d9ebc
```

Eight PCs, **consecutive, 4 bytes apart** (RV64 uncompressed instructions), jointly
~83 %. That shape is the signature of a *single tight loop of ~8 instructions*
absorbing the hart — before knowing its name. Timer-sampling skid smears a sample by
an instruction or two, but a 32-byte-wide cluster is far bigger than the skid, so
the identification is robust. (This shape-reading matters on this board because
call graphs are unavailable — the "why is this hot" step has to come from the
disassembly instead of a stack.)

## 5. From symbol to *which loop*: disassemble the exact PCs

Symbolization gave `fallback_scalar_usercopy_sum_enabled +0xa8..+0xcc`. The name
alone ("fallback", "scalar") is suggestive but not evidence. The evidence step:

```sh
riscv64-...-objdump -d vmlinux \
    --start-address=0xffffffff805d9e00 --stop-address=0xffffffff805d9ef0
```

The function contains **three** copy loops:

| PC range | loop | cost per 8 B |
|---|---|---|
| +0x3c..+0x84 | fast path: 8×`ld` + 8×`sd`, 64 B/iteration | ≈ 1.06 mem-ops + amortized bookkeeping |
| **+0xa8..+0xcc** | **misaligned shift-merge: `ld; srl; ld; sll; or; sd`** | **1 ld + 1 sd + 3 ALU + bookkeeping ≈ 5 ops** |
| +0xd0..+0xe8 | byte tail: `lb/sb` | 16 ops (tails only) |

Every hot sample lands in the middle loop and none in the fast path ⇒ **the bulk
copies run the misaligned-source path**. That is a statement read directly off the
PCs, not inferred.

## 6. Drawing the conclusions (each with its check)

1. **"The app hart is ~83 % copy loop."** Direct: sum of the cluster's percentages
   on `-C 1`. Cross-check: cpu1 was 100 % `sys` in /proc/stat, and the workload rate
   (334 Mbit ≈ 42 MB/s) × the loop's ~5 ops/8 B ≈ matches a saturated 100 MHz hart.
2. **"The copies are misaligned."** Direct: the samples sit in the shift-merge loop,
   which the routine only enters when source and destination are not co-aligned
   modulo 8. Cross-check by arithmetic: mapbench measured 26.3 µs/4 KB (~0.64 cy/B);
   the shift-merge op count predicts ~2–3× the aligned loop's cost — consistent.
   (The earlier campaign number "copy = 0.64 cy/B" was therefore a *misaligned*
   figure, and the budget table in GIGABIT_HEADROOM_ANALYSIS was corrected.)
3. **"Why misaligned": reasoned from the data layout, then checked for
   self-consistency.** The RX buffer is page-aligned and the frame lands at +0, so
   the payload begins at +54 (doff=5) or +66 (doff=8) — neither ≡ 0 (mod 8). The
   driver's copybreak linear chunk contains the header, so after the linear copy the
   destination pointer is offset by a non-8-multiple relative to the frag source.
   From then on it *never recovers*: per-aggregate payloads are n×1448 and
   1448 ≡ 0 (mod 8), so the misalignment is persistent, matching the observation
   that essentially *all* bulk samples (not a fraction) are in the slow loop.
4. **Falsifiable prediction (the test that makes this science, pending the hsq2
   boot):** with header-split the payload starts at page offset 0 and stays
   8-aligned ⇒ the same profile must show the fast unrolled loop (or, with
   `tcp_zerocopy_receive`, almost no copy loop at all). If the hs-mode profile still
   shows the shift-merge loop, conclusion 3 is wrong.

## 7. Pitfalls log (things that bit, so they're written down)

- Piping a long profiler/flasher through `head` sends SIGPIPE and kills it mid-run —
  redirect to a file, `head` the file.
- `perf record` while probe counters are in reset: the MilanDebug `reset` CSR at
  `0xf0004000` is **level-held** — write it back to 0 or every probe reads zero.
- Short-cell throughput numbers lie (slow-start credit); pair every profile with the
  peer-side `tx_bytes` time-series at steady state.
- The first profile attempt showed "60 % in recv_spin [k] 0x…" and was nearly
  misread as "the app is slow" — the `[k]` marks kernel-in-syscall-context; the
  app's own userspace code was negligible.
