[R722] POSITIVE - exact head c1bc9e21a273fd8506b4806a2470fb7bab13f72f

# R722-1: external independent review of FPGA-gPTP PR #93 (issues #87, #88)

- Repository: Mister-M-alt/FPGA-gPTP. PR #93, branch `87-88-announce-pathtrace`.
- Exact head `c1bc9e21a273fd8506b4806a2470fb7bab13f72f`, tree `8673c3750bb610ae5eab239f0675ba94326f67e7`. Base main `55680bff3b287b9a7b0c759f51471fa617c17335`.
- Scope: the [A10] assignment (#88 issuecomment-6434676531), the [A690] STOP (issuecomment-6440962747), and ruling (A) (issuecomment-6442193793). Ruling (A) authorises one top-level change: an explicit entry-zero path output.
- Edition: IEEE 802.1AS-2011 with Cor1-2013 and Cor2-2015.
- Reconstruction order:
  1. Repository guides (`README.md`, `docs/README.md`, `docs/MANAGER.md`, `docs/HDL_DEVELOPER.md`, `docs/INTEGRATION.md`, `docs/TEST_DEVELOPER.md`, `docs/SOURCE_EVIDENCE.md`). The repository has no AGENTS.md or CONTRIBUTING.md.
  2. Issue #87 and #88 bodies, then every maintainer and manager comment on both.
  3. `git diff 55680bff..c1bc9e21` and the five commits.
  4. Public evidence at milan-fpga `df89292c:review-evidence/gptp88-r1/author-r1/a690b` (handoff, receipts, companion patch).
- Prior public review findings on PR #93: none. The PR has zero reviews, and its only comments are the two review-start notices. Nothing is carried forward.

## Verdict basis

Every acceptance point holds at the exact head. I reproduced all of them independently on this host.

1. **Only 10.3.10.2.1 a)-c) disqualify an Announce.**
   - The count refusal (lengthField/8 vs stepsRemoved+1), the head refusal (first entry vs grandmasterIdentity) and the zero-length refusal are gone. See `hdl/wire/KL_gptp_rx_parser.sv:318-322`, the removed `gm_r`/`steps_r`/`ann_head_bad_w`, and the `fin_ok_r` term at `:625-632`.
   - The remaining PathTrace header rules are 8N framing and singularity. Neither is a qualification rule: they define a well-formed TLV.
   - a) and b) remain in the microcode. c) remains as the parser's all-hop loop verdict (word 12 bit 8, `:599`) consumed by the microcode (`gen_gptp_ucode.py:982-988`).
   - Under 802.1AS-2011 10.5.3.3.4, N = stepsRemoved+1 is only a NOTE.
2. **10.3.10.2.1 d) copy and keep-previous.**
   - A present TLV is staged from entry 0 and thisClock is appended (`hdl/top/KL_gptp_engine.sv:731-737`, `:986-1003`). An empty TLV gives {thisClock}.
   - Without a TLV the address-7 write changes nothing (`:990`), so the previous pathTrace stays.
   - Reset and the self-master write load `self_path_w` = {thisClock}. That matches 10.3.12.1.1 (updtRoleDisabledTree) and 10.3.12.1.4 i) (Cor1) (`:737`, `:845`, `:976-977`).
   - Presence is message word 12 bit 63, set for any PATH_TRACE header including a zero-length one (`KL_gptp_rx_parser.sv:398`, `:571`). It sits above the bits 39:8 that the unchanged microcode's loop test reads (`SHR 8`, 32-bit `CMP`, `gen_gptp_ucode.py:982-984`).
3. **ABI.**
   - The only port change is `pub_path_o` from `[7*64-1:0]` to `[8*64-1:0]`, entry k at `64*k` (`KL_gptp_engine.sv:126-127`). `pub_path_count_o` keeps its width and now counts entries from entry 0.
   - No parameter or other port changed. The bench top leaves the port unconnected (`bench/arty/bench_arty_top.sv:304-305`). Region-3 word 7 now also reads entry 0; the microcode never reads it.
   - `docs/INTEGRATION.md:456-506` documents the change (one wording RESIDUE, R722-1-F1).
4. **Named checks with planted mutants** exist for every removed refusal, the empty TLV, entry 0 as the received head, and the keep-previous cases (after reset; G1 to G2 without a TLV). I reran both arms here (see Tests).
5. **milan-fpga companion** (sha256 `fa3c22f0a2856f4e3fd79fda60cdfdcd9b281492da564ca4123c69145d71a986`, verified).
   - It applies cleanly to dev `97aab1d0`.
   - Its RTL is coherent: the CSR AS_PATH face is a combinational passthrough at dev (`milan_csr.sv:2851-2853`), so entry 0 taken from the engine beside CSR entries 1..7 cannot tear.
   - It is minimal for the ruling's list.
   - Its suites pass at the pinned head (see Tests).
