[A448]

Relates to #70

#70 lane 2: the parent adopts processor `b2db3a97` (processor `main`: PR #132,
D3 lane 1, merged as `d352bbaa`, plus PR #133, lane C1), under the
[lane-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5888775832),
the [scope record](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5880276193)
and the [ruling](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5894183475)
on this lane's STOP. The processor's D3 writer now writes and restores the
scalar records (configuration, sampling rates, clock sources, both stream
formats, presentation offsets); the firmware loads the AEM image before the
restore and starts the walk on every boot path; and the parent glue, status,
harnesses, gates and documents follow PR #132's "Parent-visible for pin
adoption: rounds 1-6, consolidated" list and PR #133's declared parent edits.

## Round 4

This round answers the round-3 review
[R412-3](https://github.com/kebag-logic/milan-fpga/pull/623#issuecomment-5909975429)
under the [round-4 assignment](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5909983141).
[R413-3](https://github.com/kebag-logic/milan-fpga/pull/623#issuecomment-5909532354)
is POSITIVE. It changes no firmware, RTL or bitstream: `sw/firmware` is
byte-identical to `597dba85`, `943a3dac` and `0a80abcb`, so round 1's capture
receipt, native evidence and sweep stand.

1. **The verdict's pins claim only what the census proves, and name two
   limits** (`fa1d6e03`; R412-3 F1, accepted as a second stated limit). The
   rule comment, the `verdict_image_pins()` docstring, the verdict section and
   refusal row of `docs/integration/BAREMETAL_FIRMWARE.md`, the gate's closing
   line and the CHANGELOG no longer say that nothing writes the verdict but
   `milan_init()`'s store. They state what the pins prove: of the writes that
   reach `aem_loaded` through a relocation on its four bytes,
   `milan_init()`'s one store is the only one. Two addresses reach those bytes
   with no relocation on them, and both are stated limits, not closed:
   - **A literal address.** A store through the product's address of
     `aem_loaded`, written as a number, is placed at that number (accepted in
     round 3; #495).
   - **Another object's address, carried outside that object.** A pointer
     formed from a neighbouring static's relocation and carried past its end
     or before its start lands on the verdict while its relocation stays on
     the neighbour. A called function that writes through it is not seen,
     because the resolver records a call's arguments and does not judge them.
     Two examples are `sscanf()` with `"%s"` overrunning a four-byte static
     declared just before the verdict, and `sscanf()` handed
     `&neighbour + k` with `k` known only at run time. Nor is a store the unit
     itself makes through such a pointer at an offset the resolver places on
     the neighbour, because the model takes a store placed on another static
     not to leave it. This is the memory-safety class the standing model
     already leaves open, and gate 1b is not a memory-safety prover.

   An offset the compiler folds into the relocation lands on the verdict's
   bytes and is refused by address. A store through an offset known only at
   run time is refused as one the census cannot place.

   R412-3's `nbr_runtime_sscanf` and `pre_overrun_sscanf` stay accepted with
   the slot kept, as the second limit says, both early and through the whole
   gate 1b. Two probes of this round's own are accepted too: this unit storing
   through a local pointer to a neighbour indexed one `int` before it, and
   through a local pointer to a four-byte array declared before the verdict,
   indexed one byte past its end. That is why the limit names the unit's own
   store as well as a callee's.
2. **A break on an interior byte** (`5b4a47e9`; R412-3 F2). Gate 1b's
   fifteenth planted break names no verdict. It declares a static just after
   `aem_loaded` and hands `sscanf()` with `"%c"` that static's address one
   `int` back plus one byte. The compiler folds the offset into the
   relocation, so the break's only reference lands on the verdict's second
   byte, and it is refused on the escape pin. Before grading it, the gate
   reads the image's relocation targets directly: `nvm_boot()` must place at
   least one on the verdict's bytes and none on the first. The closing line
   prints the byte reached, `+1`. R412-3's census mutant M9, which counts only
   relocations on the verdict's first byte, passed the fourteen earlier breaks
   and the whole gate 1b. The new break now kills it. M1 to M8 stay killed, and
   the shipping head passes with the slot kept.

The reviewer's probes and census mutants, rerun at `5b4a47e9` with R412-3's
own scripts, unchanged:

- All 25 of its gate-1b probes give the same outcome as its round-3 table.
  The unplanted head is accepted with the slot kept, and refused under
  forget-on-call. `nbr_runtime_sscanf` and `pre_overrun_sscanf` are accepted,
  within the second limit. `nbr_before_sscanf` and `nbr_byte_sscanf` are
  refused on escape alone, and every other probe is refused as that table
  records, naming the same pins or rule.
- The unplanted head, `nbr_runtime_sscanf` and `pre_overrun_sscanf` each pass
  the whole gate 1b with the slot kept and "refused 15/15".
- Census mutants M1 to M9 are all killed, M9 by "the resolver accepted a
  neighbour's address folded onto an interior byte of aem_loaded".
- Two mutants of the break itself show its premise check can fail. Moved onto
  the neighbour's byte, it is refused on "byte(s) []". Moved onto the verdict's
  first byte, it is refused on "byte(s) [0]".

Round 4 validation at `5b4a47e9`, clean tree, the physical path, every gate
rc 0:

- The full builder bank with the RV32 compiler required
  (`--require-elaboration --require-rv32`). Gate 1b "refused 15/15 planted pin
  breaks on the verdict, each naming its pins, one of them reaching it only at
  byte(s) +1 of its storage", then states both limits. It ends on "ALL GATES
  PASS EXCEPT 1 NOT RUN" (gate 11's calibration build tree, as in rounds 1 to
  3).
- The same bank with every cross-compiler candidate hidden: "EXCEPT 2 NOT
  RUN", gate 1b's compiled census (by design of that arm) and gate 11.
- The check of every probe and mutant outcome above against its receipt.
- The firmware digest: `sw/firmware` is unchanged since `597dba85`,
  `943a3dac` and `0a80abcb`, and `milan_baremetal.c` equals the capture
  receipt's `product_firmware_sha256`.
- `check_nvm_capture`, the `fw_service_budget` self-test (52 grading checks),
  and R412-3's grader mutants: W0 passes, W1 to W6 are killed, X1, X2, X4 and
  X5 are killed, and X3 passes.
- The Python idiom ratchets, the evidence classifier, `git diff --check`, and
  the six Markdown gates in the pinned environment.

## Round 3

This round answers the round-2 reviews
[R412-2](https://github.com/kebag-logic/milan-fpga/pull/623#issuecomment-5905505282)
and [R413-2](https://github.com/kebag-logic/milan-fpga/pull/623#issuecomment-5905465715)
under the [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5905511808).
It changes no firmware, RTL or bitstream: `sw/firmware` is byte-identical to
`597dba85` and `943a3dac`, so round 1's capture receipt, native evidence and
sweep stand.

1. **Gate 1b decides the verdict's pins on the linked image, by address**
   (`0a80abcb`; R412-2 F1, R413-2 F1). The first attempt stopped on a
   conflict
   ([STOP](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5906387036)).
   The census compiles position-independent, the SDK's default, so every
   access to `aem_loaded` forms its full address in a register, and the
   ruled escape rule refuses the shipping firmware on that compile. The
   [ruling](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5906400668)
   takes option 1, which this commit implements.

   Gate 1b compiles the same source a second time, with the census's flags and
   stub headers plus the product's `-no-pie` (LiteX's BIOS code model). It
   links that unit alone with the census's compiler and reads the image's
   symbol and relocation tables in Python. No disassembler runs. On that
   image:
   - every relocation that lands on the four bytes of `aem_loaded`, under any
     symbol, is the upper part or a load or store in place (`%lo` on a load or
     store). A `%lo` on an `addi`, a GOT entry, a data word or any other
     relocation forms the full address and breaks the escape pin;
   - the one store in place is in `milan_init()`. The resolver, still reading
     the census's own compile, finds exactly one store on a symbol the image
     places on those bytes: `milan_init()`'s store of `load_aem_image()`'s
     return;
   - no other symbol covers those bytes, `aem_loaded` is a local object, and
     every AUIPC carries a relocation.

   The source and compile-time pins stay as early diagnostics. The rule
   comment, `docs/integration/BAREMETAL_FIRMWARE.md` and the CHANGELOG state
   the limit the ruling accepts. A store through a literal address carries no
   relocation, is placed at that number, and is outside these pins. Bringing
   the SoC's RAM map into the gate is a separate rule (#495). Round 4 (above)
   bounds the claim these texts made and states a second limit.

   Gate 1b now plants fourteen breaks. Each is refused on the verdict, naming
   every pin it lists:
   - `alias_sscanf` and `weakref_sscanf` are refused on one name and escape.
     The reviewers' own scripts showed both accepted at `943a3dac` and at
     `a033bfd8`.
   - The nine earlier breaks stay refused, and each also names the image pin
     that decides it, except the second translation unit: the image is one
     unit linked alone, so that break stays with its source pin.
   - Three new breaks plant what no earlier spelling reached. A write under
     `#ifndef __PIE__` is seen only by the image's half of the store pin,
     since the SDK defaults to PIE. The others are the address held in a data
     word, and an AUIPC with no relocation.

   The shipping firmware passes with the slot kept. Its image holds six
   references to the verdict: three upper parts, the one store in place in
   `milan_init()`, and two loads in place. Seven mutants of the census,
   outside the tree, are each killed by a control: the census breaking
   nothing, and each pin dropped, with the store pin's two halves dropped
   separately.
2. **W6 is killed** (`a033bfd8`; R413-2 F2 and S1). A fifth armed control: a
   command that starts before arming, with 10 ms of TX allowance, passes at an
   armed bound of exactly 500 ms, and one cycle more is charged. W6 is now
   killed by name. The self-test counts 52 checks, and the harness README and
   the service page match. Round 2's item 2 below now states W6 correctly.

The reviewers' probes, rerun with their own scripts at `0a80abcb`:

- All 12 R413-2 plants and all 11 R412-2 plants are refused. The unplanted
  head is accepted with the slot kept, and refused under forget-on-call.
- `alias_sscanf`, `weakref_sscanf`, `alias_addr` and `static_alias_addr` are
  refused on one name and escape. `asm_label_sscanf` and `inline_asm_la` are
  refused on escape, and `alias_decl_only` on one name.
- The alias writes are refused on the store and one name, and the other
  writes on the store. `plain_write` and `block_extern_sscanf` are refused by
  the source rules first, as before.
- The alias and weakref demos still enable the entity after a failed CRC
  when built for the host. That is the defect the gate refuses.
- R413-2's `w6_direction.py` still gives 505 ms at the head and 495 ms under
  W6.

Round 3 validation at `0a80abcb`, clean tree, the physical path, every gate
rc 0:

- The full builder bank with the RV32 compiler required
  (`--require-elaboration --require-rv32`). Gate 1b "kept the slot of
  aem_loaded across a call under the verdict's pins, decided by address on the
  linked image of the census's -no-pie compile", and "refused 14/14 planted
  pin breaks on the verdict, each naming its pins". It ends on "ALL GATES PASS
  EXCEPT 1 NOT RUN" (gate 11's calibration build tree, as in rounds 1 and 2).
- The same bank with every cross-compiler candidate hidden: "EXCEPT 2 NOT
  RUN", gate 1b's compiled census (by design of that arm) and gate 11.
- The `fw_service_budget` self-test: 52 grading checks and 14 flash checks.
- The grader mutants:
  - R412-2's W0 passes, and W1 to W6 are killed (W3, W4 and W6 by name);
  - of X1 to X5, X3 passes, since it only arms earlier and so charges more;
    the other four are killed;
  - R413-2's six rules are all killed.
- `check_nvm_capture`; the firmware digest equals `597dba85`'s, `943a3dac`'s
  and the capture receipt's.
- The Python idiom ratchets, the evidence classifier, `git diff --check`, and
  the Markdown gates in the pinned environment.

## Round 2

This round answers the round-1 reviews
[R412-1](https://github.com/kebag-logic/milan-fpga/pull/623#issuecomment-5904318669)
and [R413-1](https://github.com/kebag-logic/milan-fpga/pull/623#issuecomment-5904299081)
under the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5904325345).
That assignment accepts the service-grader rule of `18199bac` and leaves D3
section 5.3 change 3 open for the next persistence lane. Round 2 changes no
firmware, RTL or bitstream: `sw/firmware` is byte-identical to `597dba85`
(`milan_baremetal.c` sha256 `a73ecc25...0eb3`, the capture receipt's
`product_firmware_sha256`), so round 1's capture receipt, native evidence and
sweep stand.

1. **Gate 1b reads the verdict's pins on the compiled unit** (`bab4f32d`;
   R412-1 F1, R413-1 F1). `aem_loaded`'s slot crosses a call only while:
   - the resolved census places exactly one store on `aem_loaded` in the whole
     unit, `milan_init()`'s store of `load_aem_image()`'s return. The census
     is taken under the forget-on-call rule, so it does not depend on the slot
     it decides;
   - the compiler accepts the preprocessed unit with `aem_loaded` declared a
     register variable, whose address C forbids taking;
   - it is declared once as `static int aem_loaded;` in the preprocessed unit,
     defined with internal linkage and named in no other linked unit.

   Round 2 claimed the register-variable check means no expression forms the
   address, however it is spelled. R412-2 and R413-2 showed that overstated:
   a GNU `alias` or a `weakref` of `aem_loaded` forms it and passes. Round 3
   (item 1 above) decides the pins on the linked image instead.

   The comment at the rule and `docs/integration/BAREMETAL_FIRMWARE.md` state
   that and its boundary: a store the census cannot place is refused by rule
   1b, and one it places at a number, a range, the stack or another static is
   taken, as everywhere in the model, not to land on the verdict. Four planted
   controls join the five, each refused on the verdict with its pin named:
   inside `nvm_boot()`, a phase-2 line-splice write, a `##`-paste write and a
   macro-spelled write (the write pin), and a macro-spelled address handed to
   `sscanf()` (the address pin alone: the library makes that write, so no
   store in the unit shows it). Planted into the round-1 gate, all four are
   accepted. The reviewers' probes, run with their own scripts at the head:
   `splice_write`, `paste_write` and `m_macro_set` are refused on the write
   pin and `m_macro_addr` on the write and address pins; `plain_write` and
   `m_ctrl_direct` are refused by the source rule and `alias_write` by rule
   1b; the unplanted head is accepted with the slot kept and refused under
   forget-on-call.
2. **The service grader's arming is pinned** (`666f0623`; R412-1 F2). A fourth
   self-test control: an armed `milan_status` duty, with an opportunity before
   it and a serviced block inside it, whose leading gap is one cycle past the
   allowance, must be refused on both stretches. R412-1's mutants: W0 passes,
   W1 to W5 are killed, W3 and W4 by the new control. W6, the armed bound
   without the UART allowance, passed this round's self-test. It is more
   lenient than the rule, not stricter: no control separated it, because no
   armed-path row carries a UART allowance (R413-2 F2). Round 3 adds the
   control that kills it. R413-1's six rules stay killed. The self-test
   counts 51 checks, and the harness README and the service page say what the
   four controls pin.
3. **Remaining work** (R413-1 F2, R412-1 S2): the list at the end records D3
   section 5.3 change 3 and the persistence-disabled path's unpublished PHY
   link as open. Both are in the
   [#70 record](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5904331147).
4. **The reset-to-first-PHY-publication prefix** (`943a3dac`; R412-1 S1): one
   line in `docs/findings/397_SERVICE_BUDGET.md`. Only boot's 20000 ms
   comparison grades it, and the AEM-first order added the AEM copy and CRC to
   it: 316.91802 to 373.90220 ms at 1x1, 970.14222 to 1106.14204 ms at 8x8.

Round 2 validation at `943a3dac`, clean tree, the physical path, every gate
rc 0:

- Full builder bank with the RV32 compiler required (`--require-elaboration
  --require-rv32`): gate 1b "kept the slot of aem_loaded across a call under
  the verdict's three pins, read on the compiled unit, accepted the AEM-first
  base only with it kept, and refused 9/9 planted pin breaks on the verdict,
  each naming its pin". It ends on "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11's
  calibration build tree, as in round 1). With every cross-compiler candidate
  hidden: "EXCEPT 2 NOT RUN", gate 1b's compiled census (by design of that
  arm) and gate 11.
- The `fw_service_budget` self-test (51 grading checks, 14 flash checks) and
  both reviewers' grader mutants as listed in item 2.
- `check_nvm_capture`, with all seven controls detected. The firmware digest
  equals `597dba85`'s and the capture receipt's.
- The Python idiom ratchets, the evidence classifier, `git diff --check`, and
  the Markdown gates in the pinned environment.

## Items

1. **Pin** (`43ff2435`, then `504396aa` for `b2db3a97`): the gitlink;
   `syn/yosys/rom_digests.tsv` rows for both pins (content equal to
   `c951a9ff`'s: `gen_ucode.py` changes only in comments); the RTL source lists are
   derived and unchanged; the submodule boundary diagram, PNG and manifest;
   `docs/reference/SUBMODULES.md`.
2. **PR #132's consolidated list** (D3 sections 5.2 and 8.7):
   - `0a2ace1c`: `restore_closed_o`, `restore_rb_o`, `rs_cause_o[2:0]`,
     `restore_cause_o[1:0]` and `d3_unflushed_o` connected in `KL_pp_shadow.sv`
     and carried to `PP_STAT[16]`, `[17]`, `[20:18]`, `[22:21]` (no new CSR);
     `pend_i` takes the D3 writer's unflushed records (`aecp_dyn_dirty_o` stays
     a diagnostic); the processor's combined done, busy, fail and blank.
   - `862dd4da`, `1b972392`: the restore deadlines and write backoff stay
     derived inside the processor from `CLK_HZ_P`, the parent's clock; nothing
     is restated at the instance.
   - `a8668505`: the `d3_mutants.py` disposition row.
   - The counter, snapshot word 37: graded in every `sim_nxn` leg and
     documented in the register map.
   - Harnesses: `d5eff227` (`gmstep`, `gptp`/`gptp-lat`, `ax1x1gptp`),
     `f43ff09d` (the image-less legs name CLOSED), `9cb94bdb` (`sim_nxn`: the
     AECP hold and word-37 drop replace the retired degrade arm; the
     wedged-memory arm runs after the image and reads word 36 around its heal),
     `f827d8ed` (render T8), `1c89332d` (`pp_shadow`), `ac26999e` (`nvm_cosim`).
3. **Firmware** (`4333a5a0`, #70 5880276193 item 2): every boot path starts the
   restore walk; the persistence-disabled path runs it blind; the wait ends on
   done or CLOSED. `sw/firmware/nvm_hosttest/test_boot_walk.py` boots five paths
   per shape: 9 findings on the dev firmware, both planted controls caught.
4. **The ruling's option 1**:
   - `20919727`: builder gate 1b keeps `aem_loaded`'s symbol slot across a call
     only while three pins hold (one write, the verifier's; no address taken; a
     file-scope static of the one translation unit, declared once, emitted with
     internal linkage and named by no other unit), with the soundness argument
     in one comment at the rule. Round 1 read the first two on the source text;
     round 2 (`bab4f32d`) read all three on the compiled unit, and since round
     3 (`0a80abcb`, above) the linked image of a `-no-pie` compile decides. Five
     planted breaks are each refused on the verdict with the broken pin named:
     `aem_loaded = 0;` inside `nvm_boot()`, `aem_loaded = 1;` in the UART status
     handler, `&aem_loaded` taken and written through inside `nvm_boot()`, the
     verdict without `static`, and a second translation unit declaring it;
     round 2 adds four more, round 3 five and round 4 one. An AEM-first base
     is accepted only with the slot kept and refused under the old
     forget-on-call rule.
   - `a6dc7f49`: `milan_init()` is `configure_fabric`, `load_aem_image`,
     `nvm_boot`, `entity_advertise` (D3 section 5.3 change 1), with the ledger
     fact and the order block; every statement that called it open is current.
5. **PR #133's declared parent edits**: `376391bb` re-bases the crflic `[C]`
   LeaveAll counts to `>= 3` and adds a check of the restart itself (every DUT
   LeaveAll at least 10 s after the switch's preceding one): 416/0 at
   `b2db3a97`, and exactly that check fails at the previous pin `d352bbaa`
   (5 and 5 LeaveAlls, the soonest DUT LeaveAll 2,210 ms after the switch's);
   the `milan_dp` README `[C]` row, "What it cannot show" and the failing-arm
   row. `73e50787`, `b61f1d3c`: `ieee8021q.md` MRP-4..MRP-7, the compliance
   matrix 4.2.7.1 and 4.2.7.3/4.4.1, CHANGELOG.
6. **Docs** (`3852b27c` and the commits above): the compliance matrix, the
   saved-state pages, the register map, the firmware and integration pages and
   `CHANGELOG.md` describe D3 lane 1 and the AEM-first order as in the product.
7. **The native service and capture evidence** (`18199bac`, `597dba85`): see
   the service-grader section below; the capture receipt is re-recorded and
   `check_nvm_capture` passes.

## The service grader under the AEM-first order (accepted in round 2)

The round-2 assignment accepts this rule; round 2 adds the fourth control
(item 2 above). The round-1 text follows.

The native service bank's first run at `b61f1d3c` refused every plan on two
findings, "over-budget tick stretch: aem_copy_crc" and "over-budget PHY service
stretch: aem_copy_crc". The harness measures the AEM duty from the first AEM
read to the entity enable. In the old order that span followed the writer's
arming (the first heartbeat opportunity) and held the copy alone (137 ms at
8x8). Under the ruled order it starts inside the pre-heartbeat prefix and holds
the copy, the CRC and `nvm_boot()` up to the walk: 1,015 ms with no heartbeat
opportunity, because none exists before the writer does. The harness README
already says that prefix "precedes writer liveness arming" and "must not be
interpreted as an armed-writer gap".

`18199bac` makes the enforce-service verdict charge every duty's tick and PHY
stretch from the first heartbeat opportunity; a duty that starts armed keeps
its whole span, so every old-order row and the three recorded oracle traces
grade exactly as before. The receipt records the arming cycle and the armed
bound. Three self-test controls pin the rule (the unarmed prefix is not
charged; an armed stretch one cycle past the allowance is refused on both
stretches; an armed duty keeps its whole span), and three planted wrong rules
are each refused by name. The retained failing log regrades to exactly the two
findings under the old rule and to none under the new one. The ruling did not
spell this out, so it is flagged here rather than assumed.

## Validation (round 1)

Round 2's gates are in its section above. At `597dba85`, clean tree, the
physical path, every gate rc 0:

- Full builder bank with the RV32 compiler required (`--require-elaboration
  --require-rv32`), gate 1b reading "refused 5/5 planted pin breaks on the
  verdict, each naming its pin"; and with every cross-compiler candidate
  hidden. Both end on "ALL GATES PASS EXCEPT n NOT RUN" on recorded reasons
  unrelated to this lane (the gate-11 calibration tree), as at the base.
- `milan_dp`, every leg: `gmstep` 104/0, `gptp` 182/0, `gptp-lat` 182/0,
  `obj_dir` 235/0, `notify` 382/0, `crflic` 416/0 (the restart check: the
  soonest DUT LeaveAll 10,210 ms after the switch's), `nxn` 1,845/0, `nxndv`
  1,847/0, `nxn8` 3,525/0, `nxn4c` 1,845/0, `nolpf` 235/0, `prune` 33/0,
  `ax1x1` 232/0, `aclk` 191/0; `ax1x1gptp` 139/0 with its negative control. Every leg that serves the
  image reads the walk done 1, CLOSED 0 before its first AECP command.
- `nvm_cosim` 465/465 and 39 of 39 mutants killed; its lint with no
  `PINMISSING`; `pp_shadow` 606, 606, 646 and 311 checks, 0 failures.
- `milan_dp_render` (65/0 and 152/0).
- `check_nvm_capture`, the firmware host tests (five boot paths on all five
  shapes, both planted controls caught), the `fw_service_budget` self-test
  (50 grading checks).
- Yosys portability, lint, `xvlog`, the source-list, port-contract, naming,
  evidence-classifier, idiom, feature-status, submodule, boundary-diagram,
  bare-metal-only and CI-scope gates, `git diff --check`, and the Markdown gates
  in the pinned environment.

The five native groups (PR #609's recipe), at `18199bac` (the only later
commit, `597dba85`, changes the receipt and three documents): 25 arms, 65
commands, all rc 0. Service 8x8 and 1x1: all twelve plans pass with no service
finding and zero unbacked cycles, the boot reading `walk done=1 fail=0 ...
closed=0` with the AEM copied first. Mutations: `remove-dispatch` 1,051 and 350
per-line findings, `late-sample` and `no-publish` caught by name. Capture: both
contract maxima unchanged (1x1 3.88779 ms, 12.6036x; 8x8 13.23352 ms,
3.7027x); the 100 MHz comparison moves to 9.95772 ms; `byte-only` 1.8358x,
`skip-copy` and `no-traffic` caught. `docs/findings/397_SERVICE_BUDGET.md` and
the snapshot page's section 18 carry the new figures; the page's tables are
regenerated by a script first validated by reproducing all 84 rows of the
previous page from PR #609's receipts.

Timing and area:

- Out-of-context `KL_pp_shadow` at the 1x1 arrays: 25,668 LUT, 25,937 FF, 16
  RAMB36 + 2 RAMB18, 8 DSP; the D3 writer is 912 LUT / 488 FF. PR #132's
  same-session delta for lane 1 is +1,031 LUT / +559 FF / 0 BRAM / 0 DSP; C1
  adds +93 LUT / +57 FF in `KL_srp_top` (same instrument against `d352bbaa`).
- Firmware: `milan_baremetal.o` text +287 B against the base firmware, same
  toolchain; the BIOS image text +232 B (about 41% of the 128 KiB ROM).

AX7101 1x1 TDM8 place sweep at `597dba85`, PR #615's recipe at 32 threads, the
three seeds run one at a time under the Vivado lock. Worst over the four
declared corners (Slow and Fast at 0 and 85 C):

| Seed | Directive | Worst WNS ns | Worst WHS ns | Refusal gate |
|---|---|---|---|---|
| asl | AltSpreadLogic_high | +0.064 | +0.034 | accepted |
| eto | ExtraTimingOpt | +0.034 | +0.034 | accepted |
| eppo | ExtraPostPlacementOpt | +0.135 | +0.014 | accepted |

- Every seed meets WNS >= +0.030 ns and WHS >= 0 at every corner; TNS and THS
  are zero. `eto` holds the least margin.
- `eto`'s router ended at WNS -0.248 ns (`Route 35-39`, a critical warning);
  the flow's post-route physical optimization closed it to +0.034 ns before
  the signoff reports and the bitstream. `asl` and `eppo` met at the router and
  carry no critical warning.
- Each log has none of the three refused diagnostics and 112 quasi-static
  cells; the build gate accepted all three bitstreams. All four Ethernet pairs
  read `Max Delay Datapath Only` at 8 ns.
- Post-place: at most 50,265 of 63,400 LUTs (79.3%), 58,796 registers, 92.5
  BRAM tiles, 14 DSPs.

## What remains for lanes 3-5

- Lane 3: the user names (both ENTITY names and every writable ordinal), their
  trigger, replay and cold cycle.
- Lane 4: both channel-map directions and the format/map transaction; the
  parent map plane's roll-back reset.
- Lane 5: the full saved-set fault campaign and the release bench.
- Still with #70 beyond lane 2's list: the targeted 1x1 cold cycle of every
  scalar group on silicon with restored PTOF on the wire; DR2c's firmware
  transaction limit; a matched post-place area comparison (no base sweep with
  this base's build inputs exists) and the 8x8 post-place obligation (open,
  blocked, not waived).
- From PR #133 for the bench: the DUT LeaveAll cadence against the reference
  switch and first-bind latency (#76, #606).
- Open after lane 2, for the next persistence lane (the
  [#70 record](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5904331147)):
  - D3 `SAVED_STATE_MATERIALIZATION.md` section 5.3 change 3: the restore-wait
    timeout, and the enable line reporting that the fabric holds the enable.
    Lane 2 implements changes 1 and 2. Since this pin a restore can end
    CLOSED (fail, never done) with ADP dark, and `entity_advertise()` still
    prints "fabric entity enabled" whenever the AEM verdict is non-zero; the
    `closed=` field printed just before it tells the two apart (R413-1 F2).
  - The persistence-disabled path never publishes the PHY link: `nvm_started`
    is never set there, so `phy_link_tick()` never runs and the link-status
    CSR keeps its reset constant (up, board speed, full duplex). This is
    pre-existing; this PR makes that path run the walk and come up on
    defaults (R412-1 S2).
