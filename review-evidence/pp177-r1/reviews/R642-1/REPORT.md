[R642] POSITIVE - exact head 6aaec5dfc45e84c8842f3f31f76910bfa91a96e1

# R642-1: internal independent review of PR #182 (Closes #177)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head 6aaec5dfc45e84c8842f3f31f76910bfa91a96e1, tree 5f7ae4960def91d88b3c4c053a94c021c1d3e955 (verified in the review clone: `rev-parse HEAD`, `HEAD^{tree}` and `write-tree` agree)
- Source base: processor main 22c139a4323bc96c779d13e3f6774480c5fb9b75. The delta is one commit, 20 files, +313/-44.
- Review start: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/182#issuecomment-6241834678
- Round R642-1, cleared context, all five lenses applied independently.

## Verdict

POSITIVE at the exact head. No BLOCKER, MAJOR or MINOR finding is open. The review records two RESIDUE wording items and two SUGGESTIONs; under the owner rules none of them makes the verdict NEGATIVE.

The change does what #177's frozen acceptance asks:

- A GET_AVB_INFO whose descriptor_type is not AVB_INTERFACE now answers NOT_IMPLEMENTED (status 1). The response is the command echoed at its own control_data_length, which is how 06 §8.2 reads §9.3.5.3.3's "correctly sized response".
- AVB_INTERFACE still answers SUCCESS.
- An absent AVB_INTERFACE index still answers NO_SUCH_DESCRIPTOR.
- A command under cdl 16 still answers BAD_ARGUMENTS.
- In the engine the change is confined to the GET_AVB_INFO arm of the A_PLD-exit re-dispatch, plus one comment block that counts the NOT_IMPLEMENTED assignment sites.
- Every new check has a planted mutant that fails it by name. I re-ran all nine new dispatch arms and the new decode control at this head, and every one was killed.
- The compliance review records the owner decision with every clause the issue lists.

## How the review was reconstructed

1. The processor repository has no AGENTS.md or CONTRIBUTING.md at this head (`git ls-files` shows none). The authoring conventions came from docs/README.md: reading order, ID registries, single-source rules and what `make check` enforces.
2. Issue #177: the body (owner decision 2026-10-17, the clause trace, "Done when") and the assignment comment (keep the change in the GET_AVB_INFO arm, since a separate lane works in the same engine file; STOP on a register-map, port or parameter change).
3. Authorities, read in the local IEEE 1722.1-2021 and Milan v1.2 Consolidated (2023-11-30) texts. The source PDF digests are in `receipts/authorities-and-evidence.txt`; the text is not republished.
   - 7.4.40.1: "descriptor_type is AVB_INTERFACE". Verified.
   - 7.4.40.3: names only NOT_AUTHENTICATED. Verified.
   - Table 7-141: status 1 NOT_IMPLEMENTED is "does not support the command type"; status 11 NOT_SUPPORTED is "implemented but the target ... not supported". Verified.
   - 9.3.5.3.3: "correctly sized response and a status of NOT_IMPLEMENTED". Verified.
   - Milan 5.4.2.23: "as specified in [ATDECC, Clause 7.4.40]", with nothing on a wrong descriptor. Verified.
   - The issue's clause trace is accurate.
4. The diff 22c139a4..6aaec5df and its one-commit history.
5. The author's published evidence at kebag-logic/milan-fpga@9d301680a42cd2d736a5d16085cc84a2480a7128 `review-evidence/pp177-r1`: MANIFEST.json, HANDOFF.md, PR-BODY.md, EXTERNAL-ARTIFACTS.csv and parent-evidence-classification.patch. Their digests are recorded.
6. PR #182 body and comments. The PR has no earlier public review findings: 0 reviews, 0 review comments, and its issue comments are the two review-start notices. A concurrent second-reviewer report (R643-1) was posted on the PR during this round. To keep the two reviews independent, it was **not read** before or while writing this verdict and ledger; the manager reconciles the two.

## Reviewer execution at the exact head

- Every run used the scoped Verilator 5.050 wrapper. Its `--version` reports "Verilator 5.050 2026-07-01 rev v5.050", and the binary it execs has sha256 44898b22af4178b45214a0820a04eeac8632ae721ff005e69ef1cf69121bbfdd, the same as the author's receipt.
- Campaigns ran concurrently, each with its own log and rc file (`scripts/run_all.sh`), with `--jobs` passed to every driver.
- Disposable trees went under the packet's `scratch/`.

