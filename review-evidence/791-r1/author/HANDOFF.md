# A765 HANDOFF: the split CPU's region decode (#791, part of #665)

PRIVATE. Nothing pushed. Lane $LANES/791-region-decode, branch `791-split-region-decode`, from
`dev-soft-core` `1d6bf555` (origin/dev-soft-core has not moved; origin/dev fetched at `46c971fa` for the replay's
scope steps). The PR targets `dev-soft-core`.

## Status: REVIEW READY (every item met; every gate passes: rc 0, except sweep shard 1's rc 1 from one #833 `gptp_shadow` cleanup failure, whose re-run is rc 0)

Head `03447eaa087ba0687362a7372f4a00bd40c6fd46`, two commits on `1d6bf555`, no others:

- `eb26f22d` Hand the split CPU's generator each control region as aligned power-of-two pieces, so its fetch and load decode is exact (#791)
- `03447eaa` State that the region-decode test SoC is the split SoC without DDR3, as the Arty's split image is built (#791)

| Item | State |
|---|---|
| TAKEN on #791 | posted, issuecomment-6788806939 (`receipts/posts/taken.md`) |
| STOP on #791 (interim session, root file system read-only) | posted, issuecomment-6790817378 (`receipts/posts/stop.md`); the host was restored and the round resumed |
| 1. Exact decode; (a) or (b) with the reason | **met, (a)**: comparison below |
| 2. CPU-simulation test at the last word of every control region and one past it, past-the-end faulting, plus a single-mask mutant failing a named check | **met**: self-test PASS at `03447eaa` (`receipts/region-decode/`) |
| 3. All-fabric generated CPU byte-identical | **met**: every shipped config, base `1d6bf555` vs `03447eaa` (`receipts/allfabric/`) |
| Generated decode per split shape = [origin, origin+size) | **met** for 1x1 and 8x8 (`receipts/decode/`); no Arty split config on this branch |
| Split boot to ready at 1x1 and 8x8 | **met**: 84.425 ms and 184.695 ms (`receipts/boot/`) |
| Gates | all pass (table below; sweep shard 1's #833 failure re-run once, PASS); REVIEW READY posted, issuecomment-6794688203 (`receipts/posts/review-ready.md`) |

## Host events during the round

1. **08:22-08:26: the root file system (`/`, holding `/home`) went `emergency_ro`.** An interim session found it: no
   new CPU netlist (the generator's cache and sbt's lock are under `/home`), output directory read-only. It posted
   STOP (issuecomment-6790817378), kept its drafts in scratch, and did not run the blocked work on relocated copies
   (refused by the permission system). Its notes: `receipts/posts/interim-ro-notes.md`.
2. **About 09:50: the host was reset**, killing every unit. On resume: `/home` writable. Kept, as completed before
   the events with their rc files: the region-decode self-test, the 1x1 boot, the product decode, and four replay
   jobs whose result files were whole. Re-run: the sweep (from scratch), the 8x8 boot, S2's harness, the all-fabric
   compare, test_ctrl_memory.py and every other replay job. Two replay result files were left empty by the reset
   and were re-run.
3. **Network outages after the reset** (DNS for github.com, a GitHub early EOF, PyPI unreachable): three replay
   attempts failed in their setup steps before any gate ran (`docs-gates-0` twice, `elaborate-gates-0` once).
   Each was moved aside with its logs (`receipts/ci/attempt-*`) and re-run.
4. **Shard placement slip.** My first relaunch of the sweep put its shards on 0-31, which other lanes had booked in
   the seconds since my `cpu_ranges.py show`. I stopped the four units within about a minute, during their
   clone and preflight, and relaunched them on the free 56-63, 64-71, 72-75 and 80-87.

## (a) or (b)

**(a): the split SoC hands the generator each region as its aligned power-of-two pieces.** It is exact and costs
less than (b):

- Exact by construction. The generator checks each region with one mask compare, `(address & ~(size - 1)) == origin`,
  exact for an aligned power of two. 224 KiB at 0 is 128 KiB at 0, 64 KiB at 0x2_0000 and 32 KiB at 0x3_0000, and the
  same at `sram`'s 0x1000_0000; the union is exactly the region. Shown on the generated netlists at every 32-bit
  address (`decode.py`) and in simulation at every edge.
- No generator or LiteX patch: one Python hook in the split hookup, which the all-fabric SoC never calls.
- (b), a range compare in the generator, is a Scala patch carried on every re-pin, and needs the netlist cache
  invalidated: the cache key is LiteX's hash of the region list and arguments, not the generator's source, so the
  split SoC's unchanged list would keep reusing the cached single-mask netlist. A `>=`/`<` pair also costs more logic.
- (a)'s one dependency, LiteX naming its netlist through `self.generate_netlist_name()` in `do_finalize`, is guarded:
  a finalize that never calls it is refused by name.

## Changes (file:line, reason)

- `sw/litex/ctrl_memory.py:136` `decode_pieces`: [origin, origin+size) as the fewest aligned power-of-two pieces;
  `:158` `cpu_regions`: each (origin, size, mode, bus) row as its pieces, mode and bus kept, an aligned power-of-two
  row unchanged. The map's own statement (#791).
- `sw/litex/milan_soc.py:3235` `add_ctrl_memory` calls `exact_cpu_decode(soc.cpu)`; `:3239` `exact_cpu_decode`: on a
  VexiiRiscv instance only, the CPU's naming step replaces `VexiiRiscv.memory_regions` by its pieces before LiteX names
  and generates the netlist; its `do_finalize` refuses a CPU whose naming step never ran. SoC bus regions, decoder,
  csr.csv, regions.ld and CtrlMemory unchanged.
- `tb/verilator/ctrl_service_budget/split_soc.py:401-445` `CpuPatches`: records the SoC's whole regions at the
  shipping split's input (`:426`, patched over `ctrl_memory.cpu_regions` at `:445`), so S2, S3 and the hooks harness
  keep their testbench region sizes; `cover` (default) is the shipping list and `:431` refuses one that is not its
  own power-of-two cover instead of widening it; `as-built` is the single-mask control; `:127` docstring.
- `tb/verilator/ctrl_region_decode/` (new): `run.py`, `region_soc.py`, `probe.S`, `sim_main.cpp`, `observe.vlt`,
  `decode.py`, `README.md`.
- `sw/litex/ctrl_memory_decode.py` (new) and `sw/litex/test_ctrl_memory.py:60,99,655,706,765,858,922,981`: the memory
  test's CPU decode arm, the split export check and six mutants (a helper module keeps test_ctrl_memory.py within the
  1,000-line idiom ratchet: it is exactly 1,000 lines).
