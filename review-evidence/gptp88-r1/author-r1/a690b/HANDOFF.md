# [A690b] HANDOFF — FPGA-gPTP #87 + #88 (explicit AS path from entry 0)

Status: REVIEW READY at head `c1bc9e21`. Every repository gate is rc 0 at base and head. The parent consumer list is 15/15 rc 0 with the companion applied, and tsn_fuzz `ptp` is rc 0.

- Repository: Mister-M-alt/FPGA-gPTP, branch `87-88-announce-pathtrace` (local, not pushed)
- Base: main `55680bff3b287b9a7b0c759f51471fa617c17335`
- Head: `c1bc9e21a273fd8506b4806a2470fb7bab13f72f`, four commits on [A690]'s `2ae9a957`:
  - `6f7b79c8` Publish pathTrace from its received head and keep it without a path trace TLV (#87, #88)
  - `97dcac4a` Grade the parser-drop canary only on the PathTrace shapes the parser once refused (#88)
  - `f88221c3` Keep the engine mutation arm under the module length limit and reuse the parser arm's PathTrace edits (#88)
  - `c1bc9e21` Discard the Announce grandmasterIdentity bank word in the tsngen mutant now that the parser keeps no copy (#88)
- The PR is five commits on main `55680bff`: [A690]'s `2ae9a957` (the count refusal) plus the four above.
- Ruling followed: [A10] option (A), #88 issuecomment-6442193793.
- TAKEN: #88 issuecomment-6442223950.
- REVIEW READY (head `c1bc9e21`): #88 issuecomment-6448634489.

## Outcome

- #88: an Announce is disqualified only by 802.1AS-2011 10.3.10.2.1 a)-c).
  - [A690]'s head already removed the count refusal.
  - This head removes the head refusal and accepts a zero-length path trace TLV.
- d): a present TLV's pathSequence is copied as received, its head included, and thisClock is appended. An empty one gives {thisClock}.
- #87: without a TLV nothing is written, so the previous pathTrace stays:
  - {thisClock} after reset or mastership (10.3.12.1.1, 10.3.12.1.4 i), Cor1);
  - otherwise the last path copied from a TLV, also across a grandmaster change.
- ABI, the authorised top-level change: `pub_path_o` is eight entries from entry 0 (`[8*64-1:0]`, entry k at `64*k`). `pub_path_count_o` counts the published entries, 1..8 (0 only while the raw GM is zero, as before).
- No other port, parameter or register-map change. Generated ROM images are byte-identical to the committed `.hex` files (shipping, seeded, p1 255).

## Changes (file:line at head `c1bc9e21`)

RTL:

- `hdl/wire/KL_gptp_rx_parser.sv`
  - `:39-47` header: 10.3.10.2.1 a)-c) only; empty TLV, any count, any head qualify; word 12 reports presence apart from the count.
  - `:91-93` bank map: w12 `{pathTracePresent, 54'd0, pathContainsThisClock, pathTraceCount}`. Bit 63 sits above bits 39:8, the window the microcode's loop test compares (`SHR 8`, 32-bit `CMP`), so the unchanged microcode is unaffected.
  - `:318-322` PathTrace header verdict keeps only 8N framing and singularity. The `lengthField == 0` term is gone.
  - `:569-571` a zero-length PathTrace header still marks `pt_seen_r` (presence, and the duplicate rule).
  - `:398` the deferred w12 write carries `pt_seen_r` at bit 63.
  - Head refusal removed: `gm_r`, `ann_head_bad_w`, the bad_r arm (base `:602-603`) and its `fin_ok_r` term (`:629`).
- `hdl/top/KL_gptp_engine.sv`
  - `:120-127` ports: `pub_path_count_o` and the eight-entry `pub_path_o`, documented.
  - `:29-33` region-3 map: word 7 reads entry 0 (`:799`); a write to 7 stages.
  - `:233`, `:319-324` Announce-context capture: presence (w12 bit 63) and all eight received entries w16..w23.
  - `:721-737` staging rule (10.3.10.2.1 d)), `path_append_w` for every present TLV, `self_path_w` = {thisClock}.
  - `:845` reset and `:977` address 6 (self wins) load {thisClock} at entry 0.
  - `:990-1003` address 7: with a TLV copy from entry 0, append thisClock, clear the rest; without one change nothing.
  - `:885` simulation assertion reworded (count zero beside a nonzero entry).
