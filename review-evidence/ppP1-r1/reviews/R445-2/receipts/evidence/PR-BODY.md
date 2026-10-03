[A515]
Closes #52
Closes #59
Closes #61
Closes #62
Closes #63
Closes #83

Lane P1 (persistence beyond BINDING), branch `p1-persistence` from `main` `ddb3119d`, as
assigned on #83 (comment 5965788915). The lane stopped once, on the channel maps. The
manager's ruling (#83 comment 5967611704) made map persistence the integrator's, and the
lane then finished the ruling's items. With the maps assigned to the integrator, every
acceptance line of the six issues is met.

## Items

**1. #59 and #62, the volatile set across a reset.** Section D3V of `tb/pp_top`
(`--volatile-only`, `make volatile`). Before the reset:
- the device holds a saved BINDING record, which the first boot restores;
- one controller registers, and a second registers TIME_LIMITED (IEEE 1722.1-2021
  §7.4.37.2);
- a third controller's change notifies both at sequence_id 0;
- the first locks the entity (the second is refused ENTITY_LOCKED) and sets IDENTIFY
  to 255.

A power cycle follows: `rst_n` with the device carried, then `restore_go_i`. After it:
- the binding preload arrives;
- IDENTIFY reads 0 and `aecp_lock_held_o` is 0 in every cycle from `restore_go_i`, and
  GET_CONTROL reads 0;
- a third controller's change notifies neither former controller, and for 66 s nothing
  reaches them (no CONTROLLER_AVAILABLE, no expiry DEREGISTER);
- LOCK_ENTITY from the second controller succeeds;
- sixteen new controllers register;
- a returning controller restarts at sequence_id 0, byte-exact.

Deleting `valid_r`, `lk_held_r` or `ident_r` from its reset branch each fails named D3V
checks (Milan v1.2 §5.3.4.1, §5.3.4.2, §5.3.12, §5.4.2.21).

**2. #63, the configuration index.** Main already saves record `0x00` and restores it
before the enable (D3S1, D3R1, AD5 to AD7). AD8 adds a corrupt record (configuration 0
with a wrong crc) and AD9 a torn read (cause 1). Each keeps the image default in the
first ADPDU, GET_CONFIGURATION and READ_DESCRIPTOR(ENTITY).current_configuration (review
§8 item 1; IEEE 1722.1-2021 §7.4.7/.8).

**3. #52, the clock source.** Main already met lines 1, 3 and 4: D3S1, D3C1 to D3C4,
and the marks exported as completion notifications, not `_nc_` nets. D3C5 adds a
blank, a corrupt and a torn record 0x0A: each keeps the image's index in the row,
GET_CLOCK_SOURCE and `aecp_clk_src_index_o`. D3C6 shows the saved index exported in every
cycle the ADP engine's enable is high, the first included (Milan v1.2 §5.3.11.1,
§5.4.2.15/.16).

**4. #61 and #83, names and maps.** The scalar groups were main's (#131). This PR adds
the **name stage** (Milan v1.2 §5.3.13; IEEE 1722.1-2021 §7.4.17/.18; parent D3 §3.1,
§8.5, §18.3). The D3 writer saves every writable name as record `0x80` + ordinal, the
64-byte entry verbatim:
- **Trigger.** The descriptor store's accepted live name-lane write. SET_NAME writes only
  the lanes that change, so an unchanged name saves nothing.
- **Latch.** Eight lanes, taken while no program runs.
- **Restore.** After the image is proven, a saved name is judged by SET_NAME's rule (an
  ordinal the image's name table holds, store region 0xA) and written back.
- **Roll-back.** The descriptor store's reset walks the image again, so the names return
  to the image's.
- **Exports.** `aecp_name_wr_o` does not pulse for the restore, and `d3_unflushed_o`
  covers names.

Section D3N grades:
- both ENTITY names, an EMPTY and a full 64-byte name, the IDENTIFY CONTROL's name and
  the last ordinal, saved byte-exact and restored;
- that the entries hold the image's names at the image proof (cleared first);
- the rule and the frame;
- the roll-back, the taint, and an image loaded late.

Section D3K cuts every D3 record type by `rst_n` mid-commit at fixed points: the ERASE's
grant, the WRITE's grant, after the header, one byte short, and one fixed draw.

**The channel maps are the integrator's** (the ruling on the lane's STOP, below).

**5. The parent-visible list.** Below.

**Ruling item 1: the D3 contract amendment** (documents only, no RTL; Milan v1.2
§5.3.9.1, §5.3.10.1, §5.6.1). The integrator persists the channel maps:
- **Save.** It writes records `0x60`/`0x70` + port from the phase-5 edit commit beat,
  under its own pending.