- Docs: `docs/design/SPLIT_CONTROL_MEMORY.md:37` (new "The CPU's region decode") and `:388-391` (the cache section's
  #791 sentence; the OOC table predates the fix); `tb/verilator/ctrl_service_budget/README.md:150-155,1058`;
  `tb/verilator/ctrl_split_boot/README.md:51-52`.

## New checks (planted mutant, failing words)

CPU simulation, `run.py --self-test`: the shipping decode passes all 15 checks; each mutant must fail exactly its set,
in a run that reached its end word (`receipts/region-decode/self-test.log`):

| Check | Killed by | Failing words |
|---|---|---|
| rom/sram: a load / a fetch at its last word | neither: 0x3_7ffc has bit 15 clear, so the single mask admits it | - |
| rom: a load at each seam of its decode pieces reads its word from memory | single-mask | `0x0001fffc: trap cause 5; 0x0002fffc: trap cause 5` |
| rom: a fetch at each seam of its decode pieces executes it | single-mask | `0x0001fffc: trap cause 1; 0x0002fffc: trap cause 1` |
| rom/sram: a load one word past its end ... takes a load access fault (cause 5) before its bus | cover | `traps [], mcause [], mtval []; 1 command(s) for it on the bus` |
| rom/sram: a fetch one word past its end ... takes an instruction access fault (cause 1) before its bus | cover | `traps ['2'], mcause [2], mtval ['0x0']; 1 command(s) for it on the bus` |
| DECODE the fetch / the load decode admits exactly the SoC regions it may fetch / load | both | single-mask `first difference 0x00008000, refused inside the regions`; cover `first difference 0x00038000, admitted outside the regions` |

The single-mask mutant's netlist equals #878's as-built Arty CPU, and the cover mutant's equals #878's booting
diagnostic's, both apart from the module name (normalised sha256 `05cf9dd4cff156ec...` and `ca8f558f7d84ef07...` on
each side). The names themselves differ between runs: LiteX's netlist name also hashes run-specific state. The
region README's sentence "Its cover netlist is that bring-up's booting diagnostic's own" means this content
identity; a reviewer may want it to say "apart from its name", as the single-mask sentence does (left: a new commit
would void the gate pass).

