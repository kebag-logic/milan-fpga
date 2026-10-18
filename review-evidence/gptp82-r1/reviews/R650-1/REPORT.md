[R650] NEGATIVE - exact head 85373de08a5c35487f260087ac8ceaf7a3789cdc

# R650-1 internal independent review: FPGA-gPTP PR #83 (issue #82)

- Repository: Mister-M-alt/FPGA-gPTP, PR #83, branch `82-boot-gm-thisclock`
- Exact head: `85373de08a5c35487f260087ac8ceaf7a3789cdc`, tree `322597c55a18b4f9a80f93e00dbe1256539f0cbe` (verified in the review clone)
- Source base: `b9ade3a63d1b2292d75eb9b1809647e6439542a0`. Its tree matches the parent's current gitlink `e4869fd0` (empty `git diff`).
- Parent consumer: kebag-logic/milan-fpga dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`
- Author evidence: milan-fpga `40ed29fcc1ed0b6f785b4d28b646b86796f6460b:review-evidence/gptp82-r1/`
- Round: R650-1, internal reviewer, cleared context. The review used the clone's public state, the issue and PR threads, the diff, and the published evidence.

## Verdict summary

The RTL change is small. The published interface is unchanged. At head, every graded commit names a grandmaster consistent with its path; the reviewer invariant over 427 commits found no torn read. All six #82 cases have mutants that fail them. Repository gates and the reproduced consumer suites pass.

The verdict is NEGATIVE for four reasons:

- **F1:** after a cold start, the issue's defect remains for the first 1.2003 s. Grandmaster 0 and an empty path are published until the first timer beat.
- **F2:** after a warm reset that retains a best record, a better live peer is not elected. The departed grandmaster is committed instead, which contradicts the new integration text.
- **F3:** two properties the PR claims are not graded. Two reviewer mutants pass the full 1623-check suite.
- **F4:** the receipt index lists an `iface/` directory that the evidence commit does not contain.

## Findings

### F1 - MAJOR - Conformance, RTL, Tests - cold start still publishes GM 0 and an empty path for 1.2 s

- **Where:**
  - `hdl/top/KL_gptp_engine.sv:823`: the boot commit waits for `local_clock_valid_r`.
  - `hdl/top/KL_gptp_engine.sv:983` and `:990`: GM 0 and count 0 are published until the clock is valid.
  - `hdl/top/KL_gptp_engine.sv:847-851`: slot 0 is armed at 1200 ms.
  - `hdl/ucode/gen_gptp_ucode.py:1321-1336`: S_CID is installed only by the slot-0 init leg.
  - `tb/verilator/engine/sim_main.cpp:1155-1163`: phase 1d.
  - `docs/INTEGRATION.md:488-490`.
- **Authority:**
  - Issue #82 "Done when", first bullet: "the engine publishes thisClock as grandmaster and {thisClock} as the path from reset".
  - Assignment item 1 (issuecomment-6249575055): "From reset, publish thisClock ... before any peer", per IEEE 802.1AS-2020 10.3.13.2.4 b) and i).
  - The issue reports the boot (cold) case.
- **Evidence:**
  - Reviewer probe `raw/probe/probe-head-run.log`: "PROBE-COLD first nonzero-GM commit ... 2400604 cycles after release = 1.2003 s".
  - Before that commit, the outward bank is GM 0 / count 0 (`:983`, `:990`). The parent shadow holds its reset zeros.
  - RX handlers are init-guarded (`gen_gptp_ucode.py:606-613`), so no peer can be elected in this window. The window is purely the #82 boot state.
  - Phase 1d grades only that the *first* commit names thisClock. It has no time bound, so it accepts the window.
  - The PR body and `docs/INTEGRATION.md` state the window openly, and the PR uses "Refs #82". However, no public maintainer or manager decision narrows the frozen acceptance.
- **Impact:**
  - For 1.2 s after every power-up, GET_AVB_INFO, GET_AS_PATH and ADP report the GM 0 / empty-path state that #82 was filed to remove.
  - The issue's own acceptance bullet is unmet for the cold start.
- **Required outcome:** one of the following.
  - The publication names thisClock with {thisClock} from cold-reset release. A graded, time-bounded case and a planted mutant must cover it.
  - Or a recorded maintainer/manager scope decision on #82 accepts the residual cold-start window and moves it to a tracked follow-up issue, and the acceptance text is amended to match.
- **Verification:** either is sufficient.
  - The probe line `PROBE-COLD first nonzero-GM commit` (or an equivalent suite check) shows the first commit a bounded number of cycles after cold release.
  - Or the public scope-decision link exists.

### F2 - MAJOR - Conformance, RTL, Robustness, Tests, Docs - after a warm reset a retained best record outranks a live better peer; a departed GM is published

- **Where:**
  - BTCA compares against warm-retained scratch S_BEST*: `hdl/ucode/gen_gptp_ucode.py:1548-1630`. It takes `they_win` with `S_BESTSRC` as parent at `:1607-1608`. The `same_gm` refresh re-arms the receipt watch at `:1626-1628`.
  - `hdl/top/KL_gptp_engine.sv:683-684`: the raw path is warm-retained.
  - `docs/INTEGRATION.md:468` ("Every reset leaves no elected peer.") and `:494` ("A better peer then wins through normal selection.").
  - `tb/verilator/engine/sim_main.cpp:4731-4734`: the phase-35 comment says "A warm reset clears every port vector", but the phase uses "A peer better than any retained record".
- **Authority:**
  - Assignment item 1: from reset the plane is its own grandmaster, and "When a better grandmaster appears, normal BMCA publication takes over".
  - The phase-35 comment cites 802.1AS-2020 10.3.13.2.4 for the same point: a reset leaves no port vector.
- **Evidence (reviewer probe phase `probe_warm_reset_with_a_retained_record`, `raw/probe_sim_main.diff`):**
  1. Peer A (priority1 0) wins.
  2. A warm reset is taken while A is the retained best record. The head correctly commits thisClock with {thisClock}.
  3. A falls silent, and peer B (priority1 1, worse than A, better than this plane) announces.
  4. Result (`raw/probe/probe-head-run.log`): "PROBE-WARM B announce after reset: ... last gm 0065a0fffe0000a1 (A=...a1 B=...b1 ...) parent 0065a0fffe0000a3 count 2 flags 5".
  5. B announces three more times at 1 s spacing. Each time the outward GM is still departed A and the parent is A's port, with no AMGM flag.
  6. The same probe against the base RTL shows the same A publication (`raw/probe/probe-base-run.log`). The defect predates this PR. The PR body lists it as an untested known limit ("From reading the code (not tested)").
  7. The `same_gm` branch re-arms the 3 s receipt watch on every B Announce. From code reading, A therefore stays published for as long as B keeps announcing.
- **Impact:**
  - After any warm reset taken while a peer was elected, the plane can publish a grandmaster and AS path that are no longer on the wire, and select a parent that no longer exists. This goes to GET_AVB_INFO, GET_AS_PATH and ADP through the shadow. The plane then never adopts the real grandmaster B.
  - At the same time, this PR's boot publication and its integration text tell integrators that every reset starts with no elected peer and that a better peer wins normally.
  - The suite's warm-reset case avoids the condition by construction.
- **Required outcome:**
  - Make the selection state agree with the reset-time publication, so that a record retained across reset cannot outrank a live better peer. Cover it with a simulation case (warm reset taken while a peer is elected, then a worse-than-retained but better-than-self peer) and a planted mutant.
  - Or obtain a recorded maintainer/manager scope decision that moves this to a tracked issue. In that case, `docs/INTEGRATION.md:468`/`:494` and the phase-35 comment must be corrected to describe the retained-record behaviour.
- **Verification:**
  - Re-run `scripts/make_probe_harness.py` + `scripts/build_probe.sh`. The `PROBE-WARM a peer B better than this plane is elected after the reset` check must pass, or the scope link and corrected text must exist.

### F3 - MINOR - Tests, Robustness - boot-commit uniqueness and warm-reset self-path tail are ungraded

- **Where:**
  - `hdl/top/KL_gptp_engine.sv:823-828`: boot commit retirement.
  - `hdl/top/KL_gptp_engine.sv:992`: the self path forces a zero tail.
  - `tb/verilator/engine/mutants.py:291-333`.
- **Authority:**
  - PR body: "The engine raises one commit of its own after each reset", and "The commit is still a single-cycle pulse over stable outputs".
  - Port contract `hdl/top/KL_gptp_engine.sv:118-121`: inactive slots are zero, and the self path is {thisClock}.
  - Review focus: no torn read at any transition.
- **Evidence:** reviewer mutants, `scripts/extra_mutants_r650.py` and `raw/head-extra/`.
  - `R650 boot commit never retires` deletes `boot_pub_pend_r <= 1'b0` from the firing branch. The full suite passes 1623/1623. The probe harness counts 34,765,940 commits instead of 427 (`raw/probe/probe-m03-run.log`).
  - `R650 self path keeps the raw tail` also passes 1623/1623. The reviewer invariant flags two commits that name thisClock with count 1 and the previous peer's tail after a warm reset taken while a peer was elected (`raw/probe/probe-m06-run.log`).
