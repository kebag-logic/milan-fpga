[R663] NEGATIVE - exact head d30a208d44d5868cc356e6a8b7abc89b062ca9bd

Round R663-3: internal, cleared-context, independent review of PR #767 (issues #761 and #762).

- Head `d30a208d44d5868cc356e6a8b7abc89b062ca9bd`, tree `d203767adbab4025cbfb3f760540783f65cc2e6c`.
- Delta reviewed: `eef90b42..d30a208d`, three commits:
  - `cb65d9d7`: two RTL comments;
  - `336a6f6a`: the `[762-DP]` integrated case in `tb/verilator/milan_dp/sim_nxn.cpp`;
  - `d30a208d`: its README paragraph.
- No RTL logic changes. `git diff eef90b42..d30a208d -- hdl/` changes only two `//!` lines.
- Source base: dev `e9cbb676`. Live dev: `e26f1816`. Composing the PR with live dev is the manager's candidate duty.

All five lenses were applied at this head. The verdict is NEGATIVE because of one open MINOR, R663-3-F1, filed under Conformance, Robustness, Tests and Docs. The round-3 assignment asked for the integrated case "on a shipping datapath shape". The case runs on no elaboration of the shipping AX7101 shape (`endstation_ax7101_1x1_tdm8`). The PR body calls the retired Arty shape "shipping".

The wiring itself is correct on the shipping shape. I ran the case and the three planted wiring mutants on that geometry in a disposable probe. The clean build passes, and each mutant fails exactly the named `[762-DP]` checks (see F1). So the fix only has to add the shape to the committed bench; no logic change is needed.

## Method and independence

- **Reconstruction order:**
  1. AGENTS.md, then CONTRIBUTING.md (via AGENTS).
  2. The bodies of #761 and #762.
  3. The #762 scope ruling (issue comment 6260976223) and its extension (6265746720).
  4. The round-3 assignment (PR comment 6274405031).
  5. The round-3 diff and history.
  6. The harness, the Makefile legs, `sw/litex/build.sh` and `docs/integration/BUILDING.md`.
  7. The author's round-3 REVIEW READY (#761) and the live PR body.
  8. The published evidence at `afc1a1ac`, `review-evidence/761-r1/author-r3/`.
  9. The hosted check runs at the exact head.
- **Independence disclosure:**
  - The round-3 assignment quotes the substance of R663-2-F1, and I read it as instructed.
  - To find the author's round-3 handoff, I listed PR comments by time. That listing also printed the opening of R664-3 (comment 6275950683), including its F1 headline, before my verdict was written. This was not intended.
  - I had already established the shape facts F1 rests on from `tb/verilator/milan_dp/Makefile`, `sw/litex/build.sh` and `BUILDING.md`. My probe evidence and my conclusions are my own.
  - I did not read the rest of R664-3, its packet, or the author's HANDOFF.md.
  - I read R663-2 and R664-2 only after my pass over the diff, to settle their findings.
- **Execution:** no full bank was run.
  - I ran one disposable probe campaign: four Verilator builds and runs on the shipping AX7101 1x1 TDM8 geometry.
  - I spot-checked the author's published receipts against the evidence manifest digests.
  - I inspected the hosted check runs at the exact head.
  - The reviewed clone was never modified. Its HEAD, index, tree listing and the six submodule gitlinks were verified afterwards (`receipts/clone-integrity.log`).
  - Toolchain: Verilator 5.050 at the scoped pinned path (`receipts/verilator-identity.txt`).

## Findings

### R663-3-F1 MINOR: `[762-DP]` is not run on the shipping AX7101 datapath shape, and the PR calls a retired-board shape "shipping"

