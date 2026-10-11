# HANDOFF: lane M8a-1 for #640 (split placement's on-chip control memory)

Executor [A594]. Reviewers [R606] (internal), [R607] (external).
Branch `640-m8a` from dev `e8454e2751d05b02ee8e5a571857589ab358ab86`; the manager pushed `08b90b68` as PR #721. Round 2's commits are local, not pushed.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100371426
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100426002
STOP (round 1): https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6101473717 (its handoff and PR body are kept in `stop-round/`)
Ruling: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6101485877
REVIEW READY (M8a-1): https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6104411638

## Round 2 (M8a-1, answering R606-1 and R607-1)

Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6105011666
Reviews answered: R606-1 (PR #721 comment 6104999232) and R607-1 (PR #721 comment 6105008317), both NEGATIVE on MINORs only.
Base of this round: `08b90b6859b0a7d7f172c7ae29745248895d9aa9` (`5d532e9d` plus the manager's merge of dev `ac2c5e77`). New commits only, no rebase or amend, not pushed.
REVIEW READY (round 2): https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6106342513 (text in `evidence-r2/review-ready.md`)

**Status: REVIEW READY (M8a-1 round 2).** Head `76605880a20005cbc2acad1b23ba2ccebde64ca8`: three commits on `08b90b68`, local, not pushed. Every A10 item is answered (R2.1). Every gate the change touches passed, rc 0 (R2.7). R607-1's twelve mutants are all KILLED, and R606-1's `main()`-stage mutant turns the SoC test red (R2.5). What was not taken is listed in R2.1 and R2.8.

- `be431eec9a018f56e558bdbc97407255189b12ce` Register every split memory refusal rule, refuse writable data in rom and truncated ELFs by name, and require a named failure for each rule removed, the SoC build's controls and the whole decoded window (#640)
- `516d7fb87c530f16dcf512c85a528da6f76e14ea` State the 56-tile ledger total as 116 tiles leaving 5.5, the ruled firmware limit, and the 231 LUT cells as the rom region with its decode (#640)
- `76605880a20005cbc2acad1b23ba2ccebde64ca8` Say which split memory rules the SoC build runs while it builds the memory

9 files, +843 / -245 over the round (`git diff --stat 08b90b68..76605880`).

- R2.1 Findings and the change that answers each
- R2.2 Changes, with file:line
- R2.3 The rule registry and the standing mutation check
- R2.4 The SoC build test
- R2.5 Reviewer mutants and probes re-run
- R2.6 Docs and figures
- R2.7 Gate table (round 2)
- R2.8 Not done, and why

### R2.1 Findings and the change that answers each

| Finding | Lens (reviewer's) | Change |
|---|---|---|
| R606-1-F1: writable initialised data in `rom` accepted | Robustness, Tests | New rule `writable in rom` (`memory map`), `ctrl_memory.py:271-273`; `Section.writable` from `SHF_WRITE`; unit arm (`.data` linked to run in rom) and the link plant `} > sram AT > rom` to `} > rom` (R606-1's own edit) |
| R606-1-F2 / R607-1-F1: hole graded at one address; five mutants survive | Tests | Simulation at the largest image's sram banks (64+32+8+4+2 KiB) for both regions; 47 hole addresses per region from the first word past the banks to word `0xFFFF` (the 256 KiB decoded window, past 224 KiB), incl. `0x8000`, `0x8001`, `0x8000 + words - 1`, `0xDFFF`, `0xE000`; every answer must be err alone (ack, both or none fail); 215 alias cells read back; back-to-back read presented on the cycle after err must ack with its data, both regions |
| R607-1-F1: budget boundary, three refusals unarmed | Tests | 56.0 RAMB36 accepted and 56.5 refused (`BUDGET_BSS`); arms for NOBITS in rom, shared load address, no bytes at entry; every rule in `ctrl_memory.RULES` has an arm and a mutant, enforced by the test |
| A10 item 1: one list, a standing mutation check | Tests | `ctrl_memory.RULES` (16 rules); `test_ctrl_memory.py` register arm requires `SPLIT_CONTROL_MEMORY.md` section 3's table to equal it, every rule to have a refusal arm and a mutant; 40 mutants each rebuild one definition from its own source with one edit and must be killed by a named FAIL |
| R606-1-F3 / R607-1-S1: SoC hookup untested | Tests | SoC arm: `milan_soc.py`'s own `main()` in a child process on the shipping 1x1 config's argv, exporting with `--no-compile-software`: three controls refused by rule before any Verilog, both lone flags refused (rc 2, the pairing message), and the passing split export checked (banks, no BIOS memories, rom init = image, `csr.csv` regions, Builder handed no BIOS and no shipping firmware). R606-1's `main()`-stage mutant is mutant 38 and turns it red |
| R607-1-S2 (A10 item 3, required): truncated ELF unnamed | Robustness | Rule `elf truncated` (`memory map`): every header, table and symbol read via `_unpack` (`ctrl_memory.py:185-190`), names via `_string` (`:193-199`), load segments (`:216-219`); four arms (cut in header, cut to half, segment past end, name past end) |
| R606-1-F4 = R607-1-F2: 56-tile sentences, `AREA_BUDGET.md:382`, lane row | Docs | `MARK_II_AREA_PLAN.md:861-862` and `AREA_BUDGET.md:265`: 116 tiles, 5.5 below; `AREA_BUDGET.md:382-383`: the ruled limit, up to 56 RAMB36 as mapped, and 53 out of context; `MARK_II_AREA_PLAN.md:1046`: the ruled 56-tile allocation |
| R606-1-F5: 231-LUT attribution | Docs | `SPLIT_CONTROL_MEMORY.md:157-163` and `MARK_II_AREA_PLAN.md:821`: 231 LUT cells is the `rom` region (logic bank plus bank decode and read multiplexer); basis named (LUT primitives; 220 Slice LUTs in `report_utilization`); decode cost shown (36 LUT cells for two rom banks with none in logic, 97 for the largest sram); M8a-2 weighs the bank's share only |
| R607-1-F3 (= R606-1-R2): PR body stale | Docs | PR body names the round-2 head, the base `08b90b68` = `5d532e9d` + merge of dev `ac2c5e77`, and the aggregate 7 of 7 |
| R607-1-R1 | Docs (residue) | `SPLIT_CONTROL_MEMORY.md:149-150`: the exact text |
| R607-1-R2 | Docs (residue) | Column header `LUT cells / FF` (`SPLIT_CONTROL_MEMORY.md:139`); "most of each point's LUT cells: 231 of the largest point's 328" (`:157`); "in 231 LUT cells" (`MARK_II_AREA_PLAN.md:821`). Each sentence also carries F5's attribution, since the unit change alone keeps the attribution F5 refutes |

Not taken (not in A10's list): R606-1-R1 ("measured" wording with M2's unused +2 allowance, `AREA_BUDGET.md:263`, `MARK_II_AREA_PLAN.md:832`), R606-1-S1 (trap vector), R606-1-S2 (an assertion on `rom_words` length). R607-1-S3 is the manager's separate issue.

### R2.2 Changes, with file:line (round 2)

| File:line | Change |
|---|---|
| `sw/litex/ctrl_memory.py:24-28` | Docstring: RULES and the test's requirement |
| `sw/litex/ctrl_memory.py:59` | `_SHF_WRITE` |
| `sw/litex/ctrl_memory.py:64-94` | `Rule` (check, refuses) and `RULES`: 16 rules keyed by name, in the doc table's order |
| `sw/litex/ctrl_memory.py:97-104` | `Refusal(rule, detail)`: `.rule` and `.check` (looked up in RULES, so an unregistered rule cannot refuse); the message is unchanged, `"<check>: <detail>"` |
| `sw/litex/ctrl_memory.py:139` | `Section.writable` |
| `sw/litex/ctrl_memory.py:185-199` | `_unpack` and `_string`: bounds-checked reads, refused as `elf truncated` |
| `sw/litex/ctrl_memory.py:202-246` | `read_elf`: `elf class`, `elf machine`, every read bounds-checked, load segments checked, `writable` read |
| `sw/litex/ctrl_memory.py:243-249` | `_overlap(rule, spans)`: refuses by its rule (`regions`, `addresses`, `initial bytes`) |
| `sw/litex/ctrl_memory.py:253-276` | `check_map`: each refusal names its rule; new `writable in rom` (`:271-273`) |
| `sw/litex/ctrl_memory.py:288`, `:322-330` | `budget`; `stage symbol`, `stage size` |
| `sw/litex/milan_soc.py:2743` | `add_ctrl_memory`'s CPU check refuses as `cpu origins` (was `reset entry` as the only argument; the check name stays `reset entry`) |
| `sw/litex/test_ctrl_memory.py` | Rewritten around the rule register: arms 1-7 in the docstring (`:4-46`); `refused` matches rule and check and names any other exception (`:106-118`); `Layout`/`elf`/edits (`:199-272`); `FakeSoC` (`:275-292`); `refusal_arms` (`:295-336`); `check_arms` (`:339-373`); simulation (`:376-510`); link (`:515-559`); SoC build (`:564-680`); `PROPERTIES`, `MUTANTS` (`:683-790`); `mutated` (`:793-811`); register (`:824-844`); mutants (`:847-868`); `run_arm` (`:871-878`); `main` (`:881-906`) |
| `scripts/check_py_idiom.py:174-197` | `DYNAMIC_EXEC_INVENTORY` gains `sw/litex/test_ctrl_memory.py` with its guard (the edit matches once; `ast.parse` of the result is exactly one definition of that name; runs in that module's namespace); the comment counts the fourth entry |
| `docs/design/SPLIT_CONTROL_MEMORY.md:62-110` | Section 3: the per-rule table (= RULES), the boundary, the test's register, mutation check and SoC arm |
| `docs/design/SPLIT_CONTROL_MEMORY.md:139-163` | Section 5: `LUT cells / FF`; R607-1-R1 text; the 231 attribution and basis |
| `docs/design/MARK_II_AREA_PLAN.md:821, 861-862, 1046`; `docs/design/AREA_BUDGET.md:265, 382-383` | Ledger figures (R2.6) |
| `docs/testing/TESTING.md:697-714`; `docs/testing/CI_WORKFLOWS.md:1185-1190` | The test's arms; the SoC arm's needs in the hosted job (PyYAML; one more VexiiRiscv argument set) |

The register's existing check names are unchanged (`reset entry`, `memory map`, `memory-map overlap`, `allocation over budget`, `staging buffer`), so every log line and refusal message the reviews quote still reads the same; only the rule is added.

### R2.3 The rule registry and the standing mutation check

- `ctrl_memory.RULES` is the one list. `Refusal` takes a rule key and looks its check up there.
- The register arm (`test_ctrl_memory.py:830-844`) fails CI when:
  - `SPLIT_CONTROL_MEMORY.md` section 3's table differs from RULES in any row, column or order;
  - a rule has no refusal arm in `refusal_arms`;
  - a rule has no mutant in `MUTANTS`;
  - a mutant names neither a rule nor a listed property.
- A mutant (`mutated`, `:793-811`) rebuilds one function or class from `inspect.getsource` with one literal edit, which must match exactly once; the result must parse to that one definition. It is patched in for its arm (in-process for `banks`, `checks` and `sim`; in the SoC child for `soc`) and must produce at least one FAIL; the first one is printed by name. An edit that no longer matches its source is itself a FAIL.
- The 40 mutants, at `be431eec` (`test_ctrl_memory.step1.log`):

| # | Mutant | Rule or property | Edit (`file:definition`: old to new) | Arm | Killed by (first named FAIL) |
|---:|---|---|---|---|---|
| 1 | elf class weakened | elf class | `sw/litex/ctrl_memory.py:read_elf`: `if data[:6] != b"\x7fELF\x01\x01":` to `if data[:4] != b"\x7fELF":` | checks | an ELF64 file: accepted, expected 'memory map' rule 'elf class' |
| 2 | elf machine off | elf machine | `sw/litex/ctrl_memory.py:read_elf`: `if machine != _EM_RISCV:` to `if False:` | checks | an x86 ELF32 file: accepted, expected 'memory map' rule 'elf machine' |
| 3 | truncated fields read | elf truncated | `sw/litex/ctrl_memory.py:_unpack`: `if offset + struct.calcsize(layout) > len(data):` to `if False:` | checks | an ELF cut inside its header: raised error (unpack_from requires a buffer of at least 52 bytes for unpacking 36 bytes at offset 16 (actual buffer s... |
| 4 | truncated segments read | elf truncated | `sw/litex/ctrl_memory.py:read_elf`: `if offset + filesz > len(data):` to `if False:` | checks | a load segment past the end of the file: accepted, expected 'memory map' rule 'elf truncated' |
| 5 | unterminated names read | elf truncated | `sw/litex/ctrl_memory.py:_string`: `if end < 0:` to `if False:` | checks | a section name past the end of the file: accepted, expected 'memory map' rule 'elf truncated' |
| 6 | load address read as the run address | load address | `sw/litex/ctrl_memory.py:read_elf`: `return paddr + vma - vaddr` to `return vma` | checks | the good image is planned: raised Refusal (memory map: .data's initial bytes load at 0x10000000, outside rom, the only region the bitstream initial... |
| 7 | entry address off | entry address | `sw/litex/ctrl_memory.py:check_map`: `if image.entry != rom.origin:` to `if False:` | checks | an image entering away from the reset address: accepted, expected 'reset entry' rule 'entry address' |
| 8 | entry bytes off | entry bytes | `sw/litex/ctrl_memory.py:check_map`: `if not any(s.loaded and s.vma <= image.entry` to `if False and not any(s.loaded and s.vma <= image.entry` | checks | an image with no initial bytes at the reset address: accepted, expected 'reset entry' rule 'entry bytes' |
| 9 | outside regions off | outside regions | `sw/litex/ctrl_memory.py:check_map`: `if home is None:` to `if False:` | checks | a section outside rom and sram: accepted, expected 'memory map' rule 'outside regions' |
| 10 | loads outside rom off | loads outside rom | `sw/litex/ctrl_memory.py:check_map`: `if s.loaded and not rom.holds(s.lma, s.lma + s.size):` to `if False:` | checks | initial bytes of .data left in sram, which nothing initialises: refused by 'allocation over budget' rule 'budget' (allocation over budget: 65548.5 ... |
| 11 | nobits in rom off | nobits in rom | `sw/litex/ctrl_memory.py:check_map`: `if not s.loaded and home is rom:` to `if False:` | checks | .bss reserved in rom: refused by 'memory map' rule 'writable in rom' (memory map: .bss is writable and runs at 0x00002f44 in rom, which drops write... |
| 12 | writable in rom off | writable in rom | `sw/litex/ctrl_memory.py:check_map`: `if s.writable and home is rom:` to `if False:` | checks | .data linked to run in rom: accepted, expected 'memory map' rule 'writable in rom' |
| 13 | region overlap off | regions | `sw/litex/ctrl_memory.py:check_map`: `_overlap("regions", ` to `0 and _overlap("regions", ` | checks | PLANTED: a memory-map overlap (sram moved into rom): refused by 'memory map' rule 'outside regions' (memory map: .data [0x10000000, 0x10000040) is ... |
| 14 | address overlap off | addresses | `sw/litex/ctrl_memory.py:check_map`: `_overlap("addresses", ` to `0 and _overlap("addresses", ` | checks | PLANTED: a memory-map overlap (.bss over .data): accepted, expected 'memory-map overlap' rule 'addresses' |
| 15 | load-address overlap off | initial bytes | `sw/litex/ctrl_memory.py:check_map`: `_overlap("initial bytes", ` to `0 and _overlap("initial bytes", ` | checks | .data's initial bytes loading over .rodata's: accepted, expected 'memory-map overlap' rule 'initial bytes' |
| 16 | budget off | budget | `sw/litex/ctrl_memory.py:plan`: `if need.tiles > budget:` to `if False:` | checks | PLANTED: an allocation over budget (215,000 bytes of .bss: 58 RAMB36, each region inside its own): accepted, expected 'allocation over budget' rule... |
| 17 | budget refuses exactly 56 | budget | `sw/litex/ctrl_memory.py:plan`: `if need.tiles > budget:` to `if need.tiles >= budget:` | checks | an allocation of exactly 56 RAMB36 is accepted: raised Refusal (allocation over budget: 56 RAMB36 (rom 12068 bytes in 12288, sram 217088 bytes in 2... |
| 18 | budget half a tile slack | budget | `sw/litex/ctrl_memory.py:plan`: `if need.tiles > budget:` to `if need.tiles > budget + 0.5:` | checks | an allocation of 56.5 RAMB36, half a tile over: accepted, expected 'allocation over budget' rule 'budget' |
| 19 | budget 1.5 tiles slack | budget | `sw/litex/ctrl_memory.py:plan`: `if need.tiles > budget:` to `if need.tiles > budget + 1.5:` | checks | an allocation of 56.5 RAMB36, half a tile over: accepted, expected 'allocation over budget' rule 'budget' |
| 20 | stage symbol off | stage symbol | `sw/litex/ctrl_memory.py:check_stage`: `if STAGE_SYMBOL not in image.symbols:` to `if False:` | checks | an image with no nvm_stage: raised KeyError ('nvm_stage'), expected 'staging buffer' rule 'stage symbol' |
| 21 | stage size off | stage size | `sw/litex/ctrl_memory.py:check_stage`: `if size != stage:` to `if False:` | checks | PLANTED: a staging buffer sized for another shape (1x1 image, 8x8 stage): accepted, expected 'staging buffer' rule 'stage size' |
| 22 | stage accepts a larger buffer | stage size | `sw/litex/ctrl_memory.py:check_stage`: `if size != stage:` to `if size < stage:` | checks | PLANTED: a staging buffer sized for another shape (8x8 image, 1x1 stage): accepted, expected 'staging buffer' rule 'stage size' |
| 23 | stage accepts a smaller buffer | stage size | `sw/litex/ctrl_memory.py:check_stage`: `if size != stage:` to `if size > stage:` | checks | PLANTED: a staging buffer sized for another shape (1x1 image, 8x8 stage): accepted, expected 'staging buffer' rule 'stage size' |
| 24 | banks smallest first | bank order | `sw/litex/ctrl_memory.py:banks`: `reversed(range(granules.bit_length()))` to `range(granules.bit_length())` | banks | 840 needs: power-of-two granule banks, largest first, under one granule spare (first wrong: [4097, 4581, 5090]) |
| 25 | cpu origins off | cpu origins | `sw/litex/milan_soc.py:add_ctrl_memory`: `if (soc.cpu.reset_address, soc.mem_map["sram"]) != (ctrl_...` to `if False:` | checks | a CPU resetting away from rom's origin: accepted, expected 'reset entry' rule 'cpu origins' |
| 26 | cpu origins read the reset address only | cpu origins | `sw/litex/milan_soc.py:add_ctrl_memory`: `if (soc.cpu.reset_address, soc.mem_map["sram"]) != (ctrl_...` to `if soc.cpu.reset_address != ctrl_memory.ROM.origin:` | checks | a CPU whose sram is not at sram's origin: accepted, expected 'reset entry' rule 'cpu origins' |
| 27 | rom left uninitialised for the Builder | no BIOS build | `sw/litex/milan_soc.py:add_ctrl_memory`: `soc.integrated_rom_initialized = True` to `soc.integrated_rom_initialized = False` | checks | add_ctrl_memory tells LiteX's Builder that rom holds its contents, so it builds no BIOS |
| 28 | decode one bit short | decode width | `sw/litex/milan_soc.py:CtrlMemory`: `low = (region.size - 1).bit_length() - 2` to `low = (region.size - 1).bit_length() - 3` | sim | rom answers err alone at all 47 addresses from word 0x6e00 to the window's top 0xffff (first wrong: [('0x8000', 'ack'), ('0x8001', 'ack'), ('0x81f1... |
| 29 | hole compares one bit short | hole width | `sw/litex/milan_soc.py:CtrlMemory`: `slaves.append((lambda a: a[:low] >= first, hole))` to `slaves.append((lambda a: a[:low - 1] >= first, hole))` | sim | rom answers err alone at all 47 addresses from word 0x6e00 to the window's top 0xffff (first wrong: [('0x8000', 'none'), ('0x8001', 'none'), ('0x81... |
| 30 | hole starts a word late | hole start | `sw/litex/milan_soc.py:CtrlMemory`: `slaves.append((lambda a: a[:low] >= first, hole))` to `slaves.append((lambda a: a[:low] > first, hole))` | sim | rom answers err alone at all 47 addresses from word 0x6e00 to the window's top 0xffff (first wrong: [('0x6e00', 'none')]) |
| 31 | hole answers nothing | hole answer | `sw/litex/milan_soc.py:CtrlMemory`: `self.sync += hole.err.eq(hole.cyc & hole.stb & ~hole.err)` to `self.sync += hole.err.eq(0)` | sim | rom answers err alone at all 47 addresses from word 0x6e00 to the window's top 0xffff (first wrong: [('0x6e00', 'none'), ('0x6e01', 'none'), ('0x71... |
| 32 | err held a second cycle | err pulse | `sw/litex/milan_soc.py:CtrlMemory`: `hole.err.eq(hole.cyc & hole.stb & ~hole.err)` to `hole.err.eq(hole.cyc & hole.stb)` | sim | rom: a read presented on the cycle after an err acks with its own data ((('err', 0), ('err', 4175417604))) |
| 33 | rom banks from the image start | rom contents | `sw/litex/milan_soc.py:CtrlMemory`: `words[first:first + depth]` to `words[0:depth]` | sim | rom reads its image at the first, second and last word of each of 5 banks (64, 32, 8, 4, 2 KiB) |
| 34 | a writable rom | read-only rom | `sw/litex/milan_soc.py:CtrlMemory`: `read_only=words is not None` to `read_only=False` | sim | a write to rom changes nothing |
| 35 | BIOS ROM built | no BIOS memory | `sw/litex/milan_soc.py:MilanSoC`: `kwargs.update(integrated_rom_size=0, integrated_sram_size...` to `kwargs.update(integrated_sram_size=0)` | soc | SoC build: the 8x8 stage in the 1x1 build is refused by rule 'stage size' before any Verilog is written (rc 1: AssertionError: ) |
| 36 | BIOS SRAM built | no BIOS memory | `sw/litex/milan_soc.py:MilanSoC`: `kwargs.update(integrated_rom_size=0, integrated_sram_size...` to `kwargs.update(integrated_rom_size=0)` | soc | SoC build: the 8x8 stage in the 1x1 build is refused by rule 'stage size' before any Verilog is written (rc 1: AssertionError: ) |
| 37 | control memory not added | memory hookup | `sw/litex/milan_soc.py:MilanSoC`: `add_ctrl_memory(self, Path(ctrl_firmware))` to `None` | soc | SoC build: an allocation over budget is refused by rule 'budget' before any Verilog is written (rc 1: AttributeError: 'MilanSoC' object has no attr... |
| 38 | main() staging check removed | stage in main | `sw/litex/milan_soc.py:main`: `ctrl_memory.check_stage(soc.ctrl_image,` to `(soc.ctrl_image,` | soc | SoC build: the 8x8 stage in the 1x1 build is refused by rule 'stage size' before any Verilog is written (rc 0: None) |
| 39 | flag pairing off | pairing | `sw/litex/milan_soc.py:main`: `if args.ctrl_mailbox != (args.ctrl_firmware is not None):` to `if False:` | soc | SoC build: --ctrl-mailbox alone is refused, '--ctrl-mailbox and --ctrl-firmware go together' (rc 1: ValueError: --ctrl-mailbox needs --ctrl-firmwar... |
| 40 | shipping firmware linked | no shipping firmware | `sw/litex/milan_soc.py:main`: `if args.software_profile == "baremetal" and not args.ctrl...` to `if args.software_profile == "baremetal":` | soc | the split build adds no shipping firmware |

- The planted defects of the refusal arms, each refused by its own rule (34 lines in the `rules` arm); a refusal by another rule, an unnamed exception, or acceptance is a FAIL:
  entry 0x100 (`entry address`); `.text` at 0x100 (`entry bytes`); a CPU resetting to 0x100, and sram at 0x2000_0000 (`cpu origins`); a text file, an empty file, ELF64, big-endian (`elf class`); x86 (`elf machine`); cut to 40 bytes, cut to half, a segment of 1 MiB past the end, a section name at 2^30 (`elf truncated`); `.bss` at 0x4000_0000 (`outside regions`); `.data` loaded in sram (`loads outside rom`); `.bss` in rom (`nobits in rom`); `.data` running in rom (`writable in rom`); sram moved into rom (`regions`); `.bss` over `.data` (`addresses`); `.data` loaded over `.rodata` (`initial bytes`); 58 RAMB36 and 56.5 RAMB36 (`budget`); no `nvm_stage` (`stage symbol`); 1x1 image against the 8x8 stage and the reverse (`stage size`).
- Accepted: the good image, exactly 56.0 RAMB36 (`BUDGET_BSS` = 208,832 B of `.bss`: rom 12,288 + sram 217,088 = 229,376 B), the shape's own stage, and `add_ctrl_memory` on a `FakeSoC` with the right origins (rom rx and sram rwx as `CtrlMemory`, each 224 KiB, and `integrated_rom_initialized`).

### R2.4 The SoC build test

`soc_arms` (`test_ctrl_memory.py:658-680`), each case one child process (`soc_child`, `:582-610`) running `milan_soc.main()` on `endstation_builder.emit_soc_argv` for `configs/endstation_ax7101_1x1_tdm8.yaml` (after `endstation_builder.build`) plus `--output-dir <tmp> --no-compile-software`, `PYTHONHASHSEED=0`:

| Case | Extra argv | Required |
|---|---|---|
| allocation over budget | `--ctrl-mailbox --ctrl-firmware` an image of 58 RAMB36 | rc 1, rule `budget`, no Verilog |
| memory-map overlap | the same with `.bss` at `.data` | rc 1, rule `addresses`, no Verilog |
| wrong-shape staging | the 8x8 stage (13,264 B) in the 1x1 build | rc 1, rule `stage size`, no Verilog |
| `--ctrl-mailbox` alone | | rc 2, the pairing message, no Verilog |
| `--ctrl-firmware` alone | the good image | rc 2, the pairing message, no Verilog |
| the split build | `--ctrl-mailbox --ctrl-firmware` the good image | rc 0; the export's 32-bit memories are exactly `rom_bank0..` and `sram_bank0..` at the plan's depths, no `rom` or `sram` (the BIOS memories); the rom bank init files concatenate to `rom_words`; `csr.csv` maps rom `0x00000000` and sram `0x10000000`, 229,376 B each; the Builder is handed `integrated_rom_size` 0, `integrated_sram_size` 0 and `integrated_rom_initialized` True, and no `libmilan_baremetal` package or directory |

The child records what LiteX's `Builder.build` is handed and then calls it unchanged. `--no-compile-software` skips only LiteX's software compile; with it the Builder would compile no BIOS anyway, so the BIOS decision is read from the flag the Builder reads. Each case runs in about 3 s here; the six SoC mutants run the whole arm again.

### R2.5 Reviewer mutants and probes re-run

**R607-1's harness** (`review-evidence/640-m8a-r1/reviews/R607-1/scripts/mutants.py` from the `640-m8a-review-evidence` branch at `6609230f`, run unmodified as `mutants.py <this worktree> <out> <LiteX python> --jobs 1` at `be431eec`; one job because every mutant tree shares the builder output through the worktree's `sw/builder/out` link). Receipts: `evidence-r2/r607-mutants/` (`mutants.txt`, one log per mutant).

| Mutant | Round 1 | Round 2 | First named FAIL at `be431eec` |
|---|---|---|---|
| `budget_slack_1p5` | SURVIVED | KILLED (5) | an allocation of 56.5 RAMB36, half a tile over: accepted |
| `budget_ge` | SURVIVED | KILLED (6) | an allocation of exactly 56 RAMB36 is accepted: raised Refusal |
| `nobits_in_rom_off` | SURVIVED | KILLED (2) | .bss reserved in rom: refused by rule 'writable in rom' (expected 'nobits in rom') |
| `lma_overlap_off` | SURVIVED | KILLED (1) | .data's initial bytes loading over .rodata's: accepted |
| `no_bytes_at_entry_off` | SURVIVED | KILLED (2) | an image with no initial bytes at the reset address: accepted |
| `regions_overlap_off` | KILLED | KILLED (1) | sram moved into rom: refused by rule 'outside regions' |
| `lma_identity` | ERROR (crash, no FAIL line) | KILLED (18) | the good image is planned: raised Refusal |
| `stage_lt` | KILLED | KILLED (5) | 8x8 image, 1x1 stage: accepted; also the SoC build exports the 8x8 stage in the 1x1 build |
| `low_minus1` | SURVIVED | KILLED (5) | rom answers err alone ... first wrong `0x8000` ack |
| `hole_gt` | KILLED | KILLED (5) | rom ... first wrong `0x6e00` none |
| `rom_init_offset` | KILLED | KILLED (3) | rom reads its image ...; the rom banks' init files hold the image word for word |
| `err_held` | SURVIVED | KILLED (4) | rom: a read presented on the cycle after an err acks with its own data: `('err', ...)` |

All twelve are KILLED by a named FAIL line from a base arm; the harness's edit also stops one of the test's own mutants matching, which adds a FAIL line of its own.

**R606-1's mutants.** `low_minus_one` and `hole_narrow` are the test's mutants 28 and 29; `main() staging check removed` is mutant 38. All three are killed (table above).

**Probes, re-run at `516d7fb8`** (scripts from the same branch, untouched; receipts in `evidence-r2/probes/`):

| Probe | Round 1 head | This head |
|---|---|---|
| R606-1 `probe_writable_rom.py` (`.data` linked `} > rom`) | ACCEPTED | `REFUSED memory map: ... .data is writable and runs at 0x00000070 in rom, which drops writes` |
| R607-1 `probe_malformed.py` on the largest image | truncated-64, truncated-half: unnamed `struct.error` | all seven inputs `Refusal[memory map]`; 54.5 accepted at budget 54.5, refused at 54.0 |
| R607-1 `probe_ctrlmem_sim.py` on the largest image | PASS | PASS (A-E) |
| R606-1 `probe_region_top.py` | PASS | PASS (115 addresses, 0 non-err, 0 aliased) |

### R2.6 Docs and figures

- 56-tile line: `87.5 - 6.5 + 6 - 18 + 56 + 2 - 11 = 116`, leaving 5.5 below 121.5 (plan `:861-862`, budget `:265`).
- `AREA_BUDGET.md:382-383`: "The ruled firmware limit is up to 56 RAMB36 as mapped. M8a-1's 53 at the largest shape is an out-of-context mapping, not integrated consumption."
- `MARK_II_AREA_PLAN.md:1046`: "reconcile the ruled 56-tile firmware allocation and measured linked storage".
- 231: `ctrl_memory_ooc.tsv` column `LUT` (`PRIMITIVE_GROUP == LUT`) for `s8i2_rom`; `util/s8i2_rom_utilization.rpt` Slice LUTs 220; `s1i2_rom` 36 and `s8i2_sram` 97 LUT cells.
- R607-1-R1: "Every point is within the 56-RAMB36 budget. The largest leaves 3 tiles as mapped; the budget check reads the planned 54.5, so its image can grow 6 KiB (1.5 tiles) before it is refused."

### R2.7 Gate table (round 2)

Heads: `be431eec` (code, test, rule table, idiom inventory), `516d7fb8` (ledger and fit docs only), `76605880` (one prose sentence in `SPLIT_CONTROL_MEMORY.md` section 3, outside the rule table; final). Every gate unpiped, rc recorded; logs in `evidence-r2/`, scratch under the lane's scratch directory.

| # | Gate | Head | rc | Result |
|---:|---|---|---:|---|
| 1 | `sw/litex/test_ctrl_memory.py` (LiteX stack, pinned RV32 SDK) | `be431eec` | 0 | 109 checks, 0 failures, `RESULT: PASS`; all 40 mutants caught; 70 s wall, 0.73 GB peak |
| 2 | `scripts/run_litex_sims.sh --selftest` | `516d7fb8` | 0 | 10 checks PASS |
| 3 | `scripts/run_litex_sims.sh <logs>` (pinned Verilator 5.050 on PATH) | `516d7fb8` | 0 | 7 of 7 PASS, 0 skipped (`test_ctrl_memory` and M2's `test_retained_cdc_storage` among them) |
| 4 | R607-1 `mutants.py` (twelve mutants, unmodified) | `be431eec` | 0 | 12 of 12 KILLED by named FAIL lines (R2.5) |
| 5 | R606-1 `probe_writable_rom.py`, `probe_region_top.py`; R607-1 `probe_malformed.py`, `probe_ctrlmem_sim.py` | `516d7fb8` | 0 each | R2.5 |
| 6 | `ctrl_memory.py plan` under CPython 3.12.3 `-I`, largest image, `--stage-bytes 13264`, then `3344` | `516d7fb8` | 0, then 2 (expected) | 54.5 RAMB36; `REFUSED staging buffer: nvm_stage is 13264 bytes; the requested shape stages 3344` |
| 7 | `ctrl_srp_image.py`, four points, split and flat (`fit_r2.sh`) | `516d7fb8` | 0 (12 runs) | all eight ELFs byte-identical to round 1's (`fit/elf.sha256`); the four plans identical |
| 8 | `syn/ooc/ctrl_memory_ooc.py`, four points (emission only) | `516d7fb8` | 0 | 25 files identical to the inputs round 1 mapped, apart from LiteX's date stamps in the 8 `.v` files: the mapping of section 5 stands without a new Vivado run |
| 9 | Exports without Vivado, base `08b90b68` blobs of `milan_soc.py` and `ctrl_memory.py` swapped in and restored, against head (`exports.sh`) | `516d7fb8` | 0 | default 1x1: 22 files, 0 differ (normalized `alinx_ax7101.v` `82a70c638cdac9a7`); default 8x8: 22, 0 (`9b201e1ea6455fb3`); split 1x1: 24, 0 (`599ff66161596c3f`); split 8x8: 23, 0 (`f2787d47401369ce`); worktree status unchanged |
| 10 | `sw/builder/test_builder.py --require-elaboration --require-rv32` | `516d7fb8` | 0 | `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11: the calibration's bench build tree is not on this host; the recorded reason, as in round 1) |
| 11 | `syn/yosys/run.sh` | `516d7fb8` | 0 | tops 58, pass 58, fail 0; TAP-PURITY PASS |
| 12 | `check_soc_sources.py` and `--selftest`; `sw/litex/iob_pack_selftest.py` | `516d7fb8` | 0 each | 43 modules, 77 sources; 25 checks; 22 arms, 21 mutants |
| 13 | `check_py_idiom.py` and `--selftest` (CPython 3.12.3); `check_hygiene.py --check` and `--selftest`; `check_todo_ownership.py`; `measure_fail_fast.py --check`; `measure_test_evidence.py --check`; `check_sh_idiom.py` | `76605880` | 0 each | at ratchet (`dynamic eval/exec: 0` with the inventory entry; long function 9 <= 9, long module 10 <= 10, over-long line 0) |
| 14 | `docs_check.py`; `check_em_dash.py --base 08b90b68` and `--selftest`; `gen_toc.py --check`, `--verify-anchors`, `--selftest`; `check_doc_paths.py`; `check_doc_style.py` and `--selftest`; `ci_events.py --check` and `--selftest`; `git diff --check 08b90b68 HEAD` | `76605880` | 0 each | PASS (pinned Markdown renderer) |
| 15 | `scripts/run_all_suites.sh <logs>` (VERILATOR_JOBS=2, -j8, launched with `setsid`) | `76605880` | 0 | 61 of 61 suites, 2,185,848 checks, 0 in-suite failures, 0 timed out; the same 4 declared `tsn_fuzz` skips as round 1 (tsn-gen absent); 06:40 to 08:39 |
| 16 | `sw/litex/test_ctrl_memory.py` | `76605880` | 0 | 109 checks, 0 failures, `RESULT: PASS`; 40 of 40 mutants caught; 72 s wall, 0.73 GB peak |

`be431eec` to `516d7fb8` changes `docs/design/` only, outside the rule table the test reads; `516d7fb8` to `76605880` changes one prose line of section 3. No round-2 commit touches `hdl/`, `tb/`, `syn/` or `protocol-processor`/`gptp-processor`; the suite sweep and Yosys still ran at a round-2 head because the PR head now carries M2's RTL through the dev merge.

### R2.8 Not done, and why

- No Vivado run this round: no mapped figure changed (`CtrlMemory` and the bank plan are unchanged, and the four split ELFs plan identically, R2.7).
- M8a-2 (boot, service checks, route) still waits for F-INT PR 2; primitive mapping and resource figures are round 1's (sections 5 and 6 below).

## Status (round 1)

**REVIEW READY (M8a-1).** Head `5d532e9dcd2bb8d19f8017cc0c2d6e02ec556d14`: four commits on dev `e8454e27`, local, not pushed.

- **Fit:** holds at all four points. As mapped, 34.0 / 37.5 / 47.0 / 53.0 tiles (RAMB36 + RAMB18/2) against the 56-RAMB36 budget, with no power-of-two waste.
- **Ledger:** 124 tiles before the split's conditional release, 113 after; 121.5 is the ceiling and the 13.5 reserve is untouched.
- **Planted controls:** all three fail by name, in the unit test and through the real SoC build.
- **Default:** the all-fabric default is digest-identical for both AX7101 shipping configs.
- **Gates:** every gate the change touches passed (section 11).
- **Open:** M8a-2 (boot, service checks, route) waits for F-INT PR 2.

## Contents

1. Scope of this round
2. Changes, with file:line
3. Memory map and instantiation
4. Linked spans at the four points
5. Primitive mapping, before and after
6. Ledger rows, measured
7. Planted controls, and the defect each test catches
8. Boot console and diagnostics; DDR3 at this base
9. All-fabric default: digest-identical
10. All-fabric image without DDR3 (measurement only)
11. Gate table
12. Not in this round, and open risks
13. Reproduction

## 1. Scope of this round

From the ruling (6101485877):

- the owner's 224 KB binds: up to 56 RAMB36 as mapped; the ledger takes the split's conditional release (-11 tiles) and stays at or under 121.5 with the 13.5 reserve untouched;
- no power-of-two waste; the four points at or near their floor; RAMB36 and RAMB18 reported as mapped;
- the firmware owns the reset entry in the split placement; no BIOS ROM or SRAM there; the all-fabric image keeps its BIOS;
- M8a-1 is the memory map and instantiation behind `--ctrl-mailbox`, the fit proof, the linked spans, the ledger rows, the three planted controls and the default digest-identical;
- M8a-2, after F-INT PR 2: the split-image simulation boot, `check_nvm_capture.py` 8x8, `nvm_cosim`, `nvm_capture_cpu` and the integrated route through the M0s recipe.

## 2. Changes, with file:line

Commits (one-line, no trailers):

- `c20ed894a3b577407588e30ff365480a7e7be26a` Build the split placement's firmware ROM and RAM from the linked image behind --ctrl-mailbox, in power-of-two banks with no BIOS (#640 M8a-1)
- `94190c36501cce6082b9fa93c916a8ecbaca0455` Give the split memory plan's and test's nested helpers the docstrings the Python idiom gate requires
- `a475ab5ab4e3eb75a1ab79f913cf9f6893f42d2b` Document the split placement's control memory and record M8a-1's measured firmware block RAM ledger rows (#640)
- `5d532e9dcd2bb8d19f8017cc0c2d6e02ec556d14` State the split ROM mapping default without process language, as the docs wording gate requires

18 files, +1,270 / -55.

| File:line | Change |
|---|---|
| `sw/litex/ctrl_memory.py:44-89` | New. The contract: 4,096 B per RAMB36, the 2,048 B RAMB18 granule, the 56-RAMB36 budget, `rom` at `0x0000_0000` and `sram` at `0x1000_0000`, each 224 KiB |
| `sw/litex/ctrl_memory.py:139` | `banks()`: the need in granules, its binary digits as banks, largest first |
| `sw/litex/ctrl_memory.py:151` | `read_elf()`: entry, allocated sections (address, load address, loaded or NOBITS), symbols, load segments of an RV32 ELF |
| `sw/litex/ctrl_memory.py:197` | `check_map()`: `reset entry`, `memory map` and `memory-map overlap` (sections, load addresses, regions) |
| `sw/litex/ctrl_memory.py:219` | `plan()`: the needs and banks; `allocation over budget` above 56 RAMB36 |
| `sw/litex/ctrl_memory.py:236` | `rom_words()`: the initial contents of `rom` |
| `sw/litex/ctrl_memory.py:245` | `stage_bytes()`: the shape's KLJ2 container (scripts' `inventory` and `klj2_assemble`) plus one record header, as `nvm_shape.h` derives `NVM_STAGE_BYTES` |
| `sw/litex/ctrl_memory.py:263` | `check_stage()`: `staging buffer` |
| `sw/litex/ctrl_memory.py:273, 281` | `regions_ld()` for the link; the CLI (`regions`, `plan`) |
| `sw/litex/milan_soc.py:44` | `import ctrl_memory` |
| `sw/litex/milan_soc.py:2578` | `CtrlMemory`: one region as banks of LiteX `wishbone.SRAM` behind a `wishbone.Decoder`; past the last bank, `err` at once |
| `sw/litex/milan_soc.py:2608` | `add_ctrl_memory()`: checks the CPU's reset address and `sram` origin, plans the image, adds `rom` (read-only, initialised) and `sram`, sets LiteX's `integrated_rom_initialized` so no BIOS is built |
| `sw/litex/milan_soc.py:2674, 2777-2781, 2808-2809` | `ctrl_firmware` parameter; under `ctrl_mailbox` no BIOS ROM or SRAM (`integrated_rom_size=0`, `integrated_sram_size=0`), then `add_ctrl_memory` right after `SoCCore.__init__` |
| `sw/litex/milan_soc.py:3683` | `--ctrl-firmware` |
| `sw/litex/milan_soc.py:3887` | `--ctrl-mailbox` and `--ctrl-firmware` refused apart |
| `sw/litex/milan_soc.py:4027` | passed to `MilanSoC` |
| `sw/litex/milan_soc.py:4066` | the split build adds no `libmilan_baremetal` (no BIOS to link into) |
| `sw/litex/milan_soc.py:4188` | the split build's staging check, before any export |
| `sw/firmware/ctrl/plat/ctrl_split.ld` | New. The split link: reset entry first in `rom`, `.data` in `sram` loaded from `rom`, `.bss`, 8 KiB stack |
| `sw/firmware/ctrl/plat/ctrl_split_start.S` | New. The reset entry: stack, `.data` copy, `.bss` clear, `main` |
| `sw/firmware/ctrl/test/ctrl_srp_image.py:66, 92, 180` | `link()` extracted; `--layout split` links with the split script and reports the bank plan; the flat layout is unchanged (same four spans) |
| `sw/litex/test_ctrl_memory.py` | New. 33 checks (section 7) |
| `syn/ooc/ctrl_memory_ooc.py` | New. Emits both regions of each image as `CtrlMemory` builds them, and the OOC Vivado script |
| `scripts/run_litex_sims.sh:101` | `test_ctrl_memory` in the pinned inventory |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | New. The split placement's memory contract, refusals, boot and diagnostics, fit |
| `docs/design/MARK_II_AREA_PLAN.md`, `docs/design/AREA_BUDGET.md` | Ledger rows measured (section 6) |
| `docs/testing/TESTING.md`, `docs/testing/CI_WORKFLOWS.md`, `docs/design/MAILBOX_SPLIT.md`, `docs/ARCHITECTURE_HW_SW_SPLIT.md`, `docs/litex/LITEX_SOC.md`, `docs/README.md`, `sw/firmware/ctrl/README.md` | Cross-references |

## 3. Memory map and instantiation

| Region | Origin | Size | Holds | Built from |
|---|---|---:|---|---|
| `rom` | `0x0000_0000` (CPU reset address) | 224 KiB | reset entry, `.text`, `.rodata`, initial bytes of `.data` | banks of `wishbone.SRAM`, read-only, initialised from the ELF |
| `sram` | `0x1000_0000` | 224 KiB | `.data`, `.bss`, 8 KiB stack | banks of `wishbone.SRAM`, writable, uninitialised |

- Each region spans the whole budget, so the CPU netlist does not depend on the image: both split exports elaborate the same `VexiiRiscvLitex_dd10544c3ff1037f8a13f4ce3a3dd432`.
- Banks: the need rounded up to 2,048 B granules; the granule count's binary digits, largest first; each bank aligned to its own size; the decode compares high address bits (`slave_sel[0] = adr[15:14] == 0`, ... in the export).
- Past the last bank the region answers `err` in one cycle and writes nothing.
- Split vs base `--ctrl-mailbox` export (1x1): `csr.csv` differs only in `memory_region,rom` (131,072 to 229,376) and `memory_region,sram` (8,192 to 229,376). No CSR, CSR bank, interrupt or constant changes. `soc.h` identical except its timestamp; `mem.h` differs in `ROM_SIZE`/`SRAM_SIZE`.
- Split exports: `software/bios/` is empty (no `bios.bin`); the gateware carries `rom_bank0..4.init` (1x1) / `rom_bank0..3.init` (8x8) and the identifier's `mem.init`; no `sram.init`.

## 4. Linked spans at the four points

Linked at the lane head by `ctrl_srp_image.py --with-aecp --layout split` (pinned RV32 SDK `riscv32-ilp32d--glibc--stable-2025.08-1`, `-DNDEBUG`, `--gc-sections`, 8,192 B stack). Bytes:

| Point | .text | .rodata | .data | .bss | stack | `rom` need | `sram` need | Sum | Flat span (unchanged) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1, one interface (shipping) | 83,020 | 11,950 | 56 | 37,252 | 8,192 | 95,032 | 45,520 | 140,552 | 140,400 |
| 1x1, two interfaces | 84,308 | 11,950 | 56 | 48,620 | 8,192 | 96,320 | 56,880 | 153,200 | 153,056 |
| 8x8, one interface | 83,068 | 25,158 | 448 | 77,428 | 8,192 | 108,680 | 86,080 | 194,760 | 194,224 |
| 8x8, two interfaces (largest) | 84,444 | 25,158 | 448 | 103,556 | 8,192 | 110,056 | 112,208 | 222,264 | 221,728 |

- The split need exceeds the flat span by the reset entry (88 B of `.text`), the second copy of `.data` (56 / 448 B) and alignment (8 / 0 B).
- Inside the spans: descriptor image `aecp_entity_image` 7,512 / 19,520 B (rodata); `nvm_stage` 3,344 / 13,264 B (bss), equal to `ctrl_memory.stage_bytes` for the shape; lwSRP pool `image_arena` 9,920 / 19,840 / 24,032 / 48,064 B (bss), counted once.
- The largest point uses 222,264 of 229,376 bytes (224 KiB), and its banks 54.5 of 56 RAMB36: 1.5 RAMB36 (6 KiB) of headroom.

## 5. Primitive mapping, before and after

**After** (out of context, `syn/ooc/ctrl_memory_ooc.py`, Vivado 2026.1, `xc7a100t-fgg484-2`, `-mode out_of_context -directive AreaOptimized_high`, `Synth 8-4445` promoted to an error, every ROM `$readmem` read successfully; Vivado rc 0, run 2026-10-11 03:28 to its release under the exclusive lock). Per region:

| Top | Banks, bytes | Planned RAMB36 / RAMB18 | As mapped RAMB36 / RAMB18 | LUT | FF | LUTRAM |
|---|---|---:|---:|---:|---:|---:|
| `s1i1_rom` | 64K+16K+8K+4K+2K | 23 / 1 | 22 / 1 | 120 | 27 | 0 |
| `s1i1_sram` | 32K+8K+4K+2K | 11 / 1 | 11 / 1 | 92 | 5 | 0 |
| `s1i2_rom` | 64K+32K | 24 / 0 | 23 / 1 | 36 | 3 | 0 |
| `s1i2_sram` | 32K+16K+8K | 14 / 0 | 14 / 0 | 53 | 4 | 0 |
| `s8i1_rom` | 64K+32K+8K+4K | 27 / 0 | 25 / 1 | 217 | 28 | 0 |
| `s8i1_sram` | 64K+16K+4K+2K | 21 / 1 | 21 / 1 | 90 | 5 | 0 |
| `s8i2_rom` | 64K+32K+8K+4K | 27 / 0 | 25 / 1 | 231 | 34 | 0 |
| `s8i2_sram` | 64K+32K+8K+4K+2K | 27 / 1 | 27 / 1 | 97 | 6 | 0 |

Per point:

| Point | Linked need, B | Allocated bytes (banks) | Used | Planned tiles | As mapped RAMB36 / RAMB18 | As mapped tiles | LUT / FF | Byte floor (flat span / 4,096, up) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1, one interface | 140,552 | 143,360 | 98.0% | 35.0 | 33 / 2 | **34.0** | 212 / 32 | 35 |
| 1x1, two interfaces | 153,200 | 155,648 | 98.4% | 38.0 | 37 / 1 | **37.5** | 89 / 7 | 38 |
| 8x8, one interface | 194,760 | 198,656 | 98.0% | 48.5 | 46 / 2 | **47.0** | 307 / 33 | 48 |
| 8x8, two interfaces | 222,264 | 223,232 | 99.6% | 54.5 | 52 / 2 | **53.0** | 328 / 40 | 55 |

- `sram` maps exactly as planned. Its LUTs are the bank decode and the read multiplexer.
- `rom` maps below plan for two reasons. Vivado trims a bit column constant across a bank (`16384x31` becomes 15 RAMB36 and one RAMB18). It also maps a small or sparse bank into logic: the 512-word bank at s1i1 (77 LUT6) and the 1,024-word bank at s8i1/s8i2, absent from the block-RAM mapping report (`util/*.rpt`, `map.vivado.log`).
- Most ROM LUTs come from that bank: 231 at the largest point. LiteX's memory emitter writes no `ROM_STYLE`, so this round reports Vivado's default. Forcing block RAM would cost at most the planned-minus-mapped difference, 1.0 / 0.5 / 1.5 / 1.5 tiles, and save most of those LUTs; M8a-2's route weighs it.

**Before:**

| Configuration | RAMB36 | RAMB18 | Source |
|---|---:|---:|---|
| All-fabric (and base `--ctrl-mailbox`) BIOS ROM, 13,279 x 32 | 16 | 0 | route census at `e8454e27` (round 1) |
| BIOS SRAM, 2,048 x 32 | 2 | 0 | same |
| Identifier memory (stays in both placements) | 0 | 1 | same |
| One LiteX `wishbone.SRAM` of the largest image's whole span (221,728 B) | 64 | 0 | round 1 OOC mapping |
| ROM + RAM, one `wishbone.SRAM` each, largest image | 64 | 0 | round 1 OOC mapping |

In the split, the BIOS ROM and SRAM are not built (-18 RAMB36), and the firmware takes 52 RAMB36 + 2 RAMB18 at the largest point.

## 6. Ledger rows, measured

Recorded in `docs/design/MARK_II_AREA_PLAN.md` (Firmware and block RAM ledger) and mirrored in `docs/design/AREA_BUDGET.md`:

| Item | RAMB36 delta | RAMB18 delta | Tile delta | Image tiles after |
|---|---:|---:|---:|---:|
| Recorded route at `a5ca6e51` | 74 | 27 | 87.5 | 87.5 |
| L2 credited removals: AECP and SRP storage | -6 | -1 | -6.5 | 81 |
| Measured mailbox replacement | +1 | +10 | +6 | 87 |
| M8a-1: BIOS ROM and SRAM not built in the split, measured at `e8454e27` | -18 | 0 | -18 | 69 |
| M8a-1: firmware allocation as mapped, 8x8 with two interfaces | +52 | +2 | +53 | 122 |
| M2 maximum additional allocation | +2 | 0 | +2 | 124 |
| Conditional release of remaining wrapper storage, split only | -10 | -2 | -11 | 113 |

- `87.5 - 6.5 + 6 - 18 + 53 + 2 = 124`; after the release, 113: 8.5 below 121.5, reserve untouched.
- With every bank in block RAM (the plan bound 54.5): 125.5 and 114.5.
- At the shipping 1x1 with one interface (34.0): 105 and 94.
- The census's extra RAMB18 is the 49-byte identifier memory, which stays; the estimate row's -18.5 becomes -18.
- Keeping the BIOS memories would add 18: 142 and 131.

## 7. Planted controls, and the defect each test catches

**The three controls the assignment names, through the real SoC build** (`milan_soc.py` shipping export plus `--ctrl-mailbox --ctrl-firmware`, each refused before any export; logs in `evidence-m81/`):

| Control | Plant | Result |
|---|---|---|
| Allocation over budget | the 8x8 two-interface image linked from a scratch copy of the control tree whose `ctrl_split.ld` reserves a 16 KiB stack | rc 1, `allocation over budget: 56.5 RAMB36 (rom 110056 bytes in 110592, sram 120400 bytes in 120832) exceeds the 56-RAMB36 budget`; the fixture refuses the same image with the same words (rc 2) |
| Memory-map overlap | the 1x1 image linked from a copy whose `ctrl_split.ld` places `.bss` at `ADDR(.data)`; GNU ld accepts it | rc 1, `memory-map overlap: .bss at 0x10000000 lies inside .data [0x10000000, 0x10000038) (addresses)` |
| Staging buffer for another shape | the good 1x1 one-interface image in an 8x8 build | rc 1, `staging buffer: nvm_stage is 3344 bytes; the endstation_ax7101_8x8 shape stages 13264` |

Also refused (rc 2, by argparse): `--ctrl-mailbox` without `--ctrl-firmware`, and `--ctrl-firmware` without `--ctrl-mailbox`.

**`sw/litex/test_ctrl_memory.py`** (33 checks, RESULT: PASS; in `scripts/run_litex_sims.sh`):

| Arm | What it checks | Planted defect it catches |
|---|---|---|
| banks | 840 needs up to past the budget against an independent oracle (ceil(need/2,048) and its binary digits); zero need; RAMB18 counted half | any bank rounding or ordering change (the `banks smallest first` mutant turns 4 checks red) |
| checks | an ELF written by an independent writer: needs, `rom` contents at their load addresses, stage accepted | `the map check off` (5 red), `the budget check off` (1 red), `the staging check off` (2 red) |
| controls | over budget (215,000 B of .bss, 58 RAMB36, each region inside its own); overlap (.bss over .data; `sram` moved into `rom`); staging both ways (1x1 image vs 8x8 stage, 8x8 image vs 1x1 stage); entry at 0x100; .data's initial bytes in `sram`; a section at `0x4000_0000` | each must be refused by its named check |
| simulation | the real `milan_soc.CtrlMemory` in migen: `rom` reads its image at the first, second and last word of each of 3 banks; a write to `rom` changes nothing; `sram` byte lanes at every bank edge; past the last bank `err` at once in both regions; a hole write lands in no bank (each bank's aliasing cell read back) | `banks smallest first` (misaligned decode), `the hole answers nothing` (no `err`: 2 red), `a writable rom` (1 red) |
| link | a probe linked by the real `ctrl_split.ld` behind `ctrl_split_start.S` with the pinned SDK: entry 0 is `auipc sp`; `.data` runs in `sram` and its 7 loads from `rom`; the stack tops the `sram` need; `nvm_stage` passes | link-script plants: `.data` without `AT > rom` (refused `memory map`), `ENTRY(main)` (refused `reset entry`) |

Each mutant is a monkeypatch of the code under test for one arm; the arm must report at least one failure.

## 8. Boot console and diagnostics; DDR3 at this base

The split image loses: the LiteX BIOS and its console (banner, memory, flash, SDRAM and boot commands); the BIOS DDR3 initialisation (`sdram_init`); the shipping firmware's UART commands (`libmilan_baremetal` is not linked). It keeps the UART, `timer0`, `ctrl` (reset, scratch, bus errors), the identifier memory, the `ppmem` observer and every Milan CSR. Any console there is the control firmware's (F-INT PR 2). The all-fabric image keeps its BIOS (section 9).

DDR3 stays instantiated under `--ctrl-mailbox` at this base, because `KL_pp_shadow` (unconditional at `hdl/milan/milan_datapath.sv:8003`) and its three processor memory masters still reach the window in `main_ram`. With no BIOS the DFI never makes the 1 to 0 to 1 hand-back that `pp_mem_gate` (`sw/litex/milan_soc.py:2255`) waits for, so those masters stay refused (they answer errors, as before training). Removing DDR3 belongs with the wrapper's removal (F-INT PR 2) and is measured by M8a-2's route.

## 9. All-fabric default: digest-identical

Both AX7101 shipping configs exported (recipe `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, no `--build`) with the base `milan_soc.py` (blob of `e8454e27`, swapped in and restored) and with the head. Normalization, and nothing else: LiteX timestamp lines, the export's own directory, the Verilog banner's Date line and LiteX's comment-only hierarchy tree.

| Config | Files compared | Differ | Normalized SHA-256 of `alinx_ax7101.v` |
|---|---:|---:|---|
| `ax7101` (1x1 TDM8) | 22 | 0 | `40e5304ae1fea35a02e5487f1096ed3c3bc4cdfa0732cd46e5332ce796586602` (base = head) |
| `ax8x8` | 22 | 0 | `fea8757e5546fa793dd76ac08800630fde4383ac8a289313f60b2b571b580e16` (base = head) |

The 22 files include the top `.v`, `.tcl`, `.xdc`, every `.init` (the BIOS ROM image among them), `bios.bin`, `csr.csv`, `csr.json`, the generated headers and `regions.ld`, the AEM image and manifest and `flashboot_layout.json`. Tables: `evidence-m81/digest-ax7101.txt`, `digest-ax8x8.txt`.

## 10. All-fabric image without DDR3 (measurement only)

Unchanged from round 1 (`stop-round/HANDOFF-stop.md` section 6): DDR3 holds only the processor window. Compacted, it is 14,792 B (4 RAMB36) at 1x1 and 46,640 B (12 RAMB36) at 8x8. Dropping DDR3 there would also need a compacted window and its constants, an on-chip memory on the CPU's DMA bus for the three processor masters, the removal of LiteDRAM, the PHY, `pp_mem_gate`'s DFI hold and the BIOS SDRAM init, and a pinned `spiflash` CSR location. Not done; the default flip decides it.

## 11. Gate table

Heads: `c20ed894` (first commit), `94190c36` (docstrings), `a475ab5a` (docs), `5d532e9d` (final, one doc line). Every gate unpiped, rc recorded (`evidence-m81/gates-*`).

| # | Gate | Head | rc | Result |
|---:|---|---|---:|---|
| 1 | `sw/litex/test_ctrl_memory.py` | `a475ab5a` | 0 | 33 checks, RESULT: PASS (link arm with the pinned SDK) |
| 2 | `scripts/run_litex_sims.sh --selftest` | `a475ab5a` | 0 | PASS |
| 3 | `scripts/run_litex_sims.sh <logs>` (pinned Verilator 5.050 on PATH) | `a475ab5a` | 0 | 6 of 6 PASS, 0 skipped |
| 4 | `ctrl_memory.py plan` on CPython 3.12.3 (largest image, `--stage-bytes 13264`) | `a475ab5a` | 0 | 54.5 planned |
| 5 | `check_py_idiom.py` and `--selftest` (CPython 3.12.3) | `a475ab5a` | 0, 0 | at ratchet (`c20ed894` was rc 1: two nested helpers without docstrings; fixed in `94190c36`) |
| 6 | `check_hygiene.py --check` and `--selftest`; `check_todo_ownership.py`; `measure_fail_fast.py --check`; `measure_test_evidence.py --check` | `a475ab5a` | 0 each | PASS |
| 7 | `docs_check.py`; `check_em_dash.py --base e8454e27`; `gen_toc.py --verify-anchors`, `--check`; `check_doc_paths.py`; `check_doc_style.py`; `ci_events.py --check` | `5d532e9d` | 0 each | PASS (`a475ab5a`: `docs_check.py` rc 1, process wording, fixed in `5d532e9d`) |
| 8 | `gen_toc.py --selftest`; `check_doc_style.py --selftest`; `ci_events.py --selftest` | `a475ab5a` | 0 each | PASS |
| 9 | `sw/builder/test_builder.py --require-elaboration --require-rv32` | `c20ed894` and `a475ab5a` (the tree reached `5d532e9d`, one doc line, during the run) | 0, 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: the bench build tree for its calibration is not on this host; recorded reason) |
| 10 | `check_soc_sources.py` and `--selftest`; `sw/litex/iob_pack_selftest.py` | `c20ed894` | 0 each | PASS |
| 11 | `check_sweep_shape.py --self-test`; `check_deploy_shape.py --self-test`; `check_entity_shape.py --self-test` | `c20ed894` | 0 each | PASS |
| 12 | `syn/ooc`: `dp_srcs.py --selftest`, `ooc_tcl_selftest.py`, `pp_baseline.py --selftest`, `pp_baseline_mutants.py`, `pp_baseline_reports_selftest.py`, `pp_resource_gate.py --selftest`, `pp_resource_gate_mutants.py`, `pp_resource_gate.py check-baseline` | `c20ed894` | 0 | PASS |
| 13 | `ctrl_image_selftest.py --require-rv32` | `c20ed894` | 0 | 33 checks PASS |
| 14 | `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | `c20ed894` | 0 | `test_ctrl_firmware: PASS` |
| 15 | `scripts/run_all_suites.sh <logs>` (VERILATOR_JOBS=2, -j8) | `94190c36` | 0 | 61 of 61 suites, 2,185,848 checks, 0 failures; 4 declared `tsn_fuzz` skips (tsn-gen absent). Two earlier attempts (rc 2) aborted in the preflight's hard-HUP control because they ran under `nohup`; relaunched with `setsid` only |
| 16 | `syn/yosys/run.sh` | `94190c36` | 0 | 58 of 58 tops PASS; TAP-PURITY PASS |
| 17 | Fixture, four points, split and flat (`fit_final.sh`) | `94190c36` | 0 (12 runs) | flat spans unchanged; split ELFs byte-identical to the mapped ones |
| 18 | Default exports, base vs head, both AX7101 configs (section 9) | head `milan_soc.py` = `c20ed894` blob | 0 | 22 files each, 0 differ |
| 19 | Split exports, both configs (`--ctrl-mailbox --ctrl-firmware`) | same | 0 | elaborate; no BIOS; one CPU netlist |
| 20 | Planted controls through the SoC build (section 7) | same | 1 (expected) | each refused by name |
| 21 | OOC mapping (Vivado, exclusive lock) | images of `94190c36` | 0 | section 5 |

The diff from `94190c36` to `5d532e9d` touches documentation only (`docs/`, `sw/firmware/ctrl/README.md`), which neither the suites, Yosys nor the fixture read. The diff from `c20ed894` to `94190c36` adds two docstrings.

## 12. Not in this round, and open risks

- M8a-2: the split-image simulation boot to the control application's ready state, the service checks and the integrated route (LUT, FF, RAMB deltas against M0s's split figure, WNS) wait for F-INT PR 2.
- The image linked here is the size fixture in the split layout. Its reset entry is exercised by the linked probe's layout checks, not by a CPU simulation.
- The bank decode and its data multiplexer sit on the CPU's bus path; their timing is measured only by M8a-2's route.
- Headroom at the largest point is 1.5 RAMB36 (6 KiB) under 56. Growth beyond that is refused by name.
- The split build needs its own VexiiRiscv netlist (`VexiiRiscvLitex_dd10544c3ff1037f8a13f4ce3a3dd432`), generated once for both shapes.
- DDR3 under `--ctrl-mailbox` at this base is instantiated and untrained (section 8).
- Worktree leftovers, none committed: the export recipe's three scratch symlinks (`sw/builder/out`, untracked; `configs/generated/ltn_rom.hex` and `ucode.hex`, ignored) point into the scratch work directory, and the gates' ignored build outputs (`tb/verilator/*/obj_*`, `__pycache__`, `.run_all_suites.lock`) remain. Removing them was declined by the session's permissions; `git status` shows only `?? sw/builder/out`.

## 13. Reproduction

Environment: the pinned RV32 SDK (`scripts/ci_rv32_sdk.py --verify-only`), the LiteX stack of `sw/litex/litex_pins.txt` with `sw/litex/patches/`, Vivado 2026.1, PyYAML on the host Python. Runtime archives as in round 1 (`stop-round/HANDOFF-stop.md` section 8).

```sh
python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml \
  --interfaces 2 --with-aecp --layout split --output "$OUT" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
python3 sw/litex/ctrl_memory.py plan "$OUT/ctrl_app.elf" --stage-bytes 13264
python3 syn/ooc/ctrl_memory_ooc.py "$MAP" s8i2="$OUT/ctrl_app.elf"
cd "$MAP"
vivado -mode batch -nojournal -source ctrl_memory_ooc.tcl
python3 sw/litex/test_ctrl_memory.py
```

Default digest proof: the recipe in `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` (export without `--build`), once with `e8454e27`'s `sw/litex/milan_soc.py` and once with the head's, compared by `evidence-m81/digest.py`. Split export: the same argv plus `--ctrl-mailbox --ctrl-firmware <elf>` (`evidence-m81/split-*-argv.json`). Scripts used: `evidence-m81/export.py`, `fit_final.sh`, `run_map.sh`, `gates_*.sh`.
