[R445] NEGATIVE - exact head c066dd83a2004f9b3640a933860c4d9e677d017e

# R445-1 external independent review: processor issue #83 / PR #150 (lane P1)

- Exact head `c066dd83a2004f9b3640a933860c4d9e677d017e`, tree
  `a4680a7638f44d0bcc45278088d33feea7bfe6fa`. Source base `ddb3119dbbce59f81bf7a536a1ad90a20546edb2`;
  the round-1b merge parent `main` `f4167536d358c996f4e1b70b875879c1651f85d3`.
- Scope: closes #52 #59 #61 #62 #63 #83. The D3 contract is as amended by the manager's
  ruling 5967611704: the channel maps are the integrator's, and the processor's roll-back
  resets only its two AECP stores. Parent gate 16 is as ruled in 5969246536.
- Verdict basis: three open MINORs. F1 is Docs. F2 is Conformance, RTL and Docs. F3 is
  Tests and Docs. Robustness is clean. Three RESIDUE items and three SUGGESTIONs do not
  block.
- Classification note. I wrote my first verdict (NEGATIVE, on F1) and ledger before reading
  any other review. In that pass I graded F2 and F3 as RESIDUE. Each one corrects a
  contract-ownership or coverage-status claim, which is more than wording, and I had been
  unsure. The owner rule makes "unsure" MINOR, so I now grade both MINOR (section 8).

## 1. Reconstruction order and sources

1. **Repository guidance.** The tree has no `AGENTS.md` or `CONTRIBUTING.md`. I used
   `README.md` and `docs/README.md` (conventions, single-source rules, `make check`).
2. **Scope.** Issue #83 body and its comments, read in order:
   - 5965788915, the lane assignment;
   - 5967588719, the STOP on the maps;
   - **5967611704, the ruling: maps are the integrator's**;
   - 5968343520, REVIEW READY;
   - 5968352676, round 1b;
   - 5969239148, the gate-16 STOP;
   - **5969246536, the ruling: (b), recorded against milan-fpga #643**.

   I also read the bodies of issues #52, #59, #61, #62 and #63 (#61 has three manager
   comments, one withdrawn).
3. **Authorities.** 07 §3.4, §5.1 to §5.3 and F07.8. 02 §8.1. 06 §4, §6.2.1 and §6.5. 09 §3
   (NVM row) and §8.2. The integrator guide (marks row, bring-up steps 4 to 6). 00 GAP-08,
   GAP-09, REQ-AEM-011/-013/-021, REQ-NOT-005 and REQ-PER-001/-002/-003.
4. **Diff and history.** `ddb3119d..c066dd8`: 26 commits, 61 files. The PR's own delta is
   `f4167536..c066dd8`: 22 files, 4 of them RTL (`KL_aecp_nvm_writer`,
   `KL_aecp_desc_store`, `KL_aecp_engine`, top comments). I also checked the merge
   `9ca7468`'s two conflict resolutions and `c066dd8`.
5. **Public evidence.** milan-fpga `3a657083` `review-evidence/ppP1-r1`. Every file's
   sha256 equals its `MANIFEST.json` `published_sha256`
   (`receipts/evidence/published_evidence_sha256.txt`). The live PR body equals the
   published `author/PR-BODY.md` but for one trailing blank line.
6. **Prior public findings.** At the start of my pass, PR #150 had no review, no review
   comment and no finding: only the two "review started" notices. Section 8 covers the
   one public review posted during my pass. I read it only after this verdict and ledger
   were written.

## 2. What I executed (all at the exact head unless stated)