test_ctrl_memory.py (`receipts/test_ctrl_memory/run.log`, 173 ok, 0 FAIL, `RESULT: PASS` at `03447eaa`):

| Mutant | Arm | Failing words |
|---|---|---|
| pieces unaligned | decode | `decode_pieces gives every region of up to 64 units ... (3711 wrong; ...` |
| the last piece dropped | decode | `decode_pieces gives rom and sram as 128, 64 and 32 KiB at their origins` |
| regions handed whole | decode | `cpu_regions hands the split SoC's list over as rom's and sram's pieces ...` |
| pieces handed after the name | decode | `exact_cpu_decode hands the CPU's naming step the pieces, before it names the netlist` |
| naming guard off | decode | `exact_cpu_decode refuses a CPU whose finalize never names its netlist (None)` |
| decode hookup removed | soc | `the split export hands the CPU generator rom and sram as their decode pieces ...` |

## Generated decode per split shape

`tools/product_decode.py` at `eb26f22d` (`03447eaa` changes only a README and a docstring): the builder's argv plus
`--ctrl-mailbox --ctrl-firmware` on a stand-in image of the shape at the split layout (`receipts/decode/`).

- 1x1 and 8x8 elaborate one CPU netlist, `VexiiRiscvLitex_f8b2743639f353f9ded505dea4bbc545` (sha256 `c9ce67a1...`).
  The generator is handed rom and sram as 128 + 64 + 32 KiB; the bus decoder has one exact compare per piece; DECODE
  PASS for fetch and load at every 32-bit address against the SoC's regions (DDR3 `main_ram`, CLINT and PLIC included).
