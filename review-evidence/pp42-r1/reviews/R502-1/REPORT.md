[R502] NEGATIVE - exact head 72facc6d48807808e4d97a454a0ecceb2769ac9e

# R502-1: internal independent review of processor PR #164 (Closes #42)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #164, branch `pp42-domain-notify`.
- Exact head `72facc6d48807808e4d97a454a0ecceb2769ac9e`, tree `3274eac801f2ebb6b96ca031c12752a2a1b91bcc`;
  base `main` `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8`. Three commits (`bc74bc3`, `5cd4082`, `72facc6`), 5 files, +297 -12.
- Assignment: issue #42 comment 6008771904. Review start: PR #164 comment 6011230562.
- Scope as reviewed: test only. `git diff e6a759de..72facc6d` touches `tb/pp_top/{notify_phases.hpp, sim_main.cpp,
  notify_mutants.py, README.md}` and `docs/architecture/09_verification.md`. Nothing under `hdl/`, `syn/` or `scripts/`
  changes, and no port, register or parameter changes.

## Verdict

NEGATIVE, for one open MINOR (F1). Every acceptance item of #42 and every assignment item is met at this head, and I
reproduced each of them: section DN passes, its nine controls are KILLED on exactly the checks the README lists, the full
pp_top count moves 10,444 to 10,459 and nothing else moves, and every existing arm still plants. F1 is about two
timing statements. The README (and the PR body and a bench comment) states two figures about the bench's stimulus
timing that the bench does not have. Because they are figures, the owner rule does not let them count as wording-only
RESIDUE.

## How the review was reconstructed

1. Guidance: this repository has no `AGENTS.md` or `CONTRIBUTING.md` (checked with `git ls-files`). The governing
   conventions are `README.md`, `docs/README.md` (ID registries, single-source rules, and what `make check` enforces)
   and `docs/guides/hdl-engineer.md` for the bench conventions.
2. Scope: the issue #42 body (REQ-NET-002, acceptance 1-4, GAP-04 link) and the manager's lane comment 6008771904
   (items 1-6, STOP conditions, gates). The issue thread has no other scope decision. PR #164 body.
3. Authorities: `docs/00_MILAN_COMPLIANCE_REVIEW.md` REQ-NET-002 / REQ-SRP-004. `docs/architecture/06_aecp_engine.md` §6.10
   (the face answer) and §7 (trigger classes; `T-CTR-NOTIF` limits GET_COUNTERS only, `:1011`, `:1025`).
   `08_timing.md` F08.1 (`T-CTR-NOTIF` 1 s, `T-NOTIF-MONITOR` 30-60 s). `02_interfaces.md:509,532` (DOMAIN_CHANGE consumers).
   RTL as the landed contract: `hdl/top/protocol_processor_top.sv:3178-3181,4018-4020` and
   `hdl/srp/KL_srp_domain.sv:143-145,155-157,173-184`; `hdl/aecp/KL_aecp_notify.sv:666-668,1073,1311`.
4. The diff and history `e6a759de..72facc6d`, read in full.
5. Executable evidence: the manager's public evidence `kebag-logic/milan-fpga@355c335c:review-evidence/pp42-r1`
   (MANIFEST.json, the published handoff, PR body and 148 patch). The exact-head hosted checks (snapshot below). My own
   runs (receipts below).

## Findings

### F1 - MINOR - lenses: Tests, Docs - two stated timing figures of section DN are not what the bench does