- **Lenses:** Conformance, Robustness, Tests, Docs.
- **Where:**
  - `tb/verilator/milan_dp/sim_nxn.cpp:6438` calls the case, which is defined at `:6653-6729`. The call sits in the broad flow, which runs only on these legs:
    - `obj_nxn`: `Makefile:605`, `endstation_arty_4x4`, N=4;
    - `obj_nxndv`: `:614`, a divergent copy of the Arty 4x4;
    - `obj_nxn8`: `:629`, `endstation_ax7101_8x8`, N=8, 2 wire channels, not the TDM8 master;
    - `obj_nxn4c`: `:645`, `endstation_arty_4x4`, N=4, 4 wire channels.
  - Two legs elaborate the shipping `SHAPE_AX1x1`: notify (`Makefile:309-312`) and dynmap (`:326-331`). Both `return` before the broad flow, at `sim_nxn.cpp:3031-3057`. The `obj_ax1x1` leg (`Makefile:244-249`) runs `sim_main.cpp`, not `sim_nxn.cpp`.
  - PR #767 body, Round 3 table, row `336a6f6a`: "(the shipping Arty shape `obj_nxn4c` among them)". The round-3 REVIEW READY on #761 says the same. Its mutant script header, `author-r3/receipts/r3-mutants/dp_stopped_mutants.sh`, says "the shipping Arty 4x4 shape".
- **Authority and evidence:**
  - The round-3 assignment (6274405031), item 1: "on a shipping datapath shape, STOP an AAF Stream Input ...".
  - The shipping shape is `endstation_ax7101_1x1_tdm8`:
    - `sw/litex/build.sh:195,378`: `cfg_ax7101`, "shipping bare-metal shape";
    - `docs/integration/BUILDING.md:94`: "the AX7101 ship shape";
    - `BUILDING.md:183`: "This is the shipping 1x1 TDM8 profile";
    - `tb/verilator/milan_dp/Makefile:62`: "THE SHAPE THE AX7101 ACTUALLY FLASHES".
  - The Arty is retired:
    - `BUILDING.md:95`: "a retired DUT";
    - `BUILDING.md:302`: "the retired bring-up recipe";
    - `BUILDING.md:442`: "The Arty is a retired DUT";
    - `sw/litex/build.sh:393-397`: "not built: the board is a retired DUT".
  - The AX7101 8x8 recipe "has never produced a bitstream" (`build.sh:382-385`).
  - So the four shapes that run the case are two retired-board shapes, a divergent copy of one of them, and a non-shipping AX7101 shape.
  - The configuration matters. On the shipping shape N_STREAMS=1 and the CRF Media Clock Input is ACMP sink 1 (`CRF_SNK_IDX_C`). So the wrong-vector form `acmpl_stopped_v_w[N_STREAMS:1]` feeds input 0 the CRF sink's stopped level there, and another AAF input's level on every leg that runs the case.
- **Reviewer probe** (`scripts/probe_762dp_ax1x1.sh`, `receipts/probe-ax1x1/`):
  - Setup:
    - Built from a byte copy of the head and the dynmap leg's own recipe: `SHAPE_AX1x1`, `-GTALKER_WIRE_CHANS_P=8 -GAUDIO_IF_SLOTS_P=8 -GAUDIO_IF_MASTER_P=1 -GLOOPBACK_P=1 -GI2SPB_P=0 -GLPF_P=0`, `NSTREAMS_TB=1`.
    - The one harness edit is in `receipts/probe-ax1x1/harness.diff`. It replaces the dynmap section call with the existing TRAP-1 bind, the 5.3.8.7 discard section and `[762-DP]`, unchanged.
  - Results:
    - Clean: 86 checks, 0 failures. All 13 `[762-DP]` lines pass (`clean.762dp.txt`).
    - Port tied to `'0`: fails exactly `[762-DP] 2 stopped gap: STREAM_INTERRUPTED +0` and `[762-DP] 3 stopped silence: STREAM_INTERRUPTED +0`, each got 1.
    - `acmpl_stopped_v_w[N_STREAMS:1]`, which is the CRF sink's level at N=1: fails the same two checks.
    - `acmpl_bound_v_w[N_STREAMS-1:0]`: fails exactly `[762-DP] 4 started gap: STREAM_INTERRUPTED +1`, got 0.
    - Each build takes about 37 s, so adding the shape to the bench is cheap.
- **Impact:**
  - The integrated grade of the `stopped_i` wiring is absent from the configuration the product ships and the one where #762 was observed (the AX7101, AAF input 0).
  - A shape-dependent regression at `milan_datapath.sv:6308` would pass every committed bench. For example, a slice that picks up the CRF sink's bit only at N=1.
  - The PR's claim that a shipping shape is covered is not true.