- **Impact:**
  - A regression to continuous commits would leave nothing in this repository failing. It would also copy the raw bank on every idle cycle, which can expose staged-but-uncommitted words, i.e. the torn read the change claims to prevent.
  - A regression that leaks a peer tail into the self publication would pass the engine suite.
- **Required outcome:**
  - Graded checks that exactly one engine commit follows each reset.
  - Graded checks that the self publication after a warm reset taken while a peer is elected carries count 1 and an all-zero tail.
  - A planted mutant that fails each check.
- **Verification:** both reviewer mutants fail the suite.

### F4 - MINOR - Docs - author receipt index names an `iface/` directory that is not published

- **Where:** `review-evidence/gptp82-r1/author-receipts/RECEIPTS.md` at milan-fpga `40ed29fc`. It lists "`iface/`: the published-interface checks".
- **Evidence:**
  - The evidence commit holds 125 files under `review-evidence/gptp82-r1`, none under `iface/`.
  - The interface claim appears only as prose in `author/HANDOFF.md:133-135`, plus `author-receipts/scripts/ports.py` without its output.
- **Impact:** the interface/STOP-check evidence that the index promises cannot be opened by a cold reviewer. This reviewer reproduced the claim independently (`raw/iface_check.log`), so no defect in the interface itself is alleged.
- **Required outcome:** publish the interface-check receipts, or correct the index.
- **Verification:** the listed path exists in the evidence tree, or the index no longer names it.

