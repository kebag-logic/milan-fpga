[A457] STOP
Head: `a033bfd85d7a07b781911fbb447fe757056dcac9` (branch `70-lane2-pin-d352`, local only; 25 commits on dev `79c36963`, one this round on `943a3dac`; processor pin `b2db3a97`, unchanged).

**Why.** Item 1 of the [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5905511808) (F1) hits one of the assignment's own STOP conditions on the compile gate 1b reads.

The census itself needs nothing beyond the pinned SDK. A prototype outside the tree does it:
- it compiles the firmware unit against the census stub headers and links it alone with the SDK's linker (relocations kept, no relaxation, a script that defines no symbol);
- it reads the image's symbol and relocation tables in Python. The only instruction bits it reads are the 7-bit opcode at each relocation site and at each AUIPC;
- it runs the resolver on the same compile's assembly for the stored value.

The conflict is the code model:
- The census compiles at the SDK's default, position-independent. Every access to `aem_loaded` forms the verdict's full address in a register (`lla`: `PCREL_LO12_I` on an `addi`).
- The base of `milan_init()`'s one store still holds that address at `call nvm_boot()`: in the linked image, `a5` is the verdict's address at `jal nvm_boot`.
- `nvm_boot()` hands `a5` unchanged to its first call, the external `bios_dispatch_hook_required()`.
- Rule 2 names "a register that survives into a call" and "an address that reaches a call argument". Read on that image, it forgets the slot. Gate 1b then refuses the shipping firmware, as it did before the #70 ruling. Passing would need a firmware change, which this round excludes.

The product does not compile that way. LiteX's `common.mak` builds the BIOS with `-no-pie`, and there the verdict's address is formed in place. The round-1 sweep's `bios.elf` has exactly three references to `aem_loaded` (`0x10000278`): `lw a0,632(a0)`, `sw a5,632(s10)` and `lw a5,632(s10)`, each after a `lui` of the upper part. No register ever holds the address.

**Options (decision needed):**
1. *(recommended)* Take the linked-image census on the census compile (`-std=gnu99 -O0 -fno-inline`, the same stubs) plus the product's `-no-pie`, linked alone by the pinned SDK. The census then requires:
   - every reference to the verdict's four bytes is an in-place load or store (`%lo` on a load or store);
   - the one store is in `milan_init()`, and the resolver on that compile's assembly finds its value to be `load_aem_image()`'s return;
   - any `%lo` on an `addi`, a GOT entry, a data word or another relocation kind forms the full address, and breaks the escape pin;
   - no other symbol overlaps the four bytes, `aem_loaded` is local, and every AUIPC carries a relocation.

   No relocated reference then puts the address in a register, so rule 2 holds physically for every reference the image's relocations show. A literal address is the limit below. The prototype keeps the slot for the shipping firmware and forgets it for all 23 reviewer plants and two of the gate's own control shapes, each naming the broken pin:
   - `alias_sscanf` and `weakref_sscanf`: one name and escape;
   - the writes (plain, splice, paste, macro, alias, the status handler): the store pin;
   - every address spelling (macro, block `extern`, asm label, inline `la`, alias): escape;
   - the declaration alone: one name;
   - `int aem_loaded;`: locality.

   The resolver keeps reading the PIC census. So the pins are decided on a second compile of the same source that differs only in the code model. The `a5` left at `call nvm_boot()` in the PIC compile is then a caller-saved register that the callee is not handed as an argument.
2. Take the census on the PIC census compile, linked, with rule 2 read under the calling convention. A register already used as the base of a load or store is spent, and a call does not receive it as an argument. An address that reaches a call, a return or a callee-saved register without serving as a base is an escape. This needs a data-flow walk and states an assumption about the compiler's argument set-up.
3. Move gate 1b's whole census compile to `-no-pie`: one compile for the resolver and the image, at the product's code model. Every gate-1b control and mutant must then be re-measured.

**A limit of every option.** The builder bank cannot link the product image: its BIOS libraries are built by LiteX, outside the pinned SDK, and under LTO `load_aem_image()` is inlined there, so its return is not a call. A literal address carries no relocation, and the unit's layout is not the product's. So a store through a hard-coded product address of `aem_loaded` is placed at a number and passes, as it does at this head. Closing that needs the SoC's RAM map in the gate, which is a separate rule.

**At this head:**
- Item 2 (R413-2 F2 and S1) is done in `a033bfd8`. A fifth armed control: a command that starts before arming, with 10 ms of TX allowance, passes at an armed bound of exactly 500 ms and is charged one cycle later. W6 is now killed by name ("an unarmed-start command's UART allowance left its armed bound"). The self-test counts 52 checks, and the harness README and `397_SERVICE_BUDGET.md:318` match.
- The PR body's W6 sentence is corrected in the lane packet.
- Gate 1b is unchanged from `943a3dac`. R413-2's own scripts (early stop) at this head accept `alias_sscanf` and `weakref_sscanf` with `kept=['aem_loaded']`, so F1 is open. The rule comment and `BAREMETAL_FIRMWARE.md:924-952,1558` are unchanged.

Gates at `a033bfd8`, clean tree, physical path, never piped, all rc 0:
- The builder bank with the RV32 compiler required (`--require-elaboration --require-rv32`, 1,020 s). Gate 1b is unchanged: it "kept the slot of aem_loaded across a call under the verdict's three pins ... and refused 9/9 planted pin breaks on the verdict". The run ends "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11's calibration tree, as in earlier rounds).
- The builder bank with every cross-compiler candidate hidden (672 s): "FULL BUILDER ABSENT PASS" and "EXCEPT 2 NOT RUN" (gate 1b's compiled census, by design of that arm, and gate 11).
- The `fw_service_budget` self-test: 52 grading checks, flash 14/0.
- The grader mutants:
  - W0 passes, and W1 to W6 are killed (W3, W4 and W6 by name);
  - X1, X2, X4 and X5 are killed; X3 passes, since it only arms earlier and so charges more;
  - R413's six rules are killed.
- `check_nvm_capture`, all seven controls detected.
- The firmware digest: `sw/firmware` has no difference from `597dba85` or `943a3dac`, and `milan_baremetal.c` sha256 `a73ecc25...0eb3` equals the capture receipt's.
- The Python idiom ratchets, the evidence classifier, `git diff --check`, and the six Markdown gates in the pinned environment.

Packet: `HANDOFF.md` and `PR-BODY.md` in the lane packet, with the prototype, its per-plant receipts, the head's gate-1b probe receipts, the product-image reference receipt and the gate receipt. No push, no PR.

After the ruling the lane needs one builder and documentation commit for item 1, then the builder bank, the reviewers' probes and the docs gates at that head. None of the three options needs a firmware, RTL or bitstream change.