- **Required outcome:**
  - The committed bench runs the `[762-DP]` count-graded case on an elaboration of `endstation_ax7101_1x1_tdm8` with the shipping geometry. Any route works, for example the dynmap or notify recipe or the `obj_ax1x1` leg.
  - The port tie-off and at least one wrong-vector form, preferably the `[N_STREAMS:1]` form that selects the CRF sink at N=1, each fail a named `[762-DP]` check there. The clean leg passes.
  - The PR body and the mutant script header stop calling `obj_nxn4c` or the Arty 4x4 a shipping shape.
  - Alternatively, the manager publicly rules that the existing shapes satisfy "a shipping datapath shape". In that case the wording still has to be corrected.
- **Verification:**
  - The leg log shows the 13 `[762-DP]` lines on the AX 1x1 TDM8 elaboration.
  - The mutant receipts show each named failure on that same elaboration.
  - The PR text names the shapes accurately.

### R663-3-R1 RESIDUE: PR body status lines still cite the hosted run at `eef90b42`

- **Lenses:** Docs.
- **Where:** PR #767 body:
  - Status: "Hosted CI: every check run at `eef90b42` succeeded ... Hosted CI runs on them as they reach this PR."
  - Known limitations, the `act_ci.py --selftest` bullet: "it succeeded at `eef90b42`".
- **Why:** the head `d30a208d` is pushed and has a complete hosted run (`receipts/hosted-checks-d30a208d.tsv`). 63 check runs succeeded, among them `rtl-fast`, `verilator-suites`, `yosys-portability`, `docs-check`, `docs-gates-0/1/2`, `verilator-lint`, `yosys-elaboration` and `Union milan_dp`. `Physical gPTP (nightly and manual)` was skipped, not executed. This is wording only.
- **Exact fix:**
  - In Status, replace the first two bullets with: "Hosted CI: every check run at `d30a208d` succeeded, with the nightly physical gPTP job skipped. That includes `rtl-fast`, `verilator-suites`, `yosys-portability`, `docs-check`, `docs-gates-0/1/2`, `verilator-lint` and `yosys-elaboration`."
  - Keep the round-3 commit summary as its own bullet, without "Hosted CI runs on them as they reach this PR".
  - In Known limitations, change "it succeeded at `eef90b42`" to "it succeeded at `d30a208d`".

### R663-3-S1 SUGGESTION: `[762-DP]` grades only bit 0 of the `stopped_i` vector

- **Lenses:** Tests, Robustness.
- **Where:** `tb/verilator/milan_dp/sim_nxn.cpp:6675-6729`. Every STOP, gap and silence is on AAF Stream Input 0.
- **Why:**
  - On the multi-stream legs, a wiring defect that gets bit 0 right and the others wrong would pass every `[762-DP]` check. Examples are input 0's level replicated (`{N_STREAMS{acmpl_stopped_v_w[0]}}`) or only bit 0 connected.
  - This is established by reading only. My disposable `obj_nxn4c` probe for it (`scripts/probe_762dp_replicate_nxn4c.sh`) did not reach the build: the probe tree lacked the pinned submodule gitlinks that the leg's `stack-pin` prerequisite requires.
  - On the shipping N=1 shape the defect class cannot arise. That is why this is a suggestion.
- **Suggested change:** on a leg with N >= 2 and AAF input 1 bound, add these two checks to the case:
  - with input 1 stopped and input 0 started, a gap on input 1 counts +0;
  - a gap on input 0 still counts +1.
- **Verification:** the replicate plant fails the input-1 check; the clean leg passes.

## Prior findings at this head

| Finding | Status at d30a208d | Evidence |
|---|---|---|
| R663-2-F1 MINOR (Tests): datapath `stopped_i` wiring graded by no bench | **Partly resolved; the remainder is retained as R663-3-F1** | See note 1. |
| R663-2-F2 RESIDUE: port comments said only "silence" | **Resolved** | `KL_avtp_rx_monitor_ctx.sv:152` and `milan_datapath.sv:6307` now carry R663-2's exact text, word for word (`cb65d9d7`). |
| R663-2-F3 RESIDUE: stale PR status lines | **Resolved** | See note 2. |
| R663-2-S1 SUGGESTION (CRF STOP at the timeout edges) | Retained, optional | Not assigned; `crf_rx` is not touched by the delta. |
| R663-1-S1 SUGGESTION | Retained, optional | Not touched by the delta. |
| R663-1-F1, R663-1-F2, R663-1-F3; R664-1-F1, R664-1-F2 | **Resolved** (as at `eef90b42`) | The delta touches none of their logic or harnesses. The only RTL change is two comments. |
| R664-2-R1 RESIDUE ("the head is not pushed") | **Resolved** | The sentence is gone from Known limitations. |
| R664-2-S2 SUGGESTION (paired CRF unit plants) | Retained, optional | `tb/verilator/crf_rx` is not touched by the delta. |

