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
- **[Boot and AEM image](#boot-and-aem-image)** — The raw QSPI descriptor-image slot and the identity, copy and CRC checks that must pass before either compatibility enable bit may activate the shared AVDECC control plane.
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

1. Keep both compatibility enable bits clear, leaving the shared AVDECC
   control plane disabled while the PHC and fabric gPTP plane remain active.
2. Program the generated entity ID, model ID, station MAC, SR VID, stream
   counts, lwSRP policy, MAAP count and CRF/AAF controls.
3. Copy the raw AEM image from QSPI to the protocol processor's paired DRAM
   window and verify its CRC32.
4. After the identity check and AEM verification succeed, set the
   `PP_CTRL[0]` and legacy `ADP_CTRL[0]` compatibility enable bits. The
   controls are ORed into one shared control-plane enable, so either bit alone
   enables it.

Step 4 lives in one function and nowhere else:

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
output binding and connection onward to `ptp_timestamp.i_ptp_enable`, plus the
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

The source store instrument has an uncovered class, and the resolver is what
covers it. The cast set only recognises a cast whose text contains a `*`, and
the store set only recognises a left-hand side that starts with `*` or is
`name[...]`. A cast with no `*` combined with a `->` or subscript store is
therefore outside the source instrument:

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

Both were measured GREEN on the whole gate before the resolver existed.
The resolver
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

The census now CLASSIFIES every store the compiler emits. Four classes are
placed: an address that resolves to a number (answered by number, in or out of
the window), a stack address, the address of an object this translation unit
DEFINES (a symbol it merely references is placed by the linker, not by this
unit, so `extern volatile uint32_t r; r = 1u;` is refused), and the address
helper's own return, which is the single sanctioned way into the window and
which exactly one function may store through. The
arguments of a function this unit neither exports nor takes the address of are
resolved from its call sites, which is what places the output-pointer writes in
`parse_u64()` and `seconds_to_ns()` on the stack. Anything else is a REFUSAL,
not an omission. Four mutation-table entries carry it: the runtime-derived base
above, a second unplaceable store planted inside a function the residual already
names (so the residual is pinned by count rather than exempting a function), a
store through an `extern` symbol the linker places, and a second consumer of the
address helper's return. The classifier's fail-closed default -- a store operand
the resolver cannot even read -- is measured on a hand-written `sw rd, sym, rt`,
because GCC never emits that pseudo-instruction here and an unexercised
fail-closed branch is a claim rather than a measurement.

Two stores in the shipping firmware are still not placed. They are DECLARED in
`RESOLVER_STORE_RESIDUAL` and asserted exactly, so one more unplaceable store
anywhere -- in these two functions or in any other -- is RED, and a residual
that goes away must be retired here and in the gate in the same change:

| Store | Why it is not placed |
|---|---|
| `load_aem_image()`: `dst[i] = src[i]` | the base `MILAN_AEM_DESC_BASE` resolves and is outside the window, but the loop index is not bounded by this lattice, so the sum is not placed |
| `parse_u64()`: `errno = 0` | the base is what `__errno_location()` returns, and that function is not compiled in this translation unit |

So the property this gate proves is: no store outside those two lands in the
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
| `o_ptp_enable` is driven directly by `ptp_ctrl[0]`, the `milan_csr` instance binds it directly to `cfg_ptp_enable`, and `ptp_timestamp` directly consumes that net with ungated clocks, resets, increment/adjust/TOD controls and readback | PHC startup is independent of AEM/ADP from the CSR register through the actual timestamp consumer; the CSR harness separately proves writes to `ADP_CTRL` cannot force or gate the module output |
| External RX, `ptp_timestamp`, both enabled and bypass `RXFILT_P` arms, the filter's reset-time policy/programming seams, fabric-gPTP shadow RX/TX and timestamp feedback, `gptp_ctl_mux`, MAC-boundary arbitration and external TX handshakes use direct data, clock and reset connections | checking only an endpoint or data port misses an internal/downstream valid, policy or reset gate that makes the plane externally silent before AEM succeeds |
| CSR and datapath structural checks ignore comments, census every backtick token at any column and require each checked item to be direct in its inspected generate arm | inactive comment, preprocessor or static-generate text must not stand in for a live gated connection; a future directive or nested generate requires an elaborated checker or an explicit update to this bounded model |
| `milan_reg()` is exactly base plus its argument and `milan_read()` directly dereferences that result | every call-site claim depends on those helpers preserving the register address and loaded value; helper-body refactors must update the model and its mutations |
| Firmware `MILAN_ID` and `MILAN_ID_MAGIC` equal the comment-blanked, directive-closed RTL `A_ID` address and readback default | otherwise inactive decoy text can hide a live address/value change that teaches the token-level guard to validate a different CSR or forged identity |
| The `MILAN_ID` local is not assigned or addressed between its CSR read and mismatch guard | otherwise an intervening `id = MILAN_ID_MAGIC` forges the verdict while preserving every ordering anchor |
| The identity refusal remains the exact `if (id != MILAN_ID_MAGIC)` spelling | an equivalent comparison such as `if ((id ^ MILAN_ID_MAGIC) != 0u)` is refused because this bounded model anchors the mismatch block by that exact expression; accepting another form requires extending the recognizer and its paired controls |
| A fifth pointer cast, a fifth pointer store or a third `asm` statement | the compiled census does not cover all three, so the sets are what bound address formation; a store planted inside the address helper the census exempts by name is measured invisible to the census on every run where the census is live, which is why those 2 mutants stay reason-pinned on the cast set rather than on the helper's own return-provenance rule (that rule keeps its own mutant, "milan_reg() ignores its offset") |
| No C backslash-newline that JOINS two tokens | translation phase 2 deletes the pair and can join tokens before an offset-preserving text census; independent space, tab, form-feed and vertical-tab mutants pin every whitespace form the recognizer accepts. An ordinary continuation, which puts whitespace before the backslash, is GREEN |
| No `#ifdef`/`#if` reaching `milan_init()`, `configure_fabric()`, `entity_advertise()` or the three CSR accessors, and none carrying a `#define`/`#undef`/`#include` wherever it sits | the gate would read one arm while the compiler takes the other where a TEXT rule still reads, and the address model reads every definition as unconditional text. A conditional in a UART command handler is GREEN |
| No `#pragma`, `#line`, `#error`, `#undef` or `#include_next` | the gate has no rule for them, so it refuses rather than ignores |
| The `#include` set is exactly the eleven headers listed in the gate | a twelfth include is text in the translation unit no rule reads |
| No new file in `sw/firmware/milan_baremetal/` | a quoted include resolves against this directory first, so a file here can shadow a pinned header |
| `CFLAGS` gains only `-I$(BIOS_DIRECTORY)` | held now by the recipe pin rather than by a flag rule: the compile command is pinned whole, so any added flag changes it |
| The Makefile's `include` set is exactly its three lines | `make` can only plan fragments that exist |
| `OBJECTS` may not use `?=` | `make` treats an environment variable as defined, so `?=` lets the environment choose the object list |
| No label, `goto`, `switch`, `case` or `default` in `milan_init()` or `entity_advertise()` | containment inside the choke point is not the same as being reached through its verdict test; this is the textual half, and the resolver measures the dominance itself |
| The address of `aem_loaded` may not be taken | a pointer would write the verdict with no assignment the gate can see |
| `entity_advertise` may not be exported, its address may not be formed anywhere in the firmware, and no other line of the emitted assembly may name it -- an `__attribute__((alias))` included | the arguments of a function another translation unit can name, or a table can hold, are not the arguments this unit's call sites show, so nothing here can say what verdict the choke point is entered with. The symbol-use rule is a whitelist of the four forms a private direct-called function produces, so a spelling nobody anticipated is refused rather than missed. **Remedy:** keep it `static` and call it directly |
| No indirect call and no tail transfer through a register, anywhere in the firmware | an instrument that cannot place a call edge must refuse it: a target it cannot resolve is exactly the one that could be the choke point. **Remedy:** call through a name, or model indirect targets and argument provenance completely, which is a data-flow change of its own |
| The one call edge into `entity_advertise()` must come from `milan_init()` and hand it the value `load_aem_image()` returned | the value is tracked from its PRODUCER through the emitted code, so an alias, a macro body or an assignment between the verifier and the call does not change the answer, and an argument the resolver cannot resolve is refused rather than read as verified |
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

The listed refusals bound only the spellings they recognise; what bounds the
values is the resolver above. **Three rows left this table with #153**,
and each left with an accepted case measured GREEN rather than with a claim:

| Retired refusal | Accepted case now measured GREEN |
|---|---|
| the guarded block holds the two enables and their `printf` and nothing else | `cdelay(64);` between the two enables |
| no `#ifdef`/`#if` outside `load_aem_image()` | `#ifdef MILAN_DEBUG_TOD` around a debug `printf` in a UART command handler |
| no multi-line `#define` anywhere in the file | a two-line `#define MILAN_BOOT_BANNER` |

What carries those properties now is a measurement over resolved values, not a
narrowing by exception: control reaching an enable write is answered by
removing the choke point's verdict edge, and an enable hidden in a continued
macro body is answered by reading the compiled call, where the macro is
already expanded. Retiring the remaining store-recognition families still
requires #162's Makefile half. No further refusal family is deleted until a
replacement rejects the recorded escapes by measurement.

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
