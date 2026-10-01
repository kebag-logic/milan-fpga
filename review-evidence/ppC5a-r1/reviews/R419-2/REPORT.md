[R419] NEGATIVE - exact head 44a6bb9082d31dbf933087ef007ad78a110e7053

# R419-2 external review: processor PR #140 (lane C5a, AECP deadlines and the scoreboard), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #140. Closes #57; relates to #81 and #84.
- Exact head `44a6bb9082d31dbf933087ef007ad78a110e7053`, tree `1b3a46226efb78feb6d41f4d84c4aa1e46cfc03d`. Source base `0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff` (13 commits); round-1 head `f963fe9a` plus eight round-2 commits (44db34b, 9f0299a, a2d2a24, 5107327, bf9b32d, 49041e6, 88e3459, 44a6bb9).
- Round R419-2: the external reviewer, cleared context, own detached clone. All five lenses applied.

**Verdict: NEGATIVE.** Every round-1 finding of both reviewers is resolved at this head (section 3). The lane's 55-arm campaign, my own round-1 arms and probes, and three new probes all reproduce. One new MINOR is open (F5): a GET_STREAM_INFO served inside a GET_DYNAMIC_INFO is not serialized against an ACMP step of the same sink, but the stand-alone GET_STREAM_INFO is. The classifier's contract comment justifies this with a statement that is false for that getter, and nothing in the tree records it. F5 leaves RTL, Robustness and Docs UNCLEAN. Conformance and Tests are CLEAN.

## 1. Reconstruction, in the prescribed order

1. **Workflow rules.** AGENTS.md and CONTRIBUTING.md from kebag-logic/milan-fpga at dev `e4b771f9`. This repository has neither file. Also this repository's `docs/README.md`.
2. **Issues.**
   - Frozen acceptance: #81 1-4, #57 1-3 and #84 1-4.
   - Assignment comment 5915626788 (round 1).
   - Round-2 rulings, #81 comment 5923634905:
     - F1 is graded for every reachable class;
     - the MVU fault path is fixed in this lane;
     - R418-1 F2, R419-1 F2 and both reviewers' F4 are answered;
     - suggestions are taken or retained with reasons.
   - TAKEN 5923637418; REVIEW READY 5927089371 at this head.
3. **Authorities.**
   - 03 §6: F03.7, the classifier paragraph, and rules (d) and (e).
   - 08 §4 (F08.3 and the measured table), 06 §6.9 and §8.1, 09 §8.3, and 00 REQ-MVU-005 and GAP-03.
   - `KL_pp_scoreboard.sv`, rules (1)-(6), as the encoded matrix.
   - IEEE 1722.1-2021 §7.4.17, §9.3.2.6, Table 7-141 and the clause 9 status tables; Milan v1.2 §5.4.3.3 Table 5.19 and §5.4.3.4. These were read through their in-tree quotations, because the specification PDFs are not in the tree.
4. **Diff.**
   - `git diff 0451d83d..44a6bb90`: 63 files, +3,872/−92.
   - `git diff f963fe9a..44a6bb90`: 31 files. Every RTL hunk (`KL_aecp_engine.sv` +60/−10; comments in `KL_aecp_ucpu.sv` and the top), every test hunk (DL8-DL11, HZ8-HZ12, the new wrapper taps, the tb/ucpu P20 rename), the campaign driver and its 14 new or changed patches, every docs hunk, and `syn/ooc/README.md`.
5. **Public evidence.**
   - kebag-logic/milan-fpga `4fe37ada` `review-evidence/ppC5a-r1`. `author-r2/HANDOFF.md` matches its manifest's published sha256 (`147b84eb…`, path-redacted). `author-r2/PR-BODY.md` (`9171fbeb…`) is identical to the live PR body apart from the trailing newline.
   - The manager's evidence comments: PR #140 comment 5921897578 (round-1 banks) and the round-2 review-start notice 5927195151.
