[OBSOLETE + 2026-08-16]

# HANDOVER — 2026-07-31

Repo: `~/prjs/milan-fpga`, branch **`main-push`**, head `31861d7e`
(everything below is pushed).

---

## 0. READ THIS FIRST — WAIT FOR THE SEEDS TO LAND

**Three RV32 bitstream builds are in flight. DO NOT start any area work,
DO NOT edit `KL_aecp_response_builder.sv`, and DO NOT launch more Vivado
until they finish.** They decide whether any of the rest is needed.

```sh
pgrep -c vivado                      # 0 = they are done
```

Then read the verdict — a waiter is already writing it, or reproduce it:

```sh
for d in x32 x32alt x32ext; do
  L=<litex-work>/litex-milan/work/build_ax7101_$d/gateware/vivado.log
  printf "%-8s " "$d"
  if grep -q "write_bitstream completed" $L 2>/dev/null; then echo "CLOSED - FITS"
  else grep -oE "require [0-9]+ slices|of which [0-9]+ slices are available" $L | tail -2 | tr '\n' ' '; echo; fi
done
```

* `x32`    = ExtraPostPlacementOpt — already known: **11,339 required / 11,162 available = 177 SHORT**
* `x32alt` = AltSpreadLogic_high   — pending
* `x32ext` = ExtraTimingOpt        — pending

**If one CLOSES:** flash the ALINX (§4) — that is the whole job, the area
work in §5 is not needed.
**If all three miss:** §5 is the route, and the profile that sizes it is
already measured.

The odds are maybe one in three. At RV64 all three directives failed
*identically* at 734 short, which is a design signature. At 177 short the
margin is small enough that placer strategy can plausibly matter — that is
the entire reason these two extra seeds are running.

---

## 1. What landed today

| commit | what |
|---|---|
| `4b41f628` | **VERSION 0x0021** — the Talker TSpec now describes the frame the build emits |
| `65d60552` | torture campaign binds only the peer's **(p) primaries** |
| `a1890fd4` | **class A only** — class B `credit_based_shaper` stripped |
| `31861d7e` | `--xlen` honoured on the vexiiriscv path (it was silently ignored); `--bus-standard` added |

Gates green on the final tree: **60 suites / 2,105,158 checks / 0 failures**,
**behave 520 scenarios / 0 failed**, `test_builder.py` ALL GATES PASS.

### 0x0021, the defect it fixes
`milan_datapath`'s `tctx_chans_r` reset to `4'd2` and is only written by a
TCTX CSR window **no board software drives**, while `KL_aaf_packetizer` reset
its own `chans_r` to the elaborated `WIRE_CHANS_C`. So the shipping 4-channel
Arty put a 120-octet AVTPDU on the wire and **declared 73** — 7.36 Mb/s
reserved for a stream occupying 10.368, and CBS grants credit against the
declaration. Talker 0 hid it (the fabric mux starts at `s=1`). Reset now
derives from `TALKER_WIRE_CHANS_P`. Bite-proven: restoring `4'd2` reddens
exactly one check (`got=0x49 exp=0x79`).

---

## 2. Board state

| | Arty | ALINX (AX7101) |
|---|---|---|
| gateware | **0x0021 — verified on silicon** | 0x0016 (nothing newer fits yet) |
| reach | `ssh <peer-host>` then `ssh -i ~/.ssh/id_rsa root@<bench-net>.3` | same, `…@<bench-net>.1` |
| console | `/dev/ttyUSB4` @115200 | `/dev/ttyUSB0` (CP2102) |
| power | **USB — restarts under load** | strip **OUT0** (`ssh <power-controller> 'powerstrip toggle 0'`) |
| software | current | **updated today** — `gptp2csr.sh` 3,589 → 16,054 B |

**SSH traps.** `id_ed25519` is rejected — the board takes **`id_rsa`**, which
lives on `<peer-host>`, not the dev box. `scp` needs **`-O`** (dropbear has no
SFTP). `pkill` does not exist on the busybox rootfs — kill by PID.

**Console trap.** The FTDI buffer holds stale bytes: opening the port replays
an OLD boot log. **Drain it first** (`timeout 8 cat /dev/ttyUSB4 >/dev/null`)
or you will diagnose a boot loop that is not happening. This cost three
reversed verdicts today.

**Arty needs the barrel jack.** It restarts periodically under campaign load —
confirmed live on a drained console, present on 0x0020 *and* 0x0021 so it is
not the gateware. 84.9% LUT + DDR3 + PHY on a 2.5 W USB port. Moving it to the
barrel supply likely fixes it AND puts it on the switched strip, giving a
scriptable cold cycle. **USB port-power is a dead end** — `usb1-port6/disable`
genuinely cuts VBUS but re-enabling never restores it on this VM's xHCI root
hub; only an `xhci_hcd` rebind recovers, and that bounces every device.

