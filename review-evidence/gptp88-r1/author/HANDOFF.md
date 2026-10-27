# [A690] HANDOFF — FPGA-gPTP #87 + #88 (Announce qualification, pathTrace without TLV)

Status: STOP. Every gate below is complete. Repository gates: all rc 0 at base and head. Parent consumer list: 15/15 rc 0 at base and head; the extra tsn_fuzz row fails at head as described.

- Repository: Mister-M-alt/FPGA-gPTP, branch `87-88-announce-pathtrace` (local, not pushed)
- Base: main `55680bff3b287b9a7b0c759f51471fa617c17335`
- Head: `2ae9a9579fb863237e931d330c700c71c15782af`, one commit: "Qualify an Announce whose PathTrace count differs from stepsRemoved+1 (#88)"
- Assignment: #88 issuecomment-6434676531 (with the #87 ruling, #87 issuecomment-6434676823)
- TAKEN: #88 issuecomment-6435134986
- STOP (with head `2ae9a957`): #88 issuecomment-6440962747

## Outcome

Delivered, with no port, parameter, register-map or ROM-image change: the #88 count refusal is removed. A path headed by its grandmaster is accepted at any length and published as received plus thisClock.

STOP on the rest. It needs a top-level port change, the assignment's STOP condition:

- the #88 head refusal;
- #87's keep-previous publication;
- the related zero-length-TLV refusal.

## Finding that triggers the STOP condition

The engine's publication ABI has no entry-zero channel for the path:

- `hdl/top/KL_gptp_engine.sv:118-124`: `pub_path_count_o` counts "the separately published GM at slot zero"; `pub_path_o` carries slots 1..7 only.
- `docs/INTEGRATION.md:458-460`: "Counts include the separately published grandmaster."
- milan-fpga dev `97aab1d0`: `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:666-669` takes the served head from `pub_gm_id_o`. `hdl/milan/milan_datapath.sv:2300` and `:6283-6299` say: "Entry 0, when count is nonzero, is the selected owner's grandmaster; entries 1.. are its PathTrace tail."

In each case below pathTrace[0] is not grandmasterIdentity, so the current ports can't serve it as GET_AS_PATH (IEEE 1722.1-2021 7.4.41.2):

| Case | 802.1AS-2011 (+Cor1/Cor2) pathTrace | What the ABI can serve |
|---|---|---|
| #88: path {X, B} from GM G, X != G | {X, B, thisClock} (10.3.10.2.1 d)) | {G, B, thisClock} |
| #87: after reset, a better GM G without a TLV | {thisClock} kept (10.3.12.1.4 i), Cor1; d) writes nothing without a TLV) | {G} if count 1 is kept |
| #87: GM G1 -> G2 on a TLV-less Announce | {G1, ..., thisClock} kept | {G2, ..., thisClock} |
| Related: a zero-length path trace TLV (N = 0), still refused at `hdl/wire/KL_gptp_rx_parser.sv:319` | {thisClock} (qualified under a)-c), d) appends thisClock) | {G} |

Unchanged at head:

- the head refusal (`hdl/wire/KL_gptp_rx_parser.sv:334-335` and `:602-603`, with the engine check `refuse_a_path_trace_whose_head_is_not_the_announced_gm`);
- the #87 count-zero publication (`hdl/top/KL_gptp_engine.sv:714-731`);
- the description in `docs/INTEGRATION.md`;
- the milan-fpga REGISTER_MAP 0x7DC text (that text lives in the parent; this lane may not commit there).

Options for the decision:

- (A) Add an explicit entry-zero path output to the engine, for example an eight-slot `pub_path_o` or a head port. This needs a milan-fpga companion: `KL_gptp_shadow` ports, the `milan_datapath` GET_AS_PATH entry 0, and REGISTER_MAP 0x7DC.
- (B) Keep the ABI and serve the grandmaster at entry 0 in those cases. That is not "copied as received".
- (C) Land this head now and route the rest.

## Changes (file:line, head `2ae9a957`)