1. **R663-2-F1.** What is resolved:
   - The integrated case exists. STOP_STREAMING and START_STREAMING arrive over the wire as AECP, and every count is read through `GET_COUNTERS(STREAM_INPUT,0)` with `ctr_word` (`sim_nxn.cpp:4911`). The word indices are MEDIA_LOCKED 0, MEDIA_UNLOCKED 1, STREAM_INTERRUPTED 2 and SEQ_NUM_MISMATCH 3, matching Milan Table 5.6 and the bench's existing reads.
   - The case shows all four required facts:
     - a stopped gap: SEQ_NUM_MISMATCH +1, STREAM_INTERRUPTED +0;
     - a stopped silence that expires: MEDIA_UNLOCKED +1, STREAM_INTERRUPTED +0;
     - liveness, through those two moving counters;
     - after START, a relock (MEDIA_LOCKED +1) and a gap that counts STREAM_INTERRUPTED +1.
   - The watchdog skip is safe:
     - it is guarded to only shorten the silence (`:6705-6708`);
     - expiry needs `sil_ms_r >= UNLOCK_MS_C-1` on a 1 ms tick (`KL_avtp_rx_monitor_ctx.sv:902-913`), so from 97 it expires inside the 4 ms that are run for real;
     - the "silence unlocked it" check confirms the expiry.
   - The planted mutants at `:6308` each fail a named check:
     - in the author's `obj_nxn4c` receipts, which match the manifest digests (`receipts/author-digest-check.log`);
     - in my shipping-shape probe.
   - Not met: the case runs on no shipping datapath shape, as the assignment required. This is F1.
2. **R663-2-F3.** "not pushed" is dropped, and the roles name `[R663]` (internal) and `[R664]` (external). The status points to the hosted checks; the pointer has since gone stale, which is R663-3-R1.
3. **R664-3-F1.** Read after my verdict, apart from the opening disclosed above. It has the same cause as R663-3-F1. I concur, and my shipping-shape probe adds that the wiring itself behaves correctly there.

## Comment-rule check (owner 2026-10-15)

The delta's new source comments contain no bench lane label, lane name, review round, reviewer ID or issue-comment ID:
- the two `//!` port comments;
- the `[762-DP]` block comment and its inline comments in `sim_nxn.cpp:6653-6729`.

`[762-DP]` and `[CTRS-CRF]` are check-name tags used by the harness's own output, not lane labels. No new RESIDUE instance.

## Lens results

- `[R663] PASS RTL - hdl/milan/milan_datapath.sv:6283,6307-6308,5392; hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:152,902-913; git diff eef90b42..d30a208d -- hdl/ - checked that the delta changes only two //! comment lines and no logic, and that the stopped vector feeding the monitor is the one the accept gate (:6283) and clock meter (:5952) use, width-generic in N_STREAMS. The wiring behaves correctly on the shipping AX 1x1 TDM8 elaboration: receipts/probe-ax1x1/clean.762dp.txt passes; tie0, sink1 and bound each fail only their named checks.`
- Conformance: **UNCLEAN** (R663-3-F1).
  - Examined: the round-3 assignment items 1-4 against `sim_nxn.cpp:6653-6729`, the four broad legs' shapes and the PR body.
  - Milan v1.2 5.3.8.7, 5.4.2.19, 5.4.2.20 and 5.3.8.10 Table 5.6: the count semantics of the case are correct.
  - The "shipping datapath shape" requirement is not met.
- Robustness: **UNCLEAN** (R663-3-F1).
  - Examined: configuration-dependent behaviour of the `stopped_i` slice at N=1, where the CRF sink is index 1, against N=4/8. The shipping-shape probe passes.
  - The committed bench does not cover the shipping shape.
  - S1 records the bit-0-only grading.