- **Restore.** It restores them after `restore_done_o` and before it requests the
  enable, judged against the formats the D3 walk restored and exports
  (`aecp_fmt_in_o`/`aecp_fmt_out_o` and their valid bits). The walk judges formats by
  the integrator's judge alone, so the format/map coupling is the integrator's.
- **Roll-back.** It keeps or puts back each port's reset set when the walk rolls back
  (`restore_rb_o`). The processor's roll-back resets its two AECP stores only.

The processor keeps the ATDECC side (GET_AUDIO_MAP, ADD/REMOVE_AUDIO_MAPPINGS), so maps
stay ATDECC-authoritative. The amendment is in:
- 07 §3.4, §5.1 ("Who persists what"), §5.2, §5.3;
- 02 §8.1;
- 06 (the writer's faces, §6.5);
- the integrator guide (the marks row; bring-up step 4, "restore the channel maps
  yourself");
- 00 GAP-08, GAP-09, REQ-AEM-021 and REQ-PER-001.

**Ruling item 2: #83's seeded-random reset cuts, a standing campaign.** Section D3KR of
`tb/pp_top` runs with `--cuts-only` (`make cuts`) and in the default run.
- **Record types.** Every one both producers write: the D3 writer's seven and the
  binding record `0x20`. The binding's change is a BIND_RX of sink 0 to another talker,
  which a sink in PRB_W_AVAIL saves (Milan v1.2 §5.5.3.5.6).
- **Seeds.** 32 standing seeds per type. `rst_n` falls at a clock drawn from the seed,
  anywhere from the record's ERASE grant to past its WRITE's done. A calibration commit
  per type measures that span.
- **Oracle.** The bytes the device holds at the cut, not the RTL. A whole record
  restores A or B; any other bytes must frame no record and keep the default (the
  image's value, or an unbound sink).
- **Checks.** The restore never fails, a restored binding probes PASSIVE (PRB_W_AVAIL),
  and a later change persists. Every check prints its seed, and `--cut-seed S` reruns
  one seed.
- **Mutants.** Removing the binding manager's crc compare fails 20 checks; removing the
  D3 frame's crc compare fails 30.
- **Fixed cuts.** D3K keeps its four fixed cuts.

**Ruling item 3: #61 and #83 close.** Each acceptance line, with the maps assigned to the
integrator:
- **#61 line 1.** The D3 writer commits the scalars and the names through the port. The
  marks are top outputs. The trigger is the accepted changing write: parent D3 §3.1
  "replaces mark-based acceptance" (§15 item 1, RESOLVED), and DR2b.
- **#61 line 2.** Validated records come back before the enable. A bad crc or version
  keeps the default (D3R2, D3C5, AD8, D3N4).
- **#61 line 3.** Each group is set over AECP and read back after a power cycle (D3R1,
  D3N3, AD5). Every record type is cut (D3K, D3KR).
- **#61 line 4.** The documents are updated.
- **#83 lines 1 and 2.** As #61, with CFG_IDX. The volatile set reads its defaults (D3R1,
  D3V).
- **#83 line 3.** D3KR.
- **#83 line 4.** GAP-08, GAP-09 and the REQ-AEM-011/-021 cells point at no open item.

## Validation

Pinned Verilator 5.050, at head `53e1474`.

| Gate | Result |
|---|---|
| `./scripts/run_suites.sh` | rc 0: 33 of 33 suites, 1,021,434 checks (1,020,238 on `main`) |
| `./scripts/lint_hdl.sh` | rc 0, 41 modules |
| `make check`, `scripts/gen_matrix.py --check` | rc 0 (1,069 links) |
| `tb/pp_top/d3_mutants.py --jobs 3` | 110 of 110 KILLED (87 from `main`, 21 for items 1 to 4, 2 for the campaign), six goldens PASS; every failing-check count as recorded |
| `tb/pp_top/name_wr_mutant.py` (at `4b02d4f`) | killed, golden and restored PASS |
| `aecp_mutants.py` (the 27 HZ arms), `notify_mutants.py` (the 2 ST arms), `tb/adp_engine/mutants.py` (30 arms), at `4b02d4f` | all KILLED, controls PASS |
| `tb/desc_store` region 0xA, two planted breaks | both caught |

The suite count corrects the earlier "34 of 34": `tb/` holds 33 suites, at `main` and at
the head alike.

New checks:
- `tb/pp_top` grows from 9,168 to 10,362 checks: D3 150 to 319, AD 55 to 67, D3V's 11,
  and D3KR's 1,000;
- `tb/desc_store` grows from 584 to 586.

Parent consumer set (16 commands) at milan-fpga dev `1269cdaf`, in a scratch copy:
- the trusted tree, its submodules at their pins, and the processor at this head;
- `parent-adoption-c8-cdf49d1a.patch`, then `parent-adoption-p2-p1-1269cdaf.patch`,
  applied cleanly. The second is p2's successor: p2's hunks plus the map amendment in
  the parent's D3 page, where it stated the old rule (§5.1, §5.2, §8.6, §10, §15 item
  2, §18.4), with notes in its status block, §3 item 9 and §8.4.