6. **ROM images.** All seven generator configurations regenerate byte-identically from the base and head generators. The four tracked `.hex` blobs are unchanged and equal to their regenerated images.
7. **Generator.** `hdl/ucode/gen_gptp_ucode.py` differs from base only in comments and docstrings (AST-equal).

## Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R722-1-F1 | RESIDUE | Docs | `docs/INTEGRATION.md:464`; port comment `hdl/top/KL_gptp_engine.sv:121` | The pre-existing outward gate `KL_gptp_engine.sv:1062-1064` publishes count 0 and every entry zero while the raw grandmaster is zero. That happens when an elected Announce names grandmasterIdentity 0; no rule refuses it. | The prose says the count "runs from one to eight" (comment: "1..8") and omits that gated zero case. Behaviour is unchanged from base, and no code, test, figure or clause claim depends on the sentence. The companion's shadow port comment already says `0..8`. | Wording only. After `docs/INTEGRATION.md:464` add: "It is zero, with every entry zero, only while the published grandmaster identity is zero." In `KL_gptp_engine.sv:121` replace "1..8" with "1..8 (0, every entry zero, while the published grandmaster is zero)". | Read both lines against `:1062-1064`; `make docs` stays rc 0. |
| R722-1-S1 | SUGGESTION | Conformance | `KL_gptp_engine.sv:986-1003` with `gen_gptp_ucode.py:1628-1643` (`take`) | 802.1AS-2011 10.3.10.2.1 d) copies only when "the portRole of the port is SlavePort". | The engine stages the path at the `take` that elects the sender, so a new grandmaster's path appears one Announce earlier than a literal reading, where the port is still a MasterPort. This predates #85, the handoff discloses it, it is outside ruling (A), and it is not a qualification failure. | If the owner wants literal timing, track it separately; no change is required here. | n/a |
| R722-1-S2 | SUGGESTION | Tests | `tb/verilator/engine/sim_main.cpp` (TLV-less phases) | My probe "zero-length unknown TLV marks presence" (parser marks presence on any zero-length TLV) survives the engine suite (1929/1929). The parser suite catches it (`tb/verilator/parser/sim_main.cpp:432`, `:442`). | Caught at the system level; the engine suite alone has no TLV-less Announce carrying a zero-length non-PathTrace TLV. | Optional: add one such frame to an engine keep-previous phase. | `receipts/probes/engine-probes.log`, `receipts/probes/parser-probes.log` |
| R722-1-S3 | SUGGESTION | Docs | Companion: milan-fpga `tb/verilator/tsn_fuzz/README.md:196-208, 219` | That README's own rule says to re-measure quoted PASS figures when the campaign total moves. | The quoted "638 gPTP checks" and the N10-N15 pass figures were already stale at dev (the campaign was 677). The companion moves it to 675 without refreshing them. This predates the companion and is not caused by it. | At adoption, or under its own tracking, re-measure or drop the quoted pass figures. | n/a |
| R722-1-S4 | SUGGESTION | Docs, Conformance | `KL_gptp_engine.sv:835`, `docs/INTEGRATION.md:512` (not in the delta) | Project edition decision: 802.1AS-2011 + Cor1/Cor2. | Pre-existing 802.1AS-2020 citations for the self publication. The 2011 equivalents are 10.3.12.1.1 and 10.3.12.1.4 i), which this PR already cites beside them. | Align under the existing comment and edition tracking. | n/a |

No BLOCKER, MAJOR or MINOR finding is open. RESIDUE and SUGGESTION items do not leave a lens unclean.

## Lens evidence

### Conformance — CLEAN
- **#88:** each removed refusal is isolated by a probe that violates only that rule:
  - count only: "#88 issue shape" (priority1 247 vs 248, stepsRemoved 3, one entry);
  - head only: "#88 head not the grandmaster" (two entries, stepsRemoved 1);
  - empty TLV: "#88 empty path", plus the empty TLV from the parent.
  - Each defers: elected, not master, one coherent commit, no Announce for 1.05 s (`tb/verilator/engine/sim_main.cpp:2548-2626`).
- **a)-c):** still refuse, each with its own named check and microcode-removal mutant (engine arm "(a)/(b)/(c) ... removed").
- **(b) boundary:** my reviewer probe moving `STEPS_MAX_C` to 256 is caught by 286 checks.
- **#87:** the following cases are graded from entry 0 (`:2628-2702`, `:4448-4454`):
  - G1 to G2 without a TLV keeps G1's path, G1 at entry 0;
  - a TLV-less parent refresh keeps the path;
  - after a warm reset a TLV-less grandmaster keeps {thisClock};
  - a degrade returns {thisClock}.
