[R473] NEGATIVE - exact head 91cef52b3c56cc69f66966b004782a69d2940a46

# R473-1: external independent review of processor PR #156 (lane C11: #27, #70, #75; #71 acceptance 1 and 3)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #156, base `main` `c050d97153dd0480ae741102c1647eeda9b7f273` (still the tip of `main` at review time; the head is 5 ahead, 0 behind).
- Exact head `91cef52b3c56cc69f66966b004782a69d2940a46`, tree `1033d92b04474001548689b20e1e0e4fe13a7966`, reviewed in an isolated detached clone. The clone was only read; at the end HEAD, tree, index tree and every tracked blob re-hash equal the head, and status is empty (`receipts/clone-integrity.txt`). The processor has no submodule gitlinks.
- Review start: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/156#issuecomment-5981953744

**Verdict: NEGATIVE.** Two MINOR findings are open: F1 (the ID gate passes a braced list whose member is a hyphenated ID with no row) and F2 (the figure gate's self-test does not plant three faults that 09 §7 says it plants). Both were first reported by the internal reviewer. I reproduced both independently at this head, and I retain them (section 3). Everything else in scope holds:
- the architecture pages name only landed ports;
- the RX face shows no backpressure;
- the word-stream history is verbatim, linked, and its permalinks resolve;
- the three `hdl/`/`tb/` code edits are comment-only;
- `make ids` and `make figures` catch every planted stray and fault I tried in their documented forms;
- the docs-gates CI job runs `make check`, and 09 §7 matches it;
- 02 §2 rule 5 is byte-identical to the base.

Ordering, stated plainly: my independent pass, frozen before I read any other review (`receipts/independent-verdict-before-prior-findings.md`), was POSITIVE. In that pass I saw both behaviours. I had graded the braced-list fallback and the self-test survivors as SUGGESTIONs. After resolving the prior findings, I re-grade both as MINOR, for the reasons in section 3.

## 1. Reconstruction

1. **Conventions.** The repository tracks no `AGENTS.md` or `CONTRIBUTING.md` (`git ls-files` finds none). Its conventions come from `README.md`, `docs/README.md` (sections 1 to 6) and the Makefile.
2. **Scope.** The frozen acceptance lists of issues #27, #70, #71 and #75, the manager's lane comment on #27 (issuecomment-5980174687), and the PR body. From the lane comment: #71 acceptance 2 (02 §2 rule 5) belongs to the #81/#84 lane, and rule 5 must stay untouched.
3. **Authorities.** `hdl/top/protocol_processor_top.sv` (the ports), `KL_pp_side_port.sv`, `KL_pp_nvm_port.sv`, `KL_pp_trace_ring.sv`, `KL_acmp_talker.sv`, and F01.5 and F08.1.
4. **Diff and history.** `git diff c050d971..91cef52`: 28 files, 5 commits.
5. **Public evidence.** The `review-evidence/ppC11-r1` packet of kebag-logic/milan-fpga at `4a3ae4a1`. Its manifest sha256 values match the fetched `author/HANDOFF.md` and `author/PR-BODY.md`, and the live PR body equals the published one. Also the hosted run logs at this head.

## 2. Acceptance, item by item

| Issue | Item | Result | Evidence |
|---|---|---|---|
| #27 | current architecture pages show only landed ports | met | `scripts/port_names.py`: every backticked `*_i`/`*_o` name on `docs/architecture/*.md` is a declared port under `hdl/`, 0 missing (`receipts/port-names-architecture.txt`). All 109 on 02 are ports of `protocol_processor_top`. At the base, 02 still named the module-internal `dev_gnt_i` (`receipts/port-names-architecture-BASE.txt`). Planted control: `rx_err_i` is MISSING and `rx_ready_o` is flagged internal (`receipts/port-names-planted-control.txt`). §3, §7 and §8 tables checked against the RTL: the byte faces; `host_*` (accept in IDLE, strobe at least one cycle later, exactly one per request, `rdata` 0 and `err` on a refused access, `rvalid` low while idle); `nvm_dev_*` (op codes 0/1/2, 3 reserved; ERASE len 0 = whole region; one-cycle done/err). The trace-ring lane order matches `trc_rd_lane_w = addr[1:0]`, lane 0 = [127:96] |
| #27 | RX documentation shows no backpressure | met | 02 §3 table and "RX has no backpressure"; F02.3 redrawn with no ready (render viewed); integrator guide §3; no `rx_ready`/`rx_err`/`rx_sof` remains outside `docs/history` except the integrator's "There is no `rx_ready`" |
| #27 | word-stream history discoverable | met | `docs/history/02-class-a-word-stream.md`: prose, table and both WaveDrom sources are verbatim from the base (scripted substring check), and the original captions are quoted exactly. Linked from 02 §3, docs/README §1 and the root README. The three permalinks resolve on the public repository at `c050d971` with the same blob ids, and the §3 heading slug exists (`receipts/history-permalinks.txt`) |
| #27 | links and diagrams valid | met | `make check` rc 0 at the head (`receipts/make_check_head.log`: links 1,152 OK; wavedrom 18 OK). F02.3, F02.4 and F02.7 renders viewed. The F01.2 note matches the export: both FIFO boxes sit inside the MAC domain boxes of `01-top-level.drawio` |
| #27 extra | 02 §7 `host_*`, §8 `nvm_dev_*` | met | as the first row; the §8 manager face is marked an internal seam |
| #70 | 1: a `make check` target fails on a P-/T- ID without a row | **met for every documented form except hyphenated braced members (F1)** | `make ids` = selftest + check. Probes (`receipts/ids_probes.log`): a stray in docs, in docs/history, in an RTL comment, in an untracked tb file, a deleted F01.5 row, a deleted F08.1 row, a missing family, a missing braced member, a missing heading, a missing F08.1 anchor, and the reverted `P-TX` comment all give rc 1; a git-ignored build file gives rc 0 by design. `T-NVM-{RS-DEADLINE, RS-TYPO}` gives rc 0 (F1) |
| #70 | planted control | met | 9-case `--selftest`; the head script on the base tree finds 39 uses of 3 undefined IDs (`P-MAAP-ACCEPT-CYC`, `P-MAAP-RSP-MS`, `P-TX`), as the PR body says (`receipts/ids_on_base.log`; rc 1 is the expected result) |
| #70 | 2: MAAP rows; 02 §4.2 no longer carries values | met (RESIDUE-1) | F01.5 rows match `KL_acmp_talker.sv:140/:180` (1024, 10,000), and neither is a top parameter. 02:300-301 and the derivation paragraph carry IDs only. The third stray, `P-EN-TALKER-DYN-MAPPINGS-RUNNING`, has 0 uses at base and head; `490e430^` still had one |
| #70 | 3: docs/README §2 = 09 §8 | met | both say `ids` + `params`, no gate reads values, and the value scan is still to add (09:398) |
| #70 | 4: target in the docs-gates job | met | `make check` in `hdl.yml`. The hosted docs-gates job at this head printed `ids selftest: 9 cases, OK` and `ids: 488 files … OK` (`receipts/hosted-docs-gates-pr-job-111475936324.log`) |
| #75 | 1: docs-gates runs lint (`make check`) | met | hosted log: `lint: 41 mermaid + 18 wavedrom blocks checked, OK` after `11.16.0` |
| #75 | 2: hand-authored SVG is a listed class with its rule | met | docs/README §3 bullet, the diagrams README inventory, `make figures` |
| #75 | 3: the five PNGs removed | met | none tracked. Restoring one fails `make figures` and `make check` (`receipts/fig_probes.log`, `receipts/mc_probes.log`) |
| #75 | `make figures` refuses unlisted files | met | probes: PNG, PNG in `src/`, unlisted SVG, subdirectory file, tracked dotfile all rc 1. The repo-ignored `.DS_Store` gives rc 0 by design |
| #75 | 4: 09 §7 matches CI | met for the target list (F2 concerns the self-test sentence) | the 09 §7 table and the Makefile `check` prerequisites are the same 9 targets. CI runs exactly `make check` after the two installs |
| #71 | 1: integrator §3 RX FIFO complete, FCS-good frames | met | integrator guide §3, anchor `rx-frame-atomic`; §1 points there |
| #71 | 3: REQ-REU-003 cells name the integrator | met | 00:531 Arch and Doc cells |
| #71 | rule 5 untouched | met | rule 5 text sha256 equal at base and head (`bd56ad1b…`) |
| scope | three code edits are comment-only | met | `verilator -E -P` (pinned 5.050) for the two `.sv` files, and `g++ -fpreprocessed -E -P` for `sim_main.cpp`: base = head. A second, independent comment-stripped token comparison is also equal (`receipts/comment_only.log`). Lint of both modules OK; `tb/tx_slots` 95/95; `tb/side_port` (real trace ring) 368/368 |
| scope | CI change sound | met (SUGGESTION-2) | Mermaid CLI pinned at 11.16.0 and installed with `--prefix`, with no global write. No network step beyond the two installs: the gates read no URL (`check-links.py` skips external links) |

## 3. Findings

Prior public findings: the internal reviewer's R472-1 report (https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/156#issuecomment-5982079701). I read it only after freezing my own verdict. Its F1, F2 and R1 are **retained** after independent reproduction. Its S1 to S3 are adopted as SUGGESTIONs below. No other review findings exist on this PR.

### F1: MINOR (Conformance, Robustness, Tests, Docs): `make ids` passes a braced list whose member is a hyphenated ID with no row (retains R472-1 F1)

- **Where:**
  - `scripts/check-ids.py:39`: `BRACES = re.compile(r"-\{([A-Z0-9, ]+)\}")` admits no `-` inside the braces.
  - `scripts/check-ids.py:103-104`: an unmatched `-{…}`, or any `-<lowercase>` continuation, falls through to the "family" branch, which any row under the stem satisfies.
- **Authority:** #70 acceptance 1 ("fails when a P- or T- ID used under docs/, hdl/ or tb/ has no row"). Also `docs/README.md:88-89` ("a braced list (`T-ACMP-{CMD, DELAY}`) a row for each member").
- **Evidence:** `receipts/prior_findings_probe.log`, from my reproduction in throw-away clones:
  - `T-NVM-{RS-DEADLINE, RS-TYPO}` appended to `08_timing.md` gives rc 0 and "OK", although `T-NVM-RS-TYPO` has no row;
  - the hyphen-free control `T-MRP-{JOIN, TYPO}` gives rc 1;
  - `the P-TX-shaped pool` (the issue's own stray with a prose suffix) gives rc 0.
  
  No use at the head has the hyphenated-member form, so the tree passes for the right reason today.
- **Impact:** the per-member guarantee the docs give for braced lists does not hold for multi-segment members. Multi-segment siblings are natural in this registry (`T-NVM-RS-DEADLINE` / `T-NVM-RS-AGGREGATE`), so a missing row can pass silently. That is the drift #70 exists to stop.
- **Required outcome:**
  - read a use as a family only in the documented forms (`-*`, and a hyphen at the end of a line);
  - parse braced members that contain hyphens, and check each member;
  - fail closed on any other `-{…}` or `-<text>` continuation, or parse it as an ID;
  - add self-test cases for a hyphenated braced member with no row and for an ID with a lowercase suffix.
- **Verification:** at the fixed head, the two rc-0 plants above must give rc 1, the control must keep rc 1, every probe in `receipts/ids_probes.log` must keep its rc, and `make check` must stay rc 0 on the tree.

### F2: MINOR (Tests, Docs): the figure gate's self-test does not plant three faults that 09 §7 says it plants (retains R472-1 F2)

- **Where:** `scripts/check-figures.py:173-189` (`SELFTEST_CASES`) against `docs/architecture/09_verification.md:125`. That row lists the `<svg>` root, `<image>`/`<foreignObject>` and the listed inventory, then states "The self-test plants each fault and must see it caught".
- **Evidence:** in `receipts/prior_findings_probe.log`, three mutants survive the script's own `--selftest` (rc 0):
  - the `<foreignObject>` check dropped;
  - the root-tag check dropped;
  - an empty hand-authored inventory accepted.
  
  `receipts/gate_mutants.txt` has the same kind of survivor (figures M12: a missing inventory section accepted). The production gate catches all of these on the real tree (rc 1 each), so only the regression guard that `make figures` runs first is short.
- **Impact:** 09 §7 states a verification property that does not hold. A later edit that drops any of those checks keeps `make check` and CI green. This is a test claim, not wording.
- **Required outcome:** add self-test cases for `<foreignObject>`, a non-SVG-namespace root, and a missing or empty hand-authored inventory. Alternatively, make 09 §7 name exactly the faults the self-test plants.
- **Verification:** rerun `scripts/prior_findings_probe.sh` and `scripts/gate_mutants.py`. The three F2 mutants and figures M12 must be KILLED, and `make figures` must stay rc 0 on the tree.

### RESIDUE-1 (Docs; wording only): F01.5 copies a derived timing value

- **Where:** `docs/architecture/01_overview.md:184`, the P-MAAP-RSP-MS cell: "each walk acquires after three `T-MAAP-PROBE` intervals, under 1,800 ms (Table B.8, …)".
- **Authority:** docs/README §2, "Timing values only in `F08.1`". The 1,800 ms is 3 × the `T-MAAP-PROBE` upper bound, moved here from 02 by this PR.
- **Exact fix:** delete ", under 1,800 ms", so the cell reads "each walk acquires after three `T-MAAP-PROBE` intervals (Table B.8, B.3.4.2, B.3.5.3)".

### RESIDUE-2 (Docs; wording only): two references still describe F02.7 by its old APB signals

- **Where and exact fixes:**
  - `tb/side_port/README.md:12`: replace "(F02.7 pready semantics)" with "(F02.7: each request held until its strobe)".
  - `hdl/packet_engine/KL_pp_side_port.sv:11-13` (a comment): replace "the class-E single-master port of F02.7 (psel/pwrite/paddr/pwdata/prdata/pready mapped 1:1 onto req_valid/we/addr/wdata/rdata/rvalid; wait states allowed)" with "the class-E single-master port of 02 §7 and F02.7 (an APB bridge maps psel/pwrite/paddr/pwdata/prdata/pready onto req_valid/we/addr/wdata/rdata/rvalid; wait states allowed)".
- **Why this is residue:** the meaning stays correct, because 02 §7 now carries the APB mapping in prose. Only the figure label is stale.

### RESIDUE-3 (PR body; wording only): the hosted-CI sentence is out of date

- **Where:** PR body, Validation section: "Hosted CI did not run: nothing was pushed."
- **Exact fix:** "Hosted CI at `91cef52`: docs-gates and portability pass in runs 37215798865 (push) and 37215802531 (pull_request); suites was still running when this was last updated." The manager should update this to the final state.

### RESIDUE-4 (Docs; wording only): rule 2's "no FIFO" contradicts 03 §2 (retains R472-1 R1)

- **Where:** `docs/architecture/02_interfaces.md:105`: "the top has one clock and no FIFO". 03 §2 (`03_packet_engine.md:31`) lists the top's per-engine dispatch FIFOs.
- **Exact fix:** "the top has one clock and no dual-clock FIFO".

### Suggestions (do not affect the verdict)

- **SUGGESTION-1 (Tests).** Harden the `ids` self-test. Of 13 mutants, 4 survive its `--selftest`: scan narrowed to `tb/` only, `hdl/` dropped, `docs/` dropped (M01-M03), and the master table read as the whole page (M11). An unreadable table returning rc 0 (M13) also survives (`receipts/gate_mutants.txt`). The production gate is right on each: the probes in `receipts/ids_probes.log` catch strays in docs, hdl and tb, and a missing heading or anchor. To cover these, plant one stray per scanned tree, a second table on the fixture page, and a missing heading. R472-1 S2 (duplicate rows, empty table) belongs here too.
- **SUGGESTION-2 (Robustness, CI; predates the PR in part).**
  - `pip install wavedrom` is unpinned, while `wavedrom-check` compares renders byte for byte. The hosted run resolved `2.0.3.post3`; pin `wavedrom==2.0.3.post3`.
  - `@mermaid-js/mermaid-cli@11.16.0` pins only the wrapper. Its `mermaid ^11.14.0` and `puppeteer ^23||^24||^25` float, because there is no lockfile. Locally this resolved mermaid 11.16.1 / puppeteer 25.6.0, while the registry's newest 11.x is 11.17.2. Pin `mermaid`, or commit a lockfile.
  - docs-gates checks out at depth 1, where `make stale` cannot fail. `receipts/stale_shallow_probe.log`: a source committed after its export gives rc 2 in a full clone and rc 0 in a depth-1 clone. Consider `fetch-depth: 0` for docs-gates. (R472-1 S1 overlaps.)
- **SUGGESTION-3 (Robustness).** These gate readings are lenient, and the fixed head should keep them deliberate:
  - "minus n" accepts any numeric tail on a defined stem (`P-TX-STD-SLOTS-7` gives rc 0), not just `-1`;
  - a line-broken family (`T-ADP-` then `NOPE` on the next line) gives rc 0 for any member;
  - `make figures` does not reject a raster inside `<feImage>` (rc 0).
  
  Document the first two in 09 §7, or narrow them, and consider adding `feImage` to the rejected elements.
- **SUGGESTION-4 (Docs).** F02.9's `mgmt` clock-domain cell ("own (sync or 4-phase async)") and F02.2's mgmt subgraph do not say that the landed `host_*` ports are in `clk_i`, with any bridge being the integrator's (integrator guide :48-49). This predates the PR.
- **SUGGESTION-5 (Docs).** The F00.2 GAP-14 resolution still reads "All figures Mermaid/WaveDrom/draw.io + lint", although hand-authored SVG is now a listed class. This predates the PR and is outside the #75 acceptance list.
- **SUGGESTION-6 (Docs; R472-1 S3).** `02_interfaces.md:623`: "held until `nvm_dev_gnt_i`" could read "held until `nvm_dev_gnt_i` or withdrawn at the deadline (below)".
- **Out of scope (R472-1 observation, acknowledged):** the integrator guide's short names `wr_done_i`/`wr_ready_i` predate the PR, in lines the PR does not touch.

## 4. Lens evidence

- **Conformance:**
  - every acceptance row in section 2;
  - the 02 tables and waveforms against the RTL. F02.7 timing matches `KL_pp_side_port` (write strobe at minimum latency, read with one wait state); F02.4 matches the TX shim, where `tx_ready_i` low holds the byte;
  - F01.5 MAAP rows against `KL_acmp_talker`;
  - `T-MAAP-PROBE`, `T-MAAP-ANNOUNCE`, `T-SRP-DAFRESH` and `T-BUDGET-ACMP-RESP` all exist in F08.1.
  
  UNCLEAN by F1 (#70 acceptance 1, braced members).
- **RTL:**
  - the three code edits are comment-only by two independent methods;
  - lint of `KL_pp_trace_ring` and `KL_pp_tx_slots` is OK;
  - the two suites that exercise them pass (95/95 and 368/368) with Verilator 5.050 (wrapper sha256 `905795b9…`, `--version` = 5.050 rev v5.050);
  - no behaviour change anywhere in `hdl/` or `tb/`.
  
  CLEAN.
- **Robustness:**
  - 14 `ids` probes and 16 `figures` probes, each in its own clone;
  - `make check` fails, at the right target, on a broken Mermaid block, a stray ID, a restored PNG and an un-rendered WaveDrom edit (rc 2 each, `receipts/mc_probes.log`);
  - the gates fail closed on missing tables, headings and inventory;
  - no network access in any gate.
  
  UNCLEAN by F1.
- **Tests:**
  - both self-tests pass (9 and 10 cases);
  - 25 gate mutants: 19 killed by the self-tests, 6 survived (`receipts/gate_mutants.txt`), plus 3 F2 mutants survived (`receipts/prior_findings_probe.log`);
  - the port-name probe has a planted control;
  - ids-on-base reproduces the 39 uses.
  
  UNCLEAN by F1 (no hyphenated-member case) and F2.
- **Docs:**
  - docs/README §1 to §3 and §6, 09 §7 and §8, the diagrams README, the history page, the root README, and the hdl-engineer guide's `make check` row;
  - the removed divergence row is correct, because 02 no longer diverges;
  - the three re-rendered WaveDrom figures were viewed.
  
  UNCLEAN by F1 (`docs/README.md:88-89` braced-list claim) and F2 (the 09 §7 self-test sentence). RESIDUE-1, -2 and -4 are recorded and do not affect the state.

## 5. Ledger (reviewer-owned)

| lens | state | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | 02 §1/§2/§3/§4.2/§7/§8 against `protocol_processor_top`, `KL_pp_side_port`, `KL_pp_nvm_port`, `KL_pp_trace_ring`, `KL_acmp_talker`; 01 F01.2 note and F01.5 rows; 03 §2/§8; 07 §5.5; integrator §1/§3; 00 REQ-REU-002/003, REQ-DOC-001; the acceptance of #27, #70, #71 (1, 3) and #75 | R473-1 | 91cef52b3c56cc69f66966b004782a69d2940a46 |
| RTL | CLEAN | `KL_pp_trace_ring.sv`, `KL_pp_tx_slots.sv`, `tb/tx_slots/sim_main.cpp` (preprocessed and token equality); lint of both modules; `tb/tx_slots` 95/95; `tb/side_port` 368/368 | R473-1 | 91cef52b3c56cc69f66966b004782a69d2940a46 |
| Robustness | UNCLEAN (F1) | `scripts/check-ids.py`, `scripts/check-figures.py`, Makefile `check`, `ids`, `figures`; `hdl.yml` docs-gates; 30 gate probes; 4 `make check` probes; the depth-1 `stale` probe | R473-1 | 91cef52b3c56cc69f66966b004782a69d2940a46 |
| Tests | UNCLEAN (F1, F2) | both self-tests; 25 + 3 gate mutants; the port-name probe with its planted control; ids on base | R473-1 | 91cef52b3c56cc69f66966b004782a69d2940a46 |
| Docs | UNCLEAN (F1, F2) | `docs/README.md`, `docs/architecture/09_verification.md`, `docs/diagrams/README.md`, `docs/history/02-class-a-word-stream.md`, `README.md`, `docs/guides/hdl-engineer.md`, `docs/guides/integrator.md`, 00 matrix rows, three WaveDrom renders | R473-1 | 91cef52b3c56cc69f66966b004782a69d2940a46 |

## 6. Commands and receipts

All commands ran in the foreground. Independent campaigns ran concurrently, each with its own log and rc file. `scripts/campaign.sh` (9 probes, 2 min wall time) wrote `receipts/campaign-summary.txt`:
- `make_check_head` 0;
- `ids_probes` 0;
- `fig_probes` 0;
- `mc_probes` 0;
- `comment_only` 0;
- `suite_tx_slots` 0;
- `suite_side_port` 0;
- `lint_touched` 0;
- `ids_on_base` 1 (expected: the base strays are found).

Other probes:
- `scripts/gate_mutants.py`: `receipts/gate_mutants.txt`;
- `scripts/port_names.py`: the three `receipts/port-names-*.txt` files;
- `scripts/stale_shallow_probe.sh`: `receipts/stale_shallow_probe.log`;
- `scripts/prior_findings_probe.sh`: `receipts/prior_findings_probe.log`.

Tool versions: `receipts/verilator-version.txt`, `receipts/mmdc-version.txt` (11.16.0), `receipts/wavedrom-version.txt` (2.0.3.post3; an existing read-only environment, put on `PYTHONPATH`; nothing was installed).

Hosted evidence: the docs-gates job log of pull_request run 37215802531 (merge ref `d00f87e` = head into `c050d971`) is `receipts/hosted-docs-gates-pr-job-111475936324.log`. Docs-gates and portability passed in both the push and the pull_request runs. Suites was still in progress when I read it, so I record no result for it.

## 7. Real limits

- I did not run the full processor bank (`run_suites.sh`, `lint_hdl.sh`), Yosys, the parent consumer set or the builder; the review rules exclude them. For those I rely on the executor's published handoff. My equivalent evidence is the comment-only proof and the focused suites. I found no manager bank receipts in the public evidence path. That path holds the executor's handoff and patches only.
- No hosted, act or Docker run. The hosted results above are read from GitHub, not executed by me. The suites job had not finished.
- The local Mermaid lint used mermaid 11.16.1 under CLI 11.16.0. Hosted CI resolves its own transitive versions (SUGGESTION-2), and they are not logged.
- Physical calibration NOT RUN; nothing here is hardware proof.

## 8. Pending manager duties

- Carry F1 and F2 back to the executor for a fixed head, and re-review there.
- Carry RESIDUE-1 to -4 to the residue checklist.
- Confirm the hosted suites job at the final head.
- Build and validate the current-dev candidate at the merge turn (live parent dev `fea346e76c2a57ed5cd131af8fc68dfeff57f877` with the adoption patches). Check `make ids` again after PR #154 or #155 merges.
- Update the PR body's hosted-CI sentence.
- Close #27, #70 and #75 only after merge. #71 stays open until the #81/#84 lane delivers acceptance 2.

R473-1 FINISHED