- Tests: **UNCLEAN** (R663-3-F1).
  - Examined: the `[762-DP]` liveness and count oracles, the watchdog skip guard, the author mutant receipts (digest-verified), and my four-build shipping-shape mutant probe.
  - Each test can fail for its defect, but the committed bench lacks the shipping shape.
- Docs: **UNCLEAN** (R663-3-F1).
  - Examined: `tb/verilator/milan_dp/README.md:1188-1200`, which is accurate ("every broad `sim_nxn` leg"); the PR body's Round 3 table and Status; and the REVIEW READY.
  - The PR body calls the retired Arty shape "shipping". R663-3-R1 is wording only.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | round-3 assignment; `sim_nxn.cpp:6653-6729`; Makefile legs `:244,309-331,605-645`; `build.sh:195,378-397`; `BUILDING.md:94-95,183,302,442`; PR body | none at this head (open R663-3-F1) | d30a208d44d5868cc356e6a8b7abc89b062ca9bd |
| RTL | CLEAN | `milan_datapath.sv:5392,5952,6283,6307-6308`; `KL_avtp_rx_monitor_ctx.sv:152,902-913`; hdl diff `eef90b42..d30a208d`; shipping-shape probe receipts | R663-3 | d30a208d44d5868cc356e6a8b7abc89b062ca9bd |
| Robustness | UNCLEAN | N=1 vs N=4/8 slice semantics; `CRF_SNK_IDX_C`; shipping-shape probe; bit-0-only grading (S1) | none at this head (open R663-3-F1) | d30a208d44d5868cc356e6a8b7abc89b062ca9bd |
| Tests | UNCLEAN | `[762-DP]` oracles; author `r3-mutants` and `r3-focused` receipts (digest-verified); `receipts/probe-ax1x1/*`; hosted `Union milan_dp` at head | none at this head (open R663-3-F1) | d30a208d44d5868cc356e6a8b7abc89b062ca9bd |
| Docs | UNCLEAN | `tb/verilator/milan_dp/README.md:1188-1200`; PR body (live, `receipts/pr767-body-live.md`); REVIEW READY on #761; the two port comments | none at this head (open R663-3-F1) | d30a208d44d5868cc356e6a8b7abc89b062ca9bd |

## Real limits

- **Hosted evidence:** inspected only, not accepted.
  - At `d30a208d`, 63 check runs completed with `success`, including `rtl-fast`, `verilator-suites`, `yosys-portability`, `docs-check`, `docs-gates-0/1/2` and `Union milan_dp`.
  - `Physical gPTP (nightly and manual)` was skipped, not executed.
  - Hosted and act acceptance is the manager's.
- **No manager source bank** runs at this head, and none is claimed or inferred. Source-head execution evidence is the author's published receipts.
- **Unsigned evidence:**
  - The evidence commit `afc1a1ac` is unsigned (`verification.verified=false`, reason `unsigned`), and no detached signature was found.
  - What was verified is digest identity: 12 spot-checked `author-r3` receipts match `MANIFEST.json` `published_sha256`. The manifest's own digest is in `receipts/evidence-manifest.sha256`.
  - Digest identity is not an execution attestation.
- **Not re-run:** I did not re-run the full `milan_dp` sweep, `avtp_rxmon`, the docs gates, the builder bank, Yosys or route-1x1. The delta changes no RTL logic, so route-1x1 is not required by the assignment.
- **S1 not executed:** the S1 replicate-bit probe did not run, because its disposable tree could not satisfy the `stack-pin` prerequisite. S1 rests on reading.
- **No hardware proof:** physical calibration is NOT RUN. Field skips, simulation and routing are not hardware proof.
- **Redacted logs:** the probe build logs are published in redacted form (`*.build.redacted.log`), with host toolchain and packet paths replaced by placeholders. The raw build logs stay unpublished.

## Pending manager duties

- Carry R663-3-R1 to the residue checklist.
- After F1 is addressed, build and validate the current-dev merge candidate:
  - source base `e9cbb676`;
  - live dev `e26f1816`;
  - builder and native banks;
  - link the receipts on the PR.
- Own hosted and act acceptance at the final head.
- Publish this report and the files listed in `MANIFEST.sha256`.

R663-3 FINISHED