6. **Prior findings.** R418-1 (comment 5921631179) and my own R419-1 (comment 5921721080) were read only after my independent pass over the round-2 diff. Their probe scripts were read from the published packets. No other round-2 review was read.

## 2. Executable evidence produced by this round

Everything ran in the foreground, on a `git archive` export of the exact head under `scratch/` (never in the clone), with the pinned simulator 5.050 (`receipts/tool-identity.txt`).

| Receipt | What | Result |
|---|---|---|
| `receipts/pp_top-full.log` | `make -C tb/pp_top`, all three builds | rc 0, **8,240 checks, 0 FAIL**: default build 8,164 (DL 64, HZ 176, AD 55, …), fixture build 20, timebase build 56. The TB histogram equals 08 §4: worst case 24,681 clocks, 0.103 % of T-AECP-RESP |
| `receipts/ucpu-run.log` | `make -C tb/ucpu run` | rc 0, 415/415 |
| `receipts/pp_top-{deadline,hazards,d3}.log` | the sections run alone | DL 64/0, HZ 176/0, D3 133/0 |
| `receipts/aecp-mutants/` (`summary.txt`, `arm-counts.txt`, four shard logs) | `tb/pp_top/aecp_mutants.py` in four `--only` shards | **5 controls PASS** (every (suite, target) pair passed in every shard that needed it) and **55/55 arms KILLED**, 0 UNPROVEN. Each arm's failing-check count equals the `tb/pp_top/README.md` table, for example `dl-kill-tied-off` 28, `hz-barrier-no-priority` 127, `hz-stub-restored` 74 and `mvu-echo-slot-std` 1 |
| `receipts/reviewer-mutants/` | my round-1 `scripts/reviewer_mutants.py`, unchanged (sha256 equal to the R419-1 manifest) | `r-registry-lock-preempted` **KILLED** (pp_top: 4, all DL10; tb/ucpu survives, as it must, because the exemption is the engine's). `r-kill-ack-keeps-owner` **KILLED** (DL1, and DL11 with 19 stray releases). `r-mvu-no-echo` KILLED (DL3). The three equivalent arms (R419-1 S1) still survive |
| `receipts/probe-hz-reachability-r2.log`, `scripts/probe_hz_reachability_r2.py` | my round-1 reachability arms P0-P4, unchanged, re-anchored after HZ12; plus P2b, P5 and P6 | Results: P0 SUCCESS beside; P1 waits, then SUCCESS; P3 and P4 wait, then NOT_SUPPORTED (11). P2 fails its own premise again. **P2b**: under the TX-pool stall a talker GET_TX_STATE holds its key **2** clocks and a DISCONNECT_TX **15**, where the listener's GET_RX_STATE holds all 3,000 observed. **P5**: a held SET_NAME on STREAM_OUTPUT 1 holds back a GET_TX_CONNECTION of source 1, as the new 03 §6 text says. **P6**: a held REGISTER or DEREGISTER lets a talker GET_TX_STATE and DISCONNECT_TX run beside it. The only 2 failures are P2's premise and its dependent check |
| `receipts/probe-dl-fault-combos.log`, `scripts/probe_dl_fault_combos.py` | the round-2 answer under combined conditions | **D1**: a GET_MILAN_INFO queued past its deadline with the response memory failing reads answers MVU NOT_IMPLEMENTED, echoed byte-exact, 13,396 clocks after reception, with no void counted. **D2**: an ADDRESS_ACCESS and an AVC command under a read error answer NOT_IMPLEMENTED echoed, with no void counted. **D3**: four RX slots are free afterwards and GET_CONFIGURATION answers SUCCESS. DL 70/0 |
| `receipts/probe-gdi-stream-info.log`, `scripts/probe_gdi_stream_info.py` | is a GET_STREAM_INFO inside a GET_DYNAMIC_INFO serialized like the stand-alone one? | **G0** (control, what HZ6 grades): a stand-alone GET_STREAM_INFO STREAM_INPUT 1 waits for a held UNBIND_RX of sink 1 (refused 498 clocks). **G1**: a GET_DYNAMIC_INFO carrying one GET_STREAM_INFO STREAM_INPUT 1 record is **admitted beside** the same held UNBIND_RX (class RO_SNAPSHOT, key 0xFC00, refused 0 clocks) and answers SUCCESS. G2: the same beside a held read. See F5 |
| `receipts/docs-*.log`, `receipts/lint_hdl.log` | `make links matrix modmatrix params`; `scripts/lint_hdl.sh` | rc 0: 1,003 links; 115 REQ rows and 17 GAP findings; 94 module rows, 0 untested; parameters 26/26/26; 41 modules LINT OK |
| `receipts/git-checks.txt` | `git diff --check` from 0451d83d and from f963fe9a; commit shape | Both diff checks empty. All eight round-2 commits have a one-line message, no body, no trailer and one parent. f963fe9a and 0451d83d are ancestors |
| `receipts/interface-checks.txt` | the top's parameter and port header at base vs head; the engine and µCPU headers | **The top header is identical (674 lines).** The `KL_aecp_engine` and `KL_aecp_ucpu` headers are identical between f963fe9a and the head; round 1's internal ports are unchanged. No RTL file was added, renamed or deleted |
| `receipts/hosted-exact-head-snapshot.txt` | read-only, 08:19 UTC | Run 36832325836: `docs-gates` success and `portability` success. In `suites`, lint and every suite succeeded; the campaign steps had not yet run. PR closing references: **[57]** only. Draft false; mergeable CONFLICTING (the merge-main round, as stated) |
| `receipts/tree-integrity.txt` | the clone after every run | HEAD, HEAD tree and index tree are exact. Detached, `status --ignored` empty, 401/401 tracked blobs rehash equal, no mode drift, no assume-unchanged or skip-worktree flags. **0 gitlinks**: this repository has no submodules, so there are no gitlinks to verify |

## 3. Prior public findings: resolved or retained at this head

| Finding | Status | Evidence at 44a6bb90 |
|---|---|---|
| **R419-1 F1 / R418-1 F1** (MAJOR, both): reachable NAME_WR conflict; the false four-class statement; #84 accounting | **RESOLVED** | 03 §6 (`docs/architecture/03_packet_engine.md:236-251`) now states the reachability, which I re-derived from the scoreboard rules and the classifier. ACMP presents only RO_SNAPSHOT and STREAM_CFG on stream keys. NAME_WR conflicts with a legal command. CLOCK_CFG, IDENTIFY and MAP_CFG conflict with an ACMP read only through a stream-typed command. MAP_CFG also conflicts through the class-wide STREAM_CFG cross-lock. REGISTRY_OP conflicts with nothing: its key has type 0x3F, and it falls under rule 6. Every reachable pair is graded on the listener's and the talker's keys (HZ2-HZ12), with 19 new arms, all killed (section 2). My P1, P3 and P4 behave as the text says. **The P2 substitution is accepted.** P2b measures that a talker transaction keeps its key only 2-15 clocks, so the ACMP-held direction cannot be staged by the stall. The scoreboard's conflict function is symmetric and is evaluated against every live hold, so HZ9d and HZ9e (AECP held) grade the same class, key-function and key-equality relation. `hz-name-key-none-talker` and `hz-talker-keyed-as-listener` kill them. My P5 adds the GET_TX_CONNECTION case the text names. The "Relates to #84" line is exact: REGISTRY_OP has no reachable conflict (graded by HZ1 and HZ8), and acceptance 4 is not done (`02_interfaces.md:99` still says "asynchronous assert") |
| **R418-1 F2** (MINOR): status 10 for deadline-killed ADDRESS_ACCESS and AVC | **RESOLVED** | `st_echo_w` (`hdl/aecp/KL_aecp_engine.sv:1705-1707`) covers every type but AEM_COMMAND, at A_RUN (`:3644`). DL9 grades ADDRESS_ACCESS, AVC, HDCP_APM and EXTENDED byte-exact, idle and past the deadline. `dl-non-aem-forced-status-10` is killed (4). My D2 adds the fault path. Unsolicited jobs load protocol AEM with message_type 0 (`:2801-2803`), so `st_echo_w` cannot turn a notification into an echo |
| **R419-1 F2** (MINOR): two surviving kill-seam mutants | **RESOLVED** | DL10, DL1 and DL11. My `r-registry-lock-preempted` and `r-kill-ack-keeps-owner` are now KILLED (section 2), and the author's split arms are killed too |
| **R419-1 F3 / R418-1 F3** (MINOR): REQ-MVU-005 on the fault path | **RESOLVED by the ruled fix** | The A_ALLOC and A_WR rebuilds (`:3692-3701`, `:3724-3731`) answer NOT_IMPLEMENTED with the command echoed from the RX slot. The RX slot is freed only at A_FREE (`:2567`), so it is still held during the echo. A command whose echo needs it takes the oversize slot at grant (`:2548-2554`). `pld_cmd_r` is capped at PLD_MAX_C, so `echo_len_w` cannot overflow 11 bits. DL8 covers the read, write, tied-off and 578-byte cases; `mvu-fault-status-10` (4) and `mvu-echo-slot-std` (1) are killed; my D1 covers the combined case. **Closes #57 is justified**: #57-1 TB1, #57-2 TB3 and TB4, #57-3 DL1 and DL3, plus the ruling's fault path. The other untracked finding in my F3 (the notification hold) is now recorded in-tree: 08 §4, and the F08.3 row reads "not met as written". Its tracking issue remains a manager duty (R418-1 S4) |
| **R419-1 F4 / R418-1 F4** (MINOR): check IDs, HZ banner, `maap_on` | **RESOLVED** | The tb/ucpu deadline checks are P20a-P20h. `"P20a completes: one redirect"` names only the deadline check, and P19 is GET_AUDIO_MAP's alone. Every campaign arm printed exactly one matching named FAIL line (`named=1`). The HZ banner describes the TX-pool stall. `io.maap_on = true` is justified at `tb/pp_top/sim_main.cpp:11556-11559`, and P2b shows why the talker needs it. The doubled prefixes are gone |
| R419-1 S1 (equivalent arms) | taken | Comments at `KL_aecp_ucpu.sv:480-484` and `KL_aecp_engine.sv:1709-1712`. The three arms still survive, as expected |
| R419-1 S2 (TB2 wording) | taken | "all thirteen getters, once each (not a batch that fills the 524-octet response)" (08 §4) |
| **R419-1 S3 (vendor-tool area; judge the register explanation)** | taken; **the explanation holds** | +174 registers: `u_scoreboard` 73→169 (+96), `u_dispatch` +23, `u_normalizer` +18 and the top's own +33, which together account for 170 of the 174. 169 is exactly the full hold table: 8 entries × (4 class + 16 key bits) + 8 valid + 1 barrier-pending (`KL_pp_scoreboard.sv:69`, `.MAX_HOLDS_P(8)` at the top). That is what a table whose class and key inputs were near-constant under the stub, and are now live, must grow to. +33 is the 32-bit deadline register plus the boot-hold bit. BRAM and DSP are unchanged, consistent with a lane that adds no memory. Distributed RAM +16 fits the now-live class and key bits of the dispatch records. I did not reproduce the vendor run; the reports are not public (section 7) |
| R418-1 S1, S2, S3 | taken | 06 §8.1 trade-off; top comment `:1453-1458`; 08 §4 ACMP paragraph (see S6) |
| R418-1 S4 (fan-out tracking issue) | partly taken; retained for the manager with a reason | The F08.3 row is corrected. The author's role may post only TAKEN, REVIEW READY or STOP. The open-issue search finds no tracking issue yet (section 8) |

## 4. Focus questions

- **No port, parameter or parent-visible interface change.**
  - The top's header is byte-identical to base. No RTL port line changed in round 2. No RTL file was added or renamed.
  - The wire behaviour change is listed in the PR's round-2 parent-visible list: every non-AEM AECP type answers NOT_IMPLEMENTED with the command echoed on a fault or past its deadline, and an over-long echo takes the oversize slot.
  - The parent consumer bank at dev `e4b771f9` is the manager's.
- **Closes #57, relates to #81 and #84, with exact remainders.**
  - Closing references are [57] only.
  - #81: acceptance 4 is not done (T-IDENT-BURST, T-IDENT-REARM and T-CTR-OBSERVE have no RTL; the 300 s and 60 s defaults are not pinned).
  - #84: REGISTRY_OP has no reachable conflict, and acceptance 4 is not done.
  - Both remainders are stated exactly in the PR's "What remains".
- **Every processor suite and campaign rc 0 at the head.**
  - Reproduced here: `tb/pp_top` (8,240), `tb/ucpu` (415), the AECP campaign (55/55 with 5 controls), lint and the docs gates.
  - Not reproduced here, by rule (section 7): `run_suites.sh` over all 33 suites and the other campaigns. Those are the author's (HANDOFF §7 and §8) and the manager's donor bank.
- **The register-growth explanation:** holds (section 3, R419-1 S3).

## 5. Findings

### F5 - MINOR - RTL, Robustness, Docs - a GET_STREAM_INFO inside GET_DYNAMIC_INFO bypasses the RO_SNAPSHOT serialization its stand-alone form gets, on a false contract comment

- **Where:**
  - `hdl/top/protocol_processor_top.sv:1464-1466`: "READ_DESCRIPTOR … and GET_DYNAMIC_INFO several at once, so both take the NONE key: no ACMP step writes a field either serves". GET_DYNAMIC_INFO falls to the classifier's default NONE key at `:1501`.
  - `docs/architecture/03_packet_engine.md:226-231` gives GET_DYNAMIC_INFO the no-descriptor key without stating what that excludes.
- **Authority:**
  - F03.7 (`03_packet_engine.md:203`): RO_SNAPSHOT covers "all GETs", is keyed by the "addressed descriptor", and is "blocked only vs in-flight write on the same key".
  - HZ6 grades this for a stand-alone GET_STREAM_INFO, and the classifier keys that getter by its descriptor for exactly this reason.
- **Evidence:**
  - GET_DYNAMIC_INFO serves GET_STREAM_INFO records for STREAM_INPUT and STREAM_OUTPUT (`hdl/aecp/KL_aecp_engine.sv:1085-1093`).
  - A STREAM_INPUT's stream-info status words come from the listener's binding record, written by ACMP listener steps (`protocol_processor_top.sv:3341-3352`, `lstn_recwr_w`).
  - So "no ACMP step writes a field either serves" is false for GET_DYNAMIC_INFO.
  - Probe G1 (`receipts/probe-gdi-stream-info.log`): a GET_DYNAMIC_INFO carrying GET_STREAM_INFO STREAM_INPUT 1 is admitted beside a held ACMP UNBIND_RX of sink 1, while the stand-alone GET_STREAM_INFO (G0) waits for it.
  - The PR body's "What remains" discloses that GET_DYNAMIC_INFO and READ_DESCRIPTOR "are not serialized against an ACMP step on a member stream". The tree does not. A merged PR body would be the only record, while the code comment asserts the gap is harmless.
- **Impact:**
  - A controller's GET_DYNAMIC_INFO can read a sink's stream info while an ACMP step of that sink is in flight. That is the inconsistent snapshot F03.7's RO_SNAPSHOT rule exists to prevent, and which the stand-alone getter is protected from.
  - A maintainer trusting the comment would not look for it.
  - I did not demonstrate a torn record. The admission gap itself is demonstrated.
  - For READ_DESCRIPTOR the statement holds as far as I checked: no ACMP step writes descriptor-image fields.
- **Required outcome:** either of these.
  - Make the comment true and record the limitation in the tree: in 03 §6 beside the no-descriptor-key sentence, and as a tracked remainder (an issue, or #84's recorded remainder).
  - Or serialize a GET_DYNAMIC_INFO whose records name a stream descriptor against ACMP steps of that stream.
- **Verification:** the comment and 03 §6 at the new head match `probe_gdi_stream_info.py`'s result. If the RTL changes instead, a HZ check grades it with a failing arm.

### Suggestions (no effect on coverage)

- **S6 (Docs).** In the 08 §4 paragraph (`docs/architecture/08_timing.md:187-196`), the ACMP wait is "bounded only by the AECP command's own budget: up to `T-BUDGET-AECP-WC` … plus its forced response". Two of the three conflict examples it names are not preempted: LOCK_ENTITY, and MAP_CFG through the cross-lock. Past their deadline they run to their own end, each op watchdog-bounded. Consider saying "plus its forced response or, for a command that is never preempted, the rest of its watchdog-bounded program". The real-time conclusion (a few milliseconds, inside T-ACMP-CMD) is unchanged.

## 6. Per-lens results at 44a6bb9082d31dbf933087ef007ad78a110e7053

- `[R419] PASS Conformance`.
  - Artifacts: #57-1..3 against TB1, TB3, TB4, DL1, DL3 and DL8; #81-1..3 against DL and TB; #84-1..3 against HZ1-HZ12 and 03 §6.
  - Rule (e) key release (DL1, `dl-released-before-queued`).
  - The REQ-MVU-005 status set on the deadline, fault and combined paths (DL3, DL8, D1). Every non-AEM type under Table 9-2 and Table 7-141 (DL9, D2).
  - The #81 and #84 remainders, and the closing references.
  - No open finding.
- `[R419] UNCLEAN RTL` (F5).
  - Otherwise checked: `KL_aecp_engine.sv` `st_echo_w` (:1705), the A_RUN remap (:3644), the A_ALLOC and A_WR rebuilds (:3692-3731), and the oversize request (:2548-2554).
  - In those: the echo from a still-held RX slot, `rsp_fail_w` gated by `echo_r` so no double rebuild, no 11-bit overflow, a stable oversize flag through A_ALLOC, and unsolicited jobs excluded from `st_echo_w`.
  - The top's classifier and its reachability against `KL_pp_scoreboard.sv` rules (1)-(6), symmetry included.
  - Round 2's comment-only RTL edits. Interface headers unchanged; lint 41/41.
- `[R419] UNCLEAN Robustness` (F5: a member read admitted beside a write of its sink).
  - Otherwise checked: memory faults combined with the deadline (D1); non-AEM types under faults (D2); slot and RX-slot leakage after faults (DL8, D3).
  - The kill-ack and RX-return ordering, with stray releases graded (DL1, DL11).
  - Short talker holds (P2b); over-serialization of malformed stream-typed commands (HZ12, P3, P4).
- `[R419] PASS Tests`.
  - Artifacts: `tb/pp_top/sim_main.cpp` DL8-DL11 and HZ8-HZ12, and the wrapper taps (`tb/pp_top/pp_top_wrap.sv`).
  - `tb/ucpu` P20.
  - `aecp_mutants.py` and all 55 arms, reproduced with counts equal to the README; named-check uniqueness.
  - My round-1 arms (2 formerly surviving, now killed; 3 equivalent).
  - The full `tb/pp_top` and `tb/ucpu` runs.
  - Every check I read can fail for its claimed defect (its arm fails it). No open finding.
- `[R419] UNCLEAN Docs` (F5).
  - Otherwise checked against the RTL and the measured numbers: the round-2 hunks of 00 (REQ-MVU-005, GAP-03), 03 §6, 06 §6.9 and §8.1, 08 §4 (S6 only), 09 §8.3, both guides, `tb/pp_top/README.md` (campaign table equal to my counts) and `tb/ucpu/README.md`.
  - `syn/ooc/README.md` (arithmetic and structure).
  - The PR body and author-r2 HANDOFF.
  - `make links matrix modmatrix params` rc 0.

## 7. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #57, #81 and #84 acceptance; 03 §6 rule (e) and F03.7; 06 §6.9 and §8.1; 00 REQ-MVU-005; DL1-DL11, TB1-TB5 and HZ1-HZ12 results; probes D1, D2, P0-P6; PR closing references | R419-2 | 44a6bb9082d31dbf933087ef007ad78a110e7053 |
| RTL | UNCLEAN (F5) | `KL_aecp_engine.sv` (round-2 hunks in full and their fan-in), `KL_aecp_ucpu.sv`, `protocol_processor_top.sv` classifier, pick, owners and deadline block, `KL_pp_scoreboard.sv` matrix, interface headers, lint | R419-2 | 44a6bb9082d31dbf933087ef007ad78a110e7053 |
| Robustness | UNCLEAN (F5) | probes D1-D3, G0-G2, P2b, P3 and P4; DL1, DL8 and DL11; HZ12 | R419-2 | 44a6bb9082d31dbf933087ef007ad78a110e7053 |
| Tests | CLEAN | `tb/pp_top` DL, HZ and TB sections and the wrapper taps; `tb/ucpu` P20; the 55-arm campaign and 14 new or changed patches; reviewer arms; full `tb/pp_top` (8,240) and `tb/ucpu` (415) | R419-2 | 44a6bb9082d31dbf933087ef007ad78a110e7053 |
| Docs | UNCLEAN (F5) | round-2 docs diff (00, 03, 06, 08, 09, integrator, operator), the `tb/pp_top` and `tb/ucpu` READMEs, `syn/ooc/README.md`, the PR body, author-r2 HANDOFF, docs gates | R419-2 | 44a6bb9082d31dbf933087ef007ad78a110e7053 |

## 8. Real limits

- **Simulator path.** The instructed pinned path (`$VALIDATION_STORAGE/tmp/372-manager-candidate1/pinned-tool-bin`) does not exist on this host. I used the sibling `372-manager-r2` wrapper, which reports 5.050 rev v5.050 (hashes in `receipts/tool-identity.txt`). The host default (5.052) was not used.
- **Build parallelism.**
  - The first `gsi-build` of the head ran with the Makefile's `-j 0`, before I capped the scratch copy. That one build exceeded 8 jobs.
  - Every later build was capped in the scratch Makefiles: `-j 8` alone; `-j 2` in each of four campaign shards; `-j 2` in each of three reviewer-arm groups.
  - The cap is the only byte that differs from the head in the scratch export.
- **Not run, by rule.**
  - `run_suites.sh` over all 33 suites.
  - The D3, SRP, ADP, GSI, name-write, retry, SRP-admission, descriptor-guard and NVM-figure campaigns. Round 2 changes no RTL any of them exercises apart from the engine; the AECP campaign's `d3` control and `dl-boot-hold-not-exempt` arm did run.
  - `make lint` (diagrams), `wavedrom-check` and `make stale`.
  - Yosys, and any parent, builder or donor gate.
- **Area figures.** The vendor area figures are the author's. Their reports are not public, and I judged only their arithmetic and structure.
- **Specification clauses** are read through in-tree quotations; the PDFs are not available.
- **F5** demonstrates the admission gap, not a torn record.
- **Hosted CI** was observed once, read-only: `suites` was still running its campaign steps.
- **Hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.

## 9. Pending manager duties

- Rule on F5. The author fixes it, or decides it publicly, at a new head that this reviewer re-reviews.
- Open the tracking issue for the `KL_aecp_notify` notification hold (R418-1 S4; recorded in-tree at 08 §4).
- Exact-head hosted and act acceptance. The `suites` campaign steps were pending at the snapshot.
- The donor bank and the parent consumer set at milan-fpga dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`.
- The merge-main round: this branch conflicts with processor main `3f3ea56b` (C2 + C4). It was judged here on base `0451d83d`. Build the final current-dev candidate at the merge turn, distinct from this source validation.
- A second independent positive review at the final head.
- Publish this packet: `REPORT.md` plus the files listed in `MANIFEST.sha256`.

R419-2 FINISHED
