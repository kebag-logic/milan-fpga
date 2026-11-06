[R779] NEGATIVE - exact head cc92e90a95376151a9ebd484c429bc53feb8573c

# R779-1 independent review: processor PR #215, issue #214

Head `cc92e90a95376151a9ebd484c429bc53feb8573c`, tree `4bffe18ed6a77686aad76d7fbef49316f42f7379`. Source base `a9e84b66`; the issue's own delta is `92100657..cc92e90a`, because `92100657` (PR #213) is merged in.

## Verdict

**The fix is correct, and I found no defect in the RTL.** The verdict is NEGATIVE only because of two MINOR test gaps. Each gap is a fault planted in the new encoder logic that no repository suite detects. Neither gap needs an RTL change.

| Question from the brief | Answer | Evidence |
|---|---|---|
| Can a doubled Domain or VID vector occur after a LeaveAll? | No failure found | 241,560 MRPDUs from randomized runs at six table depths: 0 doubled. `tb/srp_top` at head: OV0 to OV10 pass |
| Is an attribute event lost by merging? | No failure found | The same runs compared every MRPDU, value by value, with an independent reference of the 10 §3 merge table: 0 mismatches over 272,764 merges |
| Is the defect reproduced at base? | Yes, matching the PR's figures | Base encoder with the head testbench: `8683 checks: 8675 PASS, 8 FAIL`, 69 of 17,650 MRPDUs doubled |
| Is PR #213 listener and talker behaviour unchanged? | Yes | Listener and talker RTL are byte-identical to main. Wire comparison below |
| Is the 802.1Q-2022 clause 10 encoding cited correctly? | Yes | Each cited clause read in the 2022 text; see Conformance |
| Is the interpreter evidence sound? | Yes | See "Interpreter evidence" |

## Findings

### F-1 MINOR: nothing grades that one application's search leaves the other application's drain alone

- **Lenses:** Tests.
- **Where:** `hdl/srp/KL_srp_encoder.sv:460-461` (the `ev_app_i == APP_MSRP_C` term of `msrp_raddr_w`), stated at `hdl/srp/KL_srp_encoder.sv:425-426`. The rows are `tb/srp_encoder/sim_main.cpp` PV1 to PV12 and `tb/srp_top/sim_main.cpp` OV0 to OV10.
- **Authority:** issue #214 acceptance 1 (each value at most once per MRPDU) and 10 §3, which says the search uses the table's own read port while that application does not drain.
- **Evidence:** probe `rv-search-steals-other-read` removes that term, so an MVRP search takes the MSRP read port during an MSRP drain.
  - The probe passes all four suites that elaborate the encoder: `tb/srp_encoder` 692 of 692, `tb/srp_top` 8683 of 8683, `tb/pp_top` 11064 of 11064, `tb/srp_admission` 991231 of 991231.
  - The randomized check catches it at once: 189 doubled values and 351 mismatches in 300,000 clocks.
  - The opposite probe, `rv-search-steals-other-read-mvrp`, is caught only by OV0, in 1 of 8683 checks. No directed row grades it, and it passes the `onevec` group.
- **Impact:** the RTL at head is correct. A later edit that breaks this one term would bring back the issue's symptom, a value twice in one MRPDU, and every gate would stay green.
- **Required outcome:** add a row that offers a value of one application, with that application's table non-empty, while the other application drains, in both directions. Add a planted arm that fails the row by name.
- **Verification:** `python3 scripts/probes.py <tree> <out> rv-search-steals-other-read`, then run the new row. It must fail by name. Add the arm to `tb/srp_top/mutants.py` and to the 09 §8.14 table.

### F-2 MINOR: the value identity width and the newer FirstValue rule have no check

- **Lenses:** Tests.
- **Where:** `hdl/srp/KL_srp_encoder.sv:205-210` (`key_f`) and `hdl/srp/KL_srp_encoder.sv:483-488` (`ev_value_i` written on a hit).
- **Authority:** the banner of `key_f` and 10 §3 define the identity as the first eight octets of FirstValue. The PR's "For review" section states that two Talker values with one StreamID merge to the newer one (802.1Q-2022 35.2.2.8).
- **Evidence:** two probes pass the same four suites with the same counts as F-1.
  - `rv-key-low-mac-ignored` leaves StreamID octet 0 out of the identity. Two distinct streams that differ only there merge, so one declaration is lost. The randomized check reports 141 mismatches.
  - `rv-merge-keeps-old-value` keeps the older FirstValue on a hit. The randomized check reports 43 mismatches.
  - The neighbouring identity probes are caught: `rv-key-mac-only` and `rv-key-uid-only`.
- **Impact:** the RTL at head is correct. However, the identity decides whether a merge can lose an attribute event, and part of it is unchecked. The disclosed Talker behaviour has no test.
- **Required outcome:** add a row with two StreamIDs that differ only in the top MAC octet, which must stay two values. Add a row with two Talker values of one StreamID and different later fields, which must carry the newer one. Plant an arm under each.
- **Verification:** both probes above must fail the new rows by name.

### R-1 RESIDUE: PR body overstates byte identity

