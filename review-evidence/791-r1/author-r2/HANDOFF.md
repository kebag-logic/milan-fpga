# A765c HANDOFF: round 2 of #791 (the split CPU's region decode), PR #888

PRIVATE. Nothing pushed. Lane $LANES/791-region-decode, branch `791-split-region-decode`, base
`dev-soft-core` `1d6bf555`, round-1 head `03447eaa`. origin/dev-soft-core moved during the round to `764482b4`
(#874, S7: lwSRP's transmit path); it touches none of this branch's files and `git merge-tree` of the head with it
is clean (rc 0). No rebase: the candidate merge validation is the manager's. Authority: the round-2
ruling on #791 ([A10]), R825-1 (POSITIVE) and R826-1 (NEGATIVE: F1 MINOR; F2 SUGGESTION, taken by the ruling; F3,
F4 RESIDUE).

## Status: REVIEW READY (every ruling item done; every gate rc 0 at `596e2ae3`; no STOP condition met)

Head `596e2ae3708c4693e0929b530fea37020dc8db25`, five commits on `03447eaa`, no merge, rebase, force or amend:

- `3344c581` Refuse a split CPU whose generator may read a region list other than its naming step's aligned pieces, and name the decode checks in the re-pin procedure (#791)
- `d91e8ef1` State the region decode's root cause as the pinned generator behaves: only a region based at 0 is taken whole, so rom was inexact and sram exact (#791)
- `1b77f2a5` Build the harness's as-built control without the region-decode hookup, so the new aligned-pieces refusal leaves the single-mask control buildable (#791)
- `723db89c` Link the region-decode simulation and test_ctrl_memory.py from the LiteX re-pin procedure (#791)
- `596e2ae3` Document the region-row test in cpu_region_lists, as the Python idiom gate requires (#791)

Why five: `1b77f2a5` because the region self-test at `d91e8ef1` showed the new aligned refusal also refused the
harness's single-mask control; `723db89c` because the replay's link-health gate (`docs_check.py`) at `1b77f2a5`
flagged a bare README path (`sw/litex/patches/README.md:40: bare reference ... make it a link`); `596e2ae3` because
`check_py_idiom.py` flagged the nested `rows` helper as an undocumented public function. Every gate in the table
below ran at `596e2ae3`; runs at the superseded heads are not cited as evidence.

| Ruling item | State |
|---|---|
| TAKEN on #791 | posted, issuecomment-6797883336 (`receipts/posts/taken.md`) |
| 1. Root cause as the generator behaves (F1) | done (below); checked against R826-1's `generator_terms.txt` |
| 2. Naming guard after finalize, a test of both silent shapes, the re-pin procedure, PR wording (F2) | done (below) |
| 3. Residue F3, F4 with the exact texts | done |
| 4. Gates on a clean clone of the final head | done, all rc 0 (table below) |
| REVIEW READY on #791 | posted, issuecomment-6802190574 (`receipts/posts/review-ready.md`) |
| STOP condition: a generated CPU netlist or an all-fabric export byte changed | not met: none changed (below) |

## Changes (file:line, reason)

All line numbers at `596e2ae3`.

### Ruling item 1 (F1): the root cause as the pinned generator behaves

- `docs/design/SPLIT_CONTROL_MEMORY.md:38-43`: the generator splits each region into aligned power-of-two terms
  (SpinalHDL `AddressMapping.terms`). A region based at 0 is the exception, taken whole as the one term
  `(address & ~(size - 1)) == 0`. So `rom` became `(address & 0xfffc8000) == 0`, while `sram` at 0x1000_0000 was
  already exact as 128, 64 and 32 KiB terms. Checked against `Misc.scala:54-80` (`step = if(ptr == 0) m.size`) and
  the as-built netlist's fetch terms quoted in R826-1's `receipts/probes/generator_terms.txt`: `rom` mask
  `32'hfffc8000 == 0`; `sram` `32'hfffe0000 == 32'h10000000`, `32'hffff0000 == 32'h10020000`,
  `32'hffff8000 == 32'h10030000`. `~(0x38000 - 1) = 0xfffc8000`. That netlist,
  `VexiiRiscvLitex_18be4f88...`, sha256 `d425a0e7...`, is this round's single-mask CPU
  (`receipts/gates/netlist-identity.log`).
- `:47-48`: each piece is an aligned power of two, which one mask compare decodes exactly, at 0 as anywhere else,
  so handing the pieces makes every region exact without depending on the decomposition. (An aligned
  power-of-two piece comes out of `AddressMapping.terms` as one term: at 0, `step = size`; elsewhere the
  origin's lowest set bit, or failing that the end's, is the size.)
- `:396`: names `rom` only ("The non-power-of-two `rom` decode of #791").
- `sw/litex/ctrl_memory.py:139-149`: the `decode_pieces` docstring says the same.
- PR body: "The fault (#791)" paragraph says the same (`PR-BODY.md`).

### Ruling item 2 (F2): the naming guard

- `sw/litex/milan_soc.py:3239` `exact_cpu_decode`, docstring `:3250-3258`, finalize `:3271-3285`: after LiteX's
  finalize and the existing never-named refusal (`:3274`), it also refuses unless every region-shaped list the
  CPU holds, on the instance or on any class of it, equals the naming step's list (`:3278`), and that list is
  aligned powers of two (`:3279-3280`). The stray refusal names the netlist for removal from the generator's
  cache: in those shapes the pinned LiteX's finalize has already generated a netlist under the pieces' name from
  another list. `pieces = ... if named else []` (`:3277`) keeps the never-named refusal the one that fires first.
- `sw/litex/milan_soc.py:3291` `cpu_region_lists`: every non-empty list of `(int, int, str, str)` rows held by
  the instance or any class in its MRO, by where it is held. Reason: the generator's list at the pin is
  `VexiiRiscv.memory_regions`; a re-pin may keep it on the instance (under that name, which the instance reads
  first, or another), so the guard reads every list the generator could be handed, not one name.
- `tb/verilator/ctrl_service_budget/split_soc.py:407-411, 428-440, 451-452` `CpuPatches`: `as-built` now builds
  the SoC without the hookup (`milan_soc.exact_cpu_decode` patched to a no-op inside `applied()`) and records the
  SoC's regions in its naming step. Reason: the new aligned refusal refused the control, which hands the
  generator the whole regions (region self-test at `d91e8ef1`: `single-mask` REFUSED, `the naming step's list is
  not aligned powers of two`). The control is now the pre-#791 SoC. It hands the generator the same rows as
  before, so its netlist name, an MD5 over every generator input, is unchanged (`18be4f88` at both heads).
  `cover` is unchanged in behaviour (`split_regions` returned `self.split(regions)` for it before too).
- `tb/verilator/ctrl_service_budget/README.md:155`: the as-built control described as built without the hookup.
- `sw/litex/patches/README.md:38-52`: at any LiteX or generator re-pin, run `test_ctrl_memory.py` and
  `tb/verilator/ctrl_region_decode/run.py --self-test`, with the reason (no workflow runs the region test).
- `docs/design/SPLIT_CONTROL_MEMORY.md:54-58`: the two refusals, the cache-entry note, the re-pin pointer.
- PR wording: "a LiteX that stops calling the naming step is refused" (`PR-BODY.md`), replacing round 1's
  "cannot silently restore the single mask".

### Ruling item 3: residue

- F3, `tb/verilator/ctrl_region_decode/README.md:7`: R826-1's exact text.
- F4, `tb/verilator/ctrl_region_decode/README.md:101`: R826-1's exact text.

## New checks, planted mutants and failing words

All in `sw/litex/ctrl_memory_decode.py` (the `decode` arm of `test_ctrl_memory.py`), property `region list guard`
(`:50`). The stand-in finalize shapes are `SHAPES` (`:81`), built by `standin` (`:113`).

| Check (`:line`) | What it requires |
|---|---|
| `:177-180` | the never-named finalize is refused in the never-named refusal's own words (`no longer names it through generate_netlist_name`); tightened so the round-1 mutant `naming guard off` fails by name, not by an IndexError |
| `:181-186`, one per SHAPES row | re-collected after naming; kept on the instance as `memory_regions`; kept on the instance as `generator_regions` (R826-1's probe's name): each refused with `region list other than the pieces` and `#791`, after the naming step saw the pieces |
| `:187-190` | a naming step whose list is not aligned powers of two (`ctrl_memory.cpu_regions` patched to `list`) is refused with `not aligned powers of two` |

| Mutant (`:line`) | Edit | Fails with (`receipts/tcm/run.log`) |
|---|---|---|
| `region list check off` (`:69`) | `if stray or not all(` -> `if not all(` | `exact_cpu_decode refuses a CPU whose generator may read the whole rows after naming: re-collected after naming (None)` |
| `unaligned pieces let through` (`:71`) | the alignment test -> `True` | `exact_cpu_decode refuses a CPU whose naming step's list is not aligned powers of two (None)` |
| `the pieces themselves refused` (`:73`) | `if rows != pieces)` -> `if True)` | `exact_cpu_decode hands the CPU's naming step the pieces, before it names the netlist (..., the split CPU's generator may not read its exact region pieces ...: a region list other than the pieces is held at ['VexiiRiscv.memory_regions'] ...)` |
| `the instance not searched` (`:75`) | the instance dropped from `cpu_region_lists` | `... after naming: kept on the instance (None)` |
| `the classes not searched` (`:77`) | the classes dropped from `cpu_region_lists` | `... after naming: re-collected after naming (None)` |
| `naming guard off` (round 1's, now caught by name) | `if not named:` -> `if False:` | `exact_cpu_decode refuses a CPU whose finalize never names its netlist (the split CPU's generator may not read its exact region pieces []: ...)` |

R826-1's own probes, run unchanged on this head:
- `guard_probe.py` (`receipts/probes/guard_probe.log`): `list re-collected after naming: refused`, `list kept on
  the instance: refused`; both were `BUILT SINGLE-MASK SILENTLY` at `03447eaa`. `pinned order: built exact`.
- `cpupatches_probe.py` (`receipts/probes/cpupatches_probe.log`): `cover` builds with the shipping split and
  refuses with the split undone or the hookup absent, as at `03447eaa`; `as-built` builds and hands over the
  whole regions in every case, and now records the SoC's regions with the hookup absent too.

## Netlist identity (the ruling's STOP condition: not met)

`receipts/gates/netlist-identity.log`, rc 0, `tools/netlist_identity.py`; one environment (`PYTHONHASHSEED=0`)
for both heads. LiteX names a netlist by an MD5 over every generator input, so one name at both heads is one
generator input, and both builds elaborate the one cached file:

| CPU | `596e2ae3` | `03447eaa` | cached netlist sha256 |
|---|---|---|---|
| region test, shipping | `88c5cdf9` | `88c5cdf9` | `6b5a22fc...` |
| region test, single-mask control | `18be4f88` | `18be4f88` | `d425a0e7...` (= R826-1's as-built netlist) |
| region test, cover control | `57948043` | `57948043` | `b47ecbdf...` |
| product split export, 1x1 and 8x8 | `f8b27436` | `f8b27436` | `c9ce67a1...` (= round 1's `decode/` receipt) |
| split boot, 1x1 and 8x8 | `99bc789b` | R826-1 records `99bc789b` for both | `1fde79b5...` |

No run logged a generator command: every netlist was read from the cache, none generated. All-fabric:
`receipts/allfabric/allfabric-compare.txt`, base `1d6bf555` against `596e2ae3`, every shipped config: every
builder output identical; CPU netlist names and bytes identical (AX7101 `f5f08b17`, Arty `7c73187a`, whose export
LiteX's PLL search refuses after naming, at base and head alike); at AX7101 the top Verilog, `csr.csv` and `soc.h`
differ in comment lines only (generation timestamps), as at round 1; `0 failure(s)`.

## Gate table (head `596e2ae3`, clean clones of it; receipts under `receipts/`, index `receipts/INDEX.md`)

| Gate | rc | Result | Receipt |
|---|---|---|---|
| `test_ctrl_memory.py` (every mutant, and the new guard checks) | 0 | 182 `[ok  ]`, 0 `[FAIL]`, `test_ctrl_memory: 0 failure(s)`, `RESULT: PASS` | `tcm/` |
| region-decode `run.py --self-test` | 0 | `SELF-TEST PASS none: fails 0 check(s), wants 0`; `single-mask: fails 4, wants 4`; `cover: fails 6, wants 6`; `ctrl_region_decode self-test: PASS` | `region-decode/` |
| split export decode check (product split export, 1x1 and 8x8) | 0 | both: fetch and load `DECODE PASS`, one netlist `f8b27436` | `decode/` |
| all-fabric export compare, every shipped config, base `1d6bf555` | 0 | identical (above), `0 failure(s)` | `allfabric/` |
| netlist identity against `03447eaa` | 0 | `0 difference(s)`, no netlist generated | `gates/netlist-identity.*` |
| R826-1's guard and CpuPatches probes | 0 | both silent shapes refused | `probes/` |
| split boot 1x1 / 8x8 | 0 / 0 | `ctrl_split_boot: PASS (0 finding(s))`, ready 84.425 ms / 184.695 ms, trace's first 18 equal; as round 1 | `boot/` |
| S2 harness `--self-test` | 0 | `self-test: 0 failures` | `budget/selftest.*` |
| S2 harness 1x1/1if (`--record-budget-findings`) | 0 | `18 groups graded, 0 refusals, 34 T_svc misses (34 of 141 probe instances, 13 of 81 paths)`; round 1's line | `budget/1x1.*` |
| S2 harness 8x8/2if (`--record-budget-findings`) | 0 | `17 groups graded, 0 refusals, 63 T_svc misses (63 of 182 probe instances, 31 of 129 paths)`; round 1's line | `budget/8x8.*` |
| `git diff --check` against the merge base `1d6bf555` | 0 | no output | `gates/diff-check.*` |
| full sweep: 4 native-shards units, `MAKEFLAGS=-j4 --no-print-directory`, CPUs 0-7, 40-47, 60-63, 64-71; shard 2 (capture_coherence) on 60-63, 4 CPUs | 0, 0, 0, 0 | 65 suites (15 + 17 + 17 + 16), 65 passed, 0 timed out; 2,192,899 checks, 0 in-suite failures. No #833 failure this run, so no re-run | `sweep/` |
| workflow replay: every `run:` step of docs, elaborate, rtl-fast (firmware-boundary in the LiteX venv, firmware-verilator) and rtl, 69 job instances, each on its own clean clone of the head | 0 | `497 steps ran, 0 failed or missing; 110 not run, each with its reason`. 68 instances success; `physical-gptp` skipped by its own `if:`. The 110: 41 APT resolutions (no apt here; the packages are installed), 28 sweep-shard and union steps (run once as the sweep above), 27 source builds of the pinned Verilator and Yosys (already built here), 13 hosted GitHub API steps, the skipped job | `ci/replay-table.md`, `ci/not_run.json` |
| elaborate-gates-1 first attempt (moved aside, re-run once) | 92 | `TIMEOUT test_soc_timing_cuts (900s wall clock - result UNKNOWN, not a failure)` at host load about 100; `elaborate` then refused (`elaborate-gates-1: dependent job failed`). `test_soc_timing_cuts` does not reach the split path (no `ctrl_mailbox`, `ctrl_memory` or `exact_cpu_decode` in it). Re-run: `PASS test_soc_timing_cuts`, `simulations: 8 passed: 8`; `elaborate`, its manifest and cancel tail then success | `ci/attempt-1-*`, `ci/attempt-2-elaborate-gates-1-gate_19.log` |
| check_py_idiom.py, docs_check.py, check_doc_paths.py, check_doc_style.py | 0 | in the lane before commit; and in the replay (docs-gates-0) | `ci/replay-table.md` |

The replay runs the round's listed gates as the workflows run them: `test_builder.py --require-rv32` (docs-gates-1
and -2, builder legs 0 and 1), behave (rtl-fast bdd-conformance), `test_ctrl_firmware.py --require-rv32
--self-test` in four shards (firmware-unit and the three firmware mutant jobs), which drives every firmware mutant
driver (`acmp`, `acmp_review`, `aecp`, `ctrl`, `maap`, `plat`, `srp`, `srp_pub`), `fw_coverage.py --check`
(firmware-unit), firmware-boundary in the LiteX venv, and firmware-verilator. Every `run:` step of docs.yml is in
the replay (the docs jobs).

Replay tool changes this round (in `tools/ci/`, not in the tree): its scratch paths and unit names; `local` also
waits while the host has under 20 GB available (the rule for running beside the sweep); `tick` claims an instance
before launching it, as `local` does, so the two never run one instance twice. While the sweep ran, MemAvailable fell
to 1.7 GB for a few minutes from another lane's two Vivado runs (27 GB together); my unit held 4.6 GB. The four
round-1-code loops were stopped by PID between jobs (their running jobs finished and wrote their results) and
replaced by memory-aware loops.

## Not done / limits

- The guard reads the region lists held on the CPU and its classes after LiteX's finalize; a re-pin that hands the
  generator a list held nowhere on the CPU is caught only by the split export check and the region simulation at
  the re-pin (now named in the re-pin procedure). Stated in the PR body's limits.
- Physical calibration NOT RUN; no hardware, bench, Vivado route or flash was used.
- Hosted contexts at this head: not read (nothing pushed).

## Scratch

`/data-2/milan/tmp/791-a765c` (4.7 GB): clones (base, r1, r1-pd, head, head-pd, head-af, head-sims), final/ (this
head's runs), r1/ (the runs at `03447eaa`), superseded/ (runs at `d91e8ef1` and `1b77f2a5`, cited by no receipt
except the one link-gate log), ci/ (replay jobs, attempts, the superseded head's three jobs), tmpci/, sweep/.
Shard clones `$LANES/791-a765c-shard0..3`. No generator netlist was added to the shared cache by this
session (newest entry 14:53, before it started; no run logged a generator command).