Every command is rc 0:
- the idiom ratchets (D3KR's code included);
- the source lists;
- the port contracts (1,760 processor ports, 111 <= 111 undocumented);
- naming, and test evidence (10 <= 10 unseeded draw sites);
- `docs_check` (0 findings with the amended D3 page);
- `xvlog_gate`;
- the builder (its gate 11 not run, needing a local build tree, as before);
- `lint_rtl` (90 <= 90);
- `pp_shadow` (311);
- `nvm_cosim` lint and quick (315);
- `milan_dp` (9 benches; mutant and control arms all caught);
- `milan_dp_render` (65 + 152, 5 of 5 leg-defect arms).

Out-of-context cost: the ruling's items add no RTL. The name stage's cost stands, using
the parent's DR4 instrument (synthesis counts, LUT RAM priced as LUTs), shipping 1x1:
- `KL_aecp_nvm_writer`: +613 LUT, +11 RAM32M (+44 LUT-eq), +92 FF;
- `KL_aecp_desc_store`: +48 LUT;
- total: +705 LUT-eq and +92 FF, against the 750 / 400 names-stage ceiling.

The 8x8 writer, a diagnostic, is +1,520 LUT and +217 FF.

## Parent-visible list

1. No top-level port, parameter or register added. `KL_pp_shadow` needs no edit, and
   the modules `nvm_cosim` instantiates are unchanged.
2. `DESC_NAME_ENTRIES_P` is also the writer's name-record count, so it must stay at
   most 128. The parent builds 38 and 99, and its backend already refuses more than 128.
3. After a SET_NAME, record `0x80` + ordinal (72 bytes) is written a debounce later.
   The boot walk reads `2 × DESC_NAME_ENTRIES_P` more records and writes saved names
   back after the image proof.
4. `pend_i` keeps its sticky live-name term. The parent's adoption lane transfers names
   to `d3_unflushed_o` (D3 §10 stage 2, §18.3).
5. `aecp_name_wr_o` no longer pulses for a restore write. Live writes are unchanged.
6. Census, record space and capture are unchanged.
7. DR3a: in the bench, a blank restore's D3 terminal moves from 1,286 to 2,182 clocks
   (about 28 per erased name record), and the longest per-wait is unchanged.
8. **The channel maps are the parent's** (ruling item 1). The parent:
   - writes `0x60`/`0x70` + port from its phase-5 commit beat;
   - restores them after `restore_done_o` and before it requests the enable, judged
     against `aecp_fmt_in_o`/`aecp_fmt_out_o`;
   - keeps or puts back the reset sets on `restore_rb_o`;
   - may hold an early map command on `amap_wait_i`/`amap_edit_wait_i`.

   The processor's roll-back no longer covers the map plane. Milan-fpga #637 owns the
   parent's restore and roll-back.
9. **`parent-adoption-p2-p1-1269cdaf.patch` replaces `parent-adoption-p2-cdf49d1a.patch`**
   (apply c8, then it). It amends the parent's D3 page where it stated the old map rule.
   The names update of that page is the next pin adoption's (ruling item 4).
10. The processor documents the parent reads:
    - 07 §3.3, §3.4, §5.1, §5.2, §5.3;
    - 02 §8.1;
    - 06;
    - the integrator guide's rows and bring-up order;
    - 00 GAP-08, GAP-09 and the REQ rows;
    - 09 §8.1, §8.2.
11. The default `tb/pp_top` run is about 83 s longer (D3KR). Nothing the parent
    consumes changes.

## What remains

- The parent adopts the name stage and the map amendment in its own lanes:
  - name pending transfer;
  - DR3a and DR4 on its product;
  - a cold cycle of every writable name;
  - the map writer, restore and roll-back (#637).
- The counter-notification spacing finding is processor #148.
- Parent gate 16 at dev `bbf704ec` (Round 1b, below) waits for a decision.

## Round 1b: merge of `main` `f4167536` (lane C7, the counters face)

Merge only, as assigned on #83 (comment 5968352676). It is a `--no-ff` merge, `9ca7468`
(parents `53e1474` and `f4167536`), followed by `c066dd8`, which records one moved
mutant count and the default build's section order.

**The merge.**
- Two textual conflicts, both resolved as the union: the `.PHONY` list of
  `tb/pp_top/Makefile`, and the section flags in `tb/pp_top/sim_main.cpp`.
- Both sides' contracts stand:
  - C7's: the counters are the integrator's (02 §4.6, 06 §6.6, 07 F07.10, integrator
    guide §7.1), and 09 §8.6/§8.7 as `main` has them;
  - this PR's: the D3 amendment (07 §5.1, the channel maps the integrator's) and 09
    §8.2.
- The PR's RTL delta is line-identical on `main`, and the top's edits are comments.
  There is no port, parameter, register, census or capture change.
- Every ROM, regenerated from its generator at the base, both sides and the merge, is
  byte-identical (microcode, listener ROM, both descriptor images). Every mutation
  patch and substitution plant applies exactly once.
- `tb/pp_top` builds the bench five times, numbered the same everywhere it is
  described.

**Re-measured at the merge** (pinned Verilator 5.050):

| Gate | Result |
|---|---|
| `./scripts/run_suites.sh` | rc 0: 33 of 33 suites, 1,021,423 checks (`adp_engine` −39 and `pp_top` +28 from C7) |
| `./scripts/lint_hdl.sh`; `make check`; `gen_matrix.py --check` | rc 0 (41 modules; 1,114 links) |
| `tb/pp_top` | 10,390 checks = `main`'s 9,196 + this PR's 1,194; every section `main`'s or this PR's |
| `d3_mutants.py` | 110 of 110 KILLED, six goldens PASS |
| `notify_mutants.py` | 40 of 40 KILLED |
| `ctr_mutants.py` | 17 of 17 KILLED |
| `aecp_mutants.py` | 55 of 55 KILLED |
| `aecp_dispatch_mutants.py` | 37 of 37 KILLED |
| `acmp_mutants.py` | 19 of 19 KILLED |
| `gsi_mutants.py` | 20 of 20 caught by their named checks |
| name-write control | killed |
| `tb/adp_engine/mutants.py` | 30 of 30 KILLED |
| `tb/maap/mutants.py` | 27 of 27 KILLED |

Every control passes. Every failing-check count equals its README record but one.
`ident_burst_from_t0` fails 21, not 20: ID6d joins because the name stage's longer
D3 walk moves the identify burst's phase. `main` alone still fails 20, and the record
now says 21, with the reason.

Out-of-context cost at 1x1 against `main` `f4167536`:
- **38 names:** +705 LUT-eq and +92 FF, round 1's figures exactly.
- **39 names** (the parent's 1x1 shape at dev `bbf704ec`): +683 LUT-eq and +94 FF.
- Both are within the 750 / 400 names-stage ceiling.

**Parent consumer set at milan-fpga dev `bbf704ec`.**
- `parent-adoption-c8-cdf49d1a.patch` no longer applies there. Its `aem_assemble.py`
  hunk is not on dev; #629's clock-source table line moved the hunk's context. The
  re-based **`parent-adoption-c8-bbf704ec.patch`** keeps all 13 hunks, so no hunk
  dropped.
- `parent-adoption-p2-p1-1269cdaf.patch` applies after it unchanged.
- C7 needs no parent patch.
- Gates 1 to 15 pass.
- **Gate 16 (`milan_dp_render`) fails two checks**, T30 INTERNAL LAW, which dev's
  #634 added:
  - 227 of 292 PDUs at the 8-event fill setpoint;
  - 285 of 292 first events inside the law band.

  The processor at dev's pin, at `main` `ddb3119d` and at `main` `f4167536` passes,
  and this PR's head fails. With dev's own processor, moving only T30's feed start
  1,156 cycles later fails the same two checks; moving this PR's feed 927 cycles later
  passes. So the INTERNAL law depends on the feed's phase against the free-running
  INTERNAL grid, and the name stage's longer boot walk moves that phase. The lane
  stopped there for a decision:
  - (a) the parent makes the law phase-independent, and gate 16 is re-run;
  - (b) gate 16 is taken to review as a recorded parent finding.

**Round 1b, parent-visible.**
- At dev `bbf704ec` the parent builds 39 (1x1) and 107 (8x8) name entries, all within
  the writer's 128.
- The parent's census and capture grew with its own #629: 8x8 164 records, 13,210 B,
  13.86 ms of 24.5. This PR changes neither.
- Apply `parent-adoption-c8-bbf704ec.patch`, then the p2 successor.
- Gate 16 depends on the processor's boot length, as above.
