# Bare-metal AX7101 firmware profile

The shipping AX7101 profile uses one RV32I VexiiRiscv hart in machine mode,
with no supervisor mode, MMU, Linux, FPU, L1 cache, L2 cache or LiteX SDRAM
cache. It explicitly enables the fabric gPTP plane bought by #114; the RTL
parameter still defaults off so other configurations do not change shape by
accident. Linux remains a supported bring-up profile for the Arty and AX7101
8x8 configurations.

The capability rows on this page are checked against the
[Milan feature status ledger](../reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `soc.baremetal-profile` | `implemented` | - |
| `host.sound-card-option` | `implemented` | - |
<!-- milan-feature-status:end -->

## Contents

- **[Build contract](#build-contract)** — The checked shipping shape, its cacheless one-hart RV32I invariants, the 50 MHz Milan/CPU clock boundary and the configuration-owned gPTP ROM.
- **[Boot and AEM image](#boot-and-aem-image)** — The raw QSPI descriptor-image slot and the identity, copy and CRC checks that must pass before the protocol processor and ADP are enabled.
- **[Fabric gPTP option](#fabric-gptp-option)** — How the shipping YAML opts into the fabric plane without changing the RTL default or taking #116's software-retirement work.
- **[UART commands](#uart-commands)** — The status, TAI set/get and explicit UTC conversion commands, followed by the non-disruptive host smoke invocation.
- **[Optional Linux sound-card surface](#optional-linux-sound-card-surface)** — What the shipping build removes with `sound_card: false`, what audio fabric remains, and how retained Linux bring-up builds opt back in.
- **[Verification gates](#verification-gates)** — The mandatory local bar, complete three-directive Vivado cell, timing-clean winner and measured resource buy-back that fund the fabric gPTP plane.

## Build contract

The authoritative product shape is
[`configs/endstation_ax7101_1x1_tdm8.yaml`](../../configs/endstation_ax7101_1x1_tdm8.yaml).
The builder and `milan_soc.py` both reject a bare-metal profile unless all of
these statements hold:

- CPU is VexiiRiscv, XLEN is 32, and `cpu_count` is one.
- `l2_bytes` is zero, no FPU is selected, and no cache or prefetch Scala
  arguments are present.
- `flashboot` is `baremetal` or `none`; the `baremetal` manifest cannot be
  selected under the Linux profile.
- The Vexii netlist ISA is RV32I plus `zicsr` and `zifencei`. Machine mode is
  the only privilege level and the CPU has no MMU.
- The cacheless CPU side and the 64-bit Milan plane run at 50 MHz. Vexii's
  supported decoupled-clock boundary crosses CPU traffic back into the 100 MHz
  LiteX system fabric; the system/audio clock recipe therefore stays unchanged.
- `board.features.fabric_gptp` is true and a `gptp:` section is present. The
  builder emits `--fabric-gptp` and generates `gptp_ucode.hex` from that same
  configuration's station MAC, priority1 and 50 MHz Milan clock.

Build through the checked configuration entry point:

```console
sw/litex/build.sh ax7101
```

For an elaboration-only check, first generate the configuration artifacts,
then pass the emitted `soc_params.json` arguments to `milan_soc.py` without
`--build`. `sw/builder/test_builder.py` checks the generated command against
the named build and sweep recipes.

## Boot and AEM image

Firmware is linked into the LiteX ROM. The only mutable boot artifact is the
builder-generated protocol-processor entity image:

| QSPI slot | Offset | Budget | Format | Consumer |
|---|---:|---:|---|---|
| bitstream | `0x000000` | 4 MiB | raw FPGA configuration | FPGA configuration logic |
| AEM image | `0x400000` | 64 KiB | raw `aem_desc.bin` beginning with `AEMI` | bare-metal firmware |

`deploy.sh flash-images` writes the AEM image raw. It must not receive a
LiteX FBI header. At build time the firmware receives the image length, CRC32
and DRAM destination as generated constants. The PHC is enabled by the CSR
reset and the option-on fabric gPTP plane starts independently of the AVDECC
AEM image. Firmware therefore does not gate either one on AEM verification.
It performs this order:

1. Keep ADP and the protocol processor disabled while the PHC and fabric gPTP
   plane remain active.
2. Program the generated entity ID, model ID, station MAC, SR VID, stream
   counts, lwSRP policy, MAAP count and CRF/AAF controls.
3. Copy the raw AEM image from QSPI to the protocol processor's paired DRAM
   window and verify its CRC32.
4. Enable the protocol processor and then the ADP entity only after the
   identity check and AEM verification succeed.

A missing or corrupt image leaves the AVDECC entity disabled while the PHC and
fabric gPTP plane continue independently. The UART status line then reports
`AEM=disabled`; it is not treated as a quiet healthy boot.

### Editing contract for this firmware

Gate 1b in `sw/builder/test_builder.py` checks the shipped boot-order spelling
and rejects the mutation classes listed below. It proves the enumerated
address, reset, placement, live gPTP wiring and build-plan facts; it does
**not** prove the semantic C control/data-flow property, and the known escapes
below still report `ALL GATES PASS`. The constraints apply to
`sw/firmware/milan_baremetal/milan_baremetal.c` and
`sw/firmware/milan_baremetal/Makefile`, plus the named CSR and datapath
integration expressions. The CSR Verilator harness separately drives
`PTP_CTRL` and `ADP_CTRL` through all four combinations and observes
`o_ptp_enable`, so the direct PHC ownership claim is behavioral as well as
structural. The gate prints both its checked facts and open limits at run time;
neither this page nor the gate output may claim more than those measured facts.

One constraint is answered by a tool rather than by reading text:

- **The Makefile must build one object from one source.** The gate asks
  `make -Bn` what it would do rather than parsing the file, so every make
  assignment flavour is covered, and it pins the SET of commands make would
  run rather than scanning them for dangerous flags. That is why an injection
  spelled `-Wp,-include,hdr`, `@response.file` or `-iwithprefixbefore` is
  refused without any of them being named, and it is also why a benign
  `AR += v` is refused: the rule has no list, so it has nothing to fall
  behind and no way to make an exception.

A second tool check runs alongside the text rules, and it is an **addition**
rather than a replacement. Where an RV32 cross compiler is available, the gate
compiles the firmware and requires that no function except `milan_reg()`
materialises an address inside the Milan CSR window; where one is not, it
stands down and says so in its printed verdict. A deterministic host-only
self-test supplies a compiler selection that is known not to be RV32, makes
any attempted compile fail, and checks that the same observed no-run verdict
produces the printed `STOOD DOWN` claim.

**What this gate does not prove.** The CRC check has a measured control-flow
escape. Gate 1b finds the `crc32()` assignment and mismatch block and requires
every non-zero return to appear later in the same preprocessor arm. Those are
textual placement facts, not dominance. This warning-clean edit passes both
the base and current gate while skipping the assignment and comparison:

```c
goto crc_ok;
got = crc32((const unsigned char *)MILAN_AEM_DESC_BASE,
            MILAN_AEM_IMAGE_BYTES);
if (got != MILAN_AEM_IMAGE_CRC32) {
        ...
        return 0;
}
crc_ok:
return 1;
```

The assignment and mismatch block still exist textually and the non-zero
return is later in the same arm. Gate 1b builds no CFG, so none of those facts
proves the CRC decision executed. A structured `do`/`break` bypass has the same
effect without `goto`, so another keyword refusal is not a proof. The
verifier/control-flow half of the replacement is tracked on #153.

The source store instrument has an uncovered class. The cast set only
recognises a cast whose text contains a `*`, and the store set only recognises
a left-hand side that starts with `*` or is `name[...]`. A cast with no `*`
combined with a `->` or subscript store is therefore outside the source
instrument:

```c
typedef struct { volatile uint32_t ctrl; } *milan_adp_blk;
...
((milan_adp_blk)0x90000600u)->ctrl = 1u;      /* ADP_CTRL[0], pre-AEM */
```

That is a durable pre-AEM entity advertise. When an RV32 cross compiler is
available, the compiled census sees the materialised CSR address and rejects
the edit. When the compiled census stands down for want of that compiler, the
edit is outside both active instruments and the gate reports `ALL GATES PASS`.
Closing the property on every supported runner still requires #153 and #162
together. #153 owns the verifier/control-flow proof and the
`entity_advertise()` choke point; #162 owns a census that resolves CSR store
targets by value rather than matching printed literals. The choke point alone
does not close paged-base `->` or subscript stores, and value resolution alone
does not prove CRC success was reached. Neither issue alone is a replacement.

**And a second blind spot, on the Makefile side, from the same cause one step
over.** The recipe pin reads what `make -Bn` PRINTS, which is text make has
already expanded. A name this Makefile references but nothing defines expands
to nothing, so the pinned commands come out byte-identical and the environment
decides what the compiler actually gets:

```make
CFLAGS += $(MILAN_EXTRA_CFLAGS)
```

```
$ make -Bn                                            # what the gate sees
... -c __BASE_CFLAGS__ -I__BIOS__ <src>/milan_baremetal.c -o milan_baremetal.o
$ MILAN_EXTRA_CFLAGS='-include ../shadow.h' make -Bn  # what a real build runs
... -c __BASE_CFLAGS__ -I__BIOS__ -include ../shadow.h <src>/... -o ...
```

The gate's hostile double-run does not see it either: it perturbs three fixed
names, and an assignment that defers to a fourth is invisible to it.
`CFLAGS += $(EXTRA_CFLAGS)` is an ordinary idiom, not a contrivance.

The class is worth stating because it is the same mechanism that stopped the
compiled census from replacing the text rules: **an instrument that reads a
RESULT cannot see what an undefined name would have contributed.** Reading the
Makefile's own TEXT saw `$(MILAN_EXTRA_CFLAGS)` and refused it; reading make's
result sees an empty expansion and has nothing to refuse.

The fix is derivable and is tracked rather than implemented here: probe
`$(origin NAME)` for every name the Makefile references and refuse
`undefined`. Measured against this Makefile, every real name is `file` or
`default` and the escape is the only `undefined`, with one caveat for whoever
implements it: the accepted `tags:` case references `$(CTAGS)`, which is also
`undefined`, so the check has to be scoped to names that reach the pinned
recipes. See #162.

**Outside what any recipe pin can reach at all**, and recorded here rather
than turned into rules, because no pin over printed commands can see them:
`export CPATH` and `export COMPILER_PATH`, which GCC itself reads from the
environment; `SHELL := ...`, which changes what executes the printed command;
`.EXPORT_ALL_VARIABLES:`; and `$(shell ...)`, which runs at parse time, during
the gate's own plan run, before any recipe is printed.

Read the constraints below as what they are: they bound the spellings they
recognise, and they cost real edits to do it.

- **Any CSR store must go through `milan_write()`.** Only `milan_reg()` may
  use `MILAN_CSR_BASE` or a `(volatile uint32_t *)` cast. The set of pointer
  casts, the set of pointer stores and the set of inline-asm statements in the
  file are each pinned, so a fifth cast, a fifth store or a third `asm` is
  refused until it is added to the gate.

The rest are refusals, and each one costs a legitimate edit:

| Constraint | Why the gate needs it |
|---|---|
| `o_ptp_enable` is driven directly by `ptp_ctrl[0]` | PHC startup is independent of AEM/ADP; the CSR harness also proves writes to `ADP_CTRL` cannot force or gate the output |
| Fabric gPTP RX, shadow TX, `gptp_ctl_mux` and MAC-boundary arbitration handshakes are direct | checking only the shadow instance misses a downstream `tvalid && cfg_adp_enable` gate that makes the plane externally silent before AEM succeeds |
| The `MILAN_ID` local is not assigned or addressed between its CSR read and mismatch guard | otherwise an intervening `id = MILAN_ID_MAGIC` forges the verdict while preserving every ordering anchor |
| A fifth pointer cast, a fifth pointer store or a third `asm` statement | the compiled census does not cover all three, so the sets are what bound address formation |
| No multi-line `#define` anywhere in the file | the gate reads macro bodies one physical line at a time |
| No C backslash-newline anywhere in the file | translation phase 2 deletes the pair and can join tokens before an offset-preserving text census; independent space, tab, form-feed and vertical-tab mutants pin every whitespace form the recognizer accepts; a real preprocessor-token reader may retire this refusal |
| No `#ifdef`/`#if` outside `load_aem_image()` | the gate would read one arm while the compiler takes the other |
| No `#pragma`, `#line`, `#error`, `#undef` or `#include_next` | the gate has no rule for them, so it refuses rather than ignores |
| The `#include` set is exactly the eleven headers listed in the gate | a twelfth include is text in the translation unit no rule reads |
| No new file in `sw/firmware/milan_baremetal/` | a quoted include resolves against this directory first, so a file here can shadow a pinned header |
| `CFLAGS` gains only `-I$(BIOS_DIRECTORY)` | held now by the recipe pin rather than by a flag rule: the compile command is pinned whole, so any added flag changes it |
| The Makefile's `include` set is exactly its three lines | `make` can only plan fragments that exist |
| `OBJECTS` may not use `?=` | `make` treats an environment variable as defined, so `?=` lets the environment choose the object list |
| No label, `goto`, `switch`, `case` or `default` in `milan_init()` | containment inside the guard is not the same as being reached through it |
| The guarded block holds the two enables and their `printf` and nothing else | anything else in it is unclassified and something for control to be steered at |
| The address of `aem_loaded` may not be taken | a pointer would write the verdict with no assignment the gate can see |
| The RTL reset for `adp_ctrl`/`pp_ctrl_r` must be a literal with bit 0 clear | a named constant is not a value the gate can evaluate |
| `o_adp_enable`/`o_pp_enable` must be `assign <port> = <reg>[0];` | the gate censuses that exact bit |
| Renaming `load_aem_image`, `milan_init` or `configure_fabric` | the gate finds them by literal identifier; the refusal names the property and the anchor to update |
| Renaming the verdict `aem_loaded` | same, and the message says so rather than reporting a boot-order defect |
| REORDERING existing functions, with nothing added or removed | the cast and store sets are compared as ordered lists |
| A read-only `#define` accessor wrapping `milan_read()` | it hides a CSR primitive from the operand census; the macro contains no store |
| `##`, `%:` or `??` anywhere in the file | token pasting and the alternate spellings of `#` |
| FACTORING the CSR accessors, e.g. a `milan_set(offset, bits)` read-modify-write helper | the census places writes by RESOLVED address, and an `offset` parameter has none. **Remedy:** keep the call sites naming a register constant, or teach `CsrModel.address()` to follow the parameter, which is a data-flow change and belongs with #153 |
| Hoisting the enable mask to a named constant | the OR mask must be a value the gate can evaluate, so `\| MILAN_ENTITY_ENABLE` is not recognised as the enable write. **Remedy:** leave the mask a literal, or add the name to the firmware's `#define` table so `constant_value()` can resolve it |
| ANY change to the two commands `make` runs, a benign `AR += v` or `CC += -Wall` included | the recipe set is pinned rather than scanned for dangerous flag spellings, and the price of having no list is that benign changes are refused too. **Remedy:** add the changed command to `expected_recipes` in the gate and a mutation-table entry beside it |

The listed refusals bound only the spellings they recognise. The open CRC
reachability/provenance cases belong to #153; retiring the store-recognition
families also requires #162's value-resolving census. No refusal family is
deleted until the joint replacement rejects the recorded escapes by
measurement.

## Fabric gPTP option

`board.features.fabric_gptp` defaults to `false`; the shipping AX7101 YAML
sets it to `true`. An option-on build elaborates `KL_gptp_shadow` with
`GPTP_PLANE_EN_P=1` and passes an absolute path to the builder-generated
microcode image. A missing `gptp:` section is rejected instead of silently
using the generator's example identity or clock defaults.

This #120 integration does not change the RTL default or the CSR compatibility
surface. The #116 flip still owns the default-on transition and retirement of
the remaining software-era CSR/readback behavior. The bare-metal firmware
exposes explicit UART commands for setting the PHC epoch; the fabric plane
owns adjfine and adjtime in an option-on build. When an external grandmaster
is selected, that plane steps and disciplines the PHC; a free-running or
grandmaster board uses `milan_settime` or `milan_utc` to establish its TAI
epoch.

## UART commands

The LiteX BIOS console stays at 115200 baud and provides:

| Command | Effect |
|---|---|
| `milan_status` | Read the Milan CSR identity, PTP/ADP/processor controls, processor status, AEM state and current TAI nanoseconds. |
| `milan_gettime` | Snapshot and print the fabric PHC as `TAI_NS=0x...`. |
| `milan_settime <tai-seconds> [nanoseconds]` | Set the PHC from explicit TAI seconds. Overflow and nanoseconds outside `0..999999999` are refused. |
| `milan_utc <utc-seconds> <nanoseconds> <tai-minus-utc>` | Convert an explicit UTC value and TAI-UTC offset to TAI before setting the PHC. |

The firmware does not embed a leap-second table. The operator or controller
must provide the current TAI-UTC offset to `milan_utc`.

Run the post-flash test from the host connected to the console:

```console
MILAN_PROFILE=baremetal MILAN_UART=/dev/serial/by-id/<adapter> \
  scripts/hostplane_smoke.sh
```

It checks the CSR magic, paired AEM image, enable bits and PHC progression.
It does not set the clock, so a smoke run cannot disturb an established time.

## Optional Linux sound-card surface

`board.features.sound_card` defaults to `false`. When false, generation omits
the PCM DMA master, its LiteX CSR window, the device-tree PCM node, the
reserved capture ring, playback rings and host-role AEM clusters. The receive
AVTP parser/depacketizer, physical audio capture, AAF packetizer, channel maps,
loopback sources and render path remain fabric functions.

Linux bring-up configurations that need ALSA set `sound_card: true` and emit
`--sound-card`. `--aaf-playback` is valid only with that option. For a Linux
build that intentionally omits ALSA, run the existing smoke with
`SOUND_CARD=0`; the ALSA check is explicitly skipped while NIC, timestamp and
protocol-processor checks still run.

## Verification gates

Before a bitstream is accepted, run the builder tests, Verilator suites,
behavior tests, Yosys portability sweep, clean-tree documentation gates and
the three place-directive AX7101 sweep required by
[`CONTRIBUTING.md`](../../CONTRIBUTING.md). The placed-resource and timing
record below is the shipping option-on measurement; an elaboration estimate
is not accepted as a substitute.

### Placed-and-routed shipping record

The measured cell is commit `1e80a106`, configuration
`configs/endstation_ax7101_1x1_tdm8.yaml`, part `xc7a100t-fgg484-2`, Vivado
2026.1 and sweep tag `i120gptp50`. It uses 32 threads, no explicit placer seed
(the Vivado default), `AreaOptimized_high` synthesis, `ExploreArea`
optimization, `AggressiveExplore` physical optimization and routing, and the
three place directives below. The 100 MHz system/audio clocks and the 50 MHz
Milan/cacheless-CPU clock are asynchronous by construction.

| Place directive | Slice LUTs | Slice registers | BRAM tiles | DSP | Slices | WNS (ns) | TNS (ns) | WHS (ns) | Result |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `ExtraPostPlacementOpt` | 54,305 | 57,938 | 100 | 15 | 15,849 | +0.033 | 0.000 | +0.049 | timing met; bitstream |
| `AltSpreadLogic_high` | 54,299 | 57,939 | 100 | 15 | 15,850 | -0.029 | -0.289 | +0.013 | setup failed; bitstream |
| `ExtraTimingOpt` | 54,284 | 57,939 | 100 | 15 | 15,850 | -0.051 | -0.220 | +0.047 | setup failed; bitstream |

`ExtraPostPlacementOpt` is the shipping winner. Its bitstream is
`build_ax7101_eppo_i120gptp50/gateware/alinx_ax7101.bit`; the signed-off report
has zero setup and hold failing endpoints. The placed design occupies 15,849
of 15,850 slices, so the directive is part of the reproducible cell and is not
interchangeable with the two failing alternatives.

The first option-on experiment kept both the system and Milan planes at
100 MHz. It emitted bitstreams but did not meet setup timing:

| Place directive | WNS (ns) | TNS (ns) | WHS (ns) |
|---|---:|---:|---:|
| `AltSpreadLogic_high` | -3.933 | -11,973.169 | +0.036 |
| `ExtraTimingOpt` | -3.897 | -9,278.585 | +0.057 |
| `ExtraPostPlacementOpt` | -3.762 | -12,239.650 | +0.020 |

That result is why the cacheless CPU and 64-bit Milan plane run at 50 MHz;
3.2 Gb/s still exceeds the 1 Gb/s wire rate while the LiteX system and audio
recipe remain at 100 MHz.

Post-synthesis resource accounting also proves the intended buy-back. The
#114 Linux, plane-off baseline used 59,497 LUT, 63,092 registers, 126 BRAM
tiles and 15 DSP. The fabric gPTP plane in this build accounts for 3,364 LUT,
2,939 registers, 4.5 BRAM tiles and 4 DSP. Adding that plane to the old
baseline would require 62,861 LUT, 66,031 registers, 130.5 BRAM tiles and 19
DSP; the new option-on bare-metal build instead uses 57,111 LUT, 58,043
registers, 100 BRAM tiles and 15 DSP. The downgrade therefore funds the plane
and still frees 5,750 LUT, 7,988 registers, 30.5 BRAM tiles and 4 DSP relative
to that old-plus-plane comparison.