- **GET_AS_PATH (IEEE 1722.1-2021 7.4.41.2):** the companion serves entry 0 from the engine head (`asp_owner_head_w`), never `cfg_adp_gptp_gm`. The Table 5.22 comparator watches the same head.

### RTL — CLEAN
- **Parser:**
  - A zero-length PATH_TRACE header marks `pt_seen_r` on its header edge. That gives presence, and the duplicate rule still refuses a later PathTrace.
  - The deferred w12 write samples registered `pt_seen_r` one cycle after EOF. A zero-gap SOF clears it only on that same edge, which matches the existing `pt_cnt_r`/`pt_self_r` pattern.
  - The EOF qualification still includes the current-byte header verdict.
- **Engine:**
  - `ann_pub_present_r` is captured with the count on the w12 write, under the same frozen-context gate.
  - w16..w23 are captured; inactive entries are cleared on the address-7 edge; the clamp still prevents a ninth entry.
  - The simulation assertion guards a count-zero commit with nonzero entries.
  - `rom_clock_id_w` is constant image data, so `self_path_w` is valid at reset.
- **Lint and cost:** `make lint` (engine + bench, `-Wall`) rc 0. The cost is about 129 flops plus muxing, not synthesised here (see limits).
- **Reviewer probes**, each caught by named checks:
  - presence latched sticky;
  - entry 0 not captured;
  - count rewritten without a TLV;
  - append past eight;
  - self-master keeping stale entries;
  - count refusal for longer-only and shorter-only paths;
  - duplicate PathTrace accepted.

### Robustness — CLEAN
- Hostile shapes stay refused, or qualify only where 2011 says so:
  - zero-length TLV alone and between unknown TLVs;
  - a TLV after an empty one (refused as a duplicate);
  - a thisClock head (loop verdict still set);
  - out-of-message PathTrace bytes (absent);
  - more than eight hops (first eight published, all hops loop-checked).
- The frozen Announce context still owns presence, count and entries from enqueue through COMMIT. The overload test keeps C's path across TLV-less chasers ("#87 raw-empty overload: frozen A keeps C's path").
- Parent: tsn_fuzz `ptp` fuzz storms and the BTCA section pass with the head pinned (675/675).

### Tests — CLEAN
Repository gates at head, run by me (`receipts/head-gates/`), all rc 0:

| Gate | Result |
|---|---|
| `make contract` | PASS |
| `make -C tb/verilator/ucpu` | 768/768 |
| `make -C tb/verilator/parser` | 378/378, arm 16/16 |
| `make -C tb/verilator/engine run` | 1875 ×3 + 54 |
| engine mutation arm, 5 reviewer shards | 5 controls pass; 84/84 mutants caught on every named check |
| `make -C tb/verilator/gaskets` | 81/81, arm 5/5 |
| `make -C tb/tsngen` | 288/288, arm 4/4 |
| `make -C bench/arty test` | PASS |
| `make lint` | rc 0 |
| `make docs` | rc 0, evidence 20 exact |

- The scratch tree's 107 tracked blobs are byte-identical to the head after every gate.
- Reviewer probes (`receipts/probes/`): parser 4/4 caught; engine 9/10 caught. The one engine survivor is caught by the parser suite (S2).

Parent consumer gates on a scratch milan-fpga at dev `97aab1d0`, companion applied, gptp-processor gitlink at `c1bc9e21`, run by me (`receipts/parent-head/`):

| Gate | Result |
|---|---|
| `check_cpp_idiom.py` | rc 0 |
| `check_py_idiom.py` | rc 0 |
| `check_rtl_source_lists.py` | rc 0 |
| `check_port_contracts.py` | rc 0; gptp-processor 125 ports |
| `measure_naming.py --check` | rc 0 |
| `measure_test_evidence.py --check` | rc 0 |
| `docs_check.py` | rc 0 |
| `lint_rtl.py --check` | rc 0; 89 ≤ 89 |
| `make -C tb/verilator/gptp_shadow` | 320/320 PASS. Its mutation arm refused to run because the companion is uncommitted in scratch. |
| `make -C tb/verilator/milan_dp gptp` | 192/192, rc 0 |
| `make -C tb/verilator/tsn_fuzz ptp`, oracle at the CI pin `deca300c` | 675 pass, 0 fail. The freshness gate reports STALE only because it compares against git HEAD, which is dev in the uncommitted scratch tree. The fresh file equals the companion's regenerated `TEST_RESULTS.md` byte for byte with the timestamp normalised (`fuzz-ptp-freshness-vs-companion.txt`). |