---

## 3. The area problem — everything measured

Need **734 slices** at RV64, **177** at RV32. LUT-bound: LUTs 99.2%, FFs
44.7%, BRAM 78.9%. *Trading LUTs for FFs or BRAM is a win.*

```
RV64 m0021b : 11,709 req / 10,975 avail = 734 short | 62,902 LUT | 2,057 csets
RV32 x32    : 11,339 req / 11,162 avail = 177 short | 61,006 LUT | 2,052 csets
              -370 required, +187 available -> 557 slices recovered | -1,896 LUT
```

### Levers CLOSED — do not re-propose
| lever | measured |
|---|---|
| L2 16K→8K | **+7 slices (worse)** — array is BRAM, controller is fixed-cost |
| CBS sequential engine | dead — only **2** CBS instances ever existed |
| control-set reduction | cannot help — FFs at 44.7% while LUTs are the wall |
| bus unification → AXI | **~520 LUT ceiling** — there is no 11K of removable glue |
| tier-1 prunes | already applied in the shipping ax7101 OPTS |
| tier-2 shape-scaling | no-op at 8×8 (those blocks scale WITH the shape) |
| class B CBS strip | −53 slices (landed) |
| smaller CPU / Zephyr | oversized *and* deletes Linux — RV32 gets the win without it |

### CPU, OOC-measured (not the in-context figures)
```
VexiiRiscv RV64   10,376 LUT   12,927 FF   16 DSP     core 6,384 (62%) | L2 1,860 (18%) | ALL glue 2,132 (21%)
VexiiRiscv RV32    8,726 LUT   11,428 FF    4 DSP
```
The in-context report says 17,244 — **1.66× inflated**. The 7,578-LUT "parent
own-logic" row is **243 LUT** OOC; it is a flattening artifact, not glue.

---

## 4. If a seed CLOSED — flashing the ALINX

**The ALINX must run the latest (USER).** It is on 0x0016, missing everything
from 0x0017–0x0021, which is why the campaign shows 28 `mandatory-mask` fails.

```sh
AX_FTDI=210512180081 ./sw/litex/build.sh flash ax7101:<builddir>
```
(the AX is the **ft232H** `210512180081`; the FTDI2232 `210319AFEED0` is the Arty)

**FULL IMAGE SET REQUIRED, not just the bitstream.** The board runs **1 RX
queue** and the new build is 2 — that shifts every DMA window under an
unchanged DTB. Needs `KERNEL`/`DTB`/`OPENSBI`/`ROOTFS` env vars.
`deploy.sh` gates this with `check_dtb_csr.py` and will refuse a mismatch.