- The Arty: no split config on this branch (#878's `endstation_arty_split.yaml` is not merged).
  `endstation_arty_current` with the split flags is refused by LiteX's PLL search at export. The region test's SoC is
  the split SoC without DDR3, the Arty's, and its mutant netlists are #878's (above).

## All-fabric CPU unchanged

`tools/allfabric_compare.py` (`receipts/allfabric/allfabric-compare.txt`, rc 0): for each of the five shipped configs,
the builder's outputs (endstation_builder.py), and milan_soc.py's export on the builder's own argv, base `1d6bf555`
against `03447eaa`:

- every builder output identical;
- the CPU netlist identical: name, bytes, the region rows the generator was handed, its arguments. AX7101 (both):
  `VexiiRiscvLitex_f5f08b170311db53220574624f819159`, sha256 `c208df0b...`. Arty (all three):
  `VexiiRiscvLitex_7c73187a77da20f7d3d54867209ef638`, sha256 `2ba0e339...`;
- AX7101: top Verilog, csr.csv, csr.json and soc.h identical apart from LiteX's header comments (the export's
  timestamp, and the hierarchy listing in the top's `/* */` block, whose order varies run to run);
- Arty: the export on the builder's argv is refused by LiteX's PLL search (`No PLL config found ... ClkOut3=333.33MHz`)
  at base and at head alike, after the identical CPU is named. Not this change's: the base does the same.
- both trees clean after the runs.

## Gate table (head `03447eaa` on clean clones unless stated)

| Gate | rc | Result | Receipt |
|---|---|---|---|
| region-decode self-test (shipping + both mutants) | 0 | `SELF-TEST PASS none / single-mask (4 of 4) / cover (6 of 6)` | `region-decode/` |
| split boot 1x1 | 0 | PASS, ready 84.425 ms (4,221,272 CPU cycles), trace 18 of 18, NATIVE 0 | `boot/1x1.*` |
| split boot 8x8 | 0 | PASS, ready 184.695 ms (9,234,743 CPU cycles), trace 18 of 18, NATIVE 0 | `boot/8x8.*` |
| S2 harness 1x1/1if (`--record-budget-findings`) | 0 | 18 groups graded, 0 refusals, 34 T_svc misses (34 of 141 probe instances, 13 of 81 paths) | `budget/1x1.*` |
| S2 harness 8x8/2if (`--record-budget-findings`) | 0 | 17 groups graded, 0 refusals, 63 T_svc misses (63 of 182, 31 of 129 paths) | `budget/8x8.*` |
| S2 harness `--self-test` | 0 | `self-test: 0 failures` | `budget/self-test.*` |
| test_ctrl_memory.py | 0 | 173 ok, 0 FAIL, RESULT: PASS | `test_ctrl_memory/` |
| all-fabric export compare, every shipped config | 0 | identical (above) | `allfabric/` |
| product split decode 1x1, 8x8 (at `eb26f22d`) | - | DECODE PASS, one netlist | `decode/` |
| full sweep, 4 native-shards units, `MAKEFLAGS=-j4 --no-print-directory`, shard 2 (capture_coherence) on 4 CPUs | 0, 1, 0, 0 | 65 suites: 64 passed; `gptp_shadow` (shard 1) failed with #833's `CLEANUP FAILED: owned descendants remain` (its RTL checks 325 of 325 and its 9 controls passed). Re-run once: rc 0, PASS. 2,192,899 checks, 0 in-suite failures | `sweep/` |
| git diff --check against the merge base `1d6bf555` | 0 | no output | `gates/diff-check.*` |
| check_py_idiom.py | 0 | at commit time, in the lane | - |
| workflow replay, every `run:` step of docs, elaborate, rtl-fast (firmware-boundary in the LiteX venv, firmware-verilator) and rtl: 69 job instances, each on its own clean clone | 0 | `497 steps ran, 0 failed or missing; 110 not run, each with its reason`. 68 instances success; `physical-gptp` skipped by its own `if:`. The 110: 41 APT resolutions (no apt here; the packages are installed), 28 sweep-shard and union steps (run once as the native sweep above), 27 source builds of the pinned Verilator and Yosys (already built here), 13 hosted GitHub API steps, the skipped job | `ci/replay-table.md`, `ci/not_run.json` |

The replay runs the round's listed gates as the workflows run them: `test_builder.py --require-rv32` (docs builder
legs), behave (rtl-fast bdd-conformance), `test_ctrl_firmware.py --require-rv32 --self-test` (firmware-unit and the
three firmware mutant jobs), `fw_coverage.py --check` (firmware-unit), firmware-boundary in the LiteX venv and
firmware-verilator.

## Observation (candidate issue, not in scope)

Under the cover decode, in an earlier test draft whose banks filled only the region, a speculative instruction-cache
refill of the line just past rom's end was answered `err` by CtrlMemory's hole, and it never completed
(`receipts/observations/cover-err-hole-refill.sim.log`: `FETCH 644 00038000`, then nothing for the 5 ms limit). With
the exact decode such a refill never reaches the bus. Whether a refill into the hole inside a region (past the
image's banks) stalls the same way was not measured.

Also: at the pinned generator the data port's PMA admits a store wherever it admits a load, whatever the region's
mode (stores to `rom` and the flash window reach the bus; rom's banks drop them). Pre-existing, not graded here.

## Scratch left

`/data-2/milan/tmp/791-a765`: clones (base, final, final-af), final/ runs, explore/, ci/ (replay jobs and moved
attempts), tmpci/, sweep/ and sweep-killed-by-reset/, product/, allfabric/. Shard clones
`$LANES/791-a765-shard0..3`. The interim session's relocated generator and sbt copies were deleted
(231 MB and 1.2 MB, cited by no receipt).
