# HANDOFF - lane P2, round 4 (executor [A511])

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #145, branch `p2-nvm-port-robustness`.
- Start head: `527662d659b4ead97675744d12a43af1ea92b9b3` (pushed). Commits were added; nothing was amended.
- Assignment: #15 comment 5963997438. It answers R436-3 (PR comment 5963891560) and R437-3 (5963994045). Both are NEGATIVE on the same MINOR, F1: round 3's drain bound was pinned in one branch only.
- TAKEN: #15 comment 5964000710 (2026-10-03 01:15Z). REVIEW READY: #15 comment 5964850117 (about 02:57Z), head `3957814`.
- Scratch, outside the tree: `$VALIDATION_STORAGE/ppP2-a511`.
  - Helpers: `wt.sh`, `plants.py`, `cmp_plants.py`, `fastfig.py`, `claims.py`, `models.py`, `figures.sh`, `mkparentx.sh`, `status.sh`.
  - Logs: `logs/`, `gates/`, `pgates2/` (the parent at the final head), `rev/` (the reviewers' scripts, re-run), `ooc/`.
  - `pgates/` holds an interim parent run at `a691e0e`, stopped at gate 10 when the head moved.

## Status

Final head: `3957814550f164d72bfaad5d28cd0e7cac0ecaaf`. Local, not pushed: push is outside this lane. Three commits over `527662d`:

| Commit | Item |
|---|---|
| `f879a26` | 1: T28g-k; the randomized harness abandoning at any byte, with long records and the largest legal one, FZ10; D28 split; every round-3 review plant a figures row |
| `a691e0e` | 2: R437-1's residue R2-R4 in the reviewer's exact text |
| `3957814` | 1: FZ10's message names no other check id |

The third commit exists for one reason. R436-3's R436g and R436h, run unchanged, grep `FZ9` and `FZ[78]`. They delete the other modes, so FZ10, whose reach needs every mode, fails inside them, and its old message contained "FZ9" and "FZ7", so it showed up in their output as a head failure. With the new wording their output carries only their own checks.

Item 3: `origin/main` was still `c74711d4` at every fetch, contained in the head. No merge was needed.

## Per finding

### R436-3 F1 = R437-3 F1 (MINOR): the drain bound pinned in one branch only

The RTL was right (both reviews), and none of it changed: `KL_pp_nvm_port.sv` is blob `a62788bb`, the same at `527662d` and at the head.

**The changes, each serving the banner (`KL_pp_nvm_port.sv:85-93`: "drains the bytes an owed READ still owes and no more") and 02 §8 (`02_interfaces.md:542-548`: "its length less those that moved before the deadline").**

- `tb/nvm_port/sim_main.cpp:2446-2611`: the new phases. Each arm starts from its own reset with region 2 committed again.
  - Helpers: `babble_past_the_length` (the device presents bytes past the length, one every `TMO` / 2), `drains_exactly` and `ended_then_served`.
  - **T28g** (`an_abandoned_read_owes_what_did_not_move`): a header READ abandoned in `S_RHCOLL` after 3 and after 7 bytes is drained of exactly 5 and 1. The restore waiting on it ends DEADLINE `TMO` + 2 after the last byte, with no command. The device's done then ends the READ and the next restore is served. This is the `left_w` `S_RHCOLL` branch, `:293`.
  - **T28h** (same function): a READ abandoned in `S_RHWAIT` and in `S_RPWAIT`, every byte moved: none drained. This is the wait-state branch: `dev_len_o` is 0 there, `:295`.
  - **T28i** (`a_late_grant_owes_its_whole_length`): a header READ and a payload READ granted on the edge the deadline withdrew them are drained of their whole length, 8 and 40. This is the request branch, `dev_len_o` in a request state, `:295`.
  - **T28k** (same function): an owed WRITE granted late, whose broken device presents read bytes: none taken. This is `drain_w`'s `owed_rd_r` term, `:296`.
  - **T28j** (`a_long_owed_read_is_drained_whole`): the count's width, `:222`.
    - A 600-byte payload READ abandoned before its 11th byte, owing 590.
    - One of the largest legal length, 1,024, abandoned before its first byte.
    - The same one granted late.
    - Each is ended by the device at a legal pace while a restore waits, and that restore is served byte-exact, with `dev_rd` equal to what was owed plus the record.
    - The device presents a byte every `TMO` / 2 until the restore is issued. Without that, at 4096 the late-granted READ ended inside the post-pulse window, and the gate's coincident/4096 row failed T28j twice; it was fixed before the commit.
  - The suite is 393 checks per build (was 356).
- `tb/nvm_port/fuzz_main.cpp`: the standing randomized harness.
  - FZ9 (babble) abandons at a payload byte, or, half the time, at a header byte, the header's terminal, the payload's last byte or its terminal (`one_babble`).
  - FZ7 (resume) and FZ9 draw half their records long, up to 1,024 bytes (`long_payload`).
  - Once per seed, `one_widest` stores a READ of the largest payload the port accepts, abandons it before its first payload byte (owing all of it), and requires the restore behind it to be served.
  - `largest_legal_length` asks the port for that value: a binary search over stored headers the port takes or refuses UNFRAMED.
  - FZ10 requires the reach: abandons at header bytes, payload bytes and terminals; served requests behind READs owing 256 bytes or more; and the largest, in every seed.
  - 10 checks per build (was 9). The R436g and R436h anchors were kept on purpose: the `sil_n` payload line, the four mode loops and the two `size_t(rnd(0, 24))` draws in `one_resume`.
- `tb/nvm_port/Makefile`: the harness is built at `FUZZ_MAXP` = 65,527, the parameter's largest legal value; the suite stays at `MAXP` = 1,024.
- `tb/nvm_port/deadline_rows.py`:
  - D28 is split into D28a (`S_RHCOLL`) and D28b (`S_RPPUMP`).
  - `DRAIN_PLANTS` holds all 26 plants of both packets in the reviewers' own text. `cmp_plants.py` compares them byte for byte against `plants_drain.py` and `spec_drain.py`: 26 identical.
  - Z1, Z3, Z8 and Z10b are also rows on the harness at bound 3.
  - The gate is 160 builds (was 129).
- `tb/nvm_port/measure_figures.py`: the waiver's quoted suite size and the docstring's row count; still 989 lines.
- Docs: the `tb/nvm_port` README (every count, T28g-k, D28a/b, the plant table, the harness section) and 09 §8.6 (`09_verification.md:323-342`).

**The checks that fail without it.** Gate rows, the suite at 100:

| Plant | Fails | Named by |
|---|---|---|
| Z1, B6b (whole 8) | 2 | T28g |
| Z8, B6 (one over) | 2 | T28g |
| Z3, B8 (wait states owe 8) | 2 | T28h |
| B7 (late grant one over) | 2 | T28i |
| Z10b, B10 (8-bit count); Z10, which round 3 failed at the width lint alone | 3 | T28j |
| B12 (drain for any owed command) | 1 | T28k |
| D28a / D28b | 2 / 1 | T28g / T28f |
| Z1, Z3, Z8 on the harness at 3 | 1 each | FZ9 |
| Z10b on the harness at 3 | 3 | FZ7, FZ9, FZ10 |

The other 15 plants (Z2, Z4-Z7, Z9, Z11, Z12, B1-B5, B9, B13) fail 1 to 27 named checks each (README table). Under `make run`, Z10 and B10 stop first at `elab_bounds.sh`'s width lint.

### R436-3 R1 (RESIDUE): the PR body's Round 3 parent-visible item 3

Replaced with the reviewer's exact sentence (PR-BODY.md, Round 3 parent-visible list, item 3).

### R437-1 R2-R5 (RESIDUE, carried by R437-3)

- **R2:** `tb/nvm_port/README.md:1135-1136` and `:1141-1142`, both phrases in the reviewer's text.
- **R3:** `tb/nvm_port/sim_main.cpp:1164-1165` and `:1249-1250`.
- **R4:** `hdl/acmp/KL_acmp_nvm_shadow.sv:208` and `hdl/aecp/KL_aecp_nvm_writer.sv:260`. These are comments only. Both managers branch on `!= UNFRAMED` (`:585`, `:479`), so "3 DEADLINE (read as DEVICE)" is true. No plant, campaign patch or gate anchors on either line.
- **R5:** `parent-adoption-p2-cdf49d1a.patch`, one hunk more: line 1930 now cites "section 15 item 4 (amended)".
  - New sha256 `590f791de7fc5d00986a8d76c43e4488d522305b19876b8b4f30bc0a76f539fa`, 11,888 bytes.
  - It was `3dda850924ffe4150aa33703ac82c0784035e3387070b7c9b5fc537a7467d08b`, 9,728 bytes; that copy is in the round-3 packet.
  - It applies after c4c6 and then C8's patch (`git apply --check` on a fresh archive of `cdf49d1a`).

## Per item

1. **Device models.** No MODELS row was added. The harness gained:
   - armings for babbling in every branch (`babble_past_the_length`, which also puts a wait state's device back in its data phase);
   - a WRITE's device presenting read bytes (T28k);
   - the late-grant stage at `TMO` / 2.

   The randomized harness gained long records, abandons at every byte or terminal, the widest READ, and port-asked `MAX_PAYLOAD_P`.
   - **Mutations:** the 26 plants above plus D28a/b and four harness rows. Every plant fails a named check; none is equivalent. B12, which R437-3 measured equivalent against every legal device, fails T28k's broken device.
   - **No contract-legal device is refused:**
     - the seven legal models are 393/0 at 20, 21, 37, 100, 1,000 and 4,096 (`md1/`);
     - short read is 297/96 and silent 122/271 at each, every RW check passing;
     - the harness is 10/10 at 1, 2, 3 and 37.
   - **No RTL change.**
2. **No logic change.** R4's two port comments are the only `hdl` edits.
3. **No merge.**

## Parent-visible list

1. No port, parameter or logic change. `KL_pp_shadow` needs nothing. The port-contract gate counts 1,757 processor ports, 111 undocumented, unchanged.
2. `parent-adoption-p2-cdf49d1a.patch` changed (R5), docs only, as above. A parent adopting this head applies c4c6, then C8's `parent-adoption-c8-cdf49d1a.patch` (sha256 `aa5a88eb…`), then p2.
3. Processor documents the parent reads: 09 §8.6's rows now name T28g-k, D28a/b and the plants. 02 §8 and the banner are unchanged.

## Gates (pinned Verilator 5.050)

Every gate ran at the final head `3957814` unless noted. Processor gates ran on `git archive` exports under `gates/`; the figures gate ran in the lane tree, because it reads git history.

| Gate | rc | Result |
|---|---|---|
| `scripts/run_suites.sh` | 0 | 33 suites, 1,020,238 checks, 0 failing (round 3: 1,020,123; plus 37 × 3 + 1 × 4); `nvm_port` 1,219 = 393 × 3 + 10 × 4; `acmp_nvm` 388 |
| `make -C tb/nvm_port run` (separately) | 0 | elab guard OK; 393 × 3; the harness 10 × 4; 1,219 |
| `make -C tb/nvm_port figures` | 0 | 160 builds; 154 rows `[ok ]`; "all measured figures agree"; 946 s |
| `scripts/lint_hdl.sh` | 0 | 41 modules LINT OK |
| `syn/yosys/run.sh` | 0 | 36 tops and the Xilinx memory-map check |
| docs (CI docs job, `make check`, `gen_matrix.py --check`) | 0 | links 1,060; 115 REQ rows, 17 GAP; 94 module rows, 0 untested; 41 mermaid and 18 WaveDrom |

**Mutation campaigns.** These re-ran because two files they build changed: the R4 comments in the shadow and the writer, which `tb/pp_top` reads. Every verdict equals round 3's.

| Campaign | rc | Verdict |
|---|---|---|
| d3 (`--jobs 3`) | 0 | 87 of 87 KILLED, goldens PASS (2,469 s) |
| aecp (`--jobs 2`) | 0 | 60 checks, 60 PASS |
| aecp-dispatch (`--jobs 2`) | 0 | 41 checks, 41 PASS |
| maap (`--jobs 2`) | 0 | 32 checks, 32 PASS |
| adp (`--jobs 2`) | 0 | 32 checks, 32 PASS |
| acmp (`--jobs 2`) | 0 | 19 of 19 KILLED |
| notify (`--jobs 2`) | 0 | 40 of 40 KILLED |
| gsi (`--jobs 2`) | 0 | 20 detected |
| name_wr | 0 | decode killed |

`srp_top`, `srp_admission` and `retry_mutants` read no changed file and were not re-run.

**Parent consumer set (16) at dev `cdf49d1a`.** The processor gitlink is at `3957814`. The patches were applied in order: c4c6 (`67bcd698…`), C8's (`aa5a88eb…`), then this round's p2 (`590f791d…`). The copy is `parent2/` and the logs are `pgates2/`.

| # | Gate | rc | Note |
|---|---|---|---|
| 1 | `check_cpp_idiom.py` | 0 | |
| 2 | `check_py_idiom.py` | 0 | |
| 3 | `check_rtl_source_lists.py` | 0 | |
| 4 | `pp_srcs.py --check --selftest` | 0 | |
| 5 | `check_port_contracts.py` | 0 | 1,757 processor ports, 111 undocumented, unchanged |
| 6 | `measure_naming.py --check` | 0 | |
| 7 | `measure_test_evidence.py --check` | 0 | |
| 8 | `docs_check.py` | 0 | |
| 9 | `xvlog_gate.py --check` | 0 | |
| 10 | `test_builder.py` | 0 | "ALL GATES PASS EXCEPT 1 NOT RUN": its calibration arm needs an mf48 build tree that is not on disk, as in round 3 |
| 11 | `lint_rtl.py --check` | 0 | |
| 12 | `pp_shadow` | 0 | |
| 13 | `nvm_cosim lint` | 0 | |
| 14 | `nvm_cosim quick` | 0 | |
| 15 | `milan_dp` | 0 | 9 RESULT: PASS, none FAIL |
| 16 | `milan_dp_render` | 0 | 5 PASS |

**The reviewers' own scripts, re-run at `3957814` with only their head pin changed** (and R436-3's clone path):
- **R436-3 `run_plant.sh`, all 13 Z plants:**
  - Z1 and Z8 fail T28g, 2 each; Z3 fails T28h 2; Z10b fails T28j 3; Z10 stops at `elab_bounds.sh`'s width lint.
  - Z2 and Z5 fail T28f 1 each; Z4 22, Z6 20, Z7 19, Z9 15, Z11 15 and Z12 27 (`rev/r436f/plant_*.log`).
- **R436g** (`babble_probe.sh`): the head is 0 broken at 3, 37 and 100. Z1, Z3, Z8 and Z2 fail FZ9 at each bound (`rev/r436f/babble.log`).
- **R436h** (`resume_long_probe.sh`): the head is 0 broken at 3 and 37. Z10b fails FZ7 at each (`rev/r436f/resumelong.log`).
- **R437-3 `probe.py` with `spec_drain.py`:** base is 0 in every cell, and so is FZ:base at 1, 3 and 37. Every B plant fails at 100, 37 and 20 under pristine and coincident; the counts equal the gate rows. On the harness, all but B3, B4, B7, B12 and B13 fail.
- **R437-3 `spec_zdrain.py`:** ZD_head is 409/0 in all six cells. B6, B6b, B7 and B8 fail 3 each in every cell, B10 fails 4 and B12 fails 1 (`rev/r437f/out/`).

**Before the final head.** The same sets ran at `a691e0e`, whose tree differs only in FZ10's message, with identical verdicts (`rev/r436`, `rev/r437`). The interim parent run there was stopped at gate 10 when the head moved; gates 1-9 had passed.

**Peak memory:** 12.1 GB anonymous, once, at 03:35, when 24 plant builds ran at once. No process was lost and every result is complete. Every later wave stayed at 10 or fewer builds, under 5 GB.

## Out-of-context cost

The recipe is sv2v, then Yosys `synth_xilinx -family xc7 -flatten` (`ooc/ooc.sh`). The port's input bytes equal round 3's (`cmp`), and the measurement reproduces round 3 exactly:

| Setting | LUT / FF / CARRY4 | Over round 2 |
|---|---|---|
| default | 296 / 164 / 30 | +51 / +16 / +9 |
| 1 | 287 / 138 / 23 | +39 / +16 / +9 |
| 2^31-1 | 301 / 168 / 31 | +35 / +16 / +9 |
| 125,000,000 | 309 / 164 / 30 | +48 / +16 / +9 |

Round 4 adds nothing.

## REVIEW READY

#15 comment 5964850117, for head `3957814550f164d72bfaad5d28cd0e7cac0ecaaf`. Main was `c74711d4` at the last fetch (02:56Z). PR-BODY.md is 62,854 characters; its first line is `[A498]`, and it keeps the five `Closes` lines, since both reviews judge every issue met. A continuation waits for the re-reviews and must not re-post.