| Run | Result | Receipt |
|---|---|---|
| `tb/pp_top/aecp_dispatch_mutants.py --jobs 3`, every arm | rc 0; 4 positive controls PASS; 49 arms KILLED; "53 checks: 53 PASS, 0 FAIL". The 9 new arms fail with these counts: m9-guard-get-avb-info 14, gavb-other-type-not-supported 13, gavb-other-type-header-only 13, gavb-type-gate-dropped 13, gavb-type-low-byte 2, gavb-interface-not-implemented 16, gavb-locate-miss-ignored 1, gavb-padded-refused 2, gavb-floor-14 1. Each count equals the tb/pp_top README table and the author's HANDOFF | `receipts/dispatch-campaign.{log,rc}`, `receipts/results/dispatch-campaign.results.json`, `receipts/results/dispatch-*.FAIL-lines.txt` |
| `tb/aecp_cmds/mutants.py --jobs 3`, all 17 standing controls | rc 0; "17 of 17 detected by their named failures; golden and restored PASS", gavb-other-type-not-supported included | `receipts/decode-controls.{log,rc}`, `receipts/results/decode-controls.results.json` |
| `make -C tb/pp_top run` (all seven builds), on a local clone at the exact head | rc 0; "10483 checks: 10483 PASS, 0 FAIL", default build 9989. Both equal the author's head figures (base 9976, +13 = V5's 12 extra rows and V1b) | `receipts/pp-top-run.{log,rc}` (home paths redacted to `$HOME`) |
| `make -k links matrix reqtags modmatrix params aecpcmd ids figures stale lint` | rc 0. links 1193 OK; matrix OK (115 REQ rows; 94 module rows, 0 untested); req-tags OK; aecpcmd: self-test 231 of 231 caught, 31 commands, 84 entries walked and observed, F06.14 41 rows OK; ids 587 files OK; figures OK; lint 41 mermaid + 18 wavedrom OK | `receipts/make-check-gates.{log,rc}` |
| `scripts/lint_hdl.sh`, `scripts/check_upc_map.py`, `scripts/check_m9_opcodes.py` | rc 0 for all three. UPC MAP GATE PASS (61 constants, 89 entries); M9 OPCODE GATE PASS (30 opcodes) | `receipts/lint-hdl.*`, `receipts/check-upc-map.*`, `receipts/check-m9-opcodes.*` |
| Reviewer probe arms on the exact-head dispatch driver (`scripts/probe_dispatch.py`, patches in `probes/dispatch/`) | Control PASS. `p-gate-on-desc-ty` KILLED (V1, V1b, V3). `p-floor-15` survives the target, and the decode sweep catches it. `p-gate-ignores-bit12` survives the target and is caught only by the decode record's source digest (S1). `p-wrong-type-arm-empty` survives, which is expected: it is an equivalent mutant, because the pop-time default for 0x0027 is already the NOT_IMPLEMENTED echo. That confirms the engine comment's "keeps" | `receipts/probe-dispatch.*`, `receipts/results/probe-dispatch*` |
| Reviewer probe edits on the exact-head decode controls (`scripts/probe_decode.py`) | Golden PASS. `p-floor-15` DETECTED ("shortest AEM 0x0027 ... dispatches to GAVB is cdl 15, the table's command cdl is 16"). `p-gate-on-desc-ty` DETECTED. `p-gate-ignores-bit12`: no GET_AVB_INFO behaviour finding; its only FAIL is the "decode.json is not what the engine does: sweep inputs hdl/aecp/KL_aecp_engine.sv" digest line (S1) | `receipts/probe-decode.*`, `receipts/results/probe-decode*` |
| Review clone integrity after all runs | HEAD, tree and write-tree are exact. No tracked, untracked or ignored change. Index (mode, blob, path) is identical to the head tree. 0 worktree blobs differ from the index; 0 file modes differ. The processor tree has no gitlinks (0 entries of mode 160000), so no submodule gitlink applies | `receipts/clone-integrity.txt` |
| Hosted checks at the exact head (inspected, not owned) | Executed for both push and pull_request runs: portability success, docs-gates success. **suites in_progress** at inspection time. No skipped context was counted as a pass | `receipts/hosted-check-runs.txt` |

## Lenses

### Conformance: CLEAN

