[A826] ROUND 5 - REVIEW READY

Head: 9acb9b828b29aba71bd51303a4836f86c2278267. Branch: pf-loopbram-1. PR #987 into dev-soft-core; issue #979.
Delta from the reviewed head dc78aedae34c25a97125ecd6816a1f645db5575f; implementation base 3cda030c174b325e36c26af6420487ff91346d15.
No push, issue/PR comment, merge, board, bench or test-machine access occurred.

## Commits since dc78aeda

| Commit | Subject |
|---|---|
| 7d19336f61cec0edde5b6aca32a83932d312f039 | Grade every loopback output stream's delivery in the parent test |
| fbcaba2fb9ac01a3a3c613ab5aa186bd72a8f860 | Register the loopback suites and parent campaign in the test inventories |
| 68ff356fccc0be4b7f9063d7d926ca425ddef857 | Annotate the loopback test scripts and wrap their long lines |
| 1f3e7eb0e0ccf06648461abe41e14bb0abdc6836 | Bring the loopback tests within the idiom and host-deadline gates |
| 128909ef8b1396cf572777cbd14121b4efc08369 | Add loopback page contents and regenerate the documentation inventories |
| be69935f624171a2f4c172fd864ecc749c91c985 | State both cold timings behind the loopback suite figures |
| 9acb9b828b29aba71bd51303a4836f86c2278267 | Print the leaf loopback tally in a shape the sweep counts |

No RTL changed. Against dc78aeda, nothing under `sw/`, `configs/`, the six submodules or
`.github/` changed. Under `hdl/` only three Markdown files changed: the parameter page's
contents list and two generated test-reference tables. Every non-Markdown byte under
`hdl/` is identical, which [source-binding.json](receipts/source-binding.json.txt) records.

## Finding closures

Closure labels below are the author's dispositions; each finding is cleared only by its reviewer.

### R909-2-N1 BLOCKER: suites missing from SUITE_SECONDS - CLOSED

`scripts/suite_shards.py` registers `input_loopback` at 38 s and `input_loopback_dp` at 107 s.
Both figures are measured, not provisional. Each comes from the sweep's own
`make -C tb/verilator/<suite>` command, run cold on four pinned CPUs under host load
average about 120. The longer of two runs took 23.8 s and 67.7 s, on the uncommitted tree that
became 7d19336f. The runs at 128909ef took 22.1 s and 59.6 s. Later commits change only the
leaf's result-line format and one documentation sentence. Each figure is the longer run scaled
by 1.58 and rounded up.
That follows the repository's stated precedent for `ship8`.
`docs/testing/TESTING.md` records this provenance and that the hosted windows are owed.
Three surplus blank lines were removed, so the module stays at 999 lines, under the
1000-line ratchet. The suites are not in `PROVISIONAL_SUITES`, because that list
requires the `suite_timeout` figure rather than a measurement.

| Check at 9acb9b82 | Result |
|---|---|
| `python3 scripts/suite_shards.py --selftest` | `selftest: PASS`, exit 0 |
| `scripts/run_all_suites.sh --ci-pieces --shard i/19 --list`, i = 0..18 | 19 of 19 exit 0 |
| Ownership | each new suite owned exactly once: `input_loopback_dp` worker 15, `input_loopback` worker 16 |
| Predicted worker load | maximum 1615 s (worker 0, `follow_ring` alone, unchanged), bound 1620 s; workers 15 and 16 at 1508 s and 1507 s; all below 30 minutes |
| `scripts/run_all_suites.sh <out> --ci-pieces --shard 15/19` through the driver, preflight included | exit 0: 8 of 8 suites pass, including `input_loopback_dp`; 662439 checks, 0 in-suite failures, complete accounting |
| `scripts/run_all_suites.sh <out> --ci-pieces --shard 16/19` | exit 0: 9 of 9 suites pass, including `input_loopback`; 356128 checks, 0 in-suite failures, complete accounting. At be69935f this shard exited 90 on the leaf tally shape, fixed below |