- `hdl/wire/KL_gptp_rx_parser.sv:310-319`: the PathTrace header verdict loses the `lengthField/8 != stepsRemoved+1` term. Its comment now cites the 10.5.3.3.4 NOTE and 10.3.10.2.1 a)-c).
- The `steps_r` register and `OFF_AN_SR_END_C`, which only fed that term, are removed (base `:198`, `:220`, `:363`, `:415`, `:546-547`).
- Comments updated at `:41-45` (file header) and `:560` (TLV chain).
- Kept: odd length, overrun, zero length, non-8N, duplicate TLV, head rule, and the all-hop loop verdict (c).
- `hdl/ucode/gen_gptp_ucode.py:67-69` and `:975-976`: the qualification notes no longer state N == stepsRemoved+1. Comments only; the shipping, engine and tsngen ROM images are byte-identical to the committed `.hex` files.
- `tb/verilator/parser/sim_main.cpp:656-694`: new `check_a_path_count_need_not_match_steps_removed` with four probes, each graded on event, count and loop word, every identity, and no drop:
  - one entry with stepsRemoved 3 (the issue's shape);
  - two entries with stepsRemoved 2;
  - three entries with stepsRemoved 0;
  - a short loop {GM, thisClock} with stepsRemoved 5, which must report loop bit 8 for c).
- The base's "path-count mismatch" refusal probe is removed (comment `:365-369`).
- `tb/verilator/parser/mutants.py:76-99`, `:163-168`: the mutant "the path-count refusal restored (#88)". The docstring and `tb/verilator/parser/Makefile:22-26` now say nine defects.
- `tb/verilator/engine/sim_main.cpp:2523-2571`: new phase 8o, `defer_whatever_the_path_count`, run after 8n (`:319`; header `:82-86`):
  - issue shape: priority1 247 against our 248, stepsRemoved 3, path {GM}. Elected, parent, not master, count 2, tail {thisClock}, commit coherent, no parser drop, no Announce transmitted for 1.05 s, then a degrade hands mastership back;
  - `take_and_grade_a_path` for two entries with stepsRemoved 5, and for three entries with stepsRemoved 0.
- `tb/verilator/engine/sim_main.cpp:2364-2373`: phase 8c..8m now opens with `refuse_probe` for a) own source with one entry and stepsRemoved 3, b) stepsRemoved 255 with one entry, and c) a short loop with stepsRemoved 5. Each must be refused by the microcode, with no parser drop.
- These run first so that a mutant removing that one rule moves the plane on this probe (header `:74-75`).
- `refuse_probe` (`:2288-2307`) gains `parent_canary` (default true). The own-source probe passes false: its forged source is thisClock, so no defect could move the parent check.
- The base's malformed probe "PathTrace count differs from stepsRemoved" is removed (comment `:2742-2747`).
- `tb/verilator/engine/mutants.py`:
  - `:643-670`: the mutant "the path-count refusal restored";
  - `:671-714`: four generator mutants: "(a) the own-source refusal removed", "(b) the stepsRemoved refusal removed", "(c) the PathTrace loop refusal removed" and "a parent update must beat the best" (10.3.5);
  - `:595-609`: the existing "thisClock fills every later slot" now also names the 15 #88 zero-tail checks;
  - `:817-819`: "#88 " joins the strict named-check prefixes.
- `docs/TEST_DEVELOPER.md:35`, `:98-99`, `:124-125`: suite responsibilities.
- `docs/SOURCE_EVIDENCE.md:31`, `:33`: two line anchors moved (`gen_gptp_ucode.py#L897`, `KL_gptp_rx_parser.sv#L474`).
- `tb/tsngen/run_tsngen.py:325-331`: the comment no longer claims the parser refuses a count mismatch.

## New checks, mutants, failing words

Each mutant was planted alone at head `2ae9a957` with the suite's own stage, build and run helpers. Receipts: `receipts/mutants/`. `receipts/mutants/coverage.md` maps every new check to the mutants that fail it:

- engine: 54 of 54 new checks;
- parser: 20 of 20 new checks.