- **Lenses:** Docs.
- **Where:** PR #215 body, "Its module header, parameters and ports, is byte-identical to main's."
- **Evidence:** parameters, port names and widths are identical. The comment on `ev_ready_o` differs (`hdl/srp/KL_srp_encoder.sv:101`), and the file banner differs.
- **Impact:** wording only. No interface changes.
- **Exact fix:** "Its parameters and port declarations are unchanged; only the comment on `ev_ready_o` and the file banner differ."

### R-2 RESIDUE: banner still calls the drain the only reader

- **Lenses:** Docs.
- **Where:** `hdl/srp/KL_srp_encoder.sv:76-77`, "(push is the only writer, the drain walk the only reader)". The next sentence adds the search as a second user of the read port.
- **Impact:** wording only.
- **Exact fix:** "(push is the only writer; the drain walk and the value search share the one read port)".

### R-3 RESIDUE: new source comment shows a bench run label

- **Lenses:** Docs.
- **Where:** `tb/srp_top/sim_main.cpp:3422`, "(Run B, 10 §6.5)". This is the one instance in the reviewed delta; older instances are tracked by #746.
- **Authority:** owner comment rule of 2026-10-15.
- **Exact fix:** "(10 §6.5)".

### S-1 SUGGESTION: state the clean search restart after an accept

`rv-sr-on-survives-accept` keeps the search running after an accept. It passes `tb/srp_encoder` and `tb/srp_top`, and the randomized check catches it. It needs the same value offered on the clock straight after its accept, and I found no assembled producer that does this, so it is not a finding. A back-to-back row in `tb/srp_encoder` would close it.

### S-2 SUGGESTION: put the area in the repository

Acceptance 3 is met by the PR table and the receipts. 10 §5.1 records the issue #212 area in the document itself, and issue #214 could do the same. I reproduced the encoder's flip-flop figure independently: 1280 to 1358.

## Interpreter evidence

**Judgement: sound.** The cited gates are either proven to have run on the pinned interpreter or were re-run with an assertion.

- **Cause:** the manager's PR comment explains the lost virtual environment, and the published note is consistent with it.
- **Discarded set:** 14 gates, confirmed from the records. 13 finished, and `fw_verilator` started but never ended after `fw_boundary` failed with rc 2.
- **Re-run set:** 16 gates, those 14 plus `milan_dp_mclk` and `milan_dp_render`, which the first attempt never reached. All 16 are rc 0, each with `before` and `after` records of the pinned venv at 3.12.3. `parent-rerun.sh` turns a mismatch into rc 97.
- **Gates kept from before the loss:** 27, all ended by 12:25:48 UTC.
  - 26 of them ended by 11:53:57 UTC, before the last 3.12 bytecode write at 12:01:01 UTC, so the venv was still in use after they finished.
  - `fw_shard3_srp` ran past that time. It imports parent modules, and no 3.14 bytecode appears until 13:18:13 UTC.
- **Count:** 27 + 16 = 43 gates, matching the PR.
- **Limit:** the bytecode timestamps are the author's statement. The raw listing is not published, and the tree was cleaned.

`check_cpp_idiom.py` passed in the published receipt with every rule at 0. I applied its rules from live dev `87e9d03a` to the four C++ files this range touches, and all rules read 0. That was not a run of the full gate.

## Lens evidence

### Conformance: CLEAN

- 802.1Q-2022 text read for 10.7.5.13 c), 10.7.6.1 to 10.7.6.5, 10.7.6.12, 10.7.7, Table 10-3, 10.8.2.10.1, 11.2.3.1.7, 35.2.2.7.2 and 35.2.2.8. The file hash matches the author's recorded hash.
- Each merge row agrees with Table 10-3: VN stays VN on Join!, periodic! and rLA!; LA with Join! is AA; LA with New! is VN; VN, AN, AA and QA with Lv! are LA. "A later s replaces only an s" follows 10.7.6.5.
- Two Talker values of one StreamID with different FirstValues can merge and drop an Lv of the old value. 35.2.2.8 already forbids that change without two LeaveAllTime periods, so it is not a new violation.
- Talker Advertise, Talker Failed and Listener of one StreamID stay separate values, which agrees with 10.7.5.13 b).

### RTL: CLEAN

- Read the whole encoder, and traced `KL_srp_domain`, `KL_srp_vlan`, both walks and the intake mux.
- The search is correct across its cases: first read, hit on the last entry, restart on a changed offer, drain start, and a full table.
- All producers assert valid first, so `ev_ready_o` now being low without an offer deadlocks nothing, and there is no combinational loop.
- The 10 §3 figure holds by trace: at 2x2 the drain starts five clocks after tx!, so two pending entries still admit the Domain re-join and a third defers it. The product's 1x1 binds two of each, so 2x2 is the smallest shape.

### Robustness: CLEAN

- The randomized check ran 36 seeds at depths 2, 3, 4, 5, 8 and 12 and three offer densities, with re-arbitration, withdrawn offers, unknown types, TX and allocation backpressure, LeaveAll and cancelled own rounds.
- Result: 1,070,990 pushes, 0 doubled, 0 mismatches.
- It caught 26 of 27 planted faults, including all seven author merge arms it was given. The other one, `rv-search-ignores-start`, behaved the same as head in that run.
- The longest push stall was 5808 clocks at head and 5187 at base, in a smaller base sample. Both come from the check's own backpressure, and no run deadlocked.

