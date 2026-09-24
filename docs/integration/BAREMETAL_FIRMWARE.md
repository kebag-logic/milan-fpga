# Bare-metal AX7101 firmware profile

The shipping AX7101 profile uses one RV32I VexiiRiscv hart in machine mode,
with no supervisor mode, MMU, operating system, FPU, L1 cache, L2 cache or LiteX SDRAM
cache. It uses the fabric gPTP plane bought by #114, now the product and RTL
default. Product manifests are limited to `baremetal` and `none`, and every
product configuration requires the fabric gPTP owner. An option-off
elaboration exists only as verification-only hardware with zero gPTP owners.

The capability rows on this page are checked against the
[Milan feature status ledger](../reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `soc.baremetal-profile` | `implemented` | - |
| `gptp.fabric-product-owner` | `implemented` | - |
<!-- milan-feature-status:end -->

## Contents

- **[Build contract](#build-contract)** — The checked shipping shape, its cacheless one-hart RV32I invariants, the 50 MHz Milan/CPU clock boundary and the configuration-owned gPTP ROM.
- **[Boot and AEM image](#boot-and-aem-image)** — The raw QSPI descriptor-image slot and the identity, copy and CRC checks that must pass before either compatibility enable bit may activate the shared AVDECC control plane.
- **[Saved state: the flash writer](#saved-state-the-flash-writer)** — The boot validation of the two journal slots, the staged KLJ2 container and the control tuple, the heartbeat and debounced A/B commit, and the host model that grades all of it per shape.
- **[Fabric gPTP option](#fabric-gptp-option)** — The default fabric owner, generated microcode, and the ownerless verification-only option-off elaboration.
- **[UART commands](#uart-commands)** — The status, TAI set/get, explicit UTC conversion and saved-state slot commands, followed by the non-disruptive bench smoke invocation.
- **[Verification gates](#verification-gates)** — The mandatory local bar, complete three-directive Vivado cell, timing-clean winner and measured resource buy-back that fund the fabric gPTP plane.

## Build contract

The authoritative product shape is
[`configs/endstation_ax7101_1x1_tdm8.yaml`](../../configs/endstation_ax7101_1x1_tdm8.yaml).
The builder and `milan_soc.py` both reject a bare-metal profile unless all of
these statements hold:

- CPU is VexiiRiscv, XLEN is 32, and `cpu_count` is one.
- `l2_bytes` is zero, no FPU is selected, and no cache or prefetch Scala
  arguments are present.
- `flashboot` is `baremetal` or `none`; these are the only accepted product
  manifests.
- The Vexii netlist ISA is RV32I plus `zicsr` and `zifencei`. Machine mode is
  the only privilege level and the CPU has no MMU.
- The cacheless CPU side and the 64-bit Milan plane run at 50 MHz. Vexii's
  decoupled-clock option crosses the CPU's peripheral bridge and DMA slave
  back into the 100 MHz LiteX system fabric; its memory master stays on the
  CPU clock, and `sw/litex/milan_soc.py` crosses that port before LiteDRAM
  sees it (`cross_cpu_memory_ports`, #359: without it the first DRAM access
  after the BIOS handed the DFI back never completed and no persistent boot
  reached the firmware). The system/audio clock recipe therefore stays
  unchanged.
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
| journal slot A | `0xEE0000` | 64 KiB | KLJ2 saved-state container, raw | bare-metal firmware, read and written |
| journal slot B | `0xEF0000` | 64 KiB | KLJ2 saved-state container, raw | bare-metal firmware, read and written |

`deploy.sh flash-pair` writes the AEM image raw as the non-bit member of a
proved transition; it must not receive a LiteX FBI header. The one supported
transition is a fabric-baremetal refresh: the target AEM image verifies
first and the target bit commits last, so the old autonomous fabric owner
stays live at every incomplete prefix. Layouts naming a retired boot image
(#259) or a non-fabric owner are refused
before any programmer I/O. At build time the firmware receives the image
length, CRC32 and DRAM destination as generated constants. The PHC is enabled by the CSR reset and the
option-on fabric gPTP plane starts independently of the AVDECC AEM image.
Firmware therefore does not gate either one on AEM verification. It performs
this order:

1. Keep both compatibility enable bits clear, leaving the shared AVDECC
   control plane disabled while the PHC and fabric gPTP plane remain active.
2. Program the generated entity ID, model ID, station MAC, SR VID, stream
   counts, lwSRP policy, MAAP count and CRF/AAF controls.
3. Validate the two journal slots, stage the newer accepted saved-state
   container in the reserved window (or an all-erased one when neither slot
   is accepted), hand the backing store its control tuple and run the
   restore walk; see [Saved state](#saved-state-the-flash-writer) below.
4. Copy the raw AEM image from QSPI to the protocol processor's paired DRAM
   window and verify its CRC32.
5. After the identity check and AEM verification succeed, set the
   `PP_CTRL[0]` and legacy `ADP_CTRL[0]` compatibility enable bits. The
   controls are ORed into one shared control-plane enable, so either bit alone
   enables it.

That order is the claim, so it is checked rather than asserted: the block below
is compared step by step against the call sequence `milan_init()` actually
emits, and `scripts/check_feature_status.py` fails if either side moves. Swap
two steps here, or in the firmware, and the gate names both sequences.

<!-- milan-feature-order:firmware_boot_order:start -->
1. `configure_fabric()` — the fabric CSRs, with the PHC and the gPTP plane
   already live from the CSR reset.
2. `nvm_boot()`: the saved-state slots, the backing store and the restore
   walk, before the entity model is loaded and before the entity can be
   advertised.
3. `load_aem_image()`: copy from QSPI and verify the CRC32.
4. `entity_advertise()`: the enable bits, and only on a verified image.
<!-- milan-feature-order:firmware_boot_order:end -->

Step 5 lives in one function and nowhere else:

```c
static void entity_advertise(int verified)
{
        if (!verified)
                return;
        milan_write(MILAN_PP_CTRL, milan_read(MILAN_PP_CTRL) | 1u);
        milan_write(MILAN_ADP_CTRL, milan_read(MILAN_ADP_CTRL) | 1u);
        printf(...);
}
```

`milan_init()` calls it exactly once, as `entity_advertise(aem_loaded)`. That
is the choke point issue #153 asks for, and it is what lets the boot contract
be proved by DATA FLOW rather than by refusing constructs across the file: the
question becomes "which function stores the enable bit, which edge dominates
that store, and which value that edge was handed", and all three are answered
from the compiled code. There is
no behaviour change: the same two writes, in the same order, after the same
verdict.

A choke point is only a choke point if it has ONE entrance, and proving the
inside of the function does not prove that. An earlier revision of this page
rested the claim on the dominance measurement alone, which runs
`entity_advertise()` in isolation on a synthetic argument, so this control
passed every gate that revision had:

```c
static void (*advertise_hook)(int) = entity_advertise;
...
        advertise_hook(1);            /* from the UART status handler */
```

Every enable stays inside the choke point, the local `if (!verified)` still
dominates both writes, and the one literal call site still reads
`entity_advertise(aem_loaded)` -- and after an AEM CRC failure the UART status
command advertises the entity anyway. Gate 1b now measures the ENTRANCES too,
fail-closed: the choke point may be neither exported nor address-taken, no line
of the emitted assembly may name it except its own definition and a direct
`call`, the firmware may transfer control through no register at all, exactly
one call edge may reach the choke point and it must come from `milan_init()`,
and the value that edge hands it is tracked from the `load_aem_image()` call
that produced it. A call edge the resolver cannot place, or an argument it
cannot trace back to the verifier, is a REFUSAL and never a default of
"verified".

A missing or corrupt image leaves the AVDECC entity disabled while the PHC and
fabric gPTP plane continue independently. The UART status line then reports
`AEM=disabled`; it is not treated as a quiet healthy boot.

### What step 2 writes, and who owns each word

`configure_fabric()` writes these words in this order and no others. Each
generated value is a `generated/soc.h` constant that `sw/litex/milan_soc.py`
publishes from [`sw/litex/boot_policy.py`](../../sw/litex/boot_policy.py),
which reads the builder's `aem_overlay.json` and `lwsrp_table.json` for the
config being built. Gate 35 of `sw/builder/test_builder.py` compiles this
firmware on a host against those values for every tracked config, and for the
shipping 1x1 with its CRF output off, and holds the ordered list below (#398).

| Word | Value written | Owner |
|---|---|---|
| `ADP_CTRL` (`0x600`) | read, bit 0 cleared | firmware-internal: the pre-AEM clear the entity-enable choke point relies on |
| `PP_CTRL` (`0x920`) | read, bit 0 cleared | firmware-internal, for the same reason |
| `ADP_ENTITY_ID_LO/HI` (`0x604`, `0x608`) | `MILAN_ENTITY_ID_LO/HI` | generated from `entity.entity_id`, which defaults to the EUI-64 of `platform.mac_address` |
| `ADP_MODEL_ID_LO/HI` (`0x60C`, `0x610`) | `MILAN_MODEL_ID_LO/HI` | generated from `entity.entity_model_id` and `entity.model_id_pin` |
| `MAC_ADDR_LO/HI` (`0x108`, `0x10C`) | `MILAN_STATION_MAC_LO/HI` | generated from `platform.mac_address` |
| `MAC_CTRL` (`0x100`) | read, bit 3 (all-multicast) set | pending #403, which decides the receive-filter posture |
| `AAF_CTRL` (`0x654`) | `MILAN_SR_VID` in `[27:16]`, talker enable `[0]`, bypass `[1]` clear | VID generated from `srp.vid`; the enable is firmware-internal bring-up sequencing |
| `LWSRP_VID` (`0x684`) | `MILAN_SR_VID` | generated from `srp.vid` |
| `LWSRP_CTRL` (`0x680`) | `MILAN_LWSRP_CTRL_RESET` with bits 1:0 forced on | reset word generated from `srp.*`; the forced bits override `srp.enable_at_reset` and `srp.talker_declare_at_reset`, pending #400 |
| `MAAP_CTRL` (`0x6CC`) | block count `MILAN_N_TALKERS` + 1 in `[15:8]`, enable `[0]` | count generated from the declared AAF talkers; the enable is firmware-internal bring-up sequencing |
| `CRFT_CTRL` (`0x750`) | `MILAN_CRF_TX_CTRL_BOOT` | generated from `clocking.crf_output.enabled`: `0x3`, talker enable and class-A declare, when the output is declared; `0x0` when it is not, so `CRFT_CTRL[0]` stays clear and nothing is declared |
| `ADP_ENTITY_CAPS` (`0x614`) | not written | nothing reads the word: the ADPDU carries the processor's `ADP_ENTITY_CAPS_C` (#398) |

**Both of the last two rows are statements about the WHOLE firmware now**
(#465). Gate 35 enters it through `configure_fabric()` alone, so a
`CRFT_CTRL` write anywhere else was invisible to it: both reviewers of PR
#459 planted `milan_write(MILAN_CRF_TX_CTRL, 3u)` in `entity_advertise()`
and gate 35, gate 1b and `check_baremetal_only.py --check` all stayed green.
Gate 1b's resolver now censuses both addresses across every function the
compiler emitted, off the same resolved call operands the entity-enable
census uses: exactly one write to `0x750`, from `configure_fabric()`,
carrying the generated `MILAN_CRF_TX_CTRL_BOOT`, and none at all to `0x614`.
Each plant is a permanent mutation. The hop that PUBLISHES those words --
the loops in `sw/litex/milan_soc.py` that hand `boot_policy.fabric_constants`
and `nvm_shape.firmware_constants` to `add_constant` -- has both complete
loop bodies pinned by gate 35 using Python's parsed syntax.
Each derivation must appear in exactly one matching loop.
That loop contains only the direct `soc.add_constant(_name, _value)` call.
Comments and formatting do not change this comparison.
The substituted CRF value is refused, as are subsequent overriding writes
inside either loop, including overrides of the CRF word and heartbeat wait.

Setting the entity-enable bits is step 5's alone: only the choke point above
sets them.

### Editing contract for this firmware

Gate 1b in `sw/builder/test_builder.py` checks the shipped boot-order spelling
and rejects the mutation classes listed below. It proves the enumerated
address, reset, placement, live gPTP wiring and build-plan facts by reading
text, and, on a runner carrying the RV32 cross compiler, it proves the C
control/data-flow property by RESOLVING the values in the assembly that
compiler emits (issue #153). Where the compiler is absent both the compiled
census and the resolver stand down together, the closing verdict names that
arm, and the escapes recorded below are open again on that runner. The constraints apply to
`sw/firmware/milan_baremetal/milan_baremetal.c` and
`sw/firmware/milan_baremetal/Makefile`, plus the named CSR and datapath
integration expressions. The CSR Verilator harness separately drives
`PTP_CTRL` and `ADP_CTRL` through all four combinations and observes
`o_ptp_enable`, so CSR-output PHC ownership is behavioral. The `milan_csr`
output binding and connection onward to `ptp_sync.a_enable` (the
`ptp_csr_sync` CSR crossing that, with the `ts_counter` PHC, replaced the
`ptp_ts_top` record chain removed from `milan_datapath`), plus the
enumerated gPTP handshake, clock and reset seams, are structural checks over
comment-blanked SystemVerilog. Each match must be a direct item in its inspected
generate arm, and every backtick token in both the CSR and datapath files is
closed to that file's two shipped includes and paired `default_nettype`
directives. The identity check also follows the canonical `csr_default(A_ID)`
literal through the defaults-ROM fill and the direct AXI read address. On a
runner carrying Verilator, every CSR/datapath mutation must still elaborate as
the real `milan_csr` top or option-on `milan_datapath` source closure before it
counts; without Verilator that layer explicitly stands down, is not reported
as elaborated evidence, and is registered so the suite's closing line reads
`ALL GATES PASS EXCEPT n NOT RUN` and names it. Every arm of gate 1b that can
decline is registered that way: the RTL elaboration layer, the compiled
census, and the `MAKEFLAGS += -e` entry on a make that does not re-read
MAKEFLAGS mid-parse. The last of those is not a missing tool; the construct
is present and simply has nothing to detect on that make, and its skip text
says so. The gate prints both its
checked facts and open limits at run time;
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

**The text this gate reads is the text the compiler compiles, and that is
MEASURED rather than defended by refusals** (#408). Three measurements
carry it.

**Every preprocessor conditional the pinned GCC reads is graded one arm
selection at a time.** Each conditional group is resolved to each of its arms
in turn, and to no arm where no `#else` closes it, and every resulting text is
graded by the whole gate as a firmware of its own: the text rules on every
machine, and the preprocessed-unit comparison, the compiled census and the
resolver wherever an RV32 compiler answers. Whatever the product's headers
select, the product builds one of the firmwares graded, so no arm is read in
one state and compiled in another. That includes an arm the census stub tree
drops and the product compiles, such as `if (\n#ifdef CSR_UART_BASE\n0
&&\n#endif\n!verified) return;` inside the choke point, which names nothing
this file defines and moves no boot token.

Groups that ask only whether one macro is defined (`#ifdef N`, `#ifndef N`,
`#if defined(N)` or `#if !defined(N)`, with at most an `#else`) are graded
together when the firmware neither defines nor undefines `N` and every
`#include` precedes them: each value of `N` is one build, as it is to the
preprocessor. So a debug helper defined under one `#ifdef MILAN_DEBUG_TOD`
and called under a second is graded as the two builds that exist. Any other
condition is not evaluated, so its arms are graded in every combination with
the other groups', including combinations no build selects, and a refusal
names the selection it graded rather than claiming the product builds it.

That claim holds for the conditionals the gate's readers find, and the bound
is measured rather than assumed. The gate RUNS translation phases 1 to 3 (C11
5.1.1.2) in the standard's order and as the pinned GCC 14.3 runs them at
`-std=gnu99`, once per text, and every C directive reader in gate 1b reads
the result through one anchor. Phase 1 drops a UTF-8 byte-order mark at
offset 0 and ends a line at LF, CRLF or a lone CR; it does not replace
trigraphs, since gnu99 does not. Phase 2 deletes every splice: a backslash,
any run of space, tab, form feed, vertical tab or NUL, then a line end. Phase
3 lexes what is left: a comment is whitespace, on one line or across
several; a form feed, a vertical tab or a NUL is whitespace; and `%:` and
`%:%:` are the digraphs of `#` and `##`, found by maximal munch, so `<%:` is
`<%` and `:`. The readers used to approximate those phases in an order of
their own, and twice a spelling fell between them while GCC honoured it: a
form feed before `#`, then a `%:` digraph a splice splits (`%\`, a line end,
then `:ifdef`), each hiding a product-only arm from every reader ([R272] F1
on PR #535, rounds one and two). Every span a reader finds is mapped back to
the source, so a refusal names the line the `#` is on.

Two corpora, each firmware recorded with what the pinned GCC keeps of it, are
read by the gate's readers on every run and re-measured on the compiler
wherever it answers; the two must agree. The fixed corpus holds the 78
spellings the reviews found, the byte-order mark among them ([R273] F1 on PR
#535). The generated corpus holds 4907 more, round two's split digraph among
them: a splice at every offset of each directive line in turn, at the end of
the line before it, and at every offset of the introducer on both lines at
once, crossed with every introducer (`#` or `%:`, alone or after a form feed,
a vertical tab, a NUL or blanks, and six spellings GCC does not read as one,
such as `%:%:` and `<%:`). The first template takes all ten spellings of the
splice when no blank precedes the introducer (after a space, a tab, a form
feed, a vertical tab or a NUL, CRLF and lone-CR line ends, two in a row) and
three after one; the others take three. Its templates exercise each reader: a conditional and the
`#endif` closing it, the macro name a condition reads, `#define`, `#undef`,
`#else`, `#elifdef`, `#elifndef`, and the `##` a `#define` body pastes with.
BOUNDED, and the bound is these corpora: a spelling in neither that GCC reads
differently is outside the measurement, and the readers are exact because
they run GCC's phases in GCC's order, not because every spelling has been
tried. Three lexings no edit means are refused before any reader runs, so no
reader has to guess them: a character or string literal that no quote closes
on its line (GCC ends it there with only a warning), a raw string literal (a
gnu99 extension spanning lines), and a trigraph anywhere in the file (GCC
ignores it at `-std=gnu99` and a strict `-std` translates it, so the two read
different lines around it).

Two kinds of group are left as written. A guard whose one arm holds only
`#error` emits no code in any selection. The AEM verifier's QSPI-slot group
has another arm, the build with no AEM slot. No selection compiles that arm
and the census stub tree takes the first, so it is pinned to a literal
`printf` and `return 0;`. A condition the stub tree does not satisfy would
hand the census the other arm instead; the resolver refuses that, because the
verifier it then compiles has no copy loop to place. More than 16 selections
in the whole firmware is refused rather than graded in part, and a disabled
`#if 0` block is graded as the code it would be.

**The preprocessed unit is compared against the text.** The same compiler,
under the same flags, preprocesses each graded firmware with `-E`; each of
`milan_init()`, `configure_fabric()`, `entity_advertise()` and the three CSR
accessors is compared against its body in that unit by CONTENT -- the ordered
sequence of the CSR primitives and boot steps it calls, and the number of
statements they sit in -- read both as this gate reads it and after
translation phases 1 to 3, where a splice is deleted; and no preprocessing
directive may survive into the unit at all. Those tokens are macro-invariant,
so the texts can be compared although one has its register names expanded. A
macro that erases or moves a boot step is one disagreement, reported rather
than anticipated. The comparison reads the boot tokens and not every name the
text rules in those bodies read, the CSR identity sample and the verdict
among them, so a splice or a paste rebuilding such a name would agree in both
texts. Inside the six bodies, and in every macro this file defines that they
name at any depth, the token-joining splice ban and the `##` paste ban are
therefore KEPT, and they refuse on every machine. The paste ban reads this
file's own `#define`s: a paste through a macro a header defines, such as
`__CONCAT(i, d) = MILAN_ID_MAGIC;` before the identity guard, is outside it
([R273] F2 on PR #535), accepted on dev and here, and it is the same bound as
the plain function-like macro that forges the identity sample with no paste
at all (#544). Outside those bodies what a splice or a paste builds is
compiled, and the resolved census answers it by the store it makes. The
caveat is this instrument's and
is written at its site as well as here: the unit is the one the census STUB
tree produces, so a macro whose DEFINITION differs between that tree and the
product expands to text this comparison never sees. The stub headers' values
are asserted outside the CSR window, and their contents are trusted rather
than read.

**And which FILE each pinned include name reaches is measured too**, by
`-H`: the preprocessor lists the files it opened, and no pinned name may be
opened beside the firmware, whether the entry there is a file or a link to a
file elsewhere. It is judged by the path the preprocessor opened and by the
file that path reached. That is what a listing pin cannot say, however exact
it is about the directory. The caveat belongs with the instrument and is
written at its site as well as here: **`-H` proves resolution in the tree it
is HANDED** -- the firmware's own directory plus the census's stub header
root -- so a different `-I` set, sysroot or working directory is outside this
measurement, and the CONTENTS behind each resolved third-party name stay
trusted rather than read.

The `-E` and `-H` measurements take the census's RV32 compiler, and so does
the compiled half of the per-selection grading, so they stand down where there
is none. Both hosted builder consumers REQUIRE that compiler (#504,
`--require-rv32`), so they grade wherever a merge is graded. The text
refusals they replaced are RETIRED on every machine, with no fallback arm,
except the splice and `##` bans inside the six boot-path bodies, which are
NARROWED and refuse on every machine alike: where no RV32 compiler answers,
what the retired refusals used to refuse is a registered `NOT RUN`, never
coverage, and gate 1b's verdict says so in its first clause. The section
"Text rules retired onto instruments", below, is the ledger.

A second tool check runs alongside the text rules, and it is an **addition**
rather than a replacement. Where an RV32 cross compiler is available, the gate
compiles the firmware and requires that no function except `milan_reg()`
materialises an address inside the Milan CSR window; where one is not, it
stands down, says so in its printed verdict, and registers that stand-down so
the suite's closing line names it.

**A candidate is the RV32 target only if it says it is.** The probe that
selects the compiler is RISC-V assembly under a guard on `__riscv_xlen`,
because `riscv64-elf-gcc` assembles that asm exactly as an RV32 GCC does. A
candidate is tried bare first, then driven with `-march=rv32i -mabi=ilp32`,
and the flag set that answered is carried into every census and mutation
compile the gate makes; a candidate no flag set drives at 32 bits stands down
rather than being adopted. Without the width guard a 64-bit GCC was accepted
as "the exact RV32 target", every mutation compile then ran at 64 bits, and
the firmware's own `(volatile uint32_t *)(MILAN_CSR_BASE + offset)` became an
`-Werror` int-to-pointer-cast that failed the suite on a pristine tree (#206).
The compiler is not taken at its word twice over: every census compile's own
`.attribute arch` is read back out of the assembly the gate is about to
census, because a wrapper can honour `-march=rv32i` on the probe and drop it
on the census call. A toolchain that declares no arch attribute is reported
as declaring none rather than blamed for it.

Five self-tests hold this. Four of them run on any machine, RISC-V compiler
or not: (a) a stub compiler drives the probe through all three candidate
shapes (already RV32, 64-bit with an rv32 multilib, 64-bit only) and the
recorded argv is read back to prove the driver flags reach the compiler;
(b) a deterministic host-only selection and (c) a deterministic
64-bit-candidate selection each make any attempted compile fail and check
that the same observed no-run verdict produces the printed `STOOD DOWN`
claim; and (d) the arch check is driven over `rv32` text, `rv64` text and
text with no attribute at all. The fifth runs only on a runner where the
census is live: the probe is re-run against the adopted compiler, under this
run's own flags, asking for a 64-bit target, and must fail. Where no
candidate is adopted there is nothing to re-probe, so the census stands down,
the closing verdict names that arm, and the gate's evidence line says the
live measurement did not happen instead of claiming it did.

**A pristine tree can still redden for a toolchain reason, and that is a
deliberate open item.** Where the census compiler IS the RV32 target and the
census compile nevertheless fails, the gate raises rather than standing down:
a source it cannot compile is a source whose CSR stores it cannot census, and
converting that into a stand-down would let a genuinely uncensusable firmware
pass. The message names the compiler and quotes its last diagnostic, so the
attribution is correct, but a toolchain with unusable headers therefore
reddens a clean checkout. Separating "this toolchain cannot compile any
conforming source" from "this source is uncensusable" needs a positive
control compiled first, which is a design of its own and is not part of #206.
It is not reachable on either toolchain this repository is built with.

**The CRC decision is now proved, and by resolution rather than placement.**
The source rule still only finds the `crc32()` assignment and requires every
non-zero return to appear later in the same preprocessor arm, which are
textual placement facts and not dominance. What proves the property is the
RV32 resolver: it interprets the emitted assembly of `load_aem_image()`, reads
the CRC call's operands back as values, tracks the compared value from the
call that produced it, and then REMOVES the CFG edge the comparison takes when
the values are equal and requires every reachable return to resolve to zero.
Four shapes that passed every textual rule are mutation-table entries as a
result, each rejected with the property named:

| Edit | Resolver verdict |
|---|---|
| `goto crc_ok;` past the comparison, `crc_ok:` on the non-zero return | `can hand back a verdict this gate cannot resolve to zero ... with the CRC-equality edge REMOVED` |
| the same bypass spelled `do { ... break; ... } while (0)` | the same message, which is why banning `goto` was never the proof |
| `got = MILAN_AEM_IMAGE_CRC32;` between the call and the comparison | `never compares the value crc32() HANDED BACK against MILAN_AEM_IMAGE_CRC32` |
| the CRC taken over `SPIFLASH_BASE + MILAN_AEM_FLASH_OFFSET` | `takes its CRC over 0x20e00000, not over MILAN_AEM_DESC_BASE (0x7f700000)` |

None of the four is recognised as a construct. Each is answered by a value or
by an edge, so a fifth spelling of the same defect needs no new rule.

The source store instrument HAD two uncovered classes, and the resolver is
what covers both; #409 retired the cast, store and asm sets onto it rather
than widen them again. The cast set only recognised a cast whose text
contained a `*`, and the store set only recognised a left-hand side that
started with `*` or was `name[...]`. So a cast with no `*` combined with a
`->` or subscript store was outside the source instrument:

```c
typedef struct { volatile uint32_t ctrl; } *milan_adp_blk;
...
((milan_adp_blk)0x90000600u)->ctrl = 1u;      /* ADP_CTRL[0], pre-AEM */
```

That is a durable pre-AEM entity advertise. The compiled census sees the
materialised CSR address and rejects that literal spelling. It does NOT see
the same store through a base held in a variable, because at `-O0` the address
is built with `slli`/`ori` and no window immediate is ever printed:

```c
static unsigned int csr_page = 0x9000u;
...
((milan_adp_blk)((csr_page << 16) | MILAN_ADP_CTRL))->ctrl = 1u;
((milan_csr_page_p)((csr_page << 16) | MILAN_PP_CTRL))[0] = 1u;
```

The second class is the one both reviews of PR #491 reported and #495
records: the store set took a left-hand side back to the last `;{}`, so a
store behind a BRACE-LESS `if` read as `if (c) *p`, began with neither a `*`
nor a subscript, and was not a store at all to that rule, whatever it pointed
at. The tripwire did not fire for a whole statement class. A RESOLVED store
address has no such shape to miss, and that spelling is a permanent mutation
where the resolver runs: a brace-less `if` storing through a paged base into
`ADP_CTRL` is refused on the address it resolves to. On a runner with no RV32
compiler neither class is refused, as before #409; the hosted builder jobs
require that compiler.

Both paged-base stores were measured GREEN on the whole gate before the
resolver existed. The resolver
rejects both, because it computes the store address rather than matching one:
`the compiled firmware STORES into the Milan CSR window (0x90000000..0x90010000)
from configure_fabric(), at 0x90000600`. Its store census exempts nobody, the
address helper included, so a store planted inside that helper is answered the
same way; the compiled census remains blind to that one by construction, and
both facts are measured on the same compile every run.

**What the store census does NOT resolve, stated exactly.** An earlier
revision of the resolver built its store census only from stores whose address
resolved to a number, so a store through a base it could not resolve was
dropped before it was ever asked about and the gate reported a clean census
over the subset it had understood. A base derived at run time is enough to
reach that hole:

```c
typedef struct { volatile uint32_t ctrl; } *milan_dyn_adp_blk;
...
unsigned int runtime_page = milan_read(MILAN_ID) ^ (MILAN_ID_MAGIC ^ 0x9000u);
((milan_dyn_adp_blk)((runtime_page << 16) | MILAN_ADP_CTRL))->ctrl = 1u;
```

The census now CLASSIFIES every store the compiler emits. Five classes are
placed: an address that resolves to a number (answered by number, in or out of
the window), an address that resolves to a BOUNDED RANGE (judged by address
the same way, and a range that so much as touches the window is refused), a
stack address, the address of an object this translation unit
DEFINES (a symbol it merely references is placed by the linker, not by this
unit, so `extern volatile uint32_t r; r = 1u;` is refused), and the address
helper's own return, which is the single sanctioned way into the window and
which exactly one function may store through. The
arguments of a function this unit neither exports nor takes the address of are
resolved from its call sites, which is what places the output-pointer writes in
`parse_u64()` and `seconds_to_ns()` on the stack. Anything else is a REFUSAL,
not an omission. Mutation-table entries carry it: the runtime-derived base
above, an unplaceable store planted inside the AEM verifier beside the placed
copy store, a store through an `extern` symbol the linker places, and a second
consumer of the
address helper's return. The classifier's fail-closed default -- a store operand
the resolver cannot even read -- is measured on a hand-written `sw rd, sym, rt`,
because GCC never emits that pseudo-instruction here and an unexercised
fail-closed branch is a claim rather than a measurement.

**Every store CLASS, not only the integer ones** (R228-F1 on PR #521). The
census compiles at the adopted compiler's default ISA. For the #504 SDK that
is `rv32imafd` with the ILP32D ABI, and the overlay above with a `float`
member is stored with `fsw`, with a `double` member with `fsd`. The
classifier used to know only `sw`, `sh` and `sb`, so those two stores left no
observation at all and passed the whole gate, while the `uint32_t` one was
refused. Stores are now classified by instruction class:

- integer: `sb`, `sh`, `sw`;
- floating-point: `fsh`, `fsw`, `fsd`, `fsq`, whose stored value the
  lattice does not hold;
- RV32A: every `amo*.w` and `sc.w` instruction, whose memory operand is the
  third. These are instruction classes. An atomic builtin that GCC compiles
  to a call is not one of them; see the boundary below.

A store is judged at EVERY 32-bit word it writes, so an `fsd`, or a
misaligned `sw`, whose first byte lies just below the window is refused on the
window word it reaches. A store through a bounded range is judged over its
footprint, up to the last byte its highest placement writes. Any other
instruction that addresses memory and is not a recognised load (`lb` to `lw`,
`flh` to `flq`, `lr.w`) is reported as UNCLASSIFIED and refused by rule 1b, so
a class missing from the table fails closed.

**What a store leaves behind** (R227-2-F1 and R228-F5 on PR #521). The
lattice models two kinds of memory word: a frame slot, keyed by frame register
and displacement, and a word of a static this unit defines, keyed by symbol
and displacement. That is what lets a parked address be read back and a later
store through it be placed. A modelled word keeps a value only after a
whole-word integer store to it (`sw`) or an `amoswap.w`. Every other store
leaves it unknown: a byte or half-word store, even at the word's own offset,
an FP store, any other AMO, and an SC. A store through a frame register or a
static's address also makes every other word of that frame or that static
its footprint overlaps unknown. A store through a stack address may
land on any frame slot, so it makes every frame slot unknown. That covers a
pointer to one of this function's locals, `q = (T *)&v; q->w = x;`, and a
pointer a caller handed down. A word reloaded after any of these places
nothing, so a store through it is refused by rule 1b. Four shapes passed the
whole gate before this: a union byte and a union half-word overwrite that
leave a parked `ADP_CTRL` address in place, and an integer and a `float`
rewrite of a local through a pointer to it. All four are permanent compiled
mutants now.

Literal-assembly controls for all of this run on every machine, compiler or
none. They cover the class table, the footprint of a straddling store and of
a ranged one, and the rewrites above, each against a whole-word positive arm.
They also cover the branch refinement, which may bound a frame slot only while
no store of any class can have rewritten it since the slot was loaded. Five
compiled mutants through the paged base must each be refused on the resolved
address: `float`, `double`, and the 32-bit atomic exchange, fetch-or and
compare-exchange builtins. Each must actually emit its class where the census
ISA declares that extension. The atomic three are registered only where the
census ISA carries `a`, because without it GCC compiles them to library
calls; elsewhere that is a registered `NOT RUN`. The four compiled rewrite
mutants must each be refused as the one store `configure_fabric()` cannot
place.

**The boundary of that classification.** It reads the instructions the
compiler prints as mnemonics, in this translation unit. A raw encoding --
`.insn`, or a data word emitted inside a function -- is not an instruction to
this reader; only an inline-`asm` template can produce one here, and the
inline-`asm` set pins those templates on every machine. GCC's `lr.w`/`sc.w`
retry loop branches to numeric local labels (`1:`, `1f`, `1b`), which this
reader does not bind. So neither the loop's back edge nor its forward exit
past the SC is modelled, and the SC store is still reached in order and
judged. The census ISA is not the shipping CPU's: the shipping hart is RV32I, so
FP stores and RV32A instructions exist only in the census compile, and
classifying them makes the census stricter, never looser.

**What the census does NOT observe** (R228-F5 on PR #521), stated so no
reader takes it for more:

- A store made inside a CALLED function. The resolver records a call's
  arguments and does not judge them. So a C-library or libatomic call that
  writes through a pointer this unit forms is not observed, even when that
  pointer is a window address. Examples are `__builtin_memset` or `memcpy`
  onto `ADP_CTRL`, and a 64-bit atomic builtin, which RV32A has no
  instruction for and GCC compiles to `call __atomic_exchange_8`. The memset
  and 64-bit exchange shapes were measured passing the complete gate on the
  adopted SDK. A callee this unit defines is resolved on its own, and its
  stores are classified like any other. What it writes into its caller's
  frame through a pointer it was handed is not modelled for the caller, which
  keeps its value for that local across the call.
- A store through a resolved number changes neither model, and one through a
  bounded range drops the static words but not the frame slots. The resolver
  does not know where the linker places the stack or the statics, and it
  assumes a numeric address reaches neither.
- A byte or half-word load from a frame slot reads the slot's whole modelled
  word. A static's word is read back only by `lw`.

The text rules #408 and #409 retired onto these instruments did not cover
these shapes either.

**The residual that was a hole, and why it is gone.** An earlier revision
DECLARED the copy loop's store rather than placing it, as the residual entry
`("load_aem_image", "unplaced", None): 1`, asserted by exact count. That key
binds neither the store's base nor its value, so the budget it declares can be
SPENT by a dangerous store: redirecting only the shipping copy destination,

```c
volatile uint8_t *dst = (volatile uint8_t *)((((milan_read(MILAN_ID) ^
    (MILAN_ID_MAGIC ^ 0x9000u)) << 16) | MILAN_ADP_CTRL));
```

compiles warning-clean, keeps the store statement `dst[i] = src[i]` textually
identical, prints no window immediate, keeps the residual key set and count
byte-for-byte the same, and after the boot identity check evaluates to the
live `ADP_CTRL` (0x90000600), so the first copied byte (`'A'`, bit 0 set)
asserts the ADP enable before the CRC comparison. The complete gate accepted
it and reported the shipping tallies (found independently by both reviewers
of PR #241 round 4; measured again here on the pre-fix revision before the
fix was written).

The class fix places the store instead of declaring it: on the edge the
emitted `bltu` takes into the loop body, the branch's own comparison bounds
the loop index, so the store address is the bounded range
`[MILAN_AEM_DESC_BASE .. MILAN_AEM_DESC_BASE + MILAN_AEM_IMAGE_BYTES - 1]`,
entirely outside the control window, and rule 1d additionally pins that range
INSIDE the buffer the CRC verdict is taken over, in both directions: a
verifier with no bounded store and a bounded store outside the buffer are
both refusals. The refinement's own degenerate cases are measured on every
run: a synthetic `bltu`-bounded loop store must come back as exactly base
plus [0..63], and the same loop on a base whose sum can wrap 32 bits must
come back unplaced. Three mutation-table entries carry the retired residual,
each measured GREEN on the complete pre-fix gate first: the redirected
destination above, a destination made unresolvable while preserving the old
key and count (`MILAN_AEM_DESC_BASE + (milan_read(MILAN_VERSION) & 0x1000u)`),
and a destination bounded but outside the CRC'd buffer (`SPIFLASH_BASE`).

One store in the shipping firmware is still not placed. It is DECLARED in
`RESOLVER_STORE_RESIDUAL` and asserted exactly, so one more unplaceable store
anywhere -- in that function or in any other -- is RED, and a residual
that goes away must be retired here and in the gate in the same change. Its
identity is itself bound: the callee is part of the key, so a store through
any other unresolved base is a different, refused class rather than a budget
this entry hands out:

| Store | Why it is not placed |
|---|---|
| `parse_u64()`: `errno = 0` | the base is what `__errno_location()` returns, and that function is not compiled in this translation unit |

So the property this gate proves is: no store outside that one lands in the
control window, and any new store it cannot place reddens the gate. It is not
"every store is resolved", and the closing verdict says so on every run. One
more thing is assumed rather than proved here and is named for the same reason:
the `stack` class rests on the SoC's memory map, where the stack is RAM and not
the device window this rule measures.

**And what the store census does not answer at all: the choke point's
ENTRANCES.** Every question above is about what `entity_advertise()` CONTAINS
and what its verdict test dominates, and the dominance question runs the
function in isolation on a synthetic argument, so between them they prove
dominance for one execution and for no call edge the firmware actually has. The
resolver therefore asks a fifth question of the same assembly: `entity_advertise`
appears in no `.globl` and its address is formed nowhere, no line of the emitted
assembly names it except the four a private function called by name produces
(its label, its `.type`, its `.size` and a `call` operand), this unit emits no
`jalr` or `jr` through a register at all, exactly one call edge reaches the
choke point and it is in `milan_init()`, and the value handed on that edge is
the tag the `load_aem_image()` call produced. A call edge it cannot place, and
an argument it cannot trace to the verifier, are REFUSALS, never a default of
"verified". The symbol-use rule is a WHITELIST for the same reason: a list of
spellings to refuse is the recognizer shape this whole question exists to
retire, and `.set alias,entity_advertise` exports neither this name nor its
address while still handing another unit a global symbol that calls the choke
point. Five mutation-table entries carry it, and each was measured to
PASS the whole boot-contract gate on the revision that preceded them, where the
tally read `153/153 mutations rejected`:

| Edit | Resolver verdict |
|---|---|
| `static void (*advertise_hook)(int) = entity_advertise;` called as `advertise_hook(1)` from the UART status handler | `forms the ADDRESS of entity_advertise(), which is an ENTRANCE into the choke point this gate cannot tie to the AEM verdict` |
| a second direct call spelled `entity_advertise(1), (void)0;`, which the source rule's call counter does not match because no `;` follows the parenthesis | `enters entity_advertise() from ['milan_init', 'milan_status_handler'], not from milan_init() exactly once` |
| `#define aem_verdict aem_loaded` and `aem_verdict = 1;` after the verifier, which the assignment rule does not see because it names no `aem_loaded` | `enters entity_advertise() with [1] rather than with the one value load_aem_image() handed back` |
| an indirect call whose target is not the choke point at all, `static void (*tod_hook)(uint64_t) = print_tod;` called as `tod_hook(...)`, so the unplaceable-edge rule is exercised on its own rather than behind the address-taken rule | `transfers control through a register this resolver cannot tie to a symbol ... : milan_status_handler() at .L41 through s1` |
| `void entity_advertise_public(int) __attribute__((alias("entity_advertise")));`, which exports a name that calls the choke point without exporting this name or forming its address | `names entity_advertise() in a form this gate does not recognise ... : ['.set entity_advertise_public,entity_advertise']` |

Answering the third needed a resolver change of its own, because at `-O0` the
verdict reaches the call through the static: a word stored into one of this
unit's own symbols and read back with `lw` before the next call is now a value,
and every symbol slot is dropped at each call and at each store the resolver
cannot place, so nothing survives a write it did not see.

**The block join is a meet over all predecessors.** The same round found the
frame-memory join treating a slot missing from one side differently from a slot
missing from the other, so a value stored on one incoming path of a diamond
survived the join whenever that path was folded in second. CRC provenance and a
verifier return value could then be invented out of block layout alone. Each
block's entry state is now the meet over ALL its reachable predecessors,
recomputed whenever one of them moves, and a key absent on any predecessor is
unknown. Gate 1b measures it on two semantically equivalent diamond layouts
that must agree, on the same diamond with the store on both predecessors that
must resolve, and against the restored order-dependent join, which must
disagree with itself across the two layouts.

When the RV32 compiler is absent, the census and the resolver stand down
together and every edit above is outside all active instruments, under a
closing line that reads `ALL GATES PASS EXCEPT n NOT RUN` naming that arm.
What remains joint with #162 is the Makefile half: a second translation unit
is a second place a CSR store can live, and no instrument here reads it.

**And a second blind spot of the same cause, on the Makefile side, CLOSED by
the origin probe (#162).** The recipe pin reads what `make -Bn` PRINTS, which
is text make has already expanded. A name this Makefile references but nothing
defines expands to nothing, so the pinned commands come out byte-identical
and the environment decides what the compiler actually gets:

```make
CFLAGS += $(MILAN_EXTRA_CFLAGS)
```

```
$ make -Bn                                            # what the gate sees
... -c __BASE_CFLAGS__ -I__BIOS__ <src>/milan_baremetal.c -o milan_baremetal.o
$ MILAN_EXTRA_CFLAGS='-include ../shadow.h' make -Bn  # what a real build runs
... -c __BASE_CFLAGS__ -I__BIOS__ -include ../shadow.h <src>/... -o ...
```

The gate's hostile double-run does not see it either — measured: it perturbs
three fixed names, and an assignment that defers to a fourth expands to
nothing in both runs, which come out identical. No `-e` is even needed for
the real build: a name a makefile never assigns takes its value from the
environment by make's default rules. `CFLAGS += $(EXTRA_CFLAGS)` is an
ordinary idiom, not a contrivance.

The class is worth stating because it is the same mechanism that stopped the
compiled census from replacing the text rules: **an instrument that reads a
RESULT cannot see what an undefined name would have contributed.** Reading the
Makefile's own TEXT saw `$(MILAN_EXTRA_CFLAGS)` and refused it; reading make's
result sees an empty expansion and has nothing to refuse.

What closes it is a third instrument, not a better reading of the plan: the
gate asks make for `$(origin NAME)` for every name that reaches the pinned
recipe chain, and refuses `undefined` and `environment` by name — either one
means the environment, not the Makefile, decides the value. The scope is the
recorded caveat made executable: the closure is rooted at the recipe-driving
names (`CFLAGS`, `OBJECTS`, `LIBMILAN_BAREMETAL_DIRECTORY`, `compile`) plus
the names the unexpanded `$(value compile)` references, closed transitively
over the Makefile's own assignment chain — and NOT at recipe-only references,
because the accepted `tags:` case references `$(CTAGS)`, which this make also
reports `undefined`, in a recipe the plan never runs, and it must stay green.
Measured against this Makefile, every in-scope name is `file` or `default`;
the deferral above is a mutation in gate 1b's table, refused by the origin
probe alone. See #162.

**Round two, from the adversarial pass on the restoring PR:** two spellings
walked past that closure and were measured reaching the real compile line
with every instrument green, and both are closed, each a permanent mutation
in the table. A **computed reference** — `X = MILAN_EXTRA` then
`CFLAGS += $($(X))`, any brace spelling — defers the NAME itself to
expansion time: the walker probed `X` (origin `file`) and the environment's
`MILAN_EXTRA` was never a name anyone asked about. There is no origin to
enumerate for a name that does not exist until expansion, so a computed
reference is REFUSED outright, anywhere in the Makefile text — a never-run
recipe included, which is deliberately wider than the origin closure and is
the one place the `$(CTAGS)`-style acceptance does not extend. A **`define`
body** — `define EXTRA` carrying `$(MILAN_EXTRA_CFLAGS)`, appended to
`CFLAGS` as `$(EXTRA)` — is make's sixth assignment flavour, and the parser
treated it as a directive to skip, so the body's references were in no RHS
the closure walked. `define` is an accepted idiom, so the fix parses the
block as the assignment it is and walks its references like any other RHS;
the deferral is then refused by the same origin probe as the plain spelling.

**Outside what any recipe pin can reach at all**, and recorded here rather
than turned into rules, because no pin over printed commands can see them.
Read the list as EXAMPLES of the kind, not as the set: `export CPATH` and
`export COMPILER_PATH`, which GCC itself reads from the environment;
`SHELL := ...`, which changes what executes the printed command;
`.EXPORT_ALL_VARIABLES:`; `$(shell ...)`, which runs at parse time, during
the gate's own plan run, before any recipe is printed; `$(file >frag,TEXT)`,
which writes at parse time the fragment the pinned `-include` line then
reads, so the deferred reference never appears in any walked text;
`$(guile ...)`, which this build's make advertises in `.FEATURES` and which
injects the same way through `gmk-eval` and `gmk-expand`. The first four were
the recorded set before round three's review; the next three are the same
kind, measured, and are recorded beside them rather than left to read as
absent. A variable name outside `[A-Za-z_][A-Za-z0-9_]*`, such as
`MILAN-EXTRA`, was recorded here until the review of round ten's head and is
now RULED on instead: make reads that name, this walker has no way to spell it
in an `$(origin)` request or in the assignment closure, and the read is refused
by name rather than left unmatched (the whole-name row below). That
vocabulary is this gate's, not make's: `MILAN-EXTRA = ready` is an ordinary
variable definition to make's own reader, so the refusal costs that edit too.
Round four's review adds four more of the same kind, each measured reaching
the real compile line and each a PLAIN reference or a computed parse rather
than the `$(eval)` that round rules on: an unbracketed `$M` on an ordinary
right-hand side, which the braced reference readers never see; a conditional
-- `ifdef MILAN_SHADOW`, or an `$(if ...)` inside an assignment's own NAME --
where the environment decides WHETHER a literal flag is added rather than
what some name's value is, so no `$(origin)` enumeration answers it; a recipe
prefix or a prerequisite the file COMPUTES rather than writes (a
`$(MILAN_E)`-built `.RECIPEPREFIX`, a `.SECONDEXPANSION` prerequisite behind
`$$`), which moves the eval token out of reach of every text reader here; and
the one that needs no Makefile edit at all, an environment variable NAMED
`1`, which LiteX's own `define compile` reads as `$(1)` and this Makefile
reaches through a plain `$(compile)`, measured putting `-include ../shadow.h`
on the compile line of the UNMODIFIED tree.

**Round three, the two channels round two measured OPEN (#410).** Unlike
the ones recorded above, a wider walker could close them, and it does: each was
reproduced before the fix reaching the real compile line with the
environment variable exported, and each is a permanent mutation. A
`$(call NAME,...)` or `$(value NAME)` first argument READS a variable by
its name without the `$(NAME)` spelling the walker modelled, so the name
never entered the closure. The walker now reads that first argument as the
reference it is, by the rule its own function names it with (below), and
the deferral is refused by the same origin probe as the plain spelling; a
computed first argument, `$(call $(X))`, is refused
as the computed reference it is. A top-level `$(eval ...)` line carries an
assignment no scan over assignment lines saw, and `$(eval)` expands its
argument BEFORE make parses the result, so the text make reads is not the
text in the file. The walker parses the one shape it can prove, an eval on
a line of its own whose whole argument is a literal `NAME op VALUE`
assignment, and walks it like any other right-hand side; every other eval
written `$(eval` is refused
outright, the way the computed reference is -- an eval of a called
template, of a plain reference (`$(eval $(MILAN_HOOK))` was measured
carrying the whole assignment in from the environment), or nested inside
another expansion -- at the same cost: such an eval is RED anywhere in the
Makefile, a never-run recipe included. The accepted case of each construct
is measured GREEN by the accepted-Makefile loop: a `$(call ...)` of a
`define` the Makefile itself carries, and an `$(eval ...)` whose body is a
literal assignment of a name the Makefile defines.

**Round three's own review, two measurements and what they changed.** The
first: the paragraph above was FALSE as written for one spelling, and the
walker is what changed, not the wording. GNU make routes `$(call NAME,...)`
to a BUILT-IN function when `NAME` names one, so `$(call eval,TEXT)` IS an
eval; the scan that refuses evals keys on the literal `$(eval` token, the
line is not an assignment so nothing put it in the origin closure, and
`$(call eval,CFLAGS += $(MILAN_EXTRA_CFLAGS))` on a line of its own was
measured putting `-include ../shadow.h` on the real compile line with the
name merely exported, while the gate reported every mutation rejected and
exited 0. Every make built-in reached through `$(call)` is now refused, in
both bracket spellings, with any padding, and wherever it sits, including
the right-hand side the pinned closure never walks, which is the position
the escape used; `$(call file,...)`, which writes at parse time the
fragment the pinned `-include` reads, is a permanent mutation beside
`$(call eval,...)`. This does not close the DIRECT spellings `$(file ...)`,
`$(shell ...)` and `$(guile ...)`, which stay in the recorded list above.
The second: the parsed shape's bound is narrower than "expansion changes
the value, never the shape or the name". What holds is that every literal
reference in the eval's TEXT is walked. A value that expands to a NEWLINE
changes the shape: with make's `define NL` idiom,
`$(eval CFLAGS += -I.$(NL)include extra.mak)` is read here as one
assignment whose only reference is `NL`, origin `file`, while make reads
two lines and includes a fragment the include-set pin reads the file text
for and therefore cannot see. That case is refused too, so the include-set
pin is exact against evals again.

**Round four's own review, the other half of the dichotomy (#410).** Round
three closed the escape on the BUILT-IN a `$(call)` reaches; what it left
open was the word PARSED. An eval read here as a benign `NAME op VALUE` can
still assign a value this file does not fix, and the walker bound a name it
had not pinned. Measured, and reproduced before the fix: `$(eval CFLAGS +=
$(1))` in a `define` body, run by `$(call TMPL,$(MILAN_EXTRA_CFLAGS))`, was
read as the assignment `CFLAGS += $(1)`; `$(1)` is no walkable reference, so
nothing was deferred and nothing was probed, while the exported environment
value arrived as the call's ARGUMENT on a line the pinned closure never
walks and the gate exited 0. The site said the opposite in as many words --
a whole-line eval in a define body was "an over-approximation ..., never a
miss" -- and that sentence is deleted rather than softened, because it is a
miss.

What replaces it is a property, not a list of spellings. **A whole-line eval
is walked only where this file binds every name its value reads.** That is
global scope: a define body's eval is expanded where the define is REACHED,
so `$(1)`..`$(9)` there are that `$(call)`'s arguments, a `$(foreach)` or
`$(let)` over the call REBINDS even a name the Makefile pins and `$(origin)`
reports `file` for, and an `$(if)` or a conditional prerequisite decides from
the environment whether a literal eval runs at all -- all measured. A recipe
eval is the same: the rule the environment adds decides when it runs. And at
global scope the value itself must read only names this file binds: never a
positional parameter in any position or bracket (`$(1)`, `$(2)`, `$(10)`,
`${1}`, `$1`), never an unbracketed `$M` the braced readers cannot see, never
a computed name, never an escaped `$$` that the eval's own expansion turns
into a live reference, and none of them at any remove through this Makefile's
own assignments. A `define` whose NAME is outside the identifier class opens
a body just the same, so what scopes an eval is what `define` reaches, not
the spelling of the name it binds. Everything else is REFUSED outright, on a
refusal that names what was deferred. Nineteen permanent mutations pin it,
the review's own plant among them, each reproduced before the fix reaching
the real compile line with `-include ../shadow.h` merely exported.

**The scope reader itself, and what decides a scope.** That property is worth
exactly what the answer to "which scope is this eval in" is worth, and the
round that wrote it read the answer one line at a time, with a pattern that
tolerates a leading tab. GNU make does not read a makefile that way, and its
own grammar puts the answer in the lines BEFORE the eval. Inside a `define`
body, a line beginning with the recipe prefix is BODY TEXT, so a
tab-prefixed `endef` does not end the body and the `$(eval)` after it is the
define's (GNU make, *Defining Multi-Line Variables*: a `define`/`endef` or
conditional directive written on a recipe-prefixed line is not recognised as
a directive). Outside a body, a line beginning with the recipe prefix is a
recipe line when make is in a rule context, and ordinary makefile syntax when
it is not (GNU make, *How Makefiles Are Parsed*, step 3), so a tab-prefixed
`define helper` inside a `tags:` recipe opens no body at all. Both were
measured WRONG at the previous head on pure parser fixtures: the define
body's own eval read `global` and was walked, which is the scope restriction
simply off for a body written that way, and a real global eval after that
recipe line read `define` and was refused, which is a cost charged for
nothing. One reader now answers the role of every line, for the scope reader
and for the define reader that binds a body's value, so the two cannot
disagree about where a body ends. A hundred and thirteen pure-parser controls
hold that reader now: sixty-four over the eval SCOPE, nineteen holding the
define reader to the same body, fifteen over make's assignment precedence from
the binding side, nine holding the RULE reader to the same directive token the
scope reader uses and six over where a `#` is cut at all. Six were RED against
the head round four replaced, four more against the head after it, fourteen
against the head after that -- eight of those answering a boundary wrongly
and six pinning a text reader it does not have at all -- twelve against the
head before round eight, four against the head that round replaced, and
twenty-six against the head this repair replaces. The remaining eighty-seven
are carried-forward neighbours that answer the same on both sides of this
repair, which is what they are for: twelve of them are new here, and they are
the blank-separated counterparts and the body-suffix arms that a reader
widening every class would fail. The
round-four review measured the value reader raising `IndexError` where a
value ENDS in a bare `$`; make carries such a `$` into the expansion the way
it carries `$$`, so it is refused by name beside it, with its own controls.
No repair here claims a compiler-command or environment
consequence: every one of them is a parser result, and the
mutations, the accepted Makefile edits and the recorded-not-ruled channels
above are unchanged by them.

**Two grammars for one word, and one reader for each.** Answering every
line's role in one place ended the disagreement between the two readers; it
did not fix what either of them RECOGNISED. The same pattern still opened a
`define` and counted a nested one, and make does not spell those the same
way. An opener is reached through make's modifier loop, so `override`,
`export`, `unexport` and `private` may precede it. A body is read by
`do_define`, which takes the line's first token and counts a level only when
that token IS `define`, whether it stands alone or names an inner variable,
and never reads a modifier there at all (GNU make 4.4.1, `src/read.c`). So a
bare `define` line nests and an `override define inner` line is ordinary body
text, and the previous head had both backwards, in the same two directions as
the recipe prefix. Measured on pure parser fixtures: `define helper` / `define`
/ `endef` / `$(eval LABEL := ready)` / `endef` read that eval as `global` and
WALKED it, and bound `helper` one line of the five; `define helper` /
`override define inner` / `endef` / `$(eval LABEL := ready)` invented a level
that is not there, refused a global assignment for a scope it is not in, and
bound `helper` nothing at all (#410, the review of round four's head). The
two patterns are separate now, and the role reader picks between them by
POSITION, inside a body or not, rather than by spelling. The tracked Makefile
and the four accepted Makefile edits read line for line exactly as before.

**Where a `#` ends a line, and when `define` is not a directive.** The two
readers agreed about a line's role and recognised make's two spellings of one
word, and both still read text no make ever reads: every reader here began by
cutting `#` and the rest of the line out of the WHOLE file. make's cut is
position-dependent, and this is the ORDER it runs in. Its makefile reader
collapses continuations and removes the comment from the line it is about to
parse. A `define` body is not parsed there at all: a separate reader collects
it, stores each line AS IT STANDS, and recognises a delimiter only when the
body line's first token IS `define` or `endef`, standing alone or followed by
a BLANK; only after recognising an `endef` does it cut a comment off what
follows it. A recipe line is handed to the shell before the makefile reader's
cut is reached, so it keeps its `#` too (GNU make 4.4.1, `src/read.c`). So
`endef#literal` and `define#literal` are body TEXT, a blank-separated
`endef #done` still closes a body, and an ordinary comment inside one is a
line of the value. Cutting first had both boundaries backwards, in the same
two directions again and measured on pure parser fixtures: `define helper` /
`endef#literal` / `$(eval LABEL := ready)` / `endef` ended a body that does
not end, so that eval read `global` and was WALKED and `helper` bound the
empty string, and `define helper` / `define#literal` / `endef` /
`$(eval LABEL := ready)` invented a level, so a real global assignment read
`define` and was REFUSED and `helper` bound nothing (#410, the review of
round five's head). The cut happens per line now, by the role make reads that
line in, and every reader here scans what it leaves, so none of them can
disagree about the file's text either. The same review measured one more
order: make parses a variable definition BEFORE anything interprets a
modifier or the `define` directive, so `define = ready` is an ordinary
assignment NAMED define and opens no body, `override define = ready` is that
same assignment, and `define MILAN_TMPL =` is still a real opener. That
precedence is the OUTER reader's only; inside a body, where the body reader
parses no assignment, the same `define = ready` line nests. Both are
positions, not spellings: the identical text gets opposite answers on the two
sides of the boundary, and the controls pin it from both.

**Make's seventh assignment operator, and where a directive keyword ends.**
The precedence above was right and reached six of make's seven assignment
operators. The seventh is `:::=`, the immediately expanded flavour: make's
variable reader takes a `:` and then tests for `=`, for a second `:` and for
a third, so three colons and an `=` are one operator and not a `::=` with a
colon in front of it (GNU make 4.4.1, `src/variable.c`; the manual's
*Immediately Expanded Variable Assignment*). An operator this reader could
not see was a precedence it could not apply: `define :::= ready` opened a
body that is not there, bound nothing, and made a real global
`$(eval LABEL := ready)` after it read `define` and be REFUSED, with an
`override` before it doing the same. The same omission lost a binding
outright one line over: `all: CFLAGS :::= -g` read as a RULE, so the flag it
adds to every prerequisite of `all` was outside the closure this gate walks.
All seven operators are one set now, so the assignment, the modifier form,
the target-specific form, the nested-body form and a genuine
`define MILAN_TMPL :::=` opener each keep the answer they had for the other
six (#410, the review of round six's head).

The other boundary that review measured is where a directive keyword ENDS.
make reads a line's first word with a token reader that stops at whitespace
or at the end of the line and at nothing else, measures that whole word, and
compares it to each keyword by LENGTH AND CONTENTS -- the conditionals, the
modifier and body directives, and the `include` family alike (GNU make 4.4.1,
`src/misc.c` and `src/read.c`). A regex word boundary is not that rule: it
ends a word at any punctuation, so the ordinary literal targets `ifdef:`,
`define:` and `include-labels:` read here as directives, the rule each of
them opens was never opened, and the tab-prefixed `$(eval LABEL := ready)`
that followed read `global` and was walked instead of being refused for the
recipe line it is on. The promised recipe refusal was simply absent for a
target whose name happens to begin with a keyword, and the pre-plan scans
returned empty for all three. One token rule answers for every keyword now,
and the rule reader shares it with the role reader, so a target is a rule
with its recipe in both. A genuine conditional or `include` is still a
directive and still no rule, and a conditional between two recipe lines still
leaves that recipe open -- including a bare `endif`, whose token IS the whole
line (#410, the review of round six's head).

**Which whitespace ends that token, and which whitespace ends no body.** The
token rule above was right about the whole word and wrong about the whitespace
that ends it, and the two are not the same class in make. make builds its own
character map as it starts: space and TAB are its BLANK class, and every
remaining C whitespace byte joins them in the wider class its token reader
stops at, the vertical tab and the form feed among them (GNU make 4.4.1,
`src/main.c`, `src/makeint.h` and `src/misc.c`). Reading only the blank pair
dropped genuine directives. Writing the two bytes as `<VT>` and `<FF>`,
`ifdef<VT>LABEL` and `ifeq<FF>(ready,ready)` are conditionals make evaluates
as it reads the file, leaving the rule they sit in open; here they read as
ordinary target lines, so a pending rule was CLOSED and the tab-prefixed
`$(eval LABEL := ready)` after them read `global` and was walked instead of
being refused for the recipe line it is on. That is round six's missing recipe
refusal one boundary over, with all five pre-plan scans returning empty for it
(#410, the review of round seven's head).

The BODY reader keeps the narrower class, because make's body reader does. The
reader that collects a `define` body skips the body line's leading whitespace
and then counts a nested `define` or an `endef` only where the keyword is the
whole line or a BLANK follows it (GNU make 4.4.1, `src/read.c`). So
`endef<VT>done` and `define<FF>inner` are body TEXT that delimits nothing,
exactly as `endef#literal` is. Giving every reader the wider class would have
traded the miss above for its mirror image: a body would end where make
ends none, and that body's own eval would read `global` and be walked. Two
read stages, two classes, and the controls carry each stage's fixtures against
the other's rule.

**The run make CONSUMES is that same wider class, at every reader that
consumes one.** Ending a token where make ends one was half the rule; the
other half is the whitespace make skips before it reads a token at all, and
reading that as the blank pair left the same miss at three more positions.
make's outer reader skips it before it parses anything, its modifier loop
skips it before every word, and the reader that collects a `define` body
skips it before it looks for a delimiter (GNU make 4.4.1, `src/read.c`,
`src/misc.c`). So `define<VT>MILAN_TMPL` opens a body named `MILAN_TMPL`,
`<VT>define helper` opens one too, `<VT>define inner` nests one inside a body
and `<VT>ifeq` is the conditional that leaves a pending recipe open. All four
read as something else here, so each body's or recipe's own
`$(eval LABEL := ready)` read `global` and was WALKED with all five pre-plan
scans empty: round seven's missing refusal at the positions its own repair
did not reach. A built-in's NAME ends at that class as well, so
`$(eval<VT>...)`, `$(call<VT>NAME,...)` and `$(value<FF>NAME)` are the
parse-time hook and the deferred reads their blank-separated spellings are;
both eval scans and the named-reference closure were blind to them (#410,
the review of round eight's head).

What keeps the widened opener honest is make's assignment precedence, read
one layer finer. The vertical tab is an ordinary NAME byte to make's variable
reader, which ends a name at a BLANK and nowhere else, so `define<VT>= ready`
and `define<VT>MILAN_TMPL =` are assignments to the names those bytes form
and open no body at all, exactly as `define = ready` opens none, while
`define MILAN_TMPL <VT>=` is a genuine opener whose flavour operator sits
behind the name's own blank (GNU make 4.4.1, `src/variable.c`). Three classes,
three readers, and each stage's fixtures are carried in the controls against
the other stages' rules.

**Where a first ARGUMENT starts and where it ends, which is not one rule for
both functions.** Round eight moved the run before a built-in's arguments and
left the two positions on either side of the first argument reading the blank
pair. What `$(call NAME,...)` names is a TOKEN: make cleans the argument up
with the same two readers it ends any other token with, so
`$(call HELPER<VT>,ready)` and `$(call HELPER junk,ready)` both call `HELPER`
and the run after the name is no part of it (GNU make 4.4.1,
`src/function.c`). Neither name entered the origin closure here, and
`$(call eval<VT>,TEXT)` is the built-in `call` dispatches to with the promised
refusal absent, which is round three's escape in a spelling its own repair did
not reach. The other position is the run before a COMPUTED first argument:
make ends the function name at that same class and skips the whole run before
its arguments, so `$(call<VT> $(PICK))` defers its name exactly as
`$(call $(PICK))` does, and reading the blank pair there made the text a
reference to a name ending in that byte, with the deferred name neither walked
nor refused and the inner literal the only thing the scan saw. The same class
carries the LINE FEED wherever a reader scans stored text rather than lines,
because a `define` body keeps its newlines and is expanded whole: an
`$(eval<NL>...)` written in one is the parse-time hook, and it was neither
parsed nor refused (#410, the review of round nine's head).

`$(value NAME)` does NOT name its argument that way, and one rule for both
would have been wrong in the other direction. make looks a `value` argument up
WHOLE, with no token boundary in it, exactly as it looks up the plain
`$(NAME)` reference (GNU make 4.4.1, `src/function.c`). So
`$(value NAME<VT>)` names the variable those bytes spell while
`$(call NAME<VT>)` calls `NAME`: the same suffix byte, two functions, two
answers, both carried in the controls against each other.

**A name this walker cannot spell is refused, not approximated** (#410, the
review of round ten's head). Where a blank, a vertical tab or a comma follows
the identifier in a `value` argument or inside a plain reference, make looks
up a name outside the `[A-Za-z_][A-Za-z0-9_]*` vocabulary every reader here
spells. That vocabulary is THIS WALKER'S and not make's grammar (#410, the
review of round eleven's head): make ends an assignment's name only at
whitespace, `#`, an assignment operator or a `:` that opens none, so
`MILAN-EXTRA = ready`, `NAME,x = ready` and `.DEFAULT_GOAL = ready` are
ordinary variable definitions make binds, while `NAME<SP>` and `NAME:sub` are
names no assignment line can bind at all. What the refusal rests on is that
the `$(origin)` request this gate writes, and every assignment its closure
records, are written in that one pattern, so a name outside it is a name the
walker cannot ask about or account for. The cost therefore includes edits make
would have accepted, and it is disclosed here rather than explained away.
The walker used to keep asking `$(origin)` about the identifier the
span starts with, or to drop the read entirely where the suffix byte was one
no pattern matched, and both were recorded as covered: `$(value NAME,x)` and
`$(NAME<SP>)` put `NAME` in the origin request, `$(value NAME<VT>)` and
`$(NAME,x)` put nothing there, and `$(eval LABEL := $(value NAME,x))` was
classified bindable because `NAME` is bound. An identifier prefix is a
different variable, and an answer about it proves nothing about the one make
reads, so each of these is now REFUSED by name, wherever it sits, exactly as a
computed name is. A later expansion inside any of those spans is the computed
reference it always was, and is now seen there too:
`$(value NAME,$(PICK))`, `$(value NAME $(PICK))`, `$(NAME $(PICK))` and
`$(NAME,$(PICK))` reach the computed-name refusal. The reads that stay
COVERED are the complete ones, `$(value NAME)`, `$(NAME)`, `$(NAME:.o=.d)`
and the `$(call NAME,...)` token, and they are carried in the controls beside
the refusals so the repair cannot be met by refusing every read. A PLAIN
`$(1)` or `$(@D)` keeps the treatment recorded above: bound by the call site
whose argument text this closure walks or by the rule make binds them in, and
skipped rather than probed.

**That exemption belongs to the plain reference alone** (#410, the review of
round eleven's head). `$(value 1)` and `$(call 1)` are not positional
parameters being used; they are lookups of a variable named `1`, and neither
construct has bound one where it looks up. `value` looks its whole argument up
with no scope of any kind, and `call` reads its target and can return before
the `$(1) .. $(N)` scope it pushes exists at all. Treating those two argument
positions as make's own dropped the read from the closure AND raised no
refusal, which is the covered-looking answer about a variable the environment
decides that this whole section is against, so a numeric or automatic name in
either position is now refused by that name. `$(1)` inside a `define` body
reached through `$(call T,...)`, and a recipe's `$@`, are unchanged, and both
are carried in the controls as the counterparts that must stay skipped.

**A substitution reference is read from the COMPLETE reference** (#410, the
same review). make counts this expansion's own brackets, expands what it finds
and only then looks for the `:` and the `=` that make it a substitution, so in
`$(NAME:$(PAT)=.d)` the variable is `NAME` and `PAT` chooses the pattern.
Ending the name span at the first close bracket instead ended it inside the
nested reference, where the `=` is not yet in sight: `NAME` left the closure
and a supported idiom was refused as a computed name, inside an otherwise
bindable `$(eval ...)` as well. The whole-reference span is now what decides,
so `$(NAME:$(PAT)=.d)`, `${NAME:${PAT}=.d}`, the mixed bracket spellings,
`$(NAME:$(PAT)=$(REP))`, `$(NAME:.o=$(REP))` and the
`$(patsubst $(PAT),$(REP),$(NAME))` counterpart all keep their literal
dependency and raise no refusal. The refusals that must survive are carried
beside them: a colon whose `=` only an expansion could supply
(`$(NAME:$(PAT))`) leaves the split undecidable from the file and stays a
computed-name refusal, a name that itself expands (`$($(PICK):.o=.d)`) stays
one, and a `$(value ...)` argument is still looked up WHOLE, so the same bytes
there are computed rather than a substitution.

**And the `=` that decides it is one that SURVIVES expansion** (#410, the
review of round twelve's head). Reading the complete reference settled how far
the name span reaches; it did not settle which `=` inside it is the separator,
and the walker asked the wrong question there: whether the unexpanded text
spells one. make asks the expanded text. An `=` a nested expansion takes with
it never reaches the enclosing name: `$(subst =,,x)` hands the byte to its own
first argument and yields `x`, `$(PAT:.o=.d)` yields the substituted value of
`PAT`, and `$=` is make's one-character reference to a variable named `=`. So
`$(NAME:$(PAT:.o=.d))`, `$(NAME:$(subst =,,x))`, `$(NAME:$(PAT)$(subst =,,x))`,
`$(NAME:$(PAT)$(if ,=,x))` and `$(NAME:$=)` were answered about `NAME` while
make reads `NAME:.d`, `NAME:x`, `NAME:.ox`, `NAME:.ox` and `NAME:`: a different
variable, which on a right-hand side the origin request covered with no refusal
at all. Each is now the computed name it is, because which name make ends up
reading is not decided by the file. The eval binder is where those spellings
part company, and they are kept apart rather than grouped: the first four it
classified BINDABLE on that same identifier, directly and one assignment away
through a relay, and it now refuses each by the reference it reads, while
`$(NAME:$=)` it already refused, by its own rule for the sibling `$=` read, and
that standing refusal now names the enclosing reference instead of the read
inside it. No eval refused before this repair is bindable after it. What still
decides the split, and is carried beside them: a literal `=` OUTSIDE the
nesting survives it, so `$(NAME:$(PAT:.o=.d)=.x)` and
`$(NAME:$(PAT)$(subst =,,x)=.d)` keep `NAME`; an escaped `$$` is no expansion
at all and emits one literal `$`, so `$(NAME:$$=.d)` is the substitution
reference it looks like; and a surviving separator in front of a name this
walker cannot spell, `$(MILAN-EXTRA:...=.d)`, still reaches that name's own
refusal rather than none. What this decides is the enclosing reference's
substitution split and nothing else: a standalone `$M` on an ordinary
right-hand side stays the recorded channel above, ruled on only where an
`$(eval ...)` value reads it.

**What a clear pre-plan scan says, and what it does not.** These controls
measure how this walker CLASSIFIES a text, which is a smaller claim than GNU
make accepting the file, and one control makes the gap visible. A
`$(eval ...)` written on a recipe-prefixed line with no preceding target must
read `global` here rather than `recipe`, because outside a rule context the
prefix is not special to make's parser. make still does not read that file:
its variable reader skips an assignment operator sitting inside a `$(...)`
reference, so the line is not a variable definition, and a recipe-prefixed
line that is not one and has no preceding target is `recipe commences before
first target` (GNU make 4.4.1, `src/variable.c` and `src/read.c`; the manual's
parsing sequence settles where the prefix is special, not that every other
prefixed line is accepted). So each control that expects NO refusal also
records whether make reads that text as a makefile at all, and a clear
pre-plan scan is never by itself evidence that make accepts a Makefile
(#410, the review of round four's head). What the scope reader models is
make's line roles: the recipe prefix, the rule context, and the two `define`
spellings. A recipe prefix this Makefile COMPUTES is still outside it, and
stays recorded below rather than ruled on.

The cost is the widest of these refusals and it is the point: a template
that EVALs its argument is refused where the same template RETURNING that
argument through `$(call)` stays green, because the call site's argument is
text the closure walks and the eval's is not. The accepted
`$(call milan_include,$(BIOS_DIRECTORY))` of a `define milan_include` whose
body is `-I$(1)` is exactly that green case, and it is measured GREEN here,
beside `$(eval MILAN_INCLUDES = -I$(BIOS_DIRECTORY))`. **Remedy** for the
refused shape: return the value and assign it,
`CFLAGS += $(call tmpl,$(NAME))`, or write the assignment at top level where
its names are this file's to bind.

Read the constraints below as what they are: they bound the spellings they
recognise, and they cost real edits to do it.

- **Any CSR store must go through `milan_write()`.** Only `milan_reg()` may
  use `MILAN_CSR_BASE` or a `(volatile uint32_t *)` cast. Every other store
  the compiler emits is placed by the resolver at the address it resolves to,
  so a fifth cast, a fifth store, a fifth `asm` statement or a reordering is
  GREEN when what it stores lands outside the control window (#409). Where no
  RV32 compiler answers, that placement is a registered `NOT RUN`, and nothing
  else on that runner bounds address formation outside `milan_reg()`'s own
  spelling.

The rest are refusals, and each one costs a legitimate edit:

| Constraint | Why the gate needs it |
|---|---|
| `o_ptp_enable` is driven directly by `ptp_ctrl[0]`, the `milan_csr` instance binds it directly to `cfg_ptp_enable`, and the `ptp_csr_sync`/`ts_counter` pair directly consumes that net with ungated clocks, resets, increment/adjust/TOD controls and readback | PHC startup is independent of AEM/ADP from the CSR register through the actual PHC consumer; the CSR harness separately proves writes to `ADP_CTRL` cannot force or gate the module output |
| External RX, the pre-filter tap, both enabled and bypass `RXFILT_P` arms, the filter's reset-time policy/programming seams, fabric-gPTP shadow RX/TX and timestamp feedback, `gptp_ctl_mux`, MAC-boundary arbitration and external TX handshakes use direct data, clock and reset connections | checking only an endpoint or data port misses an internal/downstream valid, policy or reset gate that makes the plane externally silent before AEM succeeds |
| CSR and datapath structural checks ignore comments, census every backtick token at any column and require each checked item to be direct in its inspected generate arm | inactive comment, preprocessor or static-generate text must not stand in for a live gated connection; a future directive or nested generate requires an elaborated checker or an explicit update to this bounded model |
| `milan_reg()` is exactly base plus its argument and `milan_read()` directly dereferences that result | every call-site claim depends on those helpers preserving the register address and loaded value; helper-body refactors must update the model and its mutations |
| Firmware `MILAN_ID` and `MILAN_ID_MAGIC` equal the comment-blanked, directive-closed RTL `A_ID` address and readback default | otherwise inactive decoy text can hide a live address/value change that teaches the token-level guard to validate a different CSR or forged identity |
| The `MILAN_ID` local is not assigned or addressed between its CSR read and mismatch guard | otherwise an intervening `id = MILAN_ID_MAGIC` forges the verdict while preserving every ordering anchor. A splice, or a `##` paste in a macro this file defines, that rebuilds the local's name there is refused by the bans kept inside the six boot-path bodies (#408). BOUND, measured by both reviews of PR #535's first round and not changed here: an assignment inside a plain function-like macro invoked there, `MILAN_FORGE(id);`, is not refused, on dev or here (#544), and neither is a paste through a macro a header defines, `__CONCAT(i, d) = MILAN_ID_MAGIC;` ([R273] F2 on PR #535) |
| A token-joining backslash-newline, or a `##` paste in any macro this file defines that they name at any depth, inside `milan_init()`, `configure_fabric()`, `entity_advertise()` or the three CSR accessors | NARROWED (#408) from the whole file, and refused on every machine. The paste ban reads this file's `#define`s, the one behind a byte-order mark at offset 0 included ([R273] F1 on PR #535); a macro a header defines, `__CONCAT` for one, is trusted rather than read, so a paste through it is outside the ban, with the bound of the plain function-like macro (#544). The text rules reading those bodies key on names as written, and the `-E` comparison compares only the boot tokens there, so a splice or a paste rebuilding another name they read, the identity sample or the verdict, agrees in both texts ([R272] F2 on PR #535). A splice inside a comment or a literal, and one with blanks on either side, joins no token and is not refused. Outside the six bodies both are retired, below |
| A second `#define` of any name, an identical one included | the address model reads a register name and the identity magic by ONE definition, and the compiler expands every use after a second one with the second: `#define MILAN_ID_MAGIC (milan_read(MILAN_ID))` after the real one turned the identity guard into a comparison of the sample with a fresh read of itself ([R273] F1 on PR #535). **Remedy:** define it once, or in the arms of one graded group, where each arm's definition is the one definition of the firmware it builds |
| A character or string literal that no quote closes on its line, an apostrophe in the text of an `#if 0` block included; a raw string literal | GCC ends an open literal at its line end with only a warning, and honours `R"d(...)d"` at `-std=gnu99` across lines; neither is what an edit writes to mean it, and before #408 this gate read an open quote as running on to the next one, lines away ([R272] F4 on PR #535) |
| The identity refusal remains the exact `if (id != MILAN_ID_MAGIC)` spelling | an equivalent comparison such as `if ((id ^ MILAN_ID_MAGIC) != 0u)` is refused because this bounded model anchors the mismatch block by that exact expression; accepting another form requires extending the recognizer and its paired controls |
| No `#pragma`, `#line`, `#undef` or `#include_next`, and no `#error` but the one saved-state contract guard | KEPT (#408), with this reason rather than a measurement: `#undef` changes what a register name resolves to in the address model, which reads definitions out of this file's text, and `#line` rewrites the line markers the `-E` comparison finds this file's bodies by. `#pragma` and `#include_next` change what the compiler does with text this gate has already read. It has no rule for them, so it refuses rather than ignores |
| `%:` or `??` in code, and a trigraph anywhere in the file, a comment's `what??!` included | KEPT (#408), the digraph and trigraph half of the old `##`/`%:`/`??` ban, and read on the WHOLE firmware before any reader and before a conditional is resolved, as dev read it: a digraph spelling a conditional's own directive is refused on every machine, not only graded where a compiler answers. The digraphs are the tokens phase 3 builds after phase 2 has deleted every splice, so `%\`, a line end, then `:ifdef` is refused as the `%:ifdef` GCC reads; the round-one ban read the text before phase 2 and missed it ([R272] F1 on PR #535, round two). A `%:` pair phase 3 reads as other tokens, the `<%` and `:` of `<%:`, is refused too, as dev refused every `%:` pair in code, so the ban is no narrower than dev's. Outside a literal or a comment nothing but a digraph or a trigraph spells either pair, so that half costs no edit anybody writes. A trigraph is refused in comments and literals too: the pinned GCC ignores it at `-std=gnu99` and a strict `-std` replaces it before comments exist, so `// ...??/` ends its comment in one dialect and swallows the next line, a directive, in the other. The `##` half is narrowed, above |
| A `#define` or `#include` inside the AEM verifier's QSPI-slot group or an `#error` guard | NARROWED (#408) from every conditional. Those are the two kinds of group left as written rather than graded one selection at a time, and the address model reads every definition as unconditional text, so an arm no selection resolves would choose what a register name resolves to. In a graded group each arm's definition IS unconditional in the firmware that arm builds, so an `#ifdef`/`#else` choosing a `#define` is GREEN. dev exempted the verifier's group from this rule, so a `#define` there was GREEN before and is refused now |
| Any statement in the AEM verifier's no-QSPI arm beyond a literal `printf` and `return 0;` | no selection compiles that arm and the census stub tree takes the other, so it is the one text in the firmware no instrument compiles. The retired cast, store and asm sets used to read it with the rest of the file; it is pinned instead |
| More than 16 preprocessor arm selections in the whole firmware, and code inside a disabled `#if 0` | every selection is graded as a firmware of its own, so an arm nothing builds is still graded as the code it would be, and a firmware with more selections than the bound is refused rather than graded in part. **Remedy:** delete dead code rather than disabling it |
| A helper split across two conditionals whose conditions are not both a bare `defined` test of one macro, such as a definition under `#if MILAN_DEBUG > 1` and a call under `#ifdef MILAN_DEBUG` | only groups asking whether one macro is defined are graded together, as the builds that exist; any other condition is not evaluated, so its arms are graded in every combination, one with the call and without the definition included, and the census compile of that one fails. The refusal names the selection it graded, not a build the product makes. **Remedy:** test the one macro with `#ifdef`, `#ifndef` or `#if defined(...)` in both groups |
| The `#include` set is exactly the twelve headers listed in the gate | a twelfth include is text in the translation unit no rule reads. A NAME pin, and it stays one whatever the `-H` measurement says: a name that names no existing file cannot be RESOLVED at all, so the measurement cannot refuse one and the name set is what does |
| `CFLAGS` gains only `-I$(BIOS_DIRECTORY)` | held now by the recipe pin rather than by a flag rule: the compile command is pinned whole, so any added flag changes it |
| The Makefile's `include` set is exactly its three lines | `make` can only plan fragments that exist. The set is read from the file TEXT, so it is exact over the lines in the file: a line an expansion creates would be outside it, and both routes to one are refused below, but a direct `$(file >frag,TEXT)` write is a recorded channel rather than a ruled one |
| `OBJECTS` may not use `?=` | `make` treats an environment variable as defined, so `?=` lets the environment choose the object list |
| A computed variable reference -- `$($(X))`, `$(CFLAGS_$(VARIANT))`, and (#410) a computed `$(call ...)`/`$(value ...)` first argument, `$(call $(X))` and `$(call<VT> $(X))` alike -- anywhere in the Makefile, a never-run recipe included | the NAME itself is deferred to expansion time, so no `$(origin)` enumeration can cover what the environment picks; refused rather than modelled. Which function an expansion opens, and how much whitespace it then skips, are make's own rules rather than the blank pair, so a wide separator before a computed argument does not hide it (#410, the review of round nine's head). **Remedy:** spell the reference with a literal name |
| A read whose LITERAL name is outside `[A-Za-z_][A-Za-z0-9_]*` -- `$(value NAME,x)`, `$(value NAME<SP>)`, `$(value NAME<VT>)`, `$(NAME<SP>)`, `$(NAME,x)`, a `$(NAME:sub)` whose colon opens no substitution, `$(MILAN-EXTRA)`, a `$(call MILAN-TMPL)` token and a NAMED positional or automatic lookup, `$(value 1)`, `${call 1}` or `$(value @D)` -- anywhere in the Makefile, a never-run recipe included | make looks a plain reference up by its COMPLETE span and a `$(value ...)` by its WHOLE argument, commas included, so each of these names a real variable, and that identifier class is THIS GATE's vocabulary: it is the name format of the `$(origin)` line the gate writes and of every assignment its closure records, so the walker cannot ask about the name make reads or account for where its value came from. It is NOT a restriction of make's assignment grammar, which ends a name only at whitespace, `#`, an assignment operator or a `:` opening none, so `MILAN-EXTRA = ready`, `NAME,x = ready` and `.DEFAULT_GOAL = ready` are ordinary definitions make binds and this refusal costs those edits; `NAME<SP>` and `NAME:sub` are names no assignment line binds either way (#410, the review of round eleven's head). The walker answered about the identifier PREFIX instead, or dropped the read with no refusal, and reported both as covered; an answer about `NAME` is an answer about a different variable (#410, the review of round ten's head). A PLAIN `$(1)` or `$(@D)` is not in this row: it is bound by the call site whose argument text the closure walks, or per rule by make. The same bytes as a `$(value ...)` argument or a `$(call ...)` token ARE in it, because `value` builds no argument scope and `call` reads its target before it pushes one, so nothing has bound that name at the lookup being walked. **Remedy:** spell the read with the complete identifier, `$(value NAME)` or `$(NAME)`, and give the variable a name inside that vocabulary |
| A substitution reference is read from the COMPLETE reference AND from a separator that survives expansion, so `$(NAME:$(PAT)=.d)`, `${NAME:${PAT}=.d}`, the mixed bracket spellings, `$(NAME:$(PAT)=$(REP))`, `$(NAME:.o=$(REP))`, `$(NAME:$(PAT:.o=.d)=.x)`, `$(NAME:$(PAT)$(subst =,,x)=.d)` and `$(NAME:$$=.d)` keep their literal name in the closure and are NOT refused, while `$(NAME:$(PAT:.o=.d))`, `$(NAME:$(subst =,,x))`, `$(NAME:$(PAT)$(subst =,,x))`, `$(NAME:$(PAT)$(if ,=,x))` and `$(NAME:$=)` are computed-name refusals | make counts this expansion's own brackets and expands what it finds before it looks for the `:` and the `=`, so the pattern and the replacement are outside the NAME. Ending the span at the first close bracket ended it inside the nested reference, hid the `=` and read the pattern as part of the name: the literal dependency left the origin request and a supported idiom was refused as a computed name, inside an otherwise bindable `$(eval ...)` too (#410, the review of round eleven's head). Because make looks for that `=` in the text it has ALREADY expanded, testing the unexpanded text for one counted an `=` no expansion leaves behind: a nested substitution's, a nested function argument's, and the one make's one-character `$=` reference reads a variable by. The split then answered about the identifier in front of the colon while make reads `NAME:.d`, `NAME:x`, `NAME:.ox` or `NAME:`: in the closure with no refusal at all, and in the eval binder for the nested substitution and function spellings, directly and through a relay. The `$=` spelling is the one the eval binder already refused, by its own rule for the sibling `$=` read; that refusal stands and now names the enclosing reference instead (#410, the review of round twelve's head). This row is the ACCEPTANCE half of the computed-name row above, and the refusals it must not swallow are carried beside it: a colon whose `=` only an expansion could supply, `$(NAME:$(PAT))`, and a name that itself expands, `$($(PICK):.o=.d)`, stay computed-name refusals, a `$(value ...)` argument is still looked up whole rather than split, and a SURVIVING separator in front of a name this walker cannot spell reaches that name's own refusal instead. An escaped `$$` is not an expansion and consumes nothing. **Remedy** for a refused shape: put the separator outside the nesting, or compute the pattern into a name of its own and spell `$(NAME:$(PAT)=.d)` |
| A `$(call ...)`/`${call ...}` whose first argument names a make BUILT-IN function -- `$(call eval,...)`, `$(call file,...)`, `$(call shell,...)`, and a `$(call subst,...)` written to map a built-in over a list -- anywhere in the Makefile, a never-run recipe included | `call` DISPATCHES to that built-in, so the construct is the built-in written where no scan for the built-in's own token can see it, and `$(call eval,TEXT)` was measured injecting a flag from the environment with every instrument green (#410, round-three review). The name it dispatches on is the TOKEN make cuts the argument down to, so `$(call eval<VT>,TEXT)` and `$(call eval junk,TEXT)` are that built-in too (#410, the review of round nine's head). **Remedy:** spell the built-in directly, `$(subst a,b,$(TEXT))` |
| A parsed `$(eval NAME op VALUE)` whose value reads a name this Makefile gives a MULTI-LINE value -- make's `define NL` newline idiom, at any remove | `$(eval)` parses the EXPANSION, so such a value adds makefile lines this walker reads as the one assignment it parsed, and an `include` among them is outside the include-set pin, which reads the file text (#410, round-three review). **Remedy:** keep the newline idiom out of an eval's value |
| An `$(eval ...)` that is not a whole-line literal assignment -- `$(eval $(call tmpl,...))`, `$(eval $(HOOK))`, an eval nested inside another expansion -- anywhere in the Makefile, a never-run recipe included | `$(eval)` expands its argument and parses the RESULT, so the text make reads is not the text in the file and no walk over the file can enumerate it; refused rather than modelled (#410). **Remedy:** write the assignment as `$(eval NAME op VALUE)` on a line of its own, which is parsed and walked like any right-hand side, or as a plain assignment line |
| An `$(eval NAME op VALUE)` whose assignment this walker cannot BIND, even though its shape reads as benign: one in a `define` body or a recipe, wherever that body is reached from, and one at global scope whose value reads a positional parameter (`$(1)`, `$(2)`, `$(10)`, `${1}`, `$1`), an unbracketed `$M`, a computed name, an escaped `$$` or a value ending in a bare `$`, at any remove through this Makefile's own assignments | a define body's eval is expanded where the define is REACHED, so its `$(1)` is that `$(call)`'s argument, a `$(foreach)`/`$(let)` over the call rebinds even a name `$(origin)` reports `file` for, and an `$(if)` or a conditional prerequisite decides from the environment whether it runs at all; the value assigned is then not the value this walker read (#410, round-four review). Which scope an eval sits in is read the way make parses a file, tab-prefixed body and recipe text included, and a value's end is a named refusal rather than a reader crash (#410, the review of that round). The `define` spelling that DELIMITS a body is make's, not the one that OPENS it: a bare `define` line nests and a modifier before one does not, so neither an unwalked body nor a falsely refused global assignment follows from writing a body that way (#410, the review of round four's head). Where a comment ENDS a line is make's too, and it is not everywhere: a body keeps its text, so `endef#literal` and `define#literal` delimit nothing while a blank-separated `endef #done` still closes a body, and an ordinary assignment named `define` binds a variable instead of opening one (#410, the review of round five's head). That assignment is recognised in every one of make's seven operators, `:::=` included, and a directive keyword is recognised as the whole TOKEN make compares, so the literal targets `ifdef:`, `define:` and `include-labels:` are rules whose next line is a recipe and the eval on it is refused by name (#410, the review of round six's head). That token ends at make's own whitespace class and a body delimiter needs its narrower BLANK class, so a conditional separated from its argument by a vertical tab or a form feed still leaves a pending recipe open and its eval refused, while `endef<VT>done` and `define<FF>inner` stay body text that delimits nothing (#410, the review of round seven's head). The whitespace make CONSUMES is that wider class at every reader that consumes one, so `define<VT>MILAN_TMPL` opens a body, `<VT>define helper` opens one, `<VT>define inner` nests one and `<VT>ifeq` leaves a pending recipe open, while make's assignment precedence still decides the opener, `define<VT>= ready` being an assignment to the name that byte forms; a built-in's name ends at the same class, so `$(eval<VT>...)`, `$(call<VT>NAME,...)` and `$(value<FF>NAME)` are the hook and the deferred reads their blank-separated spellings are (#410, the review of round eight's head). What a `$(call)` first argument NAMES is the token make cuts it down to and what a `$(value)` argument names is the whole of it, so `$(call HELPER<VT>,ready)` and `$(call HELPER junk,ready)` read `HELPER` into the closure while `$(value NAME<VT>)` names the variable those bytes spell; the same class carries the line feed where a reader scans a body's stored text, so an `$(eval<NL>...)` written in one is the hook its one-line spelling is (#410, the review of round nine's head). **Remedy:** return the value through `$(call)` and assign it, `CFLAGS += $(call tmpl,$(NAME))`, which stays green, or write the assignment at top level where its names are this file's to bind |
| No label, `goto`, `switch`, `case` or `default` in `milan_init()` or `entity_advertise()` | containment inside the choke point is not the same as being reached through its verdict test; this is the textual half, and the resolver measures the dominance itself |
| The address of `aem_loaded` may not be taken | a pointer would write the verdict with no assignment the gate can see |
| `entity_advertise` may not be exported, its address may not be formed anywhere in the firmware, and no other line of the emitted assembly may name it -- an `__attribute__((alias))` included | the arguments of a function another translation unit can name, or a table can hold, are not the arguments this unit's call sites show, so nothing here can say what verdict the choke point is entered with. The symbol-use rule is a whitelist of the four forms a private direct-called function produces, so a spelling nobody anticipated is refused rather than missed. **Remedy:** keep it `static` and call it directly |
| No indirect call and no tail transfer through a register, anywhere in the firmware | an instrument that cannot place a call edge must refuse it: a target it cannot resolve is exactly the one that could be the choke point. **Remedy:** call through a name, or model indirect targets and argument provenance completely, which is a data-flow change of its own |
| The one call edge into `entity_advertise()` must come from `milan_init()` and hand it the value `load_aem_image()` returned | the value is tracked from its PRODUCER through the emitted code, so an alias, a macro body or an assignment between the verifier and the call does not change the answer, and an argument the resolver cannot resolve is refused rather than read as verified |
| The AEM copy loop keeps a shape this range refinement can bound: a constant destination base indexed by the counter the emitted `bltu` compares | the copy store is PLACED as a bounded range inside the CRC'd buffer instead of declared as a count-keyed residual, and a loop the lattice cannot bound (`*dst++ = *src++`, a `memcpy`, a bound held in a variable) leaves a store the gate cannot place, which is a refusal. **Remedy:** keep the `dst[i] = src[i]` form, or extend the refinement to the new shape with its own degenerate-case controls |
| The RTL reset for `adp_ctrl`/`pp_ctrl_r` must be a literal with bit 0 clear | a named constant is not a value the gate can evaluate |
| `o_adp_enable`/`o_pp_enable` must be `assign <port> = <reg>[0];` | the gate censuses that exact bit |
| Renaming `load_aem_image`, `milan_init` or `configure_fabric` | the gate finds them by literal identifier; the refusal names the property and the anchor to update |
| Renaming the verdict `aem_loaded` | same, and the message says so rather than reporting a boot-order defect |
| A macro body naming `milan_write()` or `milan_reg()` | NARROWED (#408) from every CSR primitive: a store or an address formed inside a macro is one the operand census cannot place by the register it names. A read-only `#define` accessor wrapping `milan_read()` is GREEN, because each rule that reads a read fails closed when the read is hidden: a write whose value it cannot evaluate counts as SETTING bit 0, the identity sample is found only by its literal `milan_read(MILAN_ID)` call, and the identity magic must evaluate to the RTL readback default, which a read never does and which one definition per name keeps true. The body is read as the preprocessor reads it, so a body continued across lines is read whole, and a `#define` whose `#` follows a form feed or whose name a splice splits is a definition here too; before #408's second round a continued body was read one line at a time, so a continued body naming either is newly refused |
| FACTORING the CSR accessors, e.g. a `milan_set(offset, bits)` read-modify-write helper | the census places writes by RESOLVED address, and an `offset` parameter has none. **Remedy:** keep the call sites naming a register constant, or teach `CsrModel.address()` to follow the parameter, which is a data-flow change and belongs with #153 |
| Hoisting the enable mask to a named constant | the OR mask must be a value the gate can evaluate, so `\| MILAN_ENTITY_ENABLE` is not recognised as the enable write. **Remedy:** leave the mask a literal, or add the name to the firmware's `#define` table so `constant_value()` can resolve it |
| ANY change to the two commands `make` runs, a benign `AR += v` or `CC += -Wall` included | the recipe set is pinned rather than scanned for dangerous flag spellings, and the price of having no list is that benign changes are refused too. **Remedy:** add the changed command to `expected_recipes` in the gate and a mutation-table entry beside it |

The listed refusals bound only the spellings they recognise; what bounds the
values is the resolver above. **Three rows left this table with #153**,
and each left with an accepted case measured GREEN rather than with a claim:

| Retired refusal | Accepted case now measured GREEN |
|---|---|
| the guarded block holds the two enables and their `printf` and nothing else | `cdelay(64);` between the two enables |
| no `#ifdef`/`#if` outside `load_aem_image()` | `#ifdef MILAN_DEBUG_TOD` around a debug `printf` in a UART command handler |
| no multi-line `#define` anywhere in the file | a two-line `#define MILAN_BOOT_BANNER` |

**Eight more left it with #408 and #409**, two of them only outside the six
boot-path bodies, each onto a named instrument and each with an accepted
case. Every accepted case is graded GREEN in gate 1b's
accepted-case loop, and was measured RED at dev `759da623` on the retired
rule's own sentence, with and without an RV32 compiler. The labels are the
gate's own (`retired_rule_cases` in `sw/builder/test_builder.py`); this page
names no edit of its own.

| Retired refusal | Replacing instrument | Accepted case now measured GREEN |
|---|---|---|
| no `#ifdef`/`#if` reaching `milan_init()`, `configure_fabric()`, `entity_advertise()` or the three CSR accessors | every arm selection graded as the firmware it builds: the text rules on every machine, and the `-E` comparison, the compiled census and the resolver where an RV32 compiler answers | "an #ifdef around a debug printf INSIDE milan_init()"; "a benign statement in an arm the census tree drops, inside configure_fabric()" |
| no C backslash-newline that JOINS two tokens, outside the six boot-path bodies | the resolved census; inside those bodies the ban is KEPT (row above) | "a token-joining backslash-newline inside a macro body" |
| no `##` anywhere in the file, outside the six boot-path bodies and the macros they name | the same | "a ## token paste building a call outside the boot path" |
| no new file in `sw/firmware/milan_baremetal/`, a `README` included | the `-H` include-resolution measurement, by the path each pinned name was opened at and the file it reached | a `README` and a `notes.txt` beside the firmware |
| the ordered pointer-cast set | the resolver's store census | "a fifth cast to a pointer, resolving outside the window" |
| the ordered pointer-store set | the same | "a fifth store through a pointer, resolving outside the window" |
| the ordered-list comparison that made moving code a cost | the same | "parse_u64() and seconds_to_ns() exchanged, with nothing added or removed" |
| the inline-`asm` set | the same, which reads the template's own instructions | "a fifth inline-asm statement, a fence in a UART command handler" |

Four were NARROWED rather than retired, and their rows above say what still
refuses: the token-joining splice ban and the `##` ban, each to the six
boot-path bodies ("a token-joining backslash-newline inside a macro body" and
"a ## token paste building a call outside the boot path" are GREEN), the
macro-body rule ("a read-only #define accessor over milan_read()" is GREEN)
and the rule on a conditional carrying a definition ("an #ifdef/#else
choosing a #define, read in a UART command handler" is GREEN). Two were KEPT,
with the reason in each row: the directive set, and the `%:`/`??` half of the
paste ban.

### Text rules retired onto instruments (#408, #409)

**The order of events is the argument.** At PR #498's first head six text
refusals were retired onto these instruments while the hosted runners had no
RV32 compiler. On the machines that graded a merge nothing then refused what
those rules used to refuse, and a phase-2 token splice,
`milan_\`+newline+`write(ADP_CTRL, 1u)`, advertised the entity before the AEM
verdict and PASSED the complete gate there. The second head kept the rules as
a fallback arm forced over the shipping firmware, which retired nothing, and
#498 then retired nothing at all. #504 has since made both hosted builder
consumers require the pinned Bootlin SDK (`--require-rv32`; see the
[installation and cache contract](../testing/CI_WORKFLOWS.md#elaboration)),
so the instruments grade wherever a merge is graded. There is no fallback
arm: a rule forced back where the compiler is absent refuses the very edits
the retirement accepts, and the docs job runs gate 1b with every cross
compiler hidden on every commit.

| Instrument | What it sees that the text rule cannot | Text rules it replaced |
|---|---|---|
| every arm selection graded: each conditional group resolved to each of its arms, and every resulting text graded by the whole gate as a firmware of its own | the arm the product compiles, whichever its headers select, including one the census stub tree drops: a `0 &&` short-circuiting the choke point's verdict test only where `CSR_UART_BASE` is defined names nothing this file defines and moves no boot token, and is refused in the selection that takes it | the conditional-reach ban, and (narrowed) the rule on a conditional carrying a definition |
| the preprocessed unit: the same compiler under the same flags with `-E`, and each boot-path body compared as CONTENT -- the ordered boot tokens and the statements they sit in -- read both as this gate reads it and after translation phases 1 to 3 | the text the compiler is actually handed, so a macro that erases or moves a boot step is a measured disagreement rather than a construct someone had to anticipate. It compares the boot tokens and the statement count, not every name the text rules in those bodies read. The caveat is the instrument's: the unit is the one the census stub tree produces, so a macro whose definition differs in the product is outside it | none now: the token-joining splice ban and the `##` ban inside the six boot-path bodies were retired onto it and are KEPT there instead ([R272] F2 on PR #535), since a splice or a paste rebuilding a name it does not compare agrees in both texts |
| the include-resolution measurement: `-H` reports every file the preprocessor OPENED, and no pinned name may be opened beside the firmware, through a file or a link | which FILE each pinned name resolved to, which a listing of the directory cannot say at all. The caveat is the instrument's: it proves resolution in the tree it is HANDED -- the firmware's own directory plus the gate's stub header root -- so a different `-I` set, sysroot or working directory is outside it | the directory pin |
| the resolver's store census: every store the compiler emits, of every instruction class, classified by the address it RESOLVES to at every word it writes, exempting nobody | an address built with `slli`/`ori` that prints no window immediate, a store inside the address helper the census exempts by name, a `lui`-based `asm` template, a store behind a brace-less `if` that the text store set could not see at all (#495), an FP store or an RV32A AMO or SC instruction through a paged base (R228-F1 on PR #521), and a local's parked address rewritten by a union byte or half-word store or through a pointer to the local (R227-2-F1 on PR #521). Not a store made inside a called function, such as a `memset` or 64-bit atomic library call handed a window pointer; see [What the census does NOT observe](#editing-contract-for-this-firmware) | the ordered pointer-cast set, the ordered pointer-store set, the inline-`asm` set and the ordered-list comparison; the splice and `##` bans outside the six boot-path bodies |

**What still refuses what each retired rule protected** is the mutation
table. Every entry a retired rule was pinned on is re-pinned on its
replacement's own sentence, with one stated exception: the two stores planted
inside the address helper, which the cast set answered first, are answered
first now by the helper's own return-provenance rule, on every machine. The
resolver's refusal of the same two, on its own sentence, is asserted beside
them on every run where it is live, together with the census's blindness to
them. The hostile shapes the retired rules read file-wide and in arms are
controls of their own:

- the conditional-reach ban: a call name pasted, spliced, or spliced onto a
  literal address in an arm the census stub tree drops or only the product
  compiles; a struct-overlay store at the `ADP_CTRL` address in a dropped
  arm; the `0 &&` product-only arm above; a pasted enable, a fifth cast and a
  `lui`-based `asm` store in product-only arms of a UART command handler; and
  the verifier's QSPI-slot condition made false in the stub tree. On every
  machine: the AEM guard, the pre-AEM clear and the CRC comparison each put
  behind a build flag, a dropped arm inside a CSR write's argument, and
  `ADP_CTRL`'s name moved to another register by a product-only arm. And
  the arms dev's ordered sets refused whatever its directive readers saw
  ([R272] F1 on PR #535): the product-only cast in a UART command handler
  behind a form feed, a vertical tab, a NUL or lone CR line ends, a `lui`
  store and the `0 &&` arm behind a form feed, a product arm behind an
  `#else` a splice splits, and a store in the second of two groups on
  `CSR_UART_BASE`; on every machine, the pre-AEM clear dropped by a
  product-only `#ifndef` behind each of those four spellings, the verifier's
  `#else` behind a lone CR, and, for each of the other directive readers, an
  `#undef`, a second source's `#include`, a second `#error` guard and a second
  definition of `ADP_CTRL`'s name, each behind one of those spellings;
- the splice and `##` bans: inside the six boot-path bodies, where both are
  KEPT and refuse on every machine, the five phase-2 splices of
  `milan_write` in `configure_fabric()`, the pasted call name, the four
  spliced or pasted call names in arms there, and the CSR identity sample
  forged by a splice, a paste and a paste a second macro reaches; outside
  them, a spliced call name in a UART command handler and a pasted enable in
  a product-only arm there, by the resolver. `PP_CTRL`'s name redefined onto
  `ADP_CTRL` through a `#define` whose name a splice joins is refused on
  every machine by one definition per name;
- the directory pin: `command.h` and `init.h` planted beside the firmware,
  and a link planted there to a file outside this repository;
- the cast, store and asm sets: the inline-`asm` store by literal address, the
  `lui`-based template, the widened cast, the reordered cast and a pointer
  held in a local, beside the census-only and resolver-only shapes that
  needed the compiler before #409 too.

Each of those controls was shown failing with its replacement disconnected,
at the head that retired the rule, `a13b6e2e`: with the `-E` comparison, the
resolver and the census disconnected together, all twelve splice and paste
controls then passed the whole gate; with `-H` disconnected, all three
shadowing controls pass; and with the resolver and the census disconnected,
all ten cast, store, `asm`, arm-store, redefinition and flipped-verifier
controls pass. The per-selection grading pins its entries on its own sentence
and on the property the selected firmware breaks, and with it disconnected
all fifteen of that head's selection controls failed that pin with a compiler
and all six without one.

PR #535's second round measured each fix it adds the same way, over its 43
controls, with the pinned SDK and with every cross compiler hidden (32 of
them run without a compiler). With nothing disconnected all are refused on
their own pins. Removing the lexer's form-feed, vertical-tab, NUL and lone-CR
handling lets fifteen of them through or refuses them for another reason
(nine without a compiler), and
the lexer corpus then fails on its own sentence before any firmware is
graded; removing the rejoining of a name a splice splits does the same to the
spliced-`#else` arm and to the corpus. Reading macro definitions one physical
line at a time again, as the macro-body rule did, lets three through;
removing the splice and `##` bans kept inside the six boot-path bodies,
thirteen; removing the literal and trigraph refusals, four; removing one
definition per name, four. With the `-E` comparison removed, the boot step
erased by a macro of its own name passes the whole gate, and with the
relating of groups on one macro removed, the three correlated debug edits are
refused where the compiler answers. With the per-selection grading removed,
seventeen of the 43 fail their pin with a compiler and eight without one.

PR #535's third round measured its fixes over the same 43 controls and the ten
it adds, 53 in all (41 run without a compiler), and with nothing disconnected
all are refused on their own pins. Reading the digraphs before phase 2, the
round-two order, stops the gate before any firmware is graded, on the
assertion that the readers find the `#ifdef` a split `%:` spells. With the
corpora connected, the generated corpus stops it first, on its own sentence,
at `%\`, a line end, then `:ifdef`; with only the fixed corpus connected, that
corpus passes and the assertion stops it, so the generated corpus is what
measures the phase order. With the corpora and the assertion off, the
product's selection of the split-digraph arm is not found at all, and the ban
still refuses the arm itself, because the `%:` pair a splice splits is still a
pair once phase 2 has run. With that check removed as well, which is the
round-two state, the split-digraph arm passes the whole gate on every machine
and the `%:%:` paste two splices split passes without a compiler. Keeping the
byte-order mark in phase 1 lets the identity forged behind one pass the whole
gate on every machine, and the `#include` and the `#line` behind one pass
without a compiler; the fixed corpus then fails on its own sentence. Removing
the whole-file digraph ban fails five controls: with a compiler each is
refused for another reason, the two digraph arms by the grading of the
selection the readers find, and without one four of them pass. Removing the
check for a `%:` pair phase 3 reads as other tokens lets `<%:` through
without a compiler. With the page's bound on the paste ban no longer
required, the page claiming the ban reads a header's macro passes.

**What a runner with no RV32 compiler gets** is explicitly weaker, and it is
a registered `NOT RUN`, never coverage. The compiler-absent CI control keeps
this path executable. The `-E` comparison, the `-H` measurement, the compiled
half of the per-selection grading and the resolved store census all take the
census's compiler, so its stand-down stands them down together, and every
mutation pinned on them is counted as skipped rather than rejected. The
retired text rules are gone there too, so on that runner NOTHING refuses a
token-joining splice or a `##` paste outside the six boot-path bodies, a file
beside the firmware, a cast, store or `asm` the resolver would place in the
window, or the compiler half of the retired conditional-reach ban: an arm
only one build compiles whose defect no text rule reads, such as the `0 &&`
short-circuit of the choke point's verdict test above, is graded there by the
text rules alone, which do not refuse it. The same was already true there of
a cast with no `*` plus an `->` store, a store behind a brace-less `if`, and
the verifier's CFG and CRC provenance. What still grades is every surviving
text rule: the splice and `##` bans inside the six boot-path bodies, one
`#define` per name (which is what refuses a read hidden in a second
definition of the identity magic, on every machine), the macro-body rule, the
literal and trigraph refusals, the digraph ban on the whole file, the
directive readers as the two lexer corpora recorded them (not re-measured
there), and the text half of the per-selection grading.

Measured on this change, once with the pinned SDK mapped and once with every
cross compiler hidden: gate 1b refuses 264 mutations where the compiler
answers and 206 where it does not, against 217 and 182 on dev `759da623`, and
accepts 30 firmware edits and 4 Makefile edits in both, against 17 and 4. It
reads the 4985 lexer spellings, 78 fixed and 4907 generated, as recorded in
both, and re-measures them on the compiler where it answers. Without a
compiler, 33 census and resolver entries and 25 entries measuring what the
retired rules refused are counted as skipped, not rejected.

Gate 1b's verdict says which it was in its first clause -- `TEXT RULES +
INSTRUMENTS` or `TEXT RULES ONLY, AND WEAKER` -- and the stand-down is
REGISTERED, so the suite's closing line reads `ALL GATES PASS EXCEPT n NOT
RUN` and names what did not run. It is never a silent pass.

**#504 installed the selected compiler; #408 and #409 retired text rules onto
it.**
Both hosted builder calls require the RV32 instruments to execute.
The pinned Bootlin glibc SDK retains the existing `__errno_location` residual.
No additional C-library residual is accepted.
Its default ISA, `rv32imafd` with ILP32D, is the census ISA.
That ISA emits FP stores and RV32A AMO and SC instructions the shipping hart never runs.
The store census classifies them; see the [editing contract](#editing-contract-for-this-firmware).
Local mapped-prefix trials establish compatibility only.
Fresh hosted installation and trusted act need their own evidence.

## Saved state: the flash writer

The firmware is the media owner of the saved-state design
([design page](../design/SAVED_STATE_FASTCONNECT.md) sections 3, 6, 7 and
9): the fabric keeps the record image in main memory behind the processor's
NVM port (`KL_nvm_backend`), and this firmware moves it to and from the two
journal slots. Everything it needs is generated: the slot offsets come from
`FLASHBOOT_RESERVED`, the container's staging address `MILAN_NVM_IMAGE_BASE`
is the erase block directly below the response buffer inside the reserved
processor window, and the record set (`MILAN_NVM_N_*`, the per-port
channel-map cluster counts, the donor's binding base and layout version) is
one derivation in `scripts/nvm_shape.py` shared with the record-space gate and
the host test, so the firmware never restates a count. Its five waits come from
the same file (`WRITER_TIMING_MS`, published as `MILAN_NVM_*_MS`), each beside
the design-page section it answers to (#398), and each PINNED to its value
beside that bound (#465): a bound is a range and a wait is a value, so four of
the five could move with every gate green -- heartbeat 250 to 300, erase 3,500
to 3,200, program 50 to 20, restore 3,000 to 2,000 -- and only the debounce was
held, by the host test. Gate 35 carries the pin and a planted heartbeat of
300 ms, inside section 9.4's own maximum, is refused by it. The restore wait
had no bound at all and has one now: it must outlast a heartbeat period, or
the firmware's claim that it heartbeats while it waits says nothing.

**Boot.** `nvm_boot()` runs after the fabric is configured and before the
entity model is loaded. It reads both slots through the QSPI mapping and applies
the section 6.2 acceptance order to each, rule for rule as
`scripts/nvm_klj2.py` does, including the erased-record rule of section 6.1.
The newer accepted slot (a wrap-safe signed compare of `SEQ`) is copied into
the window byte for byte; when neither is accepted the firmware stages an
all-erased container at sequence 0 and reports the failing slot's verdict.
It then programs the backing store through `PP_NVM_SEL`/`PP_NVM_DATA`: the
record area's base and length, the per-port channel-map tables (framed length
and running prefix, direction distinct), the sequence, and the verdict with
the validity bit, which is asserted only after validation. A first heartbeat
follows at once, the restore walk is started through `PP_CTRL[1]` and waited
for, and the console idle hook is installed. The boot line names both slots'
verdicts, the offered sequence and the walk's `done`, `fail`, `blank` and
`backed` bits, so a blank board reads `blank=1 fail=0 backed=1`, the register
map's "blank media behind a validated image" row, and no longer `0x5B00_008C`.

**Runtime.** The idle hook runs while the console waits for a key, so a
console command that itself runs for more than the 2,000 ms liveness deadline
lets `nvm_backed` lapse until the prompt returns; with nothing outstanding the
next heartbeat heals it, with a change outstanding `nvm_stale` records the gap.
The hook heartbeats every 250 ms, half the section 9.4
maximum, and when `PP_NVM_STAT` reports `nvm_dirty` for a whole debounce
window (1,000 ms, the provisional value section 14 leaves open) with no record
operation and no commit bracket in flight, it commits: the container is sealed
under the next sequence, validated in memory (a torn record defers the commit
rather than opening a bracket over it), the bracket is opened, the
non-authoritative slot is erased, programmed page by page and read back, and
only a slot that validates at the new sequence and matches the window byte for
byte is acknowledged. The heartbeat is serviced from the erase and program
poll loops, so a datasheet-worst-case 3 s erase never lets the liveness
deadline lapse. A failed erase, program or read-back publishes `VD_ERASE`,
`VD_PROGRAM` or `VD_VERIFY` through the store's verdict nibble and withholds
the acknowledgement, so the commit deadline revokes the durability claim
instead of the firmware asserting one.

**What is proved, and where.** `sw/firmware/nvm_hosttest/test_nvm_firmware.py`
compiles this translation unit unchanged against stub headers and a host
model of the CSR face, the flash and the clock, and grades it per shipped
shape: the staged and committed containers equal the Python encoder's byte for
byte, the verdict the firmware prints for every section 6.2 refusal equals
`klj2_decode`'s for the same bytes, the A/B rule, the debounce, the three
transaction failures and the heartbeat through a 3 s erase; `--self-test`
plants four writer defects and requires each to be caught. What it cannot
prove is the board: the real LiteSPI master, the real DRAM window and the
processor writing records into it. Today only the processor's binding records
reach the store (the manager for the other seven Milan items is the donor's
open work, design page section 12.2), so a commit on the bench carries binding
records and erased spans.

## Fabric gPTP option

`board.features.fabric_gptp` defaults to `true`; every shipping YAML profile
states the owner explicitly. An option-on build elaborates `KL_gptp_shadow` with
`GPTP_PLANE_EN_P=1` and passes an absolute path to the builder-generated
microcode image. A missing `gptp:` section is rejected instead of silently
using the generator's example identity or clock defaults.

`fabric_gptp: false` is refused because every product configuration requires
the fabric publication owner. The option-off elaboration remains reachable
only through a direct `milan_soc.py` run as verification-only hardware; its
artifacts are not flashable. Product configurations emit `owner=fabric` in the
handoff manifest, and flash preflight refuses an owner of `none` or any
owner/artifact mismatch. The bare-metal
firmware exposes explicit UART commands for setting the
PHC epoch; the fabric plane owns adjfine and adjtime. When an external
grandmaster is selected, that plane steps and disciplines the PHC; a
free-running or grandmaster board uses `milan_settime` or `milan_utc` to
establish its TAI epoch.

## UART commands

The LiteX BIOS console stays at 115200 baud and provides:

| Command | Effect |
|---|---|
| `milan_status` | Read the Milan CSR identity, PTP/ADP/processor controls, processor status, AEM state and current TAI nanoseconds. |
| `milan_gettime` | Snapshot and print the fabric PHC as `TAI_NS=0x...`. |
| `milan_settime <tai-seconds> [nanoseconds]` | Set the PHC from explicit TAI seconds. Overflow and nanoseconds outside `0..999999999` are refused. |
| `milan_utc <utc-seconds> <nanoseconds> <tai-minus-utc>` | Convert an explicit UTC value and TAI-UTC offset to TAI before setting the PHC. |
| `milan_nvm` | Validate both journal slots now and print their verdicts and sequences, the authoritative slot, the staged container, the backing store's status word and the commit counters. |
| `milan_nvm commit` | Promote the staged container into the non-authoritative slot now, whether or not the store reports changes. |
| `milan_nvm wipe` | Erase both journal slots; the staged container stays, so the next boot is a blank boot. |

The firmware does not embed a leap-second table. The operator or controller
must provide the current TAI-UTC offset to `milan_utc`.

Run the post-flash test from the host connected to the console:

```console
python3 scripts/baremetal_uart_smoke.py \
  --port /dev/serial/by-id/<adapter>
```

It checks the CSR magic, paired AEM image, enable bits and PHC progression.
It does not set the clock, so a smoke run cannot disturb an established time.

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
Milan/cacheless-CPU clock are asynchronous by construction, and every bus
that crosses between them carries a crossing: Vexii's own for the peripheral
and DMA buses, the SoC's for the memory port (#359).

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
#114 plane-off baseline used 59,497 LUT, 63,092 registers, 126 BRAM
tiles and 15 DSP. The fabric gPTP plane in this build accounts for 3,364 LUT,
2,939 registers, 4.5 BRAM tiles and 4 DSP. Adding that plane to the old
baseline would require 62,861 LUT, 66,031 registers, 130.5 BRAM tiles and 19
DSP; the new option-on bare-metal build instead uses 57,111 LUT, 58,043
registers, 100 BRAM tiles and 15 DSP. The downgrade therefore funds the plane
and still frees 5,750 LUT, 7,988 registers, 30.5 BRAM tiles and 4 DSP relative
to that old-plus-plane comparison.