- **Where:** `tb/pp_top/README.md:2506-2507` ("Each stimulus comes at least 1,000 ms (100,000 clocks) after the latest
  frame to A left"), `tb/pp_top/README.md:2497` ("Each notification leaves ... 495 after the MRPDU's last byte"),
  `tb/pp_top/notify_phases.hpp:1663` (`last_sent = 0; //!< the clock the latest frame to A left`). The same two
  statements appear in the PR body (item 6 row: "each stimulus comes at least 1,000 ms after the latest frame to A left")
  and in the published handoff ("each Domain's 495 after the MRPDU's last byte").
- **Evidence:** `receipts/probe_timing_statements.log` comes from a head copy with print-only instrumentation
  (`receipts/probe_timing_statements.patch`). The run's graded result is unchanged: 15 checks, 0 failures.
  1. `last_sent` starts at 0 and only `watch()` updates it (`notify_phases.hpp:1701`). So the REGISTER response that
     `register_controller` waits for is not counted. The response to A left at clock 3,464, and `space_out()` dropped
     `link_up_i` at clock 100,000. That is 96,536 clocks, about 965 ms, after the latest frame to A, not at least
     1,000 ms. The first stimulus is timed from clock 0, not from any frame.
  2. For the two notifying MRPDU stimuli, `t0` is taken after `feed()` returns (`notify_phases.hpp:1756,1773`), and
     `feed()` clocks 4 idle cycles after the last byte (`:93`). The probe shows `t0` 4 clocks after the last byte for
     every MRPDU, so each Domain notification leaves 495 clocks after `t0`, which is 499 clocks after the MRPDU's last
     byte. The link-edge figure (466 clocks after the edge) is right.
- **Impact:** no acceptance item changes. GET_AVB_INFO has no rate limit (06 §7), the REGISTER response is solicited
  rather than a notification, and the code comment at `:1653-1655` ("after the latest notification left") is accurate.
  But the README record of the section, and the PR's evidence for item 6, state numbers about the test that a reader
  cannot reproduce. Item 6 asks the bench to "wait out its spacing". The bench does that between notifications only,
  which is all the requirement needs, but the record claims more than that.
- **Required outcome:** make the record and the bench agree, in either of two ways.
  - Restate the figures: "at least 1,000 ms after the latest notification to A; the first stimulus comes at clock
    100,000, 965 ms after the REGISTER response", and "495 clocks after the MRPDU's stimulus point (4 clocks after its
    last byte), so 499 after the last byte". Fix the `last_sent` comment to match.
  - Or change the bench: seed `last_sent` from the REGISTER response and take `t0` at the last byte, then re-measure.
  Either way, update the PR body's item 6 row to match.
- **Verification:** re-run `receipts/probe_timing_statements.patch` (print-only) against the new head. The printed gaps
  must match the README's figures, and `--domain-notify-only` must still give 15 checks, 0 failures.

### S1 - SUGGESTION - lens: Tests - the last window has no trailing quiet check

The DN windows are contiguous. A late duplicate after any notifying step lands in the next step's window and turns it
red. Only frames after DN3b's 1.2 s window are never examined. A final quiet interval, for example one more `watch()`
with an empty-result check, would close that tail. It does not affect the acceptance.

### S2 - SUGGESTION - lens: Tests - the ADOPTED LINK_DOWN edge could still be graded for "exactly one"

The README is right that the LINK_DOWN revert (`KL_srp_domain.sv:157`) cannot be told apart from the link term at
`ev_avb_i`. My probe `r_EXPECT_SURVIVE_revert_no_strobe` confirms it: deleting that strobe survives DN, which the README
states. A link down from ADOPTED still raises both terms one clock apart. A check that this yields exactly one
GET_AVB_INFO would grade the coalescing of the two terms. That is optional and outside #42's acceptance.

No BLOCKER or MAJOR. No RESIDUE.

## Acceptance trace (each item reproduced at the exact head)

| Item | Check(s) | Reviewer evidence | Result |
|---|---|---|---|
| #42-1 / lane 1: with A registered, a differing Class A Domain gives exactly one u=1 GET_AVB_INFO for AVB_INTERFACE 0, byte-exact, no GET_AS_PATH | <bench-switch-model> (premise), DN1b, DN1c (`sequence_id` 2) | `dn_only_head.log`, `pp_top_full_head.log`: pass. The expected frame follows IEEE 1722.1 GET_AVB_INFO offsets 24-44 and Milan 5.4.5.1's per-entry sequence. `asp_takes_domain` kills DN1b and DN2b | met |
| lane 2: the declaration back to the default gives exactly one more | DN2 (premise), DN2b, DN2c (`sequence_id` 3) | pass. The strobe comes from the adoption arm `:184`, as the README states. `adopted` stays 1 (`[i]` line) | met |
| #42-2 / lane 3: an identical re-declaration sends nothing | DN3 ({3,5} again), DN3b ({3,2} again) | pass. `domain_same_readopted` kills both | met |
| #42-4 / lane 4: the link-edge leg of the OR | DN4b-DN4e, DN4 (premise: at DEFAULTS, no DOMAIN_CHANGE) | pass. My `r_link_rise_only`, `r_link_fall_only` and `r_link_level_down` are each killed on the edge they break (level: 287 frames) | met |
| #42-3 / lane 5: removing `srp_evt_domain_change_w` from `ev_avb_i` turns items 1 and 2 red; every new check has a control; every existing arm still plants | 9 controls | `notify_mutants_head_results.json`: `avb_domain_term_dropped` fails DN1b, DN1c, DN2b and DN2c, rc 1. All 9 KILLED on exactly the README's failing sets, and every one of the 15 checks is named by at least one control. 65 of 65 KILLED, 8 goldens PASS. `plant_check_{base,head}.log`: 368 of 368 arms plant at base and 377 of 377 at head (the 368 plus the 9), with no refusal | met |
| lane 6: rate limit respected, not weakened | no RTL change; the bench waits 1 s after each notification | 06 §7 defines only `T-CTR-NOTIF` (GET_COUNTERS). GET_AVB_INFO is one pending bit (`KL_aecp_notify.sv:1073,1311`). The diff has no `hdl/` change | met (see F1 for how the record describes it) |
| STOP: only the pp_top count moves | | `pp_top_graded_base_vs_head.diff`: base 10,444 to head 10,459, first build 9,956 to 9,971. The only other lines are DN's seven. No other suite compiles a changed file (`#else` path of `main` only, `sim_main.cpp:14034-14085`) | met |