| # | Probe | Result | Receipt |
|---:|---|---|---|
| 1 | Pinned simulator identity | Verilator 5.050 2026-07-01 rev v5.050 (the wrapper under the tools directory) | (this report) |
| 2 | `tb/pp_top --cuts-only` (D3KR) | rc 0, **1,000 checks, 0 failures**, 86 s. Classes at the cut per type in `cuts_summary.txt`; every type sees erased, torn-header, torn-payload and B-whole cuts; `name` never sees A whole (0 of 32), `cfg` one torn payload | `receipts/head/` |
| 3 | `--volatile-only` (D3V), `--d3-only` (D3) | rc 0: D3V 11 checks, D3 319 checks, 0 failures | `receipts/head/` |
| 4 | **Planted torn-write acceptance, D3 writer** (crc compare intact; a frame the crc refuses is routed on to the value rule) | **caught**: rc 1, 34 failures (name 29 seeds, ptof 5). For cfg, rate, clks, fmti and fmto the value rule refuses the torn value, so the plant is behaviour-equivalent there | `receipts/plants/torn_d3_refusal_ruled/` |
| 5 | **Planted torn-write acceptance, binding manager** (crc compare intact; a complete record that fails it is stored like a good one) | **caught**: rc 1, 21 failures (bind: 18 torn payload, 3 torn header) | `receipts/plants/torn_bind_refusal_stored/` |
| 6 | **Planted stale-record acceptance, D3 name stage** (a blank name record in pass 1 writes back what the reset-less name buffer still holds) | **caught**: rc 1, 4 failures (the 2 erased name seeds, plus their later-change checks) | `receipts/plants/stale_d3_name_blank_applied/` |
| 7 | **Planted stale-record acceptance, binding manager** (`valid_r` survives `rst_n` and a blank record keeps it, so the shadow's pre-cut entry is replayed) | **caught**: rc 1, 38 failures. 6 are the targeted bind verdicts (erased 2, torn header 4); 32 are a collateral cfg premise | `receipts/plants/stale_bind_blank_kept/` |
| 8 | `--cut-seed S` reproduction | Under the plants, `--cut-seed 0xA0233AE1` and `--cut-seed 0xD3C0FFEE` print exactly the full run's failure lines for those seeds (same cut offset, class and counters). At the head, a standing seed and a non-standing seed pass (39 checks, rc 0). The bench must be run from `tb/pp_top`, where its ROM images are; from another directory every check fails | `receipts/seed/` |
| 9 | The lane's own D3 controls (`d3_mutants.py --jobs 6`, the 25 arms of issues #52/#59/#61/#62/#63/#83) | 4 goldens PASS, **25 of 25 KILLED**, every failing-check count equal to its README row (`cut_binding_crc_ignored` 20, `cut_frame_crc_ignored` 30, `registry_survives_reset` 4, `lock_survives_reset` 4, `identify_survives_reset` 1, ...) | `receipts/d3_lane_controls/` |
| 10 | `notify_mutants.py --only ident_burst_from_t0`, at the head and at `main` `f4167536` | Head: golden PASS, KILLED, **21** failures. Main: **20**. The one extra is ID6d ("frame 2 to 3 spaced 14979 clocks"), as the README row states | `receipts/notify/` |
| 11 | `tb/pp_top` `make run` (five builds) | rc 0, **10,390 checks, 0 FAIL**. Default build 9,918 here against 8,724 on `main` (+1,194 = D3 +169, AD +12, D3V +11, D3KR +1,000, HZ +1, ST +1) | `receipts/pp_top_full/` |
| 12 | `tb/desc_store` | rc 0, 586 checks | `receipts/gates/` |
| 13 | `lint_hdl.sh` (pinned simulator first on PATH), `make check`, `gen_matrix.py --check` | rc 0, 0, 0: 41 modules LINT OK, 1,114 links, matrix OK | `receipts/gates/` |
| 14 | Writer elaboration at its shape edges | 1 and 128 names (maximum shape) elaborate clean; 0 and 129 are refused by `g_shape_check` | `receipts/gates/writer_shape_lint.txt` |
| 15 | ROMs regenerated from their generators at base `ddb3119d`, `53e1474`, `f4167536` and the head (microcode, listener ROM, both descriptor images and maps) | all **byte-identical** across the four. The generators' blobs are identical too | `receipts/gates/roms_sha256.txt` |
| 16 | Synthesis count, the instrument the PR names (sv2v, then Yosys 0.66 `synth_xilinx -flatten -family xc7`, RAM32M = 4 LUT-eq), base against head | 1x1, 38 names: writer 928/505 → 1,541 (+11 RAM32M)/597, store 1,326 → 1,374, so **+705 LUT-eq / +92 FF exactly**. 39 names: **+683 / +94 exactly**. 8x8 writer at 99 names: 1,220/550 → 2,769/767, i.e. +1,549 LUT / +217 FF against the stated +1,520 (S2) | `receipts/ooc/` |
| 17 | DR3a at head and `main` | Blank-restore terminal **1,286 → 2,182** clocks; longest per-wait unchanged (D3 405 / 853) | `receipts/dr3a/` |
| 18 | **Parent gate 16 phase evidence**: disposable blobless clone of milan-fpga dev `bbf704ec`, submodules at their pins, `make tdm8render` (shipping leg). Four arms below | reproduces exactly (section 6) | `receipts/gate16/` |
| 19 | Clone integrity after all probes | Exact HEAD and tree. Porcelain empty. Index equals the tree for all 501 entries. Every tracked blob re-hashes to its index blob and every mode matches. This repository carries **no gitlinks** | `receipts/clone_integrity.txt` |

The plant scripts work only by exact-once text substitution, in disposable `git archive`
copies. No tracked byte of the review clone was edited.

## 3. Acceptance, issue by issue (maps per ruling 5967611704)

| Issue, line | Verdict | Evidence |
|---|---|---|
| #52 1 (CLKSRC committed after an accepted SET, debounced port) | met (main) | D3S1 `clks`, D3C3. Reachable in D3 (319 PASS) |
| #52 2 (saved index before enable; blank/torn → image) | met | D3C5 (blank, corrupt, torn: row unset, GET 0, export 0). D3C6 (export correct in every cycle `dbg_adp_enable_o` is high, the first included) |
| #52 3 (commit bytes and restored value; refused SET commits nothing) | met (main) | D3S1/D3R1 byte-exact. The refusal arms of D3C2 / W10j |
| #52 4 (marks consumed or removed; REQ-AEM-013 updated) | met | `aecp_nvm_stb_o`/`aecp_nvm_mark_o` are top outputs (`protocol_processor_top.sv:3881-3882`), no `_nc_` net. REQ-AEM-013 updated |
| #59 1 to 3 | met | D3V1 (two registrations, one TIME_LIMITED, third controller's change notifies both at seq 0). D3V5 (the same after the cycle notifies neither). D3V6 (66 s, no CONTROLLER_AVAILABLE, no expiry DEREGISTER). D3V8 (16 SUCCESS). D3V9 (byte-exact seq 0) |
| #59 4 | met | `registry_survives_reset` KILLED, 4 (D3V5, D3V8, D3V9). `tb/pp_top/README.md:1148` |
| #62 1, 2 | met | D3V1 to D3V4 and D3V7: lock clear and IDENTIFY 0 in every cycle from `restore_go_i`; GET_CONTROL 0; LOCK_ENTITY from the second controller SUCCESS; binding preload arrives (D3V2) |
| #62 3 | met | `lock_survives_reset` 4 and `identify_survives_reset` 1, both KILLED and recorded (`README.md:1149-1150`). The registry arm is as in #59 |
| #63 1, 2, 3 | met | Record `0x00` (main #131). AD5 (SET over AECP, debounce, `rst_n`, restore: first ADPDU, GET_CONFIGURATION and ENTITY.current_configuration agree; the bench image default is 1, so it sets the non-default 0). AD7 blank, AD8 corrupt, AD9 torn |
| #61 1 | met as amended | The D3 writer commits RATE, FMT_IN/OUT, PT_OFS, CLKSRC, CFG_IDX and NAMES through the port. The parent D3 §3.1 trigger replaces mark consumption. Marks are top outputs. MAPS_IN/OUT are the integrator's by the ruling |
| #61 2 | met as amended | Restore before enable into the dyn store with valid flags, and into the name table after the image proof (D3N3, D3N7). Bad crc/version keeps the default (D3R2, D3N4, D3C5, AD8). The map store is the integrator's |
| #61 3 | met | D3R1 and D3N3 read back over GET_* and READ_DESCRIPTOR. Every record type is cut mid-commit (D3K) and at 32 seeded-random points (D3KR) |
| #61 4, #83 4 | met | GAP-08/GAP-09 bodies and the REQ-AEM-011/-021 cells point at no open item (searched: no "open", "#70", "not implemented", "later" or "owed" left in GAP-08/09). 06's former lines 326-327/406-407 are gone. Stale claims remain elsewhere (F2, F3) |
| #83 1, 2 | met as amended | As #61, with CFG_IDX. D3R1 grades the volatile set at its defaults after the saved-set cycle; D3V does so in depth |
| #83 3 | met | D3KR (32 standing seeds per type, all 8 types, real `rst_n`, the oracle from the bytes held at the cut, a restored binding PASSIVE / PRB_W_AVAIL, crc fallback). Seed printed per check; `--cut-seed` reproduces (probe 8). Beyond the two crc controls, four independent plants are caught (probes 4 to 7). D3K keeps its fixed cuts |
| Ruling 5967611704 item 1 (contract amendment in 07, 02 §8, integrator guide, REQ-PER-001) | met in the named documents | 07 §5.1 "Who persists what", §5.2 table, §5.3. 02 §8.1. 06. Integrator guide marks row and step 4. 00 rows. Stale map-stage claims survive in two port banners, the writer banner and one suite README (F2) |
| Ruling 5967611704 item 2 | met | probes 2 and 4 to 9 |

## 4. The round-1b merge

- **Both contracts kept.** C7's 09 §8.6 (NVM port) and §8.7 (counters face) are present at
  the head. So are this lane's 09 §8.2, 07 §5.1 and the integrator guide's step 4. The
  conflict resolutions in `9ca7468` are unions: the `.PHONY` list of `tb/pp_top/Makefile`,
  and `one_section` with `volatile_only || cuts_only || one_seed` and `ctr_only`.
  `dbg_name_lane_i` and C7's counter state are both initialized.
- **ROMs byte-identical** (probe 15).
- **Counts match the README.** `tb/pp_top` 10,390 (probe 11). The 25 lane controls match
  their rows (probe 9). `ident_burst_from_t0` is 21 at the head against 20 at `main`; the
  extra failure is ID6d, measured at 14,979 clocks as the README row explains (probe 10).
  That justification reproduces.
- **No port, parameter or register change.** The writer's new ports are internal. The top
  changes only comments. The parameter `DESC_NAME_ENTRIES_P` now also bounds the writer
  (refusal past 128 proven, probe 14).

## 5. Area

- **Reproduced.** +705 LUT-eq / +92 FF at 1x1 with 38 names, and +683 / +94 at 39 names
  (probe 16).
- **Where it goes.** Almost all of it is the writer: per-record dirty bits and round-robin
  pick over 38 to 39 more records, the 64-byte name buffer (11 RAM32M), the 7-bit
  cursors, and the byte mux. The store adds +48 LUT (region 0xA).
- **Necessity.** Under the contract's one-dirty-bit-per-record, no-shadow design, this is
  the expected order of cost. It sits within the parent's 750 / 400 names-stage ceiling.
  I judge it necessary for the chosen design.
- **Statement.** The figure is in the PR body's out-of-context section and in the
  published HANDOFF's parent-visible list (item 8 and R1b.5 item 5). It is absent from the
  PR body's own numbered parent-visible list (R2).

## 6. Parent gate 16 phase evidence (not re-judging ruling 5969246536)

| Arm | Processor | Bench change | Result (shipping leg, 155 checks) | First-event delay |
|---|---|---|---|---|
| A | dev's own pin `631eeb34`, dev exactly | T30 feed start +1,156 cycles | **FAIL 2**: fill 227/292, band 284/292 | 8.830..9.035 ticks |
| B | `631eeb34`, dev exactly | none | PASS | 8.385..8.589 |
| C | head `c066dd8`, with `parent-adoption-c8-bbf704ec.patch` then `-p2-p1-1269cdaf.patch` | none | **FAIL 2**: 227, 285 | 8.830..9.034 |
| D | the same as C | T30 feed start +927 | PASS | 8.385..8.589 |

Every number equals the published HANDOFF's R1b.4 tables. So dev's own pin fails the
same two T30 INTERNAL LAW checks when only the feed's phase moves, and the head passes
when its feed is moved back. The phase evidence reproduces.

Also checked:
- The re-based c8 patch's `+`/`-` lines are identical to the `cdf49d1a` original.
- The p2 successor applies after it unchanged.

## 7. Findings

### F1 - MINOR - Docs

The re-based consumer patch is described with the wrong hunk count.

- **Where.** PR #150 body, "Round 1b" → "Parent consumer set at milan-fpga dev
  `bbf704ec`", first bullet: "The re-based **`parent-adoption-c8-bbf704ec.patch`** keeps
  all 13 hunks, so no hunk dropped". The same figure is in published
  `author/PR-BODY.md:284`, `author/HANDOFF.md:745`, and issue #83 comment 5969239148
  item 3.
- **Evidence.** The published patch (sha256 `3340d2e8…4c`, 8,546 bytes) has **7 files and
  11 hunks** (`grep -c '^@@'` = 11), or 12 contiguous change blocks. The `cdf49d1a`
  original has 11 as well. Its `+`/`-` lines are identical to the re-based patch's, so the
  substantive claim (no hunk dropped) is true.
- **Impact.** The manager's ruling 5969246536 accepted this patch as a consumer patch, and
  its record carries a count that does not match the artefact. A reader who checks
  "13 hunks" against the file finds a discrepancy. The correction changes a stated
  figure, so under the owner rule this is not RESIDUE.
- **Required outcome.** Correct the PR body to "keeps all 11 hunks (7 files), every `+`/`-`
  line identical to the `cdf49d1a` original, so no hunk dropped". The issue comment is
  frozen by the no-edit rule, so a public correction note should accompany the fix.
- **Verification.** `grep -c '^@@' parent-adoption-c8-bbf704ec.patch` → 11, and
  `grep -c '^diff --git'` → 7, against the PR body text.

### F2 - MINOR - Conformance, RTL, Docs

Stale "processor map stage" claims contradict the D3 contract as amended by ruling
5967611704. My first pass graded this RESIDUE; see the classification note.

- **Authority.** Ruling 5967611704 item 1. At this head, 07 §5.1 "Who persists what" and the
  §5.2 rows for `0x60`/`0x70` ("the processor never writes or reads it"). The integrator
  guide's marks row ("Group 6's records … are **yours**").
- **Impact.**
  - The top's port banner is the integrator-facing port authority, and the integrator guide
    links "Top declaration and banner".
  - The banner tells an integrator that the processor's map stage is merely unimplemented.
    That implies a later processor release would persist maps, while the amended contract
    makes the save, restore and roll-back the integrator's to build (parent #637).
  - The engine banner, the writer banner and the suite README repeat it.
  - The writer banner's format-rule rationale still rests on maps that "reset EMPTY in this
    stage", which the amendment removed.
- **Required outcome.** Reword each place to the amended rule. No logic change. The exact
  texts:

- `hdl/top/protocol_processor_top.sv:779-781`, "…group 6 is the saved-state contract's map
  stage, triggered by map edit phase 5, and not implemented in this release." → "…group 6's
  records, the channel maps, are the integrator's to persist (07 §5.1, the ruling on
  #83): it saves a port's set from map edit phase 5, and the processor writes and
  restores no map record."
- `hdl/aecp/KL_aecp_engine.sv:469-470`, "Phase 5 is also the saved-state contract's map
  trigger (its map stage, not implemented here yet)." → "Phase 5 is also the integrator's
  map-persistence trigger (07 §5.1); the processor writes no map record."
- `hdl/aecp/KL_aecp_nvm_writer.sv:117-118`, "Channel maps are a later stage." → "Channel maps
  are the integrator's (07 §5.1); this writer never writes or reads them."
- `hdl/aecp/KL_aecp_nvm_writer.sv:94-96`, "the maps it will be checked against reset EMPTY in
  this stage, so nothing restored can be orphaned" → "the maps are the integrator's,
  restored after restore_done_o and judged against the formats this walk restored (07
  §5.1), so the format/map coupling is the integrator's".
- `tb/pp_top/README.md:665`, "maps are a later stage" → "maps are the integrator's, 07 §5.1".
- **Verification.** `grep -rn "map stage\|later stage\|not implemented" hdl/
  tb/pp_top/README.md` finds no claim of a processor map stage. `lint_hdl.sh`, `make check`
  and `gen_matrix.py --check` stay rc 0.

### F3 - MINOR - Tests, Docs

The NVM port suite's README still records the randomized cut points as owed. My first pass
graded this RESIDUE; see the classification note.

- **Where.** `tb/nvm_port/README.md:1062-1064` ("…so the randomized half is still owed")
  and `:1344-1345` ("The RANDOMIZED cut points `09_verification.md:56` asks for are still
  owed").
- **Authority.** Issue #83 cites exactly this README text as its shortfall. Its acceptance 3
  is now delivered by `tb/pp_top` D3KR, which 09 §8.2 at this head lists.
- **Impact.** The tree carries two contradicting coverage statements for the same 09 clause.
  Correcting it changes a stated coverage status, so it is not wording alone.
- **Required outcome.** Append to each passage: "(delivered at the top by `tb/pp_top`
  section D3KR, issue #83: every record type both producers write, cut by `rst_n` at 32
  seeded-random points each, `--cut-seed S` reruns one; this suite's own cuts stay
  fixed)". If anything stays port-local and owed, state it.
- **Verification.** Grep both passages; `make check` rc 0.

### R1 - RESIDUE - Docs (PR body)

The PR body still presents gate 16 as undecided. The "What remains" bullet "Parent gate 16
at dev `bbf704ec` (Round 1b, below) waits for a decision", and the Round 1b "(a)/(b)"
options, predate ruling 5969246536. Exact fix: "Parent gate 16 at dev `bbf704ec`: ruled
(b) (#83 comment 5969246536); its two T30 INTERNAL LAW checks are recorded against
milan-fpga #643, which lands before the second pin adoption."

### R2 - RESIDUE - Docs (PR body)

The numbered parent-visible list (items 1 to 11) omits the name stage's area, although the
HANDOFF's list carries it. Exact fix, a new item: "12. Area (the parent's DR4 instrument,
synthesis counts): +705 LUT-eq / +92 FF at 1x1 with 38 names (+683 / +94 at dev
`bbf704ec`'s 39), within the 750 / 400 names-stage ceiling the parent's glue shares."

### R3 - RESIDUE - Docs (PR body)

"`tb/pp_top` grows from 9,168 to 10,362 checks: D3 150 to 319, AD 55 to 67, D3V's 11, and
D3KR's 1,000" itemizes 1,192 of the 1,194 added checks. The totals are right. Exact fix:
append ", HZ 176 to 177 and ST 18 to 19 (the name saves' drain checks HZ9 and ST1)".

### S1 - SUGGESTION - Tests

D3KR's class mix leaves two thin spots:
- `name` never lands "A whole" (0 of 32);
- `cfg` lands one torn payload.

D3K's fixed ERASE-grant cut covers the first. Also, for the five small scalar types, a
torn-acceptance defect is masked by the value rule (probe 4). Consider asserting a minimum
per (type, class), or adding targeted seeds, so that a later change of span cannot leave a
class unexercised silently.

### S2 - SUGGESTION - Docs

The 8x8 writer diagnostic "+1,520 LUT, +217 FF" reproduces as +1,549 LUT / +217 FF with the
stated instrument and shape. The base (1,220/550) and FF match exactly, and the shipping
1x1 figures match exactly. Record the sv2v version and the full parameter set beside the
diagnostic, or state it as approximate.

### S3 - SUGGESTION - Robustness, Docs

Name records are keyed by the writable-name ordinal alone. A regenerated image whose name
table assigns ordinals differently would write saved names back onto other objects, while
staying within the region 0xA count. 07 §5.2 and the integrator guide could state that an
image change that renumbers names requires erasing records `0x80`+, or what guards it.

## 8. Other public review at this head (read after my verdict and ledger were written)

During my pass the internal reviewer posted R444-1 NEGATIVE at the same head (PR #150
comment 5969549669, 2026-10-03T13:19Z). I read it only after this report's verdict line,
sections 1 to 7 and ledger had been written. I first graded F2 and F3 RESIDUE; the
classification note above explains the change. Every R444-1 finding, resolved or retained
at this head:

| R444-1 item | At this head | Mine |
|---|---|---|
| F1 MINOR (stale "processor map stage" claims in 4 places) | **retained**: the text is present at the cited lines (verified) | F2, MINOR, same lenses |
| F2 MINOR (`tb/nvm_port/README.md` "still owed") | **retained**: present at `:1062-1064` and `:1344-1345` | F3, MINOR |
| F3 MINOR (hunk count 13, actually 11) | **retained**: found independently | F1, MINOR |
| R1 RESIDUE (gate-16 decision pending in the PR body) | **retained** | R1 |
| R2 RESIDUE (area missing from the parent-visible list) | **retained** | R2 |
| S1 SUGGESTION (a floor per type and class in D3KR) | open suggestion; I agree | S1 |
| S2 SUGGESTION (model a non-atomic ERASE in the cut device) | open suggestion; I did not check the device model's erase atomicity myself, so I take no position beyond agreeing it is non-blocking | none |

My R3, S2 and S3 are not in R444-1. Our measurements agree wherever both of us measured:
- D3KR 1,000/0 and its class distribution;
- the torn plant's 34 failures (name 29, ptof 5);
- the stale name plant's 4 failures;
- `ident_burst_from_t0` 21 against 20;
- the lane controls' counts;
- the ROMs;
- all four gate-16 arms.

## 9. Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | **UNCLEAN (F2)** | Acceptance of #52 #59 #61 #62 #63 #83 line by line (section 3). Rulings 5967611704 and 5969246536. Milan v1.2 §5.3.4.1/.2, §5.3.12, §5.3.13, §5.4.2.15/.16, §5.5.3.5.2; IEEE 1722.1-2021 §7.4.7/.8, §7.4.37. 00 rows. 07 §5.1 to §5.3 | R445-1 | c066dd83a2004f9b3640a933860c4d9e677d017e |
| RTL | **UNCLEAN (F2: port and module banners only; the logic is clean)** | `KL_aecp_nvm_writer` name stage (geometry, buffer ports, restore W_NNAME/W_NAPPLY, service S_NLATCH, frame/crc over 72 B, trigger tap, shape check). `KL_aecp_desc_store` region 0xA. `KL_aecp_engine` taps and `name_wr_o` gating. Top comments. Elaboration edges. Area reproduced | R445-1 | c066dd83a2004f9b3640a933860c4d9e677d017e |
| Robustness | CLEAN | Reset cuts on all 8 record types. Torn/stale plants caught. DR3a. Restore deadlines unaffected (longest per-wait unchanged). Stale buffer has no reset but never applied (stale plant proves the guard matters). nvm_cosim modules unchanged. Gate-16 phase dependency reproduced | R445-1 | c066dd83a2004f9b3640a933860c4d9e677d017e |
| Tests | **UNCLEAN (F3)** | D3KR, D3V and D3 runs. 4 independent plants. `--cut-seed`. 25 lane controls with counts. `ident_burst_from_t0` 21 against 20. Full `tb/pp_top` 10,390. `tb/desc_store` 586. ROMs. Lint and matrix | R445-1 | c066dd83a2004f9b3640a933860c4d9e677d017e |
| Docs | **UNCLEAN (F1, F2, F3)** | 00, 02, 06, 07, 09, hdl-engineer and integrator guides, `tb/pp_top`, `tb/nvm_port` and `tb/desc_store` READMEs, the PR body, the published HANDOFF and patches. `make check` (1,114 links) | R445-1 | c066dd83a2004f9b3640a933860c4d9e677d017e |

The ledger as first written, before I read R444-1:
- Conformance, RTL, Robustness and Tests: CLEAN;
- Docs: UNCLEAN (F1).

Only the reclassification of F2 and F3 changed it.

## 10. Real limits

- **Banks not re-run.** I did not re-run the full processor bank (`run_suites.sh`, 33
  suites). Of `d3_mutants.py` I ran the lane's 25 arms, not all 110; of `notify_mutants.py`
  only `ident_burst_from_t0`. I did not re-run the ctr, aecp, dispatch, acmp, gsi,
  adp_engine or maap campaigns, or the name-write control. Their PR-body results are
  unverified here.
- **Parent.** Only gate 16's shipping leg ran, in four arms. Its two-stream leg and the 5
  leg-defect arms, and gates 1 to 15, did not. The parent census and capture figures
  (164 records, 13,210 B, 13.86 ms) and name entries (39 at 1x1; 107 at 8x8 seen in the
  generated header) are the parent's, and were not re-measured.
- **Area.** These are synthesis counts (sv2v + Yosys). No Vivado, no placed comparison. The
  8x8 diagnostic differs by 29 LUTs (S2).
- **Hardware.** Physical calibration NOT RUN. No hardware. Field skips are not hardware
  proof.
- **Hosted CI.** Not inspected. The manager owns hosted/act acceptance.
- **Bank receipts.** The manager's source static/builder and native bank receipts were not
  present in the published evidence tree at `3a657083`, which holds only the author's
  packet and its manifest. I could not inspect them.

## 11. Pending manager duties

- Return F1 to F3 to the author. Their fixes are the PR body's count, plus banner and README
  text, with no logic change. Post a correction note on #83 for F1's figure.
- Carry R1 to R3 to the residue checklist.
- Build the final current-dev candidate at the merge turn (source base `ddb3119d`, live dev
  `bbf704ec`).
- Run the consumer bank at `bbf704ec` with c8-bbf704ec then the p2 successor, gate 16
  recorded against #643.
- Publish the bank receipts.
- Hosted/act acceptance.
- Merge needs two independent positive reviews.

R445-1 FINISHED