- `hdl/ucode/gen_gptp_ucode.py`: comments and docstrings only (`:63-79`, `:976-981`, `:1633-1637`, `:1776-1777`). No emitted word changes; the images are byte-identical.

Tests:

- `tb/verilator/parser/sim_main.cpp`
  - `:31` `PT_PRESENT`; every present-TLV w12 expectation carries it, and the TLV-less ones stay 0 (`:383`, renamed "absent").
  - `:712` new `check_a_path_head_and_an_empty_path_qualify`: two heads other than the grandmaster and a thisClock head (loop bit still set); an empty TLV alone and between unknown TLVs (present, count 0); a PathTrace after an empty one is refused as a duplicate.
- `tb/verilator/parser/mutants.py:203-249`: six new mutants. Makefile and README say fifteen.
  - the path-head refusal restored (#88);
  - the head is replaced by grandmasterIdentity (#88);
  - the empty-path refusal restored (#88);
  - an empty path is not marked present (#87);
  - word 12 drops the presence bit (#87);
  - word 12 marks a TLV-less Announce present (#87).
- `tb/verilator/engine/sim_main.cpp`
  - `:1117-1149` eight-entry accessor (`pub_path_entry`, head, tail) and full-path commit grading.
  - 8n `:2515`: "#88 empty path" publishes {thisClock}. "#85 absent path" keeps the {thisClock} mastership left.
  - 8o `:2548-2626`: the issue's two shapes from priority1 247, each defers (elected, not master, coherent commit, no Announce for 1.05 s):
    - stepsRemoved 3 with one entry;
    - a path headed elsewhere, checking "entry 0 is the received head".
  - 8p `:2628-2703`, new:
    - G1 elected; a better G2 without a TLV keeps G1's path, G1 at entry 0;
    - G2's empty TLV gives {thisClock};
    - G2's path headed elsewhere puts that head at entry 0;
    - G2's TLV-less refresh keeps it;
    - G2 degrades to {thisClock}.
  - `:3040` the current parent's path headed elsewhere is published from that head (was a refusal probe).
  - TLV-less refreshes keep the previous path (unknown-only, TLV-less, out-of-message, `:2956`), and the overload owner keeps C's path (`:3173`). Its chasers now carry paths other than C's.
  - After a warm reset a TLV-less grandmaster keeps {thisClock} (`:4448`).
  - Phases 35/36/38 grade full paths from entry 0 (`:5469`).
- `tb/verilator/engine/mutants.py`
  - multi-edit mutants (`:783`); the parser arm's three refusals reused by name (`:97-104`); `tails()` (`:112`);
  - new: an empty path takes no thisClock; the path-head refusal restored; the empty-path refusal restored; the received head replaced by the grandmaster; the received head is not published; the empty sequence published without a TLV (#87); a TLV-less Announce publishes {thisClock} (#87); the self path leaves entry 0 empty;
  - the patterns of the existing path mutants moved with the RTL; "thisClock is appended to an absent path" is retired (that behaviour is now the rule).
- `tb/tsngen/run_tsngen.py:328-332`: the comment no longer claims the parser needs the GM head.
- `tb/tsngen/mutants.py:61-66`: "announce grandmasterIdentity discarded" zeroes the word-9 bank write BTCA reads. At base it zeroed the parser's private `gm_r` copy, which only the retired head refusal used. Arm 4/4.

Docs:

- `docs/INTEGRATION.md:456-506`: the publication table and "Path of an elected peer" describe the new ABI.
- `docs/HDL_DEVELOPER.md:206-220`: word 7, presence bit 63.
- `docs/TEST_DEVELOPER.md:99-101`, `:125-128`.
- `docs/SOURCE_EVIDENCE.md`: line anchors recomputed (20 exact).

## New checks, mutants, failing words

How "new" is measured, not hand-listed:

- Each harness was built once more with `expect()` also printing its check name, at base `55680bff` and at head. `receipts/enum/` holds every executed name; `receipts/scripts/enum_checks.sh` builds them.
- A name is new when it runs more often at head than at base.
- Every mutant of each suite's own arm was planted alone, through that arm's own stage/build/run code (`receipts/scripts/some_mutants.py`), and every FAIL line kept (`receipts/mutants/*-sweep*/`).
- `receipts/scripts/coverage.py` maps each new name to the mutants whose run fails it (`receipts/mutants/{parser,engine}-coverage.md`).

Results:

| Suite | Base checks | Head checks | New names | Failed by a planted mutant | Arm |
|---|---:|---:|---:|---:|---|
| parser | 337 | 378 | 45 | 45 of 45 | 16/16: control + 15 mutants, 6 new |
| engine | 1703 + 53 (p1 255) | 1875 + 54 | 217 | 217 of 217 | control + 84 mutants, 8 new; 1 retired |

- Engine map: from the full sweep at `f88221c3` (`receipts/mutants/engine-sweep-f88221c3/`), 84 of 84 caught on every named check. Every engine-suite file (RTL, generator, harness, arm) is identical at `c1bc9e21`.
- History:
  - The first sweep, at `6f7b79c8` (`receipts/mutants/engine-sweep-6f7b79c8/`), had 83 of 84 on every named check. The miss, "#88 empty path: count" under "the empty-path refusal restored", cannot fail: a refused empty TLV leaves the same {thisClock}.
  - That sweep also left three "parser accepts" canaries no mutant could fail.
  - `97dcac4a` dropped that name from the mutant's list and runs the canary only on the two #88 shapes.
- The parser map comes from its full sweep (`receipts/mutants/parser-sweep/`). The parser RTL, harness and arm are unchanged since.

New mutants and failing words (examples, head values `got`, expected `exp`):

- parser, "the path-head refusal restored (#88)" (11 FAIL of 378): `FAIL #88 head not the grandmaster, two entries: event got 0000000000000000 exp 0000000000000003`
- parser, "the head is replaced by grandmasterIdentity (#88)" (3 FAIL): `FAIL #88 head not the grandmaster, two entries: identity 0 got 001122fffe334455 exp 00bad0fffe000001`
- parser, "the empty-path refusal restored (#88)" (6 FAIL): `FAIL #88 empty path: event got 0000000000000000 exp 0000000000000003`
- parser, "an empty path is not marked present (#87)" (5 FAIL), "word 12 drops the presence bit (#87)" (15 FAIL), "word 12 marks a TLV-less Announce present (#87)" (7 FAIL): `FAIL TLV-less ann: absent, zero count and loop got 8000000000000000 exp 0000000000000000`
- engine, "the path-head refusal restored" (28 FAIL of 1929): `FAIL #88 head not the grandmaster: no Announce for one interval got 0000000000000001 exp 0000000000000000` (the issue's symptom)
- engine, "the received head replaced by the grandmaster" (7 FAIL): `FAIL #88 head not the grandmaster: entry 0 is the received head got 00f5f5fffe000001 exp 00f5f5fffe0000a1` (the explicit entry-0 check)
- engine, "the received head is not published" (45 FAIL): `FAIL #88 issue shape: entry 0 is the received head got 0000000000000000 exp 00f1f1fffe000001`
- engine, "the empty sequence published without a TLV" (#87, the 2020 rule; 45 FAIL): `FAIL #87 G1 to G2 without a TLV: count got 0000000000000000 exp 0000000000000004`, `FAIL #85 absent path: count got 0000000000000000 exp 0000000000000001`
- engine, "a TLV-less Announce publishes {thisClock}" (#87; 35 FAIL): `FAIL #87 G1 to G2 without a TLV: head got 02a1b2fffec3d4e5 exp 00f6f6fffe000001`
- engine, "an empty path takes no thisClock" (7 FAIL): `FAIL #88 empty path: count got 0000000000000000 exp 0000000000000001`
- engine, "the self path leaves entry 0 empty" (23 FAIL): `FAIL self path entry 0 is thisClock got 0000000000000000 exp 02a1b2fffec3d4e5`
- engine, "the empty-path refusal restored" (9 FAIL) and "the path-count refusal restored" (34 FAIL) are the parser arm's own edits planted in the engine build.

## Base and head gate records

Every gate ran through the recorded runner, one command at a time, each with its own exit code, seconds and log, never piped. Each tree was a fresh clone.

- Environment:
  - Verilator 5.050 (pinned), with `-j 0` mapped to `-j 8` by a scratch wrapper and nothing else changed;
  - sv2v v0.0.12 (pinned);
  - Yosys 0.66 (the CI pin);
  - TMPDIR in scratch;
  - separate units, MemoryMax 10G, on this lane's booked CPUs.
- Base: [A690]'s records at `55680bff` in the same environment and from the same command list, reused as instructed (`receipts/base-a690/`).
- Head: `c1bc9e21` (`receipts/head-repo/`, spec `receipts/specs/head-repo.json`).

| # | Repository gate | Base `55680bff` | Head `c1bc9e21` |
|---|---|---|---|
| 1 | `make contract` | rc 0 | rc 0 |
| 2 | `make -C tb/verilator/ucpu` | rc 0, 768/768 | rc 0, 768/768 |
| 3 | `make -C tb/verilator/parser` (run + mutants) | rc 0, 337/337; arm 9/9 | rc 0, 378/378; arm 16/16 |
| 4 | `make -C tb/verilator/engine` (4 passes + mutants) | rc 0, 1703 ×3 + 53; arm 73/73 (3814 s) | rc 0, 1875 ×3 + 54; arm 85/85 (4321 s) |
| 5 | `make -C tb/verilator/gaskets` | rc 0, 81/81; arm 5/5 | rc 0, 81/81; arm 5/5 |
| 6 | `make -C tb/tsngen` | rc 0, 288/288; arm 4/4 | rc 0, 288/288; arm 4/4 |
| 7 | `make -C bench/arty test` | rc 0, PASS | rc 0, PASS |
| 8 | `make lint` (engine + bench) | rc 0 | rc 0 |
| 9 | `make docs` (diagrams, docs, evidence + selftests) | rc 0, evidence 20 exact | rc 0, evidence 20 exact |
| 10 | `git diff --exit-code` after the run | rc 0 | rc 0 |
| + | `syn/ooc/check_ooc_clock.py --selftest` | PASS, 30 arms | PASS, 30 arms |

Parser arm and engine arm counts include their unmutated control. `make ooc` past its selftest needs a synthesis tool this host does not have; it is not in `make all`.

## milan-fpga companion (patch, not committed)

`milan-fpga-companion.patch` (beside this file) is `git diff 97aab1d0 0ea1074f`, without the gitlink.

- `0ea1074f0d8745e73cb27abd03072a99545af9a8` is a local scratch commit on dev `97aab1d0`. It applies the patch and sets the gptp-processor gitlink to `c1bc9e21`. Never pushed.
- The adoption sets the pin itself. The patch reverses cleanly on that snapshot (`git apply --check -R`) and is byte-identical to the raw diff.
- `1c05c78d` was the same snapshot pinning `f88221c3`. The two differ only in the gitlink, and the gptp-processor trees differ only in `tb/tsngen/mutants.py`, which no parent suite reads. The companion mutants below ran on `1c05c78d`.

What it changes:

- `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv`
  - `pub_path_o` is eight entries and `pub_path_count_o` counts them.
  - The canonicaliser copies entries 0..count-1.
  - The path generation compares count and entries only, so entry 0 counts and the GM scalar does not.
- `hdl/milan/milan_datapath.sv`
  - `gptp_pub_path_w` is eight entries.
  - The CSR AS_PATH face keeps its seven-entry width and takes entries 1..7.
  - GET_AS_PATH entry 0 (`asp_resp_head_r`) and the Table 5.22 AS_PATH comparator take entry 0 from the engine (`asp_owner_head_w`, same owner selection). Previously it was `cfg_adp_gptp_gm`.
- `hdl/common/csr/milan_csr.sv`: four port comments only.
  - No width, logic or register change.
  - The frozen lockstep reference `tb/verilator/csr/milan_csr_ref.sv` is untouched.
- `docs/reference/REGISTER_MAP.md` (0x7DC section and the AS_PATH trigger paragraph) and `README.md` (GET_AS_PATH):
  - the 2011 rules;
  - the cross-edition #87 text is removed.
- `tb/verilator/tsn_fuzz`
  - `fuzz_ptp_timing.py`: `_btca_adopt`. The head and count fixtures are adoptions with no parser drop; stepsRemoved 255 on a one-hop path is the (b) refusal with no parser drop. Stale comments are corrected.
  - `wire.py`: docstring.
  - `README.md`: the two descriptions from [A690]'s note 3.
  - `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md` regenerated: 675 checks, all pass. The BTCA section goes from 82 to 80.
- `tb/verilator/gptp_shadow`
  - The wrapper exposes `pub_path_head_o`; tail k is entry k+1.
  - The harness: TLV-less keeps the path (generation silent, also across a GM change); an empty TLV gives {thisClock}; a path headed elsewhere is published from that head. 320 checks, base 310.
- `tb/verilator/milan_dp/sim_gptp.cpp`
  - The Announce comment ([A690]'s note 3).
  - A TLV-less refresh keeps path B: count, generation, no push, unchanged response, no drop.
  - A TLV-less GM switch keeps path B, GMID still at entry 0.
  - The in-flight cut now replaces `[GM]` with an empty TLV: the new response is {thisClock}.
  - A closing probe: GET_AS_PATH entry 0 is the received head (`PATH_B3`), not the grandmaster.
  - 192 checks, base 185, in both the `gptp` and `gptp-lat` legs.

Companion mutants:

- Planted one at a time in a scratch clone of snapshot `1c05c78d`; gptp_shadow, milan_dp `gptp` and tsn_fuzz `ptp` run under each.
- Receipts: `receipts/companion/mutants/`; script `receipts/scripts/companion_mutants.py`.
- 64 of 64 new parent check names fail under at least one (`receipts/companion/coverage.md`). Two more are renames with unchanged assertions.

| Mutant | gptp_shadow FAIL | milan_dp gptp FAIL | tsn_fuzz ptp FAIL |
|---|---:|---:|---:|
| the path-head refusal restored (engine) | 5 | 7 | 4 |
| the path-count refusal restored (engine) | 8 | 7 | 5 |
| the empty-path refusal restored (engine) | 5 | 7 | 0 |
| the empty sequence published without a TLV (engine, #87) | 14 | 10 | 0 |
| the received head replaced by the grandmaster (engine) | 1 | 1 | 0 |
| (b) the stepsRemoved refusal removed (engine) | 0 | 0 | 12 |
| a TLV-less Announce is dropped at the event queue (engine) | 1 | 15 | 0 |
| a TLV-less Announce is refused by the parser (engine) | 6 | 22 | 2 |
| GET_AS_PATH entry 0 served from the grandmaster (old datapath) | 0 | 4 | 0 |
| the shadow drops entry 0 (old canonicaliser) | 6 | 6 | 0 |
| the shadow publishes entry 0 as the grandmaster | 2 | 9 | 1 |

A suite with 0 FAILs under a mutant exited rc 0; every other cell's suite exited rc 2.

Examples:

- `FAIL #88 GET_AS_PATH entry 0 is the received head got 00aaccfffe010204 exp 001122fffe000044` (old datapath)
- `FAIL #87 TLV-less GM switch: GET_AS_PATH entry 0 is still GMID got 0000000000000000 exp 00aaccfffe010203` (2020 empty sequence)
- `[FAIL] better vector, path-trace head is not the announced grandmaster (10.3.10.2.1): adopted got=189629471886922981 exp=13107` (head refusal restored)

## Scratch-parent consumer gate table

Scratch clones of milan-fpga dev `97aab1d0`, all submodules initialised, never pushed.

- Base: `97aab1d0` itself (gitlink `55680bff`). [A690]'s records, reused (`receipts/base-a690/base-parent*`, `base-fuzz`).
- Head: `0ea1074f0d8745e73cb27abd03072a99545af9a8`, the companion applied plus the gitlink at `c1bc9e21` (`receipts/head-parent/`, `receipts/head-fuzz/`, specs in `receipts/specs/`).
- The list is the manager template's full 15 commands. It includes both idiom checks and milan_dp's `gptp` and `gptp-lat` legs.
- tsn_fuzz `ptp` (parent CI rtl.yml shard 1) runs in its own clone, because it rewrites its `TEST_RESULTS.md` timestamp.

| # | Consumer gate | Base (gitlink `55680bff`) | Head (`0ea1074f`, gitlink `c1bc9e21`) |
|---|---|---|---|
| 1 | `scripts/check_cpp_idiom.py` | rc 0 | rc 0 (every ratchet held) |
| 2 | `scripts/check_py_idiom.py` | rc 0 | rc 0 (over-long line 0 <= 0) |
| 3 | `scripts/xvlog_gate.py --check` | rc 0, PASS | rc 0, PASS (0 findings) |
| 4 | `scripts/check_rtl_source_lists.py` | rc 0, OK | rc 0, OK |
| 5 | `sw/builder/test_builder.py` | rc 0, all pass except 1 NOT RUN | rc 0, same (the same host-dependent arm) |
| 6 | `make -C tb/verilator/gptp_shadow -j8` | rc 0, 310/310 (rerun, see [A690] note 2) | rc 0, 320/320; lifecycle PASS |
| 7 | `scripts/check_port_contracts.py` | rc 0 (gptp-processor 125 ports) | rc 0 (gptp-processor 125 ports) |
| 8 | `scripts/measure_naming.py --check` | rc 0 | rc 0 |
| 9 | `scripts/measure_test_evidence.py --check` | rc 0 | rc 0 |
| 10 | `scripts/docs_check.py` | rc 0, 0 findings | rc 0, 0 findings |
| 11 | `scripts/lint_rtl.py --check` | rc 0 (89 <= 89) | rc 0 (89 <= 89) |
| 12 | `make -C tb/verilator/milan_dp gptp` | rc 0, 185/185 | rc 0, 192/192 |
| 13 | `make -C tb/verilator/milan_dp gptp-lat` | rc 0, 185/185 | rc 0, 192/192 |
| 14 | `make -C tb/verilator/milan_dp_gptp` | rc 0, RESULT PASS (5277 s) | rc 0, RESULT PASS (4967 s); verdict lines identical to base |
| 15 | `make -C tb/verilator/milan_dp_gm_steps` | rc 0, 6/6 | rc 0, 6/6 |
| + | `make -C tb/verilator/tsn_fuzz ptp` (own clone) | rc 0: 677 pass, freshness PASS | rc 0: 675 pass, 0 fail; freshness PASS |
| + | `make -C tb/verilator/csr` (extra; `milan_csr.sv` comments) | not run | rc 0 on `1c05c78d` (every leg, lockstep and its controls) |
| + | `make -C tb/verilator/gptp_txts` (extra; shadow width) | not run | rc 0 on `1c05c78d`, RESULT PASS |

- At head the tsn_fuzz count is 675 by design: the BTCA section's two retired-rule rejections (5 checks each) became adoptions (4 checks each).
- Without the companion, [A690]'s head failed tsn_fuzz with 6 of 677.
- The two extras ran on snapshot `1c05c78d` (`receipts/head-parent-extra/`). It differs from `0ea1074f` only in the gitlink, whose trees differ only in `tb/tsngen/mutants.py`, which neither suite reads.

## Open items / notes

- No push, no PR, no parent commit outside scratch. The companion lands with the gPTP pin adoption.
  - #89/#90/#91 ([A688]) change the generator. This lane changes it only in comments, so the two merge in either order.
  - If both companions touch tsn_fuzz, regenerate `TEST_RESULTS.md` once after both.
- Timing of d) (unchanged here, pre-existing since #85). 802.1AS-2011 10.3.10.2.1 d) copies the TLV "if ... the portRole of the port is SlavePort".
  - The engine stages the path at the BTCA `take` that elects the sender.
  - So a new grandmaster's path is published with the Announce that elects it, one Announce interval before a literal reading, in which the role becomes SlavePort only after that Announce.
  - From the next Announce both readings agree.
- Resource: the engine adds one 64-bit captured entry (w16), one 64-bit published entry and a presence flop (about 129 flops plus muxing). Not measured: this host has no synthesis tool for `make ooc` beyond its selftest (PASS, 30 arms, at base and head).
- `milan_csr.sv` changes four port comments only. The parent csr suite, its lockstep against the frozen reference and its mutation controls, and the gptp_txts suite all pass at the head snapshot (extra rows below).
- Some pre-existing engine check names still say "raw-empty"; renaming them would only churn the coverage map. Their expectations follow #87.
- Dated parent records (`docs/testing/MILAN_V12_AUDIT_2026-08-16.md`, `CHANGELOG.md`) still describe the old count-zero behaviour as history; they are not touched.
- Superseded runs, kept under `receipts/stale-f88221c3/`:
  - `97dcac4a`: repository gates stopped at gate 4 when `f88221c3` replaced it.
  - `f88221c3`: repository gates 9 of 10 rc 0. Gate 6 (tsngen) was rc 2: its arm's "announce grandmasterIdentity discarded" pattern named the removed `gm_r`; fixed in `c1bc9e21`.
  - The parent list pinned at `f88221c3` (snapshot `1c05c78d`) ran gates 1-13, all rc 0, before it was stopped for the new pin; its tsn_fuzz was rc 0.