### R1 - RESIDUE - Docs - PR body "byte-identical" wording

- **Where:** PR #83 body, Interface section: "Parameter and port declarations are byte-identical to the parent's current pin."
- **Evidence:** the `pub_path_count_o` port comment (`hdl/top/KL_gptp_engine.sv:118-121`) changed. With comments stripped, the declarations are identical (`raw/iface_check.log`, SHA-256 `5b27038e...` both sides). Only the wording overstates.
- **Exact fix:** "Parameter and port declarations are identical to the parent's current pin once comments are stripped; only the `pub_path_count_o` comment changed."

### S1 - SUGGESTION - RTL, Tests - the idle guard and the cancel branch are not graded

`R650 boot commit ignores a running handler` (drops `&& !dbg_busy_o`) and `R650 a microcode commit does not cancel the boot commit` both pass 1623/1623.

Under the current ROM both behave the same as the head design, because:
- the cold init leg writes no publication word;
- no microcode COMMIT can precede the boot commit;
- busy covers every store (`hdl/ucpu/KL_gptp_ucpu.sv:730`).

Consider a short comment saying that these guards are defensive, or a directed case if a future ROM may write the bank before S_CID.

### S2 - SUGGESTION - Robustness - zero GM as the "no election" sentinel (code reading, not executed)

`hdl/top/KL_gptp_engine.sv:982` treats raw GM 0 as "no election since reset".