- **Behaviour.** `hdl/aecp/KL_aecp_engine.sv:3391-3400` gates the full 16-bit `cfg_ix_r` (bytes @24..@25, the descriptor_type; captured at `:3631-3632`) against `DT_AVB_INTERFACE_C` once the cdl ≥ 16 floor holds. A mismatch selects `UPC_NOTIMPL_C` with `echo_r` 1. Status 1 is what the owner decision chooses. Of the readings §9.3.5.3.3 leaves open, the reflected-command size is the one 06 §8.2 adopts, and it is what the reference controller checks for a NOT_IMPLEMENTED payload (06 §8.2).
- **Refusal order.** Length, then type, then existence: 06 §6.10 states it, and V5's absent CLOCK_DOMAIN 5 row tests it. A wrong type therefore never reaches E_GAVB's locate, and NO_SUCH_DESCRIPTOR remains specific to AVB_INTERFACE (V3; E_GAVB `DESC_ADDR` → `BR_STATUS`, gen_ucode.py:1370-1372).
- **Unsolicited path.** Unsolicited GET_AVB_INFO goes A_IDLE → A_DISP with `rx_slot` NULL (`:2857`) and never reaches this A_PLD-exit arm, so notifications are unaffected.
- **Other message types.** `gavb_w` stays guarded on `aem_w` (`:1344-1345`), so non-AEM message types keep the generic echo (M9).
- **Decision record.** `docs/00_MILAN_COMPLIANCE_REVIEW.md:596` (§8 item 12) records the decision with 7.4.40.1, 7.4.40.3, Table 7-141 status 1 versus 11, 9.3.5.3.3 and Milan 5.4.2.23. Each was checked against the local standards text.
- The command model's status set and entries (`hdl/aecp/ucode/aecp_commands.json:313,317`) match the engine, and the observed sweep matches the record (`aecpcmd` OK; decode.json `NOTIMPL {floor 16, cdls 16-100, {1: echo}}`).

### RTL: CLEAN