My probes (`scripts/r502_probes.py`, graded by the tree's own `judge()`): six killed, and the one probe expected to survive did survive. That survivor documents the stated `:157` limit.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Milan 5.3.6.2/Table 5.22 trigger set as recorded in 00 REQ-NET-002 and the top's `ev_avb_i` comment. IEEE 1722.1 GET_AVB_INFO response layout against `avb_info()` (offsets 24/26/28/36/44, u bit, SUCCESS, cdl from length). Milan 5.4.5.1 per-entry `sequence_id` (0-3 on the wire). 802.1Q Domain vector shape {5,2,VID}x2 covering class A {6,3,VID}. 06 §6.10 (body is the face's) and §7 (rate limit) | R502-1 | 72facc6d48807808e4d97a454a0ecceb2769ac9e |
| RTL | CLEAN | diffstat: no `hdl/`, `syn/` or `scripts/` change, so no ports, parameters or registers move. The RTL the controls plant into (`protocol_processor_top.sv:4018-4020,3178-3181`, `KL_srp_domain.sv:143-184`, `KL_aecp_notify.sv:666-668`, `restore_done_o`) is unchanged, and each planted text occurs exactly once | R502-1 | 72facc6d48807808e4d97a454a0ecceb2769ac9e |
| Robustness | CLEAN | DN runs on its own model (`NotifyBench::model`), so the main timeline does not move (first-build lines otherwise identical). Windows are contiguous (late duplicates land in the next window; S1). The 8,167 ms span is under `T-NOTIF-MONITOR`'s 30 s floor, so no CONTROLLER_AVAILABLE. Determinism: base and head full runs give identical graded lines. My 7 probes | R502-1 | 72facc6d48807808e4d97a454a0ecceb2769ac9e |
| Tests | UNCLEAN (F1) | `notify_phases.hpp:1642-1845`, `sim_main.cpp` flag wiring, `notify_mutants.py` DOMAIN_NOTIFY and judge rules. Full pp_top six builds at base and head. notify_mutants 65/65 at head. Static plant of 377 arms. 7 reviewer probes. Timing instrumentation | R502-1 | 72facc6d48807808e4d97a454a0ecceb2769ac9e |
| Docs | UNCLEAN (F1) | `tb/pp_top/README.md` (C6 intro, section DN, mutation record and 9 rows, all matching the measured failing sets). `09_verification.md` §8.4 row and flag list. `notify_mutants.py` docstring. Line citations `:157`, `:184`, `:4018`, V6-V6i, S8, DV4 and DV5 all resolve. Docs gates links/matrix/modmatrix/params/ids/figures/stale rc 0 at base and head with identical logs | R502-1 | 72facc6d48807808e4d97a454a0ecceb2769ac9e |

## Receipts (all listed in MANIFEST.sha256)

- `scripts/run_r502.sh`: the commands as run. `scripts/plant_check.py`: static plant check. `scripts/r502_probes.py`:
  reviewer probes.
- `receipts/tool_identity.txt`: Verilator 5.050 (wrapper sha256 `905795b9...e92f`), GNU Make 4.4.1, Python 3.14.7.
- `receipts/dn_only_head.{log,rc}`, `receipts/gsi_build_head.log`: DN alone, 15 checks, 0 failures, rc 0.
- `receipts/pp_top_full_{base,head}.{log,rc}`, `receipts/pp_top_graded_base_vs_head.diff`: six builds each, rc 0, 10,444 and 10,459.
- `receipts/notify_mutants_head.{log,rc}`, `receipts/notify_mutants_head_results.json`: 65 of 65 KILLED, 8 goldens PASS, rc 0.
- `receipts/plant_check_{base,head}.{log,rc}`: 368/368 and 377/377 plant.
- `receipts/r502_probes.{log,rc}`, `receipts/r502_probes_results.json`.
- `receipts/probe_timing_statements.{patch,log}`: F1's evidence.
- `receipts/docs_gates_{base,head}.{log,rc}`: rc 0, identical.
- `receipts/hosted_checks_snapshot.txt`, `receipts/clone_integrity.txt`.

Harness notes: in the scratch copies only, the pp_top Makefile's Verilator `--build -j 0` became `-j 4` to stay inside
the 12 GB unit cap (this changes build parallelism only). Home-directory paths in the build logs are replaced by
`<VERILATOR_IMAGE>`/`<HOME>`. The review clone was never modified: `clone_integrity.txt` shows HEAD and tree exact, an
empty `git status --porcelain --ignored`, index equal to HEAD, and all 556 tracked blobs and modes byte-exact. The
repository has no submodule gitlinks (no `.gitmodules`, no mode-160000 entries), so there are none to verify.

## Prior public review findings at this head

I wrote the verdict, the findings and the ledger above before reading any other review. At the time of reading, PR #164
has no formal reviews and no inline comments. It has three issue comments: two review-start notices and one public
report, `[R503] NEGATIVE` (comment 6011470805).

| Prior finding | Status at 72facc6d | Basis |
|---|---|---|
| R503-1-F1 (MINOR, Docs): `tb/pp_top/README.md:2497` says "495 after the MRPDU's last byte". It is 499 from the last byte, or 495 from `feed()`'s return | **RETAINED** (open) | I reproduced it independently: `receipts/probe_timing_statements.log` gives last byte 340030 then `t0` 340034, and 580098 then 580102, the same clocks as that report, with the frames leaving 495 clocks after `t0`. It is part 2 of F1 above, which also covers the first-stimulus spacing statement (part 1, not raised before) and lists Tests as an attributable lens, because the bench comment at `notify_phases.hpp:1663` carries the same inaccuracy. |

## Real limits

- I did not run `./scripts/run_suites.sh` (all 33 suites), `lint_hdl.sh`, `make check`'s Mermaid `lint` and
  `wavedrom-check`, Yosys, or the parent consumer set of 17 (owner restriction on full banks). Neither changed doc
  block contains Mermaid or WaveDrom. The RTL is unchanged, so lint and Yosys are unaffected by construction. The
  parent set relies on the manager's evidence.
- I ran the other pp_top-building campaigns (d3, aecp, aecp_dispatch, acmp, ctr, gsi, name_wr, adp_engine and maap
  pp_top arms) only statically: their planted texts and patches apply at head. Their dynamic verdicts rest on the
  author's evidence. None of them plants into a changed line (the two ctr patches touching `sim_main.cpp` apply cleanly).
- I compared the 56 pre-existing notify_mutants arms by verdict at head, not record by record against a base run.
- Physical calibration was not run. No hardware. Field skips are not hardware proof.

## Pending manager duties

- Hosted/act acceptance. The snapshot at 2026-10-06T07:30:55Z shows `docs-gates` and `portability` succeeded on both
  runs, and `suites` still in progress on both (37427673979 and 37427666734).
- The final current-dev candidate at the merge turn (source base `e6a759de`, live dev `423ac5d9`; processor main has
  since moved, #134 then #22), and the review of that delta.
- The parent consumer set (17 at `28f9666f` with the 148 patch) as the manager's gate.
- Publication: in the published handoff (`review-evidence/pp42-r1/author/HANDOFF.md`), redaction replaced the check
  name "<bench-switch-model>" with `<bench-switch-model>` in two table rows. That is an evidence-publication artifact, not a defect
  of the PR.

R502-1 FINISHED