Suppose an Announce that names grandmasterIdentity 0 wins BTCA. Because `same_gm` compares raw GM 0, the raw GM would stay 0 (`gen_gptp_ucode.py:1609-1611`). The head would then publish thisClock/{thisClock} while the parent identity names the peer; the base published GM 0. This is already malformed-peer territory, and adoption is skipped at base too.

Consider a resettable "elected" bit, or rejecting a zero grandmasterIdentity.

## Prior public findings

There were no prior public review findings on PR #83 at this head. The PR has no reviews and no review comments. Its comments are the two review-start notices. The issue thread holds the assignment, TAKEN, and REVIEW READY. Nothing needed to be resolved or retained.

## Assignment checks (focus)

| Check | Result | Evidence |
|---|---|---|
| Boot, no peer: case + mutant | Present for warm reset and for the cold first commit. The cold-start window is open (F1). | Phase 1d, phase 35. Mutants `boot publication restored to zero` and `no engine commit after reset` fail all named checks (`raw/head-mutants/engine-mutants-all.log`). |
| Peer wins: case + mutant | Present and failing as claimed. Warm reset with a retained record not covered (F2). | `thisClock hides an elected peer`, `an elected peer keeps the self path` caught on their named checks. |
| Peer leaves → thisClock: case + mutant | Present and failing as claimed (asCapable-held departure). | `becoming grandmaster keeps the departed GM/path` caught on their named checks. |
| Interface to milan-fpga unchanged in width/timing | Width: unchanged. Timing: commits are single-cycle; the boot commit is registered and fires only with the µCPU idle. | `raw/iface_check.log` (comments-stripped header identical). `milan_datapath.sv:1515` consumes `gptp_pub_gm_w` from `KL_gptp_shadow`, which copies on commit (`KL_gptp_shadow.sv:733-768`). |
| Path count/entries consistent with GM at every transition | Clean at head over the whole suite. Two consistency properties are ungraded (F3). | Reviewer invariant: 427 commits, 0 GM-0, 0 bad self paths, 0 bad tails (`raw/probe/probe-head-run.log`). |
| Repository gates | Pass at head. | `raw/head-gates/*.rc` all 0: contract, lint, docs, ucpu 768, parser 337 + 9/9, gaskets 81 + 5/5, tsngen 288 + 4/4, bench tag, engine 1623 ×3 images. Engine mutation table 40/40 (control + 39) with the #82 every-named-check rule. |
| Parent consumer gates | Reproduced subset passes. Author receipts cover the rest; the two mutant arms were not run at head. | Scratch parent e9cbb676 with head engine: `gptp_shadow` 309/309; `gptp_plane` 29 + 62 + 8 (`raw/parent-consumer/`). |
| Author receipts under author-receipts/ | Published; index incomplete (F4). | 125 files at `40ed29fc`. |
| ROM unchanged | Confirmed. | Base and head generators emit identical images: default `a435fba6...`, suite `b02f66b1...`, equal to the author's `base.hex`/`head.hex` (`raw/rom_identity.log`). |
| Comment rule in the reviewed delta | Clean. | No lane labels, lane names, rounds, reviewer IDs or issue-comment IDs in added lines; only issue `#82` and clause IDs. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Issue #82 body and assignment; PR body; `KL_gptp_engine.sv:768-993`; `gen_gptp_ucode.py:606-613,1321-1381,1548-1660`; parent `milan_datapath.sv:1496-1516`, `KL_gptp_shadow.sv:635-768`; reviewer probe logs head/base | R650-1 | 85373de08a5c35487f260087ac8ceaf7a3789cdc |
| RTL | UNCLEAN (F1, F2) | `KL_gptp_engine.sv:111-137,146-158,621-993` (diff and context); `KL_gptp_ucpu.sv:425-450,700-731` (busy/commit timing); header comparison; lint gate | R650-1 | 85373de08a5c35487f260087ac8ceaf7a3789cdc |
| Robustness | UNCLEAN (F2, F3) | Warm reset taken while a peer is elected (probe); continuous-commit and tail-leak faults; zero-GM sentinel reading; pre-init window | R650-1 | 85373de08a5c35487f260087ac8ceaf7a3789cdc |
| Tests | UNCLEAN (F1, F2, F3) | `sim_main.cpp` phases 1d and 35 plus helpers; `mutants.py:291-333,459-471`; full engine mutation table run (40/40); 6 reviewer mutants (1 caught, 5 pass); base-RTL non-vacuity (6 #82 checks fail at base) | R650-1 | 85373de08a5c35487f260087ac8ceaf7a3789cdc |
| Docs | UNCLEAN (F2, F4; R1 residue) | `docs/INTEGRATION.md:462-498`, `docs/HDL_DEVELOPER.md:176-186`, `docs/TEST_DEVELOPER.md:109-110`, `docs/SOURCE_EVIDENCE.md:31` (anchors L947/L952 verified); PR body; author RECEIPTS.md and HANDOFF.md | R650-1 | 85373de08a5c35487f260087ac8ceaf7a3789cdc |

## Reviewer execution (all at exact head unless stated)

- **Simulator:** pinned Verilator 5.050 (`raw/tool-identity.log`), first on PATH.
- **Gate trees:** `git archive` exports of head and base. The only reviewer edit caps build parallelism (`raw/scratch-copy-note.txt`).
- **Repository gates:** the nine gate targets ran concurrently. All returned rc 0 (`raw/head-gates/`).
- **Engine mutation table:** `scripts/run_engine_mutants_parallel.py` imports the tree's own `mutants.py` table and applies its #82 every-named-check rule. Result: RESULT 40/40 (`raw/head-mutants/`).
- **Reviewer probe harness:** `scripts/make_probe_harness.py` derives `raw/probe_sim_main.diff`. It was built against head RTL, base RTL, and two mutant RTLs by `scripts/build_probe.sh` (`raw/probe/`). The probe run's rc is 1 only because of the F2 probe check at head. All 1623 suite checks pass.
- **Reviewer mutants:** `scripts/extra_mutants_r650.py` (`raw/head-extra/`).
- **Interface:** `scripts/iface_check.py` (`raw/iface_check.log`).
- **Parent consumer subset:** `gptp_shadow run` and `gptp_plane all` on a scratch archive of milan-fpga e9cbb676, with `gptp-processor/` replaced by the head export (`raw/parent-consumer/`).
- **Clone restored:** HEAD, tree and index tree are the exact head. `git diff --quiet HEAD` returns 0. There are 0 status lines including ignored files. The gPTP repository has no gitlinks or `.gitmodules` (`raw/clone_restore_check.log`). No parent checkout was modified.

## Real limits

- The IEEE 802.1AS-2020 and Milan v1.2 texts were not available to this reviewer. Clause meaning (10.3.13.2.4 b/i, 10.3.9.23; Milan 5.4.2.23/5.4.2.24) is taken from the frozen issue text and the parent's traceability records.
- Not run by this reviewer:
  - the parent `gptp_shadow`/`gptp_tables` mutant arms (they refuse an uncommitted gitlink, and commits are outside this review's permissions);
  - the field campaign, `milan_dp` legs, elaboration/Yosys, port-contract and wire-accountability checks.
  For these, the author's receipts at `40ed29fc` are the only evidence.
- There is no hosted execution at this head. The repository has no workflows, and the commit has 0 check runs and 0 statuses.
- Physical calibration was NOT RUN; field skips are not hardware proof. The 1.2003 s figure is at the suite's 2 MHz model clock. The 1200 ms slot-0 arm scales with `CLK_HZ_P`, so hardware should match, but this was not measured on hardware.
- S2 is from code reading and was not executed.

## Pending manager duties

- Decide F1/F2 scope: fix in this PR, or record a scope decision with tracked follow-ups.
- Carry R1 to the residue checklist.
- At the merge turn, build and validate the current-dev candidate (source base b9ade3a, live dev e9cbb676): builder and native banks, the parent mutant arms that refuse an uncommitted gitlink, the gPTP docs check and ROM-digest ledger pin-bump edits, and the full `milan_dp` / field suites. Link the receipts on the PR.
- Own hosted/act acceptance.

R650-1 FINISHED