The complete 19-shard serial sweep was not run; it is about eight hours serial.
The two shards that own the new suites ran through the real driver, preflight and tally.
The PR body's gate claim now names exactly what ran.

### R910-2-F1 MAJOR: a missing output stream passed - CLOSED

`tb/verilator/input_loopback_dp/sim_main.cpp` now grades delivery per configured output stream in
both traffic phases: the edit phase, and the clipped phase after the boot-clip reset. Each phase
records, per stream, the captured words, the delivered words, the packets and the peak backlog.
At each phase's completion point, before the reset discards the tail, two named checks run per stream:

- `WIRE_STREAM_DELIVERY <phase> stream <s>`: at least 16 packets of the stream's own words
  (the clipped phase carries 24), and delivered words within one packet of captured words.
- `WIRE_STREAM_COMPLETE <phase> stream <s>`: the undelivered tail and the peak backlog are
  each at most one packet (48 words). This is the bounded partial-packet tail.

Every existing sample, silence, mapping, coverage, deadline and aggregate assertion is unchanged;
the diff adds checks and removes none.

| Run at 9acb9b82 | Checks | Failures | Detail |
|---|---:|---:|---|
| Clean 1x1 | 16173 | 0 | per phase: 64 and 24 packets, peak backlog 48 |
| Clean 8x8 | 122549 | 0 | every stream, both phases: 64 and 24 packets, peak backlog 48, tail at most 24 |
| R910-2's exact plant, `.stream_en_i (aaf_stream_en_w & N_STREAMS'(8'h7f))` | 113837 | 4 | `WIRE_STREAM_DELIVERY` and `WIRE_STREAM_COMPLETE` for stream 7 in both phases; stream 7 captured 3088 words, delivered 0; 616 packets |

The campaign `tb/verilator/input_loopback_dp/mutants.py` now holds 2 controls and 15 plants.
All 17 pass at 9acb9b82 ([results](receipts/gates--parent-plants--results.json.txt)). A held output
is planted at each 8x8 talker 0-7, one of which is R910-2's exact text, and at the 1x1 talker.
Each plant must fail both named checks for its stream in both phases; a compile failure
counts as no detection. R909-2-S1 is adopted: both parent connection plants now also run at 1x1.

### R909-2-N3 MINOR: parent campaign not registered - CLOSED

`docs/testing/TESTING.md` lists the parent controls and campaign as an explicit campaign.
Its trigger covers changes to the `milan_datapath.sv` map writers, `g_input_invalidation`, the
talker enable, the queue or capture packed loopback fields, and the harness itself.

### R910-2-F2 MAJOR / R909-2-N2 MINOR: enabled 8x8 route - CLOSED at the floor

The enabled 8x8/1if image was exported and routed from this round's source: the RTL,
`sw/`, `configs/` and submodule bytes of 9acb9b82. The export kept the product's control-memory refusal
and measured the allocation. Synthesis used AreaOptimized_high, then opt ExploreArea,
through `vivado-slot.sh` with VIVADO_SLOTS=2 and VIVADO_MIN_GB=20. Vendor runs went one at a time.

The release placement directive missed the floor, so the other two prescribed directives were
routed from the same post-opt checkpoint, and the best is selected.

| Placement | Min setup (4 corners) | Min hold | Failing endpoints | Routing errors | LUT | FF | BRAM tiles | DSP | Floor |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ExtraPostPlacementOpt (release) | +0.008 ns | +0.036 ns | 0 | 0 | 48883 | 54671 | 111 | 11 | MISS (setup < +0.030) |
| AltSpreadLogic_high | +0.223 ns | +0.036 ns | 0 | 0 | 48901 | 54672 | 111 | 11 | PASS |
| ExtraTimingOpt | +0.003 ns | +0.036 ns | 0 | 0 | 48960 | 54671 | 111 | 11 | MISS (setup < +0.030) |

Selected: AltSpreadLogic_high, the only recipe of the three that meets #818. Its corners are
Slow 0 C and Slow 85 C at +0.223 ns setup and +0.102 ns hold, and Fast 0 C and Fast 85 C at
+1.436 ns setup and +0.036 ns hold. RAMB36 94 and RAMB18 34; 15774 occupied slices; 96133 of
96133 routable nets fully routed. All four signoff corner reports of all three recipes are in
the receipts with their hashes.
Every recipe's worst setup path is in the mailbox on the 100 MHz system clock, 76-81% routing
delay, and none is in the loopback logic. Release: `KL_mbx/u_evt/pend_r_reg[0]` to
`ctr_seen_r_reg[0][4]`. ExtraTimingOpt: `KL_mbx/u_evt/pend_r_reg[11]` to `asp_cnt_r_reg[0][15]`.
Selected: `KL_mbx/u_rx/hrd_r_reg` to `KL_mbx/reg_rdata_r_reg[21]`. The margin is placement-sensitive.
At 855529fe, round 3 met the floor with all three recipes: +0.171, +0.295 and +0.215 ns.
Here one of three meets it. The four vendor runs were sequential, in slot 0, with MemAvailable
at least 61 GB at each start ([slot use](receipts/slot-usage.json.txt)).

Control memory: 70.5 tiles (ROM 39 RAMB36 plus 1 RAMB18, SRAM 31 RAMB36), against the default 56.
That is S14 debt: 11.5 tiles above the unchanged 59-tile ledger, 14.5 above the default.
The ordinary allocator still refuses it; the export measures it without relaxing the refusal.
The enabled 8x8 firmware ELF is byte-identical to round 4's (`f9470e29...`).

The enabled 1x1 route was not repeated, because no RTL changed this round. Round 4's 1x1 route
at dc78aeda stands for identical RTL.

### Disabled identity - unchanged by construction

No RTL, firmware, configuration or submodule byte changed since dc78aeda. The round-4
canonical elaborated-netlist hashes and the equal utilization at 1x1/1if and 8x8/1if therefore
describe this head unchanged. Neither was re-run.

| Shape | Canonical SHA256, base = head |
|---|---|
| 1x1/1if | 18af89e620ea88ee2a745550bd25b1645702cec071bcba36decced2b5376d9af |
| 8x8/1if | fe344bba8709f7b8e72075b38aa81619c316c2207f948e0adaea1540e36da767 |

R909-2-S2 noted that these hashes reproduce only from identical export inputs, because the
generated CPU wrapper's name hashes them. That is stated here rather than changed in a recipe.

### Gate failures found by the author this round - FIXED

Seven gates failed on files this PR adds, and the pushed head dc78aeda carries the bytes behind
every one. Hosted docs CI and the hosted Verilator aggregate would therefore fail there. The
Python idiom gate was run first on the working tree. Five docs gates failed when the docs workflow
was replayed at the intermediate head 68ff356f. The sweep tally failed when the new suites first
ran through the sweep driver at be69935f:

| Gate | Cause | Fix |
|---|---|---|
| Python idiom | unannotated or undocumented functions and long lines in the loopback scripts | annotated, documented, wrapped; the render-queue anchor literal is split, AST-identical |
| C and C++ idiom | `std::atoi(std::getenv(...))` in the leaf harness; six multi-declarator lines in the parent harness | bounded `strtol` that refuses a malformed value; one declarator per line |
| Test-evidence ratchet | two unexplained DUT-source readers; four new host process deadlines | dispositions for both campaigns; the `timeout=` arguments are removed, so the sweep's own guard bounds them |
| Traceability matrix | the leaf suite's coverage was not generated | regenerated |
| Per-page contents | no contents list on the design page; parameter page list drifted | written contents lists with descriptions |
| Documentation inventory | three new pages | regenerated |
| Sweep tally, run by every hosted Verilator worker | the leaf suite printed `checks=N ... failures=M`, which `scripts/suite_tally.py` does not read; shard 16 exited 90, an incomplete check accounting | the result line keeps its `PASS/FAIL input-loopback` prefix and prints `N checks, M failures`; the tally reads 155604 checks in two tallies, and a planted failing line is refused |

R909-2-R1 is also fixed. The leaf README now says that bind flush is covered only together with
map invalidation, and that the bind-only term is untested.
R909-2-S3 (a parent run at the release clock) and S4 (clamping a harmless one-past index)
are not adopted. S4 would change RTL and so reopen the identity proof.

## Validation at 9acb9b82

| Gate | Result |
|---|---|
| Mutation anchors (base 3cda030c to head) | PASS, `ANCHORS INTACT 0` |
| Planner self-test; 19 shard listings | PASS; 19 of 19 exit 0 |
| Python idiom gate and self-test | PASS |
| RTL lint (`scripts/lint_rtl.py --check`) | PASS |
| docs_check, doc style, added-line em-dash (from 3cda030c) | PASS |
| xvlog gate | PASS |
| Parent campaign (2 controls, 15 plants) | PASS, 17 of 17 |
| Leaf campaign (control, 7 plants) | PASS |
| Leaf bounds (lead-3 refusal, stamp window inside/outside, both shapes) | PASS |
| `input_loopback` 8x8 and 1x1 | PASS, 79587 and 76017 checks |
| `input_loopback_dp` (both shapes) | PASS, 16173 and 122549 checks |
| `render_queue all` | PASS, 28 of 28 campaign checks |
| `chmap_capture` | PASS |
| `milan_dp run` | PASS |
| `capture_coherence run dp` | PASS, 847 checks |
| `milan_dp_render` `run`, `ship8` and the full `tdm8render-mutants` campaign | PASS: `run` and `ship8` exit 0 (three RESULT: PASS legs); campaign 32 of 32 (5 positive controls, 3 leg defects, 3 clean controls, 21 mutations), executed in pieces |
| Coherence mutants | PASS, 42 of 42 |
| Portability (63 tops) | PASS, 63 of 63, 0 FAIL |
| Reviewer probes | PASS: 6 expectation probes met, 12 observe-only identical to round 4 |
| Disabled leaf in context, base / head | capture 4339 / 4339 LUT, 3961 / 3961 FF; queue 1017 / 1015 LUT, 406 / 406 FF |
| Builder union (two legs, elaboration and RV32 required) | PASS, 114 entries; one unchanged calibration row NOT RUN |
| Sweep driver, shards 15/19 and 16/19 | PASS, exit 0, complete accounting |
| Docs workflow replay, 43 steps (merge base dd163e41) | PASS, 0 failures; lane tree clean after every step |

The render campaign runs its arms serially, about 7300 s at round 4. The session's tracked-job limit
of two hours stopped the first single run after `run`, `ship8` and 5 mutants, all passing. The
campaign was then executed at this head through the runner's own functions: `run_positive_controls`,
`run_leg_defects`, `run_clean_controls` and `run_mutations`, over disjoint parts of its own tables, each
in its own temporary directory. The union is checked to be exactly the runner's 32 arms
([combined verdict](receipts/gates--render-campaign.json.txt)). No arm, table entry or expectation
was changed. The stopped serial run is kept as a superseded receipt.

The docs workflow replay ran each gate step of `.github/workflows/docs.yml` in the lane checkout.
It used the pinned Markdown environment and judged added lines against the merge base dd163e41.
The no-git job ran in an exported copy. Skipped: installs, caches, uploads, submodule fetches
(already initialized), evidence records, the fail-fast, gate-inventory and manifest jobs, and the
two builder legs. The builder
union group runs a superset of those legs. A builder union attempt that ran concurrently with
the replay was refused, because the entity-shape self-test temporarily rewrites
`tb/verilator/csr/Makefile`. The rerun result above was taken alone; the refused attempt is kept
as a superseded receipt.

All long jobs ran as tracked jobs that this session waited on to completion. The tool's foreground
limit is ten minutes, so foreground waits polled them. No detached process was started, and none of this
lane's processes remain.

[Commands, hashes, logs and route reports](receipts/INDEX.md). Files are plain text below 200 KB.

This is author evidence, not a reviewer verdict or a clean-lens ledger. Independent re-review,
manager publication, hosted and act workflow acceptance, and live-base candidate-merge
validation remain separate.