| Suite | Mutant | Tally under the mutant | Named checks failing |
|---|---|---|---|
| parser | the path-count refusal restored (#88) | 355: 335 PASS, 20 FAIL (exactly the 20 new checks) | 8 of 8 |
| engine | the path-count refusal restored | 1804: 1782 PASS, 22 FAIL (all #88) | 9 of 9 |
| engine | thisClock fills every later slot (existing, names extended) | 1804: 1751 PASS, 53 FAIL | 23 of 23 |
| engine | (a) the own-source refusal removed | 1804: 1621 PASS, 183 FAIL | 4 of 4 |
| engine | (b) the stepsRemoved refusal removed | 1804: 1620 PASS, 184 FAIL | 5 of 5 |
| engine | (c) the PathTrace loop refusal removed | 1804: 1611 PASS, 193 FAIL | 5 of 5 |
| engine | a parent update must beat the best | 1804: 1553 PASS, 251 FAIL | 3 of 3 |

Failing words, for example:

- `FAIL #88 one entry, stepsRemoved 3: event got 0000000000000000 exp 0000000000000003` (parser, count restored)
- `FAIL #88 issue shape: no Announce for one interval got 0000000000000001 exp 0000000000000000` (engine, count restored: the issue's symptom)
- `FAIL #88 issue shape: elected     got 02a1b2fffec3d4e5 exp 00f1f1fffe000001` (engine, count restored)
- `FAIL #88 own source, one entry, stepsRemoved 3: parser-drop policy got 0000000000000010 exp 000000000000000f` (engine, count restored)
- `FAIL #88 issue shape: tail 2      got 02a1b2fffec3d4e5 exp 0000000000000000` (engine, fill)
- `FAIL #88 short loop, stepsRemoved 5: still master ...` (engine, (c) removed)
- `FAIL #88 issue shape: the degraded grandmaster yields ...` (engine, parent update must beat)

Not delivered, so no checks exist for:

- the head mutant;
- the "publishes the empty sequence" mutant (#87);
- the GET_AS_PATH copied-trace check for a non-GM head.

All three are blocked by the STOP.

## Base and head gate records

Every gate runs through the recorded runner (rc, seconds and log per command, never piped), in fresh clones:

- `repo-base` at `55680bff`, `repo-head` at `2ae9a957`.
- Environment: pinned Verilator 5.050 (`-j 0` mapped to `-j 8` by a scratch wrapper, nothing else changed), pinned sv2v v0.0.12, host Yosys 0.66 (CI `YOSYS_VERSION` v0.66, sha 86f2ddeb), TMPDIR in scratch, tsn-gen local checkout for tsngen.
- Separate units with MemoryMax 10G on booked CPUs (48-63 own, 64-79 from the picker).

Receipts: `receipts/base-repo/`, `receipts/head-repo/`, specs in `receipts/specs/`.

| # | Repository gate | Base `55680bff` | Head `2ae9a957` |
|---|---|---|---|
| 1 | `make contract` | rc 0 | rc 0 |
| 2 | `make -C tb/verilator/ucpu` | rc 0, 768/768 | rc 0, 768/768 |
| 3 | `make -C tb/verilator/parser` (run + mutants) | rc 0, 337/337; arm 9/9 | rc 0, 355/355; arm 10/10 |
| 4 | `make -C tb/verilator/engine` (4 passes + mutants) | rc 0, 1703 ×3 + 53; arm 73/73 (3814 s) | rc 0, 1751 ×3 + 53; arm 78/78 (4093 s) |
| 5 | `make -C tb/verilator/gaskets` | rc 0, 81/81; arm 5/5 | rc 0, 81/81; arm 5/5 |
| 6 | `make -C tb/tsngen` | rc 0, 288/288; arm 4/4 | rc 0, 288/288; arm 4/4 |
| 7 | `make -C bench/arty test` | rc 0, PASS | rc 0, PASS |
| 8 | `make lint` (engine + bench) | rc 0, no warning | rc 0, no warning |
| 9 | `make docs` (diagrams, docs, evidence + selftests) | rc 0, evidence 20 exact | rc 0, evidence 20 exact |
| 10 | `git diff --exit-code` after the run | rc 0 | rc 0 |
| + | `syn/ooc/check_ooc_clock.py --selftest` | rc 0, 30 arms | rc 0, 30 arms |

`make ooc` past its selftest needs Vivado, which this host does not have. It is not in `make all`.

Head history, nothing pushed:

- `6c9be398` failed parent gate 1, `check_cpp_idiom.py`: "multi-declarator declaration 1 > ratchet 0" (`uint16_t seq, steps;` in the new parser probe struct; `receipts/stale-6c9be398/`).
- `457ba9f5` fixed that and passed every repository and parent gate (`receipts/stale-457ba9f5/`, results only). But 33 of its new engine checks had no failing mutant.
- `2ae9a957` adds the four mutants, extends the fill mutant's names, and moves the a)-c) probes. It is the head every head record in this file cites.

## Scratch-parent consumer gate table

Scratch clones of milan-fpga dev `97aab1d0`, all submodules initialised:

- Base snapshot: `97aab1d0` itself (its gptp-processor gitlink is `55680bff`).
- Head snapshot: `db4cb6da5ec7e9bf21aa1302dfaa9de923072923`, a local scratch commit on `97aab1d0` that only sets the gptp-processor gitlink to `2ae9a957`. Never pushed.
- The list is the manager template's full 15 commands, which include milan_dp's `gptp` and `gptp-lat` legs and both idiom checks, plus the tsn_fuzz gPTP campaign as an extra row.
- Environment: as above, with tsn-gen built at the CI pin `deca300c` for tsn_fuzz.

Receipts: `receipts/base-parent/`, `receipts/base-parent-rerun/`, `receipts/base-parent-rerun2/`, `receipts/head-parent/`, `receipts/base-fuzz/`, `receipts/head-fuzz/`.

| # | Consumer gate | Base (gitlink `55680bff`) | Head (gitlink `2ae9a957`) |
|---|---|---|---|
| 1 | `scripts/check_cpp_idiom.py` | rc 0 (347 TUs, every ratchet 0 <= 0) | rc 0 (same) |
| 2 | `scripts/check_py_idiom.py` | rc 0 | rc 0 |
| 3 | `scripts/xvlog_gate.py --check` | rc 0, PASS | rc 0, PASS |
| 4 | `scripts/check_rtl_source_lists.py` | rc 0, OK | rc 0, OK |
| 5 | `sw/builder/test_builder.py` | rc 0, all gates pass except 1 NOT RUN | rc 0, same |
| 6 | `make -C tb/verilator/gptp_shadow -j8` | rc 0, 310/310 (see note 2) | rc 0, 310/310 |
| 7 | `scripts/check_port_contracts.py` | rc 0 (gptp-processor 125 ports) | rc 0 (same) |
| 8 | `scripts/measure_naming.py --check` | rc 0 | rc 0 |
| 9 | `scripts/measure_test_evidence.py --check` | rc 0 | rc 0 |
| 10 | `scripts/docs_check.py` | rc 0, 0 findings | rc 0, 0 findings |
| 11 | `scripts/lint_rtl.py --check` | rc 0 (89 <= 89) | rc 0 (89 <= 89) |
| 12 | `make -C tb/verilator/milan_dp gptp` | rc 0, 185/185 | rc 0, 185/185 |
| 13 | `make -C tb/verilator/milan_dp gptp-lat` | rc 0, 185/185 | rc 0, 185/185 |
| 14 | `make -C tb/verilator/milan_dp_gptp` | rc 0 (5277 s) | rc 0 (4829 s); tallies identical to base |
| 15 | `make -C tb/verilator/milan_dp_gm_steps` | rc 0, 6/6 | rc 0, 6/6 |
| + | `make -C tb/verilator/tsn_fuzz ptp` (extra; parent CI rtl.yml shard 1) | rc 0: 677 pass, 0 fail; artifact freshness PASS | rc 2: 671 pass, 6 fail (note 3) |

Notes:

1. Gate 5's NOT RUN arm is gate 11, which needs a local FPGA build report. It is host-dependent and the same at base and head.
2. Base gates 6-13 first ran while my concurrent base tsn_fuzz run, in the same clone, had rewritten only the timestamp of `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md`. All passed. I restored the file and reran 6-13 in a separate clean clone at `97aab1d0`:
   - gates 7-13: rc 0;
   - gptp_shadow: rc 2 once. Its `test_mutant_lifecycle.py` reported "CLEANUP FAILED: owned descendants remain" under host load average about 20, while all 310 checks and the controls passed. A second clean rerun gave rc 0 (`receipts/base-parent-rerun2/`).
   - Gate 14 started with the same timestamp-only change; that suite does not read the file.
   - From then on, every head-tree run and every fuzz run used its own clone.
3. tsn_fuzz pins the retired rule in two fixtures (`tb/verilator/tsn_fuzz/fuzz_ptp_timing.py:154-159` at `97aab1d0`, with their comment at `:146-150`):
   - "one path-trace hop against stepsRemoved 1": the plane now defers, failing rejected, flags, GM, parent and drop;
   - "stepsRemoved 255 on a one-hop path trace": now refused by b) in microcode, not as a parser drop, failing drop counted.
   - Measured companion (scratch only, `receipts/companion-measure/`): remove the first fixture and expect the b) refusal with no parser drop in the second (1+/5-). The campaign then passes 672/672. The only remaining failure is the chained freshness check, because `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md` (677) must be regenerated.
   - The companion would also correct the rule's description in `tb/verilator/tsn_fuzz/README.md:72-90` and the comment at `tb/verilator/milan_dp/sim_gptp.cpp:596-598`.

## Open items / notes

- STOP decision needed (A/B/C above). #87 and #88 stay open; this head closes neither.
- Parent companion for whichever lands this head: the tsn_fuzz fixtures, a regenerated `TEST_RESULTS.md`, and the two descriptions in note 3.
- No push, no PR, no parent commit outside scratch. No top-level port, parameter or register-map change. No ROM-image change (the generated images are byte-identical).
- Cited edition: IEEE 802.1AS-2011 with Cor1-2013 and Cor2-2015 (10.3.10.2.1, 10.5.3.3.4, 10.3.12.1.1, 10.3.12.1.4 i)), and IEEE 1722.1-2021 7.4.41.2.