**OpenSBI embeds the FDT** ("the BIOS jumps a1=0, so the fdt embedded in
opensbi is the only tree the kernel sees") — so a DTB change means OpenSBI
must be **rebuilt**, not just re-flashed.

**ROOTFS:** a buildroot incremental rebuild was running against
`<buildroot-src>` (tag 2026.05) →
`<buildroot-output>` (13 GB, toolchain prebuilt). **Check it finished
and that the new `rootfs.cpio.gz` actually contains `gptp2csr.sh`** before
flashing — the old image is dated 2026-07-05 and flashing it reverts a month
of board software including the `tu=1` fix.

Then **cold-cycle via the strip** (`ssh <power-controller> 'powerstrip off 0; sleep 6; powerstrip on 0'`)
and verify `devmem 0x90000004` reads `0x00010021`.

---

## 5. If all three MISSED — the `u_bld` route

Differential profile of `KL_aecp_response_builder` (Vivado OOC, baseline
**5,062 LUT**, module is **FLAT** — 3,335 lines, one 1,890-line `always_ff`
"Main FSM" at lines 1402–3292, so `report_utilization -hierarchical` returns
one row and cannot rank cost):

```
GET_COUNTERS      579 LUT
GET_STREAM_INFO   571
READ_DESCRIPTOR   561
GET_NAME          558
GET_AUDIO_MAP      14   <-- THE EXEMPLAR
```

**Read this correctly.** The four at ~570 are *near-identical*, which means
they **share** the reply-assembly path — stubbing any one collapses the same
structure. **The costs are NOT additive**: you will not get 2,269 by removing
all four. Expect more than 570 and less than 2,269.

**`GET_AUDIO_MAP` at 14 LUT is the whole argument.** The 0x001C dynamic-mapping
round already replaced its inline assembly with a backing store, and it costs
**40× less** than its siblings — in the same module. Converting the other four
the same way is *following a pattern that already ships*, not inventing one.
Target: one narrow byte-emit path driven by a per-command
`{offset, length, source}` descriptor.

**Risk:** +1 read latency per memory conversion. Precedent — `KL_crf_rx`
moving `rate_o` a clock later had to be pinned by a suite check first.
**This module is what Hive enumerates**: a response builder that synthesises
smaller but answers one descriptor wrong is worse than not fitting.

### Reproducing the profile
Scratch rig at `…/scratchpad/prof/` (`prof.tcl` + `sweep.sh`). Method: copy the
tree, make a command's opcode unreachable in a **scratch** `aecp_pkg.sv`
(`CMD_GET_COUNTERS 15'd41 -> 15'd32700`), re-synth OOC, diff against 5,062.
**Parse `^PROF`, NOT `Slice LUTs`** — Vivado echoes the tcl source line
containing that string *before* the result, and `grep -m1` grabs the echo.
That bug ate three attempts today; the data was intact every time.

---

## 6. Open items

| # | item |
|---|---|
| **49** | **GM clockIdentity latched 32 bits at a time** (USER root-cause) — [`milan_csr.sv:2326`](../../hdl/common/csr/milan_csr.sv#L2326) is a bare `{hi,lo}` concat, no commit strobe. TWO consumers act on the torn value: ``adp_advertiser.sv:420`` (spurious ADP GM_CHANGE **on the wire**) and ``KL_aecp_response_builder.sv:2426-2441`` (spurious AVB_INTERFACE counter push). **12** such concatenations exist; `o_ptp_tod_wr`/`o_ptp_offset` are the next most worrying. USER: after the audio checks. |
| **50** | **STREAM_OUTPUT unsolicited GET_COUNTERS never fire** (USER-reported) — `unsol_pend2_r` has exactly one trigger, `in0_cnt_dirty_p_i`, the STREAM_INPUT **index-0** pulse. No talker-side dirty source exists at all; listeners 1..N-1 are also dark. Needs a per-descriptor dirty vector + per-descriptor rate limiter. |
| **51** | area — see §3/§5 |
| **52** | option C (`u_bld` trim) — see §5 |
| **53** | LOCK_ENTITY/ACQUIRE_ENTITY bound descriptor **type** but not **index**. Narrowed from a hermes fuzz gap (their "any descriptor" is refuted — there IS a type bound at line 386). `w_b16`/`w_b17` are **not wired**, so it is not a one-liner, and the payload offset must be read from 1722.1 7.4.2/7.4.3 — do not infer it. |
| 37 | listener Table 5.6 per-frame vs per-interval — the validated peer also counts per-frame (measured: 72,343 ticks in a 4 s window) |
| 21 | the peer never sends Listener Ready — confirmed **not** a gPTP problem (licence stayed shut with a healthy clock) |

### Campaign harness defect worth fixing
`xside.unlicensed-silent-everywhere` FAILs on the **test host's own AVDECC
control traffic** when both device sides are unreadable. On the ALINX run it
fired 180 times while `instrument.test-machine-lossless` fired 171 — i.e. a
lossy instrument manufacturing DUT failures. It should SKIP when no device
side is readable. Of 407 FAILs, only **45** were the ALINX, and 28 of those
are features that postdate its 0x0016 image.

---

## 7. Method notes — these were expensive

* **In-context utilisation reports are inflated**, block-dependently: 1.33× for
  `u_bld`, 1.48× for `KL_aecp_top`, **1.66×** for the CPU. yosys is worse (2×
  for one block). **Only believe Vivado OOC numbers you produce yourself.**
* **Slice demand is not LUT/4.** Class B freed 461 LUT; I predicted ~104 slices
  and got **53**.
* **Never mirror a constant.** The 805-slice figure paired m0021b's
  slices-*required* with m0021's slices-*available*; the real number is **734**.
  The project's own `derive-never-mirror-constants` note covers exactly this.
* **Write raw tool reports to disk and parse afterwards.** Inline pipes into
  `awk`/`grep -m1` destroyed two profile runs.
* **Search by signature before declaring absence.** I reported "no buildroot
  source on this box" from a `-maxdepth 2` search; it was at depth 3, plus a
  13 GB prebuilt output tree named `br-milan-output`.
* **Verify a launch actually carries the flag you meant.** A "`rv32` sweep"
  ran with `--xlen=64` because `sweep.sh` has no `--xlen`; and `pkill -f` did
  not match Vivado (the output dir is not in its argv — kill by
  `/proc/<pid>/cwd` instead).

Corrections to `<worktree>/RESOURCE_PLAN.md` are in its §7
(shortfall 734 not 805, CPU row reopened at RV32, tier-1 already spent,
tier-2 a no-op at 8×8, yosys calibration is block-dependent).