For the legs I did not run, the author's receipts at companion snapshot `0ea1074f` show all 15 consumer gates exit 0. That covers `xvlog_gate`, the builder, `gptp-lat`, `milan_dp_gptp` and `milan_dp_gm_steps`, plus the companion mutation table (64/64 new parent checks failed by a planted mutant).

### Docs — CLEAN (one RESIDUE)
- `docs/INTEGRATION.md:456-506` describes the eight-entry ABI, entry k bit placement, the d) copy from the received head, the empty TLV, and keep-previous with {thisClock} after reset or mastership.
- `docs/HDL_DEVELOPER.md:206-220` and `docs/TEST_DEVELOPER.md:35, 98-101, 125-129` match the RTL and suites. The parser Makefile and README say fifteen defects, which matches its 15 mutants.
- `docs/SOURCE_EVIDENCE.md` anchors check 20 exact.
- **Comment rule (owner 2026-10-15):** I scanned all 1,094 added lines of the delta for lane or bench labels, lane names, review rounds, reviewer IDs and issue-comment IDs. There are no instances; the only label-like tokens are test identifiers (G1, G2, T1, L1, L2).
- R722-1-F1 is wording only.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Parser and engine delta; microcode a)-c) legs; engine 8n/8o/8p and warm-reset phases; companion datapath GET_AS_PATH; 802.1AS-2011 10.3.10.2.1 a)-d), 10.5.3.3.4 NOTE, 10.3.12.1.1, 10.3.12.1.4 i) (Cor1); IEEE 1722.1-2021 7.4.41.2 | R722-1 | c1bc9e21a273fd8506b4806a2470fb7bab13f72f |
| RTL | CLEAN | `KL_gptp_rx_parser.sv`, `KL_gptp_engine.sv`, generator (AST-equal), ROM images (byte-identical), lint, 7 RTL probes, companion shadow/datapath/csr | R722-1 | c1bc9e21a273fd8506b4806a2470fb7bab13f72f |
| Robustness | CLEAN | Empty, duplicate, foreign-head, thisClock-head, out-of-message and over-eight PathTrace shapes; frozen context under chasers; tsn_fuzz `ptp` storms | R722-1 | c1bc9e21a273fd8506b4806a2470fb7bab13f72f |
| Tests | CLEAN | All repository gates at head; full engine arm 84/84 (sharded); parser arm 15/15; tsngen arm 4/4; 14 reviewer probes; 11 parent gates with the companion; author base/head and companion-mutant receipts | R722-1 | c1bc9e21a273fd8506b4806a2470fb7bab13f72f |
| Docs | CLEAN (RESIDUE F1) | INTEGRATION, HDL, TEST, SOURCE_EVIDENCE guides; parser README/Makefile; source comments (comment-rule scan); companion REGISTER_MAP 0x7DC, README, tsn_fuzz README | R722-1 | c1bc9e21a273fd8506b4806a2470fb7bab13f72f |

## Real limits

- **No source bank at this head.** I ran no manager bank and claim none. No hosted check run exists for this commit; the combined status is pending with no contexts.
- **Base-side gates not rerun.** I relied on the author's base records. Base-vs-head ROM identity was established by regeneration.
- **Parent legs I did not run** (author receipts only):
  - `xvlog_gate.py --check`, `sw/builder/test_builder.py`, milan_dp `gptp-lat`, `milan_dp_gptp` (about 83 min), `milan_dp_gm_steps`, csr, gptp_txts;
  - the parent companion mutation arm. Its harness refuses uncommitted trees, and I made no commit.
- **One environment refusal.** A combined background launch of the parent legs was refused by the execution environment. I reran the legs individually.
- **No synthesis.** No out-of-context synthesis was run, so the resource cost of the wider capture and publication (about 129 flops) is unmeasured.
- **No hardware.** Physical calibration was NOT RUN, and no hardware or field evidence was produced. Field skips are not hardware proof.
- **Simulator.** Verilator 5.050 (pinned, identity verified), with `-j 0` mapped to `-j 4` by a scratch wrapper.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base 55680bff, live dev 97aab1d0f28bd753a3e11df6278d5cac54f964dd) with the builder and native banks. Link the receipts on the PR.
- Own hosted and act acceptance.
- Land the milan-fpga companion with the gPTP pin adoption, committed so that the tsn_fuzz freshness gate and the gptp_shadow mutation arm can run against it. If PR #92's companion also touches tsn_fuzz, regenerate `TEST_RESULTS.md` once after both.
- Carry R722-1-F1 to the residue checklist. Route S1-S4 at your discretion.
- Merge needs a second independent positive review.

R722-1 FINISHED