- **Confinement.** In the engine the delta touches only the GET_AVB_INFO arm (`:3383-3400`) and the comment block that bounds the NOT_IMPLEMENTED sites (`:1282-1290`). `hdl/top`, `hdl/common` and `ucpu_pkg.sv` are untouched, and no port, parameter or register map changes. The ROM is byte-identical: `make check` aecpcmd passes, and the author's digests are identical at base and head. The other lanes' commands in the same file (#176 SET_STREAM_INFO and the others) are not touched; merge interaction is the manager's at the candidate.
- **The bounding comment's count.** `UPC_NOTIMPL_C` is assigned to `upc_w`/`upc_r` at exactly three sites (`:1320`, `:3294`, `:3394`), which is what the updated comment says. The two `g_sub_upc_w` defaults (`:1114`, `:1184`) are a different signal and were already there at base.
- **`gavb_r` stays set on the refusal.** Nothing reaches the integrator face: `gsi_req_o` needs `gx_req_w`, which only a GATHER µop raises, and E_NOTIMPL runs none (`:2211-2216`).
- **Explicit assignments.** The explicit `upc_r`/`echo_r` assignments in the wrong-type arm repeat the pop-time default (an equivalent mutant, as probed). They make the intent explicit; this is not a defect.
- Lint (`lint_hdl.sh`) and the elaboration-facing gates in my runs pass.

### Robustness: CLEAN

- **Each input class has one defined answer.** cdl 12-15 answers BAD_ARGUMENTS. At cdl 16-100, every swept descriptor_type (0x0000-0x0028 and 0xFFFF) gets the NOT_IMPLEMENTED echo, except AVB_INTERFACE, which gets SUCCESS or NO_SUCH_DESCRIPTOR (the recorded sweep). A padded AVB_INTERFACE command draws the unpadded answer (V1b). A padded wrong-type command is echoed whole at its own length (V5's padded row).
- **Long commands.** Their echo length comes from the generic reflect path (06 §8.2 length sweep), which this change does not alter.
- **Floor probe.** A floor moved to 15 is caught by the recorded decode sweep (reviewer probe); a floor moved to 14 is caught by V4 (author arm).
- Reset and unsolicited behaviour are unchanged.

### Tests: CLEAN

- **New cases.**
  - V1b: padded AVB_INTERFACE, byte-exact.
  - V5: 13 byte-exact NOT_IMPLEMENTED echo rows at cdl 16 and 20. They cover ENTITY, CONFIGURATION, AUDIO_UNIT, both STREAM types, both neighbours of AVB_INTERFACE, CLOCK_DOMAIN, an absent CLOCK_DOMAIN index, 0x0109, 0x8009, 0xFFFF and a padded CLOCK_DOMAIN.
  - M9's 0x0027 row now carries a real AVB_INTERFACE 0 body, which is needed now that the wrong-type refusal is byte-identical to M9's expected echo.
  - The `dispatch_cases()` focus gives the mutation driver a booted model without double counting in the main run.
- **Mutant coverage.** Every new check has a planted mutant that fails it by name, and every one was re-killed at this head (see above). The README failing counts match my results exactly.
- **Gap.** S1 is a coverage-depth suggestion, not an acceptance gap.

### Docs: CLEAN (two RESIDUE items, one SUGGESTION)

- 06 §6.10 (`docs/architecture/06_aecp_engine.md:889-901`), the §8.1 inventory row (`:1252`), F06.14 (`:276`, regenerated, gate OK), 09 §8 (`docs/architecture/09_verification.md:574`, control count "fifteen more edits" = 17 − q1 − q2), the compliance review §8 item 12, the tb/aecp_cmds README and mutants.py docstring, and the tb/pp_top README sections are consistent with the RTL and the tests.
- **Comment rule.** A scan of every added line found no bench lane label, lane name, review round, reviewer ID or issue-comment ID in any new source comment. The only label-like token on an added line is the pre-existing "R608-1's q1" in docs 09 `:574`. That text is unchanged from base on an edited line, it is in a document rather than a source comment, and it is not a new instance (tracked class #746).
- Two prose wording slips (RES-1, RES-2) and one pre-existing scope sentence (S2) are recorded below.

## Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R642-1-RES-1 | RESIDUE | Docs, Tests | `tb/pp_top/README.md:760` | `sim_main.cpp` V5 `kRows`: 12 rows at cdl 16 cover 11 distinct types plus an absent CLOCK_DOMAIN index | Prose only: the README calls the twelve cdl-16 rows "twelve types" while listing an absent index among them. No count, check or verdict changes | Replace "twelve types (the image's other descriptors, ..., 0xFFFF and an absent CLOCK_DOMAIN index) at cdl 16" with "twelve rows at cdl 16 (eleven types: the image's other descriptors, ..., 0xFFFF; and an absent CLOCK_DOMAIN index)" | Read the sentence against V5's row table |
| R642-1-RES-2 | RESIDUE | Docs, Tests | `tb/pp_top/README.md:1405-1406` | `receipts/results/dispatch-gavb-type-low-byte.FAIL-lines.txt`: the arm fails 0x0109 and 0x8009 only; 0xFFFF also differs above bit 7 and still passes | Prose only: "the two types that differ from AVB_INTERFACE above bit 7" also fits 0xFFFF. The stated count (2) and the named rows are right | Replace with "the two types that differ from AVB_INTERFACE only above bit 7 (0x0109 and 0x8009)" | Read against the arm's FAIL lines |
| R642-1-S1 | SUGGESTION | Tests | `tb/pp_top/sim_main.cpp` V5 `kRows`; `tb/aecp_cmds/sim_main.cpp:272-276` (`desc_types()` = 0x0000-0x0028, 0xFFFF) | Reviewer probe `p-gate-ignores-bit12` (`(cfg_ix_r & 16'hEFFF) != DT_AVB_INTERFACE_C`) survives the `aecp-dispatch` target and is caught by tb/aecp_cmds only through the engine source digest, not by any GET_AVB_INFO observation (`receipts/results/probe-*-p-gate-ignores-bit12*`). Bits 8 and 15 are covered (0x0109, 0x8009); bits 9-14 are not | A partial type compare that ignores one of bits 9-14 would go undetected by behaviour. The RTL is a plain 16-bit `!=`, so there is no defect today | Optionally add walking-one V5 rows 0x0209, 0x0409, 0x0809, 0x1009, 0x2009, 0x4009, or add AVB_INTERFACE's single-bit neighbours to `desc_types()` | Re-run `probe_dispatch.py` with `p-gate-ignores-bit12`; it should be KILLED |
| R642-1-S2 | SUGGESTION | Docs, Conformance | `docs/architecture/06_aecp_engine.md:1545-1546` (§8.2) | §8.2 says "The generic NOT_IMPLEMENTED sizing below applies only to commands outside the served inventory". The served GET_AUDIO_MAP wrong-type refusal already used it at base, and #177's text (06 §6.10, the compliance review item 12) now cites §8.2 as the sizing for GET_AVB_INFO's wrong-type refusal | Pre-existing scope sentence, made narrower than the engine's real use. The delta's own statements are accurate | In a follow-up, widen the sentence to name the served commands' wrong-type NOT_IMPLEMENTED refusals (GET_AUDIO_MAP, GET_AVB_INFO) | Read §8.2 against 06 §6.5 and §6.10 |

No other finding. No earlier public review finding exists on this PR to resolve or retain.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #177 trace against the local IEEE 1722.1-2021 7.4.40/.1/.2/.3, Table 7-141, 9.3.5.3.3 and Milan v1.2 5.4.2.23; `KL_aecp_engine.sv:1282-1345,2857,3383-3400,3631-3632`; `gen_ucode.py:1356-1385`; `aecp_commands.json:309-318`; `decode.json:25,158`; compliance review §8 item 12; 06 §6.10, §8.1, §8.2 | R642-1 | 6aaec5dfc45e84c8842f3f31f76910bfa91a96e1 |
| RTL | CLEAN | Full engine delta; `UPC_NOTIMPL_C` sites; gsi/ctr face routing (`:2179-2220`); unsolicited load (`:2870-2930`); `hdl/top`/`hdl/common`/`ucpu_pkg.sv` untouched; lint, UPC-map and M9-opcode gates; aecpcmd ROM consistency; 4 reviewer probe arms | R642-1 | 6aaec5dfc45e84c8842f3f31f76910bfa91a96e1 |
| Robustness | CLEAN | Length/type/existence ordering; padded and truncated commands; recorded sweep (cdl 12-100, types 0x0000-0x0028 and 0xFFFF); non-AEM message types (M9); unsolicited path; reviewer floor and gate probes on both drivers | R642-1 | 6aaec5dfc45e84c8842f3f31f76910bfa91a96e1 |
| Tests | CLEAN | `tb/pp_top/sim_main.cpp` V1, V1b, V3, V4, V5, M9, `dispatch_cases`, focus run; 9 new dispatch patches and driver rows; the tb/aecp_cmds control; full dispatch campaign (53/53), decode controls (17/17), pp_top main run (10,483 PASS), reviewer probes | R642-1 | 6aaec5dfc45e84c8842f3f31f76910bfa91a96e1 |
| Docs | CLEAN | 06 F06.14/§6.10/§8.1/§8.2; 09 `:574`; compliance review §8; tb/pp_top and tb/aecp_cmds READMEs; mutants.py docstrings; source-comment label scan of every added line; `make check` subset (links, matrix, reqtags, modmatrix, params, aecpcmd, ids, figures, stale, lint) | R642-1 | 6aaec5dfc45e84c8842f3f31f76910bfa91a96e1 |

## Real limits

- **Full suite banks not run.** As instructed, I did not run the full processor `run_suites.sh` bank, the Yosys/sv2v netlist flow, the guard campaigns, the other 12 campaigns the author lists, or any parent, gPTP or builder bank. For those, the source-head evidence is the author's published gate receipts (HANDOFF.md and EXTERNAL-ARTIFACTS.csv). Their log bodies are not published, so only their digests and stated figures could be compared. Where I did re-run gates, the figures agree with the author's.
- **`make check` coverage.** `wavedrom-check` was not run locally: its renderer bootstraps a package environment this review does not install. The hosted docs-gates job at the exact head completed with success; that job runs `make check`.
- **Hosted suites job.** It was still in progress when inspected, so no hosted suites result is claimed.
- **No manager source bank** runs at this exact head, and none is claimed or inferred.
- **Physical calibration** was NOT RUN, and field skips are not hardware proof. No hardware was used.
- **Parent consumer gates.** The author ran these on a scratch parent at dev 7d79ffb2, not at the live dev e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f. The parent evidence gate passed only with an uncommitted two-classification patch, which the author attaches; the base needed the same patch, and the pre-existing refusal is independent of #177.
- **Concurrent review not read.** The R643-1 report on this PR was not read, to keep the reviews independent.

## Pending manager duties

- Build and validate the current-dev merge candidate: source base 22c139a4, live dev e9cbb676. This includes the builder and native banks and the 17 parent consumer gates, with the reader classifications the parent evidence gate needs adopted on dev. Link the receipts on the PR.
- Accept the hosted and act contexts at the exact head, including the hosted `suites` job, which was in progress here.
- Resolve merge order and conflicts with the lanes in the same engine file (#176, #178, #181), and re-check that the GET_AVB_INFO arm stays intact after the merge.
- Carry R642-1-RES-1 and R642-1-RES-2 to the residue checklist.
- Reconcile this report with R643-1.

R642-1 FINISHED