### Tests: UNCLEAN (F-1, F-2)

- At head: `tb/srp_encoder` 692 of 692, `tb/srp_top` 8683 of 8683.
- At base, with the head testbench: `tb/srp_encoder` 644 PASS and 48 FAIL, `tb/srp_top` 8675 PASS and 8 FAIL (OV0 to OV7). Every other check has the same outcome.
- OV rows are not vacuous: each one also requires its stimulus to have happened.
- Eleven author arms ran through the repository's driver: `20 checks: 20 PASS` (controls and named kills), including `second-queueing` on OV1 and PV1. The re-pointed arms also hold: `listener-settle-compare-dropped` on SW2, `listener-settle-skips-leave-copies` on SW4, and `listener-shares-nothing-encoder-appends` on SW1.
- 20 reviewer probes: 14 killed by `tb/srp_encoder`, 1 by OV0, 4 survive every suite run on them, and 1 behaved the same as head.

### Docs: CLEAN (R-1 to R-3 recorded)

- Checked against my own runs: the base and head figures in both READMEs, the PR's campaign arithmetic (20 controls + 270 arms + coverage = 291; coverage 174), and 09 §8.14.
- Comment rule scan over the full diff found only R-3. Words such as "LeaveAll lane" are protocol terms, not bench labels.
- `git diff --check` is clean.
- The 28 per-arm README counts were not re-derived; the brief and `HANDOFF.md` place them at the base.

### PR #213 behaviour: wire comparison

`KL_srp_listener_fsm.sv`, `KL_srp_talker_fsm.sv` and `tb/srp_stream_fsms/` are byte-identical to main. Frames from `tb/srp_top` at head and at the base encoder:

| Group | Frames | Result |
|---|---|---|
| `link` | 7 | identical in bytes and time |
| `domjoin` | 6 | identical in bytes and time |
| `share` | 90 | identical except frames 55 and 73, and the frame after each |

Frames 55 and 73 are the defect itself: base carries VID 2 as Lv and New in one MVRP MRPDU, and head carries New once (LA with New! is VN). The frame after each has identical bytes and leaves 1 ms earlier.

## Prior public findings

None to resolve. At this head PR #215 has no reviews and no review comments, and its two comments are manager notes.

## Ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 802.1Q-2022 clauses above, merge table, encoder identity | R779-1 | `cc92e90a95376151a9ebd484c429bc53feb8573c` |
| RTL | CLEAN | `KL_srp_encoder.sv`, Domain, VLAN, walks, intake mux, merge commit | R779-1 | `cc92e90a95376151a9ebd484c429bc53feb8573c` |
| Robustness | CLEAN | randomized check, 36 seeds at six depths; backpressure and own-round paths | R779-1 | `cc92e90a95376151a9ebd484c429bc53feb8573c` |
| Tests | UNCLEAN | PV and OV rows, base reproduction, 11 author arms, 20 reviewer probes | R779-1 | `cc92e90a95376151a9ebd484c429bc53feb8573c` |
| Docs | CLEAN | 09 §8.14, 10 §3 and §5.1, both READMEs, PR body, comment rule | R779-1 | `cc92e90a95376151a9ebd484c429bc53feb8573c` |

## Real limits

- **Timing was not measured.** No Vivado is available here, and the PR records area only. The new path runs from the offered value through the key compare to `ev_ready_o`, the read address and the RAM write. A generic 6-LUT mapping of the encoder alone gives depth 12 at both main and head, but that leaves out the intake mux of `KL_srp_top` and is not a timing result.
- **The parent gates were not re-run.** Their results are the author's published receipts, at a scratch parent `fff0311097` that is not public. The `milan_dp`, `pp_shadow` and `behave` logs are published as hashes only, so their tallies come from the gate table.
- **The full campaigns were not re-run.** I ran 11 of 243 SRP arms, and took the 291 of 291 total and the other 16 campaigns from receipts.
- `tb/srp_stream_fsms` was not run, because it does not elaborate the encoder and is byte-identical to main.
- The randomized check drives the encoder alone, not the assembled top.
- Physical calibration was NOT RUN, and no hardware was used. Field skips are not hardware proof.

## Pending manager duties

- Validate the current-dev merge candidate at the merge turn (source base `a9e84b66`, live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`), including builder timing for the path above and the ROM digests for the real gitlink.
- Accept the hosted runs. At review time `docs-gates` and `portability` had succeeded and `suites` was still in progress.
- Carry R-1 to R-3 to the residue checklist.

## Receipts

`receipts/` holds the raw results and `scripts/` the portable probes, all listed in `MANIFEST.sha256`. All probes ran in disposable copies. One logic-depth run left a stray untracked `abc.history` in the clone, which I removed. At the end HEAD, tree, index and working tree match the exact head with nothing untracked, and the repository has no submodule gitlinks.

R779-1 FINISHED
